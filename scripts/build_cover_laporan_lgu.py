"""Tambahkan halaman depan format laporan LGU (cover, kontrol dokumen, lembar
pengesahan, kata pengantar) ke laporan PDF yang sudah ada.

Format mengikuti contoh "LGU- Laporan AKHIR-User Requirement Specification (URS)"
yang diminta Pak Tresnandi (1 Okt 2026) untuk dokumen penagihan termin.

Pakai: py scripts/build_cover_laporan_lgu.py
"""
import os
import re
import pymupdf

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
ASSET = os.path.join(HERE, "assets", "lgu_cover")
FONT_DIR = r"C:\Windows\Fonts"
FONT_FILES = {"ar": "arial.ttf", "arb": "arialbd.ttf", "arbi": "arialbi.ttf"}
if not os.path.isdir(FONT_DIR):  # Linux: Liberation Sans (metrik sama dengan Arial)
    FONT_DIR = "/usr/share/fonts/truetype/liberation"
    FONT_FILES = {"ar": "LiberationSans-Regular.ttf", "arb": "LiberationSans-Bold.ttf",
                  "arbi": "LiberationSans-BoldItalic.ttf"}


def ff(name):
    return os.path.join(FONT_DIR, FONT_FILES[name])

RED = (196 / 255, 53 / 255, 45 / 255)
BLUE = (89 / 255, 135 / 255, 187 / 255)
TAN = (172 / 255, 163 / 255, 122 / 255)
WHITE = (1, 1, 1)
BLACK = (0, 0, 0)

W, H = pymupdf.paper_size("a4")

DOCS = [
    {
        "src": "Paket Pertamina/04_Laporan_Termin_1/Laporan_Pemenuhan_Deliverable_Termin_1_FieldTesting_GLD_Rev03.pdf",
        "lampiran_fat": "Paket Pertamina/09_Laporan_FAT_GLD_Tahap2/Laporan_FAT_GLD_Tahap2_Lengkap_dengan_Lampiran.pdf",
        "out": "Paket LGU/02_Penagihan_Termin_1/01_Laporan_Termin_1_Field_Testing_20Persen.pdf",
        "jenis": "Laporan Pemenuhan Deliverable Termin 1",
        "band": "Laporan Termin 1\nField Testing (20%)",
        "judul": "Laporan Pemenuhan Deliverable\nTermin 1 — Field Testing",
        "sub": "Pengembangan dan Field Testing Sistem\nGas Leak Detection (GLD) Tahap 2",
        "nodok": "LGU-GLD-T1-FIT-2026-001",
        "rev": "0.3",
        "tgl": "4 Oktober 2026",
        "pengantar": [
            "Puji syukur kami panjatkan ke hadirat Tuhan Yang Maha Esa atas rahmat dan karunia-Nya "
            "sehingga Laporan Pemenuhan Deliverable Termin 1 pekerjaan Pengembangan dan Field Testing "
            "Sistem Gas Leak Detection (GLD) Tahap 2 ini dapat disusun dengan baik.",
            "Laporan ini disusun sebagai dokumen pendukung pengajuan Termin 1 sebesar 20 persen. Laporan "
            "memuat pemenuhan setiap ketentuan pembayaran Termin 1, mencakup detail engineering dan desain, "
            "kesiapan komponen, konfigurasi firmware, hasil Factory Integration Test (FIT), dokumentasi "
            "instalasi dan as-built tahap laboratorium, serta register bukti pendukung. Laporan Factory "
            "Acceptance Test (FAT) beserta tiga Laporan Uji Laboratorium dan bukti pendukungnya disertakan "
            "sebagai Lampiran A. Lembar Pengesahan di halaman depan mengesahkan dokumen laporan ini; "
            "penerimaan deliverable Termin 1 dinyatakan pada Bagian 11, dan penerimaan hasil uji FAT pada "
            "Lembar Pengesahan Uji di Lampiran A. Penilaian pemenuhan dan keputusan pembayaran sepenuhnya "
            "merupakan kewenangan PT Pertamina Patra Niaga.",
            "Kami mengucapkan terima kasih kepada PT Pertamina Patra Niaga serta seluruh pihak yang telah "
            "berkontribusi dalam pelaksanaan pekerjaan ini, termasuk Lab IoT/Instrumentation and Computation "
            "Institut Teknologi Bandung. Kami terbuka terhadap saran dan masukan untuk penyempurnaan "
            "pekerjaan pada tahap berikutnya.",
        ],
    },
    {
        "src": "Paket LGU/02_Penagihan_Termin_1/src/Laporan_Termin_1_Sertifikasi_LGU.pdf",
        "out": "Paket LGU/02_Penagihan_Termin_1/03_Laporan_Termin_1_Sertifikasi_40Persen.pdf",
        "jenis": "Laporan Pemenuhan Deliverable Termin 1",
        "band": "Laporan Termin 1\nSertifikasi ATEX/IECEx (40%)",
        "judul": "Laporan Pemenuhan Deliverable\nTermin 1 — Sertifikasi",
        "sub": "Program Sertifikasi Hazardous Area (ATEX/IECEx)\nGas Leak Detector — GLD Tahap 2",
        "nodok": "LGU-GLD-T1-CERT-2026-001",
        "rev": "0.2",
        "tgl": "2 Oktober 2026",
        "pengantar": [
            "Puji syukur kami panjatkan ke hadirat Tuhan Yang Maha Esa atas rahmat dan karunia-Nya "
            "sehingga Laporan Pemenuhan Deliverable Termin 1 Program Sertifikasi Hazardous Area "
            "(ATEX/IECEx) Gas Leak Detector — GLD Tahap 2 ini dapat disusun dengan baik.",
            "Laporan ini disusun sebagai materi evaluasi Termin 1 sebesar 40 persen. Laporan menyajikan "
            "bukti pemenuhan untuk setiap syarat kontraktual Termin 1, register bukti, serta dokumen yang "
            "masih dalam penyiapan, secara apa adanya. Penilaian pemenuhan dan keputusan pembayaran "
            "sepenuhnya merupakan kewenangan PT Pertamina Patra Niaga.",
            "Kami mengucapkan terima kasih kepada PT Pertamina Patra Niaga serta seluruh pihak yang telah "
            "berkontribusi dalam pelaksanaan pekerjaan ini. Kami terbuka terhadap saran dan masukan untuk "
            "penyempurnaan pekerjaan pada tahap berikutnya.",
        ],
    },
]

