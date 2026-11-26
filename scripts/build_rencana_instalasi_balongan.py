# -*- coding: utf-8 -*-
"""Rencana Instalasi GLD RU VI Balongan (konfigurasi 26 Nov 2026).

Output: Deliverables/Rencana_Instalasi_GLD_RU-VI_Balongan.docx (+ PDF via Word COM)
"""
import os

import docx
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
ASSET = os.path.join(HERE, "assets", "lgu_cover")
RB = os.path.join(HERE, "assets", "rab_balongan")
OUT = os.path.join(ROOT, "Deliverables", "Rencana_Instalasi_GLD_RU-VI_Balongan.docx")
DIAG = os.path.join(RB, "diagram_daya_data_balongan.png")
MAP = os.path.join(RB, "peta_lokasi_balongan_26nov.png")
D3A = os.path.join(RB, "diagram_3d_balongan_overview.png")
D3B = os.path.join(RB, "diagram_3d_balongan_whb.png")
D3C = os.path.join(RB, "diagram_3d_balongan_gld.png")
D3D = os.path.join(RB, "diagram_3d_balongan_gw.png")

DOC_NO = "LGU/GLD/RI-BLG/2026-001"
REV = "0.1 (Draf)"
TANGGAL = "26 November 2026"
BLUE, INK, GRAY = "2B5FCB", "262321", "6B6B6B"


# ------------------------------------------------------------------ diagram
def build_diagram():
    fig, ax = plt.subplots(figsize=(11, 5.6))
    ax.set_xlim(0, 120); ax.set_ylim(0, 58); ax.axis("off")

    def box(x, y, w, h, title, sub, fc="#FFFFFF", ec="#262321"):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.4", fc=fc, ec=ec, lw=1.3))
        ax.text(x + w / 2, y + h * 0.64, title, ha="center", va="center", fontsize=9.5, fontweight="bold", color="#262321")
        ax.text(x + w / 2, y + h * 0.28, sub, ha="center", va="center", fontsize=7.4, color="#444444")

    def zone(x, y, w, h, label, fc):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.2", fc=fc, ec="#9AA5B8", lw=0.8, ls="--"))
        ax.text(x + 0.8, y + h - 1.6, label, fontsize=8, fontweight="bold", color="#4A5568", va="top")

    def wire(xy, xy2, color, ls="-", lw=1.8, text=None, toff=(0, 1.1)):
        ax.annotate("", xy=xy2, xytext=xy, arrowprops=dict(arrowstyle="-|>", color=color, lw=lw, ls=ls, shrinkA=0, shrinkB=0))
        if text:
            ax.text((xy[0] + xy2[0]) / 2 + toff[0], (xy[1] + xy2[1]) / 2 + toff[1], text, fontsize=7, color=color,
                    ha="center", va="bottom")

    zone(1, 30, 22, 27, "Panel RU VI (safe area)", "#EEF3FB")
    zone(25, 3, 63, 54, "Area proses WHB (risiko rendah, survei 17 Nov)", "#FFF8EC")
    zone(91, 3, 28, 54, "Gedung kantor", "#EEF6EE")

    box(3, 43, 18, 7, "PSU 24 VDC", "DLP240-24-1 (RU VI)")
    box(3, 32, 18, 7, "PSU 5 VDC + fuse", "HDR-15-5 · fuse/cabang")
    box(28, 34, 14, 9, "JB Ex d", "HLBH31 · 5 entry M20")
    box(50, 43, 15, 7, "GLD-01", "24 VDC · stanchion 1 m")
    box(50, 27, 15, 7, "GLD-02", "24 VDC · stanchion 1 m")
    box(70, 35, 15, 7, "CH-01", "5 VDC · bawah struktur")
    box(70, 8, 15, 7, "CH-02", "panel surya · stanchion")
    box(94, 36, 23, 8, "Gateway GW-01", "tepi atap · siku besi")
    box(94, 21, 14, 7, "Adaptor 5 VDC", "stopkontak/UPS")
    box(94, 6, 23, 7, "PC server + router", "dalam kantor")

    red, blu, grn = "#C0392B", "#2B5FCB", "#2E7D32"
    wire((21.4, 46.5), (27.6, 40.5), red, text="24 VDC", toff=(1.5, 1.2))
    wire((21.4, 35.5), (27.6, 37), red, text="5 VDC", toff=(1.5, -3.2))
    wire((42.4, 40.5), (49.6, 46.5), red)
    wire((42.4, 37.5), (49.6, 30.5), red)
    ax.plot([35, 35, 73], [33.6, 22, 22], color=red, lw=1.8)
    wire((73, 22), (73, 34.6), red)
    ax.text(54, 22.6, "armoured 2C 1,5 mm² (5 VDC ke CH-01)", fontsize=7, color=red, ha="center")
    wire((65.4, 46.5), (69.6, 40.5), blu, ls="--", lw=1.4)
    wire((65.4, 30.5), (69.6, 37), blu, ls="--", lw=1.4)
    ax.text(66.2, 43.8, "LoRa", fontsize=7, color=blu)
    wire((81, 34.6), (81, 15.4), blu, ls="--", lw=1.4)
    ax.text(82, 25, "LoRa ±18 m", fontsize=7, color=blu, rotation=90, va="center")
    wire((85.4, 12), (93.6, 38), blu, ls="--", lw=1.4)
    ax.text(86.5, 31, "LoRa ±80 m", fontsize=7, color=blu, rotation=72, va="center")
    wire((101, 28.4), (101, 35.6), red)
    ax.text(102, 31, "NYY 5 VDC", fontsize=7, color=red)
    wire((113, 35.6), (113, 13.4), grn, ls=":", lw=1.4)
    ax.text(112.3, 16, "Wi-Fi / LAN*", fontsize=7, color=grn, ha="right")

    ax.plot([2, 6], [0.9, 0.9], color=red, lw=1.8); ax.text(6.6, 0.9, "Daya", fontsize=7.5, va="center")
    ax.plot([14, 18], [0.9, 0.9], color=blu, lw=1.4, ls="--"); ax.text(18.6, 0.9, "Data LoRa", fontsize=7.5, va="center")
    ax.plot([30, 34], [0.9, 0.9], color=grn, lw=1.4, ls=":"); ax.text(34.6, 0.9, "Data lokal (*perlu konfirmasi)", fontsize=7.5, va="center")
    fig.tight_layout()
    fig.savefig(DIAG, dpi=220)
    plt.close(fig)


