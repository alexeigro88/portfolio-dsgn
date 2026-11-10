# Визуалы кейса Tournament Guru из скриншотов cases/_src/tournament-guru (снято с device scale 2).
# Запуск из корня проекта: python3 cases/_tools/build_tournament_guru.py
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from PIL import Image
from compose import tile, photo_tile, cover, framed, save
from flow import render_flow

SRC, OUT = 'cases/_src/tournament-guru', 'img/cases/tournament-guru'
os.makedirs(OUT, exist_ok=True)
S = 2  # device scale


def im(name): return Image.open(f'{SRC}/{name}.png').convert('RGB')
def css(img, x0, y0, x1, y1): return img.crop((x0 * S, y0 * S, x1 * S, y1 * S))


event, event_full = im('d_event'), im('d_event_full')
cat, cat_full = im('d_catalog_nomap'), im('d_catalog_nomap_full')
login = im('d_login')

# обложка: страница турнира + каталог
save(cover(event, cat), f'{OUT}/cover.jpg')

# проблемы: живые фото с турниров из галереи прототипа
for i, box in enumerate([(103, 147, 712, 594), (719, 147, 1022, 369), (1031, 147, 1334, 369)], 1):
    save(photo_tile(css(event, *box)), f'{OUT}/problem-{i}.jpg')
save(photo_tile(css(im('d_event_t1'), 103, 200, 712, 594)), f'{OUT}/problem-4.jpg')   # фото игрока с другого турнира (t1), без метки Featured

# решения: фрагменты интерфейса
save(tile(css(event_full, 100, 2415, 940, 2910)), f'{OUT}/solution-1-reviews.jpg')     # рейтинги по категориям + отзывы
save(tile(css(cat_full, 20, 48, 760, 780), valign='top'), f'{OUT}/solution-2-search.jpg')           # поиск, фильтры, рекомендации
save(tile(css(event_full, 100, 1630, 940, 2095)), f'{OUT}/solution-3-venue.jpg')      # площадка и логистика
save(tile(css(event_full, 960, 780, 1340, 1215)), f'{OUT}/solution-4-booking.jpg')    # регистрация и прозрачная цена

# флоу
render_flow(f'{OUT}/flow.jpg', [
    ('Sign in', 'Coach, parent or organizer'),
    ('Find events', 'Filters · map · recommended'),
    ('Compare', 'Verified reviews · ratings by category'),
    ('Check the details', 'Schedule · venue · what’s included'),
    ('Register team', 'Transparent fees · host confirms'),
], branches=[('Host profile', 3), ('Similar tournaments', 3)])

# экраны
save(framed(cat, (2400, 1200)), f'{OUT}/screen-catalog.jpg')
save(framed(login, (1600, 1000)), f'{OUT}/screen-login.jpg')
save(framed(event, (1600, 1000)), f'{OUT}/screen-event.jpg')
print('ok', sorted(os.listdir(OUT)))
