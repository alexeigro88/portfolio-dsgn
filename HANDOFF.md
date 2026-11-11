# Хэндофф: портфолио Алексея Гросула

Актуально на 10.11.2026. Документ для продолжения работы в другой сессии Claude: что сделано, как устроено, какие правила, что дальше.

## Цель и позиционирование
- Алексей ищет работу **Product Designer / Head of Design**. Акцент — продуктовый дизайн, лидерство подсвечено.
- Сайт — одностраничное портфолио на шаблоне **Kaleo** (все моушн-эффекты сохранены) + детальные страницы кейсов.
- **Основной язык — английский** (`index.html`), русский — второй (`ru.html`), переключатель **EN | RU** в шапке.

## Правила работы (решения и фидбек Алексея)
- Общение по-русски, кратко и конкретно.
- **Не выдумывать факты, цифры и отзывы.** Нет данных — ставить `[плейсхолдер]`. Отклонено: «0 сорванных сроков» («сроки мы тоже срывали»). Черновой отзыв Влада Ларина удалён по просьбе.
- **Не делать акцент на no-code.** Акцент — классическая продуктовая разработка: кликабельные прототипы → передача команде разработки → работа в связке с инженерами.
- Стиль: чистый, светлый, Apple-like. Тексты — от первого лица, без третьего лица.
- **Не трогать моушн и эффекты Kaleo.**
- Демо-данные прототипов (цифры на экранах) не выдавать за результаты.

## Файлы
| Путь | Что это |
|---|---|
| `ru.html` | **Источник правды.** Русская версия, весь CSS/JS inline. Все правки текста и вёрстки — здесь. |
| `index.html` | EN-версия, **генерируется**: `python3 i18n/build_en.py`. Руками не править. |
| `i18n/build_en.py` | Словарь RU→EN `T` (замена целых текстовых узлов `>текст<`, атрибутов `="текст"` и JS-строк), карта JS-строк, замена переключателя языка, `data-suffix` (` лет`→` years`, ` команды`→` teams`). Печатает непереведённые ключи (`'Язык'` — ожидаемо) и остатки кириллицы. |
| `cases/case-template.html` | Шаблон детальной страницы кейса (EN). |
| `cases/tournament-guru.html`, `cases/bookkeeper-ai.html`, `cases/stulo.html`, `cases/truescan.html` | Готовые кейсы. |
| `cases/_tools/` | Пайплайн визуалов кейсов (см. ниже). |
| `cases/_src/<проект>/` | Исходные скриншоты прототипов (DPR 2). |
| `img/` | Картинки сайта: `portrait.jpg`, `skill-*.jpg`, `format-1..3.jpg` (+ svg-фолбэк), `av-*.jpg` (фото авторов отзывов), `reel-poster.jpg`, `cases/<проект>/*.jpg`. |
| `reel/` | Шоурил в hero (см. ниже). |
| `preview/` | Автономные HTML для просмотра без сервера (картинки и видео встроены base64). Пересобираются скриптом ниже. |
| `AUDIT.md` | Ранний аудит портфолио глазами HR/нанимающего менеджера (частично выполнен). |
| `alexey-portfolio_5.backup.html`, `kaleo_reference.html`, `video_reference.mp4` | Бэкап и референсы. |

Локальный просмотр: `python3 -m http.server 8123` из корня → http://localhost:8123/ (EN), `/ru.html`, `/cases/<кейс>.html`.
Примечание: `http.server` не отдаёт видео по Range, поэтому перемотка ролика локально сбрасывается на 0 — на хостинге и в `preview/` работает.

