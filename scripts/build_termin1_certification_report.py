from pathlib import Path

from docx import Document
from PIL import Image
from docx.enum.table import WD_ALIGN_VERTICAL, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "Paket Pertamina" / "02_Sertifikasi_ATEX_IECEx"
OUT_DOCX = OUT_DIR / "Laporan_Pemenuhan_Deliverable_Termin_1_Sertifikasi_GLD.docx"

CERT_DIR = ROOT / "Sumber Dokumen" / "sertifikasi-atex-gld-v2-2026" / "GLD"
PROTOTYPE_IMAGE_1 = CERT_DIR / "1. Motherboard_Casing.jpg"
PROTOTYPE_IMAGE_2 = CERT_DIR / "2. Motherboard_ModulSensor_Casing.jpg"
PROTOTYPE_IMAGE_3 = CERT_DIR / "3. Motherboard_ModulSensor_PenutupMesh_Casing_Antena_ModulAlarm.jpg"
BRACKET_IMAGE = ROOT / "Sumber Dokumen" / "GLD U Bolt Bracket" / "GLD U-Bolt Bracket V2.png"

CHARCOAL = "2F4050"
TEAL = "1ABB9C"
LIGHT_TEAL = "E8F7F4"
PALE_GRAY = "F3F3F4"
MID_GRAY = "D9D9D9"
TEXT = "20262B"
MUTED = "5B6670"
WHITE = "FFFFFF"
GREEN = "187A63"
AMBER = "9A6500"
RED = "B23B2E"


def prepare_image(source, target, max_width=1800, quality=88):
    target.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(source) as image:
        image = image.convert("RGB")
        if image.width > max_width:
            ratio = max_width / image.width
            image = image.resize((max_width, round(image.height * ratio)), Image.Resampling.LANCZOS)
        image.save(target, "JPEG", quality=quality, optimize=True)
    return target


def set_cell_shading(cell, fill):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = tc_pr.find(qn("w:shd"))
    if shd is None:
        shd = OxmlElement("w:shd")
        tc_pr.append(shd)
    shd.set(qn("w:fill"), fill)


def set_cell_margins(cell, top=90, start=110, bottom=90, end=110):
    tc = cell._tc
    tc_pr = tc.get_or_add_tcPr()
    tc_mar = tc_pr.first_child_found_in("w:tcMar")
    if tc_mar is None:
        tc_mar = OxmlElement("w:tcMar")
        tc_pr.append(tc_mar)
    for name, value in (("top", top), ("start", start), ("bottom", bottom), ("end", end)):
        node = tc_mar.find(qn(f"w:{name}"))
        if node is None:
            node = OxmlElement(f"w:{name}")
            tc_mar.append(node)
        node.set(qn("w:w"), str(value))
        node.set(qn("w:type"), "dxa")


def set_table_borders(table, color=MID_GRAY, size="6"):
    tbl_pr = table._tbl.tblPr
    borders = tbl_pr.first_child_found_in("w:tblBorders")
    if borders is None:
        borders = OxmlElement("w:tblBorders")
        tbl_pr.append(borders)
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        tag = qn(f"w:{edge}")
        node = borders.find(tag)
        if node is None:
            node = OxmlElement(f"w:{edge}")
            borders.append(node)
        node.set(qn("w:val"), "single")
        node.set(qn("w:sz"), size)
        node.set(qn("w:space"), "0")
        node.set(qn("w:color"), color)


def set_repeat_table_header(row):
    tr_pr = row._tr.get_or_add_trPr()
    tbl_header = OxmlElement("w:tblHeader")
    tbl_header.set(qn("w:val"), "true")
    tr_pr.append(tbl_header)


def set_run_font(run, name="Arial", size=10.5, bold=None, color=TEXT):
    run.font.name = name
    run._element.get_or_add_rPr().rFonts.set(qn("w:ascii"), name)
    run._element.get_or_add_rPr().rFonts.set(qn("w:hAnsi"), name)
    run.font.size = Pt(size)
    if bold is not None:
        run.bold = bold
    run.font.color.rgb = RGBColor.from_string(color)


