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
OLD_PACKAGE = "com.alperenkilic.webwrapperbase"

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

@app.route('/')
def home():
    return render_template('index.html')

# ══════════════════════════════════════════════════════════════
#  LOGIC: GHOST MODE + PROVIDER KILLER
# ══════════════════════════════════════════════════════════════

def step1_reset_files(project_dir):
    """Resource ID çakışmalarını önlemek için public.xml'i sil."""
    pxml = os.path.join(project_dir, 'res', 'values', 'public.xml')
    if os.path.exists(pxml): os.remove(pxml)

def step2_manifest_surgical_fix(project_dir, old_pkg, new_pkg):
    """
    1. Paket adını değiştir.
    2. Activity yollarını koru.
    3. Authority'leri izole et.
    4. [KRİTİK] ÇÖKEN PROVIDER'I SİL (AndroidX Startup).
    """
    manifest_path = os.path.join(project_dir, 'AndroidManifest.xml')
    authority_map = {}
    
    if not os.path.exists(manifest_path): return {}

    with open(manifest_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # --- A) PROVIDER KILLER (ResourceNotFound Hatasının Kesin Çözümü) ---
    # <provider ... androidx.startup.InitializationProvider ... /> bloğunu bul ve sil.
    # Bu provider, paket ismi değişince kaynakları bulamayıp crash veriyor. Silersek crash biter.
    content = re.sub(
        r'<provider[^>]*androidx\.startup\.InitializationProvider[^>]*>.*?</provider>', 
        '', 
        content, 
        flags=re.DOTALL
    )
    # Tek satırlık self-closing tag hali varsa onu da sil
    content = re.sub(
        r'<provider[^>]*androidx\.startup\.InitializationProvider[^>]*/>', 
        '', 
        content
    )

    # --- B) Paket Adı ve Debug Mod ---
    if 'android:debuggable="true"' not in content:
        content = content.replace('<application', '<application android:debuggable="true"')
    
    content = content.replace(f'package="{old_pkg}"', f'package="{new_pkg}"')

    # --- C) Activity Yollarını Koru ---
    def fix_activity_path(match):
        attr, val = match.group(1), match.group(2)
        if val.startswith('.'):
            return f'{attr}="{old_pkg}{val}"'
        return match.group(0)
    content = re.sub(r'(android:name)="(\.[^"]*)"', fix_activity_path, content)

    # --- D) İzin İsimlerini Düzelt ---
    def fix_permissions(match):
        full_tag = match.group(0)
        if "permission" in full_tag.lower() or "dynamic_receiver" in full_tag.lower():
            return full_tag.replace(old_pkg, new_pkg)
        return full_tag
    content = re.sub(r'android:name="[^"]+"', fix_permissions, content)

    # --- E) Authority Haritası ---
    matches = re.findall(r'android:authorities="([^"]*)"', content)
    for old_auth in matches:
        uid = uuid.uuid4().hex[:8]
        if old_pkg in old_auth:
            new_auth = old_auth.replace(old_pkg, new_pkg) + "." + uid
        else:
            new_auth = f"{new_pkg}.provider.{uid}"
        authority_map[old_auth] = new_auth
        content = content.replace(f'android:authorities="{old_auth}"', f'android:authorities="{new_auth}"')

    with open(manifest_path, 'w', encoding='utf-8') as f:
        f.write(content)
        
    return authority_map

def step3_sync_smali_code(project_dir, old_pkg, new_pkg, authority_map):
    """Smali kodlarını senkronize et."""
    old_r_path = f"L{old_pkg.replace('.', '/')}/R"
    new_r_path = f"L{new_pkg.replace('.', '/')}/R"
    old_pkg_str = f'"{old_pkg}"'
    new_pkg_str = f'"{new_pkg}"'

    for root, dirs, files in os.walk(project_dir):
        if 'build' in dirs: dirs.remove('build')
        for fname in files:
            if fname.endswith('.smali'):
                fpath = os.path.join(root, fname)
                try:
                    with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
                        text = f.read()
                    original = text
                    
                    if old_r_path in text: text = text.replace(old_r_path, new_r_path)
                    if old_pkg_str in text: text = text.replace(old_pkg_str, new_pkg_str)
                    
                    for old_auth, new_auth in authority_map.items():
                        if old_auth in text: text = text.replace(old_auth, new_auth)

                    if text != original:
                        with open(fpath, 'w', encoding='utf-8') as f: f.write(text)
                except: pass

def step4_provider_paths_cleanup(project_dir, old_pkg, new_pkg):
    res_xml = os.path.join(project_dir, 'res', 'xml')
    if os.path.exists(res_xml):
        for f in os.listdir(res_xml):
            if f.endswith('.xml'):
                fp = os.path.join(res_xml, f)
                with open(fp, 'r', encoding='utf-8') as file: txt = file.read()
                if old_pkg in txt:
                    txt = txt.replace(old_pkg, new_pkg)
                    with open(fp, 'w', encoding='utf-8') as file: file.write(txt)

# ══════════════════════════════════════════════════════════════
#  BUILD ROUTE
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

        # 2. Logic (PROVIDER KILLER ENABLED)
        new_pkg = f"com.convert.v{job_id}"
        
        step1_reset_files(temp_folder)
        auth_map = step2_manifest_surgical_fix(temp_folder, OLD_PACKAGE, new_pkg) # Provider silme burada
        step3_sync_smali_code(temp_folder, OLD_PACKAGE, new_pkg, auth_map)
        step4_provider_paths_cleanup(temp_folder, OLD_PACKAGE, new_pkg)

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

        # 5. BUILD - ALIGN - SIGN
        safe_name = re.sub(r'[^a-zA-Z0-9_]', '', app_name.replace(" ", "_"))
        apk_unsigned = os.path.join(OUTPUT_DIR, f"{job_id}_u.apk")
        apk_aligned = os.path.join(OUTPUT_DIR, f"{job_id}_a.apk")
        apk_signed = os.path.join(OUTPUT_DIR, f"{safe_name}.apk")
        
        res = subprocess.run(["apktool", "b", temp_folder, "-o", apk_unsigned, "-f", "--use-aapt2"], 
                             capture_output=True, text=True)
        if res.returncode != 0: raise Exception(f"APKTOOL ERROR:\n{res.stderr}")

        align_res = subprocess.run(["zipalign", "-p", "-f", "-v", "4", apk_unsigned, apk_aligned], 
                                   capture_output=True, text=True)
        if align_res.returncode != 0: raise Exception(f"ZIPALIGN ERROR:\n{align_res.stderr}")

        sign_res = subprocess.run([
            "apksigner", "sign", "--ks", keystore_path, "--ks-pass", "pass:123456", 
            "--v1-signing-enabled", "true", "--v2-signing-enabled", "true", 
            "--v3-signing-enabled", "true", "--out", apk_signed, apk_aligned
        ], capture_output=True, text=True)
        if sign_res.returncode != 0: raise Exception(f"SIGNING ERROR:\n{sign_res.stderr}")

        if os.path.exists(temp_folder): shutil.rmtree(temp_folder)
        if os.path.exists(apk_unsigned): os.remove(apk_unsigned)
        if os.path.exists(apk_aligned): os.remove(apk_aligned)
        
        return f"""
        <div style="text-align:center; padding:100px; font-family:sans-serif; background:#fff;">
            <h1 style="color:green; font-size:60px;">✅</h1>
            <h2>SUCCESS</h2>
            <p>ID: {new_pkg}</p>
            <p>Provider Killer: <span style="color:red; font-weight:bold">EXECUTED</span></p>
            <p style="color:gray">AndroidX Startup Removed</p>
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
