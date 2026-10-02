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
    # --- pembaruan status per 2 Okt 2026 (rev 0.2) ---
    ('("Revisi", "0.1")', '("Revisi", "0.2")'),
    ('("Tanggal", "15 September 2026")', '("Tanggal", "2 Oktober 2026")'),
    ("seluruh bukti dan kekurangan yang teridentifikasi terhadap syarat Termin 1 ",
     "seluruh bukti pemenuhan dan pekerjaan lanjutan terhadap syarat Termin 1 "),
    ("pengembang serta kekurangan yang masih teridentifikasi terhadap syarat kontraktual, tanpa menyimpulkan ",
     "pengembang serta pekerjaan lanjutan yang sedang disiapkan terhadap syarat kontraktual, tanpa menyimpulkan "),
    ('bold_lead="Kekurangan teridentifikasi. "', 'bold_lead="Tindak lanjut. "'),
    ('"Ringkasan bukti/kekurangan"', '"Ringkasan bukti dan tindak lanjut"'),
    ("Bagian ini merinci bukti yang ditemukan dan kekurangan yang teridentifikasi untuk setiap syarat pada ",
     "Bagian ini merinci bukti yang ditemukan dan tindak lanjut untuk setiap syarat pada "),
    ("berdasarkan audit repo dokumentasi proyek per 15 September 2026.",
     "berdasarkan status pekerjaan per 2 Oktober 2026."),
    ("disusun dari seluruh bukti yang ada di repo per 15 September 2026.",
     "disusun dari seluruh bukti pekerjaan per 2 Oktober 2026."),
    ("identitas sampel/nomor seri/revisi belum ditetapkan formal.",
     "nomor seri sampel GLD2-0x1001 telah ditetapkan pada formulir aplikasi; lembar identifikasi sampel bertanda tangan sedang disiapkan."),
    ('"DALAM PENYIAPAN", "Protokol dan hasil uji khusus enclosure yang traceable sedang disiapkan."',
     '"SEBAGIAN", "Uji termal internal 30 Sep 2026 telah dilaksanakan (8 titik thermocouple, 3 kondisi beban, 180 menit); uji mekanik, sealing/IP pra-uji, dan fault condition sedang disiapkan."'),
    ("Sertifikasi masih tahap persiapan dokumen; sampel belum dikirim ke laboratorium sehingga urutan tahap masih terjaga.",
     "Formulir aplikasi dan dossier teknis telah diajukan ke GTS (agen sertifikasi) sekitar 29 Sep 2026; pengujian di laboratorium terakreditasi dilakukan sesudah tahap ini, sehingga urutan tahap terjaga."),
    ('2, "Prototipe telah diuji", "DALAM PENYIAPAN",', '2, "Prototipe telah diuji", "SEBAGIAN",'),
    ('menetapkan jenis pre-compliance test yang direncanakan.",',
     'menetapkan jenis pre-compliance test yang direncanakan. Uji termal internal telah dilaksanakan pada "\n'
     '        "30 September 2026: 8 titik thermocouple pada kondisi normal, beban maksimum, dan kipas mati selama "\n'
     '        "180 menit. Ekstrapolasi ke suhu ambien +60 °C memberikan suhu titik terpanas ± 114 °C, di bawah "\n'
     '        "batas efektif kelas suhu T4 (130 °C).",'),
    ("Protokol dan hasil uji khusus enclosure sedang disiapkan: inspeksi mekanik/dimensi, uji termal/hotspot, ",
     "Uji lanjutan khusus enclosure sedang disiapkan: inspeksi mekanik/dimensi, pelengkapan titik ukur termal, "),
    ('''Bukti kematangan fungsi sistem di atas "
        "tidak menggantikan pengujian enclosure ini.",''', '''Hasil uji termal internal akan "
        "dilengkapi dan disaksikan dalam sesi uji bersama Pertamina.",'''),
    ('''Status proyek per pertengahan September 2026 menyatakan sertifikasi masih pada "
        "tahap persiapan dokumen; ''', '''Formulir aplikasi ATEX dan dossier teknis telah diajukan ke GTS (agen "
        "sertifikasi) sekitar 29 September 2026; '''),
    ("sertifikasi dengan dua metrik yang tidak saling menggantikan:", "sertifikasi dengan metrik berikut:"),
    ('''        ("Progres keseluruhan proyek (5 fase x 4 track, bottom-up)", "≈ 20% (per 5 September 2026)", "Metrik paling konservatif — memasukkan fase Uji Laboratorium Terakreditasi (bobot 41,7% dari total durasi) yang dijadwalkan pada tahap berikutnya."),
        ("Kesiapan dokumen ATEX (checklist teknis 29 item)", "≈ 43%", "Murni kelengkapan dokumentasi/checklist teknis, tidak termasuk pelaksanaan pengujian."),''',
     '''        ("Kesiapan dokumen sertifikasi (21 butir checklist ExCB, berbobot)", "≈ 43% (per 30 September 2026)", "Kelengkapan dokumentasi teknis; tidak termasuk pelaksanaan pengujian di laboratorium."),
        ("Pengajuan ke agen sertifikasi (GTS)", "Diajukan ± 29 September 2026", "Formulir aplikasi ATEX + dossier teknis; iterasi dokumen mengikuti tanggapan GTS."),
        ("Uji termal internal", "Dilaksanakan 30 September 2026", "Indikasi positif kelas suhu T4 (± 114 °C vs batas 130 °C)."),'''),
    ("Kedua metrik ini adalah indikator", "Metrik ini adalah indikator"),
    ('''gas spesifik (rekomendasi tim: IIC) dan metode proteksi (Ex i atau Ex d) masih terbuka dan menjadi "
        "bagian dari pekerjaan uji lanjutan. Detail lengkap Kurva-S dan gap analysis per track ada di "
        "`Dashboard_Sertifikasi_GLD_ATEX_IECEx.html`."''',
     '''gas IIC dan metode proteksi Ex d (flameproof enclosure) telah ditetapkan, dengan penandaan yang "
        "diajukan II 2G Ex db IIC T4 Gb."'''),
    ('"6 Dokumen yang Masih Perlu Disusun"', '"6 Dokumen Tahap Lanjutan"'),
    ('''serta kekurangan yang masih "
        "teridentifikasi terhadap ketujuh''', '''serta pekerjaan lanjutan "
        "terhadap ketujuh'''),
    ('''"Tim pengembang tidak menyimpulkan sendiri apakah paket ini layak atau belum layak diajukan untuk "
        "pembayaran 40 persen — penilaian''', '''"Berdasarkan bukti tersebut, LGU mengajukan pembayaran Termin 1 sebesar 40 persen; "
        "penilaian'''),
    ("`Persiapan_Termin_1.md` (identitas prototipe", "kerangka kerja tim (identitas prototipe"),
    ("seluruh bukti dan kekurangan di atas", "seluruh bukti dan tindak lanjut di atas"),
    ('"Checklist dan analisis kekurangan sertifikasi"', '"Checklist dan analisis kesiapan sertifikasi"'),
    ('"`checklist-sertifikasi.html`, `laporan-analisis-kekurangan.html`, `status-kekurangan.html`."',
     '"Checklist sertifikasi, laporan analisis kesiapan, dan status per butir."'),
    ('"DALAM PENYIAPAN", "Log iterasi Rev A ke Rev B yang merujuk temuan uji disusun setelah uji enclosure."',
     '"SEBAGIAN", "Iterasi desain tersedia: PCB Node Sensor GLD telah melalui lima versi (V1 hingga V5) dan casing berkembang dari ATEX Casing v2 ke v3 (8 Sep 2026). Log keterkaitan revisi dengan temuan uji sedang dirangkum."'),
    ('3, "Ada iterasi perbaikan desain berbasis hasil uji", "DALAM PENYIAPAN",',
     '3, "Ada iterasi perbaikan desain berbasis hasil uji", "SEBAGIAN",'),
    ("""Terdapat file desain `ATEX CASING v2` dan desain bracket U-bolt sebagai versi "
        "desain terkini.",""",
     """Iterasi desain perangkat keras telah dilakukan pada dua komponen "
        "utama: (1) PCB Node Sensor GLD telah melalui lima versi, V1 hingga V5 (Gambar 3.3): V1 memuat soket "
        "delapan sensor MQ langsung pada papan utama; versi berikutnya memakai modul sensor MQ terpisah dengan "
        "penyempurnaan tata letak motherboard; V5 menggunakan susunan beberapa papan dengan konektor antar-papan "
        "dan terminal blok untuk kabel daya. Dokumentasi BOM dan layout PCB (EasyEDA) tersedia per 9–11 "
        "September 2026; (2) casing berkembang dari ATEX Casing v2 (desain mounting "
        "U-bolt) ke GLD ATEX Case v3 (8 September 2026) dengan mesh filter stainless steel, kipas DC, dan "
        "dimensi yang disesuaikan untuk kebutuhan sertifikasi Ex d.","""),
    ("""Desain tersebut terutama memodelkan assembly mounting/bracket, bukan riwayat iterasi enclosure. Change "
        "log Revisi A ke Revisi B yang merujuk temuan uji, tindakan koreksi, bukti implementasi, dan "
        "hasil uji ulang disusun setelah uji enclosure.",""",
     """Change log formal yang menautkan setiap revisi dengan temuan uji, tindakan koreksi, bukti "
        "implementasi, dan hasil uji ulang (termasuk hasil uji termal 30 September 2026) sedang dirangkum.","""),
    ("Tujuh foto perakitan pada `Sumber Dokumen/sertifikasi-atex-gld-v2-2026/GLD/`, ", "Tujuh foto perakitan prototipe, "),
    ("`ATEX CASING v2` (STEP/OBJ) dan `Desain_Bracket_L_UBolt_GLD_Mounting.pdf`.", "gambar CAD ATEX Casing v2 (STEP/OBJ) dan desain bracket U-bolt."),
    ("Basis desain mekanik enclosure dan mounting, `GLD U Bolt Bracket/`.", "Basis desain mekanik enclosure dan mounting."),
    ("""    sub(
        4, "Disaksikan dan divalidasi Pertamina",""", """    _pcb = ROOT / "scripts" / "assets" / "pcb_iterasi" / "gld_pcb_v1_v5.png"
    if _pcb.exists():
        _p = doc.add_paragraph()
        _p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        _p.add_run().add_picture(str(_pcb), width=Inches(6.3))
        add_caption(doc, "Gambar 3.3 Iterasi PCB Node Sensor GLD, versi V1 hingga V5 (tampak atas dan bawah)")
    sub(
        4, "Disaksikan dan divalidasi Pertamina","""),
    ("3 foto urutan perakitan + 4 foto komponen di `sertifikasi-atex-gld-v2-2026/GLD/`.", "3 foto urutan perakitan dan 4 foto komponen."),
    ('"`Dokumen_spesifikasi_input_2.docx`, `Parameter spesifikasi EMC_lengkap.docx`."', '"Spesifikasi input sertifikasi dan parameter uji EMC."'),
    ('"Dashboard Sertifikasi GLD ATEX/IECEx", "Kurva-S, gap analysis 4 track, dan rubrik interpretasi progres."',
     '"Dashboard Sertifikasi GLD ATEX/IECEx", "Kurva-S dan pemantauan progres 4 jalur sertifikasi."'),
    ('"Persiapan_Termin_1.md dan 3 template kerja", "Matriks gap awal (10 September 2026) dan template log uji, berita acara, serta laporan pekerjaan."',
     '"Rencana kerja Termin 1 dan template kerja", "Rencana kerja (10 September 2026) serta template log uji, berita acara, dan laporan pekerjaan."'),
    ('"`Template_Log_Uji_dan_Iterasi_Enclosure.md`"', '"Template tersedia"'),
    ('"`Template_Berita_Acara_Validasi_Prototipe.md`"', '"Template tersedia"'),
    ("Template kerja tersedia di \"\n        \"`Template_Berita_Acara_Validasi_Prototipe.md` dan diisi", "Template kerja telah \"\n        \"tersedia dan diisi"),
]

for old, new in REPL:
    assert old in src, old[:70]
    src = src.replace(old, new)

g = {"__name__": "__main__", "__file__": str(HERE / "build_termin1_certification_report.py")}
exec(compile(src, "build_termin1_certification_report_lgu", "exec"), g)
