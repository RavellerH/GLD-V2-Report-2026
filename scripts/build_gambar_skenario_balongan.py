# -*- coding: utf-8 -*-
"""Gambar teknis skematik untuk Skenario Instalasi GLD RU VI Balongan (S-1 … S-7).

Gambar ilustrasi teknis (bukan gambar kerja fabrikasi); dimensi mengikuti spesifikasi BoQ/Rencana Instalasi.
Output: scripts/assets/rab_balongan/skenario_S*.png
"""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, Polygon, Arc, Circle

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "assets", "rab_balongan")
INK, BLUE, ORG, PUR, CYA, GRN, GRY = "#262321", "#2B5FCB", "#E07B00", "#7B4FD6", "#00838F", "#3C9A3C", "#8A8F96"
STEEL, HDG, SS = "#B7BDC6", "#C9CED6", "#DDE1E6"


def new(w=11, h=7):
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_aspect("equal"); ax.axis("off")
    return fig, ax


def dim(ax, a, b, text, off=0.0, horiz=False, fs=8.5, col=INK):
    """Garis dimensi; a, b = koordinat titik, off = geser tegak lurus."""
    (x1, y1), (x2, y2) = a, b
    if horiz:
        y = y1 + off
        ax.plot([x1, x1], [y1, y], color=col, lw=0.5); ax.plot([x2, x2], [y2, y], color=col, lw=0.5)
        ax.annotate("", (x2, y), (x1, y), arrowprops=dict(arrowstyle="<->", color=col, lw=0.8))
        ax.text((x1 + x2) / 2, y, text, ha="center", va="bottom", fontsize=fs, color=col,
                bbox=dict(fc="white", ec="none", pad=0.6))
    else:
        x = x1 + off
        ax.plot([x1, x], [y1, y1], color=col, lw=0.5); ax.plot([x2, x], [y2, y2], color=col, lw=0.5)
        ax.annotate("", (x, y2), (x, y1), arrowprops=dict(arrowstyle="<->", color=col, lw=0.8))
        ax.text(x, (y1 + y2) / 2, text, ha="center", va="center", fontsize=fs, color=col, rotation=90,
                bbox=dict(fc="white", ec="none", pad=0.6))


def call(ax, xy, txt, xyt, fs=8.2, col=INK, ha="left"):
    ax.annotate(txt, xy, xytext=xyt, fontsize=fs, color=col, ha=ha, va="center",
                arrowprops=dict(arrowstyle="-", color=col, lw=0.6, shrinkA=2, shrinkB=1))


def ground(ax, x0, x1, y, depth):
    ax.plot([x0, x1], [y, y], color=INK, lw=1.4)
    step = (x1 - x0) / 40
    for i in range(41):
        x = x0 + i * step
        ax.plot([x, x - depth * 0.6], [y, y - depth], color=GRY, lw=0.5)


def earth(ax, x, y, s):
    ax.plot([x, x], [y, y - s], color=GRN, lw=1.2)
    for i, w in enumerate((1.0, 0.65, 0.3)):
        ax.plot([x - s * w * 0.5, x + s * w * 0.5], [y - s - i * s * 0.22] * 2, color=GRN, lw=1.2)


def title(fig, code, text, note="Gambar ilustrasi teknis — bukan gambar kerja fabrikasi. Dimensi dalam mm kecuali disebut lain."):
    fig.text(0.01, 0.985, f"{code}  {text}", fontsize=12.5, fontweight="bold", color=INK, va="top")
    fig.text(0.01, 0.012, note, fontsize=7.6, color="#555555", va="bottom", style="italic")
    fig.text(0.99, 0.012, "LGU · GLD Tahap 2 · RU VI Balongan · Skenario Instalasi", fontsize=7.6, color="#555555",
             va="bottom", ha="right")


def save(fig, name):
    p = os.path.join(OUT, name)
    fig.savefig(p, dpi=200, bbox_inches="tight", pad_inches=0.12, facecolor="white")
    plt.close(fig)
    return p


def block(ax, x, y, w, h, t, sub=None, fc="white", ec=INK, fs=9, lw=1.2):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.08", fc=fc, ec=ec, lw=lw))
    if sub:
        ax.text(x + w / 2, y + h * 0.64, t, ha="center", va="center", fontsize=fs, fontweight="bold", color=INK)
        ax.text(x + w / 2, y + h * 0.28, sub, ha="center", va="center", fontsize=fs - 1.8, color="#444444")
    else:
        ax.text(x + w / 2, y + h / 2, t, ha="center", va="center", fontsize=fs, fontweight="bold", color=INK)


