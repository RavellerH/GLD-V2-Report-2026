"""Paket diskusi TÜV SÜD (GLD V2) — 00 pengantar produk + lampiran 01–05 + PDF gabungan.

Tanpa nama perusahaan. Aset gambar: scripts/assets/tuv_sud_gmi/ (figures.json).
"""
import io, json, subprocess
from pathlib import Path
from PIL import Image, ImageChops, ImageDraw, ImageFont
from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor
from pypdf import PdfReader, PdfWriter

ROOT = Path(__file__).resolve().parent.parent
A = ROOT / "scripts/assets/tuv_sud_gmi"
OUT = ROOT / "Paket Meeting TUV SUD 26November2026/GMI"
UNIT = ROOT / "scripts/assets/balongan_13nov/unit_gld_4_tampak.jpg"
FIG = json.loads((A / "figures.json").read_text(encoding="utf-8"))
TANGGAL = "26 November 2026"
REV = "0.2"
NAVY = RGBColor(0x1F, 0x3A, 0x5F)
GREY = RGBColor(0x59, 0x59, 0x59)
WARN = RGBColor(0x9C, 0x3B, 0x00)
TW = 16.6  # lebar area teks (cm)
F_R = r"C:\Windows\Fonts\calibri.ttf"
F_B = r"C:\Windows\Fonts\calibrib.ttf"


TR = {}  # terjemahan string helper/diagram (diisi oleh generator versi bahasa lain)


def tr(x):
    return TR.get(x, x)


# ------------------------------------------------------------------ helpers
def shade(cell, color):
    tcPr = cell._tc.get_or_add_tcPr()
    s = OxmlElement("w:shd"); s.set(qn("w:val"), "clear"); s.set(qn("w:color"), "auto"); s.set(qn("w:fill"), color)
    tcPr.append(s)


def field(run, code):
    for t, txt in (("begin", None), (None, code), ("end", None)):
        if t:
            e = OxmlElement("w:fldChar"); e.set(qn("w:fldCharType"), t)
        else:
            e = OxmlElement("w:instrText"); e.set(qn("xml:space"), "preserve"); e.text = txt
        run._r.append(e)


def new_doc(docno, short):
    d = Document()
    d._short = short
    s = d.sections[0]
    s.page_width, s.page_height = Cm(21), Cm(29.7)
    s.left_margin = s.right_margin = Cm(2.2)
    s.top_margin, s.bottom_margin = Cm(2.8), Cm(2.4)
    s.header_distance, s.footer_distance = Cm(1.2), Cm(1.1)
    st = d.styles["Normal"]; st.font.name = "Calibri"; st.font.size = Pt(10.5)
    st.font.color.rgb = RGBColor(0x26, 0x26, 0x26)
    st.element.rPr.rFonts.set(qn("w:eastAsia"), "Calibri")
    pf = st.paragraph_format; pf.space_after = Pt(6); pf.line_spacing = 1.15
    pf.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    for name, size, before in (("Heading 1", 13.5, 16), ("Heading 2", 11, 10)):
        h = d.styles[name]; h.font.name = "Calibri"; h.font.size = Pt(size); h.font.bold = True
        h.font.color.rgb = NAVY
        rf = h.element.rPr.rFonts
        for k in ("w:asciiTheme", "w:hAnsiTheme", "w:eastAsiaTheme", "w:cstheme"):
            if rf.get(qn(k)) is not None:
                del rf.attrib[qn(k)]
        h.paragraph_format.space_before = Pt(before); h.paragraph_format.space_after = Pt(6)
        h.paragraph_format.keep_with_next = True; h.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
        if name == "Heading 1":
            border(h.element.get_or_add_pPr(), "bottom", "C9D3E0", 4, 3)
    for name in ("List Bullet", "List Number"):
        d.styles[name].paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
    hp = s.header.paragraphs[0]; hp.style = d.styles["Normal"]; hp.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r = hp.add_run("GAS LEAK DETECTOR GLD V2"); r.font.size = Pt(8); r.bold = True; r.font.color.rgb = NAVY
    r = hp.add_run(tr("   |   Diskusi Sertifikasi ATEX/IECEx \u2014 T\u00dcV S\u00dcD")); r.font.size = Pt(8); r.font.color.rgb = GREY
    hp.add_run("\t")
    r = hp.add_run(short); r.font.size = Pt(8); r.font.color.rgb = GREY
    hp.paragraph_format.tab_stops.add_tab_stop(Cm(TW), alignment=2)
    border(hp._p.get_or_add_pPr(), "bottom", "1F3A5F", 6, 4)
    fp = s.footer.paragraphs[0]; fp.style = d.styles["Normal"]; fp.alignment = WD_ALIGN_PARAGRAPH.LEFT
    border(fp._p.get_or_add_pPr(), "top", "C9D3E0", 4, 4)
    r = fp.add_run(f"{docno}   \u00b7   Rev. {REV}   \u00b7   {TANGGAL}   \u00b7   " + tr("RAHASIA")); r.font.size = Pt(8); r.font.color.rgb = GREY
    fp.add_run("\t")
    r = fp.add_run(tr("Halaman ")); r.font.size = Pt(8); r.font.color.rgb = GREY
    r = fp.add_run(); r.font.size = Pt(8); r.bold = True; field(r, "PAGE")
    r = fp.add_run(" / "); r.font.size = Pt(8); r.font.color.rgb = GREY
    r = fp.add_run(); r.font.size = Pt(8); field(r, "NUMPAGES")
    fp.paragraph_format.tab_stops.add_tab_stop(Cm(TW), alignment=2)
    return d


def border(pPr, side, color, sz, space):
    b = pPr.find(qn("w:pBdr"))
    if b is None:
        b = OxmlElement("w:pBdr"); pPr.append(b)
    e = OxmlElement("w:" + side)
    for k, v in (("val", "single"), ("sz", str(sz)), ("space", str(space)), ("color", color)):
        e.set(qn("w:" + k), v)
    b.append(e)


def tbl_borders(t, spec):
    tblPr = t._tbl.tblPr
    for old in tblPr.findall(qn("w:tblBorders")):
        tblPr.remove(old)
    b = OxmlElement("w:tblBorders")
    for side in ("top", "left", "bottom", "right", "insideH", "insideV"):
        e = OxmlElement("w:" + side)
        val, sz, col = spec.get(side, ("nil", 0, "auto"))
        e.set(qn("w:val"), val)
        if val != "nil":
            e.set(qn("w:sz"), str(sz)); e.set(qn("w:color"), col); e.set(qn("w:space"), "0")
        b.append(e)
    tblPr.append(b)


def tbl_margins(t, tb=50, lr=100):
    tblPr = t._tbl.tblPr
    m = OxmlElement("w:tblCellMar")
    for side, v in (("top", tb), ("left", lr), ("bottom", tb), ("right", lr)):
        e = OxmlElement("w:" + side); e.set(qn("w:w"), str(v)); e.set(qn("w:type"), "dxa"); m.append(e)
    tblPr.append(m)


