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

# =================================================================== 6(a).7
h1("6(a).7 Main PCB schematic")
p("The electrical schematic of the GLD main board is provided as the actual circuit schematic (not a block "
  "diagram). It is presented as 26 figures, each cut from the original EasyEDA schematic around one functional "
  "block. Every component in a figure is enclosed in a numbered boundary box, and the same number is used in the "
  "description table printed with that figure. Each figure carries a sheet information table with the "
  "drawing/document number, revision, date, title and sheet number (n of 26).")

h2("Sheet register")
SHEETS = [
    ("01", "24 VDC input, input protection and 24 V to 5 V buck (U36)", "24 VDC input; input protection"),
    ("02", "Power connector J1, battery input and external 5 V", "24 VDC input"),
    ("03", "Battery load switch (U14)", "Input protection"),
    ("04", "5 V power-path mux (U13)", "5 V rail"),
    ("05", "Battery boost to about 24 V (U1, TPS61175)", "5 V rail / +24 V backup"),
    ("06", "Battery boost to 5 V (U41, TPS61088)", "5 V rail"),
    ("07", "5 V to 3.3 V buck (U43)", "3.3 V rail"),
    ("08", "Always-on 3.3 V LDO and its source selection (U42)", "3.3 V rail"),
    ("09", "TPL5010 timer/watchdog (U46)", "3.3 V rail"),
    ("10", "ENA latch (U51) and open-drain inverter (U15)", "3.3 V rail"),
    ("11", "3V3AON voltage supervisor (U16)", "3.3 V rail"),
    ("12", "Sensor module connector H2 (one connector as example)", "MQ heater supply"),
    ("13", "Sensor module connectors H1–H8", "MQ heater supply; sensor interface"),
    ("14", "Sensor module enable I/O expander (U12)", "MQ heater supply (module enable)"),
    ("15", "VMID bias of about 2.5 V (U3)", "MQ sensor analog circuitry"),
    ("16", "Analog +5VA supply filter (L6)", "MQ sensor analog circuitry"),
    ("17", "Sensor module I2C multiplexer (U33)", "MQ sensor analog circuitry"),
    ("18", "Temperature and humidity sensor (U44, SHT40)", "Analog circuitry (environment)"),
    ("19", "ADS1256 ADC with input filters (AIN), clock and decoupling", "ADC; analog circuitry"),
    ("20", "2.5 V voltage reference and VREF buffer", "ADC"),
    ("21", "ESP32-S3-WROOM-1U-N16R8 with support parts (incl. status LED)", "ESP32-S3; LED"),
    ("22", "USB, CH340C and auto-reset", "ESP32-S3 (programming)"),
    ("23", "E22-900MM22S LoRa module and antenna connector", "LoRa"),
    ("24", "5 V fan driver (Q5, J3)", "Fan driver"),
    ("25", "24 V alarm output driver (Q4, J2)", "LED / buzzer (alarm) driver"),
    ("26", "RS-485 transceiver (U47)", "RS-485 / Modbus"),
]
table(["Drawing no.", "Title", "Requirement covered"],
      [(f"PGLD-GLD-V4-MB-SCH-{n}", t, rq) for n, t, rq in SHEETS],
      widths=(1.75, 3.1, 1.75))
p("All sheets: revision 1.0, date 2026-07-19.", size=9, italic=True, color=GRAY)

h2("Coverage of the required schematic content")
table(
    ["Required content (6(a).7)", "Where shown", "Status"],
    [
        ["24 VDC input", "Sheets 01, 02", "Provided"],
        ["Input protection", "Sheets 01–03; protection-device table below", "Provided — see findings 1–2"],
        ["5 V rail", "Sheets 01 (buck U36), 04–06", "Provided"],
        ["3.3 V rail", "Sheets 07–11", "Provided"],
        ["MQ heater supply", "Sheets 12–14 (+5 V and enable to each sensor module)",
         "Partly — heater switch is on the sensor module (finding 4)"],
        ["MQ sensor bridge / analog circuitry", "Sheets 15–18; AIN filters on sheet 19",
         "Partly — load resistor is on the sensor module (finding 4)"],
        ["ADC", "Sheets 19, 20", "Provided"],
        ["ESP32-S3", "Sheets 21, 22", "Provided"],
        ["LoRa", "Sheet 23", "Provided"],
        ["Fan driver", "Sheet 24", "Provided"],
        ["LED / buzzer driver", "Sheet 25 (24 V alarm output J2); status LED on sheet 21", "Provided"],
        ["RS-485 / Modbus", "Sheet 26", "Provided"],
        ["Protection devices", "Table below", "Provided"],
        ["Grounding", "Text below", "Provided — PE point not drawn (finding 5)"],
        ["Title block per sheet", "Sheet information table on every figure", "Provided"],
    ],
    widths=(2.0, 2.9, 1.7),
)

