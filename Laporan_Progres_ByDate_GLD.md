# LAPORAN PROGRES PER TANGGAL — PROYEK GAS LEAK DETECTION (GLD) TAHAP 2

**Periode:** 20 April – 20 Juli 2026
**Disusun per:** 23 Juli 2026
**Scope aktif:** Pilot RU IV Cilacap (roadmap: 6 Refinery Unit)
**Pihak terlibat:** LAPI Ganesha Utama (LGU) · Lab IoT & Lab Fisika ITB · PT Pertamina Patra Niaga / Kilang Pertamina Internasional

---

## Ringkasan

| Indikator | Nilai |
|---|---|
| Progres pilot Cilacap (vs baseline resmi 9 bulan) | **39%** (rencana 19% · **+20 poin**, murni sisi lab) |
| Blocker kritis aktif | 3 (catu daya · DC converter · jangkauan LoRa) |
| Action items | 24 (5 berjalan · 15 terbuka) |
| Isu & risiko | 9 (4 prioritas tinggi) |
| Dataset sensor terkumpul | 14.477 sampel · 9 sesi · 8 kanal MQ |
| Model AI | TCN per-sensor (LPG): 8 model, semua ≥92% akurasi (MQ4V 93,9%) |

Baseline dikalibrasi ke *Project Timeline 9 bulan* (Deck Kick-Off, 12 Jun 2026 → Feb 2027). Engineering front-loaded sejak April sehingga progres di depan jadwal; namun eksekusi site survey menunggu **gate TRA/JSA** dan 3 blocker teknis belum tuntas.

---

## FASE 1 — Pengembangan & Uji Laboratorium (20 April – 7 Juni 2026)

*Rencana kerja mingguan (M1–M7), setiap bulan = 4 minggu.*

### M1 · 20–26 April — *Selesai*
- ✅ **Desain Gas Test Chamber** selesai.
- ✅ **Uji node GLD lama** — verifikasi fungsi dasar.
- ✅ **Uji routing Cluster Head** — `CH_Hello` & `CH_Config` terverifikasi.
- Pengujian board sensor: PSU 5V→board 5,05V; VCC ESP32 3,305V; VBUS 4,97V.

