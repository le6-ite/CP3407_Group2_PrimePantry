# User story 06: Checkout & pay online (Stripe)

*As a customer, I want to enter my details, choose pickup or delivery, and pay online so that my
order is confirmed for this week's window.*

## Priority: P1 (highest) — Iteration 2
The revenue moment; the highest-risk story (external payment integration), so estimated
generously.

## Estimation: 2.5 days
Planning poker:
* Eti: 2 days
* Kei: 3 days
* **Agreed: 2.5 days** (Stripe integration + order model + confirmation are unknowns)

## Assumptions
* **Stripe test mode** only — no real money; card entry happens on Stripe's hosted page, so we
  never handle card data (PCI-safe).
* Pickup is free; delivery adds a flat $8.

## Description
Checkout collects fulfilment (pickup/delivery), contact details and shows an order summary.
*Place order* creates a `pending` order, opens a **Stripe Checkout Session** and redirects to
Stripe. After paying with a test card, the customer returns to a confirmation page that verifies
payment, marks the order **Confirmed** and clears the cart.

## Tasks
1. `Order` / `OrderItem` models + admin, 0.5 d
2. Checkout page (fulfilment, contact, summary, live totals), 0.6 d
3. `checkout_pay`: create order + Stripe session, redirect, 0.7 d
4. `order_confirmation`: verify payment, finalise, confirmation page, 0.5 d
5. Error handling (payment could not start) + config, 0.2 d

## UI design
INO mock-ups for Checkout and Confirmation; realised at `http://147.93.56.126:8080/checkout/`.

## Completed
✅ Iteration 2, verified end-to-end **on the deployed site** (order **#PP-00016**, test card
`4242 4242 4242 4242`). Note: a production issue where the pasted Stripe key was mangled by the
terminal into non-ASCII characters was diagnosed and fixed (keys transferred via base64).
