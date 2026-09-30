"""Интро и аутро Mazzeru v2 (фонк, 140 BPM).
Кадры рисуются на cairo, буквы — контуры шрифтов, склейка в MP4 через ffmpeg.

Запуск:
  python render.py intro landscape|vertical [preview]
  python render.py outro landscape|vertical [preview]
Общие помощники (шрифты, знак, текст, плавности) берутся из render_v1.py.
"""
import math, os, sys, subprocess
import numpy as np, cairo, imageio_ffmpeg
from render_v1 import (UNB, INT, clamp, prog, expo_out, expo_in, expo_inout, back_out, lerp,
                       rgb, circle, text, mark, Z1_POLYS, Z2_POLYS, BLUE, YELLOW, WARM, INK, WHITE)

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.normpath(os.path.join(HERE, ".."))
FPS = 30
BEAT = 60 / 140
DEEP = (0 / 255, 40 / 255, 170 / 255)
INTRO_END = 18 * BEAT        # 7.71 с
OUTRO_END = 15 * BEAT        # 6.43 с


# ---------------- помощники v2 ----------------
def rand(i, k=0):
    """детерминированный «случайный» 0..1"""
    return (math.sin(i * 127.1 + k * 311.7) * 43758.5453) % 1


def zz(ctx, cx, cy, width, color, dy1=0.0, dy2=0.0, dx1=0.0, dx2=0.0, skew=0.0, alpha=1.0):
    """только ZZ (без круга): центр (cx, cy), полная ширина width; каждую Z можно сдвинуть отдельно"""
    if width <= 0 or alpha <= 0: return
    s = width / 814
    for polys, dx, dy in ((Z1_POLYS, dx1, dy1), (Z2_POLYS, dx2, dy2)):
        ctx.save(); ctx.translate(cx + dx, cy + dy)
        ctx.transform(cairo.Matrix(1, 0, skew, 1, 0, 0))
        ctx.scale(s, s); ctx.translate(-629, -637)
        for p in polys:
            ctx.move_to(*p[0])
            for q in p[1:]: ctx.line_to(*q)
            ctx.close_path()
        rgb(ctx, color, alpha); ctx.fill(); ctx.restore()


def glitch_text(ctx, font, s, size, cx, y, t, strength=1.0, color=WHITE, tracking=0.0):
    """текст с RGB-сдвигом: синий и жёлтый слои «дрожат»"""
    j = strength * size * 0.06
    ox = (rand(int(t * 60), 1) - .5) * 2 * j; oy = (rand(int(t * 60), 2) - .5) * j
    text(ctx, font, s, size, cx - ox, y - oy, BLUE, tracking, 0.9, anchor="center")
    text(ctx, font, s, size, cx + ox, y + oy, YELLOW, tracking, 0.9, anchor="center")
    text(ctx, font, s, size, cx, y, color, tracking, anchor="center")


def kick_shake(t, beats, amp):
    """тряска камеры: затухающий импульс на каждом ударе"""
    dx = dy = 0.0
    for b in beats:
        age = t - b * BEAT
        if 0 <= age < 0.35:
            e = math.exp(-age * 14) * amp
            dx += math.sin(age * 90) * e; dy += math.cos(age * 70) * e
    return dx, dy


def layout(W, H, vertical, scale=1.0):
    """раскладка горизонтального (или столбикового) логотипа"""
    U = min(W, H); cx, cy = W / 2, H / 2
    M = U * (0.25 if vertical else 0.2) * scale
    WS = M * 1.02 / UNB.xh
    _, ww = UNB.layout("mazzeru", WS, -0.06)
    if vertical:
        WS *= min(1, (W * 0.84 * scale) / ww); _, ww = UNB.layout("mazzeru", WS, -0.06)
        MD = M * 1.22
        mark_c = (cx, cy - M * 0.9)
        word_x, word_base = cx - ww / 2, cy + M * 0.35 + UNB.xh * WS
    else:
        MD = M * 1.22; gap = M * 0.24; total = MD + gap + ww
        f = min(1, W * 0.72 * scale / total)
        M *= f; WS *= f; gap *= f; MD *= f
        _, ww = UNB.layout("mazzeru", WS, -0.06); total = MD + gap + ww
        left = cx - total / 2
        mark_c = (left + MD / 2, cy - U * 0.03)
        word_x, word_base = left + MD + gap, cy - U * 0.03 + UNB.xh * WS / 2
    return dict(U=U, cx=cx, cy=cy, M=M, MD=MD, WS=WS, ww=ww, mark=mark_c, word_x=word_x, word_base=word_base)


