"""Карусель Mazzeru «Знакомство» (6 слайдов, 1080×1350): лайм / белый / чёрный, Unbounded + Inter Tight.
Без ИИ-картинок: векторная графика + реальные скриншоты проектов. Пишет HTML и PNG."""
import os, random, sys
import topng
import brand_mark as BM

B = r"C:\Users\USER\OneDrive\Desktop\Mazzeru\brand"
ROOT = r"C:\Users\USER\OneDrive\Desktop\Mazzeru"
OUT = B + r"\instagram\carousel"
os.makedirs(OUT, exist_ok=True)
F = "file:///" + (B + r"\fonts").replace("\\", "/")
IMG = "file:///" + (ROOT + r"\assets\img").replace("\\", "/")
LIME, INK, WHITE, PAPER = "#E7FF00", "#0B0B0F", "#FFFFFF", "#F6F5EE"

# ---------------- иконки (stroke) ----------------
def ico(name, color, size=54, sw=1.8):
    d = {
        "video": '<rect x="2.5" y="6" width="13" height="12" rx="2.5"/><path d="M15.5 10.5 21.5 7v10l-6-3.5"/>',
        "person": '<circle cx="12" cy="8" r="4"/><path d="M4 21c1-4.5 4-6.5 8-6.5s7 2 8 6.5"/>',
        "grid": '<rect x="3" y="3" width="18" height="18" rx="2.5"/><path d="M3 10h18M3 15h18M10 3v18"/>',
        "cup": '<path d="M5 10h11v4a5 5 0 0 1-5 5h-1a5 5 0 0 1-5-5z"/><path d="M16 11h1.5a2.5 2.5 0 0 1 0 5H15.5M9 3c-1 1 1 2 0 3M13 3c-1 1 1 2 0 3"/>',
        "pin": '<path d="M12 21s-7-6.2-7-11a7 7 0 0 1 14 0c0 4.8-7 11-7 11z"/><circle cx="12" cy="10" r="2.6"/>',
        "globe": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c3 3.2 3 14.8 0 18M12 3c-3 3.2-3 14.8 0 18"/>',
        "chat": '<rect x="3" y="4" width="18" height="13" rx="3"/><path d="M8 20l3-3M8.5 10.5h.01M12 10.5h.01M15.5 10.5h.01"/>',
        "doc": '<path d="M6 3h8l4 4v14H6z"/><path d="M14 3v4h4M9 12h6M9 16h6"/>',
        "send": '<path d="M21 3 3 10.5l7 3 3 7z"/><path d="M10 13.5 21 3"/>',
        "rec": '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="4" fill="currentColor"/>',
        "reels": '<rect x="3" y="3" width="18" height="18" rx="5"/><path d="M3 9h18M9 3l3 6M15 3l3 6"/><path d="M10 13v5l4.5-2.5z" fill="currentColor"/>',
        "team": '<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20c.8-3.6 3.4-5.5 6.5-5.5s5.7 1.9 6.5 5.5M16 4.8a3.5 3.5 0 0 1 0 6.4M18 14.8c1.9.7 3.1 2.4 3.5 5.2"/>',
        "pinbuild": '<path d="M4 21V7l7-4v18M11 21V11l9 3v7M7 10h1M7 14h1M7 18h1M15 16h1M15 19h1"/>',
    }[name]
    return f'<svg viewBox="0 0 24 24" width="{size}" height="{size}" fill="none" stroke="{color}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round" style="color:{color}">{d}</svg>'


def mark(bg, z, size):
    return BM.svg_mark(bg, z, "mk").replace("<svg ", f'<svg style="width:{size}px;height:{size}px;display:block" ')


