# -*- coding: utf-8 -*-
"""Layout kabel isometrik + cable schedule format MoC (lembar 1) untuk instalasi GLD RU VI Balongan.

Konvensi mengikuti MoC 15769/RU IV (Tabel 10 & Gambar 8): From / To / Cable / Route Length /
Allowance / Est. Cable Length; proposed cable routing; balon nomor perangkat.
Output: scripts/assets/rab_balongan/cable_layout_iso_sheet1.png (+ dipakai build_cable_schedule_balongan.py)
"""
import math
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Polygon

HERE = os.path.dirname(os.path.abspath(__file__))
INK, CY, GRN, GRY, ORG = "#1E1E1E", "#00A6C8", "#2E8B2E", "#8A8F96", "#E07B00"
PPM = 5.8
ROT = math.radians(31.0)
U = (math.cos(ROT), math.sin(ROT)); V = (-math.sin(ROT), math.cos(ROT))
C30, S30 = math.cos(math.radians(30)), 0.5


def P(px, py):
    return ((px - 1300) / PPM, (196 - py) / PPM)


PT = {"JB": P(1324, 238), "GLD-01": P(1285, 187), "GLD-02": P(1362, 289), "CH-01": P(1370, 220), "CH-02": P(1315, 429)}
Z_JB, Z_RUN, Z_GLD, Z_CH1 = 1.0, 0.3, 0.85, 1.3   # entry JB, jalur kabel (klem/tray rendah), gland GLD, gland CH-01


def iso(x, y, z=0.0):
    return ((x - y) * C30, (x + y) * S30 + z)


def line3(ax, pts, **kw):
    q = [iso(*p) for p in pts]
    ax.plot([a for a, _ in q], [b for _, b in q], **kw)


def route(a, b):
    d = (b[0] - a[0], b[1] - a[1])
    du = d[0] * U[0] + d[1] * U[1]
    c = (a[0] + du * U[0], a[1] + du * U[1])
    return [a, c, b], abs(du) + abs(d[0] * V[0] + d[1] * V[1])


def cable(ax, pts3):
    line3(ax, pts3, color=CY, lw=3.2, solid_capstyle="round")
    line3(ax, pts3, color="white", lw=1.1)


def balloon(ax, xyz, n, dx=1.2, dy=1.6):
    x, y = iso(*xyz)
    ax.plot([x, x + dx], [y, y + dy], color=INK, lw=0.6)
    ax.add_patch(Circle((x + dx, y + dy), 0.75, fc="white", ec=INK, lw=0.8))
    ax.text(x + dx, y + dy, str(n), ha="center", va="center", fontsize=6.5, fontweight="bold")


def pole(ax, p, h, box=None, col=INK):
    line3(ax, [(p[0], p[1], 0), (p[0], p[1], h)], color=col, lw=1.6)
    bx = [(p[0] - .35, p[1] - .35, 0), (p[0] + .35, p[1] - .35, 0), (p[0] + .35, p[1] + .35, 0), (p[0] - .35, p[1] + .35, 0), (p[0] - .35, p[1] - .35, 0)]
    line3(ax, bx, color=col, lw=0.8)
    if box:
        z0, z1 = box
        x, y = iso(p[0], p[1], (z0 + z1) / 2)
        ax.add_patch(Rectangle((x + 0.15, y - (z1 - z0) / 2), 0.9, z1 - z0, fc="white", ec=col, lw=1.0))


