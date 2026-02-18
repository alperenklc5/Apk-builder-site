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

# Template'in Orijinal Paket Adı (Hata loglarından tespit ettik - KESİN DOĞRU OLMALI)
OLD_PACKAGE_NAME = "com.alperenkilic.webwrapperbase"

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

@app.route('/')
def home():
    return render_template('index.html')

# --- SMALI & PAKET DÜZELTME MOTORU (Cerrahi Müdahale) ---

def surgical_package_rename(project_dir, old_package, new_package):
    """
    Hem Manifest'i, hem Smali içeriklerini hem de Klasör yapısını değiştirir.
    Bu, 'Parse Error' ve 'Update' sorunlarını aynı anda çözer.
    """
    old_path = old_package.replace('.', '/') # com/eski/paket
    new_path = new_package.replace('.', '/') # com/yeni/paket
    
    # 1. SMALI İÇERİK VE KLASÖR DÜZELTME
    smali_dirs = [d for d in os.listdir(project_dir) if d.startswith('smali')]
    
    for smali_dir in smali_dirs:
        base_dir = os.path.join(project_dir, smali_dir)
        
        # A) İçerik Değiştirme (Referansları güncelle)
        for root, dirs, files in os.walk(base_dir):
            for filename in files:
                if filename.endswith('.smali'):
                    filepath = os.path.join(root, filename)
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                    
                    if old_path in content:
                        content = content.replace(old_path, new_path)
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(content)

        # B) Klasör Taşıma (Fiziksel Konum Değişimi)
        old_dir_full = os.path.join(base_dir, old_path)
        new_dir_full = os.path.join(base_dir, new_path)
        
        if os.path.exists(old_dir_full):
            # Yeni klasör yolunu oluştur
            os.makedirs(os.path.dirname(new_dir_full), exist_ok=True)
            
            # Eğer hedef klasör zaten varsa (nadir durum), içeriği taşı
            if os.path.exists(new_dir_full):
                for item in os.listdir(old_dir_full):
                    shutil.move(os.path.join(old_dir_full, item), new_dir_full)
                shutil.rmtree(old_dir_full) # Eskiyi sil
            else:
                # Direkt klasörü taşı
                shutil.move(old_dir_full, new_dir_full)
            
            # Boş kalan eski klasörleri temizle (örn: com/alperenkilic/webwrapperbase -> com/alperenkilic boş kalabilir)
            # Basitçe eski path'in üst klasörlerini kontrol et
            try:
                os.rmdir(os.path.dirname(old_dir_full)) # webwrapperbase silindi, alperenkilic boş mu?
                os.rmdir(os.path.dirname(os.path.dirname(old_dir_full))) # com boş mu?
            except:
                pass # Doluysa silmez, sorun yok

    # 2. MANIFEST DÜZELTME
    manifest_path = os.path.join(project_dir, 'AndroidManifest.xml')
    with open(manifest_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Paket adını güncelle
    content = content.replace(f'package="{old_package}"', f'package="{new_package}"')
    
    # Provider ve Authority çakışmalarını önle
    content = content.replace(old_package, new_package)
    
    with open(manifest_path, 'w', encoding='utf-8') as f:
        f.write(content)
        
    # 3. RESOURCE (XML) DÜZELTME
    res_path = os.path.join(project_dir, 'res')
    for root, dirs, files in os.walk(res_path):
        for filename in files:
            if filename.endswith('.xml'):
                filepath = os.path.join(root, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        xml_content = f.read()
                    if old_package in xml_content:
                        xml_content = xml_content.replace(old_package, new_package)
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(xml_content)
                except: pass

    # 4. APKTOOL.YML TEMİZLİĞİ
    yml_path = os.path.join(project_dir, 'apktool.yml')
    if os.path.exists(yml_path):
        with open(yml_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        # renameManifestPackage satırını sil (Biz manuel yaptık)
        new_lines = [line for line in lines if "renameManifestPackage" not in line]
        with open(yml_path, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)


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

        # 2. YENİ KİMLİK OLUŞTURMA
        safe_suffix = re.sub(r'[^a-z0-9]', '', app_name.lower())[:10]
        # Paket adı: com.convert.v{job_id}.{isim} (Android standartlarına uygun)
        new_package_id = f"com.convert.v{job_id}.{safe_suffix}"

        # 3. CERRAHİ PAKET DEĞİŞİMİ
        surgical_package_rename(temp_folder, OLD_PACKAGE_NAME, new_package_id)

        # 4. KAYNAK & LOGO
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

        # 5. APP NAME
        strings_path = os.path.join(temp_folder, 'res', 'values', 'strings.xml')
        if os.path.exists(strings_path):
            with open(strings_path, 'r', encoding='utf-8') as f:
                content = f.read()
            content = content.replace('WebWrapperBase', app_name)
            with open(strings_path, 'w', encoding='utf-8') as f:
                f.write(content)

        # 6. BUILD, ALIGN & SIGN (Doğru Sıralama)
        safe_name = re.sub(r'[^a-zA-Z0-9_]', '', app_name.replace(" ", "_"))
        apk_unsigned = os.path.join(OUTPUT_DIR, f"{job_id}_u.apk")
        apk_aligned = os.path.join(OUTPUT_DIR, f"{job_id}_a.apk")
        apk_signed = os.path.join(OUTPUT_DIR, f"{safe_name}.apk")
        
        # A) Apktool Build (--use-aapt2)
        build_cmd = ["apktool", "b", temp_folder, "-o", apk_unsigned, "-f", "--use-aapt2"]
        result = subprocess.run(build_cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise Exception(f"APKTOOL ERROR:\n{result.stderr}")

        # B) Zipalign (Parse hatasını önler - Şart)
        try:
            subprocess.run(["zipalign", "-p", "-f", "-v", "4", apk_unsigned, apk_aligned], check=True, capture_output=True)
            target_to_sign = apk_aligned
        except:
            # Zipalign yoksa unsigned dosyayı kullan (Riskli ama devam eder)
            target_to_sign = apk_unsigned

        # C) Apksigner (En son imza)
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
            <h2 style="font-weight:800;">SUCCESSFULLY BUILT</h2>
            <p>New ID: {new_package_id}</p>
            <p style="color:#666;">Full Package Rename Complete.</p>
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
