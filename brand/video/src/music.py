"""Трек для интро Mazzeru v2: фонк/трэп, 140 BPM в половинном темпе, 18 долей (~7.7 с).
Всё синтезировано с нуля на numpy — без чужих сэмплов, можно свободно использовать в соцсетях.

Структура (в долях, 1 доля = 0.4286 с):
  0–3   вступление: реверсный свелл, приглушённая ковбелл-мелодия, подъём
  3     ДРОП: 808 + кик + клэп + хэты + открытая ковбелл-мелодия
  3–13  грув
  13–14 стоп: тишина + глитч-заикание
  14    удар, длинный 808, аккорд, затухание до 18
"""
import numpy as np, wave, os

SR = 44100
BPM = 140
BEAT = 60 / BPM
TOTAL = 18 * BEAT
N = int(TOTAL * SR) + SR
rng = np.random.default_rng(11)
L = np.zeros(N); R = np.zeros(N)


def add(sig, t0, gain=1.0, pan=0.0):
    i = int(t0 * SR)
    if i >= N or i < 0: return
    sig = sig[: N - i]
    L[i:i + len(sig)] += sig * gain * (1 - max(0, pan))
    R[i:i + len(sig)] += sig * gain * (1 + min(0, pan))


def lp(x, cutoff):
    cutoff = np.broadcast_to(np.asarray(cutoff, float), x.shape)
    a = np.exp(-2 * np.pi * cutoff / SR)
    y = np.empty_like(x); p = 0.0
    for k in range(len(x)):
        p = (1 - a[k]) * x[k] + a[k] * p; y[k] = p
    return y


def hp(x, cutoff): return x - lp(x, cutoff)


def bp(x, lo, hi): return hp(lp(x, hi), lo)


def t_(n): return np.arange(n) / SR


def note(semi, base=55.0): return base * 2 ** (semi / 12)


# ---------- инструменты ----------
def kick():
    n = int(0.35 * SR); t = t_(n)
    f = 50 + 140 * np.exp(-t * 40)
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 9)
    return np.tanh(x * 2.2 + rng.standard_normal(n) * np.exp(-t * 500) * 0.3)


def bass808(f0, length, glide_to=None, glide_at=0.6):
    """808: синус с «щелчком», длинный хвост, опциональный глайд"""
    n = int(length * SR); t = t_(n)
    f = np.full(n, f0) * (1 + 1.8 * np.exp(-t * 60))
    if glide_to:
        g0 = int(glide_at * n)
        f[g0:] = f0 + (glide_to - f0) * (1 - np.exp(-(t[g0:] - t[g0]) * 18))
    x = np.sin(2 * np.pi * np.cumsum(f) / SR)
    env = np.minimum(1, t / 0.004) * np.exp(-t * 1.1)
    env[-int(0.02 * SR):] *= np.linspace(1, 0, int(0.02 * SR))
    return np.tanh(x * env * 2.6) * 0.9


def clap():
    n = int(0.35 * SR); t = t_(n)
    x = bp(rng.standard_normal(n), 900, 6000)
    e = np.zeros(n)
    for off in (0, 0.009, 0.019, 0.03):
        k = int(off * SR); e[k:] += np.exp(-t[: n - k] * 45)
    e += np.exp(-t * 9) * 0.4
    return np.tanh(x * e * 1.4) * 0.6


def hat(open_=False):
    n = int((0.25 if open_ else 0.05) * SR); t = t_(n)
    x = hp(rng.standard_normal(n), 8000)
    return x * np.exp(-t * (12 if open_ else 90)) * 0.4


def cowbell(freq, length=0.22):
    """фонк-ковбелл: два прямоугольника в неровной квинте + полосовой фильтр"""
    n = int(length * SR); t = t_(n)
    sq = np.sign(np.sin(2 * np.pi * freq * t)) + np.sign(np.sin(2 * np.pi * freq * 1.48 * t))
    x = bp(sq, 500, 4000) * np.exp(-t * 11)
    return x * 0.35


def swell(length):
    """реверсная тарелка: шум, нарастающий к концу"""
    n = int(length * SR); t = t_(n)
    x = hp(rng.standard_normal(n), 3000)
    return x * (t / length) ** 3 * 0.6


def riser(length, f0=300, f1=3000):
    n = int(length * SR); t = t_(n); p = t / length
    f = f0 + (f1 - f0) * p ** 2
    tone = np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.3
    noise = lp(rng.standard_normal(n), 400 + 6000 * p ** 2) * 0.5
    return (tone + noise) * p ** 2


