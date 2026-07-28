# User story 03: Add to and manage a cart

*As a customer, I want to add products to a cart and change quantities or remove items so that I
can review my order before paying.*

## Priority: P1 (highest) — Iteration 1

## Estimation: 1.5 days
Planning poker:
* Eti: 1 day
* Kei: 2 days
* **Agreed: 1.5 days** (session vs. DB cart discussed; session chosen for simplicity)

## Assumptions
* A guest (not logged in) can build a cart; it lives in the browser session.

## Description
Products can be added to a session cart from the product page or via quick-add on the catalog.
The cart page lists each line (photo, name, size, unit price, quantity ± controls, line total,
remove ×), shows a summary (items, pickup, subtotal) and a **Proceed to checkout** button. The
header shows a live item count.

## Tasks
1. Session cart helpers + `cart_add` view, 0.4 d
2. `cart` page: line items, subtotal summary, 0.5 d
3. `cart_update` view: increment / decrement / remove, 0.4 d
4. Header cart-count via a context processor, 0.2 d

## UI design
INO mock-up; realised at `http://147.93.56.126:8080/cart/`.

## Completed
✅ Iteration 1. Subtotal maths verified (e.g. 171.00 → 190.00 across quantity/remove changes).
