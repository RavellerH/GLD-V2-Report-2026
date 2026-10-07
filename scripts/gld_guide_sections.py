# -*- coding: utf-8 -*-
"""Shared content: detailed sections required by the reviewer's ATEX/IECEx revision guide.

Adds, for each checklist item, the tables and sub-sections the revision guide asks for, filled with the
data that actually exists for the GLD and marked Open / To be confirmed (TBC) / Pending certificate /
Decision required where it does not. Nothing is estimated or invented.

Used by scripts/build_cert_doc_docx.py and scripts/build_iecex_input_form_filled_docx.py.

Functions (each appends to the host document):
  photos(doc, h)        -> 2.4  photo-set coverage (guide item 4/5)
  bom(doc, h)           -> 2.6.b  Ex-critical mechanical (EX-01..17) and electrical (EL-01..13) BOM
  materials(doc, h)     -> 2.6.c  MAT-01..MAT-11
  manufacturing(doc, h) -> 2.6.d  d.1..d.13
  ex_calc(doc, h)       -> 2.6.e  e.1, e.2 (IS-01..17), e.3.1..e.3.11
  temperature(doc, h)   -> 2.6.f  f.1..f.12
  usage(doc, h)         -> 2.6.g  g.2..g.20 (+ maintenance schedule)
  nameplate(doc, h)     -> 2.6.h  proposed marking content (gas only)
  ex_certs(doc, h)      -> 2.6.i  components requiring Ex certificates
  sample(doc, h)        -> 3      sample register and fixtures
  matrix(doc, h)        -> compliance matrix against the revision guide
h is a callable(text) producing a sub-heading in the host document.
"""
import json
import os

from docx.shared import Pt, Inches, RGBColor
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
USAGE_JSON = os.path.join(REPO, "scripts", "assets", "usage_instructions_g2_g20.json")

NAVY = RGBColor(0x1B, 0x33, 0x5F)
INK = RGBColor(0x26, 0x23, 0x21)
GRAY = RGBColor(0x55, 0x5B, 0x66)
HEAD_SHADE = "EAEFF9"
NOTE_SHADE = "F3F6FC"
WARN_SHADE = "FBEEE4"
STATUS_SHADE = {"Final": "E3F1E6", "Available": "E3F1E6", "Provided": "E3F1E6", "Measured": "E3F1E6",
                "Partial": "FFF4D6", "Review": "FFF4D6", "Draft": "FFF4D6", "Preliminary": "FFF4D6",
                "Open": "FBEEE4", "TBC": "FBEEE4", "Pending certificate": "FBEEE4",
                "Decision required": "F8DADA", "Not measured": "FBEEE4", "Not tested": "FBEEE4",
                "N.A.": "EEEEEE", "Applicable": "FFF4D6"}

_doc = None


def _shade(cell, hex_color):
    el = OxmlElement("w:shd")
    el.set(qn("w:val"), "clear")
    el.set(qn("w:fill"), hex_color)
    cell._tc.get_or_add_tcPr().append(el)


def _p(text, size=10, bold=False, italic=False, color=None, space_after=5, style=None):
    para = _doc.add_paragraph(style=style) if style else _doc.add_paragraph()
    para.paragraph_format.space_after = Pt(space_after)
    r = para.add_run(text)
    r.font.size = Pt(size)
    r.font.bold = bold
    r.font.italic = italic
    r.font.color.rgb = color or INK
    return para


def _sub(text):
    para = _p(text, size=10.5, bold=True, color=NAVY, space_after=3)
    para.paragraph_format.keep_with_next = True
    return para


def _bullet(text):
    return _p(text, size=9.5, space_after=1, style="List Bullet")


def _note(text, fill=NOTE_SHADE):
    tbl = _doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.rows[0].cells[0]
    _shade(cell, fill)
    cell.paragraphs[0].paragraph_format.space_after = Pt(2)
    r = cell.paragraphs[0].add_run(text)
    r.font.size = Pt(9)
    r.font.color.rgb = GRAY
    _doc.add_paragraph().paragraph_format.space_after = Pt(2)


def _table(headers, rows, widths, status_col=None, size=8):
    tbl = _doc.add_table(rows=1, cols=len(headers))
    tbl.style = "Table Grid"
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr = tbl.rows[0]
    th = OxmlElement("w:tblHeader")
    th.set(qn("w:val"), "true")
    hdr._tr.get_or_add_trPr().append(th)
    for i, txt in enumerate(headers):
        _shade(hdr.cells[i], HEAD_SHADE)
        hdr.cells[i].paragraphs[0].paragraph_format.space_after = Pt(1)
        r = hdr.cells[i].paragraphs[0].add_run(txt)
        r.font.bold = True
        r.font.size = Pt(size)
        r.font.color.rgb = NAVY
    for vals in rows:
        row = tbl.add_row()
        row._tr.get_or_add_trPr().append(OxmlElement("w:cantSplit"))
        for i, v in enumerate(vals):
            cell = row.cells[i]
            para = cell.paragraphs[0]
            para.paragraph_format.space_after = Pt(1)
            r = para.add_run(v)
            r.font.size = Pt(size)
            if i == 0:
                r.font.bold = True
            if status_col is not None and i == status_col:
                r.font.bold = True
                for key, col in STATUS_SHADE.items():
                    if v.startswith(key):
                        _shade(cell, col)
                        break
    tbl.autofit = False
    lay = OxmlElement("w:tblLayout")
    lay.set(qn("w:type"), "fixed")
    tbl._tbl.tblPr.append(lay)
    grid = tbl._tbl.find(qn("w:tblGrid"))
    for i, gc in enumerate(grid.findall(qn("w:gridCol"))):
        gc.set(qn("w:w"), str(int(widths[i] * 1440)))
    for row in tbl.rows:
        for i, w in enumerate(widths):
            row.cells[i].width = Inches(w)
    _doc.add_paragraph().paragraph_format.space_after = Pt(2)


def _begin(d, h, title):
    global _doc
    _doc = d
    if h:
        h(title)
    else:
        _sub(title)


STATUS_LEGEND = ("Status legend: Final = confirmed and documented; Review = data exists but a rating or function "
                 "must be checked; Open = data not yet available; TBC = to be confirmed; Pending certificate = "
                 "certificate to be obtained; Decision required = design decision needed; N.A. = not applicable.")