def format_cell(cell, bold=False, color=TEXT, size=9.1, align=WD_ALIGN_PARAGRAPH.LEFT):
    cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
    set_cell_margins(cell)
    for paragraph in cell.paragraphs:
        paragraph.alignment = align
        paragraph.paragraph_format.space_after = Pt(0)
        paragraph.paragraph_format.space_before = Pt(0)
        paragraph.paragraph_format.line_spacing = 1.05
        for run in paragraph.runs:
            set_run_font(run, size=size, bold=bold, color=color)


STATUS_COLORS = {
    "TERSEDIA": GREEN,
    "SEBAGIAN": AMBER,
    "BELUM TERSEDIA": RED,
    "BELUM TERBUKTI": RED,
    "BELUM ADA": RED,
}


def status_color(value):
    upper = str(value).upper()
    for key, color in STATUS_COLORS.items():
        if key in upper:
            return color
    return TEXT


def add_table(doc, headers, rows, widths=None, font_size=9.1, status_col=None):
    table = doc.add_table(rows=1, cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    set_table_borders(table)
    hdr = table.rows[0]
    set_repeat_table_header(hdr)
    for idx, header in enumerate(headers):
        cell = hdr.cells[idx]
        cell.text = header
        set_cell_shading(cell, CHARCOAL)
        if widths:
            cell.width = Inches(widths[idx])
        format_cell(cell, bold=True, color=WHITE, size=8.8, align=WD_ALIGN_PARAGRAPH.CENTER)
    for row_idx, values in enumerate(rows):
        row = table.add_row()
        for idx, value in enumerate(values):
            cell = row.cells[idx]
            cell.text = str(value)
            if widths:
                cell.width = Inches(widths[idx])
            if row_idx % 2:
                set_cell_shading(cell, PALE_GRAY)
            align = WD_ALIGN_PARAGRAPH.CENTER if idx == 0 or idx == status_col else WD_ALIGN_PARAGRAPH.LEFT
            format_cell(cell, size=font_size, align=align)
            if idx == status_col:
                for run in cell.paragraphs[0].runs:
                    set_run_font(run, size=font_size, bold=True, color=status_color(value))
    doc.add_paragraph().paragraph_format.space_after = Pt(0)
    return table


def add_paragraph(doc, text="", bold_lead=None, style=None, align=None, size=10.5):
    p = doc.add_paragraph(style=style)
    if align is not None:
        p.alignment = align
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.line_spacing = 1.15
    if bold_lead and text.startswith(bold_lead):
        r1 = p.add_run(bold_lead)
        set_run_font(r1, size=size, bold=True)
        r2 = p.add_run(text[len(bold_lead):])
        set_run_font(r2, size=size)
    else:
        r = p.add_run(text)
        set_run_font(r, size=size)
    return p


def add_bullet(doc, text, level=0):
    style = "List Bullet" if level == 0 else "List Bullet 2"
    p = doc.add_paragraph(style=style)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.1
    r = p.add_run(text)
    set_run_font(r, size=10.2)
    return p


def add_heading(doc, text, level=1):
    p = doc.add_paragraph(style=f"Heading {level}")
    p.paragraph_format.keep_with_next = True
    p.paragraph_format.space_before = Pt(12 if level == 1 else 8)
    p.paragraph_format.space_after = Pt(5)
    r = p.add_run(text)
    set_run_font(r, size=15 if level == 1 else 12, bold=True, color="000000")
    return p


def add_caption(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(8)
    r = p.add_run(text)
    set_run_font(r, size=8.5, color=MUTED)
    r.italic = True
    return p


def add_page_number(paragraph):
    paragraph.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    run = paragraph.add_run("Halaman ")
    set_run_font(run, size=8.5, color=MUTED)
    fld_char1 = OxmlElement("w:fldChar")
    fld_char1.set(qn("w:fldCharType"), "begin")
    instr_text = OxmlElement("w:instrText")
    instr_text.set(qn("xml:space"), "preserve")
    instr_text.text = " PAGE "
    fld_char2 = OxmlElement("w:fldChar")
    fld_char2.set(qn("w:fldCharType"), "end")
    run._r.append(fld_char1)
    run._r.append(instr_text)
    run._r.append(fld_char2)


def configure_styles(doc):
    styles = doc.styles
    normal = styles["Normal"]
    normal.font.name = "Arial"
    normal._element.rPr.rFonts.set(qn("w:ascii"), "Arial")
    normal._element.rPr.rFonts.set(qn("w:hAnsi"), "Arial")
    normal.font.size = Pt(10.5)
    normal.font.color.rgb = RGBColor.from_string(TEXT)

    title = styles["Title"]
    title.font.name = "Arial"
    title._element.rPr.rFonts.set(qn("w:ascii"), "Arial")
    title._element.rPr.rFonts.set(qn("w:hAnsi"), "Arial")
    title.font.size = Pt(25)
    title.font.bold = True
    title.font.color.rgb = RGBColor(0, 0, 0)

    for level, size in ((1, 15), (2, 12)):
        style = styles[f"Heading {level}"]
        style.font.name = "Arial"
        style._element.rPr.rFonts.set(qn("w:ascii"), "Arial")
        style._element.rPr.rFonts.set(qn("w:hAnsi"), "Arial")
        style.font.size = Pt(size)
        style.font.bold = True
        style.font.color.rgb = RGBColor(0, 0, 0)


def add_document_control(doc):
    rows = [
        ("Nomor dokumen", "LGU-GLD-T1-CERT-2026-001"),
        ("Revisi", "0.1"),
        ("Tanggal", "15 September 2026"),
        ("Status", "Untuk evaluasi PT Pertamina Patra Niaga"),
        ("Disiapkan oleh", "LAPI Ganesha Utama bersama Lab IoT/Instrumentation and Computation ITB"),
        ("Ditujukan kepada", "PT Pertamina Patra Niaga"),
    ]
    table = doc.add_table(rows=len(rows), cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    set_table_borders(table)
    for i, (label, value) in enumerate(rows):
        table.rows[i].cells[0].text = label
        table.rows[i].cells[1].text = value
        table.rows[i].cells[0].width = Inches(1.65)
        table.rows[i].cells[1].width = Inches(4.85)
        set_cell_shading(table.rows[i].cells[0], PALE_GRAY)
        format_cell(table.rows[i].cells[0], bold=True, size=9.2)
        format_cell(table.rows[i].cells[1], size=9.2)


def build_document():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    tmp_dir = ROOT / "tmp" / "termin1_cert_assets"
    proto1 = prepare_image(PROTOTYPE_IMAGE_1, tmp_dir / "proto1.jpg", max_width=1400) if PROTOTYPE_IMAGE_1.exists() else None
    proto3 = prepare_image(PROTOTYPE_IMAGE_3, tmp_dir / "proto3.jpg", max_width=1600) if PROTOTYPE_IMAGE_3.exists() else None

    doc = Document()
    configure_styles(doc)
    section = doc.sections[0]
    section.page_width = Inches(8.2677)
    section.page_height = Inches(11.6929)
    section.top_margin = Inches(0.7)
    section.bottom_margin = Inches(0.65)
    section.left_margin = Inches(0.75)
    section.right_margin = Inches(0.75)

    header = section.header.paragraphs[0]
    header.text = "GLD TAHAP 2   |   TERMIN 1 SERTIFIKASI (40%)"
    header.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    for run in header.runs:
        set_run_font(run, size=8.2, bold=True, color=CHARCOAL)
    add_page_number(section.footer.paragraphs[0])

    # Cover
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(80)
    p.paragraph_format.space_after = Pt(12)
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("LAPORAN PEMENUHAN DELIVERABLE TERMIN 1")
    set_run_font(r, size=24, bold=True, color="000000")

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(22)
    r = p.add_run("Program Sertifikasi Hazardous Area (ATEX / IECEx) Gas Leak Detector — GLD Tahap 2")
    set_run_font(r, size=15, bold=False, color=CHARCOAL)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(34)
    r = p.add_run("MATERI EVALUASI TERMIN 1 SEBESAR 40 PERSEN")
    set_run_font(r, size=11.5, bold=True, color=TEAL)

    add_document_control(doc)

    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(34)
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("CATATAN SIFAT DOKUMEN")
    set_run_font(r, size=9.5, bold=True, color=MUTED)
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(
        "Laporan ini menyajikan seluruh bukti dan kekurangan yang teridentifikasi terhadap syarat Termin 1 "
        "sertifikasi apa adanya. Penilaian pemenuhan dan keputusan kesiapan pembayaran sepenuhnya "
        "merupakan evaluasi PT Pertamina Patra Niaga."
    )
    set_run_font(r, size=10.3, color=TEXT)

    doc.add_page_break()

    # 1 Ringkasan
    add_heading(doc, "1 Ringkasan", 1)
    add_paragraph(
        doc,
        "Tujuan laporan. Dokumen ini menyampaikan status pemenuhan syarat Termin 1 pada skema pembayaran "
        "dua termin proyek sertifikasi ATEX/IECEx Gas Leak Detector (GLD, Node Sensor) — Termin 1 sebesar "
        "40 persen dari nilai SPK sertifikasi. Laporan menampilkan seluruh bukti yang tersedia di sisi tim "
        "pengembang serta kekurangan yang masih teridentifikasi terhadap syarat kontraktual, tanpa menyimpulkan "
        "sendiri layak atau tidaknya pengajuan — keputusan tersebut diserahkan kepada evaluasi PT Pertamina "
        "Patra Niaga.",
        bold_lead="Tujuan laporan. ",
    )
    add_paragraph(
        doc,
        "Konteks proyek. Program sertifikasi mencakup 4 jalur paralel — ATEX (Directive 2014/34/EU, "
        "Kategori 2G Zona 1), IP66/67 (IEC 60529), EMC (EN 61000-6-2/-4), dan RF (ETSI/SDPPI) — untuk "
        "perangkat GLD (Node Sensor) saja; Cluster Head dan Gateway berada di luar lingkup proyek sertifikasi "
        "maupun RAB. Proyek aktif sejak Kick-Off 12 Juni 2026 dengan estimasi durasi keseluruhan 5 sampai "
        "8 bulan menuju uji laboratorium terakreditasi internasional.",
        bold_lead="Konteks proyek. ",
    )
    rows = [
        ("1", "Prototipe enclosure GLD tersedia", "SEBAGIAN", "Unit fisik terakit dan terfoto; identitas sampel/nomor seri/revisi belum ditetapkan formal."),
        ("2", "Prototipe telah diuji (mekanik/termal/sealing/fault)", "BELUM TERSEDIA", "Belum ditemukan protokol dan hasil uji khusus enclosure yang traceable."),
        ("3", "Ada iterasi perbaikan desain berbasis hasil uji", "BELUM TERSEDIA", "Belum ada log iterasi Rev A ke Rev B yang merujuk temuan uji."),
        ("4", "Disaksikan dan divalidasi Pertamina", "BELUM TERSEDIA", "Belum ada witness sheet/berita acara khusus uji enclosure; kunjungan yang ada bersifat pembahasan desain."),
        ("5", "Urutan sebelum uji lab terakreditasi", "TERSEDIA", "Sertifikasi masih tahap persiapan dokumen; sampel belum dikirim ke laboratorium sehingga urutan tahap masih terjaga."),
        ("6", "Berita acara", "BELUM ADA", "Notulen rapat tersedia, tetapi belum ada berita acara validasi hasil uji yang ditandatangani."),
        ("7", "Laporan pekerjaan Termin 1", "TERSEDIA", "Laporan ini adalah laporan pekerjaan yang dimaksud, disusun dari seluruh bukti yang ada di repo per 15 September 2026."),
    ]
    add_table(doc, ["No", "Syarat Termin 1", "Status", "Ringkasan bukti/kekurangan"], rows, [0.35, 1.85, 1.05, 3.6], font_size=8.5, status_col=2)

    doc.add_page_break()

    # 2 Dasar kontraktual
    add_heading(doc, "2 Dasar Kontraktual", 1)
    add_paragraph(
        doc,
        "Termin 1 pada skema pembayaran dua termin proyek sertifikasi bernilai 40 persen dari harga SPK "
        "sertifikasi. Milestone ini disyaratkan tercapai apabila seluruh kondisi berikut terpenuhi: (1) tersedia "
        "prototipe enclosure gas leak detector; (2) prototipe telah diuji; (3) hasil pengujian menghasilkan atau "
        "menutup iterasi perbaikan desain; (4) pengujian dan hasil iterasi disaksikan serta divalidasi oleh "
        "Pertamina; (5) tahap tersebut selesai sebelum pengujian dan sertifikasi di laboratorium terakreditasi "
        "internasional; dan (6) pelaksanaan dituangkan dalam berita acara dan laporan pekerjaan."
    )
    add_paragraph(
        doc,
        "Termin ini berbeda dari Termin 1 pada SPK field testing (20 persen) yang dinilai pada laporan terpisah "
        "(`Laporan_Pemenuhan_Deliverable_Termin_1_FieldTesting_GLD_Rev02`). Keduanya berjalan pada dua SPK/jalur "
        "kerja yang berbeda — sertifikasi hazardous area versus pilot/field testing sistem — sehingga bukti "
        "pemenuhannya juga dievaluasi terpisah."
    )

    doc.add_page_break()

    # 3 Matriks bukti
    add_heading(doc, "3 Matriks Bukti Pemenuhan per Syarat", 1)
    add_paragraph(
        doc,
        "Bagian ini merinci bukti yang ditemukan dan kekurangan yang teridentifikasi untuk setiap syarat pada "
        "Bagian 2, berdasarkan audit repo dokumentasi proyek per 15 September 2026."
    )

    def sub(no, title, status, bukti, kekurangan):
        add_heading(doc, f"3.{no} {title} — {status}", 2)
        for run in doc.paragraphs[-1].runs:
            set_run_font(run, size=11.5, bold=True, color=status_color(status))
        add_paragraph(doc, bukti, bold_lead="Bukti yang ditemukan. ")
        add_paragraph(doc, kekurangan, bold_lead="Kekurangan teridentifikasi. ")

    sub(
        1, "Prototipe enclosure GLD tersedia", "SEBAGIAN",
        "Bukti yang ditemukan. Tujuh foto perakitan pada `Sumber Dokumen/sertifikasi-atex-gld-v2-2026/GLD/`, "
        "tiga di antaranya menunjukkan urutan perakitan motherboard, pemasangan delapan sensor, hingga unit "
        "terakit lengkap (metadata foto utama tercatat 26 Agustus 2026). Desain mekanik pendukung tersedia pada "
        "`ATEX CASING v2` (STEP/OBJ) dan `Desain_Bracket_L_UBolt_GLD_Mounting.pdf`.",
        "Belum ada identitas unit/nomor seri, revisi desain, konfigurasi hardware-firmware yang terkunci, "
        "kondisi siap-uji, maupun lembar identifikasi sampel yang ditandatangani.",
    )
    sub(
        2, "Prototipe telah diuji", "BELUM TERSEDIA",
        "Bukti yang ditemukan. Bukti pengujian fungsi sistem, dataset gas, komunikasi LoRa, dan chamber gas "
        "tersedia dan menunjukkan kematangan fungsi sistem secara umum. Proposal sertifikasi formal juga sudah "
        "menetapkan jenis pre-compliance test yang direncanakan.",
        "Tidak ditemukan protokol dan hasil uji khusus enclosure: inspeksi mekanik/dimensi, uji termal/hotspot, "
        "simulasi sealing atau IP pra-uji, maupun uji fault condition. Bukti kematangan fungsi sistem di atas "
        "tidak menggantikan pengujian enclosure ini.",
    )
    sub(
        3, "Ada iterasi perbaikan desain berbasis hasil uji", "BELUM TERSEDIA",
        "Bukti yang ditemukan. Terdapat file desain `ATEX CASING v2` dan desain bracket U-bolt sebagai versi "
        "desain terkini.",
        "Desain tersebut terutama memodelkan assembly mounting/bracket, bukan riwayat iterasi enclosure. Belum "
        "ada change log Revisi A ke Revisi B yang merujuk temuan uji, tindakan koreksi, bukti implementasi, dan "
        "hasil uji ulang.",
    )
    sub(
        4, "Disaksikan dan divalidasi Pertamina", "BELUM TERSEDIA",
        "Bukti yang ditemukan. Notulen 6 Agustus 2026 (Lab IoT ITB) dan notulen kunjungan RU IV Cilacap "
        "menunjukkan keterlibatan aktif Pertamina dalam pembahasan desain, pemasangan, dan arah sertifikasi.",
        "Kunjungan tersebut adalah forum pembahasan desain dan progres, bukan witness uji enclosure. Belum ada "
        "witness sheet, daftar hadir sesi uji enclosure, pernyataan hasil diterima/ditolak, catatan komentar dan "
        "status penutupannya, atau tanda tangan pejabat/perwakilan Pertamina untuk validasi khusus ini.",
    )
    sub(
        5, "Selesai sebelum uji laboratorium terakreditasi", "TERSEDIA",
        "Bukti yang ditemukan. Status proyek per pertengahan September 2026 menyatakan sertifikasi masih pada "
        "tahap persiapan dokumen; belum ada klaim maupun jadwal pengiriman sampel ke laboratorium terakreditasi.",
        "Sesi pre-compliance dan witness (Syarat 2–4) tetap perlu dijadwalkan dan ditutup sebelum sampel "
        "benar-benar dikirim, agar urutan tahap ini tidak terlanggar saat proses berlanjut.",
    )
    sub(
        6, "Berita acara", "BELUM ADA",
        "Bukti yang ditemukan. Notulen rapat (12 Juni, 6 Agustus, kunjungan RU IV) tersedia sebagai rekaman "
        "diskusi.",
        "Notulen pembahasan bukan berita acara validasi hasil uji. Diperlukan berita acara khusus dengan hasil "
        "keputusan eksplisit, lampiran bukti uji, dan tanda tangan para pihak. Template kerja tersedia di "
        "`Template_Berita_Acara_Validasi_Prototipe.md` namun belum diisi karena data uji pendasarnya belum ada.",
    )
    sub(
        7, "Laporan pekerjaan Termin 1", "TERSEDIA",
        "Bukti yang ditemukan. Dokumen ini disusun sebagai laporan pekerjaan Termin 1 sertifikasi, merangkum "
        "seluruh bukti dan kekurangan di atas beserta register bukti pada Bagian 5.",
        "Laporan ini melaporkan status apa adanya; ia tidak dapat menggantikan bukti uji, witness, maupun "
        "berita acara yang secara kontraktual disyaratkan pada Syarat 2 sampai 4 dan 6.",
    )

    if proto3:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.add_run().add_picture(str(proto3), width=Inches(2.9))
        add_caption(doc, "Gambar 1 Unit GLD terakit dengan enclosure, sensor cartridge, antena, dan modul alarm (dokumentasi 26 Agustus 2026)")

    doc.add_page_break()

    # 4 Progres sertifikasi
    add_heading(doc, "4 Progres Program Sertifikasi Secara Keseluruhan", 1)
    add_paragraph(
        doc,
        "Sebagai konteks tambahan di luar syarat kontraktual Termin 1, tim pengembang memantau progres program "
        "sertifikasi dengan dua metrik yang tidak saling menggantikan:"
    )
    rows = [
        ("Progres keseluruhan proyek (5 fase x 4 track, bottom-up)", "≈ 20% (per 5 September 2026)", "Metrik paling konservatif — memasukkan fase Uji Laboratorium Terakreditasi (bobot 41,7% dari total durasi) yang belum dimulai sama sekali."),
        ("Kesiapan dokumen ATEX (checklist teknis 29 item)", "≈ 43%", "Murni kelengkapan dokumentasi/checklist teknis, tidak termasuk pelaksanaan pengujian."),
    ]
    add_table(doc, ["Metrik", "Nilai", "Definisi dan batasan"], rows, [2.15, 1.5, 3.35], font_size=8.9)
    add_paragraph(
        doc,
        "Kedua metrik ini adalah indikator kemajuan rekayasa dan administrasi internal, bukan pengganti "
        "penilaian pemenuhan syarat Termin 1 pada Bagian 2 dan 3. Skema klasifikasi area berbahaya yang "
        "ditargetkan proposal — Zona 1, Kategori 2G, Grup II, kelas suhu T4 (≤135°C) — sudah eksplisit; grup "
        "gas spesifik (rekomendasi tim: IIC) dan metode proteksi (Ex i atau Ex d) masih terbuka dan menjadi "
        "bagian dari pekerjaan uji lanjutan. Detail lengkap Kurva-S dan gap analysis per track ada di "
        "`Dashboard_Sertifikasi_GLD_ATEX_IECEx.html`."
    )

    if BRACKET_IMAGE.exists():
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.add_run().add_picture(str(BRACKET_IMAGE), width=Inches(6.3))
        add_caption(doc, "Gambar 2 Basis desain \"ATEX Casing v2\" dan bracket L / U-bolt untuk mounting GLD")

    doc.add_page_break()

    # 5 Register bukti
    add_heading(doc, "5 Register Bukti", 1)
    rows = [
        ("E-01", "Foto perakitan prototipe GLD (26 Agu 2026)", "3 foto urutan perakitan + 4 foto komponen di `sertifikasi-atex-gld-v2-2026/GLD/`."),
        ("E-02", "Desain \"ATEX Casing v2\" (STEP/OBJ) dan bracket L/U-bolt", "Basis desain mekanik enclosure dan mounting, `GLD U Bolt Bracket/`."),
        ("E-03", "Dokumen spesifikasi input dan parameter EMC", "`Dokumen_spesifikasi_input_2.docx`, `Parameter spesifikasi EMC_lengkap.docx`."),
        ("E-04", "Technical Datasheet GasleakDetector Revision 4.0", "Spesifikasi fungsional dan teknis perangkat yang menjadi objek sertifikasi."),
        ("E-05", "Proposal Sertifikasi ATEX/IP/EMC/RF (21 Februari 2026)", "Dasar lingkup, target klasifikasi Zona 1/2G/T4, dan rencana pre-compliance test."),
        ("E-06", "Notulensi Kick-Off Meeting (12 Juni 2026)", "Titik mulai proyek sertifikasi dan penyelarasan lingkup awal."),
        ("E-07", "Notulen Meeting GLD 6 Agustus 2026", "Pembahasan desain mekanik dan progres bersama Pertamina di Lab IoT ITB — bukan witness uji enclosure."),
        ("E-08", "Notulen kunjungan Pertamina RU IV Cilacap", "Pembahasan instalasi dan sertifikasi terkait lokasi, bukan witness uji enclosure."),
        ("E-09", "Dashboard Sertifikasi GLD ATEX/IECEx", "Kurva-S, gap analysis 4 track, dan rubrik interpretasi progres."),
        ("E-10", "Checklist dan analisis kekurangan sertifikasi", "`checklist-sertifikasi.html`, `laporan-analisis-kekurangan.html`, `status-kekurangan.html`."),
        ("E-11", "Persiapan_Termin_1.md dan 3 template kerja", "Matriks gap awal (10 September 2026) dan template log uji, berita acara, serta laporan pekerjaan."),
    ]
    add_table(doc, ["ID", "Bukti", "Keterangan"], rows, [0.5, 2.6, 3.65], font_size=8.5)

    add_heading(doc, "6 Dokumen yang Masih Perlu Disusun", 1)
    add_paragraph(
        doc,
        "Daftar berikut adalah dokumen kontraktual Termin 1 yang templatenya sudah tersedia tetapi belum dapat "
        "diisi karena data pendasarnya (hasil uji enclosure dan witness) belum ada."
    )
    rows = [
        ("Log Uji dan Iterasi Enclosure", "`Template_Log_Uji_dan_Iterasi_Enclosure.md`", "Menunggu pelaksanaan protokol uji enclosure (mekanik, termal/hotspot, sealing/IP pra-uji, fault condition)."),
        ("Berita Acara Validasi Prototipe", "`Template_Berita_Acara_Validasi_Prototipe.md`", "Menunggu sesi witness Pertamina atas hasil uji enclosure di atas."),
        ("Identitas sampel dan design freeze", "Belum ada dokumen", "ID sampel, revisi mekanik/PCB/firmware, tanggal rakit, PIC, dan foto enam sisi + internal."),
    ]
    add_table(doc, ["Dokumen", "Status berkas", "Menunggu"], rows, [1.95, 2.05, 2.75], font_size=8.9)

    doc.add_page_break()

    # 7 Penutup
    add_heading(doc, "7 Penutup", 1)
    add_paragraph(
        doc,
        "Laporan ini menyajikan seluruh bukti yang tersedia di sisi tim pengembang serta kekurangan yang masih "
        "teridentifikasi terhadap ketujuh syarat Termin 1 sertifikasi sebagaimana diuraikan pada Bagian 2 dan 3. "
        "Tim pengembang tidak menyimpulkan sendiri apakah paket ini layak atau belum layak diajukan untuk "
        "pembayaran 40 persen — penilaian pemenuhan syarat dan keputusan tersebut sepenuhnya berada pada "
        "evaluasi PT Pertamina Patra Niaga, dengan matriks Bagian 3 sebagai acuan tinjau per syarat."
    )
    add_paragraph(
        doc,
        "Apabila PT Pertamina Patra Niaga memerlukan sesi uji dan witness bersama untuk menutup Syarat 2 sampai "
        "4 dan 6, tim pengembang siap menjadwalkan pelaksanaan mengikuti kerangka kerja pada "
        "`Persiapan_Termin_1.md` (identitas prototipe, protokol uji, log iterasi, witness, hingga dokumen serah "
        "terima)."
    )

    add_heading(doc, "8 Lembar Evaluasi", 1)
    add_paragraph(
        doc,
        "Lembar ini disediakan untuk mencatat hasil evaluasi PT Pertamina Patra Niaga atas laporan ini, tanpa "
        "mengandaikan hasil evaluasi tersebut."
    )
    rows = [
        ("Disiapkan oleh", "LAPI Ganesha Utama", "Nama dan jabatan\n\n\nTanda tangan dan tanggal"),
        ("Diverifikasi oleh", "Lab IoT/Instrumentation and Computation ITB", "Nama dan jabatan\n\n\nTanda tangan dan tanggal"),
        ("Dievaluasi oleh", "PT Pertamina Patra Niaga", "Nama dan jabatan\n\n\nTanda tangan dan tanggal"),
    ]
    add_table(doc, ["Peran", "Pihak", "Pengesahan"], rows, [1.25, 2.25, 3.25], font_size=9.3)

    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(18)
    p.paragraph_format.space_after = Pt(4)
    r = p.add_run("Hasil evaluasi (diisi oleh PT Pertamina Patra Niaga)")
    set_run_font(r, size=10.5, bold=True)
    for choice in [
        "[  ] Syarat Termin 1 dinilai terpenuhi — diproses untuk pembayaran 40 persen",
        "[  ] Syarat Termin 1 dinilai terpenuhi sebagian — diproses dengan catatan/syarat tambahan",
        "[  ] Syarat Termin 1 dinilai belum terpenuhi — memerlukan uji dan witness lanjutan sebagaimana Bagian 6",
    ]:
        add_paragraph(doc, choice, size=10.2)

    doc.add_page_break()
    add_heading(doc, "9 Referensi Dokumen", 1)
    refs = [
        "Ketentuan Cara Pembayaran Termin 1 (40 persen) pada SPK proyek sertifikasi ATEX/IECEx GLD.",
        "PROPOSAL SERTIFIKASI GAS LEAK DETECTION SYSTEM (Hazardous Area Compliance — ATEX, IP, EMC, RF), 21 Februari 2026.",
        "Notulensi Kick Off Meeting Pertamina, 12 Juni 2026.",
        "Notulen Meeting GLD, 6 Agustus 2026, Lab IoT, Instrumentation and Computations, Gedung Laboratorium Fisika Terpadu, Institut Teknologi Bandung.",
        "Notulen kunjungan Pertamina RU IV Cilacap, 9-10 Agustus 2026.",
        "Foto perakitan prototipe GLD, 26 Agustus 2026, `sertifikasi-atex-gld-v2-2026/GLD/`.",
        "Desain \"ATEX Casing v2\" dan bracket L/U-bolt, `GLD U Bolt Bracket/`.",
        "Technical Datasheet GasleakDetector Revision 4.0, 4 September 2026.",
        "Dashboard Sertifikasi GLD ATEX/IECEx dan checklist/gap analysis pendukung.",
        "Persiapan_Termin_1.md dan template kerja pendukung, 10 September 2026.",
    ]
    for i, ref in enumerate(refs, 1):
        add_paragraph(doc, f"{i}. {ref}", size=9.4)

    doc.core_properties.title = "Laporan Pemenuhan Deliverable Termin 1 Sertifikasi GLD"
    doc.core_properties.subject = "Materi evaluasi Termin 1 sertifikasi sebesar 40 persen"
    doc.core_properties.author = "LAPI Ganesha Utama bersama Lab IoT/Instrumentation and Computation ITB"
    doc.core_properties.keywords = "GLD, Termin 1, Sertifikasi, ATEX, IECEx, Pertamina"
    doc.save(OUT_DOCX)
    print(OUT_DOCX)


if __name__ == "__main__":
    build_document()
