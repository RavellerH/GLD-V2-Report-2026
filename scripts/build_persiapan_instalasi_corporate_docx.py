# -*- coding: utf-8 -*-
"""Build corporate-format .docx (and, via Word COM elsewhere, .pdf) versions of the
3 "persiapan instalasi RU IV Cilacap" documents, parsed from their canonical HTML
sources, so they read as a formal letterhead document instead of a browser printout.

Covers:
  - Pembagian_Persiapan_Instalasi_RU-IV_Cilacap
  - Daftar_Persiapan_Vendor_Instalasi_RU-IV_Cilacap
  - Draf_Permintaan_Penyediaan_Material_Instalasi_RU-IV_Cilacap

Run: python scripts/build_persiapan_instalasi_corporate_docx.py
"""
import os
import re
import base64
import binascii

from bs4 import BeautifulSoup, NavigableString, Tag
from PIL import Image
from docx import Document
from docx.shared import Pt, Inches, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DELIV = os.path.join(REPO, "Deliverables")
TMP_IMG_DIR = os.path.join(REPO, "scripts", "assets", "_tmp_persiapan_imgs")
os.makedirs(TMP_IMG_DIR, exist_ok=True)

NAVY = RGBColor(0x1B, 0x2A, 0x4A)
GRAY = RGBColor(0x5B, 0x5B, 0x5B)
INK = RGBColor(0x1F, 0x1F, 0x1F)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
GREEN = RGBColor(0x2C, 0x6B, 0x33)
AMBER = RGBColor(0x8A, 0x6D, 0x1E)
RED = RGBColor(0xB2, 0x3A, 0x3A)

LINE_GRAY = "D8D8D8"
HEAD_SHADE = "EFEFEC"
ZEBRA_SHADE = "FAFAF8"
WARN_BG, WARN_BD = "FFF6E5", "C98A12"
DANGER_BG, DANGER_BD = "FBE9E9", "B23A3A"
OK_BG, OK_BD = "EAF4EC", "3C7A44"

STATUS_COLOR = {"ready": GREEN, "open": AMBER, "block": RED}
STATUS_BG = {"ready": "EAF4EC", "open": "FFF3DC", "block": "FBE6E4"}

DOC_SPECS = [
    dict(
        src="Pembagian_Persiapan_Instalasi_RU-IV_Cilacap.html",
        out="Pembagian_Persiapan_Instalasi_RU-IV_Cilacap.docx",
        doc_no="LGU/GLD/INSTALASI-PEMBAGIAN/2026-001",
        revision="1.5", date="1 Oktober 2026",
        header_label="Pembagian Persiapan Instalasi — RU IV Cilacap",
    ),
    dict(
        src="Daftar_Persiapan_Vendor_Instalasi_RU-IV_Cilacap.html",
        out="Daftar_Persiapan_Vendor_Instalasi_RU-IV_Cilacap.docx",
        doc_no="LGU/GLD/INSTALASI-VENDOR/2026-001",
        revision="1.2", date="1 Oktober 2026",
        header_label="Daftar Persiapan Pelaksana Instalasi — RU IV Cilacap",
    ),
    dict(
        src="Draf_Permintaan_Penyediaan_Material_Instalasi_RU-IV_Cilacap.html",
        out="Draf_Permintaan_Penyediaan_Material_Instalasi_RU-IV_Cilacap.docx",
        doc_no="LGU/GLD/INSTALASI-MATERIAL/2026-001",
        revision="1.1", date="30 September 2026",
        header_label="Draf Permintaan Material Instalasi — RU IV Cilacap",
    ),
]

PARTY_ORDER = [
    ("lgu", "LGU & ITB"),
    ("pertamina", "Pertamina RU IV"),
    ("vendor", "Pelaksana Instalasi RU IV"),
]
PARTY_HEAD_SHADE = {"lgu": "1B2A4A", "pertamina": "2E5F8A", "vendor": "8A4A15"}


