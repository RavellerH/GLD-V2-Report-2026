# -*- coding: utf-8 -*-
import os
import csv
from PIL import Image
from docx import Document
from docx.shared import Pt, Inches, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PHOTO_DIR = os.path.join(REPO, "scripts", "assets", "cert_doc_photos")
SCHEMATIC_DIR = os.path.join(REPO, "scripts", "assets", "cert_doc_schematics")
BOM_DIR = os.path.join(REPO, "scripts", "assets", "cert_doc_bom")
OUT_PATH = os.path.join(REPO, "Deliverables", "Dokumen_Teknis_Sertifikasi_GLD_IECEx_ATEX.docx")

def load_bom(fn):
    with open(os.path.join(BOM_DIR, fn), encoding="utf-8") as f:
        rows = list(csv.reader(f))
    return rows[1:]  # skip header: ID,Name,Designator,Footprint,Quantity,Manufacturer Part,Manufacturer,Supplier,Supplier Part,Price

def bom_table_rows(rows):
    out = []
    for r in rows:
        _id, name, designator, footprint, qty, mpn, mfr, supplier, supplier_part, price = (r + [""] * 10)[:10]
        lcsc = supplier_part if supplier == "LCSC" and supplier_part else "—"
        mfr_disp = mfr.split("(")[0].strip() if mfr else "—"
        mpn_disp = mpn if mpn else "—"
        out.append([designator, name, qty, mfr_disp, mpn_disp, lcsc])
    return out

NAVY = RGBColor(0x1A, 0x2B, 0x3D)
GRAY = RGBColor(0x4A, 0x4A, 0x4A)
GOOD = RGBColor(0x14, 0x91, 0x74)
WARN = RGBColor(0xB5, 0x6A, 0x1E)
GAP  = RGBColor(0xB0, 0x2A, 0x37)
LINE_GRAY = "D0D0D0"
HEAD_SHADE = "EFEFEF"
INFO_SHADE = "E4F2FA"
WARN_SHADE = "FDF1E6"

doc = Document()

# ---------- base style setup ----------
normal = doc.styles["Normal"]
normal.font.name = "Calibri"
normal.font.size = Pt(10.5)
normal.font.color.rgb = RGBColor(0x2B, 0x2B, 0x2B)
normal.paragraph_format.space_after = Pt(8)
normal.paragraph_format.line_spacing = 1.25

for i, sz, col in [(1, 16, NAVY), (2, 13, NAVY), (3, 11, NAVY)]:
    st = doc.styles[f"Heading {i}"]
    st.font.name = "Calibri"
    st.font.size = Pt(sz)
    st.font.bold = True
    st.font.color.rgb = col
    st.paragraph_format.space_before = Pt(16 if i == 1 else 12)
    st.paragraph_format.space_after = Pt(6)

sec = doc.sections[0]
sec.left_margin = sec.right_margin = Cm(2.2)
sec.top_margin = sec.bottom_margin = Cm(1.8)

def add_picture_fit(run, path, max_w_in, max_h_in):
    """Insert a picture scaled to fit within a max_w x max_h box, preserving aspect ratio."""
    with Image.open(path) as im:
        w_px, h_px = im.size
    aspect = w_px / h_px
    w_in = max_w_in
    h_in = w_in / aspect
    if h_in > max_h_in:
        h_in = max_h_in
        w_in = h_in * aspect
    run.add_picture(path, width=Inches(w_in), height=Inches(h_in))

def set_cell_shading(cell, hex_color):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hex_color)
    tcPr.append(shd)

def set_cell_border(cell, color=LINE_GRAY, sz=4):
    tcPr = cell._tc.get_or_add_tcPr()
    borders = OxmlElement("w:tcBorders")
    for edge in ("top", "left", "bottom", "right"):
        el = OxmlElement(f"w:{edge}")
        el.set(qn("w:val"), "single")
        el.set(qn("w:sz"), str(sz))
        el.set(qn("w:color"), color)
        borders.append(el)
    tcPr.append(borders)

def add_field(paragraph, field_code, fallback_text="Right-click and choose Update Field."):
    run = paragraph.add_run()
    fld_begin = OxmlElement("w:fldChar"); fld_begin.set(qn("w:fldCharType"), "begin")
    instr = OxmlElement("w:instrText"); instr.set(qn("xml:space"), "preserve"); instr.text = field_code
    fld_sep = OxmlElement("w:fldChar"); fld_sep.set(qn("w:fldCharType"), "separate")
    fld_text = OxmlElement("w:t"); fld_text.text = fallback_text
    fld_end = OxmlElement("w:fldChar"); fld_end.set(qn("w:fldCharType"), "end")
    r_el = run._r
    r_el.append(fld_begin); r_el.append(instr)
    r2 = paragraph.add_run(); r2._r.append(fld_sep)
    r3 = paragraph.add_run(); r3._r.append(fld_text)
    r4 = paragraph.add_run(); r4._r.append(fld_end)

def p(text="", size=10.5, bold=False, italic=False, color=None, space_after=8, align=None, style=None):
    para = doc.add_paragraph(style=style)
    if align is not None:
        para.alignment = align
    para.paragraph_format.space_after = Pt(space_after)
    if text:
        run = para.add_run(text)
        run.font.size = Pt(size)
        run.font.bold = bold
        run.font.italic = italic
        if color:
            run.font.color.rgb = color
    return para

def rich(para, segments, size=10.5):
    """segments: list of (text, bold, italic) tuples appended to an existing paragraph"""
    for seg in segments:
        text, bold, italic = seg
        run = para.add_run(text)
        run.font.size = Pt(size)
        run.font.bold = bold
        run.font.italic = italic

def note_box(text, shade=INFO_SHADE, label="Note"):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.rows[0].cells[0]
    set_cell_shading(cell, shade)
    set_cell_border(cell, "B9D3E0" if shade == INFO_SHADE else "E8C79A")
    cell.paragraphs[0].paragraph_format.space_after = Pt(2)
    run = cell.paragraphs[0].add_run(text)
    run.font.size = Pt(10)
    run.font.color.rgb = GRAY
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def status_run(cell_para, text, kind):
    run = cell_para.add_run(text)
    run.font.bold = True
    run.font.size = Pt(9.5)
    run.font.color.rgb = {"ok": GOOD, "wip": WARN, "gap": GAP}[kind]

def make_table(headers, rows, col_widths=None, status_col=None, font_size=9.5):
    """rows: list of lists; status_col: dict {row_idx: (status_text, kind)} applied to last column override"""
    n_cols = len(headers)
    tbl = doc.add_table(rows=1, cols=n_cols)
    tbl.style = "Table Grid"
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    # ulangi baris header di tiap halaman supaya tabel yang terpotong tetap terbaca
    trPr = tbl.rows[0]._tr.get_or_add_trPr()
    tblHeader = OxmlElement("w:tblHeader")
    tblHeader.set(qn("w:val"), "true")
    trPr.append(tblHeader)
    hdr = tbl.rows[0].cells
    for i, h in enumerate(headers):
        set_cell_shading(hdr[i], HEAD_SHADE)
        hdr[i].paragraphs[0].paragraph_format.space_after = Pt(2)
        r = hdr[i].paragraphs[0].add_run(h.upper())
        r.font.bold = True
        r.font.size = Pt(9)
        r.font.color.rgb = GRAY
    for ridx, row in enumerate(rows):
        _row = tbl.add_row()
        _cantsplit = OxmlElement("w:cantSplit")
        _row._tr.get_or_add_trPr().append(_cantsplit)
        cells = _row.cells
        for cidx, val in enumerate(row):
            cells[cidx].paragraphs[0].paragraph_format.space_after = Pt(2)
            if isinstance(val, tuple) and len(val) == 2 and val[0] == "__status__":
                status_run(cells[cidx].paragraphs[0], val[1][0], val[1][1])
            else:
                r = cells[cidx].paragraphs[0].add_run(str(val))
                r.font.size = Pt(font_size)
                if cidx == 0:
                    r.font.bold = True
    if col_widths:
        tbl.autofit = False
        tblPr = tbl._tbl.tblPr
        layout = OxmlElement("w:tblLayout")
        layout.set(qn("w:type"), "fixed")
        tblPr.append(layout)
        total_w = sum(col_widths)
        tblGrid = tbl._tbl.find(qn("w:tblGrid"))
        for i, gridCol in enumerate(tblGrid.findall(qn("w:gridCol"))):
            gridCol.set(qn("w:w"), str(int(col_widths[i] * 1440)))
        for row in tbl.rows:
            row.width = Inches(total_w)
            for i, w in enumerate(col_widths):
                row.cells[i].width = Inches(w)
    doc.add_paragraph().paragraph_format.space_after = Pt(2)
    return tbl

# ============================================================
# COVER / LETTERHEAD
# ============================================================
DOC_NO = "LGU/GLD/IECEX-TDF/2026-001"
REVISION = "1.1"
DOC_DATE = "25 September 2026"

letterhead = doc.add_table(rows=1, cols=1)
lc = letterhead.rows[0].cells[0]
set_cell_shading(lc, "1A2B3D")
lc.paragraphs[0].paragraph_format.space_after = Pt(2)
lr = lc.paragraphs[0].add_run("PT LAPI GANESHA UTAMA")
lr.font.bold = True; lr.font.size = Pt(14); lr.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
lp2 = lc.add_paragraph()
lp2.paragraph_format.space_after = Pt(3)
lr2 = lp2.add_run("In technical partnership with the Institute of Technology Bandung")
lr2.font.size = Pt(9.5); lr2.font.color.rgb = RGBColor(0xC7, 0xD2, 0xE0)
doc.add_paragraph().paragraph_format.space_after = Pt(14)

p("TECHNICAL CERTIFICATION DOCUMENT", size=10, bold=True, color=GRAY, space_after=4)
title = doc.add_heading(level=0)
title.paragraph_format.space_after = Pt(4)
tr = title.add_run("IECEx/ATEX Certification Document")
tr.font.size = Pt(22); tr.font.bold = True; tr.font.color.rgb = NAVY
title2 = doc.add_paragraph()
title2.paragraph_format.space_after = Pt(10)
tr2 = title2.add_run("Gas Leak Detector (GLD) V2")
tr2.font.size = Pt(16); tr2.font.bold = True; tr2.font.color.rgb = GRAY

p("Prepared in direct reference to the IECEx/ATEX Certification Information Requirements issued by the "
  "certification body (ExCB) \u2014 covering all three sections of that checklist: Section 1, Basic "
  "Information (Application and Organization); Section 2, Technical Documentation (Items 1\u20136: product "
  "description; name, model, and specification list; functional description and technical parameters; "
  "product photographs; intended use and installation environment; and design and manufacturing "
  "information); and Section 3, Sample Information.",
  size=10.5)

