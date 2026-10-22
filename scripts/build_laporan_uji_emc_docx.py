# -*- coding: utf-8 -*-
"""Laporan Uji Laboratorium 04 — Pra-Uji Emisi EMC (EN 55032 Class A) GLD & Cluster Head.

Sumber data: data mentah pre-scan Telkom Test House (Oktober 2026),
  Sumber Dokumen/data mentah test EMC di telkom Test House okt 20206/ (7 file .doc),
  diparse ke scripts/assets/rapat_22okt/emc_points.json (216 titik).
Gambar grafik dibuat ulang dari titik tersebut ke scripts/assets/uji_emc/.

Run:  python scripts/build_laporan_uji_emc_docx.py
PDF:  Word COM (Windows) atau python3 scripts/docx_to_pdf_with_toc.py <docx> (Linux)
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_spesifikasi_material_instalasi_docx import (  # noqa: E402
    make_doc, set_cell_shading, add_field, fix_widths, para, bullets, heading,
    table, NAVY, GRAY, WHITE, HEAD_SHADE,
)
from docx.shared import Pt, Inches, RGBColor  # noqa: E402
from docx.enum.text import WD_ALIGN_PARAGRAPH  # noqa: E402
from docx.oxml import OxmlElement  # noqa: E402
import matplotlib  # noqa: E402
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.ticker import FixedLocator, NullFormatter, NullLocator  # noqa: E402

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(REPO, "scripts", "assets", "rapat_22okt", "emc_points.json")
ASSET = os.path.join(REPO, "scripts", "assets", "uji_emc")
OUT = os.path.join(REPO, "Deliverables", "Laporan_Uji_Lab_04_Pra-Uji_Emisi_EMC_GLD_CH.docx")
DOC_NO = "LGU/GLD/UJI-LAB/2026-004"
REV = "1.0"
DATE = "22 Oktober 2026"

P = json.load(open(DATA, encoding="utf-8"))
LORA = (915e6, 925e6)


def is_lora(p):
    return LORA[0] <= p["f"] <= LORA[1]


def ffmt(f):
    if f >= 1e9:
        return f"{f / 1e9:.4f} GHz".replace(".", ",")
    if f >= 1e6:
        return f"{f / 1e6:.2f} MHz".replace(".", ",")
    return f"{f / 1e3:.1f} kHz".replace(".", ",")


def n(x, d=2):
    return f"{x:.{d}f}".replace(".", ",")


# (perangkat, uji, judul grafik, satuan, batas[(f0,f1,{detektor:nilai})], rentang)
MEAS = [
    ("GLD", "Radiasi 30 MHz–1 GHz", "dBµV/m", [(30e6, 230e6, {"Quasi-peak": 50}), (230e6, 1e9, {"Quasi-peak": 57})], (30e6, 1e9)),
    ("GLD", "Radiasi 1–6 GHz", "dBµV/m", [(1e9, 3e9, {"Peak": 76, "Average": 56}), (3e9, 6e9, {"Peak": 80, "Average": 60})], (1e9, 6e9)),
    ("GLD", "Konduksi AC — L1", "dBµV", [(1.5e5, 5e5, {"Quasi-peak": 79, "Average": 66}), (5e5, 30e6, {"Quasi-peak": 73, "Average": 60})], (1.5e5, 30e6)),
    ("GLD", "Konduksi AC — Netral", "dBµV", [(1.5e5, 5e5, {"Quasi-peak": 79, "Average": 66}), (5e5, 30e6, {"Quasi-peak": 73, "Average": 60})], (1.5e5, 30e6)),
    ("CH besar", "Radiasi 30 MHz–1 GHz", "dBµV/m", [(30e6, 230e6, {"Quasi-peak": 50}), (230e6, 1e9, {"Quasi-peak": 57})], (30e6, 1e9)),
    ("CH besar", "Radiasi 1–6 GHz", "dBµV/m", [(1e9, 3e9, {"Peak": 76, "Average": 56}), (3e9, 6e9, {"Peak": 80, "Average": 60})], (1e9, 6e9)),
    ("CH besar", "Konduksi DC", "dBµV", [(1.5e5, 5e5, {"Quasi-peak": 97, "Average": 84}), (5e5, 30e6, {"Quasi-peak": 87, "Average": 74})], (1.5e5, 30e6)),
]
SETUP = {
    "Radiasi 30 MHz–1 GHz": ("30 MHz – 1 GHz", "Quasi-peak", "120 kHz", "Jarak 3 m, OATS/SAC; antena Aaronia HyperLOG 20600 (30 MHz–6 GHz); polarisasi H & V, tinggi 1–4 m, putar 0–360°"),
    "Radiasi 1–6 GHz": ("1 – 6 GHz", "Peak & Average", "1 MHz", "Jarak 3 m, FSOATS; polarisasi H & V, tinggi 1–4 m, putar 0–360°"),
    "Konduksi AC — L1": ("150 kHz – 30 MHz", "Quasi-peak & Average", "9 kHz", "LISN AC (Compower), saluran Line"),
    "Konduksi AC — Netral": ("150 kHz – 30 MHz", "Quasi-peak & Average", "9 kHz", "LISN AC (Compower), saluran Neutral"),
    "Konduksi DC": ("150 kHz – 30 MHz", "Quasi-peak & Average", "9 kHz", "LISN DC / AAN, batas asimetrik"),
}
TICKS = [1.5e5, 3e5, 1e6, 3e6, 1e7, 3e7, 5e7, 1e8, 2e8, 3e8, 5e8, 1e9, 2e9, 3e9, 4e9, 6e9]
TLAB = {1.5e5: "150 kHz", 3e5: "300 kHz", 1e6: "1 MHz", 3e6: "3 MHz", 1e7: "10 MHz", 3e7: "30 MHz",
        5e7: "50 MHz", 1e8: "100 MHz", 2e8: "200 MHz", 3e8: "300 MHz", 5e8: "500 MHz", 1e9: "1 GHz",
        2e9: "2 GHz", 3e9: "3 GHz", 4e9: "4 GHz", 6e9: "6 GHz"}
COL = {"Quasi-peak": "#2B5FCB", "Peak": "#2B5FCB", "Average": "#C47A12"}


def chart(i, dev, test, unit, limits, span):
    pts = [p for p in P if p["dev"] == dev and p["test"] == test]
    fig, ax = plt.subplots(figsize=(7.2, 3.3), dpi=150)
    for f0, f1, lim in limits:
        for det, v in lim.items():
            ax.plot([f0, f1], [v, v], color="#B4520F" if det != "Average" else "#E0A040",
                    lw=1.6, ls="-" if det != "Average" else "--")
    for det in ["Quasi-peak", "Peak", "Average"]:
        d = [p for p in pts if p["det"] == det and not p["failed"]]
        if d:
            ax.scatter([p["f"] for p in d], [p["mag"] for p in d], s=18, color=COL[det],
                       marker="o" if det != "Average" else "s", label=f"Terukur — {det}", zorder=3)
    fl = [p for p in pts if p["failed"]]
    if fl:
        ax.scatter([p["f"] for p in fl], [p["mag"] for p in fl], s=60, marker="x", color="#B4520F",
                   linewidths=2, label="Frekuensi kerja LoRa", zorder=4)
        ax.axvspan(*LORA, color="#B4520F", alpha=0.08)
    ax.plot([], [], color="#B4520F", lw=1.6, label="Batas QP/Peak")
    if any("Average" in l for _, _, l in limits):
        ax.plot([], [], color="#E0A040", lw=1.6, ls="--", label="Batas Average")
    ax.set_xscale("log")
    ax.set_xlim(*span)
    ticks = [t for t in TICKS if span[0] <= t <= span[1]]
    ax.xaxis.set_major_locator(FixedLocator(ticks))
    ax.set_xticklabels([TLAB[t] for t in ticks])
    ax.xaxis.set_minor_locator(NullLocator())
    ax.xaxis.set_minor_formatter(NullFormatter())
    ax.set_ylabel(unit, fontsize=8)
    ax.set_xlabel("Frekuensi", fontsize=8)
    ax.tick_params(labelsize=7)
    ax.grid(True, which="both", color="#E3E6EC", lw=0.6)
    ax.set_title(f"{dev} — {test}", fontsize=9, loc="left", color="#1B2A4A")
    ax.legend(fontsize=6.5, loc="upper center", bbox_to_anchor=(0.5, -0.3), frameon=False, ncol=4)
    for s in ["top", "right"]:
        ax.spines[s].set_visible(False)
    fig.tight_layout()
    os.makedirs(ASSET, exist_ok=True)
    path = os.path.join(ASSET, f"emc_{i + 1:02d}.png")
    fig.savefig(path)
    plt.close(fig)
    return path


def figure(doc, path, caption):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.keep_with_next = True
    p.add_run().add_picture(path, width=Inches(6.6))
    c = doc.add_paragraph()
    c.alignment = WD_ALIGN_PARAGRAPH.CENTER
    c.paragraph_format.space_after = Pt(4)
    c.paragraph_format.keep_with_next = True
    r = c.add_run(caption)
    r.font.size = Pt(8.8); r.font.italic = True; r.font.color.rgb = GRAY


def front(doc, sec):
    lt = doc.add_table(rows=1, cols=1)
    lc = lt.rows[0].cells[0]
    fix_widths(lt, [6.9])
    set_cell_shading(lc, "1B2A4A")
    lr = lc.paragraphs[0].add_run("PT LAPI GANESHA UTAMA")
    lr.font.bold = True; lr.font.size = Pt(14); lr.font.color.rgb = WHITE
    lr2 = lc.add_paragraph().add_run("Bekerja sama dengan Lab IoT & Fisika Institut Teknologi Bandung")
    lr2.font.size = Pt(9.5); lr2.font.color.rgb = RGBColor(0xC7, 0xD2, 0xE0)
    doc.add_paragraph().paragraph_format.space_after = Pt(6)
    t = doc.add_heading(level=0)
    tr = t.add_run("Laporan Uji Laboratorium 04 — Pra-Uji Emisi EMC Node Sensor GLD dan Cluster Head")
    tr.font.size = Pt(18); tr.font.bold = True; tr.font.color.rgb = NAVY
    para(doc, "Pengukuran emisi terradiasi dan terkonduksi menurut EN 55032 Class A sebagai pra-uji "
              "(pre-scan) sebelum pengujian EMC resmi di laboratorium terakreditasi.", size=10.6, color=GRAY, after=10)
    rows = [
        ("Nomor dokumen", DOC_NO), ("Revisi", REV), ("Tanggal", DATE),
        ("Jenis pengujian", "Pra-uji (pre-scan) emisi elektromagnetik — bukan uji sertifikasi"),
        ("Standar acuan", "EN 55032, Class A (emisi terradiasi 30 MHz–6 GHz, emisi terkonduksi 150 kHz–30 MHz)"),
        ("Perangkat diuji", "Node Sensor GLD V2 (Gas Leak Detector); Cluster Head (varian besar)"),
        ("Lokasi pengukuran", "Telkom Test House"),
        ("Periode pengukuran", "Oktober 2026"),
        ("Disiapkan oleh", "PT LAPI Ganesha Utama, bersama Lab IoT & Fisika Institut Teknologi Bandung"),
        ("Ditujukan kepada", "PT Pertamina Patra Niaga"),
        ("Dokumen terkait", "Laporan Uji Lab 02 — Komunikasi Radio LoRa (LGU/GLD/UJI-LAB/2026-002); "
                            "Laporan FAT Sistem GLD Tahap 2 (LGU/GLD/FAT/2026-001)"),
    ]
    p_ = doc.add_paragraph()
    r = p_.add_run("Document Control")
    r.font.bold = True; r.font.size = Pt(11); r.font.color.rgb = NAVY
    mt = doc.add_table(rows=0, cols=2)
    mt.style = "Table Grid"
    for k, v in rows:
        row = mt.add_row().cells
        set_cell_shading(row[0], HEAD_SHADE)
        r0 = row[0].paragraphs[0].add_run(k)
        r0.font.bold = True; r0.font.size = Pt(9.3); r0.font.color.rgb = GRAY
        r1 = row[1].paragraphs[0].add_run(v)
        r1.font.size = Pt(9.6)
    fix_widths(mt, [1.9, 5.0])
    hp = sec.header.paragraphs[0]
    hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    hr = hp.add_run("Laporan Uji Lab 04 — Pra-Uji Emisi EMC  |  Untuk Pengesahan")
    hr.font.size = Pt(8); hr.font.color.rgb = GRAY; hr.font.italic = True
    fp = sec.footer.paragraphs[0]
    fp.add_run(f"{DOC_NO}  ·  Rev. {REV}")
    fp.paragraph_format.tab_stops.add_tab_stop(Inches(6.9), alignment=2)
    fp.add_run("\t")
    add_field(fp, "PAGE", "1")
    fp.add_run(" dari ")
    add_field(fp, "NUMPAGES", "1")
    for r in fp.runs:
        r.font.size = Pt(8); r.font.color.rgb = GRAY
    doc.add_page_break()


def keep_together(t):
    for row in t.rows:
        row._tr.get_or_add_trPr().append(OxmlElement("w:cantSplit"))
        for c in row.cells:
            for pp in c.paragraphs:
                pp.paragraph_format.keep_with_next = True


def minpt(dev, test, exclude_lora=True):
    d = [p for p in P if p["dev"] == dev and p["test"] == test and not (exclude_lora and is_lora(p))]
    return min(d, key=lambda p: p["margin"]), len(d)


def build():
    doc, sec = make_doc()
    front(doc, sec)

    # 1 ringkasan
    heading(doc, "1. Ringkasan hasil")
    para(doc, "Tujuh pengukuran emisi dilakukan pada dua perangkat: empat pada Node Sensor GLD dan tiga pada "
              "Cluster Head varian besar, dengan total **216 titik ukur** yang dicatat perangkat lunak penerima. "
              "Seluruh titik berada di bawah batas EN 55032 Class A, **kecuali titik pada frekuensi kerja radio "
              "LoRa (919,6–921,0 MHz)**, yaitu sinyal pancar perangkat itu sendiri (lihat bagian 5.1).")
    rows = []
    for dev, test, *_ in MEAS:
        m, cnt = minpt(dev, test)
        lora = [p for p in P if p["dev"] == dev and p["test"] == test and p["failed"]]
        status = ("Di bawah batas, kecuali frekuensi kerja LoRa" if lora else "Di bawah batas")
        rows.append([dev, test, str(cnt + len(lora)), f"{n(m['margin'])} dB @ {ffmt(m['f'])}", status])
    table(doc, ["Perangkat", "Pengukuran", "Titik", "Margin terkecil*", "Hasil pra-uji"], rows,
          [0.9, 1.6, 0.55, 1.75, 2.1], size=8.8)
    para(doc, "* Margin = batas − level terukur; dihitung di luar pita frekuensi kerja LoRa. Margin positif "
              "berarti emisi di bawah batas.", size=8.6, color=GRAY, italic=True)
    para(doc, "**Catatan utama:**", after=2)
    bullets(doc, [
        "Margin paling kecil ada pada GLD di **117–127 MHz (0,51–0,95 dB)**. Titik ini masih di bawah batas, "
        "tetapi terlalu dekat untuk diandalkan pada uji resmi; perlu diredam lebih dulu (bagian 6).",
        "Titik yang ditandai “Failed” oleh perangkat lunak seluruhnya berada pada frekuensi kerja LoRa. "
        "Status penilaiannya perlu dikonfirmasi ke laboratorium (bagian 5.1).",
        "Pengujian ini adalah **pra-uji**: hasilnya dipakai untuk mengarahkan perbaikan desain, bukan sebagai "
        "pernyataan kepatuhan. Uji imunitas, Gateway, dan Cluster Head varian kecil belum termasuk.",
    ])

    # 2 tujuan & lingkup
    heading(doc, "2. Tujuan dan ruang lingkup")
    bullets(doc, [
        "Mengetahui posisi emisi GLD dan Cluster Head terhadap batas EN 55032 Class A sebelum uji EMC resmi "
        "di laboratorium terakreditasi, sebagai bagian dari jalur sertifikasi (track EMC).",
        "Mengidentifikasi frekuensi dengan margin tipis yang perlu ditangani pada desain.",
        "**Termasuk:** emisi terradiasi 30 MHz–6 GHz (GLD, Cluster Head besar); emisi terkonduksi saluran AC "
        "GLD; emisi terkonduksi saluran DC Cluster Head besar.",
        "**Belum termasuk:** uji imunitas (EN 61000-6-2), Gateway, Cluster Head varian kecil, dan uji radio "
        "untuk pemancar LoRa (ETSI EN 300 220 / regulasi SDPPI).",
    ])

    # 3 perangkat & metode
    heading(doc, "3. Perangkat diuji dan metode")
    heading(doc, "3.1 Perangkat diuji", level=2)
    table(doc, ["Perangkat", "Keterangan", "Catu daya saat uji"], [
        ["Node Sensor GLD V2", "8 sensor gas, mikrokontroler ESP32-S3, radio LoRa 920–923 MHz",
         "Melalui adaptor/PSU dari jala-jala AC (emisi terkonduksi diukur di sisi AC)"],
        ["Cluster Head (varian besar)", "Simpul penghubung jaringan mesh LoRa",
         "Catu DC (emisi terkonduksi diukur di sisi DC)"],
    ], [1.7, 2.6, 2.6], size=8.8)
    para(doc, "Nomor seri unit, versi firmware, dan mode operasi saat uji tidak tercatat pada lembar data "
              "mentah; ketiganya akan dilengkapi pada laporan resmi laboratorium.", size=9.4, color=GRAY, italic=True)
    heading(doc, "3.2 Konfigurasi pengukuran", level=2)
    table(doc, ["Pengukuran", "Rentang", "Detektor", "RBW", "Konfigurasi"],
          [[k, *v] for k, v in SETUP.items()], [1.45, 1.1, 1.05, 0.55, 2.75], size=8.6)
    para(doc, "Waktu tinggal (dwell) 200 ms per titik, atenuasi otomatis. Faktor koreksi kabel (kabel biru dan "
              "Heliax) dan antena/LISN sudah dimasukkan ke nilai level oleh perangkat lunak penerima.", size=9.4)
    heading(doc, "3.3 Batas EN 55032 Class A yang dipakai", level=2)
    table(doc, ["Jenis emisi", "Rentang frekuensi", "Batas QP / Peak", "Batas Average"], [
        ["Terradiasi, 3 m", "30–230 MHz", "50 dBµV/m (QP)", "—"],
        ["Terradiasi, 3 m", "230 MHz–1 GHz", "57 dBµV/m (QP)", "—"],
        ["Terradiasi, 3 m", "1–3 GHz", "76 dBµV/m (Peak)", "56 dBµV/m"],
        ["Terradiasi, 3 m", "3–6 GHz", "80 dBµV/m (Peak)", "60 dBµV/m"],
        ["Terkonduksi AC", "0,15–0,5 MHz", "79 dBµV (QP)", "66 dBµV"],
        ["Terkonduksi AC", "0,5–30 MHz", "73 dBµV (QP)", "60 dBµV"],
        ["Terkonduksi DC (asimetrik)", "0,15–0,5 MHz", "97 dBµV (QP)", "84 dBµV"],
        ["Terkonduksi DC (asimetrik)", "0,5–30 MHz", "87 dBµV (QP)", "74 dBµV"],
    ], [1.9, 1.5, 1.75, 1.75], size=8.8)

    # 4 hasil
    heading(doc, "4. Hasil pengukuran")
    para(doc, "Setiap grafik memuat titik yang dicatat perangkat lunak penerima beserta garis batas. "
              "Tabel di bawah grafik memuat lima titik dengan margin terkecil di luar pita LoRa.")
    fig_no = 0
    for i, (dev, test, unit, limits, span) in enumerate(MEAS):
        if i in (0, 4):
            heading(doc, f"4.{1 if dev == 'GLD' else 2} {'Node Sensor GLD' if dev == 'GLD' else 'Cluster Head (varian besar)'}", level=2)
        fig_no += 1
        figure(doc, chart(i, dev, test, unit, limits, span), f"Gambar {fig_no}. {dev} — {test}")
        pts = sorted([p for p in P if p["dev"] == dev and p["test"] == test and not is_lora(p)],
                     key=lambda p: p["margin"])[:5]
        rows = [[ffmt(p["f"]), p["det"], n(p["mag"]), n(p["lim"], 0), n(p["margin"]),
                 f"{p['pol']} · {p['h']} cm · {p['ang']}°" if p["pol"] else "—"] for p in pts]
        fl = [p for p in P if p["dev"] == dev and p["test"] == test and p["failed"]]
        rows += [[ffmt(p["f"]), p["det"], n(p["mag"]), n(p["lim"], 0), n(p["margin"]) + " (LoRa)",
                  f"{p['pol']} · {p['h']} cm · {p['ang']}°"] for p in fl]
        t = table(doc, ["Frekuensi", "Detektor", f"Level ({unit})", "Batas", "Margin (dB)", "Polarisasi · tinggi · sudut"],
              rows, [1.1, 0.95, 1.05, 0.65, 1.15, 2.0], size=8.4)
        keep_together(t)

    # 5 pembahasan
    heading(doc, "5. Pembahasan")
    heading(doc, "5.1 Titik pada frekuensi kerja LoRa", level=2)
    para(doc, "Perangkat lunak menandai empat titik sebagai “Failed”: GLD pada 919,65 MHz, 920,05 MHz, dan "
              "920,39 MHz (level hingga 93,29 dBµV/m), serta Cluster Head pada 920,97 MHz (112,47 dBµV/m). "
              "Keempatnya berada pada pita kerja radio LoRa perangkat (920–923 MHz), sehingga yang terukur adalah "
              "sinyal pancar yang memang disengaja, bukan emisi liar dari rangkaian.")
    para(doc, "Pada standar emisi multimedia, pita frekuensi kerja pemancar umumnya dikeluarkan dari penilaian "
              "dan dinilai melalui standar radio tersendiri (misalnya ETSI EN 300 220 serta sertifikasi SDPPI di "
              "Indonesia). Status ini **perlu dikonfirmasi tertulis oleh Telkom Test House**. Bila diperlukan, "
              "pengukuran ulang dapat dilakukan dengan pemancar LoRa dalam keadaan idle.")
    heading(doc, "5.2 Margin tipis GLD pada 117–127 MHz", level=2)
    para(doc, "Tiga titik GLD pada 117,40 MHz, 117,89 MHz, dan 126,82 MHz (QP, polarisasi horizontal, tinggi "
              "antena 3 m) hanya 0,51–0,95 dB di bawah batas 50 dBµV/m. Variasi antar-unit dan antar-laboratorium "
              "biasanya lebih besar dari angka ini, sehingga titik ini berisiko melampaui batas pada uji resmi. "
              "Kandidat sumber yang akan diperiksa: harmonik clock mikrokontroler dan konverter DC-DC, serta kabel "
              "catu yang berperan sebagai antena.")
    heading(doc, "5.3 Cluster Head", level=2)
    para(doc, "Margin terkecil Cluster Head di luar pita LoRa adalah 3,28 dB pada 978,88 MHz (QP) dan 5,56 dB "
              "pada 1,8425 GHz (Average). Frekuensi 1,8425 GHz berdekatan dengan harmonik kedua frekuensi kerja "
              "LoRa (2 × ±921 MHz), sehingga penanganannya terkait filter keluaran radio. Emisi terkonduksi DC "
              "Cluster Head jauh di bawah batas (margin terkecil 42,41 dB).")
    heading(doc, "5.4 Emisi terkonduksi GLD", level=2)
    para(doc, "Emisi terkonduksi GLD diukur di sisi AC, artinya mencakup adaptor/PSU yang dipakai saat uji. "
              "Margin terkecil 6,03 dB (QP, 323,9 kHz, saluran Line). Pada instalasi lapangan GLD menerima "
              "24 VDC dari PSU di junction box, sehingga hasil ini mencerminkan kombinasi GLD dan adaptor uji.")

    # 6 tindak lanjut
    heading(doc, "6. Tindak lanjut")
    table(doc, ["No", "Tindak lanjut", "Penanggung jawab"], [
        ["1", "Konfirmasi tertulis ke Telkom Test House mengenai perlakuan pita frekuensi kerja LoRa; "
              "ukur ulang dengan pemancar idle bila diminta.", "LGU"],
        ["2", "Investigasi dan peredaman emisi GLD 117–127 MHz (filter catu, ferit kabel, tata letak clock/DC-DC); "
              "ukur ulang untuk memastikan margin memadai.", "LGU / Lab IoT ITB"],
        ["3", "Periksa filter keluaran radio Cluster Head terkait titik 1,8425 GHz dan 978,88 MHz.", "LGU / Lab IoT ITB"],
        ["4", "Lengkapi cakupan: uji imunitas, Gateway, Cluster Head varian kecil; catat nomor seri, firmware, "
              "dan mode operasi unit uji.", "LGU"],
        ["5", "Laksanakan uji EMC resmi di laboratorium terakreditasi setelah butir 1–3 selesai.", "LGU"],
    ], [0.4, 5.0, 1.5], size=8.8)

    # 7 lampiran & pengesahan
    heading(doc, "7. Data sumber")
    para(doc, "Data mentah hasil ekspor perangkat lunak penerima Telkom Test House (tujuh berkas): GLD — "
              "Class A Below 1G, Class A Above 1G, Class A L1, Class A L2; Cluster Head besar — Class A Below 1G, "
              "Class A Above 1G, Class A DC. Grafik dan tabel pada laporan ini disusun ulang dari titik-titik di "
              "berkas tersebut tanpa perubahan nilai. Laporan resmi laboratorium belum diterbitkan.", size=9.6)

    heading(doc, "8. Lembar pengesahan")
    sg = doc.add_table(rows=2, cols=3)
    sg.style = "Table Grid"
    for c, h in enumerate(["Disusun oleh\nLab IoT & Fisika ITB", "Diperiksa oleh\nPT LAPI Ganesha Utama",
                           "Mengetahui\nPT Pertamina Patra Niaga"]):
        cell = sg.rows[0].cells[c]
        set_cell_shading(cell, HEAD_SHADE)
        rr = cell.paragraphs[0].add_run(h)
        rr.font.bold = True; rr.font.size = Pt(9)
        cell.paragraphs[0].paragraph_format.keep_with_next = True
        cell2 = sg.rows[1].cells[c]
        cell2.paragraphs[0].add_run("\n\n\n\n")
        r2 = cell2.add_paragraph().add_run("Nama:\nJabatan:\nTanggal:")
        r2.font.size = Pt(8.8); r2.font.color.rgb = GRAY
    fix_widths(sg, [2.3, 2.3, 2.3])
    for row in sg.rows:
        row._tr.get_or_add_trPr().append(OxmlElement("w:cantSplit"))

    doc.save(OUT)
    print(OUT)


if __name__ == "__main__":
    build()
