"""Первый Reels Mazzeru: кто мы, какие проблемы решаем, какие услуги.
9:16, 1080×1920, 30 fps, 80 долей трека (~34.2 с). Палитра Instagram: только лайм + чёрный.
Шрифт: Unbounded (ExtraBold — заголовки, Medium — подписи), мелкий интерфейс — Inter Tight.

Звук: reel_track.wav — начало «Victory Lap Five» (140.15 BPM). Разметка по треку (доли):
  голос: акценты 1, 3, 4–10, 11.5, 12, 14, 16, 18, 19.5 · без голоса 20–33 · заход 34, 35, 35.5
  36 ДРОП 1 · 65 тишина · 66, 67 удары голоса · 68 ДРОП 2 · голос 69.5, 70.5, 72, 74, 76 · 76–80 затухание
Каждое появление текста стоит ровно на доле/акценте; анимации входа короткие (≤0.2 с), чтобы «попадать» в удар.

  python reel.py [preview|sheet]
"""
import math, os, sys, subprocess
import numpy as np, cairo, imageio_ffmpeg
from PIL import Image, ImageEnhance
from render_v1 import Font
from render import (UNB, INT, clamp, prog, expo_out, expo_in, expo_inout, back_out, lerp, rgb, circle, text,
                    mark, zz, kick_shake, grid, pill, rand, YELLOW, INK, WHITE, FPS, OUT_DIR)

W, H = 1080, 1920
U = W
cx, cy = W / 2, H / 2
B = 60 / 140.15                   # точный темп трека
IMG = os.path.normpath(os.path.join(OUT_DIR, "..", "..", "assets", "img"))
FONTS = os.path.normpath(os.path.join(OUT_DIR, "..", "fonts"))
HF = UNB                                                        # Unbounded ExtraBold — заголовки
MF = Font(os.path.join(FONTS, "Unbounded-Medium.ttf"))          # Unbounded Medium — подписи, плашки
GRAY = (0.11, 0.11, 0.15)
TOTAL = 80 * B

# ---------------- разметка по треку ----------------
DROP, BREAK, DROP2 = 36, 65, 68
HK = dict(words=[0, 1, 2, 3], probs=[4, 6, 8, 10], cross=[11.5, 12, 14, 15], fix=[16, 18], sub=19.5,
          serv=[22, 25, 28], key=29.5, out=32, flick=[34, 35, 35.5])
CTA = dict(logo=1.5, items=[2.5, 3, 4], button=6, handle=7)     # в долях от 68
KICKS = [0, 1, 2, 3] + list(range(4, 33, 2)) + [34, 35] + list(range(DROP, BREAK)) + [66, 67] + list(range(DROP2, 80))
SNARES = list(range(DROP + 1, BREAK, 2)) + list(range(DROP2 + 1, 80, 2))
HITS = {0: 1.6, 1: 1.3, 2: 1.3, 3: 1.6, DROP: 2.5, 66: 2.0, 67: 2.0, DROP2: 2.5}
IN = 0.2      # длительность входа текста, с


# ---------------- помощники ----------------
def glitch(ctx, s, size, x, y, t, strength=1.0, color=WHITE, font=HF):
    j = max(0, strength) * size * 0.06
    ox = (rand(int(t * 60), 1) - .5) * 2 * j; oy = (rand(int(t * 60), 2) - .5) * j
    if j > 0.5:
        text(ctx, font, s, size, x - ox, y - oy, WHITE, -0.02, 0.45, anchor="center")
        text(ctx, font, s, size, x + ox, y + oy, YELLOW, -0.02, 0.9, anchor="center")
    text(ctx, font, s, size, x, y, color, -0.02, anchor="center")


_cache = {}
def surf(key, path=None, fn=None):
    if key in _cache: return _cache[key]
    im = Image.open(path).convert("RGB")
    if fn: im = fn(im)
    a = np.array(im.convert("RGBA")); bgra = a[:, :, [2, 1, 0, 3]].copy()
    s = cairo.ImageSurface.create_for_data(bgra, cairo.FORMAT_ARGB32, im.width, im.height)
    _cache[key] = (s, bgra)
    return _cache[key]


def rrect(ctx, x, y, w, h, r):
    r = min(r, w / 2, h / 2)
    ctx.new_sub_path()
    ctx.arc(x + w - r, y + r, r, -math.pi / 2, 0); ctx.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
    ctx.arc(x + r, y + h - r, r, math.pi / 2, math.pi); ctx.arc(x + r, y + r, r, math.pi, 1.5 * math.pi)
    ctx.close_path()


def image(ctx, key, x, y, w, h, r=0, path=None, fn=None, pos=(0.5, 0.5), zoom=1.0, alpha=1.0):
    s, _ = surf(key, path, fn)
    iw, ih = s.get_width(), s.get_height()
    sc = max(w / iw, h / ih) * zoom
    ctx.save(); rrect(ctx, x, y, w, h, r); ctx.clip()
    ox = x - (iw * sc - w) * pos[0]; oy = y - (ih * sc - h) * pos[1]
    ctx.translate(ox, oy); ctx.scale(sc, sc)
    ctx.set_source_surface(s, 0, 0); ctx.get_source().set_filter(cairo.FILTER_GOOD)
    ctx.paint_with_alpha(alpha); ctx.restore()


