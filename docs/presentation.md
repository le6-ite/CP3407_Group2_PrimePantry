# PrimePantry — presentation content

Slide-by-slide content for the final CP3407 presentation. Copy each block into a slide.
Everything here reflects the **delivered, deployed** project.

- **Live site:** http://147.93.56.126:8080/
- **Repository:** https://github.com/le6-ite/CP3407_Group2_PrimePantry
- **Team:** Etigel Tcydenov · Kei Kwan Ip · Samuel Fernandez · Shane Ross (Group 2)

---

## Slide 1 — Title

**PrimePantry**
A curated food group-buying platform
CP3407 Software Engineering II · Group 2 · James Cook University
Etigel Tcydenov · Kei Kwan Ip · Samuel Fernandez · Shane Ross

---

## Slide 2 — Agenda

1. Project overview
2. Problem statement
3. Target users
4. Objectives
5. Unique selling point (USP)
6. Major features
7. User stories & Agile process
8. Technology stack
9. Database & architecture design
10. Live demo
11. Testing
12. Deliverables & conclusion

---

## Slide 3 — Project overview

A **group-buying platform** connecting consumers with trusted suppliers of premium
**seafood, meat and specialty food**.

- Customers order during a **scheduled weekly window**.
- After the cutoff, products are **sourced against actual demand** — not held as stock.
- Result: better freshness, less waste, and premium ingredients made affordable for
  individuals.
- *"We only sell products we personally enjoy and would repurchase."*

---

## Slide 4 — Problem statement

1. Premium seafood/meat/specialty products are **unavailable in local supermarkets**.
2. Suppliers require **large minimum orders** — out of reach for individuals.
3. Premium/imported brands have **limited distribution in Brisbane**.
4. Providers must **manually tally** the total quantity of each product ordered — slow and
   error-prone. **← solved by our USP**
5. Providers must **manually match orders and pack** each one — slow and mistake-prone.

---

## Slide 5 — Target users

- **Food enthusiasts** — want premium seafood/meat/specialty items not found in normal retail.
- **People with busy lifestyles** — want quality food without sourcing from multiple sellers.
- Located in / around **Brisbane, Australia**.

---

## Slide 6 — Project objectives

1. Simplify meal prep with carefully selected, convenient-to-cook products.
2. Lower wholesale purchasing barriers by letting individuals join **group orders**.
3. Build a **user-friendly group-buying platform** for premium food.
4. Provide a convenient, efficient ordering experience for busy, quality-focused buyers.

---

## Slide 7 — Unique selling point (USP)

**Group buying with a weekly cutoff.**

- A shared **order window** closes every Wednesday 18:00 (Brisbane) — shown as a live
  countdown across the site.
- Orders are **pooled**; the service provider gets an **automatic per-product quantity total**
  for the whole window → knows exactly how much to source.
- One-click **CSV shopping list** for buying — directly solves *Problem 04* (no manual tallying).

> This is what makes PrimePantry different from an ordinary online shop.

---

## Slide 8 — Major features (delivered)

**For customers**
- Register / log in (by email) · guest checkout
- Browse by category · search · product detail
- Cart (add / change quantity / remove)
- **Checkout & online payment (Stripe, test mode)**
- Weekly window with live countdown
- Order confirmation **+ email receipt**
- Order history & status · saved profile · favourites · reorder

**For the service provider (admin)**
- Manage products, categories & orders (Django admin)
- Advance order status: Confirmed → Packing → Ready → Completed
- **Aggregate "total quantity ordered per product"** for the window **+ CSV export**

---

## Slide 9 — User stories & Agile process

- Full **product backlog** prioritised (P1–P3) and estimated by **planning poker**
  (more stories than fit 2 iterations → priority practised).
- **Iteration 1 (14–21 Jul):** storefront foundation — catalog, product, cart, weekly window.
- **Iteration 2 (22–28 Jul):** accounts, **payment**, orders, admin USP, profiles, deployment.
- Tracked with iteration boards + burn-down; delivered on plan and **deployed**.

*(See `User_stories.md`, `iteration_1.md`, `iteration_2.md` in the repo.)*

---

## Slide 10 — Technology stack

