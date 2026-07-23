import csv

import stripe
from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.staticfiles import finders
from django.db.models import Count, Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.templatetags.static import static
from django.urls import reverse
from django.utils import timezone

from .models import Category, Order, OrderItem, Product
from .utils import cutoff_label, countdown_text, next_cutoff

DELIVERY_FEE = 8


def _cart_lines(request):
    """Return (lines, subtotal) for the current session cart."""
    cart = request.session.get("cart", {})
    products = {
        p.id: p
        for p in Product.objects.filter(
            id__in=[int(k) for k in cart if k.isdigit()], is_active=True
        )
    }
    lines = []
    subtotal = 0
    for key, qty in cart.items():
        product = products.get(int(key)) if key.isdigit() else None
        if not product:
            continue
        line_total = product.price * qty
        subtotal += line_total
        lines.append({"product": product, "qty": qty, "line_total": line_total})
    return lines, subtotal


def _first_static(*names, default=None):
    """Return the URL of the first static file that exists."""
    for rel in names:
        if finders.find(rel):
            return static(rel)
    return static(default or names[-1])

FEATURED_COLLECTIONS = [
    ("premium-meat-game", "hero-medallions.png"),
    ("premium-seafood", "king-salmon-fillet-ora-king-nz-500g.webp"),
]


def home(request):
    now = timezone.localtime()
    cutoff = next_cutoff(now)

    collections = []
    for slug, image in FEATURED_COLLECTIONS:
        category = Category.objects.filter(slug=slug).first()
        if category:
            collections.append(
                {"category": category, "image_url": static(f"store/assets/{image}")}
            )

    context = {
        "popular_products": Product.objects.filter(is_active=True, is_popular=True)[:3],
        "collections": collections,
        "hero_primary_url": _first_static(
            "store/assets/hero-primary.webp",
            "store/assets/hero-primary.png",
            "store/assets/hero-primary.jpg",
            "store/assets/hero-ribs.png",
        ),
        "home_poster_url": _first_static(
            "store/assets/hero-video-poster.webp",
            "store/assets/hero-video-poster.png",
            "store/assets/hero-video-poster.jpg",
            "store/assets/hero-medallions.png",
        ),
        "cutoff_label": cutoff_label(cutoff),
        "cutoff_ms": int(cutoff.timestamp() * 1000),
        "countdown_text": countdown_text(cutoff, now),
    }
    return render(request, "store/home.html", context)


def catalog(request):
    q = request.GET.get("q", "").strip()
    active_cat = request.GET.get("cat", "").strip()

    categories = list(Category.objects.all())
    products = Product.objects.filter(is_active=True).select_related("category")
    if q:
        products = products.filter(name__icontains=q)
    if active_cat:
        products = products.filter(category__slug=active_cat)
    products = list(products)

    sections = []
    for category in categories:
        if active_cat and category.slug != active_cat:
            continue
        items = [p for p in products if p.category_id == category.id]
        if items:
            sections.append(
                {
                    "category": category,
                    "products": items,
                    "number": f"{len(sections) + 1:02d}",
                }
            )

    context = {
        "q": q,
        "active_cat": active_cat,
        "categories": categories,
        "sections": sections,
        "result_count": len(products),
        "active_nav": "catalog",
        "catalog_banner_url": _first_static(
            "store/assets/catalog-banner.webp",
            "store/assets/catalog-banner.png",
            "store/assets/catalog-banner.jpg",
            "store/assets/hero-medallions.png",
        ),
    }
    return render(request, "store/catalog.html", context)


def _placeholder(request, title, active_nav="none"):
    return render(
        request,
        "store/placeholder.html",
        {"page_title": title, "active_nav": active_nav},
    )


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)

    related = list(
        Product.objects.filter(is_active=True, category=product.category)
        .exclude(id=product.id)[:3]
    )
    if len(related) < 3:
        fillers = (
            Product.objects.filter(is_active=True)
            .exclude(id=product.id)
            .exclude(category=product.category)[: 3 - len(related)]
        )
        related += list(fillers)

    context = {
        "product": product,
        "related": related,
        "price_label": "Price per weight" if product.unit == "weight" else "Price per pack",
        "added": request.GET.get("added") == "1",
        "active_nav": "catalog",
    }
    return render(request, "store/product_detail.html", context)


def cart_add(request):
    if request.method != "POST":
        return redirect("store:catalog")
    product = Product.objects.filter(
        slug=request.POST.get("slug"), is_active=True
    ).first()
    if not product:
        return redirect("store:catalog")
    try:
        qty = max(1, int(request.POST.get("qty", 1)))
    except (TypeError, ValueError):
        qty = 1
    cart = request.session.get("cart", {})
    key = str(product.id)
    cart[key] = cart.get(key, 0) + qty
    request.session["cart"] = cart
    request.session.modified = True
    return redirect(f"{product.get_absolute_url()}?added=1")