p("Document Control", size=11.5, bold=True, color=NAVY, space_after=4)
meta_rows = [
    ("Document title", "IECEx/ATEX Certification Document \u2014 Gas Leak Detector (GLD) V2"),
    ("Document no.", DOC_NO),
    ("Revision", REVISION),
    ("Date", DOC_DATE),
    ("Status", "Working Document \u2014 Draft for Internal Review"),
    ("Classification", "Confidential \u2014 prepared for ATEX/IECEx certification body (ExCB) submission"),
    ("Certification subject", "Node Sensor (GLD) \u2014 V2"),
    ("Manufacturer", "PT Galaksi Megatama Indonesia"),
    ("Design & development authority", "PT LAPI Ganesha Utama"),
    ("Technical partner", "Institute of Technology Bandung"),
    ("Reference checklist", "IECEx/ATEX Certification Information Requirements"),
]
mt = doc.add_table(rows=0, cols=2)
mt.style = "Table Grid"
for k, v in meta_rows:
    row = mt.add_row().cells
    set_cell_shading(row[0], HEAD_SHADE)
    row[0].paragraphs[0].paragraph_format.space_after = Pt(2)
    r = row[0].paragraphs[0].add_run(k)
    r.font.bold = True; r.font.size = Pt(9.5); r.font.color.rgb = GRAY
    row[1].paragraphs[0].paragraph_format.space_after = Pt(2)
    r2 = row[1].paragraphs[0].add_run(v)
    r2.font.size = Pt(10)
    row[0].width = Inches(2.0); row[1].width = Inches(4.5)

doc.add_paragraph().paragraph_format.space_after = Pt(10)

p("Revision History", size=11.5, bold=True, color=NAVY, space_after=4)
rt = doc.add_table(rows=1, cols=3)
rt.style = "Table Grid"
rhdr = rt.rows[0].cells
for i, h in enumerate(["Revision", "Date", "Description"]):
    set_cell_shading(rhdr[i], HEAD_SHADE)
    rhdr[i].paragraphs[0].paragraph_format.space_after = Pt(2)
    r = rhdr[i].paragraphs[0].add_run(h.upper())
    r.font.bold = True; r.font.size = Pt(9); r.font.color.rgb = GRAY
for rev, rev_date, rev_desc in [
    ("0.1", "11 September 2026",
     "Initial issue \u2014 Section 2 (Items 1\u20136) and Section 3."),
    ("0.2", "17 September 2026",
     "Section 1, Basic Information (Application and Organization), added \u2014 Items 1.1\u20131.5. "
     "Document now covers all three sections of the checklist."),
    ("0.3", "22 September 2026",
     "Manufacturer-of-record for Section 1 changed to PT Galaksi Megatama Indonesia (legal documents "
     "on file); PT LAPI Ganesha Utama recorded as design and development authority. Section 2.6.g "
     "draft content (safety warnings, installation procedures, operating modes, commissioning "
     "equipment) added."),
    ("0.4", "22 September 2026",
     "Candidate enclosure component data (ADC12 die-cast alloy, M20\u00d71.5 cable entry, "
     "electrostatic-safety parameters) added to Sections 2.3.c, 2.6.a, and 2.6.c, sourced from a "
     "supplier reference drawing in the casing partner's supply chain."),
    ("0.5", "22 September 2026",
     "Enclosure material grade confirmed as ADC12 (Section 2.3.c, status raised to Final with an explicit "
     "caveat that this extrapolates from the casing manufacturer's sub-component drawing, not a direct "
     "callout on the main enclosure drawing). Cable entry (Section 2.3.c) confirmed as a 2-conductor cable "
     "labeled L+/L\u2212, each conductor \u22480.75 mm diameter."),
    ("0.6", "22 September 2026",
     "Total weight corrected to 2.3 kg; IP rating confirmed as IP66; operating humidity confirmed as "
     "10\u201390% RH non-condensing (standard industrial rating, matched to a comparable certified product); "
     "cable gland confirmed as M20\u00d71.5 (IP66-rated) \u2014 all raised to Final (Section 2.3.c). Removed "
     "the ambiguous \u201cno plastic or PVC\u201d parenthetical from the product description (Section 2.1) "
     "and generalized \u201cL-bracket\u201d to \u201cbracket\u201d in that same narrative sentence (the "
     "dimensioned bracket/U-bolt specification in Section 2.3.c is unaffected). \u201cGLD V2 (Version 2)\u201d "
     "simplified to \u201cGLD V2\u201d."),
    ("0.7", "22 September 2026",
     "\u201cL-bracket\u201d terminology corrected throughout to \u201cU-bolt mounting plate\u201d (Sections "
     "2.1, 2.3.c, 2.6.g), matching the actual CAD drawing (a flat 250\u00d7250 mm plate secured by 2\u00d7 "
     "U-bolts \u2014 not an angled/L-shaped bracket)."),
    ("0.8", "24 September 2026",
     "Total weight, operating temperature, and operating humidity (Sections 2.3.c, 2.5) updated to "
     "2.378 kg, \u221220\u00b0C to +60\u00b0C, and 5\u201395% RH respectively, per current project "
     "specification data."),
    ("0.9", "25 September 2026",
     "Section 2.6.c (material specification sheets, non-metallic materials) expanded with the specific "
     "IEC 60079-0 requirements (CTI class, glow-wire/flame-retardancy, Tg vs. the confirmed operating range, "
     "UV/weathering resistance) and a list of the non-metallic components in GLD's own design that this item "
     "will need to cover (sensor mesh/flame-arrestor cover, cover-to-body sealing gasket, cable-gland seal, "
     "antenna feedthrough insulator); status remains Not yet available pending the casing partner's data."),
    ("1.0", "25 September 2026",
     "Section 2.6.c updated with materials confirmed from a newer casing-partner assembly drawing: the "
     "protective mesh cover is stainless steel (metallic, outside the scope of this non-metallic-materials "
     "item) and the cover-to-body seal is a rubber gasket (compound/grade still not specified)."),
    (REVISION, DOC_DATE,
     "Added an explicit equipment-boundary statement to Section 2.3.a: the Node Sensor (GLD) receives only "
     "24 VDC at its terminal and never carries 220 VAC internally; the AC/DC adapter is a separate, "
     "site-supplied device outside the certified unit's physical boundary. Section 2.6.c cable-gland seal "
     "remark clarified as specified together with the M20×1.5 gland itself from the BP18-1Z reference, "
     "per project direction, rather than as a separately sourced item."),
]:
    rrow = rt.add_row().cells
    for i, v in enumerate([rev, rev_date, rev_desc]):
        rrow[i].paragraphs[0].paragraph_format.space_after = Pt(2)
        r = rrow[i].paragraphs[0].add_run(v)
        r.font.size = Pt(9.5)
for _row in rt.rows:
    _row.cells[0].width = Inches(0.9)
    _row.cells[1].width = Inches(1.3)
    _row.cells[2].width = Inches(4.3)

doc.add_page_break()

# Rapatkan gaya entri daftar isi supaya TOC muat dalam satu halaman
# (dokumen ini punya banyak subjudul level-3: 2.3.a-c, 2.6.a-i).
for _toc_style, _toc_size in (("TOC 1", 9.5), ("TOC 2", 9.0), ("TOC 3", 8.5)):
    try:
        _st = doc.styles[_toc_style]
    except KeyError:
        _st = doc.styles.add_style(_toc_style, WD_STYLE_TYPE.PARAGRAPH)
    _st.font.size = Pt(_toc_size)
    _st.font.name = "Calibri"
    _st.paragraph_format.space_before = Pt(0)
    _st.paragraph_format.space_after = Pt(0)
    _st.paragraph_format.line_spacing = 1.0

p("Table of Contents", size=12, bold=True, color=NAVY, space_after=4)
toc_para = doc.add_paragraph()
add_field(toc_para, 'TOC \\o "1-3" \\h \\z \\u',
          fallback_text="Right-click and choose Update Field to generate the table of contents.")

doc.add_page_break()

# ---------- header / footer ----------
header = sec.header
header.is_linked_to_previous = False
hp = header.paragraphs[0]
hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
hr = hp.add_run("IECEx/ATEX Certification Document \u2014 Gas Leak Detector (GLD) V2  |  Confidential")
hr.font.size = Pt(8); hr.font.color.rgb = GRAY; hr.font.italic = True

footer = sec.footer
footer.is_linked_to_previous = False
fp = footer.paragraphs[0]
fr1 = fp.add_run(f"{DOC_NO}  \u00b7  Rev. {REVISION}")
fr1.font.size = Pt(8); fr1.font.color.rgb = GRAY
tab_stops = fp.paragraph_format.tab_stops
tab_stops.add_tab_stop(Inches(6.5), alignment=2)  # right-aligned tab
fp.add_run("\t")
fr2 = fp.add_run("Page ")
fr2.font.size = Pt(8); fr2.font.color.rgb = GRAY
add_field(fp, "PAGE", fallback_text="1")
fr3 = fp.add_run(" of ")
fr3.font.size = Pt(8); fr3.font.color.rgb = GRAY
add_field(fp, "NUMPAGES", fallback_text="1")

# ============================================================
# ABOUT
# ============================================================
doc.add_heading("About This Document", level=1)
p("This document is a working technical file prepared against the official IECEx/ATEX Certification "
  "Information Requirements checklist issued by the certification body (ExCB). It follows that checklist "
  "section by section: \u201c1. Basic Information (Application and Organization)\u201d, \u201c2. Technical "
  "Documentation\u201d, and \u201c3. Sample Information\u201d. Section 1 is administrative: it sets out "
  "every particular the ExCB requires and states which are already confirmed and which remain to be supplied "
  "from corporate records, without entering assumed values.")
note_box(
    "Scope of this document. This is a compilation of design evidence and an honest readiness assessment "
    "against the ExCB checklist, prepared in support of a future submission — it is not itself a "
    "certificate and does not constitute self-certification. The final enclosure/casing (material selection, "
    "manufacture, gasket, and cable entry) is being developed by an external mechanical/casing partner (PT "
    "Galaksi Megatama Indonesia — legal identity confirmed, Section 1.4) and is not yet in the authors' "
    "possession; items that depend on that design (material datasheets, manufacturing "
    "process description, explosion-protection calculations) are reported as not yet available for that "
    "reason, not because the work has stalled. The product is still at from-scratch development/prototype "
    "stage — no finalized, serialized units exist yet, which is why a formal sample register (Section "
    "3.1) is not yet available either.",
    shade=INFO_SHADE,
)

quote = doc.add_paragraph()
quote.paragraph_format.space_after = Pt(10)
rich(quote, [
    ("Original excerpt, Section 2 & 3 \u2014 source: IECEx ATEX Certification Information "
     "Requirements (ExCB):\n", False, True),
    ("\u201c1) Detailed product description; 2) Product name, model, and specification list; 3) Complete and "
     "clear functional description and technical parameters (electrical parameters, mechanical parameters, "
     "etc.); 4) Clear product photos (overall and key components); 5) Description of intended use and "
     "installation environment (e.g., gas group IIC/IIB/IIA if applicable, temperature group T1\u2013T6, "
     "ambient temperature range, area classification 0/1/2 or 20/21/22); 6) Design and manufacturing "
     "information [a\u2013i: drawings, BOM, material datasheets, manufacturing process, explosion-protection "
     "calculations, temperature group calculation, usage and installation instructions, nameplate "
     "information, Ex component certificates]. 3. Sample Information: 1) model, serial number, and status of "
     "the sample; 2) necessary test fixtures or auxiliary equipment.\u201d", False, True),
], size=9.5)

