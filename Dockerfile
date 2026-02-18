FROM python:3.9-slim-bullseye

RUN mkdir -p /usr/share/man/man1

# Apktool'un en güncel versiyonunu indirecek şekilde güncelliyoruz
RUN apt-get update && \
    apt-get install -y \
    default-jdk \
    zip \
    unzip \
    wget \
    apksigner \
    && rm -rf /var/lib/apt/lists/*
RUN apt-get update && apt-get install -y zipalign
# En güncel Apktool'u manuel kuruyoruz (2.10.0)
RUN wget https://github.com/iBotPeaches/Apktool/releases/download/v2.10.0/apktool_2.10.0.jar -O /usr/local/bin/apktool.jar && \
    echo '#!/bin/bash\njava -jar /usr/local/bin/apktool.jar "$@"' > /usr/local/bin/apktool && \
    chmod +x /usr/local/bin/apktool

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN chmod -R 777 /app/source
EXPOSE 10000
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:10000", "--timeout", "120"]
