import wave, numpy as np
from numpy.lib.stride_tricks import sliding_window_view as swv
w = wave.open(r'C:\Users\USER\AppData\Local\Temp\claude\C--Users-USER-OneDrive-Desktop-Mazzeru\dbded89a-b618-4a72-a2af-809ec598348c\scratchpad\head.wav')
sr = w.getframerate(); x = np.frombuffer(w.readframes(w.getnframes()), '<i2').astype(float) / 32768
nfft, hop = 2048, 256
frames = swv(x, nfft)[::hop] * np.hanning(nfft)
S = np.abs(np.fft.rfft(frames, axis=1)).T
def medfilt(a, k, axis):
    pad = [(0, 0), (0, 0)]; pad[axis] = (k // 2, k // 2)
    return np.median(swv(np.pad(a, pad, mode='edge'), k, axis=axis), axis=-1)
Hh = medfilt(S, 31, 1); Pp = medfilt(S, 31, 0)
Harm = S * (Hh ** 2 / (Hh ** 2 + Pp ** 2 + 1e-9))
f = np.fft.rfftfreq(nfft, 1 / sr)
voc = (f > 300) & (f < 3000)
L = np.log1p(Harm[voc] * 50)
flux = np.maximum(0, np.diff(L, axis=1, prepend=L[:, :1])).sum(0)
flux = np.convolve(flux, np.hanning(5) / 2.5, 'same')
fps = sr / hop; B = 60 / 140.15; ph = 0.045
thr = np.percentile(flux[: int(35 * fps)], 88)
peaks = [i for i in range(3, len(flux) - 4) if flux[i] == flux[i - 3:i + 4].max() and flux[i] > thr]
out = []
for i in peaks:
    t = i * hop / sr + nfft / 2 / sr * 0   # центр окна ~ начало кадра
    b = (t - ph) / B
    if b > 36 and b < 64: continue
    out.append((b, flux[i] / thr))
print("vocal onsets (beat, strength):")
print("  ".join(f"{b:5.2f}:{s:.1f}" for b, s in out if b < 81))
