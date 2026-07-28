# Build & development tools

> **Documentation owner:** Shane Ross.

The libraries and tools used to build, run and ship PrimePantry, and **how** each was used.

## Runtime dependencies (`requirements.txt`)

| Library | Version | How it is used |
|---------|---------|----------------|
| **Django** | 5.1 | Web framework — ORM, migrations, auth, templates, the built-in admin, and the test runner. |
| **gunicorn** | ≥22 | Production WSGI server (2 workers) that runs the Django app inside the container. |
| **whitenoise** | ≥6.7 | Serves compressed static assets (images, video, favicon) straight from the app — no separate static server. |
| **stripe** | ≥10 | Official Stripe SDK — creates hosted Checkout Sessions and verifies payment status. Test mode only. |
| **python-dotenv** | ≥1 | Loads secrets (Stripe keys, `DJANGO_SECRET_KEY`) from a local `.env` during development. |

## Infrastructure & dev tools

| Tool | How it is used |
|------|----------------|
| **Docker + Docker Compose** | Package the app into a reproducible image; `docker compose up -d --build` is the one-command deploy/update on the VPS. `Dockerfile`, `docker-compose.yml`, `deploy/docker-entrypoint.sh`. |
| **Nginx / Certbot** | Present on the VPS for the co-hosted site; PrimePantry itself is published directly on `:8080` (WhiteNoise handles static). A systemd + nginx alternative is documented in `DEPLOY.md`. |
| **Hostinger VPS** (Ubuntu 24.04) | Production host. A 2 GB swap file was added to absorb build-time memory spikes. |
| **Git & GitHub** | Version control and collaboration (two developers), incremental commits, merge of parallel branches. Repo: `le6-ite/CP3407_Group2_PrimePantry`. |
| **SQLite** | Database (dev and prod), stored in a Docker volume so data survives rebuilds. |
| **PyCharm** | IDE used by the team (`.idea/` project files). |
| **Pillow** (dev only) | One-off scripts to optimise uploaded photos to WebP (e.g. 265 MB of source images → ~5 MB served) and generate placeholders. |

## Design & documentation tools

| Tool | How it is used |
|------|----------------|
| **Claude design tool** (claude.ai/design) | Produced the clickable "INO"-style mock-ups for every screen, imported and realised 1-to-1 in Django templates. |
| **Mermaid** | Architecture and database (ER) diagrams, written as code and rendered natively by GitHub in [docs/design.md](./design.md) — version-controlled, no external tool needed. |
| **Markdown / GitHub** | All project documentation (this site) is Markdown, navigable from the [README](../README.md). |

## Django features leaned on

- **ORM & migrations** — models `Category`, `Product`, `Order`, `OrderItem`, `CustomerProfile`
  with migrations `0001`–`0004`; data seeded from a JSON **fixture**.
- **Auth** — registration/login (by email), sessions, `@staff_member_required` protection on
  the admin aggregate.
- **Admin** — product and order management, inline order items, bulk status actions.
- **Templating** — a small template-inheritance system (`base.html` → `base_shell.html` →
  page templates) with reusable header/banner/footer partials and a context processor for the
  live cutoff countdown and cart count.
- **Aggregation** — `Sum`/`Count` queries power the group-buying "total quantity ordered"
  report and its CSV export.
