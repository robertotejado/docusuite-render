# Bajamos a Python 3.11 para máxima compatibilidad
FROM python:3.11-slim

# Directorio de trabajo
WORKDIR /app

# Instalamos dependencias del sistema (¡AQUÍ ESTÁ LA MAGIA PARA PYCAIRO!)
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    python3-dev \
    pkg-config \
    libcairo2-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiamos requerimientos
COPY requirements.txt .

# Actualizamos herramientas base
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# Instalamos las librerías de tu app
RUN pip install --no-cache-dir -r requirements.txt

# Instalamos el servidor web
RUN pip install gunicorn

# Copiamos tu código
COPY . .

# Exponemos el puerto
EXPOSE 5000

# Arrancamos
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
