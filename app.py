import os
import shutil
import subprocess
from flask import Flask, render_template, request, send_file
import uuid

app = Flask(__name__)

# --- AYARLAR (Senin Klasör Yapına Göre Düzenlendi) ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Senin "source" klasörünün içindeki klasör isimleri:
# NOT: Eğer source içindeki klasör adların farklıysa buraları düzelt!
# Önceki adımda "standard_klasor" ve "downloader_klasor" oluşmuştu.
TEMPLATE_STD = os.path.join(BASE_DIR, 'source', 'standard_klasor')
TEMPLATE_DL = os.path.join(BASE_DIR, 'source', 'downloader_klasor')

OUTPUT_DIR = os.path.join(BASE_DIR, 'output')

# Senin JKS dosyanın adı:
KEYSTORE_PATH = os.path.join(BASE_DIR, 'yeni.jks')

# BURAYA DİKKAT: Kendi şifreni ve alias ismini yazmalısın!
KEY_PASS = "123456"      # <-- JKS şifren neyse buraya yaz
KEY_ALIAS = "key0"       # <-- Genelde "key0" olur, değiştirdiysen onu yaz

# -----------------------------------------------------

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/build', methods=['POST'])
def build_apk():
    try:
        app_name = request.form.get('app_name')
        url = request.form.get('url')
        # Hangi butona basıldıysa o tipi al (formda hidden input olacak veya buton value'su)
        # Şimdilik varsayılan olarak standard alalım veya formdan bekleyelim
        app_type = 'standard' 
        
        job_id = str(uuid.uuid4())[:8]
        temp_folder = os.path.join(OUTPUT_DIR, job_id)
        
        # 1. Kopyalama
        source_path = TEMPLATE_STD # Şimdilik sadece standardı test et
        shutil.copytree(source_path, temp_folder)
        
        # 2. İsim Değiştirme (Strings.xml)
        strings_path = os.path.join(temp_folder, 'res', 'values', 'strings.xml')
        if os.path.exists(strings_path):
            with open(strings_path, 'r', encoding='utf-8') as f:
                content = f.read()
            # "WebWrapperBase" kelimesini kullanıcının girdiği isimle değiştir
            content = content.replace('WebWrapperBase', app_name)
            with open(strings_path, 'w', encoding='utf-8') as f:
                f.write(content)

        # 3. APK Paketle
        apk_unsigned = os.path.join(OUTPUT_DIR, f"{job_id}_unsigned.apk")
        subprocess.run(["apktool", "b", temp_folder, "-o", apk_unsigned], check=True)
        
        # 4. İmzala
        apk_signed = os.path.join(OUTPUT_DIR, f"app_{job_id}.apk")
        subprocess.run([
            "apksigner", "sign", "--ks", KEYSTORE_PATH,
            "--ks-pass", f"pass:{KEY_PASS}",
            "--out", apk_signed,
            apk_unsigned
        ], check=True)
        
        # Temizlik
        shutil.rmtree(temp_folder)
        if os.path.exists(apk_unsigned):
            os.remove(apk_unsigned)
            
        return f"""
        <div style="text-align:center; margin-top:50px; font-family:sans-serif;">
            <h1 style="color:green;">✅ Uygulama Hazır!</h1>
            <h3>{app_name}</h3>
            <a href="/download/{os.path.basename(apk_signed)}" 
               style="background:#007bff; color:white; padding:15px 30px; text-decoration:none; border-radius:5px; font-size:20px;">
               📥 İNDİR
            </a>
        </div>
        """

    except Exception as e:
        return f"<h1>Hata:</h1><p>{str(e)}</p>"

@app.route('/download/<filename>')
def download_file(filename):
    return send_file(os.path.join(OUTPUT_DIR, filename), as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)