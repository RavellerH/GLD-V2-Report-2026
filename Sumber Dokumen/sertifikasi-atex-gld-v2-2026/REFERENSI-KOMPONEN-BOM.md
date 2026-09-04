# Referensi Komponen Ex-Rated untuk BOM — Casing/Enclosure GLD V2

Dokumen ini berisi hasil riset produk enclosure Ex-rated (ATEX/IECEx) yang datasheetnya lengkap (material, IP rating, sertifikat), untuk dijadikan **acuan pengisian BOM** (lihat `ANALISIS-KEKURANGAN.md` §2.4 — BOM masih kosong). Bentuk enclosure GLD V2 (badan silinder + muka sensor bundar dengan mesh, lihat `Gambar Teknik/Base_Plate_Assembled.dwg`) paling mirip dengan kategori "point/fixed gas detector housing", bukan junction box generik — jadi referensi paling relevan adalah produk AIYI di bawah.

⚠️ Ini referensi pembanding untuk membantu menentukan **spesifikasi target**, bukan komponen yang sudah dibeli/dipakai. Body sertifikasi tetap akan menilai material actual yang dipakai GLD V2 Anda — kalau mau memakai skema Ex d, sebaiknya konsultasi ke lab uji atau beli komponen bersertifikat langsung dari produsen di bawah (bukan menyalin data mereka sebagai punya sendiri).

---

## 0. Nanjing KELISAIKE — produsen produk yang Anda tautkan sebelumnya (referensi paling langsung)

Produk yang Anda link ("ATEX IECEx Gas Detector System for Petrochemical Oil Industry", Cl₂, US$280) ternyata tidak mencantumkan material casing di listing marketplace-nya. Tapi produsennya, **Nanjing KELISAIKE Safety Equipment Co., Ltd.**, punya website resmi (njklsk.cn) dengan lini produk gas detector sejenis yang datasheetnya menyebut material secara eksplisit — ini referensi **paling relevan** karena dari brand yang sama persis.

