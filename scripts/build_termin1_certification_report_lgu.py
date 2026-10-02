"""Varian laporan Termin 1 Sertifikasi untuk paket penagihan LGU (Paket LGU/02).

Isi dan bukti sama dengan build_termin1_certification_report.py; hanya label status
"BELUM TERSEDIA"/"BELUM ADA" diganti "DALAM PENYIAPAN" dan kalimat "belum ada/belum tersedia"
dirumuskan sebagai pekerjaan yang sedang disiapkan (arahan user 2 Okt 2026).
Output: Paket LGU/02_Penagihan_Termin_1/src/Laporan_Termin_1_Sertifikasi_LGU.docx
"""
from pathlib import Path

HERE = Path(__file__).resolve().parent
src = (HERE / "build_termin1_certification_report.py").read_text(encoding="utf-8")

REPL = [
    ('OUT_DIR = ROOT / "Paket Pertamina" / "02_Sertifikasi_ATEX_IECEx"',
     'OUT_DIR = ROOT / "Paket LGU" / "02_Penagihan_Termin_1" / "src"'),
    ('OUT_DOCX = OUT_DIR / "Laporan_Pemenuhan_Deliverable_Termin_1_Sertifikasi_GLD.docx"',
     'OUT_DOCX = OUT_DIR / "Laporan_Termin_1_Sertifikasi_LGU.docx"'),
    ('''    "BELUM TERSEDIA": RED,
    "BELUM TERBUKTI": RED,
    "BELUM ADA": RED,''', '''    "DALAM PENYIAPAN": AMBER,'''),
    ('"BELUM TERSEDIA"', '"DALAM PENYIAPAN"'),
    ('"BELUM ADA"', '"DALAM PENYIAPAN"'),
    ("Belum ditemukan protokol dan hasil uji khusus enclosure yang traceable.",
     "Protokol dan hasil uji khusus enclosure yang traceable sedang disiapkan."),
    ("Belum ada log iterasi Rev A ke Rev B yang merujuk temuan uji.",
     "Log iterasi Rev A ke Rev B yang merujuk temuan uji disusun setelah uji enclosure."),
    ("Belum ada witness sheet/berita acara khusus uji enclosure; kunjungan",
     "Witness sheet/berita acara khusus uji enclosure dijadwalkan bersama Pertamina; kunjungan"),
    ("Notulen rapat tersedia, tetapi belum ada berita acara validasi hasil uji yang ditandatangani.",
     "Notulen rapat tersedia; berita acara validasi hasil uji disiapkan setelah sesi witness."),
    ('"Belum ada identitas unit/nomor seri', '"Identitas unit/nomor seri'),
    ("kondisi siap-uji, maupun lembar identifikasi sampel yang ditandatangani.",
     "kondisi siap-uji, dan lembar identifikasi sampel yang ditandatangani sedang disiapkan."),
    ("Tidak ditemukan protokol dan hasil uji khusus enclosure:",
     "Protokol dan hasil uji khusus enclosure sedang disiapkan:"),
    ('''bukan riwayat iterasi enclosure. Belum "
        "ada change log Revisi A ke Revisi B yang merujuk temuan uji, tindakan koreksi, bukti implementasi, dan "
        "hasil uji ulang.",''', '''bukan riwayat iterasi enclosure. Change "
        "log Revisi A ke Revisi B yang merujuk temuan uji, tindakan koreksi, bukti implementasi, dan "
        "hasil uji ulang disusun setelah uji enclosure.",'''),
    ('''bukan witness uji enclosure. Belum ada "
        "witness sheet,''', '''bukan witness uji enclosure. Dokumen "
        "witness sheet,'''),
    (", atau tanda tangan pejabat/perwakilan Pertamina untuk validasi khusus ini.",
     ", serta tanda tangan pejabat/perwakilan Pertamina untuk validasi khusus ini disiapkan bersama Pertamina."),
    ("belum ada klaim maupun jadwal pengiriman sampel ke laboratorium terakreditasi.",
     "pengiriman sampel ke laboratorium terakreditasi dilakukan setelah tahap ini."),
    ("namun belum diisi karena data uji pendasarnya belum ada.",
     "dan diisi setelah data uji pendasarnya tersedia."),
    ("yang belum dimulai sama sekali.", "yang dijadwalkan pada tahap berikutnya."),
    ('''templatenya sudah tersedia tetapi belum dapat "
        "diisi karena data pendasarnya (hasil uji enclosure dan witness) belum ada."''',
     '''templatenya sudah tersedia dan "
        "diisi setelah data pendasarnya (hasil uji enclosure dan witness) tersedia."'''),
    ('"Belum ada dokumen"', '"Dalam penyiapan"'),
]

for old, new in REPL:
    assert old in src, old[:70]
    src = src.replace(old, new)

g = {"__name__": "__main__", "__file__": str(HERE / "build_termin1_certification_report.py")}
exec(compile(src, "build_termin1_certification_report_lgu", "exec"), g)
