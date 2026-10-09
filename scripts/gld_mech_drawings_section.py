# -*- coding: utf-8 -*-
"""Shared content: complete mechanical / enclosure / assembly drawing set for the GLD (section 2.6.a).

Used by scripts/build_cert_doc_docx.py and scripts/build_iecex_input_form_filled_docx.py so both
certification documents carry the same, complete set of technical drawings.

Sources (rendered into scripts/assets/mech_drawings/):
  - Sumber Dokumen/GLD U Bolt Bracket/            "ATEX CASING v2" CAD (STEP) — dimensioned sheet + 6 views
  - Sumber Dokumen/GLD CASE ATEX V3.pdf            "GLD ATEX CASE v3" — 7 sheets
  - Sumber Dokumen/CASING/common base M20-1.5.pdf  BP18-1Z supplier drawing
  - Manufacturer design package (dossier Rev. 25 Sep 2026, drawing/assembly pages 17–45)

render(doc, h1=..., num="2.6.a.1") appends the content to an existing python-docx Document.
"""
import os

from PIL import Image
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = os.path.join(REPO, "scripts", "assets", "mech_drawings")

NAVY = RGBColor(0x1B, 0x33, 0x5F)
INK = RGBColor(0x26, 0x23, 0x21)
GRAY = RGBColor(0x55, 0x5B, 0x66)
HEAD_SHADE = "EAEFF9"
NOTE_SHADE = "F3F6FC"
WARN_SHADE = "FBEEE4"

# ---------------------------------------------------------------- drawing register
# (id, file, title, description, type)
CASING_V2_VIEWS = [
    ("casing_v2_front.jpg", "Front"), ("casing_v2_rear.jpg", "Rear"), ("casing_v2_left.jpg", "Left"),
    ("casing_v2_right.jpg", "Right"), ("casing_v2_top.jpg", "Top"), ("casing_v2_bottom.jpg", "Bottom"),
]

GROUP_A = [
    ("M-A1", "casing_v2_sheet.jpg", "ATEX CASING v2 — enclosure envelope & U-bolt mounting plate, dimensioned sheet",
     "Orthographic and isometric views with real dimensions (enclosure neck Ø75 mm, overall probe height "
     "191.51 mm, mounting plate 250 × 250 mm with toleranced hole pattern), U-bolt parameter table (2″/DN50, "
     "M10 thread) and title block (drafted 31 Aug 2026). Drawn from the STEP solid model (mm).",
     "Dimensioned CAD drawing"),
]

GROUP_B = [
    ("M-B1", "case_v3-1.jpg", "GLD ATEX CASE v3 — sheet 1: isometric views of the assembled detector",
     "Assembled enclosure with sensor head, external antenna and alarm beacon, three isometric viewpoints.",
     "CAD render"),
    ("M-B2", "case_v3-2.jpg", "GLD ATEX CASE v3 — sheet 2: top and bottom views",
     "Top view (cable-entry bosses, alarm beacon, antenna) and bottom view (sensor-head mesh face).",
     "CAD render"),
    ("M-B3", "case_v3-3.jpg", "GLD ATEX CASE v3 — sheet 3: side and rear views",
     "Left, right and rear-isometric views showing the base, sensor head, beacon and antenna positions.",
     "CAD render"),
    ("M-B4", "case_v3-4.jpg", "GLD ATEX CASE v3 — sheet 4: front/back and mounting-lug views",
     "Views showing the wall-mounting lugs of the base and the cover opening.", "CAD render"),
    ("M-B5", "case_v3-5.jpg", "GLD ATEX CASE v3 — sheet 5: exploded views (four viewpoints)",
     "Exploded assembly: base, cover, sensor case, mesh disc, sensor-case cover, beacon, antenna and glands.",
     "CAD exploded view"),
    ("M-B6", "case_v3-6.jpg", "GLD ATEX CASE v3 — sheet 6: exploded views of the sensor-head stack",
     "Sensor case, DC fan, stainless-steel filter mesh disc and case cover shown in stacking order.",
     "CAD exploded view"),
    ("M-B7", "case_v3-7.jpg", "GLD ATEX CASE v3 — sheet 7: dimensioned drawing with title block",
     "Dimensioned orthographic views and section of the sensor case; callouts for sensor case, DC fan, "
     "stainless-steel filter mesh disc, case cover and transparent glass; title block “GLD ATEX CASE v3” "
     "(drafted 8 Sep 2026). Internal contingency/alternate enclosure design.",
     "Dimensioned CAD drawing"),
]