def title_block(d, title, subtitle, docno, purpose):
    short = d._short
    label = tr("DOKUMEN PEMBUKA") if not short[:2].isdigit() else tr("LAMPIRAN") + f" {short[:2]}"
    p = d.add_paragraph(); r = p.add_run(label); r.bold = True; r.font.size = Pt(9); r.font.color.rgb = RGBColor(0x2B, 0x5F, 0xCB)
    rPr = r._r.get_or_add_rPr(); sp = OxmlElement("w:spacing"); sp.set(qn("w:val"), "30"); rPr.append(sp)
    p.paragraph_format.space_after = Pt(2); p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p = d.add_paragraph(); r = p.add_run(title); r.bold = True; r.font.size = Pt(22); r.font.color.rgb = NAVY
    p.paragraph_format.space_after = Pt(2); p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p = d.add_paragraph(); r = p.add_run(subtitle); r.font.size = Pt(11.5); r.font.color.rgb = GREY
    p.paragraph_format.space_after = Pt(10); p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
    border(p._p.get_or_add_pPr(), "bottom", "1F3A5F", 12, 6)
    t = table(d, [
        [tr("Produk"), tr("Gas Leak Detector (GLD) V2 \u2014 detektor gas tipe titik (fixed point)")],
        [tr("Nomor dokumen"), docno],
        [tr("Revisi / tanggal"), f"{REV} / {TANGGAL}"],
        [tr("Tujuan"), purpose],
        [tr("Sumber data"), tr("Dossier IECEx/ATEX Certification Information Requirements GLD V2 (Rev. 2.1\u20132.3) dan data proyek terkini")],
    ], [3.6, TW - 3.6], header=False, label_col=True, size=9, zebra=False)
    tbl_borders(t, {"bottom": ("single", 4, "C9D3E0")})


def table(d, rows, widths, header=True, label_col=False, size=9.5, zebra=True):
    t = d.add_table(rows=len(rows), cols=len(rows[0]))
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    tblPr = t._tbl.tblPr
    lay = OxmlElement("w:tblLayout"); lay.set(qn("w:type"), "fixed"); tblPr.append(lay)
    tbl_borders(t, {"top": ("single", 8, "1F3A5F"), "bottom": ("single", 8, "1F3A5F"), "insideH": ("single", 4, "D5DCE6")})
    tbl_margins(t)
    grid = t._tbl.tblGrid
    for gc, w in zip(grid.findall(qn("w:gridCol")), widths):
        gc.set(qn("w:w"), str(int(w * 567)))
    for i, row in enumerate(rows):
        tr = t.rows[i]._tr
        trPr = tr.get_or_add_trPr(); trPr.append(OxmlElement("w:cantSplit"))
        if header and i == 0:
            trPr.append(OxmlElement("w:tblHeader"))
        body_i = i - (1 if header else 0)
        for j, val in enumerate(row):
            c = t.cell(i, j); c.width = Cm(widths[j])
            p = c.paragraphs[0]; p.paragraph_format.space_after = Pt(0); p.paragraph_format.line_spacing = 1.05
            p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(val); r.font.size = Pt(size)
            if header and i == 0:
                r.bold = True; r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF); shade(c, "1F3A5F")
            else:
                if zebra and body_i % 2 == 1:
                    shade(c, "F4F6F9")
                if label_col and j == 0:
                    r.bold = True; r.font.color.rgb = NAVY
    sp = d.add_paragraph(); sp.paragraph_format.space_after = Pt(4)
    return t


def bullets(d, items, style="List Bullet"):
    for it in items:
        p = d.add_paragraph(style=style); p.paragraph_format.space_after = Pt(3)
        if isinstance(it, tuple):
            r = p.add_run(it[0]); r.bold = True; r.font.color.rgb = NAVY; p.add_run(it[1])
        else:
            p.add_run(it)


def note(d, text, color=WARN, fill="FFF6EC"):
    t = d.add_table(rows=1, cols=1)
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_borders(t, {"left": ("single", 24, "C0601A")})
    tbl_margins(t, 90, 160)
    c = t.cell(0, 0); c.width = Cm(TW); shade(c, fill)
    p = c.paragraphs[0]; p.paragraph_format.space_after = Pt(0); p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r = p.add_run(text); r.font.size = Pt(9.5); r.bold = True; r.font.color.rgb = color
    sp = d.add_paragraph(); sp.paragraph_format.space_after = Pt(4)


def para(d, text, size=None, italic=False, color=None):
    p = d.add_paragraph(); r = p.add_run(text)
    if size: r.font.size = Pt(size)
    r.italic = italic
    if color: r.font.color.rgb = color
    return p


def crop_page(path):
    """Potong header/footer halaman sumber dan buang tepi putih."""
    im = Image.open(path).convert("RGB"); w, h = im.size
    im = im.crop((0, int(h * 0.058), w, int(h * 0.925)))
    bg = Image.new("RGB", im.size, (255, 255, 255))
    box = ImageChops.difference(im, bg).convert("L").point(lambda v: 255 if v > 18 else 0).getbbox()
    if box:
        pad = 12
        im = im.crop((max(0, box[0] - pad), max(0, box[1] - pad), min(im.width, box[2] + pad), min(im.height, box[3] + pad)))
    buf = io.BytesIO(); im.save(buf, "JPEG", quality=90); buf.seek(0)
    return buf, im.size


def figure(d, src, caption, max_w=TW, max_h=20.5, crop=True):
    if crop:
        buf, (w, h) = crop_page(src)
    else:
        buf = str(src); w, h = Image.open(src).size
    width = min(max_w, max_h * w / h)
    d.add_picture(buf, width=Cm(width))
    d.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
    d.paragraphs[-1].paragraph_format.keep_with_next = True
    p = d.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(caption); r.font.size = Pt(9); r.italic = True; r.font.color.rgb = GREY


def page_break(d):
    d.add_paragraph().add_run().add_break(WD_BREAK.PAGE)


def to_pdf(docx):
    pdf = docx.with_suffix(".pdf")
    ps = (f'$w=New-Object -ComObject Word.Application; $d=$w.Documents.Open("{docx}"); '
          f'$d.Fields.Update() | Out-Null; $d.SaveAs([ref]"{pdf}",[ref]17); $d.Close(); $w.Quit()')
    subprocess.run(["powershell", "-NoProfile", "-Command", ps], check=True)
    return pdf