# ---------------------------------------------------------------- S-1 diagram satu garis
def s1():
    fig, ax = new(12, 6.6); ax.set_xlim(0, 24); ax.set_ylim(0, 13)
    ax.add_patch(Rectangle((0.3, 1.2), 7.2, 10.8, fc="#F3F6FB", ec=GRY, lw=0.8, ls="--"))
    ax.text(0.5, 11.75, "PANEL RU VI (safe area)", fontsize=9, fontweight="bold", color="#4A5568")
    ax.add_patch(Rectangle((9.0, 1.2), 14.7, 10.8, fc="#FFF8EE", ec=GRY, lw=0.8, ls="--"))
    ax.text(9.2, 11.75, "LAPANGAN — lantai dasar WHB", fontsize=9, fontweight="bold", color="#4A5568")
    block(ax, 0.8, 9.6, 2.6, 1.4, "220 VAC", "sumber panel/UPS", fc="#EEF3FC")
    block(ax, 1.4, 6.6, 3.0, 1.6, "PSU 24 VDC", "HDR-60-24 · 2,5 A", fc="#FFF1E0")
    block(ax, 1.4, 3.0, 3.0, 1.6, "PSU 5 VDC", "HDR-15-5 · 2,4 A", fc="#F1EBFF")
    ax.plot([1.0, 1.0], [9.6, 3.8], color=INK, lw=1.2)
    ax.plot([1.0, 1.4], [7.4, 7.4], color=INK, lw=1.2); ax.plot([1.0, 1.4], [3.8, 3.8], color=INK, lw=1.2)
    ax.text(0.75, 6.0, "L/N 220 VAC", rotation=90, fontsize=7, va="center")
    for lab, y, c in (("F1 · 24 VDC", 7.4, ORG), ("F2 · 5 VDC", 3.8, PUR)):
        ax.plot([4.4, 4.8], [y, y], color=INK, lw=1.1)
        ax.add_patch(Rectangle((4.8, y - 0.2), 0.9, 0.4, fc="white", ec=INK, lw=1)); ax.plot([4.8, 5.7], [y, y], color=INK, lw=0.8)
        ax.text(5.25, y + 0.38, lab, ha="center", fontsize=7.4)
    ax.text(5.25, 2.3, "Fuse terminal + LED (D.3)\n1 per keluaran PSU", ha="center", fontsize=7.2, color="#444444")
    ax.plot([5.7, 6.9, 6.9], [7.4, 7.4, 7.25], color=ORG, lw=1.6)
    ax.plot([5.7, 6.9, 6.9], [3.8, 3.8, 7.25], color=PUR, lw=1.6)
    ax.plot([6.9, 7.6], [7.25, 7.25], color=INK, lw=3.4)
    ax.add_patch(Rectangle((7.6, 6.7), 0.35, 1.1, fc="#CCCCCC", ec=INK, lw=0.8)); ax.text(7.78, 6.4, "B.3", fontsize=7, ha="center")
    ax.plot([7.95, 10.4], [7.25, 7.25], color=INK, lw=3.4)
    ax.text(9.2, 9.6, "1 kabel NYFGbY 4×1,5 mm²\npanel → JB ± 30 m\n(+24/−24/+5/−5 VDC)", fontsize=7.6, ha="center")
    ax.plot([9.2, 9.2], [9.1, 7.6], color=GRY, lw=0.6)
    # JB
    ax.add_patch(FancyBboxPatch((10.6, 5.6), 3.6, 3.4, boxstyle="round,pad=0.02,rounding_size=0.1", fc="#E9ECF1", ec=INK, lw=1.6))
    ax.text(12.4, 8.65, "JB Ex d (A.1)", ha="center", fontsize=9, fontweight="bold")
    ax.text(12.4, 8.25, "Helon HLBH31 · 4 entry", ha="center", fontsize=7.4)
    for i, t in enumerate(["24V+", "24V−", "5V+", "5V−", "PE"]):
        ax.add_patch(Rectangle((10.95 + i * 0.6, 6.6), 0.5, 1.1, fc="white", ec=INK, lw=0.7))
        ax.text(11.2 + i * 0.6, 6.15, t, ha="center", fontsize=6.4)
    for y in (7.25,):
        ax.add_patch(Rectangle((10.4, y - 0.13), 0.2, 0.26, fc="#B08D57", ec=INK, lw=0.6))
    ax.text(10.5, 5.35, "gland Ex d (B.1)", fontsize=7, ha="center")
    outs = [("GLD-01", 10.5, "± 16 m", ORG, "24 VDC ± 10 %"), ("GLD-02", 7.4, "± 16 m", ORG, "24 VDC ± 10 %"),
            ("CH-01", 3.6, "± 14 m", PUR, "5 VDC ± 5 %")]
    for name, y, L, c, v in outs:
        ax.add_patch(Rectangle((14.2, y - 0.13 if False else 0, ), 0, 0))
        ax.add_patch(Rectangle((14.2, 7.25 - (outs.index((name, y, L, c, v))) * 0.5 - 0.13), 0.2, 0.26, fc="#B08D57", ec=INK, lw=0.6))
        y0 = 7.25 - outs.index((name, y, L, c, v)) * 0.5
        ax.plot([14.4, 16.2, 16.2, 18.6], [y0, y0, y, y], color=c, lw=2.4)
        ax.text(17.3, y + 0.25, f"armoured {L}", ha="center", fontsize=7.4)
        ax.add_patch(Rectangle((18.6, y - 0.13), 0.2, 0.26, fc="#B08D57", ec=INK, lw=0.6))
        block(ax, 18.8, y - 0.8, 3.6, 1.6, name, v, fc="#FFF1E0" if c == ORG else "#F1EBFF")
        earth(ax, 22.9, y - 0.2, 0.35) if name != "CH-01" else None
    ax.text(23.25, 8.9, "PE/\nground", fontsize=6.8, color=GRN, ha="center")
    earth(ax, 12.4, 5.6, 0.4); ax.text(12.9, 4.9, "grounding JB (F.3)", fontsize=7, color=GRN)
    ax.text(16.6, 1.6, "Catatan: GLD tanpa baterai (terminal BAT kosong). CH-02 mandiri panel surya, tanpa kabel daya.\n"
                       "GW-01 dicatu adaptor 5 VDC di dalam kantor lewat kabel NYY ± 22 m (lihat S-6).",
            fontsize=7.4, ha="center", color="#444444")
    title(fig, "Gambar S-1.", "Diagram satu garis catu daya", note="Diagram skematik — panjang kabel asumsi, diverifikasi di lapangan (HP-1).")
    return save(fig, "skenario_S1_satu_garis.png")


