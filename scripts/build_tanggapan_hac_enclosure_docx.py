# -*- coding: utf-8 -*-
"""Build "Informasi Enclosure & Status Proteksi Ledakan GLD" (corporate .docx).

Tanggapan LGU atas pertanyaan Reliability RU IV Cilacap (Ibu Luthfiatul, WA 30 Okt–2 Nov 2026)
setelah Tabel 10 Hasil Verifikasi Lokasi Perangkat terhadap HAC SRU menyatakan GLD-01…04
"Belum Memenuhi" (area Class I, Groups C/D, Div. 2). Sumber data: listing HIREP HRP-T1000-A
(Sumber Dokumen/CASING/HIREP_HRP-T1000-A_Alibaba_listing_02Nov2026.txt), pengukuran suhu internal
(Sumber Dokumen/Pengukuran Temperatur/), dan status berkas sertifikasi yang dikirim ke agen GTS.

Run:  python3 scripts/build_tanggapan_hac_enclosure_docx.py
PDF:  python3 scripts/docx_to_pdf_with_toc.py Deliverables/Informasi_Enclosure_Proteksi_Ledakan_GLD_HAC_SRU.docx
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_persiapan_instalasi_corporate_docx import (  # noqa: E402
    make_doc, set_cell_shading, add_field, NAVY, GRAY, WHITE, HEAD_SHADE,
)
from build_spesifikasi_material_instalasi_docx import (  # noqa: E402
    para, bullets, heading, table, fix_widths, banner,
)
from docx.shared import Pt, Inches, RGBColor  # noqa: E402
from docx.enum.text import WD_ALIGN_PARAGRAPH  # noqa: E402

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(REPO, "Deliverables", "Informasi_Enclosure_Proteksi_Ledakan_GLD_HAC_SRU.docx")

DOC_NO = "LGU/GLD/HAC-ENCL/2026-001"
REV = "1.3"
DATE = "2 November 2026"
HEADER = "Informasi Enclosure & Status Proteksi Ledakan GLD"


def build():
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
    tr = title.add_run("Informasi Enclosure & Status Proteksi Ledakan Gas Leak Detector (GLD)")
    tr.font.size = Pt(18); tr.font.bold = True; tr.font.color.rgb = NAVY
    para(doc, "Tanggapan atas hasil verifikasi lokasi perangkat terhadap Hazardous Area "
         "Classification (HAC) Sulfur Recovery Unit (SRU), RU IV Cilacap: identitas enclosure, "
         "modifikasi yang dilakukan, data pendukung keselamatan yang sudah tersedia, dan status "
         "sertifikasi unit GLD.",
         size=10.6, color=GRAY, after=10)

    rows = [
        ("Nomor dokumen", DOC_NO), ("Revisi", REV), ("Tanggal", DATE),
        ("Status", "Informasi teknis untuk kajian — bukan sertifikat dan bukan pernyataan kesesuaian ATEX"),
        ("Disiapkan oleh", "PT LAPI Ganesha Utama, bersama Lab IoT & Fisika Institut Teknologi Bandung"),
        ("Ditujukan kepada", "PT Pertamina Patra Niaga — Reliability RU IV Cilacap"),
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
    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    banner(doc, "Ringkasan",
           "Enclosure GLD memakai housing detektor gas tahan ledakan **HIREP HRP-T1000-A** "
           "(aluminium die-cast, rating pabrikan **Ex d IIC T6 Gb, IP66**). Untuk memungkinkan gas "
           "mencapai 8 sensor GLD, kaca depan housing diganti mesh stainless steel dan seluruh "
           "elektronik di dalamnya adalah rancangan LGU. Karena itu **rating housing tersebut tidak "
           "otomatis berlaku untuk unit GLD**. Sertifikasi ATEX/IECEx unit GLD secara utuh sedang "
           "berproses melalui agen sertifikasi.", bg="EEF3FB")

    # header/footer
    hp = sec.header.paragraphs[0]
    hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    hr = hp.add_run(HEADER + "  |  PT LAPI Ganesha Utama")
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

    # 1
    heading(doc, "1. Latar belakang")
    para(doc, "Hasil verifikasi lokasi perangkat terhadap HAC SRU (Tabel 10) menunjukkan:")
    table(doc, ["Perangkat", "Lokasi rencana", "Klasifikasi (indikatif)", "Status"], [
        ["GLD-01", "Sisi timur area proses (area MEROX)", "Class I, Groups C/D, Div. 2", "Belum memenuhi"],
        ["GLD-02", "Sisi selatan area proses, dekat batas area classified", "Class I, Groups C/D, Div. 2", "Belum memenuhi"],
        ["GLD-03", "Sisi barat daya area proses", "Class I, Groups C/D, Div. 2", "Belum memenuhi"],
        ["GLD-04", "Sisi barat laut, dekat tangki 93-T-401/402", "Class I, Groups C/D, Div. 2", "Belum memenuhi"],
        ["JB-01", "Pipe support PS27", "Class I, Groups C/D, Div. 2", "Memenuhi"],
        ["CH-01 s.d. CH-05", "Pagar pembatas SRU", "Unclassified", "Memenuhi"],
        ["Gateway", "Control Building SRU (antena di atap)", "Unclassified", "Memenuhi"],
    ], [1.15, 2.6, 1.85, 1.3])
    para(doc, "Keempat titik GLD dinyatakan belum memenuhi karena GLD harus memenuhi sertifikasi "
         "ATEX. Reliability RU IV meminta informasi proteksi lain yang dapat menjadi justifikasi, "
         "serta material, brand, dan model enclosure. Dokumen ini menjawab kedua hal tersebut.")

    # 2
    heading(doc, "2. Identitas enclosure")
    para(doc, "Casing dan modul alarm (beacon) GLD berasal dari detektor gas tetap berikut. Data di "
         "bawah adalah spesifikasi yang dinyatakan pabrikan pada katalog produknya:")
    table(doc, ["Item", "Spesifikasi pabrikan"], [
        ["Brand / model", "HIREP HRP-T1000-A — detektor gas mudah terbakar tipe tetap"],
        ["Pabrikan", "Zhengzhou HIREP Electronic Technology Co., Ltd., Henan, Tiongkok"],
        ["Metode proteksi", "Tahan api (flameproof), **Ex d IIC T6 Gb**"],
        ["Tingkat perlindungan", "IP66"],
        ["Material housing", "Aluminium die-cast"],
        ["Dimensi / berat", "195 × 185 × 95 mm / < 1.000 g"],
        ["Ulir entry kabel", "M20 × 1,5 atau G1/2"],
        ["Suhu lingkungan", "−20 °C s.d. +55 °C; RH ≤ 95% (tanpa kondensasi)"],
        ["Catu daya / konsumsi", "DC 24 V ± 12 V / ≤ 3,0 W"],
        ["Sensor bawaan", "Pembakaran katalitik, di kepala sensor stainless steel bagian bawah"],
        ["Sertifikat (dinyatakan)", "ATEX, SIL, CE, FCC, Declaration of Conformity"],
    ], [1.9, 5.0])
    banner(doc, "Catatan sertifikat housing",
           "Katalog pabrikan mencantumkan ATEX, tetapi **nomor sertifikat dan notified body belum "
           "tercantum**. LGU sedang meminta salinan resmi sertifikat (EU-type examination certificate "
           "dan/atau IECEx Certificate of Conformity) kepada pabrikan dan akan menyampaikannya setelah "
           "diterima, termasuk hasil pengecekan nomornya pada database resmi.")

    # 3
    heading(doc, "3. Modifikasi pada housing dan dampaknya")
    para(doc, "GLD menggunakan susunan 8 sensor gas (MQ-series) dengan model AI di perangkat, bukan "
         "satu sensor katalitik seperti pada konfigurasi standar detektor HIREP. Untuk itu dilakukan modifikasi berikut:")
    bullets(doc, [
        "**Kaca depan diganti mesh stainless steel** agar gas dapat mengalir ke ruang sensor.",
        "**Seluruh elektronik diganti** dengan papan GLD (ESP32-S3, 8 sensor MQ dengan heater, kipas, "
        "radio LoRa, terminal 24 VDC).",
        "**Konsumsi daya naik** dari ≤ 3 W (konfigurasi standar HIREP) menjadi sekitar 8 W.",
    ])
    para(doc, "Pada metode Ex d, sertifikat berlaku hanya untuk konfigurasi yang diuji. Perbandingan "
         "berikut menunjukkan mengapa rating housing tidak dapat dipindahkan ke unit GLD:")
    table(doc, ["Aspek", "HIREP HRP-T1000-A (konfigurasi standar pabrikan)", "GLD (saat ini)"], [
        ["Jalur masuk gas", "Kepala sensor bawah dengan elemen flame arrestor, melindungi ruang sensor kecil",
         "Mesh stainless steel di bekas jendela depan, terbuka ke ruang utama casing (±0,4 L)"],
        ["Jendela depan", "Kaca, bagian dari sambungan flameproof", "Diganti mesh"],
        ["Isi / daya", "Elektronik pabrikan, ≤ 3 W", "Elektronik GLD, ±8 W, 8 heater sensor"],
        ["Kelas suhu", "T6 (≤ 85 °C), untuk konfigurasi standar pabrikan", "Target T4 (≤ 135 °C), perlu dibuktikan sendiri"],
        ["Suhu lingkungan", "−20 °C s.d. +55 °C", "Rentang operasi GLD −20 °C s.d. +60 °C (sedang ditinjau ulang)"],
        ["Berat", "< 1.000 g", "± 2,4 kg"],
    ], [1.45, 2.7, 2.75])
    para(doc, "Kesimpulannya, mesh stainless steel pada GLD memiliki fungsi yang serupa dengan elemen "
         "pelindung pada kepala sensor detektor HIREP standar, tetapi **kesetaraannya sebagai flame arrestor "
         "belum terbukti** karena jenis elemen, luas bukaan, dan volume ruang di belakangnya berbeda. "
         "Pembuktian ini menjadi bagian dari proses sertifikasi unit GLD.")

    # 4
    heading(doc, "4. Data pendukung keselamatan yang sudah tersedia")
    table(doc, ["Aspek", "Kondisi GLD", "Sifat data"], [
        ["Catu daya", "Hanya 24 VDC; tidak ada tegangan 220 VAC di dalam unit. Adaptor AC/DC berada di luar unit.",
         "Desain"],
        ["Konsumsi daya", "Maks. terukur 7,995 W pada 24 VDC (± 0,33 A)", "Uji lab LGU"],
        ["Proteksi elektrikal", "Fuse PPTC pada jalur masuk, dioda TVS/ESD dan Schottky pada papan", "Desain (BOM)"],
        ["Suhu internal", "Titik terpanas ± 114 °C (ekstrapolasi ke suhu lingkungan +60 °C, kondisi "
         "terburuk termasuk kipas mati) vs batas T4 135 °C (130 °C setelah margin uji)", "Uji internal LGU, belum lembaga"],
        ["Suhu permukaan luar", "± 79 °C pada kondisi yang sama", "Uji internal LGU, belum lembaga"],
        ["Housing", "Aluminium die-cast, ulir & O-ring, dari produk Ex d komersial", "Spesifikasi pabrikan"],
    ], [1.5, 4.0, 1.4])
    banner(doc, "Batasan data",
           "Data suhu di atas berasal dari pengukuran internal LGU (thermocouple 8 kanal, 180 menit) dan "
           "beberapa titik komponen belum diukur. Data ini menunjukkan indikasi positif terhadap kelas "
           "suhu T4, tetapi **bukan pengganti pengujian oleh lembaga sertifikasi**.")

    # 5
    heading(doc, "5. Status sertifikasi unit GLD")
    bullets(doc, [
        "Berkas permohonan dan dokumen teknis unit GLD telah dikirim ke agen sertifikasi GTS "
        "(Shanghai Global Testing Services) sekitar 29 September 2026, dengan sampel bernomor seri "
        "GLD2-0x1001.",
        "Skema yang diajukan: **II 2G Ex db IIC T4 Gb** (Zona 1, grup gas IIC, kelas suhu T4). Skema "
        "ini masih berupa permohonan; klasifikasi akhir ditentukan lembaga sertifikasi.",
        "Dokumen teknis sedang direvisi mengikuti masukan iterasi berikutnya, termasuk penyempurnaan "
        "desain jalur masuk gas ke sensor.",
        "Perkiraan durasi sertifikasi 5–8 bulan sejak proses dimulai; jadwal pasti mengikuti lembaga.",
    ])
    para(doc, "Sebagai catatan, peralatan bersertifikat Zona 1 (EPL Gb) umumnya dapat dipakai di area "
         "yang lebih ringan seperti Zona 2 / Division 2. Penerimaan peralatan bertanda ATEX/IECEx di "
         "area berklasifikasi Class/Division tetap mengikuti kebijakan dan kajian RU IV.", size=9.8, color=GRAY)

    doc.save(OUT)
    print(OUT)


if __name__ == "__main__":
    build()