# ------------------------------------------------------------------ diagram
def flow_diagram(path):
    W, H = 2000, 760
    im = Image.new("RGB", (W, H), "white"); dr = ImageDraw.Draw(im)
    fr, fb, fs = ImageFont.truetype(F_R, 30), ImageFont.truetype(F_B, 31), ImageFont.truetype(F_R, 25)
    navy, blue, grey, light = (31, 58, 95), (43, 95, 203), (110, 110, 110), (232, 238, 245)

    def box(x, y, w, h, t1, t2="", fill=light, col=navy):
        dr.rounded_rectangle([x, y, x + w, y + h], 18, fill=fill, outline=col, width=3)
        dr.text((x + w / 2, y + h / 2 - (16 if t2 else 0)), t1, font=fb, fill=col, anchor="mm")
        if t2:
            dr.text((x + w / 2, y + h / 2 + 22), t2, font=fs, fill=grey, anchor="mm")

    def arrow(x1, y1, x2, y2, col=navy):
        dr.line([x1, y1, x2, y2], fill=col, width=4)
        import math
        a = math.atan2(y2 - y1, x2 - x1)
        for s in (2.6, -2.6):
            dr.line([x2, y2, x2 - 20 * math.cos(a + s / 6), y2 - 20 * math.sin(a + s / 6)], fill=col, width=4)

    # batas peralatan (GLD)
    for i in range(70, 1530, 30):
        dr.line([i, 40, i + 16, 40], fill=blue, width=4); dr.line([i, 560, i + 16, 560], fill=blue, width=4)
    for j in range(40, 560, 30):
        dr.line([70, j, 70, j + 16], fill=blue, width=4); dr.line([1530, j, 1530, j + 16], fill=blue, width=4)
    dr.text((90, 62), tr("Batas peralatan yang diajukan sertifikasi — Node Sensor GLD V2 (enclosure Ex db)"), font=fb, fill=blue)
    y = 150
    box(110, y, 250, 120, tr("Udara sekitar"), tr("masuk lewat mesh SS"))
    arrow(360, y + 60, 410, y + 60)
    box(410, y, 230, 120, tr("Kipas DC"), tr("aliran ke sensor"))
    arrow(640, y + 60, 690, y + 60)
    box(690, y, 250, 120, tr("8 sensor MQ"), tr("metal-oxide"))
    arrow(940, y + 60, 990, y + 60)
    box(990, y, 230, 120, tr("ADC 24-bit"), tr("ADS1256, 500 ms"))
    arrow(1220, y + 60, 1270, y + 60)
    box(1270, y, 230, 120, tr("ESP32-S3"), tr("klasifikasi AI lokal"))
    y2 = 360
    box(1050, y2, 220, 130, tr("Alarm lokal"), tr("LED + buzzer"), fill=(255, 238, 230), col=(156, 59, 0))
    box(1290, y2, 210, 130, tr("Radio LoRa"), tr("920–923 MHz"))
    arrow(1385, 270, 1160, y2)
    arrow(1385, 270, 1395, y2)
    box(110, y2, 300, 130, tr("Terminal 24 VDC"), tr("maks. ±8 W, M20×1,5"))
    box(460, y2, 270, 130, tr("Grounding PE"), tr("stud eksternal"))
    box(780, y2, 220, 130, tr("RS-485"), tr("Modbus RTU (opsional)"))
    # luar batas
    box(1610, 360, 330, 130, tr("Cluster Head → Gateway"), tr("area aman / unclassified"), fill=(245, 245, 245), col=grey)
    arrow(1500, 425, 1610, 425, col=grey)
    box(1610, 560, 330, 120, tr("Server & dashboard"), tr("intranet lokasi"), fill=(245, 245, 245), col=grey)
    arrow(1775, 490, 1775, 560, col=grey)
    box(110, 620, 420, 110, tr("Adaptor 220 VAC → 24 VDC"), tr("di luar batas peralatan"), fill=(245, 245, 245), col=grey)
    arrow(260, 620, 260, 490, col=grey)
    dr.text((1610, 300), tr("Di luar lingkup sertifikasi"), font=fr, fill=grey)
    im.save(path)


