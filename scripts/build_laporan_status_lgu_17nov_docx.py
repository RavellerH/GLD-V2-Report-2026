# -*- coding: utf-8 -*-
"""Laporan Status Proyek GLD Tahap 2 untuk internal LGU (anggaran operasional).

Output: Deliverables/Laporan_Status_Proyek_GLD_LGU_17November2026.docx
Versi lanjutan dari build_laporan_status_lgu_docx.py (30 Sep); generator lama dibiarkan utuh.
(PDF dirender via scripts/docx_to_pdf_with_toc.py.)
"""
import os
import datetime as dt

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

from build_persiapan_instalasi_corporate_docx import (
    make_doc, set_cell_shading, set_cell_border, add_field, add_picture_fit,
    set_cell_margins, set_table_borders,
    NAVY, GRAY, INK, WHITE, GREEN, AMBER, RED, HEAD_SHADE, ZEBRA_SHADE,
    OK_BG, OK_BD, WARN_BG, WARN_BD, DANGER_BG, DANGER_BD,
)

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(REPO, "Deliverables", "Laporan_Status_Proyek_GLD_LGU_17November2026.docx")
CHART = os.path.join(REPO, "scripts", "assets", "kurva_s_proyek_17nov2026.png")

DOC_NO = "LGU/GLD/LAP-STATUS/2026-002"
REVISION = "1.0"
DOC_DATE = "17 November 2026"
TODAY = dt.date(2026, 11, 17)

# Status word -> color, used for the status column of any table.
STATUS_MAP = [
    (("SELESAI", "TERSEDIA", "FINAL", "LAYAK", "TERKIRIM", "POSITIF"), GREEN),
    (("SEBAGIAN", "PROSES", "MENUNGGU", "REKOMENDASI", "AWAL", "BERJALAN", "PENYIAPAN", "DIJADWALKAN"), AMBER),
    (("BELUM", "TERTINGGAL", "GAGAL", "RISIKO"), RED),
]


def status_color(text):
    up = text.upper()
    for keys, color in STATUS_MAP:
        if any(k in up for k in keys):
            return color
    return None


doc, sec = make_doc()


def p(text="", size=10.2, bold=False, italic=False, color=None, space_after=7, align=None):
    para = doc.add_paragraph()
    para.paragraph_format.space_after = Pt(space_after)
    if align is not None:
        para.alignment = align
    if text:
        r = para.add_run(text)
        r.font.size = Pt(size)
        r.font.bold = bold
        r.font.italic = italic
        if color is not None:
            r.font.color.rgb = color
    return para


def lead(label, text, size=10.2):
    para = doc.add_paragraph()
    para.paragraph_format.space_after = Pt(7)
    r1 = para.add_run(label)
    r1.font.bold = True
    r1.font.size = Pt(size)
    r2 = para.add_run(text)
    r2.font.size = Pt(size)
    return para


def bullet(text, size=10):
    bp = doc.add_paragraph(style="List Bullet")
    bp.paragraph_format.space_after = Pt(3)
    r = bp.add_run(text)
    r.font.size = Pt(size)


def box(text, kind="warn", label=None):
    bg, bd = {"warn": (WARN_BG, WARN_BD), "ok": (OK_BG, OK_BD), "danger": (DANGER_BG, DANGER_BD)}[kind]
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.rows[0].cells[0]
    set_cell_shading(cell, bg)
    set_cell_border(cell, bd, sz=6)
    set_cell_margins(cell, top=110, bottom=110, start=130, end=130)
    para = cell.paragraphs[0]
    para.paragraph_format.space_after = Pt(0)
    if label:
        r = para.add_run(label + " ")
        r.font.bold = True
        r.font.size = Pt(9.6)
    r = para.add_run(text)
    r.font.size = Pt(9.6)
    doc.add_paragraph().paragraph_format.space_after = Pt(4)


def finish_table(tbl, keep_together=True):
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    # Lebar kolom tetap: LibreOffice mengabaikan lebar sel tanpa tblLayout fixed + tblGrid.
    tblPr = tbl._tbl.tblPr
    lay = OxmlElement("w:tblLayout"); lay.set(qn("w:type"), "fixed"); tblPr.append(lay)
    widths = [c.width for c in tbl.rows[0].cells]
    grid = tbl._tbl.tblGrid
    for gc, w in zip(grid.findall(qn("w:gridCol")), widths):
        if w:
            gc.set(qn("w:w"), str(int(w / 635)))
    trPr = tbl.rows[0]._tr.get_or_add_trPr()
    h = OxmlElement("w:tblHeader"); h.set(qn("w:val"), "true"); trPr.append(h)
    for row in tbl.rows:
        rp = row._tr.get_or_add_trPr()
        cs = OxmlElement("w:cantSplit"); cs.set(qn("w:val"), "true"); rp.append(cs)
    if keep_together:
        for row in tbl.rows[:-1]:
            for c in row.cells:
                for para in c.paragraphs:
                    para.paragraph_format.keep_with_next = True


def table(headers, rows, widths, status_col=None, font=9.0, bold_first=False):
    tbl = doc.add_table(rows=1, cols=len(headers))
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    for i, h in enumerate(headers):
        c = tbl.rows[0].cells[i]
        set_cell_shading(c, "1B2A4A")
        c.paragraphs[0].paragraph_format.space_after = Pt(1)
        r = c.paragraphs[0].add_run(h)
        r.font.bold = True
        r.font.size = Pt(8.6)
        r.font.color.rgb = WHITE
    for ri, row in enumerate(rows):
        cells = tbl.add_row().cells
        for ci, val in enumerate(row):
            c = cells[ci]
            if ri % 2 == 1:
                set_cell_shading(c, ZEBRA_SHADE)
            c.paragraphs[0].paragraph_format.space_after = Pt(1)
            r = c.paragraphs[0].add_run(str(val))
            r.font.size = Pt(font)
            if bold_first and ci == 0:
                r.font.bold = True
            if status_col is not None and ci == status_col:
                col = status_color(str(val))
                r.font.bold = True
                if col is not None:
                    r.font.color.rgb = col
    for row in tbl.rows:
        for i, w in enumerate(widths):
            row.cells[i].width = Inches(w)
    set_table_borders(tbl)
    finish_table(tbl, keep_together=len(rows) <= 9)
    doc.add_paragraph().paragraph_format.space_after = Pt(4)
    return tbl


