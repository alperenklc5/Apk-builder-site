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
        
        # 1. Template Copy
        source_path = TEMPLATE_DL if app_type == 'downloader' else TEMPLATE_STD
        shutil.copytree(source_path, temp_folder)

        # 2. BRAND NEW PACKAGE ID (Avoids "Update" error)
        # Sadece harf ve rakam kullanıyoruz, Android daha çok seviyor.
        clean_name = re.sub(r'[^a-z]', '', app_name.lower())
        new_package_id = f"com.converttoapk.v{job_id}.{clean_name}"

        # AndroidManifest.xml Update
        manifest_path = os.path.join(temp_folder, 'AndroidManifest.xml')
        if os.path.exists(manifest_path):
            with open(manifest_path, 'r', encoding='utf-8') as f:
                content = f.read()
            # Paket adını tüm referanslarıyla beraber değiştiriyoruz
            content = re.sub(r'package="[a-zA-Z0-9._]*"', f'package="{new_package_id}"', content)
            with open(manifest_path, 'w', encoding='utf-8') as f:
                f.write(content)

        # 3. ADVANCED LOGO INJECTION
        if logo_file:
            # Tüm res klasörünü gezip ic_launcher isimli her şeyi eziyoruz
            res_path = os.path.join(temp_folder, 'res')
            for root, dirs, files in os.walk(res_path):
                for filename in files:
                    # Sadece ic_launcher.png olanları değil, xml (vector) olanları da siliyoruz ki çakışmasın
                    if "ic_launcher" in filename:
                        target_file = os.path.join(root, filename)
                        if filename.endswith(".xml"):
                            os.remove(target_file) # Eski vektör logoyu sil
                        elif filename.endswith(".png"):
                            logo_file.seek(0)
                            logo_file.save(target_file) # Kendi logonu yaz

        # 4. APP NAME UPDATE
        strings_path = os.path.join(temp_folder, 'res', 'values', 'strings.xml')
        if os.path.exists(strings_path):
            with open(strings_path, 'r', encoding='utf-8') as f:
                content = f.read()
            content = content.replace('WebWrapperBase', app_name)
            with open(strings_path, 'w', encoding='utf-8') as f:
                f.write(content)

        # 5. BUILD & SIGNING
        safe_name = app_name.replace(" ", "_")
        apk_unsigned = os.path.join(OUTPUT_DIR, f"{job_id}_u.apk")
        apk_signed = os.path.join(OUTPUT_DIR, f"{safe_name}.apk")
        
        # Apktool ile inşa (f parametresi eski kalıntıları siler)
        subprocess.run(["apktool", "b", temp_folder, "-o", apk_unsigned, "-f"], check=True)
        
        # İmzalama
        subprocess.run(["apksigner", "sign", "--ks", KEYSTORE_PATH, "--ks-pass", f"pass:{KEY_PASS}", "--out", apk_signed, apk_unsigned], check=True)

        # Cleanup
        shutil.rmtree(temp_folder)
        if os.path.exists(apk_unsigned):
            os.remove(apk_unsigned)
        
        return f"""
        <div style="text-align:center; padding:100px; font-family:sans-serif; background:#fff;">
            <h1>✅ Build Success</h1>
            <p>Your unique app <b>{app_name}</b> is ready.</p>
            <a href="/download/{safe_name}.apk" style="display:inline-block; background:#000; color:#fff; padding:15px 35px; text-decoration:none; border-radius:10px; font-weight:600; margin-top:30px;">
                Download APK
            </a>
        </div>
        """

    except Exception as e:
        return f"<h1>Build Error:</h1><p>{str(e)}</p>"

@app.route('/download/<filename>')
def download(filename):
    return send_file(os.path.join(OUTPUT_DIR, filename), as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