# ---------------------------------------------------------------- S-2 jaringan & data
def s2():
    fig, ax = new(12, 5.4); ax.set_xlim(0, 24); ax.set_ylim(0, 10.5)
    zones = [(0.3, 5.6, "Lantai dasar WHB"), (6.2, 4.2, "Luar struktur"), (10.6, 4.6, "Atap carport"), (15.4, 8.3, "Dalam kantor (jaringan lokal tertutup)")]
    for x, w, t in zones:
        ax.add_patch(Rectangle((x, 1.0), w, 8.6, fc="#F7F9FC", ec=GRY, lw=0.8, ls="--"))
        ax.text(x + 0.2, 9.3, t, fontsize=8.2, fontweight="bold", color="#4A5568")
    block(ax, 0.8, 6.6, 2.4, 1.4, "GLD-01", "24 VDC", fc="#FFF1E0")
    block(ax, 0.8, 2.4, 2.4, 1.4, "GLD-02", "24 VDC", fc="#FFF1E0")
    block(ax, 3.7, 4.5, 2.0, 1.4, "CH-01", "5 VDC", fc="#F1EBFF")
    block(ax, 7.3, 4.5, 2.2, 1.4, "CH-02", "panel surya", fc="#F1EBFF")
    block(ax, 11.6, 4.5, 2.6, 1.4, "GW-01", "Gateway 5 VDC", fc="#E0F4F6")
    block(ax, 16.0, 4.5, 2.4, 1.4, "Router", "Wi-Fi 2,4 GHz", fc="#EEF3FC")
    ax.add_patch(FancyBboxPatch((19.3, 2.0), 4.1, 6.6, boxstyle="round,pad=0.02,rounding_size=0.1", fc="#EEF3FC", ec=INK, lw=1.3))
    ax.text(21.35, 8.15, "PC server lokal", ha="center", fontsize=9.5, fontweight="bold")
    for i, t in enumerate(["Broker MQTT", "Node-RED (decode)", "Database", "Backend + dashboard"]):
        ax.add_patch(Rectangle((19.6, 6.9 - i * 1.15), 3.5, 0.85, fc="white", ec=GRY, lw=0.8))
        ax.text(21.35, 7.32 - i * 1.15, t, ha="center", va="center", fontsize=8)

    def lora(a, b, t, yo=0.35):
        ax.annotate("", b, a, arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=1.6, ls=(0, (4, 2))))
        ax.text((a[0] + b[0]) / 2, (a[1] + b[1]) / 2 + yo, t, ha="center", fontsize=7.6, color=BLUE,
                bbox=dict(fc="white", ec="none", pad=0.5))
    lora((3.2, 7.2), (3.9, 5.9), "± 16 m", 0.4); lora((3.2, 3.2), (3.9, 4.5), "± 12 m", -0.6)
    lora((5.7, 5.2), (7.3, 5.2), "± 37 m"); lora((9.5, 5.2), (11.6, 5.2), "± 78 m")
    ax.text(7.0, 3.3, "LoRa 920–921 MHz (mesh)\nnormal: pull ± 90 s · alarm: push ± 10 s", fontsize=7.4, color=BLUE, ha="center")
    ax.annotate("", (16.0, 5.2), (14.2, 5.2), arrowprops=dict(arrowstyle="<|-|>", color=CYA, lw=1.6, ls=(0, (1, 1.5))))
    ax.text(15.1, 5.55, "Wi-Fi", ha="center", fontsize=7.6, color=CYA)
    ax.text(15.1, 4.55, "MQTT", ha="center", fontsize=7.0, color=CYA)
    ax.annotate("", (19.3, 5.2), (18.4, 5.2), arrowprops=dict(arrowstyle="<|-|>", color=INK, lw=1.6))
    ax.text(18.85, 5.55, "LAN", ha="center", fontsize=7.6); ax.text(18.85, 4.55, "Cat6", ha="center", fontsize=7.0)
    ax.plot([21.35, 21.35], [2.0, 1.4], color=GRY, lw=1.2, ls="--")
    ax.text(21.35, 1.15, "NIC-2 → intranet kantor (opsional, izin IT RU VI)", ha="center", fontsize=7.2, color="#555555")
    ax.text(16.0, 2.4, "Tanpa internet/WAN.\nIP tetap untuk GW & PC.", fontsize=7.2, color="#555555")
    title(fig, "Gambar S-2.", "Diagram jaringan dan alur data",
          note="Jarak dari peta (posisi ditandai 27 Nov 2026), diverifikasi di lapangan. Jalur GW → router via Wi-Fi masih menunggu konfirmasi RU VI.")
    return save(fig, "skenario_S2_jaringan.png")