def kpi_row(items):
    tbl = doc.add_table(rows=1, cols=len(items))
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, (lab, val, sub, color) in enumerate(items):
        c = tbl.rows[0].cells[i]
        set_cell_shading(c, "F5F5F3")
        set_cell_margins(c, top=120, bottom=120, start=90, end=90)
        para = c.paragraphs[0]
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        para.paragraph_format.space_after = Pt(0)
        r = para.add_run(lab + "\n")
        r.font.size = Pt(7.8)
        r.font.bold = True
        r.font.color.rgb = GRAY
        r = para.add_run(val + "\n")
        r.font.size = Pt(18)
        r.font.bold = True
        r.font.color.rgb = color
        r = para.add_run(sub)
        r.font.size = Pt(7.8)
        r.font.color.rgb = GRAY
    set_table_borders(tbl)
    doc.add_paragraph().paragraph_format.space_after = Pt(4)


# ---------------------------------------------------------------- S-curve chart
def build_chart():
    plan = [(dt.date(2026, 6, 1), 0), (dt.date(2026, 6, 30), 8), (dt.date(2026, 7, 30), 21),
            (dt.date(2026, 8, 31), 40), (dt.date(2026, 9, 30), 62), (dt.date(2026, 10, 31), 71),
            (dt.date(2026, 11, 30), 84), (dt.date(2026, 12, 31), 93), (dt.date(2027, 1, 31), 98),
            (dt.date(2027, 2, 28), 100)]
    act = [(dt.date(2026, 6, 1), 0), (dt.date(2026, 6, 12), 6), (dt.date(2026, 6, 30), 16),
           (dt.date(2026, 7, 7), 23), (dt.date(2026, 7, 15), 30), (dt.date(2026, 7, 24), 39),
           (dt.date(2026, 9, 4), 44), (dt.date(2026, 9, 17), 49), (dt.date(2026, 9, 30), 61), (TODAY, 66)]
    fc = [(TODAY, 66), (dt.date(2026, 12, 31), 68), (dt.date(2027, 1, 31), 80), (dt.date(2027, 2, 28), 92)]
    plt.rcParams.update({"font.family": "sans-serif", "font.sans-serif": ["Calibri", "Arial", "DejaVu Sans"],
                         "font.size": 10})
    fig, ax = plt.subplots(figsize=(9.2, 4.4), dpi=200)
    ax.plot([d for d, _ in plan], [v for _, v in plan], color="#8A97A6", lw=2, ls=(0, (6, 4)),
            label="Rencana (baseline Kick-Off, 9 bulan)")
    ax.plot([d for d, _ in act], [v for _, v in act], color="#1B2A4A", lw=2.6, marker="o",
            ms=5, label="Aktual (hasil assessment)")
    ax.plot([d for d, _ in fc], [v for _, v in fc], color="#2B5FCB", lw=1.8, ls=(0, (2, 3)),
            label="Proyeksi bersyarat (sertifikat Ex terbit, instalasi Jan 2027)")
    ax.axvline(TODAY, color="#B23A3A", lw=1.2, ls="--")
    ax.text(TODAY + dt.timedelta(days=3), 6, "17 Nov 2026", color="#B23A3A", fontsize=9, fontweight="bold")
    ax.annotate("Aktual 66%", xy=(TODAY, 66), xytext=(10, -18), textcoords="offset points",
                fontsize=9.5, fontweight="bold", color="#1B2A4A")
    ax.annotate("Rencana 78%", xy=(TODAY, 78), xytext=(-84, 8), textcoords="offset points",
                fontsize=9.5, fontweight="bold", color="#5B5B5B")
    ax.set_ylim(0, 105)
    ax.set_yticks([0, 20, 40, 60, 80, 100])
    ax.set_yticklabels([f"{v}%" for v in [0, 20, 40, 60, 80, 100]])
    ax.set_xlim(dt.date(2026, 6, 1), dt.date(2027, 3, 5))
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %y"))
    ax.grid(axis="y", color="#E3E3E3")
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.legend(loc="upper left", frameon=False, fontsize=9)
    fig.tight_layout()
    os.makedirs(os.path.dirname(CHART), exist_ok=True)
    fig.savefig(CHART, facecolor="white")
    plt.close(fig)


build_chart()

# ---------------------------------------------------------------- letterhead / cover
lt = doc.add_table(rows=1, cols=1)
lc = lt.rows[0].cells[0]
set_cell_shading(lc, "1B2A4A")
lc.paragraphs[0].paragraph_format.space_after = Pt(2)
r = lc.paragraphs[0].add_run("PT LAPI GANESHA UTAMA")
r.font.bold = True; r.font.size = Pt(14); r.font.color.rgb = WHITE
lp = lc.add_paragraph()
lp.paragraph_format.space_after = Pt(3)
r = lp.add_run("Bekerja sama dengan Lab IoT & Fisika Institut Teknologi Bandung")
r.font.size = Pt(9.5); r.font.color.rgb = RGBColor(0xC7, 0xD2, 0xE0)
doc.add_paragraph().paragraph_format.space_after = Pt(18)

p("LAPORAN INTERNAL", size=10, bold=True, color=GRAY, space_after=4)
title = doc.add_heading(level=0)
title.paragraph_format.space_after = Pt(4)
tr = title.add_run("Laporan Status Proyek GLD Tahap 2")
tr.font.size = Pt(22); tr.font.bold = True; tr.font.color.rgb = NAVY
p("Progres, Sertifikasi ATEX/IECEx, Termin Pembayaran, dan Timeline Kegiatan — per 17 November 2026",
  size=12, color=GRAY, space_after=18)

