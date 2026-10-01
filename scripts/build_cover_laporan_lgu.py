"""Tambahkan halaman depan format laporan LGU (cover, kontrol dokumen, lembar
pengesahan, kata pengantar) ke laporan PDF yang sudah ada.

Format mengikuti contoh "LGU- Laporan AKHIR-User Requirement Specification (URS)"
yang diminta Pak Tresnandi (1 Okt 2026) untuk dokumen penagihan termin.

Pakai: py scripts/build_cover_laporan_lgu.py
"""
import os
import pymupdf

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
ASSET = os.path.join(HERE, "assets", "lgu_cover")
FONT_DIR = r"C:\Windows\Fonts"

RED = (196 / 255, 53 / 255, 45 / 255)
BLUE = (89 / 255, 135 / 255, 187 / 255)
TAN = (172 / 255, 163 / 255, 122 / 255)
WHITE = (1, 1, 1)
BLACK = (0, 0, 0)

W, H = pymupdf.paper_size("a4")

DOCS = [
    {
        "src": "Paket Pertamina/04_Laporan_Termin_1/Laporan_Pemenuhan_Deliverable_Termin_1_FieldTesting_GLD_Rev02.pdf",
        "out": "Paket LGU/02_Penagihan_Termin_1/01_Laporan_Termin_1_Field_Testing_20Persen.pdf",
        "jenis": "Laporan Pemenuhan Deliverable Termin 1",
        "band": "Laporan Termin 1\nField Testing (20%)",
        "judul": "Laporan Pemenuhan Deliverable\nTermin 1 — Field Testing",
        "sub": "Pengembangan dan Field Testing Sistem\nGas Leak Detection (GLD) Tahap 2",
        "nodok": "LGU-GLD-T1-FIT-2026-001",
        "rev": "0.2",
        "tgl": "11 September 2026",
        "pengantar": [
            "Puji syukur kami panjatkan ke hadirat Tuhan Yang Maha Esa atas rahmat dan karunia-Nya "
            "sehingga Laporan Pemenuhan Deliverable Termin 1 pekerjaan Pengembangan dan Field Testing "
            "Sistem Gas Leak Detection (GLD) Tahap 2 ini dapat disusun dengan baik.",
            "Laporan ini disusun sebagai dokumen pendukung pengajuan Termin 1 sebesar 20 persen. Laporan "
            "memuat pemenuhan setiap ketentuan pembayaran Termin 1, mencakup detail engineering dan desain, "
            "kesiapan komponen, konfigurasi firmware, hasil Factory Integration Test (FIT), dokumentasi "
            "instalasi dan as-built tahap laboratorium, serta register bukti pendukung. Penilaian pemenuhan "
            "dan keputusan pembayaran sepenuhnya merupakan kewenangan PT Pertamina Patra Niaga.",
            "Kami mengucapkan terima kasih kepada PT Pertamina Patra Niaga serta seluruh pihak yang telah "
            "berkontribusi dalam pelaksanaan pekerjaan ini, termasuk Lab IoT/Instrumentation and Computation "
            "Institut Teknologi Bandung. Kami terbuka terhadap saran dan masukan untuk penyempurnaan "
            "pekerjaan pada tahap berikutnya.",
        ],
    },
    {
        "src": "Paket Pertamina/04_Laporan_Termin_1/Laporan_Pemenuhan_Deliverable_Termin_1_Sertifikasi_GLD.pdf",
        "out": "Paket LGU/02_Penagihan_Termin_1/03_Laporan_Termin_1_Sertifikasi_40Persen.pdf",
        "jenis": "Laporan Pemenuhan Deliverable Termin 1",
        "band": "Laporan Termin 1\nSertifikasi ATEX/IECEx (40%)",
        "judul": "Laporan Pemenuhan Deliverable\nTermin 1 — Sertifikasi",
        "sub": "Program Sertifikasi Hazardous Area (ATEX/IECEx)\nGas Leak Detector — GLD Tahap 2",
        "nodok": "LGU-GLD-T1-CERT-2026-001",
        "rev": "0.1",
        "tgl": "15 September 2026",
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
    "team_leader": "(.......................................)",
    "dirut": "Ir. Harry Fardiman",
    "ppn_jabatan": "Manager Domestic Product Content & Digitalization\nPT Pertamina Patra Niaga",
    "ppn_nama": "Agustinus Pindoan Panjaitan",
}


def fonts(page):
    page.insert_font(fontname="ar", fontfile=os.path.join(FONT_DIR, "arial.ttf"))
    page.insert_font(fontname="arb", fontfile=os.path.join(FONT_DIR, "arialbd.ttf"))
    page.insert_font(fontname="arbi", fontfile=os.path.join(FONT_DIR, "arialbi.ttf"))


def text(page, rect, s, size, font="ar", color=BLACK, align=pymupdf.TEXT_ALIGN_CENTER, lh=1.25):
    r = page.insert_textbox(pymupdf.Rect(rect), s, fontsize=size, fontname=font, color=color,
                            align=align, lineheight=lh)
    assert r >= 0, (s, r)


def underline_name(page, cx, y, s, size=10.5):
    f = pymupdf.Font(fontfile=os.path.join(FONT_DIR, "arialbd.ttf"))
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


def build(d):
    src = pymupdf.open(os.path.join(ROOT, d["src"]))
    out = pymupdf.open()
    jml = 4 + src.page_count
    cover(out, d)
    kontrol(out, d, jml)
    pengesahan(out, d)
    pengantar(out, d)
    out.insert_pdf(src)
    out.set_metadata({"title": d["judul"].replace("\n", " "), "author": "PT LAPI Ganesha Utama"})
    path = os.path.join(ROOT, d["out"])
    os.makedirs(os.path.dirname(path), exist_ok=True)
    out.save(path, garbage=3, deflate=True)
    print(path, out.page_count, "hlm")


if __name__ == "__main__":
    for d in DOCS:
        build(d)
