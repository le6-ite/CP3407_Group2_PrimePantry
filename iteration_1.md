# Iteration 1 — Foundation & storefront

**Dates:** 14 Jul 2026 (planning) → 21 Jul 2026 (delivered)
**Goal:** a browsable storefront with the group-buying window — everything a customer needs up
to (but not including) payment.

> **Documentation owner:** Shane Ross (Agile / iteration boards & burn-down).

> Note on duration: the rubric assumes 3–4 week iterations over a trimester. This project ran on
> a compressed schedule, so each iteration is ~1 week; the dates below are the real GitHub
> timeline. All planning entries are timestamped **before** Iteration 1 work began.

## Checklist
1. GitHub entry timestamps ✔ (see the [commit history](https://github.com/le6-ite/CP3407_Group2_PrimePantry/commits/main))
2. User stories are correct ✔ (see [backlog](./User_stories.md))

- **Implementation:** Etigel · **Requirements, design & planning:** whole team (Etigel, Kei, Samuel, Shane)
- **Assumed velocity (first iteration, estimated):** ~6 ideal dev-days
- **Total estimated amount of work (committed):** 5.5 days

## User stories committed

| # | Story | Priority | Est. (days) | Owner |
|---|-------|:--------:|:-----------:|-------|
| 1 | [Browse products by category](./user_stories/user_story_01_browse_catalog.md) | P1 | 1.5 | Etigel |
| 2 | [View product details](./user_stories/user_story_02_product_detail.md) | P1 | 1.0 | Etigel |
| 3 | [Add to and manage a cart](./user_stories/user_story_03_cart.md) | P1 | 1.5 | Etigel |
| 4 | [Weekly order window & cutoff](./user_stories/user_story_04_weekly_window.md) *(USP)* | P1 | 1.0 | Etigel |
| 5 | Search products | P2 | 0.5 | Etigel |

**Total: 5.5 days.**

## In progress → Completed

- Django project + `store` app, models `Category`/`Product`, admin — **completed 21 Jul (Etigel)**
- Catalog fixture (7 categories, 42 products) — **completed 21 Jul (Etigel)**
- Home (INO) + live cutoff countdown — **completed 21 Jul (Etigel)**
- Catalog with search + category filter — **completed 21 Jul (Etigel)**
- Product detail + session cart — **completed 21 Jul (Etigel)**
- Reusable header/banner/footer shell + context processor — **completed 21 Jul (Etigel)**

## Burn-down for Iteration 1

| Checkpoint | Work remaining (days) |
|-----------|:---------------------:|
| Start (planning done) | 5.5 |
| Catalog + product live | 3.0 |
| Cart working | 1.5 |
| Search + window done | 0.0 |

- **Actual velocity:** 5.5 ideal dev-days delivered.
- **Outcome:** all committed stories delivered; scope matched the plan. Estimates were slightly
  conservative (the team's higher estimates), so the team pulled the payment epic forward into
  Iteration 2 planning.