# ============================================================
# SECTION 1
# ============================================================
doc.add_heading("1. Basic Information (Application and Organization)", level=1)
p("Five items per the original checklist: the application form, the business license/company registration "
  "certificate, the organizational chart and contact information, the manufacturing plant address and "
  "production-facility profile, and — where applicable — the ISO 9001 certificate together with the "
  "quality manual and procedure index.")
note_box("How this section is presented. The items below are administrative rather than technical: they are "
         "satisfied by corporate records held by the manufacturer's legal and administrative functions, not by "
         "engineering output. Every required field is therefore set out in full so that it can be collected in a "
         "single pass, with its current status stated plainly. No field has been filled with an assumed or "
         "placeholder value.", shade=INFO_SHADE)
note_box("Manufacturer-of-record for this section: PT Galaksi Megatama Indonesia. This section reports the "
         "legal/corporate particulars of PT Galaksi Megatama Indonesia as the Manufacturer named in the ExCB "
         "application, since it holds the Indonesian industrial manufacturing business license (NIB) relevant to "
         "fabricating the equipment (KBLI 25119/25120/28221/25920 — metal products, pressurized-vessel-class "
         "containers, metalworking machinery, and special metal-treatment services). PT LAPI Ganesha Utama (LGU) "
         "is the design and development authority responsible for the electronics, firmware, and system "
         "engineering of the GLD, working with the Institute of Technology Bandung as technical partner; it is "
         "recorded as such throughout Sections 2 and 3. This attribution reflects a working decision recorded 22 "
         "September 2026 based on PT Galaksi's legal documents (deed of establishment, NIB, NPWP, MOLHR "
         "ratification decree, tax registration certificate) supplied to the authors — it has not yet been "
         "confirmed directly with either company's officers as the final arrangement for the ExCB submission and "
         "should be verified before formal filing.", shade=WARN_SHADE)

p("Original excerpt, Section 1 — source: IECEx ATEX Certification Information Requirements (ExCB):",
  size=9.5, bold=True, color=NAVY, space_after=2)
p("“1. Basic Information (Application and Organization): 1) Application form (provided by ExCB as a "
  "template). 2) Manufacturer's business license/company registration certificate. 3) Manufacturer's "
  "organizational chart and contact information. 4) Address of manufacturing plant and brief introduction of "
  "production facilities. 5) (If applicable) ISO 9001 certificate, quality manual, and directory of procedure "
  "documents (for QAR/QAN review).”", size=9.5, italic=True)

doc.add_heading("1.0 · Status Summary — Section 1", level=2)
make_table(
    ["Item", "Status", "Held by"],
    [
        ["1.1 Application form (ExCB template)", ("__status__", ("Template not yet received", "gap")),
         "Issued by the ExCB"],
        ["1.2 Business license / company registration", ("__status__", ("Partially available", "wip")),
         "Manufacturer (PT Galaksi Megatama Indonesia) — legal documents now on file; a few particulars still open"],
        ["1.3 Organizational chart and contact information", ("__status__", ("Partially available", "wip")),
         "Manufacturer — Board of Directors/Commissioners names known from the deed; a full org chart and named "
         "ExCB contacts remain to be provided"],
        ["1.4 Manufacturing plant address and facility profile", ("__status__", ("Partially available", "wip")),
         "Manufacturer's registered office and production-site addresses now on file; floor profile, process "
         "capability, and quality system still pending"],
        ["1.5 ISO 9001 certificate, quality manual, procedure index", ("__status__", ("To be confirmed", "gap")),
         "Manufacturer — quality function"],
    ],
    col_widths=[2.9, 1.6, 2.0],
)

doc.add_heading("1.1 · Application Form", level=2)
p("The application form is issued by the certification body as a template and has not yet been received; it is "
  "therefore not reproduced here. The information needed to complete it, however, is already consolidated in "
  "this document, and is restated below in the order an application form normally requests it so that "
  "transcription is a single step once the template arrives.")
make_table(
    ["Application field", "Value", "Status", "Reference"],
    [
        ["Applicant / manufacturer", "PT Galaksi Megatama Indonesia", ("__status__", ("Confirmed", "ok")),
         "Section 1.2"],
        ["Design and development authority", "PT LAPI Ganesha Utama (LGU)",
         ("__status__", ("Confirmed", "ok")), ""],
        ["Technical development partner",
         "Institute of Technology Bandung — IoT Laboratory & Physics Laboratory",
         ("__status__", ("Confirmed", "ok")), ""],
        ["Product name", "Gas Leak Detector (GLD) — Node Sensor", ("__status__", ("Confirmed", "ok")),
         "Section 2.2"],
        ["Model / version", "GLD V2", ("__status__", ("Confirmed", "ok")), "Section 2.2"],
        ["Scope of certification", "Node Sensor (GLD) only", ("__status__", ("Confirmed", "ok")), "Section 2.1"],
        ["Requested area classification", "Zone 1, Equipment Category 2G, Group II",
         ("__status__", ("Requested — subject to ExCB assessment", "wip")), "Section 2.5"],
        ["Requested temperature class", "T4 (≤135 °C)",
         ("__status__", ("Target — verification outstanding", "wip")), "Sections 2.5, 2.6.f"],
        ["Requested gas group", "IIC",
         ("__status__", ("Internal recommendation, not an ExCB decision", "wip")), "Section 2.5"],
        ["Type of protection", "Not yet selected — Ex d, Ex e, and Ex i under evaluation",
         ("__status__", ("Open", "gap")), "Section 2.6.e"],
        ["Standards to be applied",
         "IEC 60079-0, together with the standard corresponding to the type of protection once selected",
         ("__status__", ("Dependent on the item above", "gap")), "Section 2.6.e"],
        ["Certification route requested",
         "IECEx Certificate of Conformity and/or ATEX EU-type examination",
         ("__status__", ("To be confirmed with the ExCB", "gap")), ""],
        ["Intended markets", "To be provided", ("__status__", ("To be provided", "gap")), ""],
    ],
    col_widths=[1.5, 1.9, 1.5, 1.6],
)
p("The three requested classification parameters above are the applicant's proposal. They are recorded here as "
  "a request, not as an agreed or granted classification.", size=9.5, italic=True)

doc.add_heading("1.2 · Business License / Company Registration Certificate", level=2)
make_table(
    ["Required particular", "Status", "Remarks"],
    [
        ["Registered legal name", ("__status__", ("Available", "ok")), "PT Galaksi Megatama Indonesia."],
        ["Legal form and shareholding status", ("__status__", ("Available", "ok")),
         "Perseroan Terbatas (limited liability company), National Private / PMDN (domestic investment), Small "
         "Enterprise scale. Deed No. 52 (22 Sep 2022, Notary Steffi Alphanie, S.H., M.Kn., Cilegon City): "
         "President Director Nur Rohman (2,250 shares), Director Antonius Prasetyo (2,625 shares), Commissioner "
         "Crisa Andi Sujatmiko (2,625 shares); authorized capital Rp300,000,000, paid-up Rp75,000,000."],
        ["Business registration number", ("__status__", ("Available", "ok")),
         "NIB (Business Identification Number) 0510220020593, issued 5 Oct 2022 under Indonesia's risk-based "
         "business licensing (OSS) system."],
        ["Taxpayer identification number", ("__status__", ("Available", "ok")),
         "NPWP 61.126.496.1-427.000 (16-digit: 0611264961427000), Tax Service Office of Pratama West Bekasi, "
         "registered 29 Sep 2022."],
        ["Deed of establishment and latest amendment", ("__status__", ("Partially available", "wip")),
         "Deed of Establishment No. 52 dated 22 Sep 2022, ratified by Ministry of Law and Human Rights Decree No. "
         "AHU-0067398.AH.01.01.Year 2022 (29 Sep 2022, Company Register No. AHU-0194149.AH.01.11.Year 2022). No "
         "subsequent amendment deed has been supplied; whether one exists is unconfirmed."],
        ["Registered (domicile) address", ("__status__", ("Available", "ok")),
         "Plaza Summarecon Bekasi, Jl. Bulevar Ahmad Yani Kav. K.01, Level 7, Harapanmulya Village, Medansatria "
         "Sub-district, Bekasi City, West Java, Postal Code 17143."],
        ["Scope of business activity relevant to this product", ("__status__", ("Partially available", "wip")),
         "NIB lists KBLI 25119 (other prefabricated metal products for construction), 25120 (tanks, reservoirs "
         "and containers of metal – explicitly including pressurized gas cylinders), 28221 (machinery/machine "
         "tools for metalworking), and 25920 (special metal-treatment industrial services), among others, at "
         "production sites in Cikarang Selatan and Mustikajaya, Bekasi. This is a general metal-fabrication "
         "license; it does not by itself constitute an Ex-specific manufacturing qualification."],
        ["Scanned certificate, with English translation where requested", ("__status__", ("Available", "ok")),
         "NIB, NPWP, Deed of Establishment, MOLHR ratification decree, and Certificate of Registration (SKT) are "
         "on file with sworn English translations (Fikri Said Obed, S.S., Sworn Translator, Jakarta, 19 Sep "
         "2026). Notarization/legalization requirements for ExCB submission to be confirmed."],
    ],
    col_widths=[2.1, 1.3, 3.1],
)

doc.add_heading("1.3 · Organizational Chart and Contact Information", level=2)
make_table(
    ["Required particular", "Status", "Remarks"],
    [
        ["Organizational chart", ("__status__", ("Partially available", "wip")),
         "Statutory Board of Directors/Commissioners known from the deed of establishment (below); a functional "
         "chart showing the units responsible for design, production, and quality, and the reporting line "
         "between them, has not been provided."],
        ["Board of Directors and Board of Commissioners", ("__status__", ("Available", "ok")),
         "President Director: Nur Rohman. Director: Antonius Prasetyo. Commissioner: Crisa Andi Sujatmiko. "
         "(Deed No. 52, 22 Sep 2022.)"],
        ["Authorized signatory for the application", ("__status__", ("To be confirmed", "wip")),
         "The President Director (Nur Rohman) is the statutory officer entitled to represent the company "
         "(Articles of Association, Art. 12.5.a); whether he is the specific individual who will sign the ExCB "
         "application is not yet confirmed."],
        ["Certification project contact", ("__status__", ("To be provided", "gap")),
         "Name, position, e-mail, and telephone — the single point of contact for ExCB correspondence."],
        ["Technical contact for the product", ("__status__", ("To be provided", "gap")),
         "The engineer who will answer technical queries on the technical file."],
        ["Quality contact", ("__status__", ("To be provided", "gap")),
         "Counterpart for the quality assessment referred to in 1.5."],
        ["Technical partner contact",
         ("__status__", ("Organization identified; contact to be confirmed", "wip")),
         "Institute of Technology Bandung — IoT Laboratory / Physics Laboratory."],
        ["Correspondence address and working language", ("__status__", ("To be provided", "gap")),
         "English is assumed for correspondence with the ExCB unless stated otherwise."],
    ],
    col_widths=[2.1, 1.3, 3.1],
)