# ---------------------------------------------------------------- S-3 GLD
def s3():
    fig, (ax, bx) = plt.subplots(1, 2, figsize=(12, 8.2), gridspec_kw={"width_ratios": [1.55, 1]})
    for a in (ax, bx):
        a.set_aspect("equal"); a.axis("off")
    ax.set_xlim(-900, 900); ax.set_ylim(-260, 1700)
    ground(ax, -850, 850, 0, 60)
    ax.text(420, -120, "Lantai beton WHB", fontsize=8)
    # pelat dasar & anchor
    ax.add_patch(Rectangle((-120, 0), 240, 10, fc=HDG, ec=INK, lw=1))
    for x in (-90, 90):
        ax.plot([x, x], [-70, 22], color=INK, lw=1.6); ax.add_patch(Rectangle((x - 12, 10), 24, 10, fc=INK))
    # stanchion
    ax.add_patch(Rectangle((-30, 10), 60, 1000, fc=HDG, ec=INK, lw=1.1)); ax.add_patch(Rectangle((-34, 1010), 68, 8, fc=INK))
    # pelat U-bolt
    ax.add_patch(Rectangle((30, 690), 5, 250, fc=SS, ec=INK, lw=1))
    for y in (745, 885):
        ax.add_patch(Arc((0, y), 76, 76, theta1=90, theta2=270, color=INK, lw=1.4))
        ax.plot([0, 50], [y + 38, y + 38], color=INK, lw=1.4); ax.plot([0, 50], [y - 38, y - 38], color=INK, lw=1.4)
        ax.add_patch(Rectangle((35, y + 30), 14, 16, fc=INK)); ax.add_patch(Rectangle((35, y - 46), 14, 16, fc=INK))
    # unit GLD
    ax.add_patch(FancyBboxPatch((50, 670), 170, 290, boxstyle="round,pad=0,rounding_size=14", fc="#F2F2F2", ec=INK, lw=1.5))
    ax.text(135, 815, "GLD", ha="center", fontsize=12, fontweight="bold")
    ax.add_patch(FancyBboxPatch((220, 735), 34, 160, boxstyle="round,pad=0,rounding_size=10", fc="#2F6FD0", ec=INK, lw=1.2))
    ax.add_patch(Rectangle((254, 760), 12, 110, fc="white", ec=INK, lw=1, hatch="xxxx"))
    ax.plot([135, 135], [960, 1240], color=INK, lw=3); ax.add_patch(Circle((135, 1245), 9, fc=INK))
    ax.add_patch(Rectangle((150, 640), 26, 30, fc="#B08D57", ec=INK, lw=0.8))
    # kabel + drip loop
    ax.plot([163, 163, 300, 300, 260, 260, 820], [640, 520, 520, 300, 300, 40, 40], color=ORG, lw=2.6)
    ax.annotate("", (860, 40), (800, 40), arrowprops=dict(arrowstyle="-|>", color=ORG, lw=1.6))
    ax.text(700, 80, "ke JB di tengah klaster (± 16 m)", fontsize=7.8, ha="center", color=ORG)
    # grounding
    ax.plot([-120, -260, -260], [5, 5, -20], color=GRN, lw=1.4); earth(ax, -260, -20, 40)
    ax.text(-560, -215, "Grounding stanchion (F.3)\nNYA hijau-kuning 6 mm²", fontsize=7.4, color=GRN, ha="center")
    # callouts
    call(ax, (-30, 400), "Stanchion pipa 2\" Sch 40 HDG\nOD 60,3 mm (E.1)", (-880, 460))
    call(ax, (-100, 5), "Pelat dasar 240 × 240 × 10\n4 chemical anchor", (-880, 230))
    call(ax, (32, 900), "Pelat U-bolt SS304\n250 × 250 × 5 (E.3)", (-880, 1060))
    call(ax, (-20, 745), "2 U-bolt 2\" M10 + mur", (-880, 780))
    call(ax, (266, 815), "Mesh sensor DI DEPAN (tutup depan\nbermesh), menghadap area pantau —\ntidak boleh tertutup", (420, 900))
    call(ax, (163, 652), "Gland Ex d M20 (B.1) di bawah", (420, 640))
    call(ax, (135, 1150), "Antena LoRa — tegak,\nbebas dari pelat logam", (420, 1250))
    call(ax, (300, 410), "Drip loop", (420, 410))
    dim(ax, (-120, 0), (-120, 1010), "1000", off=-80)
    dim(ax, (-120, 0), (120, 0), "240", off=-150, horiz=True)
    ax.text(-880, 1620, "TAMPAK SAMPING", fontsize=9.5, fontweight="bold")
    # tampak depan pelat
    bx.set_xlim(-260, 260); bx.set_ylim(-330, 330)
    bx.add_patch(Rectangle((-30, -240), 60, 520, fc=HDG, ec=INK, lw=1, ls="--"))
    bx.add_patch(Rectangle((-125, -125), 250, 250, fc=SS, ec=INK, lw=1.3))
    for y in (-70, 70):
        for x in (-45, 45):
            bx.add_patch(Circle((x, y), 6, fc="white", ec=INK, lw=0.9))
        bx.plot([-45, 45], [y, y], color=INK, lw=2.2)
    bx.add_patch(FancyBboxPatch((-100, -110), 200, 220, boxstyle="round,pad=0,rounding_size=12", fc="none", ec=GRY, lw=1, ls=":"))
    dim(bx, (-125, 125), (125, 125), "250", off=45, horiz=True)
    dim(bx, (-125, -125), (-125, 125), "250", off=-55)
    dim(bx, (-45, -70), (45, -70), "± 90 (U-bolt M10)", off=-90, horiz=True, fs=7.6)
    bx.text(0, -300, "Pipa 2\" di belakang pelat (garis putus)\nGaris titik = outline unit GLD", ha="center", fontsize=7.4, color="#555555")
    bx.text(-250, 305, "TAMPAK DEPAN PELAT", fontsize=9.5, fontweight="bold")
    title(fig, "Gambar S-3.", "Detail pemasangan GLD-01 / GLD-02 di stanchion 1 m",
          note="Ilustrasi teknis — bukan gambar kerja fabrikasi. Dimensi mm; unit GLD = casing mesh depan (dimensi indikatif). Acuan: Gambar L-1/L-2 desain bracket LGU.")
    return save(fig, "skenario_S3_gld.png")