def fit_size(font, s, max_w, size, tracking=0.0):
    _, w = font.layout(s, size, tracking)
    return size * min(1, max_w / w)


def big(ctx, s, y, color, lt, t0=0.0, max_w=W * 0.86, size=U * 0.15, tracking=-0.02, font=HF):
    """крупный заголовок: выезжает снизу из маски за IN секунд от t0"""
    size = fit_size(font, s, max_w, size, tracking)
    p = expo_out(prog(lt, t0, t0 + IN))
    if p <= 0: return size
    ctx.save(); ctx.rectangle(0, y - size * 1.0, W, size * 1.2); ctx.clip()
    text(ctx, font, s, size, cx, y + size * 1.2 * (1 - p), color, tracking, anchor="center")
    ctx.restore()
    return size


def label(ctx, s, y, color, lt, t0, size=U * 0.026, tracking=0.08):
    p = expo_out(prog(lt, t0, t0 + IN))
    if p <= 0: return
    size = fit_size(MF, s, W * 0.86, size, tracking)
    text(ctx, MF, s, size, cx, y + U * 0.015 * (1 - p), color, tracking, p, anchor="center")


def chips(ctx, items, y, lt, t0, bg, fg, size=U * 0.028, step=0.5):
    """плашки по центру, по одной на каждые step долей от t0"""
    h = size * 2.4; gap = size * 0.55
    ws = [MF.layout(s, size, 0)[1] + size * 1.8 for s in items]
    rows, row, rw = [], [], 0
    for i, w_ in enumerate(ws):
        if row and rw + gap + w_ > W * 0.88: rows.append(row); row, rw = [], 0
        row.append(i); rw += (gap if rw else 0) + w_
    rows.append(row)
    for ri, row in enumerate(rows):
        total = sum(ws[i] for i in row) + gap * (len(row) - 1)
        x = cx - total / 2
        for i in row:
            ts = t0 + i * step * B
            p = back_out(prog(lt, ts, ts + IN), 2.2)
            if p > 0:
                yy = y + ri * (h + gap)
                ctx.save(); ctx.translate(x + ws[i] / 2, yy + h / 2); ctx.scale(p, p); ctx.translate(-(x + ws[i] / 2), -(yy + h / 2))
                pill(ctx, x, yy, ws[i], h, bg)
                text(ctx, MF, items[i], size, x + ws[i] / 2, yy + h * 0.66, fg, 0, anchor="center")
                ctx.restore()
            x += ws[i] + gap
    return len(rows) * (h + gap) - gap


def beat_pop(lt, beats, k=0.05):
    v = 0.0
    for b in beats:
        a = lt - b * B
        if 0 <= a < 0.35: v += math.exp(-a * 12) * k
    return v


def check(ctx, x, y, s, color, alpha=1.0):
    ctx.move_to(x, y - s * 0.35); ctx.line_to(x + s * 0.32, y); ctx.line_to(x + s * 0.9, y - s * 0.75)
    ctx.set_line_width(s * 0.17); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    rgb(ctx, color, alpha); ctx.stroke()


def word_pop(ctx, s, size, x, y, lt, t0, color, font=HF, tracking=-0.02):
    """слово «падает» на удар: 135% → 100% за IN секунд"""
    if lt < t0: return
    p = expo_out(prog(lt, t0, t0 + IN * 0.8))
    sc = lerp(1.35, 1, p)
    _, w = font.layout(s, size, tracking)
    ox, oy = x + w / 2, y - size * 0.36
    ctx.save(); ctx.translate(ox, oy); ctx.scale(sc, sc); ctx.translate(-ox, -oy)
    text(ctx, font, s, size, x, y, color, tracking, min(1, p * 1.5))
    ctx.restore()


# =====================================================================
# 1. ХУК (доли 0–36, вступление трека)
PROBLEMS = ["СКУЧНЫЕ REELS", "САЙТ ИЗ 2015-ГО", "ДОРОГИЕ СЪЁМКИ", "НОЛЬ ЗАЯВОК"]
SERVICES = [("ИИ-ВИДЕО", WHITE), ("МОБИЛОГРАФИЯ", YELLOW), ("САЙТЫ", WHITE)]


