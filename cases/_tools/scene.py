# 3D-сцены для визуалов кейса: изометрия, экраны в перспективе, крупный план поверх экрана, девайсы.
# HTML + CSS 3D рендерится в Playwright (DPR 2). Картинки подключаются как file:// пути.
# Браузер: CHROME_PATH=/opt/pw-browsers/chromium, если Python-Playwright не совпадает с установленным Chromium.
import os, io
from playwright.sync_api import sync_playwright
from PIL import Image

BASE = '''
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:%(w)dpx;height:%(h)dpx;overflow:hidden}
body{font-family:Inter,"Helvetica Neue",Arial,sans-serif;color:#111827;
  background:radial-gradient(120%% 90%% at 70%% 10%%,#fff7f1 0%%,#f3f4f7 45%%,#e6e9f0 100%%);position:relative}
.grid{position:absolute;inset:0;background-image:radial-gradient(rgba(15,26,46,.10) 1px,transparent 1.2px);background-size:22px 22px;
  -webkit-mask-image:radial-gradient(80%% 70%% at 50%% 50%%,#000 30%%,transparent 85%%)}
.glow{position:absolute;border-radius:50%%;filter:blur(60px);opacity:.55}
.scr{position:absolute;border-radius:10px;overflow:hidden;background:#fff;
  box-shadow:0 1px 0 rgba(255,255,255,.6) inset,0 0 0 1px rgba(15,26,46,.06),0 30px 60px -20px rgba(15,26,46,.35),0 12px 24px -12px rgba(15,26,46,.25)}
.scr img,.card img{display:block;width:100%%;height:100%%;object-fit:cover;object-position:top left}
.card{position:absolute;border-radius:14px;overflow:hidden;background:#fff;
  box-shadow:0 0 0 1px rgba(15,26,46,.06),0 40px 80px -24px rgba(15,26,46,.45),0 16px 32px -16px rgba(15,26,46,.3)}
.pin{position:absolute;display:flex;align-items:center;gap:8px;background:#fff;border-radius:999px;padding:6px 12px 6px 6px;font-size:13px;font-weight:500;
  box-shadow:0 0 0 1px rgba(15,26,46,.06),0 10px 24px -10px rgba(15,26,46,.35);white-space:nowrap}
.pin i{font-style:normal;width:22px;height:22px;border-radius:50%%;background:#EE6A1F;color:#fff;display:grid;place-items:center;font-size:11px;font-weight:600}
.dot{position:absolute;width:14px;height:14px;border-radius:50%%;background:#EE6A1F;box-shadow:0 0 0 6px rgba(238,106,31,.18),0 0 0 14px rgba(238,106,31,.08)}
'''


def src(path): return 'file://' + os.path.abspath(path)


def render(out, body, size, css='', q=88):
    """Рендер сцены: size — итоговый размер в пикселях, макет в CSS-пикселях = size/2."""
    w, h = size[0] // 2, size[1] // 2
    doc = f'<html><head><style>{BASE % {"w": w, "h": h}}{css}</style></head><body>{body}</body></html>'
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=os.environ.get('CHROME_PATH') or None, args=['--allow-file-access-from-files'])
        pg = b.new_page(viewport={'width': w, 'height': h}, device_scale_factor=2)
        tmp = os.path.abspath(out + '.scene.html')
        open(tmp, 'w').write(doc)
        pg.goto('file://' + tmp); pg.wait_for_load_state('networkidle'); pg.wait_for_timeout(300)
        img = Image.open(io.BytesIO(pg.screenshot())).convert('RGB')
        b.close(); os.remove(tmp)
    img.save(out, quality=q, optimize=True, progressive=True)


def crop_file(img_path, box, out_path, scale=2):
    """Вырезает фрагмент из PNG 2x по координатам в CSS-пикселях и сохраняет во временный PNG."""
    im = Image.open(img_path)
    im.crop(tuple(v * scale for v in box)).save(out_path)
    return out_path


# ---------- сцены ----------