# ---------------- векторные «кадры» ----------------
def scene(kind, w=400, h=300, seed=1):
    rnd = random.Random(seed)
    s = f'<svg viewBox="0 0 {w} {h}" preserveAspectRatio="xMidYMid slice" style="width:100%;height:100%;display:block" xmlns="http://www.w3.org/2000/svg">'
    defs = f'<defs><radialGradient id="g{seed}" cx="50%" cy="60%" r="60%"><stop offset="0" stop-color="{LIME}" stop-opacity=".38"/><stop offset="1" stop-color="{LIME}" stop-opacity="0"/></radialGradient></defs>'
    s += defs + f'<rect width="{w}" height="{h}" fill="{INK}"/>'
    if kind == "sun":
        s += f'<rect width="{w}" height="{h}" fill="url(#g{seed})"/>'
        for _ in range(26): s += f'<circle cx="{rnd.random()*w:.0f}" cy="{rnd.random()*h*0.5:.0f}" r="{rnd.random()*1.3+.3:.1f}" fill="#fff" opacity="{rnd.random()*.6+.2:.2f}"/>'
        s += f'<circle cx="{w*.5}" cy="{h*.5}" r="{h*.23}" fill="{LIME}"/>'
        s += f'<path d="M0 {h} L0 {h*.63} L{w*.17} {h*.47} L{w*.3} {h*.62} L{w*.47} {h*.4} L{w*.65} {h*.63} L{w*.8} {h*.5} L{w} {h*.7} L{w} {h}Z" fill="#17171d" stroke="{LIME}" stroke-opacity=".45" stroke-width="1.2"/>'
        s += f'<path d="M0 {h} L0 {h*.8} L{w*.2} {h*.67} L{w*.37} {h*.82} L{w*.58} {h*.69} L{w*.78} {h*.83} L{w} {h*.72} L{w} {h}Z" fill="{INK}"/>'
    elif kind in ("city", "tower"):
        s += f'<rect width="{w}" height="{h}" fill="url(#g{seed})"/>'
        s += f'<circle cx="{w*.5}" cy="{h*.62}" r="{h*.24}" fill="{LIME}" opacity="{.95 if kind=="tower" else .0}"/>'
        x = 0
        while x < w:
            bw = rnd.randint(int(w*.05), int(w*.11)); bh = rnd.randint(int(h*.18), int(h*.55))
            if kind == "tower" and abs(x + bw / 2 - w * .5) < w * .12: x += bw; continue
            s += f'<rect x="{x}" y="{h-bh}" width="{bw-3}" height="{bh}" fill="#0f0f14" stroke="{LIME}" stroke-opacity=".28" stroke-width="1"/>'
            for wy in range(int(h - bh + 8), h - 6, 13):
                for wx in range(x + 5, x + bw - 8, 9):
                    if rnd.random() < .34: s += f'<rect x="{wx}" y="{wy}" width="3.4" height="5" fill="{LIME}" opacity="{rnd.random()*.6+.3:.2f}"/>'
            x += bw
        if kind == "tower":
            cx = w * .5
            s += f'<path d="M{cx-14} {h} Q{cx-6} {h*.6} {cx-3} {h*.42} L{cx+3} {h*.42} Q{cx+6} {h*.6} {cx+14} {h}Z" fill="{INK}" stroke="{LIME}" stroke-width="2"/>'
            s += f'<circle cx="{cx}" cy="{h*.34}" r="{h*.11}" fill="{INK}" stroke="{LIME}" stroke-width="2.4"/><circle cx="{cx}" cy="{h*.34}" r="{h*.05}" fill="{LIME}"/>'
            s += f'<path d="M{cx} {h*.23} L{cx} {h*.12}" stroke="{LIME}" stroke-width="2"/>'
    elif kind == "planet":
        for _ in range(60): s += f'<circle cx="{rnd.random()*w:.0f}" cy="{rnd.random()*h*.7:.0f}" r="{rnd.random()*1.2+.3:.1f}" fill="#fff" opacity="{rnd.random()*.7+.2:.2f}"/>'
        s += f'<ellipse cx="{w*.5}" cy="{h*1.05}" rx="{w*.75}" ry="{h*.55}" fill="url(#g{seed})"/>'
        s += f'<circle cx="{w*.5}" cy="{h*1.9}" r="{h*1.35}" fill="#101014" stroke="{LIME}" stroke-width="2"/>'
        import math
        for _ in range(140):
            a = rnd.uniform(-1.05, -2.09); r = h * 1.35 * rnd.uniform(.9, .995)
            s += f'<circle cx="{w*.5 + math.cos(a)*r:.0f}" cy="{h*1.9 + math.sin(a)*r:.0f}" r="1.1" fill="{LIME}" opacity="{rnd.random()*.8+.2:.2f}"/>'
        s += f'<circle cx="{w*.82}" cy="{h*.22}" r="{h*.09}" fill="none" stroke="{LIME}" stroke-width="2"/>'
    elif kind == "wave":
        s += f'<rect width="{w}" height="{h}" fill="{LIME}"/>'
        for i in range(9): s += f'<circle cx="{w*.66}" cy="{h*.45}" r="{20+i*22}" fill="none" stroke="{INK}" stroke-width="{2 + i*.5}" opacity="{1 - i*.09:.2f}"/>'
        s += f'<circle cx="{w*.66}" cy="{h*.45}" r="{h*.13}" fill="{INK}"/>'
    s += '</svg>'
    return s