def s_hook(ctx, lt):
    rgb(ctx, INK); ctx.paint()
    b = lt / B
    grid(ctx, W, H, U, YELLOW, 0.12, offset=lt * U * 0.05, reveal=clamp(0.3 + b / 16))
    # --- 0–16: заголовок по словам (4 удара) + проблемы (голос) ---
    if b < HK["fix"][0]:
        out = expo_in(prog(lt, (HK["fix"][0] - 0.35) * B, HK["fix"][0] * B))
        ctx.save(); ctx.translate(0, -H * 0.75 * out)
        lines = [("ВАШ", "БИЗНЕС"), ("НЕ", "ЗАМЕЧАЮТ?")]
        k = 0
        for li, (w1, w2) in enumerate(lines):
            size_l = fit_size(HF, w1 + " " + w2, W * 0.86, U * 0.12, -0.02)
            _, tw = HF.layout(w1 + " " + w2, size_l, -0.02)
            _, w1w = HF.layout(w1 + " ", size_l, -0.02)
            x0 = cx - tw / 2; y = H * 0.27 + li * U * 0.15
            col = WHITE if li == 0 else YELLOW
            word_pop(ctx, w1, size_l, x0, y, lt, HK["words"][k] * B, col); k += 1
            word_pop(ctx, w2, size_l, x0 + w1w, y, lt, HK["words"][k] * B, col); k += 1
        ts = U * 0.06
        for i, s_ in enumerate(PROBLEMS):
            t0 = HK["probs"][i] * B
            p = expo_out(prog(lt, t0, t0 + IN))
            if p <= 0: continue
            y = H * 0.5 + i * U * 0.115
            _, w = HF.layout(s_, ts, -0.01)
            x = cx - w / 2 - W * 0.7 * (1 - p)
            tc = HK["cross"][i] * B
            cross = expo_out(prog(lt, tc, tc + 0.12))
            text(ctx, HF, s_, ts, x, y, WHITE, -0.01, 1 - 0.6 * cross)
            if cross > 0:
                ctx.rectangle(x - ts * 0.25, y - ts * 0.42, (w + ts * 0.5) * cross, ts * 0.13); rgb(ctx, YELLOW); ctx.fill()
        ctx.restore()
    # --- 16–32: «МЫ ЭТО / ИСПРАВИМ» (голос) → три услуги (музыка без голоса) ---
    if HK["fix"][0] <= b < HK["out"] + 0.5:
        out = expo_in(prog(lt, HK["out"] * B, (HK["out"] + 0.4) * B))
        ctx.save(); ctx.translate(0, -H * 0.85 * out)
        up = expo_inout(prog(lt, (HK["serv"][0] - 0.5) * B, HK["serv"][0] * B))   # фраза уезжает вверх
        sz = U * 0.13 * lerp(1, 0.62, up)
        yf = lerp(cy - U * 0.08, H * 0.15, up)
        for i, (s_, col) in enumerate([("МЫ ЭТО", WHITE), ("ИСПРАВИМ", YELLOW)]):
            t0 = HK["fix"][i] * B
            if lt < t0: continue
            p = prog(lt, t0, t0 + 0.15); pop = max(0.02, back_out(p, 2.5))
            yy = yf + i * sz * 1.25
            ctx.save(); ctx.translate(cx, yy); ctx.scale(pop, pop); ctx.translate(-cx, -yy)
            glitch(ctx, s_, fit_size(HF, s_, W * 0.86, sz, -0.02), cx, yy, lt, strength=1.4 - (lt - t0) * 3, color=col)
            ctx.restore()
        label(ctx, "ОДНА СТУДИЯ · ТРИ НАПРАВЛЕНИЯ", yf + sz * 1.25 + U * lerp(0.1, 0.07, up), WHITE, lt, HK["sub"] * B)
        for i, (s_, col) in enumerate(SERVICES):
            t0 = HK["serv"][i] * B
            y = H * 0.45 + i * U * 0.17
            size = fit_size(HF, s_, W * 0.86, U * 0.12, -0.02)
            word_pop(ctx, s_, size, cx - HF.layout(s_, size, -0.02)[1] / 2, y, lt, t0, col)
        p = back_out(prog(lt, HK["key"] * B, HK["key"] * B + IN), 2)
        if p > 0:
            ts = U * 0.036; bw_ = MF.layout("ПОД КЛЮЧ", ts, 0.08)[1] + ts * 2.4; bh_ = ts * 2.5
            y = H * 0.45 + 2 * U * 0.17 + U * 0.08
            ctx.save(); ctx.translate(cx, y + bh_ / 2); ctx.scale(p, p); ctx.translate(-cx, -(y + bh_ / 2))
            pill(ctx, cx - bw_ / 2, y, bw_, bh_, YELLOW)
            text(ctx, MF, "ПОД КЛЮЧ", ts, cx, y + bh_ * 0.66, INK, 0.08, anchor="center"); ctx.restore()
        ctx.restore()
    # --- 33–36: провал перед дропом — ZZ вспыхивают на голосовых ударах, линия растёт к дропу ---
    if b >= HK["out"] + 0.5:
        for n, f in enumerate(HK["flick"]):
            a = lt - f * B
            if 0 <= a < 0.28:
                zz(ctx, cx, cy, W * (0.45 + 0.12 * n), YELLOW, alpha=(1 - a / 0.28) ** 2)
        g = expo_in(prog(lt, (HK["flick"][-1] + 0.05) * B, DROP * B))
        ctx.rectangle(cx - W / 2 * g, cy - U * 0.004, W * g, U * 0.008); rgb(ctx, YELLOW); ctx.fill()