# ================================================================== 00 PENGANTAR PRODUK
def build_00():
    no = "GLD/ATEX-IN/2026-001-ID"
    d = new_doc(no, "Pengantar Produk")
    title_block(d, "Pengantar Produk GLD V2", "Gambaran produk dan peta dokumen yang diminta TÜV SÜD", no,
                "Bahan pengantar rapat teknis dengan TÜV SÜD melalui Microsoft Teams, Kamis, 26 November 2026, pukul 14.30 WIB (13.30 waktu Tiongkok)")

    d.add_heading("1. Agenda pembahasan", level=1)
    para(d, "Dokumen ini mengawali diskusi dengan menguraikan produk yang akan disertifikasi, kemudian memetakan setiap "
            "permintaan TÜV SÜD ke lampiran yang menanggapinya.")
    table(d, [
        ["Bagian", "Isi", "Dokumen"],
        ["A. Produk", "Fungsi, cara kerja, konstruksi, spesifikasi, batas peralatan", "00 (dokumen ini) §2–5"],
        ["B. Lingkup sertifikasi", "Usulan klasifikasi Ex dan standar yang relevan", "00 §6"],
        ["C. Permintaan TÜV SÜD", "Gambar perakitan, panduan pengguna, target penandaan Ex, IP66, ISO 9001", "Lampiran 01–05"],
        ["D. Diskusi", "Pokok bahasan untuk menyepakati jalur sertifikasi", "00 §8"],
    ], [3.6, 8.9, 4.0])

    page_break(d)
    d.add_heading("2. Gambaran produk", level=1)
    para(d, "Gas Leak Detector (GLD) V2 adalah detektor kebocoran gas tipe titik berbasis IoT untuk area proses kilang "
            "minyak dan gas — unit proses, tank farm, pipe rack dan area bongkar muat. Satu unit memantau udara di "
            "sekitarnya secara terus-menerus, mengklasifikasikan kondisi gas langsung di dalam perangkat, membunyikan "
            "alarm lokal, dan mengirim status serta alarm secara nirkabel ke sistem pemantauan.")
    figure(d, UNIT, "Gambar 1 — Unit GLD V2 konfigurasi produksi saat ini, empat tampak (antena di atas base, beacon alarm di samping).",
           max_h=9.5, crop=False)

    d.add_heading("3. Cara kerja", level=1)
    dg = A / "diagram_alur_gld.png"; flow_diagram(dg)
    figure(d, dg, "Gambar 2 — Alur sinyal dan batas peralatan. Bagian di dalam garis putus-putus adalah objek sertifikasi.", crop=False, max_h=8)
    bullets(d, [
        ("Pengambilan sampel — ", "udara sekitar masuk melalui mesh stainless steel di tutup depan; kipas DC membantu aliran ke delapan sensor gas metal-oxide (MQ-2, MQ-3B, MQ-4, MQ-5, MQ-6, MQ-7B, MQ-8, MQ-135)."),
        ("Pengolahan — ", "sinyal sensor didigitalkan ADC 24-bit (ADS1256) setiap 500 ms dan diklasifikasikan oleh model AI di ESP32-S3 menjadi Clean Air, LPG atau H₂."),
        ("Alarm — ", "dua jalur paralel: LED dan buzzer di unit, serta notifikasi LoRa ke Cluster Head dan Gateway. Keputusan alarm tidak bergantung pada koneksi server."),
        ("Catu daya — ", "hanya 24 VDC kontinu. Tidak ada 220 VAC di dalam GLD; adaptor AC/DC berada di luar batas peralatan."),
    ])

    d.add_heading("4. Konstruksi", level=1)
    table(d, [
        ["Bagian", "Keterangan"],
        ["Enclosure", "Aluminium die-cast (ADC12) dengan tutup berulir dan O-ring; basis dari housing detektor gas komersial HIREP HRP-T1000-A yang dimodifikasi"],
        ["Inlet gas", "Pelat wire-mesh stainless steel di tutup depan (menggantikan kaca housing asli)"],
        ["Elektronik", "Main board V4 (ESP32-S3, ADC, LoRa E22-900MM22S, RS-485), papan terminal, 8 modul sensor MQ, kipas DC 5 V"],
        ["Alarm", "Beacon alarm 24 V (LED dan buzzer) di sisi kanan"],
        ["Antena", "Antena LoRa di permukaan atas base, konektor SMA"],
        ["Cable entry", "M20 × 1,5 untuk kabel 24 VDC (dua inti L+/L−); gland Ex d akan ditetapkan"],
        ["Pemasangan", "Pelat U-bolt 250 × 250 mm ke pipa 2 in/DN50 (OD 60,3 mm), baut M10"],
        ["Grounding", "Stud PE eksternal di samping cable gland"],
    ], [3.4, TW - 3.4])

    d.add_heading("5. Spesifikasi utama", level=1)
    table(d, [
        ["Parameter", "Nilai", "Status"],
        ["Catu daya", "24 VDC; maks. ±8 W (≈ 0,33 A)", "Terukur"],
        ["Dimensi / massa", "200 × 90 × 290 mm / 2,378 kg", "Data desain"],
        ["Sensor", "8 × MQ metal-oxide + SHT40 (suhu/kelembapan)", "Final"],
        ["Klasifikasi gas on-device", "Clean Air, LPG, H₂", "Final (versi model saat ini)"],
        ["Komunikasi", "LoRa 920–923 MHz; RS-485 Modbus RTU read-only 9600 8N1", "Final"],
        ["Suhu operasi", "−20 °C hingga +60 °C", "Batas atas dalam peninjauan (housing dasar +55 °C)"],
        ["Kelembapan", "5–95 % RH, non-kondensasi", "Data desain"],
        ["Ingress protection", "IP66", "Target, belum diuji"],
    ], [4.0, 7.0, 5.5])

    d.add_heading("6. Lingkup sertifikasi yang diusulkan", level=1)
    p = d.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("⟨Ex⟩ II 2G  Ex db IIC T4 Gb    −20 °C ≤ Ta ≤ +60 °C"); r.bold = True; r.font.size = Pt(14); r.font.color.rgb = NAVY
    table(d, [
        ["Elemen", "Usulan", "Alasan"],
        ["Objek", "Node Sensor GLD V2 saja", "Cluster Head dan Gateway dipasang di area aman"],
        ["Area", "Zone 1 (Category 2G, EPL Gb)", "Dipasang di area proses kilang yang terklasifikasi"],
        ["Proteksi", "Ex db — flameproof enclosure", "Enclosure die-cast; heater sensor (±0,75 W/sensor) tidak memungkinkan pemenuhan batas energi keselamatan intrinsik (Ex i)"],
        ["Kelompok gas", "IIC", "Hidrogen termasuk gas sasaran deteksi"],
        ["Kelas suhu", "T4 (≤ 135 °C)", "Pengukuran internal awal: titik terpanas ≈ 114 °C diekstrapolasi ke Ta +60 °C"],
        ["Debu", "Tidak diajukan", "Atmosfer gas saja"],
        ["Standar acuan", "IEC/EN 60079-0, 60079-1; IEC 60529 (IP)", "Edisi dan tambahan sesuai arahan TÜV SÜD"],
    ], [3.0, 5.2, 8.3])
    note(d, "Semua elemen di atas adalah usulan pemohon dan belum tersertifikasi. Klasifikasi final ditetapkan oleh lembaga sertifikasi.")

    d.add_heading("7. Peta permintaan TÜV SÜD", level=1)
    table(d, [
        ["Permintaan", "Lampiran", "Isi", "Status"],
        ["Assembly drawing", "01 Gambar Perakitan", "Konfigurasi acuan, register gambar, foto rakitan & pengukuran, gambar komponen, urutan perakitan, terminal, grounding, sensor", "Tersedia sebagian — gambar berdimensi terkendali unit produksi akan diterbitkan"],
        ["User manual", "02 Panduan Pengguna", "Spesifikasi, keselamatan, instalasi, commissioning, operasi, alarm, inspeksi, pemeliharaan, penghentian", "Draf"],
        ["Target penandaan Ex", "03 Target Penandaan Ex", "Usulan marking, arti tiap elemen, nameplate, evaluasi awal T4", "Usulan tersedia"],
        ["IP66", "04 Status IP66", "Target, antarmuka sealing, rencana verifikasi IEC 60529", "Target, belum diuji"],
        ["Sertifikat ISO 9001", "05 Status ISO 9001", "Status sertifikasi produsen, dokumen mutu, jalur QAR/QAN", "Dalam proses"],
    ], [3.0, 3.1, 6.4, 4.0], size=9)

    d.add_heading("8. Pokok diskusi dengan TÜV SÜD", level=1)
    bullets(d, [
        "Skema sertifikasi: IECEx dan ATEX secara bersamaan, notified body, serta lokasi pengujian.",
        "Pemanfaatan sertifikat housing dasar setelah modifikasi (kaca depan diganti mesh, isi elektronik diganti).",
        "Metode pembuktian mesh stainless steel sebagai elemen flame path (uji transmisi api) atau kebutuhan flame arrestor bersertifikat.",
        "Penetapan Ta maksimum +60 °C dan metode uji kelas suhu T4.",
        "Uji IP66 untuk perangkat dengan inlet gas terbuka.",
        "Jumlah sampel, urutan pengujian, jadwal, estimasi biaya, serta jalur QAR/QAN dan peran ISO 9001.",
        "Format dan bahasa dokumen teknis yang dapat diterima.",
    ], style="List Number")
    f = OUT / "00_Pengantar_Produk_GLD_V2_ID.docx"; d.save(f); return f