def iso_stack(out, shots, size=(2800, 1575)):
    """Изометрический стек экранов: нижний слой первый. Экраны 1440×900."""
    w, h = size[0] // 2, size[1] // 2
    sw = round(w * 0.5); sh = round(sw * 900 / 1440)
    layers = ''
    for i, s in enumerate(shots):
        layers += f'<div class="scr" style="width:{sw}px;height:{sh}px;left:{-sw/2}px;top:{-sh/2}px;transform:translateZ({i*95}px)"><img src="{src(s)}"></div>'
    body = f'''<div class="grid"></div>
<div class="glow" style="width:520px;height:520px;right:6%;top:-10%;background:#ffb987"></div>
<div class="glow" style="width:420px;height:420px;left:4%;bottom:-20%;background:#c9d6ff"></div>
<div style="position:absolute;left:50%;top:66%;transform-style:preserve-3d;transform:rotateX(55deg) rotateZ(-38deg)">{layers}</div>'''
    render(out, body, size)


def focus(out, screen, crop, size=(900, 1020), tilt=-22, cw=0.82, cx=0.5, cy=0.56, dots=()):
    """Крупный план: экран в перспективе на фоне + увеличенный фрагмент (PNG) впереди."""
    w, h = size[0] // 2, size[1] // 2
    cim = Image.open(crop); r = cim.height / cim.width
    cardw = round(w * cw); cardh = round(cardw * r)
    if cardh > h * 0.84: cardh = round(h * 0.84); cardw = round(cardh / r)
    sw = round(w * 1.5); sh = round(sw * 900 / 1440)
    d = ''.join(f'<div class="dot" style="left:{x*cardw-7}px;top:{y*cardh-7}px"></div>' for x, y in dots)
    body = f'''<div class="grid"></div>
<div class="glow" style="width:300px;height:300px;right:-10%;top:-8%;background:#ffc7a1"></div>
<div style="position:absolute;inset:0;perspective:1200px">
  <div class="scr" style="width:{sw}px;height:{sh}px;left:{w*0.5-sw*0.42}px;top:{h*0.5-sh*0.5}px;transform:rotateX(18deg) rotateY({tilt}deg) rotateZ(4deg);opacity:.9;filter:saturate(.85)"><img src="{src(screen)}"></div>
</div>
<div style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(243,244,247,.15),rgba(230,233,240,.55))"></div>
<div class="card" style="width:{cardw}px;height:{cardh}px;left:{w*cx-cardw/2}px;top:{h*cy-cardh/2}px"><img src="{src(crop)}">{d}</div>'''
    render(out, body, size)


def journey(out, steps, size=(2400, 1200)):
    """Флоу из реальных экранов: карточки в перспективе с номерами и подписями. steps=[(png, title, sub)]."""
    w, h = size[0] // 2, size[1] // 2
    n = len(steps); sw = round(w / (n * 0.86)); sh = round(sw * 900 / 1440)
    gap = (w - 80 - sw) / (n - 1)
    cards = ''
    for i, (s, t, d) in enumerate(steps):
        x = 40 + i * gap
        last = i == n - 1
        cards += f'''<div class="scr" style="width:{sw}px;height:{sh}px;left:{x}px;top:{h*0.36-sh/2}px;transform:rotateY(-24deg) rotateX(6deg);z-index:{i}"><img src="{src(s)}"></div>
<div style="position:absolute;left:{x+8}px;top:{h*0.36+sh/2+46}px;width:{gap-16}px">
  <div style="display:flex;align-items:center;gap:8px;font-size:12px;color:{'#EE6A1F' if last else '#6B7280'};font-weight:500;letter-spacing:.04em">
    <span style="width:24px;height:24px;border-radius:50%;display:grid;place-items:center;background:{'#EE6A1F' if last else '#fff'};color:{'#fff' if last else '#111827'};box-shadow:0 0 0 1px rgba(15,26,46,.1)">{i+1}</span>STEP {i+1:02d}</div>
  <div style="font-size:19px;font-weight:600;letter-spacing:-.02em;margin-top:10px">{t}</div>
  <div style="font-size:13px;color:#4B5563;margin-top:4px;line-height:1.4">{d}</div></div>'''
    line = f'<div style="position:absolute;left:52px;right:52px;top:{h*0.36+sh/2+57}px;border-top:2px dashed rgba(238,106,31,.45)"></div>'
    body = f'<div class="grid"></div><div class="glow" style="width:420px;height:420px;right:-6%;top:-20%;background:#ffc7a1"></div><div style="position:absolute;inset:0;perspective:1600px">{cards}</div>{line}'
    render(out, body, size)