# 2. ЛОГОТИП (доли 36–40, дроп 1)
def s_logo(ctx, lt):
    rgb(ctx, YELLOW); ctx.paint()
    sx, sy = kick_shake(lt, [0, 1, 2, 3], U * 0.01)
    ctx.save(); ctx.translate(sx, sy)
    ctx.save(); ctx.translate(cx, cy); ctx.rotate(-math.radians(32))
    span = math.hypot(W, H); step = U * 0.16; x = -span + (lt * U * 0.35) % step
    while x < span: ctx.rectangle(x, -span, step * 0.35, span * 2); x += step
    rgb(ctx, INK, 0.06); ctx.fill(); ctx.restore()
    MD = U * 0.34; mc = (cx, H * 0.38)
    slam = expo_out(prog(lt, 0, 0.2)); shrink = expo_inout(prog(lt, 1.0 * B, 1.8 * B))
    zw = lerp(W * 0.84, MD * 814 / 1160, shrink) * (1 + beat_pop(lt, [0, 1, 2, 3]))
    zx = lerp(cx, mc[0] + 4 * MD / 1160, shrink); zy = lerp(cy, mc[1] + 12 * MD / 1160, shrink)
    circ = back_out(prog(lt, 1.5 * B, 2.0 * B), 2.0)
    if circ > 0: circle(ctx, mc[0], mc[1], MD / 2 * circ, INK)
    zcol = tuple(lerp(a, b, clamp(prog(lt, 1.5 * B, 1.8 * B))) for a, b in zip(INK, YELLOW))
    zz(ctx, zx, zy, zw, zcol, dy1=-H * (1 - slam), dy2=H * (1 - slam), skew=-0.5 * (1 - slam))
    WS = U * 0.2; _, ww = UNB.layout("mazzeru", WS, -0.06); WS *= min(1, W * 0.82 / ww); _, ww = UNB.layout("mazzeru", WS, -0.06)
    wb = mc[1] + MD * 0.5 + U * 0.08 + UNB.xh * WS; wx = cx - ww / 2
    pw = expo_out(prog(lt, 2 * B, 2.6 * B))
    if pw > 0:
        ctx.save(); ctx.rectangle(wx - 5, wb - WS, (ww + 10) * pw, WS * 1.3); ctx.clip()
        text(ctx, UNB, "mazzeru", WS, wx, wb, INK, -0.06); ctx.restore()
        if pw < 1: ctx.rectangle(wx + ww * pw, wb - WS, U * 0.014, WS * 1.3); rgb(ctx, INK); ctx.fill()
    label(ctx, "DIGITAL-СТУДИЯ · АСТАНА", wb + U * 0.1, INK, lt, 3 * B, U * 0.03)
    ctx.restore()


# 3. ИИ-ВИДЕО (доли 40–48)
def ai_art(w, h, t):
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, int(w), int(h)); c = cairo.Context(s)
    g = cairo.LinearGradient(0, 0, 0, h)
    g.add_color_stop_rgb(0, .16, .1, .42); g.add_color_stop_rgb(.55, .98, .45, .38); g.add_color_stop_rgb(1, 1, .8, .5)
    c.rectangle(0, 0, w, h); c.set_source(g); c.fill()
    circle(c, w * 0.5, h * (0.56 - 0.03 * t), w * 0.16, (1, .93, .7))
    for k, (col, base, amp) in enumerate([((.42, .22, .45), .62, .16), ((.25, .12, .32), .72, .12), ((.1, .05, .15), .84, .06)]):
        c.move_to(0, h)
        for i in range(0, 41):
            x = w * i / 40
            y = h * (base - amp * abs(math.sin(i * 0.55 + k * 1.7)) * (0.6 + 0.4 * math.sin(i * 0.23 + k)))
            c.line_to(x, y)
        c.line_to(w, h); c.close_path(); rgb(c, col); c.fill()
    for dx in (-0.035, 0.035):
        px = w * (0.5 + dx); py = h * 0.8
        circle(c, px, py - w * 0.075, w * 0.022, (.05, .02, .08))
        rrect(c, px - w * 0.024, py - w * 0.05, w * 0.048, w * 0.11, w * 0.02); rgb(c, (.05, .02, .08)); c.fill()
    return s


def section_head(ctx, lt, num, title, fg, accent):
    label(ctx, f"{num} · УСЛУГИ", H * 0.1, accent, lt, 0)
    big(ctx, title, H * 0.19, fg, lt, 0, size=U * 0.12)


