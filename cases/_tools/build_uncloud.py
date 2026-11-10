# Визуалы кейса Uncloud360 из экспортов Figma (cases/_src/uncloud, мобильные экраны 390pt в 3x, десктоп 2x).
# Файл Figma: Uncloud360 — AI Life Coach. Экраны концепта v2 (страница «Mobile concept — v2») — с 3D-персонажем.
# Запуск из корня: CHROME_PATH=/opt/pw-browsers/chromium python3 cases/_tools/build_uncloud.py
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from PIL import Image, ImageDraw, ImageFilter
import flat as F

SRC, OUT = 'cases/_src/uncloud', 'img/cases/uncloud'
PRES = f'{OUT}/presentation'
os.makedirs(OUT, exist_ok=True); os.makedirs(PRES, exist_ok=True)

MIST, TEAL, NAVY = (240, 247, 248), (0, 180, 190), (0, 10, 30)


def p(n): return f'{SRC}/{n}.png'


def screen(n, h=844):
    """Видимая часть экрана телефона: первые 844pt (длинные экраны прокручиваются)."""
    im = Image.open(p(n)).convert('RGB')
    return im.crop((0, 0, im.width, round(im.width * h / 390)))


def phone(n, w):
    """Плоская рамка телефона: тонкий графитовый корпус, скругление, островок. Возвращает RGBA шириной w."""
    sc = screen(n)
    bez = round(w * 0.034); r = round(w * 0.15)
    sw = w - bez * 2; sh = round(sw * sc.height / sc.width)
    H = sh + bez * 2
    out = Image.new('RGBA', (w, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(out)
    d.rounded_rectangle((0, 0, w - 1, H - 1), r, fill=(22, 26, 32, 255))
    d.rounded_rectangle((2, 2, w - 3, H - 3), r - 2, outline=(70, 76, 86, 255), width=max(2, w // 300))
    s = sc.resize((sw, sh), Image.LANCZOS)
    m = Image.new('L', (sw, sh), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, sw - 1, sh - 1), r - bez, fill=255)
    out.paste(s, (bez, bez), m)
    iw, ih = round(w * 0.28), round(w * 0.075)
    d.rounded_rectangle(((w - iw) // 2, bez + round(w * 0.025), (w + iw) // 2, bez + round(w * 0.025) + ih), ih // 2, fill=(10, 12, 16, 255))
    return out


def shadow_place(cv, layer, xy, blur=50, alpha=60, dy=40):
    a = layer.split()[-1]
    sh = Image.new('RGBA', layer.size, (0, 30, 40, 0)); sh.putalpha(a.point(lambda v: v * alpha // 255))
    pad = blur * 3
    big = Image.new('RGBA', (layer.width + pad * 2, layer.height + pad * 2), (0, 0, 0, 0)); big.paste(sh, (pad, pad), sh)
    big = big.filter(ImageFilter.GaussianBlur(blur))
    cv.alpha_composite(big, (xy[0] - pad, xy[1] - pad + dy)); cv.alpha_composite(layer, xy)


def bg(size, top=(236, 247, 248), bottom=(250, 253, 253), circle=True):
    W, H = size
    cv = F.Image.new('RGBA', size)
    g = Image.new('RGB', (1, H))
    for y in range(H):
        k = y / (H - 1); g.putpixel((0, y), tuple(round(top[i] + (bottom[i] - top[i]) * k) for i in range(3)))
    cv.paste(g.resize(size), (0, 0))
    if circle:  # большой мягкий круг Mist/Teal — без свечения
        c = Image.new('RGBA', size, (0, 0, 0, 0)); d = ImageDraw.Draw(c)
        R = round(H * 0.52); cx, cy = W // 2, round(H * 0.56)
        d.ellipse((cx - R, cy - R, cx + R, cy + R), fill=(0, 180, 190, 22))
        R2 = round(R * 0.7); d.ellipse((cx - R2, cy - R2, cx + R2, cy + R2), fill=(0, 180, 190, 18))
        cv.alpha_composite(c)
    return cv


def mascot(n, w):
    im = Image.open(p(n)).convert('RGBA'); bbox = im.getbbox(); im = im.crop(bbox)
    return im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)


# ---------- обложка: три телефона + 3D-маскот ----------
def cover(size=(2800, 1575)):
    W, H = size
    cv = bg(size)
    c = phone('v2_voice', 600); l = phone('v2_home', 520); r = phone('v2_summary', 520)
    cy = round(H * 0.13)
    shadow_place(cv, l, (W // 2 - 300 - 470, cy + 120), alpha=45)
    shadow_place(cv, r, (W // 2 + 300 - 50, cy + 120), alpha=45)
    shadow_place(cv, c, (W // 2 - 300, cy), alpha=55)
    k = mascot('m/m20', 400)
    shadow_place(cv, k, (W // 2 - 300 - 470 - 330, round(H * 0.05)), blur=30, alpha=30, dy=30)
    return cv


F.save(cover(), f'{OUT}/cover.jpg')

# ---------- ряд экранов ----------
def row(names, size=(2800, 1400), w=470, gap=56):
    W, H = size
    cv = bg(size, circle=False)
    phones = [phone(n, w) for n in names]
    total = sum(x.width for x in phones) + gap * (len(phones) - 1)
    x = (W - total) // 2; y = (H - phones[0].height) // 2 - 10
    for ph in phones:
        shadow_place(cv, ph, (x, y), alpha=40); x += ph.width + gap
    return cv


F.save(row(['v2_welcome', 'v2_home', 'v2_voice', 'v2_chat', 'v2_summary']), f'{OUT}/screens-core.jpg')
F.save(row(['journal', 'paths', 'crisis', 'profile']), f'{OUT}/screens-more.jpg')

# ---------- один телефон для разделов «ключевые экраны» ----------
for n in ('v2_home', 'v2_voice', 'v2_summary', 'journal', 'crisis'):
    cv = bg((1600, 1600), circle=False)
    ph = phone(n, 640); shadow_place(cv, ph, ((1600 - ph.width) // 2, (1600 - ph.height) // 2 - 20), alpha=40)
    F.save(cv, f'{OUT}/key-{n.replace("v2_", "")}.jpg')

# ---------- маскот: виды и выражения из листа персонажа, эволюция ----------
def poses(size=(2400, 1200)):
    """Две позы 3D-персонажа: presenting и pointing."""
    W, H = size
    cv = bg(size)
    a = mascot('m/m4', 640); b = mascot('m/m20', 600)
    shadow_place(cv, a, (round(W * 0.3 - a.width / 2), round(H * 0.5 - a.height / 2)), blur=30, alpha=30, dy=30)
    shadow_place(cv, b, (round(W * 0.7 - b.width / 2), round(H * 0.5 - b.height / 2)), blur=30, alpha=30, dy=30)
    return cv


def directions(size=(2400, 900)):
    """Другие направления маскота, которые рассматривались."""
    W, H = size
    cv = bg(size, circle=False)
    items = [mascot('m/m6', 420), mascot('k3d_welcome2', 470), mascot('m/m4', 360)]
    for im, x in zip(items, [W * 0.2, W * 0.5, W * 0.8]):
        shadow_place(cv, im, (round(x - im.width / 2), round(H * 0.5 - im.height / 2)), blur=22, alpha=24, dy=22)
    return cv


F.save(poses(), f'{OUT}/mascot-poses.jpg')
F.save(directions(), f'{OUT}/mascot-evolution.jpg')

# ---------- десктоп ----------
F.save(F.tile(Image.open(p('v2_d_voice')).convert('RGB'), size=(2400, 1640), pad=110, r=22, bg=MIST), f'{OUT}/desktop-voice.jpg')  # экран целиком карточкой на Mist
d = Image.open(p('v2_d_dashboard')).convert('RGB').crop((0, 0, 2880, 1800))
F.device(f'{OUT}/desktop-dashboard.jpg', d, f'{SRC}/_tmp', 'laptop', size=(2400, 1300), width=0.74) if os.makedirs(f'{SRC}/_tmp', exist_ok=True) is None else None

# ---------- слайды для презентации (16:9, 2880×1620) ----------
import html as _h
TMP = f'{SRC}/_tmp'

def png(img, name):
    path = os.path.abspath(f'{TMP}/{name}.png'); img.save(path); return 'file://' + path

SLIDE_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@500;600;700;800&display=swap');
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:1440px;height:810px;overflow:hidden}
body{font-family:Manrope,Inter,sans-serif;color:#000A1E;background:linear-gradient(#ECF7F8,#FAFDFD);position:relative}
.circle{position:absolute;border-radius:50%;background:rgba(0,180,190,.08)}
.lbl{font-size:13px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:#00838A}
h1{font-size:76px;font-weight:800;letter-spacing:-.035em;line-height:1}
h2{font-size:52px;font-weight:800;letter-spacing:-.03em;line-height:1.05}
p{font-size:20px;line-height:1.5;color:#485052;font-weight:500}
.chip{display:inline-block;padding:8px 14px;border-radius:999px;background:#fff;box-shadow:0 0 0 1px rgba(0,10,30,.08);font-size:15px;font-weight:600;margin:0 8px 8px 0}
.pt{display:flex;gap:14px;align-items:flex-start;margin-top:22px}.pt i{flex:none;width:28px;height:28px;border-radius:50%;background:#00B4BE;color:#000A1E;font-style:normal;font-weight:800;font-size:14px;display:grid;place-items:center}
.pt b{display:block;font-size:20px;font-weight:700}.pt span{font-size:16px;color:#485052;line-height:1.45}
img{display:block}
"""

def slide(name, body):
    from playwright.sync_api import sync_playwright
    doc = f'<html><head><style>{SLIDE_CSS}</style></head><body>{body}</body></html>'
    tmp = os.path.abspath(f'{TMP}/{name}.html'); open(tmp, 'w').write(doc)
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=os.environ.get('CHROME_PATH') or None)
        pg = b.new_page(viewport={'width': 1440, 'height': 810}, device_scale_factor=2)
        pg.goto('file://' + tmp); pg.wait_for_load_state('networkidle'); pg.wait_for_timeout(400)
        pg.screenshot(path=f'{TMP}/{name}.png'); b.close()
    F.save(Image.open(f'{TMP}/{name}.png'), f'{PRES}/{name}.jpg')

ph = lambda n, w: png(phone(n, w * 2), f'ph-{n}-{w}')
ms = lambda n, w: png(mascot(n, w * 2), f'ms-{n.replace("/", "-")}-{w}')

slide('01-title', f"""<div class="circle" style="width:760px;height:760px;right:-60px;top:40px"></div>
<div style="position:absolute;left:96px;top:0;bottom:0;width:560px;display:flex;flex-direction:column;justify-content:center">
<span class="lbl">Case study · AI life coach</span><h1 style="margin-top:18px">Uncloud360</h1>
<p style="margin-top:22px;font-size:22px">A private AI coach for work, emotions and life. Talk it through in one tap and leave with one clear next step.</p>
<div style="margin-top:28px"><span class="chip">Mobile-first</span><span class="chip">AI Voice</span><span class="chip">3D character</span><span class="chip">Design system</span></div></div>
<img src="{ph('v2_home', 270)}" style="position:absolute;left:760px;top:150px;width:270px">
<img src="{ph('v2_voice', 300)}" style="position:absolute;left:960px;top:80px;width:300px;filter:drop-shadow(0 30px 40px rgba(0,40,50,.18))">
<img src="{ms('m/m20', 210)}" style="position:absolute;left:1200px;top:30px;width:210px">""")

slide('02-one-tap', f"""<div style="position:absolute;left:96px;top:0;bottom:0;width:520px;display:flex;flex-direction:column;justify-content:center">
<span class="lbl">Core idea</span><h2 style="margin-top:16px">Help is always one tap away</h2>
<div class="pt"><i>1</i><div><b>AI Voice is the hero of Home</b><span>and the centre of the tab bar on every screen.</span></div></div>
<div class="pt"><i>2</i><div><b>The mascot is the interface</b><span>it listens, thinks and speaks, with a live transcript under it.</span></div></div>
<div class="pt"><i>3</i><div><b>Every session ends with a next step</b><span>an insight, one action and the key moments are saved.</span></div></div></div>
<img src="{ph('v2_home', 290)}" style="position:absolute;left:700px;top:115px;width:290px">
<img src="{ph('v2_voice', 290)}" style="position:absolute;left:1010px;top:65px;width:290px">""")

slide('03-mascot', f"""<div style="position:absolute;left:96px;top:0;bottom:0;width:470px;display:flex;flex-direction:column;justify-content:center">
<span class="lbl">Mascot</span><h2 style="margin-top:16px">A friendly guide with a job to do</h2>
<p style="margin-top:18px">A soft 3D cloud character with a tablet. It welcomes, points to the next action and presents insights, so the AI feels approachable from the first screen.</p>
<div class="pt"><i>1</i><div><b>Presenting</b><span>Welcome, AI Voice, Profile</span></div></div>
<div class="pt"><i>2</i><div><b>Pointing</b><span>Home hero and hints next to buttons</span></div></div></div>
<div class="circle" style="width:640px;height:640px;left:700px;top:85px"></div>
<img src="{ms('m/m4', 330)}" style="position:absolute;left:690px;top:170px;width:330px">
<img src="{ms('m/m20', 320)}" style="position:absolute;left:1030px;top:150px;width:320px">""")

slide('04-screens', f"""<div style="position:absolute;left:96px;top:56px"><span class="lbl">Mobile-first</span><h2 style="margin-top:12px;font-size:44px">From welcome to session summary</h2></div>
<div style="position:absolute;left:0;right:0;top:200px;display:flex;justify-content:center;gap:26px">
{''.join(f'<img src="{ph(n, 236)}" style="width:236px">' for n in ['v2_welcome', 'v2_home', 'v2_voice', 'v2_chat', 'v2_summary'])}</div>""")

slide('05-desktop', f"""<div style="position:absolute;left:96px;top:0;bottom:0;width:420px;display:flex;flex-direction:column;justify-content:center">
<span class="lbl">Desktop</span><h2 style="margin-top:16px">Same coach on a bigger screen</h2>
<p style="margin-top:18px">Sidebar navigation, the voice session with a live transcript and insights captured on the side.</p></div>
<img src="{png(F.fit(Image.open(p('v2_d_voice')).convert('RGB'), w=1700), 'dv')}" style="position:absolute;left:560px;top:150px;width:850px;border-radius:16px;box-shadow:0 0 0 1px rgba(0,10,30,.08),0 30px 60px -30px rgba(0,40,50,.35)">""")
print('ok', sorted(os.listdir(OUT)), sorted(os.listdir(PRES)))
