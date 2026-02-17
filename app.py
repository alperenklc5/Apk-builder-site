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
        
        job_id = str(uuid.uuid4())[:8]
        temp_folder = os.path.join(OUTPUT_DIR, job_id)
        
        # 1. Şablonu Temiz Kopyala
        source_path = TEMPLATE_DL if app_type == 'downloader' else TEMPLATE_STD
        shutil.copytree(source_path, temp_folder)

        # 2. GÜVENLİ PAKET ADI (ID Çakışması İçin)
        # Sadece harf kullanarak Android'in reddetmeyeceği bir isim oluşturuyoruz
        safe_package_name = re.sub(r'[^a-z]', '', app_name.lower())
        new_package_id = f"com.convert.app{job_id}"

        # Sadece AndroidManifest.xml içindeki ana paket adını hedef alıyoruz
        manifest_path = os.path.join(temp_folder, 'AndroidManifest.xml')
        if os.path.exists(manifest_path):
            with open(manifest_path, 'r', encoding='utf-8') as f:
                content = f.read()
            # Paket adını güvenli bir regex ile değiştiriyoruz
            content = re.sub(r'package="[a-zA-Z0-9._]*"', f'package="{new_package_id}"', content)
            with open(manifest_path, 'w', encoding='utf-8') as f:
                f.write(content)

        # 3. GÜVENLİ LOGO GÜNCELLEME
        # Hata almamak için sadece en yaygın kullanılan klasördeki logoyu değiştiriyoruz
        if logo_file:
            res_path = os.path.join(temp_folder, 'res', 'mipmap-xxxhdpi')
            if not os.path.exists(res_path):
                # Eğer klasör yoksa bir alt seviyeyi dene
                res_path = os.path.join(temp_folder, 'res', 'drawable-xxhdpi')
            
            if os.path.exists(res_path):
                target_logo = os.path.join(res_path, 'ic_launcher.png')
                logo_file.seek(0)
                logo_file.save(target_logo)

        # 4. UYGULAMA İSMİ GÜNCELLEME
        strings_path = os.path.join(temp_folder, 'res', 'values', 'strings.xml')
        if os.path.exists(strings_path):
            with open(strings_path, 'r', encoding='utf-8') as f:
                content = f.read()
            content = content.replace('WebWrapperBase', app_name)
            with open(strings_path, 'w', encoding='utf-8') as f:
                f.write(content)

        # 5. İNŞA VE İMZALAMA
        safe_name = app_name.replace(" ", "_")
        apk_unsigned = os.path.join(OUTPUT_DIR, f"{job_id}_u.apk")
        apk_signed = os.path.join(OUTPUT_DIR, f"{safe_name}.apk")
        
        # Build (Hata almamak için -f kullanıyoruz ama dosya silmiyoruz)
        subprocess.run(["apktool", "b", temp_folder, "-o", apk_unsigned, "-f"], check=True)
        
        # İmzalama
        subprocess.run(["apksigner", "sign", "--ks", KEYSTORE_PATH, "--ks-pass", f"pass:{KEY_PASS}", "--out", apk_signed, apk_unsigned], check=True)

        # Temizlik
        shutil.rmtree(temp_folder)
        if os.path.exists(apk_unsigned):
            os.remove(apk_unsigned)
        
        return f"""
        <div style="text-align:center; padding:100px; font-family:sans-serif; background:#fff;">
            <h2 style="font-weight:800;">✓ Build Completed Successfully</h2>
            <p>Application: <b>{app_name}</b></p>
            <a href="/download/{safe_name}.apk" style="display:inline-block; background:#000; color:#fff; padding:15px 35px; text-decoration:none; border-radius:10px; font-weight:600; margin-top:20px;">
                Download APK
            </a>
        </div>
        """

    except Exception as e:
        return f"<h1>Build System Error:</h1><pre>{str(e)}</pre>"

@app.route('/download/<filename>')
def download(filename):
    return send_file(os.path.join(OUTPUT_DIR, filename), as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
