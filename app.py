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

# Template'in Orijinal Paket Adı (Hata loglarından tespit ettik)
OLD_PACKAGE_NAME = "com.alperenkilic.webwrapperbase"

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

@app.route('/')
def home():
    return render_template('index.html')

def prepare_manifest_paths(manifest_path, old_package):
    """
    Sadece Activity yollarını 'Tam Yol' (Absolute Path) yapar.
    Paket adına DOKUNMAZ. Paket adını apktool değiştirecek.
    Böylece 'Class Not Found' hatası (Çökme) önlenir.
    """
    with open(manifest_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # .MainActivity -> com.alperenkilic.webwrapperbase.MainActivity
    def expand_relative_name(match):
        attr = match.group(1) 
        val = match.group(2)
        if val.startswith('.'):
            return f'{attr}="{old_package}{val}"'
        return match.group(0)

    # Activity, Service, Receiver yollarını düzelt
    content = re.sub(r'(android:name)="(\.[^"]*)"', expand_relative_name, content)
    
    with open(manifest_path, 'w', encoding='utf-8') as f:
        f.write(content)

def inject_apktool_yml(yml_path, new_package_id):
    """
    apktool.yml dosyasını güvenli bir şekilde günceller.
    renameManifestPackage komutunu dosyanın sonuna ekler.
    """
    with open(yml_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Eski renameManifestPackage satırlarını temizle
    clean_lines = [line for line in lines if "renameManifestPackage" not in line]
    
    # En sona yeni paket adını ekle (YAML formatına uygun)
    # isFrameworkApk: false ekleyerek derleme hatasını önlüyoruz
    clean_lines.append(f"\nrenameManifestPackage: {new_package_id}\n")
    
    with open(yml_path, 'w', encoding='utf-8') as f:
        f.writelines(clean_lines)

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
        shutil.copytree(source_path, temp_folder)

        # 2. TEMİZLİK (Eski Build Kalıntılarını Sil)
        # Apktool'un kafasının karışmaması için şart!
        build_cache = os.path.join(temp_folder, 'build')
        dist_cache = os.path.join(temp_folder, 'dist')
        if os.path.exists(build_cache): shutil.rmtree(build_cache)
        if os.path.exists(dist_cache): shutil.rmtree(dist_cache)

        # 3. YENİ KİMLİK OLUŞTURMA
        safe_suffix = re.sub(r'[^a-z0-9]', '', app_name.lower())[:10]
        new_package_id = f"com.convert.v{job_id}.{safe_suffix}"

        # 4. ÇİFTE STRATEJİ
        # A) Manifest: Kod yollarını sabitle (Çökme Önleyici)
        manifest_path = os.path.join(temp_folder, 'AndroidManifest.xml')
        prepare_manifest_paths(manifest_path, OLD_PACKAGE_NAME)
        
        # B) YAML: Kimliği değiştir (Güncelleme Sorunu Çözücü)
        yml_path = os.path.join(temp_folder, 'apktool.yml')
        inject_apktool_yml(yml_path, new_package_id)

        # 5. KAYNAK & LOGO
        res_path = os.path.join(temp_folder, 'res')
        
        # Public.xml sil (Build hatası önleyici)
        public_xml = os.path.join(temp_folder, 'res', 'values', 'public.xml')
        if os.path.exists(public_xml): os.remove(public_xml)

        if logo_file:
            # Adaptive icon temizliği
            for root, dirs, files in os.walk(res_path, topdown=False):
                folder_name = os.path.basename(root)
                if ("mipmap" in folder_name or "drawable" in folder_name) and ("anydpi" in folder_name or "v26" in folder_name):
                    shutil.rmtree(root)

            # Logo değişimi
            temp_logo_path = os.path.join(temp_folder, 'temp_logo.png')
            logo_file.save(temp_logo_path)
            for root, dirs, files in os.walk(res_path):
                if "mipmap" in os.path.basename(root):
                    for file in files:
                        if file.startswith("ic_launcher"):
                            os.remove(os.path.join(root, file))
                    shutil.copy(temp_logo_path, os.path.join(root, "ic_launcher.png"))
                    shutil.copy(temp_logo_path, os.path.join(root, "ic_launcher_round.png"))

        # 6. APP NAME
        strings_path = os.path.join(temp_folder, 'res', 'values', 'strings.xml')
        if os.path.exists(strings_path):
            with open(strings_path, 'r', encoding='utf-8') as f:
                content = f.read()
            content = content.replace('WebWrapperBase', app_name)
            with open(strings_path, 'w', encoding='utf-8') as f:
                f.write(content)

        # 7. BUILD & SIGN
        safe_name = re.sub(r'[^a-zA-Z0-9_]', '', app_name.replace(" ", "_"))
        apk_unsigned = os.path.join(OUTPUT_DIR, f"{job_id}_u.apk")
        apk_aligned = os.path.join(OUTPUT_DIR, f"{job_id}_a.apk")
        apk_signed = os.path.join(OUTPUT_DIR, f"{safe_name}.apk")
        
        # Build (--use-aapt2)
        build_cmd = ["apktool", "b", temp_folder, "-o", apk_unsigned, "-f", "--use-aapt2"]
        result = subprocess.run(build_cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise Exception(f"APKTOOL ERROR:\n{result.stderr}")

        # Zipalign (Parse hatasını önler)
        try:
            subprocess.run(["zipalign", "-p", "-f", "-v", "4", apk_unsigned, apk_aligned], check=True, capture_output=True)
            target_to_sign = apk_aligned
        except:
            # Zipalign yoksa devam et (Loglarda uyarı olarak kalsın)
            target_to_sign = apk_unsigned

        # Sign
        sign_cmd = ["apksigner", "sign", "--ks", KEYSTORE_PATH, "--ks-pass", f"pass:{KEY_PASS}", "--out", apk_signed, target_to_sign]
        sign_result = subprocess.run(sign_cmd, capture_output=True, text=True)
        if sign_result.returncode != 0:
            raise Exception(f"SIGNING ERROR:\n{sign_result.stderr}")

        # Cleanup
        if os.path.exists(temp_folder): shutil.rmtree(temp_folder)
        if os.path.exists(apk_unsigned): os.remove(apk_unsigned)
        if os.path.exists(apk_aligned): os.remove(apk_aligned)
        
        return f"""
        <div style="text-align:center; padding:100px; font-family:sans-serif; background:#fff;">
            <h1 style="color:green; font-size:60px;">✅</h1>
            <h2 style="font-weight:800;">READY TO INSTALL</h2>
            <p>ID: {new_package_id}</p>
            <a href="/download/{safe_name}.apk" style="display:inline-block; background:#000; color:#fff; padding:15px 35px; text-decoration:none; border-radius:10px; font-weight:600; margin-top:20px;">
                Download APK
            </a>
        </div>
        """

    except Exception as e:
        return f"""
        <div style="padding:40px; font-family:monospace; background:#f8d7da; color:#721c24;">
            <h2>💥 BUILD ERROR</h2>
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