| Layer | Technology |
|-------|-----------|
| Language / framework | **Python · Django 5.1** (server-rendered) |
| Database | **SQLite** (in a Docker volume) |
| Payments | **Stripe Checkout** (hosted, test mode) — PCI-safe |
| Email | **Gmail SMTP** (order confirmation receipts) |
| Static files | **WhiteNoise** |
| App server | **Gunicorn** |
| Packaging / deploy | **Docker + Docker Compose** on a **Hostinger VPS** (Ubuntu 24.04) |
| Version control | **Git / GitHub** (4-member collaboration) |
| Design & docs | Claude design tool (mock-ups) · **Mermaid** diagrams · Markdown / GitHub Pages |

---

## Slide 11 — Database design

Six tables (Django ORM). *Show the ER diagram from `docs/design.md`.*

- **Category** → **Product** (one-to-many)
- **Order** → **OrderItem** (one-to-many); OrderItem snapshots name/price
- **User** → **Order** (a user has many orders; guests allowed — nullable)
- **User** → **CustomerProfile** (one-to-one: saved address, phone, delivery pref)
- **CustomerProfile** ↔ **Product** (many-to-many favourites)
- Each **Order** records `round_cutoff` → drives the weekly aggregate (USP).

---

## Slide 12 — System architecture

*Show the architecture diagram from `docs/design.md`.*

- Browser → **Gunicorn (:8080)** → **Django** (views · templates · ORM) → **SQLite**.
- Static assets served by **WhiteNoise** inside the app.
- On *Place order*: Django creates a Stripe **Checkout Session** and redirects to Stripe's
  hosted page; on return, it verifies payment, confirms the order, emails a receipt and
  clears the cart.
- Whole app is **containerised**; updates ship with `git pull && docker compose up -d --build`.

---

## Slide 13 — Live demo (script)

Run against **http://147.93.56.126:8080/**:

1. **Home** — hero video, live weekly-cutoff countdown, "popular this week".
2. **Catalog** — filter by category, search "salmon".
3. **Product** → **Add to cart** → **Cart** (change quantity).
4. **Checkout** — pickup/delivery, contact → **Place order** → **Stripe test page**
   (card `4242 4242 4242 4242`) → **Confirmation** (order number, email sent).
5. **Admin** (`/admin/`) — show the order; advance status.
6. **USP:** `/staff/quantities/` — total quantity per product for the window → **Export CSV**.

---

## Slide 14 — Testing

- **10 automated tests** (`manage.py test store`) — accounts, cart, checkout, and
  **security/authorisation** (cross-user reorder, cross-session confirmation, open-redirect).
- **Acceptance testing** of every user story on the deployed site.
- **End-to-end payment verified in production** — real Stripe test purchase, order **#PP-00016**,
  visible in Django admin, the USP aggregate, and the Stripe dashboard.

---

## Slide 15 — Team & responsibilities

| Member | Contribution |
|--------|--------------|
| **Etigel Tcydenov** | Backend, storefront, checkout & payments, deployment · docs: Design, Deployment |
| **Kei Kwan Ip** | Accounts, profiles, favourites, testing · docs: Requirements, UI |
| **Samuel Fernandez** | Requirements & product research, QA · docs: Testing, Implementation |
| **Shane Ross** | Agile tracking, tooling & QA · docs: Agile, Tools, Version control |

Collaboration via GitHub (two parallel branches merged cleanly); planning-poker estimates by
all four.

---

## Slide 16 — Deliverables & conclusion

**Delivered**
- A **deployed, working** group-buying platform (all pitched features) — payments, weekly
  window, and the admin quantity aggregate (USP).
- Full documentation: requirements, design (UML + ER), testing, tools, Agile boards — on GitHub.

**What we learned** — Agile iteration & planning poker, Django end-to-end, Stripe integration,
containerised deployment, and real-world debugging (memory/OOM, credential handling, Git merges).

**Future work** — email marketing, delivery zones & pricing, product reviews, Postgres + HTTPS
custom domain.

**PrimePantry — premium food, pooled buying, zero waste.**

---

## Appendix — quick facts for Q&A

- 7 categories · 42 products (seeded from a fixture).
- Weekly cutoff: **Wednesday 18:00, Australia/Brisbane**.
- Payment: Stripe **test mode** (card `4242 4242 4242 4242`).
- Deploy: Docker on Hostinger VPS; static via WhiteNoise; SQLite in a volume.
- ~19 commits across 2 iterations (14–28 Jul 2026); 10 automated tests passing.
