from django.contrib import admin

from .models import Category, Product


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
