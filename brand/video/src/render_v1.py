"""Интро-ролик Mazzeru: кадры на cairo (векторная графика со сглаживанием),
буквы — настоящие контуры шрифтов Unbounded и Inter Tight, склейка в MP4 через ffmpeg.
Запуск: python render.py [landscape|vertical] [preview]"""
import math, os, sys, subprocess
import numpy as np, cairo, imageio_ffmpeg
from fontTools.ttLib import TTFont
from fontTools.pens.basePen import BasePen

HERE = os.path.dirname(os.path.abspath(__file__))
BR = os.path.normpath(os.path.join(HERE, "..", ".."))
FPS = 30
BEAT = 60 / 128
T_END = 16 * BEAT  # 7.5 с

BLUE = (0 / 255, 71 / 255, 255 / 255)
YELLOW = (231 / 255, 255 / 255, 0)
WARM = (250 / 255, 248 / 255, 242 / 255)
INK = (11 / 255, 11 / 255, 15 / 255)
WHITE = (1, 1, 1)


# ---------------- шрифты → контуры ----------------
class CairoPen(BasePen):
    def __init__(self, gs, ctx):
        super().__init__(gs); self.ctx = ctx; self.cur = (0, 0)
    def _moveTo(self, p): self.ctx.move_to(*p); self.cur = p
    def _lineTo(self, p): self.ctx.line_to(*p); self.cur = p
    def _curveToOne(self, a, b, c): self.ctx.curve_to(*a, *b, *c); self.cur = c
    def _qCurveToOne(self, a, b):
        x0, y0 = self.cur
        c1 = (x0 + 2 / 3 * (a[0] - x0), y0 + 2 / 3 * (a[1] - y0))
        c2 = (b[0] + 2 / 3 * (a[0] - b[0]), b[1] + 2 / 3 * (a[1] - b[1]))
        self.ctx.curve_to(*c1, *c2, *b); self.cur = b
    def _closePath(self): self.ctx.close_path()


class Font:
    def __init__(self, path):
        self.f = TTFont(path); self.gs = self.f.getGlyphSet(); self.cmap = self.f.getBestCmap()
        self.upm = self.f["head"].unitsPerEm
        self.xh = self.f["OS/2"].sxHeight / self.upm
        self.cap = self.f["OS/2"].sCapHeight / self.upm

    def layout(self, text, size, tracking=0.0):
        """список (glyph, x) и ширина при кегле size"""
        out, x = [], 0.0
        for i, ch in enumerate(text):
            g = self.cmap.get(ord(ch))
            if g is None: continue
            out.append((g, x))
            x += self.gs[g].width / self.upm * size + (tracking * size if i < len(text) - 1 else 0)
        return out, x

    def draw_glyph(self, ctx, g, size):
        """рисует глиф в текущих координатах (базовая линия y=0)"""
        ctx.save(); s = size / self.upm; ctx.scale(s, -s)
        self.gs[g].draw(CairoPen(self.gs, ctx)); ctx.restore()


UNB = Font(os.path.join(BR, "fonts", "Unbounded-ExtraBold.ttf"))
INT = Font(os.path.join(BR, "fonts", "InterTight-Bold.ttf"))


# ---------------- помощники ----------------
def clamp(v, a=0.0, b=1.0): return max(a, min(b, v))
def prog(t, a, b): return clamp((t - a) / (b - a)) if b > a else float(t >= a)
def expo_out(p): return 1 if p >= 1 else 1 - 2 ** (-10 * p)
def expo_in(p): return 0 if p <= 0 else 2 ** (10 * p - 10)
def expo_inout(p):
    if p <= 0: return 0
    if p >= 1: return 1
    return 2 ** (20 * p - 10) / 2 if p < .5 else (2 - 2 ** (-20 * p + 10)) / 2
def back_out(p, s=1.9): p -= 1; return 1 + (s + 1) * p ** 3 + s * p ** 2
def lerp(a, b, p): return a + (b - a) * p
def beat_pulse(t, start, end):
    """0..1 импульс на каждой доле между start и end"""
    if t < start or t > end: return 0.0
    ph = ((t - start) % BEAT) / BEAT
    return math.exp(-ph * 9)


def rgb(ctx, c, a=1.0): ctx.set_source_rgba(c[0], c[1], c[2], a)


def circle(ctx, x, y, r, c, a=1.0):
    if r <= 0: return
    ctx.arc(x, y, r, 0, 2 * math.pi); rgb(ctx, c, a); ctx.fill()