def build_layout(ax):
    """Gambar isometrik klaster WHB (kabel daya) — koordinat dari peta 27 Nov 2026."""
    ax.set_aspect("equal"); ax.axis("off")
    pc = ((PT["GLD-01"][0] + PT["GLD-02"][0] + PT["CH-01"][0]) / 3 + .3, (PT["GLD-01"][1] + PT["GLD-02"][1] + PT["CH-01"][1]) / 3 + .2)
    hx, hy, H = 14, 12, 5.0
    corners = [(-hx, -hy), (hx, -hy), (hx, hy), (-hx, hy)]
    w = lambda a, b: (pc[0] + a * U[0] + b * V[0], pc[1] + a * U[1] + b * V[1])
    cw = [w(*c) for c in corners]
    for z, lw, ls in ((0, 0.6, (0, (6, 3))), (H, 0.8, "-")):
        line3(ax, [(x, y, z) for x, y in cw + cw[:1]], color=GRY, lw=lw, ls=ls)
    for a in (-hx, -hx / 3, hx / 3, hx):
        for b in (-hy, 0, hy):
            x, y = w(a, b)
            line3(ax, [(x, y, 0), (x, y, H)], color=GRY, lw=0.7)
    x, y = iso(*cw[2], H); ax.text(x, y + 0.8, "STRUKTUR WHB (deck ± 5 m)", fontsize=6.5, color="#555", ha="center")
    # pipa gas kuning (indikatif, sepanjang sumbu struktur)
    a1, a2 = w(-hx, 2), w(hx, 2)
    line3(ax, [(a1[0], a1[1], 4.6), (a2[0], a2[1], 4.6)], color="#D4A600", lw=2.0)
    x, y = iso(a2[0], a2[1], 4.6); ax.text(x + 0.5, y, "pipa gas kuning", fontsize=6, color="#8A6D00")
    # perangkat
    g1, g2, c1, c2, jb = PT["GLD-01"], PT["GLD-02"], PT["CH-01"], PT["CH-02"], PT["JB"]
    pole(ax, g1, 1.0, (0.7, 1.0)); pole(ax, g2, 1.0, (0.7, 1.0)); pole(ax, c1, 1.5, (1.2, 1.55))
    pole(ax, c2, 6.0, (4.0, 4.4), col=INK)
    xs, ys = iso(c2[0], c2[1], 2.5)
    ax.add_patch(Polygon([(xs + 0.2, ys - 0.2), (xs + 2.2, ys + 0.6), (xs + 2.2, ys + 1.2), (xs + 0.2, ys + 0.4)], fc="#2E4A7D", ec=INK, lw=0.6))
    xj, yj = iso(jb[0] - 0.8, jb[1] + 0.8, 0.8)
    ax.add_patch(Rectangle((xj - 0.6, yj - 0.5), 1.2, 1.0, fc="#E9ECF1", ec=INK, lw=1.0))
    rows = []
    # kabel JB -> perangkat
    for tag, k, ze in (("W-03", "GLD-01", Z_GLD), ("W-04", "GLD-02", Z_GLD), ("W-05", "CH-01", Z_CH1)):
        pts, Lh = route(jb, PT[k])
        p3 = [(jb[0], jb[1], Z_JB), (jb[0], jb[1], Z_RUN)] + [(x, y, Z_RUN) for x, y in pts[1:]] + [(PT[k][0], PT[k][1], ze)]
        cable(ax, p3)
        mid = (pts[1][0] + 0.6 * (pts[2][0] - pts[1][0]), pts[1][1] + 0.6 * (pts[2][1] - pts[1][1])) if tag != "W-03" else PT[k]
        x, y = iso(mid[0], mid[1], Z_RUN)
        ax.text(x + (-2.2 if tag == "W-03" else 0), y - 1.3, tag, fontsize=6.5, fontweight="bold", color="#007A94", ha="center",
                bbox=dict(boxstyle="round,pad=0.12", fc="white", ec=CY, lw=0.6))
        rows.append((tag, k, Lh + (Z_JB - Z_RUN) + (ze - Z_RUN)))
    # kabel panel -> JB (keluar gambar)
    for i, (tag, dz) in enumerate((("W-01", 0.0),)):
        e = (jb[0] - 9 * U[0] - 4 * V[0] - i * .4, jb[1] - 9 * U[1] - 4 * V[1])
        p3 = [(jb[0] - .1 * i, jb[1], Z_JB - .2 * i), (jb[0] - .1 * i, jb[1], Z_RUN + dz), (e[0], e[1], Z_RUN + dz)]
        cable(ax, p3)
    x, y = iso(jb[0] - 9 * U[0] - 4 * V[0], jb[1] - 9 * U[1] - 4 * V[1], 0.3)
    ax.annotate("", (x - 2.5, y - 1.4), (x, y), arrowprops=dict(arrowstyle="-|>", color="#007A94", lw=1.2))
    ax.text(x - 3, y - 2.6, "W-01 (4 inti, 24 & 5 VDC) ke PANEL RU VI\n(lokasi & rute menunggu konfirmasi, ± 30 m)", fontsize=6.3, color="#007A94", ha="center")
    # grounding stanchion & JB
    for k, p in (("GLD-01", g1), ("GLD-02", g2), ("CH-01", c1), ("CH-02", c2), ("JB", (jb[0] - .8, jb[1] + .8))):
        line3(ax, [(p[0], p[1], 0), (p[0] + .9, p[1] - .9, 0)], color=GRN, lw=1.0)
        x, y = iso(p[0] + .9, p[1] - .9, 0)
        ax.plot([x, x], [y, y - 0.7], color=GRN, lw=1.0)
        for j, ww in enumerate((0.45, 0.28, 0.12)):
            ax.plot([x - ww, x + ww], [y - 0.7 - j * 0.22] * 2, color=GRN, lw=0.9)
    # balon & nama
    for n, (k, p, z, dx, dy) in enumerate((("GLD-01", g1, 1.0, -3.2, 2.4), ("GLD-02", g2, 1.0, 2.6, 1.2), ("CH-01", c1, 1.55, 2.6, 1.6),
                                            ("CH-02", c2, 6.0, 2.4, 1.0), ("JB-01", (jb[0] - .8, jb[1] + .8), 1.3, -1.6, -2.8)), 1):
        balloon(ax, (p[0], p[1], z), n, dx, dy)
        x, y = iso(p[0], p[1], z)
        ax.text(x + dx + (1.0 if dx > 0 else -1.0), y + dy, k, fontsize=6.8, fontweight="bold", ha="left" if dx > 0 else "right", va="center")
    # LoRa (nirkabel) ke Gateway
    x, y = iso(c2[0], c2[1], 4.2)
    ax.annotate("", (x - 6, y - 6), (x - .3, y - .3), arrowprops=dict(arrowstyle="-|>", color="#2B5FCB", lw=1.0, ls=(0, (4, 3))))
    ax.text(x - 6.3, y - 7.2, "LoRa ± 78 m ke GW-01\n(nirkabel, lihat detail B)", fontsize=6.2, color="#2B5FCB", ha="center")
    # utara
    nx, ny = iso(-26, 18, 0); tx, ty = iso(-26, 22, 0)
    ax.annotate("", (tx, ty), (nx, ny), arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.2))
    ax.text(tx, ty + 0.6, "U", fontsize=8, fontweight="bold", ha="center")
    ax.autoscale_view()
    return rows


