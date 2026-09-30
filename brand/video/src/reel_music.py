"""Оригинальный трек для первого Reels Mazzeru (140 BPM, ми мажор, 48 долей ≈ 20.6 с).
Энергия UK-грайма/гаража: нарезанные «вокальные» аккорды, саб-бас, 2-step барабаны.
Всё синтезировано с нуля на numpy — без чужих записей, свободно для соцсетей.

Карта (в долях) совпадает с монтажом reel.py:
  0–8    вступление: вокальные стабы через открывающийся фильтр, подъём, дробь
  8      ДРОП (логотип)
  8–38   грув; на 14, 22, 30 — тарелка на смене сцены, перед ней сбивка
  38     удар (финальный экран), барабаны уходят, аккорд и эхо
  43–48  плавное затухание в тишину
"""
import os, wave
import numpy as np

SR = 44100
BPM = 140
B = 60 / BPM
TOTAL = 48 * B
N = int(TOTAL * SR) + SR
rng = np.random.default_rng(7)
L = np.zeros(N); R = np.zeros(N)

# доли, по которым синхронизируется анимация (импортируются в reel.py)
DROP, END_HIT = 8, 38
SCENES = [14, 22, 30]
def groove_kicks():
    out = []
    for bar in range(DROP, END_HIT, 4):
        out += [bar, bar + 1.5, bar + 2.75]
    return [k for k in out if k < END_HIT]
def groove_snares():
    return [b for bar in range(DROP, END_HIT, 4) for b in (bar + 1, bar + 3) if b < END_HIT]


def add(sig, t0, gain=1.0, pan=0.0):
    i = int(t0 * SR)
    if i >= N or i < 0: return
    sig = sig[: N - i]
    L[i:i + len(sig)] += sig * gain * (1 - max(0, pan))
    R[i:i + len(sig)] += sig * gain * (1 + min(0, pan))


def t_(n): return np.arange(n) / SR
def mtof(m): return 440 * 2 ** ((m - 69) / 12)


def lp(x, cutoff):
    cutoff = np.broadcast_to(np.asarray(cutoff, float), x.shape)
    a = np.exp(-2 * np.pi * cutoff / SR)
    y = np.empty_like(x); p = 0.0
    for k in range(len(x)):
        p = (1 - a[k]) * x[k] + a[k] * p; y[k] = p
    return y
def hp(x, c): return x - lp(x, c)


def reson(x, f, q):
    """двухполюсный резонатор (полосовой biquad)"""
    w = 2 * np.pi * f / SR; al = np.sin(w) / (2 * q)
    b0, a0, a1, a2 = al, 1 + al, -2 * np.cos(w), 1 - al
    b0, a1, a2 = b0 / a0, a1 / a0, a2 / a0
    y = np.zeros_like(x); x1 = x2 = y1 = y2 = 0.0
    for k in range(len(x)):
        v = b0 * x[k] - b0 * x2 - a1 * y1 - a2 * y2
        x2, x1 = x1, x[k]; y2, y1 = y1, v; y[k] = v
    return y


def saw(f, n, detune=0.0):
    t = t_(n); ph = np.cumsum(np.full(n, f * (1 + detune))) / SR
    return 2 * (ph % 1) - 1


# ---------- инструменты ----------
VOWELS = {"a": (800, 1150, 2800), "o": (500, 900, 2600), "e": (550, 1800, 2700)}
def voice(midi, length, vowel="a"):
    """«вокальная» нота: пила с вибрато через три форманты, короткая огибающая (эффект нарезки)"""
    n = int(length * SR); t = t_(n); f = mtof(midi)
    vib = 1 + 0.004 * np.sin(2 * np.pi * 5.5 * t)
    ph = np.cumsum(f * vib) / SR; src = 2 * (ph % 1) - 1
    F = VOWELS[vowel]
    y = reson(src, F[0], 6) + 0.7 * reson(src, F[1], 8) + 0.25 * reson(src, F[2], 10) + 0.15 * src
    env = np.minimum(1, t / 0.006) * np.minimum(1, (length - t) / 0.02)
    return y * env * 0.5


