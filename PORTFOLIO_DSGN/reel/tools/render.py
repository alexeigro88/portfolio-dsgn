# Рендер ролика с суперсэмплингом: кадры 3840×2160 (device scale 2) → Lanczos до 1920×1080, x264 CRF 14.
# Страница должна отдавать window.seek(t). Запуск из папки reel/ при поднятом сервере (python3 -m http.server 8123 в корне проекта):
#   python3 tools/render.py http://localhost:8123/reel/reel-story-en.html reel-story-en.mp4 28
import subprocess, sys
import imageio_ffmpeg
from playwright.sync_api import sync_playwright

url, out, DUR = sys.argv[1], sys.argv[2], float(sys.argv[3])
FPS = 30
ff = subprocess.Popen([imageio_ffmpeg.get_ffmpeg_exe(), '-y', '-f', 'image2pipe', '-framerate', str(FPS), '-c:v', 'png', '-i', '-',
                       '-vf', 'scale=1920:1080:flags=lanczos', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '14',
                       '-preset', 'slow', '-profile:v', 'high', '-movflags', '+faststart', out],
                      stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={'width': 1920, 'height': 1080}, device_scale_factor=2)
    pg.goto(url, wait_until='networkidle')
    pg.evaluate('document.fonts.ready')
    pg.wait_for_timeout(1500)
    for i in range(int(FPS * DUR)):
        pg.evaluate(f'seek({i / FPS})')
        ff.stdin.write(pg.screenshot(type='png'))
    b.close()
ff.stdin.close()
print('exit', ff.wait())
