# -*- coding: utf-8 -*-
"""Laporan Perkembangan GLD Tahap 2 — Field Testing & Sertifikasi, per 5 November 2026.

Dokumen utama paket `Paket Pertamina/10_Laporan_FieldTesting_dan_Sertifikasi_5November2026/`.
Client-facing (PT Pertamina Patra Niaga), Bahasa Indonesia, format korporat LGU.
Isi merangkum dokumen yang sudah ada di repo (Laporan FAT rev 1.4, Laporan Termin 1 FT rev 0.3,
Laporan Termin 1 Sertifikasi rev 0.2, Dokumen Teknis Sertifikasi rev 3.0, Laporan EMC rev 1.0,
Informasi Enclosure HAC rev 1.4, MoC Pertamina 15769) — tanpa angka uji baru.

Run:  python3 scripts/build_laporan_perkembangan_ft_sertifikasi_nov2026.py
PDF:  python3 scripts/docx_to_pdf_with_toc.py <out.docx>
"""
import os
import sys
import datetime as dt

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import matplotlib.dates as mdates  # noqa: E402

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_persiapan_instalasi_corporate_docx import (  # noqa: E402
    make_doc, set_cell_shading, add_field, add_picture_fit, NAVY, GRAY, WHITE, HEAD_SHADE,
    GREEN, AMBER, RED,
)
import build_spesifikasi_material_instalasi_docx as S  # noqa: E402
from build_spesifikasi_material_instalasi_docx import (  # noqa: E402
    para, bullets, heading, table, fix_widths, banner,
)
from docx.shared import Pt, Inches, RGBColor  # noqa: E402
from docx.enum.text import WD_ALIGN_PARAGRAPH  # noqa: E402

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PKG = os.path.join(REPO, "Paket Pertamina", "10_Laporan_FieldTesting_dan_Sertifikasi_5November2026")
OUT = os.path.join(PKG, "00_Laporan_Perkembangan_GLD_FieldTesting_Sertifikasi_5November2026.docx")
CHART = os.path.join(REPO, "scripts", "assets", "laporan_nov2026", "kurva_s_5nov2026.png")
BLOCK = os.path.join(REPO, "Sumber Dokumen", "Pertamina RU IV 8Okt2026",
                     "block_diagram_scope_final_router_LGU_8Okt2026.png")

DOC_NO = "LGU/GLD/LAP-PERKEMBANGAN/2026-003"
REV = "1.0"
DATE = "5 November 2026"
HEADER = "Laporan Perkembangan GLD Tahap 2 — Field Testing & Sertifikasi"
TODAY = dt.date(2026, 11, 5)
ACTUAL = 63
PLAN_TODAY = 73

S.STATUS_STYLE.update({
    "LULUS (LAB)": (GREEN, "EAF4EC"),
    "Selesai": (GREEN, "EAF4EC"),
    "Memenuhi": (GREEN, "EAF4EC"),
    "Tersedia": (GREEN, "EAF4EC"),
    "Final": (GREEN, "EAF4EC"),
    "Sebagian": (AMBER, "FFF3DC"),
    "Berjalan": (AMBER, "FFF3DC"),
    "Dalam penyiapan": (AMBER, "FFF3DC"),
    "Draf": (AMBER, "FFF3DC"),
    "Usulan": (AMBER, "FFF3DC"),
    "Terbuka": (RED, "FBE6E4"),
    "Perlu konfirmasi": (RED, "FBE6E4"),
    "Menunggu": (GRAY, "EFEFEC"),
    "Belum mulai": (GRAY, "EFEFEC"),
})


