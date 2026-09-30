import os, json
os.chdir(r"C:\Users\USER\OneDrive\Desktop\Mazzeru")

D = {}


def reg(key, ru, kz, en):
    v = {"ru": ru, "kz": kz, "en": en}
    if key in D and D[key] != v:
        raise SystemExit(f"conflict {key}: {D[key]} vs {v}")
    D[key] = v
    return ru


def T(key, ru, kz, en):
    return f'data-i18n="{key}">{reg(key, ru, kz, en)}'


def t(key, tri):
    return T(key, *tri)


# ---------------------------------------------------------------- интерфейс
UI = {
    "ui.all": ("Все", "Барлығы", "All"),
    "ui.openSite": ("Открыть сайт", "Сайтты ашу", "Visit site"),
    "ui.allWorks": ("Все работы", "Барлық жұмыстар", "All work"),
    "ui.empty": ("Скоро здесь появятся проекты", "Жобалар жақында пайда болады", "Projects coming soon"),
    "ui.popular": ("★ Популярный", "★ Танымал", "★ Popular"),
    "ui.package": ("Пакет", "Пакет", "Package"),
    "ui.choose": ("Выбрать", "Таңдау", "Choose"),
    "ui.waHello": ("Здравствуйте! Хочу обсудить проект", "Сәлеметсіз бе! Жобаны талқылағым келеді", "Hello! I’d like to discuss a project"),
    "ui.waPackage": ("Здравствуйте! Интересует пакет «{name}»", "Сәлеметсіз бе! «{name}» пакеті қызықтырады", "Hello! I’m interested in the “{name}” package"),
    "ui.videoSoon": ("видео скоро", "видео жақында", "video coming soon"),
    "ui.watch": ("смотреть", "көру", "watch"),
    "ui.open": ("открыть", "ашу", "open"),
    "ui.close": ("Закрыть", "Жабу", "Close"),
    "ui.theme": ("Сменить тему", "Тақырыпты ауыстыру", "Toggle theme"),
    "ui.menu": ("Меню", "Мәзір", "Menu"),
    "ui.skip": ("Пропустить", "Өткізу", "Skip"),
    "ui.contactsTag": ("Контакты", "Байланыс", "Contacts"),
    "ui.contactsH2": ("Обсудим <em>ваш проект?</em>", "<em>Жобаңызды</em> талқылайық па?", "Let’s discuss <em>your project</em>"),
    "ui.contactsP": ("Ответим в течение 15 минут в рабочее время. Первая консультация — бесплатно.",
                     "Жұмыс уақытында 15 минут ішінде жауап береміз. Алғашқы кеңес — тегін.",
                     "We reply within 15 minutes during working hours. The first consultation is free."),
    "tag.strategy": ("Стратегия", "Стратегия", "Strategy"),
    "tag.design": ("Дизайн", "Дизайн", "Design"),
}
for k, v in UI.items():
    reg(k, *v)

NAV = {
    "home": ("Главная", "Басты бет", "Home"),
    "ai": ("ИИ контент", "ИИ контент", "AI content"),
    "web": ("Сайты", "Сайттар", "Websites"),
    "mobile": ("Мобилография", "Мобилография", "Mobilography"),
    "contacts": ("Контакты", "Байланыс", "Contacts"),
}
for k, v in NAV.items():
    reg("nav." + k, *v)

LBL = {
    "services": ("Услуги", "Қызметтер", "Services"),
    "work": ("Портфолио", "Портфолио", "Portfolio"),
    "why": ("Почему мы", "Неге біз", "Why us"),
    "team": ("Команда", "Команда", "Team"),
    "faq": ("Вопросы", "Сұрақтар", "FAQ"),
    "process": ("Процесс", "Процесс", "Process"),
    "prices": ("Цены", "Бағалар", "Pricing"),
    "numbers": ("В цифрах", "Сандармен", "In numbers"),
}
for k, v in LBL.items():
    reg("lbl." + k, *v)

reg("hdr.cta", "Обсудить проект", "Жобаны талқылау", "Let’s talk")
reg("hero.create", "Давайте создадим", "Бірге жасайық", "Let’s create")
reg("hero.works", "Смотреть работы", "Жұмыстарды көру", "See our work")
reg("hero.prices", "Смотреть цены", "Бағаларды көру", "See pricing")
reg("cta.btn", "Написать нам", "Бізге жазу", "Message us")
reg("faq.h", "Частые вопросы", "Жиі қойылатын сұрақтар", "FAQ")
reg("faq.note", "Не нашли ответ? Напишите — ответим за 15 минут.", "Жауап таппадыңыз ба? Жазыңыз — 15 минутта жауап береміз.", "Didn’t find an answer? Message us — we reply within 15 minutes.")
reg("prices.h", "Пакеты и стоимость", "Пакеттер мен бағалар", "Packages & pricing")
reg("prices.note", "Точная цена — после брифа. Пакеты можно комбинировать.", "Нақты баға — брифтен кейін. Пакеттерді біріктіруге болады.", "Exact price after the brief. Packages can be combined.")
reg("steps.h", "Как мы работаем", "Біз қалай жұмыс істейміз", "How we work")
reg("hint.click", "Нажмите на карточку, чтобы открыть", "Ашу үшін карточканы басыңыз", "Click a card to open it")