def frame(kind, x, y, w, h, label, time, seed=1, r=22, small=False):
    fs = 15 if small else 17
    return f'''<div class="frame" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;border-radius:{r}px">
      {scene(kind, 400, int(400*h/w), seed)}
      <div class="fshade"></div>
      <div class="play"><i></i></div><span class="ftime">{time}</span><span class="flabel" style="font-size:{fs}px">{label}</span></div>'''


def shot(name, x, y, w, h, r=14, duo=False, pos="top"):
    """реальный скриншот проекта; duo — дуотон лайм/чёрный"""
    cls = "duo" if duo else ""
    return f'<div class="shot {cls}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;border-radius:{r}px"><img src="{IMG}/projects/{name}.webp" style="object-position:center {pos}"></div>'


def laptop(name, x, y, w, rot=0):
    sh = w * .62
    return f'''<div class="laptop" style="left:{x}px;top:{y}px;width:{w}px;transform:rotate({rot}deg)">
      <div class="lscreen" style="height:{sh}px"><img src="{IMG}/projects/{name}.webp"></div>
      <div class="lbase"></div></div>'''


def phone(x, y, w, inner, rot=0, dark=True, hm=2.05):
    h = w * hm
    return f'''<div class="phone" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;border-radius:{w*.16}px;transform:rotate({rot}deg)">
      <div class="pscreen" style="border-radius:{w*.13}px">{inner}</div><i class="notch"></i></div>'''