# ---------------------------------------------------------------- chart
def build_chart():
    plan = [(dt.date(2026, 6, 1), 0), (dt.date(2026, 6, 30), 8), (dt.date(2026, 7, 30), 21),
            (dt.date(2026, 8, 31), 40), (dt.date(2026, 9, 30), 62), (dt.date(2026, 10, 31), 71),
            (dt.date(2026, 11, 30), 84), (dt.date(2026, 12, 31), 93), (dt.date(2027, 1, 31), 98),
            (dt.date(2027, 2, 28), 100)]
    act = [(dt.date(2026, 6, 1), 0), (dt.date(2026, 6, 12), 6), (dt.date(2026, 6, 30), 16),
           (dt.date(2026, 7, 7), 23), (dt.date(2026, 7, 15), 30), (dt.date(2026, 7, 24), 39),
           (dt.date(2026, 9, 4), 44), (dt.date(2026, 9, 17), 49), (dt.date(2026, 9, 30), 61),
           (TODAY, ACTUAL)]
    plt.rcParams.update({"font.family": "sans-serif",
                         "font.sans-serif": ["Carlito", "Calibri", "Arial", "DejaVu Sans"],
                         "font.size": 10})
    fig, ax = plt.subplots(figsize=(9.2, 4.2), dpi=200)
    ax.plot([d for d, _ in plan], [v for _, v in plan], color="#8A97A6", lw=2, ls=(0, (6, 4)),
            label="Rencana (baseline Kick-Off, 9 bulan)")
    ax.plot([d for d, _ in act], [v for _, v in act], color="#1B2A4A", lw=2.6, marker="o",
            ms=5, label="Aktual (hasil penilaian tim)")
    ax.axvline(TODAY, color="#B23A3A", lw=1.2, ls="--")
    ax.text(TODAY + dt.timedelta(days=3), 6, "5 Nov 2026", color="#B23A3A", fontsize=9,
            fontweight="bold")
    ax.annotate(f"Aktual {ACTUAL}%", xy=(TODAY, ACTUAL), xytext=(10, -16),
                textcoords="offset points", fontsize=9.5, fontweight="bold", color="#1B2A4A")
    ax.annotate(f"Rencana {PLAN_TODAY}%", xy=(TODAY, PLAN_TODAY), xytext=(-92, 8),
                textcoords="offset points", fontsize=9.5, fontweight="bold", color="#5B5B5B")
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


def kpi_row(doc, items):
    t = doc.add_table(rows=1, cols=len(items))
    t.style = "Table Grid"
    for i, (lab, val, sub, color) in enumerate(items):
        c = t.rows[0].cells[i]
        set_cell_shading(c, "F5F5F3")
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(lab + "\n"); r.font.size = Pt(7.8); r.font.bold = True; r.font.color.rgb = GRAY
        r = p.add_run(val + "\n"); r.font.size = Pt(17); r.font.bold = True; r.font.color.rgb = color
        r = p.add_run(sub); r.font.size = Pt(7.6); r.font.color.rgb = GRAY
    fix_widths(t, [6.9 / len(items)] * len(items))
    doc.add_paragraph().paragraph_format.space_after = Pt(4)


