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

        # 2. PAKET ADI DEĞİŞİMİ (KESİN ÇÖZÜM)
        # Önceki kodda 'append' yapıyorduk, bu çift satıra neden olabiliyordu.
        # Şimdi regex ile var olan satırı bulup değiştiriyoruz.
        
        safe_suffix = re.sub(r'[^a-z0-9]', '', app_name.lower())[:10]
        # Her build için tamamen rastgele bir ID (v + job_id)
        new_package_id = f"com.convert.v{job_id}.{safe_suffix}"
        
        yml_path = os.path.join(temp_folder, 'apktool.yml')
        if os.path.exists(yml_path):
            with open(yml_path, 'r', encoding='utf-8') as f:
                yml_content = f.read()
            
            # Eğer 'renameManifestPackage' anahtarı zaten varsa, değerini değiştir
            if "renameManifestPackage:" in yml_content:
                yml_content = re.sub(r'renameManifestPackage:.*', f'renameManifestPackage: {new_package_id}', yml_content)
            else:
                # Yoksa, dosyanın en başına ekle (en güvenli yer)
                yml_content = f"renameManifestPackage: {new_package_id}\n" + yml_content
                
            with open(yml_path, 'w', encoding='utf-8') as f:
                f.write(yml_content)

        # 3. KAYNAK VE LOGO YÖNETİMİ
        res_path = os.path.join(temp_folder, 'res')
        
        if logo_file:
            # A) İkon klasörlerini temizle (values-v26'ya dokunmadan)
            for root, dirs, files in os.walk(res_path, topdown=False):
                folder_name = os.path.basename(root)
                if ("mipmap" in folder_name or "drawable" in folder_name) and ("anydpi" in folder_name or "v26" in folder_name):
                    shutil.rmtree(root)

            # B) Logoyu kaydet ve dağıt
            temp_logo_path = os.path.join(temp_folder, 'temp_logo.png')
            logo_file.save(temp_logo_path)
            
            for root, dirs, files in os.walk(res_path):
                if "mipmap" in os.path.basename(root):
                    # Eski ikonları sil
                    for file in files:
                        if file.startswith("ic_launcher"):
                            os.remove(os.path.join(root, file))
                    # Yenisini koy
                    shutil.copy(temp_logo_path, os.path.join(root, "ic_launcher.png"))
                    shutil.copy(temp_logo_path, os.path.join(root, "ic_launcher_round.png"))

        # 4. PUBLIC.XML İMHASI (Build Hatasını Önlemek İçin Şart)
        public_xml = os.path.join(temp_folder, 'res', 'values', 'public.xml')
        if os.path.exists(public_xml):
            os.remove(public_xml)

        # 5. UYGULAMA İSMİ
        strings_path = os.path.join(temp_folder, 'res', 'values', 'strings.xml')
        if os.path.exists(strings_path):
            with open(strings_path, 'r', encoding='utf-8') as f:
                content = f.read()
            content = content.replace('WebWrapperBase', app_name)
            with open(strings_path, 'w', encoding='utf-8') as f:
                f.write(content)

        # 6. BUILD & SIGN
        safe_name = re.sub(r'[^a-zA-Z0-9_]', '', app_name.replace(" ", "_"))
        apk_unsigned = os.path.join(OUTPUT_DIR, f"{job_id}_u.apk")
        apk_signed = os.path.join(OUTPUT_DIR, f"{safe_name}.apk")
        
        # Build (-f force)
        build_cmd = ["apktool", "b", temp_folder, "-o", apk_unsigned, "-f"]
        result = subprocess.run(build_cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            raise Exception(f"APKTOOL ERROR:\n{result.stderr}")

        # Sign
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
            <h2 style="font-weight:800;">APP READY!</h2>
            <p style="color:#666;">Unique ID: <b>{new_package_id}</b></p>
            <p style="font-size:12px; color:#999;">If phone asks to 'Update', uninstall the old one first.</p>
            <a href="/download/{safe_name}.apk" style="display:inline-block; background:#000; color:#fff; padding:15px 35px; text-decoration:none; border-radius:10px; font-weight:600; margin-top:20px;">
                Download APK
            </a>
            <br><br>
            <a href="/" style="color:#666; text-decoration:none;">← Create Another</a>
        </div>
        """

    except Exception as e:
        return f"""
        <div style="padding:40px; font-family:monospace; background:#f8d7da; color:#721c24;">
            <h2>💥 SYSTEM ERROR</h2>
            <pre style="background:#fff; padding:15px; border:1px solid #000; white-space: pre-wrap;">{str(e)}</pre>
        </div>
        """
    finally:
        if temp_folder and os.path.exists(temp_folder):
             try: shutil.rmtree(temp_folder) 
             except: pass

@app.route('/download/<filename>')
def download(filename):
    return send_file(os.path.join(OUTPUT_DIR, filename), as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
