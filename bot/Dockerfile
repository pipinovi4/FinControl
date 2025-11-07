# ---------- 1️⃣ BUILD STAGE ----------
# Use a lightweight Python 3.12 image as the base for dependency installation
FROM python:3.12-slim AS build

# Disable .pyc file generation and ensure logs are flushed immediately
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Copy only the dependency file first to leverage Docker layer caching
COPY requirements.txt .

# Upgrade pip and install all Python dependencies
# --no-cache-dir prevents caching to reduce image size
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt


# ---------- 2️⃣ RUNTIME STAGE ----------
# Use a clean Python runtime image for production execution
FROM python:3.12-slim

# Install essential system utilities (for SSL verification, DNS resolution, etc.)
RUN apt-get update && apt-get install -y --no-install-recommends \
        ca-certificates curl \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy installed Python packages from the build stage to avoid reinstalling
COPY --from=build /usr/local/lib/python3.12 /usr/local/lib/python3.12

# Copy the bot's application source code into the container
COPY . .

# Create a non-root user for security best practices
RUN adduser --disabled-password appuser && chown -R appuser /app
USER appuser

# Expose an optional port (useful if the bot handles webhooks or a small HTTP API)
EXPOSE 4000

# Define the default command to run the bot
CMD ["python", "main.py"]