GROUP_C = [
    ("M-C1", "bp18-1.jpg", "Universal Base BP18-1Z — supplier reference drawing",
     "Die-cast base, material ADC12, 0.6 kg, scale 1:1: 2 × M20×1.5-6H cable-entry threads, 4 × M4-6H and "
     "1 × M5×1.5-6g fixing threads, 3 × Ø8 mm mounting holes, internal bore up to Ø94.7 mm, overall "
     "≈124 × 115 × 67.5 mm. Candidate junction-box/terminal sub-component from the casing supply chain.",
     "Supplier dimensioned drawing"),
]

GROUP_D = [
    ("M-D1", "pkg_17.jpg", "LoRa antenna, MQ sensor and enclosure body & cover",
     "External LoRa antenna with cable, MQ sensor with integrated stainless-steel mesh, and the enclosure "
     "body and cover (production parts).", "Component photographs"),
    ("M-D2", "pkg_18.jpg", "Rubber gasket — locations", "Rubber gaskets fitted at the cover-to-body and "
     "sensor-head joints (four locations marked).", "Component photographs"),
    ("M-D3", "pkg_19.jpg", "Rubber gasket — part", "Rubber gasket as a separate part.", "Component photograph"),
    ("M-D4", "pkg_20.jpg", "Stainless wire-mesh plate", "Front stainless-steel wire-mesh plate (gas inlet) "
     "and its seating in the cover.", "Component photographs"),
    ("M-D5", "pkg_21.jpg", "Visual/audible alarm beacon; motherboard inside base casing",
     "LED and buzzer beacon with rubber gasket; main PCB mounted in the base enclosure.",
     "Component photographs"),
    ("M-D6", "pkg_22.jpg", "Motherboard with MQ sensors inside base casing",
     "Main PCB with the eight MQ sensors fitted, seen through the open base enclosure.",
     "Component photograph"),
    ("M-D7", "pkg_24.jpg", "Common base design", "Dimensioned base design drawing with title block.",
     "Dimensioned drawing"),
    ("M-D8", "pkg_25.jpg", "Overall exploded views I and II", "Labelled exploded line drawings of the "
     "complete detector (cover, mesh, fan, sensor head, base, glands, beacon, antenna).",
     "Exploded line drawing"),
    ("M-D9", "pkg_26.jpg", "Overall exploded view III", "Exploded line drawing, third viewpoint.",
     "Exploded line drawing"),
    ("M-D10", "pkg_27.jpg", "Motherboard PCB power-in and PCB cover (terminal module)",
     "Populated main PCB (3D) and the PCB cover carrying the terminal module with the 24 VDC power-in "
     "position marked.", "CAD render"),
    ("M-D11", "pkg_28.jpg", "Motherboard and PCB cover", "Main PCB and PCB cover shown as separate parts.",
     "CAD render"),
    ("M-D12", "pkg_42.jpg", "Component drawing", "Enclosure; PCB + sensors; cover + fan; alarm module; "
     "cover + mesh; antenna 3 dBi.", "Component photographs"),
    ("M-D13", "pkg_43.jpg", "Electrical block diagram and enclosure structure",
     "Block diagram of the main board and dimensioned enclosure-structure views.",
     "Block diagram / dimensioned drawing"),
    ("M-D14", "pkg_44.jpg", "Terminal — 24 VDC power in",
     "24 VDC waterproof cable connector and the terminal block on the PCB cover.", "Photographs"),
    ("M-D15", "pkg_45.jpg", "Grounding", "External grounding stud, marked with the protective-earth symbol, "
     "installed on the enclosure body.", "Photograph"),
]

