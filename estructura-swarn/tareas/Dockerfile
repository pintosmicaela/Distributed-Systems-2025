# Imagen base oficial con Python 3.10 (o la versión que uses)
FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    gcc \
    libmariadb-dev \
    libmariadb-dev-compat \
    pkg-config \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia requirements y los instala
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo el código al contenedor
COPY . .

# Expone el puerto donde el servidor gRPC escucha
EXPOSE 50055

# Comando para ejecutar tu servidor
CMD ["python", "servidor.py"]