META = {
    "home": (("Mazzeru — ИИ контент, мобилография и сайты", "Mazzeru — ИИ контент, мобилография және сайттар", "Mazzeru — AI content, mobilography and websites"),
             ("Digital-студия из Астаны: ИИ-видео и love story, мобилография и Reels, разработка сайтов и лендингов.",
              "Астанадағы digital-студия: ИИ-видео және love story, мобилография және Reels, сайттар мен лендингтер әзірлеу.",
              "Digital studio from Astana: AI videos and love stories, mobile videography and Reels, website and landing page development.")),
    "ai": (("ИИ контент и Love Story — Mazzeru", "ИИ контент және Love Story — Mazzeru", "AI content & Love Story — Mazzeru"),
           ("ИИ-видео на заказ: love story по вашим фото, рекламные ролики, ИИ-аватары и клипы. Астана, Казахстан.",
            "Тапсырыс бойынша ИИ-видео: фотоларыңыз бойынша love story, жарнамалық роликтер, ИИ-аватарлар және клиптер. Астана, Қазақстан.",
            "Custom AI videos: love stories from your photos, ads, AI avatars and music videos. Astana, Kazakhstan.")),
    "mobile": (("Мобилография и Reels — Mazzeru", "Мобилография және Reels — Mazzeru", "Mobilography & Reels — Mazzeru"),
               ("Мобилография в Астане: съёмка Reels на iPhone, монтаж, цветокоррекция, контент для бизнеса и событий.",
                "Астанадағы мобилография: iPhone-ға Reels түсіру, монтаж, түс түзету, бизнес пен іс-шараларға контент.",
                "Mobile videography in Astana: iPhone Reels, editing, color grading, content for businesses and events.")),
    "web": (("Разработка сайтов и лендингов — Mazzeru", "Сайттар мен лендингтер әзірлеу — Mazzeru", "Websites & landing pages — Mazzeru"),
            ("Создание сайтов и лендингов под ключ в Казахстане: дизайн, разработка, анимации, интеграция с Kaspi и WhatsApp.",
             "Қазақстанда сайттар мен лендингтерді кілтін қолға жасау: дизайн, әзірлеу, анимациялар, Kaspi және WhatsApp интеграциясы.",
             "Turnkey websites and landing pages in Kazakhstan: design, development, animations, Kaspi and WhatsApp integration.")),
}
for p, (ti, de) in META.items():
    reg(f"meta.{p}.title", *ti)
    reg(f"meta.{p}.desc", *de)

PAGES = {"home": "index.html", "ai": "ai-content.html", "mobile": "mobilography.html", "web": "websites.html"}

# ---------------------------------------------------------------- логотип
MARK = ('<svg class="{cls}" viewBox="45 45 1160 1160" aria-hidden="true">'
        '<circle class="mk-bg" cx="625" cy="625" r="580"/>'
        '<path class="mk-z mk-z1" d="M365 491 L681 491 L603 573 L285 573Z M447 587 L587 587 L443 697 L607 697 L521 783 L222 783 L292 710 L320 686Z"/>'
        '<path class="mk-z mk-z2" d="M729 491 L1036 491 L965 566 L940 588 L797 697 L993 697 L889 783 L561 783 L630 716 L648 700 L808 573 L649 573Z"/></svg>')

ICONS = {
    "arrow": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
}
ARR = f'<span class="arr">{ICONS["arrow"]}</span>'


def head(key):
    ti, de = META[key]
    return f'''<!doctype html>
<html lang="ru">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{ti[0]}</title>
  <meta name="description" content="{de[0]}">
  <meta property="og:title" content="{ti[0]}">
  <meta property="og:description" content="{de[0]}">
  <meta property="og:image" content="assets/img/og.png">
  <meta name="theme-color" content="#0047ff">
  <link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter+Tight:wght@400;500;600;700;800;900&family=Unbounded:wght@700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="assets/css/style.css">
  <script>try{{var d=document.documentElement,t=localStorage.getItem("theme");if(t)d.dataset.theme=t;var q=new URLSearchParams(location.search).get("lang")||localStorage.getItem("lang");if(q)d.lang=q==="kz"?"kk":q;if(sessionStorage.getItem("intro")||/[?&]nointro/.test(location.search)||matchMedia("(prefers-reduced-motion: reduce)").matches)d.classList.add("intro-seen");if(sessionStorage.getItem("wipe")==="1")d.classList.add("wiping")}}catch(e){{}}</script>
</head>
<body data-page="{key}">
  <!-- Интро: ZZ-знак и логотип -->
  <div class="intro" aria-hidden="true">
    <div class="intro-slash"></div>
    <div class="intro-stage">
      {MARK.format(cls="intro-mark")}
      <div class="intro-word">{"".join(f"<span>{c}</span>" for c in "mazzeru")}</div>
    </div>
    <span class="intro-tag label">AI VIDEO / WEB / MOBILE FILM</span>
  </div>
  <div class="wipe" aria-hidden="true">{MARK.format(cls="")}</div>
  <div class="progress" aria-hidden="true"></div>
  <div class="cursor" aria-hidden="true"></div>
'''


def header(key):
    order = ["ai", "web", "mobile"]
    links = "\n".join(f'        <a href="{PAGES[p]}"{" class=\"active\"" if p == key else ""} data-i18n="nav.{p}">{NAV[p][0]}</a>' for p in order)
    mlinks = "\n".join(f'      <a href="{PAGES[p]}"{" class=\"active\"" if p == key else ""} data-i18n="nav.{p}">{NAV[p][0]}</a>' for p in ["home"] + order)
    return f'''
  <header class="header">
    <div class="wrap">
      <a class="logo" href="index.html" aria-label="Mazzeru">{MARK.format(cls="mark")}<span class="wordmark">mazzeru</span></a>
      <nav class="nav" aria-label="Menu">
{links}
      </nav>
      <div class="header-actions">
        <div class="lang" role="group" aria-label="Language">
          <button type="button" data-lang="kz">KZ</button><button type="button" data-lang="ru">RU</button><button type="button" data-lang="en">ENG</button>
        </div>
        <button class="icon-btn" type="button" data-theme-toggle data-i18n-aria="ui.theme" aria-label="Сменить тему">
          <svg class="theme-moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M20 14.5A8 8 0 0 1 9.5 4 8 8 0 1 0 20 14.5z"/></svg>
          <svg class="theme-sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>
        </button>
        <a class="btn btn--sm" href="#contacts" data-magnetic><span data-i18n="hdr.cta">Обсудить проект</span>{ARR}</a>
        <button class="burger" type="button" data-burger data-i18n-aria="ui.menu" aria-label="Меню" aria-expanded="false"><i></i></button>
      </div>
    </div>
  </header>

  <div class="mmenu" id="mmenu">
    <nav>
{mlinks}
      <a href="#contacts" data-close-menu data-i18n="nav.contacts">Контакты</a>
    </nav>
    <div class="mmenu-row">
      <div class="lang" role="group" aria-label="Language">
        <button type="button" data-lang="kz">KZ</button><button type="button" data-lang="ru">RU</button><button type="button" data-lang="en">ENG</button>
      </div>
      <a class="btn btn--sm" href="#" data-wa><span data-i18n="cta.btn">Написать нам</span>{ARR}</a>
    </div>
  </div>

  <main>'''


FOOTER_SCRIPTS = '''
  <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js" defer></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js" defer></script>
  <script src="assets/js/i18n.js" defer></script>
  <script src="assets/js/data.js" defer></script>
  <script src="assets/js/main.js" defer></script>
</body>
</html>
'''


