# Iteration 2 — Accounts, payment, the USP & deployment

**Dates:** 22 Jul 2026 → 28 Jul 2026
**Goal:** turn the storefront into a working shop — accounts, **online payment**, order history,
the **admin quantity aggregate (USP)**, and a deployed, containerised solution.

## Checklist
1. GitHub entry timestamps ✔ (see the [commit history](https://github.com/le6-ite/CP3407_Group2_PrimePantry/commits/main))
2. User stories are correct ✔ (see [backlog](./User_stories.md))

- **Assumed velocity from Iteration 1:** 5.5 → the team dedicated full time this iteration, so
  planned capacity was raised to ~11 ideal dev-days across the 2 developers.
- **Number of developers:** 2 (Eti, Kei)
- **Total estimated amount of work (committed):** 11.0 days

## User stories committed

| # | Story | Priority | Est. (days) | Owner |
|---|-------|:--------:|:-----------:|-------|
| 6 | [Register, log in & log out](./user_stories/user_story_05_register_login.md) | P1 | 1.5 | Eti |
| 7 | [Checkout & pay online (Stripe)](./user_stories/user_story_06_checkout_payment.md) | P1 | 2.5 | Eti |
| 8 | Order confirmation & my orders | P2 | 1.0 | Eti |
| 9 | Admin: manage products & orders | P1 | 1.0 | Eti |
| 10 | [Admin: total quantity ordered per product](./user_stories/user_story_07_admin_aggregate.md) *(USP)* | P1 | 1.5 | Eti |
| 11 | Save profile & delivery preferences | P2 | 1.5 | Kei |
| 12 | Favourites / wishlist | P3 | 1.0 | Kei |
| 13 | Reorder a past order | P3 | 0.5 | Kei |
| 14 | Export shopping list (CSV) | P3 | 0.5 | Eti |

**Total: 11.0 days.**

## In progress → Completed

- Checkout + Stripe Checkout (test) + confirmation — **completed 22 Jul (Eti)**
- `Order`/`OrderItem` models, order history, status badges — **completed 22 Jul (Eti)**
- Register/login (by email), auth-aware header — **completed 22–23 Jul (Eti)**
- Admin aggregate quantities (USP) + CSV export + order-status actions — **completed 23 Jul (Eti)**
- `CustomerProfile`: saved details, favourites, reorder + **10 automated tests** — **completed 22–23 Jul (Kei)**
- Containerised deployment to Hostinger VPS (Docker/Gunicorn) — **completed 23 Jul (Eti)**
- Merge of the two developers' branches (no conflicts) — **23 Jul**
- Production hardening: gunicorn workers, swap, Stripe key fix; end-to-end paid order **#PP-00016** — **completed 24 Jul (Eti)**

## Burn-down for Iteration 2

| Checkpoint (date) | Work remaining (days) |
|-------------------|:---------------------:|
| Start — 22 Jul | 11.0 |
| Checkout + payment done — 22 Jul | 7.0 |
| Auth + orders + admin USP — 23 Jul | 3.5 |
| Profile/favourites/reorder merged — 23 Jul | 1.0 |
| Deployed + payment verified in prod — 24 Jul | 0.0 |

- **Actual velocity:** ~11 ideal dev-days delivered (two developers working in parallel; the
  profile/favourites track ran alongside the payment track and merged cleanly).
- **Outcome:** all committed stories delivered and **deployed**. A real end-to-end Stripe test
  payment succeeded on the live site. Deferred (documented in the [backlog](./User_stories.md)):
  email receipts, delivery zones, reviews, Postgres/HTTPS.