# ------------------------------------------------------------------ 3D di atas peta
PX_PER_M = 6.8  # skala bar "10 m" = 68 px pada citra peta
# posisi (piksel citra peta) & tinggi (m) -- estimasi, verifikasi di lapangan
PTS = {
    "GLD-01": ((1262, 212), 1.0), "GLD-02": ((1303, 268), 1.0), "CH-01": ((1335, 214), 3.0),
    "CH-02": ((1332, 330), 6.0), "JB": ((1290, 240), 0.8), "GW-01": ((878, 716), 9.5),
}
ROOF = 8.0  # asumsi tinggi atap kantor


def build_3d(path, box, title, show, up=1, zs=2.0, shear=0.45, squash=0.55, labels=None):
    """Tampilan oblique 3D: citra peta di-warp jadi bidang tanah, objek digambar dgn tinggi (m) dibesarkan zs kali."""
    from PIL import Image
    from matplotlib.lines import Line2D
    x0, y0, x1, y1 = box
    im = Image.open(MAP).convert("RGB").crop(box)
    W, H = im.size
    im = im.resize((W * up, H * up), Image.LANCZOS)
    W, H = im.size
    ow, oh = int(W + shear * H), int(squash * H)
    # output (U,V) -> input (px,py): py = V/squash ; px = U - shear*py
    warped = im.transform((ow, oh), Image.AFFINE, (1, -shear / squash, 0, 0, 1 / squash, 0),
                          resample=Image.BICUBIC, fillcolor=(255, 255, 255))
    ppm = PX_PER_M * up
    ztop = 12 * ppm * zs * squash

    def proj(k, z=None):
        (px, py), h = PTS[k]
        px, py = (px - x0) * up, (py - y0) * up
        z = h if z is None else z
        return px + shear * py, squash * py - z * ppm * zs * squash

    fig, ax = plt.subplots(figsize=(11, 11 * (oh + ztop) / ow))
    ax.imshow(warped, extent=(0, ow, oh, 0))
    ax.set_xlim(0, ow); ax.set_ylim(oh, -ztop * 0.6); ax.axis("off")
    red, blu, org, pur, cya = "#E03A2F", "#2B6BFF", "#FF9F1C", "#8E5CF0", "#00BCD4"
    labels = labels or {}

    def ground(k):
        return proj(k, 0)

    def seg(a_, b_, col, ls="-", lw=2.4, z=5):
        ax.plot([a_[0], b_[0]], [a_[1], b_[1]], color=col, ls=ls, lw=lw, zorder=z, solid_capstyle="round")

    def pole(k, col="#F2F2F2", lw=4):
        g, t = ground(k), proj(k)
        ax.plot([g[0], t[0]], [g[1], t[1]], color="#222222", lw=lw + 2, zorder=6)
        ax.plot([g[0], t[0]], [g[1], t[1]], color=col, lw=lw, zorder=7)

    def dev(k, col, marker="s", ms=13):
        t = proj(k)
        ax.plot(*t, marker=marker, ms=ms, mfc=col, mec="#111111", mew=1.4, zorder=12)

    def lab(k, text, fc="#262321"):
        t = proj(k)
        dx, dy = labels.get(k, (12, -18))
        ax.annotate(text, t, xytext=(t[0] + dx * up, t[1] + dy * up), fontsize=8.5, fontweight="bold",
                    color="white", zorder=20, arrowprops=dict(arrowstyle="-", color=fc, lw=1),
                    bbox=dict(boxstyle="round,pad=0.3", fc=fc, ec="none", alpha=0.92))

    # kabel daya di tanah
    if "JB" in show:
        jb = ground("JB")
        for k in ("GLD-01", "GLD-02", "CH-01"):
            seg(jb, ground(k), red)
        seg(ground("CH-01"), proj("CH-01"), red, lw=2)
        feed = (jb[0] - 7 * ppm, jb[1] + 4 * ppm * squash)
        seg(jb, feed, red, ls="--")
        ax.annotate("ke panel RU VI\n(24 & 5 VDC, lokasi TBD)", feed, xytext=(feed[0] - 40 * up, feed[1] + 18 * up),
                    fontsize=7.5, color="white", zorder=20, arrowprops=dict(arrowstyle="-", color=red),
                    bbox=dict(boxstyle="round,pad=0.25", fc=red, ec="none", alpha=0.92))
    # tiang & perangkat
    for k in ("GLD-01", "GLD-02"):
        if k in show:
            pole(k); dev(k, org); lab(k, k + "  24 VDC · tiang 1 m")
    if "CH-01" in show:
        pole("CH-01"); dev("CH-01", pur); lab("CH-01", "CH-01  5 VDC · bawah struktur ±3 m")
    if "CH-02" in show:
        pole("CH-02"); dev("CH-02", pur)
        t = proj("CH-02")
        pw, phh = 2.2 * ppm, 1.1 * ppm * zs * squash
        ax.add_patch(plt.Polygon([(t[0] - pw / 2, t[1] - 0.3 * phh), (t[0] + pw / 2, t[1] - 0.3 * phh),
                                  (t[0] + pw / 2 + 0.3 * pw, t[1] - 1.3 * phh), (t[0] - pw / 2 + 0.3 * pw, t[1] - 1.3 * phh)],
                                 closed=True, fc="#1E3A8A", ec="#BFD3FF", lw=1, zorder=11))
        lab("CH-02", "CH-02  panel surya · tiang 6 m")
    if "JB" in show:
        pole("JB", col="#9E9E9E", lw=3); dev("JB", "#BDBDBD", "D", 11)
        lab("JB", "JB Ex d (HLBH31)", fc="#555555")
    if "GW-01" in show:
        g = ground("GW-01"); roof = proj("GW-01", ROOF); t = proj("GW-01")
        ax.plot([g[0], roof[0]], [g[1], roof[1]], color="white", lw=1.2, ls=":", zorder=6)
        ax.plot([roof[0], t[0]], [roof[1], t[1]], color="#222222", lw=6, zorder=6)
        ax.plot([roof[0], t[0]], [roof[1], t[1]], color="#B0BEC5", lw=4, zorder=7)
        dev("GW-01", cya, "^", 15)
        off = 1.5 * ppm
        seg((g[0] + off, g[1]), (roof[0] + off, roof[1]), red, ls="--", lw=1.8)
        ax.annotate("5 VDC dari adaptor\ndi dalam kantor", (roof[0] + off, (g[1] + roof[1]) / 2),
                    xytext=(roof[0] + off + 25 * up, (g[1] + roof[1]) / 2 + 10 * up), fontsize=7.5, color="white", zorder=20,
                    arrowprops=dict(arrowstyle="-", color=red), bbox=dict(boxstyle="round,pad=0.25", fc=red, ec="none", alpha=0.92))
        lab("GW-01", "GW-01  tepi atap kantor (±8 m) · siku besi")
    # LoRa
    for a_, b_, txt in (("GLD-01", "CH-01", None), ("GLD-02", "CH-01", None), ("CH-01", "CH-02", "±18 m"),
                        ("CH-02", "GW-01", "±80 m")):
        if a_ in show and b_ in show:
            A, B = proj(a_), proj(b_)
            seg(A, B, blu, ls=(0, (5, 3)), lw=2.2, z=9)
            if txt:
                ax.text((A[0] + B[0]) / 2 + 8 * up, (A[1] + B[1]) / 2, "LoRa " + txt, fontsize=8, color="white",
                        fontweight="bold", zorder=20, bbox=dict(boxstyle="round,pad=0.2", fc=blu, ec="none", alpha=0.92))
    ax.legend(handles=[Line2D([], [], color=red, lw=2.4, label="Kabel daya"),
                       Line2D([], [], color=blu, lw=2.2, ls=(0, (5, 3)), label="Link LoRa"),
                       Line2D([], [], color=org, marker="s", ls="", ms=10, mec="k", label="GLD"),
                       Line2D([], [], color=pur, marker="s", ls="", ms=10, mec="k", label="Cluster Head"),
                       Line2D([], [], color=cya, marker="^", ls="", ms=10, mec="k", label="Gateway"),
                       Line2D([], [], color="#BDBDBD", marker="D", ls="", ms=9, mec="k", label="Junction box")],
              loc="upper right", fontsize=8.5, framealpha=0.95)
    ax.set_title(title, fontsize=11.5, fontweight="bold", color="#262321", loc="left")
    ax.text(0, oh + 4, f"Tinggi dibesarkan {zs:g}× terhadap skala horizontal. Posisi & tinggi = estimasi dari citra peta.",
            fontsize=8, color="#555555", va="top")
    fig.savefig(path, dpi=200, bbox_inches="tight")
    plt.close(fig)


