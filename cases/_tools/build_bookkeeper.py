"""BookKeeper AI: обложка, экраны и фото. Запуск из корня репозитория."""
import sys
sys.path.insert(0, 'cases/_tools')
from PIL import Image
import flat as F

S, O = 'cases/_src/bookkeeper', 'img/cases/bookkeeper-ai'
BG = (241, 243, 247)


def scr(n):
    return Image.open(f'{S}/{n}.png').convert('RGB').crop((0, 0, 2880, 1800))


def tile(img, size, pad, r):
    W, H = size
    cv = Image.new('RGBA', size, BG + (255,))
    c = F.fit(img, W - pad * 2, H - pad * 2)
    F._place(cv, F._card(c, r, border=False), ((W - c.width) // 2, (H - c.height) // 2), r, blur=26, alpha=30, dy=12)
    return cv


# обложка: экран ответа с источниками + обзор знаний для SME поверх
W, H = 2800, 1575
cv = Image.new('RGBA', (W, H), BG + (255,))
a = F.fit(scr('07-answer-full'), w=1880)
F._place(cv, F._card(a, 22, border=False), (150, 150), 22, blur=34, alpha=34, dy=16)
b = F.fit(scr('10-sme'), w=1300)
F._place(cv, F._card(b, 18, border=False), (W - 150 - b.width, H - 130 - b.height), 18, blur=40, alpha=60, dy=20)
F.save(cv, f'{O}/cover.jpg')

F.save(tile(scr('07-answer-full'), (2400, 1200), 90, 22), f'{O}/screen-answer.jpg')
F.save(tile(scr('11-qc-AIInsights'), (2400, 1200), 90, 22), f'{O}/screen-insights.jpg')
for n, out in [('10-sme', 'overview'), ('05-library', 'library'), ('04-gap', 'gap'), ('06-upload', 'upload')]:
    F.save(tile(scr(n), (1600, 1000), 80, 16), f'{O}/screen-{out}.jpg')

for k in ['p1', 'p2', 'p3', 'p4', 's1', 's2', 's3', 's4']:
    Image.open(f'{S}/ai/{k}.png').convert('RGB').save(f'{O}/photo-{k}.jpg', quality=90, subsampling=0, optimize=True)
print('ok')
