# Чёткие обложки-превью (2800×1575) из настоящих экранов Figma, без генерации.
# Uncloud360: парящие карточки экранов + 3D-персонаж + вынесенные элементы UI.
# TrueScan: иллюстрация дрона, сканирующего здание, + экраны платформы.
# Запуск из корня: CHROME_PATH=/opt/pw-browsers/chromium python3 cases/_tools/build_covers.py
import os
from PIL import Image
from playwright.sync_api import sync_playwright

TMP = os.path.abspath('cases/_src/_covers'); os.makedirs(TMP, exist_ok=True)


def u(path): return 'file://' + os.path.abspath(path)


def crop_phone(src, name, h_pt=844):
    """Экран телефона 390pt: первые h_pt точек, PNG без потерь."""
    im = Image.open(src).convert('RGB'); s = im.width / 390
    im.crop((0, 0, im.width, round(h_pt * s))).save(f'{TMP}/{name}.png'); return u(f'{TMP}/{name}.png')


def cut(src, name):
    im = Image.open(src).convert('RGBA'); im.crop(im.getbbox()).save(f'{TMP}/{name}.png'); return u(f'{TMP}/{name}.png')


def render(html, out):
    doc = f'''<html><head><style>
@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@500;600;700;800&family=Inter:wght@400;500;600&display=swap');
*{{box-sizing:border-box;margin:0;padding:0}} html,body{{width:1400px;height:788px;overflow:hidden}}
img{{display:block}}
</style></head><body>{html}</body></html>'''
    p = f'{TMP}/page.html'; open(p, 'w').write(doc)
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=os.environ.get('CHROME_PATH') or None)
        pg = b.new_page(viewport={'width': 1400, 'height': 788}, device_scale_factor=2)
        pg.goto('file://' + p); pg.wait_for_load_state('networkidle'); pg.wait_for_timeout(500)
        pg.screenshot(path=f'{TMP}/shot.png'); b.close()
    Image.open(f'{TMP}/shot.png').convert('RGB').save(out, quality=94, subsampling=0, optimize=True, progressive=True)


# ---------------- Uncloud360 ----------------
U = 'cases/_src/uncloud'
home, voice, summ = crop_phone(f'{U}/v2_home.png', 'u-home'), crop_phone(f'{U}/v2_voice.png', 'u-voice'), crop_phone(f'{U}/v2_summary.png', 'u-summ')
masc = cut(f'{U}/m/m20.png', 'u-masc')
card = 'position:absolute;border-radius:34px;overflow:hidden;background:#fff;box-shadow:0 0 0 1px rgba(0,40,50,.06),0 30px 60px -28px rgba(0,50,60,.32),0 8px 18px -10px rgba(0,50,60,.14)'
chip = 'position:absolute;font-family:Manrope,sans-serif;display:flex;align-items:center;gap:8px;border-radius:999px;box-shadow:0 14px 30px -14px rgba(0,50,60,.35),0 0 0 1px rgba(0,40,50,.06)'
render(f'''
<div style="position:absolute;inset:0;background:linear-gradient(160deg,#E6F5F7 0%,#F2FAFB 55%,#FAFDFD 100%)"></div>
<div style="position:absolute;width:760px;height:760px;border-radius:50%;left:320px;top:40px;background:radial-gradient(circle,rgba(0,180,190,.14),rgba(0,180,190,.05) 60%,rgba(0,180,190,0) 72%)"></div>
<img src="{home}" style="{card};width:262px;left:250px;top:150px;border-radius:30px">
<img src="{summ}" style="{card};width:262px;right:250px;top:150px;border-radius:30px">
<img src="{voice}" style="{card};width:288px;left:556px;top:112px;z-index:2">
<img src="{masc}" style="position:absolute;width:210px;left:440px;top:8px;z-index:4;filter:drop-shadow(0 16px 20px rgba(0,50,60,.22))">
<div style="{chip};z-index:5;left:430px;top:600px;background:#000A1E;color:#fff;font-weight:700;font-size:18px;padding:14px 22px">Start session <span style="font-size:19px">→</span></div>
<div style="{chip};z-index:5;left:772px;top:530px;background:#fff;color:#00838A;font-weight:700;font-size:18px;padding:12px 20px"><i style="width:10px;height:10px;border-radius:50%;background:#00B4BE"></i>Listening</div>
<div style="position:absolute;z-index:5;left:1050px;top:560px;width:250px;background:#fff;border-radius:22px;padding:18px 20px;font-family:Manrope,sans-serif;font-weight:700;font-size:17px;line-height:1.35;color:#000A1E;box-shadow:0 18px 36px -16px rgba(0,50,60,.35),0 0 0 1px rgba(0,40,50,.06)"><span style="display:block;font-size:11px;letter-spacing:.12em;color:#00838A;margin-bottom:8px">WHAT WE UNCOVERED</span>You say yes to feel reliable — and Thursday pays for it.</div>
''', 'img/cases/uncloud/cover-sharp.jpg')

# ---------------- TrueScan ----------------
T = 'cases/_src/truescan'
def desk(src, name, s=2):
    im = Image.open(src).convert('RGB'); im.crop((0, 0, 1440 * s, 900 * s)).save(f'{TMP}/{name}.png'); return u(f'{TMP}/{name}.png')
proj, opp, prop = desk(f'{T}/project_overview.png', 't-proj'), desk(f'{T}/opp_kanban.png', 't-opp'), desk(f'{T}/proposal_builder.png', 't-prop')
drone = u(f'{T}/drone_raw1.png')
scr = 'position:absolute;border-radius:18px;overflow:hidden;background:#fff;box-shadow:0 0 0 1px rgba(255,255,255,.10),0 40px 80px -30px rgba(0,0,0,.65),0 10px 24px -12px rgba(0,0,0,.45)'
render(f'''
<div style="position:absolute;inset:0;background:radial-gradient(120% 120% at 80% 30%,#1B2C4A 0%,#0F1A2E 45%,#08101F 100%)"></div>
<img src="{drone}" style="position:absolute;left:-40px;top:-170px;width:620px">
<div style="position:absolute;inset:0;background:linear-gradient(90deg,rgba(8,16,31,0) 0%,rgba(8,16,31,0) 30%,rgba(12,22,40,.85) 44%,rgba(15,26,46,0) 70%)"></div>
<div style="position:absolute;inset:0;background-image:linear-gradient(rgba(120,160,220,.05) 1px,transparent 1px),linear-gradient(90deg,rgba(120,160,220,.05) 1px,transparent 1px);background-size:36px 36px;-webkit-mask-image:linear-gradient(90deg,transparent 35%,#000 65%)"></div>
<img src="{prop}" style="{scr};width:560px;left:790px;top:60px;opacity:.96">
<img src="{opp}" style="{scr};width:600px;left:660px;top:180px">
<img src="{proj}" style="{scr};width:640px;left:520px;top:310px;z-index:3">
''', 'img/cases/truescan/cover-sharp.jpg')
print('ok')