doc.add_heading("1.4 · Manufacturing Plant Address and Introduction of Production Facilities", level=2)
p("The Manufacturer's registered office and NIB-listed production-site addresses are now on file (below). "
  "Facility floor profile, process capability, and quality-system detail are not yet documented. The product is "
  "at prototype stage, and the specific location where serial units will be produced has not been fixed — this "
  "is stated as a fact of the current development phase, not as an omission from the file.")
make_table(
    ["Production element", "Status", "Remarks"],
    [
        ["Manufacturer's registered office and production sites", ("__status__", ("Available", "ok")),
         "PT Galaksi Megatama Indonesia — registered office: Plaza Summarecon Bekasi, Jl. Bulevar Ahmad Yani "
         "Kav. K.01, Level 7, Bekasi City, West Java. NIB-registered production sites: Jl. Kp. Jatipilar, "
         "Cikarang Selatan, Bekasi Regency; and Jl. WR Supratman, Mustikajaya, Bekasi City. NIB lists "
         "metalworking KBLI including 25120 (Manufacture of Tanks, Reservoirs and Containers of Metal – "
         "explicitly covers pressurized gas cylinders), 25119, 28221 (metalworking machinery), and 25920 "
         "(special metal-treatment services). This confirms a licensed general metal-fabrication business — it "
         "is not an Ex-certified enclosure manufacturer license, and no ISO 9001 or Ex-specific quality "
         "certificate has been supplied."],
        ["Printed circuit board fabrication and assembly", ("__status__", ("Partially available", "wip")),
         "The electronic design is maintained by LGU as a native EasyEDA/JLCPCB project and the component supply "
         "chain is referenced to LCSC supplier part numbers throughout the bill of materials (Section 2.6.b). "
         "The fabrication and assembly provider, and its address, remain to be confirmed in writing."],
        ["Enclosure / casing manufacture", ("__status__", ("Partially available", "wip")),
         "Enclosure development and manufacture sits with the Manufacturer, PT Galaksi Megatama Indonesia "
         "(identity and registered addresses above). Plant floor profile, process capability, and Ex-specific "
         "process controls remain to be provided (see remaining rows below and Sections 2.6.c/2.6.d)."],
        ["Final assembly, configuration, and functional test", ("__status__", ("Prototype stage", "wip")),
         "Currently carried out in the development laboratory environment. The production location for serial "
         "units has not been fixed."],
        ["Production facility profile", ("__status__", ("To be provided", "gap")),
         "Floor area, principal equipment, staffing, and nominal throughput — the “brief "
         "introduction” requested by the checklist."],
        ["Incoming inspection and final quality control", ("__status__", ("To be provided", "gap")),
         "Arrangements for verifying purchased components and finished units."],
        ["Ex-specific routine verification", ("__status__", ("To be provided", "gap")),
         "Routine tests and verifications required of production units once a type of protection is selected."],
    ],
    col_widths=[2.1, 1.3, 3.1],
)
p("Where any stage of serial manufacture is subcontracted, certification bodies normally expect each "
  "manufacturing location covered by the quality assessment to be identified by name and address. The final "
  "list of locations therefore depends on the production arrangement adopted after the prototype stage.",
  size=9.5, italic=True)

doc.add_heading("1.5 · ISO 9001 Certificate, Quality Manual, and Procedure Index", level=2)
make_table(
    ["Required particular", "Status", "Remarks"],
    [
        ["ISO 9001 certificate", ("__status__", ("To be confirmed", "gap")),
         "Whether the manufacturer currently holds certification and, if so, the certificate number, scope, "
         "issuing body, and validity period."],
        ["Quality manual", ("__status__", ("To be provided", "gap")), ""],
        ["Index of procedure documents", ("__status__", ("To be provided", "gap")),
         "A directory is sufficient at this stage; individual procedures are normally requested during the "
         "assessment itself."],
        ["Documented control of Ex-relevant characteristics", ("__status__", ("To be provided", "gap")),
         "How drawings, changes, and the characteristics that secure the type of protection are controlled in "
         "production."],
        ["Records of routine verification", ("__status__", ("To be provided", "gap")),
         "Record format for the routine tests referred to in 1.4."],
    ],
    col_widths=[2.1, 1.3, 3.1],
)
note_box("Note on the quality requirement. The checklist marks this item “if applicable” and links it "
         "to quality assessment review. Under both schemes a manufacturer is expected to demonstrate a quality "
         "system covering Ex production before certificates are issued — through an IECEx Quality "
         "Assessment Report, or through the corresponding production-quality or product-verification arrangement "
         "under ATEX — whether or not ISO 9001 certification is held. The route that applies to this "
         "application is to be confirmed with the ExCB; ISO 9001 certification, where held, generally shortens "
         "that assessment rather than replacing it.", shade=INFO_SHADE)

# ============================================================
# SECTION 2
# ============================================================
doc.add_heading("2. Technical Documentation", level=1)
p("Six items per the original checklist (1\u20136, with Item 6 comprising sub-items a\u2013i). This revision "
  "addresses the complete section: Items 1\u20136.")

doc.add_heading("2.1 \u00b7 Detailed Product Description", level=2)
p("The Gas Leak Detector (GLD) is an IoT-based, multi-sensor gas leak detection device designed "
  "for the early detection of flammable and process gases in oil & gas refinery environments (process units, "
  "tank farms, pipe racks, and storage/loading-unloading areas). This document addresses the GLD unit itself "
  "as the subject of the current IECEx/ATEX certification.")
p("Functionally, the GLD integrates eight channels of metal-oxide semiconductor gas sensors (MQ "
  "series), an edge-AI microcontroller/processor (ESP32-S3), and a LoRa radio module (star-topology wireless "
  "transmission) within a single fixed-point unit installed at locations with gas-leak risk. An "
  "on-device AI gas-classification model runs directly on the unit so that detection decisions do not "
  "depend on a continuous connection to a central server. "
  "When gas concentration exceeds a defined threshold, the unit triggers a local alarm (an integrated "
  "visual/audible alarm module) and simultaneously transmits an alarm notification over the LoRa network to "
  "the operator dashboard.")
p("The enclosure is designed for hazardous-area deployment at refinery sites, using metal materials "
  "(aluminum alloy and stainless steel) and mounted via a U-bolt mounting plate to existing "
  "structures without drilling or welding. Important: this design-intent statement does not constitute a "
  "claim that the enclosure has passed testing or has been Ex-certified \u2014 the explosion-protection scheme, "
  "gas group, temperature class, and target installation zone will be addressed in Section 2.5.")
p("The current production power configuration is continuous 24 VDC, supplied via an AC/DC adapter connected "
  "to the site electrical supply. A portable battery power path (Li-ion 18650) remains under development "
  "(R&D) and has not become a deployed production configuration.")

doc.add_heading("2.2 \u00b7 Product Name, Model, and Specification List", level=2)
spec_rows = [
    ("Product name", "Gas Leak Detector (GLD) \u2014 Node Sensor"),
    ("Model / version", "GLD V2"),
    ("Manufacturer", "PT Galaksi Megatama Indonesia"),
    ("Design & development authority", "PT LAPI Ganesha Utama (LGU)"),
    ("Technical development partner", "Institute of Technology Bandung \u2014 IoT Laboratory & Physics Laboratory"),
    ("End client / program owner", "PT Pertamina Patra Niaga (initial deployment site: Refinery Unit IV, Cilacap)"),
    ("Primary function", "Acquisition of 8-channel gas sensor data and LoRa transmission"),
    ("Microcontroller", "ESP32-S3-WROOM-1U-N16R8"),
    ("LoRa radio module", "E22-900MM22S"),
    ("Dimensions (L\u00d7W\u00d7H)", "200 \u00d7 90 \u00d7 290 mm"),
    ("Enclosure material", "Aluminum alloy (ADC12 die-cast) + stainless steel"),
]
st = doc.add_table(rows=0, cols=2); st.style = "Table Grid"
for k, v in spec_rows:
    row = st.add_row().cells
    set_cell_shading(row[0], HEAD_SHADE)
    row[0].paragraphs[0].paragraph_format.space_after = Pt(2)
    r = row[0].paragraphs[0].add_run(k); r.font.bold = True; r.font.size = Pt(9.5); r.font.color.rgb = GRAY
    row[1].paragraphs[0].paragraph_format.space_after = Pt(2)
    r2 = row[1].paragraphs[0].add_run(v); r2.font.size = Pt(10)
    row[0].width = Inches(2.2); row[1].width = Inches(4.3)
doc.add_paragraph().paragraph_format.space_after = Pt(6)
p("Source: official product technical datasheet (Institute of Technology Bandung, Revision 4.0), "
  "cross-referenced with internal technical specification documentation and EMC parameter measurement data.",
  size=9, italic=True, color=GRAY)

doc.add_heading("2.3 \u00b7 Functional Description and Technical Parameters (Electrical, Mechanical, etc.)", level=2)
p("Functional workflow (normal operating mode): sense \u2192 process \u2192 transmit. Each of the eight gas "
  "sensors continuously samples ambient conditions \u2192 data is normalized and classified by the on-device "
  "AI model (ESP32-S3) \u2192 the result is transmitted over the LoRa network (star-topology transmission) at a "
  "configurable interval (default 10 seconds), or immediately (event-driven) when an alarm condition is "
  "detected. Gas alarms are triggered through two parallel channels: a local visual/audible alarm module on "
  "the unit itself, and a push notification transmitted over the LoRa network to the dashboard \u2014 the "
  "alarm-push pathway has been successfully tested on a campus mesh network (field validation at a production "
  "refinery installation is still pending).")

