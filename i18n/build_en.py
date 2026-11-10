# Собирает английскую версию сайта (index.html) из русской (ru.html).
# Переводятся только целые текстовые узлы, значения атрибутов и строки в JS — разметка, стили и анимации не меняются.
# Запуск из корня проекта:  python3 i18n/build_en.py
import re, sys

SRC, OUT = 'ru.html', 'index.html'

# Текстовые узлы и значения атрибутов: русский → английский
T = {
 # meta, навигация
 'Алексей Гросул — продуктовый дизайнер и руководитель дизайна': 'Alexei Grosul — Product Designer & Head of Design',
 'Алексей Гросул — продуктовый дизайнер с опытом лида: 16 лет в IT, команда из 8 дизайнеров, no-code и AI-процессы.':
   'Alexei Grosul — Product Designer and Head of Design: 16 years in tech, a team of 8 designers, no-code and AI workflows.',
 'Алексей Гросул — на главную': 'Alexei Grosul — home',
 'Основная навигация': 'Main navigation', 'Язык': 'Language', 'Меню': 'Menu',
 'Кейсы': 'Case studies', 'Обо мне': 'About', 'Что умею': 'Skills', 'Связаться': 'Contact',
 # hero
 'Продуктовый дизайнер': 'Product Designer', 'и лид дизайна.': '&amp; Head of Design.',
 'Включаюсь в продукт на всех этапах: от первой встречи до запуска и метрик.':
   'I get involved at every stage — from the first meeting to launch and metrics.',
 '16 лет в IT. Веду команду из 8 дизайнеров, есть опыт управления разработкой. Разбираюсь в no-code, API и базах данных, поэтому проектирую то, что команда соберёт в срок.':
   '16 years in tech. I lead a team of 8 designers and have managed engineering teams. I know no-code, APIs and databases, so I design what the team can ship on time.',
 'Смотреть кейсы': 'View work',
 'Шоурил: Алексей Гросул — продуктовый дизайнер и лид дизайна': 'Showreel: Alexei Grosul — Product Designer and Head of Design',
 'Воспроизвести видео': 'Play video', 'Включить звук': 'Turn sound on', 'Проекты и компании': 'Projects and companies',
 # обо мне
 'Продуктовый подход.': 'Product mindset.', 'В дизайне и в делах.': 'In design and in delivery.',
 '16 лет в IT, последние 8 — в Zeroqode, где прошёл путь шаг за шагом: дизайнер-разработчик → тимлид команды разработки → руководитель дизайна. Работаю в связке с PM, разработкой, маркетингом и продажами и слежу за качеством и сроками, а не только за макетами.':
   '16 years in tech, the last 8 at Zeroqode, where I grew step by step: designer-developer → engineering team lead → Head of Design. I work closely with PMs, engineering, marketing and sales, and I care about quality and deadlines — not just the mockups.',
 'К скорости доставки дизайна — благодаря AI в процессах команды и настроенным AI-скиллам.': 'Faster design delivery — thanks to AI in the team’s workflow and custom AI skills.',
 'Дизайнеров в моей команде: найм, ревью, рост и стандарты качества.': 'Designers on my team: hiring, reviews, growth and quality standards.',
 # что умею
 'От стратегии': 'From strategy', 'до запущенного продукта.': 'to a shipped product.',
 'Дизайн-стратегия, продуктовый дизайн и AI-процессы — в одних руках, с опытом управления командой.':
   'Design strategy, product design and AI workflows in one place — backed by team leadership experience.',
 'Продуктовая стратегия': 'Product strategy',
 'Определяю, что строить и зачем — с учётом бизнес-целей клиента.': 'I define what to build and why, grounded in business goals.',
 'Исследование': 'Research', 'Дорожная карта': 'Roadmap', 'Позиционирование': 'Positioning',
 'Что строить, зачем и для кого.': 'What to build, why, and for whom.',
 'Продуктовый дизайн': 'Product design',
 'Превращаю сложные продукты в понятные и последовательные интерфейсы.': 'I turn complex products into clear, consistent interfaces.',
 'Дизайн-системы': 'Design systems', 'Прототипы': 'Prototypes', 'Сложное, сделанное понятным.': 'Complexity, made clear.',
 'AI в дизайн-процессах': 'AI in design workflows',
 'Встраиваю AI-инструменты в процесс разработки так, чтобы ускорять, а не заменять экспертизу.': 'I build AI tools into the workflow to speed up expertise, not replace it.',
 'AI-студия': 'AI studio', 'Автоматизация': 'Automation', 'Стандарты': 'Standards',
 'AI в процессах': 'AI workflows', 'Скорость без потери качества.': 'Speed without losing quality.',
 'Прототипы и передача в разработку': 'Prototyping &amp; dev handoff',
 'Кликабельные прототипы, спецификации и передача в разработку. Дальше — ревью реализации вместе с командой.':
   'Clickable prototypes, specs and dev handoff. Then build reviews together with the engineering team.',
 'В связке с командой разработки.': 'Hand in hand with engineering.',
 'Передача в разработку': 'Dev handoff', 'Дизайн-ревью': 'Design QA', 'Руководство командой.': 'Team leadership.',
 'Управляю командами дизайна и разработки: собеседования и найм, постановка задач, контроль качества, наставничество и грейды. Прошёл серию тренингов по лидерству.':
   'I manage design and engineering teams: interviews and hiring, task setting, quality control, mentoring and career levels. Completed a series of leadership trainings.',
 'Найм': 'Hiring', 'Наставничество': 'Mentoring', 'Стандарты качества': 'Quality standards',
 'Руководство командой': 'Team leadership', 'Найм, наставничество, качество.': 'Hiring, mentoring, quality.',
 'Подробнее +': 'More +',
 'Иллюстрация: Продуктовая стратегия': 'Illustration: Product strategy', 'Иллюстрация: Продуктовый дизайн': 'Illustration: Product design',
 'Иллюстрация: AI в процессах': 'Illustration: AI workflows', 'Иллюстрация: Прототипы и передача в разработку': 'Illustration: Prototyping and dev handoff',
 'Подробнее о продуктовой стратегии': 'More about product strategy', 'Подробнее о продуктовом дизайне': 'More about product design',
 'Подробнее об AI в процессах': 'More about AI workflows', 'Подробнее о прототипах и передаче в разработку': 'More about prototyping and dev handoff',
 # кейсы
 'Избранные кейсы': 'Selected work', 'Продукт.': 'Product.', 'С результатом.': 'With results.',
 'Кейсы скоро появятся здесь — с задачей, подходом и цифрами результата.': 'Case studies are coming soon — with the problem, the approach and measurable results.',
 'Все кейсы': 'All work',
 'Детский спорт': 'Youth sports', 'Бухгалтерия': 'Accounting', 'Финтех': 'Fintech', 'Лид-дизайнер': 'Lead Designer', 'Редизайн CRM для отдела продаж: входящие лиды, назначение, квалификация и конвертация в сделки — со всеми флоу и состояниями.': 'A redesign of a sales CRM: inbound leads, assignment, qualification and conversion to opportunities — with every flow and state.', 'Сервис для управления студенческими кредитами: все займы в одном месте, понятный следующий шаг и коучи, которые готовят документы.': 'A service for managing student loans: every loan in one place, a clear next step, and coaches who prepare the paperwork.', 'Перемотка видео': 'Video progress', 'AI-ассистент для бухгалтеров, который отвечает только по проверенным регламентам и показывает источник.': 'An AI assistant for bookkeepers that answers only from validated SOPs and shows the source.', 'Веб': 'Web',
 'Сервис для выбора детских турниров с проверенными отзывами команд, которые там играли.': 'A service for choosing youth tournaments, with verified reviews from teams who played there.', '[Отрасль]': '[Industry]', '[Название кейса]': '[Case title]',
 '[Одна фраза: какая была проблема и что сделал.]': '[One line: the problem and what I did.]',
 '[Платформа]': '[Platform]', 'Тип продукта': 'Product type', '[Роль]': '[Role]', 'Моя роль': 'My role',
 '[Срок]': '[Timeline]', 'Длительность': 'Duration', 'Смотреть кейс': 'View case',
 '[Название кейса 2]': '[Case title 2]', '[Название кейса 3]': '[Case title 3]',
 'заглушка — заменить скриншотом': 'placeholder — replace with a screenshot', 'Открыть кейс +': 'Open case +',
 'Превью проекта 2': 'Project preview 2', 'Превью проекта 3': 'Project preview 3',
 'Назад': 'Previous', 'Вперёд': 'Next',
 # цифры
 'Коротко о цифрах': 'By the numbers', 'Опыт в цифрах.': 'Experience in numbers.', '16 лет': '16 years',
 'В дизайне и IT: упаковка, 1,5 года в гейм-дизайне, 6 лет руководства разработкой, 1,5 года Head of Design.':
   'In design and tech: packaging, 1.5 years in game design, 6 years leading engineering, 1.5 years as Head of Design.',
 'Запущенных продуктов — от MVP до сложных платформ.': 'Products launched — from MVPs to complex platforms.',
 '2 команды': '2 teams',
 'Под моим руководством: разработка (6&nbsp;человек) и&nbsp;дизайн (8&nbsp;дизайнеров).': 'Under my lead: engineering (6&nbsp;developers) and&nbsp;design (8&nbsp;designers).',
 # отзывы
 'Отзывы': 'Testimonials', 'Что говорят': 'What people say', 'о совместной работе.': 'about working together.',
 'Рекомендации коллег.': 'Recommendations from colleagues.',
 'Все рекомендации на LinkedIn': 'All recommendations on LinkedIn',
 'Рабочий стол дизайнера с макетами': 'Designer’s desk with mockups', 'Командная встреча / ревью': 'Team meeting / review',
 'Созвон и стикеры с воркшопа': 'Call and workshop sticky notes',
 # как я работаю
 'Как я работаю': 'How I work', 'AI ускоряет.': 'AI speeds things up.', 'Качество — на дизайнере.': 'Quality stays with the designer.',
 'Фаза 1': 'Phase 1', 'Фаза 2': 'Phase 2', 'Фаза 3': 'Phase 3', 'Понять': 'Understand',
 'Созвоны с клиентом с первого дня, бизнес-цели и метрики. AI собирает ресерч и сводки по конкурентам и интервью, выводы делает дизайнер.':
   'Stakeholder calls from day one, business goals and metrics. AI gathers research and summaries of competitors and interviews; the designer draws the conclusions.',
 'ресерч, сводки ·': 'research, summaries ·', 'Дизайнер:': 'Designer:', 'выводы, скоуп': 'insights, scope',
 'Спроектировать': 'Design',
 'Черновой прототип до разработки. AI быстро даёт варианты, дизайнер выбирает, исправляет и доводит до системы.':
   'A draft prototype before development. AI quickly generates options; the designer selects, refines and turns them into a system.',
 'варианты, черновики ·': 'options, drafts ·', 'решения, дизайн-система': 'decisions, design system',
 'Проверить и запустить': 'Validate and launch',
 'Экспертная проверка перед разработкой: ошибки в UX, состояниях и консистентности, которые не видны без опыта. После запуска — метрики и итерации.':
   'Expert review before development: UX, state and consistency issues that are invisible without experience. After launch — metrics and iterations.',
 'проверки, отчёты ·': 'checks, reports ·', 'качество, итерации': 'quality, iterations',
 # форматы
 'Форматы работы': 'Ways to work together', 'Как я могу': 'How I can', 'быть полезен.': 'help.',
 'Открыт к позициям продуктового дизайнера или дизайн-лида, а также к консультациям по AI-процессам в дизайн-командах.':
   'Open to Product Designer and Design Lead roles, as well as consulting on AI workflows for design teams.',
 'полная занятость': 'full-time',
 'Проектирование продукта от исследования до запуска.': 'Product design from research to launch.',
 'UX/UI для веб- и мобильных продуктов': 'UX/UI for web and mobile products',
 'Работа с метриками и аналитикой': 'Working with metrics and analytics', 'Написать мне': 'Get in touch',
 'Лид дизайна': 'Design Lead', 'или руководитель дизайна': 'or Head of Design',
 'Дизайн-стратегия, стандарты и управление командой.': 'Design strategy, standards and team management.',
 'Дорожная карта дизайн-функции': 'Design function roadmap', 'Найм, наставничество, грейды': 'Hiring, mentoring, career levels',
 'Внедрение AI в процессы': 'Bringing AI into workflows', 'Консультации': 'Consulting', 'AI в дизайне': 'AI in design',
 'Разовые консультации по процессам и инструментам.': 'One-off consulting on workflows and tools.',
 'Аудит текущих процессов': 'Audit of current workflows',
 'Подбор инструментов': 'Tool selection', 'Регламенты для команды': 'Team guidelines',
 # вопросы
 'Вопросы': 'FAQ', 'Что обычно': 'What people', 'спрашивают.': 'usually ask.',
 'Почему вы ищете роль продуктового дизайнера или лида дизайна?': 'Why are you looking for a Product Designer or Design Lead role?',
 'Хочу работать ближе к продукту: влиять на решения, проверять их на данных и отвечать за результат дизайна, а не только за процесс вокруг него.':
   'I want to work closer to the product: influence decisions, validate them with data and own the outcome of design, not just the process around it.',
 'Как вы работаете с PM и разработчиками?': 'How do you work with PMs and engineers?',
 'Дизайнер подключается с первого созвона с клиентом. До разработки делаем черновой прототип и согласуем скоуп MVP, чтобы разработчики получали проверенное решение, а не набор пожеланий.':
   'Design joins from the very first stakeholder call. Before development we build a draft prototype and agree on the MVP scope, so engineers get a validated solution, not a wish list.',
 'Как вы относитесь к AI в дизайне?': 'What is your take on AI in design?',
 'Использую каждый день и выстраивал AI-процессы в команде. Но первые генерации почти всегда требуют доработки: ошибки в UX и деталях видит только дизайнер. Поэтому AI ускоряет работу, а за качество отвечает человек.':
   'I use it every day and have built AI workflows for my team. But first generations almost always need work: only a designer catches UX and detail issues. So AI speeds things up, and a human owns the quality.',
 'Есть ли у вас кейсы с метриками?': 'Do you have case studies with metrics?',
 'Часть кейсов с конкретными цифрами, и именно они лежат в основе портфолио. В остальных опираюсь на аналитику, обратную связь пользователей и команды.':
   'Some of my case studies have hard numbers, and they form the core of this portfolio. For the rest, I rely on analytics and feedback from users and the team.',
 'С какими стеками и инструментами работаете?': 'Which stacks and tools do you work with?',
 'Figma (включая MCP), Bubble и другие no-code платформы, FlutterFlow, а также стеки React, Vue, Flutter и WordPress на уровне, достаточном для общего языка с разработкой.':
   'Figma (including MCP), Bubble and other no-code platforms, FlutterFlow, plus React, Vue, Flutter and WordPress — enough to speak the same language as engineering.',
 # контакты и футер
 'Давайте': 'Let’s', 'поговорим.': 'talk.',
 'Расскажите о позиции или задаче — отвечу в течение дня.': 'Tell me about the role or project — I reply within a day.',
 'Написать': 'Write to me', 'Написать на почту': 'Email me', 'Алексей Гросул': 'Alexei Grosul',
 'Дизайн, который приносит': 'Design that drives', 'результат.': 'results.',
 'Копировать': 'Copy', 'Скопировать email': 'Copy email', 'О себе': 'About',
 'Соцсети': 'Social', 'Меню в подвале': 'Footer menu',
 '&copy; 2026 Алексей Гросул. Все права защищены.': '&copy; 2026 Alexei Grosul. All rights reserved.',
 'Наверх &uarr;': 'Back to top &uarr;',
 # форма
 'Расскажите о позиции или задаче.': 'Tell me about the role or project.', 'Что вас интересует?': 'What are you interested in?',
 'Консультация': 'Consulting', 'Другое': 'Other', 'Имя': 'Name', 'Почта': 'Email', 'Сообщение': 'Message',
 'О какой позиции или задаче речь?': 'What role or project is this about?',
 'Отправить': 'Send', 'или на почту': 'or email', 'Спасибо!': 'Thank you!',
 'Письмо открылось в почтовой программе — проверьте и отправьте. Не открылось? Напишите на':
   'Your email app has opened — check the message and send it. Didn’t open? Write to',
 'Закрыть': 'Close',
}
# Строки внутри JS
JS = {"'Воспроизвести видео'": "'Play video'", "'Пауза'": "'Pause'", "'Слайд '": "'Slide '", "' из '": "' of '",
      "'Скопировано'": "'Copied'", "'Копировать'": "'Copy'",
      "'Укажите имя, чтобы я знал, кому отвечать.'": "'Please add your name so I know who to reply to.'",
      "'Введите корректный email, например name@company.com.'": "'Please enter a valid email, e.g. name@company.com.'",
      "'Спасибо, '": "'Thank you, '"}