def contact():
    return '''
  </main>

  <footer class="contact" id="contacts" data-contacts></footer>
''' + FOOTER_SCRIPTS


def hero(p, eyebrow, h1, tag, lead, visual, second):
    return f'''
    <section class="hero">
      <div class="wrap">
        <div class="hero-text">
          {eyebrow_html(p, eyebrow)}
          <h1 data-lines {t(p + ".h1", h1)}</h1>
          <p class="hero-tag label label--muted" {t(p + ".tagline", tag)}</p>
          <p class="hero-lead" {t(p + ".lead", lead)}</p>
          <div class="hero-actions">
            <a class="btn" href="#" data-wa data-magnetic><span data-i18n="hero.create">Давайте создадим</span>{ARR}</a>
            <a class="link-arrow" href="{second[0]}"><span data-i18n="{second[1]}">{D[second[1]]["ru"]}</span>{ICONS["arrow"]}</a>
          </div>
        </div>
        <div class="hero-visual hero-visual--{p}" data-parallax>
{visual}
        </div>
      </div>
    </section>
'''


def eyebrow_html(p, city):
    if p == "home":
        return (f'<span class="hero-eyebrow"><span class="mini">{MARK.format(cls="")}</span>'
                f'<span {t("home.city", city)}</span><span class="sep"></span><span class="clock" data-clock>--:--</span></span>')
    return (f'<nav class="hero-eyebrow crumbs" aria-label="breadcrumbs"><a href="index.html" data-i18n="nav.home">Главная</a>'
            f'<span class="sep"></span><span data-i18n="nav.{p}">{NAV[p][0]}</span></nav>')


SPARK = '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2l2.2 6.3L21 10l-6.8 1.9L12 18l-2.2-6.1L3 10l6.8-1.7z"/></svg>'
PLAY = '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M7 4.5v15a1 1 0 0 0 1.5.86l12-7.5a1 1 0 0 0 0-1.72l-12-7.5A1 1 0 0 0 7 4.5z"/></svg>'


def visual(kind, browser_img=None, phone_img=None):
    reg("vis.promptH", "ИИ · промпт", "ИИ · промпт", "AI · prompt")
    reg("vis.prompt", "Love story пары, горы на закате, плёночный цвет, 4K", "Жұптың love story-і, күн батқандағы таулар, плёнка түсі, 4K", "Couple love story, mountains at sunset, film look, 4K")
    reg("vis.gen", "Генерация", "Генерация", "Generating")
    circle = f'''          <div class="hero-sun"></div>
          <div class="hero-circle">
            <span class="ring r1"></span><span class="ring r2"></span><span class="ring r3"></span>
            <svg class="ring-text" viewBox="0 0 200 200" aria-hidden="true"><defs><path id="rt-{kind}" d="M100,100 m-84,0 a84,84 0 1,1 168,0 a84,84 0 1,1 -168,0"/></defs><text><textPath href="#rt-{kind}">AI VIDEO • WEB • MOBILE FILM • AI VIDEO • WEB • MOBILE FILM •</textPath></text></svg>
            <div class="core">{MARK.format(cls="")}</div>
          </div>
'''
    prompt = f'''          <div class="vis vis-prompt">
            <div class="vp-head"><span class="vp-ico">{SPARK}</span><span data-i18n="vis.promptH">ИИ · промпт</span><span class="vp-live"></span></div>
            <p class="vp-text"><span data-type="vis.prompt"></span><i class="caret"></i></p>
            <div class="vp-bar"><i data-bar></i></div>
            <div class="vp-foot"><span data-i18n="vis.gen">Генерация</span><b data-pct>0%</b></div>
            <div class="vp-frames"><i></i><i></i><i></i><i></i></div>
          </div>
'''
    screen = f'<img src="{phone_img}" alt="">' if phone_img else '<div class="ph-footage"></div>'
    phone = f'''          <div class="vis vis-phone">
            <div class="ph-screen">{screen}
              <div class="ph-top"><span class="rec"><i></i>REC</span><span data-timecode>00:00</span></div>
              <span class="ph-play">{PLAY}</span>
              <div class="ph-bottom"><b>Reels</b><span class="ph-like">♥ <em data-likes>1.2K</em></span></div>
              <div class="ph-prog"><i></i></div>
            </div>
          </div>
'''
    body = f'<img src="{browser_img}" alt="">' if browser_img else '<div class="sk"><b class="sk-nav"></b><b class="sk-h"></b><b class="sk-h short"></b><b class="sk-l"></b><b class="sk-l short"></b><b class="sk-btn"></b></div><div class="sk-img"></div>'
    browser = f'''          <div class="vis vis-browser">
            <div class="browser-bar"><i></i><i></i><i></i><span class="url">mazzeru.kz</span></div>
            <div class="vb-body">{body}</div>
          </div>
'''
    parts = {"home": prompt + phone + browser, "ai": prompt + phone, "mobile": phone + prompt, "web": browser + phone}[kind]
    return f'<!--visual-{kind}-->' + circle + parts


def visual_photo(src, alt, badges, extra=""):
    b = "\n".join(f'          <span class="hero-badge b{i + 1}"><b></b>{x}</span>' for i, x in enumerate(badges))
    return f'''          <div class="hero-sun"></div>
          <div class="hero-circle"><img src="{src}" alt="{alt}" fetchpriority="high"></div>
{extra}          <div class="hero-mark">{MARK.format(cls="")}</div>
{b}'''


def bands(p, words):
    reg("mq." + p, *words)
    return f'''
    <div class="bands" aria-hidden="true">
      <div class="band band--yellow" data-marquee="mq.{p}"></div>
      <div class="band band--blue" data-marquee="mq.{p}"></div>
    </div>
'''


def sec_head(label_key, h2_key, h2, note=None):
    n = f'<p class="sec-note" {t(note[0], note[1:])}</p>' if note else ""
    if h2_key in D:
        h2html = f'<h2 class="h2" data-i18n="{h2_key}">{D[h2_key]["ru"]}</h2>'
    else:
        h2html = f'<h2 class="h2" {t(h2_key, h2)}</h2>'
    return f'''<div class="sec-head" data-reveal>
          <div><span class="label" data-i18n="{label_key}">{D[label_key]["ru"]}</span>{h2html}</div>
          {n}
        </div>'''


