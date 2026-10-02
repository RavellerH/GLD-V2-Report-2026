"""Versi Word (.docx) laporan penagihan Termin 1 (Paket LGU/02): cover + kontrol dokumen +
lembar pengesahan + kata pengantar + daftar isi + isi laporan (tanpa Referensi Dokumen).

Langkah: (1) python-docx membangun halaman depan & membersihkan isi laporan,
(2) Word COM menggabungkan keduanya (dijalankan dari PowerShell, lihat merge_word.ps1 yang ditulis skrip ini).
"""
import os
import subprocess

import docx
import pymupdf
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT, WD_TAB_LEADER
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, Mm

import build_cover_laporan_lgu as cv

ROOT = cv.ROOT
ASSET = cv.ASSET
TMP = os.path.join(ROOT, "Paket LGU", "02_Penagihan_Termin_1", "src")
FONT = "Arial"


def run(p, text, size=10.5, bold=False, italic=False, underline=False):
    r = p.add_run(text)
    r.font.name = FONT
    r._element.rPr.rFonts.set(qn("w:eastAsia"), FONT)
    r.font.size = Pt(size)
    r.bold = bold
    r.italic = italic
    r.underline = underline
    return r


def para(doc_or_cell, text="", size=10.5, bold=False, align=WD_ALIGN_PARAGRAPH.CENTER, after=6, before=0,
         underline=False):
    p = doc_or_cell.add_paragraph()
    p.alignment = align
    p.paragraph_format.space_after = Pt(after)
    p.paragraph_format.space_before = Pt(before)
    for i, line in enumerate(text.split("\n")):
        if i:
            p.add_run().add_break()
        run(p, line, size, bold, underline=underline)
    return p


def borders(tbl):
    b = OxmlElement("w:tblBorders")
    for e in ("top", "left", "bottom", "right", "insideH", "insideV"):
        x = OxmlElement(f"w:{e}")
        x.set(qn("w:val"), "single"); x.set(qn("w:sz"), "6"); x.set(qn("w:color"), "000000")
        b.append(x)
    tbl._tbl.tblPr.append(b)


def cell_text(cell, text, size=8.5, bold=False, align=WD_ALIGN_PARAGRAPH.CENTER):
    p = cell.paragraphs[0]
    p.alignment = align
    p.paragraph_format.space_after = Pt(0)
    for i, line in enumerate(text.split("\n")):
        if i:
            p.add_run().add_break()
        run(p, line, size, bold)


