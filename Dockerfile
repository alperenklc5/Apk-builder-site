# 1. Stabil ve garantili Linux sürümü kullan (Debian Bullseye)
FROM python:3.9-slim-bullseye

# 2. Java kurulumunda hata çıkmaması için gerekli klasörleri oluştur
RUN mkdir -p /usr/share/man/man1

# 3. Gerekli araçları yükle (Java 11, Zip, Apktool)
# 'default-jdk' genelde Java 11 kurar ve Apktool için en sağlıklısıdır.
RUN apt-get update && \
    apt-get install -y \
    default-jdk \
    zip \
    unzip \
    apktool \
    apksigner \
    && rm -rf /var/lib/apt/lists/*

# 4. Çalışma Klasörü
WORKDIR /app

# 5. Kütüphaneleri Yükle
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 6. Dosyaları Kopyala
COPY . .

# 7. İzinleri Ayarla (Önemli!)
RUN chmod -R 777 /app/source

# 8. Portu Aç ve Başlat
EXPOSE 10000
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:10000", "--timeout", "120"]