# новый знак: круг + две наклонные Z (координаты исходника 1250×1250, центр круга 625,625)
Z1_POLYS = [
    [(365, 491), (681, 491), (603, 573), (285, 573)],
    [(447, 587), (587, 587), (443, 697), (607, 697), (521, 783), (222, 783), (292, 710), (320, 686)],
]
Z2_POLYS = [
    [(729, 491), (1036, 491), (965, 566), (940, 588), (797, 697), (993, 697), (889, 783),
     (561, 783), (630, 716), (648, 700), (808, 573), (649, 573)],
]


def mark(ctx, cx, cy, size, rot=0.0, bg=WHITE, z=BLUE, alpha=1.0, circ=1.0, split=0.0, skew=0.0, zalpha=1.0):
    """знак по центру (cx, cy), size — диаметр круга.
    circ — масштаб круга, split — разлёт Z в стороны (доля size), skew — скос Z, zalpha — прозрачность Z"""
    if size <= 0 or alpha <= 0: return
    ctx.save(); ctx.translate(cx, cy); ctx.rotate(rot)
    s = size / 1160
    if circ > 0:
        ctx.arc(0, 0, 580 * s * circ, 0, 2 * math.pi); rgb(ctx, bg, alpha); ctx.fill()
    if zalpha > 0:
        for polys, sign in ((Z1_POLYS, -1), (Z2_POLYS, 1)):
            ctx.save()
            ctx.translate(sign * split * size, 0)
            ctx.transform(cairo.Matrix(1, 0, skew, 1, -skew * 0, 0))   # скос по X вокруг центра
            ctx.scale(s, s); ctx.translate(-625, -625)
            for p in polys:
                ctx.move_to(*p[0])
                for q in p[1:]: ctx.line_to(*q)
                ctx.close_path()
            rgb(ctx, z, alpha * zalpha); ctx.fill(); ctx.restore()
    ctx.restore()


def text(ctx, font, s, size, x, y, color, tracking=0.0, alpha=1.0, per_letter=None, anchor="left"):
    """per_letter(i) -> (dy, alpha_mul, scale) для анимации по буквам"""
    glyphs, w = font.layout(s, size, tracking)
    if anchor == "center": x -= w / 2
    for i, (g, gx) in enumerate(glyphs):
        dy, am, sc = per_letter(i) if per_letter else (0, 1, 1)
        if am * alpha <= 0.001: continue
        ctx.save(); ctx.translate(x + gx, y + dy)
        if sc != 1: ctx.scale(sc, sc)
        ctx.new_path(); font.draw_glyph(ctx, g, size); rgb(ctx, color, am * alpha); ctx.fill(); ctx.restore()
    return w