def exploded(out, base, scrim_on, modal, toast=None, size=(2400, 1200), labels=()):
    """Взорванная анатомия экрана по уровням высоты: страница → затемнение → модалка (→ тост)."""
    w, h = size[0] // 2, size[1] // 2
    sw = round(w * 0.46); sh = round(sw * 900 / 1440)
    mim = Image.open(modal); mw = round(sw * mim.width / 2880 * 1.0); mh = round(mw * mim.height / mim.width)
    lay = f'<div class="scr" style="width:{sw}px;height:{sh}px;left:{-sw/2}px;top:{-sh/2}px"><img src="{src(base)}"></div>'
    lay += f'<div style="position:absolute;width:{sw}px;height:{sh}px;left:{-sw/2}px;top:{-sh/2}px;border-radius:10px;background:rgba(15,26,46,.2);transform:translateZ(130px);backdrop-filter:blur(1px);box-shadow:0 0 0 1px rgba(255,255,255,.4) inset"></div>'
    lay += f'<div class="card" style="width:{mw}px;height:{mh}px;left:{-mw/2}px;top:{-mh/2}px;transform:translateZ(260px)"><img src="{src(modal)}"></div>'
    if toast:
        tim = Image.open(toast); tw = round(sw * tim.width / 2880); th = round(tw * tim.height / tim.width)
        lay += f'<div class="card" style="width:{tw}px;height:{th}px;left:{-tw/2}px;top:{sh/2-th-30}px;transform:translateZ(380px);border-radius:10px"><img src="{src(toast)}"></div>'
    pins = ''.join(f'<div class="pin" style="left:{x*w}px;top:{y*h}px"><i>{k}</i>{t}</div>' for k, (t, x, y) in enumerate(labels, 1))
    body = f'''<div class="grid"></div>
<div class="glow" style="width:500px;height:500px;right:2%;top:-14%;background:#ffc29b"></div>
<div style="position:absolute;left:50%;top:58%;transform-style:preserve-3d;transform:rotateX(56deg) rotateZ(-36deg)">{lay}</div>{pins}'''
    render(out, body, size)


LAPTOP_CSS = '''
.lap{position:absolute;left:50%;transform:translateX(-50%)}
.lid{background:linear-gradient(#2a2d33,#16181c);border-radius:22px 22px 8px 8px;padding:14px 14px 18px;box-shadow:0 0 0 1.5px #3a3d44 inset,0 50px 90px -30px rgba(15,26,46,.55)}
.lid .cam{width:6px;height:6px;border-radius:50%;background:#3b3f47;margin:-8px auto 4px}
.lid .sc{border-radius:6px;overflow:hidden;background:#000}
.lid .sc img{display:block;width:100%}
.base{height:16px;margin:0 -7%;background:linear-gradient(#dfe2e8,#b8bcc6);border-radius:0 0 18px 18px;position:relative;box-shadow:0 22px 40px -18px rgba(15,26,46,.45)}
.base::before{content:"";position:absolute;left:50%;top:0;width:16%;height:6px;transform:translateX(-50%);background:#a9aeb8;border-radius:0 0 8px 8px}
.mon .lid{border-radius:16px;padding:12px}
.stand{width:22%;height:70px;margin:0 auto;background:linear-gradient(90deg,#c9cdd5,#eef0f3,#c9cdd5);clip-path:polygon(18% 0,82% 0,100% 100%,0 100%)}
.foot{width:38%;height:10px;margin:0 auto;background:linear-gradient(#e3e6eb,#b9bec8);border-radius:6px;box-shadow:0 18px 30px -12px rgba(15,26,46,.4)}
'''


def laptop(out, shot, size=(2400, 1200), width=0.62, top=0.08):
    w, h = size[0] // 2, size[1] // 2
    lw = round(w * width)
    body = f'''<div class="grid"></div><div class="glow" style="width:520px;height:420px;left:50%;top:10%;transform:translateX(-50%);background:#ffd3b5"></div>
<div class="lap" style="width:{lw}px;top:{h*top}px"><div class="lid"><div class="cam"></div><div class="sc"><img src="{src(shot)}"></div></div><div class="base"></div></div>'''
    render(out, body, size, LAPTOP_CSS)


