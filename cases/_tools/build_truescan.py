# Визуалы кейса TrueScan из экспортов Figma (cases/_src/truescan, PNG 2x, фреймы 1440×900).
# Файл Figma: TrueScan — Entity Profiles Redesign (страницы Leads, Opportunities, Foundations).
# Экспорт фреймов: Figma MCP download_assets(nodeId, scale 2).
# Сцены (изометрия, крупный план, девайсы) — cases/_tools/scene.py.
# Запуск из корня: CHROME_PATH=/opt/pw-browsers/chromium python3 cases/_tools/build_truescan.py
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from compose import tile, save
from PIL import Image
import scene as sc

SRC, OUT = 'cases/_src/truescan', 'img/cases/truescan'
TMP = f'{SRC}/_crops'
os.makedirs(OUT, exist_ok=True); os.makedirs(TMP, exist_ok=True)


def p(name): return f'{SRC}/{name}.png'
def crop(name, box, tag): return sc.crop_file(p(name), box, f'{TMP}/{tag}.png')


# фрагменты (координаты в CSS-пикселях фрейма 1440×900; модалки и поповеры — по координатам из Figma)
c = {
    'list': crop('lead_table', (284, 150, 900, 640), 'list'),
    'filters': crop('kanban_filters', (284, 120, 860, 560), 'filters'),
    'menu': crop('row_menu', (880, 300, 1440, 860), 'menu'),
    'wiz1': crop('wiz1', (400, 204, 1040, 697), 'wiz1'),
    'convert': crop('convert', (460, 213, 980, 687), 'convert'),
    'converted': crop('opp_profile', (284, 16, 960, 520), 'converted'),
    'assign': crop('assign', (980, 250, 1400, 600), 'assign'),
    'wiz2': crop('wiz2', (400, 157, 1040, 743), 'wiz2'),
    'export': crop('export', (480, 215, 960, 685), 'export'),
    'toast': crop('toast_undo', (696, 824, 1008, 876), 'toast'),
    'empty': crop('noresults', (560, 360, 1160, 620), 'empty'),
}

# обложка: изометрический стек — список, Kanban, профиль лида, сделка после конвертации
sc.hero_drone(f'{OUT}/cover.jpg', p('drone_raw1'), [p('lead_table'), p('profile')])
sc.iso_stack(f'{OUT}/overview.jpg', [p('lead_table'), p('lead_kanban'), p('profile'), p('opp_profile')])

# задачи: экран в перспективе + крупный план
sc.focus(f'{OUT}/problem-1-list.jpg', p('lead_table'), c['list'], tilt=-24)
sc.focus(f'{OUT}/problem-2-filters.jpg', p('kanban_filters'), c['filters'], tilt=22)
sc.focus(f'{OUT}/problem-3-actions.jpg', p('row_menu'), c['menu'], tilt=-20)
sc.focus(f'{OUT}/problem-4-input.jpg', p('wiz1'), c['wiz1'], tilt=24)

# решения
sc.focus(f'{OUT}/solution-1-convert.jpg', p('convert'), c['convert'], tilt=-22)
sc.focus(f'{OUT}/solution-2-converted.jpg', p('opp_profile'), c['converted'], tilt=22)
sc.focus(f'{OUT}/solution-3-assign.jpg', p('assign'), c['assign'], tilt=-24, cw=0.78)
sc.focus(f'{OUT}/solution-4-wizard.jpg', p('wiz2'), c['wiz2'], tilt=22)

# флоу из реальных экранов
sc.journey(f'{OUT}/flow.jpg', [
    (p('wiz1'), 'New lead', 'Web form or a 3-step wizard with a duplicate check'),
    (p('lead_kanban'), 'Triage', 'Table or Kanban, tabs, filters, AI score'),
    (p('assign'), 'Assign & qualify', 'Owner in one click, status from the row'),
    (p('convert'), 'Convert', 'Preview of Account, Contact and Opportunity'),
    (p('opp_profile'), 'Opportunity', 'Lands on the deal with “Converted from lead”'),
])

# дизайн-система: анатомия уровней и состояния контролов
sc.exploded(f'{OUT}/anatomy.jpg', p('lead_table'), True, c['convert'],
            labels=[('Page · Shadow/md', .12, .8), ('Scrim · navy 20%', .1, .22), ('Modal · Shadow/lg', .66, .12)])
save(tile(Image.open(p('states')).crop((0, 280, 2880, 1940)), size=(2400, 1200), pad=80, r=28), f'{OUT}/states.jpg')

# экраны: девайсы, крупный план, пара «загрузка → данные»
sc.laptop(f'{OUT}/screen-profile.jpg', p('profile'))
sc.monitor(f'{OUT}/screen-kanban.jpg', p('lead_kanban'))
sc.focus(f'{OUT}/screen-export.jpg', p('export'), c['export'], size=(1600, 1000), cw=0.4, tilt=-20)
sc.pair(f'{OUT}/screen-skeleton.jpg', p('skeleton'), p('lead_table'), labels=('Skeleton after 300 ms', 'Data in place'))
sc.focus(f'{OUT}/screen-noresults.jpg', p('noresults'), c['empty'], size=(1600, 1000), cw=0.5, tilt=20)
# процесс: лоу-фай вайрфреймы (реконструкция ранней стадии) → UI-kit → финальный интерфейс
for n, f in (('wf_list', sc.wf_list), ('wf_profile', sc.wf_profile), ('wf_convert', sc.wf_convert)): f(f'{SRC}/{n}.png')
uikit = f'{TMP}/uikit.png'

kit = Image.new('RGB', (2880, 1800), (246, 247, 249))
fil = Image.open(p('filters')).convert('RGB'); k = 2880 / fil.width; fil = fil.resize((2880, round(fil.height * k)))
st = Image.open(p('states')).convert('RGB').crop((0, 280, 2880, 1940)); kit.paste(fil, (0, 0)); kit.paste(st.crop((0, 0, 2880, 1800 - fil.height)), (0, fil.height))
kit.save(uikit)
sc.evolution(f'{OUT}/evolution.jpg', [(p('wf_list'), 'Wireframe', 'structure & rules'), (uikit, 'UI kit', 'tokens, components, states'), (p('lead_table'), 'Interface', 'final screen')])
sc.focus(f'{OUT}/wireframe-list.jpg', p('lead_table'), p('wf_list'), size=(1600, 1000), cw=0.74, tilt=-18)
sc.focus(f'{OUT}/wireframe-profile.jpg', p('profile'), p('wf_profile'), size=(1600, 1000), cw=0.74, tilt=18)
sc.focus(f'{OUT}/wireframe-convert.jpg', p('convert'), p('wf_convert'), size=(1600, 1000), cw=0.74, tilt=-18)
print('ok', sorted(os.listdir(OUT)))
