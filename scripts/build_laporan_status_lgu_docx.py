# -*- coding: utf-8 -*-
"""Laporan Status Proyek GLD Tahap 2 untuk internal LGU (anggaran operasional).

Output: Deliverables/Laporan_Status_Proyek_GLD_LGU_30September2026.docx
(PDF dirender terpisah via Word COM).
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
OUT = os.path.join(REPO, "Deliverables", "Laporan_Status_Proyek_GLD_LGU_30September2026.docx")
CHART = os.path.join(REPO, "scripts", "assets", "kurva_s_proyek_30sep2026.png")

DOC_NO = "LGU/GLD/LAP-STATUS/2026-001"
REVISION = "1.0"
DOC_DATE = "30 September 2026"
TODAY = dt.date(2026, 9, 30)

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
           (dt.date(2026, 9, 4), 44), (dt.date(2026, 9, 17), 49), (TODAY, 49)]
    plt.rcParams.update({"font.family": "sans-serif", "font.sans-serif": ["Calibri", "Arial", "DejaVu Sans"],
                         "font.size": 10})
    fig, ax = plt.subplots(figsize=(9.2, 4.4), dpi=200)
    ax.plot([d for d, _ in plan], [v for _, v in plan], color="#8A97A6", lw=2, ls=(0, (6, 4)),
            label="Rencana (baseline Kick-Off, 9 bulan)")
    ax.plot([d for d, _ in act[:-1]], [v for _, v in act[:-1]], color="#1B2A4A", lw=2.6, marker="o",
            ms=5, label="Aktual (hasil assessment)")
    ax.plot([act[-2][0], act[-1][0]], [act[-2][1], act[-1][1]], color="#1B2A4A", lw=2, ls=":")
    ax.axvline(TODAY, color="#B23A3A", lw=1.2, ls="--")
    ax.text(TODAY + dt.timedelta(days=3), 6, "30 Sep 2026", color="#B23A3A", fontsize=9, fontweight="bold")
    ax.annotate("Aktual 49%", xy=(TODAY, 49), xytext=(12, -16), textcoords="offset points",
                fontsize=9.5, fontweight="bold", color="#1B2A4A")
    ax.annotate("Rencana 62%", xy=(TODAY, 62), xytext=(-78, 6), textcoords="offset points",
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
p("Progres, Sertifikasi ATEX/IECEx, Termin Pembayaran, dan Timeline Kegiatan — per 30 September 2026",
  size=12, color=GRAY, space_after=18)

p("Document Control", size=11, bold=True, color=NAVY, space_after=4)
mt = doc.add_table(rows=0, cols=2)
mt.style = "Table Grid"
for k, v in [
    ("Nomor dokumen", DOC_NO),
    ("Revisi", REVISION),
    ("Tanggal", DOC_DATE),
    ("Periode laporan", "20 April 2026 – 30 September 2026"),
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
             "6. Timeline Progres Harian", "7. Risiko & Keputusan yang Diperlukan", "8. Daftar Lampiran"]:
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
p("Laporan ini merangkum posisi proyek GLD Tahap 2 per 30 September 2026 untuk keperluan pelaporan "
  "anggaran operasional LGU. Proyek berjalan pada dua jalur paralel dengan metrik yang berbeda — "
  "jalur rekayasa/lapangan (Kurva-S proyek 9 bulan) dan jalur sertifikasi ATEX/IECEx — ditambah dua "
  "milestone pembayaran Termin 1 yang dinilai terpisah oleh Pertamina.")
kpi_row([
    ("PROGRES REKAYASA/LAPANGAN", "49%", "vs rencana 62% (−13 poin)", NAVY),
    ("KESIAPAN DOKUMEN SERTIFIKASI", "≈43%", "21 item checklist, berbobot", NAVY),
    ("TERMIN 1 FIELD TESTING (20%)", "Lengkap", "laporan & draf BAST tersedia", GREEN),
    ("TERMIN 1 SERTIFIKASI (40%)", "Berjalan", "bukti uji & witness disiapkan", AMBER),
])
p("Poin utama:", bold=True, space_after=3)
for t in [
    "Progres rekayasa/lapangan 49% tidak bergerak sejak 17 September, sementara baseline rencana naik ke 62% "
    "pada akhir September. Selisih −13 poin berasal dari pekerjaan yang kini tertahan gate eksternal "
    "(instalasi RU IV menunggu penugasan vendor, TRA/JSA, dan klasifikasi area oleh Pertamina), bukan "
    "dari rekayasa yang melambat.",
    "Aplikasi sertifikasi ATEX sudah dikirim ke GTS (agen sertifikasi) sekitar 29 September dengan Applicant "
    "dan Manufacturer PT Galaksi Megatama Indonesia, marking usulan II 2G Ex db IIC T4 Gb. Proses berlanjut "
    "melalui putaran iterasi dari GTS.",
    "Data pengukuran suhu pertama (30 September) memberi indikasi positif untuk kelas suhu T4: kasus "
    "terburuk ≈114°C pada ambient +60°C, di bawah batas efektif 130°C.",
    "Kedua Termin 1 dievaluasi oleh Pertamina. Dokumen Termin 1 Field Testing (laporan pemenuhan dan draf BAST) sudah lengkap. Untuk Termin 1 Sertifikasi, tim sedang menyiapkan bukti uji prototipe internal yang disaksikan Pertamina beserta berita acara, sesuai syarat kontraktual.",
]:
    bullet(t)

# ---------------------------------------------------------------- 2. Kurva-S
doc.add_heading("2. Progres Proyek & Kurva-S", level=1)
p("Baseline Kurva-S dikalibrasi ke Project Timeline 9 bulan pada Deck Kick-Off (12 Juni 2026 – Februari "
  "2027, 12 aktivitas). Progres aktual adalah rata-rata status 12 aktivitas Gantt; assessment terakhir "
  "17 September 2026 (49%) dan dikonfirmasi tetap valid per 30 September karena tidak ada aktivitas Gantt "
  "yang bergerak sejak itu.")
fig = doc.add_paragraph()
fig.alignment = WD_ALIGN_PARAGRAPH.CENTER
add_picture_fit(fig, CHART, max_w_in=6.6)
p("Gambar 1. Kurva-S proyek — rencana vs aktual, per 30 September 2026.", size=8.8, italic=True,
  color=GRAY, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=10)
table(["Tanggal", "Aktual", "Rencana", "Selisih", "Catatan"], [
    ["24 Jul 2026", "39%", "19%", "+20", "Rekayasa lab mendahului jadwal"],
    ["4 Sep 2026", "44%", "43%", "+1", "Pekerjaan mulai bergantung gate eksternal"],
    ["17 Sep 2026", "49%", "52%", "−3", "Assessment terakhir"],
    ["30 Sep 2026", "49%", "62%", "−13", "Rencana naik (integration test & HSE/permit), aktual tertahan gate"],
], [1.1, 0.8, 0.8, 0.8, 3.0])
p("Status 12 aktivitas Gantt:", bold=True, space_after=3)
table(["#", "Aktivitas", "Jadwal rencana", "Progres", "Status"], [
    ["1", "Kick-off & konfirmasi requirement", "8–15 Jun", "100%", "Selesai"],
    ["2", "Site survey & rencana pengambilan data", "15 Jun – 7 Jul", "75%", "Sebagian — survey RU IV selesai 9–10 Agu"],
    ["3", "Detailed design", "1–21 Jul", "92%", "Hampir selesai"],
    ["4", "Prototype build", "15 Jul – 21 Agu", "68%", "Berjalan"],
    ["5", "Lab test", "15 Agu – 21 Sep", "65%", "Berjalan"],
    ["6", "AI model training / validation", "15 Agu – 21 Sep", "85%", "Berjalan"],
    ["7", "Integration test (fungsional)", "1 Jul – 7 Okt", "80%", "Berjalan"],
    ["8", "HSE review & permit preparation", "1–14 Nov", "22%", "Menunggu proses RU IV"],
    ["9", "Field installation", "15 Nov – 7 Des", "0%", "Belum mulai"],
    ["10", "Field trial", "8 Des – 7 Jan", "0%", "Belum mulai"],
    ["11", "Evaluation & final report", "1–21 Jan", "0%", "Belum mulai"],
    ["12", "Industrialization roadmap", "8–21 Feb", "5%", "Awal"],
], [0.35, 2.6, 1.3, 0.7, 1.55], status_col=4)

# ---------------------------------------------------------------- 3. Sertifikasi
doc.add_heading("3. Sertifikasi ATEX/IECEx", level=1)
doc.add_heading("3.1 Kesiapan dokumen (checklist ExCB)", level=2)
p("Kesiapan dihitung dari 21 item checklist resmi (Bagian 1.1–1.5, 2.1–2.5, 2.6.a–i, 3.1–3.2) dengan bobot "
  "Final 100%, Sebagian 50%, Belum 0%: 5 Final, 8 Sebagian, 8 Belum → (5×100 + 8×50) ÷ 21 ≈ 43%. "
  "Angka ini mengukur kelengkapan dokumen, bukan waktu menuju sertifikat terbit.")
table(["Bagian", "Final", "Sebagian", "Belum", "Keterangan"], [
    ["1. Informasi dasar (1.1–1.5)", "0", "3", "2", "Legalitas & fasilitas PT Galaksi sebagian; ISO 9001 audit Okt 2026"],
    ["2.1–2.5 Deskripsi & klasifikasi", "5", "0", "0", "Lengkap; klasifikasi masih usulan tim"],
    ["2.6.a–i Desain & manufaktur", "0", "4", "5", "Gambar, BOM, instruksi, suhu sebagian; material, proses, kalkulasi, nameplate, sertifikat komponen belum"],
    ["3. Sampel (3.1–3.2)", "0", "1", "1", "S/N sampel GLD2-0x1001 kini ditetapkan tim"],
    ["Total", "5", "8", "8", "≈43%"],
], [1.9, 0.6, 0.75, 0.6, 2.65], bold_first=True)
doc.add_heading("3.2 Pengajuan ke GTS", level=2)
p("GTS (Shanghai Global Testing Services) adalah agen sertifikasi yang meneruskan aplikasi ke badan "
  "sertifikasi dan laboratorium terakreditasi. Berkas yang dikirim sekitar 29 September 2026:")
table(["Item", "Isi"], [
    ["Formulir aplikasi ATEX (A0)", "Applicant & Manufacturer PT Galaksi Megatama Indonesia; kontak Antonius Prasetyo (Director)"],
    ["Marking usulan", "II 2G Ex db IIC T4 Gb — Ex d (flameproof), Group II, IIC, Category 2G/Zone 1, IP66, stationary"],
    ["Rating & fisik", "24 VDC, ≈0,33 A, 8 W; 200 × 90 × 290 mm; 2,378 kg"],
    ["Dossier teknis", "IECEx/ATEX Certification Information Requirements Rev 25 Sep 2026 (60 halaman, disusun tim)"],
], [1.9, 4.6], bold_first=True)
box("Dossier yang terkirim masih memuat beberapa inkonsistensi yang perlu dibetulkan pada putaran iterasi "
    "berikutnya dari GTS: suhu ambient tertulis campuran −20/+60°C, −20/+85°C, dan −40/+85°C (nilai proyek: "
    "−20/+60°C); marking debu \"Ex tb IIIC\" pada bagian nameplate (di luar scope gas); cable entry PG13.5 "
    "(dokumen teknis: M20×1,5); dan konsep proteksi yang masih tertulis \"to be confirmed\".",
    kind="warn", label="Untuk iterasi berikutnya.")
doc.add_heading("3.3 Hasil pengukuran suhu (indikasi kelas suhu T4)", level=2)
p("Pengukuran internal 30 September: 8 kanal thermocouple, 3 kondisi, masing-masing 180 menit pada ambient "
  "≈24–25°C, diproyeksikan ke ambient maksimum +60°C.")
table(["Kondisi", "Body sensor MQ", "PCB", "Enclosure luar"], [
    ["Normal", "44,2 → ≈79°C", "52,4 → ≈88°C", "32,1 → ≈67°C"],
    ["Beban maksimum", "55,0 → ≈91°C", "58,3 → ≈94°C", "34,8 → ≈71°C"],
    ["Fan mati (malfungsi)", "78,4 → ≈114°C", "63,4 → ≈99°C", "43,9 → ≈79°C"],
], [1.9, 1.6, 1.4, 1.6], bold_first=True)
p("Batas T4 135°C dikurangi margin 5 K (IEC 60079-0) = 130°C. Kasus terburuk ≈114°C → margin ±16 K. "
  "Masih terbuka: DC/DC converter, inductor, dan MOSFET belum diukur; kondisi alarm/Tx belum diukur; PCB "
  "pada beban maksimum belum stabil; metadata uji belum lengkap. Perhatian: bila suhu ambient +85°C (nilai "
  "keliru di dossier) yang dipakai penilai, body sensor saat fan mati diproyeksikan ≈139°C dan melewati batas.")

# ---------------------------------------------------------------- 4. Termin
doc.add_heading("4. Status Termin Pembayaran", level=1)
doc.add_heading("4.1 Termin 1 Field Testing (20%)", level=2)
p("Laporan pemenuhan deliverable (Rev02) dan draf BAST sudah tersedia. Bukti yang terdokumentasi mencakup "
  "detail engineering, kesiapan 4 GLD dan 16 Cluster Head, konfigurasi firmware, integrasi "
  "GLD–CH–Gateway–Server, mesh/failover, dan alarm push. Langkah administratif berikutnya: pengesahan laporan "
  "dan BAST. Penilaian pemenuhan dan keputusan pembayaran merupakan evaluasi Pertamina. Instalasi, "
  "commissioning, dan as-built termasuk dalam termin lapangan berikutnya.")
doc.add_heading("4.2 Termin 1 Sertifikasi (40%)", level=2)
p("Syarat kontraktual Termin 1 Sertifikasi mencakup uji prototipe internal, iterasi desain berdasarkan hasil "
  "uji, witness dan validasi oleh Pertamina sebelum uji laboratorium terakreditasi, serta berita acara dan "
  "laporan pekerjaan. Penilaian pemenuhan merupakan evaluasi Pertamina. Status penyiapan bukti per 30 "
  "September:")
table(["#", "Syarat", "Status", "Bukti / kekurangan"], [
    ["1", "Prototipe enclosure tersedia", "Sebagian", "Unit terakit & terfoto; S/N GLD2-0x1001 ditetapkan; lembar identifikasi sampel untuk ditandatangani"],
    ["2", "Prototipe diuji (mekanik/termal/sealing/fault)", "Sebagian", "Uji termal internal 30 Sep; uji mekanik, sealing, dan fault menyusul"],
    ["3", "Iterasi desain berbasis hasil uji", "Dalam penyiapan", "Perubahan posisi antena ke atas base; dikaitkan dengan temuan uji pada sesi witness"],
    ["4", "Disaksikan & divalidasi Pertamina", "Perlu dijadwalkan", "Sesi witness uji enclosure bersama Pertamina"],
    ["5", "Selesai sebelum uji lab terakreditasi", "Tersedia", "Sampel masih di tim; sesi witness dilakukan sebelum pengiriman sampel"],
    ["6", "Berita acara", "Perlu dijadwalkan", "Template tersedia; diisi setelah sesi witness"],
    ["7", "Laporan pekerjaan", "Tersedia", "Laporan 15 Sep; perlu diperbarui setelah uji & witness"],
], [0.3, 1.9, 1.2, 3.1], status_col=2)
box("Langkah berikutnya: jadwalkan satu sesi uji internal yang disaksikan Pertamina — ulang uji termal dengan "
    "titik DC/DC, inductor, MOSFET; tambah pemeriksaan mekanik/dimensi dan uji sealing sederhana — lalu "
    "tuangkan dalam berita acara, sebelum sampel dikirim melalui GTS.", kind="ok", label="Rekomendasi.")

# ---------------------------------------------------------------- 5. Instalasi
doc.add_heading("5. Persiapan Instalasi RU IV Cilacap", level=1)
p("Arah kerja: uji chamber gas di kantor kilang (non-area proses) dan instalasi permanen di lokasi non-ATEX, "
  "yaitu perimeter Sulfur Recovery Unit. Eksekusi fisik oleh vendor yang ditunjuk Pertamina; LGU berperan "
  "sebagai basis desain, supervisi teknis/QA, dan pekerjaan elektrikal spesifik GLD.")
table(["Tahap", "Status"], [
    ["Survey lokasi", "Selesai (9–10 Agustus 2026)"],
    ["Basis desain bracket U-bolt (CAD) & dokumen persiapan", "Selesai — diteruskan ke grup Pertamina 30 Sep"],
    ["Kesiapan sisi LGU & ITB (Kurva-S persiapan instalasi)", "Selesai — 100% (keseluruhan 38%)"],
    ["Penugasan resmi vendor instalasi", "Menunggu proses RU IV"],
    ["Pengesahan TRA/JSA & izin kerja", "Menunggu proses RU IV"],
    ["Dokumen klasifikasi area perimeter SRU", "Menunggu proses RU IV"],
    ["Rapat koordinasi persiapan (29 Sep)", "Selesai — 4 keputusan diajukan"],
    ["Instalasi fisik & commissioning", "Belum mulai"],
], [3.6, 2.9], status_col=1)

# ---------------------------------------------------------------- 6. Timeline
doc.add_heading("6. Timeline Progres Harian", level=1)
p("Kronologi kegiatan dan milestone proyek dari awal fase lab hingga 30 September 2026. Rentang tanggal "
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
    ("30 Sep", "Data pengukuran suhu pertama (indikasi T4 positif); dokumen persiapan instalasi diteruskan ke Pertamina; audit progres.", "Milestone"),
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
    ["Instalasi RU IV tertahan (vendor, TRA/JSA, klasifikasi area)", "Deviasi Kurva-S melebar; termin lapangan tertunda", "Kawal 4 keputusan rapat 29 Sep", "Pertamina RU IV"],
    ["Bukti uji & witness Termin 1 Sertifikasi masih disiapkan", "Waktu evaluasi Termin 1 Sertifikasi bergantung pada sesi ini", "Jadwalkan sesi uji disaksikan Pertamina + berita acara", "LGU & Pertamina"],
    ["Urutan Termin 1: sampel terkirim sebelum witness", "Urutan syarat 5 terganggu", "Kirim sampel setelah sesi witness selesai", "LGU"],
    ["Inkonsistensi dossier di GTS (Tamb, marking debu, cable entry)", "Penilaian T4 bisa memakai +85°C → gagal", "Betulkan pada iterasi GTS berikutnya", "Tim sertifikasi"],
    ["Titik panas belum lengkap diukur", "Kelas suhu belum terverifikasi penuh", "Ukur DC/DC, inductor, MOSFET, kondisi alarm/Tx", "Tim teknis"],
    ["Sampel gas tambahan (H2S, dll.) belum tersedia", "Kapabilitas gas tambahan tertunda", "Chamber on-site di kilang; pengadaan paralel", "Pertamina & LGU"],
], [1.9, 1.5, 1.9, 1.2])
p("Keputusan yang diminta dari manajemen LGU:", bold=True, space_after=3)
for t in [
    "Persetujuan jadwal dan anggaran sesi uji internal yang disaksikan Pertamina (Termin 1 sertifikasi).",
    "Penunjukan PIC yang mengawal umpan balik iterasi dari GTS dan penyelarasan dossier.",
    "Penegasan penandatangan resmi (authorized signatory) di pihak PT Galaksi untuk formulir aplikasi.",
    "Eskalasi ke Pertamina atas item yang menunggu proses RU IV (vendor, TRA/JSA, klasifikasi area).",
]:
    bullet(t)

# ---------------------------------------------------------------- 8. Lampiran
doc.add_heading("8. Daftar Lampiran", level=1)
table(["No", "Dokumen", "Keterangan"], [
    ["01", "Kurva-S Persiapan Instalasi RU IV Cilacap", "KPI 3 pihak, 40 item persiapan"],
    ["02", "Pembagian Persiapan Instalasi RU IV Cilacap", "Matriks LGU & ITB / Pertamina / Vendor"],
    ["03", "Materi Rapat Koordinasi 29 September 2026", "Slide presentasi rapat dengan Pertamina"],
    ["04", "Laporan Termin 1 Field Testing (20%) Rev02", "Beserta draf BAST (05)"],
    ["06", "Laporan Termin 1 Sertifikasi (40%)", "Status per 15 Sep — diperbarui oleh Bagian 4.2"],
    ["07", "Dokumen Teknis Sertifikasi IECEx/ATEX Rev 1.4", "Dokumen teknis lengkap, bahasa Inggris"],
    ["08–09", "Berkas yang dikirim ke GTS", "Formulir aplikasi & dossier tim"],
    ["10", "Data Pengukuran Temperatur MQ", "Data mentah uji suhu 30 Sep"],
], [0.6, 3.0, 2.9], bold_first=True)

doc.save(OUT)
print("written", OUT)