def build_gw(ax):
    """Detail B: Gateway di tepi atap carport, kabel W-06 dari adaptor di dalam kantor; W-08 router–PC (skematik)."""
    ax.set_aspect("equal"); ax.axis("off")
    L, Wd, H, cp = 16.0, 10.0, 3.5, 6.0
    box = [(0, 0), (L, 0), (L, Wd), (0, Wd)]
    for z in (0, H):
        line3(ax, [(x, y, z) for x, y in box + box[:1]], color=GRY, lw=0.8 if z else 0.6)
    for x, y in box:
        line3(ax, [(x, y, 0), (x, y, H)], color=GRY, lw=0.7)
    cpb = [(0, 0), (L, 0), (L, -cp), (0, -cp)]
    line3(ax, [(x, y, 4.0) for x, y in cpb + cpb[:1]], color=GRY, lw=0.8)
    for x in (0.3, L / 2, L - 0.3):
        line3(ax, [(x, -cp, 0), (x, -cp, 4.0)], color=GRY, lw=0.7)
    x, y = iso(L * 0.75, Wd, H); ax.text(x, y + 0.5, "GEDUNG KANTOR", fontsize=6.5, color="#555", ha="center")
    x, y = iso(0, -cp / 2, 4.0); ax.text(x - 0.5, y, "atap carport ± 4 m", fontsize=6.2, color="#555", ha="right")
    gw = (L * 0.55, -cp)
    line3(ax, [(gw[0], gw[1], 4.0), (gw[0], gw[1], 4.5)], color=INK, lw=1.6)
    x, y = iso(gw[0], gw[1], 4.6)
    ax.add_patch(Rectangle((x - 0.45, y - 0.15), 0.9, 0.5, fc="#DFF3F5", ec=INK, lw=1.0))
    ax.plot([x, x], [y + 0.35, y + 1.6], color="#4FB3E8", lw=1.6)
    ad = (gw[0], 2.0)
    cable(ax, [(ad[0], ad[1], 0.5), (ad[0], 0.1, 0.5), (ad[0], 0.1, 3.7), (gw[0], -0.3, 3.8), (gw[0], gw[1] + 0.3, 3.8), (gw[0], gw[1], 4.5)])
    x, y = iso(ad[0], ad[1], 0.5)
    ax.add_patch(Rectangle((x - 0.5, y - 0.3), 1.0, 0.6, fc="#FFF1E0", ec=INK, lw=0.8))
    ax.text(x, y - 1.0, "Adaptor 5 V (UPS)", fontsize=6.2, va="center", ha="center")
    x2, y2 = iso(gw[0], -cp / 2, 3.8)
    ax.text(x2 + 0.8, y2 + 0.4, "W-06", fontsize=6.5, fontweight="bold", color="#007A94", bbox=dict(boxstyle="round,pad=0.12", fc="white", ec=CY, lw=0.6))
    rt, pcp = (L * 0.3, 2.0), (L * 0.3, 5.0)
    cable(ax, [(rt[0], rt[1], 0.8), (pcp[0], pcp[1], 0.8)])
    for k, p, dx in (("Router", rt, -0.8), ("PC server", pcp, -0.8)):
        x, y = iso(p[0], p[1], 0.8)
        ax.add_patch(Rectangle((x - 0.5, y - 0.3), 1.0, 0.6, fc="#EEF3FC", ec=INK, lw=0.8))
        ax.text(x + dx, y, k, fontsize=6.2, ha="right", va="center")
    x, y = iso(rt[0], 3.5, 0.8); ax.text(x + 0.6, y - 0.2, "W-08", fontsize=6.5, fontweight="bold", color="#007A94",
                                       bbox=dict(boxstyle="round,pad=0.12", fc="white", ec=CY, lw=0.6))
    x, y = iso(gw[0], gw[1], 4.6); ax.annotate("", (iso(rt[0], rt[1], 0.8)[0] + 0.5, iso(rt[0], rt[1], 0.8)[1] + 0.3), (x - 0.3, y),
                                             arrowprops=dict(arrowstyle="<|-|>", color=CY, lw=0.8, ls=(0, (1, 2))))
    balloon(ax, (gw[0], gw[1], 4.6), 6, 1.6, 1.4)
    ax.text(x + 2.8, y + 1.4, "GW-01 (siku 0,5 m)", fontsize=6.8, fontweight="bold", va="center")
    line3(ax, [(gw[0] + .3, gw[1], 4.0), (gw[0] + .3, gw[1], 0), (gw[0] + 1.3, gw[1] - 1, 0)], color=GRN, lw=1.0)
    ax.autoscale_view()
    # panjang rute = asumsi survei (gedung digambar skematik)
    return [("W-06", "GW-01", 20.0), ("W-08", "PC server", 2.0)]


