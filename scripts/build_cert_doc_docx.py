# -*- coding: utf-8 -*-
import os
from docx import Document
from docx.shared import Pt, Inches, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PHOTO_DIR = os.path.join(REPO, "scripts", "assets", "cert_doc_photos")
OUT_PATH = os.path.join(REPO, "Deliverables", "Dokumen_Teknis_Sertifikasi_GLD_IECEx_ATEX.docx")

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

def make_table(headers, rows, col_widths=None, status_col=None):
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
                r.font.size = Pt(9.5)
                if cidx == 0:
                    r.font.bold = True
    if col_widths:
        for i, w in enumerate(col_widths):
            for row in tbl.rows:
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
  "certification body (ExCB) \u2014 Section 2, Technical Documentation, Items 1\u20134: product description, "
  "product name/model/specification list, functional description and technical parameters, and product "
  "photographs. This document is being developed in stages; remaining items will follow in subsequent revisions.",
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
                       "Initial issue \u2014 Section 2, Items 1\u20134 (product description; name, model, and "
                       "specification list; functional and technical parameters; product photographs)."]):
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
  "of the official IECEx/ATEX Certification Information Requirements checklist issued by the certification "
  "body (ExCB). The table of contents follows the complete structure of the original checklist (Sections "
  "1\u20133); sections not yet completed are marked as pending and will follow in subsequent revisions.")

quote = doc.add_paragraph()
quote.paragraph_format.space_after = Pt(10)
rich(quote, [
    ("Original excerpt, Section 2, Items 1\u20134 \u2014 source: IECEx ATEX Certification Information "
     "Requirements (ExCB):\n", False, True),
    ("\u201c1) Detailed product description; 2) Product name, model, and specification list; 3) Complete and "
     "clear functional description and technical parameters (electrical parameters, mechanical parameters, "
     "etc.); 4) Clear product photos (overall and key components).\u201d", False, True),
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
p("Nine items per the original checklist (1\u20139, with Item 6 comprising sub-items a\u2013i). This revision "
  "addresses Items 1\u20134; Items 5\u20139 will follow.")

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
note_box(
    "Not yet prepared in this revision. The classification scheme (gas group, temperature class, installation "
    "zone) will be finalized based on further technical assessment and confirmed together with the "
    "certification body (ExCB / notified body).",
    shade=INFO_SHADE,
)

doc.add_heading("2.6 \u00b7 Design and Manufacturing Information (Items a\u2013i: Technical Drawings, Bill of "
                 "Materials, Material Datasheets, Manufacturing Process, Calculations, Draft Manual, "
                 "Nameplate, Ex Component Certificates)", level=2)
note_box(
    "Not yet prepared in this revision. To be completed in a subsequent revision, covering technical "
    "drawings, the bill of materials, material datasheets, a manufacturing process description, "
    "explosion-protection calculations, a draft operating/installation manual, nameplate information, and "
    "Ex component certificates.",
    shade=INFO_SHADE,
)

# ============================================================
# SECTION 3
# ============================================================
doc.add_heading("3. Sample Information", level=1)
p("Model, serial number, and sample status (whether the unit can be powered on and operated), together with "
  "any required test fixtures or auxiliary equipment.")
note_box("Not yet prepared in this revision.", shade=INFO_SHADE)

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