def monitor(out, shot, size=(1600, 1000), width=0.74, top=0.07):
    w, h = size[0] // 2, size[1] // 2
    lw = round(w * width)
    body = f'''<div class="grid"></div><div class="glow" style="width:360px;height:300px;right:0;top:0;background:#ffd3b5"></div>
<div class="lap mon" style="width:{lw}px;top:{h*top}px"><div class="lid"><div class="sc"><img src="{src(shot)}"></div></div><div class="stand"></div><div class="foot"></div></div>'''
    render(out, body, size, LAPTOP_CSS)


def pair(out, back, front, size=(1600, 1000), labels=('', '')):
    """Два экрана внахлёст в перспективе (до/после, загрузка/результат)."""
    w, h = size[0] // 2, size[1] // 2
    sw = round(w * 0.7); sh = round(sw * 900 / 1440)
    lb = ''.join(f'<div class="pin" style="left:{x}px;top:{y}px"><i>{k}</i>{t}</div>' for k, (t, x, y) in enumerate([(labels[0], w*0.06, h*0.1), (labels[1], w*0.6, h*0.86)], 1) if t)
    body = f'''<div class="grid"></div><div class="glow" style="width:320px;height:320px;right:-4%;top:-10%;background:#ffc7a1"></div>
<div style="position:absolute;inset:0;perspective:1400px">
<div class="scr" style="width:{sw}px;height:{sh}px;left:{w*0.06}px;top:{h*0.2}px;transform:rotateY(18deg) rotateX(4deg);filter:saturate(.8)"><img src="{src(back)}"></div>
<div class="scr" style="width:{sw}px;height:{sh}px;left:{w*0.26}px;top:{h*0.3}px;transform:rotateY(18deg) rotateX(4deg)"><img src="{src(front)}"></div></div>{lb}'''
    render(out, body, size)


# ---------- лоу-фай вайрфреймы (1440×900) ----------

WF_CSS = '''
body{background:#fbfbf8;font-family:"Comic Neue","Segoe Print","Bradley Hand","Helvetica Neue",Arial,sans-serif;color:#5b6170}
.paper{position:absolute;inset:0;background-image:linear-gradient(rgba(70,90,140,.07) 1px,transparent 1px),linear-gradient(90deg,rgba(70,90,140,.07) 1px,transparent 1px);background-size:24px 24px}
.b{position:absolute;border:2px solid #9aa1ae;border-radius:6px}
.f{position:absolute;background:#e3e5ea;border-radius:4px}
.d{position:absolute;border:2px dashed #b4b9c3;border-radius:6px}
.x{position:absolute;border:2px solid #b4b9c3;border-radius:4px;background:
 linear-gradient(to top right,transparent calc(50% - 1px),#c8ccd4 calc(50% - 1px),#c8ccd4 calc(50% + 1px),transparent calc(50% + 1px)),
 linear-gradient(to bottom right,transparent calc(50% - 1px),#c8ccd4 calc(50% - 1px),#c8ccd4 calc(50% + 1px),transparent calc(50% + 1px))}
.t{position:absolute;font-size:15px;color:#6b7280;white-space:nowrap}
.h{position:absolute;font-size:30px;font-weight:700;color:#4b5263}
.n{position:absolute;font-size:16px;color:#e4600f;transform:rotate(-3deg);white-space:nowrap}
.c{position:absolute;border-radius:50%;border:2px solid #9aa1ae}
.ac{position:absolute;border:2.5px solid #e4600f;border-radius:6px;background:rgba(238,106,31,.08)}
'''


def _wf(out, inner):
    body = '<div class="paper"></div>' + inner
    doc = f'<html><head><style>{BASE % {"w": 1440, "h": 900}}{WF_CSS}</style></head><body>{body}</body></html>'
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=os.environ.get('CHROME_PATH') or None)
        pg = b.new_page(viewport={'width': 1440, 'height': 900}, device_scale_factor=2)
        pg.set_content(doc); pg.wait_for_timeout(150); pg.screenshot(path=out)
        b.close()


def _shell(title):
    s = '<div class="b" style="left:16px;top:16px;width:230px;height:868px"></div><div class="x" style="left:36px;top:36px;width:120px;height:34px"></div>'
    for i in range(8): s += f'<div class="f" style="left:36px;top:{110+i*44}px;width:{150 if i%3 else 180}px;height:16px"></div>'
    s += f'<div class="h" style="left:276px;top:34px">{title}</div><div class="ac" style="left:1290px;top:36px;width:124px;height:40px"></div><div class="b" style="left:1170px;top:36px;width:104px;height:40px"></div>'
    return s


