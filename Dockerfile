FROM python:3.10-slim

WORKDIR /app

# Configurar variables de entorno para optimización de Python y rutas
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app/src

# Copiar dependencias e instalarlas
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el directorio src
COPY src/ src/

# Exponer el puerto por defecto
EXPOSE 8080

# Iniciar servidor Uvicorn en 0.0.0.0 para tráfico externo
CMD ["uvicorn", "secret_scanner.web.app:app", "--host", "0.0.0.0", "--port", "8080"]
