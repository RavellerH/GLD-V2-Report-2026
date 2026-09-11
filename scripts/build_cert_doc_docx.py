# -*- coding: utf-8 -*-
import os
import csv
from docx import Document
from docx.shared import Pt, Inches, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
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
    hdr = tbl.rows[0].cells
    for i, h in enumerate(headers):
        set_cell_shading(hdr[i], HEAD_SHADE)
        hdr[i].paragraphs[0].paragraph_format.space_after = Pt(2)
        r = hdr[i].paragraphs[0].add_run(h.upper())
        r.font.bold = True
        r.font.size = Pt(9)
        r.font.color.rgb = GRAY
    for ridx, row in enumerate(rows):
        cells = tbl.add_row().cells
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
REVISION = "0.1"
DOC_DATE = "11 September 2026"

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
  "certification body (ExCB) \u2014 covering Section 2, Technical Documentation (Items 1\u20136: product "
  "description; name, model, and specification list; functional description and technical parameters; "
  "product photographs; intended use and installation environment; and design and manufacturing "
  "information) and Section 3, Sample Information. Section 1, Basic Information (Application and "
  "Organization), remains to be completed in a subsequent revision.",
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
    ("Manufacturer", "PT LAPI Ganesha Utama"),
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
rrow = rt.add_row().cells
for i, v in enumerate([REVISION, DOC_DATE,
                       "Initial issue \u2014 Section 2, Items 1\u20136 (product description; name, model, and "
                       "specification list; functional and technical parameters; product photographs; "
                       "intended use and installation environment; design and manufacturing information) "
                       "and Section 3 (sample information)."]):
    rrow[i].paragraphs[0].paragraph_format.space_after = Pt(2)
    r = rrow[i].paragraphs[0].add_run(v)
    r.font.size = Pt(9.5)
rt.rows[0].cells[0].width = rt.rows[1].cells[0].width = Inches(0.9)
rt.rows[0].cells[1].width = rt.rows[1].cells[1].width = Inches(1.3)
rt.rows[0].cells[2].width = rt.rows[1].cells[2].width = Inches(4.3)

doc.add_paragraph().paragraph_format.space_after = Pt(10)

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
p("This document is a working technical file prepared to satisfy Section \u201c2. Technical Documentation\u201d "
  "and Section \u201c3. Sample Information\u201d of the official IECEx/ATEX Certification Information "
  "Requirements checklist issued by the certification body (ExCB). The table of contents follows the "
  "complete structure of the original checklist (Sections 1\u20133); Section 1 (Basic Information) remains "
  "pending and will follow in a subsequent revision.")
note_box(
    "Scope of this document. This is a compilation of design evidence and an honest readiness assessment "
    "against the ExCB checklist, prepared in support of a future submission — it is not itself a "
    "certificate and does not constitute self-certification. The final enclosure/casing (material selection, "
    "manufacture, gasket, and cable entry) is being developed by an external mechanical/casing partner and is "
    "not yet in the authors' possession; items that depend on that design (material datasheets, manufacturing "
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
p("Covers the application form, business license/company registration, organizational chart and contact "
  "information, manufacturing facility address and profile, and (where applicable) ISO 9001 certification.")
note_box("Not yet prepared in this revision. To be completed in a subsequent revision.", shade=INFO_SHADE)

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
  "(aluminum alloy and stainless steel \u2014 no plastic or PVC) and mounted via an L-bracket to existing "
  "structures without drilling or welding. Important: this design-intent statement does not constitute a "
  "claim that the enclosure has passed testing or has been Ex-certified \u2014 the explosion-protection scheme, "
  "gas group, temperature class, and target installation zone will be addressed in Section 2.5 (to follow).")
p("The current production power configuration is continuous 24 VDC, supplied via an AC/DC adapter connected "
  "to the site electrical supply. A portable battery power path (Li-ion 18650) remains under development "
  "(R&D) and has not become a deployed production configuration.")