def stats(p, items):
    out = []
    for n, (num, suf, lbl) in enumerate(items):
        s = f' data-suffix="{suf}"' if suf else ""
        out.append(f'          <div class="stat"><b data-count="{num}"{s}>0</b><span {t(f"{p}.stat{n}", lbl)}</span></div>')
    return '''
    <section class="section section--tight">
      <div class="wrap">
        <div class="stats" data-reveal>
''' + "\n".join(out) + '''
        </div>
      </div>
    </section>
'''


def duo(p, t1, l1, t2, l2, lab1, lab2):
    li = lambda key, xs: "\n".join(f'              <li {t(f"{key}.{i}", x)}</li>' for i, x in enumerate(xs))
    return f'''
    <section class="section">
      <div class="wrap duo">
        <div class="panel panel--blue" data-reveal>
          <span class="label" {t(p + ".c1lbl", lab1)}</span>
          <h3 {t(p + ".c1", t1)}</h3>
          <ul class="bullets">
{li(p + ".c1", l1)}
          </ul>
        </div>
        <div class="panel panel--ink" data-reveal>
          <span class="label" {t(p + ".c2lbl", lab2)}</span>
          <h3 {t(p + ".c2", t2)}</h3>
          <ul class="bullets">
{li(p + ".c2", l2)}
          </ul>
        </div>
      </div>
    </section>
'''


def steps(p, items):
    rows = "\n".join(f'          <div class="step" data-reveal><div><b {t(f"{p}.step{i}", a)}</b><span {t(f"{p}.step{i}d", b)}</span></div></div>' for i, (a, b) in enumerate(items))
    return f'''
    <section class="section section--tight" id="process">
      <div class="wrap">
        {sec_head("lbl.process", "steps.h", None)}
        <div class="steps">
{rows}
        </div>
      </div>
    </section>
'''


def portfolio(p, cat, layout, h2, filters=False, hint=True):
    note = ("hint.click",) + tuple(D["hint.click"].values()) if hint else None
    head_html = sec_head("lbl.work", p + ".portH", h2, note)
    if filters:
        head_html = head_html.replace("\n          \n        </div>", '\n          <div class="filters" data-filters></div>\n        </div>')
    return f'''
    <section class="section" id="work">
      <div class="wrap">
        {head_html}
        {orbit_html(cat) if layout == "orbit" else f'<div data-projects="{cat}" data-layout="{layout}"></div>'}
      </div>
    </section>
'''


def orbit_html(cat):
    reg("orbit.projects", "проектов", "жоба", "projects")
    reg("orbit.hint", "Наведите курсор или нажмите на проект", "Жобаға курсорды апарыңыз немесе басыңыз", "Hover or tap a project")
    return f'''<div class="orbit" data-orbit="{cat}">
          <div class="orbit-sphere"><span class="os-ring"></span><span class="os-ring os-ring--2"></span><div class="os-ball">{MARK.format(cls="")}<b data-orbit-count>0</b><span data-i18n="orbit.projects">проектов</span></div></div>
          <div class="orbit-info" aria-live="polite"></div>
          <p class="orbit-hint" data-i18n="orbit.hint">Наведите курсор или нажмите на проект</p>
        </div>'''


def tail(k):
    return f'''
    <section class="section" id="prices">
      <div class="wrap">
        {sec_head("lbl.prices", "prices.h", None, ("prices.note",) + tuple(D["prices.note"].values()))}
        <div class="packages" data-packages="{k}"></div>
      </div>
    </section>
''' + faq(k)


def faq(k):
    return f'''
    <section class="section section--tight">
      <div class="wrap faq-grid">
        <div data-reveal>
          <span class="label" data-i18n="lbl.faq" style="color:var(--blue);display:block;margin-bottom:18px">Вопросы</span>
          <h2 class="h2" data-i18n="faq.h">Частые вопросы</h2>
          <p class="sec-note" data-i18n="faq.note" style="margin:22px 0 28px">{D["faq.note"]["ru"]}</p>
          <a class="btn btn--blue" href="#" data-wa data-magnetic><span data-i18n="cta.btn">Написать нам</span>{ARR}</a>
        </div>
        <div class="faq" data-faq="{k}"></div>
      </div>
    </section>
'''


def write(key, body):
    open(PAGES[key], "w", encoding="utf-8").write(head(key) + header(key) + body + contact())


ICON_SVG = {
    "ai": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3l1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10l5.2-1.8z"/><path d="M19 15l.8 2.2L22 18l-2.2.8L19 21l-.8-2.2L16 18l2.2-.8z"/></svg>',
    "web": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><rect x="2.5" y="4" width="19" height="16" rx="2.5"/><path d="M2.5 9h19M9 14l-2 1.5L9 17M15 14l2 1.5-2 1.5"/></svg>',
    "mobile": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><rect x="6" y="2.5" width="12" height="19" rx="3"/><circle cx="12" cy="9" r="2.6"/><path d="M10.5 18h3"/></svg>',
}

# ================================================================== ГЛАВНАЯ
dirs = [("ai", "01", ("Love story, реклама, ИИ-аватары и клипы — без съёмочной группы.", "Love story, жарнама, ИИ-аватарлар мен клиптер — түсірілім тобынсыз.", "Love stories, ads, AI avatars and music videos — no film crew.")),
        ("web", "02", ("Лендинги, корпоративные сайты и сайты мероприятий на трёх языках.", "Үш тілдегі лендингтер, корпоративтік сайттар және іс-шара сайттары.", "Landing pages, corporate and event websites in three languages.")),
        ("mobile", "03", ("Reels, контент-дни и события — снято на iPhone с кино-цветокором.", "Reels, контент-күндер және іс-шаралар — iPhone-ға кино-түс түзетумен.", "Reels, content days and events — shot on iPhone with cinematic grading."))]
dir_html = "\n".join(f'''          <a class="dir dir--{c}" href="{PAGES[c]}" data-reveal>
            <div class="dir-orb"></div><div class="dir-icon">{ICON_SVG[c]}</div>
            <div class="dir-top"><span class="dir-num">{num} /</span><span class="dir-go">{ICONS["arrow"]}</span></div>
            <div><h3 data-i18n="nav.{c}">{NAV[c][0]}</h3><p {t("home.dir." + c, desc)}</p></div>
          </a>''' for c, num, desc in dirs)

