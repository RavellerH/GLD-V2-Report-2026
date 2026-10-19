"""Musik latar ambient korporat (sintesis sendiri, bebas lisensi) -> public/audio/music.wav.

  python tools/music.py [durasi_detik]

Pad akor lembut + arpeggio pluck tipis + bass, tempo 100 BPM. Volume akhir diatur di Explainer.
"""
import sys
import wave
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "public" / "audio" / "music.wav"
SR = 44100
DUR = float(sys.argv[1]) if len(sys.argv) > 1 else 185.0
BAR = 60 / 100 * 4  # 2,4 dtk
rng = np.random.default_rng(7)


def hz(m):
    return 440.0 * 2 ** ((m - 69) / 12)


# Dmaj9 - Bm9 - Gmaj9 - Aadd9 (2 bar per akor)
CHORDS = [
    [50, 57, 62, 64, 66, 69],
    [47, 54, 59, 61, 62, 66],
    [43, 50, 55, 57, 59, 62],
    [45, 52, 57, 59, 61, 64],
]
CHORD_LEN = BAR * 2

n = int(DUR * SR)
t = np.arange(n) / SR
L = np.zeros(n)
R = np.zeros(n)


def env(length, attack, release):
    e = np.ones(length)
    a, r = int(attack * SR), int(release * SR)
    e[:a] = np.linspace(0, 1, a) ** 2
    e[-r:] *= np.linspace(1, 0, r) ** 2
    return e


# pad: tiap akor dirender dengan overlap agar transisi mulus
k = 0
start = 0.0
while start < DUR:
    notes = CHORDS[k % len(CHORDS)]
    s0 = int(start * SR)
    length = min(int((CHORD_LEN + 2.0) * SR), n - s0)
    if length <= 0:
        break
    tt = np.arange(length) / SR
    sig_l = np.zeros(length)
    sig_r = np.zeros(length)
    for j, m in enumerate(notes):
        f = hz(m)
        amp = 0.6 if j == 0 else 0.35
        for det, pan in ((-0.12, 0.8), (0.12, 0.2)):
            ph = rng.uniform(0, 2 * np.pi)
            w = np.sin(2 * np.pi * f * (1 + det / 100) * tt + ph) + 0.25 * np.sin(4 * np.pi * f * tt + ph)
            sig_l += amp * w * (1 - pan)
            sig_r += amp * w * pan
    e = env(length, 1.6, 2.2)
    trem = 1 + 0.08 * np.sin(2 * np.pi * 0.2 * tt)
    L[s0:s0 + length] += sig_l * e * trem
    R[s0:s0 + length] += sig_r * e * trem
    start += CHORD_LEN
    k += 1

# arpeggio pluck (mulai setelah intro), 8th note
step = BAR / 8
pl = int(0.9 * SR)
pt = np.arange(pl) / SR
i = 0
pos = 8.0
while pos < DUR - 6:
    notes = CHORDS[int(pos // CHORD_LEN) % len(CHORDS)]
    pattern = [notes[2] + 12, notes[4], notes[3] + 12, notes[5]]
    m = pattern[i % 4]
    s0 = int(pos * SR)
    seg = min(pl, n - s0)
    pluck = (np.sin(2 * np.pi * hz(m) * pt) + 0.3 * np.sin(2 * np.pi * hz(m) * 2 * pt)) * np.exp(-pt * 6)
    pan = 0.3 + 0.4 * ((i % 4) / 3)
    amp = 0.22 if i % 2 == 0 else 0.15
    L[s0:s0 + seg] += amp * pluck[:seg] * (1 - pan)
    R[s0:s0 + seg] += amp * pluck[:seg] * pan
    pos += step
    i += 1

# bass lembut di akar akor
k = 0
start = 0.0
while start < DUR:
    m = CHORDS[k % len(CHORDS)][0] - 12
    s0 = int(start * SR)
    length = min(int(CHORD_LEN * SR), n - s0)
    tt = np.arange(length) / SR
    b = np.sin(2 * np.pi * hz(m) * tt) * env(length, 0.4, 1.0) * 0.5
    L[s0:s0 + length] += b
    R[s0:s0 + length] += b
    start += CHORD_LEN
    k += 1

# echo sederhana untuk ruang
for d, g in ((0.36, 0.25), (0.72, 0.12)):
    s = int(d * SR)
    L[s:] += g * R[:-s]
    R[s:] += g * L[:-s]

# fade in/out & normalisasi ke -3 dBFS
fade = np.ones(n)
fi, fo = int(3 * SR), int(5 * SR)
fade[:fi] = np.linspace(0, 1, fi)
fade[-fo:] = np.linspace(1, 0, fo)
L *= fade
R *= fade
peak = max(np.abs(L).max(), np.abs(R).max())
L, R = L / peak * 0.7, R / peak * 0.7
pcm = (np.stack([L, R], axis=1) * 32767).astype("<i2")
OUT.parent.mkdir(parents=True, exist_ok=True)
with wave.open(str(OUT), "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(pcm.tobytes())
print(f"{OUT.relative_to(ROOT)}: {DUR:.1f} dtk")
