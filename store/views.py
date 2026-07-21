from django.contrib.staticfiles import finders
from django.shortcuts import get_object_or_404, redirect, render
from django.templatetags.static import static
from django.utils import timezone

from .models import Category, Product
from .utils import cutoff_label, countdown_text, next_cutoff


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
    return _placeholder(request, "Cart", active_nav="cart")


def my_orders(request):
    return _placeholder(request, "My Orders", active_nav="orders")


def account(request):
    return _placeholder(request, "Account")
