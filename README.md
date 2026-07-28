# PrimePantry — a curated food group-buying platform

**CP3407 Software Engineering II · Group 2 · James Cook University**

PrimePantry is a group-buying platform that connects consumers with trusted suppliers of
premium seafood, meat and specialty food. Customers order during a scheduled weekly window;
after the cutoff, products are sourced against actual demand rather than held as stock —
improving freshness, cutting waste and making premium ingredients affordable for individuals.

- **Live site (deployed):** http://147.93.56.126:8080/
- **Repository:** https://github.com/le6-ite/CP3407_Group2_PrimePantry
- **Stack:** Django 5.1 · SQLite · Stripe (test mode) · Docker · Gunicorn · Nginx · Hostinger VPS

---

## Team

CP3407 Group 2 — four members. *Add student IDs below.* Documentation responsibilities are split
across the whole team; planning-poker estimates and technical-writing review were done by all four.

| Member | GitHub | Code contribution | Documentation owner of |
|--------|--------|-------------------|------------------------|
| **Etigel Tcydenov** | [@le6-ite](https://github.com/le6-ite) | Backend, storefront, checkout & payments, deployment | **Design** — architecture & database ([docs/design.md](./docs/design.md) §1–2) · **Deployment** ([DEPLOY.md](./DEPLOY.md)) |
| **Kei Kwan Ip** | [@KwanQueenie](https://github.com/KwanQueenie) | Accounts, profiles, favourites, testing | **Requirements** ([User_stories.md](./User_stories.md), [user_stories/](./user_stories/)) · **UI design & screenshots** ([docs/design.md](./docs/design.md) §3) |
| **Samuel Fernandez** |  [@Eslezer](https://github.com/eslezer) | Requirements research, product pitch, QA | **Testing** ([docs/testing.md](./docs/testing.md)) · **Implementation** ([docs/implementation.md](./docs/implementation.md)) |
| **Shane Ross** | — | Agile tracking, tooling & QA support | **Agile** ([iteration_1.md](./iteration_1.md), [iteration_2.md](./iteration_2.md)) · **Build & dev tools** ([docs/tools.md](./docs/tools.md)) · **Version control** writeup |

**Technical writing** (criterion 8) — README cohesion and cross-linking — is a shared responsibility, coordinated by Etigel.

Instructor **Dmitry Konovalov** (`jc138691@gmail.com`) has been added as a collaborator to view the project.

---

## Documentation index (for marking)

Everything required for marking is linked from here.

| Rubric criterion | Document |
|------------------|----------|
| 1 · Requirements | [Product backlog & user stories](./User_stories.md) → [detailed stories](./user_stories/) |
| 2 · Design | [Design: architecture, database & UI](./docs/design.md) |
| 3 · Implementation | This repository + [live site](http://147.93.56.126:8080/) · [feature summary](./docs/implementation.md) |
| 4 · Test | [Testing](./docs/testing.md) |
| 5 · Version control | Git/GitHub — see the [commit history](https://github.com/le6-ite/CP3407_Group2_PrimePantry/commits/main) |
| 6 · Build & dev tools | [Tools & libraries](./docs/tools.md) |
| 7 · Agile | [Iteration 1](./iteration_1.md) · [Iteration 2](./iteration_2.md) |
| 8 · Technical writing | This site (all pages above) |
| — Deployment | [Deployment guide](./DEPLOY.md) |

---

## Run it locally

```bash
git clone https://github.com/le6-ite/CP3407_Group2_PrimePantry.git
cd CP3407_Group2_PrimePantry
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python manage.py migrate
.venv/bin/python manage.py loaddata catalog     # 7 categories, 42 products
.venv/bin/python manage.py runserver            # http://127.0.0.1:8000/
```

Payments use Stripe **test mode** — no real money moves. Pay with card `4242 4242 4242 4242`,
any future expiry, any CVC. See [DEPLOY.md](./DEPLOY.md) to run the production (Docker) build.

## What's implemented

Register/login · browse by category · search · product detail · cart · **online payment (Stripe test)** ·
**weekly order window with countdown & cutoff** · order confirmation & history · saved profiles ·
favourites · reorder · admin product/order management · **admin aggregate "total quantity ordered per
product" with CSV shopping-list export** (the group-buying USP). See [docs/implementation.md](./docs/implementation.md).