# ===================================================================================== 2.4 photographs
def photos(d, h=None):
    _begin(d, h, "2.4.1 Photo-set coverage against the revision guide")
    _p("The revision guide asks for a photo set covering twelve views. The table maps each requested view to the "
       "figures already included in this document and lists the views still to be photographed on the current "
       "production configuration (latest enclosure and PCB). Captions follow the format “Figure 4-n. GLD V2 – "
       "<title>” with a one-sentence description; no Ex marking is shown as final and the MQ sensor mesh is not "
       "described as flame-arresting.", size=9.5)
    rows = [
        ("1", "Overall external view — front, rear, left, right, top, bottom", "Available",
         "Current production unit: Figures 4-118 (front), 4-119…4-122 (sides), 4-123 (rear), 4-116 (closed, top); "
         "CAD views M-A2 and M-B1…M-B4."),
        ("2", "Product identification / nameplate area", "Open",
         "To be photographed once the nameplate position is fixed; caption to state that the marking is draft."),
        ("3", "Front sensing area (mesh, cover, fan behind it)", "Available",
         "Figure 4-115 (fan behind the mesh in the cover), 4-118 (mesh face); M-D4."),
        ("4", "Internal sensing section (8 MQ sensors, fan, chamber)", "Available",
         "Figures 4-107, 4-109…4-115 (sensor modules fitted, fan and cover); M-D6."),
        ("5", "MQ sensor close-up (integrated protective mesh)", "Available", "Figure 4-105 (sensor module); M-D1."),
        ("6", "Main PCB — component side and underside", "Partial",
         "Figures 4-102, 4-103 (component side in the enclosure); PCB layout views 2.6.a.8. Underside photograph "
         "to be added."),
        ("7", "Power input and terminal area", "Available",
         "Figures 4-104 (labelled terminal board), 4-112…4-114 (gland, cable, 24V termination)."),
        ("8", "Grounding / bonding point", "Partial",
         "Figures 4-116, 4-120 (external grounding screw); close-up with lug and conductor to be added."),
        ("9", "Cable entry and antenna interface (all penetrations)", "Partial",
         "Figures 4-112 (cable gland), 4-110 (beacon entry), 4-119 (blanking plug), 4-101 (antenna); close-up of the "
         "antenna bulkhead to be added."),
        ("10", "Alarm module (LED/buzzer, gasket, fixing)", "Available", "Figures 4-110, 4-111; M-D5, M-E4."),
        ("11", "Enclosure opened — complete internal arrangement", "Available",
         "Figure 4-115 (open base with sensors and terminals next to the cover with fan)."),
        ("12", "Exploded / assembly sequence photographs", "Available",
         "Figures 4-101…4-117 (complete assembly sequence); exploded illustrations M-D8, M-D9, M-E1."),
    ]
    _table(["#", "Requested view", "Status", "Where shown / action"], rows, widths=(0.3, 2.2, 0.9, 3.2),
           status_col=2)