def make_doc():
    doc = Document()
    normal = doc.styles["Normal"]
    normal.font.name = "Calibri"
    normal.font.size = Pt(10.2)
    normal.font.color.rgb = INK
    normal.paragraph_format.space_after = Pt(7)
    normal.paragraph_format.line_spacing = 1.2
    for i, sz, col in [(1, 15, NAVY), (2, 12, NAVY), (3, 10.5, NAVY)]:
        st = doc.styles[f"Heading {i}"]
        st.font.name = "Calibri"
        st.font.size = Pt(sz)
        st.font.bold = True
        st.font.color.rgb = col
        st.paragraph_format.space_before = Pt(14 if i == 1 else 10)
        st.paragraph_format.space_after = Pt(5)
    sec = doc.sections[0]
    sec.left_margin = sec.right_margin = Cm(2.0)
    sec.top_margin = sec.bottom_margin = Cm(1.6)
    return doc, sec


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


def add_field(paragraph, field_code, fallback_text="1"):
    run = paragraph.add_run()
    b = OxmlElement("w:fldChar"); b.set(qn("w:fldCharType"), "begin")
    instr = OxmlElement("w:instrText"); instr.set(qn("xml:space"), "preserve"); instr.text = field_code
    sep = OxmlElement("w:fldChar"); sep.set(qn("w:fldCharType"), "separate")
    txt = OxmlElement("w:t"); txt.text = fallback_text
    end = OxmlElement("w:fldChar"); end.set(qn("w:fldCharType"), "end")
    run._r.append(b); run._r.append(instr)
    r2 = paragraph.add_run(); r2._r.append(sep)
    r3 = paragraph.add_run(); r3._r.append(txt)
    r4 = paragraph.add_run(); r4._r.append(end)


def add_picture_fit(paragraph, path, max_w_in, max_h_in=None):
    with Image.open(path) as im:
        w_px, h_px = im.size
    aspect = w_px / h_px
    w_in = max_w_in
    h_in = w_in / aspect
    if max_h_in and h_in > max_h_in:
        h_in = max_h_in
        w_in = h_in * aspect
    run = paragraph.add_run()
    run.add_picture(path, width=Inches(w_in), height=Inches(h_in))


def status_class(span_tag):
    classes = span_tag.get("class", [])
    for c in classes:
        if c in STATUS_COLOR:
            return c
    return None


def add_inline(paragraph, node, size=10.0, base_bold=False):
    if isinstance(node, NavigableString):
        text = str(node)
        if text:
            run = paragraph.add_run(text)
            run.font.size = Pt(size)
            run.font.bold = base_bold
        return
    if not isinstance(node, Tag):
        return
    if node.name in ("b", "strong"):
        for c in node.children:
            add_inline(paragraph, c, size=size, base_bold=True)
    elif node.name == "span" and status_class(node):
        cls = status_class(node)
        run = paragraph.add_run(" " + node.get_text().strip() + " ")
        run.font.size = Pt(size - 0.7)
        run.font.bold = True
        run.font.color.rgb = STATUS_COLOR[cls]
    elif node.name == "code":
        run = paragraph.add_run(node.get_text())
        run.font.size = Pt(size - 0.5)
        run.font.name = "Consolas"
        run.font.color.rgb = GRAY
    elif node.name == "a":
        run = paragraph.add_run(node.get_text())
        run.font.size = Pt(size)
        run.font.underline = True
        run.font.color.rgb = NAVY
    elif node.name == "br":
        paragraph.add_run().add_break()
    else:
        for c in node.children:
            add_inline(paragraph, c, size=size, base_bold=base_bold)


def render_table(doc, table_tag, col_widths=None):
    rows = table_tag.find_all("tr")
    if not rows:
        return
    ncols = max(len(tr.find_all(["th", "td"], recursive=False)) for tr in rows)
    tbl = doc.add_table(rows=0, cols=ncols)
    tbl.style = "Table Grid"
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    for ri, tr in enumerate(rows):
        cells_src = tr.find_all(["th", "td"], recursive=False)
        is_header = tr.find("th") is not None
        row_cells = tbl.add_row().cells
        for ci, cell_src in enumerate(cells_src):
            if ci >= ncols:
                break
            cell = row_cells[ci]
            cell.paragraphs[0].paragraph_format.space_after = Pt(2)
            if is_header:
                set_cell_shading(cell, HEAD_SHADE)
                run = cell.paragraphs[0].add_run(cell_src.get_text(" ", strip=True))
                run.font.bold = True
                run.font.size = Pt(8.6)
                run.font.color.rgb = GRAY
            else:
                if ri % 2 == 0:
                    set_cell_shading(cell, ZEBRA_SHADE)
                for c in cell_src.children:
                    add_inline(cell.paragraphs[0], c, size=9.3)
    if col_widths:
        for row in tbl.rows:
            for i, w in enumerate(col_widths):
                if i < len(row.cells):
                    row.cells[i].width = Inches(w)
    doc.add_paragraph().paragraph_format.space_after = Pt(4)


