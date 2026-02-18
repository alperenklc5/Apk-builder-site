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
    temp_folder = None
    try:
        app_name = request.form.get('app_name')
        app_type = request.form.get('app_type')
        logo_file = request.files.get('logo')
        
        job_id = str(uuid.uuid4())[:8]
        temp_folder = os.path.join(OUTPUT_DIR, job_id)
        
        # 1. Kopyalama
        source_path = TEMPLATE_DL if app_type == 'downloader' else TEMPLATE_STD
        if not os.path.exists(source_path):
             return f"<h1>Critical Error:</h1><p>Source template not found: {source_path}</p>"
        shutil.copytree(source_path, temp_folder)

        # 2. PAKET ADI DEĞİŞİMİ (YAML Güvenli Mod)
        # İsmi sadeleştir
        safe_suffix = re.sub(r'[^a-z0-9]', '', app_name.lower())[:15]
        new_package_id = f"com.convert.app{job_id}.{safe_suffix}"
        
        yml_path = os.path.join(temp_folder, 'apktool.yml')
        if os.path.exists(yml_path):
            with open(yml_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            # YAML'ı satır satır tara, eski renameManifestPackage varsa sil
            new_lines = [line for line in lines if "renameManifestPackage" not in line]
            
            # En sona temiz bir şekilde ekle
            new_lines.append(f"\nrenameManifestPackage: {new_package_id}\n")
            
            with open(yml_path, 'w', encoding='utf-8') as f:
                f.writelines(new_lines)

        # 3. LOGO TEMİZLİĞİ (Resources)
        if logo_file:
            res_path = os.path.join(temp_folder, 'res')
            
            # A) Adaptive Icon klasörlerini sil (Vektör çakışmasını önle)
            for root, dirs, files in os.walk(res_path, topdown=False):
                if "anydpi" in root or "v26" in root:
                    shutil.rmtree(root)
            
            # B) Logoyu kaydet
            temp_logo_path = os.path.join(temp_folder, 'temp_logo.png')
            logo_file.save(temp_logo_path)
            
            # C) Mipmap klasörlerine dağıt
            for root, dirs, files in os.walk(res_path):
                if "mipmap" in os.path.basename(root):
                    shutil.copy(temp_logo_path, os.path.join(root, "ic_launcher.png"))
                    # Varsa round ikonu da değiştir
                    if os.path.exists(os.path.join(root, "ic_launcher_round.png")):
                        shutil.copy(temp_logo_path, os.path.join(root, "ic_launcher_round.png"))

        # 4. UYGULAMA İSMİ
        strings_path = os.path.join(temp_folder, 'res', 'values', 'strings.xml')
        if os.path.exists(strings_path):
            with open(strings_path, 'r', encoding='utf-8') as f:
                content = f.read()
            content = content.replace('WebWrapperBase', app_name)
            with open(strings_path, 'w', encoding='utf-8') as f:
                f.write(content)

        # 5. BUILD & SIGN (LOGLAMA AÇIK)
        safe_name = re.sub(r'[^a-zA-Z0-9_]', '', app_name.replace(" ", "_"))
        apk_unsigned = os.path.join(OUTPUT_DIR, f"{job_id}_u.apk")
        apk_signed = os.path.join(OUTPUT_DIR, f"{safe_name}.apk")
        
        # Build Komutu - capture_output=True ile hatayı yakalıyoruz
        build_cmd = ["apktool", "b", temp_folder, "-o", apk_unsigned, "-f"]
        result = subprocess.run(build_cmd, capture_output=True, text=True)
        
        # Eğer build başarısızsa, stderr çıktısını döndür (BİZE LAZIM OLAN BU)
        if result.returncode != 0:
            raise Exception(f"APKTOOL ERROR:\n{result.stderr}\n\nSTDOUT:\n{result.stdout}")

        # Sign Komutu
        sign_cmd = ["apksigner", "sign", "--ks", KEYSTORE_PATH, "--ks-pass", f"pass:{KEY_PASS}", "--out", apk_signed, apk_unsigned]
        sign_result = subprocess.run(sign_cmd, capture_output=True, text=True)
        
        if sign_result.returncode != 0:
            raise Exception(f"SIGNING ERROR:\n{sign_result.stderr}")

        # Temizlik
        if os.path.exists(temp_folder):
            shutil.rmtree(temp_folder)
        if os.path.exists(apk_unsigned):
            os.remove(apk_unsigned)
        
        return f"""
        <div style="text-align:center; padding:100px; font-family:sans-serif; background:#fff;">
            <h1 style="color:green; font-size:60px;">✅</h1>
            <h2 style="font-weight:800;">SUCCESS!</h2>
            <p>ID: {new_package_id}</p>
            <a href="/download/{safe_name}.apk" style="display:inline-block; background:#000; color:#fff; padding:15px 35px; text-decoration:none; border-radius:10px; font-weight:600; margin-top:20px;">
                Download APK
            </a>
        </div>
        """

    except Exception as e:
        # Hatayı ekrana formatlı bas
        return f"""
        <div style="padding:40px; font-family:monospace; background:#f8d7da; color:#721c24;">
            <h2>💥 BUILD FAILED</h2>
            <p>Hata Detayı (Bunu bana gönder):</p>
            <pre style="background:#fff; padding:15px; border:1px solid #000; white-space: pre-wrap;">{str(e)}</pre>
        </div>
        """
    finally:
        # Temp klasörü temizle (opsiyonel, debug için kapatabilirsin)
        if temp_folder and os.path.exists(temp_folder):
             try: shutil.rmtree(temp_folder) 
             except: pass

@app.route('/download/<filename>')
def download(filename):
    return send_file(os.path.join(OUTPUT_DIR, filename), as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
