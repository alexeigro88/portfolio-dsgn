# Плоские визуалы кейса: без перспективы и свечений, крупно и резко.
# Растр собирается в PIL (Lanczos), подписи — HTML в Playwright без трансформаций.
# Картинки заранее уменьшаются до точного размера в пикселях, чтобы браузер их не пережимал.
import os, io, html
from PIL import Image, ImageDraw, ImageFilter

BG = (243, 244, 246)          # нейтральный фон, как bg/subtle в TrueScan
NAVY = (11, 21, 40)
TMP = None


def save(img, path, q=92):
    img.convert('RGB').save(path, quality=q, optimize=True, progressive=True, subsampling=0)


def _mask(size, r):
    m = Image.new('L', size, 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, size[0] - 1, size[1] - 1), r, fill=255)
    return m


def _card(img, r, border=True):
    """Скругляет картинку и добавляет тонкую обводку."""
    out = Image.new('RGBA', img.size, (0, 0, 0, 0))
    out.paste(img.convert('RGB'), (0, 0), _mask(img.size, r))
    if border:
        ImageDraw.Draw(out).rounded_rectangle((0, 0, img.width - 1, img.height - 1), r, outline=(16, 24, 40, 22), width=2)
    return out


def _place(canvas, card, xy, r, blur=28, alpha=34, dy=14):
    """Мягкая, едва заметная тень (одна на элемент) + карточка."""
    pad = blur * 3
    sh = Image.new('RGBA', (card.width + pad * 2, card.height + pad * 2), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle((pad, pad, pad + card.width, pad + card.height), r, fill=(16, 24, 40, alpha))
    sh = sh.filter(ImageFilter.GaussianBlur(blur))
    canvas.alpha_composite(sh, (xy[0] - pad, xy[1] - pad + dy))
    canvas.alpha_composite(card, xy)


def crop(path, box, s=2):
    return Image.open(path).convert('RGB').crop(tuple(v * s for v in box))


def fit(img, w=None, h=None):
    k = min((w or 10 ** 9) / img.width, (h or 10 ** 9) / img.height)
    return img.resize((round(img.width * k), round(img.height * k)), Image.LANCZOS)


def tile(img, size=(1600, 1100), pad=96, r=20, bg=BG):
    """Фрагмент UI белой карточкой по центру на нейтральном фоне."""
    W, H = size
    cv = Image.new('RGBA', size, bg + (255,))
    c = fit(img, W - pad * 2, H - pad * 2)
    _place(cv, _card(c, r), ((W - c.width) // 2, (H - c.height) // 2), r)
    return cv


def cover(art, shot, size=(2800, 1575)):
    """Обложка: иллюстрация с дроном слева на navy, справа плоский экран продукта, уходящий за край."""
    W, H = size
    cv = Image.new('RGBA', size, NAVY + (255,))
    a = Image.open(art).convert('RGB')
    a = fit(a, h=round(H * 1.22)); ax, ay = round(W * 0.0), -round(H * 0.17)
    cv.paste(a, (ax, ay))
    # плавный переход иллюстрации в фон
    fade = Image.new('L', (W, 1))
    for x in range(W):
        k = (x - W * 0.30) / (W * 0.22)
        fade.putpixel((x, 0), int(255 * max(0, min(1, k))))
    cv.paste(Image.new('RGB', size, NAVY), (0, 0), fade.resize(size))
    s = fit(Image.open(shot).convert('RGB'), w=round(W * 0.62))
    _place(cv, _card(s, 22, border=False), (round(W * 0.43), round(H * 0.15)), 22, blur=40, alpha=120, dy=24)
    return cv


# ---------- сцены с подписями (HTML, без трансформаций) ----------

CSS = '''
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:%dpx;height:%dpx;overflow:hidden}
body{background:#F3F4F6;font-family:Inter,"Helvetica Neue",Arial,sans-serif;color:#111827;-webkit-font-smoothing:antialiased}
.card{background:#fff;border-radius:14px;box-shadow:0 0 0 1px rgba(16,24,40,.06),0 10px 28px -14px rgba(16,24,40,.22);overflow:hidden}
.card img{display:block;width:100%%}
.n{width:26px;height:26px;border-radius:50%%;display:grid;place-items:center;font-size:12px;font-weight:600;background:#fff;color:#111827;box-shadow:0 0 0 1px rgba(16,24,40,.12)}
.n.on{background:#EE6A1F;color:#fff;box-shadow:none}
h4{font-size:18px;font-weight:600;letter-spacing:-.01em}
p{font-size:13.5px;line-height:1.45;color:#4B5563}
'''


def _render(out, body, size):
    from playwright.sync_api import sync_playwright
    w, h = size[0] // 2, size[1] // 2
    doc = f'<html><head><style>{CSS % (w, h)}</style></head><body>{body}</body></html>'
    tmp = os.path.abspath(out + '.html'); open(tmp, 'w').write(doc)
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=os.environ.get('CHROME_PATH') or None)
        pg = b.new_page(viewport={'width': w, 'height': h}, device_scale_factor=2)
        pg.goto('file://' + tmp); pg.wait_for_load_state('networkidle'); pg.wait_for_timeout(200)
        img = Image.open(io.BytesIO(pg.screenshot())).convert('RGB')
        b.close()
    os.remove(tmp)
    save(img, out)


def _prep(img, px_w, tag, tmpdir):
    """Картинка ровно под ширину в пикселях (2x), чтобы браузер показывал её 1:1."""
    p = os.path.abspath(f'{tmpdir}/{tag}.png'); fit(img, w=px_w).save(p); return 'file://' + p


def flow(out, steps, tmpdir, size=(2400, 1000)):
    """Флоу: колонки с крупным фрагментом интерфейса, номером, заголовком и пояснением. steps=[(img, title, sub)]."""
    w, h = size[0] // 2, size[1] // 2
    n = len(steps); gap = 20; pad = 40
    cw = (w - pad * 2 - gap * (n - 1)) / n
    thumb_h = 250
    cols = ''
    for i, (img, t, d) in enumerate(steps):
        src = _prep(img, int((cw - 24) * 2), f'flow{i}', tmpdir)
        cols += f'''<div style="width:{cw}px;display:flex;flex-direction:column;gap:18px">
  <div class="card" style="height:{thumb_h}px;display:flex;align-items:center;justify-content:center;padding:12px;background:#fff"><img src="{src}" style="width:100%;max-height:{thumb_h-24}px;object-fit:contain;border-radius:8px"></div>
  <div style="display:flex;align-items:center;gap:10px"><span class="n {'on' if i == n - 1 else ''}">{i+1}</span><div style="flex:1;height:2px;background:{'transparent' if i == n - 1 else 'repeating-linear-gradient(90deg,#D1D5DB 0 6px,transparent 6px 12px)'}"></div></div>
  <div><h4>{html.escape(t)}</h4><p style="margin-top:6px">{html.escape(d)}</p></div></div>'''
    body = f'<div style="position:absolute;inset:0;display:flex;gap:{gap}px;padding:0 {pad}px;align-items:center">{cols}</div>'
    _render(out, body, size)


def stages(out, items, tmpdir, size=(2400, 1000)):
    """Эволюция: экраны одного размера в ряд, подпись под каждым. items=[(img, title, sub)]."""
    w, h = size[0] // 2, size[1] // 2
    n = len(items); gap = 24; pad = 40
    cw = (w - pad * 2 - gap * (n - 1)) / n
    cols = ''
    for i, (img, t, d) in enumerate(items):
        src = _prep(img, int(cw * 2), f'stage{i}', tmpdir)
        cols += f'''<div style="width:{cw}px;display:flex;flex-direction:column;gap:20px">
  <div class="card"><img src="{src}"></div>
  <div style="display:flex;gap:12px;align-items:flex-start"><span class="n {'on' if i == n - 1 else ''}">{i+1}</span><div><h4>{html.escape(t)}</h4><p style="margin-top:4px">{html.escape(d)}</p></div></div></div>'''
    body = f'<div style="position:absolute;inset:0;display:flex;gap:{gap}px;padding:0 {pad}px;align-items:center">{cols}</div>'
    _render(out, body, size)


DEVICE = '''
.lid{background:#1d1f24;border-radius:20px 20px 6px 6px;padding:12px 12px 16px;box-shadow:0 0 0 1px #34373e inset,0 30px 60px -30px rgba(16,24,40,.45)}
.lid .sc{border-radius:6px;overflow:hidden}.lid img{display:block;width:100%}
.base{height:14px;margin:0 -6%;background:linear-gradient(#e4e6ea,#c3c7ce);border-radius:0 0 16px 16px;position:relative}
.base::before{content:"";position:absolute;left:50%;top:0;width:15%;height:5px;transform:translateX(-50%);background:#b3b7bf;border-radius:0 0 6px 6px}
.mon .lid{border-radius:14px;padding:10px}
.stand{width:20%;height:56px;margin:0 auto;background:linear-gradient(90deg,#cfd2d8,#eceef1,#cfd2d8);clip-path:polygon(16% 0,84% 0,100% 100%,0 100%)}
.foot{width:34%;height:8px;margin:0 auto;background:#c9cdd4;border-radius:5px}
'''


def device(out, img, tmpdir, kind='laptop', size=(2400, 1200), width=0.66):
    w, h = size[0] // 2, size[1] // 2
    lw = round(w * width)
    src = _prep(img, (lw - 24) * 2, f'dev-{kind}', tmpdir)
    inner = f'<div class="lid"><div class="sc"><img src="{src}"></div></div>'
    inner += '<div class="base"></div>' if kind == 'laptop' else '<div class="stand"></div><div class="foot"></div>'
    body = f'<style>{DEVICE}</style><div style="position:absolute;inset:0;display:grid;place-items:center"><div class="{"mon" if kind != "laptop" else ""}" style="width:{lw}px">{inner}</div></div>'
    _render(out, body, size)


def tile_k(img, k=1.1, size=(1600, 1100), r=20, bg=BG, m=64):
    """Как tile, но с единым масштабом для всех плиток: текст во всех фрагментах одного размера."""
    W, H = size
    cv = Image.new('RGBA', size, bg + (255,))
    c = img.resize((round(img.width * k), round(img.height * k)), Image.LANCZOS)
    if c.width > W - m * 2 or c.height > H - m * 2: c = fit(c, W - m * 2, H - m * 2)
    _place(cv, _card(c, r), ((W - c.width) // 2, (H - c.height) // 2), r)
    return cv


def flow_text(out, steps, size=(2400, 760)):
    """Флоу без картинок: крупные шаги-карточки со стрелками и пометкой под каждым. steps=[(title, sub, cue)]."""
    w, h = size[0] // 2, size[1] // 2
    n = len(steps); pad = 40; ar = 34
    cw = (w - pad * 2 - ar * (n - 1)) / n
    arrow = '<svg width="20" height="20" viewBox="0 0 16 16" fill="none" stroke="#9CA3AF" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M3 8h10M9 4l4 4-4 4"/></svg>'
    cells = ''
    for i, (t, d, cue) in enumerate(steps):
        last = i == n - 1
        cells += f'''<div style="width:{cw}px;display:flex;flex-direction:column;gap:14px">
  <div class="card" style="padding:22px 20px 24px;height:222px;{'background:#EE6A1F;box-shadow:none' if last else ''}">
    <span class="n" style="{'background:rgba(255,255,255,.2);color:#fff;box-shadow:none' if last else ''}">{i+1}</span>
    <h4 style="margin-top:18px;font-size:21px;{'color:#fff' if last else ''}">{html.escape(t)}</h4>
    <p style="margin-top:8px;font-size:14px;{'color:rgba(255,255,255,.88)' if last else ''}">{html.escape(d)}</p></div>
  <div style="font-size:13px;color:#4B5563;display:flex;gap:8px;align-items:center;padding-left:4px"><span style="width:6px;height:6px;border-radius:50%;background:{'#EE6A1F' if cue else 'transparent'}"></span>{html.escape(cue)}</div></div>'''
        if not last: cells += f'<div style="width:{ar}px;display:grid;place-items:center;height:222px">{arrow}</div>'
    _render(out, f'<div style="position:absolute;inset:0;display:flex;align-items:center;padding:0 {pad}px"><div style="display:flex;align-items:flex-start;width:100%">{cells}</div></div>', size)


def view(path, x, y, w, size=(1600, 1100), s=3):
    """Окно в реальный экран: кадр 16:11 с ключевым элементом целиком, родные тени макета, без наложенных карточек.
    x, y, w — левый верхний угол и ширина кадра в CSS-пикселях фрейма 1440×900; высота по пропорции."""
    h = w * size[1] / size[0]
    im = Image.open(path).convert('RGB')
    x = max(0, min(x, 1440 - w)); y = max(0, min(y, 900 - h))
    return im.crop((round(x * s), round(y * s), round((x + w) * s), round((y + h) * s))).resize(size, Image.LANCZOS)