# ---------------- общий CSS ----------------
CSS = f"""
@font-face {{ font-family: U; src: url('{F}/Unbounded-ExtraBold.ttf'); font-weight: 800; }}
@font-face {{ font-family: UM; src: url('{F}/Unbounded-Medium.ttf'); font-weight: 500; }}
@font-face {{ font-family: I; src: url('{F}/InterTight.ttf'); font-weight: 100 900; }}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html, body {{ width: 100%; height: 100%; overflow: hidden; }}
body {{ font-family: I, sans-serif; -webkit-font-smoothing: antialiased; position: relative; width: 1080px; height: 1350px; }}
.a {{ position: absolute; }}
.h {{ font-family: U; font-weight: 800; line-height: .98; letter-spacing: -.045em; text-transform: uppercase; }}
.lab {{ font-family: UM; font-size: 15px; letter-spacing: .28em; text-transform: uppercase; line-height: 1.9; }}
.bar {{ position: absolute; width: 74px; height: 8px; background: {LIME}; }}
.p1 {{ font: 500 34px/1.22 I; letter-spacing: -.01em; }}
.p1 b {{ font-weight: 800; }}
.p2 {{ font: 400 26px/1.35 I; opacity: .78; }}
.ghost {{ position: absolute; right: 40px; bottom: -50px; font: 800 250px/1 U; letter-spacing: -.06em; opacity: .09; }}
.frame {{ position: absolute; overflow: hidden; background: {INK}; box-shadow: 0 24px 50px -20px rgba(0,0,0,.6); }}
.fshade {{ position: absolute; inset: 0; background: linear-gradient(to top, rgba(0,0,0,.72), transparent 55%); }}
.play {{ position: absolute; left: 22px; bottom: 20px; width: 46px; height: 46px; border-radius: 50%; background: {LIME}; display: grid; place-items: center; }}
.play i {{ width: 0; height: 0; border-left: 14px solid {INK}; border-top: 9px solid transparent; border-bottom: 9px solid transparent; margin-left: 4px; }}
.ftime {{ position: absolute; left: 80px; bottom: 30px; font: 600 17px/1 I; color: #fff; }}
.flabel {{ position: absolute; right: 20px; bottom: 22px; font-family: UM; color: {LIME}; letter-spacing: .12em; text-align: right; line-height: 1.3; text-transform: uppercase; }}
.card {{ position: absolute; border-radius: 30px; overflow: hidden; }}
.shot {{ position: absolute; overflow: hidden; background: #fff; box-shadow: 0 18px 40px -16px rgba(0,0,0,.55); }}
.shot img {{ width: 100%; height: 100%; object-fit: cover; display: block; }}
.duo {{ background: {LIME}; }}
.duo img {{ filter: grayscale(1) contrast(1.25) brightness(1.05); mix-blend-mode: multiply; }}
.laptop {{ position: absolute; }}
.lscreen {{ background: #111; border: 9px solid #17171d; border-bottom-width: 12px; border-radius: 18px 18px 6px 6px; overflow: hidden; box-shadow: 0 30px 60px -20px rgba(0,0,0,.7); }}
.lscreen img {{ width: 100%; height: 100%; object-fit: cover; object-position: top; display: block; }}
.lbase {{ height: 15px; width: 112%; margin-left: -6%; background: linear-gradient(#cfcfd4, #8d8d94); border-radius: 0 0 22px 22px; }}
.phone {{ position: absolute; background: #17171d; padding: 7px; box-shadow: 0 30px 60px -20px rgba(0,0,0,.7), inset 0 0 0 2px #2b2b33; }}
.pscreen {{ width: 100%; height: 100%; overflow: hidden; background: {INK}; position: relative; }}
.notch {{ position: absolute; top: 12px; left: 50%; width: 32%; height: 18px; margin-left: -16%; background: #000; border-radius: 12px; }}
.chip {{ position: absolute; border-radius: 26px; border: 2px solid rgba(255,255,255,.28); padding: 22px; }}
.foot {{ position: absolute; left: 56px; right: 56px; bottom: 34px; height: 90px; }}
.foot .lab {{ font-size: 14px; line-height: 1.55; }}
.foot .line {{ position: absolute; left: 0; right: 30%; top: 0; height: 2px; background: currentColor; opacity: .5; }}
"""


def head(n, dark=True):
    fg = WHITE if dark else INK
    z = INK if dark else LIME
    bg = LIME if dark else INK
    return f'''<div class="a" style="left:56px;top:38px;display:flex;align-items:center;gap:14px;color:{fg}">{mark(bg, z, 46)}<span style="font:800 26px/1 U;letter-spacing:-.06em">mazzeru</span></div>
    <div class="a lab" style="right:50px;top:44px;color:{fg};font-size:20px;letter-spacing:.18em">{n:02d} / 06</div>'''


def foot(left, right, dark=True, n=None):
    fg = WHITE if dark else INK
    arrow = f'<svg viewBox="0 0 160 30" width="160" height="30" style="position:absolute;left:27%;top:34px"><path d="M2 15h150M136 3l16 12-16 12" fill="none" stroke="{fg}" stroke-width="1.8" stroke-linecap="round" opacity=".7"/></svg>'
    ghost = f'<div class="ghost" style="color:{fg}">{n:02d}</div>' if n else ''
    return f'''{ghost}<div class="foot" style="color:{fg}"><div class="line"></div>
      <div class="lab" style="position:absolute;left:0;top:22px">{left}</div>{arrow}
      <div class="lab" style="position:absolute;left:50%;top:22px;width:50%">{right}</div></div>'''


def page(name, body, bg, w=1080, h=1350):
    html = os.path.join(topng.TMP, name + ".html")
    doc = f"<html><head><meta charset='utf-8'><style>{CSS}body{{background:{bg}}}</style></head><body>{body}</body></html>"
    open(html, "w", encoding="utf-8").write(doc)
    open(os.path.join(OUT, name + ".html"), "w", encoding="utf-8").write(doc)
    topng.render(html, os.path.join(OUT, name + ".png"), w, h, crop_alpha=False)
    print(name)


