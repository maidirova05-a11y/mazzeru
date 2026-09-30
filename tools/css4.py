p = r'C:\Users\USER\OneDrive\Desktop\Mazzeru\assets\css\style.css'
s = open(p, encoding='utf-8').read()


def between(start, end):
    a = s.index(start)
    b = s.index(end, a)
    return a, b


# 1) интро + шторка
a, b = between('.intro {', '/* Прогресс прокрутки и курсор */')
s = s[:a] + '''.intro {
  position: fixed; inset: 0; z-index: 300;
  display: grid; place-items: center;
  background: var(--blue); color: #fff;
  overflow: hidden;
  will-change: transform;
  animation: introFail .4s 3s forwards;   /* если скрипты не загрузились */
}
@keyframes introFail { to { transform: translateY(-100%); visibility: hidden; } }
.intro-seen .intro { display: none; }
.intro-stage { position: relative; z-index: 2; display: flex; align-items: center; gap: clamp(12px, 1.8vw, 24px); }
.intro-mark { width: clamp(72px, 10vw, 140px); height: auto; will-change: transform; }
.intro-mark .mk-bg { fill: #fff; }
.intro-mark .mk-z { fill: var(--blue); }
.intro-mark .mk-cut { stroke: #fff; }
.intro-word { display: flex; font-family: var(--f-logo); font-weight: 800; font-size: clamp(46px, 10vw, 150px); letter-spacing: -0.06em; line-height: 1; overflow: hidden; padding: .06em .02em .1em; }
.intro-word span { display: inline-block; will-change: transform; }
.intro-tag { position: absolute; z-index: 2; left: 50%; bottom: 8vh; transform: translateX(-50%); white-space: nowrap; color: rgba(255,255,255,.75); }
.intro-slash { position: absolute; z-index: 1; left: -20%; top: 50%; width: 140%; height: 18vh; margin-top: -9vh; background: var(--yellow); transform: rotate(-32deg) scaleX(0); transform-origin: left center; will-change: transform; }

/* Переход между страницами — на CSS, без зависаний */
.wipe { position: fixed; inset: 0; z-index: 250; display: grid; place-items: center; background: var(--blue); transform: translateY(100%); pointer-events: none; }
.wipe svg { width: 76px; height: 76px; animation: wipeSpin 1.2s var(--ease) infinite; }
@keyframes wipeSpin { 0% { transform: rotate(0) scale(.9); } 50% { transform: rotate(180deg) scale(1.05); } 100% { transform: rotate(360deg) scale(.9); } }
.wipe .mk-bg { fill: #fff; } .wipe .mk-z { fill: var(--blue); } .wipe .mk-cut { stroke: #fff; }
.wipe.in { transform: none; transition: transform .45s cubic-bezier(.7, 0, .2, 1); pointer-events: auto; }
.wiping .wipe { transform: none; }
.wiping .wipe.out { transform: translateY(-100%); transition: transform .6s cubic-bezier(.7, 0, .2, 1); }

''' + s[b:]

# 2) подпись hero
a, b = between('.hero-eyebrow {', '.hero h1 {')
s = s[:a] + '''.hero-eyebrow { display: inline-flex; align-items: center; gap: 10px; margin-bottom: 26px; font-size: 15px; font-weight: 600; color: var(--muted); }
.hero-eyebrow .mini svg { width: 24px; height: 24px; display: block; }
.hero-eyebrow .sep { width: 18px; height: 1.5px; background: var(--line-2); }
.hero-eyebrow .clock { font-variant-numeric: tabular-nums; color: var(--ink); }
.crumbs a { color: var(--muted); transition: color .3s; }
.crumbs a:hover { color: var(--blue); }
.crumbs > span:last-child { color: var(--ink); }
''' + s[b:]

