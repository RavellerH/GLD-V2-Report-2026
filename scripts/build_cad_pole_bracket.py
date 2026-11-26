"""Gambar ulang (vektor) 'Pole & Bracket GLD / CH & Solar Panel' dari gambar sumber raster
Sumber Dokumen/POLE-BRACKET-GLD-CH-SOLAR.pdf.pdf. Hanya dimensi yang tercantum di sumber yang diberi ukuran.
Output: scripts/assets/rab_balongan/pole_bracket_redraw.{png,pdf}"""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Arc, Circle, FancyBboxPatch, Polygon, Rectangle

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "assets", "rab_balongan", "pole_bracket_redraw")
INK, THIN, CEN, ACC = "#1b1b1b", 0.6, "#555555", "#2B5FCB"
plt.rcParams.update({"font.family": "Arial", "font.size": 7})

fig = plt.figure(figsize=(16.54, 11.69))  # A3 landscape
ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 420); ax.set_ylim(0, 297); ax.set_aspect("equal"); ax.axis("off")


def L(xs, ys, lw=1.0, c=INK, ls="-", z=2):
    ax.plot(xs, ys, color=c, lw=lw, ls=ls, zorder=z, solid_capstyle="butt")


def R(x, y, w, h, lw=1.0, fc="none", z=2):
    ax.add_patch(Rectangle((x, y), w, h, fill=fc != "none", fc=fc, ec=INK, lw=lw, zorder=z))


def T(x, y, s, size=7, ha="center", va="center", rot=0, bold=False, c=INK):
    ax.text(x, y, s, fontsize=size, ha=ha, va=va, rotation=rot, color=c, fontweight="bold" if bold else "normal", zorder=5)


def dim_h(x1, x2, y, ext_from, label, above=True):
    for x in (x1, x2):
        L([x, x], [ext_from, y + (1.2 if above else -1.2)], THIN)
    ax.annotate("", (x1, y), (x2, y), arrowprops=dict(arrowstyle="<|-|>", lw=THIN, color=INK, mutation_scale=6), zorder=4)
    T((x1 + x2) / 2, y + (1.6 if above else -1.8), label)


def dim_v(y1, y2, x, ext_from, label, right=True):
    for y in (y1, y2):
        L([ext_from, x + (1.2 if right else -1.2)], [y, y], THIN)
    ax.annotate("", (x, y1), (x, y2), arrowprops=dict(arrowstyle="<|-|>", lw=THIN, color=INK, mutation_scale=6), zorder=4)
    T(x + (2.0 if right else -2.0), (y1 + y2) / 2, label, rot=90)


def leader(x, y, tx, ty, s, ha="left"):
    ax.annotate(s, (x, y), (tx, ty), fontsize=7, ha=ha, va="center",
                arrowprops=dict(arrowstyle="-|>", lw=THIN, color=INK, mutation_scale=6), zorder=5)


def title(x, y, s, sub=None):
    T(x, y, s, 8.5, bold=True)
    L([x - len(s) * 1.05, x + len(s) * 1.05], [y - 2.2, y - 2.2], 0.8)
    if sub:
        T(x, y - 5, sub, 6.5, c=CEN)


# ------------------------------------------------------------------ frame & zones
R(8, 8, 404, 281, 1.4)
R(5, 5, 410, 287, 0.5)
for i in range(1, 13):
    x = 8 + (i - 0.5) * 404 / 12
    T(x, 6.5, str(i), 6, c=CEN); T(x, 290.5, str(i), 6, c=CEN)
for i, ch in enumerate("ABCDEFGH"):
    y = 289 - (i + 0.5) * 281 / 8
    T(6.5, y, ch, 6, c=CEN); T(413.5, y, ch, 6, c=CEN)
L([206, 206], [60, 286], 0.5, CEN, (0, (6, 3)))

# ------------------------------------------------------------------ GLD: elevation 1:10
s = 0.1
gx, gy = 70, 70          # pole axis, ground level
pole_w = 6.03            # OD 60,3 mm (2") skala 1:10 — lihat catatan 3
H = 1000 * s
R(gx - 12, gy - 1.0, 24, 1.0, 1.0, "#d9d9d9")                # base plate 240 (tebal skematik)
R(gx - pole_w / 2, gy, pole_w, H + 3, 1.0, "#f2f2f2")         # pole
L([gx - pole_w / 2 - 0.4, gx + pole_w / 2 + 0.4], [gy + H * 0.45] * 2, 0.8)  # sambungan teleskopik
leader(gx + pole_w / 2, gy + H * 0.45, gx + 22, gy + H * 0.36, "Tiang teleskopik")
# bracket arm + vertical plate + GLD (skematik)
L([gx, gx + 7.5], [gy + H, gy + H], 2.2)
R(gx + 7.5, gy + H - 12, 1.0, 25, 1.0, "#d9d9d9")
R(gx + 8.5, gy + H - 4, 9, 10, 0.9, "#eef3fb"); R(gx + 10.5, gy + H - 11, 5, 7, 0.9, "#eef3fb")
ax.add_patch(Circle((gx + 13, gy + H + 1), 2.6, fill=False, ec=INK, lw=0.8, zorder=3))
L([gx + 9.5, gx + 9.5], [gy + H + 6, gy + H + 12], 1.2)
leader(gx + 17.5, gy + H + 2, gx + 30, gy + H + 10, "Unit GLD")
leader(gx + 8, gy + H - 10, gx + 16, gy + H - 40, "Pelat bracket + U-bolt\n(lihat Gambar L-2)")
dim_h(gx, gx + 7.5, gy + H + 16, gy + H + 1, "75")
dim_v(gy, gy + H, gx - 20, gx - 13, "1000", right=False)
dim_h(gx - 12, gx + 12, gy - 9, gy - 1.5, "240", above=False)
L([gx - 40, gx + 40], [gy - 1, gy - 1], 0.5, CEN)
for k in range(8):
    L([gx - 38 + k * 10, gx - 41 + k * 10], [gy - 1, gy - 4], 0.4, CEN)
