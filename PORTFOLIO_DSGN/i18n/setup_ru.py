# Разовая подготовка русской версии: alexey-portfolio_5.html → ru.html с рабочим переключателем EN | RU.
import os
SRC, OUT = 'alexey-portfolio_5.html', 'ru.html'
OLD = '<span class="lang" role="group" aria-label="Язык"><button type="button" class="on" aria-pressed="true">RU</button><button type="button" aria-pressed="false" aria-disabled="true" title="English version — скоро">EN</button></span>'
NEW = '<span class="lang" role="group" aria-label="Язык"><a href="index.html" hreflang="en" lang="en">EN</a><a class="on" href="ru.html" hreflang="ru" aria-current="page">RU</a></span>'
CSS_OLD = '.lang button{'
CSS_NEW = '.lang button,.lang a{'
s = open(SRC).read()
assert OLD in s
s = s.replace(OLD, NEW)
# стили переключателя: те же, что у кнопок, плюс для ссылок
s = s.replace('.lang button{font:inherit;', '.lang button,.lang a{display:inline-block;text-decoration:none;font:inherit;', 1)
s = s.replace('.lang button.on{', '.lang button.on,.lang a.on{', 1)
open(OUT, 'w').write(s)
os.remove(SRC)
print('ok', OUT)