checks = [("clock", ("Быстро", "Жылдам", "Fast"), ("Первый черновик — за 48 часов", "Алғашқы нобай — 48 сағатта", "First draft in 48 hours")),
          ("layers", ("Под ключ", "Кілтін қолға", "Turnkey"), ("Контент, сайт и упаковка — одна команда", "Контент, сайт және қаптама — бір команда", "Content, website and packaging — one team")),
          ("shield", ("Прозрачно", "Ашық", "Transparent"), ("Договор, фиксированная цена и сроки", "Келісімшарт, тіркелген баға мен мерзім", "Contract, fixed price and deadlines")),
          ("chat", ("На связи", "Байланыста", "In touch"), ("Отдельный чат проекта и отчёты по этапам", "Жобаның жеке чаты және кезеңдер бойынша есептер", "A dedicated project chat and stage reports"))]
check_html = "\n".join(f'          <li data-reveal><span data-icon="{ic}"></span><div><b {t(f"home.why{i}", a)}</b><span {t(f"home.why{i}d", b)}</span></div></li>' for i, (ic, a, b) in enumerate(checks))

write("home",
      hero("home", ("Астана, Казахстан", "Астана, Қазақстан", "Astana, Kazakhstan"),
           ("Идеи<br>в&nbsp;<em>движение</em>", "Идеяны<br><em>қозғалысқа</em>", "Ideas<br>into <em>motion</em>"),
           ("ИИ-видео / Сайты / Мобилография", "ИИ-видео / Сайттар / Мобилография", "AI video / Web / Mobile film"),
           ("Команда из Астаны: генерируем ИИ-видео и love story, снимаем Reels на телефон и запускаем сайты, которые продают.",
            "Астанадағы команда: ИИ-видео мен love story генерациялаймыз, телефонға Reels түсіреміз және сататын сайттарды іске қосамыз.",
            "A team from Astana: we generate AI videos and love stories, shoot Reels on a phone and launch websites that sell."),
           visual("home"),
           ("#work", "hero.works"))
      + bands("home", ("ИИ-видео|Love Story|Сайты|Лендинги|Мобилография|Reels|Цветокор|ИИ-аватары",
                       "ИИ-видео|Love Story|Сайттар|Лендингтер|Мобилография|Reels|Түс түзету|ИИ-аватарлар",
                       "AI video|Love Story|Websites|Landing pages|Mobile film|Reels|Color grading|AI avatars"))
      + f'''
    <section class="section" id="services">
      <div class="wrap">
        {sec_head("lbl.services", "home.dirs", ("Три направления", "Үш бағыт", "Three directions"), ("home.dirsNote", "Одна команда закрывает контент, съёмку и сайт — в едином стиле.", "Бір команда контентті, түсірілімді және сайтты бірыңғай стильде жасайды.", "One team covers content, shooting and the website — in one consistent style."))}
        <div class="dirs">
{dir_html}
        </div>
      </div>
    </section>
'''
      + stats("home", [(120, "+", ("проектов", "жоба", "projects")), (4, "", ("основателя", "негізін қалаушы", "founders")),
                       (3, "", ("языка", "тіл", "languages")), (48, "ч", ("до первого черновика", "алғашқы нобайға дейін", "to the first draft"))])
      + portfolio("home", "all", "orbit", ("Наши проекты", "Біздің жобалар", "Our projects"), filters=True, hint=False)
      + duo("home", ("Наша цель", "Біздің мақсат", "Our goal"),
            [('<b>Сделать премиальный контент доступным</b> — для малого бизнеса и частных клиентов', '<b>Премиум контентті қолжетімді ету</b> — шағын бизнес пен жеке клиенттер үшін', '<b>Make premium content accessible</b> — for small businesses and private clients'),
             ('Помочь брендам Казахстана <b>выделяться</b> в ленте и в поиске', 'Қазақстан брендтеріне лентада және іздеуде <b>ерекшеленуге</b> көмектесу', 'Help Kazakhstan brands <b>stand out</b> in feeds and search'),
             ('Превращать <b>личные истории</b> в фильмы, которые пересматривают', '<b>Жеке тарихтарды</b> қайта-қайта көретін фильмдерге айналдыру', 'Turn <b>personal stories</b> into films people rewatch')],
            ("Наша стратегия", "Біздің стратегия", "Our strategy"),
            [('<b>ИИ + живая съёмка</b> — скорость нейросетей и честность реальных кадров', '<b>ИИ + нақты түсірілім</b> — нейрожелілердің жылдамдығы мен шынайы кадрлардың адалдығы', '<b>AI + live shooting</b> — the speed of neural networks and the honesty of real footage'),
             ('<b>Всё в одном месте:</b> контент, сайт и упаковка бренда', '<b>Барлығы бір жерде:</b> контент, сайт және бренд қаптамасы', '<b>All in one place:</b> content, website and brand packaging'),
             ('<b>Результат в цифрах</b> — охваты, заявки, продажи', '<b>Нәтиже сандармен</b> — қамту, өтінімдер, сатылымдар', '<b>Results in numbers</b> — reach, leads, sales')],
            ("Цель", "Мақсат", "Goal"), ("Стратегия", "Стратегия", "Strategy"))
      + f'''
    <section class="section section--tight">
      <div class="wrap">
        {sec_head("lbl.why", "home.whyH", ("Почему с нами удобно", "Бізбен неге ыңғайлы", "Why it’s easy with us"))}
        <ul class="why">
{check_html}
        </ul>
      </div>
    </section>

    <section class="section" id="team">
      <div class="wrap">
        {sec_head("lbl.team", "home.teamH", ("Основатели", "Негізін қалаушылар", "Founders"), ("home.teamNote", "Нажмите на карточку — откроется Instagram.", "Карточканы басыңыз — Instagram ашылады.", "Tap a card to open Instagram."))}
        <div class="team" data-team></div>
      </div>
    </section>
'''
      + faq("home"))