# ================= 01 ОБЛОЖКА =================
page("01-cover", f'''
<div class="a" style="right:-240px;bottom:-280px;width:760px;height:760px">{mark(LIME, INK, 760)}</div>
<div class="a" style="left:56px;top:38px;display:flex;align-items:center;gap:14px">{mark(LIME, INK, 46)}<span style="font:800 26px/1 U;letter-spacing:-.06em;color:#fff">mazzeru</span></div>
<div class="a lab" style="right:50px;top:44px;color:#fff;font-size:20px;letter-spacing:.18em">01 / 06</div>
<div class="a h" style="left:44px;top:420px;color:#fff;font-size:198px;text-transform:none;letter-spacing:-.07em;white-space:nowrap">mazzeru</div>
<div class="bar" style="left:56px;top:700px"></div>
<div class="a lab" style="left:56px;top:750px;color:#fff;font-size:34px;letter-spacing:.5em">знакомимся</div>
<div class="a lab" style="left:56px;top:1210px;color:{LIME};font-size:19px;letter-spacing:.3em">ИИ-видео / Съёмка / Сайты</div>
<div class="a lab" style="left:56px;top:1250px;color:#fff;opacity:.6;font-size:17px">Digital-студия · Астана</div>
''', INK)

# ================= 02 КТО МЫ =================
def mini_card(x, y, w, h, vis, icon, title, text_, ih):
    return f'''<div class="card" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;background:{INK};color:#fff">
      <div class="a" style="left:0;top:0;width:{w}px;height:{ih}px;overflow:hidden;background:{INK}">{vis}</div>
      <div class="a" style="left:22px;top:{ih+22}px">{ico(icon, LIME, 46)}</div>
      <div class="a h" style="left:82px;top:{ih+28}px;font-size:23px;line-height:1.05">{title}</div>
      <div class="a" style="left:22px;top:{ih+86}px;width:{w-40}px;font:400 22px/1.28 I;opacity:.85">{text_}</div></div>'''

cw = 320; ch = 520; iy = 740
vis_ai = f'{scene("sun", 320, 270, 3)}<div class="play" style="left:20px;bottom:20px"><i></i></div>'
vis_shoot = f'<div class="a" style="inset:0;background:{LIME}"></div>' + phone(88, 32, 150, scene("tower", 300, 600, 5) + f'<div class="a" style="left:50%;bottom:18px;margin-left:-13px;width:26px;height:26px;border-radius:50%;background:#ff3b30;border:3px solid #fff"></div>', rot=-5)
vis_web = f'<div class="a" style="inset:0;background:{INK}"></div>' + laptop("itecx", 26, 76, 268, 0)
page("02-who", f'''
{head(2, False)}
<div class="a h" style="left:50px;top:112px;font-size:152px;color:{INK};letter-spacing:-.06em;line-height:1">Кто мы</div>
<div class="bar" style="left:56px;top:312px"></div>
<div class="a p1" style="left:56px;top:356px;width:960px;color:{INK}"><span style="font-weight:400">MAZZERU — студия, которая делает</span><br><b>видео, истории и сайты.</b></div>
<div class="a p2" style="left:56px;top:494px;width:900px;color:{INK}">Вы приходите с идеей, а мы придумываем,<br>как её показать, и доводим до готового результата.</div>
{mini_card(32, iy-100, cw, ch, vis_ai, "video", "ИИ-видео", "Реклама, клипы, презентации, визуал", 300)}
{mini_card(380, iy-100, cw, ch, vis_shoot, "person", "Съёмка", "Reels, контент для бизнеса и личных брендов", 300)}
{mini_card(728, iy-100, cw, ch, vis_web, "grid", "Сайты", "Лендинги, сайты-визитки, страницы проектов", 300)}
{foot("IDEA<br>PROCESS<br>RESULT", "Ваша идея<br>Наше решение<br>Реальный результат", False, 2)}
''', PAPER)

