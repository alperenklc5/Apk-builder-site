# Temel olarak Python kullan
FROM python:3.9-slim

# Java (OpenJDK) ve gerekli araçları yükle
RUN apt-get update && \
    apt-get install -y openjdk-17-jdk-headless zip unzip && \
    rm -rf /var/lib/apt/lists/*

# Çalışma klasörünü ayarla
WORKDIR /app

# Gereksinimleri yükle
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kodları kopyala
COPY . .

# 10000 Portunu aç (Web sitesi buradan yayın yapacak)
EXPOSE 10000

# Uygulamayı başlat
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:10000"]