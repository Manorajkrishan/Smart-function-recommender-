FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install production server
RUN pip install --no-cache-dir gunicorn

# Copy application code
COPY . .

# Create logs directory
RUN mkdir -p logs

# Migrate to SQLite (if database.json exists)
RUN if [ -f ../smart_func/database.json ]; then \
    python smart_func/migrate_to_db.py || true; \
    fi

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/api/health')" || exit 1

# Run with Gunicorn
CMD ["gunicorn", "-c", "gunicorn_config.py", "app_new:app"]