doc.add_heading("2.3.a \u00b7 Electrical Parameters \u2014 Node Sensor (GLD)", level=3)
make_table(
    ["Parameter", "Specification", "Status", "Remarks"],
    [
        ["Main power input", "24 VDC", ("__status__", ("Final \u2014 production config.", "ok")),
         "Continuous power supply from a site AC/DC adapter."],
        ["AC/DC adapter input", "220 VAC, 50 Hz", ("__status__", ("Final", "ok")),
         "Compliant with the Indonesian national electrical grid standard (PLN)."],
        ["AC/DC adapter output", "24 VDC", ("__status__", ("Final", "ok")), ""],
        ["Internal operating voltage", "5 VDC & 3.3 VDC", ("__status__", ("Final", "ok")),
         "5 VDC for the MQ sensor/heater circuitry; 3.3 VDC for ESP32-S3 logic. Per-rail current not yet documented separately."],
        ["Equipment boundary (mains exposure)", "None — 24 VDC only", ("__status__", ("Final", "ok")),
         "The Node Sensor (GLD) itself receives only 24 VDC at its terminal and never carries 220 VAC "
         "internally. The AC/DC adapter (220 VAC/50 Hz → 24 VDC) is a separate, site-supplied device "
         "outside the physical boundary of the certified unit; its own installation location (e.g., relative "
         "to the hazardous-area zone) is a site electrical-design matter, not a parameter of this equipment."],
        ["Maximum input current", "\u22480.33 A @ 24 VDC", ("__status__", ("Calculated", "ok")),
         "Calculated from measured maximum power consumption (7.995 W) divided by 24 VDC."],
        ["Maximum power consumption", "7.995 W @ 24 VDC", ("__status__", ("Measured \u2014 production config.", "ok")),
         "Applies to the continuous-power configuration. The battery (R&D) configuration is recorded separately at 5.75 W \u2014 a different operating mode, not a data conflict."],
        ["Electrical protection (fuse, reverse polarity, overvoltage, overcurrent)",
         "2\u00d7 resettable PPTC fuse (F1/F2); TVS/ESD suppression diodes (D1, D4/D5/D11, D6); Schottky diodes (D7/D13, D8/D9, D12)",
         ("__status__", ("Partially available \u2014 component-level evidence", "wip")),
         "Real components exist per the EasyEDA/JLCPCB bill of materials (Section 2.6.b): 2\u00d7 Littelfuse "
         "MINISMDC260F/16 resettable fuses (F1, F2, overcurrent), a Ruilong SMBJ33A TVS diode (D1) and 3\u00d7 "
         "UMW LESD5D5.0CT1G / 1\u00d7 DOWO SM712 ESD-protection arrays (D4, D5, D11, D6), and multiple Schottky "
         "diodes \u2014 MDD SS54 (D7, D13), MDD SS14 (D8, D9), GOOD-ARK SK36 (D12). This is genuine evidence "
         "that overcurrent and transient/ESD protection circuitry exists on the board; which specific rail "
         "each component protects and its exact circuit role (e.g., reverse-polarity blocking vs. flyback) "
         "has not yet been cross-checked against the schematic net list, and no consolidated protection-scheme "
         "write-up has been produced for ExCB review."],
    ],
    col_widths=[1.6, 1.5, 1.1, 2.3],
)

doc.add_heading("2.3.b \u00b7 Sensor and Communication Parameters \u2014 Node Sensor (GLD)", level=3)
make_table(
    ["Parameter", "Specification", "Status", "Remarks"],
    [
        ["Gas sensors", "MQ-2, MQ-3B, MQ-4, MQ-5, MQ-6, MQ-7B, MQ-8, MQ-135 (8 channels)",
         ("__status__", ("Final", "ok")), "Metal-oxide semiconductor sensors; sensing element directly exposed to ambient air."],
        ["AI gas-classification model", "On-device classifier \u2014 3 classes: Clean Air, LPG, H\u2082",
         ("__status__", ("Final", "ok")),
         "Runs locally on the ESP32-S3 (Running/Inference mode); outputs a class label and a confidence value. Does not yet cover CO\u2082, Benzene, CO, or H\u2082S."],
        ["Environmental sensor (temperature/humidity)", "SHT40-AD1B-R2 (I2C)",
         ("__status__", ("Final", "ok")), "Auxiliary temperature/humidity input included in the primary hardware design; values are available for status/telemetry."],
        ["Analog-to-digital converter", "ADS1256IDBR", ("__status__", ("Final", "ok")),
         "24-bit multi-channel analog acquisition for the 8 sensor channels; 30,000 SPS, firmware SPI clock 1.92 MHz."],
        ["Processing unit", "ESP32-S3-WROOM-1U-N16R8", ("__status__", ("Final", "ok")),
         "Certified under FCC (2AC7Z-ESPS3WROOM1U), TELEC, and CE (per Espressif data) \u2014 RF/EMC certifications, not an \u201cEx component\u201d certification."],
        ["Communication module", "LoRa, E22-900MM22S module", ("__status__", ("Final", "ok")),
         "Certified under CE, FCC, and RoHS (per Ebyte data) \u2014 RF/EMC certifications, not an \u201cEx component\u201d certification."],
        ["Operating frequency", "920 MHz", ("__status__", ("Final", "ok")),
         "Star-topology transmission; within the regional 920\u2013923 MHz ISM band (Indonesia)."],
        ["Transmit power (firmware configuration)", "17 dBm", ("__status__", ("Final", "ok")),
         "The radio module supports up to 22 dBm \u2014 17 dBm is an operational configuration, not the module's maximum limit."],
        ["Bandwidth / spreading factor / coding rate", "125 kHz / SF7 / CR 4/5", ("__status__", ("Final", "ok")), "Source: EMC parameter table and official product technical datasheet."],
        ["Antenna", "External, omnidirectional, SMA male connector, 3 dBi gain", ("__status__", ("Final", "ok")),
         "On some units, the 2.4 GHz Wi-Fi antenna remains inside the enclosure and must be relocated externally."],
        ["Data transmission interval", "Configurable, default 10 seconds", ("__status__", ("Final", "ok")),
         "Alarm events are transmitted immediately, independent of the periodic interval."],
        ["Other interfaces", "SPI, LoRa", ("__status__", ("Final", "ok")),
         "External ports/connectors: USB, sensor, power, fan, antenna, alarm buzzer."],
        ["RS-485 / Modbus interface", "Read-only Modbus RTU slave, 9600 bit/s 8N1, Unit ID 1 (THVD1410DR transceiver)",
         ("__status__", ("Final", "ok")),
         "Provides 8 read-only registers (device status word, classification result, confidence, battery voltage, power source, external power, LoRa transmission counter, node ID); not used for product control."],
    ],
    col_widths=[1.5, 1.7, 1.1, 2.2],
)

doc.add_heading("2.3.c \u00b7 Mechanical Parameters \u2014 Node Sensor (GLD)", level=3)
make_table(
    ["Parameter", "Specification", "Status", "Remarks"],
    [
        ["Enclosure material", "Aluminum alloy (ADC12 die-cast) + stainless steel",
         ("__status__", ("Final", "ok")),
         "Per project confirmation, the production enclosure is sourced from a commercially available "
         "CE/ATEX-marketed explosion-proof gas-detector housing product line (referenced supplier listing: "
         "Alibaba.com, “CE ATEX Explosion Proof H2 Sensor”), consistent with the cast-metal housing, "
         "threaded “Ex”-marked cable entry, and sensor mesh cover shown in the product photography "
         "(Section 2.4). This is corroborated by an internal case CAD drawing (“GLD ATEX CASE v3,” "
         "dated 8 September 2026) specifying a cylindrical sensor-case body (Ø102 mm outer housing ring, "
         "Ø90/Ø80 mm internal bores) that incorporates a stainless-steel filter mesh disc, a small DC "
         "cooling fan, and a transparent viewing window. PVC is not used in any housing or bracket "
         "component. Alloy grade — ADC12: the enclosure metal is die-cast aluminum grade ADC12 (a standard, "
         "widely used die-cast aluminum alloy), per project confirmation. Caveat on how this grade was "
         "established: ADC12 is the material called out on a Chinese enclosure-component manufacturer's "
         "drawing for a related die-cast sub-component (“Universal Base,” part no. BP18-1Z, from the "
         "same casing-partner supply chain — see Section 2.6.a); the “GLD ATEX CASE v3” drawing of "
         "the main enclosure body itself does not carry its own material callout. The project has confirmed "
         "ADC12 as the enclosure grade on the basis that the same casing manufacturer's die-cast product line "
         "uses this alloy consistently — this is an extrapolation from the supplier's sub-component drawing, "
         "not a direct material callout on the main enclosure drawing, and should be verified against the "
         "casing partner's own datasheet for the enclosure body before formal ExCB submission."],
        ["Dimensions (L \u00d7 W \u00d7 H)", "200 \u00d7 90 \u00d7 290 mm", ("__status__", ("Final", "ok")),
         "Consistent between the technical specification documentation and the EMC parameter table."],
        ["Total weight", "2.378 kg", ("__status__", ("Final", "ok")),
         "Total weight of PCB, casing, and sensors combined; project-confirmed value, not yet documented "
         "against a calibrated weighing record."],
        ["Mounting method", "U-bolt mounting plate, following the design already installed at the refinery",
         ("__status__", ("Final", "ok")), "Mounted to existing structures without drilling or welding."],
        ["Ingress protection (IP rating)", "IP66", ("__status__", ("Final", "ok")),
         "Project-confirmed value; not yet independently tested/verified against IEC 60529."],
        ["Cable entry (gland)", "M20\u00d71.5 cable gland (IP66-rated); power cable is 2-conductor, labeled "
         "L+/L\u2212 (positive/negative of the 24 VDC supply), each conductor \u22480.75 mm diameter",
         ("__status__", ("Final", "ok")),
         "Conductor count and per-conductor wire diameter confirmed by the project. Gland thread size "
         "(M20\u00d71.5) is selected by engineering judgment to match the BP18-1Z reference drawing from the "
         "same casing-manufacturer supply chain (Section 2.6.a) \u2014 a standard, IP66-rated gland size well "
         "suited to this conductor count/diameter, not an independent gland datasheet or fit test on GLD's "
         "own enclosure. Overall cable outer diameter and insulation rating remain to be documented."],
        ["Antenna mounting", "External, SMA male connector", ("__status__", ("Final", "ok")), ""],
        ["Operating temperature", "\u221220\u00b0C to +60\u00b0C (ambient)", ("__status__", ("Final", "ok")),
         "Project-confirmed value \u2014 a key input for temperature class (T1\u2013T6) determination in Section 2.5. Not yet documented against a calibrated test record."],
        ["Operating humidity", "5\u201395% RH, non-condensing", ("__status__", ("Final", "ok")),
         "Project-confirmed value. Not yet documented against a calibrated test record."],
    ],
    col_widths=[1.5, 1.9, 1.1, 2.0],
)
p("Source: internal technical specification documentation, Sections 1.1\u20131.3 (Node Sensor), cross-referenced "
  "with the official product technical datasheet (Revision 4.0) and component certification verification "
  "(ESP32-S3-WROOM-1U, E22-900MM22S).",
  size=9, italic=True, color=GRAY)

note_box(
    "Rows marked \u201cPending confirmation\u201d above do not reflect a documentation oversight \u2014 this is an "
    "honest status indicator. These fields are intentionally left blank because no official data yet exists "
    "(not yet measured, tested, or decided). They must not be filled with estimates in future revisions "
    "without a clear supporting data source.",
    shade=WARN_SHADE,
)

doc.add_heading("2.4 \u00b7 Product Photographs \u2014 Overall and Key Components", level=2)
p("The seven photographs below were taken directly from the Node Sensor (GLD) V2 prototype unit (no "
  "capture-date metadata is available in the source files). The first three photographs show the fully "
  "assembled unit from different angles; the remaining four show key components in close-up.")

