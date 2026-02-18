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

# Eski paket adı (Template'in orijinal paket adı)
# BURASI ÇOK ÖNEMLİ: Senin template'in orijinal paket adı neyse buraya onu yazmalısın.
# Genellikle 'com.example.template' veya 'com.converttoapk.webwrapperbase' olabilir.
# Eğer bilmiyorsan, source/standard_klasor/AndroidManifest.xml dosyasını açıp package="...." kısmına bak.
# Şimdilik varsayılan olarak 'com.example.template' koyuyorum, eğer farklıysa HATA VERİR.
OLD_PACKAGE_NAME = "com.alperenkilic.webwrapperbase" 

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

@app.route('/')
def home():
    return render_template('index.html')

# --- CLAUDE'UN ÖZEL FONKSİYONLARI ---

def fix_manifest(manifest_path, old_package, new_package):
    """
    1. Relative activity/service path'lerini absolute'a çevirir
    2. Paket adını değiştirir
    """
    with open(manifest_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Relative path'leri absolute'a çevir (.MainActivity -> com.old.MainActivity)
    # Bu sayede paket adı değişince linkler kopmaz.
    def expand_relative_name(match):
        attr_name = match.group(1) # android:name
        value = match.group(2)     # .MainActivity
        if value.startswith('.'):
            return f'{attr_name}="{old_package}{value}"'
        return match.group(0)

    content = re.sub(r'(android:name)="(\.[^"]*)"', expand_relative_name, content)

    # 2. Paket adını değiştir
    content = content.replace(f'package="{old_package}"', f'package="{new_package}"')
    
    # 3. İçerikteki eski paket referanslarını yenisiyle değiştir (Provider, Authority vb.)
    content = content.replace(old_package, new_package)

    with open(manifest_path, 'w', encoding='utf-8') as f:
        f.write(content)

def fix_smali_files(project_dir, old_package, new_package):
    """
    Smali dosyalarının içindeki Lcom/old/package; referanslarını Lcom/new/package; yapar.
    Klasörleri taşımaz, sadece içeriği değiştirir.
    """
    old_smali = old_package.replace('.', '/')
    new_smali = new_package.replace('.', '/')
    
    # smali, smali_classes2, vb. klasörleri bul
    smali_dirs = [d for d in os.listdir(project_dir) if d.startswith('smali')]

    for smali_dir in smali_dirs:
        smali_path = os.path.join(project_dir, smali_dir)
        for root, dirs, files in os.walk(smali_path):
            for filename in files:
                if filename.endswith('.smali'):
                    filepath = os.path.join(root, filename)
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                    
                    if old_smali in content:
                        content = content.replace(old_smali, new_smali)
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(content)

def fix_res_files(project_dir, old_package, new_package):
    """
    Layout ve XML dosyalarındaki eski paket referanslarını günceller.
    """
    res_path = os.path.join(project_dir, 'res')
    if not os.path.exists(res_path): return

    for root, dirs, files in os.walk(res_path):
        for filename in files:
            if filename.endswith('.xml'):
                filepath = os.path.join(root, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                    if old_package in content:
                        content = content.replace(old_package, new_package)
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(content)
                except: pass

def clean_apktool_yml(project_dir):
    """
    apktool.yml içindeki renameManifestPackage satırını siler.
    Çünkü biz manifest'i manuel düzelttik, apktool karışmasın.
    """
    yml_path = os.path.join(project_dir, 'apktool.yml')
    if os.path.exists(yml_path):
        with open(yml_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        new_lines = [line for line in lines if "renameManifestPackage" not in line]
        
        with open(yml_path, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)

# --- ANA BUILD FONKSİYONU ---

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
             return f"<h1>Error:</h1><p>Template not found at {source_path}</p>"
        shutil.copytree(source_path, temp_folder)

        # 2. YENİ PAKET ADI OLUŞTURMA
        safe_suffix = re.sub(r'[^a-z0-9]', '', app_name.lower())[:10]
        # Paket adı: com.convert.v{job_id}.{isim}
        new_package_id = f"com.convert.v{job_id}.{safe_suffix}"

        # 3. CLAUDE'UN 4 KATMANLI STRATEJİSİ
        # A) Manifest Düzeltme
        manifest_path = os.path.join(temp_folder, 'AndroidManifest.xml')
        fix_manifest(manifest_path, OLD_PACKAGE_NAME, new_package_id)
        
        # B) Smali Düzeltme (Kod referansları)
        fix_smali_files(temp_folder, OLD_PACKAGE_NAME, new_package_id)
        
        # C) Resource Düzeltme (Layout referansları)
        fix_res_files(temp_folder, OLD_PACKAGE_NAME, new_package_id)
        
        # D) Apktool.yml Temizliği
        clean_apktool_yml(temp_folder)

        # 4. LOGO VE KAYNAK YÖNETİMİ
        res_path = os.path.join(temp_folder, 'res')
        
        # Public.xml İmhası (Build hatasını önler)
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

        # 5. UYGULAMA İSMİ
        strings_path = os.path.join(temp_folder, 'res', 'values', 'strings.xml')
        if os.path.exists(strings_path):
            with open(strings_path, 'r', encoding='utf-8') as f:
                content = f.read()
            content = content.replace('WebWrapperBase', app_name)
            with open(strings_path, 'w', encoding='utf-8') as f:
                f.write(content)

        # 6. BUILD, ALIGN & SIGN
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
            <h2 style="font-weight:800;">READY TO DEPLOY</h2>
            <p>New Package ID: <b>{new_package_id}</b></p>
            <p style="color:#666;">Converted from: {OLD_PACKAGE_NAME}</p>
            <a href="/download/{safe_name}.apk" style="display:inline-block; background:#000; color:#fff; padding:15px 35px; text-decoration:none; border-radius:10px; font-weight:600; margin-top:20px;">
                Download APK
            </a>
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
