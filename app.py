import os, shutil, subprocess, uuid, re, random
from flask import Flask, render_template, request, send_file

app = Flask(__name__)

# --- Configuration ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_STD = os.path.join(BASE_DIR, 'source', 'standard_klasor')
TEMPLATE_DL = os.path.join(BASE_DIR, 'source', 'downloader_klasor')
OUTPUT_DIR = os.path.join(BASE_DIR, 'output')
KEYSTORE_PATH = os.path.join(BASE_DIR, 'yeni.jks')
KEY_PASS = "123456" 

# Template'in Orijinal Paket Adı (Bunu değiştireceğiz)
OLD_PACKAGE_NAME = "com.alperenkilic.webwrapperbase"

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

@app.route('/')
def home():
    return render_template('index.html')

def nuclear_replace(project_dir, old_pkg, new_pkg):
    """
    Bu fonksiyon projedeki HER DOSYAYI açar ve eski paket adını yeniyle değiştirir.
    Manifest, Smali, XML, Resource... Hiçbir şey kaçmaz.
    """
    old_path = old_pkg.replace('.', '/') # com/alperenkilic/webwrapperbase
    new_path = new_pkg.replace('.', '/') # com/convert/v123456

    # 1. DOSYA İÇERİKLERİNİ DEĞİŞTİR (Content Replace)
    # Manifest, Layouts, Strings, Smali Code...
    for root, dirs, files in os.walk(project_dir):
        for filename in files:
            # Sadece metin tabanlı dosyaları işle (Resimlere dokunma)
            if filename.endswith(('.xml', '.smali', '.yml', '.txt', '.html', '.java')):
                filepath = os.path.join(root, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                    
                    # Eğer eski paket adı varsa değiştir
                    if old_pkg in content or old_path in content:
                        # com.alperenkilic -> com.convert
                        content = content.replace(old_pkg, new_pkg)
                        # com/alperenkilic -> com/convert (Smali için)
                        content = content.replace(old_path, new_path)
                        
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(content)
                except:
                    pass

    # 2. SMALI KLASÖRLERİNİ FİZİKSEL TAŞI (Folder Move)
    # Bu adım 'resources.arsc' çakışmasını ve 'Parse Error'ı önler.
    smali_dirs = [d for d in os.listdir(project_dir) if d.startswith('smali')]
    
    for smali_dir in smali_dirs:
        base_smali = os.path.join(project_dir, smali_dir)
        old_dir = os.path.join(base_smali, old_path)
        new_dir = os.path.join(base_smali, new_path)

        if os.path.exists(old_dir):
            # Hedef klasörü oluştur
            os.makedirs(os.path.dirname(new_dir), exist_ok=True)
            
            # Eski klasörü yeni yere taşı
            if os.path.exists(new_dir):
                # Çakışma varsa içindekileri taşı
                for item in os.listdir(old_dir):
                    shutil.move(os.path.join(old_dir, item), new_dir)
                shutil.rmtree(old_dir)
            else:
                # Direkt taşı
                shutil.move(old_dir, new_dir)
            
            # Arkada kalan boş klasörleri temizle (com/alperenkilic boş kaldıysa sil)
            try:
                parent = os.path.dirname(old_dir) # webwrapperbase silindi, alperenkilic'e bak
                if not os.listdir(parent): os.rmdir(parent)
                grandparent = os.path.dirname(parent) # com'a bak
                if not os.listdir(grandparent): os.rmdir(grandparent)
            except:
                pass

def clean_apktool_yml(yml_path):
    """Apktool.yml ayarları."""
    if not os.path.exists(yml_path): return
    with open(yml_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    new_lines = []
    for line in lines:
        if "renameManifestPackage" in line: continue # Biz manuel yaptık
        if "versionCode:" in line:
            new_lines.append(f"  versionCode: '{random.randint(1000, 99999)}'\n")
        else:
            new_lines.append(line)
    
    with open(yml_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

@app.route('/build', methods=['POST'])
def build_apk():
    temp_folder = None
    try:
        app_name = request.form.get('app_name')
        app_type = request.form.get('app_type')
        logo_file = request.files.get('logo')
        
        # Her uygulama için BENZERSİZ BİR ID
        job_id = str(uuid.uuid4())[:8]
        temp_folder = os.path.join(OUTPUT_DIR, job_id)
        
        # 1. Kopyalama
        source_path = TEMPLATE_DL if app_type == 'downloader' else TEMPLATE_STD
        shutil.copytree(source_path, temp_folder)

        # 2. Temizlik (Eski build artıkları)
        for item in ['build', 'dist', 'META-INF']:
            path = os.path.join(temp_folder, item)
            if os.path.exists(path): shutil.rmtree(path)

        # 3. YENİ KİMLİK BELİRLEME
        # Her harf benzersiz olsun
        safe_suffix = re.sub(r'[^a-z0-9]', '', app_name.lower())[:5] + str(random.randint(10,99))
        new_package_id = f"com.convert.v{job_id}.{safe_suffix}"

        # 4. NÜKLEER DEĞİŞİM (Her şeyi değiştir)
        nuclear_replace(temp_folder, OLD_PACKAGE_NAME, new_package_id)

        # 5. YML FIX
        clean_apktool_yml(os.path.join(temp_folder, 'apktool.yml'))

        # 6. KAYNAK & LOGO
        res_path = os.path.join(temp_folder, 'res')
        
        # Public.xml sil (Çok önemli, kaynak çakışmasını önler)
        public_xml = os.path.join(temp_folder, 'res', 'values', 'public.xml')
        if os.path.exists(public_xml): os.remove(public_xml)

        if logo_file:
            # Temizlik
            for root, dirs, files in os.walk(res_path, topdown=False):
                folder_name = os.path.basename(root)
                if ("mipmap" in folder_name or "drawable" in folder_name) and ("anydpi" in folder_name or "v26" in folder_name):
                    shutil.rmtree(root)
            # Logo bas
            temp_logo_path = os.path.join(temp_folder, 'temp_logo.png')
            logo_file.save(temp_logo_path)
            for root, dirs, files in os.walk(res_path):
                if "mipmap" in os.path.basename(root):
                    for file in files:
                        if file.startswith("ic_launcher"): os.remove(os.path.join(root, file))
                    shutil.copy(temp_logo_path, os.path.join(root, "ic_launcher.png"))
                    shutil.copy(temp_logo_path, os.path.join(root, "ic_launcher_round.png"))

        # 7. STRING NAME
        strings_path = os.path.join(temp_folder, 'res', 'values', 'strings.xml')
        if os.path.exists(strings_path):
            with open(strings_path, 'r', encoding='utf-8') as f:
                content = f.read()
            # Eğer nükleer değişimden kurtulan bir yer varsa diye tekrar değiştir
            content = content.replace('WebWrapperBase', app_name)
            with open(strings_path, 'w', encoding='utf-8') as f:
                f.write(content)

        # 8. BUILD & SIGN
        safe_name = re.sub(r'[^a-zA-Z0-9_]', '', app_name.replace(" ", "_"))
        apk_unsigned = os.path.join(OUTPUT_DIR, f"{job_id}_u.apk")
        apk_aligned = os.path.join(OUTPUT_DIR, f"{job_id}_a.apk")
        apk_signed = os.path.join(OUTPUT_DIR, f"{safe_name}.apk")
        
        # Build
        subprocess.run(["apktool", "b", temp_folder, "-o", apk_unsigned, "-f", "--use-aapt2"], check=True)

        # Zipalign
        target_apk = apk_unsigned
        try:
            subprocess.run(["zipalign", "-p", "-f", "-v", "4", apk_unsigned, apk_aligned], check=True)
            target_apk = apk_aligned
        except:
            pass

        # Sign (V1+V2)
        subprocess.run([
            "apksigner", "sign", 
            "--ks", KEYSTORE_PATH, 
            "--ks-pass", f"pass:{KEY_PASS}", 
            "--v1-signing-enabled", "true", 
            "--v2-signing-enabled", "true", 
            "--out", apk_signed, 
            target_apk
        ], check=True)

        # Cleanup
        if os.path.exists(temp_folder): shutil.rmtree(temp_folder)
        if os.path.exists(apk_unsigned): os.remove(apk_unsigned)
        if os.path.exists(apk_aligned): os.remove(apk_aligned)
        
        return f"""
        <div style="text-align:center; padding:100px; font-family:sans-serif; background:#fff;">
            <h1 style="color:green; font-size:60px;">✅</h1>
            <h2 style="font-weight:800;">TOTAL SUCCESS</h2>
            <p>New ID: {new_package_id}</p>
            <p style="color:#666;">This app is completely unique.</p>
            <a href="/download/{safe_name}.apk" style="display:inline-block; background:#000; color:#fff; padding:15px 35px; text-decoration:none; border-radius:10px; font-weight:600; margin-top:20px;">
                Download APK
            </a>
        </div>
        """

    except Exception as e:
        return f"<h1>Error:</h1><pre>{str(e)}</pre>"

@app.route('/download/<filename>')
def download(filename):
    return send_file(os.path.join(OUTPUT_DIR, filename), as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
