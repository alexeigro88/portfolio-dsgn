import os, sys
os.chdir('/home/user/alexeigro88/portfolio-dsgn')
sys.path.insert(0, 'cases/_tools')
from PIL import Image
import flat as F
S, O = 'cases/_src/truescan', 'img/cases/truescan'
BG = (241, 243, 246)


def tile(img, size, pad, r=14):
    """Фрагмент целиком по центру, без серой обводки, мягкая тень."""
    W, H = size
    cv = Image.new('RGBA', size, BG + (255,))
    c = F.fit(img, W - pad * 2, H - pad * 2)
    F._place(cv, F._card(c, r, border=False), ((W - c.width) // 2, (H - c.height) // 2), r, blur=24, alpha=26, dy=10)
    return cv


def full(p, s):
    return Image.open(p).convert('RGB').crop((0, 0, 1440 * s, 900 * s))


# от вайрфрейма к интерфейсу: экраны и секции целиком, с воздухом
for name, im in [('evo-1-wireframe', full(f'{S}/wf_list.png', 2)),
                 ('evo-2-uikit', F.crop(f'{S}/states.png', (32, 128, 1408, 560))),
                 ('evo-3-interface', full(f'{S}/x3/lead_table.png', 3))]:
    F.save(tile(im, (1848, 1200), 110), f'{O}/{name}.jpg')

# состояния контролов: четыре секции целиком, с отступом сверху и снизу
F.save(tile(F.crop(f'{S}/states.png', (32, 128, 1408, 980)), (2400, 1500), 120, r=18), f'{O}/states.jpg')
print('ok')

# модалка экспорта: срез строго внутри окна (без затемнения по углам), скругление как у модалки
m = F.crop(f'{S}/export.png', (482, 217, 958, 683))
k = min((1600 - 300) / m.width, (1000 - 200) / m.height)
F.save(tile(m, (1600, 1000), 100, r=round(16 * 2 * k)), f'{O}/screen-export.jpg')
print('export ok')
