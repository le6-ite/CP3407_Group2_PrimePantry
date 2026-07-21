from django.contrib.staticfiles import finders
from django.db import models
from django.templatetags.static import static
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(max_length=90, unique=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "name"]
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f"{reverse('store:catalog')}?cat={self.slug}"


class Product(models.Model):
    WEIGHT = "weight"
    PIECE = "piece"
    UNIT_CHOICES = [(WEIGHT, "By weight"), (PIECE, "By piece / pack")]

    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="products"
    )
    name = models.CharField(max_length=160)
    slug = models.SlugField(max_length=170, unique=True)
    size_label = models.CharField(max_length=40, blank=True)
    unit = models.CharField(max_length=10, choices=UNIT_CHOICES, default=WEIGHT)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField(blank=True)
    image = models.CharField(
        max_length=120,
        blank=True,
        help_text="Filename inside static/store/assets/, e.g. prod-wagyu.png",
    )
    is_popular = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["category__order", "name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("store:product_detail", args=[self.slug])

    @property
    def image_url(self):
        # Resolve the first image that actually exists, so dropping a file named
        # "<slug>.webp" (or .jpg/.png) into static/store/assets/ makes it appear
        # with no code change. Optimised webp wins over the raw upload.
        candidates = [f"store/assets/{self.slug}.{ext}" for ext in ("webp", "jpg", "jpeg", "png")]
        if self.image:
            candidates.append(f"store/assets/{self.image}")
        for rel in candidates:
            if finders.find(rel):
                return static(rel)
        return static("store/assets/placeholder.png")

    @property
    def from_price(self):
        return self.price


class Order(models.Model):
    PENDING = "pending"
    PAID = "paid"
    CANCELLED = "cancelled"
    STATUS_CHOICES = [(PENDING, "Pending"), (PAID, "Paid"), (CANCELLED, "Cancelled")]

    PICKUP = "pickup"
    DELIVERY = "delivery"
    FULFILMENT_CHOICES = [(PICKUP, "Pickup"), (DELIVERY, "Delivery")]

    full_name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=40, blank=True)
    fulfilment = models.CharField(
        max_length=10, choices=FULFILMENT_CHOICES, default=PICKUP
    )
    address = models.CharField(max_length=255, blank=True)
    note = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    delivery_fee = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    round_cutoff = models.DateTimeField(null=True, blank=True)
    stripe_session_id = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.number

    @property
    def number(self):
        return f"PP-{self.pk:05d}" if self.pk else "PP-—"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, null=True, blank=True
    )
    name = models.CharField(max_length=200)
    size_label = models.CharField(max_length=40, blank=True)
    unit_price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} × {self.name}"

    @property
    def line_total(self):
        return self.unit_price * self.quantity