TTD = {
    "tempat": "Bandung, ........ Oktober 2026",
    "team_leader": "Dr. Maman Budiman",
    "dirut": "Ir. Harry Fardiman",
    "ppn_jabatan": "Manager Domestic Product Content & Digitalization\nPT Pertamina Patra Niaga",
    "ppn_nama": "Agustinus Pindoan Panjaitan",
}


def fonts(page):
    for n in FONT_FILES:
        page.insert_font(fontname=n, fontfile=ff(n))


def text(page, rect, s, size, font="ar", color=BLACK, align=pymupdf.TEXT_ALIGN_CENTER, lh=1.25):
    r = page.insert_textbox(pymupdf.Rect(rect), s, fontsize=size, fontname=font, color=color,
                            align=align, lineheight=lh)
    assert r >= 0, (s, r)


def underline_name(page, cx, y, s, size=10.5):
    f = pymupdf.Font(fontfile=ff("arb"))
    w = f.text_length(s, fontsize=size)
    text(page, (cx - 150, y, cx + 150, y + 18), s, size, "arb")
    page.draw_line((cx - w / 2, y + size + 2), (cx + w / 2, y + size + 2), width=0.7)


def cover(doc, d):
    page = doc.new_page(width=W, height=H)
    fonts(page)
    # blok merah-biru kanan atas
    page.draw_rect(pymupdf.Rect(482, 33, 519, 69), color=None, fill=RED)
    page.draw_rect(pymupdf.Rect(482, 73, 519, 110), color=None, fill=BLUE)
    text(page, (60, 300, W - 60, 400), d["judul"], 24, "arb", lh=1.3)
    text(page, (60, 420, W - 60, 480), d["sub"], 14, "arb", lh=1.35)
    # pita bawah (logo + alamat LGU), judul pita ditulis ulang
    bh = W * 630 / 1558
    by = H - bh
    page.insert_image(pymupdf.Rect(0, by, W, H), filename=os.path.join(ASSET, "cover_band.png"))
    k = W / 1558
    page.draw_rect(pymupdf.Rect(0, by, 1249 * k, by + 172 * k), color=None, fill=TAN)
    text(page, (18, by + 8, 1240 * k, by + 172 * k), d["band"], 15, "arb", WHITE,
         pymupdf.TEXT_ALIGN_LEFT, lh=1.2)