def chop(chord, length, vowel="a"):
    return sum(voice(m, length, vowel) for m in chord) / len(chord)


def kick():
    n = int(0.4 * SR); t = t_(n)
    f = 45 + 150 * np.exp(-t * 35)
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 7)
    return np.tanh(x * 2.5 + rng.standard_normal(n) * np.exp(-t * 600) * 0.4)


def snare():
    n = int(0.3 * SR); t = t_(n)
    body = np.sin(2 * np.pi * 190 * t) * np.exp(-t * 30) * 0.6
    noise = hp(rng.standard_normal(n), 1500) * np.exp(-t * 16)
    e = np.zeros(n)
    for off in (0, 0.011, 0.022):
        k = int(off * SR); e[k:] += np.exp(-t[: n - k] * 50)
    return np.tanh((body + noise * (0.6 + 0.4 * e)) * 1.3) * 0.6


def hat(open_=False):
    n = int((0.22 if open_ else 0.04) * SR); t = t_(n)
    return hp(rng.standard_normal(n), 7500) * np.exp(-t * (14 if open_ else 110)) * 0.35


def sub(f, length):
    n = int(length * SR); t = t_(n)
    x = np.sin(2 * np.pi * f * t) + 0.25 * np.sin(2 * np.pi * 2 * f * t)
    env = np.minimum(1, t / 0.005) * np.minimum(1, (length - t) / 0.03) * np.exp(-t * 0.8)
    return np.tanh(x * env * 1.8) * 0.8


def pad(chord, length, cutoff=2500):
    n = int(length * SR); t = t_(n)
    x = sum(saw(mtof(m), n, d) for m in chord for d in (-0.004, 0.004)) / (2 * len(chord))
    return lp(x, cutoff) * np.minimum(1, t / 0.4) * np.minimum(1, (length - t) / 0.5) * 0.5


def crash():
    n = int(1.6 * SR); t = t_(n)
    return hp(rng.standard_normal(n), 4000) * np.exp(-t * 2.2) * 0.35


def riser(length):
    n = int(length * SR); t = t_(n); p = t / length
    return lp(rng.standard_normal(n), 300 + 8000 * p ** 2) * p ** 2 * 0.6


def impact():
    n = int(2.5 * SR); t = t_(n)
    f = 32 + 100 * np.exp(-t * 6)
    return np.tanh(np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 1.3) * 1.6 + hp(rng.standard_normal(n), 3000) * np.exp(-t * 2.5) * 0.3)


