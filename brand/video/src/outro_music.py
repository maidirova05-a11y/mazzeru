"""Трек для аутро Mazzeru: тот же фонк-мир, что и в интро, но мягче и «на выдохе».
140 BPM, 15 долей (~6.4 с). Всё синтезировано на numpy — свободно для соцсетей.

  0–1   свуш-переход (шторка) + саб-падение
  1     мягкий удар: аккорд-пэд, ковбелл с эхом
  1–9   лёгкий грув: кик через долю, римшот, тихие хэты, 808 с глайдом, мелодия-эхо
  9–10  подъём
  10    финальный удар (логотип), длинный хвост, затухание к 15
"""
import os, wave
import numpy as np
from music import (SR, add, lp, hp, bp, t_, note, kick, bass808, hat, cowbell, swell, riser, impact, pad, rng)
import music as M

BEAT = 60 / 140
TOTAL = 15 * BEAT
N = int(TOTAL * SR) + SR
M.N = N
M.L = np.zeros(N); M.R = np.zeros(N)
B = BEAT


def rim():
    n = int(0.12 * SR); t = t_(n)
    x = bp(rng.standard_normal(n), 1500, 5000) * np.exp(-t * 60) + np.sin(2 * np.pi * 1700 * t) * np.exp(-t * 80) * 0.5
    return x * 0.5


def whoosh(length):
    """свуш: шум с фильтром, открывающимся и закрывающимся"""
    n = int(length * SR); t = t_(n); p = t / length
    cut = 300 + 7000 * np.sin(np.pi * p) ** 2
    return lp(rng.standard_normal(n), cut) * np.sin(np.pi * p) ** 1.5 * 0.7


def echo_bell(freq, t0, gain, repeats=4, delay=B * 0.75):
    for k in range(repeats):
        add(lp(cowbell(freq, 0.25), 3000 - k * 600), t0 + k * delay, gain * 0.5 ** k, 0.5 if k % 2 else -0.5)


# 0–1: свуш шторки, саб-падение
add(whoosh(B * 1.05), 0, 0.9)
n = int(B * SR); tt = t_(n)
add(np.sin(2 * np.pi * np.cumsum(120 - 70 * tt / B) / SR) * (tt / B) ** 2 * 0.5, 0, 0.8)

# 1: мягкий удар
add(kick(), B, 0.9)
add(pad([note(12, 87.3), note(15, 87.3), note(19, 87.3), note(22, 87.3)], 8 * B), B, 0.55)
add(hp(rng.standard_normal(int(1.2 * SR)), 4000) * np.exp(-t_(int(1.2 * SR)) * 3) * 0.25, B, 0.8)
echo_bell(440 * 2 ** (12 / 12), B, 0.55)

# 1–9: грув вполсилы
MEL = [12, 15, 17, 15, 19, 17, 15, 12]
for b in range(1, 9):
    t0 = b * B; rel = b - 1
    if rel % 2 == 0 and b > 1: add(kick(), t0, 0.75)
    if rel % 4 == 2: add(kick(), t0 + B * 0.75, 0.55)
    if rel % 2 == 1: add(rim(), t0, 0.7)
    for h in range(4):
        add(hat(open_=(h == 2 and rel % 2 == 1)), t0 + h * B / 4, 0.3 if h % 2 == 0 else 0.18, 0.4 if h % 2 else -0.4)
    if rel % 2 == 1:
        echo_bell(440 * 2 ** (MEL[rel] / 12), t0 + B / 2, 0.35, 3)
for b, semi, glide in [(1, 0, None), (3, 3, None), (5, 5, 3), (7, 3, 0)]:
    add(bass808(note(semi, 43.65), 2 * B * 0.97, note(glide, 43.65) if glide is not None else None), b * B, 0.75)

# 9–10: подъём + заикание ковбелла
add(riser(B, 500, 5000), 9 * B, 0.5)
add(swell(B), 9 * B, 0.6)
for k, dt in enumerate([0, .25, .45, .6, .72, .82, .9]):
    add(cowbell(440 * 2 ** (MEL[k] / 12), 0.05), 9 * B + dt * B, 0.35 + 0.05 * k)

# 10: финальный удар и хвост
add(impact(), 10 * B, 0.9)
add(kick(), 10 * B, 1.0)
add(bass808(note(0, 43.65), 5 * B), 10 * B, 0.85)
add(pad([note(12, 87.3), note(19, 87.3), note(24, 87.3), note(27, 87.3)], 5 * B + 0.5), 10 * B, 0.5)
echo_bell(880, 10 * B, 0.45, 5, B * 0.5)

# мастер
L, R = M.L, M.R
T = int(TOTAL * SR)
fade = np.ones(N); fs = int((TOTAL - 1.0) * SR); fade[fs:] = np.linspace(1, 0, N - fs) ** 2
ML = np.tanh(L * fade * 0.85)[:T]; MR = np.tanh(R * fade * 0.85)[:T]
pk = max(abs(ML).max(), abs(MR).max()); ML, MR = ML / pk * 0.95, MR / pk * 0.95
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "mazzeru-outro-music.wav")
with wave.open(out, "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((np.stack([ML, MR], 1) * 32767).astype("<i2").tobytes())
print("outro music ok", round(TOTAL, 3), "s")