# 3) круг и «студийная консоль»
a, b = between('.hero-circle {', '/* ---------- Бегущие ленты')
s = s[:a] + '''.hero-circle { position: absolute; inset: 6%; border-radius: 50%; overflow: hidden; background: radial-gradient(circle at 32% 28%, #3a78ff, var(--blue) 55%, #0033c4); }
.ring { position: absolute; border-radius: 50%; border: 1.5px dashed rgba(255,255,255,.28); }
.ring.r1 { inset: 12%; animation: spin 40s linear infinite; }
.ring.r2 { inset: 26%; border-style: solid; border-color: rgba(255,255,255,.14); }
.ring.r3 { inset: 38%; border-color: rgba(231,255,0,.5); animation: spin 22s linear infinite reverse; }
.ring-text { position: absolute; inset: 0; width: 100%; height: 100%; animation: spin 30s linear infinite; }
.ring-text text { fill: rgba(255,255,255,.85); font: 800 9.2px var(--f-display); letter-spacing: .32em; }
.core { position: absolute; left: 50%; top: 50%; width: 18%; translate: -50% -50%; animation: float 6s ease-in-out infinite; }
.core svg { width: 100%; height: auto; display: block; }
.core .mk-bg { fill: #fff; } .core .mk-z { fill: var(--blue); } .core .mk-cut { stroke: #fff; }
@keyframes spin { to { rotate: 360deg; } }
.hero-sun { position: absolute; width: 50%; aspect-ratio: 1; border-radius: 50%; background: var(--yellow); left: -4%; bottom: -12%; z-index: -1; }
@keyframes float { 50% { transform: translateY(-10px); } }

/* Карточки «студийной консоли» */
.vis { position: absolute; z-index: 3; border-radius: 18px; box-shadow: 0 30px 60px -28px rgba(0, 20, 90, .55); will-change: transform; }
.vis-prompt { left: -6%; top: 14%; width: 50%; padding: 16px; background: var(--surface); color: var(--ink); animation: float 7s ease-in-out infinite; }
.vp-head { display: flex; align-items: center; gap: 8px; font-size: 12px; font-weight: 800; letter-spacing: .08em; text-transform: uppercase; margin-bottom: 10px; }
.vp-ico { width: 26px; height: 26px; border-radius: 8px; display: grid; place-items: center; background: var(--blue); color: var(--yellow); }
.vp-ico svg { width: 15px; height: 15px; }
.vp-live { margin-left: auto; width: 8px; height: 8px; border-radius: 50%; background: #1ec26b; box-shadow: 0 0 0 3px rgba(30,194,107,.2); }
.vp-text { font-size: 14px; line-height: 1.4; min-height: 3.9em; font-weight: 500; }
.caret { display: inline-block; width: 2px; height: 1.05em; margin-left: 2px; vertical-align: -2px; background: var(--blue); animation: blink 1s steps(1) infinite; }
@keyframes blink { 50% { opacity: 0; } }
.vp-bar { height: 6px; border-radius: 6px; background: var(--surface-2); overflow: hidden; margin: 10px 0 6px; }
.vp-bar i { display: block; height: 100%; width: 0; border-radius: 6px; background: linear-gradient(90deg, var(--blue), #6e9bff); }
.vp-foot { display: flex; justify-content: space-between; font-size: 11.5px; font-weight: 700; color: var(--muted); }
.vp-foot b { color: var(--ink); font-variant-numeric: tabular-nums; }
.vp-frames { display: grid; grid-template-columns: repeat(4, 1fr); gap: 6px; margin-top: 10px; }
.vp-frames i { aspect-ratio: 1; border-radius: 8px; background: var(--surface-2); transition: background .5s; }
.vp-frames i.on:nth-child(1) { background: linear-gradient(135deg, #ffb46b, #ff6b8b); }
.vp-frames i.on:nth-child(2) { background: linear-gradient(135deg, #6e9bff, #0047ff); }
.vp-frames i.on:nth-child(3) { background: linear-gradient(135deg, #e7ff00, #7bd88f); }
.vp-frames i.on:nth-child(4) { background: linear-gradient(135deg, #0b0b0f, #3a3a55); }

.vis-phone { right: 2%; top: 4%; width: 30%; aspect-ratio: 9 / 18; padding: 6px; border-radius: 26px; background: #0b0b0f; animation: float 8s ease-in-out infinite -2s; }
.ph-screen { position: relative; width: 100%; height: 100%; border-radius: 21px; overflow: hidden; background: #111; color: #fff; }
.ph-screen > img { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; object-position: top; }
.ph-footage { position: absolute; inset: 0; background: linear-gradient(160deg, #0b0b0f, #0047ff 35%, #6e9bff 55%, #e7ff00 80%, #ff8a4c); background-size: 100% 300%; animation: footage 7s ease-in-out infinite alternate; }
.ph-footage::after { content: ""; position: absolute; left: 20%; right: 20%; bottom: 18%; height: 34%; border-radius: 50% 50% 0 0; background: rgba(11,11,15,.55); filter: blur(2px); }
@keyframes footage { to { background-position: 0 100%; } }
.ph-top { position: absolute; top: 10px; left: 10px; right: 10px; display: flex; justify-content: space-between; font-size: 10px; font-weight: 800; letter-spacing: .06em; font-variant-numeric: tabular-nums; }
.rec { display: inline-flex; align-items: center; gap: 4px; }
.rec i { width: 7px; height: 7px; border-radius: 50%; background: #ff3b3b; animation: blink 1.2s steps(1) infinite; }
.ph-play { position: absolute; left: 50%; top: 50%; translate: -50% -50%; width: 40px; height: 40px; border-radius: 50%; display: grid; place-items: center; background: rgba(255,255,255,.25); backdrop-filter: blur(6px); }
.ph-play svg { width: 16px; height: 16px; margin-left: 2px; }
.ph-bottom { position: absolute; left: 10px; right: 10px; bottom: 16px; display: flex; justify-content: space-between; align-items: center; font-size: 11px; }
.ph-like em { font-style: normal; font-weight: 800; }
.ph-prog { position: absolute; left: 10px; right: 10px; bottom: 8px; height: 3px; border-radius: 3px; background: rgba(255,255,255,.3); overflow: hidden; }
.ph-prog i { display: block; height: 100%; width: 40%; background: var(--yellow); animation: prog 6s linear infinite; }
@keyframes prog { from { width: 0; } to { width: 100%; } }

.vis-browser { left: 8%; bottom: 2%; width: 58%; overflow: hidden; background: var(--surface); rotate: -3deg; animation: float 9s ease-in-out infinite -4s; }
.browser-bar { display: flex; align-items: center; gap: 6px; padding: 9px 12px; background: var(--surface-2); }
.browser-bar i { width: 8px; height: 8px; border-radius: 50%; background: var(--line-2); }
.browser-bar .url { margin-left: 10px; padding: 2px 10px; border-radius: 6px; background: var(--surface); font-size: 10px; font-weight: 700; color: var(--muted); }
.vb-body { position: relative; display: grid; grid-template-columns: 1.2fr 1fr; gap: 10px; padding: 12px; aspect-ratio: 16 / 9; }
.vb-body > img { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; object-position: top; }
.sk { display: flex; flex-direction: column; gap: 6px; }
.sk b { display: block; border-radius: 4px; background: var(--surface-2); position: relative; overflow: hidden; }
.sk b::after, .sk-img::after { content: ""; position: absolute; inset: 0; background: linear-gradient(90deg, transparent, rgba(255,255,255,.6), transparent); translate: -100% 0; animation: shimmer 2.4s ease-in-out infinite; }
@keyframes shimmer { to { translate: 100% 0; } }
.sk-nav { height: 6px; width: 40%; }
.sk-h { height: 12px; background: var(--ink) !important; }
.sk-h.short { width: 70%; background: var(--blue) !important; }
.sk-l { height: 5px; } .sk-l.short { width: 60%; }
.sk-btn { height: 14px; width: 45%; border-radius: 99px !important; background: var(--yellow) !important; margin-top: auto; }
.sk-img { position: relative; overflow: hidden; border-radius: 8px; background: radial-gradient(circle at 70% 30%, var(--yellow) 0 22%, transparent 23%), var(--blue); }

/* Варианты для страниц услуг */
.hero-visual--ai .vis-prompt { left: 0; top: 26%; width: 62%; }
.hero-visual--ai .vis-phone { right: 4%; top: 2%; width: 28%; }
.hero-visual--mobile .vis-phone { right: 10%; top: 2%; width: 40%; }
.hero-visual--mobile .vis-prompt { left: -4%; top: auto; bottom: 10%; width: 46%; }
.hero-visual--web .vis-browser { left: -4%; top: 22%; bottom: auto; width: 84%; rotate: -4deg; }
.hero-visual--web .vis-phone { right: -2%; top: auto; bottom: 0; width: 26%; }

''' + s[b:]

