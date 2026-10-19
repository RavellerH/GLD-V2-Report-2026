"""Isi formulir TTH TLKM02/F/013 v02 (Permohonan Uji Conformance Test) untuk
sewa chamber EMC uji GLD Node Sensor & Cluster Head, atas nama PT LAPI Ganesha Utama.

Final: isian kontak, tanggal & pemohon dari Bu Nina (19 Okt 2026).
Output: Deliverables/Permohonan_Uji_CT_TTH_EMC_GLD_LGU.docx
"""
from pathlib import Path

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_COLOR_INDEX
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt

ROOT = Path(__file__).resolve().parent.parent
SIGNATURE = ROOT / "scripts" / "assets" / "ttd_nina_siti_aminah.png"
OUT = ROOT / "Deliverables" / "Permohonan_Uji_CT_TTH_EMC_GLD_LGU.docx"

FOOTER = "TLKM02/F/013 Versi 02"


def run(p, text, bold=False, hl=False, size=10, italic=False):
    r = p.add_run(text)
    r.bold = bold
    r.italic = italic
    r.font.size = Pt(size)
    if hl:
        r.font.highlight_color = WD_COLOR_INDEX.YELLOW
    return r


def borders(table):
    tbl = table._tbl
    pr = tbl.tblPr
    b = OxmlElement("w:tblBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        e = OxmlElement(f"w:{edge}")
        e.set(qn("w:val"), "single")
        e.set(qn("w:sz"), "4")
        e.set(qn("w:color"), "808080")
        b.append(e)
    pr.append(b)


def fixed(table, widths):
    table.autofit = False
    lay = OxmlElement("w:tblLayout")
    lay.set(qn("w:type"), "fixed")
    table._tbl.tblPr.append(lay)
    for row in table.rows:
        for cell, w in zip(row.cells, widths):
            cell.width = w


def cell(c, parts):
    """parts: list of (text, hl) atau str."""
    p = c.paragraphs[0]
    p.paragraph_format.space_after = Pt(0)
    for part in parts if isinstance(parts, list) else [parts]:
        if isinstance(part, tuple):
            run(p, part[0], hl=part[1], size=9.5)
        else:
            run(p, part, size=9.5)


def label(c, text):
    p = c.paragraphs[0]
    p.paragraph_format.space_after = Pt(0)
    run(p, text, bold=True, size=9.5)


def heading(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(3)
    run(p, text, bold=True, size=11)


def kv_table(doc, rows):
    t = doc.add_table(rows=len(rows), cols=2)
    borders(t)
    for i, (k, v) in enumerate(rows):
        label(t.cell(i, 0), k)
        cell(t.cell(i, 1), v)
    fixed(t, [Cm(4.6), Cm(12.4)])
    return t


def build():
    doc = Document()
    sec = doc.sections[0]
    sec.page_width, sec.page_height = Cm(21.59), Cm(27.94)
    sec.left_margin = sec.right_margin = Cm(2.2)
    sec.top_margin = sec.bottom_margin = Cm(1.8)
    st = doc.styles["Normal"]
    st.font.name = "Arial"
    st.font.size = Pt(10)

    fp = sec.footer.paragraphs[0]
    run(fp, FOOTER, size=8)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run(p, "Permohonan Uji Conformance Test (CT)", bold=True, size=14)
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    run(p, "Nomor Registrasi: ", size=9.5)
    run(p, "RCT-YYXXX (diisi TTH)", size=9.5, italic=True)

    heading(doc, "Data Pelanggan:")
    kv_table(doc, [
        ("Nama Perusahaan", ["PT LAPI Ganesha Utama"]),
        ("Alamat Perusahaan", ["Jl. Dederuk No. 30, Kelurahan Sadang Serang, Kecamatan Coblong, "
                               "Kota Bandung, Jawa Barat 40133"]),
        ("Nama Kontak", ["Dr. Nina Siti Aminah"]),
        ("Nomor Kontak", ["081214295251"]),
        ("Surel Kontak", ["nina@itb.ac.id"]),
    ])

    heading(doc, "Data Perangkat:")
    t = doc.add_table(rows=1, cols=3)
    borders(t)
    label(t.cell(0, 0), "Parameter")
    label(t.cell(0, 1), "Perangkat 1")
    label(t.cell(0, 2), "Perangkat 2")
    rows = [
        ("Nama Perangkat",
         ["Gas Leak Detection (GLD) — Node Sensor"],
         ["Gas Leak Detection (GLD) — LoRa Cluster Head"]),
        ("Merek", ["GLD (prototipe)"], ["GLD (prototipe)"]),
        ("Tipe/Model", ["GLD V2 (Node Sensor, versi 2)"], ["CH V2 (Cluster Head, versi 2)"]),
        ("Kapasitas",
         ["LoRa 920 MHz, maks. 22 dBm, BW 125 kHz; catu 24 VDC, konsumsi maks. ±8 W"],
         ["LoRa dual 920 MHz (star) / 921 MHz (mesh), maks. 22 dBm, BW 125 kHz; "
          "catu 5 VDC, konsumsi maks. 0,73 W"]),
        ("Nomor Seri", ["GLD-V2-001"],
         ["Prototipe — belum bernomor seri"]),
        ("Negara Pembuat", ["Indonesia"], ["Indonesia"]),
    ]
    for k, a, b in rows:
        r = t.add_row()
        label(r.cells[0], k)
        cell(r.cells[1], a)
        cell(r.cells[2], b)
    fixed(t, [Cm(3.4), Cm(6.8), Cm(6.8)])

    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(4)
    run(p, "Referensi Uji: ", bold=True, size=9.5)
    run(p, "Uji EMC — emisi radiasi (radiated emission) dan emisi konduksi "
        "(conducted emission). ", size=9.5)
    run(p, "Metode dan batas ambang sesuai prosedur uji Telkom Test House.", size=9.5)

    heading(doc, "Agenda CT:")
    for mark, txt in (("☐", "Uji Petik"), ("☐", "Uji Verifikasi (UV)"),
                      ("☐", "Acceptance Test Procedure (ATP)"), ("☐", "Uji Terima (UT)")):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(0)
        run(p, f"{mark}  {txt}", size=9.5)
    p = doc.add_paragraph()
    run(p, "☒  Lainnya, sebutkan: ", bold=True, size=9.5)
    run(p, "Sewa chamber (semi-anechoic chamber) untuk pengujian EMC radiated & conducted "
        "emission pada prototipe Node Sensor GLD dan LoRa Cluster Head, sebagai data "
        "pendukung pengajuan sertifikasi.", size=9.5)

    heading(doc, "Periode CT:")
    kv_table(doc, [
        ("Durasi dalam hari kerja", ["1 (satu) hari kerja"]),
        ("Tanggal pelaksanaan", ["16 Oktober 2026"]),
    ])

    doc.add_page_break()
    heading(doc, "Pernyataan:")
    for i, s in enumerate([
        "Kami menyatakan bahwa permohonan ini telah diisi dengan keadaan yang sebenarnya.",
        "Kami menjamin bahwa nama perangkat, merek, tipe/model, kapasitas, nomor seri, dan "
        "negara pembuat perangkat uji yang kami ajukan sama dengan yang diserahkan ke "
        "Telkom Test House (TTH).",
        "Kami mengetahui dan menyetujui referensi uji yang tertera di permohonan ini.",
        "Kami bertanggung jawab atas pengiriman, pembongkaran, dan pengambilan perangkat uji "
        "sehingga biaya tak terduga yang muncul pada proses tersebut bukan menjadi tanggung "
        "jawab TTH. Jumlah perangkat uji maksimal sebanyak 2 (dua) buah.",
        "Kami bersedia mengambil perangkat uji terlebih dahulu sebelum mengunduh Laporan "
        "Hasil Uji (LHU).",
        "Kami dengan sadar memahami, menyetujui, dan melaksanakan setiap butir dalam "
        "permohonan ini serta menyatakan bahwa permohonan ini sah.",
    ], 1):
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Cm(0.6)
        p.paragraph_format.first_line_indent = Cm(-0.6)
        p.paragraph_format.space_after = Pt(2)
        run(p, f"{i}.  {s}", size=9.5)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(18)
    run(p, "Bandung, ", size=10)
    run(p, "19 Oktober 2026", size=10)

    t = doc.add_table(rows=4, cols=3)
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    heads = ("Pemohon", "Mengetahui", "Menyetujui")
    names = (["Dr. Nina Siti Aminah"], ["[Nama Test Engineer TTH]"],
             ["[Nama Officer TTH]"])
    roles = ("Pelanggan", "Test Engineer TTH", "Officer TTH")
    for j in range(3):
        for i, content in enumerate((heads[j], "\n\n\nTanda tangan\n", None, roles[j])):
            c = t.cell(i, j)
            c.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            if i == 2:
                for part in names[j]:
                    if isinstance(part, tuple):
                        run(c.paragraphs[0], part[0], hl=part[1], size=9.5, bold=True)
                    else:
                        run(c.paragraphs[0], part, size=9.5, italic=True)
            elif i == 1 and j == 0 and SIGNATURE.exists():
                c.paragraphs[0].add_run().add_picture(str(SIGNATURE), height=Cm(2.0))
            else:
                run(c.paragraphs[0], content, size=9.5, bold=(i == 0))
    fixed(t, [Cm(5.6)] * 3)

    OUT.parent.mkdir(exist_ok=True)
    doc.save(OUT)
    print(OUT)


if __name__ == "__main__":
    build()
