# Визуалы для кейсов из скриншотов прототипа: окно браузера, плитка с фрагментом UI, обложка из двух окон.
# Используется скриптами cases/_tools/build_<проект>.py. Скриншоты снимаются с device scale 2.
from PIL import Image, ImageDraw, ImageFilter

BG_TOP, BG_BOTTOM = (243, 244, 247), (229, 232, 239)   # светлый фон в стиле сайта (#f5f5f7)


def gradient(w, h, top=BG_TOP, bottom=BG_BOTTOM):
    g = Image.new('RGB', (1, h))
    for y in range(h):
        k = y / max(1, h - 1)
        g.putpixel((0, y), tuple(round(top[i] + (bottom[i] - top[i]) * k) for i in range(3)))
    return g.resize((w, h))


def rounded_mask(size, r):
    m = Image.new('L', size, 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, size[0] - 1, size[1] - 1), r, fill=255)
    return m


def shadow(size, r, blur, alpha=70, spread=0):
    """Мягкая тень под карточкой: возвращает RGBA-слой с полями под размытие."""
    pad = blur * 3
    s = Image.new('RGBA', (size[0] + pad * 2, size[1] + pad * 2), (0, 0, 0, 0))
    ImageDraw.Draw(s).rounded_rectangle((pad - spread, pad - spread, pad + size[0] + spread, pad + size[1] + spread), r, fill=(20, 22, 50, alpha))
    return s.filter(ImageFilter.GaussianBlur(blur)), pad


def browser(shot, width, bar=None, r=None):
    """Окно браузера с верхней панелью и тремя точками; shot — PIL Image страницы."""
    bar = bar or round(width * 0.028)
    r = r or round(width * 0.014)
    sh = shot.resize((width, round(shot.height * width / shot.width)), Image.LANCZOS)
    win = Image.new('RGB', (width, sh.height + bar), (255, 255, 255))
    d = ImageDraw.Draw(win)
    d.rectangle((0, 0, width, bar), fill=(246, 246, 248))
    d.line((0, bar - 1, width, bar - 1), fill=(228, 229, 234), width=max(1, width // 1400))
    rr = max(4, bar // 6)
    for i, c in enumerate([(255, 95, 87), (254, 188, 46), (40, 200, 64)]):
        cx = bar * 0.55 + i * bar * 0.42
        d.ellipse((cx - rr, bar / 2 - rr, cx + rr, bar / 2 + rr), fill=c)
    # адресная строка
    aw = width * 0.32
    d.rounded_rectangle((width / 2 - aw / 2, bar * 0.24, width / 2 + aw / 2, bar * 0.76), bar * 0.26, fill=(255, 255, 255), outline=(228, 229, 234))
    win.paste(sh, (0, bar))
    out = Image.new('RGBA', win.size, (0, 0, 0, 0))
    out.paste(win, (0, 0), rounded_mask(win.size, r))
    return out


def place(canvas, layer, xy, r, blur=None, alpha=60):
    """Кладёт RGBA-слой на холст с мягкой тенью."""
    blur = blur or max(12, layer.width // 40)
    s, pad = shadow(layer.size, r, blur, alpha)
    canvas.alpha_composite(s, (xy[0] - pad, xy[1] - pad + blur // 2))
    canvas.alpha_composite(layer, xy)


def tile(crop, size=(900, 1020), pad=56, r=22, valign='center'):
    """Плитка 3:3.4: фрагмент интерфейса белой карточкой на светлом фоне."""
    W, H = size
    cv = gradient(W, H).convert('RGBA')
    maxw, maxh = W - pad * 2, H - pad * 2
    k = min(maxw / crop.width, maxh / crop.height)
    c = crop.resize((round(crop.width * k), round(crop.height * k)), Image.LANCZOS)
    card = Image.new('RGBA', c.size, (0, 0, 0, 0)); card.paste(c, (0, 0), rounded_mask(c.size, r))
    x = (W - c.width) // 2
    y = (H - c.height) // 2 if valign == 'center' else pad
    place(cv, card, (x, y), r, blur=18, alpha=45)
    return cv.convert('RGB')


def photo_tile(img, size=(900, 1020)):
    """Плитка-фото: кадрирование по центру под нужную пропорцию."""
    W, H = size
    k = max(W / img.width, H / img.height)
    im = img.resize((round(img.width * k), round(img.height * k)), Image.LANCZOS)
    x, y = (im.width - W) // 2, (im.height - H) // 2
    return im.crop((x, y, x + W, y + H)).convert('RGB')


def cover(main, second, size=(2800, 1575)):
    """Обложка 16:9: главное окно слева, второе окно справа внизу внахлёст."""
    W, H = size
    cv = gradient(W, H).convert('RGBA')
    a = browser(main, round(W * 0.70))
    b = browser(second, round(W * 0.50))
    ax, ay = round(W * 0.06), round(H * 0.10)
    bx, by = W - b.width - round(W * 0.05), round(H * 0.36)
    place(cv, a, (ax, ay), round(a.width * 0.014), alpha=55)
    place(cv, b, (bx, by), round(b.width * 0.014), alpha=75)
    return cv.convert('RGB')


def framed(shot, size, margin=0.07):
    """Скриншот в окне браузера по центру холста нужной пропорции."""
    W, H = size
    cv = gradient(W, H).convert('RGBA')
    w = round(W * (1 - margin * 2))
    win = browser(shot, w)
    if win.height > H * (1 - margin * 2):
        w = round(w * H * (1 - margin * 2) / win.height); win = browser(shot, w)
    place(cv, win, ((W - win.width) // 2, (H - win.height) // 2), round(win.width * 0.014), alpha=55)
    return cv.convert('RGB')


def save(img, path, q=86):
    img.convert('RGB').save(path, quality=q, optimize=True, progressive=True)