# ---------------------------------------------------------------- S-4 CH-01
def s4():
    fig, ax = new(10, 7.6); ax.set_xlim(-1100, 1300); ax.set_ylim(-260, 2300)
    ground(ax, -1050, 1250, 0, 70); ax.text(560, -150, "Lantai dasar WHB (bawah struktur)", fontsize=8)
    ax.add_patch(Rectangle((-120, 0), 240, 10, fc=HDG, ec=INK, lw=1))
    for x in (-90, 90):
        ax.plot([x, x], [-70, 22], color=INK, lw=1.6); ax.add_patch(Rectangle((x - 12, 10), 24, 10, fc=INK))
    ax.add_patch(Rectangle((-30, 10), 60, 1490, fc=HDG, ec=INK, lw=1.1)); ax.add_patch(Rectangle((-34, 1500), 68, 8, fc=INK))
    ax.add_patch(Rectangle((30, 1150), 6, 360, fc=SS, ec=INK, lw=1))
    for y in (1210, 1450):
        ax.add_patch(Arc((0, y), 76, 76, theta1=90, theta2=270, color=INK, lw=1.4))
        ax.plot([0, 50], [y + 38, y + 38], color=INK, lw=1.4); ax.plot([0, 50], [y - 38, y - 38], color=INK, lw=1.4)
    ax.add_patch(FancyBboxPatch((50, 1170), 220, 320, boxstyle="round,pad=0,rounding_size=12", fc="#EFE8FF", ec=INK, lw=1.5))
    ax.text(160, 1330, "CH-01", ha="center", fontsize=8.5, fontweight="bold")
    ax.plot([160, 160], [1490, 1900], color=INK, lw=3); ax.add_patch(Circle((160, 1905), 12, fc=INK))
    ax.add_patch(Rectangle((200, 1140), 30, 30, fc="#B08D57", ec=INK, lw=0.8))
    ax.plot([215, 215, 300, 300, 260, 260, 1150], [1140, 1020, 1020, 760, 760, 40, 40], color=PUR, lw=2.6)
    ax.annotate("", (1220, 40), (1130, 40), arrowprops=dict(arrowstyle="-|>", color=PUR, lw=1.6))
    ax.text(820, 100, "kabel armoured 5 VDC ke JB ± 14 m", fontsize=7.8, ha="center", color=PUR)
    ax.plot([-120, -330, -330], [5, 5, -20], color=GRN, lw=1.4); earth(ax, -330, -20, 40)
    ax.text(-560, -215, "Grounding stanchion (F.3)", fontsize=7.4, color=GRN, ha="center")
    call(ax, (160, 1750), "Antena LoRa tegak, tidak\nterhalang struktur di atasnya", (480, 2100))
    call(ax, (36, 1480), "Bracket CH (E.4) + 2 U-bolt 2\" M10", (480, 1750))
    call(ax, (215, 1150), "Gland (B.1)", (480, 1300))
    call(ax, (300, 900), "Kabel diklem ke stanchion\n+ drip loop", (480, 900))
    call(ax, (-30, 700), "Stanchion pipa 2\" Sch 40 HDG\n1,5 m (E.7)", (-1060, 820))
    call(ax, (-100, 5), "Pelat dasar 240 × 240 × 10\n4 chemical anchor", (-1060, 340))
    dim(ax, (-120, 0), (-120, 1500), "1 500", off=-110)
    ax.text(-1060, 2200, "TAMPAK SAMPING", fontsize=9.5, fontweight="bold")
    ax.text(-1060, 1700, "Posisi: di tengah GLD-01 (± 16 m)\ndan GLD-02 (± 12 m), di bawah\nstruktur WHB. Tiang sendiri,\ntanpa klem ke struktur existing.\nTanpa panel surya.",
            fontsize=7.8, color="#444444", va="top")
    title(fig, "Gambar S-4.", "Detail pemasangan CH-01 di stanchion sendiri 1,5 m",
          note="Ilustrasi teknis — bukan gambar kerja fabrikasi. Dimensi mm; dimensi unit CH indikatif.")
    return save(fig, "skenario_S4_ch01.png")