h2("Protection devices")
table(
    ["Designator", "Part", "Location", "Function", "Sheet"],
    [
        ["F1", "MINISMDC260F/16-2", "Series with 24V+ after J1", "Overcurrent on 24 V line (PTC)", "01"],
        ["D1", "SMBJ33A", "After F1, to 24V−", "Surge / transient clamp on 24 V line (TVS)", "01"],
        ["L1", "ACM7060-301-2PL", "Series with 24V+ and return", "Common-mode noise", "01"],
        ["L4", "MPZ2012S101AT000", "Series with +24V", "High-frequency noise (ferrite)", "01"],
        ["D2 / R26", "LBZT52C12T1G / 100k", "Gate of Q3", "12 V gate-source limit for Q3", "01"],
        ["Q3", "SI7465DP-T1-GE3", "+24V to buck input", "High-side switch", "01"],
        ["F2", "MINISMDC260F/16-2", "Series with battery input J1.2", "Battery overcurrent (PTC)", "02"],
        ["Q2 / R1", "AO4407 / 100k", "Battery to VBAT_IN", "High-side switch", "02"],
        ["D7 / D13", "SS54", "5VEXT to +5V; boost to +24V", "Reverse-current blocking (OR-ing)", "02, 05"],
        ["D3 / D10", "BAT54C", "Source of U42 (3V3AON)", "OR-ing of supply sources", "08"],
        ["D8 / D9", "SS14", "Loads J2 and J3", "Flyback for inductive loads", "24, 25"],
        ["D4 / D5 / D11", "LESD5D5.0CT1G", "USB D−, D+, VBUS", "USB ESD", "22"],
        ["D6", "SM712", "RS-485 A/B", "RS-485 line TVS", "26"],
        ["L6", "GZ1005D600TF", "+5V to +5VA", "Analog supply noise isolation", "16"],
    ],
    widths=(0.85, 1.4, 1.65, 2.15, 0.55),
)

h2("Grounding")
for t in [
    "The circuit uses a single GND net; there is no separate AGND or chassis-ground net. The AGND/PGND/DGND pins "
    "of all ICs are connected to GND.",
    "The 24 V return (J1 pin 5, 24V−) enters GND through one winding of common-mode choke L1 (pin 2 to pin 3). "
    "J1 pins 1 and 3 are connected directly to GND.",
    "The analog supply +5VA is separated from +5V by ferrite bead L6; analog and digital ground are joined at GND.",
    "The shell/EP pads of USB1 and the GND pads of the LoRa module/antenna connector are connected to GND.",
    "A connection point from circuit GND to the enclosure / protective earth is not drawn on the schematic; it is "
    "defined by the enclosure grounding drawing (6(a).10).",
]:
    bullet(t)

h2("Findings to be resolved before the dossier is finalised")
table(
    ["#", "Finding (from the schematic)", "Action"],
    [
        ["1", "F1 and F2 are MINISMDC260F/16-2; the \"/16\" suffix normally means a 16 V rating, while F1 is on "
              "the 24 V line.", "Confirm the PTC voltage rating from the datasheet or change the part."],
        ["2", "Q3 (24 V) and Q2 (battery) have the source on the input side and the gate pulled to GND; with this "
              "orientation the body diode does not block reverse polarity.",
         "Confirm the intended function. The dossier text \"P-channel MOSFET reverse-polarity protection\" (§3.6) "
         "must match the actual circuit."],
        ["3", "Battery input, battery boost to 24 V (TPS61175) and to 5 V (TPS61088), battery load switch and "
              "power-path mux are populated on the main board.",
         "Decide whether the battery path is excluded (depopulated / not fitted) or included in the certified "
         "configuration; the production configuration is stated as 24 VDC only."],
        ["4", "Each sensor connector H1–H8 carries only +5 V, VMID, enable, I2C and AIN. The per-channel heater "
              "switch and the sensor load resistor are not on the main board.",
         "Provide the sensor-module schematic and layout as a separate drawing set."],
        ["5", "Single GND net; no chassis/PE connection point on the board.",
         "Show the GND-to-enclosure/PE arrangement in the grounding drawing (6(a).10)."],
        ["6", "RS-485 has TVS D6 only; no 120 Ω termination or A/B bias resistors.",
         "Confirm termination/bias is provided externally (installation note) or is not required."],
        ["7", "Converter output voltages (≈5.0 V, ≈24 V, ≈5.3 V) are calculated from feedback resistors, not "
              "measured.", "Record measured rail voltages in the routine/functional test."],
        ["8", "The load type on alarm output J2 (24 V siren/beacon) is not defined on the schematic.",
         "Identify the alarm module (manufacturer/model, current) in the BOM (6.b)."],
    ],
    widths=(0.3, 3.3, 3.0),
    bold_first=True,
)