GROUP_E = [
    ("M-E1", "pkg_33.jpg", "Assembly drawing — exploded view",
     "Casing cover, stainless wire-mesh plate, wire-mesh locking bracket and DC fan.", "Assembly illustration"),
    ("M-E2", "pkg_34.jpg", "Assembly step — casing cover", "Casing cover parts.", "Assembly illustration"),
    ("M-E3", "pkg_35.jpg", "Assembly step — sensor case and rubber gasket",
     "Sensor case with rubber gasket (drawing also labels a battery case — see note).", "Assembly illustration"),
    ("M-E4", "pkg_36.jpg", "Assembly step — LED & buzzer", "Alarm beacon fitted to the base.",
     "Assembly illustration"),
    ("M-E5", "pkg_37.jpg", "Assembly step — 24 VDC power in", "Cable entry for the 24 VDC supply.",
     "Assembly illustration"),
    ("M-E6", "pkg_38.jpg", "Assembly step — put motherboard into base casing", "Base casing and motherboard "
     "placement.", "Assembly photographs"),
    ("M-E7", "pkg_39.jpg", "Assembly step — secure motherboard; install LoRa antenna cable",
     "Secure the motherboard with the designated mounting screws and install the antenna cable.",
     "Assembly photographs"),
    ("M-E8", "pkg_40.jpg", "Assembly step — antenna position",
     "In the current version the LoRa antenna is positioned above the base enclosure (earlier side position "
     "superseded).", "Assembly photographs"),
    ("M-E9", "pkg_41.jpg", "Assembly step — alarm cables, DC fan and cover closure",
     "Connect LED/buzzer cables; attach DC fan to the cover behind the stainless-steel mesh plate; connect the "
     "fan cable; close the cover by turning it clockwise.", "Assembly photographs"),
]

GROUP_F = [
    ("M-F1", "pkg_29.jpg", "MQ-2 and MQ-3 — sensor parameters and dimension drawings", "Data sheet shows MQ-3; the fitted part is MQ-3B (BOM) — data sheet of the B-variant to be confirmed.", "Sensor data sheet"),
    ("M-F2", "pkg_30.jpg", "MQ-4 and MQ-5 — sensor parameters and dimension drawings", "", "Sensor data sheet"),
    ("M-F3", "pkg_31.jpg", "MQ-6 and MQ-7 — sensor parameters and dimension drawings", "Data sheet shows MQ-7; the fitted part is MQ-7B (BOM) — data sheet of the B-variant to be confirmed.", "Sensor data sheet"),
    ("M-F4", "pkg_32.jpg", "MQ-8 and MQ-135 — sensor parameters and dimension drawings", "",
     "Sensor data sheet"),
]

GROUPS = [
    ("A", "Primary enclosure and mounting — ATEX CASING v2", GROUP_A),
    ("B", "Enclosure design GLD ATEX CASE v3 — complete sheet set", GROUP_B),
    ("C", "Junction-box / terminal base — supplier drawing", GROUP_C),
    ("D", "Components, structure, terminal and grounding", GROUP_D),
    ("E", "Assembly sequence", GROUP_E),
    ("F", "MQ sensor dimension drawings", GROUP_F),
]

doc = None


def _shade(cell, hex_color):
    el = OxmlElement("w:shd")
    el.set(qn("w:val"), "clear")
    el.set(qn("w:fill"), hex_color)
    cell._tc.get_or_add_tcPr().append(el)


def _p(text, size=10, bold=False, italic=False, color=None, space_after=6, align=None):
    para = doc.add_paragraph()
    para.paragraph_format.space_after = Pt(space_after)
    if align is not None:
        para.alignment = align
    r = para.add_run(text)
    r.font.size = Pt(size)
    r.font.bold = bold
    r.font.italic = italic
    r.font.color.rgb = color or INK
    return para