def kontrol(doc, d, jml):
    page = doc.new_page(width=W, height=H)
    fonts(page)
    x = [60, 160, 400, 455, 535]
    y = [100, 150, 172, 194, 470, 494, 520]
    for yy in y:
        page.draw_line((x[0], yy), (x[-1], yy), width=0.6)
    for xx in (x[0], x[-1]):
        page.draw_line((xx, y[0]), (xx, y[-1]), width=0.6)
    page.draw_line((x[1], y[0]), (x[1], y[-1]), width=0.6)
    page.draw_line((x[2], y[0]), (x[2], y[-1]), width=0.6)
    page.draw_line((x[3], y[1]), (x[3], y[-1]), width=0.6)
    page.insert_image(pymupdf.Rect(x[0] + 18, y[0] + 6, x[1] - 18, y[1] - 6),
                      filename=os.path.join(ASSET, "logo_lgu.png"))
    page.insert_image(pymupdf.Rect(x[2] + 22, y[0] + 12, x[4] - 22, y[1] - 12),
                      filename=os.path.join(ASSET, "logo_pertamina.png"))
    text(page, (x[1] + 4, y[0] + 12, x[2] - 4, y[1]), d["judul"].replace("\n", " "), 8.5)
    hdr = ["No. Kontrak:", "Dokumen", "Rev", "Jml. Hal"]
    val = ["", d["jenis"], d["rev"], str(jml)]
    for i in range(4):
        al = pymupdf.TEXT_ALIGN_LEFT if i == 0 else pymupdf.TEXT_ALIGN_CENTER
        text(page, (x[i] + 4, y[1] + 6, x[i + 1] - 4, y[2]), hdr[i], 8.5, align=al)
        text(page, (x[i] + 4, y[2] + 6, x[i + 1] - 4, y[3]), val[i], 8.5, align=al)
    text(page, (x[1] + 6, 270, x[2] - 6, 380), d["judul"].replace("\n", " "), 14, "arb", lh=1.2)
    text(page, (x[1] + 6, 385, x[2] - 6, 440), d["sub"].replace("\n", " "), 10, lh=1.25)
    text(page, (x[1] + 4, y[3] + 250, x[2] - 4, y[4]), "2026", 10, "arb")
    hdr2 = ["Date", "Revision", "Prepared\nby", "Approved\nby"]
    val2 = [d["tgl"], "Rev " + d["rev"], "LGU", ""]
    for i in range(4):
        al = pymupdf.TEXT_ALIGN_LEFT if i == 0 else pymupdf.TEXT_ALIGN_CENTER
        text(page, (x[i] + 4, y[4] + 3, x[i + 1] - 4, y[5]), hdr2[i], 8.5, align=al, lh=1.1)
        text(page, (x[i] + 4, y[5] + 7, x[i + 1] - 4, y[6]), val2[i], 8.5, align=al)


def pengesahan(doc, d):
    page = doc.new_page(width=W, height=H)
    fonts(page)
    cx = W / 2
    text(page, (60, 80, W - 60, 110), "LEMBAR PENGESAHAN", 16, "arb")
    text(page, (60, 135, W - 60, 230), d["judul"].replace("\n", " ") + "\n" + d["sub"].replace("\n", " "),
         12, "arb", lh=1.45)
    text(page, (60, 245, W - 60, 290), "Dikerjakan oleh,\nPT LAPI Ganesha Utama", 10.5, lh=1.6)
    text(page, (60, 305, W - 60, 350), "Untuk\nPT Pertamina Patra Niaga", 10.5, lh=1.6)
    text(page, (60, 365, W - 60, 385), TTD["tempat"], 10.5)
    lx, rx = cx - 120, cx + 120
    text(page, (lx - 120, 395, lx + 120, 415), "Team Leader,", 10.5)
    text(page, (rx - 120, 395, rx + 120, 415), "Direktur Utama,", 10.5)
    underline_name(page, lx, 478, TTD["team_leader"])
    underline_name(page, rx, 478, TTD["dirut"])
    text(page, (60, 535, W - 60, 575), TTD["ppn_jabatan"], 10.5, "arb", lh=1.5)
    underline_name(page, cx, 650, TTD["ppn_nama"])


