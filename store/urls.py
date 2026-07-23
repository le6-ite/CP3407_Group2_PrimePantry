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
    path("orders/<int:order_id>/reorder/", views.reorder, name="reorder"),
    path("account/", views.account, name="account"),
    path("account/sign-in/", views.login_register, name="auth"),
    path("account/favorites/", views.favorites, name="favorites"),
    path("account/favorites/add-all/", views.favorites_add_all, name="favorites_add_all"),
    path("product/<slug:slug>/favorite/", views.favorite_toggle, name="favorite_toggle"),
    path("logout/", views.logout_view, name="logout"),
    path("staff/quantities/", views.admin_quantities, name="admin_quantities"),
    path("staff/quantities/export/", views.export_shopping_list, name="admin_quantities_export"),
]
