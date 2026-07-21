#!/usr/bin/env bash
# Pull the latest code and restart PrimePantry on the VPS.
# Run from the project directory:  bash deploy/update.sh
set -euo pipefail

git pull
.venv/bin/pip install -r requirements.txt
set -a; . ./.env; set +a
.venv/bin/python manage.py migrate --noinput
.venv/bin/python manage.py collectstatic --noinput
sudo systemctl restart primepantry
echo "Updated and restarted."
