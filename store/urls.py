from django.urls import path

from . import views

app_name = "store"

urlpatterns = [
    path("", views.home, name="home"),
    path("catalog/", views.catalog, name="catalog"),
    path("product/<slug:slug>/", views.product_detail, name="product_detail"),
    path("cart/", views.cart, name="cart"),
    path("orders/", views.my_orders, name="my_orders"),
    path("account/", views.account, name="auth"),
]
