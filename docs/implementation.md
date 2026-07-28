# Implementation summary

The delivered, deployed solution. Live at **http://147.93.56.126:8080/**; source in this
repository (Django app in the `store` app).

## Delivered features

### Customer storefront
- **Home** — full-viewport hero, live weekly-cutoff countdown, "popular this week", "shop by
  collection", looping background video.
- **Catalog** — all 42 products grouped by 7 categories, **server-side search** and
  **category filter**, quick-add to cart.
- **Product detail** — photo, price, pack size, description, quantity stepper, add-to-cart,
  favourite toggle, "you may also like".
- **Cart** — session cart: add, change quantity, remove, live subtotal.
- **Checkout** — pickup (free) or delivery ($8), contact details, order summary, and
  **online payment via Stripe Checkout (test mode)**.
- **Confirmation** — order number, group-buying pickup message, cart cleared on success.

### Accounts
- **Register / log in / log out** (login by email).
- **My orders** — history with live status badges (Confirmed → Packing → Ready → Completed);
  **reorder** a past order.
- **Profile** — save contact & delivery preferences; checkout pre-fills from them.
- **Favourites** — wishlist of products; "add all favourites to cart".

### Group-buying model (the USP)
- **Weekly order window** — a shared cutoff (next Wednesday 18:00, Australia/Brisbane) shown
  as a live countdown across the site; every order is tagged to its window.
- **Admin aggregate quantities** — `/staff/quantities/` sums the total quantity ordered per
  product for the current window, with order counts and bars (solves *Problem 04*: no manual
  tallying).
- **Export shopping list** — one-click CSV of the aggregate for sourcing.

### Service-provider tools
- **Django admin** — manage products, categories and orders; inline order items; **inline
  status editing** and **bulk actions** (mark Packing / Ready / Completed).

## Mapping to the original product backlog

| Backlog item (from the pitch) | Status |
|-------------------------------|:------:|
| Register account · Log in | ✅ |
| Product categories · Browse products | ✅ |
| Product information | ✅ |
| Add to cart · Place an order | ✅ |
| Pay online | ✅ (Stripe test) |
| Product search | ✅ |
| Admin can manage products | ✅ (Django admin) |
| Weekly order cutoff system | ✅ |
| View total quantity ordered for each product | ✅ (+ CSV export) |

Additional value delivered beyond the pitch: saved profiles, favourites, reorder, order status
lifecycle, and full containerised deployment.

## Deployment
Containerised and deployed on a Hostinger VPS — see [DEPLOY.md](../DEPLOY.md). Updates ship with
`git pull && docker compose up -d --build`.