## Главная страница — текущее содержимое
- **Шапка:** логотип, меню `#work` Кейсы · `#team` · `#services` · `#stories` Отзывы, переключатель EN|RU, кнопка Contact (`.navr .btn-sm`, высота 33px). Мобильное меню: `.mbtn` + `nav.mnav#mnav` (селекторы `.gnav .mnav`, т.к. шаблон прячет `.gnav nav`), JS в конце файла: toggle, клик по ссылке, клик вне, Escape, resize.
- **Hero-видео:** `reel/reel-story-en-vo.mp4`, постер `img/reel-poster.jpg`. Звук по умолчанию: флаг `userMuted`, `tryPlay` пробует со звуком → фолбэк без звука, `unlock` по pointerdown/keydown/touchend. Кнопки пауза/звук `.vctl`, **полоса прогресса** `.vbar#vbar` (время, клик/перетаскивание/стрелки ±5 с).
- **Обо мне:** «16 лет в IT, последние 8 — в Zeroqode: дизайнер-разработчик → тимлид команды разработки → руководитель дизайна…». Карточки: 🚀 `+50%` к скорости доставки дизайна (AI в процессах команды) и `8` дизайнеров в команде.
- **Цифры:** 16 лет (упаковка, 1,5 года гейм-дизайн, 6 лет руководства разработкой, 1,5 года Head of Design) · 200+ запущенных продуктов · 2 команды (разработка 6 человек, дизайн 8 дизайнеров).
- **Навыки:** 4 карточки, 4-я — «Прототипы и передача в разработку».
- **Кейсы (`#work`):** 01 Tournament Guru → `cases/tournament-guru.html`, 02 BookKeeper AI → `cases/bookkeeper-ai.html`, 03 StuLo → `cases/stulo.html`. Обложки `img/cases/<проект>/cover.jpg`. Роль и срок в карточках — `[Роль]`, `[Срок]`.
- **Отзывы (`#srail`):** Tatiana Smirnova, Ana Alcaza, Julia Fishchenko, Alexander Rusnac, Julia Verbitchi (цитаты на английском, фото `img/av-*.jpg`), ссылка «Все рекомендации на LinkedIn» справа от заголовка.
- **Форматы работы:** без цен, картинки `img/format-{1,2,3}.jpg`.
- **Футер:** компактный, без фамилии-вордмарка; соцсети с тултипами (`.tsoc a::after` + `data-tip`): Dribbble, LinkedIn, Instagram, **Telegram** (https://t.me/alexeighty8); иконка почты — синий градиентный тайл.
- **Контакты:** alexeigro@gmail.com · Dribbble https://dribbble.com/AlexeiG · LinkedIn https://md.linkedin.com/in/alexei-grosul-63aa6a73 · Instagram https://www.instagram.com/alex.eighty8/ · Telegram @alexeighty8.

### Технические особенности шаблона
- Lenis smooth scroll, pinned rails, stacked work cards, кастомный курсор (белая точка — это он), count-up через `data-count` + `data-prefix`/`data-suffix`, `<dialog>` контактов (`data-open-sheet`).
- Squircle: карточки `.sq` — JS SVG (`sqPath`, фактор 1.6); нативный `corner-shape:squircle` в `@supports`; `.btn,.pbtn{corner-shape:squircle!important}`; круги (аватары, `.vbtn`, курсор) остаются кругами.
- Доп. CSS вставлять в **последний** `</style>` (раньше ошибочно попадало внутрь media query).
- Градиентный текст: `padding-right:.12em;margin-right:-.12em`, иначе режется последняя буква.

## Кейсы
**Шаблон** (`cases/case-template.html`): раскладка по референсу anton-ux.framer.website/batmind, типографика и токены 1:1 с главной (Figtree / Inter Tight / Inter; `.h1`=h-xl, `.h2`=h-l, `.body`=lede-l). Секции: обложка → интро + meta (роль, команда, сроки, платформа, пользователи) → Design process (5 шагов) → Problems (сетка `.mix` 4 карточки + 4 картинки) → Solutions (так же) → User flow → Design system (шрифты + 6 цветов из реальных токенов прототипа) → UI design (`.screens`: широкий + 2) → Results → What I learned → Next case + CTA. Персона из шаблона в кейсах убрана.

**Цепочка «следующий кейс»:** Tournament Guru → BookKeeper AI → StuLo → TrueScan → Uncloud360 → Tournament Guru. У карточки `.ncase` есть светлый градиент `.ncase .media::after` под подписью.

| Кейс | Прототип | Суть | Шрифты / токены |
|---|---|---|---|
| Tournament Guru | https://app.tournamentgurus.com/ | Выбор детских турниров с проверенными отзывами | Space Grotesk + Inter, navy/blue/red |
| BookKeeper AI | https://bookkeeper-ai-tau.vercel.app/ | Внутренний AI-ассистент бухгалтерской фирмы: отвечает только по опубликованным SOP, с источниками; роли Bookkeeper / SME / QC Librarian | Manrope, `#1A73E8`, статусы Published/Needs Revalidation |
| TrueScan | Figma `rFFixRw1aznY4sWHRFKyJk` (Leads, Opportunities, Proposals, Projects, Time tracking, Foundations) | **Не редизайн**: операционная платформа с нуля для компании 3D-сканирования зданий (reality capture). Цикл: Leads → Opportunities → Proposals (шаблон на 18 секций) → Projects → Time tracking (часы, суточные, пробег, недельное согласование). Роль — Lead Designer, срок 2 недели. Метрики только посчитанные по файлу: 100 экранов, 5 модулей, 3 клика лид→сделка, 3600+ инстансов | Inter, brand `#EE6A1F`, sidebar `#0F1A2E` |
| StuLo | https://stulo-v2.vercel.app/#signin («Explore the demo») | Управление федеральными студенческими кредитами США: синк займов, следующий шаг, AI-коуч + живые коучи, декодер писем, PSLF | Bricolage Grotesque + Manrope, navy `#121740`, bright `#465AFF` |

Во всех кейсах **плейсхолдеры** ждут ответа Алексея: роль, команда, сроки, год, результаты (3 метрики), «What I learned». Также `[Роль]`/`[Срок]` в карточках на главной.
Особенности: у Tournament Guru нет мобильной версии и карта с водяным знаком API — используются только десктоп-скрины без карты. В StuLo текст письма в декодере введён для демонстрации. У StuLo скрыт демо-переключатель `.demo-tg`.

### Пайплайн визуалов (`cases/_tools/`)
- `compose.py`: `gradient`, `browser(shot,width)` (окно браузера), `tile(crop,size=(900,1020),pad=56,r=22,valign)` (фрагмент UI карточкой на светлом фоне), `photo_tile`, `cover(main,second)` (16:9, два окна внахлёст), `framed(shot,size)`, `save`.
- `flow.py`: `render_flow(out, steps, branches=[(текст, номер_шага)], size)` — HTML-схема через Playwright.
- `build_<проект>.py`: читает `cases/_src/<проект>/*.png` (DPR 2; `css()` кропает в CSS-пикселях ×2), пишет `img/cases/<проект>/`: `cover`, `problem-1..4`, `solution-1..4`, `flow`, `screen-*`.
- Скрины снимаются Playwright 1440×900, DPR 2; фрагменты — через `locator.screenshot()` у карточки, найденной по тексту. Запуск из корня: `python3 cases/_tools/build_stulo.py`.
- Новый кейс: снять скрины → `build_<проект>.py` → HTML генерируется копированием готового кейса (head/шапка/футер) с заменой секций → ссылка в карточке на главной (`ru.html` + словарь `build_en.py`) → цепочка next case → проверка 1440/390 (нет горизонтального скролла, все картинки грузятся) → пересборка превью.

### Пересборка превью
```python
import re,base64,mimetypes,os
def build(src,out,links,base='.'):
    s=open(src).read()
    def rep(m):
        p=os.path.normpath(os.path.join(base,m.group(2)))
        if not os.path.exists(p): return m.group(0)
        mt=mimetypes.guess_type(p)[0] or 'application/octet-stream'
        return m.group(1)+'"data:'+mt+';base64,'+base64.b64encode(open(p,'rb').read()).decode()+'"'
    s,n=re.subn(r'((?:src|poster)=)"((?:\.\./)?(?:img|reel)/[^"]+)"',rep,s)
    for a,b in links.items(): s=s.replace('href="%s'%a,'href="%s'%b)
    open(out,'w').write(s)
L={'index.html':'portfolio-en.html','ru.html':'portfolio-ru.html','cases/case-template.html':'case-template.html','cases/tournament-guru.html':'case-tournament-guru.html','cases/bookkeeper-ai.html':'case-bookkeeper-ai.html','cases/stulo.html':'case-stulo.html'}
build('index.html','preview/portfolio-en.html',L); build('ru.html','preview/portfolio-ru.html',L)
CL={'../index.html':'portfolio-en.html','case-template.html':'case-template.html','tournament-guru.html':'case-tournament-guru.html','bookkeeper-ai.html':'case-bookkeeper-ai.html','stulo.html':'case-stulo.html'}
for c in ('tournament-guru','bookkeeper-ai','stulo'):
    build(f'cases/{c}.html',f'preview/case-{c}.html',CL,base='cases')
```

## Шоурил (hero)
- Финал: `reel/reel-story-en-vo.mp4` (28 с, 7 сцен, анимированный маскот, голос ElevenLabs «Mike», музыка с даккингом). Исходник — `reel/reel-story-en.html` (таймлайн с `window.seek(t)`).
- Рендер: `reel/tools/render.py` — Playwright DPR 2 (4K) → Lanczos до 1080p, x264 CRF 14. Маскот — видео-плейты, подобранные по цвету фона (rgb 236,235,244), без вырезки: `reel/mascot-*-plate/`, исходные кадры `reel/mascot-*-frames/`.
- Звук: `reel/voice/mix.py` — фразы `reel/voice/final/vo_01..07.wav` (нарезка дубля `vo_take.mp3` по silencedetect), музыка с sidechaincompress, loudnorm −16 LUFS.
- Русская версия ролика не нужна. Старые версии — `reel/drafts/`.

## Что дальше
1. ~~Кейс TrueScan~~ — готов (`cases/truescan.html`, `build_truescan.py`; экспорт фреймов Figma 2x через MCP `download_assets`, нужен доступ к www.figma.com; для `flow.py` — `CHROME_PATH=/opt/pw-browsers/chromium`). Исходный план: (Figma, командный аккаунт): https://www.figma.com/design/rFFixRw1aznY4sWHRFKyJk/TrueScan-%E2%80%94-Entity-Profiles-Redesign?node-id=1-3
   Страницы: Read me, Foundations (Foundations — V2, 12 Interaction states, 13 Filter dropdowns & sort), Icons, **Leads** (00 Notes, 01 List, 02 Profile, 03 Flows, 04 States), Opportunities, Proposals · Draft, Projects, Time tracking · Draft.
   План: прочитать Read me / Notes (задача и контекст) → экспортировать PNG 2x ключевых экранов в `cases/_src/truescan/` → токены из Foundations → `cases/_tools/build_truescan.py` (для фреймов из Figma вместо скринов браузера) → `cases/truescan.html` → добавить карточку 04 на главную (сейчас «01 / 03» … «03 / 03» — обновить нумерацию) и вставить в цепочку next case. Проверить, можно ли показывать проект публично (NDA); при необходимости обезличить данные.
2. Ещё кейсы из прототипов: Listing Suite https://listing-suite.vercel.app/ · Care Around Me https://care-around-me.vercel.app/
3. Заполнить плейсхолдеры кейсов, когда Алексей пришлёт роль, команду, сроки, год, результаты, выводы.
4. Открытые мелочи: финальный заголовок hero, фотореальные картинки форматов, фото получше для Julia F., реальные цифры для карточки достижений, CV (PDF) — см. `AUDIT.md`.

## TrueScan — как устроены визуалы
- Стиль по фидбеку Алексея: плоско, крупно, без перспективы/3D и сильных свечений, без наложенных теней-карточек.
- `cases/_tools/flat.py`: `view()` — кадр-окно в реальный экран 16:11 (элемент целиком, родные тени макета), `flow_text`, `device`, `cover` (дрон из фрейма «E0 · Sign in» + экран). JPEG q92 без субдискретизации.
- Экспорт фреймов из Figma: MCP `download_assets` (scale 2/3) → `cases/_src/truescan/` и `x3/`. Нужен хост www.figma.com в сети окружения.
- `CHROME_PATH=/opt/pw-browsers/chromium python3 cases/_tools/build_truescan.py`.
- Кейсы при открытии прокручиваются наверх (скрипт в начале body); прогресс-бар шоурила — тонкая линия по низу ролика.

## Uncloud360 (кейс №1 на главной)
- Figma `E9hPeByYOE9UiyuvSDhl5I`. Мобильный AI-коуч (выгорание, семья, работа), упор на мобилку, десктоп вторым.
- **Маскот — 3D-персонаж с телом** (облако с руками и планшетом, позы presenting/pointing) — экраны концепта **v2** (страница «Mobile concept — v2», напр. 32:559). Не облако Nimbus/Kota из v4.
- `cases/_tools/build_uncloud.py`: телефоны в плоских рамках, обложка, ряды экранов, позы маскота, слайды для презентации → `img/cases/uncloud/presentation/` (5 шт., 2880×1620, Manrope).
- Роль Lead Designer, срок 3 недели. Десктоп — тоже v2 (страница «Desktop concept — v2», 37:2 и др.). Плейсхолдер остался только у команды.