# ================= 03 ИИ-ВИДЕО =================
page("03-ai", f'''
{head(3)}
<div class="a h" style="left:50px;top:118px;font-size:120px;color:{LIME};letter-spacing:-.06em;white-space:nowrap">AI<span style="color:#fff">-ВИДЕО</span></div>
<div class="bar" style="left:56px;top:262px"></div>
<div class="a p1" style="left:56px;top:300px;width:590px;color:#fff;font-size:29px"><b>Создаём ролики с помощью нейросетей:</b> рекламу, презентации продуктов, атмосферные клипы и визуал для брендов.</div>
<div class="a p2" style="left:56px;top:486px;width:590px;color:#fff;font-size:22px">Не нужны съёмочная группа, локация и актёры, а картинка выглядит как кино. Подходит, когда нужно быстро и нестандартно.</div>
<div class="a h" style="left:52px;top:640px;font-size:124px;color:{LIME};letter-spacing:-.05em">БЕЗ</div>
<div class="a" style="left:316px;top:638px;height:160px;border-left:2px solid rgba(231,255,0,.5);padding-left:26px;color:#fff">
  <div style="display:flex;gap:16px;align-items:center;height:53px">{ico("team", "#fff", 36)}<span style="font:500 25px I">съёмочной группы</span></div>
  <div style="display:flex;gap:16px;align-items:center;height:53px">{ico("pin", "#fff", 36)}<span style="font:500 26px I">локаций</span></div>
  <div style="display:flex;gap:16px;align-items:center;height:53px">{ico("person", "#fff", 36)}<span style="font:500 26px I">актёров</span></div></div>
{frame("sun", 700, 280, 324, 230, "AI CINEMATIC<br>STORY", "00:08", 11)}
{frame("city", 700, 530, 324, 230, "PRODUCT<br>VIDEO", "00:06", 12)}
{frame("wave", 56, 850, 330, 240, "BRAND<br>VISUAL", "00:07", 13, small=True)}
{frame("planet", 410, 800, 614, 290, "CREATIVE<br>CONCEPT", "00:10", 14)}
{foot("IDEA<br>AI TOOLS<br>UNLIMITED VISUALS", "Больше возможностей<br>для ваших идей", True, 3)}
''', INK)

# ================= 04 СЪЁМКА =================
def chip(x, y, w, h, icon, t1, t2):
    return f'''<div class="chip" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;color:#fff">{ico(icon, LIME, 52)}
      <div style="margin-top:14px;font:800 22px/1.15 U;letter-spacing:-.03em;text-transform:uppercase">{t1}</div><div style="font:400 20px/1.25 I;opacity:.8;margin-top:4px">{t2}</div></div>'''

def scard(x, y, w, h, kind, seed, t1, t2):
    return f'''<div class="card" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;background:{INK}">
      <div class="a" style="inset:0">{scene(kind, 400, int(400*h/w), seed)}</div>
      <div class="fshade"></div>
      <div class="a" style="left:22px;bottom:20px;color:#fff"><div style="font:800 19px/1.1 U;letter-spacing:-.03em;text-transform:uppercase">{t1}</div><div style="font:400 20px/1.2 I;opacity:.85;margin-top:5px">{t2}</div></div></div>'''

page("04-shoot", f'''
<div class="a" style="left:0;top:0;width:1080px;height:600px;opacity:.9">{scene("tower", 1080, 600, 21)}</div>
<div class="a" style="left:0;top:0;width:1080px;height:620px;background:linear-gradient(to bottom, rgba(11,11,15,.15), {INK} 96%)"></div>
{head(4)}
{phone(820, 96, 170, scene("city", 300, 620, 22) + f'<div class="a" style="left:50%;bottom:26px;margin-left:-16px;width:32px;height:32px;border-radius:50%;background:#ff3b30;border:4px solid #fff"></div>', rot=7)}
<div class="a h" style="left:50px;top:150px;font-size:118px;color:#fff;letter-spacing:-.065em">Съёмка</div>
<div class="a h" style="left:54px;top:290px;font-size:56px;color:{LIME}">в Астане</div>
<div class="bar" style="left:56px;top:378px"></div>
<div class="a p1" style="left:56px;top:418px;width:760px;color:#fff;font-size:30px"><b>Снимаем рилсы, рекламные ролики, контент для бизнеса</b> и личных брендов.</div>
<div class="a p2" style="left:56px;top:566px;width:720px;color:#fff;font-size:24px">Продумываем идею, кадр и монтаж. Вы получаете готовое видео, а не сырой материал.</div>
{chip(56, 668, 300, 168, "reels", "Reels", "для бизнеса")}
{chip(380, 668, 300, 168, "cup", "Заведения", "и услуги")}
{chip(704, 668, 300, 168, "person", "Личные", "бренды")}
{scard(40, 870, 320, 270, "sun", 31, "Мероприятия", "Динамичные рилсы")}
{scard(380, 870, 320, 270, "wave", 32, "Бизнес", "Рекламные ролики")}
{scard(720, 870, 320, 270, "city", 33, "Недвижимость", "Фото и видео объекта")}
{foot("IDEA<br>SHOOT<br>EDIT<br>RESULT", "Продумываем<br>Снимаем<br>Монтируем", True, 4)}
''', INK)

