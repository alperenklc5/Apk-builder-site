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

# Template'in Orijinal Paket Adı
OLD_PACKAGE_NAME = "com.alperenkilic.webwrapperbase"

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

@app.route('/')
def home():
    return render_template('index.html')

# ─── CLAUDE'UN MOTORU (DÜZELTİLMİŞ TEMİZLİK) ───

def full_package_rename(project_dir, old_pkg, new_pkg):
    old_path = old_pkg.replace('.', '/')
    new_path = new_pkg.replace('.', '/')
    
    # 1. Manifest
    step1_fix_manifest(project_dir, old_pkg, new_pkg)
    # 2. Smali İçerik
    step2_fix_smali_content(project_dir, old_path, new_path)
    # 3. Smali Klasör Taşıma
    step3_move_smali_dirs(project_dir, old_path, new_path)
    # 4. Res XML
    step4_fix_res_xml(project_dir, old_pkg, new_pkg)
    # 5. Strings
    step5_fix_strings_xml(project_dir, old_pkg, new_pkg)
    # 6. Apktool.yml (Kütüphanesiz)
    step6_fix_apktool_yml(project_dir)

def step1_fix_manifest(project_dir, old_pkg, new_pkg):
    path = os.path.join(project_dir, 'AndroidManifest.xml')
    if not os.path.exists(path): return
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Relative -> Absolute
    def expand(m):
        attr, val = m.group(1), m.group(2)
        return f'{attr}="{old_pkg}{val}"' if val.startswith('.') else m.group(0)
    content = re.sub(r'(android:name)="(\.[^"]*)"', expand, content)

    # Package değişimi
    content = content.replace(f'package="{old_pkg}"', f'package="{new_pkg}"')
    # Authority
    content = content.replace(old_pkg, new_pkg)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def step2_fix_smali_content(project_dir, old_path, new_path):
    smali_dirs = [d for d in os.listdir(project_dir) if d.startswith('smali')]
    for smali_dir in smali_dirs:
        base = os.path.join(project_dir, smali_dir)
        for root, _, files in os.walk(base):
            for fname in files:
                if not fname.endswith('.smali'): continue
                fpath = os.path.join(root, fname)
                with open(fpath, 'r', encoding='utf-8', errors='replace') as f:
                    text = f.read()
                if old_path in text:
                    text = text.replace(old_path, new_path)
                    with open(fpath, 'w', encoding='utf-8') as f:
                        f.write(text)

def step3_move_smali_dirs(project_dir, old_path, new_path):
    smali_dirs = [d for d in os.listdir(project_dir) if d.startswith('smali')]
    for smali_dir in smali_dirs:
        base = os.path.join(project_dir, smali_dir)
        old_dir = os.path.join(base, old_path)
        new_dir = os.path.join(base, new_path)
        
        if not os.path.isdir(old_dir): continue
        
        os.makedirs(os.path.dirname(new_dir), exist_ok=True)
        if os.path.exists(new_dir):
            _merge_move(old_dir, new_dir)
        else:
            shutil.move(old_dir, new_dir)
        
        try:
            top_level = old_path.split('/')[0]
            _cleanup_empty(os.path.join(base, top_level))
        except: pass

def step4_fix_res_xml(project_dir, old_pkg, new_pkg):
    res_path = os.path.join(project_dir, 'res')
    if not os.path.exists(res_path): return
    
    # Public.xml SİL
    public_xml = os.path.join(res_path, 'values', 'public.xml')
    if os.path.exists(public_xml): os.remove(public_xml)

    for root, _, files in os.walk(res_path):
        for fname in files:
            if not fname.endswith('.xml'): continue
            fpath = os.path.join(root, fname)
            try:
                with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
                    text = f.read()
                if old_pkg in text:
                    text = text.replace(old_pkg, new_pkg)
                    with open(fpath, 'w', encoding='utf-8') as f:
                        f.write(text)
            except: pass

def step5_fix_strings_xml(project_dir, old_pkg, new_pkg):
    values_path = os.path.join(project_dir, 'res', 'values')
    if not os.path.exists(values_path): return
    for fname in os.listdir(values_path):
        if not fname.endswith('.xml'): continue
        fpath = os.path.join(values_path, fname)
        with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
            text = f.read()
        if old_pkg in text:
            text = text.replace(old_pkg, new_pkg)
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(text)

