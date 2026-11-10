# Изометрические стопки экранов для блоков Problems / Details that matter (TrueScan).
# Рендер в Chromium с deviceScaleFactor 3 из экспортов Figma 2x/3x — экраны остаются резкими.
# Запуск из корня: CHROME_PATH=/opt/pw-browsers/chromium python3 cases/_tools/iso_pair.py
import os
from PIL import Image
from playwright.sync_api import sync_playwright

S, O = 'cases/_src/truescan', 'img/cases/truescan'
TMP = os.path.abspath('cases/_src/_covers'); os.makedirs(TMP, exist_ok=True)


def scr(src, name, s):
    im = Image.open(src).convert('RGB'); im.crop((0, 0, 1440 * s, 900 * s)).save(f'{TMP}/{name}.png')
    return 'file://' + f'{TMP}/{name}.png'


def iso(out, shots, W=900, H=760):
    sw = 640; sh = round(sw * 900 / 1440)
    layers = ''.join(
        f'<div class="s" style="transform:translate3d({i*40}px,{i*-150}px,{i*40}px)"><img src="{u}"></div>'
        for i, u in enumerate(shots))
    html = f'''<html><head><style>
*{{margin:0;padding:0;box-sizing:border-box}} html,body{{width:{W}px;height:{H}px;overflow:hidden}}
body{{background:linear-gradient(160deg,#F6F7F9,#ECEFF3)}}
.stage{{position:absolute;left:50%;top:64%;transform-style:preserve-3d;transform:rotateX(50deg) rotateZ(-32deg)}}
.s{{position:absolute;width:{sw}px;height:{sh}px;left:{-sw/2}px;top:{-sh/2}px;border-radius:14px;overflow:hidden;background:#fff;
   box-shadow:0 0 0 1px rgba(16,24,40,.08),0 40px 60px -24px rgba(16,24,40,.28)}}
.s img{{display:block;width:100%;height:100%}}
</style></head><body><div class="stage">{layers}</div></body></html>'''
    p = f'{TMP}/iso.html'; open(p, 'w').write(html)
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=os.environ.get('CHROME_PATH') or None)
        pg = b.new_page(viewport={'width': W, 'height': H}, device_scale_factor=3)
        pg.goto('file://' + p); pg.wait_for_timeout(400); pg.screenshot(path=f'{TMP}/iso.png'); b.close()
    Image.open(f'{TMP}/iso.png').convert('RGB').save(out, quality=93, subsampling=0, optimize=True, progressive=True)


X3 = f'{S}/x3'
iso(f'{O}/problems-iso.jpg', [scr(f'{S}/timesheet.png', 'p3', 2), scr(f'{S}/proposal_builder.png', 'p2', 2), scr(f'{X3}/lead_table.png', 'p1', 3)])
iso(f'{O}/details-iso.jpg', [scr(f'{X3}/wiz2.png', 'd3', 3), scr(f'{X3}/opp_profile.png', 'd2', 3), scr(f'{X3}/convert.png', 'd1', 3)])
print('ok')