def impact():
    n = int(2.2 * SR); t = t_(n)
    f = 35 + 90 * np.exp(-t * 7)
    boom = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 1.6)
    crash = hp(rng.standard_normal(n), 2500) * np.exp(-t * 2.6) * 0.3
    return np.tanh((boom * 1.5 + crash) * 1.4)


def pad(freqs, length):
    n = int(length * SR); t = t_(n)
    x = sum(np.sin(2 * np.pi * f * t) + 0.5 * np.sin(2 * np.pi * f * 2.002 * t) for f in freqs) / len(freqs)
    return lp(x, 2200) * np.minimum(1, t / 0.03) * np.exp(-t * 0.9) * 0.6


# ---------- аранжировка ----------
B = BEAT
MEL = [12, 12, 15, 12, 17, 15, 12, 10, 12, 12, 15, 19, 17, 15, 12, 10]   # фа-минор, фонк-ход (в полутонах)
COW = 440.0

# вступление: мелодия приглушена фильтром, свелл и подъём к дропу
for s in range(12):                                     # восьмые долей 0–3 (6 шт.) → 16-е для плотности
    t0 = s * B / 4
    if t0 >= 3 * B: break
    c = cowbell(COW * 2 ** (MEL[s % 16] / 12 - 1), 0.2)
    add(lp(c, 500 + 1500 * s / 12), t0, 0.7, -0.2 if s % 2 else 0.2)
add(swell(3 * B), 0, 0.9)
add(riser(3 * B), 0, 0.5)

# ДРОП и грув: доли 3–13
for b in range(3, 13):
    t0 = b * B
    rel = b - 3
    # кик: на долю и синкопа
    if rel % 2 == 0: add(kick(), t0, 1.0)
    if rel % 4 == 3: add(kick(), t0 + B / 2, 0.8)
    # клэп на «2 и 4» половинного темпа
    if rel % 2 == 1: add(clap(), t0, 0.8)
    # хэты 16-ми, дроби на каждой 4-й доле
    div = 8 if rel % 4 == 3 else 4
    for h in range(div):
        add(hat(open_=(div == 4 and h == 2 and rel % 2 == 1)), t0 + h * B / div, 0.5 if h % 2 == 0 else 0.35, 0.4 if h % 2 else -0.4)
    # ковбелл-мелодия 16-ми
    for s in range(4):
        idx = (rel * 4 + s) % 16
        if s == 3 and rel % 2 == 0: continue
        add(cowbell(COW * 2 ** (MEL[idx] / 12)), t0 + s * B / 4, 0.55, 0.25 if s % 2 else -0.25)

# 808-линия: длинные ноты с глайдами
bassline = [(3, 0, 2, None), (5, 0, 2, 3), (7, 5, 2, None), (9, 3, 2, 0), (11, 0, 2, -2)]
for b, semi, dur, glide in bassline:
    add(bass808(note(semi, 43.65), dur * B * 0.98, note(glide, 43.65) if glide is not None else None), b * B, 0.95)

# стоп и глитч: доля 13 — только нарезка ковбелла, ускоряющаяся
for k, dt in enumerate([0, 0.12, 0.22, 0.30, 0.36, 0.40]):
    add(cowbell(COW * 2 ** (MEL[k] / 12 + 0.25 * k / 12), 0.05), 13 * B + dt * B / 0.43, 0.6)
add(riser(B, 800, 6000), 13 * B, 0.45)

# доля 14: финальный удар
add(impact(), 14 * B, 1.0)
add(kick(), 14 * B, 1.0)
add(bass808(note(0, 43.65), 4 * B), 14 * B, 0.9)
add(pad([note(12, 87.3), note(15, 87.3), note(19, 87.3), note(24, 87.3)], 4 * B + 0.5), 14 * B, 0.5)
add(cowbell(COW * 2, 0.9), 14 * B, 0.4)

# мастер
T = int(TOTAL * SR)
fade = np.ones(N); fs = int((TOTAL - 0.7) * SR); fade[fs:] = np.linspace(1, 0, N - fs) ** 2
ML = np.tanh(L * fade * 0.85)[:T]; MR = np.tanh(R * fade * 0.85)[:T]
pk = max(abs(ML).max(), abs(MR).max()); ML, MR = ML / pk * 0.95, MR / pk * 0.95

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "mazzeru-intro-music.wav")
with wave.open(out, "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((np.stack([ML, MR], 1) * 32767).astype("<i2").tobytes())
print("music ok", round(TOTAL, 3), "s")
