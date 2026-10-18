"""Alat bantu narasi (Gemini TTS) untuk video GLD.

  python3 tools/vo.py export   -> tulis naskah per adegan ke tts/ (siap ditempel ke Gemini TTS)
  python3 tools/vo.py check    -> bandingkan durasi public/audio/vo/*.wav dengan durasi adegan
  python3 tools/vo.py generate -> SATU panggilan Gemini TTS untuk semua adegan, lalu dipotong per adegan
  python3 tools/vo.py split    -> potong ulang rekaman utuh (_full.wav) tanpa memanggil API

Naskah dan durasi dibaca langsung dari src/timeline.ts, jadi timeline tetap satu-satunya sumber.
Hanya memakai pustaka standar Python. Key: env var GEMINI_API_KEY atau file env di root repo.
"""
import array
import base64
import json
import os
import re
import sys
import urllib.error
import urllib.request
import wave
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TIMELINE = ROOT / "src" / "timeline.ts"
TTS_DIR = ROOT / "tts"
VO_DIR = ROOT / "public" / "audio" / "vo"
FULL_TAKE = VO_DIR / "_full.wav"

VOICE = "Erinome"
MODEL = "gemini-2.5-flash-preview-tts"
GAP_SEC = 2

# Instruksi gaya untuk Gemini TTS (ditempel sebelum naskah tiap adegan).
STYLE = (
    "Bacakan dalam Bahasa Indonesia baku dengan nada formal, tenang, dan meyakinkan, "
    "seperti narator video teknologi industri. Tempo sedang, jeda singkat di setiap koma."
)


def scenes():
    src = TIMELINE.read_text(encoding="utf-8")
    pattern = re.compile(
        r"id: '(\w+)',\s+title: '([^']*)',\s+startSec: (\d+),\s+endSec: (\d+),\s+vo: '([^']*)'"
    )
    out = []
    for i, m in enumerate(pattern.finditer(src)):
        sid, title, start, end, vo = m.groups()
        out.append({"n": i + 1, "id": sid, "title": title, "dur": int(end) - int(start), "vo": vo})
    if not out:
        sys.exit("Tidak menemukan adegan di src/timeline.ts")
    return out


def name(s):
    # Harus sama dengan voPath() di src/assets.ts.
    return f"{s['n']:02d}_{s['id']}"


def export():
    TTS_DIR.mkdir(exist_ok=True)
    lines = [f"# Naskah narasi GLD (Gemini TTS)\n\nInstruksi gaya: {STYLE}\n"]
    for s in scenes():
        (TTS_DIR / f"{name(s)}.txt").write_text(f"{STYLE}\n\n{s['vo']}\n", encoding="utf-8")
        words = len(s["vo"].split())
        lines.append(
            f"## {name(s)} — {s['title']} ({s['dur']} dtk, {words} kata)\n\n"
            f"Simpan hasil sebagai `public/audio/vo/{name(s)}.wav`\n\n{s['vo']}\n"
        )
    (TTS_DIR / "NASKAH_LENGKAP.md").write_text("\n".join(lines), encoding="utf-8")
    (TTS_DIR / "SEKALIGUS.txt").write_text(full_prompt() + "\n", encoding="utf-8")
    print(f"Naskah ditulis ke {TTS_DIR}")


def check():
    ok = True
    for s in scenes():
        wav = VO_DIR / f"{name(s)}.wav"
        if not wav.exists():
            print(f"  BELUM ADA  {wav.relative_to(ROOT)}")
            ok = False
            continue
        with wave.open(str(wav)) as w:
            dur = w.getnframes() / w.getframerate()
        # Sisakan ~0,5 dtk agar narasi tidak terpotong oleh fade akhir adegan.
        status = "OK" if dur <= s["dur"] - 0.5 else "TERLALU PANJANG"
        if status != "OK":
            ok = False
        print(f"  {status:16s} {name(s)}: audio {dur:5.1f} dtk / slot {s['dur']} dtk")
    if ok:
        print("Semua narasi muat. Set VO_READY = true di src/assets.ts.")
    else:
        print("Perbaiki yang belum OK: rekam ulang lebih cepat, atau ubah startSec/endSec di src/timeline.ts.")


def api_key():
    if os.environ.get("GEMINI_API_KEY"):
        return os.environ["GEMINI_API_KEY"]
    env = ROOT.parent.parent / "env"  # file env di root repo (diabaikan git)
    for line in env.read_text(encoding="utf-8").splitlines():
        if line.startswith("GEMINI_API_KEY="):
            return line.split("=", 1)[1].strip()
    sys.exit("GEMINI_API_KEY tidak ditemukan (env var atau file env di root repo).")


def read_pcm(path):
    with wave.open(str(path)) as w:
        rate = w.getframerate()
        pcm = array.array("h", w.readframes(w.getnframes()))
    return pcm, rate


def write_pcm(path, pcm, rate):
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(rate)
        w.writeframes(pcm.tobytes())