# ================================================================== 01 GAMBAR PERAKITAN
def build_01():
    no = "GLD/ATEX-AD/2026-001-ID"
    d = new_doc(no, "01 Gambar Perakitan")
    title_block(d, "Paket Gambar Perakitan", "Assembly drawing · foto rakitan · gambar komponen dan referensi", no,
                "Tanggapan atas permintaan TÜV SÜD: Assembly drawing")
    note(d, "Draf teknis — bukan gambar produksi terkendali. Lembar sumber ditampilkan dengan label aslinya (bahasa Inggris).")
    d.add_heading("1. Konfigurasi acuan", level=1)
    para(d, "Konfigurasi fisik acuan adalah unit produksi per foto 7 Oktober 2026: suplai 24 VDC kontinu, mesh stainless "
            "steel di tutup depan, kipas DC di belakang mesh, delapan modul MQ, main board V4 dan papan terminal, antena "
            "LoRa di atas base, beacon alarm di samping, dan kabel masuk di sisi kiri. Lubang bawah prototipe ditutup blanking plug.")
    table(d, [
        ["Parameter", "Data / catatan"],
        ["Dimensi", "200 × 90 × 290 mm; dicocokkan ulang dengan konfigurasi terbaru"],
        ["Massa", "2,378 kg; belum ditimbang dengan timbangan terkalibrasi"],
        ["Material", "ADC12 (enclosure) + stainless steel (mesh); bukti material dari pemasok akan dilampirkan"],
        ["Pemasangan", "Pelat 250 × 250 mm; U-bolt 2 in/DN50, M10"],
        ["Cable entry", "M20 × 1,5; gland prototipe polimer akan diganti gland Ex d"],
    ], [3.4, TW - 3.4])
    d.add_heading("2. Register gambar", level=1)
    table(d, [
        ["Kelompok", "Isi", "Bagian"],
        ["Foto perakitan & ukur", "Foto aktual rakitan, tampak luar, pengukuran ulir, bore, O-ring, kedalaman", "Lembar 1–10"],
        ["M-D1–D15", "Komponen, gasket, mesh, beacon, main board, exploded view, terminal, grounding", "Lembar 11–18"],
        ["M-E1–E6, M-E8", "Urutan perakitan; posisi antena terbaru di M-E8", "Lembar 19–25"],
        ["PCB & sketsa ukur", "Render PCB V4, sketsa sambungan ulir MS-01–04, terminal MS-06", "Lembar 26–30"],
        ["M-C1, M-F1–F4", "Gambar pemasok base BP18-1Z (kandidat) dan dimensi sensor MQ", "Lembar 31–35"],
    ], [3.6, 10.0, 2.9])
    d.add_heading("3. Catatan pengendalian desain", level=1)
    bullets(d, [
        "Gambar CAD casing v2 dan desain alternatif V3 tidak disertakan karena menampilkan posisi antena lama di samping base. Gambar berdimensi untuk unit produksi (antena di atas) akan diterbitkan terpisah.",
        "M-E3 dan M-D14 memuat detail lama (konfigurasi baterai) yang tidak berlaku untuk konfigurasi 24 VDC.",
        "Masih diperlukan gambar terkendali untuk celah dan panjang flame path, toleransi dan engagement ulir, volume internal, mesh dan retensinya, gasket, penetrasi kabel/antena/alarm, serta torsi.",
        "Pengukuran awal: bore ≈ Ø84,7 mm; tinggi leher ulir ≈ 14,8 mm; panjang ulir cover ≈ 18,9 mm; O-ring tali 2,70 mm, OD ≈ 91 mm; estimasi ulir cover M96 × 1,5; volume bruto ≈ 0,4 L. Nilai ini belum merupakan dimensi produksi yang disetujui.",
        "BP18-1Z hanya kandidat/referensi pemasok.",
    ])
    figs = [x for x in FIG if x["file"].startswith("a")]
    for k, fg in enumerate(figs, 1):
        page_break(d)
        d.add_heading(f"Lembar {k} — {fg['title']}", level=2)
        figure(d, A / fg["file"], fg["caption"].replace(" • label asli dipertahankan", "").replace("Lembar asli CIR", "Sumber: dossier CIR"), max_h=21.5)
    f = OUT / "01_Gambar_Perakitan_GLD_V2_ID.docx"; d.save(f); return f


# ================================================================== 02 PANDUAN PENGGUNA
MANUAL = [
    ("g.1 Peringatan keselamatan", "Hanya personel terlatih dan berwenang boleh memasang, mengoperasikan, menginspeksi atau memelihara GLD. Isolasi dan verifikasi suplai 24 VDC serta terapkan lockout/tagout sebelum membuka enclosure atau mengubah wiring; pastikan area aman. Gunakan hanya konfigurasi suplai 24 VDC. Uji alarm dengan prosedur lokasi dan pelindung pendengaran bila perlu. Nulling hanya pada udara bersih yang telah dipastikan dan harus berhasil 8/8. Dilarang mengebor, mengelas, memperbesar lubang, memintas (bypass) proteksi atau mengubah enclosure tanpa persetujuan. Hentikan pengoperasian unit apabila rusak, kemasukan air, ada fault sensor yang belum selesai, alarm gagal atau kontinuitas PE hilang."),
    ("g.2 Lingkungan pemasangan", "Target penggunaan adalah instalasi tetap di unit proses, tank farm, pipe rack dan area bongkar muat kilang: Group II, Category 2G/EPL Gb, Zone 1, IIC, T4, gas saja — tunduk pada persetujuan lembaga sertifikasi. Hanya lokasi yang memenuhi marking dan kondisi sertifikat final yang boleh digunakan. Debu mudah terbakar dikecualikan. Lindungi alat dari benturan, perubahan tanpa izin, kontaminasi dan kondisi di luar batas. Jaga akses inlet, sambungan, antena dan kabel."),
    ("g.3 Pemasangan mekanis", "Gunakan pelat U-bolt yang disetujui, sesuai gambar dan BOM terkendali; jangan mengubah struktur penyangga tanpa persetujuan pemilik lokasi. Pastikan dudukan tidak longgar, berputar atau bergeser akibat getaran dan beban yang dapat diperkirakan. Ikuti orientasi dan torsi final. Hindari benturan, deformasi, dan inlet yang terhalang dinding, pipa atau pelat."),
    ("g.4 Inlet gas dan area sensing", "Mesh depan, jalur udara, kipas DC dan delapan sensor MQ harus tetap dapat menerima udara sekitar. Dilarang menutup, mengecat, menempelkan pita, memasang filter/membran tambahan atau mengubah jalur gas tanpa persetujuan. Jangan merusak mesh pelindung bawaan sensor. Fungsi perlindungan mesh dibuktikan melalui pengujian tipe."),
    ("g.5 Suplai listrik", "Gunakan 24 VDC kontinu; adaptor 220 VAC/50 Hz ke 24 VDC berada di luar batas perangkat. Rail internal 5 VDC untuk sensor/heater dan 3,3 VDC untuk logika. Verifikasi polaritas dan sambungan terminal, kabel, PE dan proteksi hulu. Rangkaian dilengkapi PTC, TVS dan proteksi lain. Toleransi input, arus start, rating fuse hulu, ukuran kawat dan terminal ditetapkan dalam spesifikasi final."),
    ("g.6 Cable entry", "Ulir M20 × 1,5. Gunakan hanya gland, adaptor, blanking plug dan seal yang disetujui untuk konsep Ex, kelompok gas, ulir, IP, diameter luar kabel dan temperatur instalasi. Gland polimer prototipe bukan komponen final. Jangan mengubah lubang atau meninggalkan lubang terbuka. Ikuti urutan sealing/clamping dan torsi pemasok; catat part number dan referensi sertifikat."),
    ("g.7 Grounding dan bonding", "Sambungkan enclosure ke protective earth (PE) melalui stud dan lug yang disetujui; pastikan permukaan kontak, washer dan fastener sesuai gambar. Verifikasi kontinuitas sebelum pemberian daya dan sesudah servis. Jangan mengasumsikan GND rangkaian sama dengan PE."),
    ("g.8 Instalasi antena", "Antena LoRa berada di atas base dengan antarmuka SMA dan kabel RF internal. Gunakan posisi, model, seal dan pemasangan sesuai BOM/gambar yang disetujui. Jangan mengganti atau mengubah penetrasi, kabel, fitting dan antena tanpa review."),
    ("g.9 Commissioning", "Sebelum energisasi, periksa kesesuaian area, kondisi enclosure, mesh, kipas, gland/plug/seal, polaritas 24 VDC, kontinuitas PE, antena dan pemasangan. Setelah suplai diberikan, pastikan sensor, kipas, alarm dan komunikasi terinisialisasi tanpa fault. Lakukan nulling di udara bersih dan terima hanya hasil 8/8. Verifikasi alarm lokal dan penerimaan data/alarm di Cluster Head/Gateway; uji gas hanya melalui prosedur resmi. Catat model, serial, hardware, firmware/AI, tanggal, tegangan, hasil nulling dan alarm."),
    ("g.10 Mode operasi", "Inference Mode: operasi normal, klasifikasi gas dan alarm lokal/LoRa. Dataset Mode: pengumpulan data untuk engineering terkontrol. Nulling Mode: penyesuaian baseline sensor di udara bersih, harus 8/8. Kembalikan ke Inference Mode setelah aktivitas selesai dan pastikan tidak ada fault."),
    ("g.11 Operasi normal", "Setelah commissioning dan nulling berhasil, jalankan Inference Mode. Periksa daya, kondisi enclosure, diagnostik, status komunikasi dan fault setiap periode operasi. Jangan mengubah firmware/model, threshold, parameter kalibrasi atau fitur Ex tanpa persetujuan. Bila komunikasi hilang atau fault belum selesai, beri tahu operator dan terapkan prosedur impairment lokasi."),
    ("g.12 Penanganan alarm dan fault", "Alarm memiliki dua jalur paralel: LED/buzzer lokal dan notifikasi LoRa. Putusnya LoRa bukan bukti tidak ada gas. Perlakukan setiap alarm sebagai kejadian keselamatan proses nyata hingga prosedur lokasi membuktikan sebaliknya. Jangan menonaktifkan, mereset atau mengubah parameter untuk menyembunyikan alarm/fault."),
    ("g.13 Pembersihan", "Isolasi sesuai prosedur. Gunakan kain lembut bebas serat yang sedikit dibasahi air bersih atau pembersih ringan yang disetujui. Jangan gunakan abrasif, pelarut agresif, udara tekan atau semprotan bertekanan tinggi; jangan biarkan cairan masuk. Periksa mesh, seal, gasket dan penetrasi; jangan menusuk mesh."),
    ("g.14 Inspeksi dan pemeliharaan berkala", "Personel berwenang mengikuti jadwal di bawah; interval dapat dipersingkat sesuai kondisi lokasi. Isolasi 24 VDC, LOTO dan konfirmasi area aman sebelum pembukaan. Catat nomor seri, tanggal, kondisi, temuan, tindakan, komponen pengganti, hasil nulling/uji/PE, versi perangkat lunak dan personel."),
    ("g.15 Nulling dan kalibrasi sensor", "Lakukan setelah start-up dan stabilisasi, tanpa fault, di udara bersih yang telah dipastikan. Hasil harus 8/8; bila gagal, cari penyebab, koreksi dan ulangi. Nulling bukan cara menutupi drift, kontaminasi atau fault. Kalibrasi gas memerlukan prosedur, gas referensi dan peralatan yang disetujui."),
    ("g.16 Inspeksi bagian kritis Ex", "Periksa enclosure, cover, mesh, sambungan/ulir, gasket, gland, adaptor/plug, bonding, antena, beacon, kipas dan modul MQ. Verifikasi part number, material, pemasangan, retensi, engagement dan sealing; tidak boleh ada korosi, aus, retak, deformasi, kontaminasi atau modifikasi yang tidak disetujui."),
    ("g.17 Kontrol firmware dan konfigurasi", "Hanya versi firmware dan model AI yang disetujui untuk revisi hardware terkait yang boleh digunakan. Identifikasi versi/build/hash dan catat per unit. Perubahan akuisisi, klasifikasi, alarm, kipas, daya, komunikasi dan diagnostik harus dievaluasi, disetujui dan dapat di-rollback."),
    ("g.18 Pembatasan perbaikan", "Perbaikan hanya boleh dilakukan oleh personel berwenang dengan prosedur dan komponen pengganti yang disetujui. Dilarang mengebor, mengelas, memodifikasi ulir, memperbesar lubang, memintas (bypass) proteksi atau mengikir/menggerinda/melapisi flame path. Inspeksi dan uji fungsi sebelum unit dioperasikan kembali."),
    ("g.19 Penyimpanan dan transportasi", "Gunakan kemasan pelindung terhadap benturan, getaran, kelembapan, korosi dan debu. Lindungi mesh, antena, ulir, permukaan sealing, cable entry dan stud PE. Lepas pelindung sementara inlet sebelum operasi dan inspeksi unit sebelum energisasi."),
    ("g.20 Penghentian penggunaan", "Isolasi dan verifikasi suplai tidak bertegangan, terapkan LOTO dan konfirmasi area aman. Lepas koneksi daya, PE, antena, komunikasi dan mounting; amankan kabel tersisa. Tandai unit decommissioned dan tangani pembuangan elektronik/logam/PCB sesuai aturan lokasi."),
]


