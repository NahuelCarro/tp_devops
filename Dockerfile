FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install bash and netcat for wait-for-it.sh functionality
RUN apt-get update && \
    apt-get install -y --no-install-recommends bash netcat-openbsd && \
    rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy API code into subfolder for correct module path
COPY app/ ./app

# Copy wait-for-it and strip Windows CRLF endings
COPY wait-for-it.sh /wait-for-it.sh
RUN sed -i 's/\r$//' /wait-for-it.sh && chmod +x /wait-for-it.sh

# Set Python path and expose port
ENV PYTHONPATH=/app
EXPOSE 8000

# Start the application, waiting for the database
CMD ["/wait-for-it.sh", "db:5432", "--", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