# ===================================================================================== 2.6.b BOM
def bom(d, h=None):
    _begin(d, h, "2.6.b.1 Ex-critical mechanical / construction components")
    _p("Components whose substitution could affect the explosion-protection concept, in the format requested by "
       "the revision guide. The electronic BOM above remains the full component list; this table is the Ex-critical "
       "subset and is controlled by part number or drawing number.", size=9.5)
    ex = [
        ("EX-01", "Main enclosure body", "PT Galaksi Megatama Indonesia", "GLD ATEX CASE v3 / common base (M-B7, M-D7)",
         "ADC12 die-cast aluminium alloy; wall thickness TBC; surface treatment TBC", "Flameproof enclosure (Ex d, proposed)",
         "Drawings M-B7, M-D7", "Open"),
        ("EX-02", "Enclosure cover (threaded)", "PT Galaksi Megatama Indonesia", "TBC",
         "Aluminium alloy; thread form, pitch and engagement TBC", "Flameproof joint", "Assembly M-E9 (closed by turning clockwise)",
         "Open"),
        ("EX-03", "Front stainless-steel wire-mesh plate + locking bracket", "TBC", "TBC (M-D4, M-E1)",
         "Stainless steel; grade, mesh/pore size, thickness, layers TBC", "Gas inlet; flame-path element if certified",
         "Photograph, assembly illustration", "Open"),
        ("EX-04", "MQ sensor integrated protective mesh", "Sensor manufacturer TBC", "MQ-2, MQ-3B, MQ-4, MQ-5, MQ-6, MQ-7B, MQ-8, MQ-135",
         "Stainless-steel mesh (per sensor construction)", "Protective element; no flame-arresting claim",
         "Sensor data sheets (M-F1…M-F4)", "Open"),
        ("EX-05", "DC sampling fan", "CIXIKEJI", "CX5010B5H (DC brushless, 50 × 50 × 10 mm frame)",
         "DC 5 V, 0.23 A (≈1.2 W); CE/FCC/RoHS only — no Ex certification; max. temperature TBC",
         "Gas sampling; potential ignition source (IS-02)", "Label, Figure 4-108; driven by Q5 (sheet 24)",
         "Partial"),
        ("EX-06", "Gaskets / O-rings", "TBC", "TBC (M-D2, M-D3)", "Rubber; compound, hardness, temperature range TBC",
         "Environmental sealing (IP66)", "Photographs", "Open"),
        ("EX-07", "Cable gland (24 VDC entry)", "TBC", "TBC", "M20×1.5 entry thread (BP18-1Z reference); Ex d barrier "
         "gland required for IIC; cable range, IP, temperature TBC", "Cable-entry flame path and sealing",
         "Current prototype uses a general-purpose black polymer gland (Figure 4-112) — to be replaced by a certified "
         "metallic Ex d barrier gland", "Pending certificate"),
        ("EX-08", "Blanking plug / adaptor", "TBC", "TBC", "Metallic hexagon plug fitted in the lower entry; thread "
         "and certification TBC", "Closes unused entry", "Figure 4-119", "Pending certificate"),
        ("EX-09", "Antenna bulkhead / SMA interface", "TBC", "TBC", "SMA; material and sealing TBC",
         "Enclosure penetration", "—", "Open"),
        ("EX-10", "External antenna", "TBC", "TBC", "Omnidirectional, 3 dBi, SMA; material/environmental rating TBC",
         "RF radiator", "M-D1", "Open"),
        ("EX-11", "LED / buzzer alarm beacon", "TBC", "TBC", "Driven at 24 V from J2 (sheet 25); housing, gasket, "
         "current TBC", "Local alarm; separate penetration", "M-D5", "Open"),
        ("EX-12", "Grounding stud", "TBC", "TBC", "External stud with PE symbol; size and material TBC",
         "Protective earth / bonding", "M-D15; Figures 4-116, 4-120", "Open"),
        ("EX-13", "Mounting fasteners", "TBC", "U-bolt mounting plate (M-A1)", "U-bolt 2″/DN50, M10 thread; plate "
         "250 × 250 mm; fastener grade TBC", "Mechanical retention", "Drawing M-A1", "Partial"),
        ("EX-14", "Internal insulating parts (PCB cover / terminal module)", "TBC", "M-D10, M-D11",
         "Material, flammability, CTI TBC", "Insulation of terminals", "CAD render", "Open"),
        ("EX-15", "PCB substrate", "TBC (PCB fabricator)", "Main board Ø84 mm (2.6.a.8)",
         "Laminate grade, UL 94 rating, Tg, CTI, thickness TBC", "Carrier of energized circuits", "Layout views", "Open"),
        ("EX-16", "Potting / adhesive", "—", "—", "Not used in the current design (to be confirmed)", "—", "—", "TBC"),
        ("EX-17", "Battery and holder", "—", "Battery path on main board (sheets 02–06); BAT −/+ terminal on the "
         "terminal board (Figure 4-104); battery case in M-E3",
         "—", "Included only if retained in the certified configuration", "Schematic", "Decision required"),
    ]
    _table(["Ref.", "Component", "Manufacturer", "Part / drawing no.", "Material / rating", "Safety function",
            "Evidence", "Status"], ex, widths=(0.45, 1.0, 0.75, 0.85, 1.25, 0.85, 0.75, 0.6), status_col=7, size=7)

    _sub("2.6.b.2 Ex-critical electrical components")
    _p("Electrical components that affect input protection, fault energy, heater power, surface temperature, "
       "isolation, switching or ignition risk. Data from the released main-board schematic (2.6.a.7) and the "
       "electronic BOM.", size=9.5)
    el = [
        ("EL-01", "Resettable PTC fuse F1 (24 V) / F2 (battery)", "Littelfuse", "MINISMDC260F/16-2", "I-hold 2.6 A, "
         "I-trip 5.0 A, V-max 16 V", "Overcurrent protection", "Datasheet; sheets 01, 02",
         "Review — 16 V rating on a 24 V line"),
        ("EL-02", "TVS diode D1", "Ruilon", "SMBJ33A", "V-RWM 33 V, P-pk 600 W", "Input transient/overvoltage",
         "Datasheet; sheet 01", "Final"),
        ("EL-02a", "TVS D6 (RS-485), ESD D4/D5/D11 (USB)", "DOWO / UMW", "SM712 / LESD5D5.0CT1G", "Line clamps",
         "Interface protection", "Sheets 22, 26", "Final"),
        ("EL-03", "P-MOSFET Q3 + zener D2", "Vishay / LRC", "SI7465DP-T1-GE3 / LBZT52C12T1G", "V-DS, I-D per datasheet; "
         "V-GS limited to 12 V", "Input switch (reverse-polarity function TBC)", "Sheet 01",
         "Review — orientation"),
        ("EL-03a", "Common-mode choke L1, ferrite L4", "TDK", "ACM7060-301-2PL / MPZ2012S101AT000", "Per datasheet",
         "Input EMI filtering", "Sheet 01", "Final"),
        ("EL-04", "Buck converter U36 (24 V → 5 V)", "Texas Instruments", "LMR51450", "VIN ≤ 36 V; output ≈5.0 V "
         "(calculated)", "Power conversion; possible hot surface", "Sheet 01", "Final"),
        ("EL-04a", "Buck converter U43 (5 V → 3.3 V), LDO U42", "Texas Instruments", "TPS62162 / TPS7A0233",
         "3.3 V rails", "Logic supply", "Sheets 07, 08", "Final"),
        ("EL-05", "Boost converters U1 (batt → 24 V), U41 (batt → 5 V)", "Texas Instruments", "TPS61175 / TPS61088",
         "Battery path", "Power conversion; possible hot surface", "Sheets 05, 06", "Decision required — battery path"),
        ("EL-05a", "Battery load switch U14, power mux U13, P-MOSFET Q2", "TI / JSMSEMI", "TPS22964C / TPS2116 / AO4407",
         "Battery path", "Battery switching", "Sheets 02–04", "Decision required — battery path"),
        ("EL-06", "Power inductors", "ABC / SXN / APV", "GSSM06304R7M2AU 4.7 µH; SMDRH105R-2R2NT; ANR3015T2R2M; "
         "SMDRH105R-100MT", "I-sat, I-rms, ΔT TBC", "Possible hot surface", "Sheets 01, 05, 06, 07",
         "Open — ΔT not measured"),
        ("EL-07", "MQ heater supply", "—", "+5 V to sensor connectors H1–H8; enable via PCF8574 (U12)",
         "Heater voltage 5 V; per-channel switch on sensor module", "Heater power / surface temperature",
         "Sheets 12–14", "Open — sensor-module schematic"),
        ("EL-08", "Fan driver Q5 + flyback D9", "— / MDD", "AO3400A / SS14", "Low-side switch, 5 V", "Fan current",
         "Sheet 24", "Final"),
        ("EL-09", "Alarm driver Q4 + flyback D8", "— / MDD", "AO3400A / SS14", "Low-side switch, 24 V output J2",
         "Alarm load switching", "Sheet 25", "Final"),
        ("EL-10", "Main PCB", "PCB fabricator TBC", "MotherBoardGLDVer2", "Ø84 mm, two copper layers",
         "Carrier of energized circuits", "2.6.a.8", "Open — laminate data"),
        ("EL-11", "ESP32-S3 module", "Espressif", "ESP32-S3-WROOM-1U-N16R8", "3.3 V", "Main energized electronics",
         "Sheet 21", "Final"),
        ("EL-12", "LoRa module", "Ebyte", "E22-900MM22S", "0–22 dBm, 920–923 MHz", "RF source", "Sheet 23", "Final"),
        ("EL-13", "Terminals / connectors", "Boomele / TBC", "J1 power 2×3 (pin 6 = 24V+, pin 5 = 24V−); XH-2A; "
         "H1–H8 2×4 1.27 mm", "Current/voltage rating TBC", "Loose-contact heating / sparking", "Sheets 02, 13",
         "Open — VIN connector MPN"),
    ]
    _table(["Ref.", "Component", "Manufacturer", "Part no.", "Rating", "Safety function", "Evidence", "Status"],
           el, widths=(0.45, 1.05, 0.7, 1.05, 0.95, 0.85, 0.65, 0.8), status_col=7, size=7)
    _note(STATUS_LEGEND)