def grid(ctx, W, H, U, color, alpha, offset=0.0, reveal=1.0):
    step = U * 0.08
    ctx.set_line_width(max(1, U * 0.0012))
    n = 0
    x = (offset % step)
    while x < W:
        n += 1
        if rand(n, 5) < reveal:
            ctx.move_to(x, 0); ctx.line_to(x, H)
        x += step
    y = (offset * 0.6 % step)
    while y < H:
        n += 1
        if rand(n, 6) < reveal:
            ctx.move_to(0, y); ctx.line_to(W, y)
        y += step
    rgb(ctx, color, alpha); ctx.stroke()


def hud(ctx, W, H, U, t, color, alpha):
    """угловые подписи в стиле видоискателя"""
    ts = U * 0.022; m = U * 0.06
    fr = int(t * FPS)
    text(ctx, INT, "MAZZERU / ASTANA", ts, m, m + ts, color, 0.3, alpha)
    text(ctx, INT, f"00:00:{int(t):02d}:{fr % FPS:02d}", ts, W - m, m + ts, color, 0.2, alpha, anchor="right_")
    # REC
    if (fr // 8) % 2 == 0:
        circle(ctx, m + ts * 0.4, H - m - ts * 0.35, ts * 0.35, (1, 0.23, 0.23), alpha)
    text(ctx, INT, "REC", ts, m + ts * 1.2, H - m, color, 0.3, alpha)
    # уголки рамки
    L = U * 0.05; ctx.set_line_width(max(1.5, U * 0.003))
    for (x, y, sx, sy) in ((m * 0.6, m * 0.6, 1, 1), (W - m * 0.6, m * 0.6, -1, 1), (m * 0.6, H - m * 0.6, 1, -1), (W - m * 0.6, H - m * 0.6, -1, -1)):
        ctx.move_to(x, y + sy * L); ctx.line_to(x, y); ctx.line_to(x + sx * L, y)
    rgb(ctx, color, alpha); ctx.stroke()


def text_right(ctx, font, s, size, x, y, color, tracking=0.0, alpha=1.0):
    _, w = font.layout(s, size, tracking)
    return text(ctx, font, s, size, x - w, y, color, tracking, alpha)


# чинить anchor="right_" через обёртку
_text = text
def text(ctx, font, s, size, x, y, color, tracking=0.0, alpha=1.0, per_letter=None, anchor="left"):
    if anchor == "right_":
        _, w = font.layout(s, size, tracking); return _text(ctx, font, s, size, x - w, y, color, tracking, alpha, per_letter)
    return _text(ctx, font, s, size, x, y, color, tracking, alpha, per_letter, anchor)


# =====================================================================
#                                ИНТРО
# =====================================================================
def scene_intro(ctx, t, W, H, vertical):
    Lo = layout(W, H, vertical); U, cx, cy = Lo["U"], Lo["cx"], Lo["cy"]
    B = BEAT
    DROP, CUT, END = 3 * B, 13 * B, 14 * B

    # ---------------- 1. вступление: тёмный экран, сетка, слова ----------------
    if t < DROP:
        rgb(ctx, INK); ctx.paint()
        grid(ctx, W, H, U, BLUE, 0.35, offset=t * U * 0.05, reveal=expo_out(prog(t, 0, 1.0)))
        # сканирующая линия
        sy = (t / DROP) * H * 1.2 - H * 0.1
        g = cairo.LinearGradient(0, sy - U * 0.12, 0, sy)
        g.add_color_stop_rgba(0, *BLUE, 0); g.add_color_stop_rgba(1, *BLUE, 0.45)
        ctx.rectangle(0, sy - U * 0.12, W, U * 0.12); ctx.set_source(g); ctx.fill()
        hud(ctx, W, H, U, t, WHITE, 0.7 * expo_out(prog(t, 0.05, 0.4)))
        # слова на каждую долю
        words = ["AI VIDEO", "WEB", "MOBILE FILM"]
        k = min(2, int(t / B)); age = t - k * B
        size = U * (0.13 if vertical else 0.12)
        if not vertical and k == 2: size *= 0.8
        pop = max(0.02, back_out(clamp(age / 0.12), 2.5))
        ctx.save(); ctx.translate(cx, cy); ctx.scale(pop, pop); ctx.translate(-cx, -cy)
        glitch_text(ctx, INT, words[k], size, cx, cy + size * 0.36, t, strength=1.6 - age * 3)
        ctx.restore()
        # вспышка перед дропом
        if t > DROP - 0.09:
            rgb(ctx, WHITE, prog(t, DROP - 0.09, DROP)); ctx.paint()
        return

    # ---------------- 5. финальная карточка ----------------
    if t >= END:
        rgb(ctx, WARM); ctx.paint()
        grid(ctx, W, H, U, BLUE, 0.08, offset=t * U * 0.02)
        e = expo_out(prog(t, END, END + 0.7))
        circle(ctx, W + U * 0.1, -U * 0.08, U * 0.48 * e, BLUE)
        circle(ctx, -U * 0.1, H + U * 0.08, U * 0.36 * e, YELLOW)
        s_end = 0.72 if not vertical else 0.8
        mc = Lo["mark"]; ly = (mc[1] + Lo["word_base"] - UNB.xh * Lo["WS"] / 2) / 2 if vertical else mc[1]
        ctx.save(); ctx.translate(cx, cy); ctx.scale(s_end, s_end); ctx.translate(-cx, -ly)
        pe = expo_out(prog(t, END + 0.05, END + 0.45))
        mark(ctx, mc[0], mc[1], Lo["MD"], 0, BLUE, WHITE, circ=back_out(prog(t, END, END + 0.35), 2.2),
             split=(1 - pe) * 0.9, skew=-(1 - pe) * 0.7, zalpha=clamp(prog(t, END + 0.05, END + 0.12)))
        # слово проявляется шторкой
        pw = expo_out(prog(t, END + 0.15, END + 0.75))
        ctx.save(); ctx.rectangle(Lo["word_x"] - 5, Lo["word_base"] - Lo["WS"], (Lo["ww"] + 10) * pw, Lo["WS"] * 1.3); ctx.clip()
        text(ctx, UNB, "mazzeru", Lo["WS"], Lo["word_x"], Lo["word_base"], BLUE, -0.06)
        ctx.restore()
        if 0 < pw < 1:
            ctx.rectangle(Lo["word_x"] + Lo["ww"] * pw, Lo["word_base"] - Lo["WS"], U * 0.012, Lo["WS"] * 1.3); rgb(ctx, YELLOW); ctx.fill()
        ctx.restore()
        ts = U * (0.028 if vertical else 0.022)
        bottom = cy + (Lo["word_base"] - ly) * s_end
        pt = expo_out(prog(t, END + 0.5, END + 1.0))
        yy = bottom + U * 0.1 + U * 0.04 * (1 - pt)
        text(ctx, INT, "AI VIDEO / WEB / MOBILE FILM", ts, cx, yy, INK, 0.32, alpha=pt, anchor="center")
        pc = expo_out(prog(t, END + 0.7, END + 1.2))
        text(ctx, INT, "@mazzeru.studio", ts * 1.25, cx, yy + U * 0.08, BLUE, 0.02, alpha=pc, anchor="center")
        # вспышка удара
        if t < END + 0.25:
            rgb(ctx, WHITE, 1 - prog(t, END, END + 0.25)); ctx.paint()
        return

    # ---------------- 2–4. дроп, логотип, стоп ----------------
    strobe = CUT <= t < END and int((t - CUT) / (B / 4)) % 2 == 1
    bg, fg, acc = (YELLOW, INK, BLUE) if strobe else (BLUE, WHITE, YELLOW)
    rgb(ctx, bg); ctx.paint()

    kicks = [3, 5, 7, 9, 11, 3 + 1.5, 7 + 1.5, 11 + 1.5]
    sx, sy_ = kick_shake(t, kicks, U * 0.012)
    ctx.save(); ctx.translate(sx, sy_)

    # диагональные полосы на фоне (ритм)
    ctx.save(); ctx.translate(cx, cy); ctx.rotate(-math.radians(32))
    span = math.hypot(W, H); step = U * 0.16; off = (t * U * 0.35) % step
    x = -span + off
    while x < span:
        ctx.rectangle(x, -span, step * 0.35, span * 2); x += step
    rgb(ctx, WHITE if not strobe else INK, 0.05); ctx.fill(); ctx.restore()

    # линии скорости после дропа
    if t < 6 * B:
        for i in range(14):
            life = 0.5 + rand(i, 1) * 0.4
            t0 = DROP + rand(i, 2) * 1.2
            age = t - t0
            if 0 <= age < life:
                p = age / life
                y = H * (0.08 + 0.84 * rand(i, 3))
                w = W * (0.25 + 0.4 * rand(i, 4))
                xe = W * 1.2 - (W * 1.6 + w) * expo_out(p)
                ctx.rectangle(xe, y, w, U * (0.006 + 0.014 * rand(i, 5)))
                rgb(ctx, YELLOW, 0.9 * (1 - p)); ctx.fill()

    mc = Lo["mark"]
    big_w = W * (0.82 if vertical else 0.62)
    # ZZ: влёт сверху/снизу на дропе, потом сжатие в знак
    slam = expo_out(prog(t, DROP, DROP + 0.28))
    shrink = expo_inout(prog(t, 6 * B, 7 * B))
    # размер ZZ внутри знака: 814/1160 диаметра
    small_w = Lo["MD"] * 814 / 1160
    zw = lerp(big_w, small_w, shrink)
    # ZZ в знаке смещены от центра круга на (4, 12) единиц исходника
    zx = lerp(cx, mc[0] + 4 * Lo["MD"] / 1160, shrink); zy = lerp(cy, mc[1] + 12 * Lo["MD"] / 1160, shrink)
    beat_pop = 0
    for b in (3, 5, 7, 9, 11):
        age = t - b * B
        if 0 <= age < 0.3: beat_pop += math.exp(-age * 12) * 0.05
    zw *= 1 + beat_pop
    # стоп: Z разлетаются
    cut = prog(t, CUT, END)
    split = expo_in(cut) * zw * 0.35
    # круг за знаком появляется при сжатии
    circ = back_out(prog(t, 6.6 * B, 7.4 * B), 2.0)
    if circ > 0:
        circle(ctx, zx, zy, Lo["MD"] / 2 * circ * (1 + beat_pop), fg)
    zcol = tuple(lerp(a, b, clamp(prog(t, 6.6 * B, 7.2 * B))) for a, b in zip(fg, bg))
    zz(ctx, zx, zy, zw, zcol,
       dy1=-H * 1.1 * (1 - slam), dy2=H * 1.1 * (1 - slam), dx1=-split, dx2=split,
       skew=-0.5 * (1 - slam))

    # слово: шторка слева направо с жёлтой кромкой
    if t > 7 * B:
        pw = expo_out(prog(t, 7 * B, 8.4 * B))
        wx, wb, WS, ww = Lo["word_x"], Lo["word_base"], Lo["WS"], Lo["ww"]
        sc = 1 + beat_pop
        ctx.save(); ctx.translate(wx, wb); ctx.scale(sc, sc); ctx.translate(-wx, -wb)
        ctx.save(); ctx.rectangle(wx - 5, wb - WS, (ww + 10) * pw, WS * 1.3); ctx.clip()
        dx = split * 1.6 if cut > 0 else 0
        text(ctx, UNB, "mazzeru", WS, wx + dx, wb, fg, -0.06)
        ctx.restore()
        if pw < 1:
            ctx.rectangle(wx + ww * pw, wb - WS, U * 0.014, WS * 1.3); rgb(ctx, acc); ctx.fill()
        ctx.restore()

    # подпись: печатается по буквам, мигающий курсор
    if t > 9 * B:
        tag = "AI VIDEO / WEB / MOBILE FILM"
        n = int(len(tag) * clamp(prog(t, 9 * B, 11 * B)))
        ts = U * (0.03 if vertical else 0.026)
        ty = Lo["word_base"] + U * (0.12 if vertical else 0.11)
        if not vertical: ty = cy + Lo["M"] * 0.5 + U * 0.11
        _, full = INT.layout(tag, ts, 0.32)
        x0 = cx - full / 2
        wshown = text(ctx, INT, tag[:n], ts, x0, ty, fg, 0.32, 0.95) if n else 0
        if n < len(tag) or int(t * 4) % 2 == 0:
            ctx.rectangle(x0 + wshown + ts * 0.3, ty - ts * 0.85, ts * 0.55, ts * 1.0); rgb(ctx, acc); ctx.fill()

    ctx.restore()
    # HUD поверх — только на дропе, коротко
    if t < DROP + 0.6:
        hud(ctx, W, H, U, t, WHITE, 0.6 * (1 - prog(t, DROP + 0.3, DROP + 0.6)))


# =====================================================================
#                                АУТРО
# =====================================================================
CONTACTS = [("INSTAGRAM", "@mazzeru.studio"), ("TELEGRAM", "@aldeke7122"),
            ("WHATSAPP", "+7 776 198 4474"), ("САЙТ", "mazzeru.vercel.app")]


def pill(ctx, x, y, w, h, color, alpha=1.0):
    r = h / 2
    ctx.new_sub_path()
    ctx.arc(x + w - r, y + r, r, -math.pi / 2, math.pi / 2); ctx.arc(x + r, y + r, r, math.pi / 2, 3 * math.pi / 2)
    ctx.close_path(); rgb(ctx, color, alpha); ctx.fill()


def scene_outro(ctx, t, W, H, vertical):
    U = min(W, H); cx, cy = W / 2, H / 2
    B = BEAT
    HIT1, COLL, HIT2 = 1 * B, 9 * B, 10 * B

    # фон: прозрачная «дыра» в начале — здесь просто тёплый белый, как конец любого ролика
    rgb(ctx, WARM); ctx.paint()
    # 1. синяя шторка снизу вверх, со скруглённой кромкой
    wp = expo_inout(prog(t, 0, HIT1))
    top = H * (1 - wp) - (1 - wp) * U * 0.2
    ctx.rectangle(0, top, W, H - top + 2); rgb(ctx, BLUE); ctx.fill()
    if wp < 1:
        circle(ctx, cx, top + 2, W * 0.75 * (1 - wp) + 1, BLUE)

    if t < HIT2:
        # мягкие круги на фоне, дышат в бит
        breathe = sum(math.exp(-(t - b * B) * 6) * 0.04 for b in (1, 3, 5, 7) if t >= b * B)
        ci = expo_out(prog(t, HIT1, HIT1 + 0.8))
        coll = expo_in(prog(t, COLL, HIT2))
        circle(ctx, W + U * 0.05, H * 0.15, U * 0.38 * ci * (1 + breathe) * (1 - coll), YELLOW)
        circle(ctx, -U * 0.08, H * 0.92, U * 0.3 * ci * (1 - coll), DEEP)

        # знак: выпрыгивает на ударе, уходит наверх
        up = expo_inout(prog(t, 1.6 * B, 2.6 * B))
        md0 = U * (0.34 if vertical else 0.3)
        hs = U * (0.13 if vertical else 0.095)
        ts = U * (0.036 if vertical else 0.024)
        ph = ts * 2.6; gap = ts * 0.6
        # весь блок (знак + заголовок + контакты) центрируется по вертикали
        block = md0 * 0.55 + U * 0.06 + hs * 1.9 + hs * 0.55 + 4 * ph + 3 * gap
        my_top = cy - block / 2 + md0 * 0.55 / 2
        md = md0 * lerp(1, 0.55, up)
        my = lerp(cy, my_top, up)
        my = lerp(my, cy, coll)
        md = lerp(md, U * 0.22, coll)
        pz = expo_out(prog(t, HIT1 + 0.05, HIT1 + 0.45))
        mark(ctx, cx, my, md * (1 + breathe), 0, WHITE, BLUE, circ=back_out(prog(t, HIT1, HIT1 + 0.35), 2.2),
             split=(1 - pz) * 0.9 + math.sin(math.pi * prog(t, COLL, HIT2)) * 0.25, skew=-(1 - pz) * 0.7,
             zalpha=clamp(prog(t, HIT1 + 0.05, HIT1 + 0.12)))

        # заголовок
        hy = my + md * 0.5 + U * 0.06 + hs * 0.8
        lines = [("ДАВАЙТЕ", WHITE), ("СОЗДАДИМ", YELLOW)]
        for i, (ln, col) in enumerate(lines):
            p = expo_out(prog(t, 2.3 * B + i * 0.08, 3.4 * B + i * 0.08))
            q = expo_in(prog(t, COLL - 0.1, COLL + 0.25))
            if p <= 0 or q >= 1: continue
            y = hy + i * hs * 0.95
            ctx.save(); ctx.rectangle(0, y - hs * 0.95, W, hs * 1.05); ctx.clip()
            text(ctx, INT, ln, hs, cx, y + hs * 1.3 * (1 - p) - hs * q * 1.3, col, -0.03, anchor="center")
            ctx.restore()

        # контакты: плашки выезжают слева по очереди
        pw_ = min(W * 0.86, U * (0.9 if vertical else 0.62))
        y0 = hy + hs * 1.45
        for i, (lab, val) in enumerate(CONTACTS):
            p = expo_out(prog(t, 3.6 * B + i * 0.12, 4.8 * B + i * 0.12))
            q = expo_in(prog(t, COLL - 0.15 + i * 0.03, COLL + 0.2 + i * 0.03))
            if p <= 0 or q >= 1: continue
            x = cx - pw_ / 2 - W * (1 - p) + W * q * 1.2
            y = y0 + i * (ph + gap)
            pill(ctx, x, y, pw_, ph, WHITE, 0.14)
            pill(ctx, x + ph * 0.18, y + ph * 0.18, ph * 0.64, ph * 0.64, YELLOW)
            text(ctx, INT, str(i + 1), ts * 0.9, x + ph * 0.5, y + ph * 0.62, INK, 0, anchor="center")
            text(ctx, INT, lab, ts * 0.75, x + ph * 1.05, y + ph * 0.6, YELLOW, 0.3)
            _, lw = INT.layout(lab, ts * 0.75, 0.3)
            text(ctx, INT, val, ts, x + ph * 1.05 + lw + ts * 1.2, y + ph * 0.64, WHITE, 0.02)
        return

    # 3. финал: логотип на синем, удар
    Lo = layout(W, H, vertical, 0.9)
    ci = expo_out(prog(t, HIT2, HIT2 + 0.7))
    circle(ctx, W + U * 0.1, -U * 0.1, U * 0.45 * ci, DEEP)
    circle(ctx, -U * 0.12, H + U * 0.12, U * 0.4 * ci, YELLOW)
    mc = Lo["mark"]
    pe = expo_out(prog(t, HIT2, HIT2 + 0.4))
    mark(ctx, mc[0], mc[1], Lo["MD"], 0, WHITE, BLUE, circ=back_out(prog(t, HIT2 - 0.02, HIT2 + 0.3), 2.2),
         split=(1 - pe) * 0.9, skew=-(1 - pe) * 0.6, zalpha=clamp(prog(t, HIT2, HIT2 + 0.08)))
    pw = expo_out(prog(t, HIT2 + 0.1, HIT2 + 0.7))
    wx, wb, WS, ww = Lo["word_x"], Lo["word_base"], Lo["WS"], Lo["ww"]
    ctx.save(); ctx.rectangle(wx - 5, wb - WS, (ww + 10) * pw, WS * 1.3); ctx.clip()
    text(ctx, UNB, "mazzeru", WS, wx, wb, WHITE, -0.06); ctx.restore()
    if 0 < pw < 1:
        ctx.rectangle(wx + ww * pw, wb - WS, U * 0.012, WS * 1.3); rgb(ctx, YELLOW); ctx.fill()
    ts = U * (0.03 if vertical else 0.024)
    ty = (wb + U * 0.14) if vertical else (cy + Lo["M"] * 0.5 + U * 0.12)
    pt = expo_out(prog(t, HIT2 + 0.45, HIT2 + 0.95))
    text(ctx, INT, "@mazzeru.studio", ts * 1.3, cx, ty + U * 0.03 * (1 - pt), YELLOW, 0.02, pt, anchor="center")
    pa = expo_out(prog(t, HIT2 + 0.65, HIT2 + 1.15))
    text(ctx, INT, "AI VIDEO / WEB / MOBILE FILM", ts * 0.85, cx, ty + U * 0.075, WHITE, 0.32, pa * 0.8, anchor="center")
    if t < HIT2 + 0.2:
        rgb(ctx, WHITE, 1 - prog(t, HIT2, HIT2 + 0.2)); ctx.paint()


# =====================================================================
SCENES = {"intro": (scene_intro, INTRO_END, "mazzeru-intro-music.wav", "mazzeru-intro"),
          "outro": (scene_outro, OUTRO_END, "mazzeru-outro-music.wav", "mazzeru-outro")}


def frame(scene, t, W, H, vertical, blur=3):
    acc = None
    samples = [t + (k / blur - 0.5) / FPS * 0.9 for k in range(blur)] if blur > 1 else [t]
    for ts in samples:
        surf = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H)
        ctx = cairo.Context(surf); ctx.set_antialias(cairo.ANTIALIAS_BEST)
        scene(ctx, max(0, ts), W, H, vertical)
        arr = np.ndarray((H, W, 4), np.uint8, surf.get_data()).astype(np.float32)
        acc = arr if acc is None else acc + arr
    acc /= len(samples)
    return acc[:, :, [2, 1, 0]].astype(np.uint8)