BANNER_STYLE = {
    "danger": (DANGER_BG, DANGER_BD),
    "ok": (OK_BG, OK_BD),
    "default": (WARN_BG, WARN_BD),
}


def render_banner(doc, div_tag):
    classes = div_tag.get("class", [])
    kind = "danger" if "danger" in classes else ("ok" if "ok" in classes else "default")
    bg, bd = BANNER_STYLE[kind]
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.rows[0].cells[0]
    set_cell_shading(cell, bg)
    set_cell_border(cell, bd, sz=6)
    cell.paragraphs[0].paragraph_format.space_after = Pt(2)
    for c in div_tag.children:
        add_inline(cell.paragraphs[0], c, size=9.6)
    doc.add_paragraph().paragraph_format.space_after = Pt(6)


def render_linklist(doc, ul_tag):
    for li in ul_tag.find_all("li", recursive=False):
        bp = doc.add_paragraph(style="List Bullet")
        bp.paragraph_format.space_after = Pt(3)
        for c in li.children:
            add_inline(bp, c, size=9.8)


def render_party_grid(doc, grid_tag):
    """grid3 with 3x <div class="col lgu|pertamina|vendor">."""
    tbl = doc.add_table(rows=2, cols=3)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    for ci, (key, label) in enumerate(PARTY_ORDER):
        hcell = tbl.rows[0].cells[ci]
        set_cell_shading(hcell, PARTY_HEAD_SHADE[key])
        hcell.paragraphs[0].paragraph_format.space_after = Pt(2)
        r = hcell.paragraphs[0].add_run(label)
        r.font.bold = True; r.font.size = Pt(9); r.font.color.rgb = WHITE
        bcell = tbl.rows[1].cells[ci]
        set_cell_shading(bcell, "FAFAF8")
        col_div = grid_tag.find("div", class_=re.compile(rf"\bcol\b.*\b{key}\b|\b{key}\b.*\bcol\b"))
        if col_div is None:
            # fallback: find by dot class inside
            for cd in grid_tag.find_all("div", class_="col"):
                if cd.find("span", class_=re.compile(rf"\bdot\b.*\b{key}\b")):
                    col_div = cd
                    break
        first = True
        if col_div:
            ul = col_div.find("ul")
            items = ul.find_all("li", recursive=False) if ul else []
            for li in items:
                p_ = bcell.paragraphs[0] if first else bcell.add_paragraph()
                first = False
                p_.paragraph_format.space_after = Pt(5)
                dash = p_.add_run("• ")
                dash.font.size = Pt(9); dash.font.bold = True
                for c in li.children:
                    if isinstance(c, Tag) and c.name == "li":
                        continue
                    add_inline(p_, c, size=8.8)
        set_cell_margins(bcell)
        tbl.rows[1].cells[ci].width = Inches(2.05)
        tbl.rows[0].cells[ci].width = Inches(2.05)
    set_table_borders(tbl)
    doc.add_paragraph().paragraph_format.space_after = Pt(6)


def set_cell_margins(cell, top=90, start=100, bottom=90, end=100):
    tcPr = cell._tc.get_or_add_tcPr()
    mar = OxmlElement("w:tcMar")
    for name, val in (("top", top), ("start", start), ("bottom", bottom), ("end", end)):
        node = OxmlElement(f"w:{name}")
        node.set(qn("w:w"), str(val))
        node.set(qn("w:type"), "dxa")
        mar.append(node)
    tcPr.append(mar)