def wf_list(out):
    s = _shell('Leads')
    s += '<div class="b" style="left:276px;top:100px;width:420px;height:42px"></div>'
    for i, wd in enumerate([110, 110, 130, 110]): s += f'<div class="b" style="left:{716+i*126}px;top:100px;width:{wd}px;height:42px;border-radius:21px"></div>'
    for i, t in enumerate(['All', 'New', 'Needs info', 'Contacted', 'Qualified', '...']): s += f'<div class="t" style="left:{280+i*130}px;top:170px">{t} (n)</div>'
    s += '<div class="f" style="left:276px;top:196px;width:70px;height:4px;background:#9aa1ae"></div>'
    s += '<div class="b" style="left:276px;top:214px;width:1144px;height:620px"></div>'
    for r in range(9):
        y = 240 + r * 64
        s += f'<div class="c" style="left:296px;top:{y}px;width:34px;height:34px"></div><div class="f" style="left:346px;top:{y+4}px;width:160px;height:12px"></div><div class="f" style="left:346px;top:{y+22}px;width:110px;height:9px"></div>'
        s += f'<div class="f" style="left:560px;top:{y+10}px;width:230px;height:12px"></div><div class="d" style="left:830px;top:{y+4}px;width:90px;height:26px;border-radius:13px"></div>'
        s += f'<div class="f" style="left:960px;top:{y+10}px;width:70px;height:12px"></div><div class="f" style="left:1080px;top:{y+10}px;width:130px;height:12px"></div><div class="t" style="left:1360px;top:{y+6}px">⋯</div>'
    s += '<div class="n" style="left:860px;top:212px">status pill?</div><div class="n" style="left:1210px;top:860px">pagination + per page</div>'
    s += '<div class="n" style="left:1100px;top:156px">→ ⋯ menu: convert, status, archive</div>'
    _wf(out, s)


def wf_profile(out):
    s = _shell('John Doe')
    s += '<div class="b" style="left:276px;top:96px;width:1144px;height:150px"></div><div class="c" style="left:300px;top:120px;width:64px;height:64px"></div>'
    s += '<div class="f" style="left:384px;top:132px;width:220px;height:18px"></div><div class="f" style="left:384px;top:160px;width:120px;height:12px"></div>'
    s += '<div class="ac" style="left:1210px;top:120px;width:186px;height:40px"></div><div class="n" style="left:1150px;top:170px">Convert — only when Qualified</div>'
    for i in range(4): s += f'<div class="f" style="left:{300+i*270}px;top:204px;width:250px;height:8px;{"background:#9aa1ae" if i==0 else ""}"></div>'
    for i, (t, hh) in enumerate([('Contact', 170), ('Company', 150), ('Project', 210)]):
        y = 270 + sum([190, 170, 230][:i])
        s += f'<div class="b" style="left:276px;top:{y}px;width:800px;height:{hh}px"></div><div class="t" style="left:296px;top:{y+16}px;font-weight:700">{t}</div>'
        for k in range(2): s += f'<div class="f" style="left:{296+k*380}px;top:{y+56}px;width:240px;height:12px"></div><div class="f" style="left:{296+k*380}px;top:{y+96}px;width:180px;height:12px"></div>'
    s += '<div class="b" style="left:1096px;top:270px;width:324px;height:170px"></div><div class="t" style="left:1116px;top:286px;font-weight:700">Owner</div><div class="ac" style="left:1116px;top:380px;width:130px;height:36px"></div>'
    s += '<div class="b" style="left:1096px;top:460px;width:324px;height:330px"></div><div class="t" style="left:1116px;top:476px;font-weight:700">Details</div>'
    for k in range(6): s += f'<div class="f" style="left:1116px;top:{520+k*42}px;width:110px;height:10px"></div><div class="f" style="left:1300px;top:{520+k*42}px;width:96px;height:10px"></div>'
    s += '<div class="n" style="left:1100px;top:440px">assign to me = 1 click</div>'
    _wf(out, s)


