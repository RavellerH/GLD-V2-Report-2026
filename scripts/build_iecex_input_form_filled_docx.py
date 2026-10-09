# -*- coding: utf-8 -*-
"""Build Deliverables/IECEx_ATEX_Certification_Information_Requirements_GLD.docx

A filled-in, English-only, professionally formatted version of the working-draft
template `Sumber Dokumen/input form sertifikasi/IECEx ATEX Certification
Information Requirements_Rev18092026.docx`. Follows that template's own
section/item flow and narrative style (leaner than the exhaustive item-by-item
status tracking in Dokumen_Teknis_Sertifikasi_GLD_IECEx_ATEX.docx, which
remains the authoritative, more granular companion document). Task-style
annotations in the source template (e.g. "(DARI PT GALAXY)",
"(MINTA KE VENDOR CASING)") are rewritten here as professional status notes.
"""
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
DRAWING_DIR = os.path.join(REPO, "scripts", "assets", "cert_doc_drawings")
IM_CAD_DIR = os.path.join(REPO, "scripts", "assets", "instruction_manual_cad")
BOM_DIR = os.path.join(REPO, "scripts", "assets", "cert_doc_bom")
OUT_PATH = os.path.join(REPO, "Deliverables", "IECEx_ATEX_Certification_Information_Requirements_GLD.docx")

def load_bom(fn):
    with open(os.path.join(BOM_DIR, fn), encoding="utf-8") as f:
        rows = list(csv.reader(f))
    return rows[1:]

def bom_summary(rows):
    lines = len(rows)
    qty = sum(int(r[4]) for r in rows)
    return lines, qty

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
normal = doc.styles["Normal"]
normal.font.name = "Calibri"
normal.font.size = Pt(10.5)
normal.font.color.rgb = RGBColor(0x2B, 0x2B, 0x2B)
normal.paragraph_format.space_after = Pt(8)
normal.paragraph_format.line_spacing = 1.25

for i, sz, col in [(1, 16, NAVY), (2, 13, NAVY), (3, 11, NAVY), (4, 10.5, NAVY), (5, 10, NAVY), (6, 9, NAVY)]:
    st = doc.styles[f"Heading {i}"]
    st.font.name = "Calibri"
    st.font.size = Pt(sz)
    st.font.bold = True
    st.font.color.rgb = col
    st.font.italic = False
    st.paragraph_format.space_before = Pt(16 if i == 1 else 12)
    st.paragraph_format.space_after = Pt(6)

sec = doc.sections[0]
sec.left_margin = sec.right_margin = Cm(2.2)
sec.top_margin = sec.bottom_margin = Cm(1.8)

def add_picture_fit(run, path, max_w_in, max_h_in):
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
    for seg in segments:
        text, bold, italic = seg
        run = para.add_run(text)
        run.font.size = Pt(size)
        run.font.bold = bold
        run.font.italic = italic

def status_line(label, size=9.5):
    para = doc.add_paragraph()
    para.paragraph_format.space_after = Pt(10)
    r = para.add_run("Status: ")
    r.font.size = Pt(size); r.font.bold = True; r.font.color.rgb = GRAY
    r2 = para.add_run(label)
    r2.font.size = Pt(size); r2.font.italic = True; r2.font.color.rgb = GRAY
    return para

def note_box(text, shade=INFO_SHADE):
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

def make_table(headers, rows, col_widths=None, font_size=9.5):
    tbl = doc.add_table(rows=1, cols=len(headers))
    tbl.style = "Table Grid"
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr = tbl.rows[0].cells
    for i, h in enumerate(headers):
        set_cell_shading(hdr[i], HEAD_SHADE)
        hdr[i].paragraphs[0].paragraph_format.space_after = Pt(2)
        r = hdr[i].paragraphs[0].add_run(h)
        r.font.bold = True; r.font.size = Pt(9); r.font.color.rgb = GRAY
    for row in rows:
        cells = tbl.add_row().cells
        for i, val in enumerate(row):
            cells[i].paragraphs[0].paragraph_format.space_after = Pt(2)
            r = cells[i].paragraphs[0].add_run(str(val))
            r.font.size = Pt(font_size)
    if col_widths:
        for trow in tbl.rows:
            for i, w in enumerate(col_widths):
                if i < len(trow.cells):
                    trow.cells[i].width = Inches(w)
    doc.add_paragraph().paragraph_format.space_after = Pt(6)
    return tbl

def caption(text, size=8.5):
    cp = doc.add_paragraph()
    cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cp.paragraph_format.space_after = Pt(12)
    r = cp.add_run(text)
    r.font.size = Pt(size); r.font.color.rgb = GRAY; r.font.italic = True

def figure(path, max_w=6.2, max_h=None, cap=None):
    fp_ = doc.add_paragraph()
    fp_.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = fp_.add_run()
    add_picture_fit(run, path, max_w, max_h or 9)
    if cap:
        caption(cap)

# ============================================================
# COVER
# ============================================================
DOC_NO = "GMI/GLD/IECEX-CIR/2026-001"
REVISION = "2.2"
DOC_DATE = "9 October 2026"

letterhead = doc.add_table(rows=1, cols=1)
lc = letterhead.rows[0].cells[0]
set_cell_shading(lc, "1A2B3D")
lc.paragraphs[0].paragraph_format.space_after = Pt(2)
lr = lc.paragraphs[0].add_run("PT GALAKSI MEGATAMA INDONESIA")
lr.font.bold = True; lr.font.size = Pt(14); lr.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
lp2 = lc.add_paragraph()
lp2.paragraph_format.space_after = Pt(3)
lr2 = lp2.add_run("Manufacturer of record")
lr2.font.size = Pt(9.5); lr2.font.color.rgb = RGBColor(0xC7, 0xD2, 0xE0)
doc.add_paragraph().paragraph_format.space_after = Pt(14)

p("CERTIFICATION INFORMATION REQUIREMENTS — FILLED WORKING COPY", size=10, bold=True, color=GRAY, space_after=4)
title = doc.add_heading(level=0)
title.paragraph_format.space_after = Pt(4)
tr = title.add_run("IECEx/ATEX Certification Information Requirements")
tr.font.size = Pt(20); tr.font.bold = True; tr.font.color.rgb = NAVY
title2 = doc.add_paragraph()
title2.paragraph_format.space_after = Pt(10)
tr2 = title2.add_run("Gas Leak Detector (GLD) V2")
tr2.font.size = Pt(15); tr2.font.bold = True; tr2.font.color.rgb = GRAY

p("This document follows, item by item, the section order of the ExCB information-requirements checklist, "
  "filled in with the confirmed design data of the GLD and a status note for each item.", size=10.5)

