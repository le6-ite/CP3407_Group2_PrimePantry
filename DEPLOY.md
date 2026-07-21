# Deploying PrimePantry to a Hostinger VPS

Stack: **Django + Gunicorn + Nginx + systemd** on Ubuntu/Debian. Static files are
served by **WhiteNoise** (no separate static config needed). Database is SQLite by
default (loaded from the committed fixture).

Placeholders to replace: `<user>` (your Linux user), `<vps-ip>` (your server IP or
domain), `<github-user>` (your GitHub username).

---

## 0. Push the code to GitHub (from your Mac, once)

```bash
cd "/Users/le6ite/Desktop/CP3407_Soft_Dev/2 assignment/prime pantry"
git remote add origin https://github.com/<github-user>/primepantry.git
git push -u origin main
```

On github.com → repo **Settings → Collaborators**, add your groupmate and the
instructor (`jc138691@gmail.com`, Dmitry Konovalov).

---

## 1. Install system packages (on the VPS, once)

```bash
sudo apt update
sudo apt install -y python3-venv python3-pip nginx git
```

## 2. Clone and set up the app

```bash
cd ~
git clone https://github.com/<github-user>/primepantry.git
cd primepantry
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

## 3. Create the `.env` file

```bash
cp .env.example .env
# generate a secret key:
.venv/bin/python -c "from django.core.management.utils import get_random_secret_key as k; print(k())"
nano .env
```
Set:
```
DJANGO_SECRET_KEY=<paste the generated key>
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=<vps-ip>,127.0.0.1,localhost
DJANGO_CSRF_TRUSTED_ORIGINS=http://<vps-ip>
```

## 4. Initialise the database and static files

```bash
set -a; . ./.env; set +a          # load env into this shell
.venv/bin/python manage.py migrate
.venv/bin/python manage.py loaddata catalog      # 7 categories, 42 products
.venv/bin/python manage.py collectstatic --noinput
.venv/bin/python manage.py createsuperuser        # for /admin/
```

## 5. Run under systemd (gunicorn)

```bash
# edit deploy/primepantry.service and replace <user> first
sudo cp deploy/primepantry.service /etc/systemd/system/primepantry.service
sudo systemctl daemon-reload
sudo systemctl enable --now primepantry
sudo systemctl status primepantry --no-pager
```

## 6. Nginx reverse proxy

```bash
# edit deploy/nginx-primepantry.conf and set server_name first
sudo cp deploy/nginx-primepantry.conf /etc/nginx/sites-available/primepantry
sudo ln -sf /etc/nginx/sites-available/primepantry /etc/nginx/sites-enabled/primepantry
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t && sudo systemctl restart nginx
```

Open `http://<vps-ip>/` — the site is live. Your groupmate opens the same URL.

## 7. (Optional) HTTPS with a domain

Point a domain at the VPS, then:
```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain
```
Then set `DJANGO_CSRF_TRUSTED_ORIGINS=https://your-domain` in `.env` and
`sudo systemctl restart primepantry`.

---

## Making updates later

```bash
# on your Mac
git add -A && git commit -m "..." && git push

# on the VPS
cd ~/primepantry && bash deploy/update.sh
```

`deploy/update.sh` pulls, installs deps, migrates, re-collects static, and restarts.

---

## Alternative: deploy with Docker (if the VPS already runs Docker)

If port 80 is already held by an existing Docker stack, skip the systemd + nginx
steps above and run PrimePantry as its own container on a free port (8080).

```bash
cd ~/CP3407_Group2_PrimePantry
git pull
# .env must exist (see step 3). For port 8080, set:
#   DJANGO_CSRF_TRUSTED_ORIGINS=http://<vps-ip>:8080
docker compose up -d --build
docker compose ps
```

Open `http://<vps-ip>:8080/`. The SQLite DB lives in the `pp_data` volume, so it
survives rebuilds. Create an admin user:

```bash
docker compose exec web python manage.py createsuperuser
```

Update later:
```bash
git pull && docker compose up -d --build
```

## Troubleshooting
- `docker compose logs -f web` — app logs (Docker).
- `sudo journalctl -u primepantry -n 50` — gunicorn logs (systemd).
- 400 Bad Request → `<vps-ip>` missing from `DJANGO_ALLOWED_HOSTS`.
- Admin login CSRF error → set `DJANGO_CSRF_TRUSTED_ORIGINS` to your `http(s)://host`.
- Images/CSS missing → re-run `collectstatic`, check gunicorn is running.
