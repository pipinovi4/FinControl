# ===========================
#        BUILD STAGE
# ===========================
FROM python:3.12-slim AS build

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

ARG TELEGRAM_BOT_TOKEN

ARG BACKEND_URL

ARG ABOUT_FILE_ID

# System deps for building wheels
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source
COPY . .

# ===========================
#        RUNTIME STAGE
# ===========================
FROM python:3.12-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Runtime deps only
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy compiled wheels and installed libs from build stage
COPY --from=build /usr/local /usr/local

# Copy source code
COPY --from=build /app /app

# For safety
RUN adduser --disabled-password botuser && chown -R botuser /app
USER botuser

EXPOSE 4000

CMD ["python", "main.py"]