### M2 · 27 April – 3 Mei — *Selesai*
- ✅ **Uji Node GLD baru** — 2 unit board (#0001 & #0002); semua parameter OK. Terverifikasi: TCA9548A I²C mux, ADS1115 ADC, MCP3208 8-channel ADC (8/8 aktif), LoRa, sensor.
- ✅ **Uji konsumsi baterai CH** — Test 1: 1 device online; Test 2: 3 CH + 1 Node online (CH ~4,03–4,08 V / 85–90%).
- 📄 `Design.md` (algoritma sistem) & desain EasyEDA chamber.

### M3 · 4–10 Mei — *Berjalan*
- Uji fungsional sistem **GLD–CH–GW–Server** dimulai.
- Pembuatan chamber & uji pembacaan sensor.
- Uji daya **panel surya → CH** (percobaan berdurasi 1 minggu).
- 🔧 Perbaikan firmware CH: **power recovery guard + WDT**.

### M4 · 11–17 Mei — *Berjalan*
- Uji **jarak & reliabilitas** komunikasi data.
- Uji konsumsi baterai **Node GLD**: aktif 2 mnt 37 dtk, sleep 3 mnt (3,267 V aktif / 200 mV nonaktif). Uji node mode 24 V.

### M5–M6 · 18–31 Mei — *Berjalan*
- Uji sistem di lingkungan kampus ITB (indoor, obstacle pohon/gedung, outdoor terbuka).
- 📋 **Site Survey Technical Checklist** disusun (pemetaan area, titik node, uji RF, power, server, gas/AI).
- Evaluasi.

### Uji Cluster Head — Topologi Star-Mesh & Failover — *Milestone ✅*
- Konfigurasi otomatis: CH1/CH2/CH3-GW discovery & pilih parent berdasarkan **RSSI terbaik**.
- Topologi normal: `Node → CH1 → CH2 → CH3/GW` dengan ACK tiap hop.
- **Failover terbukti:** saat CH2 mati (ACK timeout 3×), CH1 re-config dan pindah parent ke CH3/GW — data tetap sampai, **0 loss**.

### Karakterisasi RF LoRa (kampus) — *Temuan*
- Area terbuka: 100 m @ −71 dBm, PDR 100%.
- Bawah pepohonan: 80 m, PDR 100%.
- Area gedung + pohon: antena RX dinaikkan ke 6 m memperbaiki link (−81 dBm, PDR 100%).
- Batas jangkauan (area Fisika): −112 dBm, PDR 26%.

### M7 · 1–7 Juni — *Berjalan*
- Persiapan pemasangan sistem.

---

## FASE 2 — Kick-Off & Progres Menuju Field (12 Juni – 20 Juli 2026)

### 12 Juni — Kick-Off Meeting Pertamina — *Milestone ✅*
- Baseline **timeline 9 bulan** disepakati; scope **6 RU** (RU II–VII).
- **Target implementasi Desember 2026**; field test kolaborasi RU-VII Kasim.
- Desain end-to-end; sistem **pelengkap** (bukan pengganti); instalasi via pihak ke-3 + koordinasi HSE tiap RU.
- Dua SPK: (1) compiler & sertifikasi hazardous area; (2) implementasi 6 unit kilang.

### 18 Juni — Prinsip Pemodelan AI ditetapkan
- Pergeseran ke **fingerprint 8-sensor** & pola relatif (fase transien / stasioner / saturasi), bukan amplitudo absolut.
- Proyek ditegaskan setara **TRL-7** (level industri).

### 26 Juni — Temuan Jangkauan LoRa
- ⚠️ **Antena LoRa 6 m maks ±100 m** pada kondisi obstruksi (spec target 1–2 km LOS).
- Model **TCNN** mulai dikembangkan (prediksi 5 dtk dari 5 dtk sebelumnya).

### 30 Juni — Project Report June (Lab IoT ITB)
- Uji komponen **PCB GLD v1 & v2** — Done.
- Uji **baterai GLD** — Progress; assembly casing (sirine & buzzer menunggu pengiriman).
- **Desain chamber** Done; **assembly chamber** (mekanik & elektrikal) Progress.
- Pengumpulan dataset GLD — Progress; **model ML/AI (LPG)** — perlu konfirmasi jenis gas yang dilatih.
- Uji & validasi ML/AI — Progress; uji fungsional GLD-CH-GW-Server — Progress.

### 2 Juli — Repositori Kode
- Source code masih tersebar (GLD & AI · jaringan · server) → **rencana konsolidasi** satu repo utama.

### 6 Juli — Uji Komunikasi 2 Cluster Head — *Milestone ✅*
- Charging 08:00–16:00 menaikkan baterai **3,0 → 3,4 V** (±20%).
- Mahasiswa PJ penyelesaian chamber didapatkan.

### 6–8 Juli — Uji Ketahanan Baterai CH (LitoKala) — *Daya*
- 1 baterai LitoKala mampu supply board CH **~40 jam** (periode transmit 10 dtk); 3 baterai ~33 jam.
- Lapangan (dengan solar): **CH3 hidup 8 hari** (baterai awal 4,0 V), CH5 5 hari — teridentifikasi defisit energi kecil pada 1 panel.

### 9 Juli — Rantai Komunikasi GLD–CH–GW–Server Tersambung — *Milestone ✅*
- Data mengalir penuh **Node → CH → GW → server** (MQTT) — rantai komunikasi end-to-end terbukti, menjadi dasar uji fungsional terintegrasi.

### 9 Juli — Kinerja Solar
- Vp = 7,25 V; Ip = 0,05 A (matahari mulai redup). **Pengisian belum optimal** — lokasi hanya optimal 10:00–13:00 → **rekomendasi pindah ke rooftop**.

### 13 Juli — Profil Beban Daya GLD — *Blocker teridentifikasi ⚠️*
- Jalur 5 V & 24 V normal (±6 W).
- 🔴 **Mode baterai hanya 2,43 W** vs kebutuhan ±6 W — mode baterai belum mampu menyuplai 8 heater MQ penuh.

### 13 Juli — Update Repo Frontend (gasleakdetectionV2-April) — *Update*
- Peta dashboard pindah ke **MapLibre** (menghapus Mapbox, local tiles — hilangkan flicker).
- **Default deployment diubah ke RU IV Cilacap.**
- Ditambahkan **device CRUD** penuh + **gas trend heatmap overlay** + RU map zoom.

### 14 Juli — Solar–Baterai
- Pukul 11:00–15:00 tegangan stabil **±4,17 V** (baterai penuh). Setelah 14:00 arus/daya negatif (mulai discharge) → turun ke ±4,12 V.

### 15 Juli — Akuisisi Data & Model TCN — *Milestone ✅ / ML*
- Akuisisi dataset GLD-F001: sesi **Clean Air, LPG, O₂, CO₂** — total **14.477 sampel** di 8 kanal MQ (~2,7 jam logging).
- **Model TCN per-sensor (Board12) selesai:** 8 model independen (1/sensor), semua **≥92% akurasi** prediksi LPG 5 dtk ke depan. Terbaik **MQ4V 93,9%** (F1 0,923). Ekspor TFLite int8 ~72 KB untuk edge.

### 16 Juli — Uji Fungsional Sistem + Inferensi AI — *Milestone ✅*
- Rantai penuh **sensor → CH → GW → server** berjalan end-to-end. **Inferensi AI berjalan di komputer/laptop dengan emulator ESP32** — belum on-device; **deploy ke ESP32 fisik = langkah berikutnya**. Fungsional terintegrasi (GLD-CH-GW-Server) tercapai jauh sebelum jadwal resmi (September).

### 16 Juli — Analisis Daya Sistem GLD & CH, Uji Mesh & Downlink — *Milestone ✅*
**Budget daya GLD node (baterai 7P = 7×4000 mAh = 28 Ah, ~70,4 Wh usable):**
- Draw ON terverifikasi **5,75 W** (5 V × 1,15 A) — mengklarifikasi anomali "2,43 W" sebelumnya (pengukuran tak lengkap).
- Duty 29% (T_ON 65 s / T_OFF 159 s) → runtime **1,76 hari**. Variasi T_ON: 10 s → 8,63 hari; 30 s → 3,22 hari; 60 s → 1,86 hari.
- Variasi jumlah baterai: 7P 1,76 hari · 30P 7,54 hari · **120P baru ~30,16 hari**.
- **Target 30 hari batt-only butuh ~120 sel (tidak realistis).** Opsi paling masuk akal: **perpanjang OFF ~63 menit** (ON tetap 65 s) atau berbasis solar.
- ⚠️ Catatan: baterai LitoKala banyak yang hanya 2500 mAh; **TPL5010 belum optimal** — saat non-aktif board masih ~0,4 V & tetap mencuplik data.

**Cluster Head:**
- Konsumsi CH **84 mA** (ESP32-S3 58 mA + LoRa 2×6,8 mA + dll) ≈ 7,56 Wh/hari.
- 1 panel surya: defisit **−0,66 Wh/hari**. **2 panel surya: surplus 1,5–4,4 Wh/hari** (Isc 1,29 A, Pmax ~6,51 W) — kebutuhan energi CH teratasi.
- Power path: Panel → charger **BQ25185** → baterai 18650 → **TPS63020** 3,3 V → beban CH.

**Jaringan:** **Uji mesh 8-CH se-kampus ITB** (CH1–CH8, multi-hop hingga Layer 3, route depth 1–3) & **uji downlink GLD** (server→node lewat mesh) + perbaikan firmware downlink → **keterbatasan jangkauan LoRa per-hop disiasati mesh multi-hop**.

### 16 Juli — Temuan Sensor & Aplikasi UI
- Respons sensor berkorelasi positif pada **CO₂**, tidak pada **O₂** (O₂ menggantikan gas terdeteksi).
- **Baseline berbeda per sensor** (MQ135 > MQ8) → **threshold ditetapkan per-MQ**; baseline sebagai panduan QC.
- **Aplikasi UI GLD** dibuat (tab dataset, capture, save, download) — bangun model langsung di PC.
- Uji sinyal LoRa acak (sekitar ITB): Gerbang Utara 242 m PDR 100%; Depan LFT 177 m PDR 100%; STEI Lt.2 200 m PDR 87%.

### 17 Juli — Urutan Kerja Koordinasi
- Disepakati: **LGU undang Pertamina ke lab → uji lab → baru kunjungan RU**. Dokumen JSA/TRA perlu dikonfirmasi kesiapannya.

### 20 Juli — Simulasi Siklus Operasi & Arahan Daya
- Program simulasi diunggah ke board GLD: **ON 60 s / OFF 100 s / interval WAKE 160 s** (warm-up → akuisisi → inferensi → transmit LoRa).
- Strategi manajemen daya: inferensi tidak kontinu; saat inferensi suplai MQ diputus, **ESP tetap menyala**.
- 🔴 Arahan: **circuit DC converter harus diganti/dimodifikasi**; modifikasi baterai ditahan sementara, fokus dialihkan.

---

### 23 Juli — Update Repo Server/Firmware (PertaminaGLD) — *Update*
- Commit aktif (22–23 Jul): firmware **GLD/CH/GW** + **Operator Hub workflows**, peningkatan reliability & test coverage.
- Manajemen daya **TPL5010** (timer nanopower untuk duty-cycle) & algoritma **nulling**, dataset handling.
- *Catatan: repo ML edge (gas-leak-ml-chamber-system) commit terakhir 24 Jun — belum ada update baru.*

### 23 Juli — Progress Gas Test Chamber — *Milestone ✅*
Sistem kendali chamber berfungsi (kendali dua-arah real-time via ESP32):
- **Solenoid valve** — pengendalian aliran gas presisi.
- **Pompa penghisap** dengan pengaturan **duty cycle** — kontrol dinamika udara chamber.
- **2× BME280** (I²C 0x76 & 0x77, modif solder pad) — komparasi suhu/tekanan/kelembapan internal vs eksternal.
- **TGS2610** (sensor gas referensi) via **ADS1115** eksternal + **voltage divider** (5V→3,3V).
- Daya: **LM2596** step-down → 5V → ESP32/BME280/TGS2610/relay/**driver motor BTS7960**.
- **Rencana lanjut:** rapikan wiring → **buat PCB layout**; ganti pompa lebih senyap; pasang rangkaian di dinding belakang chamber.

---

## Blocker Kritis Aktif (per 20 Juli)

| # | Blocker | Metrik | Dampak |
|---|---|---|---|
| 1 | Autonomi baterai GLD di bawah target 30 hari (draw ON 5,75 W terverifikasi; 7P = 1,76 hari; TPL5010 belum optimal) | 7P = 1,76 hari / 30 hari | GLD tak dapat mandiri 30 hari — perlu perpanjang OFF / solar |
| 2 | DC converter perlu diganti/dimodifikasi | Arahan 20 Jul | Menahan finalisasi desain catu daya |
| 3 | Jangkauan LoRa jauh di bawah spec | ~100 m / 1–2 km | Menaikkan jumlah CH & biaya deployment |

## Gate Menuju Field (RU IV Cilacap)
- ⛔ **TRA/JSA** — rencana & workflow survei Cilacap sudah siap; **penyusunan TRA/JSA menjadi gate** untuk eksekusi site survey fisik.
- Site visit Pertamina ke lab LGU → uji lab → kunjungan RU.

---

*Laporan disusun dari: Timeline Kerjaan Mingguan · Deck Kick-Off 12 Jun · Notulensi Kick-Off · MoM RU IV Cilacap · Laporan Progres 18 Jun–20 Jul · Project Report June · Board12 TCN per-Sensor · dataset GLD-F001 · Test Sinyal LoRa. Persentase progres bersifat estimasi turunan dari status aktivitas.*