# ===================================================================================== 2.6.c materials
def materials(d, h=None):
    _begin(d, h, "2.6.c.1 Non-metallic materials register (MAT-01 … MAT-11)")
    _p("Format requested by the revision guide. Each material is to be supported by the supplier's datasheet or "
       "conformity declaration covering service-temperature range, heat/cold resistance, ageing, flame retardancy "
       "(UL 94 / glow-wire), CTI where relevant, electrostatic properties, chemical and UV/weather resistance, and "
       "Tg where relevant. Where the material is not yet identified the item stays Open.", size=9.5)
    rows = [
        ("MAT-01", "Cover-to-body gasket", "Rubber; compound TBC", "TBC", "Temp. range, ageing, chemical resistance",
         "Datasheet", "Open"),
        ("MAT-02", "Cable-gland body and sealing ring", "Current prototype: black polymer gland (Figure 4-112); "
         "final: per certified Ex d gland", "Gland supplier", "Temp., flame rating, UV/chemical, electrostatic",
         "Datasheet / certificate", "Open"),
        ("MAT-03", "Main PCB laminate", "FR-4 type expected; exact grade TBC", "PCB fabricator", "Tg, CTI, UL 94",
         "Material datasheet", "Open"),
        ("MAT-04", "Connector housings (J1, XH-2A, H1–H8)", "TBC", "Boomele / TBC", "CTI, UL 94, temp. rating",
         "Datasheet", "Open"),
        ("MAT-05", "Wire insulation (24 VDC cable, 2 conductors L+/L−, Ø≈0.75 mm)", "TBC", "TBC",
         "Temp. rating, flame rating", "Cable datasheet", "Open"),
        ("MAT-06", "Antenna housing / insulator", "TBC", "TBC", "Temp., UV, electrostatic properties", "Datasheet",
         "Open"),
        ("MAT-07", "Fan impeller / housing", "Plastic (grade TBC)", "CIXIKEJI (CX5010B5H)", "Temp., flame rating, "
         "mechanical", "Fan datasheet", "Open"),
        ("MAT-08", "Adhesive / sealant", "Not used (TBC)", "—", "Temp., chemical resistance, ageing", "Datasheet",
         "TBC"),
        ("MAT-09", "Enclosure powder coating", "Powder coating ≤0.2 mm (BP18-1Z reference)", "Casing supply chain",
         "Charge transfer <10 nC; surface capacitance <5 pF", "Supplier drawing", "Partial"),
        ("MAT-10", "Transparent window (GLD ATEX CASE v3)", "Glass; type TBC", "TBC", "Impact and thermal-shock "
         "tests for Ex d windows; temp. rating", "Drawing M-B7", "Open"),
        ("MAT-11", "Alarm beacon lens / dome", "TBC", "TBC", "UV, impact, electrostatic, flame rating", "Datasheet",
         "Open"),
    ]
    _table(["Ref.", "Component", "Material / grade", "Manufacturer", "Important properties", "Evidence", "Status"],
           rows, widths=(0.55, 1.4, 1.15, 0.85, 1.35, 0.8, 0.5), status_col=6, size=7.5)


# ===================================================================================== 2.6.d manufacturing
def manufacturing(d, h=None):
    _begin(d, h, "2.6.d.1 Manufacturing and assembly process control")
    _p("Manufacturing and assembly processes that may affect explosion protection are controlled through approved "
       "drawings, work instructions, inspection criteria and production records. The sub-sections below follow the "
       "structure of the revision guide; parameters that the enclosure manufacturer has not yet issued are marked "
       "TBC rather than assumed.", size=9.5)
    secs = [
        ("d.1 Enclosure manufacturing and machining control",
         "Body and cover are produced by die casting (ADC12) and machined to controlled drawings. Safety-critical "
         "dimensions — threaded joints, wall thickness, sealing surfaces and other flame-path features — are "
         "inspected against the specified tolerances before assembly. Inspection method, measuring equipment and "
         "acceptance criteria: TBC (enclosure manufacturer). For Ex d, gap, joint length and thread engagement are "
         "the controlled characteristics."),
        ("d.2 Enclosure surface treatment",
         "Powder coating is shown on the BP18-1Z reference (≤0.2 mm, charge transfer <10 nC, surface capacitance "
         "<5 pF). Coating of flame-path surfaces is not permitted unless approved. Final treatment for the GLD "
         "enclosure: TBC."),
        ("d.3 Front stainless-steel mesh assembly",
         "The mesh plate is fitted with its locking bracket in the specified orientation (M-E1) and inspected for "
         "deformation, damage, contamination or incomplete seating before the cover is accepted. Mesh part number, "
         "fastening torque and any adhesive: TBC."),
        ("d.4 DC fan installation",
         "The DC fan is attached to the enclosure cover behind the stainless-steel mesh plate and its cable connected "
         "to J3 (M-E9). Airflow direction, screw type, torque, clearance to the mesh and connector locking are to be "
         "defined on the assembly drawing (TBC)."),
        ("d.5 MQ sensor array installation",
         "Eight MQ sensors (MQ-2, MQ-3B, MQ-4, MQ-5, MQ-6, MQ-7B, MQ-8, MQ-135) are mounted on the sensor modules "
         "at fixed positions H1–H8. Position/type correspondence is verified visually to prevent interchange; the "
         "integrated sensor mesh must be undamaged. Position map: TBC on a controlled drawing."),
        ("d.6 PCB assembly and inspection",
         "SMT assembly by the PCB assembler from the released design files (EasyEDA/JLCPCB), followed by visual "
         "inspection, polarity/orientation check, firmware programming and functional test. PCB revision is "
         "recorded for traceability. Assembler name/address and AOI use: TBC."),
        ("d.7 Cable entry and terminal assembly",
         "Only the approved gland/adaptor for the M20×1.5 entry is used; thread verification, sealing ring, cable "
         "size, tightening torque and treatment of unused entries (approved blanking plug) are checked. The 24 VDC "
         "supply is connected to J1 pins 6 (24V+) and 5 (24V−). Torque values: TBC."),
        ("d.8 Grounding and bonding assembly",
         "External grounding stud with washer–lug–nut sequence; continuity between stud and all conductive enclosure "
         "parts is tested before release. Stud size, torque and continuity acceptance limit: TBC."),
        ("d.9 Gasket and sealing installation",
         "Correct gasket part, orientation, clean and undamaged sealing surfaces, no twisting; replacement whenever "
         "damaged or after a defined number of openings (TBC)."),
        ("d.10 Final enclosure closure",
         "Clean mating/threaded surfaces, close the cover by turning clockwise to full engagement, apply the locking "
         "feature and inspect after closure. Minimum thread engagement and final torque: TBC."),
        ("d.11 Firmware and configuration control",
         "Each unit is programmed with the approved firmware version, AI model version (three classes: clean air, "
         "LPG, H2), configuration file, alarm thresholds and LoRa settings. Programming is verified and recorded "
         "against the serial number. Changes require controlled approval and a rollback path."),
        ("d.12 Final inspection and routine test",
         "Visual inspection; enclosure integrity; mesh condition; fan operation; 8/8 sensor detection; power "
         "consumption at 24 VDC (≤8 W); alarm test; LoRa communication; grounding continuity; IP/leak check if "
         "required as a routine test; serial number and documentation check. Ex d routine overpressure test, if "
         "required by the certificate: TBC."),
    ]
    for title, body in secs:
        _sub(title)
        _p(body, size=9.5)
    _sub("d.13 Applicability of special processes")
    _table(["Process", "Applicability"], [
        ("Die casting", "Applicable — enclosure in ADC12 die-cast aluminium"),
        ("Machining of flame-path surfaces", "Applicable for Ex d (final concept to be confirmed)"),
        ("Welding", "Not used in the current design (to be confirmed by the enclosure manufacturer)"),
        ("Potting", "Not used (to be confirmed)"),
        ("Bonding adhesive", "Not used unless specified for mesh or seal (TBC)"),
        ("Surface treatment (powder coating)", "Applicable — parameters per enclosure manufacturer (TBC)"),
    ], widths=(2.2, 4.4), size=8.5)


