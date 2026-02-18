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

# Template'in Orijinal Paket Adı (Kesin Doğru Olmalı)
OLD_PACKAGE_NAME = "com.alperenkilic.webwrapperbase"

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

@app.route('/')
def home():
    return render_template('index.html')

def ghost_mode_manifest_fix(manifest_path, old_pkg, new_pkg):
    """
    Bu fonksiyon 'Yüklenmedi' hatasının panzehiridir.
    1. Kod yollarını sabitler (Crash olmasın diye).
    2. Paket adını değiştirir (Update demesin diye).
    3. Authority'leri değiştirir (Yüklenmedi demesin diye).
    """
    with open(manifest_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # ADIM 1: Önce tüm Activity/Service yollarını ESKİ paket adıyla sabitle (Absolute Path)
    # Örn: android:name=".MainActivity" -> android:name="com.alperenkilic...MainActivity"
    # Bunu yapmazsak, paket adı değişince sistem kodları bulamaz ve çöker.
    def expand_relative_name(match):
        attr = match.group(1) 
        val = match.group(2)
        if val.startswith('.'):
            return f'{attr}="{old_pkg}{val}"'
        return match.group(0)

    # android:name niteliklerini yakala ve genişlet
    content = re.sub(r'(android:name)="(\.[^"]*)"', expand_relative_name, content)
    
    # ADIM 2: Ana Paket Adını Değiştir
    content = content.replace(f'package="{old_pkg}"', f'package="{new_pkg}"')

    # ADIM 3: KRİTİK! Authority Çakışmalarını Önle
    # Manifest içinde 'authorities' geçen her satırdaki eski paket adını yenisiyle değiştir.
    # Sadece replace(old, new) yaparsak kod yolları bozulur (Adım 1 bunu korudu ama riskli).
    # Bu yüzden regex ile sadece 'authorities' kısmına odaklanıyoruz.
    
    def replace_authority(match):
        full_match = match.group(0)
        return full_match.replace(old_pkg, new_pkg)

    content = re.sub(r'android:authorities="[^"]*"', replace_authority, content)
    
    # Ekstra Güvenlik: Provider isimlerinde de paket adı geçiyorsa ve authority ise değiştir
    # Ancak kod yollarına (android:name) dokunmamaya dikkat et.
    
    with open(manifest_path, 'w', encoding='utf-8') as f:
        f.write(content)

def update_apktool_yml(yml_path):
    """Versiyonu yükseltir ve renameManifestPackage'i temizler."""
    if not os.path.exists(yml_path): return
    with open(yml_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    new_lines = []
    for line in lines:
        if "renameManifestPackage" in line: continue
        if "versionCode:" in line:
            new_lines.append(f"  versionCode: '{random.randint(1000, 9999)}'\n")
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
        
        job_id = str(uuid.uuid4())[:8]
        temp_folder = os.path.join(OUTPUT_DIR, job_id)
        
        # 1. Kopyalama
        source_path = TEMPLATE_DL if app_type == 'downloader' else TEMPLATE_STD
        shutil.copytree(source_path, temp_folder)

        # 2. Meta-Inf ve Build Cache Temizliği
        for item in ['build', 'dist', 'META-INF']:
            path = os.path.join(temp_folder, item)
            if os.path.exists(path): shutil.rmtree(path)

        # 3. YENİ KİMLİK
        safe_suffix = re.sub(r'[^a-z0-9]', '', app_name.lower())[:10]
        new_package_id = f"com.convert.v{job_id}.{safe_suffix}"

        # 4. MANIFEST HAYALET MODU (GHOST MODE)
        manifest_path = os.path.join(temp_folder, 'AndroidManifest.xml')
        ghost_mode_manifest_fix(manifest_path, OLD_PACKAGE_NAME, new_package_id)

        # 5. YML FIX
        update_apktool_yml(os.path.join(temp_folder, 'apktool.yml'))

        # 6. KAYNAK & LOGO
        res_path = os.path.join(temp_folder, 'res')
        public_xml = os.path.join(temp_folder, 'res', 'values', 'public.xml')
        if os.path.exists(public_xml): os.remove(public_xml)

        if logo_file:
            # Vektör ikon temizliği
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

        # 7. STRING NAME FIX
        strings_path = os.path.join(temp_folder, 'res', 'values', 'strings.xml')
        if os.path.exists(strings_path):
            with open(strings_path, 'r', encoding='utf-8') as f:
                content = f.read()
            content = content.replace('WebWrapperBase', app_name)
            with open(strings_path, 'w', encoding='utf-8') as f:
                f.write(content)

        # 8. BUILD & SIGN
        safe_name = re.sub(r'[^a-zA-Z0-9_]', '', app_name.replace(" ", "_"))
        apk_unsigned = os.path.join(OUTPUT_DIR, f"{job_id}_u.apk")
        apk_aligned = os.path.join(OUTPUT_DIR, f"{job_id}_a.apk")
        apk_signed = os.path.join(OUTPUT_DIR, f"{safe_name}.apk")
        
        # Build (-f şart)
        subprocess.run(["apktool", "b", temp_folder, "-o", apk_unsigned, "-f", "--use-aapt2"], check=True)

        # Zipalign (Yüklenmedi hatasının gizli sebebi olabilir)
        # Eğer sunucuda zipalign yoksa, unsigned dosyayı kullanmaya devam et ama loga yaz.
        target_apk = apk_unsigned
        try:
            subprocess.run(["zipalign", "-p", "-f", "-v", "4", apk_unsigned, apk_aligned], check=True)
            target_apk = apk_aligned
        except:
            print("WARNING: Zipalign not found, skipping alignment.")

        # Sign (V1 ve V2 imzalama zorunlu)
        subprocess.run([
            "apksigner", "sign", 
            "--ks", KEYSTORE_PATH, 
            "--ks-pass", f"pass:{KEY_PASS}", 
            "--v1-signing-enabled", "true", # Eski cihazlar için
            "--v2-signing-enabled", "true", # Yeni cihazlar için (Yüklenmedi hatasını çözer)
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
            <h2 style="font-weight:800;">READY!</h2>
            <p>ID: {new_package_id}</p>
            <p style="color:#666;">Ghost Mode Active: No Conflicts.</p>
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
