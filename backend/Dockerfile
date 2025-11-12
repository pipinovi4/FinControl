# ---------- BUILD ----------
FROM python:3.12-slim AS build

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# 1️⃣ Оголошуємо ВСІ build ARG-и (для прозорості та debug)
ARG DB_USER
ARG DB_PASSWORD
ARG DB_HOST
ARG DB_PORT
ARG DB_NAME

ARG JWT_SECRET
ARG JWT_ALGO
ARG ACCESS_EXPIRE_MINUTES
ARG REFRESH_EXPIRE_DAYS

ARG MAIL_USERNAME
ARG MAIL_PASSWORD
ARG MAIL_FROM
ARG MAIL_PORT
ARG MAIL_SERVER
ARG MAIL_STARTTLS
ARG MAIL_SSL_TLS
ARG USE_CREDENTIALS

ARG FRONTEND_URL
ARG BACKEND_URL
ARG ALLOWED_ORIGINS

# 2️⃣ DEBUG — не зберігається в runtime
RUN echo "🔧 Backend build with:" \
 && echo "DB_USER=$DB_USER" \
 && echo "DB_HOST=$DB_HOST" \
 && echo "MAIL_FROM=$MAIL_FROM" \
 && echo "FRONTEND_URL=$FRONTEND_URL" \
 && echo "BACKEND_URL=$BACKEND_URL" \
 && echo "ALLOWED_ORIGINS=$ALLOWED_ORIGINS"

# dependencies
COPY requirements.txt .

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get purge -y build-essential \
    && rm -rf /var/lib/apt/lists/*

# source code
COPY app ./app
COPY main.py .
COPY db ./db


# ---------- RUNTIME ----------
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# переносимо бібліотеки і код
COPY --from=build /usr/local /usr/local
COPY --from=build /app /app

RUN adduser --disabled-password appuser && chown -R appuser /app
USER appuser

EXPOSE 8000

# Gunicorn server
CMD ["gunicorn", "main:application", \
     "--workers", "3", \
     "--worker-class", "uvicorn.workers.UvicornWorker", \
     "--bind", "0.0.0.0:8000", \
     "--timeout", "120", \
     "--keep-alive", "65", \
     "--preload"]
