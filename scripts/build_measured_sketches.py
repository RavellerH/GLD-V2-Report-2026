# -*- coding: utf-8 -*-
"""Dimensioned sketches of the GLD V2 enclosure joint, drawn from caliper / steel-rule measurements (7 Oct 2026).

Source photographs: Sumber Dokumen/Foto_Assembly_GLD_07Okt2026/{Base_*,Cover_*,Oring_*,Gasket_*}.jpg
(Figures 4-128 ... 4-137 of the certification documents).

These are ILLUSTRATIONS of measured values, not controlled manufacturing drawings. Features that were not
measured are drawn dashed and labelled "not measured". Output: scripts/assets/measured_sketches/MS-0N.png
"""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Circle, Rectangle

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(REPO, "scripts", "assets", "measured_sketches")
os.makedirs(OUT, exist_ok=True)

INK = "#262321"
BLUE = "#2B5FCB"
GREY = "#8A8F98"
HATCH_FC = "#E8EBF0"

# ---------------------------------------------------------------- measured values (mm)
BORE = 84.7            # base bore at top of neck (caliper)
WALL_TOP = 5.80        # neck wall at top, bore to thread crest (caliper)
WALL_ROOT = 10.50      # neck wall at root, above O-ring (caliper)
H_THREAD = 14.8        # threaded neck height above O-ring level (caliper)
H_NECK = 20.2          # neck height from painted body shoulder (caliper)
DEPTH_BASE = 45.0      # rim to PCB-boss ledge (steel rule)
COVER_THREAD = 18.9    # cover internal thread length (caliper)
COVER_DEPTH = 47.5     # cover rim to mesh (steel rule)
OR_CORD = 2.70         # O-ring cord (caliper)
OR_OD = 91.0           # O-ring outside diameter, free (caliper)
PITCH = 1.5            # derived from ~10 crests over 14.8 mm

R_IN = BORE / 2
R_THR = R_IN + WALL_TOP            # 48.15 -> thread major diameter ~96.3
R_ROOT = R_IN + WALL_ROOT          # 52.85
H_LAND = H_NECK - H_THREAD         # 5.4


def dim(ax, p1, p2, text, off=(0, 0), side="h", fs=8, color=BLUE):
    """Dimension line with arrows between p1 and p2, text at midpoint shifted by off."""
    ax.annotate("", xy=p1, xytext=p2, arrowprops=dict(arrowstyle="<->", lw=0.8, color=color,
                                                      shrinkA=0, shrinkB=0))
    mx, my = (p1[0] + p2[0]) / 2 + off[0], (p1[1] + p2[1]) / 2 + off[1]
    ax.text(mx, my, text, fontsize=fs, color=color, ha="center", va="center",
            rotation=90 if side == "v" else 0,
            bbox=dict(fc="white", ec="none", pad=0.6))


def ext(ax, x1, y1, x2, y2):
    ax.plot([x1, x2], [y1, y2], lw=0.5, color=BLUE)


def thread(ax, r, z0, z1, outward=True, depth=0.9):
    xs, ys = [], []
    n = int((z1 - z0) / PITCH)
    for i in range(n + 1):
        z = z0 + i * PITCH
        xs += [r, r - depth if outward else r + depth]
        ys += [z, z + PITCH / 2]
    ax.plot(xs[:-1], ys[:-1], lw=0.6, color=INK)


def title_block(fig, code, title, sources):
    fig.subplots_adjust(bottom=0.13)
    fig.text(0.02, 0.075, f"{code}  ·  {title}", fontsize=10, weight="bold", color=INK)
    fig.text(0.02, 0.012, "GLD V2 — illustrative sketch drawn from caliper / steel-rule measurements of the current "
             "production unit (7 Oct 2026).\nNot a controlled drawing; dashed features not measured. "
             f"Source: {sources}. Dimensions in mm.", fontsize=6.5, color=GREY, linespacing=1.4)
    fig.add_artist(Rectangle((0.008, 0.002), 0.984, 0.105, transform=fig.transFigure, fill=False, lw=0.8,
                             ec=INK))


def finish(ax):
    ax.set_aspect("equal")
    ax.axis("off")


