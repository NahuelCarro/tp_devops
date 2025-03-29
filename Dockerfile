FROM python:3.9-slim

# Seteo el directorio de trabajo
WORKDIR /app

# Copio el archivo de requirements.txt
COPY requirements.txt .

# Instalo los paquetes del requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copio el directorio actual en /app
COPY app/ /app
COPY wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh

ENV PYTHONPATH=/app
EXPOSE 8000

# Corro la aplicacion
CMD ["/wait-for-it.sh", "db:5432", "--", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]