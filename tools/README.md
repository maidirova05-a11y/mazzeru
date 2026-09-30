# tools — генераторы

Скрипты, из которых собраны сайт и материалы. Пути внутри — абсолютные (`C:\Users\USER\OneDrive\Desktop\Mazzeru\...`), при работе на другом компьютере поправьте константы `B`, `ROOT`, `TMP` в начале файлов.

| Файл | Что делает |
|---|---|
| `gen4.py`, `css4.py` | генерируют 4 страницы сайта (`index.html` и др.) |
| `brand_mark.py` | геометрия знака ZZ (SVG) |
| `brand.py` | логотипы в SVG (`brand/logo/svg`) |
| `topng.py` | SVG/HTML → PNG через headless Edge (запускать из PowerShell) |
| `insta.py` | шаблоны Instagram (`brand/instagram`) |
| `carousel.py` | карусель «Знакомство» (`brand/instagram/carousel`) |
| `ds_build.py` | секция брендбука |
| `vocal2.py`, `analyze.py` | разбор трека для монтажа Reels |

Видео: `brand/video/src` (`render.py` — интро и аутро, `reel.py` — первый Reels, `music.py`/`outro_music.py` — своя музыка).