p("Document Control", size=11, bold=True, color=NAVY, space_after=4)
mt = doc.add_table(rows=0, cols=2)
mt.style = "Table Grid"
for k, v in [
    ("Nomor dokumen", DOC_NO),
    ("Revisi", REVISION),
    ("Tanggal", DOC_DATE),
    ("Periode laporan", "20 April 2026 – 17 November 2026 (fokus perubahan sejak 30 September 2026)"),
    ("Menggantikan", "LGU/GLD/LAP-STATUS/2026-001 (30 September 2026)"),
    ("Ditujukan kepada", "Manajemen PT LAPI Ganesha Utama — pelaporan anggaran operasional"),
    ("Proyek", "Gas Leak Detection (GLD) Tahap 2 — PT Pertamina Patra Niaga (pilot RU IV Cilacap)"),
    ("Klasifikasi", "Internal — Konfidensial"),
]:
    row = mt.add_row().cells
    set_cell_shading(row[0], HEAD_SHADE)
    row[0].paragraphs[0].paragraph_format.space_after = Pt(2)
    r0 = row[0].paragraphs[0].add_run(k)
    r0.font.bold = True; r0.font.size = Pt(9.3); r0.font.color.rgb = GRAY
    row[1].paragraphs[0].paragraph_format.space_after = Pt(2)
    r1 = row[1].paragraphs[0].add_run(v)
    r1.font.size = Pt(9.6)
    row[0].width = Inches(1.9); row[1].width = Inches(4.6)
doc.add_paragraph().paragraph_format.space_after = Pt(14)

p("Daftar Isi", size=11, bold=True, color=NAVY, space_after=4)
for line in ["1. Ringkasan Eksekutif", "2. Progres Proyek & Kurva-S", "3. Sertifikasi ATEX/IECEx",
             "4. Status Termin Pembayaran", "5. Persiapan Instalasi RU IV Cilacap",
             "6. Timeline Progres Harian", "7. Risiko & Keputusan yang Diperlukan", "8. Dokumen Rujukan"]:
    p(line, size=10, space_after=2)
doc.add_page_break()

# header / footer
header = sec.header
header.is_linked_to_previous = False
hp = header.paragraphs[0]
hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
hr = hp.add_run("Laporan Status Proyek GLD Tahap 2  |  Internal — Konfidensial")
hr.font.size = Pt(8); hr.font.color.rgb = GRAY; hr.font.italic = True
fp = sec.footer.paragraphs[0]
fr = fp.add_run(f"{DOC_NO}  ·  Rev. {REVISION}  ·  {DOC_DATE}")
fr.font.size = Pt(8); fr.font.color.rgb = GRAY
fp.add_run("  ·  Halaman ")
add_field(fp, "PAGE", "1")
fp.add_run(" dari ")
add_field(fp, "NUMPAGES", "1")
for run in fp.runs:
    run.font.size = Pt(8); run.font.color.rgb = GRAY

# ---------------------------------------------------------------- 1. Ringkasan
doc.add_heading("1. Ringkasan Eksekutif", level=1)
p("Laporan ini merangkum posisi proyek GLD Tahap 2 per 17 November 2026 untuk keperluan pelaporan "
  "anggaran operasional LGU, melanjutkan laporan 30 September 2026. Proyek berjalan pada dua jalur paralel "
  "dengan metrik berbeda — jalur rekayasa/lapangan (Kurva-S proyek 9 bulan) dan jalur sertifikasi "
  "ATEX/IECEx — ditambah dua milestone pembayaran Termin 1 yang dinilai terpisah oleh Pertamina.")
kpi_row([
    ("PROGRES REKAYASA/LAPANGAN", "66%", "vs rencana 78% (−12 poin)", NAVY),
    ("PERSIAPAN INSTALASI RU IV", "48%", "3 pihak; sisi LGU 100%", NAVY),
    ("TERMIN 1 FIELD TESTING (20%)", "Lengkap", "laporan rev 0.3 + FAT, 5 Okt", GREEN),
    ("TERMIN 1 SERTIFIKASI (40%)", "Berjalan", "berita acara witness belum ada", AMBER),
])
p("Poin utama:", bold=True, space_after=3)
for t in [
    "Progres rekayasa/lapangan naik dari 61% (30 September) menjadi 66% per 17 November, terhadap rencana 78% "
    "(selisih −12 poin). Seluruh selisih berasal dari aktivitas lapangan (instalasi, field trial, evaluasi). "
    "Aktivitas yang bisa dikerjakan tanpa instalasi sudah ≥90%, sehingga batas atas sebelum instalasi ≈67%.",
    "Pertamina RU IV menerbitkan HAC area SRU (2 Nov) dan MoC No. 15769/RU IV (3 Nov). Keempat titik GLD berada "
    "di Class I Div. 2, sehingga pemasangan GLD menunggu sertifikat Ex; infrastruktur pendukung (tiang, kabel, "
    "JB-01, server, jaringan) boleh disiapkan lebih dulu. Ini mengoreksi asumsi sebelumnya bahwa instalasi "
    "permanen berada di titik non-ATEX.",
    "Jalur sertifikasi kini menjadi jalur kritis jadwal lapangan. Sampel GLD2-0x1001 dibawa ke GTS pada 12 "
    "Oktober; dokumen teknis sertifikasi diperbarui mengikuti Panduan Revisi (rev 3.0); pre-scan EMC di Telkom "
    "Test House menunjukkan emisi di bawah batas kecuali frekuensi kerja LoRa (perlu konfirmasi lab).",
    "Laporan FAT (7/7 lulus lab) dan 3 Laporan Uji Lab formal dimasukkan ke Laporan Termin 1 Field Testing "
    "rev 0.3 (5 Oktober). Kedua Termin 1 tetap dievaluasi oleh Pertamina.",
    "Rollout berikutnya disiapkan paralel: rapat koordinasi RU VI Balongan 13 November (rencana 4 GLD / 2 CH / "
    "2 Gateway). Aplikasi dashboard kini menerima data MQTT dari Node-RED dan mendukung MySQL/MariaDB sesuai "
    "MoC (diuji 15 November).",
]:
    bullet(t)

# ---------------------------------------------------------------- 2. Kurva-S
doc.add_heading("2. Progres Proyek & Kurva-S", level=1)
p("Baseline Kurva-S dikalibrasi ke Project Timeline 9 bulan pada Deck Kick-Off (12 Juni 2026 – Februari "
  "2027, 12 aktivitas). Progres aktual adalah rata-rata status 12 aktivitas Gantt dengan bobot sama; "
  "di-reassess per 17 November 2026 menjadi 66% (795 ÷ 12). Rencana per 17 November = 78% (interpolasi "
  "71% per 31 Oktober dan 84% per 30 November). Pekerjaan sertifikasi ATEX/IECEx tidak termasuk dalam 12 "
  "aktivitas ini dan dilaporkan terpisah pada Bagian 3. Item yang menunggu pihak Pertamina tidak dihitung "
  "sebagai progres LGU.")
