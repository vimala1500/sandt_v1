# Use Python 3.11 slim image as base
# 'slim' version is smaller and more suitable for production
FROM python:3.11-slim

# Set working directory inside the container
# All subsequent commands will run from this directory
WORKDIR /app

# Copy requirements first (for better Docker layer caching)
# This allows Docker to cache the pip install step if requirements don't change
COPY requirements.txt .

# Install Python dependencies
# --no-cache-dir reduces image size by not storing pip cache
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application code into the container
COPY . .

# Expose port 8080 (Cloud Run default port)
# Cloud Run expects applications to listen on the PORT environment variable
EXPOSE 8080

# Set environment variable for production
ENV DASH_DEBUG=False

# Command to run the application
# Uses gunicorn as production WSGI server for better performance
CMD exec gunicorn --bind :8080 --workers 1 --threads 8 --timeout 0 app:server