# ---------------------------------------------------------------- S-5 CH-02
def s5():
    fig, ax = new(10, 9); ax.set_xlim(-3.4, 3.6); ax.set_ylim(-0.6, 7.4)
    ground(ax, -3.3, 3.5, 0, 0.12); ax.text(-3.25, -0.33, "Permukaan tanah/beton di luar struktur WHB", fontsize=8)
    ax.add_patch(Rectangle((-0.3, -0.25), 0.6, 0.25, fc="#C8C3B8", ec=INK, lw=0.8))
    ax.add_patch(Rectangle((-0.13, 0), 0.26, 0.012, fc=HDG, ec=INK))
    ax.add_patch(Rectangle((-0.03, 0.01), 0.06, 6.0, fc=HDG, ec=INK, lw=1)); ax.add_patch(Rectangle((-0.035, 6.0), 0.07, 0.03, fc=INK))
    # unit CH ± 4,2 m, antena di atas — bebas halangan
    ax.add_patch(FancyBboxPatch((0.04, 4.0), 0.3, 0.42, boxstyle="round,pad=0,rounding_size=0.03", fc="#EFE8FF", ec=INK, lw=1.4))
    ax.text(0.19, 4.21, "CH", ha="center", fontsize=8, fontweight="bold")
    ax.plot([0.19, 0.19], [4.42, 5.2], color=INK, lw=2.4); ax.add_patch(Circle((0.19, 5.21), 0.03, fc=INK))
    # 1 panel surya ± 2,5 m, DI BAWAH unit CH
    cx, cy = 0.62, 2.5
    pts = [(cx - 0.5, cy - 0.07), (cx + 0.5, cy + 0.07), (cx + 0.5, cy + 0.14), (cx - 0.5, cy)]
    ax.add_patch(Polygon(pts, closed=True, fc="#2E4A7D", ec=INK, lw=1))
    ax.plot([0.03, 0.15], [2.45, 2.45], color=INK, lw=2); ax.plot([0.15, 0.62], [2.45, 2.52], color=INK, lw=1.6)
    ax.plot([1.12, 1.12, 0.4, 0.4, 0.3], [2.6, 3.3, 3.3, 4.0, 4.0], color=INK, lw=0.8, ls="--")
    # grounding
    ax.plot([0.13, 1.0, 1.0], [0.005, 0.005, -0.1], color=GRN, lw=1.3); earth(ax, 1.0, -0.1, 0.12)
    call(ax, (0.19, 5.0), "Antena LoRa tegak di atas CH —\nbebas halangan panel", (1.4, 5.6))
    call(ax, (0.34, 4.2), "Unit CH-02 + bracket CH (E.4)\nbaterai CH di dalam unit", (1.4, 4.45))
    call(ax, (0.4, 3.6), "Kabel panel → CH,\ndiklem UV ke tiang", (1.4, 3.6))
    call(ax, (1.0, 2.6), "1 panel surya + bracket (E.5) DI BAWAH CH\nmenghadap UTARA, kemiringan ± 10–15°", (1.4, 2.95))
    call(ax, (0.02, 1.4), "Stanchion pipa 2\" Sch 40 HDG\n6 m, 1 batang (E.2)", (1.4, 1.75))
    call(ax, (0.2, 0.0), "Pelat dasar 240 × 240 × 10\n+ 4 chemical anchor", (1.4, 0.85))
    call(ax, (1.0, -0.15), "Grounding (F.3)", (2.2, 0.25))
    dim(ax, (-0.13, 0), (-0.13, 6.0), "6,0 m", off=-1.2)
    dim(ax, (-0.13, 0), (-0.13, 4.21), "± 4,2 m (CH)", off=-0.8)
    dim(ax, (-0.13, 0), (-0.13, 2.5), "± 2,5 m (panel)", off=-0.4)
    ax.text(-3.3, 7.15, "TAMPAK SAMPING", fontsize=9.5, fontweight="bold")
    ax.text(-3.3, 6.9, "Urutan:\n1. Anchor & curing 24 jam\n2. Uji link di titik rencana\n3. Rakit CH + panel di bawah\n4. Dirikan tiang (izin ketinggian,\n    min. 3 orang + tali pengarah)\n5. Cek pengisian & RSSI",
            fontsize=7.8, color="#444444", va="top")
    title(fig, "Gambar S-5.", "Detail pemasangan CH-02 di stanchion 6 m — CH ± 4,2 m, 1 panel surya di bawahnya",
          note="Ilustrasi teknis — bukan gambar kerja fabrikasi. Dimensi m; tinggi indikatif. Panel di bawah CH agar antena LoRa bebas.")
    return save(fig, "skenario_S5_ch02.png")


