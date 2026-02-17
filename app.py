import os, shutil, subprocess, uuid
from flask import Flask, render_template, request, send_file

app = Flask(__name__)

# --- AYARLAR ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Klasör isimlerinin senin GitHub'daki isimlerle birebir aynı olduğundan emin ol!
TEMPLATE_STD = os.path.join(BASE_DIR, 'source', 'standard_klasor')
TEMPLATE_DL = os.path.join(BASE_DIR, 'source', 'downloader_klasor')
OUTPUT_DIR = os.path.join(BASE_DIR, 'output')
KEYSTORE_PATH = os.path.join(BASE_DIR, 'yeni.jks')
KEY_PASS = "123456" 

if not os.path.exists(OUTPUT_DIR): os.makedirs(OUTPUT_DIR)

@app.route('/')
def home(): return render_template('index.html')

@app.route('/build', methods=['POST'])
def build_apk():
    try:
        app_name = request.form.get('app_name')
        url = request.form.get('url')
        app_type = request.form.get('app_type') # 'standard' veya 'downloader'
        logo_file = request.files.get('logo')

        job_id = str(uuid.uuid4())[:8]
        temp_folder = os.path.join(OUTPUT_DIR, job_id)
        
        # 1. Doğru Template'i Kopyala
        source_path = TEMPLATE_DL if app_type == 'downloader' else TEMPLATE_STD
        shutil.copytree(source_path, temp_folder)

        # 2. Uygulama İsmini Değiştir (strings.xml)
        strings_path = os.path.join(temp_folder, 'res', 'values', 'strings.xml')
        if os.path.exists(strings_path):
            with open(strings_path, 'r', encoding='utf-8') as f:
                content = f.read()
            content = content.replace('WebWrapperBase', app_name)
            with open(strings_path, 'w', encoding='utf-8') as f:
                f.write(content)

        # 3. Logo Değiştir (Eğer yüklendiyse)
        if logo_file:
            # En yaygın ikon yolunu hedefliyoruz (xxxhdpi)
            logo_path = os.path.join(temp_folder, 'res', 'mipmap-xxxhdpi', 'ic_launcher.png')
            if os.path.exists(logo_path):
                logo_file.save(logo_path)

        # 4. APK İnşa Et ve İmzala
        safe_name = app_name.replace(" ", "_")
        apk_unsigned = os.path.join(OUTPUT_DIR, f"{job_id}_u.apk")
        apk_signed = os.path.join(OUTPUT_DIR, f"{safe_name}.apk") # Logdaki hata burada düzeldi!
        
        subprocess.run(["apktool", "b", temp_folder, "-o", apk_unsigned], check=True)
        subprocess.run(["apksigner", "sign", "--ks", KEYSTORE_PATH, "--ks-pass", f"pass:{KEY_PASS}", "--out", apk_signed, apk_unsigned], check=True)

        # Temizlik
        shutil.rmtree(temp_folder)
        if os.path.exists(apk_unsigned): os.remove(apk_unsigned)
        
        return f'<h1>✅ Hazır!</h1><a href="/download/{safe_name}.apk" style="font-size:20px; color:green; text-decoration:none; border:2px solid green; padding:10px;">📥 {app_name}.apk İNDİR</a>'

    except Exception as e: return f"<h1>❌ Hata Oluştu:</h1><p>{str(e)}</p>"

@app.route('/download/<filename>')
def download(filename): return send_file(os.path.join(OUTPUT_DIR, filename), as_attachment=True)

if __name__ == '__main__': app.run(host='0.0.0.0', port=10000)
