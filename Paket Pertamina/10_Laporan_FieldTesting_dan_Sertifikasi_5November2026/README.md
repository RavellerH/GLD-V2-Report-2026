# Paket Laporan GLD Tahap 2 — Field Testing & Sertifikasi (per 5 November 2026)

Paket ini menghimpun dokumen terbaru untuk dilaporkan ke **PT Pertamina Patra Niaga**, untuk dua jalur kerja: **field testing** (pilot RU IV Cilacap, area SRU) dan **sertifikasi ATEX/IECEx** Node Sensor GLD. Mulailah dari dokumen `00`, yang merangkum status kedua jalur dan merujuk ke dokumen pendukung dengan kode yang sama dengan nama file.

| Kode | File | Isi |
|---|---|---|
| **00** | `00_Laporan_Perkembangan_GLD_FieldTesting_Sertifikasi_5November2026.{pdf,docx}` | **Dokumen utama (7 hlm).** Kurva-S program, hasil FAT, persiapan instalasi SRU sesuai MoC 15769 & HAC, status pengajuan sertifikasi, kelengkapan dokumen teknis, data uji pendukung, status Termin 1 kedua jalur, tindak lanjut per pihak |
| **01** | `01_Field_Testing/` | |
| 01-01 | `01-01_Laporan_Termin_1_Field_Testing_20Persen_Rev0.3_dengan_Laporan_FAT.pdf` | Laporan pemenuhan Termin 1 FT (rev 0.3, 5 Okt) + Lampiran A: Laporan FAT rev 1.4, bukti uji 1–9, tiga Laporan Uji Lab (140 hlm) |
| 01-02 | `01-02_Draft_BAST_Termin_1_Field_Testing_20Persen.pdf` | Draf Berita Acara Serah Terima Termin 1 FT |
| 01-03 | `01-03_Spesifikasi_Material_Instalasi_GLD_RU-IV_Rev1.5.pdf` | Spesifikasi material & kebutuhan instalasi (2 Okt) |
| 01-04 | `01-04_Daftar_Perangkat_dan_Kebutuhan_Pemasangan_GLD_Rev1.2.pdf` | Daftar perangkat & kebutuhan pemasangan (2 Okt) |
| 01-05 | `01-05_Pembagian_Persiapan_Instalasi_RU-IV_Rev1.5.pdf` | Matriks pembagian persiapan LGU / RU IV / pelaksana |
| 01-06 | `01-06_Daftar_Persiapan_Pelaksana_Instalasi_RU-IV_Rev1.2.pdf` | Daftar persiapan untuk pelaksana instalasi |
| 01-07 | `01-07_Block_Diagram_Lingkup_RU-IV_Final_8Okt2026.png` | Block diagram lingkup RU IV versi final (dengan router LGU) |
| 01-08 | `01-08_Informasi_Enclosure_Proteksi_Ledakan_GLD_HAC_SRU_Rev1.4.pdf` | Tanggapan LGU atas hasil verifikasi HAC SRU (2 Nov) |
| 01-09 | `01-09_Technical_Datasheet_Rev4.0/` | Technical Datasheet Lab IoT ITB Rev 4.0 (Whole System, GLD, CH, Gateway, Server — ID) |
| **02** | `02_Sertifikasi_ATEX_IECEx/` | |
| 02-01 | `02-01_Laporan_Termin_1_Sertifikasi_40Persen_Rev0.2.pdf` | Laporan pemenuhan Termin 1 Sertifikasi (rev 0.2, 2 Okt) |
| 02-02 | `02-02_IECEx_ATEX_Certification_Document_GLD_V2_Rev3.0.pdf` | Dokumen teknis sertifikasi (bahasa Inggris, rev 3.0, 9 Okt, 156 hlm) |
| 02-03 | `02-03_Laporan_Teknis_Pengujian_EMC_GLD_CH_Rev1.0.pdf` | Laporan pra-uji EMC di Telkom Test House (uji 15 Okt) |
| 02-04 | `02-04_Data_Pengukuran_Temperatur_MQ_30Sep2026.pdf` | Data pengukuran suhu internal (dasar kelas suhu T4) |
| 02-05 | `02-05_Formulir_Aplikasi_ATEX_GTS_29Sep2026.pdf` | Formulir aplikasi ATEX yang diajukan ke GTS |

## Catatan

- Angka progres program (63% per 5 Nov, rencana ≈73%) adalah **penilaian tim**: dua aktivitas naik sejak 30 Sep (site survey 90→100% atas dasar MoC 15769 & verifikasi HAC; lab test 72→90% atas dasar Laporan FAT, tiga Laporan Uji Lab, dan pra-uji EMC). Rincian di dokumen 00 §1.1.
- Angka sertifikasi ≈52% mengukur **kelengkapan dokumen teknis** (21 butir matriks panduan revisi), bukan kemajuan menuju terbitnya sertifikat.
- Skema sertifikasi II 2G Ex db IIC T4 Gb adalah **skema yang diajukan**; klasifikasi akhir ditentukan lembaga sertifikasi.
- Penilaian pemenuhan Termin 1 (field testing 20% dan sertifikasi 40%) sepenuhnya merupakan evaluasi Pertamina.
- MoC No. 15769/RU IV tidak disertakan karena merupakan dokumen Pertamina; dokumen 00 merujuk isinya.

Generator dokumen 00: `scripts/build_laporan_perkembangan_ft_sertifikasi_nov2026.py` → PDF via `scripts/docx_to_pdf_with_toc.py`.