def step6_fix_apktool_yml(project_dir):
    yml_path = os.path.join(project_dir, 'apktool.yml')
    if not os.path.exists(yml_path): return
    
    with open(yml_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    new_lines = []
    for line in lines:
        if "renameManifestPackage" in line: continue
        if "versionCode:" in line:
            try:
                parts = line.split(':')
                if len(parts) > 1:
                    ver = int(re.sub(r"[^\d]", "", parts[1]))
                    new_ver = ver + random.randint(1, 100)
                    new_lines.append(f"  versionCode: '{new_ver}'\n")
                    continue
            except: pass
        new_lines.append(line)
        
    with open(yml_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

def _merge_move(src, dst):
    for item in os.listdir(src):
        s, d = os.path.join(src, item), os.path.join(dst, item)
        if os.path.isdir(s):
            os.makedirs(d, exist_ok=True)
            _merge_move(s, d)
        else:
            shutil.move(s, d)
    shutil.rmtree(src)

def _cleanup_empty(path):
    if not os.path.isdir(path): return
    for sub in os.listdir(path):
        _cleanup_empty(os.path.join(path, sub))
    if not os.listdir(path):
        os.rmdir(path)

# ── FLASK ROUTES ─────────────────────────────────────────────

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

        # 2. Temizlik (Build artıkları)
        for item in ['build', 'dist', 'META-INF']:
            p = os.path.join(temp_folder, item)
            if os.path.exists(p): shutil.rmtree(p)

        # 3. YENİ KİMLİK
        safe_suffix = re.sub(r'[^a-z0-9]', '', app_name.lower())[:5] + str(random.randint(10,99))
        new_package_id = f"com.convert.v{job_id}.{safe_suffix}"

        # 4. CLAUDE MOTORUNU ÇALIŞTIR
        full_package_rename(temp_folder, OLD_PACKAGE_NAME, new_package_id)

        # 5. LOGO (BURASI DÜZELTİLDİ - KRİTİK NOKTA)
        res_path = os.path.join(temp_folder, 'res')
        if logo_file:
            # SADECE 'mipmap' veya 'drawable' içindeki v26'yı sil. 
            # 'values-v26'ya DOKUNMA!
            for root, dirs, files in os.walk(res_path, topdown=False):
                folder_name = os.path.basename(root)
                if ("mipmap" in folder_name or "drawable" in folder_name):
                    if "anydpi" in folder_name or "v26" in folder_name:
                        shutil.rmtree(root)
            
            temp_logo = os.path.join(temp_folder, 'temp.png')
            logo_file.save(temp_logo)
            for root, dirs, files in os.walk(res_path):
                if "mipmap" in os.path.basename(root):
                    for f in files:
                        if f.startswith("ic_launcher"): os.remove(os.path.join(root, f))
                    shutil.copy(temp_logo, os.path.join(root, "ic_launcher.png"))
                    shutil.copy(temp_logo, os.path.join(root, "ic_launcher_round.png"))

        # 6. APP NAME
        strings_path = os.path.join(temp_folder, 'res', 'values', 'strings.xml')
        if os.path.exists(strings_path):
            with open(strings_path, 'r', encoding='utf-8') as f: c = f.read()
            c = c.replace('WebWrapperBase', app_name)
            with open(strings_path, 'w', encoding='utf-8') as f: f.write(c)

        # 7. BUILD
# --- 7. TOTAL TRANSFORMATION (CRASH & CONFLICT FIX) ---
        safe_name = re.sub(r'[^a-zA-Z0-9_]', '', app_name.replace(" ", "_"))
        apk_unsigned = os.path.join(OUTPUT_DIR, f"{job_id}_u.apk")
        apk_aligned = os.path.join(OUTPUT_DIR, f"{job_id}_a.apk")
        apk_signed = os.path.join(OUTPUT_DIR, f"{safe_name}.apk")

        # A) SMALI & RESOURCE CONTENT REPLACE
        # Bu kısım kodun içindeki 'com.alperenkilic...' yazılarını yeni paketle değiştirir.
        old_path = OLD_PACKAGE_NAME.replace('.', '/')
        new_path = new_package_id.replace('.', '/')
        
        for root, dirs, files in os.walk(temp_folder):
            for filename in files:
                if filename.endswith(('.smali', '.xml', '.yml')):
                    filepath = os.path.join(root, filename)
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        text = f.read()
                    if OLD_PACKAGE_NAME in text or old_path in text:
                        text = text.replace(OLD_PACKAGE_NAME, new_package_id)
                        text = text.replace(old_path, new_path)
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(text)

        # B) SMALI FOLDER MOVE (PHYSICAL)
        # Sınıfları yeni klasör yoluna taşır, böylece uygulama 'duruyor' demez.
        smali_dirs = [d for d in os.listdir(temp_folder) if d.startswith('smali')]
        for s_dir in smali_dirs:
            src = os.path.join(temp_folder, s_dir, old_path)
            dst = os.path.join(temp_folder, s_dir, new_path)
            if os.path.exists(src):
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                shutil.move(src, dst)

        # C) BUILD, ALIGN & SIGN
        build_process = subprocess.run(["apktool", "b", temp_folder, "-o", apk_unsigned, "-f", "--use-aapt2"], 
                                         capture_output=True, text=True)
        if build_process.returncode != 0:
            raise Exception(f"BUILD ERROR:\n{build_process.stderr}")

        # Zipalign
        target_for_signing = apk_unsigned
        try:
            subprocess.run(["zipalign", "-f", "-v", "4", apk_unsigned, apk_aligned], check=True, capture_output=True)
            target_for_signing = apk_aligned
        except: pass

        # Apksigner (V1+V2)
        subprocess.run(["apksigner", "sign", "--ks", KEYSTORE_PATH, "--ks-pass", f"pass:{KEY_PASS}", 
                        "--v1-signing-enabled", "true", "--v2-signing-enabled", "true", 
                        "--out", apk_signed, target_for_signing], check=True)

        # Temizlik
        if os.path.exists(temp_folder): shutil.rmtree(temp_folder)
        if os.path.exists(apk_unsigned): os.remove(apk_unsigned)
        if os.path.exists(apk_aligned): os.remove(apk_aligned)
        
        return f"""
        <div style="text-align:center; padding:100px; font-family:sans-serif;">
            <h1 style="color:green;">✅ SUCCESS!</h1>
            <p>ID: {new_package_id}</p>
            <a href='/download/{safe_name}.apk' style="background:#000; color:#fff; padding:10px 20px;">Download APK</a>
        </div>
        """

    except Exception as e:
        return f"<div style='background:#fdd; padding:20px; color:red;'><h2>ERROR</h2><pre>{str(e)}</pre></div>"

@app.route('/download/<filename>')
def download(filename):
    return send_file(os.path.join(OUTPUT_DIR, filename), as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
