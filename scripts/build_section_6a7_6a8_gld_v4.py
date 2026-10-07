# -*- coding: utf-8 -*-
"""Insert-ready dossier section 6(a).7 (Main PCB schematic) and 6(a).8 (PCB layout), GLD V4 main board.

Sources (provided by the team, 7 Oct 2026):
  Sumber Dokumen/Schematic_PCB_GLD_V4/Main-PCB-Schematic-GLD-V4.pdf   (26 figures, EasyEDA rev 1.0 / 2026-07-19)
  Sumber Dokumen/Schematic_PCB_GLD_V4/PCB_Layout_GLD_V4_MainBoard.pdf (10 annotated layout views)
Rendered assets: scripts/assets/gld_v4_sch/sheet-NN.png, scripts/assets/gld_v4_pcb/viewNN.jpg

Written in English to match the IECEx/ATEX dossier. Structure follows the reviewer's
"Panduan Revisi ATEX/IECEx" items 6(a).7 and 6(a).8.

Output: Deliverables/Dossier_Section_6a7_6a8_Schematic_PCB_GLD_V4.docx
"""
import os
import glob

from docx import Document
from docx.shared import Pt, Inches, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCH = os.path.join(REPO, "scripts", "assets", "gld_v4_sch")
PCB = os.path.join(REPO, "scripts", "assets", "gld_v4_pcb")
OUT = os.path.join(REPO, "Deliverables", "Dossier_Section_6a7_6a8_Schematic_PCB_GLD_V4.docx")

NAVY = RGBColor(0x1B, 0x33, 0x5F)
INK = RGBColor(0x26, 0x23, 0x21)
GRAY = RGBColor(0x55, 0x5B, 0x66)
HEAD_SHADE = "EAEFF9"
NOTE_SHADE = "F3F6FC"
WARN_SHADE = "FBEEE4"

doc = Document()
st = doc.styles["Normal"]
st.font.name = "Calibri"
st.font.size = Pt(10)
st.font.color.rgb = INK
sec = doc.sections[0]
sec.left_margin = sec.right_margin = Cm(2.0)
sec.top_margin = sec.bottom_margin = Cm(1.8)
CONTENT_W = 6.6  # inches (A4/Letter minus margins, conservative)

fp = sec.footer.paragraphs[0]
fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = fp.add_run("GLD V2 — Section 6(a).7 Main PCB Schematic / 6(a).8 PCB Layout  ·  Page ")
r.font.size = Pt(8)
r.font.color.rgb = GRAY
for kind, text in (("begin", None), (None, "PAGE"), ("end", None)):
    run = fp.add_run()
    run.font.size = Pt(8)
    run.font.color.rgb = GRAY
    if kind:
        fc = OxmlElement("w:fldChar")
        fc.set(qn("w:fldCharType"), kind)
        run._r.append(fc)
    else:
        it = OxmlElement("w:instrText")
        it.set(qn("xml:space"), "preserve")
        it.text = text
        run._r.append(it)


def shade(cell, hex_color):
    el = OxmlElement("w:shd")
    el.set(qn("w:val"), "clear")
    el.set(qn("w:fill"), hex_color)
    cell._tc.get_or_add_tcPr().append(el)


def p(text="", size=10, bold=False, italic=False, color=None, space_after=6, align=None):
    para = doc.add_paragraph()
    para.paragraph_format.space_after = Pt(space_after)
    if align is not None:
        para.alignment = align
    run = para.add_run(text)
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = color or INK
    return para


def h1(text):
    return p(text, size=15, bold=True, color=NAVY, space_after=6)


def h2(text):
    return p(text, size=12, bold=True, color=NAVY, space_after=4)


def bullet(text):
    para = doc.add_paragraph(style="List Bullet")
    para.paragraph_format.space_after = Pt(2)
    run = para.add_run(text)
    run.font.size = Pt(10)
    return para


def note_box(text, fill=NOTE_SHADE):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.rows[0].cells[0]
    shade(cell, fill)
    cell.paragraphs[0].paragraph_format.space_after = Pt(2)
    run = cell.paragraphs[0].add_run(text)
    run.font.size = Pt(9)
    run.font.color.rgb = GRAY
    doc.add_paragraph().paragraph_format.space_after = Pt(2)