# ================= 05 САЙТЫ =================
def dcard(x, y, w, h, icon, t1, t2, vis):
    return f'''<div class="card" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;background:{INK};color:#fff">
      <div class="a" style="left:22px;top:22px">{ico(icon, LIME, 44)}</div>
      <div class="a h" style="left:22px;top:78px;font-size:22px;line-height:1.08">{t1}</div>
      <div class="a" style="left:22px;top:146px;width:{w-40}px;font:400 20px/1.28 I;opacity:.85">{t2}</div>{vis}</div>'''

page("05-web", f'''
{head(5, False)}
<div class="a" style="right:-140px;top:140px;width:640px;height:400px;background:{LIME};border-radius:50%"></div>
{laptop("itecx", 650, 200, 380, -6)}
{phone(920, 262, 120, f'<img src="{IMG}/projects/smarthub.webp" style="width:100%;height:100%;object-fit:cover;object-position:30% top">', rot=5)}
<div class="a h" style="left:50px;top:112px;font-size:122px;color:{INK};letter-spacing:-.06em;line-height:1">Сайты</div>
<div class="a h" style="left:54px;top:258px;font-size:38px;color:{INK};letter-spacing:-.05em">под вашу задачу</div>
<div class="bar" style="left:56px;top:330px"></div>
<div class="a p1" style="left:56px;top:366px;width:520px;color:{INK};font-size:28px"><b>Делаем сайты под вашу задачу:</b> лендинг для услуги, сайт-визитку для эксперта, страницу для проекта.</div>
<div class="a p2" style="left:56px;top:552px;width:520px;color:{INK};font-size:22px">Продумываем структуру и дизайн, чтобы сайт был понятным и вёл клиента к заявке.</div>
{dcard(36, 660, 316, 490, "grid", "Лендинг", "Для услуг и продуктов. Понятно, убедительно, с фокусом на заявку.", shot("ascora", 22, 290, 272, 176, 14))}
{dcard(382, 660, 316, 490, "person", "Сайт-визитка", "Для экспертов и компаний. Упаковывает вас и вызывает доверие.", shot("onerlab", 22, 290, 272, 176, 14))}
{dcard(728, 660, 316, 490, "doc", "Страница проекта", "Для мероприятий, продуктов и отдельных инициатив.", shot("astanatechcup", 22, 290, 272, 176, 14))}
{foot("IDEA<br>STRUCTURE<br>DESIGN<br>RESULT", "Сайт, который ведёт<br>к действию.", False, 5)}
''', PAPER)

# ================= 06 CTA =================
def step(x, y, w, h, n, icon, t):
    return f'''<div class="a" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;border:2px solid {INK};border-radius:28px;padding:20px;color:{INK}">
      <div class="h" style="font-size:54px;letter-spacing:-.06em;line-height:1">{n}</div>
      <div class="a" style="right:20px;top:24px"><svg viewBox="0 0 24 24" width="36" height="36" fill="none" stroke="{INK}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M4 12h15M14 6l6 6-6 6"/></svg></div>
      <div style="margin-top:14px;width:58px;height:58px;border-radius:16px;background:{INK};display:grid;place-items:center">{ico(icon, LIME, 34)}</div>
      <div style="margin-top:14px;font:600 24px/1.2 I">{t}</div></div>'''

