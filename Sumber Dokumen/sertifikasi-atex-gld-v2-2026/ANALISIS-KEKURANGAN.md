# Analisis Kekurangan — Persiapan Sertifikasi IECEx/ATEX GLD V2 2026

Dokumen ini membandingkan persyaratan pada `IECEx ATEX Certification Information Requirements_Ind.docx` dengan dokumen yang sudah ada (`Dokumen_spesifikasi_input_2.docx`, `Parameter spesifikasi EMC_lengkap.docx`, foto di folder `GLD/`) untuk mengidentifikasi apa yang **masih kurang atau belum lengkap** sebelum berkas bisa diajukan ke lembaga sertifikasi.

Status per item: ✅ Ada/Lengkap · ⚠️ Ada tapi belum lengkap ("to be confirmed") · ❌ Belum ada sama sekali

---

## 1. Ringkasan Prioritas (isu paling kritis)

1. **❌ Sensor gas MQ (MQ-2/3B/4/5/6/7B/8/135) memakai elemen pemanas (heater) internal** yang biasanya beroperasi di kisaran 300–400°C. Ini **sangat menentukan kelas temperatur (T1–T6)** dan berpotensi membuat desain saat ini gagal syarat suhu permukaan maksimum untuk zona berbahaya. Belum ada perhitungan hot-spot/estimasi titik terpanas (butir 1.6 checklist). Ini kemungkinan **blocker teknis utama**, bukan cuma isu dokumentasi.
2. **❌ Baterai Li-ion tanpa sertifikasi Ex** — Node Sensor pakai baterai cadangan Li-ion 18650 (4.2V, ~2800 mAh — dokumen menulis "28000 mAh", kemungkinan salah ketik) dan Cluster Head pakai baterai Li-ion 12000 mAh + panel surya. Baterai adalah komponen yang wajib sertifikat Ex atau evaluasi tersendiri (thermal runaway, short circuit) — belum ada data produsen/model/sertifikasi baterai maupun proteksinya (over-charge, over-discharge, short-circuit).
3. **❌ Kelompok gas (IIC/IIB/IIA), kelas temperatur (T1–T6), rentang suhu lingkungan, dan klasifikasi zona (0/1/2)** — parameter dasar yang menentukan skema sertifikasi — **sama sekali belum didefinisikan** di dokumen manapun. Tanpa ini, lingkup pengujian IECEx/ATEX belum bisa ditentukan.
4. **❌ Ingress Protection (IP rating)** — semua tiga perangkat masih "[to be confirmed]" untuk IP rating, padahal ini persyaratan dasar enclosure untuk area berbahaya.
5. **⚠️ Material enclosure kini dipilih: Aluminum alloy + Stainless steel** (dikonfirmasi user 27 Agustus 2026, untuk Node Sensor/GLD, Cluster Head, dan Gateway — lihat `REFERENSI-KOMPONEN-BOM.md` §0), konsisten dengan produk sejenis di pasaran (KELISAIKE K500/K800, AIYI). Tapi grade spesifik (mis. seri aluminium, grade stainless 304/316L) **masih belum ditentukan**, dan checklist masih minta gambar teknik struktur enclosure dengan parameter celah (gap)/panjang/volume — krusial jika desain memakai proteksi flameproof (Ex d), dan belum tersedia sama sekali.
6. **❌ Ketinggian pemasangan belum tersertifikasi untuk instalasi permanen** — dikonfirmasi rapat resmi 6 Agustus 2026 (repo `GLD-V2-Report-2026`, `gate:cert-height`): uji coba di kilang baru dipasang setinggi orang, bukan ketinggian instalasi final. Sertifikasi ATEX/IECEx perangkat perlu eksplisit mencakup skenario ketinggian pemasangan aktual di lapangan.
7. **❌ Solar panel Cluster Head dan keamanan baterai Li-ion 18650 CH belum disourcing/didokumentasikan** — dikonfirmasi 19 Agustus 2026 (`gate:solar-cert`, `gate:ch-batt-safety`): solar panel wajib tersertifikasi hazardous/flammable area, dan keamanan sel/BMS baterai Li-ion 18650 Cluster Head (mis. IEC 62133/UN 38.3) masih terbuka, PIC LGU. Ini memperkuat isu kritis #2 di atas — bukan cuma Node Sensor, Cluster Head juga punya baterai Li-ion yang sama sekali belum diverifikasi.
8. **⚠️ Material PVC eksplisit dihindari** untuk seluruh housing/bracket sesuai keputusan resmi rapat 6 Agustus 2026 — konsisten dengan kebutuhan sertifikasi area berbahaya, tapi berarti pilihan material enclosure/bracket harus dikonfirmasi ulang tidak memakai PVC di manapun (termasuk komponen kecil seperti dudukan kabel).