def pengantar(doc, d):
    page = doc.new_page(width=W, height=H)
    fonts(page)
    text(page, (60, 80, W - 60, 110), "KATA PENGANTAR", 16, "arb")
    y = 135
    for para in d["pengantar"]:
        r = pymupdf.Rect(70, y, W - 70, y + 200)
        left = page.insert_textbox(r, para, fontsize=10.5, fontname="ar", align=pymupdf.TEXT_ALIGN_JUSTIFY,
                                   lineheight=1.5)
        y = r.y1 - left + 12
    y += 20
    for s, f in [(TTD["tempat"], "ar"), ("PT LAPI Ganesha Utama", "ar")]:
        text(page, (W - 300, y, W - 70, y + 18), s, 10.5, f, align=pymupdf.TEXT_ALIGN_RIGHT)
        y += 22
    y += 55
    text(page, (W - 300, y, W - 70, y + 18), TTD["team_leader"], 10.5, align=pymupdf.TEXT_ALIGN_RIGHT)
    text(page, (W - 300, y + 22, W - 70, y + 40), "Team Leader", 10.5, align=pymupdf.TEXT_ALIGN_RIGHT)


def headings(src):
    """Judul bab (15 pt) & sub-bab (12 pt) bernomor dari laporan sumber -> (level, judul, halaman)."""
    out = []
    for i, page in enumerate(src):
        for b in page.get_text("dict")["blocks"]:
            for ln in b.get("lines", []):
                t = "".join(s["text"] for s in ln["spans"]).strip()
                sz = max(s["size"] for s in ln["spans"])
                if sz > 11.5 and re.match(r"^\d+(\.\d+)?\s", t):
                    out.append((1 if sz > 13.5 else 2, t, i + 1))
    return out


def daftar_isi(doc, entries, catatan="Nomor halaman mengikuti nomor \"Halaman\" pada laporan."):
    page = doc.new_page(width=W, height=H)
    fonts(page)
    text(page, (60, 80, W - 60, 110), "DAFTAR ISI", 16, "arb")
    far = pymupdf.Font(fontfile=ff("ar"))
    fbd = pymupdf.Font(fontfile=ff("arb"))
    rows = entries
    y = 140
    x1 = W - 70
    for lvl, judul, hal in rows:
        font, f = ("arb", fbd) if lvl == 1 else ("ar", far)
        size = 10.5 if lvl == 1 else 10
        x0 = 70 if lvl == 1 else 92
        page.insert_text((x0, y), judul, fontname=font, fontsize=size)
        if hal is not None:
            num = str(hal)
            nw = far.text_length(num, fontsize=10)
            page.insert_text((x1 - nw, y), num, fontname="ar", fontsize=10)
            start = x0 + f.text_length(judul, fontsize=size) + 6
            dots = int((x1 - nw - 6 - start) / far.text_length(".", fontsize=10))
            if dots > 0:
                page.insert_text((start, y), "." * dots, fontname="ar", fontsize=10, color=(0.45, 0.45, 0.45))
        y += 22 if lvl == 1 else 18
    page.insert_text((70, y + 14), catatan, fontname="ar",
                     fontsize=8.5, color=(0.4, 0.4, 0.4))


def fat_label(t):
    """Di dalam Lampiran A, lampiran milik Laporan FAT disebut 'Lampiran FAT n' agar tidak tertukar."""
    if t.startswith("Lampiran "):
        return "Lampiran FAT " + t[len("Lampiran "):]
    return "Isi Laporan FAT (FAT-01 s.d. FAT-07)" if t.startswith("Laporan Factory") else t


