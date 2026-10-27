FROM python:3.12-slim

# Don't write .pyc files, and flush logs immediately
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install dependencies first (better layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .

EXPOSE 5000

# Run with gunicorn (production server), reachable from outside the container
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "app:app"]
