# -*- coding: utf-8 -*-
"""Cable schedule (gambar teknik A3) instalasi GLD RU VI Balongan.

Output: Deliverables/Instalasi_GLD_RU-VI_Balongan/Cable_Schedule_GLD_RU-VI_Balongan.pdf
        scripts/assets/rab_balongan/skenario_S8_cable_schedule.png
"""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
PDF = os.path.join(ROOT, "Deliverables", "Instalasi_GLD_RU-VI_Balongan", "Cable_Schedule_GLD_RU-VI_Balongan.pdf")
PNG = os.path.join(HERE, "assets", "rab_balongan", "skenario_S8_cable_schedule.png")
INK, ORG, PUR, CYA, GRN, BLU, GRY = "#262321", "#E07B00", "#7B4FD6", "#00838F", "#2E8B2E", "#2B5FCB", "#8A8F96"

ARM = "NYFGbY 4×1,5 mm² 0,6/1 kV\n(armour pita baja, ready stock)"
ROWS = [  # tag, dari, ke, jenis, inti, tegangan, panjang, gland asal, gland tujuan, keterangan, warna
    ("W-01", "Panel RU VI\nPSU 24 V (F1) & 5 V (F2)", "JB · E1", ARM, "+24 / −24 / +5 / −5", "24 & 5 VDC", "± 30", "B.3 CW M20 (non-Ex)", "B.1 Ex d M20", "Rute & jarak panel diverifikasi (HP-1)", ORG),
    ("W-03", "JB · E2", "GLD-01", ARM, "L+ / L− / PE", "24 VDC", "± 16", "B.1 Ex d M20", "B.1 Ex d M20", "JB di tengah antara GLD-01 & GLD-02", ORG),
    ("W-04", "JB · E3", "GLD-02", ARM, "L+ / L− / PE", "24 VDC", "± 16", "B.1 Ex d M20", "B.1 Ex d M20", "Diklem ke struktur/lantai, drip loop", ORG),
    ("W-05", "JB · E4", "CH-01", ARM, "+ / − (PE)", "5 VDC", "± 14", "B.1 Ex d M20", "Adaptor M20 + CW M20*", "Naik ke stanchion 1,5 m", PUR),
    ("W-06", "Adaptor 5 V\n(kantor, UPS)", "GW-01", "NYY 2×1,5 mm² tahan UV\n+ conduit fleksibel", "+ / −", "5 VDC", "± 22", "—", "Adaptor M20 + nylon M20*", "Tembusan dinding disegel", CYA),
    ("W-07", "Panel surya\nCH-02 (± 2,5 m)", "CH-02 (± 4,2 m)", "Kabel PV bawaan panel\n(min. 2×2,5 mm² UV)", "+ / −", "≤ 24 VDC", "± 2", "MC4 / bawaan", "Adaptor M20 + nylon M20*", "Diklem UV ke tiang", GRN),
    ("W-08", "Router", "PC server", "UTP Cat6", "4 pair", "—", "± 2", "RJ45", "RJ45", "Jaringan lokal, tanpa internet", BLU),
    ("W-09", "PC server NIC-2", "Intranet kantor", "UTP Cat6", "4 pair", "—", "s.d.k.", "RJ45", "RJ45", "Opsional, izin IT RU VI", GRY),
    ("E-01…E-05", "Stanchion GLD-01/02,\nJB, CH-01, CH-02", "Titik ground RU VI", "NYA 1×6 mm² hijau-kuning", "PE", "—", "5 × ± 5", "Skun + earth clamp", "Skun", "F.3", GRN),
]
HEAD = ["No. kabel", "Dari", "Ke", "Jenis kabel", "Inti", "Tegangan", "Panjang (m)", "Gland/entry asal", "Gland/entry tujuan", "Rute / keterangan"]
COLW = [0.055, 0.09, 0.075, 0.17, 0.065, 0.055, 0.06, 0.11, 0.115, 0.13]


