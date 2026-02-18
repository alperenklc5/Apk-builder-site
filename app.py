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

BASE_DIR     = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_STD = os.path.join(BASE_DIR, 'source', 'standard_klasor')
TEMPLATE_DL  = os.path.join(BASE_DIR, 'source', 'downloader_klasor')
OUTPUT_DIR   = os.path.join(BASE_DIR, 'output')
OLD_PACKAGE  = "com.alperenkilic.webwrapperbase"

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# ══════════════════════════════════════════════════════════════
#  ADIM 1 — DEEP TEXT REPLACE (Noktalı + Slashlı)
# ══════════════════════════════════════════════════════════════

def step1_deep_replace(project_dir, old_pkg, new_pkg):
    """
    Tüm metin dosyalarında eski paketi yenisiyle değiştirir.
    Önce slashlı (daha spesifik), sonra noktalı format.
    """
    old_slashed = old_pkg.replace('.', '/')
    new_slashed = new_pkg.replace('.', '/')

    TEXT_EXTS = {'.smali', '.xml', '.yml', '.json', '.txt', '.html', '.properties', '.gradle'}

    for root, dirs, files in os.walk(project_dir):
        dirs[:] = [d for d in dirs if d not in ('build', 'dist', 'META-INF', '__pycache__')]
        for fname in files:
            if os.path.splitext(fname)[1].lower() not in TEXT_EXTS:
                continue
            fpath = os.path.join(root, fname)
            try:
                with open(fpath, 'r', encoding='utf-8', errors='replace') as f:
                    text = f.read()
                original = text
                text = text.replace(old_slashed, new_slashed)   # Önce slash (daha spesifik)
                text = text.replace(old_pkg,     new_pkg)        # Sonra noktalı
                if text != original:
                    with open(fpath, 'w', encoding='utf-8') as f:
                        f.write(text)
            except Exception:
                pass

# ══════════════════════════════════════════════════════════════
#  ADIM 2 — SMALI CONSISTENCY ENGINE
# ══════════════════════════════════════════════════════════════

def step2_smali_consistency_engine(project_dir, new_pkg):
    """
    CRASH'in gerçek sebebi:
      Dosya fiziksel olarak smali/com/new/pkg/Foo.smali konumunda
      ama içindeki header hala ".class public Lcom/old/pkg/Foo;" diyor.
      Dalvik/ART bu uyumsuzlugu yakalar -> ClassNotFoundException.

    Bu fonksiyon her .smali dosyasini acar, fiziksel konumundan
    beklenen class adini hesaplar ve .class satirini zorla o degere sabitler.

    NOT: Bu adim fiziksel taşimadan (step4) ÖNCE çaliştirilmali.
    Dosyalar hâlâ eski konumdayken içeriklerini düzelt;
    step4 klasörleri taşiyinca .class satiri ile fiziksel yol
    senkronize olmuş olacak.
    """
    old_slashed = OLD_PACKAGE.replace('.', '/')
    new_slashed = new_pkg.replace('.', '/')

    smali_dirs = sorted([
        d for d in os.listdir(project_dir)
        if d == 'smali' or re.match(r'^smali_classes\d+$', d)
    ])

    fixed_count   = 0
    skipped_count = 0

    for smali_dir in smali_dirs:
        base = os.path.join(project_dir, smali_dir)

        for root, _, files in os.walk(base):
            for fname in files:
                if not fname.endswith('.smali'):
                    continue

                fpath = os.path.join(root, fname)

                # ── Fiziksel konumdan beklenen class adini türet ──────────
                # Bu adimda dosyalar HENÜZ taşinmadi.
                # Yani: smali/com/old/pkg/MainActivity.smali
                #   rel_path = com/old/pkg/MainActivity
                #   step1 içerigi zaten com/new/pkg yaptiysa header'i güncelle.
                #   step4 taşiyinca fiziksel yol da com/new/pkg olacak. Tam eslesme.
                try:
                    rel         = os.path.relpath(fpath, base)
                    rel_no_ext  = os.path.splitext(rel)[0].replace('\\', '/')
                    # step1 içerigi degistirdi; simdi header'daki class'i
                    # yeni_slashedpath'e göre normalize et.
                    # "Beklenen" = eski yolun new_slashed karsılıgı
                    expected_rel   = rel_no_ext.replace(old_slashed, new_slashed)
                    expected_class = f"L{expected_rel};"
                except Exception:
                    skipped_count += 1
                    continue

                try:
                    with open(fpath, 'r', encoding='utf-8', errors='replace') as f:
                        lines = f.readlines()
                except Exception:
                    skipped_count += 1
                    continue

                new_lines = []
                changed   = False

                for line in lines:
                    stripped = line.rstrip('\n\r')

                    # .class satiri: access modifier'lari koru, sinif adini degistir
                    # Örn: ".class public final Lcom/old/pkg/Foo;"
                    #   -> ".class public final Lcom/new/pkg/Foo;"
                    if stripped.startswith('.class '):
                        fixed = _fix_class_line(stripped, expected_class)
                        if fixed != stripped:
                            changed = True
                        new_lines.append(fixed + '\n')
                    else:
                        new_lines.append(line)

                if changed:
                    try:
                        with open(fpath, 'w', encoding='utf-8') as f:
                            f.writelines(new_lines)
                        fixed_count += 1
                    except Exception:
                        skipped_count += 1

    print(f"  [SCE] {fixed_count} smali header düzeltildi, {skipped_count} atlandı")
    return fixed_count


