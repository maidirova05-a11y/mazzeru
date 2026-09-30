"""Новый знак Mazzeru: круг + две наклонные Z. Координаты сняты с исходника 1250×1250.
Используется всеми генераторами (сайт, логотипы, шаблоны, видео)."""

VIEWBOX = (45, 45, 1160, 1160)          # круг вписан в квадрат
CIRCLE = (625, 625, 580)                # cx, cy, r

# левая Z: верхняя планка + нижняя часть (между ними тонкий просвет, как в оригинале)
Z1_POLYS = [
    [(365, 491), (681, 491), (603, 573), (285, 573)],
    [(447, 587), (587, 587), (443, 697), (607, 697), (521, 783), (222, 783), (292, 710), (320, 686)],
]
# правая Z — одним контуром
Z2_POLYS = [
    [(729, 491), (1036, 491), (965, 566), (940, 588), (797, 697), (993, 697), (889, 783),
     (561, 783), (630, 716), (648, 700), (808, 573), (649, 573)],
]
ZZ_BBOX = (222, 491, 1036, 783)


def poly_d(polys):
    return " ".join("M" + " L".join(f"{x} {y}" for x, y in p) + "Z" for p in polys)


Z1_D = poly_d(Z1_POLYS)
Z2_D = poly_d(Z2_POLYS)
VB = " ".join(map(str, VIEWBOX))


def svg_mark(bg, z, cls="", extra=""):
    """полный знак: круг bg, ZZ цветом z"""
    c = f' class="{cls}"' if cls else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg"{c} viewBox="{VB}"{extra}>'
            f'<circle cx="{CIRCLE[0]}" cy="{CIRCLE[1]}" r="{CIRCLE[2]}" fill="{bg}"/>'
            f'<path d="{Z1_D}" fill="{z}"/><path d="{Z2_D}" fill="{z}"/></svg>')


def svg_zz(z):
    """только ZZ без круга"""
    x0, y0, x1, y1 = ZZ_BBOX
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0} {y0} {x1 - x0} {y1 - y0}" width="{x1 - x0}" height="{y1 - y0}">'
            f'<path d="{Z1_D}" fill="{z}"/><path d="{Z2_D}" fill="{z}"/></svg>')


def g_mark(bg, z, x=0, y=0, size=100):
    """знак как <g> для вставки в другой SVG: левый верхний угол (x, y), сторона size"""
    s = size / VIEWBOX[2]
    return (f'<g transform="translate({x} {y}) scale({s:.6f}) translate({-VIEWBOX[0]} {-VIEWBOX[1]})">'
            f'<circle cx="{CIRCLE[0]}" cy="{CIRCLE[1]}" r="{CIRCLE[2]}" fill="{bg}"/>'
            f'<path d="{Z1_D}" fill="{z}"/><path d="{Z2_D}" fill="{z}"/></g>')
