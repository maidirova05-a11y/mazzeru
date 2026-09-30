import json, os, shutil, datetime

D = r"C:\Users\USER\AppData\Local\Temp\claude\C--Users-USER-OneDrive-Desktop-Mazzeru\dbded89a-b618-4a72-a2af-809ec598348c\scratchpad\ds\project"
BR = r"C:\Users\USER\OneDrive\Desktop\Mazzeru\brand"
os.makedirs(D + r"\fonts", exist_ok=True)
for f in ["Unbounded-ExtraBold.ttf", "InterTight-Regular.ttf", "InterTight-Bold.ttf", "InterTight-Black.ttf"]:
    shutil.copy(os.path.join(BR, "fonts", f), os.path.join(D, "fonts", f))

C = lambda n, l, d, u: {"name": n, "value": {"light": l, "dark": d}, "usage": u}
tokens = {
    "name": "Mazzeru", "version": 1,
    "color": {
        "themes": [{"id": "light", "name": "Светлая"}, {"id": "dark", "name": "Тёмная"}],
        "tokens": [
            C("warm-white", "#faf8f2", "#0a0a0d", "Фон страницы и постов. Основной цвет площади (около 60% макета)."),
            C("surface", "#ffffff", "#141418", "Карточки, окна браузера и телефона в макетах, плашки на warm-white."),
            C("sand", "#f0ede3", "#1d1d23", "Подложки, неактивные кнопки, плашки на warm-white."),
            C("ink", "#0b0b0f", "#f5f3ec", "Заголовки и текст на warm-white, surface и sand; тёмные плашки."),
            C("muted", "#5d5c66", "#a09ea8", "Второстепенный текст и подписи на warm-white и surface."),
            C("line", "#0b0b0f1a", "#ffffff1a", "Тонкие линии и рамки карточек."),
            C("cobalt", "#0047ff", "#2e66ff", "Главный фирменный цвет: круги, акцентное слово в заголовке, фон кейсов, синие кнопки. Как текст — на warm-white и surface."),
            C("cobalt-deep", "#0033c4", "#1a4ee6", "Тень и глубина внутри синей сферы, нажатое состояние синих кнопок."),
            C("cobalt-light", "#6e9bff", "#8fb2ff", "Блик на сфере и прогресс-полосы; не для текста."),
            C("acid", "#e7ff00", "#e7ff00", "Акцент: кнопки CTA, круги, стикеры, цифры на синем и чёрном. Никогда не текст на warm-white."),
            C("on-cobalt", "#ffffff", "#ffffff", "Текст и знак на cobalt."),
            C("on-acid", "#0b0b0f", "#0b0b0f", "Текст, иконки и стрелки на acid."),
        ],
    },
    "type": {
        "fonts": [
            {"family": "Unbounded", "file": "fonts/Unbounded-ExtraBold.ttf", "weight": "800"},
            {"family": "Inter Tight", "file": "fonts/InterTight-Regular.ttf", "weight": "400"},
            {"family": "Inter Tight", "file": "fonts/InterTight-Bold.ttf", "weight": "700"},
            {"family": "Inter Tight", "file": "fonts/InterTight-Black.ttf", "weight": "900"},
        ],
        "families": {
            "logo": "\"Unbounded\", \"Inter Tight\", sans-serif",
            "sans": "\"Inter Tight\", system-ui, sans-serif",
        },
        "groups": [
            {"name": "Логотип", "family": "logo", "styles": [
                {"name": "wordmark", "fontSize": "58px", "lineHeight": 1, "fontWeight": 800, "letterSpacing": "-0.06em", "sample": "mazzeru", "usage": "Только вордмарк и большие цифры-акценты. Всегда строчными."},
                {"name": "numeral", "fontSize": "92px", "lineHeight": 1, "fontWeight": 800, "letterSpacing": "-0.05em", "sample": "120+", "usage": "Крупные цифры в постах-результатах, цвет cobalt."},
            ]},
            {"name": "Заголовки", "family": "sans", "styles": [
                {"name": "display-xl", "fontSize": "140px", "lineHeight": 0.9, "fontWeight": 900, "letterSpacing": "-0.045em", "sample": "ИДЕИ В ДВИЖЕНИЕ", "usage": "Главный заголовок поста 1080 px, КАПСОМ, 2–4 слова, одно слово cobalt."},
                {"name": "display-l", "fontSize": "88px", "lineHeight": 0.95, "fontWeight": 900, "letterSpacing": "-0.035em", "sample": "НАШИ ПРОЕКТЫ", "usage": "Заголовки разделов на сайте и в карусели, КАПСОМ."},
                {"name": "heading", "fontSize": "34px", "lineHeight": 1, "fontWeight": 900, "letterSpacing": "-0.02em", "sample": "ЛЕНДИНГ КОФЕЙНИ", "usage": "Названия карточек, кейсов и пакетов, КАПСОМ."},
            ]},
            {"name": "Текст", "family": "sans", "styles": [
                {"name": "lead", "fontSize": "19px", "lineHeight": 1.55, "fontWeight": 400, "sample": "Генерируем ИИ-видео, снимаем Reels и запускаем сайты, которые продают.", "usage": "Подзаголовок под главным заголовком, цвет muted."},
                {"name": "body", "fontSize": "17px", "lineHeight": 1.55, "fontWeight": 400, "sample": "Первый черновик — за 48 часов.", "usage": "Основной текст."},
                {"name": "label", "fontSize": "12px", "lineHeight": 1, "fontWeight": 700, "letterSpacing": "0.32em", "sample": "ИИ-ВИДЕО / САЙТЫ / МОБИЛОГРАФИЯ", "usage": "Надзаголовки и подписи КАПСОМ с разрядкой; в постах 1080 px — 26 px."},
                {"name": "button", "fontSize": "12.5px", "lineHeight": 1, "fontWeight": 800, "letterSpacing": "0.2em", "sample": "ДАВАЙТЕ СОЗДАДИМ", "usage": "Текст кнопок-таблеток КАПСОМ."},
            ]},
        ],
    },
    "spacing": {"tokens": [
        {"name": "space-1", "value": "8px", "usage": "Между чипами и иконкой с текстом."},
        {"name": "space-2", "value": "16px", "usage": "Отступ между карточками, боковое поле на телефоне."},
        {"name": "space-3", "value": "24px", "usage": "Внутренний отступ карточек."},
        {"name": "space-4", "value": "32px", "usage": "Боковое поле на компьютере."},
        {"name": "space-6", "value": "48px", "usage": "Отступ между блоками внутри секции."},
        {"name": "space-safe", "value": "80px", "usage": "Безопасное поле в постах и сторис 1080 px."},
    ]},
    "radius": {"tokens": [
        {"name": "radius-sm", "value": "18px", "usage": "Медиа, фото, небольшие карточки."},
        {"name": "radius-md", "value": "28px", "usage": "Крупные карточки, панели, блок контактов."},
        {"name": "radius-mark", "value": "24%", "usage": "Скругление знака ZZ (24 при стороне 100)."},
        {"name": "radius-pill", "value": "999px", "usage": "Кнопки, чипы, фильтры, стикеры."},
    ]},
    "formats": {"note": "Размеры материалов для Instagram.", "tokens": [
        {"name": "ig-post", "value": "1080x1350", "usage": "Пост и карусель, 4:5."},
        {"name": "ig-story", "value": "1080x1920", "usage": "Сторис, Reels, обложки «Актуального», 9:16."},
        {"name": "ig-avatar", "value": "1080x1080", "usage": "Аватарка, обрезается в круг."},
    ]},
}
json.dump(tokens, open(os.path.join(D, "tokens.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)

# ---- ассеты ----
IDS = {
    "Logos": [
        ("mazzeru-logo-blue.svg", "6bf2ef62fe64b8adcfe18c682563d17c", 5593, "image/svg+xml"),
        ("mazzeru-logo-white.svg", "5a7f9e72c88f5b4af6f9f08c25e0af57", 5593, "image/svg+xml"),
        ("mazzeru-logo-black.svg", "f6ca81449eb21ea9c97565a414eb69b0", 5593, "image/svg+xml"),
        ("mazzeru-logo-tagline-blue.svg", "5c750a63ce869c3b310d5e1bfe3f8273", 16254, "image/svg+xml"),
        ("mazzeru-logo-on-blue.svg", "ba0e31701f3180b659cd17a49d3c9497", 5742, "image/svg+xml"),
        ("mazzeru-logo-on-yellow.svg", "4aa0c59eee3f7c8b2a471ed65a5e6918", 5742, "image/svg+xml"),
        ("mazzeru-logo-on-white.svg", "5c33243801481b81740a04d0e205117e", 5742, "image/svg+xml"),
        ("mazzeru-wordmark-blue.svg", "21f08a55f64d089420601825c677b8b1", 5279, "image/svg+xml"),
        ("mazzeru-wordmark-black.svg", "b9adbe9f75125e8cbd3992874e3b14d2", 5279, "image/svg+xml"),
        ("mazzeru-wordmark-white.svg", "ea4cc579659a6a15568779d73eed52bd", 5279, "image/svg+xml"),
        ("mazzeru-wordmark-yellow.svg", "d93e79337bb4dea2910a10b32cbbfec5", 5279, "image/svg+xml"),
        ("mazzeru-logo-blue.png", "5a13e94c6636a06ceb44c8ebd4479a09", 35108, "image/png"),
        ("mazzeru-logo-on-blue.png", "4dfc0e78027d4090f753b7ac395d3c10", 34186, "image/png"),
        ("mazzeru-wordmark-blue.png", "38efbd7df5739c0abd3e814616d54fc3", 34246, "image/png"),
    ],
    "Mark": [
        ("mazzeru-mark-blue.svg", "e60666b0cd0a29931cb5b9217a721aaf", 335, "image/svg+xml"),
        ("mazzeru-mark-white.svg", "8838881ac26af4342d91ba9b44cb0ce3", 335, "image/svg+xml"),
        ("mazzeru-mark-yellow.svg", "731a5e6713316f9e2a71350117c1897b", 335, "image/svg+xml"),
        ("mazzeru-mark-black.svg", "3b0ad6a1d6593513404c3429b62d5b5f", 335, "image/svg+xml"),
        ("mazzeru-mark-blue.png", "a9357e8ee9dc2ebd7fc08b1adf7fb1b0", 25798, "image/png"),
        ("mazzeru-mark-white.png", "78a371edc21c380b659dc678aab6d2c5", 24701, "image/png"),
    ],
    "Instagram": [
        ("ig-avatar.png", "396bc3af6f28678becd1309ec8b655d7", 15575, "image/png"),
        ("post-1-headline.png", "6aa9c563d883643045ce460fc410e168", 81228, "image/png"),
        ("post-2-case.png", "dc40f06c52e121f1608946b02fbd953a", 326627, "image/png"),
        ("post-3-tips.png", "1af11f4744a4bedcb7685a1c41f1e78a", 71160, "image/png"),
        ("story-template.png", "1e80cab1c20e10374c3aa32c7b6b2349", 1261931, "image/png"),
    ],
    "Highlights": [
        ("highlight-ai.png", "76f677c18b6cce496d95c9b28c038485", 18260, "image/png"),
        ("highlight-web.png", "acf34f0b72321b9e3d1778146b5b52f2", 18978, "image/png"),
        ("highlight-mobile.png", "7433a7ed41102f91d79e871c3cbfecda", 21648, "image/png"),
        ("highlight-price.png", "19e4bf25a5bca17fd60da57cb149319a", 15157, "image/png"),
        ("highlight-team.png", "5ed2fe32cf688b0ae17c50fcc3bf1daa", 26305, "image/png"),
        ("highlight-reviews.png", "00b1f2696b0a27cfd7e2d20ca336e26e", 15229, "image/png"),
    ],
}
TILES = {"Logos": "l", "Mark": "s", "Instagram": "m", "Highlights": "s"}
READMES = {
    "Logos": """# Логотипы

Все файлы в кривых (шрифт не нужен). PNG — 2400 px в ширину, прозрачный фон.

- `mazzeru-logo-blue` — основная версия: синий знак + синий вордмарк, для светлого фона `warm-white` / белого.
- `mazzeru-logo-white` — белый знак с синей Z + белый вордмарк, для синего и тёмного фона.
- `mazzeru-logo-black` — чёрный знак с жёлтой Z + чёрный вордмарк, для жёлтого фона и печати в одну краску.
- `mazzeru-logo-tagline-blue` — с подписью AI VIDEO / WEB / MOBILE FILM.
- `mazzeru-logo-on-blue`, `-on-yellow`, `-on-white` — логотип уже на фирменном фоне с полями (для обложек, шапок, превью).
- `mazzeru-wordmark-*` — только слово mazzeru в четырёх цветах (синий, чёрный, белый, жёлтый). Жёлтый — только на синем или чёрном.
""",
    "Mark": """# Знак ZZ

Для аватарок, иконок приложения, водяного знака на видео и мест меньше 120 px. PNG — 1024 × 1024.

- `mazzeru-mark-blue` — основной: синий квадрат, белая Z.
- `mazzeru-mark-white` — белый квадрат, синяя Z (на синем фоне).
- `mazzeru-mark-yellow` — жёлтый квадрат, чёрная Z.
- `mazzeru-mark-black` — чёрный квадрат, жёлтая Z.
""",
    "Instagram": """# Instagram

Готовые примеры в фирменном стиле, 1080 px. Правила — в разделе «Instagram».

- `ig-avatar` — аватарка профиля 1080 × 1080 (Instagram обрежет в круг).
- `post-1-headline` — пост-заголовок / анонс, 1080 × 1350.
- `post-2-case` — пост-кейс на синем фоне, 1080 × 1350.
- `post-3-tips` — первый слайд карусели-совета на жёлтом, 1080 × 1350.
- `story-template` — сторис 1080 × 1920.
""",
    "Highlights": """# Обложки «Актуального»

1080 × 1920, иконка по центру. Порядок в профиле: ИИ, Сайты, Мобило, Цены, Команда, Отзывы.

- `highlight-ai` — синий фон, жёлтая звезда.
- `highlight-web` — чёрный фон, жёлтое окно браузера.
- `highlight-mobile` — жёлтый фон, синий телефон.
- `highlight-price` — синий фон, белый ценник.
- `highlight-team` — светлый фон, синие люди.
- `highlight-reviews` — жёлтый фон, чёрный отзыв.
""",
}
assetGroups, groups = {}, []
for g, items in IDS.items():
    groups.append(g)
    assetGroups[g] = {"name": g, "tile": TILES[g], "order": [n for n, *_ in items],
                      "files": {n: {"name": n, "blob": i, "size": s, "type": t} for n, i, s, t in items}}
    os.makedirs(os.path.join(D, "assets", g), exist_ok=True)
    open(os.path.join(D, "assets", g, "README.md"), "w", encoding="utf-8").write(READMES[g])

now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
index = {"v": 3, "layout": "files", "createdOnFiles": {"v": 1, "at": now}, "title": "Mazzeru", "namespace": "Mazzeru",
         "libraries": [], "sections": {}, "groups": groups, "assetGroups": assetGroups, "blobs": {},
         "docs": {"readme": "project/README.md", "sections": []},
         "lastChange": {"by": "Claude", "at": now, "via": "Claude Code", "note": "Брендбук Mazzeru: логотипы, цвета, шрифты, шаблоны Instagram"}}
json.dump(index, open(os.path.join(D, "design-system.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)

# ---- обложка ----
os.makedirs(os.path.join(D, "components", "Cover"), exist_ok=True)
open(os.path.join(D, "components", "Cover", "preview.html"), "w", encoding="utf-8").write("""<!-- @dsCard height=300 -->
<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<title>Mazzeru</title>
<style>
  html, body { margin:0; height:100%; }
  body { background:var(--warm-white); color:var(--ink); font-family:var(--font-sans); overflow:hidden; }
  .cover { position:relative; height:300px; overflow:hidden; }
  .art { position:absolute; top:0; left:480px; width:480px; height:300px; overflow:hidden; }
  .art svg { display:block; width:480px; height:300px; }
  .cobalt { fill:var(--cobalt); }
  .acid { fill:var(--acid); }
  .ink { fill:var(--ink); }
  .ground { fill:var(--warm-white); }
  .slash { stroke:var(--acid); stroke-width:16px; stroke-linecap:round; fill:none; }
  .words { position:absolute; left:var(--space-6); bottom:var(--space-6); max-width:440px; }
  .name { margin:0; font-family:var(--font-logo); font-weight:800; font-size:80px; line-height:.95; letter-spacing:-0.06em; color:var(--cobalt); }
  .tag { margin:var(--space-2) 0 0 4px; font-size:14px; line-height:20px; color:var(--muted); }
</style>
</head>
<body>
<div class="cover">
<div class="art" aria-hidden="true">
<svg viewBox="0 0 480 300" width="480" height="300">
<!--
  blocks      cobalt disc 360 (the brand's big circle, bleeding off the top-right) · acid disc 200 bleeding off the bottom · ink pill 144×48 (radius-pill) — about 40% of 960×300
  arrangement one large cobalt circle with an acid satellite and an ink pill, as in the site hero and posts
  pattern     the ZZ slash: three acid diagonals at a space-4 pitch cut across the cobalt disc, from the mark's parallel stroke ("круги" + знак ZZ)
  scales      pitch space-4 (32px); pill rx radius-pill (half of 48); discs from the circle motif; stroke 16px = space-2
-->
<circle class="cobalt" cx="330" cy="110" r="180"/>
<circle class="acid" cx="130" cy="300" r="100"/>
<rect class="ink" x="40" y="40" width="144" height="48" rx="24"/>
<path class="slash" d="M380 60 L270 170"/>
<path class="slash" d="M412 92 L302 202"/>
<path class="slash" d="M444 124 L360 208"/>
</svg>
</div>
<div class="words">
  <h1 class="name">Mazzeru</h1>
  <p class="tag">ИИ-видео, сайты и мобилография из Астаны.</p>
</div>
</div>
</body>
</html>
""")
print("ok", now)