def set_table_borders(table, color=LINE_GRAY, size="4"):
    tbl_pr = table._tbl.tblPr
    borders = OxmlElement("w:tblBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        node = OxmlElement(f"w:{edge}")
        node.set(qn("w:val"), "single")
        node.set(qn("w:sz"), size)
        node.set(qn("w:space"), "0")
        node.set(qn("w:color"), color)
        borders.append(node)
    tbl_pr.append(borders)


def render_card_grid(doc, grid_tag):
    """grid3 with 3x <div class="card"> (num + h3 + p) — simple summary cards."""
    cards = grid_tag.find_all("div", class_="card")
    if not cards:
        return
    tbl = doc.add_table(rows=1, cols=len(cards))
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, card in enumerate(cards):
        cell = tbl.rows[0].cells[i]
        set_cell_shading(cell, "F5F5F3")
        set_cell_margins(cell, top=120, bottom=120)
        h3 = card.find("h3")
        p_tag = card.find("p")
        para = cell.paragraphs[0]
        para.paragraph_format.space_after = Pt(3)
        if h3:
            r = para.add_run(h3.get_text(strip=True))
            r.font.bold = True; r.font.size = Pt(9.5); r.font.color.rgb = NAVY
        if p_tag:
            p2 = cell.add_paragraph()
            for c in p_tag.children:
                add_inline(p2, c, size=8.6)
    set_table_borders(tbl)
    doc.add_paragraph().paragraph_format.space_after = Pt(6)


def render_two_col(doc, div_tag):
    colcards = div_tag.find_all("div", class_="colcard")
    tbl = doc.add_table(rows=1, cols=len(colcards))
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, cc in enumerate(colcards):
        cell = tbl.rows[0].cells[i]
        is_warn = "warn" in cc.get("class", [])
        set_cell_shading(cell, WARN_BG if is_warn else OK_BG)
        set_cell_margins(cell)
        h4 = cc.find("h4")
        para = cell.paragraphs[0]
        para.paragraph_format.space_after = Pt(4)
        if h4:
            r = para.add_run(h4.get_text(strip=True))
            r.font.bold = True; r.font.size = Pt(9.3)
            r.font.color.rgb = AMBER if is_warn else GREEN
        ul = cc.find("ul")
        if ul:
            for li in ul.find_all("li", recursive=False):
                lp = cell.add_paragraph()
                lp.paragraph_format.space_after = Pt(3)
                dash = lp.add_run("• ")
                dash.font.size = Pt(8.8); dash.font.bold = True
                for c in li.children:
                    add_inline(lp, c, size=8.8)
    set_table_borders(tbl)
    doc.add_paragraph().paragraph_format.space_after = Pt(6)


def render_subhead(doc, div_tag):
    doc.add_heading(div_tag.get_text(strip=True), level=2)


def render_note(doc, p_tag):
    para = doc.add_paragraph()
    para.paragraph_format.space_after = Pt(6)
    for c in p_tag.children:
        add_inline(para, c, size=9.2)
    for r in para.runs:
        r.font.italic = True
        r.font.color.rgb = GRAY


_img_counter = [0]


def save_data_uri(src):
    m = re.match(r"data:image/(\w+);base64,(.*)", src, re.S)
    if not m:
        return None
    ext, b64 = m.group(1), m.group(2)
    ext = "jpg" if ext == "jpeg" else ext
    _img_counter[0] += 1
    path = os.path.join(TMP_IMG_DIR, f"img_{_img_counter[0]}.{ext}")
    try:
        data = base64.b64decode(b64)
    except binascii.Error:
        return None
    with open(path, "wb") as f:
        f.write(data)
    return path


def render_evgrid(doc, div_tag):
    cards = div_tag.find_all("div", class_=re.compile(r"\bevcard\b"))
    for card in cards:
        img = card.find("img")
        cap = card.find("div", class_="evcap")
        full = "evfull" in card.get("class", [])
        if img:
            path = None
            src = img.get("src", "")
            if src.startswith("data:image"):
                path = save_data_uri(src)
            if path:
                fp = doc.add_paragraph()
                fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
                add_picture_fit(fp, path, max_w_in=6.0 if full else 3.0, max_h_in=4.4 if full else 2.6)
        if cap:
            cp = doc.add_paragraph()
            cp.paragraph_format.space_after = Pt(10)
            cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
            cap_children = list(cap.children)
            for i, c in enumerate(cap_children):
                add_inline(cp, c, size=8.6)
                if isinstance(c, Tag) and c.name == "b" and i + 1 < len(cap_children):
                    cp.add_run().add_break()
            for r in cp.runs:
                r.font.color.rgb = GRAY
                r.font.italic = True


def render_flowdiag(doc, div_tag):
    nodes = div_tag.find_all("div", class_="fnode")
    steps = []
    for n in nodes:
        b = n.find("b")
        sp = n.find("span")
        label = b.get_text(strip=True) if b else ""
        desc = sp.get_text(strip=True) if sp else ""
        steps.append(f"{label} — {desc}" if desc else label)
    para = doc.add_paragraph()
    para.paragraph_format.space_after = Pt(8)
    run = para.add_run(" → ".join(f"({i+1}) {s}" for i, s in enumerate(steps)))
    run.font.size = Pt(9.3)
    run.font.color.rgb = INK


def render_sign(doc, div_tag):
    parts = list(div_tag.find_all("div", recursive=False))
    if not parts:
        return
    tbl = doc.add_table(rows=1, cols=len(parts))
    for i, part in enumerate(parts):
        cell = tbl.rows[0].cells[i]
        set_cell_margins(cell, top=400, bottom=100)
        for c in part.children:
            add_inline(cell.paragraphs[0], c, size=9.5)
    set_table_borders(tbl)
    doc.add_paragraph().paragraph_format.space_after = Pt(6)


def render_children(doc, parent, skip=None):
    """Generic dispatcher: walk parent's direct children and render each block
    by tag/class. Used both for a <div class="body"> wrapper and, when a section
    has no such wrapper, directly on the <section> (with `skip` = its head div)."""
    for child in parent.children:
        if not isinstance(child, Tag) or child is skip:
            continue
        classes = child.get("class") or []
        if child.name == "div" and "banner" in classes:
            render_banner(doc, child)
        elif child.name == "table" and "table" in classes:
            render_table(doc, child)
        elif child.name == "ul" and ("linklist" in classes or "plain" in classes):
            render_linklist(doc, child)
        elif child.name == "div" and "subhead" in classes:
            render_subhead(doc, child)
        elif child.name == "div" and "grid3" in classes:
            if child.find("div", class_="col"):
                render_party_grid(doc, child)
            elif child.find("div", class_="card"):
                render_card_grid(doc, child)
        elif child.name == "div" and "two-col" in classes:
            render_two_col(doc, child)
        elif child.name == "div" and "evgrid" in classes:
            render_evgrid(doc, child)
        elif child.name == "div" and "flowdiag" in classes:
            render_flowdiag(doc, child)
        elif child.name == "div" and "legend" in classes:
            pass  # skip color legend, not meaningful on paper without matching colors
        elif child.name == "div" and "sign" in classes:
            render_sign(doc, child)
        elif child.name == "p" and ("role" in classes or "note" in classes):
            render_note(doc, child)
        elif child.name == "p":
            pp = doc.add_paragraph()
            pp.paragraph_format.space_after = Pt(6)
            for c in child.children:
                add_inline(pp, c, size=10)
        elif child.name == "div" and not classes:
            # unclassed wrapper div (e.g. an extra <div class="body" style="...">
            # further down) - recurse into it
            render_children(doc, child)


def add_document_control(doc, doc_no, revision, date, spec):
    rows = [
        ("Nomor dokumen", doc_no),
        ("Revisi", revision),
        ("Tanggal", date),
        ("Status", "Draf kerja — untuk koordinasi PT Pertamina Patra Niaga, RU IV Cilacap"),
        ("Disiapkan oleh", "PT LAPI Ganesha Utama, bersama Lab IoT & Fisika Institut Teknologi Bandung"),
        ("Ditujukan kepada", "PT Pertamina Patra Niaga — RU IV Cilacap"),
    ]
    doc.add_paragraph().paragraph_format.space_after = Pt(2)
    p_ = doc.add_paragraph()
    r = p_.add_run("Document Control")
    r.font.bold = True; r.font.size = Pt(11); r.font.color.rgb = NAVY
    p_.paragraph_format.space_after = Pt(4)
    mt = doc.add_table(rows=0, cols=2)
    mt.style = "Table Grid"
    for k, v in rows:
        row = mt.add_row().cells
        set_cell_shading(row[0], HEAD_SHADE)
        row[0].paragraphs[0].paragraph_format.space_after = Pt(2)
        r0 = row[0].paragraphs[0].add_run(k)
        r0.font.bold = True; r0.font.size = Pt(9.3); r0.font.color.rgb = GRAY
        row[1].paragraphs[0].paragraph_format.space_after = Pt(2)
        r1 = row[1].paragraphs[0].add_run(v)
        r1.font.size = Pt(9.6)
        row[0].width = Inches(1.9); row[1].width = Inches(4.6)
    doc.add_paragraph().paragraph_format.space_after = Pt(12)


def build_one(spec):
    src_path = os.path.join(DELIV, spec["src"])
    out_path = os.path.join(DELIV, spec["out"])
    soup = BeautifulSoup(open(src_path, encoding="utf-8").read(), "html.parser")
    wrap = soup.find("main", class_="wrap")
    hero = wrap.find("section", class_="hero")

    doc, sec = make_doc()

    # letterhead
    lt = doc.add_table(rows=1, cols=1)
    lc = lt.rows[0].cells[0]
    set_cell_shading(lc, "1B2A4A")
    lc.paragraphs[0].paragraph_format.space_after = Pt(2)
    lr = lc.paragraphs[0].add_run("PT LAPI GANESHA UTAMA")
    lr.font.bold = True; lr.font.size = Pt(14); lr.font.color.rgb = WHITE
    lp2 = lc.add_paragraph()
    lp2.paragraph_format.space_after = Pt(3)
    lr2 = lp2.add_run("Bekerja sama dengan Lab IoT & Fisika Institut Teknologi Bandung")
    lr2.font.size = Pt(9.5); lr2.font.color.rgb = RGBColor(0xC7, 0xD2, 0xE0)
    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    # title
    h1 = hero.find("h1")
    title = doc.add_heading(level=0)
    title.paragraph_format.space_after = Pt(4)
    title_text = h1.get_text(" ", strip=True)
    tr = title.add_run(title_text)
    tr.font.size = Pt(19); tr.font.bold = True; tr.font.color.rgb = NAVY

    sub = hero.find("p", class_="sub")
    if sub:
        p_ = doc.add_paragraph()
        p_.paragraph_format.space_after = Pt(12)
        for c in sub.children:
            add_inline(p_, c, size=10.8)
        for r in p_.runs:
            r.font.color.rgb = GRAY

    add_document_control(doc, spec["doc_no"], spec["revision"], spec["date"], spec)
    doc.add_page_break()

    # header / footer
    header = sec.header
    header.is_linked_to_previous = False
    hp = header.paragraphs[0]
    hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    hr = hp.add_run(spec["header_label"] + "  |  Draf Kerja — Konfidensial")
    hr.font.size = Pt(8); hr.font.color.rgb = GRAY; hr.font.italic = True

    footer = sec.footer
    footer.is_linked_to_previous = False
    fp = footer.paragraphs[0]
    fr1 = fp.add_run(f"{spec['doc_no']}  ·  Rev. {spec['revision']}")
    fr1.font.size = Pt(8); fr1.font.color.rgb = GRAY
    fp.paragraph_format.tab_stops.add_tab_stop(Inches(6.9), alignment=2)
    fp.add_run("\t")
    add_field(fp, "PAGE", "1")
    fp.add_run(" dari ")
    add_field(fp, "NUMPAGES", "1")
    for r in fp.runs:
        r.font.size = Pt(8); r.font.color.rgb = GRAY

    # body: walk top-level children of <main class="wrap"> after hero
    started = False
    for node in wrap.children:
        if not isinstance(node, Tag):
            continue
        if node is hero:
            started = True
            continue
        if not started:
            continue
        if node.name == "footer":
            continue
        if node.name == "div" and "banner" in (node.get("class") or []):
            render_banner(doc, node)
        elif node.name == "section" and "section" in (node.get("class") or []):
            head = node.find("div", class_="head")
            body = node.find("div", class_="body")
            if head:
                h2 = head.find("h2")
                n_span = head.find("span", class_="n")
                num = n_span.get_text(strip=True) if n_span else ""
                heading_text = f"{num}. {h2.get_text(strip=True)}" if num else h2.get_text(strip=True)
                doc.add_heading(heading_text, level=1)
            if body:
                render_children(doc, body)
            else:
                render_children(doc, node, skip=head)
        # top-level grid3 (Pembagian doesn't have one outside sections; Daftar_Vendor's summary
        # grid3 sits directly under wrap, before section 1)
        elif node.name == "div" and "grid3" in (node.get("class") or []):
            if node.find("div", class_="card"):
                render_card_grid(doc, node)

    doc.save(out_path)
    print("written", out_path)
    return out_path


if __name__ == "__main__":
    for spec in DOC_SPECS:
        build_one(spec)