fig = doc.add_paragraph()
fig.alignment = WD_ALIGN_PARAGRAPH.CENTER
add_picture_fit(fig, CHART, max_w_in=6.6)
p("Gambar 1. Kurva-S proyek — rencana, aktual, dan proyeksi bersyarat, per 17 November 2026.", size=8.8,
  italic=True, color=GRAY, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=10)
table(["Tanggal", "Aktual", "Rencana", "Selisih", "Catatan"], [
    ["24 Jul 2026", "39%", "19%", "+20", "Rekayasa lab mendahului jadwal"],
    ["4 Sep 2026", "44%", "43%", "+1", "Pekerjaan mulai bergantung gate eksternal"],
    ["17 Sep 2026", "49%", "52%", "−3", "Uji ketahanan RF, persiapan instalasi"],
    ["30 Sep 2026", "61%", "62%", "−1", "Desain & prototipe selesai, diajukan ke sertifikasi; uji suhu"],
    ["17 Nov 2026", "66%", "78%", "−12", "FAT & uji lab formal, MoC 15769; instalasi menunggu sertifikat Ex"],
], [1.1, 0.8, 0.8, 0.8, 3.0])
p("Status 12 aktivitas Gantt (perubahan sejak 30 Sep ditandai):", bold=True, space_after=3)
table(["#", "Aktivitas", "Jadwal rencana", "Progres", "Status"], [
    ["1", "Kick-off & konfirmasi requirement", "8–15 Jun", "100%", "Selesai"],
    ["2", "Site survey & rencana pengambilan data", "15 Jun – 7 Jul", "100%", "Selesai — MoC 15769 memuat titik, rute kabel, lingkup SRU (sebelumnya 90%)"],
    ["3", "Detailed design", "1–21 Jul", "100%", "Selesai"],
    ["4", "Prototype build", "15 Jul – 21 Agu", "100%", "Selesai — sampel S/N GLD2-0x1001"],
    ["5", "Lab test", "15 Agu – 21 Sep", "95%", "Berjalan — FAT 7/7 lulus lab + 3 laporan uji lab (sebelumnya 72%)"],
    ["6", "AI model training / validation", "15 Agu – 21 Sep", "90%", "Berjalan — Laporan Uji Lab 01; model per-RU via chamber menyusul (sebelumnya 85%)"],
    ["7", "Integration test (fungsional)", "1 Jul – 7 Okt", "95%", "Berjalan — FAT, MQTT ingest + MySQL di aplikasi, paket serah-terima server (sebelumnya 80%)"],
    ["8", "HSE review & permit preparation", "1–14 Nov", "100%", "Selesai (sisi LGU)"],
    ["9", "Field installation", "15 Nov – 7 Des", "0%", "Belum mulai — pemasangan GLD menunggu sertifikat Ex (MoC)"],
    ["10", "Field trial", "8 Des – 7 Jan", "0%", "Belum mulai"],
    ["11", "Evaluation & final report", "1–21 Jan", "0%", "Belum mulai"],
    ["12", "Industrialization roadmap", "8–21 Feb", "15%", "Awal — alokasi per RU, koordinasi RU VI Balongan (sebelumnya 5%)"],
], [0.35, 2.4, 1.2, 0.65, 1.9], status_col=4)
box("Proyeksi bersyarat: dengan asumsi sertifikat Ex terbit dalam estimasi 5–8 bulan sejak Kick-Off dan instalasi "
    "berjalan Januari 2027, progres diperkirakan ±68% (31 Des), ±80% (31 Jan), dan ±92% (28 Feb). Program "
    "kemungkinan belum mencapai 100% pada akhir Februari 2027 kecuali sertifikat terbit lebih cepat atau "
    "titik GLD direlokasi ke area tidak terklasifikasi. Angka per aktivitas di atas adalah penilaian tim "
    "berdasarkan bukti dokumen, belum dikonfirmasi satu per satu oleh pimpinan proyek.",
    kind="warn", label="Catatan.")

# ---------------------------------------------------------------- 3. Sertifikasi
doc.add_heading("3. Sertifikasi ATEX/IECEx", level=1)
doc.add_heading("3.1 Kesiapan dokumen (checklist ExCB)", level=2)
p("Angka kesiapan dokumen ≈43% (21 item checklist resmi, bobot Final 100% / Sebagian 50% / Belum 0%) adalah "
  "hasil penilaian 30 September dan belum dihitung ulang. Sejak itu dokumen teknis bertambah banyak, tetapi "
  "sebagian besar butir yang masih kurang memerlukan data uji atau keputusan dari mitra casing, bukan teks:")
table(["Pekerjaan Okt–Nov", "Status"], [
    ["Daftar tindak lanjut revisi vs dossier terkirim ke GTS (7 Okt)", "Tersedia — 8 kontradiksi & 13 gambar/foto yang perlu disiapkan"],
    ["Skematik & layout PCB main board V4 (2.6.a.7–8)", "Tersedia — skematik sensor board belum ada"],
    ["Gambar teknik/CAD lengkap, foto assembly unit produksi, ukuran base/tutup/O-ring", "Tersedia — sketsa dari foto ukur, belum gambar terkendali"],
    ["Struktur detail mengikuti Panduan Revisi (BOM Ex, material, proses, kalkulasi, nameplate)", "Sebagian — kerangka lengkap, banyak nilai menunggu uji/mitra casing"],
    ["Dokumen Teknis Sertifikasi", "Rev 3.0 (9 Okt), 156 halaman"],
], [3.6, 2.9], status_col=1)
doc.add_heading("3.2 Pengajuan & sampel ke GTS", level=2)
p("GTS (Shanghai Global Testing Services) adalah agen sertifikasi yang meneruskan aplikasi ke badan "
  "sertifikasi dan laboratorium terakreditasi.")