def front(d, entries, cover_png, out):
    doc = docx.Document()
    s = doc.sections[0]
    s.page_width, s.page_height = Mm(210), Mm(297)
    for m in ("top_margin", "bottom_margin", "left_margin", "right_margin"):
        setattr(s, m, 0)
    s.header_distance = s.footer_distance = 0
    p = doc.paragraphs[0] if doc.paragraphs else doc.add_paragraph()
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.space_before = Pt(0)
    p.add_run().add_picture(cover_png, width=Mm(209), height=Mm(295))

    s2 = doc.add_section(WD_SECTION.NEW_PAGE)
    s2.top_margin = s2.bottom_margin = Inches(1)
    s2.left_margin = s2.right_margin = Inches(0.9)
    s2.header_distance = s2.footer_distance = Inches(0.4)

    # --- kontrol dokumen
    judul1 = d["judul"].replace("\n", " ")
    sub1 = d["sub"].replace("\n", " ")
    t = doc.add_table(rows=6, cols=4)
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.autofit = False
    borders(t)
    widths = [Inches(1.4), Inches(3.3), Inches(0.75), Inches(1.1)]
    for row in t.rows:
        for c, w in zip(row.cells, widths):
            c.width = w
    c = t.cell(0, 0); c.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    c.paragraphs[0].add_run().add_picture(os.path.join(ASSET, "logo_lgu.png"), height=Inches(0.5))
    cell_text(t.cell(0, 1), judul1)
    m = t.cell(0, 2).merge(t.cell(0, 3)); m.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    m.paragraphs[0].add_run().add_picture(os.path.join(ASSET, "logo_pertamina.png"), height=Inches(0.36))
    for i, h in enumerate(["No. Kontrak:", "Dokumen", "Rev", "Jml. Hal"]):
        cell_text(t.cell(1, i), h, align=WD_ALIGN_PARAGRAPH.LEFT if i == 0 else WD_ALIGN_PARAGRAPH.CENTER)
    for i, v in enumerate(["", d["jenis"], d["rev"], str(d["_jml"])]):
        cell_text(t.cell(2, i), v)
    big = t.cell(3, 1)
    bp = big.paragraphs[0]; bp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    bp.paragraph_format.space_before = Pt(120)
    run(bp, judul1, 14, True)
    para(big, sub1, 10, after=90, before=10)
    para(big, "2026", 10, True, after=4)
    for i, h in enumerate(["Date", "Revision", "Prepared by", "Approved by"]):
        cell_text(t.cell(4, i), h, align=WD_ALIGN_PARAGRAPH.LEFT if i == 0 else WD_ALIGN_PARAGRAPH.CENTER)
    for i, v in enumerate([d["tgl"], "Rev " + d["rev"], "LGU", ""]):
        cell_text(t.cell(5, i), v, align=WD_ALIGN_PARAGRAPH.LEFT if i == 0 else WD_ALIGN_PARAGRAPH.CENTER)
    t.rows[3].height = Inches(4.6)

    # --- lembar pengesahan
    doc.add_page_break()
    para(doc, "LEMBAR PENGESAHAN", 16, True, after=24)
    para(doc, judul1 + "\n" + sub1, 12, True, after=24)
    para(doc, "Dikerjakan oleh,\nPT LAPI Ganesha Utama", after=16)
    para(doc, "Untuk\nPT Pertamina Patra Niaga", after=16)
    para(doc, cv.TTD["tempat"], after=10)
    sig = doc.add_table(rows=3, cols=2)
    sig.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell_text(sig.cell(0, 0), "Team Leader,", 10.5); cell_text(sig.cell(0, 1), "Direktur Utama,", 10.5)
    sig.rows[1].height = Inches(0.9)
    for i, n in enumerate([cv.TTD["team_leader"], cv.TTD["dirut"]]):
        p = sig.cell(2, i).paragraphs[0]; p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run(p, n, 10.5, True, underline=True)
    para(doc, cv.TTD["ppn_jabatan"], 10.5, True, before=36, after=70)
    para(doc, cv.TTD["ppn_nama"], 10.5, True, underline=True)

    # --- kata pengantar
    doc.add_page_break()
    para(doc, "KATA PENGANTAR", 16, True, after=20)
    for t_ in d["pengantar"]:
        p = para(doc, t_, 10.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY, after=10)
        p.paragraph_format.line_spacing = 1.4
    para(doc, cv.TTD["tempat"] + "\nPT LAPI Ganesha Utama", align=WD_ALIGN_PARAGRAPH.RIGHT, before=18, after=60)
    para(doc, cv.TTD["team_leader"] + "\nTeam Leader", align=WD_ALIGN_PARAGRAPH.RIGHT)

    # --- daftar isi
    doc.add_page_break()
    para(doc, "DAFTAR ISI", 16, True, after=20)
    for lvl, judul, hal in entries:
        p = doc.add_paragraph()
        pf = p.paragraph_format
        pf.space_after = Pt(6 if lvl == 1 else 3)
        pf.left_indent = Inches(0 if lvl == 1 else 0.3)
        pf.tab_stops.add_tab_stop(Inches(6.45), WD_TAB_ALIGNMENT.RIGHT, WD_TAB_LEADER.DOTS)
        run(p, judul, 10.5 if lvl == 1 else 10, lvl == 1)
        run(p, "\t" + str(hal), 10)
    para(doc, "Nomor halaman mengikuti nomor \"Halaman\" pada laporan.", 8.5, align=WD_ALIGN_PARAGRAPH.LEFT, before=12)
    doc.save(out)


def clean_body(src, out):
    d = docx.Document(src)
    body = d.element.body
    start = None
    for p in d.paragraphs:
        if p.style.name.startswith("Heading") and "Referensi Dokumen" in p.text:
            start = p._p
            break
    if start is not None:
        prev = start.getprevious()
        kill = []
        el = start
        while el is not None:
            if el.tag != qn("w:sectPr"):
                kill.append(el)
            el = el.getnext()
        # buang page break kosong tepat sebelum heading
        if prev is not None and prev.tag == qn("w:p") and not "".join(prev.itertext()).strip() \
                and prev.xpath(".//w:br[@w:type='page']"):
            kill.append(prev)
        for el in kill:
            body.remove(el)
    d.save(out)


