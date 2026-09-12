# Sertifikasi ATEX / IECEx — GLD (Node Sensor)

Dokumen pelacakan progres proyek sertifikasi kepatuhan area berbahaya untuk perangkat **GLD (Node Sensor)** — mencakup 4 track paralel: **ATEX** (Directive 2014/34/EU, Kategori 2G Zona 1), **IP66/67** (IEC 60529), **EMC** (EN 61000-6-2/-4), dan **RF** (ETSI/SDPPI), sesuai lingkup proposal sertifikasi formal (21 Februari 2026, aktif sejak Kick-Off 12 Juni 2026, estimasi durasi 5–8 bulan).

**Scope perangkat: GLD (Node Sensor) saja.** Cluster Head dan Gateway tidak termasuk dalam proyek sertifikasi maupun RAB saat ini — proposal formal secara konsisten menjelaskan satu perangkat (8 sensor MQx + processing + LoRa + enclosure), dan hal ini dikonfirmasi langsung ke tim penyusun dokumen ini.

## Isi folder

| File | Isi |
|---|---|
| `Dashboard_Sertifikasi_GLD_ATEX_IECEx.{html,pdf}` | Kurva-S sertifikasi (4 track), rekomendasi skema klasifikasi (grup gas/kelas suhu/zona), gap analysis dokumentasi teknis per track, isu kritis & gate terbuka |
| `Persiapan_Termin_1.md` | Audit kesiapan bukti kontraktual Termin 1 skema sertifikasi dua termin, matriks gap, kriteria keluar, dan urutan kerja |
| `Template_Log_Uji_dan_Iterasi_Enclosure.md` | Form kerja untuk identitas sampel, hasil pengujian, temuan, perubahan desain, retest, dan witness |
| `Template_Berita_Acara_Validasi_Prototipe.md` | Draft berita acara witness dan validasi prototipe oleh para pihak |
| `Template_Laporan_Pekerjaan_Termin_1.md` | Kerangka laporan pekerjaan Termin 1 beserta daftar lampiran wajib |

## Ringkasan status (per 12 September 2026)

- **Progres keseluruhan proyek (5-fase, termasuk uji lab): ≈23%** (naik dari ≈20% per 5 Sep) — angka paling konservatif, memperhitungkan bahwa fase Uji Lab Terakreditasi (bobot terbesar timeline, 41,7%) belum dimulai sama sekali.
- **Kesiapan internal pra-submission: ≈48%** (naik dari ≈42% per 5 Sep). Pendorong utama kenaikan: enclosure **GLD ATEX Case v3** memperoleh gambar teknik berdimensi (8 Sep) dan unit fisiknya sudah terakit (10 Sep), serta dokumen teknis submission Bagian 2–3 dilengkapi. Angka ini murni bagian yang ada di tangan tim, tidak termasuk pengujian di lab akreditasi.
- ⚠️ **Termin 1 SPK sertifikasi (40%) belum dapat diajukan** — prototipe enclosure kini tersedia, tetapi protokol & hasil uji enclosure, witness/validasi Pertamina atas uji tersebut, berita acara, dan laporan pekerjaan belum ada. Angka kesiapan ≈48% **bukan** pengganti acceptance milestone pembayaran. Rincian → bagian 09 pada `Dashboard_Sertifikasi_GLD_ATEX_IECEx.html` dan `Persiapan_Termin_1.md`.
- ⚠️ **Tiga isu Ex baru dari desain v3**: DC fan di ruang sensor (sumber nyala potensial, tanpa sertifikat Ex), jendela kaca transparan (wajib uji impact & thermal shock IEC 60079-0), dan mounting lug cor yang berbeda dari basis desain bracket U-bolt yang sudah diserahkan ke vendor.
- Skema target yang sudah ditetapkan proposal: **Zona 1, Kategori 2G, Grup II, kelas suhu T4 (≤135°C)**.
- Yang masih terbuka: grup gas spesifik (rekomendasi tim: **IIC**, karena H₂ termasuk gas target), metode proteksi (Ex i vs Ex d), gambar teknik enclosure, BOM per-komponen, dan verifikasi suhu elemen sensing sensor gas — lihat dashboard untuk detail lengkap per item.

## Catatan penting

⚠️ **Skema klasifikasi (grup gas/kelas suhu/zona) yang direkomendasikan dalam dashboard ini adalah hasil analisis tim penyusun dokumen — bukan keputusan resmi dari notified body atau lembaga sertifikasi (ExCB).** Wajib dikonfirmasi lebih lanjut sebelum dipakai sebagai acuan pengujian final. Seluruh angka progres bersifat estimasi interpretatif, bukan hasil audit resmi — dijelaskan metodologinya secara terbuka di bagian akhir dashboard.

⚠️ **Status Termin 1 per 10 September 2026: belum siap diajukan.** Bukti keberadaan prototipe sudah ada, tetapi bukti uji enclosure, iterasi berbasis hasil uji, witness/validasi Pertamina, berita acara, dan laporan pekerjaan khusus Termin 1 belum ditemukan di repo. Lihat `Persiapan_Termin_1.md`.