# ===================================================================================== 2.6.e explosion protection
def ex_calc(d, h=None):
    _begin(d, h, "2.6.e.1 Gas access path and internal arrangement")
    _p("Ambient gas enters through the stainless-steel mesh at the front of the enclosure. During the sampling cycle "
       "the internal DC fan draws gas through this mesh into the sensing chamber, where the eight MQ sensors are "
       "installed. Each MQ sensor has its own stainless-steel protective mesh around the sensing element, so the "
       "sampled gas passes two successive mesh structures before reaching the sensing element.", size=9.5)
    _sub("2.6.e.2 Identification and assessment of potential ignition sources")
    rows = [
        ("IS-01", "MQ sensor internal heater", "Hot surface", "Two meshes between atmosphere and element",
         "Measured sensor-body surface ≤78.4 °C (fan stalled, 24.8 °C ambient); confirm heater construction and any "
         "flame-arresting function from manufacturer data", "Open"),
        ("IS-02", "DC sampling fan", "Winding heating, commutation, stalled rotor", "Front mesh upstream of fan",
         "Fan CIXIKEJI CX5010B5H, 5 V 0.23 A; body measured 36.3 °C; confirm locked-rotor behaviour", "Open"),
        ("IS-03", "Main PCB", "Arc/spark, component failure, overheating", "Gas accessibility of PCB volume TBC",
         "Confirm whether the PCB volume is separated from the sensing chamber (see e.3.2)", "Open"),
        ("IS-04", "DC/DC converters", "Semiconductor / inductor heating, switching fault", "Depends on IS-03",
         "PTC, TVS and MOSFET input stage present; converter temperatures not yet measured", "Open"),
        ("IS-05", "24 VDC terminals and connectors", "Make/break spark, loose-contact heating", "Depends on IS-03",
         "Confirm terminal location, rating, torque, creepage/clearance", "Open"),
        ("IS-06", "LED / audible alarm module", "Switching, heating, fault", "Separate beacon housing",
         "Obtain module construction/certification data", "Open"),
        ("IS-07", "ESP32-S3 / LoRa / digital electronics", "Overheating, electrical fault", "Depends on IS-03",
         "Assess maximum component temperatures", "Open"),
        ("IS-08", "RF transmitter / antenna", "RF energy", "External antenna", "Max. 22 dBm into a 3 dBi antenna; assess "
         "against IEC 60079-0 RF threshold", "Open"),
        ("IS-09", "Power inductors", "Surface heating", "Depends on IS-03", "Measure worst-case ΔT", "Open"),
        ("IS-10", "MOSFETs, diodes, protection devices", "Local overheating on overload/surge", "Depends on IS-03",
         "Verify ratings and protective-device coordination (F1/F2 voltage rating)", "Open"),
        ("IS-11", "Electrostatic charging of non-metallic parts", "ESD", "Gasket, antenna insulation, gland parts",
         "Identify exposed non-metallic parts and dimensions (MAT register)", "Open"),
        ("IS-12", "Metallic enclosure and joints", "Spark from poor bonding/impact", "External atmosphere",
         "Verify bonding continuity and grounding", "Open"),
        ("IS-13", "Cable entry / gland / blanking devices", "Loss of protection", "External atmosphere",
         "Prototype gland is a general-purpose polymer type; finalize Ex d gland/plug list (EX-07, EX-08)", "Open"),
        ("IS-14", "Front stainless-steel mesh", "Flame transmission path", "Direct interface",
         "Confirm construction; certificate/test if claimed as flame-arresting", "Open"),
        ("IS-15", "MQ sensor protective mesh", "Flame transmission path", "Around each sensing element",
         "No flame-arresting claim without manufacturer documentation", "Open"),
        ("IS-16", "Mechanical impact / friction", "Mechanical spark", "Fan is the only moving part",
         "Confirm fan clearance and retention", "Open"),
        ("IS-17", "Battery circuit", "High fault current, cell heating", "Battery path populated on main board",
         "Decide exclusion/depopulation from the certified configuration", "Decision required"),
    ]
    _table(["Ref.", "Potential ignition source", "Mechanism", "Exposure / existing feature", "Assessment required",
            "Status"], rows, widths=(0.45, 1.15, 1.0, 1.25, 2.15, 0.6), status_col=5, size=7.5)
    _sub("2.6.e.3 Explosion-protection concept and protective construction")
    parts = [
        ("e.3.1 Overall concept", "Potential ignition sources are isolated from the external atmosphere, enclosed in a "
         "protective construction, or controlled so they cannot ignite it. The applicant proposes flameproof "
         "enclosure Ex d (marking proposal II 2G Ex db IIC T4 Gb), subject to ExCB confirmation."),
        ("e.3.2 Gas-accessible and protected volumes", "The front sensing chamber is intentionally gas-accessible. "
         "Whether the main PCB is separated from it by a partition (PCB plate) or shares the same volume is still to "
         "be confirmed on the section drawing; the assessment of IS-03…IS-10 depends on this."),
        ("e.3.3 Front stainless-steel mesh", "First protective element in the gas inlet; mechanical protection and, "
         "only where supported by certification, flame arresting."),
        ("e.3.4 MQ sensor protective construction", "Each sensor's integrated stainless-steel mesh surrounds the sensing "
         "and heating structure; no Ex claim without manufacturer documentation."),
        ("e.3.5 DC fan", "Located in the gas path behind the mesh; surface temperature, winding temperature, stalled "
         "rotor and commutation to be assessed."),
        ("e.3.6 Main electronics", "Main PCB, converters, processing and RF electronics and connectors are treated as "
         "potential ignition sources; protection depends on e.3.2."),
        ("e.3.7 Flame-transmission paths", "Front gas inlet, cover joint, threaded interfaces, cable entries, antenna "
         "interface, alarm-module connection and any other wall penetration are to be identified and controlled; "
         "gap/length/volume values to be supplied by the enclosure manufacturer."),
        ("e.3.8 Cable entries, antenna, alarm module", "All penetrations use components compatible with the final "
         "concept, gas group IIC, temperature range, IP66 and the M20×1.5 thread."),
        ("e.3.9 Grounding and electrostatic protection", "The metallic enclosure is bonded to protective earth through "
         "the external grounding stud; conductive parts keep electrical continuity."),
        ("e.3.10 Temperature protection", "Surface temperatures of sensors, fan, converters, enclosure and alarm module "
         "are evaluated at maximum load and fault conditions (2.6.f); T-class assigned only after testing."),
        ("e.3.11 Fault and abnormal conditions", "Fan stall (measured), blocked airflow, heater abnormality, converter "
         "failure, short circuit, loose terminal and maximum ambient are to be covered."),
    ]
    for t, b in parts:
        _sub(t)
        _p(b, size=9.5)