# ---------------------------------------------------------------- S-6 Gateway, router, server
def s6():
    fig, ax = new(12, 7.6); ax.set_xlim(-1.0, 13.0); ax.set_ylim(-0.7, 6.9)
    ground(ax, -0.9, 12.9, 0, 0.12)
    # gedung kantor
    ax.add_patch(Rectangle((6.0, 0), 6.6, 3.5, fc="#F4F1EA", ec=INK, lw=1.4))
    ax.text(10.9, 3.15, "Gedung kantor", fontsize=9, fontweight="bold")
    ax.add_patch(Rectangle((6.0, 1.0), 0.06, 1.2, fc="#A9D3F5", ec=INK, lw=0.6)); ax.text(5.95, 1.6, "jendela", fontsize=6.8, ha="right")
    # carport
    ax.add_patch(Polygon([(0.0, 3.92), (6.0, 4.05), (6.0, 4.12), (0.0, 3.99)], fc="#BFC5CC", ec=INK, lw=1.1))
    for x in (0.25, 3.0):
        ax.add_patch(Rectangle((x, 0), 0.14, 3.92, fc="#D9D9D9", ec=INK, lw=0.8))
        for k in range(6):
            ax.add_patch(Rectangle((x, 0.2 + k * 0.25), 0.14, 0.12, fc="#F2C200" if k % 2 == 0 else "#262321", lw=0))
    ax.text(2.0, 4.35, "Atap carport (seng)", fontsize=8)
    # siku + GW + antena (tepi atap, sisi kiri)
    ax.plot([0.05, 0.35], [4.0, 4.0], color=INK, lw=3); ax.plot([0.05, 0.05], [4.0, 4.5], color=INK, lw=3)
    ax.add_patch(FancyBboxPatch((-0.12, 4.5), 0.34, 0.32, boxstyle="round,pad=0,rounding_size=0.03", fc="#DFF3F5", ec=INK, lw=1.4))
    ax.text(0.05, 4.66, "GW", ha="center", fontsize=8, fontweight="bold")
    ax.plot([0.05, 0.05], [4.82, 5.75], color="#4FB3E8", lw=3); ax.add_patch(Circle((0.05, 5.76), 0.045, fc="#4FB3E8"))
    # kabel NYY ke dalam kantor
    ax.plot([0.15, 0.4, 0.4, 0.55, 0.55, 6.0, 6.3, 6.3, 6.9], [4.5, 4.5, 4.3, 4.3, 3.8, 3.8, 3.8, 1.05, 1.05], color=INK, lw=1.6)
    ax.add_patch(Circle((6.0, 3.8), 0.07, fc="#E0A03C", ec=INK, lw=0.6))
    # dalam kantor: adaptor+UPS, router, PC
    block(ax, 6.9, 0.15, 1.5, 0.5, "UPS / stopkontak", fs=7.2, fc="white")
    block(ax, 6.9, 0.85, 1.0, 0.4, "Adaptor 5 V", fs=6.8, fc="#FFF1E0")
    ax.add_patch(Rectangle((6.4, 1.6), 2.2, 0.06, fc=INK)); ax.plot([6.5, 6.5], [0, 1.6], color=INK, lw=1); ax.plot([8.5, 8.5], [0, 1.6], color=INK, lw=1)
    block(ax, 6.5, 1.66, 1.0, 0.36, "Router", fs=7.4, fc="#EEF3FC")
    for r in (0.25, 0.42, 0.6):
        ax.add_patch(Arc((7.0, 2.02), r, r, theta1=40, theta2=140, color=CYA, lw=1))
    ax.add_patch(Rectangle((9.4, 0), 0.7, 1.35, fc="#E9ECF1", ec=INK, lw=1)); ax.text(9.75, 0.7, "PC\nserver", ha="center", fontsize=7.2, fontweight="bold")
    ax.add_patch(Rectangle((10.5, 1.6), 1.3, 0.06, fc=INK)); ax.add_patch(Rectangle((10.75, 1.66), 0.8, 0.55, fc="#DDE6F5", ec=INK, lw=0.8))
    ax.text(11.15, 1.93, "layar", ha="center", fontsize=6.6)
    ax.plot([7.5, 9.0, 9.0, 9.4], [1.84, 1.84, 0.9, 0.9], color=BLUE, lw=1.6)
    ax.text(8.6, 2.0, "LAN Cat6", fontsize=7, color=BLUE)
    ax.plot([10.1, 10.6, 10.6], [0.4, 0.4, -0.05], color=GRY, lw=1.2, ls="--"); ax.text(10.65, 0.15, "NIC-2 intranet\n(opsional)", fontsize=6.6, color="#555555")
    # wifi link
    ax.annotate("", (6.4, 2.0), (0.25, 4.6), arrowprops=dict(arrowstyle="<|-|>", color=CYA, lw=1.4, ls=(0, (1, 1.5))))
    ax.text(4.6, 2.3, "Wi-Fi 2,4 GHz\n(GW ↔ router)", fontsize=7.6, color=CYA, ha="center")
    # callouts & dims
    call(ax, (0.05, 5.4), "Antena Gateway di atas GW", (1.6, 6.05))
    call(ax, (0.22, 4.68), "GW-01 di atas siku", (1.6, 5.55))
    call(ax, (0.3, 4.02), "Siku L 50×50×5 HDG: tegak ± 0,5 m +\nkaki ± 0,3 m dibaut ke tepi atap (E.6)", (1.6, 4.95))
    call(ax, (3.0, 3.8), "Kabel NYY 2×1,5 mm² ± 22 m\ndalam conduit + klem (C.2, C.3)", (0.75, 2.55))
    call(ax, (6.0, 3.8), "Tembusan dinding disegel", (6.4, 4.5))
    dim(ax, (0.05, 0), (0.05, 3.98), "± 4,0 m", off=-0.6)
    dim(ax, (0.05, 4.0), (0.05, 4.5), "0,5", off=-0.35, fs=7.4)
    ax.text(-0.9, 6.6, "POTONGAN — carport & gedung kantor", fontsize=9.5, fontweight="bold")
    title(fig, "Gambar S-6.", "Detail Gateway di tepi atap carport, router dan PC server di dalam kantor",
          note="Ilustrasi teknis — skala tidak tepat. Dimensi dalam m. Lokasi router dekat jendela sisi carport untuk sinyal Wi-Fi terbaik.")
    return save(fig, "skenario_S6_gateway_server.png")