LANG_RU = '<span class="lang" role="group" aria-label="Язык"><button type="button" class="on" aria-pressed="true">RU</button><button type="button" aria-pressed="false" aria-disabled="true" title="English version — скоро">EN</button></span>'
LANG_EN = '<span class="lang" role="group" aria-label="Language"><a class="on" href="index.html" hreflang="en" aria-current="page">EN</a><a href="ru.html" hreflang="ru" lang="ru">RU</a></span>'

s = open(SRC).read()
assert LANG_RU not in s, 'в ru.html ещё старый переключатель — сначала запусти i18n/setup_ru.py'
s = s.replace('<html lang="ru">', '<html lang="en">', 1)
# переключатель: EN активен, RU — ссылка
s = re.sub(r'<span class="lang" role="group" aria-label="Язык">.*?</span>', LANG_EN, s, count=1, flags=re.S)
miss = []
for ru, en in sorted(T.items(), key=lambda kv: -len(kv[0])):
    pat_txt = re.compile(r'>(\s*)' + re.escape(ru) + r'(\s*)<')
    pat_att = re.compile(r'="' + re.escape(ru) + r'"')
    s, a = pat_txt.subn(lambda m: '>' + m.group(1) + en + m.group(2) + '<', s)
    s, b = pat_att.subn('="' + en.replace('&amp;', '&') + '"', s)
    if not a + b: miss.append(ru)
for ru, en in JS.items():
    if ru not in s: miss.append(ru)
    s = s.replace(ru, en)
s = s.replace('data-suffix=" лет"', 'data-suffix=" years"').replace('data-suffix=" команды"', 'data-suffix=" teams"')
open(OUT, 'w').write(s)
# контроль: кириллица вне комментариев и стилей
body = re.sub(r'<!--.*?-->|<style.*?</style>|/\*.*?\*/', '', s, flags=re.S)
left = sorted(set(re.findall(r'[^<>"\']*[А-Яа-яЁё][^<>"\']*', body)) - {'RU'})
print('не найдено в исходнике:', miss)
print('осталась кириллица:', [x.strip() for x in left if x.strip() and 'lang="ru"' not in x][:40])