# ================================================================ MS-01 base neck, half section
def ms01():
    fig, ax = plt.subplots(figsize=(9, 7.2))
    z_ledge = H_NECK - DEPTH_BASE
    # neck wall (hatched solid section): threaded zone + land
    neck = Polygon([(R_IN, H_NECK), (R_THR, H_NECK), (R_THR, H_LAND), (R_ROOT, H_LAND), (R_ROOT, 0),
                    (R_IN, 0)], closed=True, fc=HATCH_FC, ec=INK, lw=1.1, hatch="////")
    ax.add_patch(neck)
    thread(ax, R_THR, H_LAND, H_NECK)
    # body below shoulder (not measured): dashed
    ax.plot([R_ROOT, R_ROOT + 8, R_ROOT + 8, R_IN + 6], [0, 0, z_ledge - 6, z_ledge - 6], ls="--", lw=0.8,
            color=GREY)
    ax.plot([R_IN, R_IN], [0, z_ledge], lw=1.1, color=INK)
    ax.plot([R_IN, R_IN - 14], [z_ledge, z_ledge], lw=1.1, color=INK)
    ax.text(R_IN - 14, z_ledge - 8.5, "PCB-boss ledge (floor below not measured)", fontsize=7, color=GREY,
            ha="left", va="top")
    ax.text(R_ROOT + 9, z_ledge / 2, "body wall\nnot measured", fontsize=7, color=GREY, va="center")
    # O-ring on the land
    ax.add_patch(Circle((R_THR + OR_CORD / 2 + 0.3, H_LAND + OR_CORD / 2), OR_CORD / 2, fc=INK, ec=INK))
    ax.annotate("O-ring Ø2.70 cord", xy=(R_THR + 1.6, H_LAND + 1.0), xytext=(R_IN - 30, H_LAND + 3),
                fontsize=7.5, color=INK, arrowprops=dict(arrowstyle="-", lw=0.6, color=INK))
    # centreline
    ax.plot([0, 0], [z_ledge - 10, H_NECK + 10], ls="-.", lw=0.7, color=GREY)
    ax.text(0.8, H_NECK + 8, "℄", fontsize=11, color=GREY)
    # dimensions
    ext(ax, 0, H_NECK + 1, 0, H_NECK + 16)
    ext(ax, R_IN, H_NECK + 1, R_IN, H_NECK + 16)
    dim(ax, (0, H_NECK + 14), (R_IN, H_NECK + 14), "bore Ø84.7 (R 42.35)", off=(0, 1.8))
    ext(ax, R_THR, H_NECK + 1, R_THR, H_NECK + 8)
    dim(ax, (R_IN, H_NECK + 6), (R_THR, H_NECK + 6), "5.80", off=(0, 1.8))
    ext(ax, R_ROOT, -1, R_ROOT, -7)
    ext(ax, R_IN, -1, R_IN, -7)
    dim(ax, (R_IN, -5.5), (R_ROOT, -5.5), "10.50", off=(0, -1.8))
    ext(ax, R_THR + 1, H_NECK, R_ROOT + 22, H_NECK)
    ext(ax, R_ROOT + 1, H_LAND, R_ROOT + 16, H_LAND)
    ext(ax, R_ROOT + 1, 0, R_ROOT + 22, 0)
    dim(ax, (R_ROOT + 14, H_LAND), (R_ROOT + 14, H_NECK), "14.8 (≈10 threads)", off=(2.6, 0), side="v")
    dim(ax, (R_ROOT + 20, 0), (R_ROOT + 20, H_NECK), "20.2", off=(2.0, 0), side="v")
    ext(ax, R_IN - 1, H_NECK, R_IN - 22, H_NECK)
    dim(ax, (R_IN - 20, z_ledge), (R_IN - 20, H_NECK), "≈45 (rule)", off=(-2.4, 0), side="v")
    ax.annotate("external thread ≈M96 × 1.5 (derived:\nØ84.7 + 2 × 5.80; ≈10 crests / 14.8 mm)",
                xy=(R_THR - 0.3, H_NECK - 3), xytext=(R_THR + 6, H_NECK + 26), fontsize=7.5, color=INK,
                arrowprops=dict(arrowstyle="-", lw=0.6, color=INK))
    ax.text(R_ROOT + 1, -1.5, "painted body shoulder", fontsize=7, color=GREY, va="top")
    ax.set_xlim(-8, R_ROOT + 30)
    ax.set_ylim(z_ledge - 14, H_NECK + 38)
    finish(ax)
    title_block(fig, "MS-01", "Base enclosure — threaded neck, half section",
                "Figures 4-128, 4-129, 4-130, 4-131, 4-133, 4-136")
    fig.savefig(os.path.join(OUT, "MS-01_base_neck_half_section.png"), dpi=200, bbox_inches="tight")
    plt.close(fig)


