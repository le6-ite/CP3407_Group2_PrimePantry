# User story 01: Browse products by category

*As a customer, I want to browse the catalog grouped by category so that I can quickly find the
premium products I'm interested in.*

## Priority: P1 (highest) — Iteration 1
The catalog is the entry point to the whole shop; nothing can be bought without it.

## Estimation: 1.5 days
Planning poker (before Iteration 1):
* Eti: 1 day
* Kei: 2 days
* **Agreed: 1.5 days** (Kei flagged image handling; Eti had done Django ORM listing before)

## Assumptions
* Products and categories are seeded from a fixture.
* Each product has a photo; missing photos fall back to a placeholder.

## Description
The catalog page lists every active product grouped under its category, in a responsive grid,
each card showing photo, name and price. Category "pills" filter to a single category
(`?cat=<slug>`). A full-bleed banner sits at the top.

*Description-v1:* a flat list of products.
*Description-v2 (final):* products grouped into numbered category sections with a filter bar,
plus quick "+ Add to cart" on each card.

## Tasks
1. `Category` and `Product` models + admin, 0.4 d
2. Catalog fixture (7 categories, 42 products), 0.3 d
3. Catalog view: group by category, filter by `?cat=`, 0.4 d
4. INO-style template: banner, filter pills, product grid, 0.4 d

## UI design
Mock-up produced in the Claude design tool (INO style). Realised at
`http://147.93.56.126:8080/catalog/`.

## Completed
✅ Iteration 1. Search added on top (story 05). Live: `/catalog/` and `/catalog/?cat=premium-seafood`.
