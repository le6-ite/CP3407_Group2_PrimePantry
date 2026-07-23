from django.contrib import admin

from .models import Category, Order, OrderItem, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "order")
    list_editable = ("order",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "size_label", "price", "is_popular", "is_active")
    list_filter = ("category", "is_popular", "is_active", "unit")
    list_editable = ("price", "is_popular", "is_active")
    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("product", "name", "size_label", "unit_price", "quantity")
    can_delete = False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("number", "full_name", "status", "fulfilment", "total", "created_at")
    list_editable = ("status",)
    list_filter = ("status", "fulfilment", "round_cutoff")
    search_fields = ("full_name", "email", "stripe_session_id")
    readonly_fields = ("stripe_session_id", "created_at", "subtotal", "total")
    inlines = [OrderItemInline]
    actions = ["mark_packing", "mark_ready", "mark_completed"]

    @admin.display(description="Order")
    def number(self, obj):
        return obj.number

    @admin.action(description="Mark selected as Packing")
    def mark_packing(self, request, queryset):
        n = queryset.update(status=Order.PACKING)
        self.message_user(request, f"{n} order(s) marked as Packing.")

    @admin.action(description="Mark selected as Ready for pickup")
    def mark_ready(self, request, queryset):
        n = queryset.update(status=Order.READY)
        self.message_user(request, f"{n} order(s) marked as Ready for pickup.")

    @admin.action(description="Mark selected as Completed")
    def mark_completed(self, request, queryset):
        n = queryset.update(status=Order.COMPLETED)
        self.message_user(request, f"{n} order(s) marked as Completed.")
