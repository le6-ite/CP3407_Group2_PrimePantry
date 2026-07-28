# Product backlog & user stories

This is the full product backlog for PrimePantry, prioritised and estimated **before
Iteration 1**. There are deliberately **more stories than fit into two iterations** so that
priority has to be exercised — the lowest-priority items sit in the *Not enough time* bucket.

**Priority** — `P1` = highest (must-have, build first), `P3` = lowest (nice-to-have).
**Estimate** — ideal developer-days, agreed by planning poker (see each detailed story for the
poker numbers). Estimators: **Eti** and **Samuel**.

Detailed stories live in [`user_stories/`](./user_stories/).

## Backlog (planned before Iteration 1)

| # | User story | Priority | Estimate (days) | Iteration |
|---|------------|:--------:|:---------------:|:---------:|
| 1 | [Browse products by category](./user_stories/user_story_01_browse_catalog.md) | P1 | 1.5 | 1 |
| 2 | [View product details](./user_stories/user_story_02_product_detail.md) | P1 | 1.0 | 1 |
| 3 | [Add to and manage a cart](./user_stories/user_story_03_cart.md) | P1 | 1.5 | 1 |
| 4 | [Weekly order window & cutoff](./user_stories/user_story_04_weekly_window.md) *(USP)* | P1 | 1.0 | 1 |
| 5 | Search products | P2 | 0.5 | 1 |
| 6 | [Register, log in & log out](./user_stories/user_story_05_register_login.md) | P1 | 1.5 | 2 |
| 7 | [Checkout & pay online (Stripe)](./user_stories/user_story_06_checkout_payment.md) | P1 | 2.5 | 2 |
| 8 | Order confirmation & my orders | P2 | 1.0 | 2 |
| 9 | Admin: manage products & orders | P1 | 1.0 | 2 |
| 10 | [Admin: total quantity ordered per product](./user_stories/user_story_07_admin_aggregate.md) *(USP)* | P1 | 1.5 | 2 |
| 11 | Save profile & delivery preferences | P2 | 1.5 | 2 |
| 12 | Favourites / wishlist | P3 | 1.0 | 2 |
| 13 | Reorder a past order | P3 | 0.5 | 2 |
| 14 | Export shopping list (CSV) | P3 | 0.5 | 2 |

**Total estimated (planned): 15.5 days.**

## Not enough time / future backlog

Prioritised but **not** scheduled into Iterations 1–2 (documented so priority is visible):

| # | User story | Priority | Estimate (days) |
|---|------------|:--------:|:---------------:|
| 15 | Real email order receipts (SMTP) | P3 | 1.0 |
| 16 | Delivery zones & distance-based pricing | P3 | 1.5 |
| 17 | Product ratings & reviews | P3 | 2.0 |
| 18 | Move to Postgres + HTTPS custom domain | P2 | 1.0 |

## Priority justification (summary)

- **P1** — the transaction core and the USP: without browse → product → cart → **pay**, and
  the **weekly window + admin quantity aggregate**, there is no viable product.
- **P2** — strongly improves the experience (search, order history, saved profiles) but the
  core works without them; scheduled once P1 is safe.
- **P3** — genuinely optional polish (favourites, reorder, CSV export); scheduled last, and
  the least valuable (reviews, delivery zones, email) were deferred entirely.

Priorities were re-checked at the start of each iteration; none changed after Iteration 1.
