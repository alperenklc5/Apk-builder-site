import os, shutil, subprocess, uuid, re
from flask import Flask, render_template, request, send_file

app = Flask(__name__)

# --- Configuration ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_STD = os.path.join(BASE_DIR, 'source', 'standard_klasor')
TEMPLATE_DL = os.path.join(BASE_DIR, 'source', 'downloader_klasor')
OUTPUT_DIR = os.path.join(BASE_DIR, 'output')
KEYSTORE_PATH = os.path.join(BASE_DIR, 'yeni.jks')
KEY_PASS = "123456" 

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/build', methods=['POST'])
def build_apk():
    try:
        app_name = request.form.get('app_name')
        app_type = request.form.get('app_type')
        logo_file = request.files.get('logo')
        
        # 1. Benzersiz bir iş ID'si ve klasör oluştur
        job_id = str(uuid.uuid4())[:8]
        temp_folder = os.path.join(OUTPUT_DIR, job_id)
        
        # 2. Şablonu kopyala
        source_path = TEMPLATE_DL if app_type == 'downloader' else TEMPLATE_STD
        shutil.copytree(source_path, temp_folder)

        # 3. DINAMIK PAKET ADI AYARI (Çakışmayı önleyen kısım)
        # İsmi temizleyip 'com.converttoapk.isim' formatına getiriyoruz
        clean_name = re.sub(r'[^a-zA-Z0-9]', '', app_name.lower())
        new_package_id = f"com.converttoapk.{clean_name}.id{job_id}"

        # AndroidManifest.xml içinde eski paket adını yenisiyle değiştir
        manifest_path = os.path.join(temp_folder, 'AndroidManifest.xml')
        if os.path.exists(manifest_path):
            with open(manifest_path, 'r', encoding='utf-8') as f:
                manifest_content = f.read()
            # 'com.example.template' senin ana template paket adın olmalı
            manifest_content = manifest_content.replace('com.example.template', new_package_id)
            with open(manifest_path, 'w', encoding='utf-8') as f:
                f.write(manifest_content)

        # apktool.yml içindeki paket adını da güncelle
        yml_path = os.path.join(temp_folder, 'apktool.yml')
        if os.path.exists(yml_path):
            with open(yml_path, 'r', encoding='utf-8') as f:
                yml_content = f.read()
            yml_content = re.sub(r'renameManifestPackage:.*', f'renameManifestPackage: {new_package_id}', yml_content)
            with open(yml_path, 'w', encoding='utf-8') as f:
                f.write(yml_content)

        # 4. Uygulama İsmini Güncelle (strings.xml)
        strings_path = os.path.join(temp_folder, 'res', 'values', 'strings.xml')
        if os.path.exists(strings_path):
            with open(strings_path, 'r', encoding='utf-8') as f:
                content = f.read()
            content = content.replace('WebWrapperBase', app_name)
            with open(strings_path, 'w', encoding='utf-8') as f:
                f.write(content)

        # 5. Logoyu Güncelle
        if logo_file:
            logo_path = os.path.join(temp_folder, 'res', 'mipmap-xxxhdpi', 'ic_launcher.png')
            if os.path.exists(logo_path):
                logo_file.save(logo_path)

        # 6. İnşa ve İmzalama
        safe_name = app_name.replace(" ", "_")
        apk_unsigned = os.path.join(OUTPUT_DIR, f"{job_id}_u.apk")
        apk_signed = os.path.join(OUTPUT_DIR, f"{safe_name}.apk")
        
        subprocess.run(["apktool", "b", temp_folder, "-o", apk_unsigned], check=True)
        subprocess.run(["apksigner", "sign", "--ks", KEYSTORE_PATH, "--ks-pass", f"pass:{KEY_PASS}", "--out", apk_signed, apk_unsigned], check=True)

        # Temizlik
        shutil.rmtree(temp_folder)
        if os.path.exists(apk_unsigned):
            os.remove(apk_unsigned)
        
        return f"""
        <div style="text-align:center; padding:100px; font-family:sans-serif; background:#fff;">
            <h1 style="font-size:50px;">✅</h1>
            <h2 style="font-weight:800; color:#000;">Build Successful!</h2>
            <p style="color:#666;">Your app <b>{app_name}</b> is ready with unique ID: {new_package_id}</p>
            <a href="/download/{safe_name}.apk" style="display:inline-block; background:#000; color:#fff; padding:18px 40px; text-decoration:none; border-radius:12px; font-weight:700; margin-top:20px;">
                DOWNLOAD APK FILE
            </a>
            <br><br>
            <a href="/" style="color:#888; text-decoration:none; font-size:14px;">← Back to dashboard</a>
        </div>
        """

    except Exception as e:
        return f"<h1>Error during build:</h1><p>{str(e)}</p>"

@app.route('/download/<filename>')
def download(filename):
    return send_file(os.path.join(OUTPUT_DIR, filename), as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