def s_ai(ctx, lt):
    rgb(ctx, INK); ctx.paint()
    g = cairo.RadialGradient(cx, H * 0.5, 0, cx, H * 0.5, U * 0.9)
    g.add_color_stop_rgba(0, *YELLOW, 0.14); g.add_color_stop_rgba(1, *YELLOW, 0)
    ctx.rectangle(0, 0, W, H); ctx.set_source(g); ctx.fill()
    section_head(ctx, lt, "01", "ИИ-ВИДЕО", WHITE, YELLOW)
    cw, ch = W * 0.84, W * 0.84 * 0.9
    x0, y0 = cx - cw / 2, H * 0.235
    pc = expo_out(prog(lt, 0.5 * B, 0.5 * B + IN))
    y0 += U * 0.1 * (1 - pc)
    rrect(ctx, x0, y0, cw, ch, U * 0.04); rgb(ctx, GRAY, pc); ctx.fill()
    prompt = "love story в горах, закат, 35mm"
    n = int(len(prompt) * clamp(prog(lt, 1 * B, 2.5 * B)))
    ts = U * 0.034
    rrect(ctx, x0 + U * 0.03, y0 + U * 0.03, cw - U * 0.06, U * 0.1, U * 0.05); rgb(ctx, WHITE, 0.08 * pc); ctx.fill()
    text(ctx, INT, "*", ts * 1.3, x0 + U * 0.065, y0 + U * 0.093, YELLOW, 0, pc)
    tw = text(ctx, INT, prompt[:n], ts, x0 + U * 0.11, y0 + U * 0.093, WHITE, 0, pc) if n else 0
    if n < len(prompt) and int(lt / (B / 2)) % 2 == 0:
        ctx.rectangle(x0 + U * 0.115 + tw, y0 + U * 0.062, ts * 0.12, ts * 1.1); rgb(ctx, YELLOW); ctx.fill()
    ix, iy, iw, ih = x0 + U * 0.03, y0 + U * 0.16, cw - U * 0.06, ch - U * 0.19
    gen = prog(lt, 3 * B, 5 * B)
    if lt > 2.5 * B:
        art = ai_art(iw, ih, gen)
        ctx.save(); rrect(ctx, ix, iy, iw, ih, U * 0.025); ctx.clip()
        ctx.set_source_surface(art, ix, iy); ctx.paint()
        nz = 1 - expo_out(gen)
        if nz > 0.01:
            cell = U * 0.02
            for gy in range(int(ih / cell) + 1):
                for gx in range(int(iw / cell) + 1):
                    v = rand(gx * 131 + gy * 7 + int(lt / (B / 4)) * 977, 3)     # шум меняется на 16-е
                    ctx.rectangle(ix + gx * cell, iy + gy * cell, cell, cell)
                    ctx.set_source_rgba(v, v * 0.9, v, nz * 0.95); ctx.fill()
        ctx.restore()
        if gen < 1:
            bw_ = iw * 0.6
            rrect(ctx, cx - bw_ / 2 - U * 0.03, iy + ih / 2 - U * 0.06, bw_ + U * 0.06, U * 0.12, U * 0.03); rgb(ctx, INK, 0.75); ctx.fill()
            text(ctx, MF, f"ГЕНЕРАЦИЯ {int(gen * 100)}%", U * 0.026, cx, iy + ih / 2 - U * 0.005, WHITE, 0.08, anchor="center")
            rrect(ctx, cx - bw_ / 2, iy + ih / 2 + U * 0.02, bw_, U * 0.012, U * 0.006); rgb(ctx, WHITE, 0.2); ctx.fill()
            rrect(ctx, cx - bw_ / 2, iy + ih / 2 + U * 0.02, bw_ * gen, U * 0.012, U * 0.006); rgb(ctx, YELLOW); ctx.fill()
        else:
            p = back_out(prog(lt, 5 * B, 5 * B + IN), 2)
            if p > 0:
                ts2 = U * 0.024; bw2 = MF.layout("ГОТОВО", ts2, 0.08)[1] + ts2 * 2
                ctx.save(); ctx.translate(ix + U * 0.03 + bw2 / 2, iy + U * 0.06); ctx.scale(p, p); ctx.translate(-(ix + U * 0.03 + bw2 / 2), -(iy + U * 0.06))
                pill(ctx, ix + U * 0.03, iy + U * 0.03, bw2, U * 0.06, YELLOW)
                text(ctx, MF, "ГОТОВО", ts2, ix + U * 0.03 + bw2 / 2, iy + U * 0.069, INK, 0.08, anchor="center"); ctx.restore()
    ch_h = chips(ctx, ["Love story", "Реклама", "Клипы", "ИИ-аватары"], H * 0.68, lt, 5 * B, YELLOW, INK)
    label(ctx, "Без съёмочной группы и дорогих локаций", H * 0.68 + ch_h + U * 0.08, WHITE, lt, 7 * B)


# 4. МОБИЛОГРАФИЯ (доли 48–56)
def flat(im):
    im = ImageEnhance.Color(im).enhance(0.25); im = ImageEnhance.Contrast(im).enhance(0.6)
    return ImageEnhance.Brightness(im).enhance(1.1)


def graded(im):
    im = ImageEnhance.Contrast(im).enhance(1.15); return ImageEnhance.Color(im).enhance(1.25)