# ---- schematic figures
doc.add_page_break()
h2("Schematic figures (sheets 01–26)")
p("The pages below reproduce the schematic figures exactly as issued, including the per-figure sheet "
  "information table and component description table.", size=9, color=GRAY)
for i, path in enumerate(sorted(glob.glob(os.path.join(SCH, "sheet-*.png")))):
    if i:
        doc.add_page_break()
    picture(path, CONTENT_W, max_h_in=9.0)

# =================================================================== 6(a).8
doc.add_page_break()
h1("6(a).8 PCB layout")
p("The layout of the GLD main board is presented in ten views generated from the EasyEDA PCB file of the same "
  "project. Each view highlights one aspect required by item 6(a).8; numbered markers on the view correspond to "
  "the legend printed below it.")

h2("Board data")
table(
    ["Parameter", "Value", "Source / status"],
    [
        ["Board name", "Main Board GLD (MotherBoardGLDVer2)", "Layout file"],
        ["Board outline", "Circular, Ø 84.0 mm", "Dimension in view 04"],
        ["Copper layers", "Top and bottom (two views of copper)", "Views 01, 02"],
        ["Component side", "All SMD parts on top; only through-hole connectors pass to the bottom", "View 02"],
        ["Enclosure fixing holes", "4 × Ø 3.2 mm on Ø 64 mm pitch circle, at (0, +32), (+32, 0), (0, −32), "
                                   "(−32, 0) mm from centre", "View 05"],
        ["Additional holes", "4 × Ø 3.0 mm near the board edge (≈ ±39 mm from centre)",
         "View 05 — purpose (casing screw or standoff) to be confirmed against the mechanical drawing"],
        ["Ground", "GND pour on top and bottom; 176 of 400 vias stitch the GND pours", "Views 09, 10"],
        ["Laminate, thickness, copper weight", "Not stated in the layout package",
         "To be provided (FR-4 grade, UL 94 rating, Tg, CTI) — see 6.b / 6.c"],
        ["Layout revision / date", "Not stated in the layout package", "To be added to the drawing table"],
    ],
    widths=(1.6, 2.9, 2.1),
)

h2("Drawing register")
VIEWS = [
    ("01", "Top layer", "Top layer"),
    ("02", "Bottom layer", "Bottom layer"),
    ("03", "Component placement", "Component placement"),
    ("04", "Board dimensions", "Board dimensions"),
    ("05", "Mounting holes", "Mounting holes"),
    ("06", "Connectors", "Connectors"),
    ("07", "High-current / power area", "High-current / power area"),
    ("08", "Sensor interface", "Sensor interface"),
    ("09", "Grounding arrangement — top", "Grounding arrangement"),
    ("10", "Grounding arrangement — bottom", "Grounding arrangement"),
]
table(["Drawing no.", "Title", "Requirement covered", "Rev / date"],
      [(f"PGLD-GLD-V4-MB-PCB-{n}", t, rq, "TBC") for n, t, rq in VIEWS],
      widths=(1.75, 2.0, 1.95, 0.9))

h2("Coverage of the required layout content")
table(
    ["Required content (6(a).8)", "Where shown", "Status"],
    [
        ["Top layer", "View 01", "Provided"],
        ["Bottom layer", "View 02", "Provided"],
        ["Component placement", "View 03", "Provided"],
        ["Board dimensions", "View 04", "Provided"],
        ["Mounting holes", "View 05", "Provided — purpose of 4 × Ø 3.0 mm holes to confirm"],
        ["Connectors", "View 06", "Provided"],
        ["High-current / power area", "View 07", "Provided"],
        ["Sensor interface", "View 08", "Provided"],
        ["Grounding arrangement", "Views 09, 10", "Provided"],
        ["One set per board (Main, Sensor, Alarm, Terminal)", "Main board only",
         "Open — sensor-module board layout to be added"],
    ],
    widths=(2.3, 1.6, 2.7),
)

