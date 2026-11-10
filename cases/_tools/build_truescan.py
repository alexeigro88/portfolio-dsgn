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
T = {
    'problem-1-list':      c('lead_table', 284, 150, 920, 560),      # вкладки статусов и строки лидов
    'problem-2-filters':   c('kanban_filters', 284, 110, 880, 520),  # фильтры, чипы и выпадающий список Owner
    'problem-3-actions':   c('row_menu', 860, 330, 1440, 760),       # меню строки и подменю статуса
    'problem-4-input':     c('wiz1', 400, 204, 1040, 600),           # мастер: дубль email
    'solution-1-convert':  c('convert', 460, 213, 980, 687),         # конвертация с превью записей
    'solution-2-converted': c('opp_profile', 284, 16, 1000, 420),    # баннер «Converted from lead»
    'solution-3-assign':   c('assign', 900, 250, 1424, 640),         # назначение владельца в один клик
    'solution-4-wizard':   c('wiz2', 400, 300, 1040, 743),           # мастер: автокомплит адреса
}
for k, im in T.items():
    F.save(F.tile_k(im), f'{OUT}/{k}.jpg')

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
for n, f in (('wf_list', S.wf_list), ('wf_profile', S.wf_profile), ('wf_convert', S.wf_convert)):
    f(p(n))
kit = Image.new('RGB', (2880, 1800), (246, 247, 249))
fil = full('filters'); fil = fil.resize((2880, round(fil.height * 2880 / fil.width)), Image.LANCZOS)
kit.paste(fil, (0, 0)); kit.paste(full('states').crop((0, 280, 2880, 280 + 1800 - fil.height)), (0, fil.height))
kit.save(f'{TMP}/uikit.png')
F.stages(f'{OUT}/evolution.jpg', [
    (full('wf_list'), 'Wireframe', 'Structure, rules and open questions'),
    (kit, 'UI kit', 'Tokens, components and their states'),
    (full('lead_table'), 'Interface', 'The final Leads screen'),
], TMP, size=(2400, 900))
for n in ('wf_list', 'wf_profile', 'wf_convert'):
    F.save(F.tile(full(n), size=(1600, 1000), pad=56, r=14), f'{OUT}/wireframe-{n[3:]}.jpg')

# ---------- дизайн-система: состояния контролов ----------
F.save(F.tile(full('states').crop((0, 280, 2880, 1940)), size=(2400, 1200), pad=80, r=20), f'{OUT}/states.jpg')

# ---------- экраны ----------
F.device(f'{OUT}/screen-profile.jpg', full('profile'), TMP, 'laptop', size=(2400, 1200), width=0.7)
F.device(f'{OUT}/screen-kanban.jpg', full('lead_kanban'), TMP, 'monitor', size=(1600, 1000), width=0.8)
F.save(F.tile(c('export', 480, 215, 960, 685), size=(1600, 1000), pad=72), f'{OUT}/screen-export.jpg')
F.save(F.tile(full('skeleton'), size=(1600, 1000), pad=72, r=14), f'{OUT}/screen-skeleton.jpg')
F.save(F.tile(full('noresults'), size=(1600, 1000), pad=72, r=14), f'{OUT}/screen-noresults.jpg')
print('ok', sorted(os.listdir(OUT)))
