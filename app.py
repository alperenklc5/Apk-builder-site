import os
import re
import shutil
import subprocess
import uuid
import random
from flask import Flask, render_template, request, send_file

app = Flask(__name__)

# ══════════════════════════════════════════════════════════════
#  AYARLAR
# ══════════════════════════════════════════════════════════════

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_STD = os.path.join(BASE_DIR, 'source', 'standard_klasor')
TEMPLATE_DL = os.path.join(BASE_DIR, 'source', 'downloader_klasor')
OUTPUT_DIR = os.path.join(BASE_DIR, 'output')

# Template'in GERÇEK Orijinal Paket Adı
OLD_PACKAGE = "com.alperenkilic.webwrapperbase"

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

@app.route('/')
def home():
    return render_template('index.html')

# ══════════════════════════════════════════════════════════════
#  CLAUDE'UN MOTORU
# ══════════════════════════════════════════════════════════════

def step1_deep_replace(project_dir, old_pkg, new_pkg):
    old_dotted = old_pkg
    new_dotted = new_pkg
    old_slashed = old_pkg.replace('.', '/')
    new_slashed = new_pkg.replace('.', '/')

    for root, dirs, files in os.walk(project_dir):
        if 'build' in dirs: dirs.remove('build')
        for fname in files:
            if fname.endswith(('.smali', '.xml', '.yml', '.json', '.txt', '.html')):
                fpath = os.path.join(root, fname)
                try:
                    with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
                        text = f.read()
                    original = text
                    text = text.replace(old_slashed, new_slashed)
                    text = text.replace(old_dotted, new_dotted)
                    if text != original:
                        with open(fpath, 'w', encoding='utf-8') as f:
                            f.write(text)
                except: pass