# 4) команда + орбита
a, b = between('/* Команда */', '/* Пакеты */')
s = s[:a] + '''/* Команда: круглые аватары с вращающимся текстом */
.team { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; perspective: 1200px; }
.founder {
  position: relative; overflow: hidden; isolation: isolate;
  display: flex; flex-direction: column; align-items: center; text-align: center; gap: 6px;
  padding: 26px 18px 22px; border-radius: var(--radius);
  background: var(--surface); border: 1px solid var(--line);
  transition: color .5s, border-color .5s;
}
.founder::before { content: ""; position: absolute; z-index: -1; width: 170%; aspect-ratio: 1; left: -35%; top: 100%; border-radius: 50%; background: var(--blue); transition: top .7s var(--ease); }
.founder:hover { color: #fff; border-color: var(--blue); }
.founder:hover::before { top: -35%; }
.f-ava { position: relative; width: 168px; aspect-ratio: 1; margin-bottom: 14px; }
.f-ring { position: absolute; inset: 0; width: 100%; height: 100%; color: var(--blue); animation: spin 18s linear infinite; transition: color .5s; }
.f-ring text { fill: currentColor; font: 800 10.5px var(--f-display); letter-spacing: .28em; text-transform: uppercase; }
.founder:hover .f-ring { color: var(--yellow); }
.f-photo { position: absolute; inset: 17%; border-radius: 50%; overflow: hidden; background: var(--blue); }
.f-photo img { width: 100%; height: 100%; object-fit: cover; object-position: center 22%; transition: transform .8s var(--ease); }
.founder:hover .f-photo img { transform: scale(1.12); }
.f-photo .avatar-ph { width: 100%; height: 100%; display: grid; place-items: center; color: #fff; font: 800 34px var(--f-logo); }
.f-badge { position: absolute; right: 6%; bottom: 8%; width: 40px; height: 40px; border-radius: 50%; display: grid; place-items: center; background: var(--yellow); color: #0b0b0f; box-shadow: 0 6px 16px rgba(0,0,0,.2); transition: transform .5s var(--ease); }
.f-badge svg { width: 18px; height: 18px; }
.founder:hover .f-badge { transform: rotate(-20deg) scale(1.12); }
.founder .chip { margin-bottom: 6px; }
.founder b { font-family: var(--f-display); font-weight: 900; font-size: 18px; line-height: 1.1; letter-spacing: -0.02em; text-transform: uppercase; }
.founder b small { display: block; font-size: 12px; font-weight: 600; letter-spacing: .02em; text-transform: none; opacity: .6; margin-top: 4px; }
.f-role { font-size: 14px; opacity: .75; }
.f-ig { margin-top: 10px; display: inline-flex; align-items: center; gap: 6px; height: 32px; padding: 0 14px 0 10px; border-radius: 999px; font-size: 12.5px; font-weight: 800; background: var(--surface-2); color: var(--ink); transition: background .4s, color .4s; }
.f-ig svg { width: 15px; height: 15px; }
.founder:hover .f-ig { background: var(--yellow); color: #0b0b0f; }

/* ---------- Орбита проектов ---------- */
.orbit { position: relative; height: clamp(560px, 62vw, 780px); border-radius: var(--radius); overflow: hidden; isolation: isolate; touch-action: pan-y;
  background: radial-gradient(ellipse at center, color-mix(in srgb, var(--blue) 10%, var(--bg)) 0, var(--bg) 62%); }
.orbit::before { content: ""; position: absolute; inset: 0; z-index: -1; opacity: .5;
  background-image: radial-gradient(var(--line-2) 1px, transparent 1.2px); background-size: 26px 26px;
  -webkit-mask-image: radial-gradient(ellipse at center, #000 20%, transparent 70%); mask-image: radial-gradient(ellipse at center, #000 20%, transparent 70%); }
.orbit-sphere { position: absolute; left: 50%; top: 50%; width: clamp(160px, 22vw, 270px); aspect-ratio: 1; translate: -50% -50%; z-index: 10; pointer-events: none; }
.os-ball { position: absolute; inset: 0; border-radius: 50%; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 4px; color: #fff;
  background: radial-gradient(circle at 34% 28%, #9bbcff 0, #3a78ff 18%, var(--blue) 48%, #0028a8 78%, #001a6e 100%);
  box-shadow: inset -18px -24px 50px rgba(0, 10, 60, .55), inset 10px 14px 30px rgba(255,255,255,.18), 0 40px 90px -30px rgba(0, 71, 255, .7);
  animation: breathe 5s ease-in-out infinite; }
.os-ball svg { width: 26%; height: auto; margin-bottom: 6px; }
.os-ball .mk-bg { fill: #fff; } .os-ball .mk-z { fill: var(--blue); } .os-ball .mk-cut { stroke: #fff; }
.os-ball b { font: 900 clamp(34px, 4vw, 52px)/1 var(--f-display); letter-spacing: -0.04em; }
.os-ball span { font-size: 11px; font-weight: 800; letter-spacing: .24em; text-transform: uppercase; opacity: .8; }
@keyframes breathe { 50% { transform: scale(1.03); } }
.os-ring { position: absolute; inset: -22% -34%; border-radius: 50%; border: 2px solid var(--yellow); transform: rotateX(74deg) rotateZ(-14deg); }
.os-ring--2 { inset: -44% -60%; border: 1.5px dashed var(--line-2); transform: rotateX(72deg) rotateZ(12deg); }
.orbit-bubble {
  position: absolute; left: 0; top: 0; z-index: 5;
  width: var(--bs, 92px); aspect-ratio: 1; border-radius: 50%; overflow: hidden; padding: 0;
  border: 3px solid var(--c, var(--blue)); background: var(--surface-2);
  box-shadow: 0 14px 30px -12px rgba(0, 20, 90, .5);
  will-change: transform; transition: box-shadow .4s, filter .4s;
}
.orbit-bubble img { width: 100%; height: 100%; object-fit: cover; pointer-events: none; }
.orbit-bubble .ph { position: absolute; inset: 0; padding: 10px; }
.orbit-bubble .ph b { font-size: 10px; }
.orbit-bubble .ph svg { width: 20px; height: 20px; }
.orbit-bubble.b-ai { --c: var(--blue); }
.orbit-bubble.b-mobile { --c: var(--yellow); }
.orbit-bubble.b-web { --c: var(--ink); }
.orbit-bubble.on { box-shadow: 0 0 0 5px color-mix(in srgb, var(--c) 35%, transparent), 0 30px 60px -20px rgba(0, 20, 90, .6); }
.orbit.dim .orbit-bubble:not(.on) { filter: grayscale(.7) opacity(.5); }
.orbit-info {
  position: absolute; z-index: 60; left: 0; top: 0; width: min(340px, 86%);
  padding: 22px; border-radius: 22px; background: var(--surface); border: 1px solid var(--line);
  box-shadow: 0 30px 70px -30px rgba(0, 20, 90, .55);
  opacity: 0; visibility: hidden; transform: translateY(8px); transition: opacity .3s, visibility .3s, transform .4s var(--ease);
}
.orbit-info.show { opacity: 1; visibility: visible; transform: none; }
.orbit-info h3 { font-size: 24px; letter-spacing: -0.03em; margin: 12px 0 8px; }
.orbit-info p { color: var(--muted); font-size: 14.5px; margin-bottom: 12px; }
.orbit-info .proj-meta { margin-bottom: 14px; }
.orbit-info .btn { height: 46px; font-size: 11px; padding-left: 20px; }
.orbit-info .btn .arr { width: 32px; height: 32px; }
.orbit-hint { position: absolute; left: 50%; bottom: 18px; translate: -50% 0; z-index: 2; font-size: 13px; font-weight: 600; color: var(--muted); white-space: nowrap; }

''' + s[b:]

