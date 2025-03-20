FROM python:3.11-slim

WORKDIR /app

# Copiar archivos de requisitos primero para aprovechar la caché de Docker
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código
COPY . .

# Puerto para gRPC y API
EXPOSE 50051 8000

# Iniciar la aplicación
CMD ["python", "src/main.py"] 