LEGENDS = {
    "01": ("Top layer — Main Board GLD", [
        ("1", "ESP32-S3", "Main MCU module: runs the GLD firmware; SPI to LoRa and ADC, I²C to sensors, GPIO for alarm/fan."),
        ("2", "LoRa E22-900MM22S", "LoRa radio for communication with the cluster head."),
        ("3", "U.FL antenna connector", "Connection to the external LoRa antenna."),
        ("4", "Sensor ports (8)", "Eight 2 × 4 headers around the board, one per sensor module (yellow circle = module outline)."),
        ("5", "ADS1256", "24-bit ADC reading the eight analog sensor channels."),
        ("6", "TCA9548A", "8-channel I²C multiplexer, one channel per sensor port."),
        ("7", "PCF8574", "I/O expander providing the enable signals EN0–EN7 for each sensor."),
        ("8", "Micro-USB", "USB port for firmware flashing and serial debug."),
        ("9", "CH340C", "USB-to-UART converter for programming and serial monitor."),
        ("10", "ALARM connector", "24 V siren/beacon output."),
        ("11", "FAN connector", "5 V fan output."),
        ("12", "RS-485 connector", "RS-485 bus (A/B)."),
        ("13", "VIN connector", "Power input: 24V+, 24V−, 5VEXT, GND, BAT (battery)."),
        ("14", "PTC fuse", "Limits current on the 24 V line under short circuit."),
        ("15", "TVS", "Clamps voltage surges on the 24 V input."),
        ("16", "Common-mode filter", "Filters common-mode noise on the 24 V input."),
        ("17", "Buck 24 V → 5 V", "LMR51450 regulator stepping 24 V down to 5 V."),
        ("18", "Battery boost → 24 V", "TPS61175 boosting the battery to the +24V rail."),
        ("19", "Battery boost → 5 V", "TPS61088 generating 5 V from the battery."),
    ]),
    "02": ("Bottom layer — Main Board GLD", [
        ("1", "Bottom GND pour (solid blue area)", "GND plane filling almost the whole bottom side; connected to the top pour through vias."),
        ("2", "Through-hole connectors", "The only parts passing through to the bottom; all SMD parts are on the top side."),
    ]),
    "03": ("Component placement — Main Board GLD", [
        ("1", "ESP32-S3", "Main MCU: runs the firmware and controls all blocks."),
        ("2", "LoRa (E22-900MM22S)", "LoRa radio for communication with the cluster head."),
        ("3", "Antenna (U.FL)", "External LoRa antenna connector."),
        ("4", "ADS1256", "24-bit ADC for the eight analog sensor channels."),
        ("5", "TCA9548", "8-channel I²C mux, one channel per sensor port."),
        ("6", "PCF8574", "I/O expander for the enable signals EN0–EN7."),
        ("7", "USB", "Micro-USB + CH340C for firmware flashing and serial monitor."),
        ("8", "RS-485", "THVD1410 transceiver for the RS-485 bus."),
        ("9", "Alarm driver", "MOSFET switching the 24 V siren/beacon."),
        ("10", "Fan driver", "MOSFET switching the 5 V fan."),
        ("11", "SHT40", "Temperature and humidity sensor inside the enclosure."),
        ("12", "Power block", "Power input and protection (VIN connector, fuse, TVS, filter)."),
        ("13", "TPL5010", "Watchdog timer that wakes the system periodically."),
    ]),
    "04": ("Board dimensions — Main Board GLD", [
        ("1", "Board diameter: 84 mm", "Circular board (outline) matching the round aluminium enclosure."),
        ("2", "Enclosure-hole pitch circle: Ø 64 mm", "The four enclosure fixing holes lie on this circle, 90° apart."),
    ]),
    "05": ("Mounting holes — Main Board GLD", [
        ("1", "Enclosure holes (4 × Ø 3.2 mm)", "Hole pattern of the enclosure footprint on the Ø 64 mm circle; board-to-enclosure fixing screws. "
                                               "Positions from centre: (0, +32), (+32, 0), (0, −32), (−32, 0) mm."),
        ("2", "Additional holes (4 × Ø 3.0 mm)", "Four further fixing holes near the board edge (≈ ±39 mm from centre). "
                                                "Exact use (enclosure screw or standoff) to be confirmed with the mechanical drawing."),
    ]),
    "06": ("Connectors — Main Board GLD", [
        ("1", "VIN", "Power input, 2 × 3 pins: 24V+, 24V−, 5VEXT, GND, BAT (battery)."),
        ("2", "ALARM", "24 V siren/beacon output (pin 1 = +24V, pin 2 = MOSFET switch side)."),
        ("3", "FAN", "5 V fan output (pin 1 = +5V, pin 2 = MOSFET switch side)."),
        ("4", "RS-485", "RS-485 bus: B (pin 1) and A (pin 2)."),
        ("5", "Micro-USB", "Firmware flashing and serial debug."),
        ("6", "U.FL (antenna)", "External LoRa antenna connector."),
        ("7", "Sensor ports (8)", "Eight 2 × 4 headers (1.27 mm pitch): GND, +5V, AINx, SCLx, SDAx, ENx, VMID — one sensor module each."),
    ]),
    "07": ("High-current / power area — Main Board GLD", [
        ("1", "Power input & protection", "VIN connector, fuse, TVS, common-mode filter, ferrite: 24 V entry path."),
        ("2", "24 V → 5 V converter", "LMR51450 buck, 4.7 µH inductor, P-MOSFET switch."),
        ("3", "Battery → 24 V converter", "TPS61175 boost, 10 µH inductor, SK36 diode and OR-ing diode to the +24V rail."),
        ("4", "Battery → 5 V converter + power mux", "TPS61088 boost, 2.2 µH inductor, TPS2116 power mux selecting the 5 V source."),
        ("5", "Battery protection", "Fuse, P-MOSFET, load switch: disconnects the battery when the system sleeps."),
    ]),
    "08": ("Sensor interface — Main Board GLD", [
        ("1", "Sensor ports (8)", "Eight headers: +5V, GND, VMID, ENx, SDAx/SCLx (I²C per channel), AINx (analog to ADC)."),
        ("2", "TCA9548A", "I²C mux splitting the ESP32 I²C bus into 8 channels for 8 sensors."),
        ("3", "PCF8574", "I/O expander generating EN0–EN7 to switch each sensor module."),
        ("4", "ADS1256 + 8 MHz crystal", "8-channel 24-bit ADC, SPI to ESP32, clocked from an 8 MHz crystal."),
        ("5", "2.5 V reference + buffer", "ADR03 generates VREF, buffered by OPA320 for the ADC."),
        ("6", "VMID buffer", "OPA320 follower generating VMID (analog mid-bias) for the sensor modules."),
    ]),
    "09": ("Grounding arrangement (top) — Main Board GLD", [
        ("1", "GND pour", "One GND copper area (green line along the board edge) on top and bottom, filling all free area: "
                          "short return paths and noise shielding."),
        ("2", "GND vias (examples)", "176 of the 400 vias connect the top and bottom GND pours; blue circles mark examples."),
        ("3", "24V− → GND at the common-mode filter", "The 24 V input return (24V−) joins system GND through the return "
                                                      "winding of the common-mode choke."),
        ("4", "Analog area without split ground", "Single GND net. The analog area (ADS1256, voltage reference, OPA320) is "
                                                  "separated through the +5VA supply (ferrite), not by a split ground."),
    ]),
    "10": ("Grounding arrangement (bottom) — Main Board GLD", [
        ("1", "GND pour", "Bottom GND copper area filling all free area."),
        ("2", "GND vias (examples)", "176 of 400 vias stitch the top and bottom GND pours; blue circles mark examples."),
    ]),
}

for n, title, _ in VIEWS:
    doc.add_page_break()
    cap, items = LEGENDS[n]
    picture(os.path.join(PCB, f"view{n}.jpg"), 4.9, max_h_in=3.6 if len(items) > 12 else 5.2)
    caption(f"Figure 8-{int(n)}. {cap}")
    table(["Drawing no.", "Rev", "Date", "Title", "Sheet"],
          [(f"PGLD-GLD-V4-MB-PCB-{n}", "TBC", "TBC", title, f"{int(n)} of 10")],
          widths=(1.8, 0.5, 0.8, 2.6, 0.9), bold_first=False)
    table(["No", "Item", "Description"], items, widths=(0.4, 1.8, 4.4))

doc.add_paragraph()
note_box("Open items for 6(a).8: (a) layout revision and date for the drawing table; (b) PCB laminate grade, "
         "UL 94 rating, Tg, CTI, board thickness and copper weight; (c) purpose of the 4 × Ø 3.0 mm holes; "
         "(d) layout drawings of the sensor-module board.", fill=WARN_SHADE)

doc.save(OUT)
print("written", OUT)
