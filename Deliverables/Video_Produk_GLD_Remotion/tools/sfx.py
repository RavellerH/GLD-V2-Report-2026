"""Sintesis sound effect video GLD (bebas lisensi, dibuat dari nol).

  python tools/sfx.py   -> tulis public/audio/sfx/*.wav

Gaya: korporat, lembut, tidak menutupi narasi. Hanya memakai pustaka standar Python.
"""
import array
import math
import random
import wave
from pathlib import Path

SR = 44100
OUT = Path(__file__).resolve().parent.parent / "public" / "audio" / "sfx"
random.seed(3)


def env(n, attack, release, curve=2.0):
    a, r = int(attack * SR), int(release * SR)
    out = []
    for i in range(n):
        if i < a:
            out.append((i / max(a, 1)) ** 0.7)
        else:
            out.append(max(0.0, 1 - (i - a) / max(r, 1)) ** curve)
    return out


def lowpass(x, cutoff):  # cutoff: float atau list per sampel (Hz), one-pole
    y, prev = [], 0.0
    for i, v in enumerate(x):
        c = cutoff[i] if isinstance(cutoff, list) else cutoff
        a = 1 - math.exp(-2 * math.pi * c / SR)
        prev += a * (v - prev)
        y.append(prev)
    return y


def highpass(x, cutoff):
    lp = lowpass(x, cutoff)
    return [v - l for v, l in zip(x, lp)]


def noise(n):
    return [random.uniform(-1, 1) for _ in range(n)]


def tone(n, f0, f1=None, harm=(1.0,), phase=0.0):
    out, ph = [], phase
    for i in range(n):
        f = f0 if f1 is None else f0 + (f1 - f0) * i / n
        ph += 2 * math.pi * f / SR
        out.append(sum(a * math.sin(ph * (k + 1)) for k, a in enumerate(harm)))
    return out


def mix(*tracks):
    n = max(len(t) for t in tracks)
    return [sum(t[i] for t in tracks if i < len(t)) for i in range(n)]


def save(name, x, peak=0.8):
    m = max(1e-9, max(abs(v) for v in x))
    pcm = array.array("h", (int(v / m * peak * 32767) for v in x))
    OUT.mkdir(parents=True, exist_ok=True)
    with wave.open(str(OUT / f"{name}.wav"), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())
    print(f"  {name}.wav  {len(x) / SR:.2f} dtk")


def whoosh(dur=0.9, lo=300, hi=3500):
    n = int(dur * SR)
    sweep = [lo + (hi - lo) * math.sin(math.pi * i / n) ** 2 for i in range(n)]
    x = highpass(lowpass(noise(n), sweep), 150)
    e = [math.sin(math.pi * i / n) ** 1.6 for i in range(n)]
    return [v * a for v, a in zip(x, e)]


def chime(freqs, step=0.11, decay=0.45):
    parts = []
    for k, f in enumerate(freqs):
        n = int((decay + 0.05) * SR)
        t = tone(n, f, harm=(1.0, 0.25, 0.08))
        e = env(n, 0.004, decay, 3.0)
        parts.append([0.0] * int(k * step * SR) + [v * a for v, a in zip(t, e)])
    return mix(*parts)


def build():
    print(f"Menulis SFX ke {OUT}")
    save("whoosh", whoosh(0.9), 0.55)                       # transisi antar-adegan
    save("whoosh_short", whoosh(0.45, 500, 4500), 0.6)      # coretan, gerak cepat
    n = int(0.14 * SR)                                      # pop lembut: kartu/label muncul
    save("pop", [v * a for v, a in zip(tone(n, 760, 560, (1.0, 0.15)), env(n, 0.003, 0.13, 3))], 0.55)
    n = int(0.09 * SR)                                      # blip: paket data / pergantian pola
    save("blip", [v * a for v, a in zip(tone(n, 1320, 1180), env(n, 0.002, 0.085, 2.5))], 0.45)
    n = int(0.035 * SR)                                     # tick: klik UI / katup
    save("tick", [v * a for v, a in zip(highpass(noise(n), 2000), env(n, 0.001, 0.03, 4))], 0.5)
    # alarm: 3x dua nada, tidak menusuk
    beeps = []
    for k in range(3):
        for j, f in enumerate((988, 784)):
            m = int(0.16 * SR)
            t = tone(m, f, harm=(1.0, 0.3))
            e = env(m, 0.01, 0.14, 1.5)
            beeps.append([0.0] * int((k * 0.42 + j * 0.18) * SR) + [v * a for v, a in zip(t, e)])
    save("alarm", mix(*beeps), 0.6)
    save("error", chime([523, 392], 0.16, 0.35), 0.5)       # CH gagal
    save("success", chime([659, 880, 1319], 0.1, 0.5), 0.5)  # rute pulih / klasifikasi
    # cabut kabel: snap + thump rendah
    n = int(0.25 * SR)
    snap = [v * a for v, a in zip(highpass(noise(n), 1500), env(n, 0.001, 0.04, 5))]
    thump = [v * a for v, a in zip(tone(n, 140, 70), env(n, 0.002, 0.2, 3))]
    save("unplug", mix(snap, [0.6 * v for v in thump]), 0.6)
    # dentang logam: tutup terlepas
    n = int(0.9 * SR)
    parts = [[v * a for v, a in zip(tone(n, f), env(n, 0.001, d, 3))] for f, d in ((1180, 0.8), (2730, 0.5), (4120, 0.3), (610, 0.6))]
    save("clank", mix(*parts, [0.4 * v for v in whoosh(0.3, 800, 5000)]), 0.45)
    # dengung pompa (loop 2 dtk)
    n = 2 * SR
    hum = mix(tone(n, 118, harm=(1.0, 0.5, 0.3, 0.15)), [0.08 * v for v in lowpass(noise(n), 900)])
    fade = int(0.05 * SR)
    hum = [v * min(1, i / fade, (n - i) / fade) for i, v in enumerate(hum)]
    save("hum", hum, 0.35)
    # riser: membangun ke penutup
    n = int(2.6 * SR)
    sweep = [400 + 5000 * (i / n) ** 2 for i in range(n)]
    riser = [v * (i / n) ** 1.5 for i, v in enumerate(lowpass(noise(n), sweep))]
    pad = [0.25 * v * (i / n) for i, v in enumerate(tone(n, 220, 440, (1.0, 0.4, 0.2)))]
    save("rise", mix(riser, pad), 0.5)


if __name__ == "__main__":
    build()