def render(kind, orient, preview=False):
    scene, T, music, name = SCENES[kind]
    vertical = orient == "vertical"
    W, H = (1080, 1920) if vertical else (1920, 1080)
    if preview:
        from PIL import Image
        ts = [x * T / 10 for x in range(10)] + [T - 0.05]
        ims = [Image.fromarray(frame(scene, tt, W, H, vertical, 1)) for tt in ts]
        tw = 384 if not vertical else 162; th = int(tw * H / W)
        sheet = Image.new("RGB", ((tw + 8) * 6, (th + 8) * 2), "gray")
        for i, im in enumerate(ims):
            sheet.paste(im.resize((tw, th)), ((i % 6) * (tw + 8), (i // 6) * (th + 8)))
        p = os.path.join(OUT_DIR, f"preview-{kind}-{orient}.png"); sheet.save(p); print(p)
        return
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    out = os.path.join(OUT_DIR, f"{name}-{'9x16' if vertical else '16x9'}.mp4")
    cmd = [ff, "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
           "-i", os.path.join(OUT_DIR, music),
           "-c:v", "libx264", "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p", "-movflags", "+faststart",
           "-c:a", "aac", "-b:a", "256k", "-shortest", out]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    n = int(round(T * FPS))
    for i in range(n):
        proc.stdin.write(frame(scene, i / FPS, W, H, vertical).tobytes())
    proc.stdin.close(); proc.wait()
    print("saved", out)


if __name__ == "__main__":
    a = sys.argv[1:]
    render(a[0] if a else "intro", a[1] if len(a) > 1 else "landscape", "preview" in a)
