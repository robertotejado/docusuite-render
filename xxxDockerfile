# Usamos una imagen oficial y ligera de Python
FROM python:3.11-slim

# Evita que Python escriba archivos temporales (.pyc) y fuerza la salida de consola
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Establecemos el directorio de trabajo
WORKDIR /app

# Instalamos TODAS las dependencias de sistema requeridas
# (Incluyendo libcairo2-dev y pkg-config para pycairo)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    libffi-dev \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev \
    libjpeg-dev \
    libfreetype6-dev \
    pkg-config \
    libcairo2-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiamos el requirements.txt
COPY requirements.txt .

# Actualizamos las herramientas base de compilación de Python
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# Instalamos las dependencias de la Suite
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el resto del código
COPY . .

# Creamos las carpetas necesarias para persistencia
RUN mkdir -p static/attachments
RUN mkdir -p exports_temp

# Exponemos el puerto
EXPOSE 5000

# Arrancamos la app
CMD ["python", "app.py"]