# ================================================================ MS-02 cover, half section
def ms02():
    fig, ax = plt.subplots(figsize=(9, 7.2))
    r_t = R_THR            # mating internal thread (nominal)
    wall = 4.0             # drawing thickness only (not measured)
    # threaded zone (solid hatched, inner profile is the thread)
    sec = Polygon([(r_t, 0), (r_t + wall, 0), (r_t + wall, -COVER_DEPTH - 3), (R_IN - 4, -COVER_DEPTH - 3),
                   (R_IN - 4, -COVER_DEPTH), (R_IN, -COVER_DEPTH), (R_IN, -COVER_THREAD - 3), (r_t, -COVER_THREAD)],
                  closed=True, fc=HATCH_FC, ec=GREY, lw=0.8, ls="--", hatch="////")
    ax.add_patch(sec)
    ax.plot([r_t, r_t], [0, -COVER_THREAD], lw=1.1, color=INK)
    thread(ax, r_t, -COVER_THREAD, 0, outward=False)
    # mesh
    ax.plot([0, R_IN - 4], [-COVER_DEPTH, -COVER_DEPTH], lw=2.2, color=INK)
    ax.text(4, -COVER_DEPTH + 1.5, "stainless-steel mesh (sensing face)", fontsize=7.5, color=INK)
    ax.text(r_t + wall + 1.5, -COVER_DEPTH / 2, "cover wall / outer profile\nnot measured (drawn dashed)",
            fontsize=7, color=GREY, va="center")
    ax.plot([0, 0], [-COVER_DEPTH - 10, 10], ls="-.", lw=0.7, color=GREY)
    ax.text(0.8, 7, "℄", fontsize=11, color=GREY)
    # dims
    ext(ax, r_t + wall + 1, 0, r_t + wall + 30, 0)
    ext(ax, r_t + 1, -COVER_THREAD, r_t + wall + 22, -COVER_THREAD)
    ext(ax, R_IN - 3, -COVER_DEPTH, r_t + wall + 30, -COVER_DEPTH)
    dim(ax, (r_t + wall + 20, -COVER_THREAD), (r_t + wall + 20, 0), "≈18.9\ninternal thread", off=(4.2, 0), side="v")
    dim(ax, (r_t + wall + 28, -COVER_DEPTH), (r_t + wall + 28, 0), "≈47.5 (rule)", off=(2.6, 0), side="v")
    ax.annotate("internal thread mating ≈M96 × 1.5 (derived)", xy=(r_t + 0.5, -8), xytext=(8, 8),
                fontsize=7.5, color=INK, arrowprops=dict(arrowstyle="-", lw=0.6, color=INK))
    ax.text(r_t - 1, 1.2, "cover rim", fontsize=7, color=GREY, ha="right")
    ax.set_xlim(-8, r_t + wall + 40)
    ax.set_ylim(-COVER_DEPTH - 14, 16)
    finish(ax)
    title_block(fig, "MS-02", "Enclosure cover — internal thread and depth, half section",
                "Figures 4-135, 4-137")
    fig.savefig(os.path.join(OUT, "MS-02_cover_half_section.png"), dpi=200, bbox_inches="tight")
    plt.close(fig)


