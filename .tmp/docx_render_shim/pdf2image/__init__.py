"""Minimal local compatibility layer for the document skill renderer.

The Windows workspace already provides PyMuPDF but not pdf2image/Poppler.
This module implements only the two functions used by render_docx.py.
"""

from pathlib import Path

import fitz


def pdfinfo_from_path(pdf_path):
    with fitz.open(pdf_path) as document:
        if document.page_count == 0:
            return {}
        rect = document[0].rect
        return {"Page size": f"{rect.width:g} x {rect.height:g} pts"}


def convert_from_path(
    pdf_path,
    dpi=150,
    fmt="png",
    thread_count=1,
    output_folder=None,
    paths_only=True,
    output_file="page",
    **_kwargs,
):
    if fmt.lower() != "png":
        raise ValueError("This compatibility layer supports PNG output only")
    out_dir = Path(output_folder or Path(pdf_path).parent)
    out_dir.mkdir(parents=True, exist_ok=True)
    paths = []
    matrix = fitz.Matrix(float(dpi) / 72.0, float(dpi) / 72.0)
    with fitz.open(pdf_path) as document:
        for page_number, page in enumerate(document, start=1):
            target = out_dir / f"{output_file}0000-{page_number:02d}.png"
            pixmap = page.get_pixmap(matrix=matrix, alpha=False)
            pixmap.save(str(target))
            paths.append(str(target))
    return paths
