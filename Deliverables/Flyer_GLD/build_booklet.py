"""Render flyer A4 + booklet 4 halaman (A4) lalu impose ke 2 lembar A3 landscape untuk cetak bolak-balik dilipat.
Lembar 1 (sisi luar): hal 4 | hal 1.  Lembar 2 (sisi dalam): hal 2 | hal 3.
    python build_booklet.py
"""
import subprocess
from pathlib import Path

import pymupdf

D = Path(__file__).resolve().parent
CHROME = r"C:/Program Files/Google/Chrome/Application/chrome.exe"


def pdf(html, out):
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                    f"--print-to-pdf={D / out}", (D / html).as_uri()], check=True, capture_output=True)


pdf("Flyer_GLD_A4.html", "Flyer_GLD_A4.pdf")
pdf("Booklet_GLD_4hal.html", "Booklet_GLD_A4_4hal.pdf")
pdf("XBanner_GLD_60x160.html", "XBanner_GLD_60x160cm.pdf")

src = pymupdf.open(D / "Booklet_GLD_A4_4hal.pdf")
assert len(src) == 4, len(src)
a3 = pymupdf.open()
W, H = pymupdf.paper_size("a3-l")
for left, right in ((3, 0), (1, 2)):
    pg = a3.new_page(width=W, height=H)
    pg.show_pdf_page(pymupdf.Rect(0, 0, W / 2, H), src, left)
    pg.show_pdf_page(pymupdf.Rect(W / 2, 0, W, H), src, right)
a3.save(D / "Booklet_GLD_A3_cetak_lipat.pdf", deflate=True, garbage=3)
print("ok")
