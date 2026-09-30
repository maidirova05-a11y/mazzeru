"""Генерация логотипов Mazzeru: SVG в кривых."""
import os
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

B = r"C:\Users\USER\OneDrive\Desktop\Mazzeru\brand"
os.makedirs(B + r"\logo\svg", exist_ok=True)

BLUE, YELLOW, WHITE, INK = "#0047FF", "#E7FF00", "#FAF8F2", "#0B0B0F"


def text_path(font_file, text, size, tracking_em=0.0, x0=0, y0=0):
    """Контур текста как SVG path. y0 — базовая линия. Возвращает (d, ширина)."""
    f = TTFont(font_file)
    gs = f.getGlyphSet()
    cmap = f.getBestCmap()
    upm = f["head"].unitsPerEm
    sc = size / upm
    pen = SVGPathPen(gs)
    x = 0
    for i, ch in enumerate(text):
        g = cmap.get(ord(ch))
        if g is None:
            continue
        tp = TransformPen(pen, (sc, 0, 0, -sc, x0 + x, y0))
        gs[g].draw(tp)
        x += gs[g].width * sc + (tracking_em * size if i < len(text) - 1 else 0)
    return pen.getCommands(), x


def cap_height(font_file, size):
    f = TTFont(font_file)
    return f["OS/2"].sCapHeight * size / f["head"].unitsPerEm, f["OS/2"].sxHeight * size / f["head"].unitsPerEm


UNB = B + r"\fonts\Unbounded-ExtraBold.ttf"
INTB = B + r"\fonts\InterTight-Bold.ttf"

# ---------- знак ZZ: круг + две наклонные Z (100x100) ----------
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import brand_mark as BM


def mark(bg, z, cut=None, x=0, y=0, s=1.0, rx=None):
    return BM.g_mark(bg, z, x, y, 100 * s)


def save(name, w, h, body, bg=None):
    rect = f'<rect width="{w}" height="{h}" fill="{bg}"/>' if bg else ""
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.0f} {h:.0f}" width="{w:.0f}" height="{h:.0f}">{rect}{body}</svg>\n'
    open(os.path.join(B, "logo", "svg", name + ".svg"), "w", encoding="utf-8").write(svg)


# Знак — 4 цветовые версии
save("mazzeru-mark-blue", 100, 100, mark(BLUE, "#FFFFFF", BLUE))
save("mazzeru-mark-white", 100, 100, mark("#FFFFFF", BLUE, "#FFFFFF"))
save("mazzeru-mark-yellow", 100, 100, mark(YELLOW, INK, YELLOW))
save("mazzeru-mark-black", 100, 100, mark(INK, YELLOW, INK))

# Вордмарк
WS = 200  # кегль
wd, ww = text_path(UNB, "mazzeru", WS, tracking_em=-0.06)
capH, xH = cap_height(UNB, WS)
pad = 4
top = xH  # высота строчных (в mazzeru нет выносных)
WH = top + pad * 2
for nm, col in [("blue", BLUE), ("black", INK), ("white", "#FFFFFF"), ("yellow", YELLOW)]:
    save(f"mazzeru-wordmark-{nm}", ww + pad * 2, WH, f'<path transform="translate({pad} {top + pad})" d="{wd}" fill="{col}"/>')

# Горизонтальный логотип: знак + вордмарк
def lockup(name, mk, word_col, bg=None, tagline_col=None):
    ms = WH * 1.02                      # знак чуть выше строчных
    gap = ms * 0.28
    w = ms + gap + ww + pad * 2
    h = ms
    body = mark(*mk, x=0, y=0, s=ms / 100)
    body += f'<path transform="translate({ms + gap} {(h - WH) / 2 + top + pad})" d="{wd}" fill="{word_col}"/>'
    if tagline_col:
        tsz = ms * 0.2
        td, tw = text_path(INTB, "AI VIDEO / WEB / MOBILE FILM", tsz, tracking_em=0.32)
        scale = min(1, ww / tw)
        body += f'<path transform="translate({ms + gap} {h + tsz * 1.9}) scale({scale})" d="{td}" fill="{tagline_col}"/>'
        h += tsz * 2.6
    if bg:
        m = h * 0.35
        body = f'<g transform="translate({m} {m})">{body}</g>'
        w, h = w + 2 * m, h + 2 * m
    save(name, w, h, body, bg)


lockup("mazzeru-logo-blue", (BLUE, "#FFFFFF", BLUE), BLUE)
lockup("mazzeru-logo-black", (INK, YELLOW, INK), INK)
lockup("mazzeru-logo-white", ("#FFFFFF", BLUE, "#FFFFFF"), "#FFFFFF")
lockup("mazzeru-logo-tagline-blue", (BLUE, "#FFFFFF", BLUE), BLUE, tagline_col=INK)
lockup("mazzeru-logo-on-blue", ("#FFFFFF", BLUE, "#FFFFFF"), "#FFFFFF", bg=BLUE)
lockup("mazzeru-logo-on-yellow", (BLUE, "#FFFFFF", BLUE), BLUE, bg=YELLOW)
lockup("mazzeru-logo-on-white", (BLUE, "#FFFFFF", BLUE), BLUE, bg=WHITE)
print(sorted(os.listdir(B + r"\logo\svg")))