# ---------------- сцена ----------------
def scene(ctx, t, W, H, vertical):
    U = min(W, H)                                # опорная единица
    cx, cy = W / 2, H / 2

    # раскладка логотипа
    M = U * (0.25 if vertical else 0.2)          # сторона знака
    WS = M * 1.02 / UNB.xh                       # кегль слова: высота строчных ≈ знаку
    _, ww = UNB.layout("mazzeru", WS, -0.06)
    if vertical:
        WS *= min(1, (W * 0.84) / ww); _, ww = UNB.layout("mazzeru", WS, -0.06)
        mark_final = (cx, cy - M * 0.9)
        word_x, word_base = cx - ww / 2, cy + M * 0.35 + UNB.xh * WS
        tag_y = word_base + U * 0.12
    else:
        MD = M * 1.22
        gap = M * 0.24; total = MD + gap + ww
        f = min(1, W * 0.72 / total)             # логотип занимает не больше 72% ширины
        M *= f; WS *= f; gap *= f; MD *= f
        _, ww = UNB.layout("mazzeru", WS, -0.06); total = MD + gap + ww
        left = cx - total / 2
        mark_final = (left + MD / 2, cy - U * 0.03)
        word_x, word_base = left + MD + gap, cy - U * 0.03 + UNB.xh * WS / 2
        tag_y = cy + M * 0.5 + U * 0.11

    # ---------- фон ----------
    # 0–0.9 с: синий круг вырастает из центра на тёплом белом
    rgb(ctx, WARM); ctx.paint()
    diag = math.hypot(W, H) / 2
    grow = expo_inout(prog(t, 0.05, 0.9))
    if t < 5.65:
        circle(ctx, cx, cy, diag * 1.05 * grow, BLUE)

    # жёлтый разрез по диагонали 0.55–1.15
    p_in, p_out = expo_inout(prog(t, 0.55, 0.9)), expo_inout(prog(t, 0.95, 1.3))
    if 0.55 < t < 1.3:
        ctx.save(); ctx.translate(cx, cy); ctx.rotate(-math.radians(32))
        L = diag * 2.4; h = U * 0.2
        x0 = -L / 2 + L * p_out; x1 = -L / 2 + L * p_in
        ctx.rectangle(x0, -h / 2, max(0, x1 - x0), h); rgb(ctx, YELLOW); ctx.fill(); ctx.restore()

    # фоновые круги в груве 2.8–4.7: жёлтый справа снизу, тёмно-синий слева сверху
    if 2.5 < t < 5.2:
        e = back_out(prog(t, 2.6, 3.3), 1.4); ex = expo_in(prog(t, 4.6, 5.0))
        pulse = beat_pulse(t, 2 * BEAT, 10 * BEAT)
        r = U * 0.34 * e * (1 + 0.03 * pulse) * (1 - ex)
        circle(ctx, W - U * 0.05, H + U * 0.02, r, YELLOW)
        circle(ctx, U * 0.02, -U * 0.02, U * 0.22 * e * (1 - ex), (0 / 255, 51 / 255, 196 / 255))

    # кольца от знака на каждую долю
    if 2 * BEAT < t < 10 * BEAT:
        for k in range(2, 10):
            tb = k * BEAT; age = t - tb
            if 0 <= age < 1.2:
                p = expo_out(age / 1.2)
                ctx.arc(*mark_final, M * (0.6 + 2.2 * p), 0, 2 * math.pi)
                ctx.set_line_width(U * 0.006 * (1 - p) + 0.5)
                rgb(ctx, WHITE, 0.45 * (1 - p)); ctx.stroke()

    # ---------- знак ----------
    pulse = beat_pulse(t, 4 * BEAT, 10 * BEAT) * 0.04
    if t < 5.63:
        # появление: круг выпрыгивает 0.70–1.05, Z влетают с боков со скосом и защёлкиваются 0.80–1.20
        circ = back_out(prog(t, 0.70, 1.05), 2.2)
        pin = expo_out(prog(t, 0.80, 1.20))
        split = (1 - pin) * 1.5
        skew = -(1 - pin) * 0.9
        zal = clamp(prog(t, 0.80, 0.95))
        # в груве Z коротко разъезжаются на каждую долю
        split += beat_pulse(t, 4 * BEAT, 10 * BEAT) * 0.07
        # перед пролётом: Z разлетаются и схлопываются обратно
        split += math.sin(math.pi * prog(t, 4.78, 5.1)) * 0.35
        shift = expo_inout(prog(t, 1.15, 1.7))
        back = expo_inout(prog(t, 4.75, 5.05))         # возврат в центр перед пролётом
        mx = lerp(lerp(cx, mark_final[0], shift), cx, back)
        my = lerp(lerp(cy, mark_final[1], shift), cy, back)
        rot = expo_inout(prog(t, 4.9, 5.63)) * math.pi * 2
        zoom = 1 + expo_in(prog(t, 5.05, 5.63)) * 34      # пролёт сквозь знак
        size = M * 1.22 * (1 + pulse) * zoom
        if t >= 0.70:
            mark(ctx, mx, my, size, rot, circ=circ, split=split, skew=skew, zalpha=zal)

    # ---------- слово ----------
    if 1.2 < t < 5.1:
        def pl(i):
            p = expo_out(prog(t, 1.25 + i * 0.055, 1.85 + i * 0.055))
            q = expo_in(prog(t, 4.62 + i * 0.03, 4.95 + i * 0.03))
            return (WS * 1.1 * (1 - p) - WS * 1.2 * q, clamp(p * 1.4) * (1 - q), 1)
        ctx.save()
        # клип: буквы выезжают из-под линии, как в интро сайта
        ctx.rectangle(0, word_base - WS * 1.05, W, WS * 1.3); ctx.clip()
        sc = 1 + pulse
        ctx.translate(word_x, word_base); ctx.scale(sc, sc); ctx.translate(-word_x, -word_base)
        text(ctx, UNB, "mazzeru", WS, word_x, word_base, WHITE, -0.06, per_letter=pl)
        ctx.restore()

    # ---------- подпись ----------
    if 1.9 < t < 5.0:
        tag = "AI VIDEO / WEB / MOBILE FILM"
        ts = U * (0.03 if vertical else 0.026)
        p = expo_out(prog(t, 1.95, 2.9)); q = expo_in(prog(t, 4.55, 4.85))
        track = lerp(0.9, 0.32, p)
        text(ctx, INT, tag, ts, cx, tag_y, WHITE, track, alpha=clamp(p * 1.3) * (1 - q) * 0.9, anchor="center")

    # ---------- вспышка на финальном ударе ----------
    if 5.55 < t < 5.95:
        f = 1 - prog(t, 5.6, 5.95)
        rgb(ctx, WHITE, clamp(f)); ctx.paint()

    # ---------- финальная карточка ----------
    if t >= 5.6:
        e = expo_out(prog(t, 5.62, 6.4))
        # круги въезжают в углы, не задевая логотип
        circle(ctx, W + U * 0.12, -U * 0.05, U * 0.45 * e, BLUE)
        circle(ctx, -U * 0.08, H + U * 0.08, U * 0.36 * e, YELLOW)
        # логотип синим, уменьшенный вокруг своего центра
        s_end = 0.72 if not vertical else 0.8
        mfx, mfy = mark_final
        ly = (mfy + word_base - UNB.xh * WS / 2) / 2 if vertical else mfy
        ctx.save(); ctx.translate(cx, cy); ctx.scale(s_end, s_end); ctx.translate(-cx, -ly)
        pe = expo_out(prog(t, 5.7, 6.1))
        mark(ctx, mfx, mfy, M * 1.22, 0, BLUE, WHITE, circ=back_out(prog(t, 5.62, 6.0), 2.2),
             split=(1 - pe) * 0.9, skew=-(1 - pe) * 0.7, zalpha=clamp(prog(t, 5.7, 5.8)))
        def pl2(i):
            p = expo_out(prog(t, 5.7 + i * 0.04, 6.25 + i * 0.04))
            return (WS * (1 - p), clamp(p * 1.5), 1)
        ctx.save(); ctx.rectangle(-W, word_base - WS * 1.05, W * 3, WS * 1.3); ctx.clip()
        text(ctx, UNB, "mazzeru", WS, word_x, word_base, BLUE, -0.06, per_letter=pl2)
        ctx.restore(); ctx.restore()
        # подпись и контакты
        ts = U * (0.028 if vertical else 0.022)
        pt = expo_out(prog(t, 6.1, 6.7))
        bottom = cy + (word_base - ly) * s_end
        yy = bottom + U * 0.1 + U * 0.05 * (1 - pt)
        text(ctx, INT, "AI VIDEO / WEB / MOBILE FILM", ts, cx, yy, INK, 0.32, alpha=pt, anchor="center")
        pc = expo_out(prog(t, 6.35, 6.9))
        text(ctx, INT, "@mazzeru.studio", ts * 1.25, cx, yy + U * 0.08, BLUE, 0.02, alpha=pc, anchor="center")

    # затемнение в самом конце
    if t > T_END - 0.25:
        rgb(ctx, WARM, prog(t, T_END - 0.25, T_END) * 0.0); ctx.paint()