def label_render(view, pas, out, crop, title, items, legend_loc="lower left", legend=True):
    """Beri label, tag & garis dimensi pada render Blender (scripts/render_3d_balongan_blender.py)."""
    import json
    from PIL import Image
    from matplotlib.lines import Line2D
    with open(os.path.join(RB, f"render3d_pts_{pas}.json")) as f:
        pos = json.load(f)[view]
    im = Image.open(os.path.join(RB, f"render3d_{view}.png")).convert("RGB").crop(crop)
    w, h = im.size

    def xy(k):
        return pos[k][0] - crop[0], pos[k][1] - crop[1]

    fig, ax = plt.subplots(figsize=(11, 11 * h / w))
    ax.imshow(im); ax.axis("off"); ax.set_xlim(0, w); ax.set_ylim(h, 0)
    for it in items:
        kind = it[0]
        if kind == "lab":
            _, k, text, dx, dy, col = it
            x, y = xy(k)
            tx = min(max(x + dx, 300), w - 300)
            ty = min(max(y + dy, 30), h - 30)
            ax.annotate(text, (x, y), xytext=(tx, ty), fontsize=8.6, fontweight="bold", color="white",
                        ha="center", va="center", zorder=10,
                        arrowprops=dict(arrowstyle="-|>", color=col, lw=1.5, shrinkA=0, shrinkB=2),
                        bbox=dict(boxstyle="round,pad=0.35", fc=col, ec="white", lw=0.8, alpha=0.95))
        elif kind == "tag":
            _, k, text, col = it[:4]
            off = it[4] if len(it) > 4 else (0, 0)
            x, y = xy(k)
            ax.text(x + off[0], y + off[1], text, fontsize=8, fontweight="bold", color=col, ha="center", va="center",
                    zorder=11, bbox=dict(boxstyle="round,pad=0.25", fc="white", ec=col, lw=1.2, alpha=0.95))
        elif kind == "dim":
            _, a, b, text, off = it
            (x1, y1), (x2, y2) = xy(a), xy(b)
            x1o, x2o = x1 + off, x2 + off
            ax.plot([x1, x1o], [y1, y1], color="#111111", lw=0.8, zorder=9)
            ax.plot([x2, x2o], [y2, y2], color="#111111", lw=0.8, zorder=9)
            ax.annotate("", (x2o, y2), xytext=(x1o, y1), zorder=9,
                        arrowprops=dict(arrowstyle="<|-|>", color="#111111", lw=1.3, shrinkA=0, shrinkB=0))
            ax.text((x1o + x2o) / 2 + (14 if off >= 0 else -14), (y1 + y2) / 2, text, fontsize=8.6, fontweight="bold",
                    color="#111111", ha="left" if off >= 0 else "right", va="center", zorder=11,
                    bbox=dict(boxstyle="round,pad=0.2", fc="#FFF6C9", ec="#111111", lw=0.8))
    if legend:
        ax.legend(handles=[Line2D([], [], color="#1E9BFF", lw=3, ls="--", label="Link LoRa"),
                           Line2D([], [], color="#FF8A00", marker="s", ls="", ms=10, mec="k", label="GLD"),
                           Line2D([], [], color="#9B4DFF", marker="s", ls="", ms=10, mec="k", label="Cluster Head"),
                           Line2D([], [], color="#19D3B0", marker="s", ls="", ms=10, mec="k", label="Gateway"),
                           Line2D([], [], color="#6E737A", marker="s", ls="", ms=10, mec="k", label="Struktur baja")],
                  loc=legend_loc, fontsize=8.2, framealpha=0.92)
    ax.set_title(title, fontsize=11.5, fontweight="bold", color="#262321", loc="left")
    fig.savefig(out, dpi=170, bbox_inches="tight")
    plt.close(fig)


