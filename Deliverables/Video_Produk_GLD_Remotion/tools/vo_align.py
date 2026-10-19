"""Potong rekaman utuh per adegan berdasarkan transkripsi (lebih akurat daripada proporsi teks).

  VO_VIDEO=ogi VO_LANG=id python tools/vo_align.py

Rekaman (_full.wav) dipecah di setiap jeda >= 0,3 dtk, semua potongan ditranskripsi dalam SATU panggilan
model teks, lalu awal tiap adegan dicari dari kata-kata pembuka naskahnya.
"""
import base64
import os
import io
import json
import re
import sys
import time
import urllib.request
import wave

import vo

TEXT_MODEL = os.environ.get("VO_TEXT_MODEL", "gemini-3.8-flash")


def norm(s):
    return re.sub(r"[^a-z0-9 ]", "", s.lower().replace("-", " ")).split()


def wav_bytes(pcm, rate):
    buf = io.BytesIO()
    with wave.open(buf, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(rate)
        w.writeframes(pcm.tobytes())
    return buf.getvalue()


def main():
    pcm, rate = vo.read_pcm(vo.FULL_TAKE)
    win = rate // 50
    pk = [max(abs(v) for v in pcm[i:i + win]) for i in range(0, len(pcm) - win, win)]
    loud = sorted(pk)[int(len(pk) * 0.95)]
    quiet = [p < loud * 0.04 for p in pk]
    # potongan bicara dipisah jeda >= 0,3 dtk
    segs, start, gap = [], None, 0
    for i, q in enumerate(quiet + [True] * 20):
        if not q:
            if start is None:
                start = i
            gap = 0
        elif start is not None:
            gap += 1
            if gap >= 15:
                segs.append((start, i - gap + 1))
                start, gap = None, 0
    parts = []
    for k, (a, b) in enumerate(segs):
        parts.append({"text": f"Segment {k}:"})
        parts.append({"inlineData": {"mimeType": "audio/wav", "data": base64.b64encode(wav_bytes(pcm[a * win:b * win], rate)).decode()}})
    parts.append({"text": "Transcribe each segment verbatim. Output exactly one line per segment: <number>: <transcript>"})
    body = json.dumps({"contents": [{"parts": parts}]}).encode()
    for attempt in range(int(os.environ.get("VO_TRIES", "8"))):
        try:
            req = urllib.request.Request(
                f"https://generativelanguage.googleapis.com/v1beta/models/{TEXT_MODEL}:generateContent",
                data=body, headers={"Content-Type": "application/json", "x-goog-api-key": vo.api_key()})
            text = json.load(urllib.request.urlopen(req, timeout=300))["candidates"][0]["content"]["parts"][0]["text"]
            break
        except Exception as e:  # layanan sering 503 sesaat
            print("  coba lagi:", e)
            time.sleep(75)
    else:
        sys.exit("Transkripsi gagal.")
    tr = {}
    for line in text.splitlines():
        m = re.match(r"\s*(?:Segment\s*)?(\d+)\s*:\s*(.*)", line)
        if m:
            tr[int(m.group(1))] = m.group(2)
    for k in range(len(segs)):
        print(f"  [{k:2d}] {segs[k][0] * 0.02:6.2f}s  {tr.get(k, '?')}")

    sc = vo.scenes()
    starts = []
    for s in sc:
        head = norm(s["vo"])[:3]
        best = None
        for k in range(len(segs)):
            if k in starts or (starts and k <= starts[-1]):
                continue
            if norm(tr.get(k, ""))[:3] == head:
                best = k
                break
        if best is None:
            sys.exit(f"Awal adegan {s['id']} tidak ditemukan: {' '.join(head)}")
        starts.append(best)
    pad = int(rate * 0.15)
    for i, s in enumerate(sc):
        a = segs[starts[i]][0] * win
        last = (starts[i + 1] - 1) if i + 1 < len(sc) else len(segs) - 1
        b = segs[last][1] * win
        seg = vo.trim_tail(pcm[max(0, a - pad):min(len(pcm), b + pad)], rate)
        vo.write_pcm(vo.VO_DIR / f"{vo.name(s)}.wav", seg, rate)
        print(f"  {vo.name(s)}: {len(seg) / rate:5.1f} dtk  (segmen {starts[i]}–{last})")
    vo.check()


if __name__ == "__main__":
    main()
