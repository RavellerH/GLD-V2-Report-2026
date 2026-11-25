from pathlib import Path
import shutil
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from pypdf import PdfReader, PdfWriter

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "Paket Meeting TUV SUD 26November2026"
OUT.mkdir(exist_ok=True)
CERT = ROOT / "Deliverables/Dokumen_Teknis_Sertifikasi_GLD_IECEx_ATEX.pdf"
MANUAL = ROOT / "Deliverables/Instruction_Manual_GLD.pdf"
PHOTO = ROOT / "scripts/assets/balongan_13nov/unit_gld_4_tampak.jpg"
BLUE = RGBColor(0x2B, 0x5F, 0xCB)


def shade(cell, color):
    tcPr = cell._tc.get_or_add_tcPr()
    s = OxmlElement("w:shd")
    s.set(qn("w:val"), "clear"); s.set(qn("w:color"), "auto"); s.set(qn("w:fill"), color)
    tcPr.append(s)


def new_doc():
    d = Document()
    sec = d.sections[0]
    sec.page_width, sec.page_height = Cm(21), Cm(29.7)
    sec.left_margin = sec.right_margin = Cm(2)
    sec.top_margin = sec.bottom_margin = Cm(1.8)
    st = d.styles["Normal"]; st.font.name = "Calibri"; st.font.size = Pt(10)
    st.paragraph_format.space_after = Pt(4)
    return d


def h(d, text, size=12):
    p = d.add_paragraph(); r = p.add_run(text); r.bold = True; r.font.size = Pt(size); r.font.color.rgb = BLUE
    p.paragraph_format.space_before = Pt(8)
    return p


def table(d, rows, widths, head=True):
    t = d.add_table(rows=len(rows), cols=len(rows[0])); t.style = "Table Grid"
    tblPr = t._tbl.tblPr; lay = OxmlElement("w:tblLayout"); lay.set(qn("w:type"), "fixed"); tblPr.append(lay)
    for i, row in enumerate(rows):
        for j, val in enumerate(row):
            c = t.cell(i, j); c.width = Cm(widths[j]); c.text = ""
            r = c.paragraphs[0].add_run(val); r.font.size = Pt(9)
            if head and i == 0:
                r.bold = True; shade(c, "DCE6F7")
    d.add_paragraph()
    return t


def bullets(d, items):
    for it in items:
        d.add_paragraph(it, style="List Bullet")


def slim(page):
    import re
    from pypdf.generic import DictionaryObject, NameObject
    res = page["/Resources"].get_object()
    xo = res.get("/XObject")
    if not xo:
        return page
    used = set(re.findall(rb"/([^\s/\[\]<>()]+)\s+Do", page.get_contents().get_data()))
    keep = DictionaryObject({NameObject(k): v for k, v in xo.get_object().items() if k[1:].encode() in used})
    new_res = DictionaryObject(res); new_res[NameObject("/XObject")] = keep
    page[NameObject("/Resources")] = new_res
    return page


def to_pdf(docx):
    import subprocess
    pdf = docx.with_suffix(".pdf")
    ps = (f'$w=New-Object -ComObject Word.Application; $d=$w.Documents.Open("{docx}"); '
          f'$d.SaveAs([ref]"{pdf}",[ref]17); $d.Close(); $w.Quit()')
    subprocess.run(["powershell", "-NoProfile", "-Command", ps], check=True)
    return pdf


# ---------------------------------------------------------------- 01 assembly drawings
cert = PdfReader(str(CERT)); w = PdfWriter()
for i in [52, 53] + list(range(56, 76)):
    w.add_page(slim(cert.pages[i]))
with open(OUT / "01_Assembly_Drawing_GLD_V2.pdf", "wb") as f:
    w.write(f)

# ---------------------------------------------------------------- 02 user manual
shutil.copy(MANUAL, OUT / "02_User_Manual_GLD_V2_Rev1.0.pdf")

# ---------------------------------------------------------------- 03 info sheet (EN)
d = new_doc()
p = d.add_paragraph(); r = p.add_run("Gas Leak Detector (GLD) V2"); r.bold = True; r.font.size = Pt(16); r.font.color.rgb = BLUE
p = d.add_paragraph(); r = p.add_run("Pre-application information — TÜV SÜD ATEX/IECEx discussion, 26 November 2026"); r.font.size = Pt(11)
p = d.add_paragraph(); r = p.add_run("Status of each item is stated as it stands; nothing in this sheet is a certified rating.")
r.italic = True; r.font.size = Pt(9)

