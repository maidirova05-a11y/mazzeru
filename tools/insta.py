"""Шаблоны для Instagram в стиле Mazzeru → PNG."""
import os
import topng

B = r"C:\Users\USER\OneDrive\Desktop\Mazzeru\brand"
OUT = B + r"\instagram"
os.makedirs(OUT, exist_ok=True)
F = "file:///" + (B + r"\fonts").replace("\\", "/")
IMG = "file:///" + r"C:\Users\USER\OneDrive\Desktop\Mazzeru\assets\img".replace("\\", "/")

import brand_mark as BM
Z = lambda c="mk", bg="#0047FF", z="#fff": BM.svg_mark(bg, z, c)
LOGO = lambda col="#0047FF", bg="#0047FF", z="#fff": f'<div class="logo">{Z("mk", bg, z)}<span style="color:{col}">mazzeru</span></div>'

CSS = f"""
@font-face {{ font-family: U; src: url('{F}/Unbounded-ExtraBold.ttf'); font-weight: 800; }}
@font-face {{ font-family: I; src: url('{F}/InterTight.ttf'); font-weight: 100 900; }}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html, body {{ width: 100%; height: 100%; overflow: hidden; }}
body {{ font-family: I, sans-serif; -webkit-font-smoothing: antialiased; position: relative; }}
.logo {{ display: flex; align-items: center; gap: 18px; }}
.logo .mk {{ width: 70px; height: 70px; }}
.logo span {{ font: 800 58px/1 U; letter-spacing: -0.06em; }}
.label {{ font: 700 26px/1 I; letter-spacing: .32em; text-transform: uppercase; }}
.h {{ font: 900 170px/.9 I; letter-spacing: -0.045em; text-transform: uppercase; }}
.pill {{ display: inline-flex; align-items: center; gap: 22px; height: 96px; padding: 0 16px 0 44px; border-radius: 99px; font: 800 26px/1 I; letter-spacing: .2em; text-transform: uppercase; }}
.pill i {{ width: 64px; height: 64px; border-radius: 50%; display: grid; place-items: center; font-style: normal; font-size: 30px; }}
.circle {{ position: absolute; border-radius: 50%; }}
.bigmark svg {{ width: 100%; height: 100%; display: block; }}
"""


def page(name, w, h, body, bg):
    html = os.path.join(topng.TMP, name + ".html")
    open(html, "w", encoding="utf-8").write(
        f"<html><head><meta charset='utf-8'><style>{CSS}body{{background:{bg};width:{w}px;height:{h}px}}</style></head><body>{body}</body></html>")
    out = os.path.join(OUT, name + ".png")
    topng.render(html, out, w, h, crop_alpha=False)
    print(name)


# 1. Аватарка профиля 1080×1080 (Instagram обрезает в круг)
page("ig-avatar", 1080, 1080, f'<div style="position:absolute;inset:0;display:grid;place-items:center">{Z("", "#0047FF", "#fff").replace("<svg ", "<svg style=\"width:640px;height:640px\" ")}</div>', "#0047FF")

# 2. Обложки «Актуального» 1080×1920 (видна центральная окружность)
ICONS = {
    "ai": '<path d="M12 2l2.2 6.3L21 10l-6.8 1.9L12 18l-2.2-6.1L3 10l6.8-1.7z" fill="currentColor"/><path d="M19 15l.8 2.2L22 18l-2.2.8L19 21l-.8-2.2L16 18l2.2-.8z" fill="currentColor"/>',
    "web": '<rect x="2.5" y="4" width="19" height="16" rx="2.5" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="M2.5 9h19M9 14l-2 1.5L9 17M15 14l2 1.5-2 1.5" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>',
    "mobile": '<rect x="6" y="2.5" width="12" height="19" rx="3" fill="none" stroke="currentColor" stroke-width="1.8"/><circle cx="12" cy="9" r="2.6" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="M10.5 18h3" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>',
    "price": '<path d="M4 12V4h8l8 8-8 8z" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/><circle cx="8.5" cy="8.5" r="1.5" fill="currentColor"/>',
    "team": '<circle cx="9" cy="8" r="3.5" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="M2.5 20c.8-3.6 3.4-5.5 6.5-5.5s5.7 1.9 6.5 5.5M16 4.8a3.5 3.5 0 0 1 0 6.4M18 14.8c1.9.7 3.1 2.4 3.5 5.2" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>',
    "reviews": '<path d="M4 5h16v11H8l-4 4z" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/><path d="m12 7.5.9 1.9 2.1.3-1.5 1.4.4 2.1-1.9-1-1.9 1 .4-2.1-1.5-1.4 2.1-.3z" fill="currentColor"/>',
}
HL = [("ai", "#0047FF", "#E7FF00"), ("web", "#0B0B0F", "#E7FF00"), ("mobile", "#E7FF00", "#0047FF"),
      ("price", "#0047FF", "#fff"), ("team", "#FAF8F2", "#0047FF"), ("reviews", "#E7FF00", "#0B0B0F")]
for k, bg, fg in HL:
    page(f"highlight-{k}", 1080, 1920,
         f'<div style="position:absolute;inset:0;display:grid;place-items:center;color:{fg}"><svg viewBox="0 0 24 24" style="width:420px;height:420px">{ICONS[k]}</svg></div>', bg)

