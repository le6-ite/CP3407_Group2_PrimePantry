# User story 07: Admin — total quantity ordered per product (USP)

*As the service provider, I want to see the total quantity ordered for each product this week so
that I know exactly how much to source — without tallying orders by hand.*

## Priority: P1 (highest) — Iteration 2 · **Unique selling point**
Directly solves *Problem 04* from the pitch (manual tallying is slow and error-prone) and is the
core operational payoff of the group-buying model.

## Estimation: 1.5 days
Planning poker:
* Eti: 1 day
* Kei: 2 days
* **Agreed: 1.5 days** (aggregation query + staff-only page + export)

## Assumptions
* Only confirmed orders (paid / packing / ready / completed) count.
* Aggregation is for the **current** weekly window.

## Description
A staff-only page (`/staff/quantities/`) lists, for the current window, each product with its
**total quantity ordered**, the number of orders, and a proportional bar — biggest first. A
one-click **Export shopping list** downloads the same data as CSV for sourcing.

## Tasks
1. Aggregation query (`Sum`/`Count`, grouped by product), 0.5 d
2. `@staff_member_required` page + INO admin layout, 0.6 d
3. CSV export view + button, 0.4 d

## UI design
INO admin mock-up; realised at `http://147.93.56.126:8080/staff/quantities/` (staff login).

## Completed
✅ Iteration 2. Verified with seeded confirmed orders (e.g. King Salmon 3 × 500g, Wagyu 2 × 300g);
CSV export confirmed. Order-status management (Packing/Ready/Completed) added to Django admin.