> Sumber tambahan (6–8): repo internal proyek `GLD-V2-Report-2026` (`memory/decisions.md`, `memory/blockers_metrics.md`) — hasil rapat resmi tim ITB/LGU/Pertamina, bukan dari dua dokumen sumber PDF/DOCX awal di folder ini. Rencana sertifikasi perangkat untuk kilang sendiri tercatat sebagai **action item resmi** dengan PIC "Tim ITB bersama Pertamina" (rapat 6 Agustus) — jadi dokumen ini sejalan dengan proses yang memang sedang berjalan di pihak proyek.

---

## 2. Dokumentasi Teknis (mengacu checklist §1)

### 2.1 Deskripsi Produk
| Item | Status | Catatan |
|---|---|---|
| Nama produk, model, spesifikasi | ✅ | Ada di `Parameter spesifikasi EMC_lengkap.docx` dan `Dokumen_spesifikasi_input_2.docx` |
| Parameter kelistrikan lengkap | ⚠️ | Banyak field masih "[to be confirmed]": arus maksimum, tegangan internal, daya adaptor, dll (lihat §4 di bawah) |
| Foto produk keseluruhan + komponen utama | ⚠️ | Ada 6 foto di `GLD/` (motherboard, casing, modul sensor, penutup mesh, modul alarm) — tapi **belum ada foto produk jadi/final assembly per tipe (Node Sensor, Cluster Head, Gateway) secara terpisah dan berlabel**, dan belum ada foto komponen individual (baterai, gasket, terminal, cable gland) |
| Kelompok gas IIC/IIB/IIA | ❌ | Belum ditentukan |
| Kelas temperatur T1–T6 | ❌ | Belum dihitung/ditentukan |
| Rentang temperatur lingkungan | ⚠️ | Operating temperature masih "[to be confirmed] °C" di ketiga perangkat |
| Klasifikasi area Zona | ❌ | Belum ditentukan |

### 2.2 Gambar Teknik
| Item | Status |
|---|---|
| Assembly drawing | ❌ Belum ditemukan file gambar teknik (hanya foto, bukan gambar berdimensi) |
| Gambar komponen | ❌ |
| Diagram skematik kelistrikan | ❌ |
| Layout PCB | ❌ (foto motherboard ada, tapi bukan layout/gerber resmi) |
| Struktur enclosure + parameter proteksi ledakan (celah/panjang/volume) | ❌ |
| Gambar junction box | ❌ |
| Gambar terminal | ❌ |
| Gambar sambungan grounding | ❌ |

Semua gambar di atas harus mencantumkan **dimensi, toleransi, dan material** — belum ada satu pun draft.