def build_02():
    no = "GLD/ATEX-UM/2026-001-ID"
    d = new_doc(no, "02 Panduan Pengguna")
    title_block(d, "Panduan Pengguna GLD V2", "Instalasi, pengoperasian, inspeksi dan pemeliharaan", no,
                "Tanggapan atas permintaan TÜV SÜD: User manual")
    note(d, "Draf untuk penelaahan. Belum boleh dipakai untuk instalasi di atmosfer eksplosif sebelum sertifikat terbit.")
    d.add_heading("1. Deskripsi produk", level=1)
    para(d, "GLD V2 adalah detektor gas tipe titik untuk instalasi tetap. Udara sekitar masuk melalui mesh stainless steel; kipas DC membantu "
            "aliran ke delapan sensor MQ. ESP32-S3 melakukan klasifikasi AI lokal (Clean Air, LPG, H₂); alarm visual/audibel "
            "dan notifikasi LoRa aktif saat kriteria alarm terpenuhi. Ambang confidence ≥ 30 % bukan konsentrasi gas atau %LEL. "
            "GLD tidak dimaksudkan sebagai satu-satunya sistem proteksi.")
    table(d, [
        ["Parameter", "Spesifikasi"],
        ["Suplai", "24 VDC kontinu; maks. ±8 W (≈ 0,33 A); PSU ≥ 1 A per unit"],
        ["Sensor", "MQ-2, MQ-3B, MQ-4, MQ-5, MQ-6, MQ-7B, MQ-8, MQ-135"],
        ["Akuisisi", "ADS1256, 24-bit; interval pemindaian 500 ms"],
        ["Komunikasi", "LoRa E22-900MM22S, 920–923 MHz; laporan rutin 10 detik, alarm segera"],
        ["RS-485", "Modbus RTU read-only, 9600 bit/s, 8N1, Unit ID 1; 8 register"],
        ["Lingkungan", "−20 hingga +60 °C (batas atas dalam peninjauan); 5–95 % RH non-kondensasi; IP66 target"],
        ["Target Ex", "II 2G Ex db IIC T4 Gb; gas saja; belum tersertifikasi"],
    ], [3.4, TW - 3.4])
    d.add_heading("2. Petunjuk keselamatan, instalasi dan operasi", level=1)
    for h, t in MANUAL:
        d.add_heading(h, level=2); para(d, t)
        if h.startswith("g.12"):
            table(d, [
                ["Kondisi", "Tindakan"],
                ["Alarm gas", "Ikuti prosedur respons gas darurat lokasi"],
                ["Fault sensor / nulling tidak 8/8", "Investigasi, perbaiki, ulangi nulling di udara bersih"],
                ["Komunikasi LoRa terputus", "Beri tahu operator; terapkan prosedur impairment lokasi"],
                ["Alarm lokal gagal", "Hentikan pengoperasian, perbaiki, lalu verifikasi"],
                ["Fault grounding", "Isolasi hingga kontinuitas pulih"],
                ["Air masuk / enclosure rusak", "Hentikan pengoperasian; inspeksi sebelum commissioning ulang"],
            ], [6.0, TW - 6.0])
        if h.startswith("g.14"):
            table(d, [
                ["Interval", "Aktivitas minimum"],
                ["Harian / setiap shift", "Daya, enclosure, diagnostik, fault, LoRa"],
                ["Setiap 3 bulan", "Mesh, area MQ, kontaminasi/sumbatan, kerusakan"],
                ["Setiap 6 bulan", "Uji alarm, nulling 8/8, kipas, ulir dan antarmuka"],
                ["Tahunan", "Inspeksi lengkap: PE/bonding, gland/terminal, gasket, antena, alarm, LoRa, umur sensor"],
            ], [4.0, TW - 4.0])
    d.add_heading("3. Terminal dan pengawatan lapangan", level=1)
    para(d, "Terminal BAT tidak digunakan dalam konfigurasi 24 VDC. Port servis dan RS-485 bukan jalur kontrol produksi.")
    m = [x for x in FIG if x["file"].startswith("m")][0]
    figure(d, A / m["file"], "MS-06 — terminal dan pengawatan lapangan, papan terminal GLD V4 (tidak berskala).", max_h=12)
    d.add_heading("4. Yang dilengkapi sebelum manual final", level=1)
    para(d, "Kondisi khusus sertifikat, kinerja deteksi gas, gas dan interval kalibrasi, nilai torsi, batas suplai, "
            "orientasi/clearance, komponen Ex, bukti IP66, versi firmware/AI yang disetujui.")
    f = OUT / "02_Panduan_Pengguna_GLD_V2_ID.docx"; d.save(f); return f


