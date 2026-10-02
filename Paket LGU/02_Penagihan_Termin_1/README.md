# Dokumen Penagihan Termin 1 — GLD Tahap 2 (format cover LGU)

Laporan Termin 1 dengan halaman depan format laporan LGU (cover, lembar kontrol dokumen, lembar pengesahan, kata pengantar, daftar isi), sesuai contoh *LGU – Laporan AKHIR – User Requirement Specification (URS)* yang diminta Pak Tresnandi (1 Okt 2026).

| No | File | Isi |
|---|---|---|
| 01 | `01_Laporan_Termin_1_Field_Testing_20Persen.pdf` | Laporan pemenuhan Termin 1 Field Testing (20%), rev 0.2, 11 Sep 2026 — 5 hlm depan + 11 hlm isi |
| 02 | `02_Draft_BAST_Termin_1_Field_Testing_20Persen.{pdf,docx}` | Draf BAST pendamping dengan kop format laporan LGU (logo LGU | judul | logo Pertamina); `.docx` untuk diisi nomor/tanggal/SPK |
| 03 | `03_Laporan_Termin_1_Sertifikasi_40Persen.pdf` | Laporan pemenuhan Termin 1 Sertifikasi (40%), rev 0.1, 15 Sep 2026 — 5 hlm depan + 9 hlm isi |

## Yang masih perlu dilengkapi sebelum ditandatangani
- **No. Kontrak** di lembar kontrol dokumen (kosong).
- Team Leader: **Dr. Maman Budiman** (sudah tercantum di lembar pengesahan & kata pengantar).
- **Tanggal** pengesahan ("........ Oktober 2026").
- Nama Direktur Utama (Ir. Harry Fardiman) dan pejabat Pertamina (Agustinus Pindoan Panjaitan, Manager Domestic Product Content & Digitalization) diambil dari contoh laporan URS — mohon dicek masih sesuai untuk kontrak GLD.

Sumber: `scripts/build_cover_laporan_lgu.py` (halaman depan digabung ke PDF laporan asli di `Paket Pertamina/04_Laporan_Termin_1/`).

## Catatan penulisan status
Pada laporan Sertifikasi (03), status syarat ditulis **Tersedia / Sebagian / Dalam Penyiapan** — tidak memakai label "belum tersedia" / "belum ada" (arahan 2 Okt 2026). Substansi bukti sama dengan laporan 15 Sep; sumber varian ini `scripts/build_termin1_certification_report_lgu.py` (output antara di `src/`).