dm = f'''<div class="a" style="left:0;right:0;top:64px;text-align:center;color:#fff;font:600 15px I;opacity:.8">New Message</div>
 <div class="a" style="left:50%;top:104px;margin-left:-44px;width:88px;height:88px;border-radius:50%;background:{LIME};display:grid;place-items:center">{mark(INK, LIME, 60)}</div>
 <div class="a" style="left:0;right:0;top:204px;text-align:center;color:#fff;font:600 18px I">mazzeru.studio</div>
 <div class="a" style="left:16px;right:16px;top:280px;height:52px;border-radius:26px;background:#222;color:#bbb;font:400 15px/52px I;padding-left:18px">Привет! У меня есть идея…</div>
 <div class="a" style="right:24px;top:288px;width:36px;height:36px;border-radius:50%;background:{LIME}"></div>
 <div class="a" style="left:0;right:0;top:360px;height:300px;background:#151519"></div>'''
keys = ""
for r_i, row in enumerate(["йцукенгшщзх", "фывапролдж", "ячсмитьбю"]):
    for k_i, ch_ in enumerate(row):
        keys += f'<div class="a" style="left:{10 + k_i*27.5 + r_i*10}px;top:{376 + r_i*52}px;width:23px;height:40px;border-radius:7px;background:#3a3a42;color:#fff;font:500 16px/40px I;text-align:center">{ch_}</div>'
dm += keys

page("06-cta", f'''
{head(6, False)}
{phone(740, 92, 290, dm, rot=6, hm=1.78)}
<div class="a h" style="left:48px;top:118px;font-size:96px;color:{INK};letter-spacing:-.06em;line-height:1.02">Есть<br>идея?</div>
<div class="a h" style="left:48px;top:328px;font-size:82px;color:{INK};letter-spacing:-.06em;line-height:1.02">Давайте<br>создадим.</div>
<div class="bar" style="left:56px;top:548px;background:{INK}"></div>
<div class="a p1" style="left:56px;top:590px;width:520px;color:{INK};font-size:28px">Снимаем в Астане, остальное делаем онлайн.</div>
{step(40, 720, 312, 250, "01", "chat", "Пишете идею в Direct")}
{step(368, 720, 312, 250, "02", "doc", "Обсуждаем формат, сроки и стоимость")}
{step(696, 720, 312, 250, "03", "video", "Делаем, показываем, вносим правки")}
<div class="a" style="left:40px;top:988px;width:600px;height:106px;background:{INK};border-radius:30px;color:#fff">
  <div class="a" style="left:26px;top:30px">{ico("pin", LIME, 50)}</div>
  <div class="a" style="left:96px;top:26px"><div class="lab" style="font-size:16px;color:#fff;letter-spacing:.1em;line-height:1.2;font-weight:700">АСТАНА</div><div style="font:400 15px/1.3 I;opacity:.8;letter-spacing:.06em">СЪЁМКА НА ЛОКАЦИИ</div></div>
  <div class="a" style="left:300px;top:22px;height:68px;border-left:2px solid rgba(255,255,255,.3)"></div>
  <div class="a" style="left:326px;top:30px">{ico("globe", LIME, 50)}</div>
  <div class="a" style="left:394px;top:26px"><div class="lab" style="font-size:16px;color:#fff;letter-spacing:.1em;line-height:1.2;font-weight:700">ONLINE</div><div style="font:400 15px/1.3 I;opacity:.8;letter-spacing:.06em">ПРОЕКТЫ ЛЮБОЙ СЛОЖНОСТИ</div></div></div>
<div class="a" style="left:40px;top:1112px;width:1000px;height:106px;background:{INK};border-radius:30px;color:#fff">
  <div class="a" style="left:30px;top:28px">{ico("send", "#fff", 56)}</div>
  <div class="a" style="left:118px;top:20px;font:400 20px I;opacity:.85">Обсудим вашу идею в Direct</div>
  <div class="a h" style="left:118px;top:48px;font-size:38px;letter-spacing:-.04em;text-transform:none">@mazzeru.studio</div>
  <div class="a" style="right:26px;top:22px;width:68px;height:68px;border-radius:50%;background:{LIME};display:grid;place-items:center"><svg viewBox="0 0 24 24" width="34" height="34" fill="none" stroke="{INK}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 12h15M14 6l6 6-6 6"/></svg></div></div>
{foot("IDEA<br>PROCESS<br>RESULT", "Ваша идея<br>Наше решение<br>Реальный результат", False, 6).replace("bottom:44px", "bottom:14px").replace("height:90px", "height:70px")}
''', LIME)

