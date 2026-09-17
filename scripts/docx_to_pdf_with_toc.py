# -*- coding: utf-8 -*-
"""Konversi DOCX -> PDF lewat LibreOffice (UNO) sambil MEMPERBARUI field.

Alasan skrip ini ada: `soffice --convert-to pdf` tidak memperbarui field TOC
Word, sehingga halaman daftar isi di PDF hanya berisi teks fallback
("Right-click and choose Update Field..."). Skrip ini membuka dokumen lewat
UNO, me-refresh field + indeks (TOC, PAGE, NUMPAGES), lalu mengekspor PDF.

Pakai:
    python3 scripts/docx_to_pdf_with_toc.py <input.docx> [output.pdf]

Catatan: butuh `libreoffice-writer` + `python3-uno`. Di Linux, font Calibri/
Cambria disubstitusi Carlito/Caladea (metric-compatible) — pasang
`fonts-crosextra-carlito` dan `fonts-crosextra-caladea` agar tata letaknya
sama dengan hasil Word.
"""
import os
import subprocess
import sys
import time
import uno
from com.sun.star.beans import PropertyValue


def _url(path):
    return uno.systemPathToFileUrl(os.path.abspath(path))


def _prop(name, value):
    p = PropertyValue()
    p.Name = name
    p.Value = value
    return p


def connect(port=2002, tries=30):
    ctx_local = uno.getComponentContext()
    resolver = ctx_local.ServiceManager.createInstanceWithContext(
        "com.sun.star.bridge.UnoUrlResolver", ctx_local)
    url = f"uno:socket,host=127.0.0.1,port={port};urp;StarOffice.ComponentContext"
    for _ in range(tries):
        try:
            return resolver.resolve(url)
        except Exception:
            time.sleep(1)
    raise RuntimeError("tidak bisa terhubung ke soffice via UNO")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 1
    src = sys.argv[1]
    dst = sys.argv[2] if len(sys.argv) > 2 else os.path.splitext(src)[0] + ".pdf"

    proc = subprocess.Popen([
        "soffice", "--headless", "--norestore", "--invisible",
        "--accept=socket,host=127.0.0.1,port=2002;urp;",
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        ctx = connect()
        desktop = ctx.ServiceManager.createInstanceWithContext(
            "com.sun.star.frame.Desktop", ctx)
        doc = desktop.loadComponentFromURL(
            _url(src), "_blank", 0, (_prop("Hidden", True), _prop("UpdateDocMode", 3)))

        # perbarui isi field & indeks: TOC dulu, lalu PAGE/NUMPAGES
        for _ in range(2):
            if hasattr(doc, "refresh"):
                doc.refresh()
            if hasattr(doc, "getTextFields"):
                doc.getTextFields().refresh()
            if hasattr(doc, "getDocumentIndexes"):
                idx = doc.getDocumentIndexes()
                for i in range(idx.getCount()):
                    idx.getByIndex(i).update()

        doc.storeToURL(_url(dst), (_prop("FilterName", "writer_pdf_Export"),))
        doc.close(False)
        print("written", dst)
        return 0
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=20)
        except subprocess.TimeoutExpired:
            proc.kill()


if __name__ == "__main__":
    sys.exit(main())