# ================================================================== ИИ КОНТЕНТ
pipes = [("photo", ("Ваши фото", "Сіздің фотоларыңыз", "Your photos"), ("Отбираем лучшие ракурсы и эмоции", "Ең жақсы ракурстар мен эмоцияларды таңдаймыз", "We pick the best angles and emotions")),
         ("spark", ("Обучение модели", "Модельді оқыту", "Model training"), ("ИИ запоминает лица героев", "ИИ кейіпкерлердің бетін есте сақтайды", "The AI learns the characters’ faces")),
         ("wand", ("Генерация сцен", "Сахналар генерациясы", "Scene generation"), ("Каждый кадр по сценарию", "Әр кадр сценарий бойынша", "Every frame follows the script")),
         ("film", ("Кино-монтаж", "Кино-монтаж", "Cinematic edit"), ("Музыка, голос, цветокор", "Музыка, дауыс, түс түзету", "Music, voice, grading"))]
pipe_html = "\n".join(f'          <div class="pipe" data-reveal><span class="scan"></span><span class="ico" data-icon="{ic}"></span><b {t(f"ai.pipe{i}", a)}</b><span class="txt" {t(f"ai.pipe{i}d", b)}</span></div>' for i, (ic, a, b) in enumerate(pipes))

write("ai",
      hero("ai", ("01 / ИИ контент", "01 / ИИ контент", "01 / AI content"),
           ("Ваша история<br><em>как в кино</em>", "Сіздің тарихыңыз<br><em>кинодағыдай</em>", "Your story<br><em>like a movie</em>"),
           ("Love story / Реклама / ИИ-аватары", "Love story / Жарнама / ИИ-аватарлар", "Love story / Ads / AI avatars"),
           ("Превращаем фотографии и воспоминания в видео, которое трогает до мурашек, — без съёмочной группы и декораций.",
            "Фотосуреттер мен естеліктерді жүрекке жететін видеоға айналдырамыз — түсірілім тобынсыз және декорациясыз.",
            "We turn photos and memories into videos that give you goosebumps — no film crew, no sets."),
           visual("ai"),
           ("#prices", "hero.prices"))
      + bands("ai", ("Love Story|ИИ-видео|Оживление фото|ИИ-аватары|Реклама без съёмок|Клипы|4K",
                     "Love Story|ИИ-видео|Фотоларды жандандыру|ИИ-аватарлар|Түсірілімсіз жарнама|Клиптер|4K",
                     "Love Story|AI video|Photo animation|AI avatars|Ads without a shoot|Music videos|4K"))
      + stats("ai", [(60, "+", ("ИИ-роликов", "ИИ-ролик", "AI videos")), (3, "", ("дня — мини-ролик", "күн — мини-ролик", "days for a mini video")),
                     (4, "K", ("разрешение", "ажыратымдылық", "resolution")), (3, "", ("языка озвучки", "дыбыстау тілі", "voice-over languages"))])
      + duo("ai", ("Что создаём", "Не жасаймыз", "What we create"),
            [('<b>Love Story</b> — история пары для свадьбы или годовщины', '<b>Love Story</b> — той немесе мерейтойға арналған жұп тарихы', '<b>Love Story</b> — a couple’s story for a wedding or anniversary'),
             ('<b>Семейные фильмы</b> — оживляем старые фото', '<b>Отбасылық фильмдер</b> — ескі фотоларды жандандырамыз', '<b>Family films</b> — we bring old photos to life'),
             ('<b>Рекламные ролики</b> для Reels, TikTok, YouTube', 'Reels, TikTok, YouTube үшін <b>жарнамалық роликтер</b>', '<b>Ads</b> for Reels, TikTok, YouTube'),
             ('<b>ИИ-аватары</b> и клипы для артистов', 'Әртістерге арналған <b>ИИ-аватарлар</b> мен клиптер', '<b>AI avatars</b> and music videos for artists')],
            ("Что нужно от вас", "Сізден не қажет", "What we need"),
            [('<b>10–30 фотографий</b> героев', 'Кейіпкерлердің <b>10–30 фотосуреті</b>', '<b>10–30 photos</b> of the main characters'),
             ('Короткий рассказ — <b>можно голосовым</b>', 'Қысқаша әңгіме — <b>дауыспен де болады</b>', 'A short story — <b>a voice message works</b>'),
             ('Пожелания по настроению и музыке', 'Көңіл-күй мен музыка бойынша тілектер', 'Wishes for the mood and music'),
             ('Дата, к которой нужен ролик', 'Ролик қажет болатын күн', 'The date you need the video by')],
            ("Услуги", "Қызметтер", "Services"), ("Для старта", "Бастау үшін", "To start"))
      + steps("ai", [(("Бриф", "Бриф", "Brief"), ("Узнаём вашу историю и цели", "Тарихыңыз бен мақсаттарыңызды білеміз", "We learn your story and goals")),
                     (("Сценарий", "Сценарий", "Script"), ("Пишем сюжет и раскадровку", "Сюжет пен раскадровка жазамыз", "We write the plot and storyboard")),
                     (("Генерация", "Генерация", "Generation"), ("Создаём сцены по вашим фото", "Фотоларыңыз бойынша сахналар жасаймыз", "We create scenes from your photos")),
                     (("Финал", "Финал", "Final"), ("Монтаж, звук, цветокор", "Монтаж, дыбыс, түс түзету", "Editing, sound, grading"))])
      + portfolio("ai", "ai", "reels", ("Работы: ИИ контент", "Жұмыстар: ИИ контент", "Work: AI content"))
      + f'''
    <section class="section section--tight">
      <div class="wrap">
        {sec_head("lbl.process", "ai.techH", ("Как фото становится фильмом", "Фото қалай фильмге айналады", "How a photo becomes a film"))}
        <div class="pipeline">
{pipe_html}
        </div>
      </div>
    </section>
'''
      + tail("ai"))

# ================================================================== МОБИЛОГРАФИЯ
IMG = "https://images.unsplash.com/photo-1501785888041-af3ef285b470?auto=format&fit=crop&w=1600&q=75"
presets = [("saturate(1.25) contrast(1.12) brightness(.96) hue-rotate(-6deg)", "linear-gradient(180deg, rgba(0,120,140,.18), transparent 50%, rgba(255,120,40,.22))", "linear-gradient(90deg,#1ba3b0,#ff8a4c)", "Teal &amp; Orange"),
           ("saturate(1.1) contrast(1.05) brightness(1.05) sepia(.25)", "linear-gradient(180deg, rgba(255,190,90,.3), rgba(255,120,80,.2))", "#ffb25c", "Golden hour"),
           ("saturate(.7) contrast(1.25) brightness(.9)", "linear-gradient(180deg, rgba(40,60,90,.35), rgba(10,10,20,.3))", "#3b4a66", "Moody"),
           ("saturate(1.4) contrast(1.1) brightness(1.02) hue-rotate(8deg)", "linear-gradient(180deg, rgba(255,80,180,.18), rgba(80,120,255,.2))", "linear-gradient(90deg,#ff5fb7,#5a78ff)", "Vivid")]