doc.add_heading("2.2 \u00b7 Product Name, Model, and Specification List", level=2)
spec_rows = [
    ("Product name", "Gas Leak Detector (GLD) \u2014 Node Sensor"),
    ("Model / version", "GLD V2 (Version 2)"),
    ("Manufacturer", "PT LAPI Ganesha Utama"),
    ("Technical development partner", "Institute of Technology Bandung \u2014 IoT Laboratory & Physics Laboratory"),
    ("End client / program owner", "PT Pertamina Patra Niaga (initial deployment site: Refinery Unit IV, Cilacap)"),
    ("Primary function", "Acquisition of 8-channel gas sensor data and LoRa transmission"),
    ("Microcontroller", "ESP32-S3-WROOM-1U-N16R8"),
    ("LoRa radio module", "E22-900MM22S"),
    ("Dimensions (L\u00d7W\u00d7H)", "200 \u00d7 90 \u00d7 290 mm"),
    ("Enclosure material", "Aluminum alloy + stainless steel"),
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
        ["Maximum input current", "\u22480.33 A @ 24 VDC", ("__status__", ("Calculated", "ok")),
         "Calculated from measured maximum power consumption (7.995 W) divided by 24 VDC."],
        ["Maximum power consumption", "7.995 W @ 24 VDC", ("__status__", ("Measured \u2014 production config.", "ok")),
         "Applies to the continuous-power configuration. The battery (R&D) configuration is recorded separately at 5.75 W \u2014 a different operating mode, not a data conflict."],
        ["Backup battery path (R&D, not in production)", "Li-ion 18650 cells, 7 in parallel, 4.2 V/cell, \u224828,000 mAh total",
         ("__status__", ("Development pathway", "wip")),
         "Not yet a deployed production configuration. Cell/BMS safety certification (e.g., UN 38.3, IEC 62133) not yet obtained. Firmware-reported diagnostic thresholds: low battery at 3.50 V, critical at 3.30 V (status/flag only, not an active power cutoff)."],
        ["Electrical protection (fuse, reverse polarity, overvoltage, overcurrent)", "\u2014",
         ("__status__", ("Pending confirmation", "gap")), "Scope of electrical protection not yet defined/documented."],
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
        ["Enclosure material", "Aluminum alloy + stainless steel", ("__status__", ("Specific grade pending", "wip")),
         "PVC is not used in any housing or bracket component. Specific grade still under determination."],
        ["Dimensions (L \u00d7 W \u00d7 H)", "200 \u00d7 90 \u00d7 290 mm", ("__status__", ("Final", "ok")),
         "Consistent between the technical specification documentation and the EMC parameter table."],
        ["Total weight", "\u2014", ("__status__", ("Pending confirmation", "gap")), "Not yet weighed/documented."],
        ["Mounting method", "L-bracket, following the design already installed at the refinery",
         ("__status__", ("Final", "ok")), "Mounted to existing structures without drilling or welding."],
        ["Ingress protection (IP rating)", "\u2014", ("__status__", ("Pending confirmation", "gap")),
         "Not yet tested/determined."],
        ["Cable entry (gland)", "\u2014", ("__status__", ("Pending confirmation", "gap")),
         "Cable gland specification not yet determined."],
        ["Antenna mounting", "External, SMA male connector", ("__status__", ("Final", "ok")), ""],
        ["Operating temperature", "\u2014", ("__status__", ("Pending confirmation", "gap")),
         "Ambient operating temperature range not yet determined \u2014 key parameter for temperature class (T1\u2013T6) determination in Section 2.5."],
        ["Operating humidity", "\u2014", ("__status__", ("Pending confirmation", "gap")), ""],
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
        run.add_picture(os.path.join(PHOTO_DIR, fn), width=Inches(2.75))
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
        ["Ambient temperature range", "\u2014", ("__status__", ("Pending confirmation", "gap")),
         "Not yet measured or specified."],
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
        ["Junction box / terminal / grounding connection drawings", ("__status__", ("Not yet available", "gap")), ""],
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
    "external mechanical/casing development partner and its bill of materials has not yet been provided to "
    "the authors.",
    shade=WARN_SHADE,
)

doc.add_heading("2.6.c \u00b7 Material Specification Sheets / Datasheets (Non-Metallic Materials)", level=3)
p("Datasheets or supplier conformity declarations for non-metallic materials (enclosure components, seals, "
  "insulators, potting compounds) \u2014 covering heat/cold resistance, anti-aging, anti-static, flame "
  "retardancy, CTI value, and chemical resistance \u2014 have not yet been collected.")
note_box(
    "Status: Not yet available. Dependent on the enclosure design and material selection, which sits with "
    "the external casing development partner rather than the authors.",
    shade=INFO_SHADE,
)

doc.add_heading("2.6.d \u00b7 Manufacturing Process Description", level=3)
p("A description of manufacturing processes relevant to explosion-protection safety (enclosure machining "
  "accuracy control, explosion-proof surface treatment, welding, potting, die-casting, bonding) has not yet "
  "been documented.")
note_box(
    "Status: Not yet available. This describes the casing partner's manufacturing process, not an internal "
    "electronics process \u2014 it will need to be obtained from that partner once their process is "
    "finalized.",
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
        ["a) Safety warnings", ("__status__", ("Not yet available", "gap")),
         "No Ex-specific safety warnings have been drafted."],
        ["b) Installation requirements (cable entry, torque, grounding, cleaning)",
         ("__status__", ("Partially available", "wip")),
         "A mechanical mounting method exists separately (L-bracket, installed to existing structures without "
         "drilling or welding \u2014 see Section 2.3.c), but cable-entry method, torque values, grounding "
         "requirements, and cleaning requirements have not yet been formally specified."],
        ["c) Operating instructions and maintenance requirements", ("__status__", ("Partially available", "wip")),
         "A firmware command/operation reference exists (Serial, MQTT, and LoRa command protocol for "
         "engineering use), but it covers software operation and commissioning \u2014 not Ex-specific "
         "maintenance or inspection requirements (frequency, content, precautions)."],
    ],
    col_widths=[2.4, 1.3, 3.0],
)
note_box(
    "Status: Partially available \u2014 not yet consolidated into an Ex-specific installation and operation "
    "manual for ExCB review.",
    shade=INFO_SHADE,
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

# ============================================================
# FOOTER NOTE
# ============================================================
doc.add_paragraph()
foot = doc.add_paragraph()
foot.paragraph_format.space_before = Pt(14)
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
