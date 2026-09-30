"""SVG → PNG через headless Edge (прозрачный фон), с обрезкой по содержимому."""
import os, subprocess, re, sys
from PIL import Image

EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
TMP = r"C:\Users\USER\AppData\Local\Temp\claude\C--Users-USER-OneDrive-Desktop-Mazzeru\dbded89a-b618-4a72-a2af-809ec598348c\scratchpad\render"
os.makedirs(TMP, exist_ok=True)


def render(html_path, out_png, w, h, crop_alpha=True):
    subprocess.run([EDGE, "--headless=new", "--disable-gpu", "--no-first-run", f"--user-data-dir={TMP}\\ud",
                    "--hide-scrollbars", "--virtual-time-budget=2500", "--allow-file-access-from-files", "--default-background-color=00000000", "--force-device-scale-factor=1",
                    f"--window-size={w},{h}", f"--screenshot={out_png}", "file:///" + html_path.replace("\\", "/")],
                   check=True, capture_output=True, timeout=120)
    im = Image.open(out_png).convert("RGBA")
    if crop_alpha:
        bb = im.getchannel("A").getbbox()
        if bb:
            im = im.crop(bb)
    im.save(out_png, optimize=True)
    return im.size


def svg_to_png(svg, png, width):
    txt = open(svg, encoding="utf-8").read()
    vw, vh = map(float, re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', txt).groups())
    h = round(width * vh / vw)
    html = os.path.join(TMP, "r.html")
    open(html, "w", encoding="utf-8").write(
        f'<html><body style="margin:0;background:transparent"><img src="file:///{svg.replace(chr(92), "/")}" style="width:{width}px;height:{h}px;display:block"></body></html>')
    return render(html, png, max(width, 520) + 20, h + 20)


if __name__ == "__main__":
    B = r"C:\Users\USER\OneDrive\Desktop\Mazzeru\brand\logo"
    os.makedirs(B + r"\png", exist_ok=True)
    for f in sorted(os.listdir(B + r"\svg")):
        name = f[:-4]
        width = 1024 if "mark" in name else 2400
        print(name, svg_to_png(os.path.join(B, "svg", f), os.path.join(B, "png", name + ".png"), width))