preset_html = "\n".join(f'          <button type="button"{" class=\"active\"" if i == 0 else ""} data-filter="{f}" data-tint="{tn}"><i style="background:{c}"></i>{n}</button>' for i, (f, tn, c, n) in enumerate(presets))

reg("mobile.gradeLink", "Цветокор до/после", "Түс түзету дейін/кейін", "Grading before/after")
write("mobile",
      hero("mobile", ("03 / Мобилография", "03 / Мобилография", "03 / Mobile film"),
           ("Кино<br>на&nbsp;<em>телефон</em>", "Телефонмен<br><em>кино</em>", "Cinema<br>on a <em>phone</em>"),
           ("Reels / Съёмка / Цветокор", "Reels / Түсірілім / Түс түзету", "Reels / Shooting / Grading"),
           ("Снимаем Reels, TikTok и Shorts для брендов, экспертов и событий. Сценарий, съёмка, монтаж и фирменный цветокор — быстро и в трендах.",
            "Брендтерге, сарапшыларға және іс-шараларға Reels, TikTok және Shorts түсіреміз. Сценарий, түсірілім, монтаж және фирмалық түс түзету — жылдам әрі трендте.",
            "We shoot Reels, TikTok and Shorts for brands, experts and events. Script, shooting, editing and signature grading — fast and on-trend."),
           visual("mobile"),
           ("#grading", "mobile.gradeLink"))
      + bands("mobile", ("Reels|TikTok|Shorts|Цветокор|Монтаж|Контент-день|Свадебный тизер|Предметка",
                         "Reels|TikTok|Shorts|Түс түзету|Монтаж|Контент-күн|Той тизері|Заттық түсірілім",
                         "Reels|TikTok|Shorts|Color grading|Editing|Content day|Wedding teaser|Product shoot"))
      + stats("mobile", [(300, "+", ("роликов", "ролик", "videos")), (2, "М", ("просмотров", "қаралым", "views")),
                         (24, "ч", ("тизер события", "іс-шара тизері", "event teaser")), (4, "K", ("60 fps", "60 fps", "60 fps"))])
      + duo("mobile", ("Что снимаем", "Не түсіреміз", "What we shoot"),
            [('<b>Reels для бизнеса</b> — кафе, салоны, магазины', '<b>Бизнеске арналған Reels</b> — кафелер, салондар, дүкендер', '<b>Reels for business</b> — cafés, salons, shops'),
             ('<b>Контент-дни</b> для экспертов и блогеров', 'Сарапшылар мен блогерлерге <b>контент-күндер</b>', '<b>Content days</b> for experts and bloggers'),
             ('<b>Свадьбы и события</b> — тизер в тот же день', '<b>Тойлар мен іс-шаралар</b> — тизер сол күні', '<b>Weddings and events</b> — same-day teaser'),
             ('<b>Предметка</b> для маркетплейсов', 'Маркетплейстерге <b>заттық түсірілім</b>', '<b>Product shoots</b> for marketplaces')],
            ("Почему мобильно", "Неге мобильді", "Why mobile"),
            [('<b>Быстро</b> — без громоздкой техники', '<b>Жылдам</b> — ауыр техникасыз', '<b>Fast</b> — no bulky gear'),
             ('<b>Нативно</b> — формат, который любят алгоритмы', '<b>Нативті</b> — алгоритмдер ұнататын формат', '<b>Native</b> — the format algorithms love'),
             ('<b>Кино-цветокор</b> в фирменном стиле', 'Фирмалық стильдегі <b>кино-түс түзету</b>', '<b>Cinematic grading</b> in your brand style'),
             ('<b>Дешевле</b> классического продакшна', 'Классикалық продакшннан <b>арзанырақ</b>', '<b>Cheaper</b> than classic production')],
            ("Услуги", "Қызметтер", "Services"), ("Преимущества", "Артықшылықтар", "Benefits"))
      + steps("mobile", [(("Идеи", "Идеялар", "Ideas"), ("Контент-план и сценарии", "Контент-жоспар және сценарийлер", "Content plan and scripts")),
                         (("Съёмка", "Түсірілім", "Shooting"), ("iPhone, свет, стабилизация", "iPhone, жарық, тұрақтандыру", "iPhone, lighting, stabilization")),
                         (("Монтаж", "Монтаж", "Editing"), ("Динамика, звук, титры", "Динамика, дыбыс, титрлер", "Pacing, sound, titles")),
                         (("Цветокор", "Түс түзету", "Grading"), ("Фирменная картинка", "Фирмалық сурет", "Your signature look"))])
      + portfolio("mobile", "mobile", "reels", ("Работы: мобилография", "Жұмыстар: мобилография", "Work: mobilography"))
      + f'''
    <section class="section section--tight" id="grading">
      <div class="wrap">
        {sec_head("lbl.process", "mobile.gradeH", ("До и после цветокора", "Түс түзетуге дейін және кейін", "Before & after grading"), ("mobile.gradeHint", "Потяните ползунок и переключайте пресеты.", "Жүгірткіні тартып, пресеттерді ауыстырыңыз.", "Drag the slider and switch presets."))}
        <div class="compare" data-compare data-reveal>
          <img class="before" src="{IMG}" alt="" loading="lazy">
          <img class="after" src="{IMG}" alt="" loading="lazy">
          <div class="after-tint"></div>
          <span class="chip lbl l" {t("mobile.before", ("до", "дейін", "before"))}</span><span class="chip lbl r" {t("mobile.after", ("после", "кейін", "after"))}</span>
          <div class="handle"></div>
          <input type="range" min="0" max="100" value="50" aria-label="before / after">
        </div>
        <div class="filters presets" data-presets>
{preset_html}
        </div>
      </div>
    </section>
'''
      + tail("mobile"))