def _fig_style(d):
    """Paragraph style for drawing/figure titles: outline level 6 (PDF bookmark) and source of the list of drawings."""
    from docx.enum.style import WD_STYLE_TYPE
    from docx.oxml import OxmlElement as _OE
    from docx.oxml.ns import qn as _qn
    name = "GLD Figure Title"
    try:
        return d.styles[name]
    except KeyError:
        st = d.styles.add_style(name, WD_STYLE_TYPE.PARAGRAPH)
        st.base_style = d.styles["Normal"]
        st.paragraph_format.keep_with_next = True
        ppr = st.element.get_or_add_pPr()
        ol = _OE("w:outlineLvl")
        ol.set(_qn("w:val"), "5")
        ppr.append(ol)
        return st


def _hd(d, text, level, size, align=None, after=4, color=None):
    """Real Word heading (for TOC + PDF outline) with explicit run formatting."""
    if level == 6:
        para = d.add_paragraph(style=_fig_style(d))
    else:
        para = d.add_heading("", level=level)
    para.paragraph_format.space_after = Pt(after)
    para.paragraph_format.space_before = Pt(8 if level <= 5 else 2)
    para.paragraph_format.keep_with_next = True
    if align is not None:
        para.alignment = align
    r = para.add_run(text)
    r.font.size = Pt(size)
    r.font.bold = True
    r.font.italic = False
    r.font.name = "Calibri"
    r.font.color.rgb = color or NAVY
    return para


def _sub(text):
    return _hd(doc, text, 5, 11)


def _note(text, fill=NOTE_SHADE):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.rows[0].cells[0]
    _shade(cell, fill)
    cell.paragraphs[0].paragraph_format.space_after = Pt(2)
    r = cell.paragraphs[0].add_run(text)
    r.font.size = Pt(9)
    r.font.color.rgb = GRAY
    doc.add_paragraph().paragraph_format.space_after = Pt(2)


def _table(headers, rows, widths):
    tbl = doc.add_table(rows=1, cols=len(headers))
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
        r.font.size = Pt(8.5)
        r.font.color.rgb = NAVY
    for vals in rows:
        row = tbl.add_row()
        row._tr.get_or_add_trPr().append(OxmlElement("w:cantSplit"))
        for i, v in enumerate(vals):
            para = row.cells[i].paragraphs[0]
            para.paragraph_format.space_after = Pt(1)
            r = para.add_run(v)
            r.font.size = Pt(8.5)
            if i == 0:
                r.font.bold = True
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
    doc.add_paragraph().paragraph_format.space_after = Pt(2)


def _fit(path, max_w, max_h):
    with Image.open(path) as im:
        w, h = im.size
    width = max_w
    if width * h / w > max_h:
        width = max_h * w / h
    return width


def _figure(fid, fn, title, desc, max_w, max_h):
    path = os.path.join(A, fn)
    para = doc.add_paragraph()
    para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    para.paragraph_format.space_after = Pt(2)
    para.paragraph_format.keep_with_next = True
    para.add_run().add_picture(path, width=Inches(_fit(path, max_w, max_h)))
    _hd(doc, f"{fid}. {title}", 6, 9.5, align=WD_ALIGN_PARAGRAPH.CENTER, after=1 if desc else 12)
    if desc:
        cap = doc.add_paragraph()
        cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        cap.paragraph_format.space_after = Pt(12)
        r2 = cap.add_run(desc)
        r2.font.size = Pt(8.5)
        r2.font.color.rgb = GRAY


import gld_hide_flags as _hide  # noqa: E402