| Parameter | K500 (Wall-Mounted) | K800 Series |
|---|---|---|
| Material casing | **Aluminum alloy + stainless steel** | **Aluminum alloy + stainless steel** |
| Marking Ex | ExdII CT6 (sesuai IEC61508) | Exd II CT6 — satu sumber pihak ketiga menulis "Exd IIC T6" (grup gas lebih spesifik) |
| Dimensi | 160 × 126 × 78 mm | 183 × 143 × 107 mm |
| Berat | 3,0–3,5 kg | 2,0–2,5 kg |
| Suhu operasi | −20°C s/d +50°C (varian −50°C s/d +50°C) | −20°C s/d +50°C |
| Kabel transmisi | — | 3-core shielded, 3×1,5 mm² |
| Sertifikasi disebutkan | CE, CMC, Ex, MA, UL, CCC | UL, CE, CMC, Ex, MA |
| Sumber | [njklsk.en.made-in-china.com](https://njklsk.en.made-in-china.com/product/eFuGRIVbkBhd/China-K500-Wall-Mounted-Gas-Detector-for-Distributed-Control-System-DCS-.html), [njklsk.cn](https://www.njklsk.cn/K800-Series-Fixed-Gas-Detector-pd45847535.html) | sama |

**Catatan penting:**
- Grade spesifik aluminium/stainless steel (mis. seri 316L, EN AC-xxxxx) **tidak dicantumkan** di kedua datasheet ini — hanya disebut "aluminum alloy and stainless steel" secara umum. Untuk BOM resmi, ini masih perlu didalami langsung ke produsen.
- IP rating dan nomor sertifikat Ex/ATEX/UL **tidak dicantumkan eksplisit** di kedua halaman produk — hanya nama sertifikasi tanpa nomor. Ini pola sama seperti listing awal yang Anda kirim: klaim "ATEX/UL/CE" di marketplace B2B sering tidak disertai bukti nomor sertifikat yang bisa diverifikasi.
- Ada inkonsistensi kecil grade gas antar-sumber untuk K800 ("Exd II" vs "Exd IIC") — jangan jadikan acuan pasti sebelum konfirmasi ke produsen.
- Kombinasi **aluminium + stainless steel** ini konsisten dengan referensi AIYI di bawah (§1) — pola umum industri gas detector: badan utama aluminium die-cast, bagian yang kontak langsung lingkungan/sensor pakai stainless steel.

---

## 1. AIYI — ATEX & SIL2 Certified Gas Detector (referensi paling dekat bentuk & fungsi)

| Parameter | Nilai |
|---|---|
| Material enclosure | 316L stainless steel + die-casting aluminum + K9 glass (dengan metalisasi) + O-ring seal + epoxy powder coating |
| IP rating | IP65 |
| Marking Ex | Ex d IIC T6 Gb (flameproof, gas group IIC, kelas suhu T6) |
| Dimensi | 165 × 140 × 78 mm, &plusmn;1.483 kg |
| Kabel | RVVP 3×1.5mm² atau RVVP 4×1.0mm² |
| Fitur relevan | Sensor hot-swap/modular, OLED display, kalibrasi otomatis |
| Sumber | [aiyitec.com](https://www.aiyitec.com/gas-detection-system/fixed-gas-detector/atex-and-sil2-certified-gas-detector.html) |

**Relevansi untuk GLD V2:** kombinasi material ini menjawab beberapa baris BOM sekaligus — enclosure (aluminium die-cast + SS 316L untuk bagian yang kontak langsung dengan lingkungan korosif), gasket/seal (O-ring), dan "sumber cahaya"/jendela indikator (K9 glass termetalisasi, kalau GLD V2 punya jendela LED/display). Kelas T6 mengasumsikan suhu permukaan maks 85&deg;C — ini **acuan target**, bukan jaminan; GLD V2 masih harus dihitung ulang karena ada heater sensor MQ yang lebih panas dari desain referensi ini.

## 2. Abtech SSD Range — Ex d Empty Enclosure (referensi sertifikat & struktur casing logam)

| Parameter | Nilai |
|---|---|
| Material | Aluminium (standard) atau Stainless Steel (custom, fabricated) |
| Marking Ex | Ex d, untuk Zone 1 Gas & Zone 21 Dust |
| Sertifikat ATEX | INERIS 13ATEX0019X Issue 01 |
| Sertifikat IECEx | IECEx INE 14.0061X-002 |
| Rentang dimensi (SS) | ESSD234 170×230×150mm s/d ESSD768 570×1020×390mm |
| Opsi | Bisa dipasang jendela (window) & kontrol lokal; bisa dikombinasi dengan Ex e enclosure |
| Datasheet | Stainless Steel: ABDS0074 Rev 01 &middot; Aluminium: ABDS0075 Rev 01 |
| Sumber | [abtech-inc.com](https://www.abtech-inc.com/products/enclosures/hazardous-area-enclosures/explosion-proof-enclosure-ssd-range) |

**Relevansi:** contoh **format datasheet dan struktur nomor sertifikat** yang perlu ditiru saat menyusun dokumen enclosure GLD V2 sendiri — checklist §1.2 & §1.8 meminta persis data seperti ini (nomor sertifikat ATEX/IECEx eksplisit, bukan cuma "ATEX certified" di judul produk).

## 3. Referensi Lain (untuk perbandingan lebih lanjut, belum diverifikasi detail)

| Produk | Material/IP disebutkan | Sertifikat | Link |
|---|---|---|---|
| Bartec EJC | Aluminium, IP66 | ATEX Ex db IIC T6…T3 Gb, IECEx Ex db IIC T6…T3 Gb | [bartec.com](https://bartec.com/products-solutions/product-finder/product-detail/flameproof-enclosures-ejc-ex-d-iic/) |
| Phoenix Mecano Ex Aluminium | Aluminium, IP66 | ATEX II 2G Ex db IIC T6 | [phoenix-mecano.ch](https://www.phoenix-mecano.ch/en/products/enclosures/ex-atex-enclosures/ex-aluminum-enclosure/) |
| R. STAHL Ex d Aluminium | Aluminium (empty enclosure) | ATEX/IECEx (lini produk umum) | r-stahl.com (halaman produk memblokir akses otomatis — cek manual) |
| International Gas Detectors TOC-750X | 316 stainless steel / white powder-coated aluminium | EN 60079 series, Ex d | [internationalgasdetectors.com](https://www.internationalgasdetectors.com/product/750-atex-addressable-gas-detector/) |

---

## Cara Pakai Referensi Ini di Dokumen Sertifikasi GLD V2

1. **Bandingkan, jangan salin** — gunakan angka di atas sebagai kisaran wajar (mis. IP65/IP66, Ex d IIC T6, material aluminium die-cast + SS316L) untuk menyusun *target spesifikasi* GLD V2, lalu verifikasi lewat pengukuran/pengujian aktual desain Anda.
2. Isi baris BOM checklist §1.3 (enclosure, gasket/seal, sumber cahaya) dengan **produsen & model aktual** yang Anda pakai/beli — bukan produk pembanding ini.
3. Kalau berencana membeli enclosure jadi (bukan custom), produk **Abtech SSD** atau **R. STAHL Ex d Aluminium** cocok dijadikan opsi "beli enclosure bersertifikat" ketimbang mensertifikasi casing custom dari nol — ini bisa mempercepat proses karena sertifikat Ex Component sudah ada (checklist §1.8).
4. Klaim "ATEX/IECEx" di judul listing marketplace (seperti produk made-in-china yang dicek sebelumnya) **tidak bisa dipakai sebagai bukti** kecuali nomor sertifikatnya eksplisit dicantumkan dan bisa diverifikasi di database resmi ([iecex.iec.ch](https://www.iecex-certs.com) untuk IECEx, atau situs Notified Body untuk ATEX).

---
*Dibuat otomatis berdasarkan riset web pada 2026-08-26. Data pihak ketiga, perlu diverifikasi ulang langsung ke produsen sebelum dijadikan acuan resmi dalam pengajuan sertifikasi.*
