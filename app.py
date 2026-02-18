import os, shutil, subprocess, uuid, re
import yaml # YAML işlemleri için (Eğer hata verirse pip install pyyaml gerekir ama text olarak da halledebiliriz)
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
        
        # 1. Kopyalama
        source_path = TEMPLATE_DL if app_type == 'downloader' else TEMPLATE_STD
        shutil.copytree(source_path, temp_folder)

        # --- YENİ STRATEJİ BAŞLIYOR ---

        # 2. PAKET ADI DEĞİŞİMİ (APKTOOL.YML YÖNTEMİ)
        # Manifest'i regex ile bozmak yerine apktool.yml dosyasına talimat veriyoruz.
        # Bu sayede "Exit Status 1" hatası almıyoruz çünkü iç referanslar bozulmuyor.
        
        safe_suffix = re.sub(r'[^a-z0-9]', '', app_name.lower())[:10]
        new_package_id = f"com.convert.app{job_id}.{safe_suffix}"
        
        yml_path = os.path.join(temp_folder, 'apktool.yml')
        if os.path.exists(yml_path):
            with open(yml_path, 'r', encoding='utf-8') as f:
                yml_content = f.read()
            
            # Eğer zaten renameManifestPackage varsa değiştir, yoksa ekle
            if "renameManifestPackage:" in yml_content:
                yml_content = re.sub(r'renameManifestPackage:.*', f'renameManifestPackage: {new_package_id}', yml_content)
            else:
                # Dosyanın sonuna değil, versionInfo'nun altına veya en başa eklemek daha güvenli
                yml_content = f"renameManifestPackage: {new_package_id}\n" + yml_content
                
            with open(yml_path, 'w', encoding='utf-8') as f:
                f.write(yml_content)

        # 3. LOGO DEVRİMİ (Adaptive Icon Temizliği)
        # Android'in vektör ikonlarını siliyoruz, PNG'mizi kral ilan ediyoruz.
        if logo_file:
            res_path = os.path.join(temp_folder, 'res')
            
            # A) Düşman klasörleri yok et (XML ikonları)
            for root, dirs, files in os.walk(res_path, topdown=False):
                if "anydpi" in root or "v26" in root:
                    shutil.rmtree(root)
            
            # B) Logoyu kaydet ve tüm mipmap klasörlerine dağıt
            # Önce logoyu geçici olarak kaydet
            temp_logo_path = os.path.join(temp_folder, 'temp_logo.png')
            logo_file.save(temp_logo_path)
            
            # Tüm mipmap klasörlerini bul ve logoyu oraya kopyala
            for root, dirs, files in os.walk(res_path):
                if "mipmap" in os.path.basename(root):
                    # Hedef dosya yolu
                    target = os.path.join(root, "ic_launcher.png")
                    # Python ile dosyayı kopyala (resim işleme yapmadan direkt copy)
                    shutil.copy(temp_logo_path, target)
                    
                    # Varsa round ikonu da değiştir ki kare çıkmasın
                    target_round = os.path.join(root, "ic_launcher_round.png")
                    shutil.copy(temp_logo_path, target_round)

        # 4. UYGULAMA İSMİ (Strings.xml)
        strings_path = os.path.join(temp_folder, 'res', 'values', 'strings.xml')
        if os.path.exists(strings_path):
            with open(strings_path, 'r', encoding='utf-8') as f:
                content = f.read()
            content = content.replace('WebWrapperBase', app_name)
            with open(strings_path, 'w', encoding='utf-8') as f:
                f.write(content)

        # 5. BUILD & SIGN (Temiz Build)
        safe_name = app_name.replace(" ", "_")
        apk_unsigned = os.path.join(OUTPUT_DIR, f"{job_id}_u.apk")
        apk_signed = os.path.join(OUTPUT_DIR, f"{safe_name}.apk")
        
        # -f: Force overwrite, --use-aapt2: Bazen daha kararlıdır (opsiyonel)
        subprocess.run(["apktool", "b", temp_folder, "-o", apk_unsigned, "-f"], check=True)
        
        # İmzalama
        subprocess.run(["apksigner", "sign", "--ks", KEYSTORE_PATH, "--ks-pass", f"pass:{KEY_PASS}", "--out", apk_signed, apk_unsigned], check=True)

        # Temizlik
        sh