h(d, "1. Product")
table(d, [
    ["Parameter", "Value"],
    ["Product", "Gas Leak Detector (GLD) V2 — fixed gas detection node, 8 metal-oxide gas sensors (MQ series) behind a stainless-steel wire mesh, internal fan, on-device AI classification"],
    ["Manufacturer / applicant", "PT Galaksi Megatama Indonesia"],
    ["Supply", "24 VDC, max. ≈ 8 W (≈ 0.33 A); AC/DC adaptor outside the equipment boundary"],
    ["Communication", "LoRa 920–923 MHz (wireless); RS-485 / Modbus RTU interface"],
    ["Dimensions / weight", "200 × 90 × 290 mm / 2.378 kg"],
    ["Enclosure", "Aluminium die-cast housing HIREP HRP-T1000-A (Zhengzhou HIREP). Supplier claim: Ex d IIC T6 Gb, IP66, −20…+55 °C, ≤ 3 W. Certificate number not yet obtained. Modified for GLD: front glass replaced by stainless wire mesh, internals replaced."],
    ["Cable entry", "M20 × 1.5; certified Ex d cable gland to be specified (prototype gland is general-purpose)"],
], [4.2, 12.8])
d.add_picture(str(PHOTO), width=Cm(15))
d.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
p = d.add_paragraph("Current production unit — four views (antenna on top of base).")
p.alignment = WD_ALIGN_PARAGRAPH.CENTER; p.runs[0].font.size = Pt(8.5)

h(d, "2. Target Ex marking (applicant's proposal)")
p = d.add_paragraph(); r = p.add_run("ATEX:  ⟨Ex⟩ II 2G  Ex db IIC T4 Gb    −20 °C ≤ Ta ≤ +60 °C"); r.bold = True; r.font.size = Pt(12)
p = d.add_paragraph(); r = p.add_run("IECEx:  Ex db IIC T4 Gb    −20 °C ≤ Ta ≤ +60 °C"); r.bold = True; r.font.size = Pt(12)
table(d, [
    ["Element", "Proposal", "Basis / status"],
    ["Group / category", "II, 2G (EPL Gb, Zone 1)", "Intended installation in Zone 1/2 refinery areas"],
    ["Type of protection", "Ex db (flameproof)", "Die-cast enclosure with mesh flame path; Ex i not feasible with ≈ 0.75 W sensor heaters"],
    ["Gas group", "IIC", "Hydrogen is in the detection scope"],
    ["Temperature class", "T4 (≤ 135 °C)", "Internal measurement (8 thermocouples, fan-stalled case) extrapolated to +60 °C: ≈ 114 °C internal hot spot, ≈ 79 °C enclosure surface. Preliminary, not witnessed."],
    ["Ambient range", "−20 °C … +60 °C", "Open point: housing supplier rating is +55 °C"],
    ["Dust", "Not proposed", "Gas atmospheres only"],
], [3.4, 4.0, 9.6])
p = d.add_paragraph("Open points for discussion: (a) stainless wire mesh as flame-path element — test approach; "
                    "(b) Ta +60 °C vs housing +55 °C; (c) whether the housing's existing certificate can be used as a basis "
                    "after the modification; (d) supplier T6 rating applies to ≤ 3 W content and is not claimed for GLD.")
p.runs[0].font.size = Pt(9)

h(d, "3. IP66")
table(d, [
    ["Item", "Status"],
    ["Target rating", "IP66 (IEC 60529)"],
    ["Test evidence", "None yet — not tested on GLD"],
    ["Housing", "Supplier claims IP66/IP67 for the original housing"],
    ["Design concern", "Gas inlet through the front wire mesh and internal fan create an open path to the sensor chamber; IP66 must be confirmed by test, possibly with the sensor chamber treated separately"],
    ["Cable gland", "IP66-rated Ex d gland M20 × 1.5 to be specified"],
], [4.2, 12.8])

h(d, "4. ISO 9001")
table(d, [
    ["Item", "Status"],
    ["ISO 9001 certificate (PT Galaksi Megatama Indonesia)", "In progress — certification audit planned October 2026; certificate number, scope and issuing body to be provided once issued"],
    ["Quality manual / procedure index", "To be provided"],
    ["Ex production quality (QAR / QAN)", "To be agreed with the certification body"],
], [6.0, 11.0])

h(d, "5. Documents in this package")
bullets(d, [
    "01 — Assembly and component drawings (drawing register, exploded views, assembly sequence, terminal, grounding, sensor dimensions)",
    "02 — User manual (Instruction Manual GLD V2, Rev 1.0, working draft)",
    "03 — This information sheet (target Ex marking, IP66, ISO 9001) with proposed nameplate",
])
info = OUT / "03_Target_Ex_Marking_IP66_ISO9001_GLD_V2.docx"
d.save(info)
info_pdf = to_pdf(info)
# append proposed nameplate pages from cert doc
r2 = PdfReader(str(info_pdf)); w = PdfWriter()
for pg in r2.pages: w.add_page(pg)
for i in [152, 153]: w.add_page(slim(cert.pages[i]))
with open(info_pdf, "wb") as f: w.write(f)

print("ok", sorted(x.name for x in OUT.iterdir()))
