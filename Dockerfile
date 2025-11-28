# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY mcp_pipe.py .
COPY calculator.py .
COPY dataverse.py .
COPY vnexpress.py .
COPY zingmp3.py .
COPY mcp_config.json* ./

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONIOENCODING=utf-8

# Default command (can be overridden)
CMD ["python", "mcp_pipe.py", "vnexpress.py"]