# 5) адаптив
s = s.replace("  .team { grid-template-columns: repeat(2, 1fr); }\n  .member:last-child:nth-child(4n+1) { grid-column: auto; aspect-ratio: 4 / 5; }\n  .member:last-child:nth-child(odd) { grid-column: span 2; aspect-ratio: 16 / 10; }\n",
              "  .team { grid-template-columns: repeat(2, 1fr); }\n")
s = s.replace("  .team { grid-template-columns: 1fr; }\n  .member, .member:last-child:nth-child(odd) { grid-column: auto; aspect-ratio: 5 / 4; }\n",
              """  .team { grid-template-columns: repeat(2, 1fr); gap: 10px; }
  .founder { padding: 18px 10px 16px; border-radius: 20px; }
  .f-ava { width: 128px; margin-bottom: 8px; }
  .f-badge { width: 32px; height: 32px; }
  .founder b { font-size: 14px; }
  .f-role { font-size: 12.5px; }
  .f-ig { font-size: 11px; padding: 0 10px 0 8px; }
  .orbit { height: 500px; }
  .orbit-info { position: relative; left: auto !important; top: auto !important; width: 100%; margin-top: 14px; display: none; transform: none; }
  .orbit-info.show { display: block; }
  .orbit-hint { font-size: 11.5px; }
""")
s = s.replace("  .hero-badge { font-size: 9.5px; padding: 8px 12px; }\n  .hero-badge.b1 { left: 0; }\n  .hero-badge.b2 { right: 0; }\n",
              """  .vis-prompt { padding: 11px; border-radius: 14px; }
  .vp-head { font-size: 9.5px; margin-bottom: 6px; }
  .vp-ico { width: 20px; height: 20px; }
  .vp-text { font-size: 11px; }
  .vp-frames { gap: 4px; margin-top: 6px; }
  .vis-phone { border-radius: 20px; padding: 4px; }
  .ph-screen { border-radius: 16px; }
  .ph-top, .ph-bottom { font-size: 8.5px; }
  .ph-play { width: 30px; height: 30px; }
""")
open(p, 'w', encoding='utf-8').write(s)
print("ok")