def frame(t, W, H, vertical, blur=3):
    """кадр с motion blur: среднее нескольких моментов внутри кадра"""
    acc = None
    samples = [t + (k / blur - 0.5) / FPS * 0.9 for k in range(blur)] if blur > 1 else [t]
    for ts in samples:
        surf = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H)
        ctx = cairo.Context(surf); ctx.set_antialias(cairo.ANTIALIAS_BEST)
        scene(ctx, max(0, ts), W, H, vertical)
        arr = np.ndarray((H, W, 4), np.uint8, surf.get_data()).astype(np.float32)
        acc = arr if acc is None else acc + arr
    acc /= len(samples)
    return acc[:, :, [2, 1, 0]].astype(np.uint8)   # BGRx → RGB


def render(orient, preview=False):
    vertical = orient == "vertical"
    W, H = (1080, 1920) if vertical else (1920, 1080)
    out_dir = os.path.normpath(os.path.join(HERE, ".."))
    if preview:
        from PIL import Image
        for tt in [0.5, 0.8, 1.0, 1.5, 2.2, 3.0, 4.8, 5.4, 6.0, 7.2]:
            Image.fromarray(frame(tt, W, H, vertical, 1)).save(os.path.join(out_dir, f"preview-{orient}-{tt:.1f}.png"))
        return
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    out = os.path.join(out_dir, f"mazzeru-intro-{'9x16' if vertical else '16x9'}.mp4")
    cmd = [ff, "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
           "-i", os.path.join(out_dir, "mazzeru-intro-music.wav"),
           "-c:v", "libx264", "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p", "-movflags", "+faststart",
           "-c:a", "aac", "-b:a", "256k", "-shortest", out]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    n = int(round(T_END * FPS))
    for i in range(n):
        proc.stdin.write(frame(i / FPS, W, H, vertical).tobytes())
        if i % 30 == 0: print(orient, i, "/", n, flush=True)
    proc.stdin.close(); proc.wait()
    print("saved", out)


if __name__ == "__main__":
    render(sys.argv[1] if len(sys.argv) > 1 else "landscape", "preview" in sys.argv)
