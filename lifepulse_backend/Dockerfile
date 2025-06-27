FROM python:3.11-slim

# Create working directory
WORKDIR /app

# Install required system packages
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN adduser --disabled-password --gecos "" celeryuser

# Copy project requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app source code
COPY . .

# Collect static files (as root to avoid permission issues)
RUN python manage.py collectstatic --noinput

# Fix permissions on static and app folders
RUN chown -R celeryuser:celeryuser /app

# Switch to non-root user
USER celeryuser

# Expose port for Gunicorn
EXPOSE 8000

# Start Django using Gunicorn
CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000"]