# ===================================================================================== 2.6.f temperature
def temperature(d, h=None):
    _begin(d, h, "2.6.f.1 Temperature-class evaluation structure (revision guide f.1–f.12)")
    _sub("f.1 Proposed temperature class")
    _p("T4 (≤135 °C; effective limit 130 °C with the 5 K margin). Final assignment only after the hot-spot "
       "measurements, extrapolation to maximum ambient and fault conditions are complete.", size=9.5)
    _sub("f.2 Maximum ambient temperature")
    _p("+60 °C, the rated maximum of the operating range −20 °C to +60 °C. Note: an assessment at +85 °C would "
       "raise the fan-stalled sensor-body value to about 139 °C, above the T4 limit; +85 °C is therefore not the "
       "rated ambient.", size=9.5)
    _sub("f.3 Candidate hottest points")
    _table(["Ref.", "Component / location", "Reason", "Measurement status"], [
        ("T-01", "MQ sensor heater / sensor head", "Heater active during operation", "Measured (TC-1)"),
        ("T-02", "DC fan motor/electronics", "Sampling and stalled condition", "Measured (TC-2)"),
        ("T-03", "5 V converter (U36 LMR51450)", "Supplies MQ heaters", "Not measured (TC-3 planned)"),
        ("T-04", "3.3 V regulator (U43/U42)", "MCU supply", "Not measured"),
        ("T-05", "Boost/buck converter ICs", "Switching losses", "Not measured (TC-3 planned)"),
        ("T-06", "Power inductors", "Copper/core losses", "Not measured (TC-4 planned)"),
        ("T-07", "Input MOSFET / protection devices", "Conduction/fault heating", "Not measured (TC-5 planned)"),
        ("T-08", "ESP32-S3", "Processing / AI inference", "Covered by PCB hottest area (TC-6)"),
        ("T-09", "LoRa module", "RF transmission", "Not measured at maximum TX"),
        ("T-10", "LED/buzzer alarm module", "Alarm active", "Not measured"),
        ("T-11", "Main enclosure external surface", "Governs T-class under Ex d", "Measured (TC-7/TC-8)"),
        ("T-12", "Front mesh / cover near sensor chamber", "Heater and airflow", "Not measured"),
    ], widths=(0.5, 2.0, 1.8, 2.3), status_col=3, size=8)
    _sub("f.4 Worst-case operating condition")
    for b in ["maximum permitted input supply voltage", "maximum ambient temperature (+60 °C)",
              "all eight MQ heaters energized", "ESP32-S3 performing AI inference",
              "LoRa transmitting at the maximum approved power (22 dBm)", "local alarm active",
              "DC fan operating according to the production sampling cycle"]:
        _bullet(b)
    _sub("f.5 Fan failure / airflow loss")
    _p("Measured: fan-stalled run of 180 min. Sensor body rose from 44.2 °C (normal) to 78.4 °C, PCB from 52.4 °C to "
       "63.4 °C, external enclosure from 32.1 °C to 43.9 °C — the fan-stalled condition is the governing case so far.",
       size=9.5)
    _sub("f.6 Blocked or restricted mesh")
    _p("Not tested. To be included where it affects internal cooling.", size=9.5)
    _sub("f.7 Electrical fault conditions")
    _p("Regulator fault, heater overvoltage, shorted load, abnormal high current and component overload: not tested; "
       "to be assessed by test or by circuit-protection analysis (EL-01…EL-07).", size=9.5)
    _sub("f.8 Measurement method")
    _p("Thermocouples at eight points plus ambient reference, logged for 180 minutes per condition. To be recorded "
       "for each point: ambient, input voltage, current, operating mode, fan/alarm/RF state, stabilization time and "
       "temperature. Thermocouple type and calibration: not yet recorded.", size=9.5)
    _sub("f.9 Thermal stabilization")
    _p("Criterion ≤2 K/h. The PCB reading under maximum load was still rising in the final hour (46.4 → 55.8 → "
       "58.3 °C) and must be repeated until stable.", size=9.5)
    _sub("f.10 Temperature correction / extrapolation")
    _p("T(Ta,max) = Ta,max + (T,measured − T,amb,test). Example from the fan-stalled run: 60 + (78.4 − 24.8) ≈ 114 °C. "
       "Use of this method is subject to ExCB acceptance; confirmation at maximum ambient is part of type testing.",
       size=9.5)
    _sub("f.11 Results table")
    _table(["Ref.", "Point", "Condition", "Test ambient", "Measured", "Rise", "Est. at +60 °C", "Status"], [
        ("T-01", "MQ sensor body", "Normal", "24.9 °C", "44.2 °C", "19.3 K", "≈79 °C", "Measured"),
        ("T-01", "MQ sensor body", "Maximum load", "24.2 °C", "55.0 °C", "30.8 K", "≈91 °C", "Measured"),
        ("T-01", "MQ sensor body", "Fan stalled", "24.8 °C", "78.4 °C", "53.6 K", "≈114 °C", "Measured"),
        ("T-02", "Fan motor", "Normal / stalled", "24.9 / 24.8 °C", "36.3 °C", "11.4 / 11.5 K", "≈71 °C", "Measured"),
        ("T-03", "5 V converter IC", "Maximum load", "—", "—", "—", "—", "Not measured"),
        ("T-04", "Power inductor", "Maximum load", "—", "—", "—", "—", "Not measured"),
        ("T-05", "PCB hottest area (incl. ESP32-S3)", "Fan stalled", "24.8 °C", "63.4 °C", "38.6 K", "≈99 °C",
         "Measured"),
        ("T-05", "PCB hottest area", "Maximum load", "24.2 °C", "58.3 °C", "34.1 K", "≈94 °C",
         "Preliminary — not stable"),
        ("T-06", "LoRa module", "Maximum TX", "—", "—", "—", "—", "Not measured"),
        ("T-07", "Alarm module", "Alarm active", "—", "—", "—", "—", "Not measured"),
        ("T-08", "External enclosure", "Fan stalled", "24.8 °C", "43.9 °C", "19.1 K", "≈79 °C",
         "Preliminary — check TC-7 contact"),
    ], widths=(0.45, 1.35, 0.9, 0.75, 0.65, 0.65, 0.75, 1.1), status_col=7, size=7.5)
    _sub("f.12 Preliminary temperature-class statement")
    _p("The GLD is proposed for temperature class T4. The final classification remains open pending the remaining "
       "hot-spot measurements (T-03, T-04, T-06, T-07, T-09, T-10, T-12), thermal stabilization at maximum load, "
       "maximum-ambient confirmation and the relevant fault conditions. The highest extrapolated value so far, "
       "≈114 °C, is below the effective T4 limit of 130 °C.", size=9.5)