table(["Item", "Status"], [
    ["Formulir aplikasi & dossier tim", "Dikirim ±29 September 2026 (Applicant & Manufacturer PT Galaksi Megatama Indonesia)"],
    ["Marking usulan", "II 2G Ex db IIC T4 Gb — Ex d, Group II, IIC, 2G/Zone 1, IP66 (target, belum diuji)"],
    ["Sampel GLD2-0x1001", "Dibawa ke Shanghai 12 Oktober 2026 dengan surat pengantar & surat keterangan Bea Cukai; berisi baterai Li-ion 7×18650 (UN 3481)"],
    ["Umpan balik iterasi dari GTS", "Belum tercatat di repo per 17 November"],
], [1.9, 4.6], bold_first=True)
box("Dossier yang terkirim masih memuat inkonsistensi yang perlu dibetulkan pada putaran iterasi GTS: suhu "
    "ambient campuran (−20/+60°C, −20/+85°C, −40/+85°C; nilai proyek −20/+60°C), marking debu \"Ex tb IIIC\", "
    "cable entry PG13.5 (dokumen teknis M20×1,5), dan konsep proteksi \"to be confirmed\". Bila penilai memakai "
    "+85°C, body sensor saat fan mati diproyeksikan ≈139°C dan melewati batas T4.",
    kind="warn", label="Untuk iterasi berikutnya.")
doc.add_heading("3.3 Enclosure & klasifikasi area (temuan November)", level=2)
p("Casing dan modul alarm GLD berasal dari detektor gas HIREP HRP-T1000-A (Zhengzhou HIREP Electronic "
  "Technology). Klaim penjual Ex d IIC T6 Gb berlaku untuk produk utuh; nomor sertifikat ATEX tidak "
  "tercantum, rating suhu housing −20…+55°C (di bawah +60°C GLD) dan T6 untuk daya ≤3 W (GLD ±8 W). "
  "Penggantian kaca depan dengan wire mesh dan penggantian elektronik berarti sertifikat produk HIREP tidak "
  "dapat dipakai untuk GLD. Tanggapan resmi ke Reliability RU IV dikirim 2 November (dokumen Informasi "
  "Enclosure & Proteksi Ledakan GLD — HAC SRU). MoC mensyaratkan minimal setara Zone 2 Group IIB T3 untuk "
  "titik GLD di area SRU.")
doc.add_heading("3.4 Pre-scan EMC (Telkom Test House, Oktober)", level=2)
p("Emisi EN 55032 Class A untuk GLD dan Cluster Head besar: semua titik di bawah batas kecuali frekuensi kerja "
  "LoRa 920–921 MHz (sinyal pancar sendiri, umumnya dinilai lewat standar radio — perlu konfirmasi lab). "
  "Margin GLD <1 dB di 117–127 MHz. Belum ada uji imunitas, uji Gateway, atau laporan resmi lab. Dua temuan "
  "terbuka dari Laporan EMC tim (28 Okt): EIRP LoRa (GLD ≈25 dBm, CH mesh ≈30 dBm) perlu dicek ke batas SDPPI, "
  "dan inlet gas + fan terbuka berisiko untuk target IP66.")
doc.add_heading("3.5 Hasil pengukuran suhu (indikasi kelas suhu T4)", level=2)
p("Tidak ada data suhu baru sejak 30 September. Hasil saat itu (8 kanal thermocouple, proyeksi ke ambient "
  "+60°C): kasus terburuk body sensor MQ saat fan mati ≈114°C, di bawah batas efektif T4 130°C (margin ±16 K); "
  "enclosure luar ≈79°C. DC/DC converter, inductor, MOSFET, dan kondisi alarm/Tx masih belum diukur.")

# ---------------------------------------------------------------- 4. Termin
doc.add_heading("4. Status Termin Pembayaran", level=1)
doc.add_heading("4.1 Termin 1 Field Testing (20%)", level=2)
p("Laporan Termin 1 Field Testing diperbarui ke rev 0.3 (5 Oktober 2026, ±140 halaman) dengan Laporan FAT "
  "rev 1.4 (7/7 item lulus uji lab) dan 3 Laporan Uji Lab formal (Model AI, LoRa, Mesh & Integrasi) sebagai "
  "Lampiran A; versi Word lengkap juga tersedia. Langkah administratif berikutnya: pengesahan laporan dan "
  "BAST. Penilaian pemenuhan dan keputusan pembayaran merupakan evaluasi Pertamina. Instalasi, commissioning, "
  "SAT, dan as-built termasuk dalam termin lapangan berikutnya.")
doc.add_heading("4.2 Termin 1 Sertifikasi (40%)", level=2)
p("Syarat kontraktual mencakup uji prototipe internal, iterasi desain berdasarkan hasil uji, witness dan "
  "validasi Pertamina sebelum uji laboratorium terakreditasi, serta berita acara dan laporan pekerjaan. "
  "Penilaian pemenuhan merupakan evaluasi Pertamina. Status bukti per 17 November:")
table(["#", "Syarat", "Status", "Bukti / kekurangan"], [
    ["1", "Prototipe enclosure tersedia", "Tersedia", "Sampel S/N GLD2-0x1001; foto assembly unit produksi (7 Okt)"],
    ["2", "Prototipe diuji (mekanik/termal/sealing/fault)", "Sebagian", "Uji termal internal 30 Sep; pre-scan EMC Okt; uji mekanik, sealing, dan fault belum tercatat"],
    ["3", "Iterasi desain berbasis hasil uji", "Sebagian", "Antena dipindah ke muka atas base; daftar tindak lanjut revisi 7 Okt"],
    ["4", "Disaksikan & divalidasi Pertamina", "Perlu konfirmasi", "Berita acara witness belum ada di repo"],
    ["5", "Selesai sebelum uji lab terakreditasi", "Perlu konfirmasi", "Sampel dibawa ke GTS 12 Okt; perlu dipastikan urutan dengan sesi witness"],
    ["6", "Berita acara", "Perlu dijadwalkan", "Template tersedia"],
    ["7", "Laporan pekerjaan", "Tersedia", "Laporan 15 Sep; perlu diperbarui dengan bukti Okt–Nov"],
], [0.3, 1.9, 1.2, 3.1], status_col=2)
box("Sampel sudah dibawa ke GTS sebelum ada berita acara witness yang tercatat di repo. Perlu dipastikan "
    "dengan Pertamina bagaimana syarat witness dipenuhi — misalnya witness atas uji ulang pada unit kedua, "
    "atau berita acara atas uji yang sudah dilakukan — sebelum Termin 1 Sertifikasi diajukan.",
    kind="warn", label="Perlu ditindaklanjuti.")