# 3. Пост-обложка (анонс) 1080×1350
page("post-1-headline", 1080, 1350, f'''
<div class="circle" style="width:600px;height:600px;background:#0047FF;right:-190px;bottom:-60px"></div>
<div class="circle" style="width:380px;height:380px;background:#E7FF00;right:250px;bottom:-230px"></div>
<div class="bigmark" style="position:absolute;right:150px;bottom:360px;width:170px;height:170px;transform:rotate(-12deg);filter:drop-shadow(0 20px 30px rgba(0,30,120,.35))">{Z("", "#fff", "#0047FF")}</div>
<div style="position:absolute;left:80px;top:80px">{LOGO()}</div>
<div class="label" style="position:absolute;left:84px;top:250px;color:#0047FF">Digital-студия · Астана</div>
<div class="h" style="position:absolute;left:76px;top:320px;color:#0B0B0F;font-size:136px">Идеи<br>в<br><span style="color:#0047FF">движение</span></div>
<div class="label" style="position:absolute;left:84px;bottom:230px;color:#0B0B0F">ИИ-видео / Сайты / Мобилография</div>
<div class="pill" style="position:absolute;left:80px;bottom:80px;background:#E7FF00;color:#0B0B0F">Давайте создадим<i style="background:#0B0B0F;color:#E7FF00">→</i></div>
''', "#FAF8F2")

# 4. Пост-кейс 1080×1350
page("post-2-case", 1080, 1350, f'''
<div class="circle" style="width:420px;height:420px;background:#E7FF00;right:-120px;top:-120px"></div>
<div style="position:absolute;left:80px;top:80px">{LOGO("#fff", "#fff", "#0047FF")}</div>
<div style="position:absolute;left:80px;right:80px;top:230px;border-radius:36px;overflow:hidden;background:#fff;box-shadow:0 40px 80px -30px rgba(0,0,40,.6);transform:rotate(-2deg)">
  <div style="display:flex;gap:10px;padding:18px 22px;background:#F0EDE3"><i style="width:16px;height:16px;border-radius:50%;background:#ccc"></i><i style="width:16px;height:16px;border-radius:50%;background:#ccc"></i><i style="width:16px;height:16px;border-radius:50%;background:#ccc"></i></div>
  <img src="{IMG}/projects/itecx.webp" style="display:block;width:100%;height:500px;object-fit:cover;object-position:top">
</div>
<div class="label" style="position:absolute;left:84px;top:900px;color:#E7FF00">Кейс · Сайт под ключ</div>
<div class="h" style="position:absolute;left:78px;top:950px;color:#fff;font-size:150px">ITECX</div>
<div style="position:absolute;left:84px;bottom:90px;right:80px;display:flex;gap:14px">
  <span class="pill" style="height:70px;padding:0 30px;background:#E7FF00;color:#0B0B0F;font-size:22px">KZ · RU · EN</span>
  <span class="pill" style="height:70px;padding:0 30px;background:rgba(255,255,255,.14);color:#fff;font-size:22px;border:2px solid rgba(255,255,255,.3)">3D-глобус</span>
  <span class="pill" style="height:70px;padding:0 30px;background:rgba(255,255,255,.14);color:#fff;font-size:22px;border:2px solid rgba(255,255,255,.3)">Регистрация</span>
</div>
''', "#0047FF")

# 5. Пост-совет (карусель) 1080×1350
page("post-3-tips", 1080, 1350, f'''
<div style="position:absolute;left:80px;top:80px">{LOGO("#0B0B0F", "#0B0B0F", "#E7FF00")}</div>
<div class="label" style="position:absolute;right:80px;top:104px;color:#0B0B0F">01 / 05</div>
<div class="h" style="position:absolute;left:76px;top:300px;color:#0B0B0F;font-size:150px">3 ошибки<br>в&nbsp;Reels</div>
<div style="position:absolute;left:80px;right:80px;top:680px;display:grid;gap:22px">
  <div style="display:flex;gap:26px;align-items:center;background:#0B0B0F;color:#FAF8F2;border-radius:32px;padding:34px 36px;font:700 38px/1.2 I"><b style="font:900 64px/1 I;color:#E7FF00">01</b>Нет крючка в первые 2 секунды</div>
  <div style="display:flex;gap:26px;align-items:center;background:#0047FF;color:#fff;border-radius:32px;padding:34px 36px;font:700 38px/1.2 I"><b style="font:900 64px/1 I;color:#E7FF00">02</b>Серый цвет без цветокора</div>
  <div style="display:flex;gap:26px;align-items:center;background:#FAF8F2;color:#0B0B0F;border-radius:32px;padding:34px 36px;font:700 38px/1.2 I"><b style="font:900 64px/1 I;color:#0047FF">03</b>Нет призыва к действию</div>
</div>
<div class="label" style="position:absolute;left:84px;bottom:90px;color:#0B0B0F">Листай →</div>
''', "#E7FF00")

# 6. Сторис 1080×1920
page("story-template", 1080, 1920, f'''
<div class="circle" style="width:1000px;height:1000px;background:#0047FF;left:40px;top:560px;overflow:hidden">
  <img src="{IMG}/hero/mobile.webp" style="width:100%;height:100%;object-fit:cover;opacity:.95">
</div>
<div class="circle" style="width:560px;height:560px;background:#E7FF00;left:-160px;bottom:-120px;z-index:-1"></div>
<div style="position:absolute;left:80px;top:140px">{LOGO()}</div>
<div class="h" style="position:absolute;left:76px;top:300px;color:#0B0B0F;font-size:140px">Новый<br><span style="color:#0047FF">кейс</span></div>
<div class="pill" style="position:absolute;right:80px;bottom:200px;background:#E7FF00;color:#0B0B0F">Смотреть<i style="background:#0B0B0F;color:#E7FF00">→</i></div>
''', "#FAF8F2")