p("Document Control", size=11.5, bold=True, color=NAVY, space_after=4)
meta_rows = [
    ("Document title", "IECEx/ATEX Certification Information Requirements — Gas Leak Detector (GLD) V2 (Filled Working Copy)"),
    ("Document no.", DOC_NO),
    ("Revision", REVISION),
    ("Date", DOC_DATE),
    ("Status", "Working Document — Draft for Internal Review"),
    ("Classification", "Confidential — prepared for ATEX/IECEx certification body (ExCB) submission"),
    ("Based on", "IECEx/ATEX Certification Information Requirements checklist (ExCB)"),
    ("Applicant / Manufacturer", "PT Galaksi Megatama Indonesia"),
    ("Companion document", "Technical documentation file GMI/GLD/IECEX-TDF/2026-001 (exhaustive item-by-item "
     "status) — authoritative for item-level status where the two documents differ"),
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
    row[0].width = Inches(2.1); row[1].width = Inches(4.4)

doc.add_paragraph().paragraph_format.space_after = Pt(10)
note_box(
    "Scope of this document. This is a compilation of design evidence and an honest readiness assessment "
    "against the ExCB checklist, prepared in support of a future submission — it is not itself a "
    "certificate and does not constitute self-certification. The product is still at from-scratch "
    "development/prototype stage; no finalized, serialized units exist yet.",
    shade=WARN_SHADE,
)

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
    ("0.1", "22 September 2026",
     "Initial issue — filled in against the ExCB information-requirements checklist, covering all three "
     "sections of the checklist."),
    ("0.2", "22 September 2026",
     "Total weight corrected to 2.3 kg; IP rating confirmed as IP66; operating humidity confirmed as "
     "10–90% RH non-condensing; cable gland confirmed as M20×1.5 (IP66-rated) — all raised to Final "
     "(Section 2.3). Power consumption rounded to 8 W. Removed the ambiguous “no plastic or PVC” "
     "parenthetical from the product description (Section 2.1) and generalized “L-bracket” to "
     "“bracket” in that same narrative sentence (the dimensioned bracket/U-bolt specification in "
     "Section 2.3 is unaffected). “GLD V2 (Version 2)” simplified to “GLD V2”. Layout fix: kept the "
     "Section 2.6.b BOM paragraph together across the page break."),
    ("0.3", "22 September 2026",
     "“Bracket”/“L-bracket” terminology corrected throughout to “U-bolt mounting plate” (Sections 2.1, "
     "2.3, 2.6.a), matching the actual CAD drawing (a flat 250×250 mm plate secured by 2× U-bolts — not "
     "an angled/L-shaped bracket)."),
    ("0.4", "24 September 2026",
     "Total weight, operating temperature, and operating humidity (Section 2.3) updated to 2.378 kg, "
     "−20°C to +60°C, and 5–95% RH respectively, per current project specification data."),
    ("0.5", "28 September 2026",
     "Type of protection narrowed to a single team recommendation, Ex d (flameproof enclosure), in Section "
     "2.5 — selected over Ex e and Ex i based on the existing ADC12 die-cast enclosure with a stainless-steel "
     "mesh flame path and the MQ-sensor heaters' continuous, unregulated power draw. Section 2.6.e updated "
     "accordingly. Still an internal recommendation, not an ExCB decision."),
    ("0.6", "28 September 2026",
     "Applicant/Manufacturer identity simplified to a single entity, PT Galaksi Megatama Indonesia (document "
     "number prefix changed to GMI/...). The separate “design and development authority” and “technical "
     "partner” entries were removed (letterhead, Document Control, Sections 1.2, 1.4)."),
    ("0.7", "30 September 2026",
     "Section 2.6.f populated with a preliminary internal surface-temperature measurement (normal, maximum-load "
     "and fan-stalled conditions), extrapolated to +60°C ambient: highest value ≈114°C against an effective "
     "T4 limit of 130°C. Status raised to Partially available; open measurement items listed."),
    ("0.8", "7 October 2026",
     "Section 2.6.a extended with the released main-board electrical schematic (26 sheets, Section 2.6.a.7) "
     "and ten annotated PCB layout views with board data (Section 2.6.a.8)."),
    ("0.9", "7 October 2026",
     "Section 2.6.a.1 added: complete mechanical, enclosure and assembly drawing set (ATEX CASING v2 sheet and "
     "six CAD views, all seven GLD ATEX CASE v3 sheets, BP18-1Z supplier drawing, component/structure/terminal/"
     "grounding drawings, assembly sequence and MQ sensor dimension drawings), with a drawing register."),
    ("1.0", "7 October 2026",
     "Full audit against the reviewer's revision guide: added 2.4.1 photo-set coverage; 2.6.b.1–2 Ex-critical "
     "mechanical (EX-01…17) and electrical (EL-01…13) BOM; 2.6.c.1 non-metallic materials register (MAT-01…11); "
     "2.6.d.1 manufacturing process control d.1–d.13; 2.6.e.1–3 gas path, ignition-source assessment IS-01…17 and "
     "protection concept e.3.1–e.3.11; 2.6.f.1 temperature-class structure f.1–f.12 with results table; 2.6.g.1 "
     "usage and installation instructions g.2–g.20; 2.6.h.1 proposed nameplate (gas only, −20…+60 °C); 2.6.i.1 "
     "required Ex component certificates; 3.3–3.4 sample register (GLD2-0x1001) and fixtures; compliance matrix."),
    ("1.1", "7 October 2026",
     "Section 2.4.2 added: photo set of the current production configuration (23 photographs, Figures 4-101–4-123); EX-05 fan model (CIXIKEJI CX5010B5H, 5 V 0.23 A), EX-07 polymer prototype gland to be replaced by a certified Ex d gland, EX-08/EX-12/EX-17 and photo-coverage table updated."),
    ("1.2", "7 October 2026",
     "Section 2.6.a.8: GLD V4 main board and PCB cover (terminal board) renders added (Figure 8-11) with the changes from V3."),
    ("1.3", "7 October 2026",
     "Nameplate location added: top face of the base beside the antenna (Figure 4-124; 2.6.h.1)."),
    ("1.4", "7 October 2026",
     "Antenna interface photographs added (Figures 4-125, 4-126); EX-09 updated."),
    ("1.5", "7 October 2026",
     "Estimated thread dimensions added (Figure 4-127; e.3.12): cover \u2248M100 \u00d7 2, entries M20 \u00d7 1.5, antenna SMA 1/4\u2033-36 UNS \u2014 estimates pending the enclosure drawing."),
    ("1.6", "7 October 2026",
     "Caliper measurements of the base and cover O-ring added (Figures 4-128\u20134-132; e.3.12, EX-01/02/06): neck wall 10.50/5.80 mm, thread height \u224814.8 mm, bore \u2248\u00d884.7 mm, O-ring cord \u00d82.70 mm; cover thread re-estimated \u2248M96 \u00d7 1.5."),
    ("1.7", "7 October 2026",
     "Further measurements added (Figures 4-133\u20134-137): base depth \u224845 mm, cover thread length \u224818.9 mm, cover depth \u224847.5 mm, O-ring OD \u224891.0 mm; free volume \u22480.4 L (indicative)."),
    ("1.8", "7 October 2026",
     "Measured sketches MS-01\u2026MS-04 of the cover-to-base joint added (e.3.13), illustrative, from caliper measurements."),
    ("1.9", "7 October 2026",
     "Proposed nameplate artwork MS-05 (2.6.h.1) and terminal/field-wiring diagram MS-06 (2.6.g.1) added (drafts)."),
    ("2.0", "7 October 2026",
     "Navigation: five-level Table of Contents, List of Drawings/Figures with page numbers, PDF bookmarks to individual drawings and photographs; photo groups added. No technical content changed."),
    ("2.1", "7 October 2026",
     "Audit against the reviewer's revision guide: application form received and completed; ISO 9001 in progress; internal file names and working-draft references removed; product description and 2.5 completed (gas path, EPL Gb, Tamb, humidity, gas-only scope, installation conditions); shared sections updated as in the technical documentation file rev. 2.8."),
    (REVISION, DOC_DATE,
     "Figures showing the superseded antenna position (antenna on the side of the base) withheld: earlier prototype photographs, ATEX CASING v2 and GLD ATEX CASE v3 drawings, assembly steps M-E7/M-E9; references repointed. Revised drawings to follow."),
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

for _lvl, (_toc_style, _toc_size) in enumerate((("TOC 1", 10.5), ("TOC 2", 9.5), ("TOC 3", 9), ("TOC 4", 8.5), ("TOC 5", 8)), 1):
    try:
        _st = doc.styles[_toc_style]
    except KeyError:
        _st = doc.styles.add_style(_toc_style, WD_STYLE_TYPE.PARAGRAPH)
    _st.font.size = Pt(_toc_size)
    _st.font.name = "Calibri"
    _st.font.bold = (_lvl == 1)
    _st.paragraph_format.left_indent = Cm(0.45 * (_lvl - 1))
    _st.paragraph_format.space_before = Pt(0)
    _st.paragraph_format.space_after = Pt(2)

p("Table of Contents", size=13, bold=True, color=NAVY, space_after=6)
toc_para = doc.add_paragraph()
add_field(toc_para, 'TOC \\o "1-5" \\h \\z \\u',
          fallback_text="Right-click and choose Update Field to generate the table of contents.")

try:
    _st6 = doc.styles["TOC 6"]
except KeyError:
    _st6 = doc.styles.add_style("TOC 6", WD_STYLE_TYPE.PARAGRAPH)
_st6.font.size = Pt(8.5)
_st6.font.name = "Calibri"
_st6.paragraph_format.left_indent = Cm(0)
_st6.paragraph_format.space_before = Pt(0)
_st6.paragraph_format.space_after = Pt(0)
doc.add_page_break()
p("List of Drawings, Schematic Sheets, Sketches and Photographs", size=12, bold=True, color=NAVY, space_after=2)
p("Every drawing (M-xx), schematic sheet and layout view (Figure 8-n), measured sketch (MS-xx) and assembly "
  "photograph (Figure 4-1xx) with its page. All entries are also PDF bookmarks.", size=8.5, color=GRAY, space_after=4)
lof_para = doc.add_paragraph()
add_field(lof_para, 'TOC \\h \\z \\t "GLD Figure Title,1"',
          fallback_text="Right-click and choose Update Field to generate the list of drawings.")

doc.add_page_break()

# header / footer
header = sec.header
header.is_linked_to_previous = False
hp = header.paragraphs[0]
hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
hr = hp.add_run("IECEx/ATEX Certification Information Requirements — GLD V2 (Filled)  |  Confidential")
hr.font.size = Pt(8); hr.font.color.rgb = GRAY; hr.font.italic = True

footer = sec.footer
footer.is_linked_to_previous = False
fp = footer.paragraphs[0]
fr1 = fp.add_run(f"{DOC_NO}  ·  Rev. {REVISION}")
fr1.font.size = Pt(8); fr1.font.color.rgb = GRAY
tab_stops = fp.paragraph_format.tab_stops
tab_stops.add_tab_stop(Inches(6.5), alignment=2)
fp.add_run("\t")
add_field(fp, "PAGE", fallback_text="1")
fp.add_run(" of ")
add_field(fp, "NUMPAGES", fallback_text="1")
for run in fp.runs:
    run.font.size = Pt(8); run.font.color.rgb = GRAY

# ============================================================
# SECTION 1 - BASIC INFORMATION
# ============================================================
import sys as _gsys
_gsys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gld_guide_sections as _guide  # noqa: E402
import gld_assembly_photos_section as _photos07  # noqa: E402
_H4 = lambda t: doc.add_heading(t, level=4)  # noqa: E731
doc.add_heading("1. Basic Information (Application and Organization)", level=1)
p("Application form (provided by ExCB as a template). Manufacturer's business license/company registration "
  "certificate. Manufacturer's organizational chart and contact information. Address of manufacturing plant "
  "and brief introduction of production facilities. (If applicable) ISO 9001 certificate, quality manual, and "
  "directory of procedure documents (for QAR/QAN review).", size=9.5, italic=True, color=GRAY)

doc.add_heading("1.1 · Application Form", level=2)
p("Issued by the ExCB as a template (application form A0); the template has been received, completed by the "
  "applicant and submitted together with this dossier.")
status_line("Template received from the ExCB; completed form submitted with the dossier.")

doc.add_heading("1.2 · Manufacturer's Business License / Company Registration Certificate", level=2)
p("The Applicant and Manufacturer named in this application is PT Galaksi Megatama Indonesia, which holds "
  "the Indonesian industrial manufacturing business license (NIB) relevant to fabricating the equipment.")
make_table(
    ["Particular", "Value"],
    [
        ["Registered legal name", "PT Galaksi Megatama Indonesia"],
        ["Legal form", "Perseroan Terbatas (limited liability company), National Private / PMDN, Small Enterprise scale"],
        ["Business registration number (NIB)", "0510220020593, issued 5 Oct 2022 (OSS system)"],
        ["Taxpayer ID (NPWP)", "61.126.496.1-427.000, registered 29 Sep 2022"],
        ["Deed of establishment", "Deed No. 52, 22 Sep 2022 (Notary Steffi Alphanie, S.H., M.Kn., Cilegon City)"],
        ["Ministerial ratification", "MOLHR Decree No. AHU-0067398.AH.01.01.Year 2022 (29 Sep 2022)"],
        ["Registered (domicile) address", "Plaza Summarecon Bekasi, Jl. Bulevar Ahmad Yani Kav. K.01, Level 7, "
         "Bekasi City, West Java 17143"],
        ["Relevant KBLI (business scope)", "25119, 25120 (tanks/reservoirs/containers of metal, incl. "
         "pressurized gas cylinders), 28221, 25920"],
    ],
    col_widths=[2.3, 4.2],
)
status_line("Available — legal documents on file with sworn English translations (Fikri Said Obed, S.S., "
            "19 Sep 2026). Legal form/shareholding, business registration, and domicile address confirmed; ISO "
            "9001 certification status addressed separately below.")

doc.add_heading("1.3 · Manufacturer's Organizational Chart and Contact Information", level=2)
p("The statutory Board of Directors and Board of Commissioners are known from the deed of establishment:")
make_table(
    ["Position", "Name"],
    [
        ["President Director", "Nur Rohman"],
        ["Director", "Antonius Prasetyo"],
        ["Commissioner", "Crisa Andi Sujatmiko"],
    ],
    col_widths=[2.3, 4.2],
)
status_line("Partially available — statutory officers known. A functional organizational chart (design/"
            "production/quality reporting lines) and named ExCB correspondence contacts (certification project "
            "contact, technical contact, quality contact) have not yet been provided.")

doc.add_heading("1.4 · Address of Manufacturing Plant and Brief Introduction of Production Facilities", level=2)
p("Registered office and NIB-registered production sites of the Manufacturer, PT Galaksi Megatama Indonesia:")
make_table(
    ["Site", "Address / Role"],
    [
        ["Registered office", "Plaza Summarecon Bekasi, Jl. Bulevar Ahmad Yani Kav. K.01, Level 7, Bekasi City, West Java"],
        ["Production site 1", "Jl. Kp. Jatipilar, Cikarang Selatan, Bekasi Regency"],
        ["Production site 2", "Jl. WR Supratman, Mustikajaya, Bekasi City"],
        ["Electronics design/assembly", "Native EasyEDA/JLCPCB project; fabrication/assembly provider and its address to be confirmed in writing"],
    ],
    col_widths=[2.3, 4.2],
)
status_line("Partially available — registered addresses on file (general metal-fabrication license, "
            "KBLI 25120 covers pressurized gas cylinders; not an Ex-specific manufacturing license). Floor "
            "area, principal equipment, staffing, and nominal throughput (“brief introduction” "
            "requested by the checklist) not yet provided. Production location for serial units has not been "
            "fixed — the product is at prototype stage.")

doc.add_heading("1.5 · ISO 9001 Certificate, Quality Manual, and Directory of Procedure Documents (for QAR/QAN review)", level=2)
p("ISO 9001 certification of the manufacturer is currently in progress, with the certification audit planned "
  "for October 2026. The certificate, quality manual, and procedure-document index will be submitted once "
  "available.")
status_line("Open — certification and supporting documents in progress. Under both IECEx and ATEX schemes, a quality system covering Ex "
            "production is expected before certificates are issued (IECEx Quality Assessment Report, or the "
            "corresponding production-quality/product-verification route under ATEX) whether or not ISO 9001 "
            "is held; the applicable route is to be confirmed with the ExCB.")

doc.add_page_break()

# ============================================================
# SECTION 2 - TECHNICAL DOCUMENTATION
# ============================================================
doc.add_heading("2. Technical Documentation", level=1)

doc.add_heading("2.1 · Detailed Product Description", level=2)
p("The Gas Leak Detector (GLD) is an IoT-based, multi-sensor gas leak detection device designed for the "
  "early detection of flammable and process gases in oil & gas refinery environments (process units, tank "
  "farms, pipe racks, and storage/loading-unloading areas).")
p("Functionally, the GLD integrates eight channels of metal-oxide semiconductor gas sensors (MQ series), an "
  "edge-AI microcontroller/processor (ESP32-S3), and a LoRa radio module (star-topology wireless transmission) "
  "within a single fixed-point unit installed at locations with gas-leak risk. An on-device AI gas-"
  "classification model runs directly on the unit so that detection decisions do not depend on a continuous "
  "connection to a central server. Ambient gas enters through the front stainless-steel mesh; an internal DC "
  "fan assists the flow towards the eight MQ sensors, each with its own integrated stainless-steel protective "
  "mesh. When the multi-sensor response pattern and the configured alarm criteria indicate a leak, the unit "
  "triggers a local alarm (an integrated visual/audible alarm module) and simultaneously transmits an alarm "
  "notification over the LoRa network, via the cluster head and gateway, to the operator dashboard.")
p("The enclosure is designed for hazardous-area deployment at refinery sites, using metal materials (aluminum "
  "alloy — ADC12 die-cast grade — and stainless steel) and mounted via a U-bolt mounting plate "
  "to existing structures without drilling or welding. The current production power configuration is "
  "continuous 24 VDC, supplied via an AC/DC adapter (220 VAC/50 Hz → 24 VDC) connected to the site "
  "electrical supply. The Node Sensor (GLD) itself receives only 24 VDC at its terminal and never carries "
  "220 VAC internally — the AC/DC adapter is a separate, site-supplied device outside the physical boundary "
  "of the certified unit.")
note_box(
    "Important: this design-intent description does not constitute a claim that the enclosure has passed "
    "testing or has been Ex-certified. The explosion-protection scheme, gas group, temperature class, and "
    "target installation zone are addressed in Section 2.5.",
    shade=WARN_SHADE,
)

doc.add_heading("2.2 · Product Name, Model, and Specification List", level=2)
make_table(
    ["Field", "Value"],
    [
        ["Product name", "Gas Leak Detector (GLD)"],
        ["Model / version", "GLD V2"],
        ["Manufacturer", "PT Galaksi Megatama Indonesia"],
        ["Program owner", "PT Pertamina Patra Niaga (initial deployment site: Refinery Unit IV, Cilacap)"],
        ["Primary function", "Acquisition of 8-channel gas sensor data and LoRa transmission"],
        ["Microcontroller", "ESP32-S3-WROOM-1U-N16R8"],
        ["LoRa radio module", "E22-900MM22S"],
        ["Dimensions (L×W×H)", "200 × 90 × 290 mm"],
        ["Enclosure material", "Aluminum alloy (ADC12 die-cast) + stainless steel"],
    ],
    col_widths=[2.3, 4.2],
)

doc.add_heading("2.3 · Complete and Clear Functional Description and Technical Parameters (Electrical, Mechanical, etc.)", level=2)
p("Functional workflow (normal operating mode): sense → process → transmit. Each of the eight gas "
  "sensors continuously samples ambient conditions → data is normalized and classified by the on-device AI "
  "model (ESP32-S3) → the result is transmitted over the LoRa network (star-topology transmission) at a "
  "configurable interval, or immediately (event-driven) when an alarm condition is detected. Gas alarms are "
  "triggered through two parallel channels: a local visual/audible alarm module on the unit itself, and a "
  "push notification transmitted over the LoRa network to the dashboard.")

p("Electrical Parameters:", bold=True, size=10.5, space_after=3)
make_table(
    ["Parameter", "Specification"],
    [
        ["Input voltage", "24 VDC (continuous)"],
        ["Source adapter (if AC-fed)", "220 VAC / 50 Hz input → 24 VDC output"],
        ["Internal voltage rails", "5 VDC (sensor/heater circuitry), 3.3 VDC (ESP32-S3 logic)"],
        ["Measured power consumption", "8 W @ 24 VDC (≈ 0.33 A) — production configuration"],
        ["Cable/PSU sizing margin", "≥ 1 A per unit (sizing margin only; actual draw is well below this)"],
        ["Power cable", "2-conductor, labeled L+/L− (positive/negative of the 24 VDC supply), each "
         "conductor ≈ 0.75 mm diameter"],
        ["Electrical protection", "Resettable PPTC fuses (F1/F2), TVS/ESD suppression diodes, Schottky diodes on power rails"],
    ],
    col_widths=[2.3, 4.2],
)

p("Sensor and Communication Parameters:", bold=True, size=10.5, space_after=3)
make_table(
    ["Parameter", "Specification"],
    [
        ["Gas sensor array", "8 channels, metal-oxide (MQ-2, MQ-3B, MQ-4, MQ-5, MQ-6, MQ-7B, MQ-8, MQ-135)"],
        ["Signal acquisition", "24-bit multi-channel ADC (ADS1256IDBR, 30,000 SPS), 500 ms scan interval"],
        ["AI gas-classification model", "On-device classifier — 3 classes: Clean Air, LPG, H₂; "
         "alarm at confidence ≥ 30%. Does not yet cover CO₂, Benzene, CO, or H₂S"],
        ["Temperature/humidity telemetry", "SHT40 sensor (auxiliary)"],
        ["LoRa radio", "E22-900MM22S, star-topology transmission, 920–923 MHz ISM band (Indonesia)"],
        ["Data transmission interval", "Configurable, default 10 s; alarm events transmitted immediately"],
        ["RS-485 / Modbus interface", "Read-only Modbus RTU slave, 9600 bit/s 8N1, Unit ID 1 (THVD1410DR) — "
         "8 read-only registers for external integration; not used for product control"],
    ],
    col_widths=[2.3, 4.2],
)

p("Mechanical Parameters:", bold=True, size=10.5, space_after=3)
make_table(
    ["Parameter", "Specification", "Status"],
    [
        ["Dimensions (L×W×H)", "200 × 90 × 290 mm", "Final"],
        ["Total weight", "2.378 kg", "Final (project-confirmed, not yet calibration-verified)"],
        ["Enclosure material", "Aluminum alloy (ADC12 die-cast) + stainless steel", "Final (see caveat below)"],
        ["Mounting method", "U-bolt mounting plate (2″/DN50), no drilling/welding", "Final"],
        ["Ingress protection (IP rating)", "IP66", "Final"],
        ["Cable entry (gland)", "M20×1.5 cable gland (IP66-rated), power cable L+/L−, ≈ 0.75 mm/conductor", "Final (see note below)"],
        ["Antenna mounting", "External, SMA male connector", "Final"],
        ["Operating temperature range", "−20°C to +60°C (ambient)", "Final (project-confirmed)"],
        ["Operating humidity range", "5–95% RH, non-condensing", "Final (project-confirmed)"],
    ],
    col_widths=[2.1, 2.9, 1.5],
)
note_box(
    "Caveat on the ADC12 enclosure grade. ADC12 is the material called out on a Chinese enclosure-component "
    "manufacturer's drawing for a related die-cast sub-component (“Universal Base,” part no. BP18-1Z, "
    "from the same casing-partner supply chain — Section 2.6.a); the “GLD ATEX CASE v3” drawing "
    "of the main enclosure body itself does not carry its own material callout. ADC12 has been confirmed as "
    "the enclosure grade on the basis that the same casing manufacturer's die-cast product line uses this "
    "alloy consistently — an extrapolation from the supplier's sub-component drawing, not a direct "
    "material callout on the main enclosure drawing. This should be verified against the casing partner's own "
    "datasheet for the enclosure body before formal ExCB submission.",
    shade=WARN_SHADE,
)
note_box(
    "Caveat on cable gland. M20×1.5 matches the thread size used on the BP18-1Z reference drawing from the "
    "same casing manufacturer (Section 2.6.a) and is a standard, IP66-rated gland size well suited to a "
    "2-conductor cable with ≈0.75 mm conductors — selected by engineering judgment from that reference, not "
    "from an independent gland datasheet or fit test on GLD's own enclosure. This should be confirmed by "
    "test/fit-check before formal ExCB submission. The operating temperature and humidity ranges above are "
    "current project-specification values (24 Sep 2026), not yet documented against a calibrated test record.",
    shade=WARN_SHADE,
)

p("Three operating modes are distinguished at firmware level:", size=10.5)
make_table(
    ["Mode", "Purpose", "Use restriction"],
    [
        ["Inference", "Normal gas-class inference and alarm operation", "Production operating mode after commissioning"],
        ["Dataset", "Engineering / data-collection activity", "Not a substitute for approved detection operation"],
        ["Nulling", "Sensor baseline / calibration activity", "Clean air only; approved procedure; requires complete 8/8 result"],
    ],
    col_widths=[1.3, 3.1, 2.3],
)

doc.add_heading("2.4 · Clear Product Photos (Overall and Key Components)", level=2)
import gld_hide_flags as _hide  # noqa: E402
if not _hide.HIDE_SIDE_ANTENNA:
    p("The photographs below were taken directly from the Node Sensor (GLD) V2 prototype unit.")
for fn, cap in [
    ("3._Motherboard_ModulSensor_PenutupMesh_Casing_Antena_ModulAlarm.jpg",
     "Assembled unit — motherboard, sensor module, mesh cover, casing, external antenna, and local alarm module."),
    ("Casing_Belakang.jpg", "Enclosure, rear view — mounting flange and cable-entry area."),
]:
    if _hide.hidden_file(fn):
        continue
    figure(os.path.join(PHOTO_DIR, fn), max_w=4.8, max_h=3.6, cap=cap)

_guide.photos(doc, _H4)
_photos07.render(doc, _H4)
doc.add_heading("2.5 · Description of Intended Use and Installation Environment", level=2)
p("The GLD is intended for continuous, fixed-point monitoring of flammable and selected process gas leaks in "
  "oil & gas refinery hazardous areas: process units, tank farms, pipe racks, and loading/unloading areas.")
make_table(
    ["Parameter", "Value", "Status"],
    [
        ["Gas group", "IIC", "Internal recommendation, not an ExCB decision"],
        ["Temperature class", "T4 (≤135°C)", "Target — preliminary internal measurement supports it (Section 2.6.f); formal verification outstanding"],
        ["Area classification", "Zone 1, Equipment Category 2G, Group II", "Requested — subject to ExCB assessment"],
        ["Type of protection", "Ex d — flameproof enclosure (II 2G Ex db IIC T4 Gb)", "Internal recommendation, not an ExCB decision"],
        ["Equipment protection level", "EPL Gb", "Proposed — subject to ExCB assessment"],
        ["Ambient temperature", "−20 °C to +60 °C", "Rated range"],
        ["Operating humidity", "5–95 % RH, non-condensing", "Rated range"],
        ["Explosive atmosphere", "Gas atmospheres only — combustible dust not included; no dust marking requested", "Final"],
    ],
    col_widths=[1.8, 2.9, 2.0],
)
p("Type of protection selected over Ex e and Ex i based on the existing enclosure design: a die-cast "
  "aluminum (ADC12) housing whose front stainless-steel mesh is the intended flame-path element of the gas "
  "inlet (subject to type test or a certified flame arrestor) — the same pattern used by the three comparable certified gas detectors "
  "reviewed as references (all Ex d). Ex i was set aside because the MQ-series sensor heaters draw "
  "continuous power (≈0.75 W each) directly from an unregulated 24 VDC supply rather than through "
  "certified current-limiting barriers, difficult to reconcile with intrinsically-safe energy limits for "
  "Group IIC.", size=9.5, italic=True)
p("These classification parameters are the applicant's proposal, recorded here as a request, not as an agreed "
  "or granted classification. Installation: fixed mounting by the U-bolt mounting plate with the front mesh "
  "unobstructed; 24 VDC cable through a certified Ex d gland (M20 × 1.5); unused entries closed with certified "
  "Ex d plugs; external protective-earth connection; the cover must not be opened while an explosive "
  "atmosphere may be present.", size=9.5, italic=True)

doc.add_heading("2.6 · Design and Manufacturing Information", level=2)

doc.add_heading("2.6.a · Complete Drawings (Assembly, Component, Electrical Schematic, PCB Layout, Enclosure Structure, Junction Box, Terminal, Grounding)", level=3)
p("An electrical schematic capture and a corresponding 9-sheet block-diagram set exist for the GLD V2 main "
  "board, exported from the native EasyEDA/JLCPCB source project, with pin-to-net traceability evidence.")
figure(os.path.join(SCHEMATIC_DIR, "02-diagram.png"), max_w=6.0, max_h=4.2,
       cap="Schematic block diagram, sheet 2 of 9 — main power distribution.")
figure(os.path.join(SCHEMATIC_DIR, "10-pcb-layout.png"), max_w=4.6, max_h=4.6,
       cap="Main board PCB layout (top copper) — native EasyEDA/JLCPCB export, production-intent board.")
if not _hide.HIDE_SIDE_ANTENNA:
    p("A dimensioned mechanical drawing exists for the enclosure's external envelope and mounting hardware, "
      "drafted from a solid CAD model (STEP format, millimeter units):")
    figure(os.path.join(DRAWING_DIR, "bracket-mounting-drawing.png"), max_w=6.2, max_h=4.6,
           cap="Enclosure envelope & U-bolt mounting plate assembly — dimensioned drawing sheet "
               "(drafted 31 Aug 2026, from a STEP solid model).")
    p("A separate, internal contingency/alternate enclosure design (“GLD ATEX CASE v3”) exists in "
      "parallel with the primary commercial-enclosure sourcing path referenced in Section 2.3:")
    figure(os.path.join(IM_CAD_DIR, "gld_atex_case_v3_dimensioned.png"), max_w=6.2, max_h=4.6,
           cap="“GLD ATEX CASE v3” dimensioned drawing sheet (8 Sep 2026) — "
               "internal contingency/alternate enclosure design, not the confirmed production enclosure.")
p("A candidate junction-box/terminal sub-component drawing has also been received via the casing partner's "
  "supply chain (Chinese enclosure-component manufacturer):")
figure(os.path.join(IM_CAD_DIR, "bp18-1z_common_base_reference.png"), max_w=6.0, max_h=4.6,
       cap="“Universal Base” BP18-1Z — supplier reference drawing (ADC12 die-cast aluminum "
           "alloy, 0.6 kg). Candidate component under evaluation; footprint does not match GLD's main "
           "enclosure, not yet confirmed as part of GLD's design.")
make_table(
    ["Drawing type", "Status"],
    [
        ["Electrical schematic — main board", "Available — 26 sheets PGLD-GLD-V4-MB-SCH-01 to -26, rev. 1.0 (Section 2.6.a.7); sensor-module board schematic not yet included"],
        ["PCB layout — main board", "Partially available — 10 views PGLD-GLD-V4-MB-PCB-01 to -10 (Section 2.6.a.8); layout rev/date, laminate data and sensor-module board layout open"],
        ["Assembly drawing", "Partially available — covers external envelope and mounting hardware, not internal PCB/component assembly sequence"],
        ["Component drawing", "Not yet available"],
        ["Enclosure structure drawing (gap, length, volume)", "Partially available — external envelope dimensioned; Ex-d-specific flame-path parameters not yet called out"],
        ["Junction box / terminal / grounding connection drawings", "Candidate reference only — BP18-1Z drawing above, not yet confirmed as part of GLD's design"],
    ],
    col_widths=[2.9, 3.6],
)

# ---- 2.6.a.7 / 2.6.a.8: released main-board schematic set and PCB layout views (shared content) ----
import sys as _sys
_sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gld_v4_board_section as _board  # noqa: E402
import gld_mech_drawings_section as _mech  # noqa: E402
doc.add_page_break()
_mech.render(doc, h1=lambda t: doc.add_heading(t, level=4), content_w=6.2, num="2.6.a.1")
doc.add_page_break()
_board.render(doc, h1=lambda t: doc.add_heading(t, level=4), h2=lambda t: doc.add_heading(t, level=5), content_w=6.2, num7="2.6.a.7", num8="2.6.a.8")
doc.add_page_break()

h_26b = doc.add_heading("2.6.b · Bill of Materials (BOM) for Key Components Affecting Explosion-Proof Safety", level=3)
h_26b.paragraph_format.keep_with_next = True
mb_lines, mb_qty = bom_summary(load_bom("motherboard.csv"))
sb_lines, sb_qty = bom_summary(load_bom("sensorboard.csv"))
p_26b = p(f"A complete, itemized electronic-component BOM exists for both boards, exported directly from the "
  f"EasyEDA/JLCPCB source project (manufacturer, manufacturer part number, and LCSC supplier part number per "
  f"line item): {mb_lines} line items / {mb_qty} placed components on the main board, {sb_lines} line items / "
  f"{sb_qty} placed components on the sensor board. Full listing maintained in "
  f"the technical documentation file GMI/GLD/IECEX-TDF/2026-001, Section 2.6.b.")
p_26b.paragraph_format.keep_together = True
p_26b.paragraph_format.keep_with_next = True
sl_26b = status_line("Partially available. The explosion-safety-relevant subset the checklist actually asks for "
            "(enclosure, gasket, cable entry device, battery, potting compound, and the gas sensor itself, "
            "with material grade and Ex/UL/CCC certification for each) is compiled in Sections 2.6.b.1–2.6.b.2 "
            "with open items marked per row — these are mechanical/safety parts, not electronic components, and sit with the Manufacturer, PT "
            "Galaksi Megatama Indonesia. The gas sensor itself (MQ2) is sourced outside the LCSC supply chain, "
            "without a manufacturer/LCSC part reference; its Ex status is not yet verified.")
sl_26b.paragraph_format.keep_together = True

_guide.bom(doc, _H4)
doc.add_heading("2.6.c · Material Specification Sheets / Datasheets (Non-Metallic Materials)", level=3)
p("Datasheets or supplier conformity declarations for non-metallic materials (enclosure components, seals, "
  "insulators, potting compounds) — covering heat/cold resistance, anti-aging, anti-static, flame "
  "retardancy, CTI value, and chemical resistance — have not yet been collected.")
p("Per IEC 60079-0:2017, once GLD's specific non-metallic components are identified the applicable "
  "requirements are: a Comparative Tracking Index (CTI) class per Table 5/6 appropriate to the equipment's "
  "creepage/clearance design; a glow-wire or needle-flame flame-retardancy result per §26.4–26.5; a "
  "glass-transition temperature (Tg) safely outside the confirmed −20°C to +60°C ambient operating range "
  "(Section 2.3); and UV/weathering-resistance data for any component exposed outdoors. These thresholds "
  "are cited from the standard itself and have not yet been matched against actual component datasheets.")
p("Non-metallic components in the design that this item will need to cover: the cover-to-body sealing "
  "gasket providing the IP66 rating (Section 2.3 — identified as a rubber gasket in the casing partner's "
  "assembly drawing, specific compound/grade not yet specified); the integral seal of the candidate "
  "M20×1.5 cable gland — per project direction, specified together with the gland itself from the "
  "BP18-1Z reference (Section 2.3), rather than as a separately sourced component; and the antenna/SMA "
  "feedthrough insulator (material not yet specified). The protective mesh cover over the gas-sensing "
  "element is now identified as a "
  "stainless-steel wire mesh in the same assembly drawing — being metallic, it falls outside this specific "
  "non-metallic-materials checklist item.")
status_line("Not yet available, pending the enclosure design and material selection with the casing partner "
            "— this data has been formally requested from that partner. "
            "Partial candidate data: the BP18-1Z reference drawing (Section 2.6.a) specifies a powder-coating "
            "surface treatment with electrostatic-safety parameters directly relevant to this item — "
            "maximum surface charge transfer <10 nC and maximum surface capacitance <5 pF (coating thickness "
            "≤0.2 mm), consistent with IEC 60079-0 coating requirements — but this describes a "
            "supplier's candidate component, not a confirmed datasheet for GLD's own enclosure finish.")

_guide.materials(doc, _H4)
doc.add_heading("2.6.d · Manufacturing Process Description", level=3)
p("A description of manufacturing processes relevant to explosion-protection safety (enclosure machining "
  "accuracy control, explosion-proof surface treatment, welding, potting, die-casting, bonding) has not yet "
  "been documented.")
status_line("Not yet available — this describes the Manufacturer's (PT Galaksi Megatama Indonesia) "
            "process, not an internal electronics process.")

_guide.manufacturing(doc, _H4)
doc.add_heading("2.6.e · Explosion-Protection Calculations and Explanations (if applicable)", level=3)
p("Flame-path (joint gap, length) and free-internal-volume calculations specific to Ex d (Section 2.5, team "
  "recommendation) have not yet been performed, pending final enclosure geometry and ExCB confirmation.")
status_line("Not yet available — pending ExCB confirmation of the Ex d protection concept and final enclosure design.")

_guide.ex_calc(doc, _H4)
doc.add_heading("2.6.f · Temperature Group Calculation (Hottest-Point Temperature Estimation)", level=3)
p("A preliminary internal surface-temperature measurement has been carried out on a GLD V2 unit (eight "
  "thermocouple channels plus ambient; normal operation, maximum load, and fan stalled; 180 minutes each at "
  "approximately 24–25°C ambient). Maximum values, extrapolated to the +60°C maximum rated ambient:")
make_table(
    ["Condition", "MQ sensor body", "PCB", "External enclosure"],
    [
        ["Normal operation", "44.2 → ≈79°C", "52.4 → ≈88°C", "32.1 → ≈67°C"],
        ["Maximum load", "55.0 → ≈91°C", "58.3 → ≈94°C", "34.8 → ≈71°C"],
        ["Fan stalled (malfunction)", "78.4 → ≈114°C", "63.4 → ≈99°C", "43.9 → ≈79°C"],
    ],
    col_widths=[1.9, 1.6, 1.5, 1.7],
)
p("The highest extrapolated value (≈114°C) is below the effective T4 limit of 130°C (135°C less the 5 K "
  "margin under IEC 60079-0). Under the recommended Ex d concept, the external enclosure surface (≈79°C) "
  "governs the temperature class. Open items: DC/DC converter, power inductor and MOSFET/diode not yet "
  "measured; alarm/transmit condition not measured; maximum-load PCB reading not yet at thermal "
  "equilibrium; test metadata (date, unit, thermocouple type, supply voltage) not yet recorded; confirmation "
  "at maximum ambient requires ExCB type testing. Full detail in the companion technical document.")
status_line("Partially available — preliminary internal measurement; indicates T4 is achievable with margin.")

_guide.temperature(doc, _H4)
doc.add_heading("2.6.g · Usage and Installation Instructions (Draft)", level=3)
p("Safety warnings:", bold=True, size=10.5, space_after=3)
for b in [
    "Only trained and authorized personnel may install, commission, operate, inspect, or maintain the detector.",
    "Isolate and verify the 24 VDC supply before opening the enclosure or changing wiring. Apply the site lockout/tagout procedure.",
    "Use only the approved production power arrangement: 24 VDC.",
    "Perform alarm tests with appropriate site controls and hearing protection where audible devices are connected.",
    "Perform sensor nulling only in confirmed clean air. Accept the operation only when all eight sensors report a complete 8/8 result; otherwise correct the cause and repeat.",
    "Do not drill, weld, enlarge cable entries, bypass protective devices, or modify the enclosure without written engineering and Ex approval.",
    "Remove the unit from service if there is visible damage, water ingress, an unresolved sensor fault, failed alarm proof, or a loss of protective-earth continuity.",
]:
    bp = doc.add_paragraph(style="List Bullet")
    bp.paragraph_format.space_after = Pt(2)
    bp.add_run(b).font.size = Pt(10)

p("Detailed installation requirements:", bold=True, size=10.5, space_after=3)
p("Cable entry method: use only cable glands, adaptors, blanking elements, and seals approved for the final "
  "protection concept, certificate, thread form, IP rating, cable outer diameter, and installation "
  "temperature. Do not create new entries, enlarge an entry, leave unused entries open, or substitute a "
  "general-purpose gland. Maintain the manufacturer sealing/clamping sequence and record the installed "
  "component part number and certificate reference.", size=10)
p("Torque requirements: torque values shall comply with the approved enclosure, terminal, cable-gland, and "
  "blanking-plug manufacturer instructions (specific torque figures not yet available, dependent on final "
  "hardware selection).", size=10)
p("Grounding requirements: connect the enclosure to the approved protective-earth system using the designated "
  "grounding terminal; verify continuity before energization.", size=10)
p("Cleaning requirements: isolate the equipment per site procedure and use a soft lint-free cloth lightly "
  "dampened with clean water or an approved mild cleaner; do not use abrasives, aggressive solvents, dry "
  "compressed air, high-pressure spray, or tools that can damage the enclosure, gasket, label, antenna, or "
  "cable entries; keep liquid out of all openings.", size=10)

p("Operating instructions and maintenance requirements:", bold=True, size=10.5, space_after=3)
p("Before each operating period, check power, enclosure condition, diagnostic status, communication status, "
  "and the absence of active faults. Treat an alarm as a real process-safety event until the site response "
  "procedure establishes otherwise. Do not change firmware, model files, alarm thresholds, or calibration "
  "parameters from the field without controlled approval and a documented rollback path.", size=10)
status_line("Partially available (draft) — not yet consolidated into an Ex-specific installation and "
            "operation manual for ExCB review; also feeds the separate GLD instruction manual.")

_guide.usage(doc, _H4)
doc.add_heading("2.6.h · Nameplate Information (must include all ATEX-required marking information)", level=3)
p("Nameplate artwork cannot yet be finalized: it depends on the certificate number, protection marking, "
  "temperature class, ambient range, IP rating, and serialization scheme, none of which has been assigned yet.")
status_line("Not yet available.")

_guide.nameplate(doc, _H4)
doc.add_heading("2.6.i · Ex Component Certificates", level=3)
p("No components in this design currently hold an Ex component certificate. The processing unit "
  "(ESP32-S3-WROOM-1U-N16R8) and the communication module (E22-900MM22S) hold RF/EMC certifications (FCC, "
  "TELEC, CE, RoHS) — these are not Ex component certificates and do not satisfy this item.")
status_line("Not yet available.")

doc.add_page_break()

# ============================================================
# SECTION 3 - SAMPLE INFORMATION
# ============================================================
_guide.ex_certs(doc, _H4)
doc.add_heading("3. Sample Information", level=1)

doc.add_heading("3.1 · Model, Serial Number, and Status of the Sample", level=2)
p("Sample submitted: model GLD V2 (GLD_V2), serial number GLD2-0x1001. The sample powers on and runs in "
  "Inference (normal operation) mode. Full sample register in Section 3.3.")
status_line("Available — sample identified (GLD2-0x1001); firmware/AI-model version to be recorded on the sample label.")

doc.add_heading("3.2 · Necessary Test Fixtures or Auxiliary Equipment", level=2)
p("Equipment anticipated for commissioning and bench-level functional verification:")
make_table(
    ["Equipment", "Purpose"],
    [
        ["Regulated 24 VDC power supply", "Provides a stable 24 VDC supply during commissioning and functional testing."],
        ["Digital multimeter", "Measures actual voltage, verifies polarity and continuity, supports grounding/bonding verification."],
        ["Calibrated gas source / gas test kit", "Provides the required gas types to verify correct sensor response."],
        ["Gas test chamber", "Provides a controlled gas-exposure environment for reproducible test conditions."],
        ["Alarm load / relay simulator", "Verifies that the alarm output and connected electrical load operate correctly."],
        ["LoRa peer / gateway", "Verifies that data transmitted by the GLD is successfully received by the intended system."],
        ["Laptop and approved software", "Reviews diagnostic information, configuration, logging, firmware identification; stores commissioning and test evidence."],
        ["Calibrated torque screwdriver", "Ensures glands, terminals, enclosure fasteners, and grounding connections are tightened to approved torque values."],
    ],
    col_widths=[2.3, 4.2],
)
status_line("Draft plan only — not yet executed, and not evidence of ExCB/laboratory test readiness.")

# ---------- footer note ----------
doc.add_paragraph().paragraph_format.space_before = Pt(10)
foot = doc.add_paragraph()
r = foot.add_run(
    "This is a working document, filled in against the ExCB information-requirements checklist. It follows "
    "the checklist's own section order rather than the more exhaustive item-by-item status tracking of the "
    "technical documentation file GMI/GLD/IECEX-TDF/2026-001 — the two documents are maintained in parallel and should "
    "stay consistent; treat the exhaustive tracking document as authoritative for item-level status where "
    "they differ. Data sources: the official product technical datasheet (Revision 4.0), internal technical "
    "specification documentation, EMC parameter measurement data, EasyEDA/"
    "JLCPCB design exports, and PT Galaksi Megatama Indonesia's legal documents."
)
r.font.size = Pt(9); r.font.color.rgb = GRAY; r.font.italic = True

_guide.sample(doc, _H4)
doc.add_page_break()
_guide.matrix(doc, lambda t: doc.add_heading(t, level=1))

doc.save(OUT_PATH)
print("written", OUT_PATH)
