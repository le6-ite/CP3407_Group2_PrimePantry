# Testing

PrimePantry is tested at two levels: **automated tests** (Django's test runner, run against a
throwaway database) and **acceptance testing** (manually exercising each user story, including
a real end-to-end Stripe test payment on the deployed site).

## How to run the automated tests

```bash
.venv/bin/python manage.py test store
```

```
Found 10 test(s).
..........
----------------------------------------------------------------------
Ran 10 tests in 0.7s
OK
```

The tests build a fresh SQLite test database, so they never touch development or production
data. They use Django's `TestCase` (each test runs in a transaction that is rolled back) and
the built-in test `Client` to drive real HTTP requests through the URL/view/template stack.

## Automated test coverage

`store/tests.py` — **10 tests** covering the accounts, cart, checkout and security behaviour:

| Test | What it verifies |
|------|------------------|
| `test_account_requires_login` | The account page redirects anonymous users to sign-in (access control). |
| `test_profile_can_be_saved` | A logged-in user can save profile details (name, phone, address, delivery preference). |
| `test_favorite_toggle_and_add_all_to_cart` | Adding/removing favourites works, and "add all favourites" fills the cart. |
| `test_quick_add_returns_to_filtered_catalog` | Quick-add from the catalog returns the user to the same filtered/searched view. |
| `test_reorder_adds_owned_order_items_to_cart` | "Reorder" copies a past order's items back into the cart. |
| `test_user_cannot_reorder_someone_elses_order` | A user **cannot** reorder another user's order (authorisation). |
| `test_checkout_is_prefilled_from_profile` | Checkout pre-fills name/email/phone/address from the saved profile. |
| `test_checkout_can_save_contact_details_to_profile` | The "save these details" option persists them to the profile. |
| `test_paid_confirmation_is_not_visible_to_another_session` | A paid order's confirmation is not exposed to a different browser session (privacy). |
| `test_external_next_url_is_not_used_after_login` | Open-redirect protection: an external `?next=` URL is ignored after login (security). |

The suite deliberately includes **security/authorisation** cases (cross-user reorder,
cross-session confirmation, open-redirect) as well as happy-path behaviour.

## Acceptance testing

Each user story was verified against its acceptance criteria on the deployed site
(http://147.93.56.126:8080/).

| # | User story | Acceptance check | Result |
|---|------------|------------------|:------:|
| 1 | Register / log in | Create an account with email + password, sign in, sign out | ✅ |
| 2 | Browse by category | Filter catalog by each of the 7 categories | ✅ |
| 3 | Search | Search "salmon" returns matches across categories | ✅ |
| 4 | Product detail | Correct photo, price, size, description, related items | ✅ |
| 5 | Cart | Add, change quantity, remove; subtotal recalculates | ✅ |
| 6 | **Checkout & pay** | Place order → Stripe test page → pay `4242…` → confirmation, cart cleared | ✅ (order **#PP-00016** on prod) |
| 7 | Weekly window | Countdown shows time to next Wed 18:00; order tagged to that window | ✅ |
| 8 | **Admin aggregate (USP)** | `/staff/quantities/` sums quantity per product for the window | ✅ |
| 9 | Export shopping list | CSV downloads with product, size, total qty, orders | ✅ |
| 10 | Manage products/orders | Django admin: edit products, advance order status | ✅ |
| 11 | My orders | Order history with live status badges | ✅ |
| 12 | Profile & favourites | Save details; favourite products; reorder | ✅ |

**End-to-end payment evidence.** A full test purchase was completed on the live VPS: the app
created a Stripe Checkout Session, the `4242 4242 4242 4242` test card was accepted, the
browser returned to the confirmation page (order **#PP-00016**), the cart was emptied, and the
order appears in Django admin and counts toward the current window's aggregate. The payment is
visible in the Stripe dashboard → Payments (test mode).

## Test data

- Product/category data: the reproducible fixture
  [`store/fixtures/catalog.json`](../store/fixtures/catalog.json) (7 categories, 42 products),
  loaded with `manage.py loaddata catalog`.
- Payments: Stripe **test cards** — success `4242 4242 4242 4242`; Stripe also documents
  decline cards for negative testing.

## What could be added next

- View-level tests for catalog filtering/search and the aggregate maths.
- A mocked-Stripe test of the `checkout_pay` → confirmation flow (the network call is
  currently exercised only through manual acceptance).
