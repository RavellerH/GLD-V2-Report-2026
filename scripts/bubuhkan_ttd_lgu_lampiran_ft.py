"""Bubuhkan identitas (dan bila tersedia, gambar tanda tangan) LGU pada lembar pengesahan
di Lampiran A laporan Termin 1 Field Testing (SP-002/KPI43400/2026-S0).

Permintaan Pak Tresnandi (19 Okt 2026): "Tandatangannya LGU di lampiran laporan tolong
dibubuhkan dulu" — sebelum diajukan tanda tangan ke Pak Pindoan.

Kolom LGU yang diisi (hanya kolom LGU; kolom Lab IoT ITB & Pertamina dibiarkan kosong):
  - Laporan FAT (Lampiran A) — "Disiapkan oleh PT LAPI Ganesha Utama"
  - Laporan Uji Lab 01/02/03  — "Diperiksa oleh PT LAPI Ganesha Utama"

Gambar tanda tangan (opsional, PNG latar transparan/putih) dibaca dari TTD_IMG; stempel dari
STEMPEL_IMG. Bila tidak ada, kotak tanda tangan dibiarkan kosong untuk tanda tangan basah.

Pakai: python scripts/bubuhkan_ttd_lgu_lampiran_ft.py
"""
import os

import pymupdf

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SRC = os.path.join(ROOT, "Paket LGU", "02_Penagihan_Termin_1", "01_Laporan_Termin_1_Field_Testing_20Persen.pdf")
OUT = os.path.join(ROOT, "Paket LGU", "02_Penagihan_Termin_1",
                   "01_Laporan_Termin_1_Field_Testing_20Persen_TTD_LGU.pdf")
TTD_DIR = os.path.join(HERE, "assets", "ttd_lgu")
TTD_IMG = os.path.join(TTD_DIR, "ttd_lgu.png")
STEMPEL_IMG = os.path.join(TTD_DIR, "stempel_lgu.png")

PENANDATANGAN = {
    "nama": "Dr. Maman Budiman",
    "jabatan": "Team Leader",
    "tanggal": "5 Oktober 2026",
}
LAMPIRAN_MULAI = 16  # halaman 16 = sampul Lampiran A


def isi_kolom_lgu(page):
    heads = page.search_for("PT LAPI Ganesha Utama")
    if not heads or "engesahan" not in page.get_text():
        return False
    head = heads[-1]
    namas = [r for r in page.search_for("Nama:") if abs(r.x0 - head.x0) < 3 and r.y0 > head.y1]
    if not namas:
        return False
    nama = namas[0]
    jab = [r for r in page.search_for("Jabatan:") if abs(r.x0 - head.x0) < 3 and r.y0 > nama.y0][0]
    tgl = [r for r in page.search_for("Tanggal:") if abs(r.x0 - head.x0) < 3 and r.y0 > jab.y0][0]
    lebar = 158
    for r, teks in ((nama, PENANDATANGAN["nama"]), (jab, PENANDATANGAN["jabatan"]),
                    (tgl, PENANDATANGAN["tanggal"])):
        page.insert_text((r.x1 + 3, r.y1 - 2.2), teks, fontsize=8, fontname="helv", color=(0, 0, 0))
    area = pymupdf.Rect(head.x0 + 4, head.y1 + 12, head.x0 + lebar - 10, nama.y0 - 4)
    if os.path.exists(STEMPEL_IMG):
        page.insert_image(pymupdf.Rect(area.x0 + 30, area.y0, area.x0 + 30 + area.height, area.y1),
                          filename=STEMPEL_IMG, keep_proportion=True, overlay=True)
    if os.path.exists(TTD_IMG):
        page.insert_image(area, filename=TTD_IMG, keep_proportion=True, overlay=True)
    return True


def main():
    doc = pymupdf.open(SRC)
    hal = [i + 1 for i in range(LAMPIRAN_MULAI - 1, doc.page_count) if isi_kolom_lgu(doc[i])]
    doc.save(OUT, garbage=3, deflate=True)
    print("Kolom LGU diisi pada halaman:", hal)
    print("Gambar tanda tangan:", "ada" if os.path.exists(TTD_IMG) else "TIDAK ADA (kotak dibiarkan kosong)")
    print("->", OUT)


if __name__ == "__main__":
    main()