# ---------------------------------------------------------------- 5. Instalasi
doc.add_heading("5. Persiapan Instalasi RU IV Cilacap", level=1)
p("MoC No. 15769/RU IV Rev 0 (3 November 2026, Issued for Approval) menetapkan lingkup field test di area SRU "
  "(relokasi dari OM60): 4 GLD pada tiang baru 2\" HDG (±1,5 m), 5 CH pada pagar SRU, JB-01 di pipe support "
  "PS27, 1 Gateway di Control Room SRU, PC server (MySQL + Node-RED + MQTT), dan router LGU. Catu daya 24 VDC "
  "dari PSU di Control Room melalui kabel armored 14 AWG ke JB-01 lalu ke tiap GLD. Sistem bersifat "
  "standalone/advisory. Penyedia material dan pelaksana instalasi berada di pihak RU IV; LGU sebagai basis "
  "desain, supervisi teknis/QA, dan pekerjaan elektrikal spesifik GLD.")
box("HAC area SRU (2 November) menempatkan keempat titik GLD di Class I Groups C/D Div. 2. Kesimpulan MoC: "
    "infrastruktur pendukung boleh disiapkan lebih dulu, pemasangan GLD menunggu sertifikat Ex (minimal setara "
    "Zone 2 IIB T3) atau relokasi ke titik tidak terklasifikasi.",
    kind="warn", label="Gate instalasi.")
doc.add_heading("5.1 Pekerjaan LGU & ITB", level=2)
table(["Tahap", "Status"], [
    ["Survey lokasi", "Selesai (9–10 Agustus 2026)"],
    ["Spesifikasi Material Instalasi (rev 1.5) & Daftar Perangkat", "Selesai — dikirim ke Pertamina 1 Okt"],
    ["Block diagram lingkup final dengan router LGU", "Selesai (8 Okt)"],
    ["Checklist instalasi block diagram — 19 item persiapan LGU", "Selesai (28 Okt)"],
    ["Tanggapan HAC: informasi enclosure & proteksi ledakan", "Selesai — dikirim ke RU IV 2 Nov"],
    ["Aplikasi dashboard: MQTT ingest + MySQL/MariaDB, register RU4 per MoC", "Selesai — diuji 15 Nov"],
    ["Paket serah-terima PC server (Operator Hub, Node-RED, MariaDB, firmware)", "Selesai — diverifikasi 9–10 Nov"],
    ["Supervisi QA, terminasi, energize, commissioning, BA (di lokasi)", "Siap — menunggu pekerjaan RU IV"],
], [3.6, 2.9], status_col=1)
doc.add_heading("5.2 Kurva-S Persiapan Instalasi (3 pihak)", level=2)
table(["Pihak", "18 Sep", "17 Nov", "Keterangan"], [
    ["LGU & ITB", "100%", "100%", "15 dari 15 item"],
    ["Pertamina RU IV", "0%", "21%", "3 dari 14 — klasifikasi area (HAC), titik & rute kabel (MoC), metode mounting (MoC)"],
    ["Vendor / pelaksana instalasi", "0%", "9%", "1 dari 11 — orientasi pemasangan terjawab MoC (tiang vertikal)"],
    ["Keseluruhan", "38%", "48%", "19 dari 40 item"],
], [1.7, 0.7, 0.7, 3.4], bold_first=True)
doc.add_heading("5.3 Item di pihak Pertamina (tidak dihitung dalam progres LGU)", level=2)
table(["Item", "Pihak"], [
    ["Pengesahan MoC 15769 (status Rev 0: Issued for Approval)", "Pertamina RU IV"],
    ["Pengesahan TRA/JSA & penerbitan izin kerja", "Pertamina RU IV (HSE)"],
    ["Penugasan pelaksana instalasi & pengadaan material (eBVL)", "Pertamina RU IV"],
    ["Penyediaan PC server, PSU 24 VDC, kabel, JB-01, tiang", "Pertamina RU IV"],
    ["Kesepakatan jumlah perangkat (MoC 4 GLD/5 CH vs tabel alokasi 3 GLD/2 CH)", "Pertamina & LGU"],
    ["Sertifikat Ex untuk titik GLD (atau relokasi ke titik tidak terklasifikasi)", "Jalur sertifikasi / Pertamina RU IV"],
], [3.9, 2.6])

# ---------------------------------------------------------------- 6. Timeline
doc.add_heading("6. Timeline Progres Harian", level=1)
p("Kronologi kegiatan dan milestone proyek dari awal fase lab hingga 17 November 2026. Rentang tanggal "
  "dipakai untuk periode kerja mingguan fase awal.")
