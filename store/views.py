from django.shortcuts import render
from django.templatetags.static import static
from django.utils import timezone

from .models import Category, Product
from .utils import cutoff_label, countdown_text, next_cutoff

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
    }
    return render(request, "store/catalog.html", context)


def _placeholder(request, title, active_nav="none"):
    return render(
        request,
        "store/placeholder.html",
        {"page_title": title, "active_nav": active_nav},
    )


def product_detail(request, slug):
    return _placeholder(request, "Product")


def cart(request):
    return _placeholder(request, "Cart", active_nav="cart")


def my_orders(request):
    return _placeholder(request, "My Orders", active_nav="orders")


def account(request):
    return _placeholder(request, "Account")