### 2.3 Bill of Materials (BOM)
❌ **Belum ada BOM formal.** Yang tersedia baru sebatas nama komponen tingkat tinggi di tabel spesifikasi (mikrokontroler ESP32S3-WROOM-1U, modul LoRa E22-900MM22S, sensor MQ). Untuk tiap komponen di bawah ini, checklist mensyaratkan produsen, model, grade material, sertifikasi (UL/ATEX/CCC), dan parameter teknis (CTI, flame retardancy, ketahanan kimia, Tg) — **semuanya belum ada**:
- Enclosure/casing
- Gasket/seal
- Terminal
- Cable entry device (cable gland) — spesifikasi masih "[to be confirmed]" di semua perangkat
- Sakelar
- Sumber cahaya (bila ada indikator LED, dsb.)
- Baterai (Li-ion 18650, Li-ion 12000 mAh)
- Bahan potting
- Komponen plastik
- PCB

### 2.4 Data Sheet Material Non-Logam
❌ Belum ada satu pun datasheet material (ketahanan suhu, anti-aging, antistatik, tahan api, nilai CTI, ketahanan kimia, laporan uji/deklarasi kesesuaian dari pemasok).

### 2.5 Proses Manufaktur
❌ Belum ada deskripsi proses (kontrol presisi enclosure, perlakuan permukaan, pengelasan, potting, die casting, bonding/perekat) — relevan terutama bila casing metal dilas/di-casting untuk proteksi Ex d.

### 2.6 Perhitungan
❌ **Belum ada perhitungan proteksi ledakan** dan **belum ada perhitungan/estimasi titik terpanas** — lihat poin kritis §1.1 di atas soal heater sensor MQ.

### 2.7 Draft Manual
❌ Belum ada draft manual (peringatan keselamatan, metode pemasukan kabel, torsi pengencangan, syarat grounding, syarat pembersihan, petunjuk operasi, jadwal pemeliharaan).

### 2.8 Label & Sertifikat Komponen
| Item | Status |
|---|---|
| Nameplate/label dengan marking ATEX | ❌ Belum ada desain label |
| Sertifikat Ex untuk komponen bersertifikat (ESP32, modul LoRa E22) | ❌ Belum ada — checklist HTML sudah menandai kebutuhan ini dengan tag `ESP32·E22` tapi belum ada dokumen sertifikat terlampir |

---

## 3. Informasi Sampel (checklist §2)
| Item | Status |
|---|---|
| Model sampel per tipe | ✅ Ada (Node Sensor / Cluster Head / Gateway) |
| Nomor seri | ❌ Belum ada |
| Kondisi/status sampel (bisa dinyalakan?) | ❌ Belum dikonfirmasi |
| Fixture pengujian | ❌ Belum disiapkan |

---

## 4. Field "to be confirmed" — Update Status (setelah cross-check repo internal proyek)

`Dokumen_spesifikasi_input_2.docx` sudah diperbarui (26 Agustus 2026) menggunakan data resmi dari repo internal proyek `GLD-V2-Report-2026` (notulen rapat, hasil pengujian daya/RF, spek EMC terverifikasi). **~40 dari 56 field yang sebelumnya kosong kini terisi** dengan data bersumber jelas (frekuensi, daya, dimensi, material, mounting, dsb). Sisanya sengaja dibiarkan `[to be confirmed]` karena memang belum ada data resmi — jangan diisi kira-kira. Yang masih terbuka:
- Berat total (semua 3 perangkat)
- IP rating Node Sensor & Gateway (Cluster Head sudah terkonfirmasi IP66/67)
- Cable entry/gland spesifik, DC connector Gateway, konektor antena Gateway
- Rentang suhu & kelembapan operasi (semua perangkat)
- Detail proteksi elektrikal (fuse/reverse polarity/overvoltage/overcurrent) — hanya diketahui "ditangani sebagian oleh BQ25185" untuk CH
- Kapasitas baterai Cluster Head (12000 mAh belum ada sumber konfirmasi)
- Jumlah maksimum Sensor Node per Cluster Head/Gateway (`gate:capacity` — action item resmi terbuka, Tim Komunikasi ITB)

Detail lengkap per field (versi sebelum update) ada di riwayat commit git; ringkasan asli:

## 4b. Field "to be confirmed" yang Masih Terbuka (dari `Dokumen_spesifikasi_input_2.docx`)

### Node Sensor
- Internal operating voltages (5V/3.3V)
- Maximum input current, maximum power consumption (draft: 0,3 A / 0,3×24 W — masih perlu konfirmasi, dan **tidak konsisten** dengan tabel EMC yang menyebut 7.995 W)
- Battery capacity (tertulis "28000 mAh" — kemungkinan typo, 18650 tunggal biasanya 2000–3500 mAh)
- Proteksi elektrikal (fuse/reverse polarity/overvoltage/overcurrent) — ditulis "all" tapi belum ada bukti desain/komponen
- Environmental sensor (jenis belum disebutkan)
- Processing unit — dikonfirmasi ESP32S3 di dokumen lain, tapi field ini masih placeholder
- Enclosure material, dimensi, berat, metode mounting, IP rating, cable entry spec

### Cluster Head
- Battery capacity, solar panel rated power & nominal voltage, charge controller type — semua "[to be confirmed]"
- Internal operating voltage, arus & daya maksimum
- Proteksi elektrikal (overcharge/over-discharge/short-circuit/reverse polarity)
- Frekuensi operasi, daya RF maksimum, jenis & gain antena — **tidak konsisten** dengan tabel EMC yang sudah menyebut 920/921 MHz, 22 dBm, 3/8 dBi
- Jumlah maksimum Sensor Node yang didukung
- Enclosure material, dimensi, berat, IP rating, cable entry, mounting antena & panel surya

### LoRa Gateway
- Arus & daya maksimum, konektor DC, proteksi elektrikal
- Frekuensi, daya RF, antena, gain — sama, tidak konsisten dengan tabel EMC
- Backhaul (Ethernet/Wi-Fi/4G), protokol komunikasi (MQTT/HTTP/TCP-IP)
- Enclosure material, dimensi, berat, IP rating, mounting, konektor antena

**Catatan konsistensi:** `Dokumen_spesifikasi_input_2.docx` dan `Parameter spesifikasi EMC_lengkap.docx` perlu disatukan — beberapa nilai (frekuensi, daya pancar, gain antena, daya konsumsi) sudah final di tabel EMC tapi belum disalin ke dokumen spesifikasi utama, sehingga dokumen spesifikasi resmi yang diserahkan ke lembaga sertifikasi berisiko kelihatan belum matang/konsisten.

---

## 5. Rekomendasi Langkah Berikut
1. Tentukan lebih dulu **skema sertifikasi target**: kelompok gas, kelas temperatur, zona instalasi (Zona 1/2 atau 21/22) — ini menentukan semua pengujian selanjutnya.
2. Lakukan **pengukuran/estimasi suhu permukaan** dengan heater MQ sensor menyala terus-menerus pada kondisi terburuk (worst case) untuk menentukan kelas T.
3. Putuskan skema proteksi ledakan (Ex d / Ex e / Ex i / Ex n, dst.) — ini menentukan apakah perlu gambar celah/gap flameproof atau cukup jalur proteksi lain (mis. Ex i untuk baterai/sirkuit daya rendah).
4. Kumpulkan datasheet resmi untuk tiap komponen kritikal: baterai (dengan sertifikasi/UN38.3 minimal), modul LoRa E22, cable gland, gasket, konektor.
5. Selesaikan seluruh field "[to be confirmed]" di `Dokumen_spesifikasi_input_2.docx`, sinkronkan dengan tabel EMC.
6. Buat gambar teknik resmi (assembly, skematik, PCB layout, enclosure) — bukan hanya foto.
7. Susun BOM lengkap dan draft manual sesuai format checklist.

---
*Dibuat otomatis berdasarkan isi folder pada 2026-08-26. Silakan perbarui saat dokumen sumber berubah.*
