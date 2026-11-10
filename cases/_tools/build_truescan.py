# Визуалы кейса TrueScan из экспортов Figma (cases/_src/truescan, PNG 2x, фреймы 1440×900).
# Файл Figma: TrueScan — Entity Profiles Redesign (страницы Leads, Opportunities, Foundations, Time tracking).
# Экспорт фреймов: Figma MCP download_assets(nodeId, scale 2). Иллюстрация с дроном — фрейм «E0 · Sign in».
# Стиль: плоско, крупно, без перспективы и свечений (cases/_tools/flat.py). Вайрфреймы — cases/_tools/scene.py.
# Запуск из корня: CHROME_PATH=/opt/pw-browsers/chromium python3 cases/_tools/build_truescan.py
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from PIL import Image
import flat as F

SRC, OUT = 'cases/_src/truescan', 'img/cases/truescan'
TMP = f'{SRC}/_crops'
os.makedirs(OUT, exist_ok=True); os.makedirs(TMP, exist_ok=True)


def p(name): return f'{SRC}/{name}.png'
def c(name, *box): return F.crop(p(name), box)        # координаты в CSS-пикселях фрейма 1440×900
def full(name): return Image.open(p(name)).convert('RGB')


# ---------- обложка ----------
F.save(F.cover(p('drone_raw1'), p('lead_table')), f'{OUT}/cover.jpg')

# ---------- задачи и решения: крупные фрагменты, 16:11 ----------
# кадр = окно в экран (экспорт 3x в cases/_src/truescan/x3): элемент целиком + контекст, без наложенных теней
X3 = f'{SRC}/x3'
V = {
    'problem-1-list':       ('lead_table', 284, 16, 660),      # заголовок, фильтры, вкладки статусов, строки
    'problem-2-filters':    ('kanban_filters', 284, 16, 660),  # фильтры с счётчиками, чипы, список Owner
    'problem-3-actions':    ('row_menu', 764, 345, 660),       # меню строки и подменю статуса
    'problem-4-input':      ('wiz1', 334, 186, 771),           # мастер целиком: дубль email
    'solution-1-convert':   ('convert', 342, 190, 756),        # модалка конвертации целиком
    'solution-2-converted': ('opp_profile', 284, 16, 700),     # баннер «Converted from lead», шапка сделки
    'solution-3-assign':    ('assign', 784, 218, 640),         # колонка Owner и поповер назначения
    'solution-4-wizard':    ('wiz2', 269, 140, 902),           # мастер целиком: автокомплит адреса
}
for k, (n, x, y, w) in V.items():
    F.save(F.view(f'{X3}/{n}.png', x, y, w), f'{OUT}/{k}.jpg')

# ---------- флоу: фрагменты ключевых шагов ----------
F.flow_text(f'{OUT}/flow.jpg', [
    ('New lead', 'Web form, or a 3-step wizard for manual entry', 'Duplicate email check'),
    ('Triage', 'Table or Kanban, status tabs, filters and AI score', 'Export the current view'),
    ('Assign & qualify', 'Owner in one click, status right from the row', 'Archive with 8 s Undo'),
    ('Convert', 'Preview of the Account, Contact and Opportunity to be created', 'Qualified leads only'),
    ('Opportunity', 'Lands on the new deal with a “Converted from lead” banner', ''),
])

# ---------- от вайрфрейма к интерфейсу ----------
import scene as S
S.wf_list(p('wf_list'))
# один и тот же фрагмент (шапка + таблица) на трёх стадиях — крупно, чтобы было видно разницу
EV = (262, 8, 986, 478)                                    # CSS-пиксели, пропорция ≈ 1.54
for name, im in (('evo-1-wireframe', c('wf_list', *EV)),
                 ('evo-2-uikit', F.crop(p('states'), (40, 128, 764, 598))),
                 ('evo-3-interface', F.crop(f'{SRC}/x3/lead_table.png', EV, s=3))):
    F.save(F.fit(im, w=1448), f'{OUT}/{name}.jpg')

# ---------- дизайн-система: состояния контролов ----------
F.save(F.tile(full('states').crop((0, 280, 2880, 1940)), size=(2400, 1200), pad=80, r=20), f'{OUT}/states.jpg')

# ---------- экраны ----------
F.device(f'{OUT}/screen-profile.jpg', full('profile'), TMP, 'laptop', size=(2400, 1200), width=0.7)
F.device(f'{OUT}/screen-kanban.jpg', full('lead_kanban'), TMP, 'monitor', size=(1600, 1000), width=0.8)
F.save(F.tile(c('export', 480, 215, 960, 685), size=(1600, 1000), pad=72), f'{OUT}/screen-export.jpg')
F.save(F.tile(full('skeleton'), size=(1600, 1000), pad=72, r=14), f'{OUT}/screen-skeleton.jpg')
F.save(F.tile(full('noresults'), size=(1600, 1000), pad=72, r=14), f'{OUT}/screen-noresults.jpg')
print('ok', sorted(os.listdir(OUT)))