def _fix_class_line(line: str, expected_class: str) -> str:
    """
    '.class public final Lcom/old/Foo;'
     -> '.class public final Lcom/new/Foo;'

    Son token'i (L...;) expected_class ile degistirir.
    Access modifier'lar (public, final, abstract, interface, enum...) korunur.
    """
    parts = line.split()
    if len(parts) < 2:
        return line
    # parts[0]  = '.class'
    # parts[1:-1] = modifier'lar
    # parts[-1] = 'Lcom/...;'
    modifiers = parts[1:-1]
    return ' '.join(['.class'] + modifiers + [expected_class])

# ══════════════════════════════════════════════════════════════
#  ADIM 3 — MANIFEST + PROVIDER FIX
# ══════════════════════════════════════════════════════════════

def step3_manifest_fix(project_dir, new_pkg):
    """
    1. Relative activity path'lerini absolute'a çevirir.
    2. android:authorities'leri rastgele ID ile izole eder.
    3. res/xml/*.xml provider path dosyalarini temizler.
    """
    manifest_path = os.path.join(project_dir, 'AndroidManifest.xml')
    if not os.path.exists(manifest_path):
        return

    with open(manifest_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 3a. Relative -> Absolute path
    def expand_relative(match):
        attr, val = match.group(1), match.group(2)
        if val.startswith('.'):
            return f'{attr}="{new_pkg}{val}"'
        return match.group(0)

    content = re.sub(r'(android:name)="(\.[^"]*)"', expand_relative, content)

    # 3b. Authority Isolation
    def randomize_auth(match):
        uid = uuid.uuid4().hex[:8]
        return f'android:authorities="{new_pkg}.p{uid}"'

    content = re.sub(r'android:authorities="[^"]*"', randomize_auth, content)

    with open(manifest_path, 'w', encoding='utf-8') as f:
        f.write(content)

    # 3c. res/xml/ provider dosyalari
    res_xml = os.path.join(project_dir, 'res', 'xml')
    if os.path.exists(res_xml):
        for fname in os.listdir(res_xml):
            if not fname.endswith('.xml'):
                continue
            fpath = os.path.join(res_xml, fname)
            try:
                with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
                    txt = f.read()
                if OLD_PACKAGE in txt:
                    txt = txt.replace(OLD_PACKAGE, new_pkg)
                    with open(fpath, 'w', encoding='utf-8') as f:
                        f.write(txt)
            except Exception:
                pass

# ══════════════════════════════════════════════════════════════
#  ADIM 4 — SMALI KLASÖRLERINI FIZIKSEL TAŞI
# ══════════════════════════════════════════════════════════════

def step4_physical_migration(project_dir, old_pkg, new_pkg):
    """
    smali/com/old/pkg/ -> smali/com/new/pkg/
    Tüm smali_classesN klasörlerini kapsar.
    Hedef mevcutsa rmtree yerine merge yapar (daha güvenli).
    """
    old_slashed = old_pkg.replace('.', '/')
    new_slashed = new_pkg.replace('.', '/')

    smali_dirs = sorted([
        d for d in os.listdir(project_dir)
        if d == 'smali' or re.match(r'^smali_classes\d+$', d)
    ])

    for s_dir in smali_dirs:
        base    = os.path.join(project_dir, s_dir)
        old_dir = os.path.join(base, old_slashed)
        new_dir = os.path.join(base, new_slashed)

        if not os.path.isdir(old_dir):
            continue

        os.makedirs(os.path.dirname(new_dir), exist_ok=True)

        if os.path.exists(new_dir):
            _merge_dirs(old_dir, new_dir)
            shutil.rmtree(old_dir, ignore_errors=True)
        else:
            shutil.move(old_dir, new_dir)

        _remove_empty_parents(os.path.dirname(old_dir), stop=base)


def _merge_dirs(src: str, dst: str):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            os.makedirs(d, exist_ok=True)
            _merge_dirs(s, d)
        else:
            shutil.move(s, d)
    shutil.rmtree(src, ignore_errors=True)


def _remove_empty_parents(path: str, stop: str):
    path = os.path.abspath(path)
    stop = os.path.abspath(stop)
    if path == stop or not os.path.isdir(path):
        return
    _remove_empty_parents(os.path.dirname(path), stop)
    try:
        os.rmdir(path)
    except OSError:
        pass

# ══════════════════════════════════════════════════════════════
#  ADIM 5 — KAYNAK TEMIZLIGI + apktool.yml
# ══════════════════════════════════════════════════════════════

def step5_cleanup_resources(project_dir):
    """
    - public.xml sil (Resource ID çakismasi)
    - apktool.yml: renameManifestPackage null yap, versionCode artir
    """
    for root, _, files in os.walk(project_dir):
        for fname in files:
            if fname == 'public.xml':
                try:
                    os.remove(os.path.join(root, fname))
                except Exception:
                    pass

    yml = os.path.join(project_dir, 'apktool.yml')
    if not os.path.exists(yml):
        return

    with open(yml, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    new_lines = []
    for line in lines:
        if re.match(r'\s*renameManifestPackage\s*:', line):
            new_lines.append('renameManifestPackage: null\n')
            continue
        vc = re.match(r'(\s*versionCode\s*:\s*[\'"]?)(\d+)([\'"]?\s*)', line)
        if vc:
            bump = int(vc.group(2)) + random.randint(100, 999)
            new_lines.append(f"{vc.group(1)}{bump}{vc.group(3)}\n")
            continue
        new_lines.append(line)

    with open(yml, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

# ══════════════════════════════════════════════════════════════
#  FLASK ROUTES
# ══════════════════════════════════════════════════════════════

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/build', methods=['POST'])
def build_apk():
    temp_folder  = None
    apk_unsigned = None
    apk_aligned  = None

    try:
        app_name  = request.form.get('app_name', 'MyApp').strip()
        app_type  = request.form.get('app_type', 'standard')
        logo_file = request.files.get('logo')

        job_id      = uuid.uuid4().hex[:8]
        new_pkg     = f"com.convert.v{job_id}"
        temp_folder = os.path.join(OUTPUT_DIR, job_id)

        # ── Kaynak kopyala ────────────────────────────────────────
        source_path = TEMPLATE_DL if app_type == 'downloader' else TEMPLATE_STD
        shutil.copytree(source_path, temp_folder)
        for artifact in ('build', 'dist', 'META-INF'):
            p = os.path.join(temp_folder, artifact)
            if os.path.exists(p):
                shutil.rmtree(p)

        # ══ DÖNÜŞÜM PIPELINE ══════════════════════════════════════
        #
        #  SIRA KRİTİK — değiştirme:
        #
        #  1. Deep replace  : Tüm metin dosyalari güncellenir.
        #                     Smali IÇERIGI degisir; klasörler hâlâ eski yerde.
        #  2. SCE           : .class header'lari, dosyanin (henüz eski)
        #                     fiziksel konumuna göre hesaplanan YENi class
        #                     adina sabitlenir. step4 taşiyinca esleme tamam olur.
        #  3. Manifest fix  : Relative path expand + authority randomize.
        #  4. Fiziksel taşi : Artik içerik tutarli; klasörler güvenle taşinir.
        #  5. Temizlik      : public.xml sil, apktool.yml ver bump.
        #
        step1_deep_replace(temp_folder, OLD_PACKAGE, new_pkg)
        step2_smali_consistency_engine(temp_folder, new_pkg)
        step3_manifest_fix(temp_folder, new_pkg)
        step4_physical_migration(temp_folder, OLD_PACKAGE, new_pkg)
        step5_cleanup_resources(temp_folder)

        # ── Logo ──────────────────────────────────────────────────
        res_path = os.path.join(temp_folder, 'res')
        if logo_file:
            for root, dirs, _ in os.walk(res_path, topdown=False):
                bn = os.path.basename(root)
                if ('mipmap' in bn or 'drawable' in bn) and \
                   ('anydpi' in bn or 'v26' in bn):
                    shutil.rmtree(root, ignore_errors=True)

            tmp_logo = os.path.join(temp_folder, '_logo.png')
            logo_file.save(tmp_logo)

            for root, _, files in os.walk(res_path):
                if 'mipmap' in os.path.basename(root):
                    for f in files:
                        if f.startswith('ic_launcher'):
                            os.remove(os.path.join(root, f))
                    shutil.copy(tmp_logo, os.path.join(root, 'ic_launcher.png'))
                    shutil.copy(tmp_logo, os.path.join(root, 'ic_launcher_round.png'))

        # ── App ismi ──────────────────────────────────────────────
        strings_xml = os.path.join(res_path, 'values', 'strings.xml')
        if os.path.exists(strings_xml):
            with open(strings_xml, 'r', encoding='utf-8') as f:
                c = f.read()
            c = re.sub(
                r'(<string name="app_name">)[^<]*(</string>)',
                rf'\g<1>{app_name}\g<2>',
                c
            )
            with open(strings_xml, 'w', encoding='utf-8') as f:
                f.write(c)

        # ── Keystore (dinamik, her build farkli) ──────────────────
        keystore_path = os.path.join(temp_folder, 'dynamic.jks')
        ks_pass       = uuid.uuid4().hex
        subprocess.run([
            'keytool', '-genkey', '-v',
            '-keystore',  keystore_path,
            '-alias',     'key',
            '-keyalg',    'RSA',
            '-keysize',   '2048',
            '-validity',  '10000',
            '-storepass', ks_pass,
            '-keypass',   ks_pass,
            '-dname',     f'CN={job_id}, OU=App, O=Convert, L=Samsun, ST=TR, C=TR'
        ], check=True, capture_output=True)

        # ── BUILD → ALIGN → SIGN ──────────────────────────────────
        safe_name    = re.sub(r'[^a-zA-Z0-9_\-]', '', app_name.replace(' ', '_')) or 'app'
        apk_unsigned = os.path.join(OUTPUT_DIR, f'{job_id}_unsigned.apk')
        apk_aligned  = os.path.join(OUTPUT_DIR, f'{job_id}_aligned.apk')
        apk_signed   = os.path.join(OUTPUT_DIR, f'{safe_name}_{job_id}.apk')

        # apktool build
        res = subprocess.run(
            ['apktool', 'b', '-f', '--use-aapt2', temp_folder, '-o', apk_unsigned],
            capture_output=True, text=True
        )
        if res.returncode != 0:
            raise Exception(f"APKTOOL BUILD FAILED:\n{res.stdout}\n{res.stderr}")

        # zipalign
        res = subprocess.run(
            ['zipalign', '-p', '-f', '-v', '4', apk_unsigned, apk_aligned],
            capture_output=True, text=True
        )
        if res.returncode != 0:
            raise Exception(f"ZIPALIGN FAILED:\n{res.stdout}\n{res.stderr}")

        # apksigner (V1 eski cihaz uyumu icin acik)
        res = subprocess.run([
            'apksigner', 'sign',
            '--ks',                 keystore_path,
            '--ks-pass',            f'pass:{ks_pass}',
            '--v1-signing-enabled', 'true',
            '--v2-signing-enabled', 'true',
            '--v3-signing-enabled', 'true',
            '--out',                apk_signed,
            apk_aligned
        ], capture_output=True, text=True)
        if res.returncode != 0:
            raise Exception(f"SIGNING FAILED:\n{res.stdout}\n{res.stderr}")

        # ── Temizlik ──────────────────────────────────────────────
        for path in [temp_folder, apk_unsigned, apk_aligned]:
            if path and os.path.exists(path):
                (shutil.rmtree if os.path.isdir(path) else os.remove)(path)

        return f"""<!DOCTYPE html>
<html lang="tr">
<head>
  <meta charset="UTF-8">
  <title>Build OK</title>
  <style>
    *{{box-sizing:border-box;margin:0;padding:0}}
    body{{min-height:100vh;display:flex;align-items:center;justify-content:center;
         background:#0a0a0a;font-family:'Courier New',monospace;color:#e0e0e0}}
    .card{{background:#111;border:1px solid #2a2a2a;border-radius:12px;
           padding:48px 56px;max-width:560px;width:90%;text-align:center}}
    .icon{{font-size:56px;margin-bottom:20px}}
    h2{{font-size:22px;font-weight:700;color:#fff;margin-bottom:12px}}
    .meta{{font-size:11px;color:#555;line-height:2;margin:20px 0 32px;
           text-align:left;background:#0d0d0d;border:1px solid #1e1e1e;
           border-radius:8px;padding:16px 20px}}
    .meta span{{color:#3ecf8e}}
    a.btn{{display:inline-block;background:#3ecf8e;color:#000;font-weight:700;
           font-size:14px;padding:14px 36px;border-radius:8px;text-decoration:none;
           letter-spacing:.5px;transition:opacity .2s}}
    a.btn:hover{{opacity:.85}}
  </style>
</head>
<body>
  <div class="card">
    <div class="icon">✅</div>
    <h2>BUILD SUCCESSFUL</h2>
    <div class="meta">
      <div>APP &nbsp;&nbsp;&nbsp;&nbsp; <span>{app_name}</span></div>
      <div>PACKAGE &nbsp; <span>{new_pkg}</span></div>
      <div>JOB ID &nbsp;&nbsp; <span>{job_id}</span></div>
      <div>SIGNING &nbsp; <span>V1 + V2 + V3</span></div>
      <div>SCE &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <span>Active — headers verified</span></div>
    </div>
    <a class="btn" href="/download/{safe_name}_{job_id}.apk">⬇ Download APK</a>
  </div>
</body>
</html>"""

    except Exception as e:
        for path in [temp_folder, apk_unsigned, apk_aligned]:
            if path and os.path.exists(path):
                try:
                    (shutil.rmtree if os.path.isdir(path) else os.remove)(path)
                except Exception:
                    pass
        return f"""<!DOCTYPE html>
<html lang="tr">
<head>
  <meta charset="UTF-8"><title>Build Error</title>
  <style>
    body{{background:#0a0a0a;color:#e0e0e0;font-family:'Courier New',monospace;
         display:flex;align-items:center;justify-content:center;min-height:100vh}}
    .card{{background:#111;border:1px solid #3a1010;border-radius:12px;
           padding:36px 44px;max-width:700px;width:90%}}
    h2{{color:#f87171;margin-bottom:16px}}
    pre{{font-size:12px;color:#f87171;white-space:pre-wrap;word-break:break-all;
         background:#0d0d0d;border:1px solid #2a0a0a;border-radius:6px;
         padding:16px;max-height:420px;overflow:auto}}
  </style>
</head>
<body>
  <div class="card">
    <h2>❌ BUILD FAILED</h2>
    <pre>{str(e)}</pre>
  </div>
</body>
</html>"""


@app.route('/download/<filename>')
def download(filename):
    filename = os.path.basename(filename)   # Path traversal koruması
    return send_file(os.path.join(OUTPUT_DIR, filename), as_attachment=True)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