def step2_fix_manifest(project_dir, new_pkg):
    manifest_path = os.path.join(project_dir, 'AndroidManifest.xml')
    if not os.path.exists(manifest_path): return

    with open(manifest_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Relative path düzeltme
    def expand_relative(match):
        attr, val = match.group(1), match.group(2)
        if val.startswith('.'): return f'{attr}="{new_pkg}{val}"'
        return match.group(0)
    content = re.sub(r'(android:name)="(\.[^"]*)"', expand_relative, content)

    # Authority Isolation
    def randomize_auth(match):
        uid = uuid.uuid4().hex[:8]
        return f'android:authorities="{new_pkg}.provider.{uid}"'
    content = re.sub(r'android:authorities="[^"]*"', randomize_auth, content)
    
    with open(manifest_path, 'w', encoding='utf-8') as f:
        f.write(content)

def step3_migrate_smali(project_dir, old_pkg, new_pkg):
    old_path = old_pkg.replace('.', '/')
    new_path = new_pkg.replace('.', '/')
    smali_dirs = [d for d in os.listdir(project_dir) if d.startswith('smali')]
    
    for s_dir in smali_dirs:
        base = os.path.join(project_dir, s_dir)
        old_dir_full = os.path.join(base, old_path)
        new_dir_full = os.path.join(base, new_path)
        if os.path.exists(old_dir_full):
            os.makedirs(os.path.dirname(new_dir_full), exist_ok=True)
            if os.path.exists(new_dir_full): shutil.rmtree(new_dir_full)
            shutil.move(old_dir_full, new_dir_full)
            try:
                p = os.path.dirname(old_dir_full)
                if not os.listdir(p): os.rmdir(p)
                gp = os.path.dirname(p)
                if not os.listdir(gp): os.rmdir(gp)
            except: pass

def step4_sanitize_res(project_dir):
    pxml = os.path.join(project_dir, 'res', 'values', 'public.xml')
    if os.path.exists(pxml): os.remove(pxml)
    
    yml = os.path.join(project_dir, 'apktool.yml')
    if os.path.exists(yml):
        with open(yml, 'r', encoding='utf-8') as f: lines = f.readlines()
        nl = []
        for l in lines:
            if "renameManifestPackage" in l: continue
            if "versionCode:" in l:
                try:
                    p = l.split(':')
                    v = int(re.sub(r"\D", "", p[1]))
                    nl.append(f"  versionCode: '{v + random.randint(100,999)}'\n")
                except: nl.append(l)
            else: nl.append(l)
        with open(yml, 'w', encoding='utf-8') as f: f.writelines(nl)

# ══════════════════════════════════════════════════════════════
#  BUILD ROUTE (CRITICAL FIX: ZIPALIGN ZORUNLU)
# ══════════════════════════════════════════════════════════════

@app.route('/build', methods=['POST'])
def build_apk():
    temp_folder = None
    try:
        app_name = request.form.get('app_name')
        app_type = request.form.get('app_type')
        logo_file = request.files.get('logo')
        
        job_id = str(uuid.uuid4())[:8]
        temp_folder = os.path.join(OUTPUT_DIR, job_id)
        
        # 1. Kaynak
        source_path = TEMPLATE_DL if app_type == 'downloader' else TEMPLATE_STD
        shutil.copytree(source_path, temp_folder)
        for i in ['build', 'dist', 'META-INF']:
            p = os.path.join(temp_folder, i)
            if os.path.exists(p): shutil.rmtree(p)

        # 2. Logic
        new_pkg = f"com.convert.v{job_id}"
        step1_deep_replace(temp_folder, OLD_PACKAGE, new_pkg)
        step2_fix_manifest(temp_folder, new_pkg)
        step3_migrate_smali(temp_folder, OLD_PACKAGE, new_pkg)
        step4_sanitize_res(temp_folder)

        # 3. Assets
        res_path = os.path.join(temp_folder, 'res')
        if logo_file:
            for root, dirs, files in os.walk(res_path, topdown=False):
                if ("mipmap" in root or "drawable" in root) and ("anydpi" in root or "v26" in root):
                    shutil.rmtree(root)
            t_logo = os.path.join(temp_folder, 't.png')
            logo_file.save(t_logo)
            for root, dirs, files in os.walk(res_path):
                if "mipmap" in os.path.basename(root):
                    for f in files:
                        if f.startswith("ic_launcher"): os.remove(os.path.join(root, f))
                    shutil.copy(t_logo, os.path.join(root, "ic_launcher.png"))
                    shutil.copy(t_logo, os.path.join(root, "ic_launcher_round.png"))

        s_path = os.path.join(res_path, 'values', 'strings.xml')
        if os.path.exists(s_path):
            with open(s_path, 'r', encoding='utf-8') as f: c = f.read()
            c = c.replace('WebWrapperBase', app_name)
            with open(s_path, 'w', encoding='utf-8') as f: f.write(c)

        # 4. Keystore
        keystore_path = os.path.join(temp_folder, 'dynamic.jks')
        subprocess.run([
            "keytool", "-genkey", "-v", "-keystore", keystore_path, "-alias", "key", 
            "-keyalg", "RSA", "-keysize", "2048", "-validity", "10000",
            "-storepass", "123456", "-keypass", "123456",
            "-dname", f"CN={job_id}, OU=App, O=Convert, L=Samsun, ST=TR, C=TR"
        ], check=True, capture_output=True)

        # 5. BUILD - ALIGN - SIGN (KRİTİK BÖLÜM)
        safe_name = re.sub(r'[^a-zA-Z0-9_]', '', app_name.replace(" ", "_"))
        apk_unsigned = os.path.join(OUTPUT_DIR, f"{job_id}_u.apk")
        apk_aligned = os.path.join(OUTPUT_DIR, f"{job_id}_a.apk")
        apk_signed = os.path.join(OUTPUT_DIR, f"{safe_name}.apk")
        
        # A) APKTOOL BUILD
        res = subprocess.run(["apktool", "b", temp_folder, "-o", apk_unsigned, "-f", "--use-aapt2"], 
                             capture_output=True, text=True)
        if res.returncode != 0:
            raise Exception(f"APKTOOL ERROR:\n{res.stderr}")

        # B) ZIPALIGN (ZORUNLU - TRY-EXCEPT YOK!)
        # -p: page align (resources.arsc için şart)
        # -f: overwrite
        # -v: verbose
        # 4: 4-byte boundary
        align_res = subprocess.run(
            ["zipalign", "-p", "-f", "-v", "4", apk_unsigned, apk_aligned],
            capture_output=True, text=True
        )
        
        if align_res.returncode != 0:
            # Eğer zipalign hata verirse işlemi DURDUR. Bozuk APK üretme.
            raise Exception(f"ZIPALIGN ERROR (System missing zipalign?):\n{align_res.stderr}")

        # C) APKSIGNER (Hizalanmış APK'yı imzala)
        # İmzalama MUTLAKA zipalign'dan SONRA yapılmalı (V2/V3 için)
        sign_res = subprocess.run([
            "apksigner", "sign", 
            "--ks", keystore_path, 
            "--ks-pass", "pass:123456", 
            "--v1-signing-enabled", "true", 
            "--v2-signing-enabled", "true", 
            "--v3-signing-enabled", "true", 
            "--out", apk_signed, 
            apk_aligned  # <--- DİKKAT: aligned apk girdisi
        ], capture_output=True, text=True)

        if sign_res.returncode != 0:
            raise Exception(f"SIGNING ERROR:\n{sign_res.stderr}")

        # Temizlik
        if os.path.exists(temp_folder): shutil.rmtree(temp_folder)
        if os.path.exists(apk_unsigned): os.remove(apk_unsigned)
        if os.path.exists(apk_aligned): os.remove(apk_aligned)
        
        return f"""
        <div style="text-align:center; padding:100px; font-family:sans-serif; background:#fff;">
            <h1 style="color:green; font-size:60px;">✅</h1>
            <h2>SUCCESS</h2>
            <p>ID: {new_pkg}</p>
            <p>Aligned: YES (4-byte)</p>
            <a href="/download/{safe_name}.apk" style="display:inline-block; background:#000; color:#fff; padding:15px 35px; text-decoration:none; border-radius:10px; margin-top:20px;">
                Download APK
            </a>
        </div>
        """

    except Exception as e:
        return f"<div style='padding:20px; background:#fdd; color:red;'><pre>{str(e)}</pre></div>"

@app.route('/download/<filename>')
def download(filename):
    return send_file(os.path.join(OUTPUT_DIR, filename), as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