# ---------------------------------------------------------------- S-7 JB
def s7():
    fig, ax = new(10, 6.4); ax.set_xlim(0, 20); ax.set_ylim(0, 12.5)
    ax.add_patch(FancyBboxPatch((4.5, 3.2), 9, 7.4, boxstyle="round,pad=0.02,rounding_size=0.3", fc="#E9ECF1", ec=INK, lw=2))
    ax.text(9.0, 10.0, "JB Ex d 4 entry — Helon HLBH31 (A.1)", ha="center", fontsize=8.8, fontweight="bold")
    ax.text(9.0, 9.4, "Ex d · 4 entry M20 · IP66 · aluminium alloy · ready stock", ha="center", fontsize=7.8)
    labels = ["24V+", "24V−", "5V+", "5V−", "PE"]
    for i, t in enumerate(labels):
        x = 5.6 + i * 1.5
        ax.add_patch(Rectangle((x, 6.2), 1.1, 2.0, fc="white", ec=INK, lw=1))
        ax.text(x + 0.55, 8.5, t, ha="center", fontsize=8.5, fontweight="bold",
                color=ORG if "24" in t else (PUR if "5V" in t else GRN))
    ax.add_patch(Rectangle((5.4, 5.9), 7.6, 0.25, fc=GRY, ec=INK, lw=0.6)); ax.text(9.2, 5.45, "rel DIN + terminal block", ha="center", fontsize=7.4)
    entries = [("E1", "IN 24 & 5 VDC\n4 inti, panel", INK), ("E2", "OUT GLD-01\n± 16 m", ORG),
               ("E3", "OUT GLD-02\n± 16 m", ORG), ("E4", "OUT CH-01\n± 14 m", PUR)]
    for i, (e, t, c) in enumerate(entries):
        x = 5.8 + i * 2.0
        ax.add_patch(Rectangle((x, 2.6), 0.7, 0.6, fc="#B08D57", ec=INK, lw=0.8))
        ax.plot([x + 0.35, x + 0.35], [2.6, 1.6], color=c, lw=2.4)
        ax.text(x + 0.35, 3.55, e, ha="center", fontsize=7.6, fontweight="bold")
        ax.text(x + 0.35, 1.0, t, ha="center", fontsize=7, va="center")
    ax.text(9.2, 0.15, "Keempat entry terisi cable gland Ex d M20 (B.1) — tidak ada entry kosong, sehingga tidak perlu stopping plug.",
            ha="center", fontsize=7.6, color="#444444")
    earth(ax, 14.2, 4.5, 0.6); ax.plot([13.5, 14.2], [4.5, 4.5], color=GRN, lw=1.2)
    ax.text(14.9, 3.6, "Grounding JB (F.3)\nke titik ground RU VI", fontsize=7.4, color=GRN)
    ax.text(14.6, 8.6, "Pemasangan:\n• di tengah antara\n  GLD-01 & GLD-02\n• dibaut ke struktur/stanchion\n• entry menghadap ke bawah\n• tidak ada PSU di dalam JB\n• torsi tutup & gland\n  sesuai pabrikan",
            fontsize=7.6, va="top", color="#333333")
    ax.text(0.2, 8.6, "Pengkabelan:\nE1 → 24V+/24V−/5V+/5V−\nE2, E3 → 24V+/24V−\nE4 → 5V+/5V−\nPE → armour & earth\nArmour kabel dijepit\ndi cone gland",
            fontsize=7.6, va="top", color="#333333")
    title(fig, "Gambar S-7.", "Tata letak junction box (JB) dan entry kabel",
          note="Ilustrasi teknis — susunan terminal final mengikuti unit dari pabrikan.")
    return save(fig, "skenario_S7_jb.png")


if __name__ == "__main__":
    for f in (s1, s2, s3, s4, s5, s6, s7):
        print(f())