# ================================================================== 03 TARGET PENANDAAN EX
def build_03():
    no = "GLD/ATEX-EX/2026-001-ID"
    d = new_doc(no, "03 Target Penandaan Ex")
    title_block(d, "Target Penandaan Ex", "Usulan klasifikasi ATEX/IECEx, nameplate dan evaluasi awal kelas suhu", no,
                "Tanggapan atas permintaan TÜV SÜD: Target Ex marking")
    d.add_heading("1. Usulan penandaan", level=1)
    for line in ("ATEX:   ⟨Ex⟩ II 2G  Ex db IIC T4 Gb", "IECEx:   Ex db IIC T4 Gb", "−20 °C ≤ Ta ≤ +60 °C   ·   IP66 (target)"):
        p = d.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(line); r.bold = True; r.font.size = Pt(13); r.font.color.rgb = NAVY
        p.paragraph_format.space_after = Pt(2)
    d.add_paragraph()
    table(d, [
        ["Elemen", "Arti", "Status"],
        ["II", "Peralatan Group II (non-tambang)", "Usulan"],
        ["2G", "Kategori 2, atmosfer gas — Zone 1", "Usulan"],
        ["Ex db", "Flameproof enclosure", "Usulan"],
        ["IIC", "Kelompok gas IIC (mencakup H₂)", "Usulan"],
        ["T4", "Suhu permukaan maksimum 135 °C", "Usulan; evaluasi awal di §3"],
        ["Gb", "Equipment Protection Level Gb", "Usulan"],
        ["Ta", "−20 hingga +60 °C", "Batas atas dalam peninjauan: rating housing dasar +55 °C"],
        ["Debu", "Tidak diajukan", "Gas saja"],
    ], [2.4, 7.4, 6.7])
    note(d, "Usulan — belum tersertifikasi. Penandaan ini tidak boleh diterapkan sebagai klaim sertifikasi.")
    d.add_heading("2. Usulan nameplate", level=1)
    table(d, [
        ["Elemen", "Isi / status"],
        ["Produsen", "Nama dan alamat produsen — dicantumkan setelah ditetapkan"],
        ["Produk", "Gas Leak Detector — GLD V2"],
        ["Nomor seri / tahun", "Per unit; contoh sampel GLD2-0x1001"],
        ["Penandaan", "Simbol Ex segi enam, II 2G; Ex db IIC T4 Gb — usulan"],
        ["Rating", "24 VDC, 8 W maks.; Ta −20 hingga +60 °C; IP66 target"],
        ["Cable entry", "M20 × 1,5"],
        ["Sertifikat", "Nomor ATEX/IECEx dan CE/notified body diisi setelah terbit"],
        ["Peringatan", "WARNING – DO NOT OPEN WHEN AN EXPLOSIVE ATMOSPHERE MAY BE PRESENT, ditambah peringatan sesuai sertifikat"],
        ["Lokasi & bahan", "Permukaan datar atas base di samping antena; pelat 80 × 55 mm stainless steel 0,5 mm, etsa/engraving; 4 rivet atau perekat"],
    ], [3.6, TW - 3.6])
    x = [f for f in FIG if f["file"].startswith("x")][0]
    figure(d, A / x["file"], "MS-05 — rancangan nameplate (bukan penandaan tersertifikasi).", max_h=7)
    figure(d, A / "nameplate_mockup_figure.jpg", "Ilustrasi posisi nameplate pada unit: permukaan datar atas base di samping antena (usulan, bukan penandaan tersertifikasi). Kanan: detail.", crop=False, max_h=7.8)
    d.add_heading("3. Evaluasi awal kelas suhu T4", level=1)
    para(d, "Batas T4 adalah 135 °C; evaluasi memakai batas efektif 130 °C (margin 5 K). Pengukuran internal dengan "
            "termokopel delapan titik, 180 menit per kondisi, diekstrapolasi ke Ta +60 °C: T(Ta,max) = Ta,max + (T terukur − Ta uji).")
    table(d, [
        ["Kondisi", "Badan sensor MQ", "PCB", "Enclosure luar"],
        ["Normal", "44,2 → ≈ 79 °C", "52,4 → ≈ 88 °C", "32,1 → ≈ 67 °C"],
        ["Beban maksimum", "55,0 → ≈ 91 °C", "58,3 → ≈ 94 °C", "34,8 → ≈ 71 °C"],
        ["Kipas berhenti", "78,4 → ≈ 114 °C", "63,4 → ≈ 99 °C", "43,9 → ≈ 79 °C"],
    ], [4.1, 4.1, 4.1, 4.2])
    table(d, [
        ["Ref.", "Titik panas potensial", "Status"],
        ["T-01", "Heater/badan MQ", "Terukur"],
        ["T-02", "Motor/elektronik kipas", "Terukur"],
        ["T-03–07", "Konverter 5 V, regulator 3,3 V, induktor, MOSFET/proteksi", "Belum terukur"],
        ["T-08", "ESP32-S3 / titik panas PCB", "Terukur; beban maksimum belum stabil"],
        ["T-09", "LoRa pada TX maksimum", "Belum terukur"],
        ["T-10", "Alarm LED/buzzer aktif", "Belum terukur"],
        ["T-11", "Permukaan luar enclosure", "Terukur"],
        ["T-12", "Mesh/cover depan", "Belum terukur"],
    ], [2.2, 8.6, 5.7])
    para(d, "Data ini hasil uji internal awal, bukan hasil sertifikasi. Metode dan pengujian pada ambient maksimum dikonfirmasi bersama lembaga sertifikasi.", size=9.5, italic=True)
    d.add_heading("4. Bukti yang masih diperlukan", level=1)
    bullets(d, [
        "Gambar flame path terkendali, data material enclosure, dan pengujian tipe Ex db IIC.",
        "Pembuktian mesh depan sebagai elemen flame path (sertifikat atau uji).",
        "Gland Ex d IIC, plug/adaptor, beacon dan feed-through antena yang sesuai atau dicakup penilaian perangkat.",
        "Sertifikat housing dasar HIREP HRP-T1000-A (klaim pemasok Ex d IIC T6 Gb, −20…+55 °C, IP66). Rating T6 pemasok berlaku untuk isi ≤ 3 W dan tidak diklaim untuk GLD (±8 W).",
        "Bukti IP66 dan hasil pengujian temperatur final.",
    ])
    f = OUT / "03_Target_Penandaan_Ex_GLD_V2_ID.docx"; d.save(f); return f