# ------------------------------------------------------------------ docx helpers
def borders(tbl, color="808080"):
    tblPr = tbl._tbl.tblPr
    b = OxmlElement("w:tblBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        e = OxmlElement(f"w:{edge}")
        e.set(qn("w:val"), "single"); e.set(qn("w:sz"), "4"); e.set(qn("w:color"), color)
        b.append(e)
    tblPr.append(b)


def shade(cell, hexcol):
    tcPr = cell._tc.get_or_add_tcPr()
    s = OxmlElement("w:shd"); s.set(qn("w:val"), "clear"); s.set(qn("w:color"), "auto"); s.set(qn("w:fill"), hexcol)
    tcPr.append(s)


def cell_text(cell, text, bold=False, size=8.8, color=None):
    p = cell.paragraphs[0]
    p.paragraph_format.space_after = Pt(0)
    r = p.add_run(text); r.bold = bold; r.font.size = Pt(size)
    if color:
        r.font.color.rgb = RGBColor.from_string(color)


def fixed(tbl, widths):
    tblPr = tbl._tbl.tblPr
    lay = OxmlElement("w:tblLayout"); lay.set(qn("w:type"), "fixed"); tblPr.append(lay)
    for gc, w in zip(tbl._tbl.tblGrid.findall(qn("w:gridCol")), widths):
        gc.set(qn("w:w"), str(int(w / 635)))
    trPr = tbl.rows[0]._tr.get_or_add_trPr()
    h = OxmlElement("w:tblHeader"); h.set(qn("w:val"), "true"); trPr.append(h)
    for row in tbl.rows:
        cs = OxmlElement("w:cantSplit"); cs.set(qn("w:val"), "true"); row._tr.get_or_add_trPr().append(cs)


def table(d, headers, rows, widths, size=8.8):
    widths = [Inches(w) for w in widths]
    tbl = d.add_table(rows=1, cols=len(headers))
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    borders(tbl)
    for c, h in zip(tbl.rows[0].cells, headers):
        shade(c, INK); cell_text(c, h, bold=True, size=8.6, color="FFFFFF")
    for i, row in enumerate(rows):
        cells = tbl.add_row().cells
        for j, v in enumerate(row):
            if i % 2:
                shade(cells[j], "F3F5F9")
            cell_text(cells[j], str(v), size=size, bold=(j == 0))
    for row in tbl.rows:
        for c, w in zip(row.cells, widths):
            c.width = w
    fixed(tbl, widths)
    d.add_paragraph().paragraph_format.space_after = Pt(2)


def para(d, text, bold=False, size=10, after=5, italic=False):
    p = d.add_paragraph(); p.paragraph_format.space_after = Pt(after)
    r = p.add_run(text); r.bold = bold; r.italic = italic; r.font.size = Pt(size)
    return p


def bullet(d, text):
    p = d.add_paragraph(style="List Bullet"); p.paragraph_format.space_after = Pt(2)
    p.add_run(text).font.size = Pt(9.8)


def h(d, text, lvl=1):
    p = d.add_heading(text, level=lvl)
    for r in p.runs:
        r.font.color.rgb = RGBColor.from_string(BLUE if lvl == 1 else INK)
        r.font.name = "Calibri"
        r.font.size = Pt(13 if lvl == 1 else 11)


def note(d, text, fill="FFF4E5", line="E0A03C"):
    t = d.add_table(rows=1, cols=1); t.alignment = WD_TABLE_ALIGNMENT.CENTER
    borders(t, line)
    c = t.rows[0].cells[0]; shade(c, fill); cell_text(c, text, size=9.2)
    d.add_paragraph().paragraph_format.space_after = Pt(2)


def figure(d, path, caption, width):
    p = d.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(2); p.paragraph_format.keep_with_next = True
    p.add_run().add_picture(path, width=width)
    c = d.add_paragraph(); c.alignment = WD_ALIGN_PARAGRAPH.CENTER; c.paragraph_format.space_after = Pt(8)
    r = c.add_run(caption); r.italic = True; r.font.size = Pt(8.5)


def page_field(p):
    for t in ("begin", None, "end"):
        r = p.add_run()
        if t is None:
            it = OxmlElement("w:instrText"); it.set(qn("xml:space"), "preserve"); it.text = "PAGE"; r._r.append(it)
        else:
            fc = OxmlElement("w:fldChar"); fc.set(qn("w:fldCharType"), t); r._r.append(fc)
        r.font.size = Pt(8)


# ------------------------------------------------------------------ document
def build():
    build_diagram()
    O, C, B_, P_, G_ = "#00977A", "#D50000", "#454A52", "#7B2FE0", "#F07800"
    label_render("overview", "wide", D3A, (0, 330, 2200, 1400), "A. Gambaran lokasi — klaster WHB ke Gateway di atap kantor", [
        ("lab", "GW-01", "GW-01 Gateway · tepi atap kantor", 120, -230, O),
        ("lab", "BLDG", "Gedung kantor: adaptor 5 VDC, router & PC server di dalam", 330, 170, B_),
        ("tag", "LORA:CH-02>GW-01", "LoRa CH-02 → GW-01 ± 80 m", "#0077E6", (60, 40)),
        ("lab", "STRUCT", "Klaster WHB: GLD-01, GLD-02, CH-01, CH-02", -300, 230, G_),
        ("dim", "ROOF:base", "ROOF:top", "± 8 m", -60),
        ("lab", "COL1", "Bangunan, kolom & unit proses dari citra peta (bentuk/tinggi ilustratif)", 120, -120, "#6E737A"),
    ])
    label_render("whb", "wide", D3B, (0, 120, 2200, 1250), "B. Klaster WHB — posisi GLD, Cluster Head, dan relay LoRa", [
        ("lab", "GLD-01", "GLD-01 · 24 VDC, di bawah struktur", -380, -150, G_),
        ("lab", "GLD-02", "GLD-02 · 24 VDC, di bawah struktur", 120, 300, G_),
        ("lab", "CH-01", "CH-01 · 5 VDC, di bawah struktur", 300, 90, P_),
        ("lab", "CH-02:pv", "CH-02 · panel surya", -420, -60, P_),
        ("lab", "STRUCT", "Struktur WHB (kolom beton, girder, deck)", -60, -170, B_),
        ("tag", "LORA:CH-01>CH-02", "LoRa ± 18 m", "#0077E6"),
        ("dim", "CH-02:base", "CH-02:top", "6 m", -60),
        ("dim", "CH-01:base", "CH-01:top", "± 1,5 m", 70),
    ], legend_loc="lower right")
    label_render("gld", "detail", D3C, (0, 120, 2200, 1400), "C. Detail mounting GLD (skala nyata)", [
        ("lab", "GLD-02", "GLD-02 · enclosure 200 × 90 × 290 mm, antena di atas", 420, -200, G_),
        ("lab", "GLD-02:gland", "Cable gland Ex d M20 × 1,5", 420, 40, "#8D6E00"),
        ("lab", "GLD-02:base", "Pelat dasar 240 × 240 × 10 mm + anchor, dicor", 420, 120, B_),
        ("dim", "GLD-02:base", "GLD-02:top", "1,0 m", -110),
    ], legend=False)
    label_render("gw", "detail", D3D, (300, 0, 2200, 1350), "D. Detail Gateway di tepi atap kantor (skala nyata)", [
        ("lab", "GW-01", "GW-01 Gateway · 5 VDC ± 0,73 W", 430, -60, O),
        ("lab", "SIKU", "Siku L 50 × 50 × 5 HDG ± 1,5 m, baut/klem SS304", -380, -150, B_),
        ("dim", "SIKU:base", "SIKU:top", "1,5 m", -90),
    ], legend=False)
    d = docx.Document()
    st = d.styles["Normal"]; st.font.name = "Calibri"; st.font.size = Pt(10)
    s = d.sections[0]
    s.page_width, s.page_height = Inches(8.27), Inches(11.69)
    s.left_margin = s.right_margin = Inches(0.7)
    s.top_margin = Inches(1.15); s.bottom_margin = Inches(0.8); s.header_distance = Inches(0.35)

    t = s.header.add_table(rows=1, cols=3, width=Inches(6.87))
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    c0, c1, c2 = t.rows[0].cells
    for c, w in zip(t.rows[0].cells, [Inches(1.5), Inches(3.87), Inches(1.5)]):
        c.width = w
    c0.paragraphs[0].add_run().add_picture(os.path.join(ASSET, "logo_lgu.png"), height=Inches(0.42))
    p = c1.paragraphs[0]; p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("PT LAPI GANESHA UTAMA"); r.bold = True; r.font.size = Pt(11)
    p2 = c1.add_paragraph(); p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p2.add_run("Rencana Instalasi GLD · RU VI Balongan"); r.font.size = Pt(8)
    c2.paragraphs[0].add_run().add_picture(os.path.join(ASSET, "logo_pertamina.png"), height=Inches(0.3))
    c2.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
    fp = s.footer.paragraphs[0]; fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = fp.add_run(f"{DOC_NO} · Rev {REV} · Halaman "); r.font.size = Pt(8)
    page_field(fp)

    tp = d.add_paragraph(); tp.alignment = WD_ALIGN_PARAGRAPH.CENTER; tp.paragraph_format.space_after = Pt(2)
    r = tp.add_run("RENCANA INSTALASI"); r.bold = True; r.font.size = Pt(16); r.font.color.rgb = RGBColor.from_string(BLUE)
    tp = d.add_paragraph(); tp.alignment = WD_ALIGN_PARAGRAPH.CENTER; tp.paragraph_format.space_after = Pt(10)
    r = tp.add_run("Gas Leak Detection (GLD) Tahap 2 — Field Test RU VI Balongan"); r.bold = True; r.font.size = Pt(12)

    table(d, ["Item", "Keterangan"], [
        ("Nomor dokumen", DOC_NO), ("Revisi", REV), ("Tanggal", TANGGAL),
        ("Lokasi", "PT Kilang Pertamina Internasional RU VI Balongan, Indramayu — area WHB"),
        ("Lingkup", "2 GLD, 2 Cluster Head (CH), 1 Gateway, PC server lokal"),
        ("Acuan", "Site survey & notulensi rapat 17 Nov 2026; rapat koordinasi 13 Nov 2026; contoh material RU VI (terminal box HEXLON, PSU TDK-Lambda); konfigurasi dikonfirmasi 26 Nov 2026"),
    ], [1.6, 5.25])

    h(d, "1. Tujuan dan batasan")
    para(d, "Dokumen ini merencanakan pemasangan sistem GLD di RU VI Balongan untuk uji performansi dan reliabilitas di lapangan. "
            "Isinya: tata letak titik, skema catu daya dan jalur data, metode mounting, pembagian tanggung jawab, tahapan kerja, "
            "serta kriteria commissioning.")
    note(d, "Batasan keselamatan: unit GLD belum memiliki sertifikat Ex (proses sertifikasi berjalan). Sesuai kesepakatan survei "
            "17 Nov 2026, GLD dipasang di area bawah bersuhu aman yang dinilai berisiko rendah, bukan di zona berbahaya, dan "
            "penempatan final mengikuti persetujuan HSE/klasifikasi area RU VI. GLD dioperasikan tanpa baterai (24 VDC saja), "
            "dengan temperature cut-off pada firmware dan fan aktif hanya saat sampling.")

    h(d, "2. Tata letak titik")
    figure(d, os.path.join(RB, "peta_lokasi_balongan_26nov.png"),
           "Gambar 1. Rencana titik GLD, Cluster Head, dan Gateway (citra Google Maps; garis merah = jalur data). "
           "Jarak dalam dokumen ini diukur kasar dari skala peta dan perlu diverifikasi di lapangan.", Inches(6.85))
    para(d, "Lokasi GLD-01, GLD-02, dan CH-01 berada di lantai dasar di bawah struktur WHB: area beratap dengan kolom "
            "beton persegi, girder baja, serta pipa gas dan pipa berinsulasi di atasnya (survei 17–18 November 2026).",
         size=9.5)
    figure(d, os.path.join(RB, "foto_survei_lokasi_gld_18nov.jpg"),
           "Foto 1. Lokasi GLD di bawah struktur WHB (foto survei 18 November 2026).", Inches(5.2))
    table(d, ["ID", "Fungsi", "Posisi", "Catu daya", "Mounting", "Jarak (estimasi)"], [
        ("GLD-01", "Sensor gas", "Area WHB, di bawah struktur, dekat CH-01", "24 VDC via JB", "Stanchion 2\" HDG 1 m + pelat U-bolt", "± 11 m ke CH-01"),
        ("GLD-02", "Sensor gas", "Area WHB, di bawah struktur, selatan GLD-01", "24 VDC via JB", "Stanchion 2\" HDG 1 m + pelat U-bolt", "± 9 m ke CH-01"),
        ("CH-01", "Relay LoRa dari 2 GLD", "Di antara GLD, di bawah struktur, posisi rendah ± 1,5 m (tanpa cahaya matahari)", "5 VDC via JB", "Klem ke struktur existing; stanchion bila tidak memungkinkan", "± 18 m ke CH-02"),
        ("CH-02", "Relay LoRa ke Gateway", "Di luar struktur, terpapar matahari", "Panel surya + baterai CH", "Stanchion 2\" HDG s/d 6 m + bracket panel surya", "± 80 m (garis lurus) ke GW-01"),
        ("GW-01", "Gateway LoRa", "Tepi atap gedung kantor", "5 VDC, adaptor di dalam kantor", "Dudukan siku besi L 50×50×5 HDG", "—"),
        ("Server", "PC server lokal + router", "Dalam gedung kantor", "Stopkontak/UPS kantor", "—", "—"),
    ], [0.6, 1.05, 1.35, 1.05, 1.6, 1.2], size=8.3)

    h(d, "3. Skema catu daya dan jalur data")
    figure(d, DIAG, "Gambar 2. Diagram satu garis catu daya dan jalur data.", Inches(6.85))
    h(d, "Model 3D instalasi", 2)
    para(d, "Model 3D berikut dibangun dari citra peta untuk memperlihatkan posisi dan ketinggian GLD, Cluster Head, "
            "dan Gateway serta arah link LoRa. Lokasi junction box dan rute kabel belum ditentukan sehingga tidak digambarkan "
            "(lihat diagram satu garis di atas). Tampilan A–B: ukuran perangkat dibesarkan 5× agar terlihat (tinggi tiang nyata); "
            "tampilan C–D: skala nyata. Posisi, bentuk bangunan, dan tinggi atap kantor (± 8 m) adalah estimasi dari citra.", size=9.5)
    figure(d, D3A, "Gambar 3. Gambaran lokasi: klaster WHB dan Gateway di tepi atap kantor.", Inches(6.85))
    figure(d, D3B, "Gambar 4. Klaster WHB: GLD-01/02 (stanchion 1 m) dan CH-01 (± 1,5 m) di lantai dasar bawah struktur WHB (kolom beton, girder, deck digambar transparan); "
                   "CH-02 bertenaga surya (6 m) merelay data ke Gateway.", Inches(6.85))
    figure(d, D3C, "Gambar 5. Detail GLD di stanchion 1 m dengan pelat U-bolt.", Inches(6.85))
    figure(d, D3D, "Gambar 6. Detail Gateway: dudukan siku besi di tepi atap kantor.", Inches(6.85))
    para(d, "Catu daya. PSU 24 VDC memakai unit RU VI (TDK-Lambda DLP240-24-1) di panel RU VI (safe area), ditambah PSU 5 VDC "
            "(Mean Well HDR-15-5) dan fuse per cabang di panel yang sama. Dua jalur kabel armoured (24 VDC dan 5 VDC) ditarik ke "
            "satu terminal box Ex d di lapangan, lalu dicabangkan ke GLD-01, GLD-02 (24 VDC) dan CH-01 (5 VDC). Tidak ada PSU di "
            "lapangan. CH-02 mandiri dengan panel surya. Gateway dicatu 5 VDC dari adaptor di dalam kantor; tidak ada 220 VAC di luar gedung.")
    para(d, "Jalur data. GLD-01 dan GLD-02 mengirim data via LoRa ke CH-01, diteruskan ke CH-02, lalu ke Gateway di tepi atap "
            "kantor. Gateway meneruskan ke PC server lokal di dalam kantor (rencana: Wi-Fi 2,4 GHz ke router LGU, seperti skema RU IV; "
            "perlu dikonfirmasi). Sistem berdiri sendiri (standalone/advisory), tidak terhubung ke DCS.")
    table(d, ["Ruas", "Kabel", "Panjang (asumsi)", "Keterangan"], [
        ("Panel RU VI → JB (24 VDC)", "Armoured 2C 1,5 mm² Cu/XLPE/SWA", "± 30 m", "Jarak panel belum diukur"),
        ("Panel RU VI → JB (5 VDC)", "Armoured 2C 1,5 mm²", "± 30 m", "Naik ke 2,5 mm² bila jatuh tegangan > 5 %"),
        ("JB → GLD-01 / GLD-02", "Armoured 2C 1,5 mm²", "2 × ± 15 m", "Gland Ex d M20 di kedua ujung"),
        ("JB → CH-01", "Armoured 2C 1,5 mm²", "± 10 m", "5 VDC"),
        ("Adaptor kantor → GW-01", "NYY 2C 1,5 mm² tahan UV + conduit", "± 20 m", "5 VDC, beban ± 0,73 W"),
    ], [1.75, 2.0, 1.1, 2.0], size=8.5)
    para(d, "Total kabel armoured ± 110 m (termasuk cadangan 10 %) → 3 roll 50 m; kabel NYY 1 roll 50 m.", size=9.5)

    h(d, "4. Junction box dan metode mounting")
    bullet(d, "Junction box: terminal box HEXLON/Helon HLBH31-D/M20×1.5F atau setara (Ex db IIC T6 Gb, IP66), dipesan dengan 5 entry "
              "M20 × 1,5 bawaan pabrik (2 input + 3 output). Enclosure Ex d tidak boleh dilubangi di lapangan karena membatalkan "
              "sertifikat; entry tak terpakai ditutup stopping plug Ex d.")
    bullet(d, "GLD: stanchion pipa 2\" Sch 40 HDG, tinggi 1 m di atas pelat dasar 240 × 240 × 10 mm (anchor bolt), pelat dudukan "
              "250 × 250 × 5 mm SS304 dengan 2 U-bolt 2\" M10.")
    bullet(d, "CH-01: diklem ke struktur existing dengan bracket U-bolt tanpa las/bor; stanchion dipakai bila tidak ada struktur yang sesuai.")
    bullet(d, "CH-02: stanchion 2\" HDG s/d 6 m, bracket CH dan rangka panel surya dengan sudut kemiringan yang dapat diatur.")
    bullet(d, "GW-01: siku baja L 50 × 50 × 5 mm HDG ± 1,5 m di tepi atap kantor, diikat ke struktur atap dengan baut/klem SS304 "
              "(tanpa las di lokasi), lengkap pelat dudukan dan klem enclosure Gateway/antena.")
    figure(d, os.path.join(RB, "pole_bracket_redraw.png"),
           "Gambar 7. Acuan pole & bracket GLD, Cluster Head, dan panel surya (desain LGU, dimensi mm).", Inches(6.85))

    h(d, "5. Pembagian tanggung jawab")
    table(d, ["Pihak", "Tanggung jawab"], [
        ("LGU & ITB", "Suplai GLD, CH, panel surya CH, Gateway (dengan adaptor), router; basis desain bracket; supervisi teknis & QA; "
                      "terminasi di unit GLD/CH, energize, konfigurasi, commissioning, dan berita acara"),
        ("RU VI Balongan", "Izin kerja/HSE, persetujuan titik & klasifikasi area, PSU 24 VDC di panel, ruang panel & stopkontak/UPS "
                           "kantor, akses atap kantor, PC server/jaringan sesuai kesepakatan"),
        ("Pelaksana instalasi", "Penyediaan & pemasangan stanchion, bracket, dudukan Gateway, JB, cable gland, penarikan kabel, "
                                "grounding (pelaksana RU VI, atau jasa instalasi LGU bila diambil sesuai penawaran)"),
    ], [1.5, 5.35])

    h(d, "6. Tahapan kerja")
    table(d, ["No", "Tahap", "Kegiatan", "PIC", "Durasi"], [
        ("1", "Konfirmasi desain", "Validasi titik & rute kabel, jarak panel–JB, cara pasang CH-01, jalur data GW–server", "LGU + RU VI", "1 minggu"),
        ("2", "Pengadaan & fabrikasi", "PO material, fabrikasi stanchion/bracket/siku, indent JB HLBH31", "Pelaksana / LGU", "2–4 minggu"),
        ("3", "Izin kerja & HSE", "Permit, JSA, toolbox meeting, isolasi panel (LOTO)", "RU VI + pelaksana", "Paralel tahap 2"),
        ("4", "Pekerjaan mekanis", "Pengecoran/anchor stanchion, pasang bracket, JB, dudukan GW", "Pelaksana", "2 hari"),
        ("5", "Pengkabelan", "Penarikan kabel, gland, terminasi di JB & panel, grounding, kabel GW", "Pelaksana", "2 hari"),
        ("6", "Pemasangan perangkat", "Mount GLD, CH-01, CH-02 + panel surya, Gateway", "LGU (QA) + pelaksana", "1 hari"),
        ("7", "Energize & commissioning", "Uji tegangan, LoRa per hop, alarm push, data di server", "LGU", "2 hari"),
        ("8", "Serah terima", "Berita acara instalasi & commissioning, awal masa uji", "LGU + RU VI", "—"),
    ], [0.35, 1.35, 2.85, 1.35, 0.95], size=8.5)
    para(d, "Pekerjaan lapangan (tahap 4–7) ± 7 hari kerja, di luar waktu tunggu izin kerja.", size=9.5)

    h(d, "7. Kriteria commissioning")
    table(d, ["No", "Uji", "Kriteria terima"], [
        ("C-1", "Tegangan di terminal GLD-01/02", "24 VDC ± 10 % saat fan aktif"),
        ("C-2", "Tegangan di terminal CH-01", "5 VDC ± 5 % saat transmit"),
        ("C-3", "Kontinuitas & isolasi kabel, grounding", "Tidak ada hubung singkat; earthing JB & stanchion terhubung"),
        ("C-4", "Link LoRa per hop (GLD→CH-01→CH-02→GW)", "RSSI lebih baik dari −90 dBm, tanpa paket hilang beruntun"),
        ("C-5", "Data normal sampai server", "Data tiap GLD tampil di dashboard sesuai interval"),
        ("C-6", "Alarm push", "Gas uji pada GLD memicu alarm di server tanpa pull request"),
        ("C-7", "Temperature cut-off & fan sampling", "Cut-off aktif sesuai setelan; fan hanya jalan saat sampling"),
        ("C-8", "Operasi kontinu", "Tidak ada gangguan selama 24 jam pertama"),
    ], [0.5, 3.0, 3.35], size=8.6)

    h(d, "8. Hal yang perlu dikonfirmasi")
    for t in ["Lokasi panel RU VI dan jarak panel ke junction box (menentukan panjang kabel dan penampang jalur 5 VDC).",
              "Kesediaan PSU 24 VDC DLP240-24-1 milik RU VI dan ruang di panel untuk PSU 5 VDC & fuse.",
              "CH-01 dapat diklem ke struktur existing atau perlu stanchion.",
              "Jalur data Gateway ke PC server (Wi-Fi ke router di kantor, atau LAN) dan lokasi PC server.",
              "Akses ke atap kantor dan izin memasang dudukan siku besi; titik masuk kabel Gateway ke dalam gedung.",
              "Persetujuan HSE atas titik GLD (area risiko rendah) selama sertifikat Ex belum terbit.",
              "Verifikasi jarak di lapangan (estimasi dari peta: GLD–CH-01 ± 10 m, CH-01–CH-02 ± 18 m, CH-02–GW ± 80 m)."]:
        bullet(d, t)

    h(d, "Lampiran — Daftar material (kuantitas)")
    table(d, ["Kode", "Material", "Qty", "Satuan"], [
        ("A.1", "Terminal box Ex d HLBH31-D/M20×1.5F atau setara, 5 entry", "1", "unit"),
        ("B.1", "Cable gland armoured M20 × 1,5 Ex d", "9", "pcs"),
        ("B.2", "Stopping plug M20 × 1,5 Ex d", "1", "pcs"),
        ("C.1", "Kabel armoured 2C 1,5 mm² Cu/XLPE/SWA", "3", "roll 50 m"),
        ("C.2", "Kabel NYY 2C 1,5 mm² tahan UV (Gateway)", "1", "roll 50 m"),
        ("C.3", "Conduit & klem jalur kabel Gateway", "1", "lot"),
        ("D.2", "PSU 5 VDC Mean Well HDR-15-5 (di panel RU VI)", "1", "unit"),
        ("D.3", "Fuse terminal & terminal block di panel RU VI", "1", "set"),
        ("E.1", "Stanchion GLD 2\" HDG 1 m", "2", "set"),
        ("E.2", "Stanchion CH 2\" HDG s/d 6 m", "2", "set"),
        ("E.3", "Bracket GLD (pelat U-bolt)", "2", "set"),
        ("E.4", "Bracket Cluster Head", "2", "set"),
        ("E.5", "Bracket panel surya CH-02", "1", "set"),
        ("E.6", "Dudukan Gateway siku besi", "1", "set"),
        ("F.1", "Aksesoris terminasi (skun, heat-shrink, label, earth tag)", "3", "set"),
    ], [0.6, 4.35, 0.7, 1.2], size=8.6)
    para(d, "Perangkat GLD, CH, panel surya CH, Gateway beserta adaptor, dan router disediakan LGU (tidak termasuk daftar di atas).", size=9, italic=True)

    d.save(OUT)
    print("written", OUT)


if __name__ == "__main__":
    build()