photos = [
    ("3._Motherboard_ModulSensor_PenutupMesh_Casing_Antena_ModulAlarm.jpg",
     "Complete unit \u2014 front view",
     "The fully assembled Node Sensor (GLD): the main enclosure (blue) with sensor mesh cover, external LoRa "
     "antenna, and a visual alarm module (cylindrical housing, red lens) mounted on the right side."),
    ("Casing_Belakang.jpg",
     "Complete unit \u2014 alternate angle",
     "An alternate view of the assembled unit, showing the position of the antenna, alarm module, and the "
     "cable-gland side of the enclosure."),
    ("PenutupMesh_Casing.jpg",
     "Complete unit \u2014 front view (without antenna and alarm module)",
     "The main enclosure with the sensor mesh cover installed, shown in a flat front view illustrating the "
     "enclosure shape and its four mounting bolt holes."),
    ("1._Motherboard_Casing.jpg",
     "Key component \u2014 PCB inside enclosure (before sensor modules)",
     "The main PCB installed inside the enclosure prior to gas sensor module installation. The "
     "ESP32-S3-WROOM-1U microcontroller, LoRa radio module, and power circuitry are visible."),
    ("2._Motherboard_ModulSensor_Casing.jpg",
     "Key component \u2014 PCB with eight gas sensor modules",
     "The same PCB with eight channels of MQ-series gas sensors (MQ-2, MQ-3B, MQ-4, MQ-5, MQ-6, MQ-7B, MQ-8, "
     "MQ-135) installed around the central microcontroller."),
    ("ModulAlarm.jpg",
     "Key component \u2014 visual alarm module (close-up)",
     "The visual alarm (beacon/strobe) module, constructed of metal with a red lens, connected to the main "
     "enclosure via a dedicated cable gland."),
    ("PenutupMesh.jpg",
     "Key component \u2014 sensor mesh cover (close-up)",
     "The metal mesh cover that protects the gas sensing elements while serving as a diffusion path for gas "
     "to reach the sensors beneath."),
]

# 2-column photo grid via a borderless table
n_photo_cols = 2
photo_tbl = doc.add_table(rows=0, cols=n_photo_cols)
photo_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
for idx in range(0, len(photos), n_photo_cols):
    row_cells = photo_tbl.add_row().cells
    for c in range(n_photo_cols):
        if idx + c >= len(photos):
            break
        fn, title_, desc = photos[idx + c]
        cell = row_cells[c]
        cell.paragraphs[0].paragraph_format.space_after = Pt(2)
        run = cell.paragraphs[0].add_run()
        add_picture_fit(run, os.path.join(PHOTO_DIR, fn), max_w_in=2.75, max_h_in=2.5)
        cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        cap = cell.add_paragraph()
        cap.paragraph_format.space_after = Pt(10)
        r1 = cap.add_run(title_ + "\n"); r1.font.bold = True; r1.font.size = Pt(9.5)
        r2 = cap.add_run(desc); r2.font.size = Pt(8.5); r2.font.color.rgb = GRAY
doc.add_paragraph().paragraph_format.space_after = Pt(4)

note_box(
    "Photographic completeness \u2014 status as-is. The seven photographs above cover the complete unit and its "
    "key components (PCB, sensor modules, alarm module, mesh cover), substantively satisfying checklist Item "
    "2.4. Still outstanding: (a) formally labeled photographs of each face (front/back/left/right/top/bottom) "
    "with a scale reference, as is customary in ExCB submission packages; (b) separate photographs of "
    "individual components such as the battery, gaskets/seals, terminals, and cable glands.",
    shade=INFO_SHADE,
)

doc.add_heading("2.5 \u00b7 Description of Intended Use and Installation Environment "
                 "(Gas Group, Temperature Class, Area Classification)", level=2)
p("The GLD is intended for continuous, fixed-point monitoring of flammable and toxic gas leaks in oil & gas "
  "refinery hazardous areas \u2014 process units, tank farms, pipe racks, and loading/unloading areas. The "
  "specific Ex classification parameters below reflect the project engineering team's current "
  "recommendation, developed from the intended deployment envelope and the gases the device is designed to "
  "detect; none of these parameters has yet been confirmed with the certification body (ExCB) or a notified "
  "body, and none should be treated as final.")
make_table(
    ["Parameter", "Recommended value", "Status", "Rationale / remarks"],
    [
        ["Gas group", "IIC", ("__status__", ("Team recommendation \u2014 pending ExCB confirmation", "wip")),
         "Hydrogen (H\u2082) is one of the three gases the classifier is designed to detect (Section 2.3.b); "
         "IIC is required for hydrogen and inherently covers IIB and IIA."],
        ["Temperature class", "T4 (\u2264135\u00b0C)", ("__status__", ("Team recommendation \u2014 pending verification", "wip")),
         "Not yet substantiated by measurement. MQ-series metal-oxide sensors rely on an internal heating "
         "element as their normal operating principle; a hot-spot measurement specific to the sensor models "
         "and enclosure configuration used here has not yet been performed (see 2.6.f)."],
        ["Ambient temperature range", "\u221220\u00b0C to +60\u00b0C", ("__status__", ("Final", "ok")),
         "Project-confirmed value, consistent with the Mechanical Parameters table (Section 2.3.c). Distinct "
         "from the MQ-sensor hot-spot surface temperature above, which remains the top-priority open item for "
         "the T4 recommendation."],
        ["Area classification (zone)", "Zone 1", ("__status__", ("Team recommendation \u2014 pending ExCB confirmation", "wip")),
         "Assessed as sufficient for the general refinery deployment envelope, including areas near storage. "
         "Zone 0 would only apply if the detector were installed directly inside a tank vapor space."],
    ],
    col_widths=[1.3, 1.1, 1.9, 2.4],
)
note_box(
    "These are engineering recommendations, not a certification decision. An independent readiness "
    "assessment of the same checklist item, prepared separately from the underlying firmware/hardware "
    "repository, reached the same conclusion \u2014 gas group, temperature class, ambient range, and zone "
    "are not yet formally established. Final classification requires explicit agreement with the ExCB.",
    shade=WARN_SHADE,
)

doc.add_heading("2.6 \u00b7 Design and Manufacturing Information", level=2)
p("Nine sub-items (a\u2013i) per the original checklist. Status is reported item by item below; most "
  "sub-items are not yet available \u2014 this is reported plainly rather than implied to be complete.")

doc.add_heading("2.6.a \u00b7 Complete Drawings (Assembly, Component, Electrical Schematic, PCB Layout, "
                 "Enclosure Structure, Junction Box, Terminal, Grounding)", level=3)
p("An electrical schematic capture and a corresponding PCB layout exist for the GLD V2 main board as native "
  "EasyEDA/JLCPCB source design files (not just a derived summary). From the schematic's traced net list, a "
  "supporting block-diagram set (9 sheets, functional/block level, 204 components mapped with documented "
  "pin-to-net traceability) has been produced and is reproduced in full below. Field labels in the source "
  "diagrams are in Indonesian; English captions are provided under each sheet.")
schematic_sheets = [
    ("01-diagram.png", "Sheet 1 of 9 \u2014 Overall architecture",
     "Power input, power distribution, analog acquisition, sensor control, main control (ESP32-S3), and "
     "external interfaces (alarm, RS-485, LoRa antenna, programming/configuration)."),
    ("02-diagram.png", "Sheet 2 of 9 \u2014 Main power",
     "Main power input rails and distribution: +5 V / +5VA analog, 3.3 V, and +24 V for the alarm circuit."),
    ("03-diagram.png", "Sheet 3 of 9 \u2014 Always-on power",
     "The always-on power domain that remains active independent of the main control state."),
    ("04-diagram.png", "Sheet 4 of 9 \u2014 Sensor module",
     "The external gas sensor module: 8 analog channels with per-channel I2C enable, including the sensor, "
     "DAC, and power-switch sub-blocks."),
    ("05-diagram.png", "Sheet 5 of 9 \u2014 Analog acquisition",
     "The 8-channel analog acquisition front end: analog inputs, ADC (ADS1256), reference, and VMID biasing."),
    ("06-diagram.png", "Sheet 6 of 9 \u2014 I2C & sensor control",
     "I2C channel selection (TCA9548A), per-channel sensor enable (PCF8574), and the temperature/humidity "
     "sensor (SHT40)."),
    ("07-diagram.png", "Sheet 7 of 9 \u2014 ESP32 connections",
     "Main controller (ESP32-S3) interface map: SPI to the ADC, I2C to sensor/control, UART for USB and "
     "RS-485, and GPIO for alarm, power, button, and LED."),
    ("08-diagram.png", "Sheet 8 of 9 \u2014 Alarm & status",
     "Alarm output and status-indication circuitry driven from the main controller."),
    ("09-diagram.png", "Sheet 9 of 9 \u2014 System flow",
     "Overall signal and data flow across the board, summarizing how the preceding eight sheets connect end "
     "to end."),
]
for fn, title, desc in schematic_sheets:
    fig_para = doc.add_paragraph()
    fig_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    fig_run = fig_para.add_run()
    fig_run.add_picture(os.path.join(SCHEMATIC_DIR, fn), width=Inches(5.6))
    fig_cap = doc.add_paragraph()
    fig_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    fig_cap.paragraph_format.space_after = Pt(12)
    fcr1 = fig_cap.add_run(title + "\n")
    fcr1.font.bold = True; fcr1.font.size = Pt(9.5)
    fcr2 = fig_cap.add_run(desc)
    fcr2.font.size = Pt(8.5); fcr2.font.color.rgb = GRAY
pcb_fig_para = doc.add_paragraph()
pcb_fig_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
pcb_fig_run = pcb_fig_para.add_run()
pcb_fig_run.add_picture(os.path.join(SCHEMATIC_DIR, "10-pcb-layout.png"), width=Inches(2.7))
pcb_fig_run2 = pcb_fig_para.add_run("   ")
pcb_fig_run2.add_picture(os.path.join(SCHEMATIC_DIR, "11-pcb-3d-render.png"), width=Inches(2.7))
pcb_fig_cap = doc.add_paragraph()
pcb_fig_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
pcb_fig_cap.paragraph_format.space_after = Pt(12)
pcr1 = pcb_fig_cap.add_run("Main board PCB layout (top copper) and 3D populated render\n")
pcr1.font.bold = True; pcr1.font.size = Pt(9.5)
pcr2 = pcb_fig_cap.add_run(
    "Both exported directly from the EasyEDA/JLCPCB source project (production-intent board, circular "
    "outline with six mounting holes). The 3D render shows the ESP32-S3-WROOM module, micro-USB connector, "
    "power inductors, and 8-channel I2C header block in their real placed positions; it is an illustrative "
    "render, not a dimensioned drawing."
)
pcr2.font.size = Pt(8.5); pcr2.font.color.rgb = GRAY
p("A dimensioned mechanical drawing sheet also exists for the enclosure's external envelope and its "
  "mounting hardware, drafted from a solid CAD model (STEP format, millimeter units) with a formal title "
  "block, orthographic and isometric views, and a parts table \u2014 reproduced below.")
