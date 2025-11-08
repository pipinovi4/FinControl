# ---------- BUILD ----------
FROM python:3.12-slim AS build

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# 1) Copy only dependency file first → keeps cache when code changes
COPY requirements.txt .

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get purge -y build-essential \
    && rm -rf /var/lib/apt/lists/*

# 2) Now copy only actual application code
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

# 3) Bring installed packages from builder
COPY --from=build /usr/local /usr/local
COPY --from=build /app /app

RUN adduser --disabled-password appuser && chown -R appuser /app
USER appuser

EXPOSE 8000

CMD ["uvicorn", "main:application", "--host", "0.0.0.0", "--port", "8000"]
