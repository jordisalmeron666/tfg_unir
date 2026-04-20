#Usar una imagen base de Python
FROM python:3.13-slim

# Establecer la zona horaria del sistema
ENV TZ=Europe/Madrid

# Install system dependencies required for building Python packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libc6-dev && \
    rm -rf /var/lib/apt/lists/*

#Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar los archivos necesarios
COPY requirements.txt /app/
COPY *.py /app/

#Instalar las dependencias python
RUN pip install --no-cache-dir -r requirements.txt


# entrypoint
CMD ["python", "/app/main.py"]