DRAWING_DIR = os.path.join(REPO, "scripts", "assets", "cert_doc_drawings")
bd_fig_para = doc.add_paragraph()
bd_fig_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
bd_fig_run = bd_fig_para.add_run()
bd_fig_run.add_picture(os.path.join(DRAWING_DIR, "bracket-mounting-drawing.png"), width=Inches(6.2))
bd_fig_cap = doc.add_paragraph()
bd_fig_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
bd_fig_cap.paragraph_format.space_after = Pt(12)
bdr1 = bd_fig_cap.add_run("Enclosure envelope & mounting bracket \u2014 dimensioned drawing sheet\n")
bdr1.font.bold = True; bdr1.font.size = Pt(9.5)
bdr2 = bd_fig_cap.add_run(
    "Orthographic and isometric views with real dimensions (enclosure neck \u00d875 mm, overall probe height "
    "191.51 mm, mounting plate 250\u00d7250 mm with toleranced hole pattern), a U-bolt parameter table "
    "(2\u2033/DN50, M10 thread), and a title block (drafted 31 Aug 2026). Source: dimensioned CAD drawing "
    "derived from a STEP solid model of the enclosure and bracket assembly."
)
bdr2.font.size = Pt(8.5); bdr2.font.color.rgb = GRAY
make_table(
    ["Drawing type", "Status", "Remarks"],
    [
        ["Electrical schematic (component-level) / block diagram", ("__status__", ("Partially available", "wip")),
         "Schematic capture and a derived 9-sheet block-diagram set exist with traceability evidence "
         "(pin-to-net mapping). Not yet issued in a released, revision-controlled drawing format with a "
         "formal drawing number."],
        ["PCB layout", ("__status__", ("Partially available", "wip")),
         "Native EasyEDA/JLCPCB layout export (routed copper) and a 3D solid model exist for the same board "
         "revision. Not yet issued as a dimensioned, toleranced, released drawing with a formal drawing "
         "number."],
        ["Assembly drawing", ("__status__", ("Partially available", "wip")),
         "A dimensioned drawing sheet exists for the enclosure/bracket mounting assembly (title block, "
         "orthographic + isometric views, parts table). It covers the external envelope and mounting "
         "hardware, not the internal PCB/component assembly sequence."],
        ["Component drawing", ("__status__", ("Not yet available", "gap")), ""],
        ["Enclosure structure drawing (gap, length, volume)", ("__status__", ("Partially available", "wip")),
         "External envelope is dimensioned (from a real STEP solid model, millimeter units) in the drawing "
         "above. The Ex-d-specific flame-path parameters \u2014 joint gap, length, and free internal volume "
         "\u2014 are not called out; that dimensioning has to be added deliberately once a protection concept "
         "is confirmed (Section 2.5), not derived automatically from the CAD export."],
        ["Junction box / terminal / grounding connection drawings",
         ("__status__", ("Candidate reference only", "wip")),
         "A Chinese enclosure-component supplier's drawing for a die-cast “Universal Base” (part no. "
         "BP18-1Z, material ADC12, 0.6 kg, drawing scale 1:1) has been received via the casing partner's supply "
         "chain. It specifies 2× M20×1.5-6H cable-entry threads, 4× M4-6H and 1× M5×1.5-6g "
         "fixing threads, 3× Ø8 mm mounting holes, an internal bore up to Ø94.7 mm, and overall "
         "dimensions approximately 124×115×67.5 mm. Its footprint does not match GLD's main enclosure "
         "(200×90×290 mm), so this is understood as a candidate junction-box/terminal sub-component "
         "under evaluation, not yet confirmed as part of GLD's design. A dedicated grounding connection drawing "
         "has not been provided."],
    ],
    col_widths=[2.6, 1.3, 2.8],
)
note_box(
    "Real dimensioned CAD drawings now exist for the enclosure's external envelope and mounting hardware, "
    "and native PCB layout/schematic source files exist for the electronics. What is still missing for a "
    "certifiable drawing package: internal component/assembly drawings, junction box and "
    "grounding-connection drawings, and \u2014 specific to explosion protection \u2014 flame-path gap/length/"
    "volume dimensioning, which requires a confirmed protection concept before it can be drawn.",
    shade=INFO_SHADE,
)

doc.add_heading("2.6.b \u00b7 Bill of Materials (BOM) for Explosion-Safety-Relevant Components", level=3)
mb_rows = load_bom("motherboard.csv")
sb_rows = load_bom("sensorboard.csv")
mb_lines, mb_qty = len(mb_rows), sum(int(r[4]) for r in mb_rows)
sb_lines, sb_qty = len(sb_rows), sum(int(r[4]) for r in sb_rows)
p(f"A complete, itemized electronic-component BOM for both the main board and the external sensor board now "
  f"exists, exported directly from the EasyEDA/JLCPCB source project (manufacturer, manufacturer part "
  f"number, and LCSC supplier part number for each line item; {mb_lines} line items / {mb_qty} placed "
  f"components on the main board, {sb_lines} line items / {sb_qty} placed components on the sensor board "
  f"\u2014 full tables below). This is real, traceable sourcing data and materially improves on the previous "
  f"status.")
p("It does not, however, satisfy this checklist item as written. The checklist asks specifically for the "
  "explosion-safety-relevant BOM \u2014 enclosure, gaskets, terminals, cable entry devices, switches, light "
  "sources, battery, potting compound, and plastic parts, each with material grade and Ex/UL/CCC "
  "certification status. None of those mechanical/safety items appear in an electronic CAD BOM: the "
  "enclosure is present only as a placeholder mechanical symbol (designator U50, no manufacturer or "
  "dimensional data attached), and the gas sensor itself (MQ2, designator I1) has no manufacturer or "
  "supplier part number recorded \u2014 it is sourced outside the LCSC/JLCPCB supply chain and its Ex status "
  "is unverified. Comparative research on Ex-rated enclosure products from other manufacturers exists "
  "internally as a reference for target specifications only \u2014 it describes third-party products, not "
  "this product's actual components, and is not included here.")
make_table(
    ["Designator", "Value / part", "Qty", "Manufacturer", "Manufacturer part no.", "LCSC #"],
    bom_table_rows(mb_rows),
    col_widths=[1.0, 1.35, 0.4, 1.15, 1.65, 0.85],
    font_size=7.5,
)
p("External sensor board (gas-sensing front end):")
make_table(
    ["Designator", "Value / part", "Qty", "Manufacturer", "Manufacturer part no.", "LCSC #"],
    bom_table_rows(sb_rows),
    col_widths=[1.0, 1.35, 0.4, 1.15, 1.65, 0.85],
    font_size=7.5,
)
note_box(
    "Status: Partially available. Full electronic-component BOM with real manufacturer/supplier data now "
    "exists (source: EasyEDA/JLCPCB export, 11 Sep 2026). The explosion-safety-relevant subset the checklist "
    "actually asks for \u2014 enclosure, gasket, cable entry device, battery, potting compound, and the gas "
    "sensor itself, with material grade and Ex/UL/CCC certification for each \u2014 remains not yet compiled. "
    "These are mechanical/safety parts, not electronic components: the enclosure itself is under design by an "
    "external mechanical/casing development partner (legal identity now confirmed as PT Galaksi Megatama "
    "Indonesia — see Section 1.4) and its bill of materials has not yet been provided to the authors.",
    shade=WARN_SHADE,
)

doc.add_heading("2.6.c \u00b7 Material Specification Sheets / Datasheets (Non-Metallic Materials)", level=3)
p("Datasheets or supplier conformity declarations for non-metallic materials (enclosure components, seals, "
  "insulators, potting compounds) \u2014 covering heat/cold resistance, anti-aging, anti-static, flame "
  "retardancy, CTI value, and chemical resistance \u2014 have not yet been collected.")
p("Per IEC 60079-0:2017, once GLD's specific non-metallic components are identified the applicable "
  "requirements are: a Comparative Tracking Index (CTI) class per Table 5/6 appropriate to the equipment's "
  "creepage/clearance design; a glow-wire or needle-flame flame-retardancy result per \u00a726.4\u201326.5; a "
  "glass-transition temperature (Tg) safely outside the confirmed \u221220\u00b0C to +60\u00b0C ambient operating "
  "range (Section 2.3.c); and UV/weathering-resistance data for any component exposed outdoors. These "
  "thresholds are cited from the standard itself and have not yet been matched against actual component "
  "datasheets.")
p("Non-metallic components in the design that this item will need to cover: the cover-to-body sealing "
  "gasket providing the IP66 rating (Section 2.3.c \u2014 identified as a rubber gasket in the casing "
  "partner's assembly drawing, specific compound/grade not yet specified); the integral seal of the "
  "candidate M20\u00d71.5 cable gland \u2014 per project direction, specified together with the gland "
  "itself from the BP18-1Z reference (Section 2.3.c), rather than as a separately sourced component; and "
  "the antenna/SMA feedthrough insulator (material not yet specified). The protective mesh cover over the "
  "gas-sensing element is now identified as a stainless-steel wire mesh in the same assembly drawing "
  "\u2014 being metallic, it falls outside this "
  "specific non-metallic-materials checklist item.")
note_box(
    "Status: Not yet available. Dependent on the enclosure design and material selection, which sits with "
    "the external casing development partner (PT Galaksi Megatama Indonesia, Section 1.4) rather than the "
    "authors; this data has been formally requested from that partner. Partial candidate data: the BP18-1Z "
    "reference drawing (Section 2.6.a) specifies a powder-coating surface treatment with two "
    "electrostatic-safety parameters directly relevant to this checklist item \u2014 "
    "maximum surface charge transfer <10 nC and maximum surface capacitance <5 pF (coating thickness \u2264 0.2 "
    "mm). These are the type of parameter IEC 60079-0 requires for coated/non-metallic surfaces on Ex "
    "equipment, but they describe a supplier's candidate component, not a confirmed datasheet for GLD's own "
    "enclosure finish.",
    shade=INFO_SHADE,
)

doc.add_heading("2.6.d \u00b7 Manufacturing Process Description", level=3)
p("A description of manufacturing processes relevant to explosion-protection safety (enclosure machining "
  "accuracy control, explosion-proof surface treatment, welding, potting, die-casting, bonding) has not yet "
  "been documented.")
note_box(
    "Status: Not yet available. This describes the casing partner's (PT Galaksi Megatama Indonesia) "
    "manufacturing process, not an internal electronics process \u2014 it will need to be obtained from that "
    "partner once their process is finalized.",
    shade=INFO_SHADE,
)

doc.add_heading("2.6.e \u00b7 Explosion-Protection Calculations and Explanations (if applicable)", level=3)
p("Calculations depend on the explosion-protection concept selected (e.g., Ex d, Ex e, Ex i), which has not "
  "yet been confirmed with the ExCB, and on final enclosure geometry from the casing development partner. No "
  "calculations have been performed.")
note_box(
    "Status: Not yet available \u2014 pending protection-concept confirmation and final enclosure design.",
    shade=INFO_SHADE,
)