def wf_convert(out):
    s = _shell('Leads')
    s += '<div class="f" style="left:276px;top:100px;width:1144px;height:740px;background:#eceef1"></div>'
    s += '<div class="b" style="left:460px;top:200px;width:520px;height:480px;background:#fbfbf8"></div><div class="t" style="left:484px;top:222px;font-size:22px;font-weight:700">Convert to opportunity</div>'
    for k, t in enumerate(['Account — new / existing', 'Contact', 'Opportunity · Prospecting']):
        y = 290 + k * 84
        s += f'<div class="b" style="left:484px;top:{y}px;width:472px;height:68px"></div><div class="x" style="left:500px;top:{y+16}px;width:36px;height:36px"></div><div class="t" style="left:552px;top:{y+22}px">{t}</div>'
    s += '<div class="d" style="left:484px;top:550px;width:472px;height:50px"></div><div class="t" style="left:500px;top:564px">what happens to the lead…</div>'
    s += '<div class="b" style="left:700px;top:620px;width:100px;height:40px"></div><div class="ac" style="left:816px;top:620px;width:140px;height:40px"></div>'
    s += '<div class="n" style="left:1000px;top:300px">no inputs — just preview</div><div class="n" style="left:1000px;top:630px">loading → redirect to deal</div>'
    _wf(out, s)


def evolution(out, stages, size=(2400, 1200)):
    """Три стадии в перспективе слева направо: [(png, label, sub)] — вайрфрейм → UI-kit → интерфейс."""
    w, h = size[0] // 2, size[1] // 2
    sw = round(w * 0.45); sh = round(sw * 900 / 1440)
    cards = ''
    for i, (s, t, d) in enumerate(stages):
        x = 40 + i * (w - 80 - sw) / (len(stages) - 1)
        cards += f'''<div class="scr" style="width:{sw}px;height:{sh}px;left:{x}px;top:{h*0.45-sh/2+i*-14}px;transform:rotateY(-28deg) rotateX(8deg);z-index:{i}"><img src="{src(s)}"></div>
<div class="pin" style="left:{x+30}px;top:{h*0.45+sh/2+56}px"><i>{i+1}</i>{t}<span style="color:#6B7280;font-weight:400">&nbsp;· {d}</span></div>'''
    body = f'<div class="grid"></div><div class="glow" style="width:480px;height:420px;right:-6%;top:-18%;background:#ffc29b"></div><div style="position:absolute;inset:0;perspective:1500px">{cards}</div>'
    render(out, body, size)


def hero_drone(out, art, shots, size=(2800, 1575)):
    """Обложка: иллюстрация (дрон сканирует здание) слева на тёмном фоне + экраны продукта в перспективе справа."""
    w, h = size[0] // 2, size[1] // 2
    aw = round(h * 1024 / 1536 * 1.32)
    sw = round(w * 0.47); sh = round(sw * 900 / 1440)
    scr = ''
    for i, s in enumerate(shots):
        scr += f'<div class="scr" style="width:{sw}px;height:{sh}px;left:{w*0.42+i*w*0.09}px;top:{h*0.16+i*h*0.21}px;transform:rotateY(-22deg) rotateX(8deg) rotateZ(1deg);box-shadow:0 0 0 1px rgba(255,255,255,.08),0 50px 90px -30px rgba(0,0,0,.7),0 0 80px -10px rgba(70,140,255,.25)"><img src="{src(s)}"></div>'
    body = f'''<div style="position:absolute;inset:0;background:radial-gradient(90% 90% at 75% 40%,#13254a 0%,#0a1428 55%,#060c1a 100%)"></div>
<div style="position:absolute;left:{w*0.015}px;top:-{h*0.16}px;width:{aw}px;height:{round(aw*1.5)}px;background:url('{src(art)}') center/cover"></div>
<div style="position:absolute;inset:0;background:linear-gradient(90deg,rgba(6,12,26,0) 0%,rgba(6,12,26,0) 32%,rgba(10,20,40,.92) 52%,rgba(10,20,40,0) 100%)"></div>
<div style="position:absolute;inset:0;background-image:linear-gradient(rgba(90,160,255,.06) 1px,transparent 1px),linear-gradient(90deg,rgba(90,160,255,.06) 1px,transparent 1px);background-size:32px 32px;-webkit-mask-image:linear-gradient(90deg,transparent 35%,#000 70%)"></div>
<div class="glow" style="width:420px;height:420px;right:4%;top:-12%;background:#ee6a1f;opacity:.28"></div>
<div style="position:absolute;inset:0;perspective:1500px">{scr}</div>'''
    render(out, body, size)