PS = r'''
$ErrorActionPreference = "Stop"
$w = New-Object -ComObject Word.Application
$w.Visible = $false
$body = $w.Documents.Open("{body}")
$doc = $w.Documents.Open("{front}")
$end = $doc.Content
$end.Collapse(0)
$end.InsertBreak(2)
$n = $doc.Sections.Count
$last = $doc.Sections.Item($n)
foreach ($k in 1..3) {{
  $last.Headers.Item($k).LinkToPrevious = $false
  $last.Footers.Item($k).LinkToPrevious = $false
}}
$last.PageSetup.TopMargin = $body.Sections.Item(1).PageSetup.TopMargin
$last.PageSetup.BottomMargin = $body.Sections.Item(1).PageSetup.BottomMargin
$last.PageSetup.LeftMargin = $body.Sections.Item(1).PageSetup.LeftMargin
$last.PageSetup.RightMargin = $body.Sections.Item(1).PageSetup.RightMargin
$last.PageSetup.HeaderDistance = $body.Sections.Item(1).PageSetup.HeaderDistance
$last.PageSetup.FooterDistance = $body.Sections.Item(1).PageSetup.FooterDistance
$last.Headers.Item(1).Range.FormattedText = $body.Sections.Item(1).Headers.Item(1).Range.FormattedText
$last.Footers.Item(1).Range.FormattedText = $body.Sections.Item(1).Footers.Item(1).Range.FormattedText
$last.Footers.Item(1).PageNumbers.RestartNumberingAtSection = $true
$last.Footers.Item(1).PageNumbers.StartingNumber = 1
$body.Close(0)
$r = $last.Range
$r.Collapse(1)
$r.InsertFile("{body}")
foreach ($i in 1..($n-1)) {{
  $s = $doc.Sections.Item($i)
  foreach ($k in 1..3) {{ $s.Headers.Item($k).Range.Text = ""; $s.Footers.Item($k).Range.Text = "" }}
}}
$doc.Fields.Update() | Out-Null
$doc.SaveAs([ref]"{out}", [ref]16)
$doc.SaveAs([ref]"{pdf}", [ref]17)
$doc.Close(0)
$w.Quit()
'''


def main():
    os.makedirs(TMP, exist_ok=True)
    bodies = {
        "01": os.path.join(ROOT, "Paket Pertamina", "04_Laporan_Termin_1",
                           "Laporan_Pemenuhan_Deliverable_Termin_1_FieldTesting_GLD_Rev02.docx"),
        "03": os.path.join(TMP, "Laporan_Termin_1_Sertifikasi_LGU.docx"),
    }
    for d in cv.DOCS:
        key = os.path.basename(d["out"])[:2]
        final_pdf = os.path.join(ROOT, d["out"])
        fp = pymupdf.open(final_pdf)
        d["_jml"] = fp.page_count
        cover_png = os.path.join(TMP, f"cover_{key}.png")
        fp[0].get_pixmap(dpi=200).save(cover_png)
        src = pymupdf.open(os.path.join(ROOT, d["src"]))
        if "Referensi Dokumen" in src[-1].get_text():
            src.delete_page(src.page_count - 1)
        entries = [e for e in cv.headings(src) if "Referensi Dokumen" not in e[1]]
        front_docx = os.path.join(TMP, f"front_{key}.docx")
        body_docx = os.path.join(TMP, f"body_{key}.docx")
        front(d, entries, cover_png, front_docx)
        clean_body(bodies[key], body_docx)
        out_docx = final_pdf[:-4] + ".docx"
        check_pdf = os.path.join(TMP, f"word_check_{key}.pdf")
        ps = PS.format(body=body_docx, front=front_docx, out=out_docx, pdf=check_pdf)
        ps_path = os.path.join(TMP, f"merge_{key}.ps1")
        open(ps_path, "w", encoding="utf-8-sig").write(ps)
        subprocess.run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", ps_path], check=True)
        print(out_docx, pymupdf.open(check_pdf).page_count, "hlm (cek render Word)")


if __name__ == "__main__":
    main()
