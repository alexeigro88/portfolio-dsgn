# Плитки «экран целиком + увеличенный фрагмент»: весь экран как контекст (приглушён),
# рамка на нужной области и тот же фрагмент крупно поверх. Ничего не обрезано по краям карточки.
# Запуск из корня: python3 cases/_tools/focus_tiles.py
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from PIL import Image, ImageDraw, ImageFilter
import flat as F

S, O = 'cases/_src/truescan', 'img/cases/truescan'
W, H = 1600, 1100
ACC = (238, 106, 31)


def rr_mask(size, r):
    m = Image.new('L', size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, size[0] - 1, size[1] - 1), r, fill=255); return m


def tile(src, s, box, out, anchor='br'):
    full = Image.open(src).convert('RGB')
    scr = full.crop((0, 0, 1440 * s, 900 * s))
    cv = Image.new('RGB', (W, H), (243, 244, 246))
    # контекст: весь экран по ширине карточки, приглушён
    k = (W - 120) / scr.width
    bg = scr.resize((W - 120, round(scr.height * k)), Image.LANCZOS)
    veil = Image.new('RGB', bg.size, (246, 247, 249))
    bg = Image.blend(bg, veil, 0.55)
    bx, by = 60, 60
    cv.paste(bg, (bx, by), rr_mask(bg.size, 18))
    # рамка на области фрагмента
    x0, y0, x1, y1 = box
    d = ImageDraw.Draw(cv)
    d.rounded_rectangle((bx + x0 * k * s, by + y0 * k * s, bx + x1 * k * s, by + y1 * k * s), 10, outline=ACC, width=4)
    # фрагмент крупно
    crop = full.crop((x0 * s, y0 * s, x1 * s, y1 * s))
    maxw, maxh = W * 0.74, H * 0.72
    z = min(maxw / crop.width, maxh / crop.height)
    crop = crop.resize((round(crop.width * z), round(crop.height * z)), Image.LANCZOS)
    pad = 6
    card = Image.new('RGBA', (crop.width + pad * 2, crop.height + pad * 2), (0, 0, 0, 0))
    card.paste(Image.new('RGB', card.size, (255, 255, 255)), (0, 0), rr_mask(card.size, 22))
    card.paste(crop, (pad, pad), rr_mask(crop.size, 17))
    cx = W - card.width - 40 if 'r' in anchor else 40
    cy = H - card.height - 40 if 'b' in anchor else 40
    sh = Image.new('RGBA', (card.width + 160, card.height + 160), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle((80, 80, 80 + card.width, 80 + card.height), 22, fill=(16, 24, 40, 60))
    sh = sh.filter(ImageFilter.GaussianBlur(26))
    base = cv.convert('RGBA'); base.alpha_composite(sh, (cx - 80, cy - 80 + 14)); base.alpha_composite(card, (cx, cy))
    F.save(base, f'{O}/{out}.jpg')


X3 = f'{S}/x3'
T = [
    ('problem-1-list', f'{X3}/lead_table.png', 3, (284, 90, 1000, 380), 'br'),
    ('problem-2-proposal', f'{S}/proposal_builder.png', 2, (100, 70, 760, 500), 'br'),
    ('problem-3-project', f'{S}/project_overview.png', 2, (284, 16, 1000, 400), 'br'),
    ('problem-4-time', f'{S}/timesheet.png', 2, (284, 60, 1000, 460), 'br'),
    ('solution-1-convert', f'{X3}/convert.png', 3, (460, 213, 980, 687), 'br'),
    ('solution-2-converted', f'{X3}/opp_profile.png', 3, (284, 16, 1000, 400), 'br'),
    ('solution-3-assign', f'{X3}/assign.png', 3, (1000, 290, 1410, 560), 'bl'),
    ('solution-4-wizard', f'{X3}/wiz2.png', 3, (400, 157, 1040, 743), 'br'),
]
for out, src, s, box, a in T:
    tile(src, s, box, out, a)
print('ok')
