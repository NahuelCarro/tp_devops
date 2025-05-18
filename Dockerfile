FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy API code into subfolder for correct module path
COPY app/ ./app

# Set Python path and expose port
ENV PYTHONPATH=/app
EXPOSE 8000

# Start the application directly with ddtrace-run and uvicorn
CMD ["ddtrace-run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
