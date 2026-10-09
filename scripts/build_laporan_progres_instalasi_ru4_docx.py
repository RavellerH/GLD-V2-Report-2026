# -*- coding: utf-8 -*-
"""Build "Laporan Progres Pekerjaan Instalasi GLD — RU IV Cilacap" (corporate .docx).

Laporan status pekerjaan persiapan instalasi RU IV Cilacap per 9 Oktober 2026:
kronologi sejak survey 9-10 Agu, desain lingkup final 8 Okt, status kesiapan
per pihak, butir konfirmasi, langkah berikutnya, dan dokumen terkait. Konten
merangkum keputusan yang sudah tercatat (dec:55, 106-109, 125, 163-175, 204-207);
tidak ada angka/klaim baru. Helper format dipakai ulang dari
build_spesifikasi_material_instalasi_docx.py.

Run:  python3 scripts/build_laporan_progres_instalasi_ru4_docx.py
PDF:  python3 scripts/docx_to_pdf_with_toc.py Deliverables/<nama>.docx
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_persiapan_instalasi_corporate_docx import (  # noqa: E402
    make_doc, set_cell_shading, add_field, NAVY, GRAY, WHITE,
)
from build_spesifikasi_material_instalasi_docx import (  # noqa: E402
    para, bullets, heading, table, fix_widths, banner,
)
from docx.shared import Pt, Inches, RGBColor  # noqa: E402
from docx.enum.text import WD_ALIGN_PARAGRAPH  # noqa: E402

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(REPO, "Deliverables", "Laporan_Progres_Instalasi_GLD_RU-IV_Cilacap_9Oktober2026.docx")
DOC_NO = "LGU/GLD/LAP-INSTALASI/2026-001"
REV = "1.0"
DATE = "9 Oktober 2026"
HEADER = "Laporan Progres Pekerjaan Instalasi GLD — RU IV Cilacap"
SRC = os.path.join(REPO, "Sumber Dokumen")
BLOCK = os.path.join(SRC, "Pertamina RU IV 8Okt2026", "block_diagram_scope_final_router_LGU_8Okt2026.png")
LAYOUT = os.path.join(SRC, "Pertamina RU IV 2Okt2026", "layout_titik.jpg")
CH_PHOTOS = os.path.join(REPO, "scripts", "assets", "ch_mount_photos")


def picture(doc, path, width, caption):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.keep_with_next = True
    p.add_run().add_picture(path, width=Inches(width))
    para(doc, caption, size=8.8, color=GRAY, italic=True)


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
    tr = title.add_run("Laporan Progres Pekerjaan Instalasi GLD — RU IV Cilacap")
    tr.font.size = Pt(18); tr.font.bold = True; tr.font.color.rgb = NAVY
    para(doc, "Status persiapan pemasangan sistem Gas Leak Detection (GLD) Tahap 2 di area aman perimeter "
         "Sulfur Recovery Unit (SRU) RU IV Cilacap, dari survey lokasi Agustus sampai penetapan desain "
         "lingkup kerja final 8 Oktober 2026.", size=10.6, color=GRAY, after=10)

    rows = [
        ("Nomor dokumen", DOC_NO), ("Revisi", REV), ("Tanggal", DATE),
        ("Periode laporan", "9 Agustus – 9 Oktober 2026"),
        ("Disiapkan oleh", "PT LAPI Ganesha Utama, bersama Lab IoT & Fisika Institut Teknologi Bandung"),
        ("Ditujukan kepada", "PT Pertamina Patra Niaga — RU IV Cilacap"),
    ]
    p_ = doc.add_paragraph()
    r = p_.add_run("Document Control")
    r.font.bold = True; r.font.size = Pt(11); r.font.color.rgb = NAVY
    mt = doc.add_table(rows=0, cols=2)
    mt.style = "Table Grid"
    for k, v in rows:
        row = mt.add_row().cells
        set_cell_shading(row[0], "EEF2F7")
        row[0].paragraphs[0].paragraph_format.space_after = Pt(2)
        r0 = row[0].paragraphs[0].add_run(k)
        r0.font.bold = True; r0.font.size = Pt(9.3); r0.font.color.rgb = GRAY
        row[1].paragraphs[0].paragraph_format.space_after = Pt(2)
        r1 = row[1].paragraphs[0].add_run(v)
        r1.font.size = Pt(9.6)
    fix_widths(mt, [1.9, 5.0])
    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # header/footer
    hp = sec.header.paragraphs[0]
    hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    hr = hp.add_run(HEADER)
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

    # 1. ringkasan
    heading(doc, "1. Ringkasan")
    table(doc, ["Aspek", "Status per 9 Oktober 2026"], [
        ["Survey lokasi", "Selesai — kunjungan RU IV Cilacap 9–10 Agustus 2026"],
        ["Lokasi pemasangan", "Area aman di perimeter SRU (dikonfirmasi Pertamina 17 September); layout titik dari RU IV "
                              "2 Oktober: 2 GLD, 2 junction box, 3 Cluster Head, 1 Gateway di gedung"],
        ["Desain lingkup kerja", "Block diagram lingkup final 8 Oktober 2026 — pembagian LGU (perangkat) dan "
                                 "Pertamina (instalasi, mounting support, infrastruktur) sudah jelas"],
        ["Perangkat & dokumen LGU", "Siap — perangkat sistem, router, desain bracket, spesifikasi material, daftar "
                                    "perangkat, dan draf JSA/HSE sudah diserahkan atau tersedia"],
        ["Spesifikasi material", "Rev 1.6 (9 Oktober) sudah selaras dengan block diagram final"],
        ["Pemasangan fisik", "Dilaksanakan RU IV melalui kontrak jasa pelaksana instalasi (MoM 29 September); "
                             "persiapan kontrak diperkirakan ± 1–2 bulan, jadwal mengikuti proses RU IV"],
        ["Commissioning & SAT", "Dilakukan LGU setelah pemasangan fisik selesai"],
    ], [1.75, 5.15])
    para(doc, "Seluruh pekerjaan persiapan dari sisi LGU telah dikerjakan. Tahap berikutnya adalah konfirmasi beberapa "
         "butir teknis (Bagian 6) dan proses kontrak jasa pemasangan di RU IV.", size=9.8)

    # 2. kronologi
    heading(doc, "2. Kronologi pekerjaan")
    table(doc, ["Tanggal", "Kegiatan", "Hasil"], [
        ["9–10 Agu", "Kunjungan & survey lokasi RU IV Cilacap", "Survey lokasi selesai; notulen kunjungan tersedia"],
        ["17 Sep", "Penetapan arah instalasi", "Chamber uji gas di kantor kilang + instalasi permanen hanya di lokasi "
                                              "non-ATEX; lokasi di perimeter SRU dikonfirmasi Pertamina"],
        ["17 Sep", "Matriks pembagian persiapan & daftar persiapan pelaksana", "Dokumen dibagikan ke Pertamina"],
        ["18 Sep", "Kurva-S persiapan instalasi", "Seluruh item persiapan sisi LGU selesai (15/15)"],
        ["29 Sep", "Rapat koordinasi persiapan pemasangan (daring)", "Pemasangan via kontrak jasa; posisi titik "
                                                                     "dikonfirmasi di sesi teknis; LGU kirim daftar perangkat rinci"],
        ["1 Okt", "Spesifikasi material instalasi rev 1.4", "Dikirim ke grup Pertamina bersama Pembagian Persiapan "
                                                          "rev 1.5 & Daftar Persiapan Pelaksana rev 1.2"],
        ["2 Okt", "Rapat teknis pemasangan; desain RU IV diterima", "Block diagram, layout titik, MoM 29 Sep; "
                                                                    "tanggapan LGU, Daftar Perangkat rev 1.2, "
                                                                    "Spesifikasi rev 1.5 (konfigurasi tiang CH)"],
        ["8 Okt", "Block diagram lingkup revisi & final", "Router Wi-Fi LGU ditambahkan; Gateway 5 VDC dari UPS; "
                                                          "GLD → CH via LoRa"],
        ["9 Okt", "Penyelarasan dokumen", "Spesifikasi Material rev 1.6 & Daftar Perangkat rev 1.3"],
    ], [0.85, 2.6, 3.45])

    # 3. desain lingkup
    heading(doc, "3. Desain lingkup kerja final")
    picture(doc, BLOCK, 6.9, "Gambar 3.1 Block diagram lingkup kerja RU IV final 8 Oktober 2026. Biru = disuplai LGU; "
                             "kuning = disuplai Pertamina (instalasi, mounting support, infrastruktur).")
    table(doc, ["Lingkup LGU (penyedia perangkat)", "Lingkup Pertamina RU IV (instalasi & infrastruktur)"], [
        ["Unit GLD (Node Sensor)", "Stanchion 2\" HDG + mounting support GLD & Gateway"],
        ["Cluster Head + panel surya (bracket panel dibawa LGU)", "Junction box SS316 + PSU 220 VAC → 24 VDC per titik GLD"],
        ["Gateway + adaptor", "Kabel daya 24 VDC 2C 16 AWG dari junction box ke GLD"],
        ["Router Wi-Fi 2,4 GHz + adaptor", "Server, UPS, dan jaringan IT di gedung"],
        ["Basis desain, supervisi QA, terminasi, energize, commissioning", "Pemasangan fisik, pekerjaan sipil & kelistrikan, K3"],
    ], [3.45, 3.45])
    para(doc, "Alur data: GLD → (LoRa) → Cluster Head → (LoRa mesh) → Gateway → (Wi-Fi 2,4 GHz) → router LGU → "
         "(LAN Cat6 lokal, tanpa internet) → server. Server terhubung ke jaringan IT kantor untuk akses dashboard.",
         size=9.6)
    picture(doc, LAYOUT, 6.9, "Gambar 3.2 Layout rencana titik pemasangan dari RU IV (2 Oktober 2026): GLD-1 & GLD-2 "
                              "dengan JB-1 & JB-2, CH-1 s/d CH-3 di perimeter, GW-1 di gedung.")

    # 4. progres teknis
    heading(doc, "4. Penyesuaian desain selama periode laporan")
    table(doc, ["Butir", "Keputusan", "Sumber"], [
        ["Tiang GLD", "Tiang baru pipa galvanis 2\" Sch40 (OD 60,3 mm) ditanam & dicor, 1,0 m di atas tanah; "
                      "sensor ± 0,5 m dari tanah (gas lebih berat dari udara)", "Spesifikasi §3.1"],
        ["Tiang Cluster Head", "Pipa 2\" Sch40 4,0 m; unit CH & antena di atas tiang; bracket 2 panel surya diklem "
                               "ke tiang (dibawa LGU)", "Spesifikasi §3.2"],
        ["Dimensi CH besar", "± Ø76 × 104 mm (enclosure aluminium silinder)", "Daftar Perangkat"],
        ["Catu daya GLD", "24 VDC ≥ 1 A per unit (konsumsi ≈ 8 W); PSU di junction box SS316 per titik",
         "Block diagram 8 Okt"],
        ["Cable entry GLD", "Gland M20 × 1,5", "Block diagram 8 Okt"],
        ["Gateway", "Di dalam gedung, 5 VDC lewat adaptor dari UPS; antena di luar pada mast", "Block diagram 8 Okt"],
        ["Jaringan lokal", "Gateway → router Wi-Fi 2,4 GHz (LGU) → LAN Cat6 → server; tanpa internet", "Block diagram 8 Okt"],
    ], [1.45, 4.15, 1.3])
    ph = doc.add_paragraph()
    ph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    ph.paragraph_format.keep_with_next = True
    for fn in ("ch_bracket_solar_detail.jpg", "ch_mast_antena_atap.jpg"):
        ph.add_run().add_picture(os.path.join(CH_PHOTOS, fn), height=Inches(2.5))
        ph.add_run("    ")
    para(doc, "Gambar 4.1 Konfigurasi Cluster Head dari uji LGU & ITB: bracket 2 panel surya di tiang (kiri), unit CH & "
              "antena di atas tiang (kanan).", size=8.8, color=GRAY, italic=True)

    # 5. status per pihak
    heading(doc, "5. Status kesiapan per pihak")
    heading(doc, "5.1 LGU & ITB", level=2)
    table(doc, ["Item", "Status"], [
        ["Unit GLD (3 terpasang + 1 cadangan), Cluster Head (tersedia > 5 unit), Gateway, router Wi-Fi", "Siap"],
        ["Gas test chamber portable untuk pengambilan data di kantor kilang", "Siap"],
        ["Desain bracket/pelat U-bolt (CAD) untuk fabrikasi pelaksana", "Diserahkan"],
        ["Spesifikasi Material Instalasi (rev 1.6) & Daftar Perangkat (rev 1.3)", "Tersedia"],
        ["Matriks pembagian persiapan, daftar persiapan pelaksana, draf JSA/HSE", "Diserahkan"],
        ["Konfigurasi PC server, MQTT broker, dashboard, dan router", "Disiapkan LGU, dipasang saat mobilisasi"],
    ], [5.4, 1.5])
    heading(doc, "5.2 Pertamina RU IV (mengikuti proses RU IV)", level=2)
    table(doc, ["Item", "Status"], [
        ["Kontrak jasa pelaksana instalasi", "Proses kontrak RU IV"],
        ["Pengesahan TRA/JSA, izin kerja, izin masuk personel & barang", "Menunggu proses RU IV"],
        ["Material: stanchion, pondasi, junction box SS316, PSU, kabel 24 VDC, grounding", "Menunggu proses RU IV"],
        ["Server, UPS, jaringan IT, ruang Gateway", "Menunggu proses RU IV"],
        ["Fabrikasi pelat mounting & pemasangan fisik", "Setelah kontrak pelaksana"],
    ], [5.4, 1.5])

    # 6. konfirmasi
    heading(doc, "6. Butir yang perlu dikonfirmasi RU IV")
    table(doc, ["No", "Butir", "Dipakai untuk"], [
        ["1", "Jumlah titik final (layout 2 Oktober: 2 GLD, 3 CH, 1 Gateway, 2 junction box)", "Volume material & BoQ"],
        ["2", "Dokumen klasifikasi area tertulis dari HSE bahwa titik Field non-ATEX (label \"CL.I DV.I\" sudah "
              "dihapus dari block diagram 8 Oktober)", "Dasar instalasi permanen"],
        ["3", "Lokasi mast antena Gateway dan rute kabel koaksial (belum tergambar di block diagram)", "Panjang & tipe koaksial"],
        ["4", "Penyedia adaptor Gateway & router (usulan: disertakan LGU) dan letak UPS terhadap ruang Gateway",
         "Jalur 220 VAC ber-UPS"],
        ["5", "Jarak rute kabel junction box → GLD (16 AWG cukup sampai ± 45 m)", "Ukuran & panjang kabel"],
        ["6", "Standar grounding & proteksi petir tiang CH / mast Gateway", "Item grounding"],
        ["7", "Orientasi pelat U-bolt pada tiang vertikal (dicek bersama pelaksana sebelum fabrikasi)", "Fabrikasi pelat"],
        ["8", "Pelaksana instalasi yang ditunjuk & jadwal mobilisasi", "Jadwal pemasangan"],
    ], [0.4, 4.4, 2.1])

    # 7. langkah berikut
    heading(doc, "7. Langkah berikutnya")
    table(doc, ["No", "Kegiatan", "Pihak"], [
        ["1", "Penyampaian dokumen rev terbaru (Spesifikasi 1.6, Daftar Perangkat 1.3, block diagram final)", "LGU"],
        ["2", "Konfirmasi butir Bagian 6; LGU menyesuaikan BoQ setelah jumlah titik final", "RU IV & LGU"],
        ["3", "Proses kontrak jasa pelaksana instalasi & perizinan", "RU IV"],
        ["4", "Pengadaan material, pekerjaan sipil (tiang & pondasi), junction box & kabel daya", "Pelaksana RU IV"],
        ["5", "Fabrikasi & pemasangan pelat/bracket, GLD, CH, Gateway (supervisi LGU)", "Pelaksana RU IV & LGU"],
        ["6", "Instalasi PC server & router, terminasi, energize, commissioning, SAT", "LGU & ITB"],
    ], [0.4, 4.9, 1.6])

    # 8. dokumen terkait
    heading(doc, "8. Dokumen terkait")
    bullets(doc, [
        "Spesifikasi Material & Kebutuhan Instalasi GLD — RU IV Cilacap, LGU/GLD/INSTALASI-SPEK/2026-001 rev 1.6 (9 Okt 2026)",
        "Daftar Perangkat dan Kebutuhan Pemasangan GLD, LGU/GLD/INSTALASI-PERANGKAT/2026-001 rev 1.3 (9 Okt 2026)",
        "Pembagian Persiapan Instalasi RU IV Cilacap rev 1.5 dan Daftar Persiapan Pelaksana Instalasi rev 1.2 (1 Okt 2026)",
        "Tanggapan Desain Pemasangan GLD RU IV Cilacap (2 Okt 2026)",
        "Block diagram lingkup final dan layout titik pemasangan dari RU IV (2 & 8 Okt 2026)",
        "Minutes of Meeting Koordinasi Persiapan Pemasangan GLD RU IV Cilacap (29 Sep 2026)",
    ], size=9.6)

    doc.save(OUT)
    print("written", OUT)


if __name__ == "__main__":
    build()