# ================================================================ MS-03 assembled flameproof joint
def ms03():
    fig, ax = plt.subplots(figsize=(9, 6.6))
    # base neck
    ax.add_patch(Polygon([(R_IN, H_NECK), (R_THR, H_NECK), (R_THR, H_LAND), (R_ROOT, H_LAND), (R_ROOT, 0),
                          (R_IN, 0)], closed=True, fc=HATCH_FC, ec=INK, lw=1.1, hatch="////"))
    thread(ax, R_THR, H_LAND, H_NECK)
    # cover screwed home: rim on O-ring, internal thread overlaps the neck
    z_rim = H_LAND + OR_CORD * 0.75          # O-ring compressed (illustrative)
    z_top = z_rim + COVER_THREAD
    ax.add_patch(Polygon([(R_THR, z_rim), (R_THR + 4, z_rim), (R_THR + 4, z_top + 10), (R_THR, z_top + 10)],
                         closed=True, fc="#F4F6FA", ec=GREY, lw=0.8, ls="--", hatch="\\\\\\\\"))
    ax.add_patch(Circle((R_THR + 2, H_LAND + OR_CORD * 0.375), OR_CORD * 0.42, fc=INK, ec=INK))
    ax.plot([0, 0], [-6, z_top + 14], ls="-.", lw=0.7, color=GREY)
    # engagement band
    ax.add_patch(Rectangle((R_THR - 1.2, z_rim), 1.2, H_NECK - z_rim, fc="#F6C26B", ec="none", alpha=0.7))
    ext(ax, R_THR + 5, z_rim, R_THR + 22, z_rim)
    ext(ax, R_THR + 1, H_NECK, R_THR + 22, H_NECK)
    dim(ax, (R_THR + 18, z_rim), (R_THR + 18, H_NECK), "engaged ≤14.8\n(limited by neck)", off=(5.5, 0), side="v")
    ax.text(R_IN - 38, H_NECK + 8, "enclosure interior\n(free volume ≈0.4 L, indicative)", fontsize=7.5, color=INK)
    ax.text(R_THR + 6, z_top + 6, "cover (thread ≈18.9)", fontsize=7.5, color=GREY)
    ax.text(R_ROOT + 1, H_LAND - 1.5, "O-ring (weather seal,\nnot part of the flame path)", fontsize=7,
            color=INK, va="top")
    rule = ("IEC 60079-1, threaded joint, Group IIC, free volume >100 cm³:\n"
            "≥5 full threads engaged and axial engagement ≥8 mm; tolerance class 6g/6H.\n"
            "Measured: ≈10 threads over ≤14.8 mm → indicatively satisfied; to be confirmed on the controlled "
            "drawing\nand by measuring engagement with the cover screwed home.")
    ax.text(R_IN - 40, -4, rule, fontsize=7.5, color=INK, va="top",
            bbox=dict(fc="#F3F6FC", ec=BLUE, lw=0.6, pad=4))
    ax.set_xlim(R_IN - 42, R_ROOT + 30)
    ax.set_ylim(-26, z_top + 16)
    finish(ax)
    title_block(fig, "MS-03", "Cover-to-base threaded flameproof joint — assembled detail",
                "Figures 4-127 to 4-137")
    fig.savefig(os.path.join(OUT, "MS-03_threaded_joint_detail.png"), dpi=200, bbox_inches="tight")
    plt.close(fig)


# ================================================================ MS-04 O-ring
def ms04():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9, 4.8), gridspec_kw=dict(width_ratios=[2.2, 1]))
    r_o, r_i = OR_OD / 2, OR_OD / 2 - OR_CORD
    a1.add_patch(Circle((0, 0), r_o, fc=INK, ec=INK))
    a1.add_patch(Circle((0, 0), r_i, fc="white", ec=INK))
    a1.plot([-r_o - 6, r_o + 6], [0, 0], ls="-.", lw=0.6, color=GREY)
    a1.plot([0, 0], [-r_o - 6, r_o + 6], ls="-.", lw=0.6, color=GREY)
    dim(a1, (-r_o, r_o + 8), (r_o, r_o + 8), "OD ≈91.0 (caliper, free state)", off=(0, 3))
    ext(a1, -r_o, 0, -r_o, r_o + 10)
    ext(a1, r_o, 0, r_o, r_o + 10)
    dim(a1, (-r_i, -8), (r_i, -8), "ID ≈85.6 (derived)", off=(0, 3))
    a1.set_xlim(-r_o - 10, r_o + 10)
    a1.set_ylim(-r_o - 10, r_o + 16)
    finish(a1)
    a2.add_patch(Circle((0, 0), OR_CORD / 2, fc=INK, ec=INK))
    dim(a2, (-OR_CORD / 2, -2.4), (OR_CORD / 2, -2.4), "Ø2.70", off=(0, -0.7), fs=8)
    a2.text(0, 2.6, "Section A–A (cord)", fontsize=8, ha="center", color=INK)
    a2.text(0, -4.6, "Rubber; compound, hardness\nand temperature range TBC", fontsize=7, ha="center",
            color=GREY)
    a2.set_xlim(-4, 4)
    a2.set_ylim(-6, 4)
    finish(a2)
    title_block(fig, "MS-04", "Cover-to-base O-ring", "Figures 4-132, 4-134")
    fig.savefig(os.path.join(OUT, "MS-04_O-ring.png"), dpi=200, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    ms01(); ms02(); ms03(); ms04()
    print("written", sorted(os.listdir(OUT)))