def block(ax, x, y, w, h, t, sub=None, fc="white"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.002,rounding_size=0.006", fc=fc, ec=INK, lw=1.1))
    ax.text(x + w / 2, y + h * (0.62 if sub else 0.5), t, ha="center", va="center", fontsize=7.6, fontweight="bold")
    if sub:
        ax.text(x + w / 2, y + h * 0.27, sub, ha="center", va="center", fontsize=6.2, color="#444")


def wire(ax, pts, c, tag, tpos, lw=2.2, ls="-"):
    xs, ys = zip(*pts)
    ax.plot(xs, ys, color=c, lw=lw, ls=ls, solid_capstyle="butt")
    ax.text(*tpos, tag, fontsize=6.6, fontweight="bold", color=c, ha="center", va="center",
            bbox=dict(boxstyle="round,pad=0.15", fc="white", ec=c, lw=0.8))


def build():
    fig = plt.figure(figsize=(16.54, 11.69))  # A3 landscape
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    ax.add_patch(Rectangle((0.012, 0.015), 0.976, 0.97, fc="none", ec=INK, lw=1.6))
    ax.add_patch(Rectangle((0.018, 0.021), 0.964, 0.958, fc="none", ec=INK, lw=0.5))
    ax.text(0.03, 0.955, "CABLE SCHEDULE — INSTALASI GLD RU VI BALONGAN", fontsize=14, fontweight="bold", va="top")
    ax.text(0.03, 0.93, "Catu daya 24/5 VDC, jalur data lokal, dan grounding · posisi titik per 27 Nov 2026", fontsize=8.5, color="#444", va="top")

    # ---------------- diagram routing
    Y0 = 0.56
    zones = [(0.03, 0.17, "PANEL RU VI (safe area)"), (0.215, 0.43, "LAPANGAN — lantai dasar WHB & luar struktur"),
             (0.66, 0.31, "GEDUNG KANTOR & ATAP CARPORT")]
    for x, w, t in zones:
        ax.add_patch(Rectangle((x, Y0), w, 0.335, fc="#F7F9FC", ec=GRY, lw=0.7, ls="--"))
        ax.text(x + 0.005, Y0 + 0.325, t, fontsize=7, fontweight="bold", color="#4A5568", va="top")
    block(ax, 0.045, 0.80, 0.065, 0.04, "PSU 24 V", "HDR-60-24", "#FFF1E0")
    block(ax, 0.045, 0.66, 0.065, 0.04, "PSU 5 V", "HDR-15-5", "#F1EBFF")
    for y, t in ((0.82, "F1"), (0.68, "F2")):
        ax.add_patch(Rectangle((0.125, y - 0.008), 0.025, 0.016, fc="white", ec=INK, lw=0.8)); ax.text(0.1375, y + 0.017, t, fontsize=6.3, ha="center")
        ax.plot([0.11, 0.125], [y, y], color=INK, lw=0.9)
    ax.text(0.0775, 0.605, "220 VAC dari panel/UPS RU VI\n(lingkup RU VI)", fontsize=6.2, ha="center", color="#555")
    # JB
    ax.add_patch(FancyBboxPatch((0.255, 0.68), 0.075, 0.13, boxstyle="round,pad=0.002,rounding_size=0.008", fc="#E9ECF1", ec=INK, lw=1.4))
    ax.text(0.2925, 0.795, "JB Ex d", ha="center", fontsize=7.6, fontweight="bold"); ax.text(0.2925, 0.78, "HLBH31 · 4 entry", ha="center", fontsize=6.2)
    for i, e in enumerate(["E1", "E2", "E3", "E4"]):
        ax.text(0.2925, 0.762 - i * 0.017, e, ha="center", fontsize=6.2, color="#555")
    block(ax, 0.47, 0.83, 0.07, 0.04, "GLD-01", "24 VDC · 1 m", "#FFF1E0")
    block(ax, 0.47, 0.74, 0.07, 0.04, "GLD-02", "24 VDC · 1 m", "#FFF1E0")
    block(ax, 0.47, 0.65, 0.07, 0.04, "CH-01", "5 VDC · 1,5 m", "#F1EBFF")
    block(ax, 0.565, 0.635, 0.07, 0.04, "CH-02", "± 4,2 m", "#F1EBFF")
    block(ax, 0.565, 0.585, 0.07, 0.03, "Panel surya", "± 2,5 m (di bawah CH)", "#E8F4E8")
    block(ax, 0.70, 0.82, 0.07, 0.04, "GW-01", "atap carport", "#E0F4F6")
    block(ax, 0.70, 0.68, 0.07, 0.04, "Adaptor 5 V", "UPS kantor", "#FFF1E0")
    block(ax, 0.80, 0.68, 0.06, 0.04, "Router", "Wi-Fi 2,4 GHz", "#EEF3FC")
    block(ax, 0.89, 0.68, 0.065, 0.04, "PC server", "lokal", "#EEF3FC")
    ax.plot([0.15, 0.19, 0.19], [0.82, 0.82, 0.79], color=ORG, lw=1.2); wire(ax, [(0.19, 0.79), (0.255, 0.762)], INK, "W-01 (4 inti)", (0.222, 0.80))
    ax.plot([0.15, 0.19, 0.19], [0.68, 0.68, 0.79], color=PUR, lw=1.2)
    wire(ax, [(0.33, 0.728), (0.40, 0.728), (0.40, 0.85), (0.47, 0.85)], ORG, "W-03", (0.40, 0.81))
    wire(ax, [(0.33, 0.711), (0.43, 0.711), (0.43, 0.76), (0.47, 0.76)], ORG, "W-04", (0.445, 0.735))
    wire(ax, [(0.33, 0.694), (0.38, 0.694), (0.38, 0.67), (0.47, 0.67)], PUR, "W-05", (0.415, 0.67))
    wire(ax, [(0.60, 0.615), (0.60, 0.635)], GRN, "W-07", (0.58, 0.625))
    wire(ax, [(0.735, 0.72), (0.735, 0.82)], CYA, "W-06", (0.735, 0.77))
    wire(ax, [(0.86, 0.70), (0.89, 0.70)], BLU, "W-08", (0.875, 0.73))
    wire(ax, [(0.9225, 0.68), (0.9225, 0.625)], GRY, "W-09", (0.9225, 0.645), ls="--")
    ax.text(0.9225, 0.607, "intranet (opsional)", fontsize=6.2, ha="center", color="#555")
    lora = dict(color=BLU, lw=1.0, ls=(0, (4, 3)))
    ax.plot([0.54, 0.555, 0.555, 0.54], [0.85, 0.85, 0.67, 0.67], **lora); ax.plot([0.54, 0.555], [0.76, 0.76], **lora)
    ax.plot([0.555, 0.565], [0.67, 0.655], **lora); ax.plot([0.635, 0.68, 0.68, 0.70], [0.655, 0.655, 0.84, 0.84], **lora)
    ax.plot([0.77, 0.83, 0.83], [0.84, 0.84, 0.72], color=CYA, lw=1.0, ls=(0, (1, 2)))
    ax.text(0.80, 0.85, "Wi-Fi", fontsize=6.2, color=CYA)
    ax.text(0.663, 0.75, "LoRa", fontsize=6.2, color=BLU, rotation=90)
    for x, y in ((0.505, 0.825), (0.505, 0.735), (0.505, 0.645), (0.645, 0.635), (0.2925, 0.675)):
        ax.plot([x, x], [y, y - 0.012], color=GRN, lw=1.0)
        for k, w in enumerate((0.008, 0.005, 0.002)):
            ax.plot([x - w, x + w], [y - 0.012 - k * 0.004] * 2, color=GRN, lw=1.0)
    ax.text(0.235, 0.625, "E-01…E-05: grounding stanchion & JB → titik ground RU VI", fontsize=6.3, color=GRN)
    # legenda
    lx, ly = 0.03, 0.535
    for i, (c, t, ls) in enumerate([(ORG, "24 VDC (armoured)", "-"), (PUR, "5 VDC (armoured)", "-"), (CYA, "5 VDC Gateway (NYY)", "-"),
                                     (GRN, "PV / grounding", "-"), (BLU, "LAN Cat6 / LoRa (putus-putus)", "-"), (GRY, "Opsional", "--")]):
        ax.plot([lx + i * 0.16, lx + i * 0.16 + 0.025], [ly, ly], color=c, lw=2.2, ls=ls)
        ax.text(lx + i * 0.16 + 0.03, ly, t, fontsize=6.8, va="center")

    # ---------------- tabel cable schedule
    tx, ty, rh, hh = 0.03, 0.505, 0.0295, 0.026
    xs = [tx]
    for w in COLW:
        xs.append(xs[-1] + w * 0.94 / sum(COLW))
    ax.add_patch(Rectangle((tx, ty - hh), xs[-1] - tx, hh, fc=INK, ec=INK))
    for i, t in enumerate(HEAD):
        ax.text((xs[i] + xs[i + 1]) / 2, ty - hh / 2, t, color="white", fontsize=7, fontweight="bold", ha="center", va="center")
    y = ty - hh
    for r, row in enumerate(ROWS):
        if r % 2:
            ax.add_patch(Rectangle((tx, y - rh), xs[-1] - tx, rh, fc="#F3F5F9", ec="none"))
        ax.add_patch(Rectangle((tx, y - rh), 0.006, rh, fc=row[-1], ec="none"))
        for i, t in enumerate(row[:-1]):
            ax.text(xs[i] + 0.009 if i == 0 else (xs[i] + xs[i + 1]) / 2, y - rh / 2, t, fontsize=6.4, va="center",
                    ha="left" if i == 0 else "center", fontweight="bold" if i == 0 else "normal", linespacing=1.15)
        ax.plot([tx, xs[-1]], [y - rh, y - rh], color="#C8CDD6", lw=0.5)
        y -= rh
    for x_ in xs:
        ax.plot([x_, x_], [ty, y], color="#C8CDD6", lw=0.5)
    ax.add_patch(Rectangle((tx, y), xs[-1] - tx, ty - y, fc="none", ec=INK, lw=1.0))
    ax.text(tx, y - 0.012, "* Adaptor ulir dalam M20×1,5 (bubut) + gland non-Ex untuk CH/GW: usulan, menunggu persetujuan. "
            "Gland Ex d hanya pada JB dan GLD. Semua panjang = estimasi dari peta, diverifikasi di lapangan (HP-1).",
            fontsize=6.6, color="#444", va="top")

    # ---------------- ringkasan & warna inti & title block
    bx, by = 0.03, 0.035
    ax.text(bx, by + 0.085, "RINGKASAN PANJANG", fontsize=7.6, fontweight="bold")
    for i, t in enumerate(["NYFGbY 4×1,5 mm² (W-01, W-03…W-05): ± 76 m (asumsi) → BoQ dilebihkan 3 roll 50 m (C.1)",
                           "NYY 2×1,5 mm² (W-06): ± 22 m → 1 roll 50 m (C.2) · NYA 1×6 mm² (E-01…E-05): ± 25 m (F.3)",
                           "UTP Cat6 (W-08): ± 2 m · Kabel PV (W-07): bawaan panel surya"]):
        ax.text(bx, by + 0.065 - i * 0.017, "• " + t, fontsize=6.8)
    cx = 0.40
    ax.text(cx, by + 0.085, "IDENTIFIKASI INTI (NYFGbY 4×1,5)", fontsize=7.6, fontweight="bold")
    ax.text(cx, by + 0.032, "W-01: 4 inti = +24 / −24 / +5 / −5 (sleeve label). W-03…W-05: 2 inti +/−, 1 PE, 1 cadangan.", fontsize=6.4, color="#444")
    for i, (c, t) in enumerate([("#8B4513", "Coklat = + (L+)"), ("#1F5FBF", "Biru = − (L−/0 V)"), ("#2E8B2E", "Hijau-kuning = PE"), ("#222222", "Hitam = cadangan")]):
        ax.add_patch(Rectangle((cx + (i % 2) * 0.12, by + 0.06 - (i // 2) * 0.02), 0.012, 0.01, fc=c, ec=INK, lw=0.4))
        ax.text(cx + (i % 2) * 0.12 + 0.016, by + 0.065 - (i // 2) * 0.02, t, fontsize=6.8, va="center")
    ax.text(cx, by + 0.012, "Label kabel UV di kedua ujung. Armour dijepit di cone gland → PE.", fontsize=6.6, color="#444")
    title_block(ax, "Cable Schedule Rinci & Diagram Routing", "LGU/GLD/CS-BLG/2026-001 · Lembar 2/2")
    return fig


def title_block(ax, judul, nomor, by=0.035):
    tb = 0.66
    ax.add_patch(Rectangle((tb, by - 0.012), 0.322, 0.112, fc="white", ec=INK, lw=1.2))
    rows = [("Proyek", "Gas Leak Detection (GLD) Tahap 2 — Field Test RU VI Balongan"), ("Judul", judul),
            ("No. gambar", nomor), ("Revisi / tanggal", "0.2 (Draf) · 27 November 2026"),
            ("Skala", "Tanpa skala (NTS) · A3"), ("Acuan", "Rencana Instalasi RI-BLG · Skenario Instalasi SI-BLG")]
    for i, (k, v) in enumerate(rows):
        yy = by + 0.082 - i * 0.0175
        ax.text(tb + 0.006, yy, k, fontsize=6.6, color="#555", va="center"); ax.text(tb + 0.075, yy, v, fontsize=6.9, va="center", fontweight="bold" if i < 2 else "normal")
        if i:
            ax.plot([tb, tb + 0.322], [yy + 0.0088] * 2, color="#C8CDD6", lw=0.5)
    ax.plot([tb + 0.07, tb + 0.07], [by - 0.012, by + 0.1], color="#C8CDD6", lw=0.5)
    ax.text(tb + 0.316, by + 0.108, "PT LAPI GANESHA UTAMA", fontsize=7.4, fontweight="bold", ha="right", color="#2B5FCB")


def main():
    from matplotlib.backends.backend_pdf import PdfPages
    import build_cable_layout_iso_balongan as ISO
    f1 = ISO.sheet1(title_block)
    f2 = build()
    with PdfPages(PDF) as pdf:
        pdf.savefig(f1)
        pdf.savefig(f2)
    f1.savefig(PNG.replace("skenario_S8_cable_schedule", "skenario_S8_cable_layout"), dpi=170)
    f2.savefig(PNG, dpi=170)
    plt.close("all")
    print(PDF)


if __name__ == "__main__":
    main()