# ================================================================== САЙТЫ
stack = ["Figma", "HTML / CSS", "JavaScript", "TypeScript", "React", "Next.js", "Vite", "Tailwind", "GSAP", "Node.js", "Tilda", "WordPress", "Kaspi Pay", "amoCRM", "Google Analytics", "Яндекс Метрика", "KZ · RU · EN"]
browser = '''          <div class="browser"><div class="browser-bar"><i></i><i></i><i></i></div><img src="assets/img/projects/itecx.webp" alt="ITECX"></div>
'''
write("web",
      hero("web", ("02 / Сайты", "02 / Сайттар", "02 / Websites"),
           ("Сайты,<br>которые<br><em>продают</em>", "Сататын<br><em>сайттар</em>", "Websites<br>that <em>sell</em>"),
           ("Лендинги / Сайты / Магазины", "Лендингтер / Сайттар / Дүкендер", "Landings / Websites / Stores"),
           ("От идеи и дизайна до запуска, аналитики и поддержки. Быстрые, красивые на телефоне и на трёх языках — KZ, RU, EN.",
            "Идея мен дизайннан бастап іске қосу, аналитика және қолдауға дейін. Жылдам, телефонда әдемі және үш тілде — KZ, RU, EN.",
            "From idea and design to launch, analytics and support. Fast, beautiful on phones and in three languages — KZ, RU, EN."),
           visual("web", "assets/img/projects/itecx.webp", "assets/img/projects/astanatechcup.webp"),
           ("#work", "hero.works"))
      + bands("web", ("Лендинги|Корпоративные сайты|Сайты мероприятий|UI/UX|Анимации|SEO|Kaspi Pay|KZ · RU · EN",
                      "Лендингтер|Корпоративтік сайттар|Іс-шара сайттары|UI/UX|Анимациялар|SEO|Kaspi Pay|KZ · RU · EN",
                      "Landing pages|Corporate websites|Event websites|UI/UX|Animations|SEO|Kaspi Pay|KZ · RU · EN"))
      + stats("web", [(40, "+", ("сайтов", "сайт", "websites")), (10, "", ("дней — лендинг", "күн — лендинг", "days for a landing page")),
                      (95, "+", ("PageSpeed", "PageSpeed", "PageSpeed")), (3, "", ("языка на сайте", "тіл сайтта", "site languages"))])
      + duo("web", ("Что разрабатываем", "Не әзірлейміз", "What we build"),
            [('<b>Лендинги</b> под рекламу и запуски', 'Жарнама мен іске қосуға арналған <b>лендингтер</b>', '<b>Landing pages</b> for ads and launches'),
             ('<b>Корпоративные сайты</b> и сайты-визитки', '<b>Корпоративтік сайттар</b> және сайт-визиткалар', '<b>Corporate websites</b> and business card sites'),
             ('<b>Сайты мероприятий</b> с регистрацией участников', 'Қатысушыларды тіркейтін <b>іс-шара сайттары</b>', '<b>Event websites</b> with participant registration'),
             ('<b>Интернет-магазины</b> с оплатой Kaspi', 'Kaspi төлемі бар <b>интернет-дүкендер</b>', '<b>Online stores</b> with Kaspi payments')],
            ("Что вы получите", "Сіз не аласыз", "What you get"),
            [('<b>Уникальный дизайн</b> с анимациями', 'Анимациялары бар <b>бірегей дизайн</b>', '<b>Unique design</b> with animations'),
             ('<b>Три языка</b> — KZ, RU, EN', '<b>Үш тіл</b> — KZ, RU, EN', '<b>Three languages</b> — KZ, RU, EN'),
             ('<b>Заявки</b> в WhatsApp, Telegram, CRM', 'WhatsApp, Telegram, CRM-ге <b>өтінімдер</b>', '<b>Leads</b> to WhatsApp, Telegram, CRM'),
             ('<b>SEO и аналитика</b> с первого дня', 'Алғашқы күннен <b>SEO және аналитика</b>', '<b>SEO and analytics</b> from day one')],
            ("Услуги", "Қызметтер", "Services"), ("Результат", "Нәтиже", "Result"))
      + steps("web", [(("Бриф", "Бриф", "Brief"), ("Цели, аудитория, конкуренты", "Мақсаттар, аудитория, бәсекелестер", "Goals, audience, competitors")),
                      (("Дизайн", "Дизайн", "Design"), ("Прототип и макеты в Figma", "Figma-да прототип пен макеттер", "Prototype and mockups in Figma")),
                      (("Разработка", "Әзірлеу", "Development"), ("Вёрстка, анимации, интеграции", "Беттеу, анимациялар, интеграциялар", "Coding, animations, integrations")),
                      (("Запуск", "Іске қосу", "Launch"), ("Домен, SEO, аналитика", "Домен, SEO, аналитика", "Domain, SEO, analytics"))])
      + portfolio("web", "web", "grid", ("Работы: сайты", "Жұмыстар: сайттар", "Work: websites"), hint=False)
      + f'''
    <section class="section section--tight">
      <div class="wrap">
        {sec_head("lbl.process", "web.stackH", ("Технологии", "Технологиялар", "Technologies"))}
        <div class="stack" data-reveal>
          {"".join(f"<span>{s}</span>" for s in stack)}
        </div>
      </div>
    </section>
'''
      + tail("web"))

# ================================================================== i18n.js
lines = ["/* ==========================================================",
         "   ПЕРЕВОДЫ ИНТЕРФЕЙСА: ключ -> { ru, kz, en }",
         "   Ключи совпадают с атрибутом data-i18n в HTML.",
         "   Проекты, цены, FAQ и команда переводятся в data.js.",
         "   ========================================================== */",
         "window.I18N = {"]
for k, v in D.items():
    lines.append(f"  {json.dumps(k, ensure_ascii=False)}: {{ ru: {json.dumps(v['ru'], ensure_ascii=False)}, kz: {json.dumps(v['kz'], ensure_ascii=False)}, en: {json.dumps(v['en'], ensure_ascii=False)} }},")
lines.append("};\n")
open("assets/js/i18n.js", "w", encoding="utf-8").write("\n".join(lines))
open("assets/img/favicon.svg", "w", encoding="utf-8").write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="45 45 1160 1160"><circle cx="625" cy="625" r="580" fill="#0047ff"/><path d="M365 491 L681 491 L603 573 L285 573Z M447 587 L587 587 L443 697 L607 697 L521 783 L222 783 L292 710 L320 686Z" fill="#fff"/><path d="M729 491 L1036 491 L965 566 L940 588 L797 697 L993 697 L889 783 L561 783 L630 716 L648 700 L808 573 L649 573Z" fill="#fff"/></svg>' + chr(10))
print("keys:", len(D))