def table(headers, rows, widths, bold_first=True):
    tbl = doc.add_table(rows=1, cols=len(headers))
    tbl.style = "Table Grid"
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr = tbl.rows[0]
    th = OxmlElement("w:tblHeader")
    th.set(qn("w:val"), "true")
    hdr._tr.get_or_add_trPr().append(th)
    for i, txt in enumerate(headers):
        shade(hdr.cells[i], HEAD_SHADE)
        hdr.cells[i].paragraphs[0].paragraph_format.space_after = Pt(1)
        rr = hdr.cells[i].paragraphs[0].add_run(txt)
        rr.font.bold = True
        rr.font.size = Pt(8.5)
        rr.font.color.rgb = NAVY
    for vals in rows:
        row = tbl.add_row()
        row._tr.get_or_add_trPr().append(OxmlElement("w:cantSplit"))
        for idx, val in enumerate(vals):
            para = row.cells[idx].paragraphs[0]
            para.paragraph_format.space_after = Pt(1)
            para.paragraph_format.space_before = Pt(1)
            run = para.add_run(val)
            run.font.size = Pt(8.5)
            if idx == 0 and bold_first:
                run.font.bold = True
    tbl.autofit = False
    layout = OxmlElement("w:tblLayout")
    layout.set(qn("w:type"), "fixed")
    tbl._tbl.tblPr.append(layout)
    grid = tbl._tbl.find(qn("w:tblGrid"))
    for i, gc in enumerate(grid.findall(qn("w:gridCol"))):
        gc.set(qn("w:w"), str(int(widths[i] * 1440)))
    for row in tbl.rows:
        for i, w in enumerate(widths):
            row.cells[i].width = Inches(w)
    doc.add_paragraph().paragraph_format.space_after = Pt(2)
    return tbl


def picture(path, width_in, max_h_in=8.6):
    from PIL import Image
    w, hgt = Image.open(path).size
    width = min(width_in, max_h_in * w / hgt)
    para = doc.add_paragraph()
    para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    para.paragraph_format.space_after = Pt(2)
    para.add_run().add_picture(path, width=Inches(width))


def caption(text):
    p(text, size=9, bold=True, color=NAVY, space_after=3, align=WD_ALIGN_PARAGRAPH.CENTER)


# =================================================================== cover block
p("IECEx / ATEX CERTIFICATION INFORMATION — GAS LEAK DETECTOR (GLD V2)", size=9, bold=True, color=GRAY,
  space_after=2)
p("Section 6(a).7 Main PCB Schematic and 6(a).8 PCB Layout", size=18, bold=True, color=NAVY, space_after=2)
p("Insert for item 6 \"Design and manufacturing information\", a. Complete drawings", size=10.5, color=GRAY,
  space_after=8)

table(
    ["Item", "Details"],
    [
        ["Board", "Main board (motherboard) of the GLD — EasyEDA project \"MotherBoardGLDVer2\", "
                  "design package \"GLD V4\""],
        ["Source files", "1-Schematic_MotherBoardGLDVer2.json (EasyEDA 6.5.57) and the corresponding PCB "
                         "layout of the same project"],
        ["Schematic revision / date", "1.0 / 2026-07-19 (from the title block of the EasyEDA schematic)"],
        ["Drawing numbers", "PGLD-GLD-V4-MB-SCH-01 … -26 (schematic) and PGLD-GLD-V4-MB-PCB-01 … -10 (layout) — "
                            "proposed numbering, to be aligned with the applicant's document control"],
        ["Scope", "Main board only. The sensor-module board (8 pcs, connected to H1–H8) is a separate PCB and is "
                  "not covered by this insert"],
    ],
    widths=(1.7, 4.9),
)

# =================================================================== 6(a).7 / 6(a).8 (shared content)
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gld_v4_board_section as board  # noqa: E402

board.render(doc, h1=h1, h2=h2, content_w=CONTENT_W)

doc.save(OUT)
print("written", OUT)