def caption(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(8)
    r = p.add_run(text); r.font.size = Pt(8.8); r.font.italic = True; r.font.color.rgb = GRAY


# ---------------------------------------------------------------- build
def build():
    build_chart()
    doc, sec = make_doc()

    # letterhead
    lt = doc.add_table(rows=1, cols=1)
    lc = lt.rows[0].cells[0]
    fix_widths(lt, [6.9])
    set_cell_shading(lc, "1B2A4A")
    lc.paragraphs[0].paragraph_format.space_after = Pt(2)
    lr = lc.paragraphs[0].add_run("PT LAPI GANESHA UTAMA")
    lr.font.bold = True; lr.font.size = Pt(14); lr.font.color.rgb = WHITE
    lp2 = lc.add_paragraph()
    lp2.paragraph_format.space_after = Pt(3)
    lr2 = lp2.add_run("Bekerja sama dengan Lab IoT & Fisika Institut Teknologi Bandung")
    lr2.font.size = Pt(9.5); lr2.font.color.rgb = RGBColor(0xC7, 0xD2, 0xE0)
    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    title = doc.add_heading(level=0)
    tr = title.add_run("Laporan Perkembangan Gas Leak Detection (GLD) Tahap 2 — "
                       "Field Testing dan Sertifikasi")
    tr.font.size = Pt(18); tr.font.bold = True; tr.font.color.rgb = NAVY
    para(doc, "Status kedua jalur kerja per 5 November 2026: hasil uji, persiapan instalasi di "
         "area SRU RU IV Cilacap, status pengajuan sertifikasi ATEX/IECEx, kelengkapan dokumen "
         "Termin 1, serta tindak lanjut yang diperlukan dari masing-masing pihak.",
         size=10.6, color=GRAY, after=10)

    p_ = doc.add_paragraph()
    r = p_.add_run("Kontrol Dokumen")
    r.font.bold = True; r.font.size = Pt(11); r.font.color.rgb = NAVY
    mt = doc.add_table(rows=0, cols=2)
    mt.style = "Table Grid"
    for k, v in [
        ("Nomor dokumen", DOC_NO), ("Revisi", REV), ("Tanggal", DATE),
        ("Periode pelaporan", "30 September – 5 November 2026 (lanjutan laporan perkembangan "
                              "17 September 2026 dan materi rapat 29 September 2026)"),
        ("Status", "Laporan perkembangan untuk informasi dan evaluasi PT Pertamina Patra Niaga"),
        ("Disiapkan oleh", "PT LAPI Ganesha Utama, bersama Lab IoT & Fisika Institut Teknologi Bandung"),
        ("Ditujukan kepada", "PT Pertamina Patra Niaga — tim proyek GLD Tahap 2 dan RU IV Cilacap"),
    ]:
        row = mt.add_row().cells
        set_cell_shading(row[0], HEAD_SHADE)
        row[0].paragraphs[0].paragraph_format.space_after = Pt(2)
        r0 = row[0].paragraphs[0].add_run(k)
        r0.font.bold = True; r0.font.size = Pt(9.3); r0.font.color.rgb = GRAY
        row[1].paragraphs[0].paragraph_format.space_after = Pt(2)
        r1 = row[1].paragraphs[0].add_run(v)
        r1.font.size = Pt(9.6)
    fix_widths(mt, [1.9, 5.0])
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

    # header/footer
    hp = sec.header.paragraphs[0]
    hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    hr = hp.add_run(HEADER + "  |  PT LAPI Ganesha Utama")
    hr.font.size = Pt(8); hr.font.color.rgb = GRAY; hr.font.italic = True
    fp = sec.footer.paragraphs[0]
    fp.add_run(f"{DOC_NO}  ·  Rev. {REV}  ·  {DATE}")
    fp.paragraph_format.tab_stops.add_tab_stop(Inches(6.9), alignment=2)
    fp.add_run("\t")
    add_field(fp, "PAGE", "1")
    fp.add_run(" dari ")
    add_field(fp, "NUMPAGES", "1")
    for r in fp.runs:
        r.font.size = Pt(8); r.font.color.rgb = GRAY

    # ------------------------------------------------ ringkasan
    heading(doc, "Ringkasan")
    kpi_row(doc, [
        ("PROGRES PROGRAM", f"{ACTUAL}%", f"rencana {PLAN_TODAY}% · 5 Nov 2026", NAVY),
        ("HASIL FAT (LAB)", "7/7", "item uji lulus di laboratorium", GREEN),
        ("DOKUMEN SERTIFIKASI", "≈52%", "kelengkapan 21 butir dokumen teknis", AMBER),
        ("INSTALASI SRU", "MoC", "No. 15769 diterima 3 Nov 2026", AMBER),
    ])
    bullets(doc, [
        "**Field testing — pengujian laboratorium tuntas.** Laporan Factory Acceptance Test (FAT) "
        "mencatat 7 dari 7 item uji lulus di laboratorium (akuisisi 8 sensor, AI di perangkat, LoRa, "
        "mesh dan failover Cluster Head, integrasi end-to-end, push alarm, dashboard), didukung tiga "
        "Laporan Uji Laboratorium formal. Laporan FAT telah menjadi Lampiran A Laporan Termin 1 Field "
        "Testing (rev 0.3).",
        "**Instalasi RU IV — lingkup kini mengacu MoC No. 15769/RU IV** (area SRU, relokasi dari OM60). "
        "MoC menyimpulkan infrastruktur pendukung (mounting, jalur kabel, junction box, server, "
        "jaringan) dapat disiapkan lebih dulu, sedangkan pemasangan unit GLD menunggu sertifikat Ex, "
        "karena keempat titik GLD berada di area Class I, Groups C/D, Div. 2 menurut HAC SRU.",
        "**Persiapan dari sisi LGU selesai.** Spesifikasi material, daftar perangkat, pembagian "
        "persiapan, daftar persiapan pelaksana, dan skema jaringan (block diagram final 8 Okt 2026) "
        "telah diserahkan; pekerjaan LGU berikutnya (supervisi/QA, terminasi dan energize, aplikasi "
        "server, commissioning) dilakukan saat instalasi di lokasi berlangsung.",
        "**Sertifikasi — berkas dan sampel sudah di agen sertifikasi.** Formulir aplikasi dan dossier "
        "teknis diajukan ke GTS (Shanghai Global Testing Services, agen sertifikasi) sekitar "
        "29 Sep 2026 dengan skema usulan **II 2G Ex db IIC T4 Gb**; sampel GLD2-0x1001 disiapkan untuk "
        "dibawa langsung ke GTS bersama surat pengantar 12 Okt 2026. Dokumen teknis kini rev 3.0 "
        "(156 halaman) mengikuti panduan revisi; data pendukung baru: pengukuran suhu internal dan "
        "pra-uji EMC di Telkom Test House.",
        "**Skema usulan melampaui batas minimum MoC.** MoC mensyaratkan Ex minimal setara Zone 2, "
        "Group IIB, T3; skema yang diajukan adalah Zone 1 (EPL Gb), Group IIC, T4 — klasifikasi akhir "
        "tetap ditentukan lembaga sertifikasi.",
    ])

    # ------------------------------------------------ 1
    heading(doc, "1. Jalur Field Testing")
    heading(doc, "1.1 Kurva-S program", level=2)
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    add_picture_fit(p, CHART, 6.8, 3.3)
    caption(doc, "Gambar 1. Kurva-S program GLD Tahap 2 — rencana (baseline Deck Kick-Off 9 bulan) "
                 "dan aktual hasil penilaian tim per 5 November 2026.")
    para(doc, "Progres dihitung sebagai rata-rata 12 aktivitas jadwal (metodologi sama dengan "
         "laporan sebelumnya). Dua aktivitas dinilai naik sejak 30 September 2026 berdasarkan bukti "
         "yang kini tersedia:")
    table(doc, ["No", "Aktivitas", "30 Sep", "5 Nov", "Dasar penilaian / keterangan"], [
        ["1", "Kick-off & konfirmasi kebutuhan", "100%", "100%", "Selesai"],
        ["2", "Site survey & rencana pengumpulan data", "90%", "100%",
         "Titik final perangkat ditetapkan dalam MoC 15769 dan diverifikasi terhadap HAC SRU"],
        ["3", "Detailed design", "100%", "100%", "Selesai"],
        ["4", "Prototype build", "100%", "100%", "Unit GLD V2 terakit; sampel sertifikasi GLD2-0x1001"],
        ["5", "Lab test", "72%", "90%",
         "Laporan FAT 7/7, tiga Laporan Uji Lab, uji suhu internal, pra-uji EMC 15 Okt; "
         "sisa: uji stabilitas jangka panjang dan kapasitas"],
        ["6", "AI model training / validation", "85%", "85%",
         "Model di perangkat tervalidasi lab; pelatihan gas tambahan per lokasi menyusul"],
        ["7", "Integration test (fungsional)", "80%", "80%",
         "End-to-end lab tuntas; integrasi di jaringan lokasi menyusul instalasi"],
        ["8", "HSE review & permit preparation (sisi LGU)", "100%", "100%",
         "Bahan dari sisi LGU lengkap; penerbitan izin oleh RU IV"],
        ["9", "Field installation", "0%", "0%", "Mengikuti MoC 15769 (lihat 1.3)"],
        ["10", "Field trial", "0%", "0%", "Setelah instalasi"],
        ["11", "Evaluation & final report", "0%", "0%", "Jan 2027"],
        ["12", "Industrialization roadmap", "5%", "5%", "Feb 2027"],
        ["", "Rata-rata (progres program)", "61%", f"{ACTUAL}%", f"Rencana per 5 Nov ≈ {PLAN_TODAY}%"],
    ], [0.35, 2.05, 0.6, 0.6, 3.3])
    para(doc, f"Selisih terhadap rencana (≈{PLAN_TODAY - ACTUAL} poin) berasal dari sisa uji lab/"
         "integrasi jangka panjang dan dari jadwal instalasi lapangan, yang menurut MoC 15769 kini "
         "mengikuti penerbitan sertifikat Ex untuk titik GLD. Angka progres adalah estimasi tim "
         "berdasarkan status aktivitas, bukan hasil audit resmi.", size=9.6, color=GRAY)

    heading(doc, "1.2 Hasil Factory Acceptance Test (laboratorium)", level=2)
    table(doc, ["No", "Item uji", "Hasil utama", "Status"], [
        ["FAT-01", "Akuisisi 8 sensor gas dan perekaman data",
         "8/8 sensor terbaca; dataset 1.870 pembacaan unik", "LULUS (LAB)"],
        ["FAT-02", "Klasifikasi gas oleh AI di dalam perangkat",
         "AI berjalan di perangkat; uji real-time 97,65%; validasi model 99,73% (INT8 99,20%)",
         "LULUS (LAB)"],
        ["FAT-03", "Komunikasi radio LoRa GLD ke Cluster Head",
         "PDR 100% pada 177 m dan 243 m jalur pandang bebas", "LULUS (LAB)"],
        ["FAT-04", "Mesh multi-hop dan failover Cluster Head",
         "Mesh 8 CH, 3 lapis; failover tanpa kehilangan data; downlink berhasil", "LULUS (LAB)"],
        ["FAT-05", "Integrasi end-to-end GLD – CH – Gateway – Server",
         "Data mengalir end-to-end", "LULUS (LAB)"],
        ["FAT-06", "Alarm otomatis (push alarm)",
         "Alarm otomatis di server saat GLD disemprot LPG, tanpa permintaan data", "LULUS (LAB)"],
        ["FAT-07", "Monitoring data dan alarm di dashboard",
         "Data dan alarm tampil di dashboard laboratorium", "LULUS (LAB)"],
    ], [0.7, 2.0, 3.15, 1.05], status_col=3)
    para(doc, "Rincian prosedur, kriteria lulus, dan bukti tiap item ada di Laporan FAT (Lampiran A "
         "dokumen 01-01). Pengujian di lokasi (SAT), termasuk waktu respons alarm terukur, dilakukan "
         "setelah instalasi.", size=9.6, color=GRAY)

    heading(doc, "1.3 Persiapan instalasi di area SRU RU IV Cilacap", level=2)
    para(doc, "Kronologi sejak rapat koordinasi 29 September 2026:")
    table(doc, ["Tanggal", "Kegiatan / dokumen"], [
        ["29 Sep", "Rapat koordinasi instalasi LGU – Pertamina (tindak lanjut site survey)"],
        ["1–2 Okt", "Spesifikasi Material Instalasi (rev 1.5), Daftar Perangkat (rev 1.2), Pembagian "
                    "Persiapan (rev 1.5), Daftar Persiapan Pelaksana (rev 1.2) diserahkan; rapat teknis "
                    "pemasangan 2 Okt"],
        ["8 Okt", "Block diagram lingkup RU IV versi final, termasuk router Wi-Fi LGU (Gambar 2)"],
        ["21 Okt", "Kebutuhan field testing dan spesifikasi PC server diteruskan Pertamina ke setiap RU"],
        ["30 Okt – 2 Nov", "Hasil verifikasi lokasi terhadap HAC SRU; LGU menyampaikan dokumen "
                           "Informasi Enclosure & Status Proteksi Ledakan GLD (rev 1.4)"],
        ["3 Nov", "MoC No. 15769/RU IV — Field Test Multi-Modality Gas Leak Detector System, area SRU"],
    ], [1.2, 5.7])
    if os.path.exists(BLOCK):
        p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        add_picture_fit(p, BLOCK, 6.4, 3.6)
        caption(doc, "Gambar 2. Block diagram lingkup RU IV (versi final 8 Oktober 2026): GLD – CH via "
                     "LoRa; Gateway – router Wi-Fi LGU – server lokal via LAN.")
    para(doc, "**Ringkasan MoC 15769 dan hasil verifikasi HAC SRU:**")
    table(doc, ["Perangkat", "Lokasi", "Klasifikasi (HAC, indikatif)", "Status"], [
        ["GLD-01 s.d. GLD-04", "Area proses SRU, tiang 2\" HDG baru", "Class I, Groups C/D, Div. 2",
         "Menunggu"],
        ["JB-01", "Pipe support PS27", "Class I, Groups C/D, Div. 2", "Memenuhi"],
        ["CH-01 s.d. CH-05", "Pagar pembatas SRU", "Unclassified", "Memenuhi"],
        ["Gateway + server", "Control Room / Control Building SRU", "Unclassified", "Memenuhi"],
    ], [1.45, 2.35, 1.95, 1.15], status_col=3)
    para(doc, "Status \"Memenuhi\" mengikuti hasil verifikasi HAC; "
         "\"Menunggu\" berarti pemasangan unit GLD menunggu sertifikat Ex (minimal setara Zone 2, "
         "Group IIB, T3) atau relokasi ke area unclassified, sesuai kesimpulan MoC. Sistem dijalankan "
         "secara standalone dan advisory (tidak terhubung F&G/DCS) selama field test.",
         size=9.6, color=GRAY)

    para(doc, "**Status pekerjaan per pihak:**")
    table(doc, ["Pihak", "Lingkup", "Status"], [
        ["LGU & ITB", "Spesifikasi, daftar perangkat, pembagian persiapan, skema jaringan, unit "
                      "GLD/CH/Gateway, bracket panel surya CH, router Wi-Fi", "Selesai"],
        ["LGU & ITB", "Supervisi/QA pemasangan, terminasi dan energize 24 VDC, instalasi aplikasi "
                      "server, commissioning, berita acara", "Menunggu"],
        ["Pertamina RU IV", "Infrastruktur pendukung sesuai MoC: tiang/mounting, JB-01, kabel 24 VDC "
                            "armored, PSU, server + UPS, jaringan, izin kerja", "Berjalan"],
        ["Pelaksana instalasi", "Fabrikasi dan pemasangan fisik, termasuk HSE ketinggian",
         "Belum mulai"],
    ], [1.4, 4.35, 1.15], status_col=2)

    para(doc, "**Butir yang perlu diselaraskan antara MoC dan dokumen LGU:** MoC merupakan acuan "
         "lapangan; dokumen LGU akan disesuaikan setelah butir berikut dikonfirmasi.")
    table(doc, ["No", "Butir", "MoC 15769", "Dokumen LGU / data lain", "Status"], [
        ["1", "Jumlah unit area SRU", "4 GLD, 5 CH, 1 Gateway",
         "Spesifikasi Material: 3 GLD, 6 CH (perencanaan); tabel alokasi per RU (3 Nov): 3 GLD, 2 CH",
         "Perlu konfirmasi"],
        ["2", "Tinggi pemasangan GLD", "± 1,5 m",
         "Rekomendasi LGU: sensor ± 0,5 m dari tanah untuk gas lebih berat dari udara (LPG, H2S)",
         "Perlu konfirmasi"],
        ["3", "Skema catu daya 24 VDC", "PSU di Control Room, kabel armored 14 AWG via JB-01",
         "Dokumen LGU: opsi PSU per lokasi; kebutuhan 24 VDC ≥ 1 A per GLD terpenuhi skema MoC",
         "Berjalan"],
        ["4", "Database server", "MySQL", "Aplikasi saat ini memakai SQLite; disesuaikan bila diperlukan",
         "Berjalan"],
        ["5", "Angka akurasi model AI", "99,31% (validasi lab)",
         "Laporan FAT: 99,73% (model) / 99,20% (INT8 di perangkat) / 97,65% (real-time)",
         "Berjalan"],
    ], [0.35, 1.3, 1.6, 2.6, 1.05], status_col=4)

    heading(doc, "1.4 Termin 1 Field Testing (20%)", level=2)
    para(doc, "Dokumen Termin 1 Field Testing lengkap: Laporan Pemenuhan Deliverable rev 0.3 "
         "(5 Oktober 2026) dengan Laporan FAT beserta bukti uji sebagai Lampiran A, dan draf Berita "
         "Acara Serah Terima. Penilaian pemenuhan dan keputusan pembayaran merupakan evaluasi "
         "PT Pertamina Patra Niaga.")

    # ------------------------------------------------ 2
    heading(doc, "2. Jalur Sertifikasi ATEX/IECEx")
    heading(doc, "2.1 Status pengajuan", level=2)
    table(doc, ["Aspek", "Status"], [
        ["Objek sertifikasi", "Node Sensor GLD V2 (Cluster Head dan Gateway dipasang di area "
                              "unclassified, di luar objek sertifikasi)"],
        ["Pemohon / produsen", "PT Galaksi Megatama Indonesia (mitra produksi casing)"],
        ["Agen sertifikasi", "GTS — Shanghai Global Testing Services Co., Ltd.; meneruskan ke lembaga "
                             "sertifikasi dan laboratorium terakreditasi"],
        ["Skema yang diajukan", "II 2G Ex db IIC T4 Gb — Zona 1, grup gas IIC, kelas suhu T4, metode "
                                "proteksi flameproof (Ex d); suhu lingkungan −20 °C s.d. +60 °C; IP66 (target)"],
        ["Berkas", "Formulir aplikasi dan dossier teknis diajukan sekitar 29 September 2026"],
        ["Sampel", "GLD2-0x1001, disiapkan untuk dibawa langsung ke GTS (surat pengantar dan surat "
                   "keterangan Bea Cukai 12 Oktober 2026)"],
        ["Tahap berikutnya", "Iterasi dokumen atas masukan GTS, lalu pengujian di laboratorium "
                             "terakreditasi"],
    ], [1.7, 5.2])
    para(doc, "Perbandingan dengan syarat MoC: Zona 1 (EPL Gb) mencakup penggunaan di Zona 2; grup "
         "IIC mencakup IIB; kelas suhu T4 (≤ 135 °C) lebih ketat dari T3 (≤ 200 °C). Bila sertifikat "
         "terbit sesuai skema usulan, syarat minimum MoC terpenuhi. HAC SRU memakai sistem Class/"
         "Division; kesetaraannya dengan sistem zona perlu dikonfirmasi HSE RU IV.", size=9.6)

    heading(doc, "2.2 Kelengkapan dokumen teknis sertifikasi", level=2)
    para(doc, "Dokumen Teknis Sertifikasi (rev 3.0, 9 Oktober 2026, bahasa Inggris) disusun mengikuti "
         "daftar persyaratan informasi IECEx/ATEX dan panduan revisi. Status per butir:")
    table(doc, ["Butir", "Persyaratan", "Status", "Keterangan"], [
        ["1.1–1.2", "Formulir aplikasi; legalitas usaha", "Final", "PT Galaksi Megatama Indonesia"],
        ["1.3–1.4", "Organisasi & kontak; alamat & fasilitas produksi", "Sebagian",
         "Fungsi QA/produksi dan perakit PCB dilengkapi"],
        ["1.5", "ISO 9001", "Terbuka", "Audit direncanakan Oktober 2026"],
        ["2.1–2.3", "Deskripsi produk, spesifikasi, parameter teknis", "Final", ""],
        ["2.4", "Foto produk (12 pandangan)", "Sebagian", "10 dari 12 lengkap"],
        ["2.5", "Lingkungan penggunaan (IIC, T4, Zona 1, −20…+60 °C)", "Final", "Klasifikasi usulan"],
        ["6(a)", "Gambar teknik, skematik, layout PCB, terminal/grounding", "Sebagian",
         "Gambar terkendali bertoleransi; skematik modul sensor"],
        ["6.b", "Daftar komponen kritis Ex", "Sebagian", ""],
        ["6.c", "Material non-logam", "Terbuka", "Datasheet pemasok"],
        ["6.d", "Proses manufaktur", "Sebagian", "Parameter proses dikonfirmasi"],
        ["6.e", "Sumber penyulutan & konsep proteksi", "Sebagian", "17 sumber penyulutan teridentifikasi"],
        ["6.f", "Kelas suhu", "Sebagian", "Pengukuran internal; titik ukur tambahan"],
        ["6.g", "Instruksi penggunaan & instalasi", "Draf", ""],
        ["6.h", "Nameplate", "Usulan", "Artwork usulan, hanya gas"],
        ["6.i", "Sertifikat komponen Ex", "Terbuka", "Sertifikat housing & cable gland Ex"],
        ["3", "Sampel dan perlengkapan uji", "Sebagian", "Sampel teridentifikasi"],
    ], [0.75, 2.6, 0.95, 2.6], status_col=2)
    para(doc, "Dihitung dengan bobot Final 100% / Sebagian 50% / Terbuka 0% atas 21 butir matriks "
         "panduan revisi (4 Final, 14 Sebagian/Draf/Usulan, 3 Terbuka), kelengkapan dokumen ≈ 52% "
         "(30 Sep 2026: ≈ 43%). Angka ini mengukur kelengkapan dokumen, bukan kemajuan menuju "
         "terbitnya sertifikat.", size=9.6, color=GRAY)

    heading(doc, "2.3 Data uji pendukung", level=2)
    table(doc, ["Aspek", "Hasil", "Sifat data"], [
        ["Suhu internal (kelas suhu T4)",
         "Titik terpanas ≈ 114 °C (ekstrapolasi ke +60 °C, termasuk kipas mati) terhadap batas efektif "
         "T4 130 °C; permukaan luar ≈ 79 °C", "Uji internal, 8 thermocouple, 180 menit"],
        ["EMC — emisi (EN 55032 Class A)",
         "212 dari 216 titik ukur di bawah batas; 4 titik di atas batas berada pada frekuensi kerja "
         "LoRa 920 MHz (sinyal pancar perangkat); margin tipis GLD di 117–127 MHz",
         "Pra-uji Telkom Test House, 15 Okt 2026"],
        ["Enclosure",
         "Housing komersial HIREP HRP-T1000-A, aluminium die-cast (rating pabrikan Ex d IIC T6 Gb, "
         "IP66); kaca depan diganti mesh stainless steel sehingga rating housing tidak otomatis "
         "berlaku untuk GLD", "Spesifikasi pabrikan; salinan sertifikat diminta ke pabrikan"],
        ["Catu daya", "Hanya 24 VDC di dalam unit; konsumsi maks. terukur 7,995 W (≈ 0,33 A)",
         "Uji lab LGU"],
    ], [1.6, 3.65, 1.65])
    para(doc, "Seluruh data di atas adalah data pendukung internal/pra-uji dan tidak menggantikan "
         "pengujian oleh laboratorium terakreditasi.", size=9.6, color=GRAY)

    heading(doc, "2.4 Termin 1 Sertifikasi (40%)", level=2)
    para(doc, "Status bukti pemenuhan tujuh syarat Termin 1 sertifikasi (Laporan Pemenuhan "
         "Deliverable rev 0.2):")
    table(doc, ["No", "Syarat", "Status", "Ringkasan bukti"], [
        ["1", "Prototipe enclosure GLD tersedia", "Sebagian",
         "Unit terakit dan terfoto; nomor seri sampel GLD2-0x1001"],
        ["2", "Prototipe telah diuji", "Sebagian",
         "Uji termal internal 30 Sep; pra-uji EMC 15 Okt; uji mekanik/sealing/fault disiapkan"],
        ["3", "Iterasi perbaikan desain berbasis hasil uji", "Sebagian",
         "PCB V1–V5 dengan catatan perubahan; casing v2 → v3; posisi antena dipindah ke atas"],
        ["4", "Disaksikan dan divalidasi Pertamina", "Dalam penyiapan",
         "Sesi witness uji internal dijadwalkan bersama Pertamina"],
        ["5", "Sebelum uji laboratorium terakreditasi", "Tersedia",
         "Pengajuan ke agen GTS; uji laboratorium dilakukan sesudahnya"],
        ["6", "Berita acara", "Dalam penyiapan", "Disusun setelah sesi witness"],
        ["7", "Laporan pekerjaan Termin 1", "Tersedia", "Laporan Pemenuhan Deliverable rev 0.2"],
    ], [0.35, 2.15, 1.15, 3.25], status_col=2)
    para(doc, "Penilaian pemenuhan dan keputusan pembayaran merupakan evaluasi PT Pertamina Patra Niaga.",
         size=9.6, color=GRAY)

    # ------------------------------------------------ 3
    heading(doc, "3. Tindak lanjut")
    table(doc, ["No", "Tindak lanjut", "Pihak"], [
        ["1", "Konfirmasi jumlah unit dan titik final area SRU (butir 1.3 no. 1–2)",
         "Pertamina RU IV + LGU"],
        ["2", "Penyiapan infrastruktur pendukung sesuai MoC (mounting, JB-01, kabel, PSU, server, "
              "jaringan) dan penunjukan pelaksana instalasi", "Pertamina RU IV"],
        ["3", "Keputusan jadwal pemasangan GLD: menunggu sertifikat Ex atau relokasi titik ke area "
              "unclassified (sesuai MoC)", "Pertamina RU IV"],
        ["4", "Penyesuaian Spesifikasi Material dan Daftar Perangkat LGU terhadap MoC 15769",
         "LGU"],
        ["5", "Revisi dossier mengikuti iterasi dari GTS; salinan sertifikat housing dari pabrikan",
         "LGU + PT Galaksi"],
        ["6", "Penjadwalan sesi witness uji internal prototipe (Termin 1 sertifikasi syarat 4 & 6)",
         "LGU + Pertamina"],
        ["7", "Pelengkap uji pendukung: titik ukur suhu tambahan, uji imunitas EMC, verifikasi daya "
              "pancar radio terhadap regulasi SDPPI, pra-uji IP", "LGU"],
        ["8", "Evaluasi dokumen Termin 1 Field Testing dan Termin 1 Sertifikasi", "Pertamina"],
    ], [0.35, 4.95, 1.6])

    # ------------------------------------------------ 4
    heading(doc, "4. Daftar dokumen dalam paket")
    table(doc, ["Kode", "Dokumen", "Revisi / tanggal"], [
        ["00", "Laporan Perkembangan GLD — Field Testing & Sertifikasi (dokumen ini)", "1.0 · 5 Nov 2026"],
        ["01-01", "Laporan Pemenuhan Deliverable Termin 1 Field Testing (20%), dengan Lampiran A "
                  "Laporan FAT + bukti uji + 3 Laporan Uji Lab", "0.3 · 5 Okt 2026"],
        ["01-02", "Draf Berita Acara Serah Terima Termin 1 Field Testing", "Draf"],
        ["01-03", "Spesifikasi Material & Kebutuhan Instalasi GLD RU IV", "1.5 · 2 Okt 2026"],
        ["01-04", "Daftar Perangkat dan Kebutuhan Pemasangan GLD RU IV", "1.2 · 2 Okt 2026"],
        ["01-05", "Pembagian Persiapan Instalasi RU IV", "1.5"],
        ["01-06", "Daftar Persiapan Pelaksana Instalasi RU IV", "1.2"],
        ["01-07", "Block diagram lingkup RU IV (final, dengan router LGU)", "8 Okt 2026"],
        ["01-08", "Informasi Enclosure & Status Proteksi Ledakan GLD (tanggapan HAC SRU)", "1.4 · 2 Nov 2026"],
        ["01-09", "Technical Datasheet Lab IoT ITB (5 dokumen, ID)", "Rev 4.0"],
        ["02-01", "Laporan Pemenuhan Deliverable Termin 1 Sertifikasi (40%)", "0.2 · 2 Okt 2026"],
        ["02-02", "IECEx/ATEX Certification Document — GLD V2 (bahasa Inggris)", "3.0 · 9 Okt 2026"],
        ["02-03", "Laporan Teknis Pengujian EMC GLD & Cluster Head (pra-uji)", "1.0 · 28 Okt 2026"],
        ["02-04", "Data pengukuran temperatur sensor MQ (uji internal)", "30 Sep 2026"],
        ["02-05", "Formulir aplikasi ATEX yang diajukan ke GTS", "29 Sep 2026"],
    ], [0.65, 4.65, 1.6])

    para(doc, "Bandung, 5 November 2026", after=2)
    para(doc, "PT LAPI Ganesha Utama", bold=True, after=2)
    os.makedirs(PKG, exist_ok=True)
    doc.save(OUT)
    print("saved", OUT)


if __name__ == "__main__":
    build()
