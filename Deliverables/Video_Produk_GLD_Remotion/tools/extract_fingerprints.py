"""Ekstrak "sidik jari gas" 8-sensor dari dataset chamber GLD -> src/data/fingerprints.json.

Respons per sensor = persentil-95 tegangan dikurangi baseline (median 30 sampel pertama).
`shape`     = respons dinormalisasi ke sensor terkuat pada rekaman itu (bentuk pola).
`amplitude` = besar respons total skala log (udara bersih ~0, LPG = 1), supaya
              radar chart tidak membesar-besarkan respons yang sebenarnya kecil.

Jalankan dari folder proyek video:  python3 tools/extract_fingerprints.py
"""
import csv
import json
import math
import statistics
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATASET = HERE.parents[2] / "Dataset"
OUT = HERE.parent / "src" / "data" / "fingerprints.json"

SENSORS = ["MQ8", "MQ135", "MQ3", "MQ5", "MQ4", "MQ7", "MQ6", "MQ2"]

# Satu rekaman per kelas. LPG memakai dua rekaman lalu dirata-rata agar pola tidak
# bergantung pada satu sesi saja.
RECORDINGS = {
    "clean": ["gld_F001_20260715_035005 - [CLEAN AIR].csv"],
    "lpg": [
        "gld_F001_20260715_041830 - [LPG].csv",
        "gld_F001_20260715_142549_LPG.csv",
    ],
    "co2": ["gld_F001_20260715_075820_CARBON DIOXIDE.csv"],
}

# Rentang skala log amplitude (volt).
NOISE_FLOOR_V = 0.001
FULL_SCALE_V = 2.2


def responses(path):
    rows = list(csv.DictReader(open(path, newline="")))
    out = []
    for s in SENSORS:
        v = [float(r["voltage_" + s]) for r in rows]
        base = statistics.median(v[:30])
        p95 = sorted(v)[int(0.95 * len(v))]
        out.append(max(p95 - base, 0.0))
    return out


def main():
    result = {"sensors": SENSORS, "source": "Dataset chamber GLD, 13-15 Jul 2026", "gases": {}}
    for gas, files in RECORDINGS.items():
        per_file = [responses(DATASET / f) for f in files]
        raw = [statistics.mean(col) for col in zip(*per_file)]
        peak = max(raw)
        shape = [round(x / peak, 3) if peak > 0 else 0 for x in raw]
        amp = math.log10(max(peak, NOISE_FLOOR_V) / NOISE_FLOOR_V) / math.log10(FULL_SCALE_V / NOISE_FLOOR_V)
        result["gases"][gas] = {
            "files": files,
            "raw_delta_v": [round(x, 4) for x in raw],
            "shape": shape,
            "amplitude": round(min(max(amp, 0), 1), 3),
        }
    OUT.write_text(json.dumps(result, indent=2) + "\n")
    print(f"Ditulis: {OUT}")
    for gas, g in result["gases"].items():
        print(f"  {gas:6s} amp={g['amplitude']:.2f} shape={g['shape']}")


if __name__ == "__main__":
    main()
