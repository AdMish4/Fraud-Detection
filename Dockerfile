# Use a lightweight Python base image
FROM python:3.11-slim

# Prevent Python from writing .pyc files and buffer issues
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies (minimal)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc curl git \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency list first (for caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project
COPY . .

# Expose the Streamlit port
EXPOSE 8501

# Default port (used if $PORT not provided)
ENV PORT=8501

# Run Streamlit app
CMD streamlit run fraud_detection.py --server.port $PORT --server.address 0.0.0.0 --server.headless true