# -*- coding: utf-8 -*-
"""Build 3 laporan uji laboratorium GLD Tahap 2 (corporate .docx) — pendukung Laporan FAT.

  01  Uji Model AI (klasifikasi gas di perangkat)         -> FAT-01, FAT-02
  02  Uji Komunikasi Radio LoRa                           -> FAT-03
  03  Uji Jaringan Mesh, Failover, Downlink & Integrasi   -> FAT-04 .. FAT-07

Semua angka dikutip dari bukti yang sudah ada (presentasi model AI 6 Agustus 2026,
lembar kerja uji sinyal LoRa, catatan kerja mingguan Apr–Jul 2026). Gambar bukti
diambil dari dokumen sumber dan disimpan di scripts/assets/uji_lab/.

Run:  python3 scripts/build_laporan_uji_lab_docx.py
PDF:  python3 scripts/docx_to_pdf_with_toc.py Deliverables/Laporan_Uji_Lab_0X_....docx
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_spesifikasi_material_instalasi_docx import (  # noqa: E402
    make_doc, set_cell_shading, add_field, fix_widths, para, bullets, heading,
    table, NAVY, GRAY, WHITE, HEAD_SHADE,
)
from docx.shared import Pt, Inches, RGBColor  # noqa: E402
from docx.enum.text import WD_ALIGN_PARAGRAPH  # noqa: E402
from PIL import Image  # noqa: E402

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSET = os.path.join(REPO, "scripts", "assets", "uji_lab")
DELIV = os.path.join(REPO, "Deliverables")
DATE = "4 Oktober 2026"
REV = "1.1"


def figure(doc, name, caption, max_w=6.3, max_h=3.6):
    path = os.path.join(ASSET, name)
    w, h = Image.open(path).size
    scale = min(max_w / (w / 96), max_h / (h / 96))
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(2)
    p.add_run().add_picture(path, width=Inches((w / 96) * scale))
    c = doc.add_paragraph()
    c.alignment = WD_ALIGN_PARAGRAPH.CENTER
    c.paragraph_format.space_after = Pt(8)
    r = c.add_run(caption)
    r.font.size = Pt(8.8); r.font.italic = True; r.font.color.rgb = GRAY


def front(doc, sec, title, subtitle, doc_no, header_label, rows_extra):
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

    t = doc.add_heading(level=0)
    tr = t.add_run(title)
    tr.font.size = Pt(18); tr.font.bold = True; tr.font.color.rgb = NAVY
    para(doc, subtitle, size=10.6, color=GRAY, after=10)

    rows = [("Nomor dokumen", doc_no), ("Revisi", REV), ("Tanggal", DATE)] + rows_extra + [
        ("Lokasi uji", "Lab IoT, Instrumentation and Computations, Gedung Laboratorium Fisika Terpadu, dan "
                       "area kampus Institut Teknologi Bandung"),
        ("Disiapkan oleh", "PT LAPI Ganesha Utama, bersama Lab IoT & Fisika Institut Teknologi Bandung"),
        ("Ditujukan kepada", "PT Pertamina Patra Niaga"),
        ("Dokumen terkait", "Laporan Factory Acceptance Test (FAT) Sistem GLD Tahap 2, LGU/GLD/FAT/2026-001"),
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

    hp = sec.header.paragraphs[0]
    hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    hr = hp.add_run(header_label + "  |  Untuk Pengesahan")
    hr.font.size = Pt(8); hr.font.color.rgb = GRAY; hr.font.italic = True
    fp = sec.footer.paragraphs[0]
    fp.add_run(f"{doc_no}  ·  Rev. {REV}")
    fp.paragraph_format.tab_stops.add_tab_stop(Inches(6.9), alignment=2)
    fp.add_run("\t")
    add_field(fp, "PAGE", "1")
    fp.add_run(" dari ")
    add_field(fp, "NUMPAGES", "1")
    for r in fp.runs:
        r.font.size = Pt(8); r.font.color.rgb = GRAY
    doc.add_page_break()


def signoff(doc, n):
    heading(doc, f"{n}. Lembar pengesahan")
    sg = doc.add_table(rows=2, cols=3)
    sg.style = "Table Grid"
    heads = ["Dilaksanakan oleh\nLab IoT ITB", "Diperiksa oleh\nPT LAPI Ganesha Utama",
             "Mengetahui\nPT Pertamina Patra Niaga"]
    for c, h in enumerate(heads):
        cell = sg.rows[0].cells[c]
        set_cell_shading(cell, HEAD_SHADE)
        rr = cell.paragraphs[0].add_run(h)
        rr.font.bold = True; rr.font.size = Pt(9)
        cell2 = sg.rows[1].cells[c]
        cell2.paragraphs[0].add_run("\n\n\n\n")
        r2 = cell2.add_paragraph().add_run("Nama:\nJabatan:\nTanggal:")
        r2.font.size = Pt(8.8); r2.font.color.rgb = GRAY
    fix_widths(sg, [2.3, 2.3, 2.3])
    # jaga tabel tanda tangan tetap utuh dalam satu halaman
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    for row in sg.rows:
        trPr = row._tr.get_or_add_trPr()
        cs = OxmlElement("w:cantSplit"); trPr.append(cs)
    for cell in sg.rows[0].cells:
        for pp in cell.paragraphs:
            pp.paragraph_format.keep_with_next = True


# --------------------------------------------------------------------- 01 AI
def build_ai():
    doc, sec = make_doc()
    no = "LGU/GLD/UJI-LAB/2026-001"
    front(doc, sec, "Laporan Uji Laboratorium 01 — Model AI Klasifikasi Gas di Perangkat GLD",
          "Pengujian akuisisi data 8 sensor gas, pelatihan dan pengujian model CNN Dual-Branch, "
          "kuantisasi untuk mikrokontroler ESP32-S3, serta uji real-time langsung di perangkat GLD.",
          no, "Laporan Uji Lab 01 — Model AI GLD",
          [("Periode uji", "s.d. 6 Agustus 2026 (hasil dipresentasikan pada rapat 6 Agustus 2026)"),
           ("Item FAT terkait", "FAT-01 (akuisisi sensor), FAT-02 (klasifikasi AI di perangkat)")])

    heading(doc, "1. Tujuan")
    bullets(doc, [
        "Memastikan 8 sensor gas MQ pada node GLD menghasilkan data yang valid dan konsisten untuk dataset.",
        "Mengukur akurasi model klasifikasi gas pada data uji dari dataset pengembangan yang belum pernah dilihat model.",
        "Memastikan model tetap akurat setelah diperkecil (kuantisasi) agar muat di ESP32-S3.",
        "Memastikan model berjalan langsung di perangkat (on-device) dan mengklasifikasikan gas sebenarnya secara real-time.",
    ])

    heading(doc, "2. Perangkat dan konfigurasi")
    table(doc, ["Komponen", "Keterangan"], [
        ["Node GLD", "ESP32-S3, 8 sensor MQ (MQ2, MQ3, MQ4, MQ5, MQ6, MQ7, MQ8, MQ135); unit uji real-time: device 1001"],
        ["Model", "CNN Dual-Branch: cabang A Conv1D (16 filter, kernel 3) untuk 8 nilai ADC sensor; "
                  "cabang B Dense untuk 7 fitur pengetahuan datasheet sensor; digabung lalu Dense 16 → output kelas"],
        ["Pelatihan", "Maksimum 200 epoch dengan early stopping (15 epoch), batch 32, 15% data latih untuk validasi"],
        ["Runtime di perangkat", "TensorFlow Lite Micro, model INT8 ditanam di firmware sebagai header C"],
        ["Keluaran di perangkat", "Sesuai Technical Datasheet Rev 4.0 Gas Leak Detector (4 September 2026), bagian 4.1: "
                                  "label Clean Air, LPG, dan H2 beserta nilai confidence"],
    ], [1.6, 5.3])
    para(doc, "Laporan ini memuat dua tahap uji: (1) validasi model pada dataset pengembangan berlabel LPG, CO₂, "
         "dan udara bersih (Bagian 4.1 dan 4.2); (2) uji real-time di perangkat dengan konfigurasi label Clean Air, "
         "LPG, dan H2 sesuai Technical Datasheet Rev 4.0 (Bagian 4.3).", size=9.6)
    figure(doc, "ai_arsitektur.png", "Gambar 1. Arsitektur model CNN Dual-Branch")

    heading(doc, "3. Metode")
    bullets(doc, [
        "**Dataset pengembangan.** 1.870 pembacaan sensor unik (duplikat dibuang) pada 3 kondisi: LPG, CO₂, dan udara bersih. "
        "Dibagi seimbang 80% latih (1.496) dan 20% uji (374).",
        "**Uji model.** Model diuji pada 374 data uji independen; dihitung akurasi, F1-score, dan presisi per kelas.",
        "**Kuantisasi.** Model dikonversi bertahap: Keras → TFLite float32 → TFLite INT8, akurasi diukur ulang tiap tahap.",
        "**Uji real-time di perangkat.** Model INT8 dijalankan di board ESP32-S3 (device 1001) nonstop ±11,7 menit "
        "dengan paparan H2 dan udara bersih; hasil klasifikasi dibandingkan dengan gas sebenarnya yang dipaparkan.",
    ])
    figure(doc, "ai_data.png", "Gambar 2. Sebaran data per kondisi gas dan sensor yang dipakai")

    heading(doc, "4. Hasil")
    heading(doc, "4.1 Akurasi pada data uji (dataset pengembangan)", level=2)
    table(doc, ["Parameter", "Hasil"], [
        ["Akurasi keseluruhan (374 data uji)", "99,73%"],
        ["F1-score rata-rata", "99,56%"],
        ["Presisi LPG (220 data)", "100%"],
        ["Presisi CO₂ (109 data)", "100%"],
        ["Presisi udara bersih (45 data)", "98%"],
    ], [3.5, 3.4])
    figure(doc, "ai_hasil_uji.png", "Gambar 3. Hasil uji model dan confusion matrix")
    heading(doc, "4.2 Kuantisasi untuk ESP32-S3", level=2)
    table(doc, ["Versi model", "Ukuran", "Akurasi"], [
        ["Keras (asli)", "57,95 KB", "99,73%"],
        ["TFLite float32", "11,29 KB", "99,73%"],
        ["TFLite INT8 (format yang ditanam di perangkat)", "9,14 KB", "99,20%"],
    ], [3.0, 1.9, 2.0])
    para(doc, "Model diperkecil 84% dengan penurunan akurasi hanya 0,53 poin persen.", size=9.6)
    heading(doc, "4.3 Uji real-time di perangkat (label Clean Air, LPG, H2)", level=2)
    table(doc, ["Parameter", "Hasil"], [
        ["Perangkat", "Board ESP32-S3 GLD, device 1001"],
        ["Durasi", "±11,7 menit nonstop"],
        ["Jumlah pembacaan", "1.176"],
        ["Gas yang dipaparkan", "H2 dan udara bersih"],
        ["Akurasi real-time", "97,65%"],
        ["H2", "Presisi 98,4% (676 benar dari 687)"],
        ["Udara bersih", "Presisi 96,9% (474 benar dari 489)"],
    ], [3.0, 3.9])
    figure(doc, "ai_realtime.png", "Gambar 4. Hasil uji real-time di perangkat (device 1001)")

    heading(doc, "5. Kesimpulan")
    bullets(doc, [
        "Kedelapan sensor menghasilkan data valid; dataset pengembangan 1.870 pembacaan berhasil disusun (FAT-01 lulus).",
        "Pada dataset pengembangan, model mencapai akurasi 99,73% pada data uji dan 99,20% setelah kuantisasi "
        "INT8 berukuran 9,14 KB.",
        "Di perangkat (label Clean Air, LPG, H2), model berjalan langsung di ESP32-S3 dengan akurasi real-time "
        "97,65% pada paparan H2 dan udara bersih; keputusan alarm diambil di node tanpa menunggu server "
        "(FAT-02 lulus). Deteksi LPG di perangkat dibuktikan pada uji alarm otomatis (FAT-06).",
    ])
    signoff(doc, 6)
    out = os.path.join(DELIV, "Laporan_Uji_Lab_01_Model_AI_GLD.docx")
    doc.save(out); print("written", out)


# ------------------------------------------------------------------- 02 LoRa
def build_lora():
    doc, sec = make_doc()
    no = "LGU/GLD/UJI-LAB/2026-002"
    front(doc, sec, "Laporan Uji Laboratorium 02 — Komunikasi Radio LoRa",
          "Pengujian jarak dan keandalan komunikasi LoRa antara node GLD dan Cluster Head di lingkungan "
          "kampus ITB: kuat sinyal (RSSI), SNR, dan persentase paket sampai (PDR) pada berbagai jarak dan halangan.",
          no, "Laporan Uji Lab 02 — Komunikasi LoRa",
          [("Periode uji", "Mei – Juli 2026"),
           ("Item FAT terkait", "FAT-03 (komunikasi radio GLD ke Cluster Head)")])

    heading(doc, "1. Tujuan")
    para(doc, "Mencari jarak terjauh yang masih menjaga PDR 100% dengan RSSI/SNR yang punya margin aman, "
         "sambil mencatat halangan (gedung, pepohonan), sebagai dasar penempatan GLD dan Cluster Head di lokasi RU.",
         size=9.8)

    heading(doc, "2. Perangkat dan konfigurasi")
    table(doc, ["Komponen", "Keterangan"], [
        ["Pengirim", "Node GLD / modul LoRa E22-900MM22S"],
        ["Penerima", "Cluster Head (receiver di Labtek XV untuk uji acak)"],
        ["Frekuensi", "920–923 MHz (STAR 920 MHz, MESH 921 MHz)"],
        ["Antena", "Omni 3 dBi; tinggi antena divariasikan 2–6 m"],
        ["Parameter dicatat", "Jarak, koordinat, RSSI (min/avg/maks), SNR (min/avg/maks), paket terkirim/diterima, PDR"],
    ], [1.6, 5.3])

    heading(doc, "3. Metode")
    bullets(doc, [
        "Node GLD mengirim N paket per titik (100 paket pada uji acak) ke penerima.",
        "Titik dipindah bertahap; jarak, koordinat GPS, dan halangan dicatat.",
        "Batas link aman = jarak terjauh dengan PDR 100% dan RSSI/SNR masih punya margin.",
    ])
    figure(doc, "lora_simulasi.png", "Gambar 1. Skema pengujian simulasi komunikasi LoRa di sekitar ITB")

    heading(doc, "4. Hasil")
    heading(doc, "4.1 Uji baseline berdasarkan kondisi lingkungan", level=2)
    table(doc, ["No", "Kondisi", "Jarak (m)", "Tinggi antena Tx / Rx (m)", "RSSI (dBm)", "PDR"], [
        ["1", "Area terbuka", "10", "3 / 3", "−47", "100%"],
        ["2", "Area terbuka", "30", "3 / 3", "−57", "100%"],
        ["3", "Area terbuka", "100", "3 / 3", "−71", "100%"],
        ["4", "Bawah pepohonan", "80", "3 / 3", "−78", "100%"],
        ["5", "Bawah pepohonan", "80", "4 / 4", "−84", "100%"],
        ["6", "Belakang gedung + pepohonan", "tidak dicatat", "3 / 3", "−93", "98%"],
        ["7", "Belakang gedung + pepohonan (antena diubah)", "tidak dicatat", "2 / 6", "−81", "100%"],
        ["8", "Area Indomaret", "tidak dicatat", "2 / 6", "−104", "68%"],
        ["9", "Area Fisika (batas jangkauan)", "tidak dicatat", "2 / 6", "−112", "26%"],
    ], [0.4, 2.3, 0.9, 1.3, 0.9, 0.7], size=8.8)
    para(doc, "Baris 6–9 diukur berdasarkan kondisi halangan; jarak tidak dicatat pada lembar uji.", size=9, color=GRAY)
    heading(doc, "4.2 Uji acak di kampus (receiver di Labtek XV, 100 paket per titik)", level=2)
    table(doc, ["Titik", "Lokasi", "Jarak (m)", "RSSI avg (dBm)", "SNR avg (dB)", "PDR"], [
        ["Tx 1", "Depan Gedung Minyak", "87", "−94 (uji real-time singkat)", "8,8", "tidak diukur (uji singkat)"],
        ["Tx 2", "Gerbang Utara", "243", "−101", "6,5", "100% (100/100)"],
        ["Tx 3", "Depan LFT", "177", "−94", "9,3", "100% (100/100)"],
        ["Tx 4", "STEI Lt.2 (Labtek V)", "201", "−115", "−5,2", "87% (87/100)"],
        ["Tx 5", "Depan Gedung Fisika", "342", "−120 (sesaat)", "−14,8", "0%"],
        ["Tx 6", "SAPPK", "141", "tidak terbaca", "tidak terbaca", "0% (data tidak sampai, terhalang gedung)"],
    ], [0.5, 1.6, 0.8, 1.6, 1.0, 1.4], size=8.8)
    heading(doc, "4.3 Uji orientasi antena 3 dBi (receiver arah selatan, 100 m)", level=2)
    para(doc, "Depan GKUT, arah selatan, 100 m: RSSI −89 / −72 / −60 dBm (min/avg/maks), SNR 9,2 / 10,4 / 11,5 dB, "
         "PDR 100%. Titik 200–300 m dan arah lain (barat daya, barat) mengalami timeout karena terhalang gedung. "
         "Uji orientasi dalam laporan ini memakai antena 3 dBi.", size=9.6)
    figure(doc, "lora_baseline.png", "Gambar 2. Rekap uji baseline komunikasi LoRa per kondisi lingkungan")

    heading(doc, "5. Kesimpulan")
    bullets(doc, [
        "Di area terbuka, PDR 100% tercapai hingga 100 m (RSSI −71 dBm); pada jalur pandang bebas di kampus, "
        "PDR 100% tercapai pada 177 m dan 243 m (FAT-03 lulus: PDR 100% pada link jalur pandang bebas).",
        "Batas jangkauan per hop teridentifikasi: gedung dan pepohonan menurunkan kualitas link (PDR 87% pada "
        "201 m terhalang gedung; putus di atas ±340 m). Jarak antar-hop di lokasi ditetapkan di bawah batas ini.",
        "Menaikkan antena penerima ke 6 m memperbaiki link di area gedung dan pepohonan (−93 dBm/98% menjadi −81 dBm/100%).",
        "Keterbatasan jarak per hop diatasi dengan jaringan mesh multi-hop Cluster Head (lihat Laporan Uji Lab 03) "
        "dan penempatan antena Cluster Head/Gateway yang tinggi.",
    ])
    signoff(doc, 6)
    out = os.path.join(DELIV, "Laporan_Uji_Lab_02_Komunikasi_LoRa_GLD.docx")
    doc.save(out); print("written", out)


# ------------------------------------------------------------------- 03 Mesh
def build_mesh():
    doc, sec = make_doc()
    no = "LGU/GLD/UJI-LAB/2026-003"
    front(doc, sec, "Laporan Uji Laboratorium 03 — Jaringan Mesh, Failover, Downlink, dan Integrasi Sistem",
          "Pengujian pembentukan jaringan mesh Cluster Head secara otomatis, pemulihan saat satu Cluster Head mati, "
          "jaringan mesh 8 Cluster Head se-kampus ITB, perintah balik (downlink) ke GLD, serta integrasi "
          "GLD – Cluster Head – Gateway – Server dan alarm otomatis.",
          no, "Laporan Uji Lab 03 — Mesh & Integrasi",
          [("Periode uji", "20 April – 8 Agustus 2026"),
           ("Item FAT terkait", "FAT-04 (mesh & failover), FAT-05 (end-to-end), FAT-06 (alarm otomatis), FAT-07 (dashboard)")])

    heading(doc, "1. Tujuan")
    bullets(doc, [
        "Memastikan Cluster Head (CH) membentuk jaringan mesh secara otomatis dan memilih parent terbaik.",
        "Memastikan jaringan pulih otomatis tanpa kehilangan data saat satu CH mati (failover).",
        "Memastikan jaringan mesh bekerja pada skala 8 CH dengan beberapa lapis (multi-hop).",
        "Memastikan perintah dari Gateway sampai ke GLD melalui mesh (downlink).",
        "Memastikan data dan alarm mengalir dari GLD sampai server dan dashboard.",
    ])

    heading(doc, "2. Perangkat dan konfigurasi")
    table(doc, ["Komponen", "Keterangan"], [
        ["Node GLD", "Alamat 0xAA01 (uji CH) dan 0xF020 (uji downlink)"],
        ["Cluster Head", "ESP32-S3 + 2 radio LoRa: STAR 920 MHz (ke GLD) dan MESH 921 MHz (antar-CH); panel surya + baterai"],
        ["Gateway", "Radio MESH → Wi-Fi → MQTT"],
        ["Server", "MQTT broker, backend, dan dashboard di laboratorium"],
    ], [1.6, 5.3])

    heading(doc, "3. Hasil uji")
    heading(doc, "3.1 Pembentukan mesh otomatis (20–26 April 2026)", level=2)
    para(doc, "CH3/Gateway aktif pertama, disusul CH2 dan CH1. Setiap CH mengirim permintaan konfigurasi, "
         "menerima respons, lalu memilih parent berdasarkan RSSI terbaik. Topologi terbentuk: "
         "Node 0xAA01 → CH1 → CH2 → CH3/Gateway → server MQTT, dengan konfirmasi (ACK) di setiap hop.", size=9.6)
    figure(doc, "mesh_topologi_normal.png", "Gambar 1. Topologi normal — aliran data berhasil")
    heading(doc, "3.2 Failover saat CH mati", level=2)
    table(doc, ["Langkah", "Hasil"], [
        ["CH2 dimatikan", "CH1 mengirim ke CH2 tiga kali tanpa ACK (backoff 100/200/400 ms) → failover dimulai"],
        ["Mencari parent baru", "CH1 menyiarkan permintaan konfigurasi; CH3/Gateway merespons (RSSI −105 dBm)"],
        ["Parent berubah", "CH2 (0x0002) → CH3/Gateway (0x0003); ACK OK"],
        ["Topologi baru", "Node → CH1 → CH3/Gateway (melewati CH2)"],
        ["Data", "Tetap terkirim, tidak ada data hilang, tanpa intervensi manual"],
    ], [1.6, 5.3])
    figure(doc, "failover_log.png", "Gambar 2. Log failover CH1: parent berpindah dari CH2 ke CH3/Gateway")
    heading(doc, "3.3 Mesh 8 Cluster Head se-kampus ITB (16 Juli 2026)", level=2)
    para(doc, "8 CH ditempatkan di beberapa gedung kampus ITB dan membentuk jaringan 3 lapis menuju Gateway: "
         "lapis 1 CH3, CH5, CH8; lapis 2 CH1, CH4; lapis 3 CH2 (kedalaman rute 1–3). Semua CH berstatus terpasang "
         "dan terhubung ke Gateway.", size=9.6)
    figure(doc, "mesh_8ch.png", "Gambar 3. Peta dan topologi uji mesh 8 Cluster Head, 16 Juli 2026", max_h=3.4)
    heading(doc, "3.4 Downlink Gateway → CH → GLD", level=2)
    para(doc, "Perintah dari Gateway dikirim ke node GLD 0xF020 melalui jalur mesh. Setelah perbaikan firmware "
         "downlink, perintah sampai ke GLD melalui CH.", size=9.6)
    figure(doc, "downlink.png", "Gambar 4. Uji downlink ke GLD 0xF020 melalui mesh", max_h=3.2)
    heading(doc, "3.5 Integrasi end-to-end dan alarm otomatis", level=2)
    table(doc, ["Uji", "Tanggal", "Hasil"], [
        ["Rantai GLD – CH – Gateway – Server", "16 Juli 2026", "Data mengalir end-to-end tanpa intervensi manual"],
        ["Alarm otomatis (push alarm)", "6–8 Agustus 2026",
         "GLD disemprot LPG pada konfigurasi Gateway + 3 CH; status server berubah menjadi alarm otomatis "
         "tanpa permintaan data dari server; waktu respons tidak diukur dengan pencatat waktu (interval laporan "
         "radio sesuai desain 10 detik), pengukuran terhadap KPI ≤30 detik dilakukan pada Site Acceptance Test"],
        ["Monitoring dashboard", "6 Agustus 2026", "Data dan alarm tampil di dashboard; didemonstrasikan saat kunjungan Pertamina"],
    ], [2.0, 1.3, 3.6], size=9)

    heading(doc, "4. Kesimpulan")
    bullets(doc, [
        "CH membentuk mesh dan memilih parent secara otomatis (FAT-04).",
        "Saat satu CH mati, jaringan pulih otomatis tanpa kehilangan data (FAT-04).",
        "Mesh 8 CH dengan 3 lapis berfungsi di kampus ITB, dan downlink ke GLD berhasil (FAT-04).",
        "Data dan alarm mengalir dari GLD sampai server dan dashboard secara otomatis (FAT-05, FAT-06, FAT-07).",
    ])
    signoff(doc, 5)
    out = os.path.join(DELIV, "Laporan_Uji_Lab_03_Mesh_Integrasi_GLD.docx")
    doc.save(out); print("written", out)


if __name__ == "__main__":
    build_ai()
    build_lora()
    build_mesh()
