# Визуалы кейса StuLo из скриншотов cases/_src/stulo (device scale 2, вьюпорт 1440×900).
# el_*.png — скриншоты отдельных карточек интерфейса, d_*.png — экраны целиком (демо-переключатель скрыт).
# Запуск из корня проекта: python3 cases/_tools/build_stulo.py
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from PIL import Image
from compose import tile, cover, framed, save
from flow import render_flow

SRC, OUT = 'cases/_src/stulo', 'img/cases/stulo'
os.makedirs(OUT, exist_ok=True)
S = 2  # device scale


def im(name): return Image.open(f'{SRC}/{name}.png').convert('RGB')
def css(img, x0, y0, x1, y1): return img.crop((x0 * S, y0 * S, x1 * S, y1 * S))


dash = im('d_dashboard')

# обложка: дашборд + чат с AI-коучем
save(cover(dash, im('d_coach_answer')), f'{OUT}/cover-browser.jpg')  # обложка — cover.jpg, сгенерирована (cases/_src/stulo/ai/cover-papers.webp)

# проблемы
save(tile(css(im('d_loans'), 290, 330, 1070, 760)), f'{OUT}/problem-1-loans.jpg')       # несколько займов у разных сервисеров
save(tile(im('el_plans'), valign='top'), f'{OUT}/problem-2-plans.jpg')                   # множество планов, SAVE закрывается
save(tile(im('el_rescue')), f'{OUT}/problem-3-rescue.jpg')                               # просрочка и дефолт
save(tile(im('el_pslf_loans')), f'{OUT}/problem-4-eligibility.jpg')                      # не все займы подходят под PSLF

# решения
save(tile(im('el_checklist')), f'{OUT}/solution-1-checklist.jpg')                        # следующий шаг и чек-лист
save(tile(im('el_onboarding')), f'{OUT}/solution-2-sync.jpg')                            # загрузка файла StudentAid.gov
save(tile(im('el_decoder')), f'{OUT}/solution-3-decoder.jpg')                            # письмо сервисера простым языком
save(tile(im('el_coach'), valign='top'), f'{OUT}/solution-4-coach.jpg')                  # AI-коуч + живой коуч

# флоу
render_flow(f'{OUT}/flow.jpg', [
    ('Sign up', 'Free loan analysis'),
    ('Sync loans', 'StudentAid.gov file · no FSA ID'),
    ('Compare plans', 'RAP · IBR · PSLF estimates'),
    ('Prepare forms', 'Prefilled .gov forms'),
    ('Coach review', 'Sign, mail, recertify'),
], branches=[('Letter decoder · loan rescue', 2), ('AI coach', 3), ('PSLF tracker', 5)])

# экраны
save(framed(dash, (2400, 1200)), f'{OUT}/screen-dashboard.jpg')
save(framed(im('d_pslf'), (1600, 1000)), f'{OUT}/screen-pslf.jpg')
save(framed(im('d_signin'), (1600, 1000)), f'{OUT}/screen-signin.jpg')
print('ok', sorted(os.listdir(OUT)))
