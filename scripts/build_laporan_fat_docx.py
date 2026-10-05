# -*- coding: utf-8 -*-
"""Build "Laporan Factory Acceptance Test (FAT) — Sistem GLD Tahap 2" (corporate .docx).

Merangkum bukti FAT yang sudah ada (uji lab Mei–Agustus 2026, witness Pertamina
6 Agustus 2026) ke format baku per item uji: tujuan, prosedur, kriteria lulus,
hasil, bukti. Tidak ada angka baru — semua nilai dikutip dari bukti di
Paket Pertamina/03_Pengajuan_Termin_1_FieldTesting_20Persen_Rev02/ dan memory.

Run:  python3 scripts/build_laporan_fat_docx.py
PDF:  python3 scripts/docx_to_pdf_with_toc.py Deliverables/Laporan_FAT_GLD_Tahap2.docx
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_spesifikasi_material_instalasi_docx import (  # noqa: E402
    make_doc, set_cell_shading, add_field, fix_widths, para, bullets, heading,
    table, banner, NAVY, GRAY, WHITE, HEAD_SHADE,
)
from docx.shared import Pt, Inches, RGBColor  # noqa: E402
from docx.enum.text import WD_ALIGN_PARAGRAPH  # noqa: E402

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(REPO, "Deliverables", "Laporan_FAT_GLD_Tahap2.docx")

DOC_NO = "LGU/GLD/FAT/2026-001"
REV = "1.4"
DATE = "5 Oktober 2026"
HEADER = "Laporan Factory Acceptance Test — Sistem GLD Tahap 2"

LULUS = "LULUS (LAB)"
SEBAGIAN = "SEBAGIAN"
BELUM = "BELUM DIUJI"

# status warna untuk helper table()
import build_spesifikasi_material_instalasi_docx as _b  # noqa: E402
from build_persiapan_instalasi_corporate_docx import GREEN, AMBER, RED  # noqa: E402
_b.STATUS_STYLE.update({
    LULUS: (GREEN, "EAF4EC"),
    SEBAGIAN: (AMBER, "FFF3DC"),
    BELUM: (RED, "FBE6E4"),
})

FAT_ITEMS = [
    dict(
        no="FAT-01", judul="Akuisisi 8 sensor gas dan perekaman data",
        tujuan="Memastikan kedelapan sensor MQ pada node GLD terbaca valid dan datanya dapat direkam.",
        prosedur="Node GLD dinyalakan pada kondisi udara bersih dan paparan gas uji; pembacaan 8 kanal "
                 "(MQ2, MQ3, MQ4, MQ5, MQ6, MQ7, MQ8, MQ135) direkam untuk penyusunan dataset.",
        kriteria="8 dari 8 kanal sensor menghasilkan pembacaan valid dan konsisten; data tersimpan.",
        hasil="8 dari 8 kanal terbaca valid. Dataset pengembangan 1.870 pembacaan unik dari 8 sensor berhasil "
              "disusun pada 3 kondisi (LPG, CO₂, udara bersih), dibagi 80% latih / 20% uji.",
        bukti="Presentasi hasil model CNN Dual-Branch (slide 4: data yang digunakan); dataset Lab IoT ITB.",
        status=LULUS),
    dict(
        no="FAT-02", judul="Klasifikasi gas oleh AI di dalam perangkat (on-device)",
        tujuan="Memastikan model AI berjalan langsung di ESP32-S3 dan mengklasifikasikan kondisi gas dengan akurat.",
        prosedur="(a) Validasi model pada dataset pengembangan: model dilatih dan diuji pada data yang belum pernah "
                 "dilihat, lalu dikuantisasi INT8 agar muat di ESP32-S3. (b) Uji real-time di perangkat: model "
                 "ditanam di firmware dan dijalankan di board ESP32-S3 (device 1001) terhadap gas sebenarnya.",
        kriteria="Model berjalan di ESP32-S3 tanpa server dan menghasilkan klasifikasi benar pada uji real-time "
                 "(KPI proposal: Classification Accuracy).",
        hasil="(a) Dataset pengembangan (LPG, CO₂, udara bersih): akurasi data uji 99,73% (374 data, F1 rata-rata "
              "99,56%); setelah kuantisasi INT8 (9,14 KB) 99,20%. (b) Konfigurasi model di perangkat sesuai "
              "Technical Datasheet Rev 4.0 (4 September 2026): label Clean Air, LPG, dan H2 beserta nilai "
              "confidence. Uji real-time di perangkat ±11,7 menit nonstop, 1.176 pembacaan, akurasi 97,65% "
              "(H2 presisi 98,4%; udara bersih 96,9%). Deteksi LPG di perangkat dibuktikan pada FAT-06.",
        bukti="Presentasi hasil model CNN Dual-Branch (slide 8–10); Technical Datasheet Rev 4.0 Gas Leak Detector "
              "(bagian 4.1, keluaran klasifikasi); Laporan Uji Laboratorium 01.",
        status=LULUS),
    dict(
        no="FAT-03", judul="Komunikasi radio LoRa GLD ke Cluster Head",
        tujuan="Memastikan data GLD terkirim ke Cluster Head (CH) pada jarak dan kondisi lingkungan nyata.",
        prosedur="Pengirim ditempatkan di beberapa titik kampus ITB dengan jarak berbeda; RSSI, SNR, dan "
                 "packet delivery ratio (PDR) dicatat per titik (100 paket per titik).",
        kriteria="PDR 100% pada link jalur pandang bebas antar-hop, dan batas jangkauan per hop teridentifikasi "
                 "sebagai dasar penempatan GLD dan CH.",
        hasil="PDR 100% pada link jalur pandang bebas 177 m (depan LFT) dan 243 m (Gerbang Utara). Batas "
              "jangkauan teridentifikasi: PDR 87% pada 201 m terhalang gedung (STEI Lt.2); link putus di atas "
              "±340 m atau saat terhalang berat. Jarak antar-hop di lokasi ditetapkan di bawah batas ini dan "
              "jangkauan diperluas dengan jaringan mesh multi-hop (FAT-04).",
        bukti="Lembar kerja uji sinyal LoRa (Test Sinyal LoRa.xlsx).",
        status=LULUS),
    dict(
        no="FAT-04", judul="Jaringan mesh multi-hop dan failover Cluster Head",
        tujuan="Memastikan CH dapat saling meneruskan data (multi-hop) dan jaringan pulih saat satu CH mati.",
        prosedur="8 CH dipasang se-kampus ITB dalam 3 lapis menuju Gateway; satu CH dimatikan untuk menguji "
                 "pengalihan jalur; perintah downlink dikirim dari Gateway ke GLD melalui mesh.",
        kriteria="Semua CH terhubung ke Gateway; saat satu CH mati, node berpindah jalur tanpa kehilangan data; "
                 "downlink sampai ke GLD.",
        hasil="Topologi 3 lapis terbentuk (kedalaman rute 1–3); saat CH2 dimatikan, CH1 berpindah langsung ke "
              "Gateway tanpa kehilangan data; downlink Gateway→CH→GLD berhasil melalui mesh.",
        bukti="Kutipan catatan uji Lab IoT ITB: uji CH dan failover (Mei 2026), uji mesh 8 CH dan downlink "
              "(16 Juli 2026); Laporan Uji Laboratorium 03.",
        status=LULUS),
    dict(
        no="FAT-05", judul="Integrasi end-to-end GLD – CH – Gateway – Server",
        tujuan="Memastikan data mengalir utuh dari node sensor sampai server.",
        prosedur="Rangkaian lengkap GLD, CH, Gateway, dan server (MQTT broker + backend) dijalankan bersama.",
        kriteria="Data node diterima server melalui seluruh rantai tanpa intervensi manual.",
        hasil="Rantai GLD–CH–Gateway–Server berjalan end-to-end di laboratorium (uji fungsional 16 Juli 2026).",
        bukti="Catatan uji fungsional 16 Juli 2026; Technical Datasheet Rev 4.0 (Whole System, Gateway, Server).",
        status=LULUS),
    dict(
        no="FAT-06", judul="Alarm otomatis (push alarm)",
        tujuan="Memastikan kebocoran gas memicu alarm di server secara otomatis, tanpa menunggu permintaan data.",
        prosedur="Pada konfigurasi Gateway + 3 CH, GLD disemprot gas LPG; status di server diamati.",
        kriteria="Status server berubah menjadi alarm secara otomatis, tanpa permintaan data dari server (push).",
        hasil="Status server berubah menjadi alarm secara otomatis tanpa permintaan data dari server (uji 6–8 "
              "Agustus 2026). Keputusan alarm diambil di node oleh AI di perangkat, lalu dikirim langsung ke "
              "server. Waktu respons tidak diukur dengan pencatat waktu pada uji ini; interval laporan radio "
              "sesuai desain adalah 10 detik (Technical Datasheet Rev 4.0). Waktu respons terhadap KPI proposal "
              "(≤30 detik) diukur pada Site Acceptance Test di lokasi.",
        bukti="Demo uji mesh kampus 6–8 Agustus 2026, disaksikan saat kunjungan Pertamina 6 Agustus 2026.",
        status=LULUS),
    dict(
        no="FAT-07", judul="Monitoring data dan alarm di dashboard",
        tujuan="Memastikan data sensor dan alarm dapat dipantau pada aplikasi.",
        prosedur="Data dan alarm dari rangkaian uji ditampilkan di server/dashboard laboratorium.",
        kriteria="Data dan status alarm tiap node tampil di dashboard.",
        hasil="Data dan status alarm tiap node tampil di dashboard laboratorium. Masukan Pertamina pada rapat "
              "6 Agustus 2026 (kolom Area dan identitas peralatan, tampilan ppm real-time) merupakan penyesuaian "
              "tampilan aplikasi untuk lokasi; tidak termasuk kriteria FAT-07 dan dikerjakan pada konfigurasi "
              "aplikasi di lokasi.",
        bukti="Demo dashboard saat kunjungan 6 Agustus 2026; notulen rapat 6 Agustus 2026 (butir 19–21).",
        status=LULUS),
]


RINGKAS = {
    "FAT-01": "8/8 sensor terbaca; dataset 1.870 pembacaan unik",
    "FAT-02": "AI berjalan di perangkat; uji real-time 97,65%; validasi model 99,73% (INT8 99,20%)",
    "FAT-03": "PDR 100% pada 177 m dan 243 m jalur pandang bebas; batas jangkauan per hop teridentifikasi",
    "FAT-04": "Mesh 8 CH, 3 lapis; failover tanpa kehilangan data; downlink berhasil",
    "FAT-05": "Data mengalir end-to-end GLD–CH–Gateway–Server",
    "FAT-06": "Alarm otomatis di server saat GLD disemprot LPG, tanpa permintaan data",
    "FAT-07": "Data dan alarm tampil di dashboard laboratorium",
}


def build():
    doc, sec = make_doc()

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
    tr = title.add_run("Laporan Factory Acceptance Test (FAT) — Sistem Gas Leak Detection Tahap 2")
    tr.font.size = Pt(18); tr.font.bold = True; tr.font.color.rgb = NAVY
    para(doc, "Hasil uji penerimaan di laboratorium (Lab IoT, Instrumentation and Computations, ITB) atas "
         "node sensor GLD, Cluster Head, Gateway, dan server sebelum perangkat dikirim ke lokasi Refinery "
         "Unit. Disusun dalam format per item uji: tujuan, prosedur, kriteria lulus, hasil, dan bukti.",
         size=10.6, color=GRAY, after=10)

    rows = [
        ("Nomor dokumen", DOC_NO), ("Revisi", REV), ("Tanggal", DATE),
        ("Status", "Untuk pengesahan — hasil uji laboratorium (FAT), bukan Site Acceptance Test (SAT)"),
        ("Lokasi uji", "Lab IoT, Instrumentation and Computations, Gedung Laboratorium Fisika Terpadu, ITB, Bandung"),
        ("Periode uji", "Mei – Agustus 2026; disaksikan PT Pertamina Patra Niaga pada 6 Agustus 2026"),
        ("Disiapkan oleh", "PT LAPI Ganesha Utama, bersama Lab IoT & Fisika Institut Teknologi Bandung"),
        ("Ditujukan kepada", "PT Pertamina Patra Niaga"),
    ]
    p_ = doc.add_paragraph()
    r = p_.add_run("Document Control")
    r.font.bold = True; r.font.size = Pt(11); r.font.color.rgb = NAVY
    mt = doc.add_table(rows=0, cols=2)
    mt.style = "Table Grid"
    for k, v in rows:
        row = mt.add_row().cells
        set_cell_shading(row[0], HEAD_SHADE)
        row[0].paragraphs[0].paragraph_format.space_after = Pt(2)
        r0 = row[0].paragraphs[0].add_run(k)
        r0.font.bold = True; r0.font.size = Pt(9.3); r0.font.color.rgb = GRAY
        row[1].paragraphs[0].paragraph_format.space_after = Pt(2)
        r1 = row[1].paragraphs[0].add_run(v)
        r1.font.size = Pt(9.6)
    fix_widths(mt, [1.9, 5.0])

    header = sec.header
    hp = header.paragraphs[0]
    hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    hr = hp.add_run(HEADER + "  |  Untuk Pengesahan")
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

    # 1
    heading(doc, "1. Dasar dan pengertian")
    bullets(doc, [
        "**Dasar kontraktual.** Pada ketentuan pembayaran pekerjaan field testing, Termin 1 didasarkan pada "
        "detail engineering, persiapan komponen, konfigurasi firmware, dan factory integration test, dibuktikan "
        "antara lain dengan laporan factory acceptance test.",
        "**Dasar proposal.** Proposal GLD Tahap 2 (Kontrak Payung) §14.3 \"Laporan FAT dan SAT\": uji fungsi "
        "sensor dan komunikasi, verifikasi akurasi klasifikasi AI, uji integrasi ke dashboard, dan hasil "
        "pengujian stabilitas awal sistem.",
        "**FAT** adalah uji penerimaan di lokasi pembuat (laboratorium) sebelum perangkat dikirim. "
        "**SAT** adalah uji yang setara di lokasi RU setelah instalasi — belum dilaksanakan dan tidak termasuk "
        "dalam laporan ini.",
    ])

    # 2
    heading(doc, "2. Perangkat dan konfigurasi uji")
    table(doc, ["Perangkat", "Jumlah tersedia", "Dipakai dalam uji FAT"], [
        ["Node sensor GLD", "4 unit (3 untuk RU IV + 1 cadangan)",
         "Uji real-time AI pada device 1001; uji CH dan downlink pada node beralamat 0xAA01 dan 0xF020"],
        ["Cluster Head (CH)", "16 unit (9 besar + 7 kecil)",
         "3 unit pada uji failover dan alarm otomatis; 8 unit pada uji mesh 16 Juli 2026"],
        ["Gateway", "1 unit", "1 unit (radio mesh LoRa → Wi-Fi → MQTT)"],
        ["Server laboratorium", "1 set", "MQTT broker, backend, dan dashboard"],
    ], [1.5, 2.0, 3.4])
    para(doc, "Konfigurasi firmware dan parameter radio mengacu pada Technical Datasheet Rev 4.0 Lab IoT ITB "
         "(Whole System, Gas Leak Detector, Cluster Head, Gateway, Server).", size=9.6)

    # 3
    heading(doc, "3. Ringkasan hasil")
    table(doc, ["No", "Item uji", "Hasil utama", "Status"],
          [[i["no"], i["judul"], RINGKAS[i["no"]], i["status"]] for i in FAT_ITEMS],
          [0.7, 1.9, 3.2, 1.1], size=8.8, status_col=3)
    para(doc, "LULUS (LAB) = kriteria lulus terpenuhi pada pengujian laboratorium. Ketujuh item lulus. "
         "Penerimaan hasil uji dinyatakan melalui lembar pengesahan uji (Bagian 5).", size=9, color=GRAY)

    # 4
    heading(doc, "4. Rincian per item uji")
    for i in FAT_ITEMS:
        heading(doc, f"{i['no']} — {i['judul']}", level=2)
        table(doc, ["Aspek", "Uraian"], [
            ["Tujuan", i["tujuan"]],
            ["Prosedur", i["prosedur"]],
            ["Kriteria lulus", i["kriteria"]],
            ["Hasil", i["hasil"]],
            ["Bukti", i["bukti"]],
            ["Status", i["status"]],
        ], [1.4, 5.5], size=9.2, status_col=None)

    # 5
    heading(doc, "5. Lembar pengesahan uji")
    para(doc, "Dengan ditandatanganinya lembar ini, para pihak menyatakan telah memeriksa dan/atau menyaksikan "
         "hasil Factory Acceptance Test FAT-01 sampai FAT-07 sebagaimana diuraikan dalam laporan ini.", size=9.8)
    sg = doc.add_table(rows=2, cols=3)
    sg.style = "Table Grid"
    heads = ["Disiapkan oleh\nPT LAPI Ganesha Utama", "Diperiksa oleh\nLab IoT ITB",
             "Disaksikan dan diterima oleh\nPT Pertamina Patra Niaga"]
    for c, h in enumerate(heads):
        cell = sg.rows[0].cells[c]
        set_cell_shading(cell, HEAD_SHADE)
        rr = cell.paragraphs[0].add_run(h)
        rr.font.bold = True; rr.font.size = Pt(9)
        cell2 = sg.rows[1].cells[c]
        cell2.paragraphs[0].add_run("\n\n\n\n")
        p2 = cell2.add_paragraph()
        r2 = p2.add_run("Nama:\nJabatan:\nTanggal:")
        r2.font.size = Pt(8.8); r2.font.color.rgb = GRAY
    fix_widths(sg, [2.3, 2.3, 2.3])
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

    # lampiran
    heading(doc, "Lampiran — Daftar bukti")
    table(doc, ["No", "Bukti", "Item terkait"], [
        ["1", "Notulen rapat 6 Agustus 2026 di Lab IoT ITB (kehadiran PT Pertamina Patra Niaga)", "Witness, FAT-06, FAT-07"],
        ["2", "Presentasi hasil model CNN Dual-Branch (6 Agustus 2026)", "FAT-01, FAT-02"],
        ["3", "Lembar kerja uji sinyal LoRa (RSSI, SNR, PDR per titik)", "FAT-03"],
        ["4", "Kutipan catatan uji Lab IoT ITB: uji CH dan failover (Mei 2026), baseline LoRa, uji mesh 8 CH dan downlink (16 Juli 2026)", "FAT-03, FAT-04, FAT-05"],
        ["5", "Technical Datasheet Rev 4.0 Lab IoT ITB (5 dokumen)", "FAT-02, FAT-05, FAT-06, konfigurasi"],
        ["6", "Foto unit GLD terakit", "Perangkat uji"],
        ["7", "Laporan Uji Laboratorium 01 — Model AI (LGU/GLD/UJI-LAB/2026-001)", "FAT-01, FAT-02"],
        ["8", "Laporan Uji Laboratorium 02 — Komunikasi LoRa (LGU/GLD/UJI-LAB/2026-002)", "FAT-03"],
        ["9", "Laporan Uji Laboratorium 03 — Mesh, Failover, Downlink & Integrasi (LGU/GLD/UJI-LAB/2026-003)", "FAT-04 s.d. FAT-07"],
    ], [0.4, 4.6, 1.9], size=9)

    doc.save(OUT)
    print("written", OUT)


if __name__ == "__main__":
    build()