# ===================================================================================== 2.6.g usage
def usage(d, h=None):
    _begin(d, h, "2.6.g.1 Usage and installation instructions — complete structure (g.2 … g.20)")
    _p("The following sections complete the draft instructions above in the structure of the revision guide "
       "(g.1 Safety warnings is given in 2.6.g.a). Values not yet defined are stated as such in the notes of each "
       "section.", size=9.5)
    with open(USAGE_JSON, encoding="utf-8") as f:
        secs = json.load(f)
    for s in secs:
        _sub(f"{s['id']} {s['title']}")
        table_rows = []
        for b in s["blocks"]:
            parts = [x.strip() for x in b.split("  ") if x.strip()]
            if len(parts) >= 2 and not b.startswith("-") and len(parts[0]) < 40 and not b.endswith(".") \
                    and not b[0].isdigit():
                table_rows.append(parts[:2])
                continue
            if table_rows:
                _table(table_rows[0], table_rows[1:], widths=(1.8, 4.8), size=8)
                table_rows = []
            if b.startswith("-"):
                _bullet(b.lstrip("- ").strip())
            elif len(b) < 60 and not b.endswith(".") and not b.endswith(":"):
                _p(b, size=9.5, bold=True, space_after=2)
            else:
                _p(b, size=9.5)
        if table_rows:
            _table(table_rows[0], table_rows[1:], widths=(1.8, 4.8), size=8)


# ===================================================================================== 2.6.h nameplate
def nameplate(d, h=None):
    _begin(d, h, "2.6.h.1 Proposed nameplate content (draft — not a certified marking)")
    _p("The nameplate artwork is finalized only after certification. The content below is the applicant's proposal "
       "for gas atmospheres only; no dust marking (category D / Ex t) is proposed, and the ambient range is the rated "
       "−20 °C to +60 °C.", size=9.5)
    _table(["Field", "Proposed content", "Status"], [
        ("Manufacturer", "PT Galaksi Megatama Indonesia, Bekasi, Indonesia", "Final"),
        ("Product / model", "Gas Leak Detector — GLD V2", "Final"),
        ("Serial number", "Per unit (sample: GLD2-0x1001)", "Final"),
        ("Year of manufacture", "Per unit", "Final"),
        ("ATEX equipment group / category", "II 2G", "Proposed — pending ExCB"),
        ("Ex marking", "Ex db IIC T4 Gb", "Proposed — pending ExCB"),
        ("Ambient temperature", "−20 °C ≤ Ta ≤ +60 °C", "Final (rated range)"),
        ("IP rating", "IP66", "Proposed — test evidence pending"),
        ("Electrical rating", "24 VDC, 8 W max.", "Final"),
        ("Cable entry", "M20×1.5", "TBC"),
        ("Certificate numbers", "ATEX / IECEx certificate numbers", "Pending certificate"),
        ("CE marking + notified-body number", "CE xxxx", "Pending certificate"),
        ("Warnings", "“WARNING – DO NOT OPEN WHEN AN EXPLOSIVE ATMOSPHERE MAY BE PRESENT”; additional warnings "
         "(e.g. electrostatic charging) as required by the certificate", "Proposed"),
    ], widths=(1.7, 3.6, 1.3), status_col=2, size=8)