def cart(request):
    lines, subtotal = _cart_lines(request)
    context = {
        "lines": lines,
        "subtotal": subtotal,
        "item_count": sum(l["qty"] for l in lines),
        "active_nav": "cart",
    }
    return render(request, "store/cart.html", context)


def cart_update(request):
    if request.method != "POST":
        return redirect("store:cart")
    product = Product.objects.filter(slug=request.POST.get("slug")).first()
    action = request.POST.get("action")
    cart = request.session.get("cart", {})
    if product and str(product.id) in cart:
        key = str(product.id)
        if action == "inc":
            cart[key] += 1
        elif action == "dec":
            cart[key] = max(1, cart[key] - 1)
        elif action == "remove":
            del cart[key]
        request.session["cart"] = cart
        request.session.modified = True
    return redirect("store:cart")


def checkout(request):
    lines, subtotal = _cart_lines(request)
    if not lines:
        return redirect("store:cart")
    form = request.session.pop("checkout_form", {})
    if not form and request.user.is_authenticated:
        form = {"full_name": request.user.first_name, "email": request.user.email}
    context = {
        "lines": lines,
        "subtotal": subtotal,
        "delivery_fee": DELIVERY_FEE,
        "form": form,
        "error": request.session.pop("checkout_error", ""),
        "active_nav": "cart",
    }
    return render(request, "store/checkout.html", context)


def checkout_pay(request):
    if request.method != "POST":
        return redirect("store:checkout")
    lines, subtotal = _cart_lines(request)
    if not lines:
        return redirect("store:cart")

    full_name = request.POST.get("full_name", "").strip()
    email = request.POST.get("email", "").strip()
    phone = request.POST.get("phone", "").strip()
    fulfilment = request.POST.get("fulfilment", Order.PICKUP)
    address = request.POST.get("address", "").strip()
    note = request.POST.get("note", "").strip()

    if not full_name or not email:
        request.session["checkout_form"] = {
            "full_name": full_name, "email": email, "phone": phone,
            "fulfilment": fulfilment, "address": address, "note": note,
        }
        request.session["checkout_error"] = "Please enter your name and email."
        return redirect("store:checkout")

    delivery_fee = DELIVERY_FEE if fulfilment == Order.DELIVERY else 0
    total = subtotal + delivery_fee

    order = Order.objects.create(
        user=request.user if request.user.is_authenticated else None,
        full_name=full_name, email=email, phone=phone, fulfilment=fulfilment,
        address=address, note=note, subtotal=subtotal, delivery_fee=delivery_fee,
        total=total, round_cutoff=next_cutoff(),
    )
    for line in lines:
        product = line["product"]
        OrderItem.objects.create(
            order=order, product=product, name=product.name,
            size_label=product.size_label, unit_price=product.price,
            quantity=line["qty"],
        )

    # Track the order in the session so guests can see it under "My orders".
    session_orders = request.session.get("orders", [])
    session_orders.append(order.pk)
    request.session["orders"] = session_orders
    request.session.modified = True

    # Without Stripe keys, fall back to a mock "paid" so the flow still works.
    if not settings.STRIPE_SECRET_KEY:
        order.status = Order.PAID
        order.save(update_fields=["status"])
        request.session["cart"] = {}
        request.session.modified = True
        return redirect(f"{reverse('store:order_confirmation')}?order={order.pk}")

    stripe.api_key = settings.STRIPE_SECRET_KEY
    stripe_lines = []
    for line in lines:
        product = line["product"]
        label = product.name
        if product.size_label:
            label = f"{product.name} ({product.size_label})"
        stripe_lines.append({
            "price_data": {
                "currency": "aud",
                "product_data": {"name": label},
                "unit_amount": int(product.price * 100),
            },
            "quantity": line["qty"],
        })
    if delivery_fee:
        stripe_lines.append({
            "price_data": {
                "currency": "aud",
                "product_data": {"name": "Delivery"},
                "unit_amount": int(delivery_fee * 100),
            },
            "quantity": 1,
        })

    session = stripe.checkout.Session.create(
        mode="payment",
        line_items=stripe_lines,
        customer_email=email,
        success_url=request.build_absolute_uri(reverse("store:order_confirmation"))
        + "?session_id={CHECKOUT_SESSION_ID}",
        cancel_url=request.build_absolute_uri(reverse("store:checkout")),
        metadata={"order_id": str(order.pk)},
    )
    order.stripe_session_id = session.id
    order.save(update_fields=["stripe_session_id"])
    return redirect(session.url, code=303)