def s_mobile(ctx, lt):
    rgb(ctx, YELLOW); ctx.paint()
    section_head(ctx, lt, "02", "МОБИЛОГРАФИЯ", INK, INK)
    pw_, ph_ = W * 0.4, W * 0.4 * 1.9
    pin = expo_out(prog(lt, 0.5 * B, 0.5 * B + 0.3))
    x0 = cx - pw_ / 2; y0 = H * 0.25 + H * 0.4 * (1 - pin)
    ang = math.radians(-4) * (1 - expo_out(prog(lt, 1 * B, 2 * B)))
    ctx.save(); ctx.translate(cx, y0 + ph_ / 2); ctx.rotate(ang); ctx.translate(-cx, -(y0 + ph_ / 2))
    rrect(ctx, x0 - U * 0.016, y0 - U * 0.016, pw_ + U * 0.032, ph_ + U * 0.032, U * 0.07); rgb(ctx, INK); ctx.fill()
    path = os.path.join(IMG, "hero", "mobile.webp")
    zoom = 1.25 - 0.1 * prog(lt, 0, 8 * B)
    image(ctx, "mob_flat", x0, y0, pw_, ph_, U * 0.055, path, flat, zoom=zoom)
    sp = expo_inout(prog(lt, 3 * B, 5 * B))
    sx = x0 + pw_ * (1 - sp)
    if sp > 0:
        ctx.save(); ctx.rectangle(sx, y0, pw_, ph_); ctx.clip()
        image(ctx, "mob_grade", x0, y0, pw_, ph_, U * 0.055, path, graded, zoom=zoom); ctx.restore()
        if sp < 1:
            ctx.rectangle(sx - 2, y0, 4, ph_); rgb(ctx, WHITE); ctx.fill()
            circle(ctx, sx, y0 + ph_ / 2, U * 0.032, WHITE)
            text(ctx, INT, "‹ ›", U * 0.028, sx, y0 + ph_ / 2 + U * 0.01, INK, 0, anchor="center")
    m = U * 0.035
    if int(lt / B) % 2 == 0: circle(ctx, x0 + m, y0 + m * 1.6, U * 0.011, (1, .25, .25))   # REC мигает в долю
    fr = int(lt * FPS)
    text(ctx, INT, f"REC 00:{int(lt):02d}:{fr % FPS:02d}", U * 0.022, x0 + m * 1.7, y0 + m * 1.6 + U * 0.008, WHITE, 0.1)
    tag = "ПОСЛЕ ЦВЕТОКОРА" if sp > 0.5 else "ИСХОДНИК"
    ts = U * 0.018; tw_ = MF.layout(tag, ts, 0.06)[1] + ts * 2
    pill(ctx, cx - tw_ / 2, y0 + ph_ - U * 0.085, tw_, U * 0.05, INK, 0.75)
    text(ctx, MF, tag, ts, cx, y0 + ph_ - U * 0.053, YELLOW if sp > 0.5 else WHITE, 0.06, anchor="center")
    ctx.restore()
    ch_h = chips(ctx, ["Reels", "Съёмка", "Монтаж", "Цветокор"], H * 0.25 + ph_ + U * 0.07, lt, 5 * B, INK, YELLOW)
    label(ctx, "Контент, который досматривают", H * 0.25 + ph_ + U * 0.07 + ch_h + U * 0.08, INK, lt, 7 * B)


# 5. САЙТЫ (доли 56–65)
SITES = ["itecx", "ascora", "onerlab", "smarthub", "astanatechcup"]
DOMAINS = {"itecx": "itecx.kz", "ascora": "ascora.kz", "onerlab": "onerlab.kz", "smarthub": "smarthub.kz", "astanatechcup": "astanatechcup.kz"}
def s_web(ctx, lt):
    rgb(ctx, INK); ctx.paint()
    grid(ctx, W, H, U, YELLOW, 0.08)
    section_head(ctx, lt, "03", "САЙТЫ", WHITE, YELLOW)
    bw, bh = W * 0.86, W * 0.86 * 0.78
    pin = expo_out(prog(lt, 0.5 * B, 0.5 * B + 0.3))
    x0 = cx - bw / 2; y0 = H * 0.25 + U * 0.15 * (1 - pin)
    rrect(ctx, x0 + U * 0.02, y0 + U * 0.035, bw, bh, U * 0.035); rgb(ctx, YELLOW, pin); ctx.fill()
    rrect(ctx, x0, y0, bw, bh, U * 0.035); rgb(ctx, WHITE, pin); ctx.fill()
    bar = U * 0.075
    ctx.save(); rrect(ctx, x0, y0, bw, bh, U * 0.035); ctx.clip()
    ctx.rectangle(x0, y0, bw, bar); rgb(ctx, (0.94, 0.93, 0.89)); ctx.fill(); ctx.restore()
    for i, col in enumerate([(1, .37, .34), (1, .74, .18), (.16, .8, .25)]):
        circle(ctx, x0 + U * 0.04 + i * U * 0.035, y0 + bar / 2, U * 0.011, col, pin)
    # проект меняется на каждую 2-ю долю: 0, 1, 3, 5, 7
    switches = [0, 1, 3, 5, 7]
    k = max(i for i, sw in enumerate(switches) if lt >= sw * B)
    ph = lt - switches[k] * B
    vx, vy, vw, vh = x0, y0 + bar, bw, bh - bar
    rrect(ctx, x0 + bw * 0.25, y0 + bar * 0.2, bw * 0.5, bar * 0.6, bar * 0.3); rgb(ctx, WHITE, pin); ctx.fill()
    text(ctx, INT, DOMAINS[SITES[k]], U * 0.024, cx, y0 + bar * 0.62, INK, 0.02, pin * 0.8, anchor="center")
    ctx.save(); ctx.rectangle(vx, vy, vw, vh); ctx.clip()
    sl = expo_out(clamp(ph / 0.2)) if k > 0 else 1
    if k > 0 and sl < 1:
        image(ctx, "site_" + SITES[k - 1], vx - vw * 0.3 * sl, vy, vw, vh, 0, os.path.join(IMG, "projects", SITES[k - 1] + ".webp"), pos=(0.5, 0.0), alpha=pin)
    image(ctx, "site_" + SITES[k], vx + vw * (1 - sl), vy, vw, vh, 0, os.path.join(IMG, "projects", SITES[k] + ".webp"), pos=(0.5, 0.0), alpha=pin)
    ctx.restore()
    cxp = vx + vw * (0.62 + 0.12 * math.sin(lt * 2.2)); cyp = vy + vh * (0.55 + 0.15 * math.cos(lt * 1.7))
    ctx.move_to(cxp, cyp); ctx.rel_line_to(0, U * 0.05); ctx.rel_line_to(U * 0.013, -U * 0.012); ctx.rel_line_to(U * 0.02, U * 0.008)
    ctx.close_path(); rgb(ctx, INK, pin); ctx.fill_preserve(); rgb(ctx, WHITE, pin); ctx.set_line_width(2); ctx.stroke()
    ch_h = chips(ctx, ["Лендинги", "Под ключ", "KZ · RU · EN", "SEO"], y0 + bh + U * 0.1, lt, 5 * B, YELLOW, INK)
    label(ctx, "Сайт, который приводит заявки", y0 + bh + U * 0.1 + ch_h + U * 0.08, WHITE, lt, 7 * B)


