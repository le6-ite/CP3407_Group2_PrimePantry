FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Bake static files into the image (WhiteNoise serves them from STATIC_ROOT).
RUN DJANGO_SECRET_KEY=build DJANGO_DEBUG=False python manage.py collectstatic --noinput

EXPOSE 8000
ENTRYPOINT ["sh", "deploy/docker-entrypoint.sh"]
