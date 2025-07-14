# Build stage - instala dependencias y herramientas de compilación
FROM python:3.9-slim as builder

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Runtime stage - imagen final limpia
FROM python:3.9-slim as runtime

WORKDIR /app

# Copiar solo las dependencias instaladas desde el builder
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

COPY app/ ./app

ENV PYTHONPATH=/app
EXPOSE 8000

# Empezar la aplicación directamente con ddtrace-run y uvicorn
CMD ["ddtrace-run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