L([gx, gx], [gy - 6, gy + H + 4], 0.4, CEN, (0, (8, 2, 1, 2)))
title(gx, 270, "POLE & BRACKET — GAS LEAK DETECTOR", "TAMPAK SAMPING   SKALA 1:10")

# ------------------------------------------------------------------ base plate plan 1:4 (sama untuk GLD & CH)
s2 = 0.25
px, py = 160, 172
R(px - 30, py - 30, 60, 60, 1.1, "#f4f4f4")
for dx in (-1, 1):
    for dy in (-1, 1):
        cx, cy = px + dx * (120 - 20) * s2, py + dy * (120 - 20) * s2
        ax.add_patch(Circle((cx, cy), 25.4 / 2 * s2, fill=False, ec=INK, lw=0.9, zorder=3))
        L([cx - 4, cx + 4], [cy, cy], 0.35, CEN); L([cx, cx], [cy - 4, cy + 4], 0.35, CEN)
ax.add_patch(Circle((px, py), 60.3 / 2 * s2, fill=True, fc="#dddddd", ec=INK, lw=0.9, zorder=3))
T(px, py, "TIANG", 5, c=CEN)
dim_h(px - 30, px + 30, py - 40, py - 31, "240", above=False)
dim_v(py - 30, py + 30, px + 40, px + 31, "240")
dim_h(px - 30, px - 25, py + 38, py + 31, "20")
dim_v(py - 30, py - 25, px - 40, px - 31, "20", right=False)
leader(px - 25 + 2.2, py + 25 + 2.2, px - 12, py + 44, "4 × Ø25,4")
title(px, 233, "PELAT DASAR (DETAIL C)", "TAMPAK BAWAH   SKALA 1:4")

# ------------------------------------------------------------------ CH: elevation 1:40
s3 = 1 / 40
cx0, cy0 = 245, 70
HC = 6000 * s3
R(cx0 - 6, cy0 - 1.0, 12, 1.0, 1.0, "#d9d9d9")
R(cx0 - 1.2, cy0, 2.4, HC, 0.9, "#f2f2f2")
for k in range(1, 6):
    L([cx0 - 1.8, cx0 + 1.8], [cy0 + k * 1000 * s3] * 2, 0.7)
for k in range(6):
    T(cx0 - 4.6, cy0 + (k + 0.5) * 1000 * s3, "1000", 6, rot=90)
    L([cx0 - 1.2, cx0 - 4], [cy0 + k * 1000 * s3] * 2, THIN)
L([cx0 - 1.2, cx0 - 4], [cy0 + HC] * 2, THIN)
L([cx0 - 3.2, cx0 - 3.2], [cy0, cy0 + HC], THIN)
dim_v(cy0, cy0 + HC, cx0 - 16, cx0 - 8, "6000", right=False)
by = cy0 + 1430 * s3   # posisi bracket surya diskalakan dari gambar sumber (tidak berdimensi)
ax.add_patch(Polygon([(cx0 + 1.2, by), (cx0 + 9, by + 3.2), (cx0 + 9, by + 4.2), (cx0 + 1.2, by + 1)], closed=True, fc="#eef3fb", ec=INK, lw=0.8, zorder=3))
R(cx0 + 1.2, cy0 + HC - 4, 2.0, 4, 0.8, "#eef3fb")
for lab, (x, y, r) in {"A": (cx0, cy0 + HC - 2, 7), "B": (cx0 + 3, by + 2, 8), "C": (cx0, cy0, 7)}.items():
    ax.add_patch(Circle((x, y), r, fill=False, ec=INK, lw=0.6, ls=(0, (4, 2)), zorder=3))
    T(x + r + 2.5, y - r + 1, lab, 8, bold=True)
leader(cx0 + 1.2, cy0 + 3000 * s3, cx0 + 22, cy0 + 2700 * s3, "Tiang teleskopik")
title(cx0 + 2, 270, "POLE & BRACKET — CLUSTER HEAD & SOLAR PANEL", "TAMPAK SAMPING   SKALA 1:40")