# ===================================================================================== 2.6.i Ex certificates
def ex_certs(d, h=None):
    _begin(d, h, "2.6.i.1 Components requiring Ex certificates")
    _p("Ex-certified components needed for the proposed Ex d construction (gas group IIC). Each certificate must "
       "cover gas group IIC, the ambient range −20 °C to +60 °C and the thread form used.", size=9.5)
    _table(["Component", "Required certification", "Supplier / certificate no.", "Status"], [
        ("Flameproof enclosure (if a certified empty enclosure is used)", "Ex db IIC component certificate (ATEX/IECEx)",
         "TBC", "Pending certificate"),
        ("Cable gland, 24 VDC entry", "Ex d barrier gland for IIC, M20×1.5, IP66", "TBC", "Pending certificate"),
        ("Blanking plug / adaptor", "Ex d IIC, M20×1.5", "TBC", "Pending certificate"),
        ("Front mesh / flame arrestor (if claimed)", "Certificate or test evidence of flame-arresting function", "TBC",
         "Pending certificate"),
        ("Alarm beacon (if outside the flameproof enclosure)", "Ex certificate of the beacon, or inclusion in the "
         "equipment assessment", "TBC", "Open"),
        ("Antenna feed-through (if a certified bushing is used)", "Ex d IIC bushing", "TBC", "Open"),
        ("ESP32-S3 module, LoRa module", "RF/EMC certificates only (FCC, TELEC, CE) — not Ex certificates",
         "Espressif / Ebyte", "N.A. for Ex"),
    ], widths=(2.0, 2.2, 1.2, 1.2), status_col=3, size=8)


# ===================================================================================== 3 sample
def sample(d, h=None):
    _begin(d, h, "3.3 Sample register (current)")
    _table(["Item", "Value", "Status"], [
        ("Model", "GLD V2 (GLD_V2)", "Final"),
        ("Serial number", "GLD2-0x1001", "Final"),
        ("Status", "Powers on and runs in Inference / normal operation mode", "Final"),
        ("Hardware revision", "Main board MotherBoardGLDVer2, schematic rev. 1.0 (19 Jul 2026)", "Final"),
        ("Firmware / AI model version", "To be recorded on the sample label and test record", "Open"),
        ("Configuration", "24 VDC production configuration; battery path status per decision EX-17", "Decision required"),
    ], widths=(1.8, 3.6, 1.2), status_col=2, size=8.5)
    _sub("3.4 Test fixtures and auxiliary equipment (revision-guide list)")
    _table(["Equipment", "Purpose"], [
        ("Regulated 24 VDC power supply", "Stable 24 VDC during commissioning and functional testing"),
        ("Digital multimeter", "Voltage, polarity, continuity and grounding/bonding verification"),
        ("Calibrated gas source / gas test kit", "Verify sensor response to the target gases"),
        ("Gas test chamber", "Reproducible controlled gas exposure"),
        ("Alarm load / relay simulator", "Verify the 24 V alarm output (J2) and its load"),
        ("LoRa peer / gateway", "Verify reception of transmitted data"),
        ("Laptop and approved software", "Diagnostics, configuration, logging, firmware identification"),
        ("Calibrated torque screwdriver", "Glands, terminals, enclosure fasteners and grounding to approved torque"),
    ], widths=(2.2, 4.4), size=8.5)


# ===================================================================================== compliance matrix
def matrix(d, h=None):
    _begin(d, h, "Annex · Compliance matrix against the reviewer's revision guide")
    _p("Each requirement of the revision guide, where it is addressed in this document, and its status.", size=9.5)
    rows = [
        ("1.1", "Application form", "1.1", "Final"),
        ("1.2", "Business licence / registration", "1.2", "Final"),
        ("1.3", "Organisation chart and contacts", "1.3", "Partial — QA/production functions to add"),
        ("1.4", "Plant address and facilities", "1.4", "Partial — PCB assembler to add"),
        ("1.5", "ISO 9001", "1.5", "Open — audit planned Oct 2026"),
        ("2.1–2.3", "Product description, specification, technical parameters", "2.1–2.3", "Final"),
        ("2.4", "Photo set (12 views)", "2.4, 2.4.1, 2.4.2", "Partial — 9/12 available; PCB underside, grounding-lug and antenna-bulkhead close-ups to add"),
        ("2.5", "Intended use and environment (IIC, T4, Zone 1, −20…+60 °C)", "2.5", "Final (proposed classification)"),
        ("6(a).1–6(a).6", "Assembly, section, enclosure, mesh, MQ arrangement, fan drawings", "2.6.a, 2.6.a.1",
         "Partial — controlled toleranced drawings to issue"),
        ("6(a).7", "Main PCB schematic", "2.6.a.7", "Final (main board); sensor module open"),
        ("6(a).8", "PCB layout", "2.6.a.8", "Partial — rev/date, laminate data, sensor module"),
        ("6(a).9–6(a).13", "Terminal, grounding, cable entry, antenna, alarm drawings", "2.6.a.1 (M-D14, M-D15, M-D5)",
         "Partial — dimensioned drawings to issue"),
        ("6.b", "Ex-critical BOM (EX-01…17, EL-01…13)", "2.6.b, 2.6.b.1–2", "Partial"),
        ("6.c", "Non-metallic materials (MAT register)", "2.6.c, 2.6.c.1", "Open — supplier datasheets"),
        ("6.d", "Manufacturing process (d.1–d.13)", "2.6.d, 2.6.d.1", "Partial — parameters TBC"),
        ("6.e", "Ignition sources IS-01…17 and protection concept e.3", "2.6.e, 2.6.e.1–3", "Partial"),
        ("6.f", "Temperature class f.1–f.12", "2.6.f, 2.6.f.1", "Partial — measurements outstanding"),
        ("6.g", "Usage and installation instructions g.1–g.20", "2.6.g, 2.6.g.1", "Draft available"),
        ("6.h", "Nameplate (gas only, −20…+60 °C)", "2.6.h, 2.6.h.1", "Proposed"),
        ("6.i", "Ex component certificates", "2.6.i, 2.6.i.1", "Pending certificate"),
        ("3.1–3.2", "Sample and fixtures", "3.1–3.4", "Final"),
    ]
    _table(["Guide item", "Requirement", "Section", "Status"], rows, widths=(0.9, 2.8, 1.3, 1.6), status_col=3,
           size=8)
