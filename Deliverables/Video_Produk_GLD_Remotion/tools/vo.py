"""Alat bantu narasi (Gemini TTS) untuk video GLD.

  python3 tools/vo.py export   -> tulis naskah per adegan ke tts/ (siap ditempel ke Gemini TTS)
  python3 tools/vo.py check    -> bandingkan durasi public/audio/vo/*.wav dengan durasi adegan

Naskah dan durasi dibaca langsung dari src/timeline.ts, jadi timeline tetap satu-satunya sumber.
Hanya memakai pustaka standar Python.
"""
import re
import sys
import wave
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TIMELINE = ROOT / "src" / "timeline.ts"
TTS_DIR = ROOT / "tts"
VO_DIR = ROOT / "public" / "audio" / "vo"

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


if __name__ == "__main__":
    {"export": export, "check": check}.get(sys.argv[1] if len(sys.argv) > 1 else "", lambda: sys.exit(__doc__))()
