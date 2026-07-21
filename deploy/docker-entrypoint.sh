#!/bin/sh
set -e

python manage.py migrate --noinput

# Seed the catalog only on first run (when the product table is empty),
# so admin edits are not overwritten on every restart.
if ! python manage.py shell -c "import sys; from store.models import Product; sys.exit(0 if Product.objects.exists() else 1)"; then
  echo "Seeding catalog fixture..."
  python manage.py loaddata catalog
fi

exec gunicorn primepantry.wsgi:application --bind 0.0.0.0:8000 --workers 3
