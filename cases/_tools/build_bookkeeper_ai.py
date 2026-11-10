# Визуалы кейса BookKeeper AI из скриншотов cases/_src/bookkeeper-ai (снято с device scale 2, вьюпорт 1440×900).
# Запуск из корня проекта: python3 cases/_tools/build_bookkeeper_ai.py
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from PIL import Image
from compose import tile, cover, framed, save
from flow import render_flow

SRC, OUT = 'cases/_src/bookkeeper-ai', 'img/cases/bookkeeper-ai'
os.makedirs(OUT, exist_ok=True)
S = 2  # device scale


def im(name): return Image.open(f'{SRC}/{name}.png').convert('RGB')
def css(img, x0, y0, x1, y1): return img.crop((x0 * S, y0 * S, x1 * S, y1 * S))


answer, review_sme, review_qc = im('d_answer_ack'), im('d_review_sme'), im('d_review_qc')

# обложка: ответ с источниками + обзор знаний для SME
save(cover(answer, review_sme), f'{OUT}/cover.jpg')

# проблемы: состояние базы знаний глазами бухгалтера и эксперта
save(tile(css(im('d_library'), 305, 255, 795, 880)), f'{OUT}/problem-1-outdated.jpg')        # SOP с истёкшей проверкой
save(tile(css(im('d_client_search'), 440, 455, 1275, 735)), f'{OUT}/problem-2-clients.jpg')  # много клиентов — свои регламенты
save(tile(css(im('d_unanswered'), 440, 100, 1275, 400)), f'{OUT}/problem-3-gaps.jpg')        # нет опубликованного ответа
save(tile(css(im('d_sme_queue'), 300, 215, 862, 630)), f'{OUT}/problem-4-queue.jpg')        # очередь на проверку экспертом

# решения: фрагменты интерфейса
save(tile(css(answer, 440, 100, 1275, 525)), f'{OUT}/solution-1-sources.jpg')               # ответ со ссылками и статусом источника
save(tile(css(im('d_clarify'), 440, 100, 1275, 395)), f'{OUT}/solution-2-scope.jpg')         # общий или клиентский регламент
save(tile(css(im('d_answer_general'), 440, 100, 1275, 380)), f'{OUT}/solution-3-ack.jpg')    # подтверждение перед ответом
save(tile(css(review_qc, 300, 90, 1420, 690)), f'{OUT}/solution-4-review.jpg')  # приоритеты SME / QC

# флоу
render_flow(f'{OUT}/flow.jpg', [
    ('Ask', 'Bookkeeper asks in plain language'),
    ('Clarify scope', 'General or client-specific'),
    ('Retrieve', 'Published sources only'),
    ('Answer', 'Citations · source status'),
    ('Feedback', 'Helpful · report an issue'),
], branches=[('No source → SME queue', 3), ('Needs revalidation → acknowledge', 4), ('SME validates · QC certifies', 5)])

# экраны
save(framed(im('d_home'), (2400, 1200)), f'{OUT}/screen-home.jpg')
save(framed(im('d_sme_unanswered'), (1600, 1000)), f'{OUT}/screen-gaps.jpg')
save(framed(im('d_upload'), (1600, 1000)), f'{OUT}/screen-upload.jpg')
print('ok', sorted(os.listdir(OUT)))