# 6. ПАУЗА (доли 65–68): тишина, затем два удара голоса — «ДАВАЙТЕ» / «СОЗДАДИМ»
def s_break(ctx, lt):
    rgb(ctx, INK); ctx.paint()
    if lt < B and int(lt / (B / 4)) % 2 == 0:
        ctx.rectangle(cx - U * 0.018, cy - U * 0.045, U * 0.036, U * 0.09); rgb(ctx, YELLOW); ctx.fill()
    size = fit_size(HF, "СОЗДАДИМ", W * 0.86, U * 0.15, -0.02)
    for i, (s_, col) in enumerate([("ДАВАЙТЕ", WHITE), ("СОЗДАДИМ", YELLOW)]):
        t0 = (1 + i) * B
        if lt < t0: continue
        p = prog(lt, t0, t0 + 0.14); pop = max(0.02, back_out(p, 2.5))
        yy = cy - size * 0.25 + (i - 0.5) * size * 1.35
        ctx.save(); ctx.translate(cx, yy); ctx.scale(pop, pop); ctx.translate(-cx, -yy)
        glitch(ctx, s_, size, cx, yy, lt, strength=1.6 - (lt - t0) * 4, color=col)
        ctx.restore()


# 7. ФИНАЛ (доли 68–80: дроп 2, с 76.5 — затухание)
def s_cta(ctx, lt):
    rgb(ctx, YELLOW); ctx.paint()
    e = expo_out(prog(lt, 0, 0.4))
    circle(ctx, W + U * 0.12, -U * 0.12, U * 0.34 * e, INK)
    ctx.arc(-U * 0.12, H + U * 0.04, max(1, U * 0.4 * e), 0, 2 * math.pi); ctx.set_line_width(U * 0.02); rgb(ctx, INK); ctx.stroke()
    s1 = big(ctx, "ДАВАЙТЕ", H * 0.24, INK, lt, 0, max_w=W * 0.8, size=U * 0.14)
    y2 = H * 0.24 + s1 * 1.35
    pb = expo_out(prog(lt, 0, IN))
    ctx.rectangle(0, y2 - s1 * 1.0, W * pb, s1 * 1.28); rgb(ctx, INK); ctx.fill()
    big(ctx, "СОЗДАДИМ", y2, YELLOW, lt, 0.05, max_w=W * 0.8, size=s1)
    MD = U * 0.15
    WS = U * 0.12; _, ww = UNB.layout("mazzeru", WS, -0.06)
    gap = MD * 0.24; total = MD + gap + ww; left = cx - total / 2; ly = H * 0.47
    t0 = CTA["logo"] * B
    pe = expo_out(prog(lt, t0, t0 + 0.3))
    mark(ctx, left + MD / 2, ly, MD * (1 + beat_pop(lt, [2, 4, 6, 8], 0.04)), 0, INK, YELLOW,
         circ=back_out(prog(lt, t0, t0 + 0.25), 2.2), split=(1 - pe) * 0.9, skew=-(1 - pe) * 0.6, zalpha=clamp(prog(lt, t0, t0 + 0.08)))
    pw = expo_out(prog(lt, t0 + 0.1, t0 + 0.6))
    wx, wb = left + MD + gap, ly + UNB.xh * WS / 2
    ctx.save(); ctx.rectangle(wx - 5, wb - WS, (ww + 10) * pw, WS * 1.3); ctx.clip()
    text(ctx, UNB, "mazzeru", WS, wx, wb, INK, -0.06); ctx.restore()
    items = ["ИИ-видео", "Мобилография", "Сайты и лендинги"]
    ts = U * 0.036
    for i, s_ in enumerate(items):
        t_ = CTA["items"][i] * B
        p = expo_out(prog(lt, t_, t_ + IN))
        if p <= 0: continue
        _, w = MF.layout(s_, ts, 0)
        tot = ts * 1.3 + w; x = cx - tot / 2
        y = H * 0.56 + i * U * 0.075 + U * 0.02 * (1 - p)
        check(ctx, x, y - ts * 0.1, ts, INK, p)
        text(ctx, MF, s_, ts, x + ts * 1.3, y, INK, 0, p)
    p = back_out(prog(lt, CTA["button"] * B, CTA["button"] * B + IN), 2)
    if p > 0:
        bw_, bh_ = W * 0.74, U * 0.13; bx, by = cx - bw_ / 2, H * 0.7
        pulse = 1 + beat_pop(lt, [7, 8, 9, 10, 11], 0.03)
        ctx.save(); ctx.translate(cx, by + bh_ / 2); ctx.scale(p * pulse, p * pulse); ctx.translate(-cx, -(by + bh_ / 2))
        pill(ctx, bx, by, bw_, bh_, INK)
        bs = U * 0.036
        text(ctx, HF, "ПИШИТЕ В DIRECT →", bs, cx, by + bh_ * 0.62, YELLOW, 0.02, anchor="center")
        ctx.restore()
    label(ctx, "@mazzeru.studio", H * 0.8, INK, lt, CTA["handle"] * B, U * 0.04, 0.02)


