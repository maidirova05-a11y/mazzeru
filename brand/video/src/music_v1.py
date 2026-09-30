"""Оригинальный трек для интро Mazzeru: 128 BPM, 16 долей (7.5 с).
Синтез с нуля на numpy — без чужих сэмплов, можно свободно использовать в Instagram."""
import numpy as np, wave, os

SR = 44100
BPM = 128
BEAT = 60 / BPM          # 0.46875 с
TOTAL = 16 * BEAT        # 7.5 с
N = int(TOTAL * SR) + SR // 2
rng = np.random.default_rng(7)
mixL = np.zeros(N); mixR = np.zeros(N)


def add(sig, t0, gain=1.0, pan=0.0):
    i = int(t0 * SR)
    if i >= N: return
    sig = sig[: N - i]
    l = gain * np.cos((pan + 1) * np.pi / 4) * np.sqrt(2)
    r = gain * np.sin((pan + 1) * np.pi / 4) * np.sqrt(2)
    mixL[i:i + len(sig)] += sig * l
    mixR[i:i + len(sig)] += sig * r


def env(n, a=0.002, d=0.2, curve=4.0):
    t = np.arange(n) / SR
    e = np.minimum(1, t / max(a, 1e-4)) * np.exp(-curve * t / d)
    return e


def lowpass(x, cutoff):
    """однополюсный НЧ-фильтр; cutoff может быть массивом"""
    cutoff = np.broadcast_to(np.asarray(cutoff, float), x.shape)
    a = np.exp(-2 * np.pi * cutoff / SR)
    y = np.empty_like(x); prev = 0.0
    for k in range(len(x)):
        prev = (1 - a[k]) * x[k] + a[k] * prev
        y[k] = prev
    return y


def highpass(x, cutoff):
    return x - lowpass(x, cutoff)


def kick(len_s=0.45):
    n = int(len_s * SR); t = np.arange(n) / SR
    f = 45 + 110 * np.exp(-t * 32)
    ph = 2 * np.pi * np.cumsum(f) / SR
    body = np.sin(ph) * np.exp(-t * 7)
    click = rng.standard_normal(n) * np.exp(-t * 400) * 0.25
    return np.tanh((body + click) * 1.6)


def clap():
    n = int(0.3 * SR); t = np.arange(n) / SR
    noise = highpass(rng.standard_normal(n), 900)
    e = np.zeros(n)
    for off in (0, 0.011, 0.022):
        k = int(off * SR); e[k:] += np.exp(-(t[: n - k]) * 38)
    e += np.exp(-t * 12) * 0.35
    return noise * e * 0.5


def hat(open_=False):
    n = int((0.22 if open_ else 0.06) * SR); t = np.arange(n) / SR
    x = highpass(rng.standard_normal(n), 7000)
    return x * np.exp(-t * (14 if open_ else 70)) * 0.35


def saw(freq, n):
    t = np.arange(n) / SR
    out = np.zeros(n)
    for k in range(1, 18):
        out += np.sin(2 * np.pi * freq * k * t) / k * (-1) ** (k + 1)
    return out * (2 / np.pi)


def bass(freq, len_s):
    n = int(len_s * SR); t = np.arange(n) / SR
    x = saw(freq, n) * 0.6 + np.sin(2 * np.pi * freq / 2 * t) * 0.8
    cut = 180 + 900 * np.exp(-t * 18)
    return lowpass(x, cut) * env(n, 0.004, len_s, 2.5)


def pluck(freq, len_s=0.35):
    n = int(len_s * SR); t = np.arange(n) / SR
    x = saw(freq, n) * 0.5 + saw(freq * 1.005, n) * 0.5
    return lowpass(x, 600 + 5000 * np.exp(-t * 14)) * env(n, 0.002, 0.25, 5)


def pad(freqs, len_s, attack=0.05):
    n = int(len_s * SR); t = np.arange(n) / SR
    x = sum(saw(f, n) + saw(f * 1.004, n) for f in freqs) / len(freqs)
    e = np.minimum(1, t / attack) * np.exp(-t * 1.1)
    return lowpass(x, 1800) * e


