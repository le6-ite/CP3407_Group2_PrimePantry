from decimal import Decimal

from django.contrib.auth.models import User
from django.contrib.sessions.middleware import SessionMiddleware
from django.http import Http404
from django.test import RequestFactory, TestCase, override_settings
from django.urls import reverse

from . import views
from .models import Category, CustomerProfile, Order, OrderItem, Product


class AccountFeatureTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="sam@example.com",
            email="sam@example.com",
            password="test-password-123",
            first_name="Sam Example",
        )
        self.profile = CustomerProfile.objects.create(user=self.user)
        self.category = Category.objects.create(
            name="Meat", slug="meat", order=1
        )
        self.product = Product.objects.create(
            category=self.category,
            name="Rump Steak",
            slug="rump-steak",
            size_label="500g",
            unit=Product.WEIGHT,
            price=Decimal("18.50"),
        )
        self.second_product = Product.objects.create(
            category=self.category,
            name="Beef Sausages",
            slug="beef-sausages",
            size_label="6 pack",
            unit=Product.PIECE,
            price=Decimal("12.00"),
        )

    def request(self, method, path, data=None):
        factory = RequestFactory()
        request = getattr(factory, method)(path, data=data or {})
        SessionMiddleware(lambda req: None).process_request(request)
        request.session.save()
        request.user = self.user
        return request

    def test_account_requires_login(self):
        response = self.client.get(reverse("store:account"))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.url,
            f"{reverse('store:auth')}?next={reverse('store:account')}",
        )

    def test_profile_can_be_saved(self):
        request = self.request(
            "post",
            reverse("store:account"),
            {
                "full_name": "Sam Supplier",
                "email": "supplier@example.com",
                "phone": "0400 000 000",
                "address": "12 Market St, Brisbane QLD 4000",
                "preferred_fulfilment": CustomerProfile.DELIVERY,
            },
        )
        response = views.account(request)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Profile saved.")
        self.user.refresh_from_db()
        self.profile.refresh_from_db()
        self.assertEqual(self.user.first_name, "Sam Supplier")
        self.assertEqual(self.user.username, "supplier@example.com")
        self.assertEqual(self.profile.phone, "0400 000 000")
        self.assertEqual(self.profile.preferred_fulfilment, CustomerProfile.DELIVERY)

    def test_favorite_toggle_and_add_all_to_cart(self):
        self.client.force_login(self.user)
        self.client.post(reverse("store:favorite_toggle", args=[self.product.slug]))
        self.assertTrue(self.profile.favorite_products.filter(pk=self.product.pk).exists())

        response = self.client.post(reverse("store:favorites_add_all"))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("store:cart"))
        self.assertEqual(self.client.session["cart"], {str(self.product.pk): 1})

        self.client.post(reverse("store:favorite_toggle", args=[self.product.slug]))
        self.assertFalse(self.profile.favorite_products.filter(pk=self.product.pk).exists())

    def test_quick_add_returns_to_filtered_catalog(self):
        return_url = f"{reverse('store:catalog')}?cat={self.category.slug}"

        response = self.client.post(
            reverse("store:cart_add"),
            {"slug": self.product.slug, "qty": "1", "next": return_url},
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, return_url)
        self.assertEqual(self.client.session["cart"], {str(self.product.pk): 1})
        self.assertEqual(
            self.client.session["shop_notice"],
            f"{self.product.name} added to your cart.",
        )

    def test_reorder_adds_owned_order_items_to_cart(self):
        self.client.force_login(self.user)
        order = Order.objects.create(
            user=self.user,
            full_name="Sam Example",
            email="sam@example.com",
            subtotal=Decimal("37.00"),
            total=Decimal("37.00"),
            status=Order.PAID,
        )
        OrderItem.objects.create(
            order=order,
            product=self.product,
            name=self.product.name,
            size_label=self.product.size_label,
            unit_price=self.product.price,
            quantity=2,
        )

        response = self.client.post(reverse("store:reorder", args=[order.pk]))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("store:cart"))
        self.assertEqual(self.client.session["cart"], {str(self.product.pk): 2})

    def test_user_cannot_reorder_someone_elses_order(self):
        other = User.objects.create_user("other@example.com", password="password")
        order = Order.objects.create(
            user=other,
            full_name="Other User",
            email="other@example.com",
            total=Decimal("12.00"),
        )
        request = self.request(
            "post", reverse("store:reorder", args=[order.pk])
        )

        with self.assertRaises(Http404):
            views.reorder(request, order.pk)

    def test_checkout_is_prefilled_from_profile(self):
        self.profile.phone = "0400 111 222"
        self.profile.address = "44 Queen St, Brisbane QLD 4000"
        self.profile.preferred_fulfilment = CustomerProfile.DELIVERY
        self.profile.save()
        request = self.request("get", reverse("store:checkout"))
        request.session["cart"] = {str(self.product.pk): 1}

        response = views.checkout(request)

        self.assertContains(response, "0400 111 222")
        self.assertContains(response, "44 Queen St, Brisbane QLD 4000")
        self.assertContains(response, 'value="delivery" checked')

    @override_settings(STRIPE_SECRET_KEY="")
    def test_checkout_can_save_contact_details_to_profile(self):
        self.client.force_login(self.user)
        session = self.client.session
        session["cart"] = {str(self.product.pk): 1}
        session.save()

        response = self.client.post(
            reverse("store:checkout_pay"),
            {
                "full_name": "Updated Name",
                "email": self.user.email,
                "phone": "0400 333 444",
                "fulfilment": Order.DELIVERY,
                "address": "88 River Rd, Brisbane QLD 4000",
                "save_profile": "1",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.profile.refresh_from_db()
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, "Updated Name")
        self.assertEqual(self.profile.phone, "0400 333 444")
        self.assertEqual(self.profile.address, "88 River Rd, Brisbane QLD 4000")
        self.assertEqual(self.profile.preferred_fulfilment, CustomerProfile.DELIVERY)

    def test_paid_confirmation_is_not_visible_to_another_session(self):
        order = Order.objects.create(
            user=self.user,
            full_name="Sam Example",
            email="sam@example.com",
            status=Order.PAID,
            total=Decimal("18.50"),
        )

        response = self.client.get(
            reverse("store:order_confirmation"), {"order": order.pk}
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("store:catalog"))

    def test_external_next_url_is_not_used_after_login(self):
        response = self.client.post(
            f"{reverse('store:auth')}?next=https://example.net/phishing",
            {"action": "login", "email": self.user.email, "password": "test-password-123"},
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("store:account"))
