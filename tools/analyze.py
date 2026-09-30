import wave, numpy as np
w = wave.open(r'C:\Users\USER\OneDrive\Desktop\Mazzeru\brand\video\_track_mono.wav')
sr = w.getframerate(); x = np.frombuffer(w.readframes(w.getnframes()), '<i2').astype(np.float32) / 32768
print("dur", len(x) / sr)
hop = 256
n = len(x) // hop
fr = x[: n * hop].reshape(n, hop)
# низкочастотная энергия (грубо: сглаживание) и общая
low = np.convolve(x, np.ones(40) / 40, 'same')[: n * hop].reshape(n, hop)
e_low = np.sqrt((low ** 2).mean(1)); e_all = np.sqrt((fr ** 2).mean(1))
on = np.maximum(0, np.diff(np.log(e_all + 1e-4), prepend=0))
fps = sr / hop
# темп: автокорреляция онсетов
ac = np.correlate(on - on.mean(), on - on.mean(), 'full')[len(on) - 1:]
lags = np.arange(len(ac)) / fps
best = None
for bpm in np.arange(130, 150, 0.05):
    lag = 60 / bpm * fps
    v = sum(np.interp(lag * k, np.arange(len(ac)), ac) for k in (1, 2, 4, 8))
    if best is None or v > best[0]: best = (v, bpm)
bpm = best[1]; print("bpm", round(bpm, 2))
beat = 60 / bpm
# фаза: максимизируем онсеты на долях (по низу — кик)
onl = np.maximum(0, np.diff(np.log(e_low + 1e-4), prepend=0))
t = np.arange(n) / fps
bestp = max(np.arange(0, beat, 0.005), key=lambda ph: np.interp(np.arange(ph, t[-1], beat), t, onl).sum())
print("phase", round(bestp, 3))
# энергия по тактам (4 доли)
bars = np.arange(bestp, t[-1] - 4 * beat, 4 * beat)
for i, b0 in enumerate(bars):
    m = (t >= b0) & (t < b0 + 4 * beat)
    el = e_low[m].mean(); ea = e_all[m].mean()
    print(f"bar {i:3d} t={b0:7.2f}  low={el:.3f} all={ea:.3f} " + "#" * int(ea * 120))
