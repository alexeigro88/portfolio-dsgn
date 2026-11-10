# Схема пользовательского флоу для кейса: шаги слева направо + ответвления под нужным шагом.
# Рендер HTML в Playwright, стиль — как у сайта (Helvetica Neue / Inter, синий акцент, squircle).
from playwright.sync_api import sync_playwright
from PIL import Image
import io, html

CSS = '''
*{box-sizing:border-box;margin:0}
body{width:1200px;height:600px;background:linear-gradient(#f3f4f7,#e5e8ef);font-family:"Helvetica Neue",Helvetica,Inter,Arial,sans-serif;display:flex;flex-direction:column;justify-content:center;padding:0 48px}
.row{display:flex;align-items:center;gap:0}
.s{flex:1;background:#fff;border-radius:22px;corner-shape:squircle;padding:22px 20px;box-shadow:0 18px 40px -22px rgba(20,22,50,.25),inset 0 0 0 1px rgba(0,0,0,.04);min-height:132px}
.s .n{font-size:13px;color:#256fff;font-variant-numeric:tabular-nums}
.s b{display:block;font-weight:500;font-size:21px;letter-spacing:-.02em;margin-top:10px;color:#1d1d1f}
.s p{font-size:14px;color:#5e5e63;margin-top:6px;line-height:1.4}
.s.last{background:#256fff}.s.last .n{color:rgba(255,255,255,.75)}.s.last b{color:#fff}.s.last p{color:rgba(255,255,255,.85)}
.ar{width:34px;flex:none;display:grid;place-items:center;color:#256fff}
.br{display:flex;gap:0;margin-top:18px}
.br .slot{flex:1}.br .gap{width:34px;flex:none}
.br .b{margin-left:14px;border-left:2px dashed #b9c6e6;padding:14px 0 0 16px}
.br .b span{display:inline-block;background:rgba(255,255,255,.7);border-radius:12px;corner-shape:squircle;padding:9px 14px;font-size:14px;color:#3a3a3e;box-shadow:inset 0 0 0 1px rgba(0,0,0,.05)}
'''

ARROW = '<svg width="18" height="18" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M3 8h10M9 4l4 4-4 4"/></svg>'


def render_flow(out, steps, branches=(), size=(2400, 1200)):
    cells = []
    for i, (t, d) in enumerate(steps):
        cls = 's last' if i == len(steps) - 1 else 's'
        cells.append(f'<div class="{cls}"><span class="n">{i+1:02d}</span><b>{html.escape(t)}</b><p>{html.escape(d)}</p></div>')
        if i < len(steps) - 1: cells.append(f'<div class="ar">{ARROW}</div>')
    br = []
    for i in range(len(steps)):
        items = [html.escape(t) for t, at in branches if at == i + 1]
        inner = '<div class="b">' + ' '.join(f'<span>{x}</span>' for x in items) + '</div>' if items else ''
        br.append(f'<div class="slot">{inner}</div>')
        if i < len(steps) - 1: br.append('<div class="gap"></div>')
    doc = f'<html><head><style>{CSS}</style></head><body><div class="row">{"".join(cells)}</div><div class="br">{"".join(br)}</div></body></html>'
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1200, 'height': 600}, device_scale_factor=size[0] / 1200)
        pg.set_content(doc); pg.wait_for_timeout(200)
        img = Image.open(io.BytesIO(pg.screenshot())).convert('RGB')
        b.close()
    img.resize(size, Image.LANCZOS).save(out, quality=88, optimize=True)
