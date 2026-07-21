from django.urls import path

from . import views

app_name = "store"

urlpatterns = [
    path("", views.home, name="home"),
    path("catalog/", views.catalog, name="catalog"),
    path("product/<slug:slug>/", views.product_detail, name="product_detail"),
    path("cart/add/", views.cart_add, name="cart_add"),
    path("cart/update/", views.cart_update, name="cart_update"),
    path("cart/", views.cart, name="cart"),
    path("checkout/", views.checkout, name="checkout"),
    path("checkout/pay/", views.checkout_pay, name="checkout_pay"),
    path("order/confirmation/", views.order_confirmation, name="order_confirmation"),
    path("orders/", views.my_orders, name="my_orders"),
    path("account/", views.account, name="auth"),
]