TL = [
    ("FASE 1 — LAB (20 APR – 7 JUN 2026)",),
    ("20–26 Apr", "Desain chamber gas; uji node GLD lama; uji routing Cluster Head.", "Engineering"),
    ("27 Apr – 3 Mei", "Uji node GLD baru #0001/#0002 (ADC 8 kanal, LoRa); uji baterai CH.", "Engineering"),
    ("4–10 Mei", "Uji fungsional dimulai; uji solar ke CH; firmware CH power-recovery guard + watchdog.", "Engineering"),
    ("11–17 Mei", "Uji jarak & reliabilitas LoRa; profil konsumsi baterai node.", "Engineering"),
    ("18–31 Mei", "Uji sistem se-kampus; Site Survey Technical Checklist; topologi star-mesh & failover CH terbukti.", "Milestone"),
    ("1–7 Jun", "Persiapan pemasangan; uji RF LoRa (100 m, PDR 100%).", "Engineering"),
    ("FASE 2 — KICK-OFF & MENUJU LAPANGAN (JUN – JUL 2026)",),
    ("12 Jun", "Kick-Off dengan Pertamina — baseline 9 bulan, scope 6 Refinery Unit.", "Milestone"),
    ("18 Jun", "Prinsip AI fingerprint 8-sensor ditetapkan; target TRL-7.", "Engineering"),
    ("26 Jun", "Uji antena LoRa; pengembangan model TCN dimulai.", "Engineering"),
    ("30 Jun", "Project Report Juni: PCB v1/v2 selesai; progres chamber & dataset.", "Laporan"),
    ("6–8 Jul", "Uji 2 Cluster Head; uji baterai CH ±40 jam; uji lapangan CH3 8 hari.", "Engineering"),
    ("9 Jul", "Rantai komunikasi GLD–CH–Gateway–Server tersambung (MQTT).", "Milestone"),
    ("15 Jul", "Dataset 14.477 sampel; model TCN 8 sensor akurasi ≥92%.", "Milestone"),
    ("16 Jul", "Uji fungsional end-to-end; analisis daya; uji mesh 8-CH multi-hop se-kampus.", "Milestone"),
    ("23 Jul", "Repo server aktif (firmware, Operator Hub, nulling); sistem kendali chamber gas berbasis ESP32.", "Engineering"),
    ("24 Jul", "Rapat LGU–Pertamina: versi 24 VDC siap sertifikasi; 18 action item.", "Rapat"),
    ("30 Jul", "Rapat mingguan: kunjungan Cilacap dimajukan ke 9–10 Agustus; arsitektur aplikasi lokal.", "Rapat"),
    ("FASE 3 — SURVEY & DOKUMENTASI (AGU 2026)",),
    ("6 Agu", "Rapat resmi instalasi & mounting di Lab IoT ITB — bracket tanpa bor/las; requirement gas Benzena/CO/H2S.", "Rapat"),
    ("6–8 Agu", "Demo mesh Gateway + 3 CH; push alarm otomatis berhasil diuji.", "Milestone"),
    ("9 Agu", "Model CNN Dual-Branch ditetapkan sebagai model AI resmi (99,20% on-chip).", "Milestone"),
    ("9–10 Agu", "Kunjungan RU IV Cilacap — survey lokasi selesai.", "Milestone"),
    ("19 Agu", "Datasheet Sistem konsolidasi; inferensi AI on-device dikonfirmasi; catu daya 24 VDC final.", "Dokumen"),
    ("31 Agu", "Desain CAD bracket U-bolt v2; laporan progres 20 Apr – 31 Agu difinalisasi.", "Dokumen"),
    ("FASE 4 — SERTIFIKASI & PERSIAPAN INSTALASI (SEP 2026)",),
    ("4 Sep", "Proposal formal direkonsiliasi; presentasi progres untuk VP Pertamina; 6 gate integrasi ditutup; Kurva-S 44%.", "Laporan"),
    ("5 Sep", "Dashboard sertifikasi; target Zona 1 / 2G / T4 dan usulan grup gas IIC.", "Sertifikasi"),
    ("10 Sep", "Checklist kesiapan instalasi 3 jalur; audit kesiapan Termin 1.", "Dokumen"),
    ("11 Sep", "Dokumen teknis sertifikasi (bahasa Inggris, format korporat) dimulai; laporan Termin 1 Field Testing.", "Sertifikasi"),
    ("15 Sep", "Laporan pemenuhan Termin 1 Sertifikasi (40%).", "Laporan"),
    ("17 Sep", "Uji awal ketahanan RF terhadap interferensi; Bagian 1 checklist ExCB; lokasi instalasi permanen: perimeter SRU; Kurva-S 49%.", "Milestone"),
    ("18 Sep", "Kurva-S persiapan instalasi (38%) atas permintaan Pertamina.", "Laporan"),
    ("22 Sep", "Instruction Manual GLD; PT Galaksi Megatama Indonesia teridentifikasi sebagai manufacturer; spesifikasi IP66 & cable gland.", "Sertifikasi"),
    ("23 Sep", "Formulir aplikasi ATEX dari GTS diterima.", "Sertifikasi"),
    ("24 Sep", "Spesifikasi final: suhu operasi −20/+60°C, kelembapan 5–95% RH, berat 2,378 kg.", "Sertifikasi"),
    ("25 Sep", "Material mesh (stainless) & gasket (karet) dikonfirmasi; batas kelistrikan 24 VDC; dossier tim Rev 25 Sep.", "Sertifikasi"),
    ("28 Sep", "Metode proteksi Ex d dipilih (usulan tim); Applicant = PT Galaksi; bahan rapat Pertamina disiapkan.", "Sertifikasi"),
    ("29 Sep", "Aplikasi & dossier dikirim ke GTS; rapat koordinasi persiapan instalasi dengan Pertamina.", "Milestone"),
    ("30 Sep", "Data pengukuran suhu pertama (indikasi T4 positif); dokumen persiapan instalasi diteruskan ke Pertamina; Kurva-S 61%.", "Milestone"),
    ("FASE 5 — FAT, SAMPEL KE GTS & MoC RU IV (OKT – NOV 2026)",),
    ("1 Okt", "Spesifikasi Material Instalasi, Pembagian Persiapan, Daftar Pelaksana dikirim ke grup Pertamina.", "Dokumen"),
    ("2 Okt", "Desain lingkup RU IV dari Pertamina diterima; dimensi CH besar diukur; riwayat PCB GLD V1–V5.", "Engineering"),
    ("4–5 Okt", "Laporan FAT (7/7 lulus lab) & 3 Laporan Uji Lab; Laporan Termin 1 Field Testing rev 0.3.", "Milestone"),
    ("7 Okt", "Daftar tindak lanjut revisi ATEX; skematik & layout PCB V4; gambar teknik & foto assembly masuk dokumen sertifikasi.", "Sertifikasi"),
    ("8 Okt", "Block diagram lingkup RU IV final dengan router LGU.", "Dokumen"),
    ("12 Okt", "Sampel GLD2-0x1001 dibawa ke GTS Shanghai.", "Milestone"),
    ("15 Okt", "Pre-scan EMC GLD & CH di Telkom Test House.", "Sertifikasi"),
    ("18–22 Okt", "Video produk GLD (Digitalization Day) & konsep OGI; Pertamina teruskan kebutuhan field test ke tiap RU; rapat 22 Okt.", "Rapat"),
    ("28 Okt", "Laporan EMC rev 1.0; checklist instalasi — semua persiapan LGU selesai.", "Dokumen"),
    ("2 Nov", "HAC SRU: titik GLD di Class I Div. 2; casing teridentifikasi HIREP HRP-T1000-A; tanggapan enclosure ke RU IV.", "Milestone"),
    ("3 Nov", "MoC 15769/RU IV diterima; tabel alokasi perangkat per RU (28 GLD, 22 CH, 7 GW).", "Milestone"),
    ("9–15 Nov", "Paket serah-terima PC server diverifikasi; aplikasi dashboard dengan MQTT ingest + MySQL.", "Engineering"),
    ("13 Nov", "Rapat koordinasi implementasi RU VI Balongan.", "Rapat"),
    ("17 Nov", "Kurva-S proyek 66%; Kurva-S persiapan instalasi 48%.", "Laporan"),
]
tbl = doc.add_table(rows=1, cols=3)
tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
for i, h in enumerate(["Tanggal", "Kegiatan / milestone", "Kategori"]):
    c = tbl.rows[0].cells[i]
    set_cell_shading(c, "1B2A4A")
    c.paragraphs[0].paragraph_format.space_after = Pt(1)
    r = c.paragraphs[0].add_run(h)
    r.font.bold = True; r.font.size = Pt(8.6); r.font.color.rgb = WHITE
