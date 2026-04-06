#Usar una imagen base de Python
FROM python:3.13-slim
ENV TZ=Europe/Berlin

#Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Install system dependencies required for building Python packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libc6-dev && \
    rm -rf /var/lib/apt/lists/*

# entrypoint
CMD python
