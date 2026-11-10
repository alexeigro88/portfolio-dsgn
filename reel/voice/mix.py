# Сведение озвучки с музыкой ролика reel-story-en.
# Фразы vo_01..vo_07 ставятся на старт своих сцен, музыка приглушается под голосом (sidechain),
# итог выравнивается до −16 LUFS / −1.5 dBTP и вклеивается в видео.
# Запуск из папки reel/:  python3 voice/mix.py voice/draft  reel-story-en-vo-draft.mp4
import sys, glob, subprocess, imageio_ffmpeg

VO_DIR, OUT = sys.argv[1], sys.argv[2]
FF = imageio_ffmpeg.get_ffmpeg_exe()
T = [1.9, 5.15, 9.1, 13.45, 17.1, 21.0, 24.6]  # старт каждой фразы, с
files = [sorted(glob.glob(f'{VO_DIR}/vo_{k:02d}.*'))[0] for k in range(1, 8)]

args = [FF, '-y', '-loglevel', 'error', '-i', 'sound-story.wav']
F = ''
for k, (t, f) in enumerate(zip(T, files), 1):
    args += ['-i', f]; ms = int(t * 1000)
    # обрезаем тишину по краям фразы, чтобы старт совпадал со сценой
    F += (f'[{k}]silenceremove=start_periods=1:start_threshold=-45dB,aformat=sample_rates=44100:channel_layouts=stereo,'
          f'adelay={ms}|{ms},apad=whole_dur=28[v{k}];')
F += ''.join(f'[v{k}]' for k in range(1, 8)) + 'amix=inputs=7:normalize=0,volume=1.6,asplit=2[vo][key];'
F += '[0]volume=0.85[mu];[mu][key]sidechaincompress=threshold=0.02:ratio=8:attack=15:release=350[duck];'
F += '[duck][vo]amix=inputs=2:normalize=0,loudnorm=I=-16:TP=-1.5:LRA=11[out]'
subprocess.run(args + ['-filter_complex', F, '-map', '[out]', '-ar', '44100', '-t', '28', 'voice/mix.wav'], check=True)
subprocess.run([FF, '-y', '-loglevel', 'error', '-i', 'reel-story-en.mp4', '-i', 'voice/mix.wav', '-c:v', 'copy',
                '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', OUT], check=True)
print('ok', OUT)
