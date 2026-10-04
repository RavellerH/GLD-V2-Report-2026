# -*- coding: utf-8 -*-
"""Gabungkan Laporan FAT + seluruh lampiran (termasuk 3 Laporan Uji Lab) menjadi satu PDF
dengan halaman depan format laporan LGU (cover, kontrol dokumen, lembar pengesahan,
kata pengantar, daftar isi), halaman pemisah per lampiran, dan bookmark.

Run: python3 scripts/merge_laporan_fat_lengkap.py
Out: Paket Pertamina/09_Laporan_FAT_GLD_Tahap2/Laporan_FAT_GLD_Tahap2_Lengkap_dengan_Lampiran.pdf
"""
import os
import sys
import pymupdf

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_cover_laporan_lgu as lgu  # noqa: E402

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(REPO, "Paket Pertamina", "09_Laporan_FAT_GLD_Tahap2")
OUT = os.path.join(D, "Laporan_FAT_GLD_Tahap2_Lengkap_dengan_Lampiran.pdf")
A4 = pymupdf.paper_rect("a4")
NAVY = (0x1B / 255, 0x2A / 255, 0x4A / 255)
GREY = (0.3, 0.3, 0.3)

COVER = {
    "jenis": "Laporan Factory Acceptance Test",
    "band": "Laporan FAT\nField Testing GLD Tahap 2",
    "judul": "Laporan Factory Acceptance Test\n(FAT)",
    "sub": "Pengembangan dan Field Testing Sistem\nGas Leak Detection (GLD) Tahap 2",
    "nodok": "LGU/GLD/FAT/2026-001",
    "rev": "1.3",
    "tgl": "4 Oktober 2026",
    "pengantar": [
        "Puji syukur kami panjatkan ke hadirat Tuhan Yang Maha Esa atas rahmat dan karunia-Nya "
        "sehingga Laporan Factory Acceptance Test (FAT) pekerjaan Pengembangan dan Field Testing "
        "Sistem Gas Leak Detection (GLD) Tahap 2 ini dapat disusun dengan baik.",
        "Laporan ini menyajikan hasil pengujian perangkat GLD, Cluster Head, Gateway, dan server di "
        "laboratorium sebelum perangkat dikirim ke lokasi, mencakup tujuh item uji (FAT-01 sampai FAT-07), "
        "lembar pengesahan uji, serta lampiran bukti pendukung termasuk tiga Laporan Uji Laboratorium. "
        "Pengujian di lokasi (Site Acceptance Test dan commissioning) akan dilaporkan terpisah setelah "
        "instalasi di RU IV Cilacap. Penilaian penerimaan sepenuhnya merupakan kewenangan "
        "PT Pertamina Patra Niaga.",
        "Kami mengucapkan terima kasih kepada PT Pertamina Patra Niaga serta seluruh pihak yang telah "
        "berkontribusi dalam pelaksanaan pekerjaan ini, termasuk Lab IoT/Instrumentation and Computation "
        "Institut Teknologi Bandung. Kami terbuka terhadap saran dan masukan untuk penyempurnaan "
        "pekerjaan pada tahap berikutnya.",
    ],
}
FRONT = 5  # cover, kontrol dokumen, lembar pengesahan, kata pengantar, daftar isi

# Bab laporan FAT: (level, judul, halaman di laporan FAT)
BAB_FAT = [
    (1, "1. Dasar dan pengertian", 2),
    (1, "2. Perangkat dan konfigurasi uji", 2),
    (1, "3. Ringkasan hasil", 2),
    (1, "4. Rincian per item uji", 2),
    (1, "5. Lembar pengesahan uji", 4),
    (1, "Daftar bukti lampiran", 5),
]