def full_prompt():
    # Satu teks untuk semua adegan; dipakai generate() dan tts/SEKALIGUS.txt (AI Studio manual).
    sc = scenes()
    return (
        f"{STYLE} Teks terdiri atas {len(sc)} paragraf. "
        f"Setelah setiap paragraf, diam selama {GAP_SEC} detik sebelum paragraf berikutnya.\n\n"
        + "\n\n".join(s["vo"] for s in sc)
    )


def generate():
    # Satu panggilan API untuk kedelapan adegan, lalu dipotong per adegan (split).
    body = {
        "contents": [{"parts": [{"text": full_prompt()}]}],
        "generationConfig": {
            "responseModalities": ["AUDIO"],
            "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": VOICE}}},
        },
    }
    req = urllib.request.Request(
        f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent",
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json", "x-goog-api-key": api_key()},
    )
    try:
        resp = json.load(urllib.request.urlopen(req, timeout=600))
    except urllib.error.HTTPError as e:
        sys.exit(f"HTTP {e.code}: {e.read().decode()[:600]}")
    data = resp["candidates"][0]["content"]["parts"][0]["inlineData"]["data"]
    VO_DIR.mkdir(parents=True, exist_ok=True)
    pcm = array.array("h", base64.b64decode(data))
    write_pcm(FULL_TAKE, pcm, 24000)
    print(f"Rekaman utuh: {FULL_TAKE.relative_to(ROOT)} ({len(pcm) / 24000:.1f} dtk, suara {VOICE})")
    split()


def split():
    # Potong rekaman utuh di (jumlah adegan - 1) jeda terpanjang.
    pcm, rate = read_pcm(FULL_TAKE)
    win = rate // 50  # 20 ms
    rms = [
        (sum(x * x for x in pcm[i:i + win]) / win) ** 0.5
        for i in range(0, len(pcm) - win, win)
    ]
    loud = sorted(rms)[int(len(rms) * 0.95)]
    silent = [r < loud * 0.04 for r in rms]

    gaps, start = [], None
    for i, s in enumerate(silent + [False]):
        if s and start is None:
            start = i
        elif not s and start is not None:
            if start > 0 and i < len(silent):  # abaikan hening di awal/akhir
                gaps.append((i - start, start, i))
            start = None
    sc = scenes()
    if len(gaps) < len(sc) - 1:
        sys.exit(f"Hanya {len(gaps)} jeda ditemukan, butuh {len(sc) - 1}. Generate ulang.")
    longest = sorted(gaps, reverse=True)[: len(sc) - 1]
    if longest[-1][0] * 0.02 >= 1.0:
        # Jeda antar-paragraf terdengar jelas: potong di jeda terpanjang.
        cuts = sorted((a + b) // 2 * win for _, a, b in longest)
    else:
        # Jeda antar-paragraf tidak lebih panjang dari jeda kalimat: cari jeda (>= 0,3 dtk)
        # terdekat dengan perkiraan batas adegan dari proporsi huruf terhadap waktu bicara.
        print("  Jeda antar-paragraf tidak jelas; memotong berdasarkan proporsi teks.")
        speech_at = [0]
        for s in silent:
            speech_at.append(speech_at[-1] + (not s))
        total_chars = sum(len(s["vo"]) for s in sc)
        cand = [(a + b) // 2 for n, a, b in gaps if n >= 15]
        cuts, acc, prev = [], 0, 0
        for s in sc[:-1]:
            acc += len(s["vo"])
            target = acc / total_chars * speech_at[-1]
            t = next(i for i, v in enumerate(speech_at) if v >= target)
            m = min((c for c in cand if c > prev), key=lambda c: abs(c - t))
            cuts.append(m * win)
            prev = m
    bounds = [0] + cuts + [len(pcm)]

    pad = int(rate * 0.15)
    total_chars = sum(len(s["vo"]) for s in sc)
    total_sec = len(pcm) / rate
    for s, a, b in zip(sc, bounds, bounds[1:]):
        seg_silent = silent[a // win: b // win]
        first = next((i for i, x in enumerate(seg_silent) if not x), 0)
        last = len(seg_silent) - next((i for i, x in enumerate(reversed(seg_silent)) if not x), 0)
        lo, hi = max(a, a + first * win - pad), min(b, a + last * win + pad)
        seg = pcm[lo:hi]
        write_pcm(VO_DIR / f"{name(s)}.wav", seg, rate)
        dur = len(seg) / rate
        expect = len(s["vo"]) / total_chars * total_sec
        note = "" if 0.6 < dur / expect < 1.4 else "  <- durasi tak wajar, cek potongan"
        print(f"  {name(s)}: {dur:5.1f} dtk{note}")
    check()


if __name__ == "__main__":
    {"export": export, "check": check, "generate": generate, "split": split}.get(sys.argv[1] if len(sys.argv) > 1 else "", lambda: sys.exit(__doc__))()