doc.add_heading("2.6.f \u00b7 Temperature Group Calculation (Hottest-Point Temperature Estimation)", level=3)
p("No hottest-point temperature calculation or measurement has been performed for this product. As general "
  "context: MQ-series metal-oxide gas sensors operate using an internal heating element, a class of sensor "
  "commonly associated with published operating temperatures in the approximate 200\u2013400\u00b0C range \u2014 "
  "however, this is a general characteristic of the sensor class, not a measured value for the specific "
  "sensor models, drive circuitry, and enclosure configuration used in this product. A worst-case hot-spot "
  "measurement is identified as the top-priority action required to substantiate the recommended T4 "
  "classification in Section 2.5.")
note_box("Status: Not yet available.", shade=INFO_SHADE)

doc.add_heading("2.6.g \u00b7 Usage and Installation Instructions (Draft)", level=3)
make_table(
    ["Sub-item", "Status", "Remarks"],
    [
        ["a) Safety warnings", ("__status__", ("Draft available", "wip")),
         "Drafted below (18 Sep 2026); not yet reviewed against a selected explosion-protection concept."],
        ["b) Installation requirements (cable entry, torque, grounding, cleaning)",
         ("__status__", ("Draft available", "wip")),
         "Procedural text drafted below; the mechanical mounting method itself (U-bolt mounting plate, no drilling/welding "
         "\u2014 Section 2.3.c) and the specific cable gland/torque values are still pending final component "
         "selection."],
        ["c) Operating instructions and maintenance requirements", ("__status__", ("Draft available", "wip")),
         "Drafted below, alongside a firmware command/operation reference (Serial, MQTT, LoRa protocol) used "
         "for engineering commissioning. Ex-specific maintenance frequency/content is not yet defined pending "
         "protection-concept selection."],
    ],
    col_widths=[2.4, 1.3, 3.0],
)
note_box(
    "Status: Draft text available (source: internal working draft, Rev. 18 Sep 2026). This is a draft for "
    "review, not a finalized, Ex-approved installation and operation manual. It has not been checked against a "
    "selected type of protection (Ex d/e/i, Section 2.6.e), a confirmed temperature class (Section 2.6.f), or "
    "finalized cable-entry/enclosure hardware. It also feeds the standalone Instruction_Manual_GLD deliverable.",
    shade=WARN_SHADE,
)

p("2.6.g.a \u00b7 Safety Warnings (Draft)", size=10.5, bold=True, color=NAVY, space_after=2)
for _b in [
    "Only trained and authorized personnel may install, commission, operate, inspect, or maintain the detector.",
    "Isolate and verify the 24 VDC supply before opening the enclosure or changing wiring. Apply the site "
    "lockout/tagout procedure.",
    "Use only the approved production power arrangement: 24 VDC.",
    "Perform alarm tests with appropriate site controls and hearing protection where audible devices are "
    "connected.",
    "Perform sensor nulling only in confirmed clean air. Accept the operation only when all eight sensors "
    "report a complete 8/8 result; otherwise correct the cause and repeat.",
    "Do not drill, weld, enlarge cable entries, bypass protective devices, or modify the enclosure without "
    "written engineering and Ex approval.",
    "Remove the unit from service if there is visible damage, water ingress, an unresolved sensor fault, "
    "failed alarm proof, or a loss of protective-earth continuity.",
]:
    bp = doc.add_paragraph(style="List Bullet")
    bp.paragraph_format.space_after = Pt(2)
    br = bp.add_run(_b)
    br.font.size = Pt(10)

p("2.6.g.b \u00b7 Detailed Installation Requirements (Draft)", size=10.5, bold=True, color=NAVY, space_after=2)
p("Cable entry method: Use only cable glands, adaptors, blanking elements, and seals approved for the final "
  "protection concept, certificate, thread form, IP rating, cable outer diameter, and installation "
  "temperature. Do not create new entries, enlarge an entry, leave unused entries open, or substitute a "
  "general-purpose gland. Maintain the manufacturer sealing and clamping sequence. Record the installed "
  "component part number and certificate reference.", size=10)
p("Torque requirements: Torque values shall comply with the approved enclosure, terminal, cable-gland, and "
  "blanking-plug manufacturer instructions. (Specific torque figures are not yet available \u2014 dependent on "
  "final hardware selection.)", size=10)
p("Grounding requirements: Connect the enclosure to the approved protective-earth system using the "
  "designated grounding terminal. Verify continuity before energization.", size=10)
p("Cleaning requirements: For routine cleaning, isolate the equipment as required by site procedure and use "
  "a soft lint-free cloth lightly dampened with clean water or an approved mild cleaner. Do not use "
  "abrasives, aggressive solvents, dry compressed air, high-pressure spray, or tools that can damage the "
  "enclosure, gasket, label, antenna, or cable entries. Keep liquid out of all openings.", size=10)

p("2.6.g.c \u00b7 Operating Instructions and Maintenance Requirements (Draft)", size=10.5, bold=True, color=NAVY,
  space_after=2)
p("Before each operating period, check power, enclosure condition, diagnostic status, communication status, "
  "and the absence of active faults. Treat an alarm as a real process-safety event until the site response "
  "procedure establishes otherwise. If the detector reports a fault or loses required communication, notify "
  "the responsible operator and place the affected detection point in the site impairment process. Do not "
  "change firmware, model files, alarm thresholds, or calibration parameters from the field without "
  "controlled approval and a documented rollback path.", size=10)
p("Three operating modes are distinguished:", size=10)
make_table(
    ["Mode", "Purpose", "Use restriction"],
    [
        ["Inference", "Normal gas-class inference and alarm operation", "Production operating mode after "
         "commissioning"],
        ["Dataset", "Engineering / data-collection activity", "Not a substitute for approved detection "
         "operation"],
        ["Nulling", "Sensor baseline / calibration activity", "Clean air only; perform under approved "
         "procedure; require complete 8/8 result"],
    ],
    col_widths=[1.3, 3.0, 2.4],
)

doc.add_heading("2.6.h \u00b7 Nameplate Information", level=3)
p("Nameplate artwork cannot yet be finalized: it depends on the certificate number, protection marking, "
  "temperature class, ambient range, IP rating, and serialization scheme \u2014 none of which has been "
  "assigned yet.")
note_box("Status: Not yet available.", shade=INFO_SHADE)

doc.add_heading("2.6.i \u00b7 Ex Component Certificates", level=3)
p("No components in this design currently hold an Ex component certificate. As noted in Section 2.3.b, the "
  "processing unit (ESP32-S3-WROOM-1U-N16R8) and the communication module (E22-900MM22S) hold RF/EMC "
  "certifications (FCC, TELEC, CE, RoHS) \u2014 these are not Ex component certificates and do not satisfy "
  "this item.")
note_box("Status: Not yet available.", shade=INFO_SHADE)

# ============================================================
# SECTION 3
# ============================================================
doc.add_heading("3. Sample Information", level=1)
p("Model, serial number, and sample status (whether the unit can be powered on and operated), together with "
  "any required test fixtures or auxiliary equipment.")

doc.add_heading("3.1 \u00b7 Model, Serial Number, and Status", level=2)
p("No formal sample register or dossier for ExCB submission has been established. Internal engineering and "
  "bench testing reference the \u201cGLD V2\u201d board configuration under firmware environment gld_v2; a "
  "discrete unit serial-numbering scheme for certification samples has not yet been implemented.")
note_box(
    "Status: Not yet available. The product is still being built from scratch at prototype/development "
    "stage; no finalized, serialized unit yet exists to register as a submission sample. This item becomes "
    "actionable once a build reaches a stable, submission-ready configuration.",
    shade=INFO_SHADE,
)

doc.add_heading("3.2 \u00b7 Test Fixtures and Auxiliary Equipment", level=2)
p("A draft internal functional test plan identifies the minimum equipment anticipated for bench-level "
  "verification (this plan has not yet been executed and is not evidence of lab readiness):")
make_table(
    ["Test group", "Minimum equipment"],
    [
        ["Firmware / serial", "Engineering commissioning tool or serial terminal; firmware package with recorded version"],
        ["I2C / ADC / DAC", "No additional equipment for protocol-level acknowledgement/readback; multimeter or oscilloscope where physical voltage must be substantiated"],
        ["Power / watchdog timer", "Controlled 24 V supply, an applicable battery source, multimeter, and oscilloscope/logic analyzer"],
        ["Alarm", "The actual alarm load, multimeter/oscilloscope, and hearing protection if an audible buzzer is fitted"],
        ["LoRa", "At least one counterpart Cluster Head/Gateway device with recorded configuration"],
        ["RS-485 / Modbus", "An RS-485/USB-RS485 master with proper termination and the agreed register map"],
    ],
    col_widths=[1.8, 4.9],
)
note_box(
    "Status: Draft plan only \u2014 not yet executed, and not evidence of ExCB/laboratory test readiness.",
    shade=INFO_SHADE,
)

p("A second, commissioning-oriented equipment list is drafted separately (source: internal working draft, "
  "Rev. 18 Sep 2026), organized by physical test apparatus rather than by test group:")
make_table(
    ["Equipment", "Purpose"],
    [
        ["Regulated 24 VDC power supply", "Provides a stable 24 VDC supply to the GLD during commissioning "
         "and functional testing."],
        ["Digital multimeter", "Measures the actual voltage, verifies polarity and continuity, and supports "
         "grounding/bonding verification."],
        ["Calibrated gas source / gas test kit", "Provides the required gas types to verify that the sensors "
         "respond correctly when exposed to the target gases."],
        ["Gas test chamber", "Provides a controlled gas-exposure environment so that gas concentration, "
         "exposure time, and test conditions can be reproduced."],
        ["Alarm load / relay simulator", "Physically verifies that the alarm output and connected electrical "
         "load operate correctly."],
        ["LoRa peer / gateway", "Verifies that data transmitted by the GLD is successfully received by the "
         "intended system."],
        ["Laptop and approved software", "Used to review diagnostic information, configuration, logging, "
         "firmware identification, and to store commissioning and test evidence."],
        ["Calibrated torque screwdriver", "Ensures that glands, terminals, enclosure fasteners, and "
         "grounding connections are tightened to the approved torque values."],
    ],
    col_widths=[2.0, 4.7],
)

# ============================================================
# FOOTER NOTE
# ============================================================
foot = doc.add_paragraph()
foot.paragraph_format.space_before = Pt(10)
r = foot.add_run(
    "This is a working document, prepared in stages, drafted in direct reference to the IECEx/ATEX "
    "Certification Information Requirements (original English/Mandarin version issued by the certification "
    "body). Data sources: the official product technical datasheet (Institute of Technology Bandung, "
    "Revision 4.0), internal technical specification documentation, EMC parameter measurement data, and "
    "product photography. Fields marked \u201cPending confirmation\u201d are not yet final and must not be "
    "relied upon for procurement or certification purposes without further verification."
)
r.font.size = Pt(8.5)
r.font.italic = True
r.font.color.rgb = RGBColor(0x8A, 0x8A, 0x8A)

doc.save(OUT_PATH)
print("written", OUT_PATH)