SECTIONS = [(0, s_hook, INK), (DROP, s_logo, YELLOW), (40, s_ai, INK), (48, s_mobile, YELLOW), (56, s_web, INK), (BREAK, s_break, INK), (DROP2, s_cta, YELLOW)]
HARD = {DROP, BREAK, DROP2}
TR = 0.22
FADE = (76.5, 79.8)


def punch(t):
    dx = dy = 0.0; z = 1.0
    for k in KICKS:
        a = t - k * B
        if 0 <= a < 0.3:
            e = math.exp(-a * 16) * U * (0.004 if k < DROP else 0.007) * HITS.get(k, 1)
            dx += math.sin(a * 95 + k) * e; dy += math.cos(a * 80 + k) * e
    for sn in SNARES:
        a = t - sn * B
        if 0 <= a < 0.3: z += math.exp(-a * 14) * 0.012
    return dx, dy, z


def scene(ctx, t):
    idx = max(i for i, (b, _, _) in enumerate(SECTIONS) if t >= b * B)
    b, fn, bg = SECTIONS[idx]
    lt = t - b * B
    dx, dy, z = punch(t)
    ctx.save(); ctx.translate(cx + dx, cy + dy); ctx.scale(z, z); ctx.translate(-cx, -cy)
    if idx > 0 and lt < TR and b not in HARD:
        pb, pfn, _ = SECTIONS[idx - 1]
        pfn(ctx, t - pb * B)
        p = expo_out(lt / TR)
        ctx.save(); ctx.arc(cx, cy, math.hypot(W, H) / 2 * p + 1, 0, 2 * math.pi); ctx.clip()
        fn(ctx, lt); ctx.restore()
        ctx.arc(cx, cy, math.hypot(W, H) / 2 * p, 0, 2 * math.pi); ctx.set_line_width(U * 0.03 * (1 - p))
        rgb(ctx, INK if bg == YELLOW else YELLOW); ctx.stroke()
    else:
        fn(ctx, lt)
    ctx.restore()
    for d in (DROP, DROP2):
        a = t - d * B
        if 0 <= a < 0.22:
            rgb(ctx, WHITE, 0.7 * (1 - a / 0.22) ** 2); ctx.paint()
    f = prog(t, FADE[0] * B, FADE[1] * B)
    if f > 0:
        rgb(ctx, INK, math.sin(f * math.pi / 2) ** 2); ctx.paint()


def frame(t, blur=2):
    acc = None
    samples = [t + (k / blur - 0.5) / FPS * 0.8 for k in range(blur)] if blur > 1 else [t]
    for ts in samples:
        s = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H); c = cairo.Context(s)
        scene(c, max(0, min(TOTAL - 1e-3, ts)))
        a = np.ndarray((H, W, 4), np.uint8, s.get_data()).astype(np.float32)
        acc = a if acc is None else acc + a
    return (acc / len(samples))[:, :, [2, 1, 0]].astype(np.uint8)


def sheet(beats, name, tw=216):
    th = int(tw * H / W)
    ims = [Image.fromarray(frame(b * B, 1)).resize((tw, th)) for b in beats]
    cols = 10
    sh = Image.new("RGB", ((tw + 8) * cols, (th + 8) * ((len(ims) + cols - 1) // cols)), "gray")
    for i, im in enumerate(ims): sh.paste(im, ((i % cols) * (tw + 8), (i // cols) * (th + 8)))
    p = os.path.join(OUT_DIR, name); sh.save(p); print(p)


if __name__ == "__main__":
    if "preview" in sys.argv:
        sheet([0.1, 1.2, 3.5, 11, 15.5, 19, 23, 31, 34.1, 36.3, 39, 46, 53, 62, 65.5, 67.5, 68.3, 70, 75, 78.5], "preview-reel.png")
    elif "sheet" in sys.argv:
        # плотная проверка на наложения: кадр в конце каждой доли
        sheet([b + 0.9 for b in range(0, 40)], "sheet-reel-1.png", 180)
        sheet([b + 0.9 for b in range(40, 80)], "sheet-reel-2.png", 180)
    else:
        ff = imageio_ffmpeg.get_ffmpeg_exe()
        out = os.path.join(OUT_DIR, "mazzeru-reel-01.mp4")
        cmd = [ff, "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
               "-i", os.path.join(OUT_DIR, "reel_track.wav"),
               "-c:v", "libx264", "-preset", "slow", "-crf", "17", "-pix_fmt", "yuv420p", "-movflags", "+faststart",
               "-c:a", "aac", "-b:a", "256k", "-shortest", out]
        pr = subprocess.Popen(cmd, stdin=subprocess.PIPE)
        for i in range(int(round(TOTAL * FPS))): pr.stdin.write(frame(i / FPS).tobytes())
        pr.stdin.close(); pr.wait(); print("saved", out)
