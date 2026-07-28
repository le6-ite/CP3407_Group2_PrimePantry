# User story 02: View product details

*As a customer, I want to open a product to see its photo, price, size and description so that I
can decide whether to buy it.*

## Priority: P1 (highest) — Iteration 1

## Estimation: 1.0 day
Planning poker (all four members):
* Etigel: 1 · Kei: 1 · Samuel: 1 · Shane: 1
* **Agreed: 1.0 day**

## Assumptions
* Products carry a single price and a pack size (e.g. "500g"); no multi-variant pricing.

## Description
A product page shows a large photo, category breadcrumb, name, "Information" description, pack
size, price in AUD, a quantity stepper and an **Add to cart** button. A "You may also like"
row shows related products (same category first).

## Tasks
1. `product_detail` view: fetch product + related, 0.3 d
2. Template: hero image, info, size, price, quantity stepper (JS), 0.5 d
3. "You may also like" related grid, 0.2 d

## UI design
INO mock-up; realised at `http://147.93.56.126:8080/catalog/` → open any product.

## Completed
✅ Iteration 1. Favourite toggle added later for signed-in users (story 12).
