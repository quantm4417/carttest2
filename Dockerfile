FROM python:3.11-slim

# Install system dependencies for Playwright and Chromium
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    ca-certificates \
    fonts-liberation \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libatspi2.0-0 \
    libcups2 \
    libdbus-1-3 \
    libdrm2 \
    libgbm1 \
    libgtk-3-0 \
    libnspr4 \
    libnss3 \
    libwayland-client0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxkbcommon0 \
    libxrandr2 \
    xdg-utils \
    libu2f-udev \
    libvulkan1 \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright and browsers (skip system deps since we installed them manually)
RUN pip install --no-cache-dir playwright==1.40.0 && \
    playwright install chromium && \
    playwright install-deps chromium || true

# Copy application
COPY app/ ./app/

# Create data directories
RUN mkdir -p /app/data/uploads /app/data/images

# Expose port
EXPOSE 5000

# Set environment variables
ENV FLASK_APP=app
ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1
ENV PLAYWRIGHT_BROWSERS_PATH=/ms-playwright

# Run Flask
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0", "--port=5000"]