def allowance(L):
    a = max(2, math.ceil(L * 0.10))
    return a, round(100 * a / L)


def sheet1(title_block):
    """Lembar 1 A3: layout isometrik + Tabel cable schedule format MoC + ketentuan."""
    fig = plt.figure(figsize=(16.54, 11.69))
    bg = fig.add_axes([0, 0, 1, 1]); bg.set_xlim(0, 1); bg.set_ylim(0, 1); bg.axis("off")
    bg.add_patch(Rectangle((0.012, 0.015), 0.976, 0.97, fc="none", ec=INK, lw=1.6))
    bg.add_patch(Rectangle((0.018, 0.021), 0.964, 0.958, fc="none", ec=INK, lw=0.5))
    bg.text(0.03, 0.955, "LAYOUT CABLE PEMASANGAN GLD — RU VI BALONGAN", fontsize=14, fontweight="bold", va="top")
    bg.text(0.03, 0.93, "Proposed cable routing (isometrik, tanpa skala) dari posisi titik 27 Nov 2026 · format mengikuti MoC 15769/RU IV",
            fontsize=8.5, color="#444", va="top")
    a = fig.add_axes([0.03, 0.43, 0.6, 0.48]); r1 = build_layout(a)
    bg.text(0.035, 0.44, "DETAIL A — Klaster WHB (catu daya 24/5 VDC dari JB-01)", fontsize=8, fontweight="bold")
    b = fig.add_axes([0.66, 0.50, 0.31, 0.36]); r2 = build_gw(b)
    bg.text(0.665, 0.48, "DETAIL B — Gateway & ruang kantor (skematik)", fontsize=8, fontweight="bold")
    bg.add_patch(Rectangle((0.655, 0.47), 0.32, 0.43, fc="none", ec=GRY, lw=0.6, ls="--"))
    arm = "NYFGbY 4×1,5 mm² (ready stock)"
    data = [("W-01", "Panel RU VI (PSU 24 V F1 & 5 V F2)", "JB-01", arm + " · 4 inti", 27.0)]
    cab = {"W-03": arm, "W-04": arm, "W-05": arm, "W-06": "NYY 2×1,5 mm² UV + conduit", "W-08": "UTP Cat6"}
    frm = {"W-03": "JB-01", "W-04": "JB-01", "W-05": "JB-01", "W-06": "Adaptor 5 V (kantor, UPS)", "W-08": "Router"}
    for t, k, L in r1 + r2:
        data.append((t, frm[t], k, cab[t], L))
    head = ["No. kabel", "From", "To", "Cable", "Route Length", "Allowance", "Est. Cable Length"]
    cw = [0.06, 0.15, 0.08, 0.17, 0.07, 0.08, 0.08]
    x0, y0, rh = 0.03, 0.40, 0.024
    xs = [x0]
    for w in cw:
        xs.append(xs[-1] + w)
    bg.text(x0, y0 + 0.008, "Tabel 1. Cable Schedule Instalasi GLD RU VI Balongan", fontsize=8, fontweight="bold")
    bg.add_patch(Rectangle((x0, y0 - rh), xs[-1] - x0, rh, fc="#BDD7EE", ec=INK, lw=0.6))
    for i, t in enumerate(head):
        bg.text((xs[i] + xs[i + 1]) / 2, y0 - rh / 2, t, fontsize=7, fontweight="bold", ha="center", va="center")
    y = y0 - rh
    tot_arm = 0
    for tag, fr, to, cb, L in data:
        al, pc = allowance(L)
        est = math.ceil(L + al)
        if cb.startswith(arm):
            tot_arm += est
        vals = [tag, fr, to, cb, f"{L:.0f} m", f"{al} m ({pc}%)", f"{est} m"]
        for i, v in enumerate(vals):
            bg.text((xs[i] + xs[i + 1]) / 2, y - rh / 2, v, fontsize=6.8, ha="center", va="center", fontweight="bold" if i == 0 else "normal")
        bg.add_patch(Rectangle((x0, y - rh), xs[-1] - x0, rh, fc="none", ec=INK, lw=0.5))
        y -= rh
    for xx in xs:
        bg.plot([xx, xx], [y0, y], color=INK, lw=0.5)
    bg.text(x0, y - 0.012, f"Total NYFGbY 4×1,5 mm² (W-01, W-03…W-05) ≈ {tot_arm} m (asumsi) → BoQ dilebihkan: 3 roll × 50 m = 150 m. Grounding E-01…E-05: NYA 1×6 mm² hijau-kuning, 5 × ± 5 m. "
            "W-01: panjang asumsi (lokasi panel RU VI belum ditentukan).", fontsize=6.8, va="top")
    notes = ["1. Jalur kabel merupakan proposed cable routing dari posisi titik pada peta (27 Nov 2026); diverifikasi saat survei (HP-1).",
             "2. Semua kabel daya NYFGbY 4×1,5 mm² (ready stock); JB-01 = terminal box Ex d Helon HLBH31, 4 entry M20; gland Ex d M20 di JB-01 dan GLD.",
             "3. Estimasi panjang = rute horizontal mengikuti grid struktur WHB + jalur vertikal + allowance 10 % (min. 2 m) untuk",
             "    terminasi, cable dressing dan toleransi instalasi; dipakai sebagai dasar BoQ.",
             "4. Kabel diklem pada struktur/lantai, atau memakai cable tray/conduit bila diminta RU VI; segregasi dari kabel proses.",
             "5. Routing aktual dapat disesuaikan kondisi lapangan atas verifikasi & persetujuan User/Owner RU VI.",
             "6. Seluruh tiang logam GLD/CH, JB-01 dan siku Gateway di-bonding ke sistem grounding terdekat (IEC 60079-14)."]
    bg.text(0.03, y - 0.04, "KETENTUAN", fontsize=7.6, fontweight="bold")
    for i, t in enumerate(notes):
        bg.text(0.03, y - 0.058 - i * 0.0145, t, fontsize=6.7)
    lx, ly = 0.75, 0.40
    bg.text(lx, ly + 0.008, "LEGENDA", fontsize=7.6, fontweight="bold")
    items = [(CY, "Rute kabel (proposed)", "-"), ("#2B5FCB", "LoRa / Wi-Fi (nirkabel)", "--"), (GRN, "Grounding ke titik ground RU VI", "-"),
             (GRY, "Struktur/gedung eksisting (indikatif)", "-"), ("#D4A600", "Pipa gas kuning (acuan posisi GLD)", "-")]
    for i, (c, t, ls) in enumerate(items):
        bg.plot([lx, lx + 0.025], [ly - 0.02 - i * 0.02] * 2, color=c, lw=2.4, ls=ls)
        bg.text(lx + 0.03, ly - 0.02 - i * 0.02, t, fontsize=6.8, va="center")
    bg.text(lx, ly - 0.13, "Balon: 1 GLD-01 · 2 GLD-02 · 3 CH-01 · 4 CH-02 · 5 JB-01 · 6 GW-01", fontsize=6.6, va="center")
    title_block(bg, "Layout Cable & Cable Schedule", "LGU/GLD/CS-BLG/2026-001 · Lembar 1/2")
    return fig


if __name__ == "__main__":
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(14, 7), gridspec_kw={"width_ratios": [2, 1]})
    r1 = build_layout(a1); r2 = build_gw(a2)
    fig.savefig(os.path.join(HERE, "assets", "rab_balongan", "cable_layout_iso_test.png"), dpi=110)
    for t, k, L in r1 + r2:
        a, pc = allowance(L)
        print(t, k, round(L, 1), a, pc, math.ceil(L + a))
