"""Render flyer, X-banner, dan booklet 4 halaman (GLD & OGI, ID & EN) lalu impose booklet ke 2 lembar A3
landscape untuk cetak bolak-balik dilipat. Lembar 1 (luar): hal 4 | hal 1. Lembar 2 (dalam): hal 2 | hal 3.
    python make_en.py && python build_booklet.py
"""
import subprocess
from pathlib import Path

import pymupdf

D = Path(__file__).resolve().parent
CHROME = r"C:/Program Files/Google/Chrome/Application/chrome.exe"


def pdf(html, out):
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                    f"--print-to-pdf={D / out}", (D / html).as_uri()], check=True, capture_output=True)


def impose(a4, a3):
    src = pymupdf.open(D / a4)
    assert len(src) == 4, (a4, len(src))
    doc = pymupdf.open()
    W, H = pymupdf.paper_size("a3-l")
    for left, right in ((3, 0), (1, 2)):
        pg = doc.new_page(width=W, height=H)
        pg.show_pdf_page(pymupdf.Rect(0, 0, W / 2, H), src, left)
        pg.show_pdf_page(pymupdf.Rect(W / 2, 0, W, H), src, right)
    doc.save(D / a3, deflate=True, garbage=3)


pdf("Flyer_GLD_A4.html", "Flyer_GLD_A4.pdf")
pdf("XBanner_GLD_60x160.html", "XBanner_GLD_60x160cm.pdf")
pdf("XBanner_GLD_60x160_EN.html", "XBanner_GLD_EN_60x160cm.pdf")
pdf("XBanner_OGI_60x160.html", "XBanner_OGI_60x160cm.pdf")
pdf("XBanner_OGI_60x160_EN.html", "XBanner_OGI_EN_60x160cm.pdf")
for name in ("GLD", "GLD_EN", "OGI", "OGI_EN"):
    src = f"Booklet_{name.split('_')[0]}_4hal{'_EN' if name.endswith('_EN') else ''}.html"
    pdf(src, f"Booklet_{name}_A4_4hal.pdf")
    impose(f"Booklet_{name}_A4_4hal.pdf", f"Booklet_{name}_A3_cetak_lipat.pdf")
print("ok")
