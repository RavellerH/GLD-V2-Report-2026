# -*- coding: utf-8 -*-
"""Build "Spesifikasi Teknis Material Instalasi GLD — RU IV Cilacap" (corporate .docx).

Dokumen untuk tim PT Pertamina Patra Niaga, bahan rapat 2 Oktober 2026: spesifikasi
tiang besi (ditanam & dicor), kabel catu daya 24 VDC (dua opsi skema PSU), jaringan
Gateway-server, fastener, grounding, dan BoQ. Konten di-hardcode di skrip ini
(bukan diparse dari HTML); helper format diambil dari
build_persiapan_instalasi_corporate_docx.py agar tampilan seragam.

Run:  python3 scripts/build_spesifikasi_material_instalasi_docx.py
PDF:  python3 scripts/docx_to_pdf_with_toc.py Deliverables/<nama>.docx
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_persiapan_instalasi_corporate_docx import (  # noqa: E402
    make_doc, set_cell_shading, add_field, NAVY, GRAY, WHITE, INK,
    GREEN, AMBER, RED, HEAD_SHADE, ZEBRA_SHADE,
)
from docx.shared import Pt, Inches, RGBColor  # noqa: E402
from docx.enum.text import WD_ALIGN_PARAGRAPH  # noqa: E402
from docx.oxml import OxmlElement  # noqa: E402
from docx.oxml.ns import qn  # noqa: E402

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(REPO, "Deliverables",
                   "Spesifikasi_Material_Instalasi_GLD_RU-IV_Cilacap.docx")

DOC_NO = "LGU/GLD/INSTALASI-SPEK/2026-001"
REV = "1.0"
DATE = "1 Oktober 2026"
HEADER = "Spesifikasi Material Instalasi GLD — RU IV Cilacap"

# Asumsi perencanaan (diganti begitu data lapangan tersedia)
N_GLD = 3
N_CH = 6          # CH tersedia >5 unit; 6 dipakai sbg angka perencanaan
N_GW = 1

STATUS_STYLE = {
    "FINAL": (GREEN, "EAF4EC"),
    "USULAN": (AMBER, "FFF3DC"),
    "KONFIRMASI": (RED, "FBE6E4"),
}


# ---------------------------------------------------------------- helpers
def para(doc, text, size=10.2, bold=False, color=None, italic=False, after=6):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(after)
    _runs(p, text, size, bold, color, italic)
    return p


def _runs(p, text, size=10.2, bold=False, color=None, italic=False):
    """**tebal** didukung secara sederhana."""
    parts = text.split("**")
    for i, part in enumerate(parts):
        if not part:
            continue
        r = p.add_run(part)
        r.font.size = Pt(size)
        r.font.bold = bold or (i % 2 == 1)
        r.font.italic = italic
        if color is not None:
            r.font.color.rgb = color


def bullets(doc, items, size=10):
    for it in items:
        p = doc.add_paragraph(style="List Bullet")
        p.paragraph_format.space_after = Pt(3)
        _runs(p, it, size)


def heading(doc, text, level=1):
    h = doc.add_heading(level=level)
    r = h.add_run(text)
    r.font.color.rgb = NAVY
    return h


def table(doc, head, rows, widths, size=9.2, status_col=None):
    t = doc.add_table(rows=1, cols=len(head))
    t.style = "Table Grid"
    for i, h in enumerate(head):
        c = t.rows[0].cells[i]
        set_cell_shading(c, "1B2A4A")
        c.paragraphs[0].paragraph_format.space_after = Pt(1)
        r = c.paragraphs[0].add_run(h)
        r.font.bold = True; r.font.size = Pt(size); r.font.color.rgb = WHITE
    for ri, row in enumerate(rows):
        cells = t.add_row().cells
        for i, val in enumerate(row):
            c = cells[i]
            c.paragraphs[0].paragraph_format.space_after = Pt(1)
            if status_col is not None and i == status_col and val in STATUS_STYLE:
                col, bg = STATUS_STYLE[val]
                set_cell_shading(c, bg)
                r = c.paragraphs[0].add_run(val)
                r.font.bold = True; r.font.size = Pt(size - 0.6); r.font.color.rgb = col
                continue
            if ri % 2 == 1:
                set_cell_shading(c, ZEBRA_SHADE)
            _runs(c.paragraphs[0], str(val), size)
    fix_widths(t, widths)
    doc.add_paragraph().paragraph_format.space_after = Pt(2)
    return t


def fix_widths(t, widths):
    """Lebar kolom tetap (tblLayout=fixed + tblGrid) agar Word & LibreOffice patuh."""
    tblPr = t._tbl.tblPr
    lay = OxmlElement("w:tblLayout"); lay.set(qn("w:type"), "fixed")
    tblPr.append(lay)
    grid = t._tbl.tblGrid
    for gc, w in zip(grid.findall(qn("w:gridCol")), widths):
        gc.set(qn("w:w"), str(int(w * 1440)))
    for row in t.rows:
        for i, w in enumerate(widths):
            row.cells[i].width = Inches(w)


def banner(doc, title, text, bg="FFF6E5"):
    t = doc.add_table(rows=1, cols=1)
    t.style = "Table Grid"
    c = t.rows[0].cells[0]
    set_cell_shading(c, bg)
    c.paragraphs[0].paragraph_format.space_after = Pt(2)
    r = c.paragraphs[0].add_run(title)
    r.font.bold = True; r.font.size = Pt(9.8)
    p2 = c.add_paragraph()
    p2.paragraph_format.space_after = Pt(2)
    _runs(p2, text, 9.4)
    fix_widths(t, [6.9])
    doc.add_paragraph().paragraph_format.space_after = Pt(2)


# ---------------------------------------------------------------- build
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
    tr = title.add_run("Spesifikasi Material & Kebutuhan Instalasi GLD — RU IV Cilacap")
    tr.font.size = Pt(18); tr.font.bold = True; tr.font.color.rgb = NAVY
    para(doc, "Tiang besi, kabel catu daya 24 VDC, jaringan Gateway–server, fastener, "
         "grounding, dan daftar kebutuhan (BoQ) untuk pemasangan sistem Gas Leak Detection "
         "di area aman perimeter Sulfur Recovery Unit (SRU). Disusun agar tim PT Pertamina "
         "Patra Niaga dan vendor instalasi dapat mulai menyiapkan material.",
         size=10.6, color=GRAY, after=10)

    # document control
    rows = [
        ("Nomor dokumen", DOC_NO), ("Revisi", REV), ("Tanggal", DATE),
        ("Status", "Draf kerja — bahan rapat koordinasi 2 Oktober 2026, bukan dokumen pengadaan final"),
        ("Disiapkan oleh", "PT LAPI Ganesha Utama, bersama Lab IoT & Fisika Institut Teknologi Bandung"),
        ("Ditujukan kepada", "PT Pertamina Patra Niaga — RU IV Cilacap & vendor instalasi yang ditunjuk"),
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
    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    para(doc, "Cara membaca status", bold=True, color=NAVY, after=3)
    table(doc, ["Status", "Arti"], [
        ["FINAL", "Angka sudah tetap dari desain/keputusan proyek — boleh dipakai langsung untuk pengadaan."],
        ["USULAN", "Usulan teknis LGU berdasarkan praktik umum industri — boleh dipakai untuk estimasi, "
                   "disesuaikan bila standar RU IV berbeda."],
        ["KONFIRMASI", "Bergantung kondisi lapangan/keputusan RU IV — perlu dijawab di rapat sebelum pengadaan."],
    ], [1.2, 5.7], status_col=0)

    # header/footer
    header = sec.header
    hp = header.paragraphs[0]
    hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    hr = hp.add_run(HEADER + "  |  Draf Kerja")
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

    # 1. ringkasan
    heading(doc, "1. Ringkasan — yang perlu disiapkan")
    table(doc, ["Kebutuhan", "Spesifikasi singkat", "Jumlah (perencanaan)", "Status"], [
        ["Tiang GLD", "Pipa baja galvanis 2\" Sch40 (OD 60,3 mm), panjang 2,5 m, ditanam & dicor", f"{N_GLD} batang", "USULAN"],
        ["Tiang Cluster Head", "Pipa baja galvanis 2\" Sch40 (OD 60,3 mm), panjang 4,0 m, ditanam & dicor", f"{N_CH} batang*", "USULAN"],
        ["Pondasi cor", "GLD 40×40×80 cm · CH 50×50×100 cm, beton fc' ≥ 20 MPa", f"{N_GLD + N_CH} titik*", "USULAN"],
        ["Catu daya GLD", "24 VDC, kapasitas ≥ 1 A per unit (konsumsi aktual ≈ 0,33 A)", f"{N_GLD} unit beban", "FINAL"],
        ["Kabel daya 24 VDC", "2 inti tembaga; ukuran mengikuti jarak (Tabel 4.2): 1,5–6 mm²", "Σ jarak + cadangan", "KONFIRMASI"],
        ["Kabel jaringan", "Cat6 (PC ↔ router LGU, PC ↔ intranet kantor)", "2 jalur", "USULAN"],
        ["PC server", "PC fisik dekat Gateway, 2 port LAN (dual-network)", "1 unit", "FINAL"],
        ["Klem U-bolt & pelat", "U-bolt 2\"/DN50 thread M10, pelat 250×250 mm (desain LGU)", "2 U-bolt per titik", "FINAL"],
        ["Grounding tiang", "Bonding ke sistem grounding RU IV", f"{N_GLD + N_CH + N_GW} titik*", "KONFIRMASI"],
    ], [1.35, 3.35, 1.25, 0.95], status_col=3)
    para(doc, f"* Unit Cluster Head (CH) yang tersedia lebih dari 5. Dokumen ini memakai **{N_CH} titik CH "
         "sebagai angka perencanaan**; jumlah final mengikuti penempatan di lapangan (prinsipnya CH "
         "sesedikit mungkin selama seluruh GLD terjangkau). CH memakai panel surya + baterai, "
         "**tidak memerlukan kabel daya**.", size=9.2, color=GRAY)

    # 2. konfigurasi
    heading(doc, "2. Konfigurasi sistem yang dipasang")
    table(doc, ["Perangkat", "Jumlah", "Sumber daya", "Penempatan"], [
        ["GLD (Node Sensor)", f"{N_GLD} unit", "24 VDC melalui kabel", "Titik deteksi di area aman perimeter SRU"],
        ["Cluster Head (CH)", f">5 tersedia (rencana {N_CH})", "Panel surya (2 panel) + baterai, tanpa kabel", "Di antara GLD dan Gateway, membentuk jaringan LoRa mesh"],
        ["Gateway (GW)", f"{N_GW} unit", "Menunggu konfirmasi tim LGU (lihat §5)", "Safe area, dekat PC server"],
        ["PC server", "1 unit", "220 VAC", "Dekat Gateway; disediakan Pertamina, dikonfigurasi LGU"],
        ["Router lapangan", "1 unit", "220 VAC", "Dekat PC server; disediakan LGU"],
    ], [1.4, 1.35, 1.95, 2.2])
    para(doc, "Alur data: GLD → (LoRa) → CH → (LoRa mesh) → Gateway → (Wi-Fi) → router LGU → PC server "
         "(MQTT broker + dashboard). PC server juga tersambung ke intranet kantor kilang lewat port LAN "
         "kedua agar dashboard dapat diakses dari kantor.", size=9.6)

    # 3. tiang
    heading(doc, "3. Spesifikasi tiang besi (ditanam & dicor)")
    para(doc, "Tiang harus berupa pipa ber-OD 60,3 mm (2\" NPS) karena klem U-bolt pada desain bracket "
         "GLD dirancang untuk diameter ini. Pipa ukuran lain tidak dapat dipakai tanpa mengubah U-bolt.",
         size=9.8)
    heading(doc, "3.1 Tiang GLD", level=2)
    table(doc, ["Parameter", "Spesifikasi", "Status"], [
        ["Material", "Pipa baja karbon galvanis celup panas (hot-dip galvanized), mis. ASTM A53 / API 5L Gr.B", "USULAN"],
        ["Ukuran", "2\" NPS Schedule 40 — OD 60,3 mm, tebal dinding 3,91 mm", "FINAL"],
        ["Panjang batang", "2,5 m = 1,8 m di atas tanah + 0,7 m tertanam di cor", "USULAN"],
        ["Tinggi pasang unit GLD", "± 1,5 m dari tanah (setinggi orang, sesuai arahan rapat 6 Agustus). "
                                   "Posisi dapat digeser sepanjang tiang", "KONFIRMASI"],
        ["Ujung atas", "Ditutup pipe cap (las di bengkel atau ulir) agar air hujan tidak masuk", "USULAN"],
        ["Ujung bawah (dalam cor)", "Diberi besi silang/angkur (mis. 2× besi Ø12 mm tembus pipa) agar tiang tidak berputar", "USULAN"],
        ["Pondasi", "Lubang 40 × 40 × 80 cm, beton fc' ≥ 20 MPa (± K-250), permukaan atas dibuat miring menjauhi tiang", "USULAN"],
        ["Masa tunggu", "Unit GLD dipasang setelah beton cukup kuat (umumnya ≥ 3 hari; ikuti praktik vendor)", "USULAN"],
        ["Tegak lurus", "Toleransi vertikal ≤ 1° (cek waterpass saat pengecoran)", "USULAN"],
    ], [1.6, 4.3, 1.0], status_col=2)
    banner(doc, "Catatan tinggi sensor",
           "Tinggi 1,5 m mengikuti arahan rapat 6 Agustus (instalasi baru dicoba setinggi orang). Dalam praktik "
           "umum, sensor untuk gas yang lebih berat dari udara (LPG, H₂S) dipasang lebih rendah, sedangkan untuk gas "
           "ringan (H₂, metana) lebih tinggi. Karena posisi unit bisa digeser di sepanjang tiang, tinggi final "
           "per titik dapat disepakati bersama HSE RU IV tanpa mengubah tiang.")

    heading(doc, "3.2 Tiang Cluster Head (dan Gateway bila di luar ruangan)", level=2)
    table(doc, ["Parameter", "Spesifikasi", "Status"], [
        ["Material & ukuran", "Sama dengan tiang GLD: pipa baja galvanis 2\" Sch40, OD 60,3 mm", "USULAN"],
        ["Panjang batang", "4,0 m = 3,0 m di atas tanah + 1,0 m tertanam", "USULAN"],
        ["Alasan tinggi", "Antena LoRa ditempatkan di atas halangan (orang, kendaraan, peralatan) untuk jangkauan antar-CH", "USULAN"],
        ["Pondasi", "Lubang 50 × 50 × 100 cm, beton fc' ≥ 20 MPa, angkur silang di ujung bawah", "USULAN"],
        ["Dudukan panel surya", "2 panel per CH, menghadap utara, kemiringan ± 10–15°. Dimensi panel diserahkan tim LGU", "KONFIRMASI"],
        ["Mounting CH", "Pelat U-bolt yang sama dengan GLD (2\"/DN50, M10)", "FINAL"],
        ["Tinggi final per titik", "Ditentukan tim RF LGU saat penempatan (line of sight antar-CH)", "KONFIRMASI"],
    ], [1.6, 4.3, 1.0], status_col=2)

    heading(doc, "3.3 Grounding & penandaan", level=2)
    bullets(doc, [
        "Setiap tiang logam di-bonding ke sistem grounding RU IV (mis. kabel BC/NYA hijau-kuning 16 mm² + klem pipa "
        "+ sepatu kabel), atau ground rod tersendiri bila titik grounding jauh. **Metode dan nilai resistansi mengikuti "
        "standar RU IV.**",
        "Tiang CH yang lebih tinggi dari struktur sekitarnya: perlu tidaknya proteksi petir ditentukan HSE/elektrikal RU IV.",
        "Setiap tiang diberi label nomor titik (GLD-01…03, CH-01…, GW-01) yang sama dengan nomor di dashboard.",
    ])

    # 4. kabel daya
    heading(doc, "4. Catu daya & kabel 24 VDC untuk GLD")
    para(doc, "Hanya GLD yang membutuhkan kabel daya. Setiap GLD bekerja pada **24 VDC** dengan kapasitas "
         "sumber **≥ 1 A per unit**; konsumsi terukur maksimum ≈ 8 W (≈ 0,33 A). Unit GLD tidak pernah "
         "menerima 220 VAC — konversi AC/DC dilakukan PSU di luar unit.", size=9.8)

    heading(doc, "4.1 Dua opsi skema PSU", level=2)
    table(doc, ["", "Opsi A — PSU per titik", "Opsi B — PSU pusat"], [
        ["Konsep", "Tiap GLD punya PSU 220 VAC→24 VDC di box/panel terdekat yang ada stop kontak/220 VAC",
                   "Satu PSU 24 VDC di panel/ruang kontrol; kabel ditarik ke tiap GLD"],
        ["PSU", "24 VDC, ≥ 1 A (disarankan 2,5 A tipe DIN-rail industri), 1 per GLD",
                "24 VDC, ≥ 5 A (3 × 1 A + cadangan), tipe DIN-rail industri"],
        ["Proteksi", "MCB 2 A di sisi 220 VAC + terminal block", "MCB di sisi AC + sekring/MCB DC 2 A per jalur GLD"],
        ["Kabel 24 VDC", "Pendek (umumnya ≤ 50 m) → cukup 2 × 1,5 mm²", "Panjang → ukuran naik sesuai Tabel 4.2"],
        ["Kelebihan", "Kabel kecil & murah, gangguan satu titik tidak memengaruhi titik lain",
                      "Satu titik perawatan, bisa digabung dengan UPS"],
        ["Syarat", "Ada sumber 220 VAC di dekat tiap titik; box PSU di area aman", "Tiap GLD ditarik kabel sendiri (home-run), "
                                                                               "tidak disambung berantai"],
    ], [1.0, 2.95, 2.95])

    heading(doc, "4.2 Ukuran kabel vs panjang maksimum", level=2)
    para(doc, "Panjang maksimum satu arah (PSU → GLD) agar drop tegangan ≤ 5 % (1,2 V dari 24 V). "
         "Kabel tembaga 2 inti, resistansi pada 20 °C; dihitung untuk kapasitas desain 1 A dan untuk konsumsi aktual 0,33 A.",
         size=9.6)
    table(doc, ["Luas penampang", "Resistansi (Ω/km)", "Maks. @ 1 A (desain)", "Maks. @ 0,33 A (aktual)"], [
        ["2 × 1,5 mm²", "12,1", "50 m", "150 m"],
        ["2 × 2,5 mm²", "7,41", "80 m", "245 m"],
        ["2 × 4 mm²", "4,61", "130 m", "390 m"],
        ["2 × 6 mm²", "3,08", "195 m", "590 m"],
    ], [1.6, 1.6, 1.85, 1.85])
    para(doc, "**Rekomendasi:** pilih ukuran berdasarkan kolom 1 A (desain) agar ada cadangan. Bila jarak > 195 m, "
         "gunakan Opsi A (PSU lokal) untuk titik tersebut. Batas tegangan input minimum GLD belum dinyatakan "
         "tim desain; angka 5 % dipakai sebagai batas konservatif.", size=9.6)

    heading(doc, "4.3 Jenis kabel, rute & terminasi", level=2)
    table(doc, ["Parameter", "Spesifikasi", "Status"], [
        ["Konduktor", "2 inti tembaga, berlabel L+ / L− (positif / negatif 24 VDC)", "FINAL"],
        ["Jenis kabel", "Kabel daya/instrumen luar ruang berpelindung armor (mis. SWA), tahan UV & minyak", "USULAN"],
        ["Material selubung & rute", "Mengikuti standar kabel RU IV (ditanam, conduit, atau cable tray existing)", "KONFIRMASI"],
        ["Masuk ke unit GLD", "Cable gland M20 × 1,5 (IP66). Diameter luar kabel harus masuk rentang klem gland; "
                              "kabel armor memerlukan gland tipe armored", "FINAL"],
        ["Terminasi", "Ujung kabel diberi ferrule/skun; sambungan ke konduktor L+/L− di dalam unit dikerjakan teknisi LGU", "FINAL"],
        ["Pelaksana", "Penarikan kabel & PSU oleh vendor/RU IV; terminasi akhir, energize & commissioning oleh LGU", "FINAL"],
    ], [1.6, 4.3, 1.0], status_col=2)

    heading(doc, "4.4 Menghitung panjang kabel", level=2)
    para(doc, "Jarak titik GLD ke sumber listrik belum diukur. Panjang kabel per titik dihitung dengan:", size=9.8)
    para(doc, "Panjang kabel = (jarak rute aktual × 1,10) + 3 m cadangan di sisi PSU + 3 m cadangan di sisi GLD",
         bold=True, size=10, after=4)
    para(doc, "Faktor 1,10 menampung belokan dan naik-turun rute; ukur rute kabel, bukan jarak garis lurus. "
         "Contoh perencanaan (asumsi, bukan data lapangan):", size=9.6)
    table(doc, ["Asumsi jarak rute per GLD", "Panjang per titik", f"Total {N_GLD} GLD", "Ukuran kabel (desain 1 A)"], [
        ["20 m (Opsi A, PSU dekat)", "28 m", "84 m → beli 100 m", "2 × 1,5 mm²"],
        ["50 m", "61 m", "183 m → beli 200 m", "2 × 1,5 mm²"],
        ["100 m (Opsi B, PSU pusat)", "116 m", "348 m → beli 400 m", "2 × 4 mm²"],
    ], [1.95, 1.4, 1.75, 1.8])

    # 5. jaringan & server
    heading(doc, "5. Gateway, PC server & jaringan")
    table(doc, ["Item", "Spesifikasi", "Penyedia", "Status"], [
        ["PC server", "PC fisik, 2 port LAN (NIC kedua bisa USB-LAN), dekat Gateway, di safe area. "
                      "Usulan minimum: 4 core / 8 GB RAM / SSD 256 GB", "Pertamina", "USULAN"],
        ["Router lapangan", "Router Wi-Fi untuk Gateway ↔ PC server (jaringan GLD terpisah dari jaringan kilang)", "LGU", "FINAL"],
        ["Kabel PC ↔ router", "Cat6 patch cord 2–5 m", "LGU", "USULAN"],
        ["Kabel PC ↔ intranet kantor", "Cat6 ke titik jaringan kantor terdekat; panjang mengikuti lokasi (> 90 m → switch/fiber). "
                                       "Akses hanya untuk API/dashboard", "Pertamina (IT RU IV)", "KONFIRMASI"],
        ["Jarak Gateway ↔ router", "Sebaiknya dalam satu ruangan/area tanpa sekat logam (Gateway memakai Wi-Fi)", "—", "USULAN"],
        ["Daya Gateway", "Menunggu konfirmasi tim LGU (adaptor 220 VAC atau panel surya + baterai seperti CH)", "LGU", "KONFIRMASI"],
        ["Stop kontak 220 VAC", "Minimal 4 titik di lokasi PC (PC, monitor, router, Gateway)", "Pertamina", "USULAN"],
        ["UPS", "Disarankan ≥ 1 kVA untuk PC + router agar alarm tetap tercatat saat listrik padam", "Pertamina", "USULAN"],
    ], [1.45, 3.2, 1.25, 1.0], status_col=3)

    # 6. fastener
    heading(doc, "6. Bracket, fastener & aksesori per titik")
    table(doc, ["Item", "Spesifikasi", "Per titik", "Status"], [
        ["U-bolt", "2\"/DN50, thread M10, lebar dalam 62–65 mm, tinggi dalam 95–100 mm, panjang ulir 40 mm", "2 buah", "FINAL"],
        ["Mur & ring", "M10 — mur + ring datar + ring per, material anti-karat (disarankan SS316 karena dekat laut)", "4 set", "USULAN"],
        ["Pelat mounting", "250 × 250 mm, dibuat vendor sesuai gambar desain LGU", "1 buah", "FINAL"],
        ["Spacer", "45–60 mm (bila perlu)", "sesuai kebutuhan", "FINAL"],
        ["Kabel ties", "Tahan UV, stainless atau nylon UV", "± 10 buah", "USULAN"],
        ["Larangan", "Tanpa PVC pada housing/bracket; tanpa bor/las pada struktur existing kilang", "—", "FINAL"],
    ], [1.3, 3.65, 1.0, 0.95], status_col=3)
    banner(doc, "Perlu dicek sebelum fabrikasi pelat",
           "Desain pelat U-bolt saat ini secara visual paling sesuai untuk pipa horizontal (handrail). Karena "
           "seluruh titik memakai tiang baru yang berdiri vertikal, kecocokan orientasi pelat pada tiang vertikal "
           "perlu dicek tim desain LGU bersama vendor sebelum pelat difabrikasi.", bg="FBE9E9")

    # 7. BoQ
    heading(doc, "7. Daftar kebutuhan (BoQ) perencanaan")
    para(doc, f"Basis: {N_GLD} GLD + {N_CH} CH + {N_GW} Gateway. Angka CH dan panjang kabel adalah asumsi perencanaan; "
         "sesuaikan setelah titik final ditetapkan.", size=9.6)
    n_pole = N_GLD + N_CH
    table(doc, ["No", "Item", "Spesifikasi", "Qty", "Penyedia"], [
        ["1", "Pipa tiang GLD", "Galvanis 2\" Sch40, 2,5 m", f"{N_GLD} batang", "Vendor"],
        ["2", "Pipa tiang CH", "Galvanis 2\" Sch40, 4,0 m", f"{N_CH} batang", "Vendor"],
        ["3", "Pipe cap 2\"", "Penutup ujung atas tiang", f"{n_pole} buah", "Vendor"],
        ["4", "Beton cor", f"GLD {N_GLD}×0,13 m³ + CH {N_CH}×0,25 m³ ≈ {N_GLD*0.128 + N_CH*0.25:.1f} m³ (belum termasuk susut/sisa)", "± 2 m³", "Vendor"],
        ["5", "U-bolt 2\" M10 + mur/ring", "Lihat §6", f"{2*n_pole} U-bolt, {4*n_pole} set mur", "Vendor"],
        ["6", "Pelat mounting 250×250 mm", "Sesuai gambar LGU", f"{n_pole} buah", "Vendor"],
        ["7", "Dudukan panel surya CH", "2 panel per CH", f"{N_CH} set", "Vendor (dimensi dari LGU)"],
        ["8", "PSU 24 VDC", "Opsi A: 3 × (≥1 A) · Opsi B: 1 × (≥5 A)", "3 atau 1 unit", "RU IV / vendor"],
        ["9", "Box/panel PSU + MCB + terminal", "Untuk area aman", "3 atau 1 set", "RU IV / vendor"],
        ["10", "Kabel daya 2 inti", "Ukuran & panjang per §4", "Σ per §4.4", "RU IV / vendor"],
        ["11", "Kabel grounding + klem", "Mengikuti standar RU IV", f"{n_pole + N_GW} titik", "Vendor"],
        ["12", "PC server + UPS + stop kontak", "Lihat §5", "1 set", "Pertamina"],
        ["13", "Kabel Cat6", "Patch + jalur ke intranet kantor", "2 jalur", "LGU / IT RU IV"],
        ["14", "Router lapangan", "Lihat §5", "1 unit", "LGU"],
        ["15", "Unit GLD, CH, Gateway, panel surya CH", "Perangkat sistem", f"{N_GLD} / {N_CH} / {N_GW}", "LGU"],
    ], [0.4, 1.75, 2.6, 1.15, 1.0])

    # 8. pertanyaan rapat
    heading(doc, "8. Yang perlu diputuskan di rapat 2 Oktober")
    table(doc, ["No", "Pertanyaan untuk RU IV / vendor", "Dampak bila belum dijawab"], [
        ["1", "Titik/koordinat final 3 GLD di perimeter SRU, dan jarak rute ke sumber 220 VAC terdekat", "Panjang & ukuran kabel tidak bisa dipesan"],
        ["2", "Pilih Opsi A (PSU per titik) atau Opsi B (PSU pusat)", "Jumlah PSU & ukuran kabel"],
        ["3", "Standar kabel & rute RU IV (ditanam / conduit / cable tray), termasuk material selubung", "Jenis kabel & cable gland"],
        ["4", "Standar & titik grounding, serta perlu tidaknya proteksi petir untuk tiang CH", "Item grounding di BoQ"],
        ["5", "Izin galian & pengecoran di area perimeter SRU, serta dokumen klasifikasi area tertulis", "Jadwal mobilisasi vendor"],
        ["6", "Lokasi ruangan PC server/Gateway, ketersediaan 220 VAC, UPS, dan titik jaringan intranet kantor", "Penempatan Gateway & kabel LAN"],
        ["7", "Vendor yang ditunjuk & jadwal fabrikasi/pemasangan", "Jadwal instalasi"],
    ], [0.4, 4.0, 2.5])

    heading(doc, "9. Batasan dokumen")
    bullets(doc, [
        "Angka berstatus USULAN berasal dari praktik umum industri, bukan dari kajian struktur/elektrikal formal. "
        "Vendor dan RU IV dapat menyesuaikan dengan standar yang berlaku di kilang.",
        "Pembagian kerja tetap: vendor yang ditunjuk Pertamina mengerjakan fabrikasi & pemasangan fisik (termasuk "
        "pekerjaan ketinggian dan K3); LGU menyediakan basis desain, supervisi teknis/QA, serta terminasi elektrikal, "
        "energize, dan commissioning GLD.",
        "Instalasi permanen hanya di lokasi yang tidak memerlukan ATEX (area aman), sesuai kesepakatan sebelumnya.",
    ], size=9.6)

    doc.save(OUT)
    print("written", OUT)


if __name__ == "__main__":
    build()
