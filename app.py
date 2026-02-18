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

# Template'in GERÇEK Orijinal Paket Adı (Hata görüntüsünden aldım)
OLD_PACKAGE_NAME = "com.alperenkilic.webwrapperbase"

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

@app.route('/')
def home():
    return render_template('index.html')

# --- KRİTİK FONKSİYON ---
def smart_manifest_fix(manifest_path, old_package, new_package):
    """
    1. Kodun yerini kaybetmemesi için Activity yollarını 'Tam Yol'a çevirir.
    2. Paket adını değiştirir.
    3. Authority çakışmasını önler.
    """
    with open(manifest_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # ADIM 1: Nokta ile başlayan Activity isimlerini, ESKİ paket adıyla birleştir.
    # Örn: android:name=".MainActivity" -> android:name="com.alperenkilic.webwrapperbase.MainActivity"
    # Böylece biz paket adını değiştirsek bile, sistem kodları eski yerde bulabilir.
    def expand_relative_name(match):
        attr = match.group(1) # android:name
        val = match.group(2)  # .MainActivity
        if val.startswith('.'):
            return f'{attr}="{old_package}{val}"'
        return match.group(0)

    # Activity, Service, Receiver, Provider etiketlerini düzelt
    content = re.sub(r'(android:name)="(\.[^"]*)"', expand_relative_name, content)

    # ADIM 2: Provider Authorities (Çakışma Önleyici)
    # Eğer authorities="com.alperenkilic..." varsa onu yeni paket yap ki diğer uygulamalarla çakışmasın
    content = content.replace(f'android:authorities="{old_package}', f'android:authorities="{new_package}')

    # ADIM 3: Ana Paket Adını Değiştir (Kimlik Değişimi)
    # package="com.alperenkilic..." -> package="com.yeni.id..."
    content = re.sub(rf'package="{re.escape(old_package)}"', f'package="{new_package}"', content)

    with open(manifest_path, 'w', encoding='utf-8') as f:
        f.write(content)

# --- ANA BUILD ---

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

        # 2. YENİ PAKET ADI
        safe_suffix = re.sub(r'[^a-z0-9]', '', app_name.lower())[:10]
        # Paket adı: com.convert.v{job_id}.{isim}
        new_package_id = f"com.convert.v{job_id}.{safe_suffix}"

        # 3. MANIFEST DÜZELTME (Maskeleme Yöntemi)
        manifest_path = os.path.join(temp_folder, 'AndroidManifest.xml')
        smart_manifest_fix(manifest_path, OLD_PACKAGE_NAME, new_package_id)
        
        # ÖNEMLİ: Smali dosyalarına DOKUNMUYORUZ! Kodlar olduğu gibi kalsın.
        # Bu sayede "Class Not Found" veya çökme hatası almayacağız.

        # 4. APKTOOL.YML TEMİZLİĞİ
        # Biz manifest'i hallettik, apktool karışmasın.
        yml_path = os.path.join(temp_folder, 'apktool.yml')
        if os.path.exists(yml_path):
            with open(yml_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            # renameManifestPackage satırını sil
            new_lines = [line for line in lines if "renameManifestPackage" not in line]
            with open(yml_path, 'w', encoding='utf-8') as f:
                f.writelines(new_lines)

        # 5. KAYNAK VE LOGO YÖNETİMİ
        res_path = os.path.join(temp_folder, 'res')
        
        # Public.xml İmhası (Şart)
        public_xml = os.path.join(temp_folder, 'res', 'values', 'public.xml')
        if os.path.exists(public_xml):
            os.remove(public_xml)

        if logo_file:
            # İkon klasörlerini temizle (values-v26'ya dokunmadan)
            for root, dirs, files in os.walk(res_path, topdown=False):
                folder_name = os.path.basename(root)
                if ("mipmap" in folder_name or "drawable" in folder_name) and ("anydpi" in folder_name or "v26" in folder_name):
                    shutil.rmtree(root)

            # Logoyu kaydet ve dağıt
            temp_logo_path = os.path.join(temp_folder, 'temp_logo.png')
            logo_file.save(temp_logo_path)
            
            for root, dirs, files in os.walk(res_path):
                if "mipmap" in os.path.basename(root):
                    for file in files:
                        if file.startswith("ic_launcher"):
                            os.remove(os.path.join(root, file))
                    shutil.copy(temp_logo_path, os.path.join(root, "ic_launcher.png"))
                    shutil.copy(temp_logo_path, os.path.join(root, "ic_launcher_round.png"))

        # 6. UYGULAMA İSMİ
        strings_path = os.path.join(temp_folder, 'res', 'values', 'strings.xml')
        if os.path.exists(strings_path):
            with open(strings_path, 'r', encoding='utf-8') as f:
                content = f.read()
            content = content.replace('WebWrapperBase', app_name)
            with open(strings_path, 'w', encoding='utf-8') as f:
                f.write(content)

        # 7. BUILD, ALIGN & SIGN
        safe_name = re.sub(r'[^a-zA-Z0-9_]', '', app_name.replace(" ", "_"))
        apk_unsigned = os.path.join(OUTPUT_DIR, f"{job_id}_u.apk")
        apk_aligned = os.path.join(OUTPUT_DIR, f"{job_id}_a.apk")
        apk_signed = os.path.join(OUTPUT_DIR, f"{safe_name}.apk")
        
        # Build (--use-aapt2)
        build_cmd = ["apktool", "b", temp_folder, "-o", apk_unsigned, "-f", "--use-aapt2"]
        result = subprocess.run(build_cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise Exception(f"APKTOOL ERROR:\n{result.stderr}")

        # Zipalign
        try:
            subprocess.run(["zipalign", "-p", "-f", "-v", "4", apk_unsigned, apk_aligned], check=True, capture_output=True)
            target_to_sign = apk_aligned
        except:
            target_to_sign = apk_unsigned

        # Sign
        sign_cmd = ["apksigner", "sign", "--ks", KEYSTORE_PATH, "--ks-pass", f"pass:{KEY_PASS}", "--out", apk_signed, target_to_sign]
        sign_result = subprocess.run(sign_cmd, capture_output=True, text=True)
        
        if sign_result.returncode != 0:
            raise Exception(f"SIGNING ERROR:\n{sign_result.stderr}")

        # Temizlik
        if os.path.exists(temp_folder):
             shutil.rmtree(temp_folder)
        if os.path.exists(apk_unsigned):
             os.remove(apk_unsigned)
        if os.path.exists(apk_aligned):
             os.remove(apk_aligned)
        
        return f"""
        <div style="text-align:center; padding:100px; font-family:sans-serif; background:#fff;">
            <h1 style="color:green; font-size:60px;">✅</h1>
            <h2 style="font-weight:800;">APP READY!</h2>
            <p>ID: {new_package_id}</p>
            <p style="color:#666;">Stable Release (No Smali Mod)</p>
            <a href="/download/{safe_name}.apk" style="display:inline-block; background:#000; color:#fff; padding:15px 35px; text-decoration:none; border-radius:10px; font-weight:600; margin-top:20px;">
                Download APK
            </a>
        </div>
        """

    except Exception as e:
        return f"""
        <div style="padding:40px; font-family:monospace; background:#f8d7da; color:#721c24;">
            <h2>💥 CRITICAL ERROR</h2>
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