# ---------- гармония: E – C#m – A – B, по такту (4 доли) ----------
CHORDS = [[64, 68, 71, 76], [61, 64, 68, 73], [61, 64, 69, 73], [63, 66, 71, 75]]
ROOTS = [82.41, 69.30, 55.00, 61.74]
def chord_at(beat): return int(beat // 4) % 4

# ритм нарезки внутри такта (в 16-х) и какой голос ведёт
CHOP_RHYTHM = [(0, 3), (3, 2), (6, 3), (8, 1), (10, 2), (12, 3), (14, 2)]

# 1. вступление: стабы через фильтр, без барабанов
for bar in range(0, 8, 4):
    for pos, top in CHOP_RHYTHM:
        b = bar + pos / 4
        c = CHORDS[chord_at(b)]
        s = chop(c[:3] + [c[top]], 0.16, "a")
        add(lp(s, 1100 + 4000 * (b / 8) ** 1.5), b * B, 2.4, -0.3 if pos % 4 else 0.3)
add(pad(CHORDS[0], 4 * B, 1500), 0, 1.0)
add(pad(CHORDS[1], 4 * B, 2200), 4 * B, 1.0)
INTRO_KICKS = [0, 1, 2, 3, 4, 5]   # на каждое появление строки хука
for k in INTRO_KICKS: add(lp(kick(), 900), k * B, 0.7)
for k in INTRO_KICKS: add(sub(ROOTS[chord_at(k)], 0.9 * B), k * B, 0.5)
add(riser(4 * B), 4 * B, 0.6)
for k in range(12):   # дробь малого, ускоряется к дропу
    b = 6 + 2 * (1 - (1 - k / 12) ** 1.6)
    add(snare(), b * B, 0.25 + 0.4 * k / 12)

# 2. грув 8–38
for k in groove_kicks(): add(kick(), k * B, 1.0)
for s in groove_snares(): add(snare(), s * B, 0.85)
for b16 in range(DROP * 4, END_HIT * 4):
    b = b16 / 4
    swing = 0.03 * B if b16 % 2 else 0
    op = (b16 % 8 == 6)
    add(hat(open_=op), b * B + swing, 0.5 if b16 % 2 == 0 else 0.3, 0.35 if b16 % 2 else -0.35)
for bar in range(DROP, END_HIT, 4):
    ci = chord_at(bar); c = CHORDS[ci]
    add(sub(ROOTS[ci], 1.45 * B), bar * B, 0.9)
    add(sub(ROOTS[ci], 1.2 * B), (bar + 1.5) * B, 0.8)
    add(sub(ROOTS[ci], 1.2 * B), (bar + 2.75) * B, 0.8)
    vowel = "a" if (bar // 4) % 2 == 0 else "o"
    for pos, top in CHOP_RHYTHM:
        b = bar + pos / 4
        if b >= END_HIT: break
        add(chop(c[:3] + [c[top] + 12 * (pos == 12)], 0.15, vowel), b * B, 0.75, -0.3 if pos % 4 else 0.3)
    add(pad(c, 4 * B, 1600), bar * B, 0.3)
# смены сцен: сбивка перед и тарелка на смене
for sc in [DROP] + SCENES:
    add(crash(), sc * B, 0.9)
    if sc != DROP:
        for k in range(4): add(snare(), (sc - 0.5 + k / 8) * B, 0.35 + 0.1 * k)
add(impact(), DROP * B, 0.9)

# 3. финал 38–48
add(impact(), END_HIT * B, 1.0)
add(kick(), END_HIT * B, 1.0)
add(crash(), END_HIT * B, 1.0)
add(sub(ROOTS[0], 5 * B), END_HIT * B, 0.8)
add(pad(CHORDS[0] + [59], 10 * B, 2200), END_HIT * B, 0.7)
for k, (b, m) in enumerate([(38, 76), (38.75, 73), (39.5, 71), (40.5, 76), (41.25, 75), (42, 71), (43, 68)]):
    add(chop([m, m - 12], 0.3, "a"), b * B, 0.7 * 0.85 ** k, 0.4 if k % 2 else -0.4)
for b in (40, 42): add(kick(), b * B, 0.5)
for b16 in range(38 * 4, 44 * 4, 2): add(hat(), b16 / 4 * B, 0.2, 0.3)

# мастер: затухание с 43-й доли в полную тишину к 48-й
T = int(TOTAL * SR)
fade = np.ones(N)
f0, f1 = int(43 * B * SR), T
fade[f0:f1] = np.cos(np.linspace(0, np.pi / 2, f1 - f0)) ** 2
fade[f1:] = 0
ML = np.tanh(L * fade * 0.8)[:T]; MR = np.tanh(R * fade * 0.8)[:T]
pk = max(abs(ML).max(), abs(MR).max()); ML, MR = ML / pk * 0.95, MR / pk * 0.95

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "mazzeru-reel-01-music.wav")
    with wave.open(out, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((np.stack([ML, MR], 1) * 32767).astype("<i2").tobytes())
    rms = [float(np.sqrt(np.mean(ML[int(b * B * SR):int((b + 1) * B * SR)] ** 2))) for b in range(48)]
    print("reel music ok", round(TOTAL, 2), "s")
    print(" ".join(f"{r:.2f}" for r in rms))
