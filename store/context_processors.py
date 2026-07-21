from django.utils import timezone

from .utils import cutoff_label, countdown_text, next_cutoff


def order_window(request):
    """Cutoff countdown + cart count for the shared header/banner on every page."""
    now = timezone.localtime()
    cutoff = next_cutoff(now)
    cart = request.session.get("cart", {}) if hasattr(request, "session") else {}
    cart_count = sum(cart.values()) if isinstance(cart, dict) else 0
    return {
        "ow_cutoff_label": cutoff_label(cutoff),
        "ow_cutoff_ms": int(cutoff.timestamp() * 1000),
        "ow_countdown_text": countdown_text(cutoff, now, seconds=True),
        "cart_count": cart_count,
    }