zi = 0
for row in TL:
    cells = tbl.add_row().cells
    if len(row) == 1:
        m = cells[0].merge(cells[1]).merge(cells[2])
        set_cell_shading(m, "D9DEE6")
        m.paragraphs[0].paragraph_format.space_after = Pt(1)
        r = m.paragraphs[0].add_run(row[0])
        r.font.bold = True; r.font.size = Pt(8.6); r.font.color.rgb = NAVY
        zi = 0
        continue
    for ci, val in enumerate(row):
        c = cells[ci]
        if zi % 2 == 1:
            set_cell_shading(c, ZEBRA_SHADE)
        c.paragraphs[0].paragraph_format.space_after = Pt(1)
        r = c.paragraphs[0].add_run(val)
        r.font.size = Pt(8.8)
        if ci == 0:
            r.font.bold = True
        if ci == 2 and val == "Milestone":
            r.font.bold = True; r.font.color.rgb = NAVY
    zi += 1
for row in tbl.rows:
    for i, w in enumerate([1.15, 4.35, 1.0]):
        row.cells[i].width = Inches(w)
set_table_borders(tbl)
finish_table(tbl, keep_together=False)
doc.add_paragraph().paragraph_format.space_after = Pt(4)

# ---------------------------------------------------------------- 7. Risiko
doc.add_heading("7. Risiko & Keputusan yang Diperlukan", level=1)
table(["Risiko / isu", "Dampak", "Tindak lanjut", "Pihak"], [
    ["Pemasangan GLD menunggu sertifikat Ex (HAC/MoC)", "Instalasi, field trial, evaluasi, dan termin lapangan tertunda", "Kawal iterasi GTS; kaji relokasi titik GLD ke area tidak terklasifikasi", "LGU & Pertamina RU IV"],
    ["Sertifikat HIREP tidak berlaku untuk GLD termodifikasi", "Tidak bisa memakai klaim Ex d bawaan casing", "Selesaikan sertifikasi GLD sendiri; flame arrestor bersertifikat di bukaan sensor", "Tim sertifikasi & mitra casing"],
    ["Inkonsistensi dossier di GTS (Tamb, marking debu, cable entry)", "Penilaian T4 bisa memakai +85°C → gagal", "Betulkan pada iterasi GTS berikutnya", "Tim sertifikasi"],
    ["Urutan witness vs pengiriman sampel Termin 1 Sertifikasi", "Syarat 4–6 belum terdokumentasi", "Sepakati dengan Pertamina bentuk witness & berita acara", "LGU & Pertamina"],
    ["Jumlah perangkat RU IV berbeda antar dokumen", "BoQ, register aplikasi, dan termin bisa tidak sinkron", "Konfirmasi tertulis ke Pertamina", "LGU"],
    ["EIRP LoRa & margin EMC tipis", "Bisa gagal uji RF/EMC resmi", "Cek batas SDPPI; atur daya pancar; uji ulang", "Tim teknis"],
    ["Titik panas belum lengkap diukur", "Kelas suhu belum terverifikasi penuh", "Ukur DC/DC, inductor, MOSFET, kondisi alarm/Tx", "Tim teknis"],
], [1.9, 1.5, 1.9, 1.2])
p("Keputusan yang diminta dari manajemen LGU:", bold=True, space_after=3)
for t in [
    "Arah pilot RU IV: menunggu sertifikat Ex, atau mengusulkan ke Pertamina relokasi titik GLD ke area tidak "
    "terklasifikasi agar field test dapat dimulai lebih awal.",
    "Penunjukan PIC yang mengawal iterasi GTS dan penyelarasan dossier, termasuk koordinasi dengan mitra casing.",
    "Persetujuan pendekatan witness Termin 1 Sertifikasi bersama Pertamina (bentuk, jadwal, anggaran).",
    "Alokasi tim untuk persiapan paralel RU VI Balongan dan RU lain tanpa mengganggu jalur sertifikasi.",
]:
    bullet(t)

# ---------------------------------------------------------------- 8. Rujukan
doc.add_heading("8. Dokumen Rujukan", level=1)
table(["No", "Dokumen", "Keterangan"], [
    ["01", "Dashboard Proyek GLD (HTML & PDF)", "Kurva-S, Gantt, KPI per 17 Nov"],
    ["02", "Kurva-S Persiapan Instalasi RU IV Cilacap rev 1.1", "Kesiapan 3 pihak per 17 Nov (48%)"],
    ["03", "MoC No. 15769/RU IV Rev 0 & HAC area SRU", "Dokumen Pertamina, 2–3 Nov"],
    ["04", "Informasi Enclosure & Proteksi Ledakan GLD — HAC SRU", "Tanggapan LGU ke RU IV, 2 Nov"],
    ["05", "Laporan Termin 1 Field Testing rev 0.3 + Laporan FAT rev 1.4", "5 Okt"],
    ["06", "Dokumen Teknis Sertifikasi IECEx/ATEX rev 3.0", "Bahasa Inggris"],
    ["07", "Daftar Tindak Lanjut Revisi ATEX", "7 Okt"],
    ["08", "Laporan Teknis Pengujian EMC rev 1.0", "28 Okt"],
    ["09", "Deck Koordinasi Implementasi RU VI Balongan", "13 Nov"],
    ["10", "Laporan Status Proyek 30 September 2026", "Versi sebelumnya"],
], [0.6, 3.2, 2.7], bold_first=True)

doc.save(OUT)
print("written", OUT)