def order_confirmation(request):
    session_id = request.GET.get("session_id")
    order = None

    if session_id and settings.STRIPE_SECRET_KEY:
        stripe.api_key = settings.STRIPE_SECRET_KEY
        order = Order.objects.filter(stripe_session_id=session_id).first()
        try:
            session = stripe.checkout.Session.retrieve(session_id)
        except Exception:
            session = None
        if order and session and session.payment_status == "paid":
            if order.status != Order.PAID:
                order.status = Order.PAID
                order.save(update_fields=["status"])
                request.session["cart"] = {}
                request.session.modified = True
        elif order and order.status != Order.PAID:
            return redirect("store:cart")
    else:
        order = Order.objects.filter(
            pk=request.GET.get("order"), status=Order.PAID
        ).first()

    if not order or order.status != Order.PAID:
        return redirect("store:catalog")
    return render(request, "store/confirmation.html", {"order": order, "active_nav": "cart"})


def my_orders(request):
    if request.user.is_authenticated:
        orders = Order.objects.filter(user=request.user)
    else:
        orders = Order.objects.filter(id__in=request.session.get("orders", []))
    context = {"orders": orders.prefetch_related("items"), "active_nav": "orders"}
    return render(request, "store/my_orders.html", context)


def login_register(request):
    if request.user.is_authenticated and request.method == "GET":
        return redirect("store:my_orders")
    next_url = request.GET.get("next") or request.POST.get("next") or ""
    mode = request.GET.get("mode", "login")
    error = ""
    values = {}
    if request.method == "POST":
        action = request.POST.get("action", "login")
        mode = "register" if action == "register" else "login"
        email = request.POST.get("email", "").strip().lower()
        password = request.POST.get("password", "")
        values = {"email": email, "full_name": request.POST.get("full_name", "").strip()}
        if action == "register":
            if not email or not password:
                error = "Email and password are required."
            elif password != request.POST.get("confirm", ""):
                error = "Passwords do not match."
            elif len(password) < 6:
                error = "Password must be at least 6 characters."
            elif User.objects.filter(username=email).exists():
                error = "An account with this email already exists."
            else:
                user = User.objects.create_user(
                    username=email, email=email, password=password
                )
                if values["full_name"]:
                    user.first_name = values["full_name"][:150]
                    user.save(update_fields=["first_name"])
                login(request, user)
                return redirect(next_url or "store:my_orders")
        else:
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect(next_url or "store:my_orders")
            error = "Invalid email or password."
    context = {
        "mode": mode, "error": error, "values": values,
        "next": next_url, "active_nav": "none",
    }
    return render(request, "store/auth.html", context)


def logout_view(request):
    logout(request)
    return redirect("store:home")


COUNTED_STATUSES = [Order.PAID, Order.PACKING, Order.READY, Order.COMPLETED]


def _window_aggregate(cutoff):
    """Per-product totals for a window's confirmed orders, biggest first."""
    return list(
        OrderItem.objects.filter(
            order__round_cutoff=cutoff,
            order__status__in=COUNTED_STATUSES,
            product__isnull=False,
        )
        .values(
            "product_id", "product__name", "product__size_label",
            "product__category__name",
        )
        .annotate(total_qty=Sum("quantity"), order_count=Count("order", distinct=True))
        .order_by("-total_qty")
    )


@staff_member_required
def admin_quantities(request):
    cutoff = next_cutoff()
    agg = _window_aggregate(cutoff)
    products = {
        p.id: p for p in Product.objects.filter(id__in=[r["product_id"] for r in agg])
    }
    max_qty = max((r["total_qty"] for r in agg), default=1) or 1
    rows = []
    for r in agg:
        product = products.get(r["product_id"])
        rows.append({
            "name": r["product__name"],
            "category": r["product__category__name"] or "—",
            "qty": r["total_qty"],
            "size_label": r["product__size_label"] or "pack",
            "orders": r["order_count"],
            "bar_pct": round(r["total_qty"] / max_qty * 100),
            "image_url": product.image_url if product else static("store/assets/placeholder.png"),
        })
    context = {
        "rows": rows,
        "cutoff": cutoff,
        "total_orders": Order.objects.filter(
            round_cutoff=cutoff, status__in=COUNTED_STATUSES
        ).count(),
    }
    return render(request, "store/admin_quantities.html", context)


@staff_member_required
def export_shopping_list(request):
    cutoff = next_cutoff()
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = (
        f'attachment; filename="shopping-list-{cutoff:%Y-%m-%d}.csv"'
    )
    writer = csv.writer(response)
    writer.writerow(["Product", "Category", "Size", "Total quantity", "Orders"])
    for r in _window_aggregate(cutoff):
        writer.writerow([
            r["product__name"],
            r["product__category__name"] or "",
            r["product__size_label"] or "",
            r["total_qty"],
            r["order_count"],
        ])
    return response
