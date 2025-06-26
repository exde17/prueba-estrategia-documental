# Usa una imagen base de Python 3.13
FROM python:3.13-slim

# Instala netcat para health checks
RUN apt-get update && apt-get install -y netcat-openbsd && rm -rf /var/lib/apt/lists/*

# Establece el directorio de trabajo en el contenedor
WORKDIR /app

# Copia el archivo de requisitos primero para aprovechar el cache de Docker
COPY requirements.txt .

# Instala las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia el código fuente de la aplicación
COPY . .

# Expone el puerto 8000 (puerto por defecto de FastAPI)
EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