LAMPIRAN = [
    ("1", "Notulen Rapat 6 Agustus 2026 (Witness PT Pertamina Patra Niaga)",
     "Notulen rapat di Lab IoT ITB yang dihadiri PT Pertamina Patra Niaga.", "Witness, FAT-06, FAT-07",
     ["Lampiran_01_Notulen_Rapat_Witness_6Agustus2026.pdf"]),
    ("2", "Hasil Uji Model AI CNN Dual-Branch",
     "Presentasi tim Lab IoT ITB: dataset, arsitektur, akurasi uji, kuantisasi, uji real-time di perangkat.",
     "FAT-01, FAT-02", ["Lampiran_02_Hasil_Uji_Model_AI_CNN_DualBranch.pdf"]),
    ("3", "Data Uji Sinyal LoRa", "Lembar kerja RSSI, SNR, dan PDR per titik uji di kampus ITB.", "FAT-03",
     ["Lampiran_03_Uji_Sinyal_LoRa.pdf"]),
    ("4", "Catatan Uji CH, Mesh, Failover, dan End-to-End (April-Juli 2026)",
     "Catatan kerja mingguan tim Lab IoT ITB (87 halaman).", "FAT-04, FAT-05",
     ["Lampiran_04_Uji_CH_Mesh_Failover_EndToEnd_Apr-Jul2026.pdf"]),
    ("5", "Technical Datasheet Rev 4.0 Lab IoT ITB",
     "Whole System, Gas Leak Detector, Cluster Head, Gateway, dan Server.", "FAT-05, konfigurasi",
     [f"Lampiran_05_Technical_Datasheet_Rev4.0/Technical-Datasheet-{n}-ID.pdf"
      for n in ["Whole-System", "GasleakDetector", "CH", "Gateway", "Server"]]),
    ("6", "Foto Unit GLD Terakit", "Unit GLD yang diuji.", "Perangkat uji",
     ["Lampiran_06_Foto_Unit_GLD_Terakit.jpg"]),
    ("7", "Laporan Uji Laboratorium 01: Model AI", "Nomor dokumen LGU/GLD/UJI-LAB/2026-001", "FAT-01, FAT-02",
     ["Lampiran_07_Laporan_Uji_Lab_01_Model_AI.pdf"]),
    ("8", "Laporan Uji Laboratorium 02: Komunikasi LoRa", "Nomor dokumen LGU/GLD/UJI-LAB/2026-002", "FAT-03",
     ["Lampiran_08_Laporan_Uji_Lab_02_Komunikasi_LoRa.pdf"]),
    ("9", "Laporan Uji Laboratorium 03: Mesh, Failover, Downlink & Integrasi",
     "Nomor dokumen LGU/GLD/UJI-LAB/2026-003", "FAT-04 s.d. FAT-07",
     ["Lampiran_09_Laporan_Uji_Lab_03_Mesh_Integrasi.pdf"]),
]


def main():
    body = pymupdf.open()
    toc = []
    out = body

    def addpdf(path):
        out.insert_pdf(pymupdf.open(os.path.join(D, path)))

    def addimg(path):
        p = out.new_page(width=A4.width, height=A4.height)
        p.insert_image(pymupdf.Rect(40, 40, A4.width - 40, A4.height - 40),
                       filename=os.path.join(D, path), keep_proportion=True)

    def sep(no, title, desc, fat):
        p = out.new_page(width=A4.width, height=A4.height)
        p.draw_rect(pymupdf.Rect(0, 0, A4.width, 70), color=None, fill=NAVY)
        p.insert_text((40, 42), "PT LAPI GANESHA UTAMA", fontsize=15, color=(1, 1, 1), fontname="hebo")
        p.insert_text((40, 60), "Laporan Factory Acceptance Test - Sistem GLD Tahap 2  |  LGU/GLD/FAT/2026-001",
                      fontsize=9, color=(0.8, 0.85, 0.9))
        p.insert_text((40, 330), f"LAMPIRAN {no}", fontsize=30, color=NAVY, fontname="hebo")
        p.insert_textbox(pymupdf.Rect(40, 350, A4.width - 40, 430), title, fontsize=17, color=NAVY, fontname="hebo")
        p.insert_textbox(pymupdf.Rect(40, 430, A4.width - 40, 520), desc, fontsize=11, color=GREY)
        p.insert_text((40, 540), f"Bukti untuk: {fat}", fontsize=11, color=GREY, fontname="heit")
        toc.append([1, f"Lampiran {no} - {title}", out.page_count])

    addpdf("00_Laporan_FAT_GLD_Tahap2.pdf")
    for no, title, desc, fat, files in LAMPIRAN:
        sep(no, title, desc, fat)
        for fn in files:
            (addimg if fn.endswith(".jpg") else addpdf)(fn)

    # halaman depan format laporan LGU, lalu isi
    out = pymupdf.open()
    lgu.cover(out, COVER)
    lgu.kontrol(out, COVER, FRONT + body.page_count)
    lgu.pengesahan(out, COVER)
    lgu.pengantar(out, COVER)
    entries = [(lvl, t, FRONT + h) for lvl, t, h in BAB_FAT]
    entries += [(1, t, FRONT + h) for _, t, h in toc]
    lgu.daftar_isi(out, entries, "Nomor halaman mengacu pada urutan halaman berkas PDF ini.")
    out.insert_pdf(body)
    outline = [[1, "Cover", 1], [1, "Lembar Pengesahan", 3], [1, "Kata Pengantar", 4], [1, "Daftar Isi", 5],
               [1, "Laporan Factory Acceptance Test (FAT)", FRONT + 1]]
    outline += [[2, t, FRONT + h] for _, t, h in BAB_FAT]
    outline += [[1, t, FRONT + h] for _, t, h in toc]
    out.set_toc(outline)
    out.set_metadata({"title": "Laporan Factory Acceptance Test (FAT) - Sistem GLD Tahap 2",
                      "author": "PT LAPI Ganesha Utama"})
    out.save(OUT, garbage=4, deflate=True)
    print(OUT, out.page_count, "halaman", round(os.path.getsize(OUT) / 1e6, 1), "MB")


if __name__ == "__main__":
    main()