def lampiran_sep(doc, no, judul, desc, rujukan):
    page = doc.new_page(width=W, height=H)
    fonts(page)
    page.draw_rect(pymupdf.Rect(482, 33, 519, 69), color=None, fill=RED)
    page.draw_rect(pymupdf.Rect(482, 73, 519, 110), color=None, fill=BLUE)
    text(page, (60, 300, W - 60, 340), f"LAMPIRAN {no}", 26, "arb")
    text(page, (60, 350, W - 60, 400), judul, 16, "arb", lh=1.3)
    text(page, (80, 410, W - 80, 470), desc, 10.5, lh=1.4)
    text(page, (80, 480, W - 80, 520), "Dirujuk pada: " + rujukan, 10, lh=1.4, color=(0.35, 0.35, 0.35))


def build(d):
    src = pymupdf.open(os.path.join(ROOT, d["src"]))
    # Bagian "Referensi Dokumen" (daftar sumber internal) tidak disertakan pada paket penagihan.
    last = src[-1].get_text()
    if "Referensi Dokumen" in last:
        src.delete_page(src.page_count - 1)
    out = pymupdf.open()
    entries = [e for e in headings(src) if "Referensi Dokumen" not in e[1]]
    lamp, lamp_toc = None, []
    if d.get("lampiran_fat"):
        fat = pymupdf.open(os.path.join(ROOT, d["lampiran_fat"]))
        lamp = pymupdf.open()
        lampiran_sep(lamp, "A", "Laporan Factory Acceptance Test (FAT)",
                     "Nomor dokumen LGU/GLD/FAT/2026-001 Rev 1.4, beserta lampiran bukti 1-9 "
                     "(termasuk Laporan Uji Laboratorium 01, 02, dan 03).",
                     "Bagian 6 (Pelaksanaan Factory Integration Test) dan Bagian 8 (Register Bukti)")
        lamp.insert_pdf(fat, from_page=5)
        # bookmark laporan FAT tanpa halaman depannya (5 hlm)
        for lvl, t, pg in fat.get_toc():
            if pg > 5 and t not in ("Cover", "Lembar Pengesahan", "Kata Pengantar", "Daftar Isi"):
                lamp_toc.append((lvl, t, pg - 5 + 1))
    jml = 5 + src.page_count + (lamp.page_count if lamp else 0)
    cover(out, d)
    kontrol(out, d, jml)
    pengesahan(out, d)
    pengantar(out, d)
    front = 5
    base = front + src.page_count
    if lamp:
        # satu konvensi untuk seluruh daftar isi: nomor urut halaman berkas PDF
        di = [(lvl, j, front + hal) for lvl, j, hal in entries]
        di.append((1, "Lampiran A - Laporan Factory Acceptance Test (FAT)", base + 1))
        di += [(2, fat_label(t), base + pg) for lvl, t, pg in lamp_toc if lvl == 1]
        daftar_isi(out, di, "Nomor halaman mengacu pada urutan halaman berkas PDF ini.")
    else:
        daftar_isi(out, entries)
    out.insert_pdf(src)
    toc = [[1, "Cover", 1], [1, "Lembar Pengesahan", 3], [1, "Kata Pengantar", 4], [1, "Daftar Isi", 5]]
    toc += [[lvl, judul, front + hal] for lvl, judul, hal in entries]
    if lamp:
        out.insert_pdf(lamp)
        toc.append([1, "Lampiran A - Laporan Factory Acceptance Test (FAT)", base + 1])
        toc += [[min(lvl + 1, 3), fat_label(t) if lvl == 1 else t, base + pg] for lvl, t, pg in lamp_toc]
    out.set_toc(toc)
    out.set_metadata({"title": d["judul"].replace("\n", " "), "author": "PT LAPI Ganesha Utama"})
    path = os.path.join(ROOT, d["out"])
    os.makedirs(os.path.dirname(path), exist_ok=True)
    out.save(path, garbage=3, deflate=True)
    print(path, out.page_count, "hlm")


if __name__ == "__main__":
    for d in DOCS:
        build(d)