def render(d, h1=None, content_w=6.2, num="2.6.a.1"):
    """Append the complete mechanical drawing set to document d."""
    global doc
    doc = d
    if h1:
        h1(f"{num} Mechanical, enclosure and assembly drawings — complete set")
    else:
        _p(f"{num} Mechanical, enclosure and assembly drawings — complete set", size=14, bold=True, color=NAVY)
    _p("This subsection reproduces every mechanical, enclosure and assembly drawing currently available for the "
       "GLD: the CAD drawings of the primary enclosure and mounting plate, the full sheet set of the GLD ATEX "
       "CASE v3 enclosure design, the supplier drawing of the candidate junction-box base, and the component, "
       "structure, terminal, grounding, assembly-sequence and sensor drawings of the manufacturer's design "
       "package. Each figure carries a reference number (M-xx) listed in the register below.")

    _sub("Drawing register")
    rows = []
    for g, gtitle, items in GROUPS:
        for fid, fn, title, desc, typ in items:
            rows.append((fid, title, typ, g))
    rows.insert(1, ("M-A2", "ATEX CASING v2 — six orthographic CAD views (front, rear, left, right, top, bottom)",
                    "CAD render", "A"))
    rows = [(r[0], r[1], ("Withheld in this issue" if _hide.hidden_ref(r[0]) else r[2]), r[3]) for r in rows]
    _table(["Ref.", "Title", "Type", "Group"], rows, widths=(0.6, 3.9, 1.5, 0.6))

    _note("Status of this drawing set: the CAD sheets (M-A1, M-B7, M-C1, M-D7) carry real dimensions and title "
          "blocks; the remaining figures are CAD renders, line illustrations or photographs of production parts. "
          "Controlled, toleranced drawings that call out the Ex d flame-path parameters (joint gap and length, "
          "thread engagement, free internal volume) are still to be issued by the enclosure manufacturer. "
          "Two figures still show superseded details: M-E3 labels a battery case and M-D14 labels the power input "
          "as \"battery or 24 VDC\"; the production configuration is 24 VDC only. M-E8 records that the antenna "
          "has moved from the side to the top of the base enclosure.", fill=WARN_SHADE)

    if _hide.HIDE_SIDE_ANTENNA:
        _note(_hide.WITHHELD_NOTE + " Withheld references: " + ", ".join(sorted(_hide.SIDE_ANTENNA_MREFS)) + ".")
    for g, gtitle, items in GROUPS:
        shown = [it for it in items if not _hide.hidden_ref(it[0])]
        if g == "A" and _hide.hidden_ref("M-A2"):
            shown = []
        doc.add_page_break()
        _sub(f"{g}. {gtitle}")
        if not shown:
            _note(_hide.WITHHELD_NOTE)
            continue
        items = shown
        if g == "A":
            fid, fn, title, desc, _ = items[0]
            _figure(fid, fn, title, desc, content_w, 6.5)
            # six views in a 3 x 2 grid
            tbl = doc.add_table(rows=2, cols=3)
            tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
            for k, (vfn, label) in enumerate(CASING_V2_VIEWS):
                cell = tbl.rows[k // 3].cells[k % 3]
                para = cell.paragraphs[0]
                para.alignment = WD_ALIGN_PARAGRAPH.CENTER
                path = os.path.join(A, vfn)
                para.add_run().add_picture(path, width=Inches(_fit(path, content_w / 3 - 0.15, 2.4)))
                lp = cell.add_paragraph()
                lp.alignment = WD_ALIGN_PARAGRAPH.CENTER
                lr = lp.add_run(label + " view")
                lr.font.size = Pt(8.5)
                lr.font.color.rgb = GRAY
            cap = doc.add_paragraph()
            cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            cap.paragraph_format.space_after = Pt(12)
            r1 = cap.add_run("M-A2. ATEX CASING v2 — six orthographic CAD views\n")
            r1.font.bold = True
            r1.font.size = Pt(9.5)
            r1.font.color.rgb = NAVY
            r2 = cap.add_run("Rendered from the same STEP solid model as M-A1 (enclosure, sensor head and U-bolt "
                             "mounting plate).")
            r2.font.size = Pt(8.5)
            r2.font.color.rgb = GRAY
            continue
        for i, (fid, fn, title, desc, _) in enumerate(items):
            if i and g in ("B", "C", "F"):
                doc.add_page_break()
            max_h = 8.3 if g in ("D", "E", "F") else 7.5
            _figure(fid, fn, title, desc, content_w, max_h if g != "D" else 4.2)