# ------------------------------------------------------------------ detail A 1:5
ax0, ay0 = 330, 205
R(ax0 - 3.34, ay0, 6.68, 50, 1.0, "#f2f2f2")
R(ax0 + 3.34, ay0 + 33, 5.5, 14, 1.0, "#eef3fb")
L([ax0 - 4.3, ax0 + 4.3], [ay0 + 43, ay0 + 43], 1.6); L([ax0 - 4.3, ax0 + 4.3], [ay0 + 37, ay0 + 37], 1.6)
L([ax0, ax0], [ay0 - 3, ay0 + 53], 0.4, CEN, (0, (8, 2, 1, 2)))
dim_h(ax0 - 3.34, ax0 + 3.34, ay0 + 57, ay0 + 51, "Ø33,4")
leader(ax0 + 8.8, ay0 + 40, ax0 + 22, ay0 + 30, "Cluster Head /\nRouting Node")
leader(ax0 + 4.3, ay0 + 37, ax0 + 22, ay0 + 16, "Klem")
title(ax0 + 8, 273, "DETAIL A", "SKALA 1:5")

# ------------------------------------------------------------------ detail B (skematik)
bx0, by0 = 330, 120
R(bx0 - 3.34, by0, 6.68, 62, 1.0, "#f2f2f2")
L([bx0 - 4.3, bx0 + 4.3], [by0 + 30] * 2, 1.6); L([bx0 - 4.3, bx0 + 4.3], [by0 + 26] * 2, 1.6)
ax.add_patch(Polygon([(bx0 + 3.34, by0 + 28), (bx0 + 14, by0 + 28), (bx0 + 14, by0 + 31), (bx0 + 3.34, by0 + 31)], closed=True, fc="#d9d9d9", ec=INK, lw=0.8, zorder=3))
ax.add_patch(Polygon([(bx0 + 6, by0 + 31), (bx0 + 44, by0 + 44), (bx0 + 44, by0 + 47), (bx0 + 6, by0 + 34)], closed=True, fc="#c9d7f0", ec=INK, lw=0.9, zorder=3))
L([bx0 + 14, bx0 + 20], [by0 + 31, by0 + 36], 1.2)
ax.add_patch(Arc((bx0 + 6, by0 + 31), 22, 22, theta1=0, theta2=19, lw=THIN, color=INK, zorder=4))
T(bx0 + 20, by0 + 30, "α", 7)
leader(bx0 + 34, by0 + 44, bx0 + 50, by0 + 56, "Panel surya")
leader(bx0 + 10, by0 + 28, bx0 + 30, by0 + 16, "Bracket panel surya\n(sudut α dapat diatur)")
leader(bx0 + 4.3, by0 + 26, bx0 + 30, by0 + 4, "Klem U-bolt ke tiang")
title(bx0 + 15, 192, "DETAIL B", "SKEMATIK, TANPA SKALA")

# ------------------------------------------------------------------ notes & title block
notes = [
    "CATATAN",
    "1. Dimensi dalam milimeter. Gambar digambar ulang dari gambar desain sumber \"Pole & Bracket GLD / Cluster Head & Solar Panel\";",
    "    hanya dimensi yang tercantum di sumber yang diberi ukuran. Jangan mengukur langsung dari gambar.",
    "2. Detail C (pelat dasar 240 × 240 mm, 4 lubang Ø25,4) berlaku untuk tiang GLD dan tiang CH.",
    "3. Diameter tiang GLD, tebal pelat dasar, material, dan tinggi bracket panel surya belum ditetapkan di sumber;",
    "    gambar di sini skematik. Ditetapkan bersama pelaksana setelah site survey.",
    "4. Pelat bracket GLD 250 × 250 mm dengan U-bolt 2\" (OD 60,3 mm) M10: lihat Gambar L-2.",
]
for i, t in enumerate(notes):
    T(14, 52 - i * 4.6, t, 6.8 if i else 7.5, ha="left", bold=(i == 0))
R(300, 8, 112, 46, 1.0)
for y in (19, 30, 41):
    L([300, 412], [y, y], 0.6)
L([340, 340], [8, 41], 0.6)
rows = [("Judul", "POLE & BRACKET GLD / CH & SOLAR PANEL"), ("Proyek", "Gas Leak Detection (GLD) V2"),
        ("Satuan / lembar", "mm  ·  proyeksi sudut pertama  ·  1/1  ·  Rev. A")]
for (k, v), y in zip(rows, (35.5, 24.5, 13.5)):
    T(303, y, k, 6.2, ha="left", c=CEN); T(343, y, v, 7.2, ha="left", bold=(k == "Judul"))
T(356, 47.5, "PT LAPI GANESHA UTAMA", 9, bold=True, c=ACC)
fig.savefig(OUT + ".png", dpi=300); fig.savefig(OUT + ".pdf")
print(OUT)
