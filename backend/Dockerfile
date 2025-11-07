# ---------- 1️⃣ BUILD STAGE ----------
# Use a minimal Python 3.12 image to install dependencies
FROM python:3.12-slim AS build

# Disable bytecode generation and enable unbuffered output for clean logging
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Define working directory inside the container
WORKDIR /app

# Copy only the requirements file first to leverage Docker layer caching
COPY requirements.txt .

# Upgrade pip and install dependencies
# --no-cache-dir keeps the image smaller by removing package caches
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt


# ---------- 2️⃣ RUNTIME STAGE ----------
# Use a fresh, lightweight Python runtime image for production
FROM python:3.12-slim

# Install minimal system tools (required for SSL certificates or DNS resolution)
RUN apt-get update && apt-get install -y --no-install-recommends \
        ca-certificates curl \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy installed Python libraries from the build stage
COPY --from=build /usr/local/lib/python3.12 /usr/local/lib/python3.12

# Copy the entire bot source code into the runtime container
COPY . .

# Create a non-root user for security and assign ownership
RUN adduser --disabled-password appuser && chown -R appuser /app
USER appuser

# Expose port 4000 (optional, useful if bot uses webhooks or HTTP callbacks)
EXPOSE 4000

# Define the default startup command
CMD ["python", "main.py"]
