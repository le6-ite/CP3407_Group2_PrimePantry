import logging

from django.core.mail import send_mail

from .utils import cutoff_label

logger = logging.getLogger(__name__)


def send_order_confirmation(order):
    """Email the customer a receipt for a paid order.

    Failures are logged, never raised — a mail outage must not break checkout.
    """
    lines = [
        f"Hi {order.full_name},",
        "",
        f"Thanks for your order! We've received order {order.number} and it is confirmed.",
        "",
        "Your items:",
    ]
    for item in order.items.all():
        label = item.name
        if item.size_label:
            label = f"{item.name} ({item.size_label})"
        lines.append(f"  {item.quantity} x {label} — ${item.line_total:.2f}")
    lines.append("")
    lines.append(f"Subtotal: ${order.subtotal:.2f}")
    if order.delivery_fee:
        lines.append(f"Delivery: ${order.delivery_fee:.2f}")
    lines.append(f"Total: ${order.total:.2f}")
    lines.append("")
    if order.fulfilment == order.DELIVERY:
        lines.append(f"Delivery to: {order.address}")
    else:
        lines.append("Fulfilment: pickup")
    if order.round_cutoff:
        lines.append(
            "Your order is part of this week's group buy — the ordering window "
            f"closes {cutoff_label(order.round_cutoff)}, after which we source "
            "everything fresh against actual demand."
        )
    lines.append("")
    lines.append("PrimePantry — premium ingredients, group-buying prices.")

    try:
        send_mail(
            subject=f"PrimePantry order {order.number} confirmed",
            message="\n".join(lines),
            from_email=None,  # DEFAULT_FROM_EMAIL
            recipient_list=[order.email],
        )
    except Exception:
        logger.exception("Order confirmation email failed for order %s", order.pk)
