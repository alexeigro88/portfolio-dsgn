# Визуалы кейса TrueScan из экспортов Figma (cases/_src/truescan, PNG 2x, фреймы 1440×900).
# Файл Figma: TrueScan — Entity Profiles Redesign (страницы Leads, Opportunities, Foundations).
# Экспорт фреймов: Figma MCP download_assets(nodeId, scale 2). Запуск из корня: python3 cases/_tools/build_truescan.py
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from PIL import Image
from compose import tile, cover, framed, save
from flow import render_flow

SRC, OUT = 'cases/_src/truescan', 'img/cases/truescan'
os.makedirs(OUT, exist_ok=True)
S = 2  # масштаб экспорта


def im(name): return Image.open(f'{SRC}/{name}.png').convert('RGB')
def css(img, x0, y0, x1, y1): return img.crop((x0 * S, y0 * S, x1 * S, y1 * S))


# обложка: список лидов + профиль лида
save(cover(im('lead_table'), im('profile')), f'{OUT}/cover.jpg')

# задачи
save(tile(css(im('lead_table'), 284, 150, 900, 640)), f'{OUT}/problem-1-list.jpg')            # тысячи входящих лидов, статусы
save(tile(css(im('kanban_filters'), 284, 120, 860, 560)), f'{OUT}/problem-2-filters.jpg')     # фильтры и представления
save(tile(css(im('row_menu'), 720, 300, 1440, 860)), f'{OUT}/problem-3-actions.jpg')          # много действий над лидом
save(tile(css(im('wiz1'), 400, 204, 1040, 697)), f'{OUT}/problem-4-input.jpg')                # ввод данных, дубли

# решения
save(tile(css(im('convert'), 460, 213, 980, 687)), f'{OUT}/solution-1-convert.jpg')         # конвертация с превью записей
save(tile(css(im('opp_profile'), 284, 16, 960, 520)), f'{OUT}/solution-2-converted.jpg')      # баннер «Converted from lead»
save(tile(css(im('assign'), 900, 220, 1440, 700)), f'{OUT}/solution-3-assign.jpg')            # назначение владельца без Apply
save(tile(css(im('wiz2'), 400, 157, 1040, 743)), f'{OUT}/solution-4-wizard.jpg')              # мастер в 3 шага, автокомплит адреса

# флоу
render_flow(f'{OUT}/flow.jpg', [
    ('New lead', 'Web form or 3-step wizard'),
    ('Triage', 'Table · Kanban · filters'),
    ('Assign & qualify', 'Owner, status, AI score'),
    ('Convert', 'Preview Account, Contact, Opportunity'),
    ('Opportunity', 'Profile with “Converted from lead”'),
], branches=[('Duplicate email check', 1), ('Export current view', 2), ('Archive · Undo 8 s', 3)])

# дизайн-система: состояния контролов
save(tile(css(im('states'), 0, 140, 1440, 970), size=(2400, 1500), pad=96, r=28), f'{OUT}/states.jpg')

# экраны
save(framed(im('profile'), (2400, 1200)), f'{OUT}/screen-profile.jpg')
save(framed(im('lead_kanban'), (1600, 1000)), f'{OUT}/screen-kanban.jpg')
save(framed(im('export'), (1600, 1000)), f'{OUT}/screen-export.jpg')
save(framed(im('noresults'), (1600, 1000)), f'{OUT}/screen-noresults.jpg')
save(framed(im('skeleton'), (1600, 1000)), f'{OUT}/screen-skeleton.jpg')
print('ok', sorted(os.listdir(OUT)))