# ================================================================== 04 IP66
def build_04():
    no = "GLD/ATEX-IP/2026-001-ID"
    d = new_doc(no, "04 Status IP66")
    title_block(d, "Status IP66 dan Rencana Verifikasi", "Ingress protection — target desain dan bukti pengujian", no,
                "Tanggapan atas permintaan TÜV SÜD: IP66")
    note(d, "Ringkasan: IP66 adalah target desain dan belum diuji pada GLD V2.")
    d.add_heading("1. Target dan batas klaim", level=1)
    para(d, "IP66 berarti kedap debu (IP6X) dan tahan semburan air kuat (IPX6) menurut IEC 60529. Penilaian mencakup unit "
            "GLD lengkap, bukan hanya gland atau housing. Inlet gas sengaja terbuka ke udara sekitar, sehingga kesesuaian "
            "mesh dengan IP66 harus dibuktikan tanpa mengganggu pengambilan sampel gas.")
    d.add_heading("2. Antarmuka sealing", level=1)
    table(d, [
        ["Antarmuka", "Kondisi saat ini / tindakan"],
        ["Mesh depan dan retensinya", "Stainless steel; grade, ukuran pori, tebal dan retensi ditetapkan dan divalidasi"],
        ["Cover / O-ring", "O-ring karet, tali 2,70 mm, OD ≈ 91 mm; material, kekerasan dan rentang suhu ditetapkan"],
        ["Cable entry 24 VDC", "M20 × 1,5; gland polimer prototipe diganti gland Ex d logam dengan rating IP yang sesuai"],
        ["Penetrasi lain", "Blanking plug, feed-through antena, beacon diverifikasi sesuai desain final"],
        ["Housing dasar", "Klaim pemasok IP66/67 untuk housing asli; tidak otomatis berlaku setelah kaca depan diganti mesh dan kipas ditambahkan"],
    ], [4.2, TW - 4.2])
    d.add_heading("3. Rencana verifikasi (usulan)", level=1)
    bullets(d, [
        "Bekukan konfigurasi sampel: BOM, revisi gambar, gland/kabel, seal, torsi penutupan dan orientasi; dokumentasikan foto dan nomor seri.",
        "Sepakati standar dan edisi uji (IEC 60529), urutan, kondisi, jumlah sampel dan kriteria penerimaan bersama TÜV SÜD.",
        "Laboratorium kompeten melaksanakan uji IP6X (debu) dan IPX6 (semburan air).",
        "Inspeksi ingress dan uji fungsi pascauji: pengambilan sampel gas, alarm dan komunikasi.",
    ], style="List Number")
    d.add_heading("4. Bukti yang akan diserahkan", level=1)
    para(d, "Laporan laboratorium, identitas sampel, gambar sealing dan perakitan final, datasheet/sertifikat komponen, foto pengujian.")
    f = OUT / "04_Status_IP66_GLD_V2_ID.docx"; d.save(f); return f


# ================================================================== 05 ISO 9001
def build_05():
    no = "GLD/ATEX-QMS/2026-001-ID"
    d = new_doc(no, "05 Status ISO 9001")
    title_block(d, "Status Sertifikasi ISO 9001", "Sistem manajemen mutu produsen dan persiapan QAR/QAN", no,
                "Tanggapan atas permintaan TÜV SÜD: sertifikat ISO 9001")
    note(d, "Ringkasan: sertifikasi ISO 9001 produsen dalam proses; salinan sertifikat diserahkan setelah terbit.")
    d.add_heading("1. Produsen", level=1)
    table(d, [
        ["Data", "Keterangan"],
        ["Produsen", "Produsen pemohon — identitas dicantumkan pada formulir aplikasi"],
        ["Lokasi produksi", "Lokasi produksi serial ditetapkan setelah tahap prototipe"],
        ["Perakitan PCB", "Fabrikasi dan perakitan PCB dilakukan oleh penyedia jasa PCB assembly"],
    ], [3.6, TW - 3.6])
    d.add_heading("2. Status ISO 9001", level=1)
    para(d, "Proses sertifikasi ISO 9001 produsen berjalan; audit sertifikasi dijadwalkan Oktober 2026. Nomor sertifikat, "
            "lingkup, lembaga penerbit dan masa berlaku disampaikan setelah sertifikat terbit.")
    d.add_heading("3. Kelengkapan sistem mutu", level=1)
    table(d, [
        ["Dokumen", "Status / tindakan"],
        ["Sertifikat ISO 9001", "Diserahkan setelah terbit; lingkup dan lokasi diperiksa kesesuaiannya"],
        ["Manual mutu dan daftar prosedur", "Dalam penyusunan"],
        ["Mutu produksi Ex", "Jalur IECEx QAR dan ATEX QAN/verifikasi produk dikonfirmasi bersama TÜV SÜD"],
        ["Organisasi", "Penanggung jawab desain, produksi dan mutu serta kontak ditetapkan"],
    ], [5.0, TW - 5.0])
    para(d, "Catatan: pada skema IECEx dan ATEX, produsen tetap perlu menunjukkan sistem mutu produksi Ex (QAR/QAN) "
            "terlepas dari kepemilikan ISO 9001; ISO 9001 umumnya mempersingkat penilaian tersebut.", size=9.5, italic=True)
    f = OUT / "05_Status_ISO_9001_Produsen_ID.docx"; d.save(f); return f


if __name__ == "__main__":
    docs = [build_00(), build_01(), build_02(), build_03(), build_04(), build_05()]
    pdfs = [to_pdf(x) for x in docs]
    w = PdfWriter()
    labels = ["00 Pengantar Produk", "01 Gambar Perakitan", "02 Panduan Pengguna", "03 Target Penandaan Ex", "04 Status IP66", "05 Status ISO 9001"]
    for lab, pdf in zip(labels, pdfs):
        start = len(w.pages)
        for pg in PdfReader(str(pdf)).pages:
            w.add_page(pg)
        w.add_outline_item(title=lab, page_number=start)
    with open(OUT / "GLD_V2_Paket_Diskusi_TUV_SUD_Lengkap_ID.pdf", "wb") as f:
        w.write(f)
    for p in pdfs + [OUT / "GLD_V2_Paket_Diskusi_TUV_SUD_Lengkap_ID.pdf"]:
        print(p.name, len(PdfReader(str(p)).pages), "hlm", round(p.stat().st_size / 1e6, 1), "MB")
