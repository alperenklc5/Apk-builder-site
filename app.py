import os, shutil, subprocess, uuid, re, random
import yaml
from flask import Flask, render_template, request, send_file

app = Flask(__name__)

# --- Configuration ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_STD = os.path.join(BASE_DIR, 'source', 'standard_klasor')
TEMPLATE_DL = os.path.join(BASE_DIR, 'source', 'downloader_klasor')
OUTPUT_DIR = os.path.join(BASE_DIR, 'output')
KEYSTORE_PATH = os.path.join(BASE_DIR, 'yeni.jks')
KEY_PASS = "123456" 

# Template'in GERÇEK Orijinal Paket Adı
OLD_PACKAGE_NAME = "com.alperenkilic.webwrapperbase"

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

@app.route('/')
def home():
    return render_template('index.html')

# ── CLAUDE'UN MOTORU (Flask Entegreli) ───────────────────────

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
    # 5. Strings (Authority için)
    step5_fix_strings_xml(project_dir, old_pkg, new_pkg)
    # 6. Apktool.yml
    step6_fix_apktool_yml(project_dir)

def step1_fix_manifest(project_dir, old_pkg, new_pkg):
    path = os.path.join(project_dir, 'AndroidManifest.xml')
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Relative -> Absolute
    def expand(m):
        attr, val = m.group(1), m.group(2)
        return f'{attr}="{old_pkg}{val}"' if val.startswith('.') else m.group(0)
    content = re.sub(r'(android:name)="(\.[^"]*)"', expand, content)

    # Package değişimi
    content = content.replace(f'package="{old_pkg}"', f'package="{new_pkg}"')
    # Authority ve diğer referanslar
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
        
        # Boş klasör temizliği
        try:
            top_level = old_path.split('/')[0]
            _cleanup_empty(os.path.join(base, top_level))
        except: pass

def step4_fix_res_xml(project_dir, old_pkg, new_pkg):
    res_path = os.path.join(project_dir, 'res')
    if not os.path.exists(res_path): return
    
    # public.xml SİL (Kritik)
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
    try:
        with open(yml_path, 'r') as f:
            data = yaml.safe_load(f)
        if 'renameManifestPackage' in data:
            data['renameManifestPackage'] = None
        # Versiyon artır
        if 'versionInfo' in data and 'versionCode' in data['versionInfo']:
             data['versionInfo']['versionCode'] = str(int(data['versionInfo']['versionCode']) + random.randint(1,100))
        
        with open(yml_path, 'w') as f:
            yaml.dump(data, f, default_flow_style=False)
    except:
        pass

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

        # 2. Temizlik
        for item in ['build', 'dist', 'META-INF']:
            p = os.path.join(temp_folder, item)
            if os.path.exists(p): shutil.rmtree(p)

        # 3. YENİ KİMLİK
        safe_suffix = re.sub(r'[^a-z0-9]', '', app_name.lower())[:5] + str(random.randint(10,99))
        new_package_id = f"com.convert.v{job_id}.{safe_suffix}"

        # 4. CLAUDE MOTORUNU ÇALIŞTIR
        full_package_rename(temp_folder, OLD_PACKAGE_NAME, new_package_id)

        # 5. LOGO & ICON
        res_path = os.path.join(temp_folder, 'res')
        if logo_file:
            for root, dirs, files in os.walk(res_path, topdown=False):
                if "anydpi" in root or "v26" in root: shutil.rmtree(root)
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
        safe_name = re.sub(r'[^a-zA-Z0-9_]', '', app_name.replace(" ", "_"))
        apk_unsigned = os.path.join(OUTPUT_DIR, f"{job_id}_u.apk")
        apk_signed = os.path.join(OUTPUT_DIR, f"{safe_name}.apk")
        
        subprocess.run(["apktool", "b", temp_folder, "-o", apk_unsigned, "-f", "--use-aapt2"], check=True)
        
        # Zipalign & Sign
        target = apk_unsigned
        try:
            apk_aligned = os.path.join(OUTPUT_DIR, f"{job_id}_a.apk")
            subprocess.run(["zipalign", "-p", "-f", "-v", "4", apk_unsigned, apk_aligned], check=True)
            target = apk_aligned
        except: pass

        subprocess.run(["apksigner", "sign", "--ks", KEYSTORE_PATH, "--ks-pass", f"pass:{KEY_PASS}", 
                        "--v1-signing-enabled", "true", "--v2-signing-enabled", "true", 
                        "--out", apk_signed, target], check=True)

        if os.path.exists(temp_folder): shutil.rmtree(temp_folder)
        if os.path.exists(apk_unsigned): os.remove(apk_unsigned)
        
        return f"<h1>SUCCESS: {new_package_id}</h1> <a href='/download/{safe_name}.apk'>Download</a>"

    except Exception as e:
        return f"ERROR: {str(e)}"

@app.route('/download/<filename>')
def download(filename):
    return send_file(os.path.join(OUTPUT_DIR, filename), as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