def riser(len_s, f0=200, f1=2400):
    n = int(len_s * SR); t = np.arange(n) / SR
    p = t / len_s
    noise = rng.standard_normal(n)
    sweep = lowpass(noise, f0 + (f1 * 3 - f0) * p ** 2)
    f = f0 + (f1 - f0) * p ** 2
    tone = np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.25
    return (sweep * 0.6 + tone) * p ** 1.6


def impact():
    n = int(1.6 * SR); t = np.arange(n) / SR
    f = 38 + 70 * np.exp(-t * 9)
    boom = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 2.2)
    crash = highpass(rng.standard_normal(n), 3000) * np.exp(-t * 3.2) * 0.35
    return np.tanh((boom * 1.4 + crash) * 1.3)


def swoosh(len_s=0.5):
    n = int(len_s * SR); t = np.arange(n) / SR
    p = t / len_s
    x = lowpass(rng.standard_normal(n), 300 + 7000 * p ** 3)
    return x * np.sin(np.pi * p) ** 2


A = 110.0  # ля

def note(semi):
    return A * 2 ** (semi / 12)


# 0 → 2 доли: подъём к первому удару
add(riser(2 * BEAT), 0, 0.55)
# доля 2: удар — знак появляется
add(impact(), 2 * BEAT, 0.9)
# доли 2–10: грув
bassline = [0, 0, 7, 5, 0, 0, 3, 5]  # ля-минор
for b in range(2, 10):
    t0 = b * BEAT
    add(kick(), t0, 0.95)
    if b % 2 == 1:
        add(clap(), t0, 0.55, 0.05)
    for h in range(2):
        add(hat(open_=(h == 1 and b % 2 == 1)), t0 + h * BEAT / 2, 0.45, 0.35 if h else -0.35)
    add(bass(note(bassline[b - 2] - 12), BEAT * 0.9), t0 + BEAT / 2, 0.55)
# арпеджио поверх
arp = [12, 15, 19, 22, 19, 15]
k = 0
for s in range(4 * 2, 4 * 10):          # шестнадцатые с 2-й по 10-ю долю
    if s % 2 == 0 or s % 3 == 0:
        add(pluck(note(arp[k % len(arp)] + 12), 0.3), s * BEAT / 4, 0.16, 0.5 if k % 2 else -0.5)
        k += 1
# доли 10–12: взлёт в знак
add(swoosh(2 * BEAT), 10 * BEAT, 0.7)
add(riser(2 * BEAT, 400, 5000), 10 * BEAT, 0.35)
for s in range(8):                       # «стучащий» снейр-ролл
    add(clap(), 10 * BEAT + s * BEAT / 4, 0.15 + 0.05 * s)
# доля 12: финальный удар и аккорд
add(impact(), 12 * BEAT, 1.0)
add(kick(), 12 * BEAT, 0.9)
add(pad([note(0), note(3), note(7), note(12), note(15)], TOTAL - 12 * BEAT + 0.4, 0.02), 12 * BEAT, 0.35)
add(pluck(note(24), 1.2), 12 * BEAT, 0.25)

# мастер: плавное затухание, лимитер
fade = np.ones(N)
fs = int((TOTAL - 0.6) * SR)
fade[fs:] = np.linspace(1, 0, N - fs) ** 2
L = np.tanh(mixL * fade * 0.9) ; R = np.tanh(mixR * fade * 0.9)
peak = max(abs(L).max(), abs(R).max())
L, R = L / peak * 0.95, R / peak * 0.95
L = L[: int(TOTAL * SR)]; R = R[: int(TOTAL * SR)]

out = os.path.join(os.path.dirname(__file__), "..", "mazzeru-intro-music.wav")
with wave.open(out, "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    data = (np.stack([L, R], 1) * 32767).astype("<i2")
    w.writeframes(data.tobytes())
print("music ok", round(TOTAL, 3), "s")
