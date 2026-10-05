# Dokumen Penagihan Termin 1 — GLD Tahap 2 (format cover LGU)

Laporan Termin 1 dengan halaman depan format laporan LGU (cover, lembar kontrol dokumen, lembar pengesahan, kata pengantar, daftar isi), sesuai contoh *LGU – Laporan AKHIR – User Requirement Specification (URS)* yang diminta Pak Tresnandi (1 Okt 2026).

| No | File | Isi |
|---|---|---|
| 01 | `01_Laporan_Termin_1_Field_Testing_20Persen.{pdf,docx}` | Laporan pemenuhan Termin 1 Field Testing (20%), **rev 0.3, 5 Okt 2026** — 5 hlm depan + 10 hlm isi + **Lampiran A: Laporan FAT rev 1.4 lengkap dengan lampiran bukti 1–9** (termasuk 3 Laporan Uji Lab) — PDF 140 hlm (±6,5 MB). `.docx` (±10 MB) berisi bagian yang sama: halaman depan, isi laporan, Laporan FAT & 3 Laporan Uji Lab dapat diedit; bukti FAT 1–6 berupa gambar halaman. Dibangun `scripts/build_word_termin1_ft_lengkap.py` (Linux, tanpa Word COM). |
| 02 | `02_Draft_BAST_Termin_1_Field_Testing_20Persen.{pdf,docx}` | Draf BAST pendamping dengan kop format laporan LGU (logo LGU | judul | logo Pertamina); `.docx` untuk diisi nomor/tanggal/SPK |
| 03 | `03_Laporan_Termin_1_Sertifikasi_40Persen.{pdf,docx}` | Laporan pemenuhan Termin 1 Sertifikasi (40%), rev 0.2, 2 Okt 2026 — status diperbarui (uji termal 30 Sep, pengajuan GTS ±29 Sep, Ex d) — 5 hlm depan + 9 hlm isi (Referensi Dokumen internal tidak disertakan) |

## Yang masih perlu dilengkapi sebelum ditandatangani
- **No. Kontrak** di lembar kontrol dokumen (kosong).
- Team Leader: **Dr. Maman Budiman** (sudah tercantum di lembar pengesahan & kata pengantar).
- **Tanggal** pengesahan ("........ Oktober 2026").
- Nama Direktur Utama (Ir. Harry Fardiman) dan pejabat Pertamina (Agustinus Pindoan Panjaitan, Manager Domestic Product Content & Digitalization) diambil dari contoh laporan URS — mohon dicek masih sesuai untuk kontrak GLD.

Sumber: `scripts/build_cover_laporan_lgu.py` (halaman depan digabung ke PDF laporan asli di `Paket Pertamina/04_Laporan_Termin_1/`).

## Catatan penulisan status
Pada laporan Sertifikasi (03), status syarat ditulis **Tersedia / Sebagian / Dalam Penyiapan** — tidak memakai label "belum tersedia" / "belum ada" (arahan 2 Okt 2026). Rev 0.2 memperbarui bukti ke status 2 Okt 2026; sumber varian ini `scripts/build_termin1_certification_report_lgu.py` (output antara di `src/`).

Versi Word (`.docx`) dibangun oleh `scripts/build_word_penagihan_lgu.py` (halaman depan dapat diedit: No. Kontrak, tanggal, nama penandatangan). Folder `src/` berisi berkas antara.
