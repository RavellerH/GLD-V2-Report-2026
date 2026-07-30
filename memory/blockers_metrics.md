# Blockers, Gates & Metrics (sumber angka)

> Ini **satu sumber kebenaran** untuk angka kunci. File lain merujuk ke sini.

## Status progres (per 24 Jul 2026)
- **Progres pilot Cilacap: 39%** vs baseline resmi **19%** → **+20 poin** (murni sisi engineering lab, BUKAN kesiapan lapangan; jangan over-claim).
- Action items: **25** (5 berjalan, 15 terbuka, 1 selesai). Isu & risiko: **8** (3 tinggi).
- **Koreksi penting:** inferensi AI kini di **PC + emulator ESP32**, belum on-device. **Dataset konsisten & siap pakai** (isu konsistensi resolved). **Jangkauan LoRa disiasati mesh** (bukan blocker keras).

## Blocker kritis aktif (3)
| ID | Blocker | Metrik | Dampak |
|---|---|---|---|
| blk:power | Autonomi baterai GLD < target 30 hari | draw ON **5,75 W**; 7P(28Ah)=**1,76 hari**; 30 hari butuh ~120 sel | GLD tak mandiri 30 hari → perlu perpanjang OFF ~63 mnt / solar |
| blk:tpl | TPL5010 belum memutus daya | board ~**0,4 V** & cuplik data saat "off" | Duty-cycle belum efektif hemat daya |
| blk:conv | DC converter perlu diganti/dimodifikasi | arahan 20 Jul | Menahan finalisasi catu daya |
| blk:ai-edge | Deploy inferensi AI ke ESP32 on-device | kini di PC + emulator | Belum jalan di perangkat lapangan |

## Diminimalkan / resolved
- ~~blk:lora~~ → jangkauan LoRa ~100 m/hop **disiasati mesh multi-hop** (uji 8-CH se-kampus, Layer 3). Konsekuensi: butuh lebih banyak CH (mis. RU VII 11 CH). Risiko, bukan blocker.
- ~~isu konsistensi data~~ → **dataset konsisten & siap dipakai**.
- CH catu daya → **teratasi 2 panel** (surplus 1,5–4,4 Wh/hari).

## Mesh LoRa (uji 8-CH, 16 Jul)
Deployment se-kampus ITB: GW ← Layer 1 (CH3/CH5/CH8) ← Layer 2 (CH1/CH4) ← Layer 3 (CH2). Route depth 1–3, status installed. Downlink (GW→CH→GLD 0xF020) tembus lewat mesh + fix firmware.

## Gate
| ID | Gate | Status |
|---|---|---|
| gate:jsa | TRA/JSA | Belum disusun → menahan eksekusi site survey fisik RU IV Cilacap |

## Metrik daya (Update Timeline Juli, 16 Jul 2026)
**GLD node (baterai 7P = 7×4000 mAh = 28 Ah, ~70,4 Wh usable):**
- Draw ON 5,75 W (5V×1,15A). Duty 29% (T_ON 65s / T_OFF 159s) → runtime 1,76 hari.
- Variasi T_ON: 10s→8,63 hari · 30s→3,22 hari · 60s→1,86 hari.
- Variasi baterai: 7P→1,76 · 14P→3,52 · 30P→7,54 · 60P→15,08 · 120P→30,16 hari.
- Target 30 hari: ~120 sel (tak realistis) **atau** perpanjang OFF ~63 mnt (ON tetap 65s).

**Cluster Head:**
- Konsumsi 84 mA ≈ 7,56 Wh/hari. 1 panel: defisit −0,66 Wh/hari. **2 panel: surplus 1,5–4,4 Wh/hari** (Isc 1,29 A, Pmax ~6,51 W) → teratasi.
- Power path: Panel (7,77 V/0,74 A) → BQ25185 → 18650 → TPS63020 3,3 V → beban.
- Ketahanan: 1 baterai LitoKala ~40 jam (transmit 10s); lapangan CH3 8 hari / CH5 5 hari.

## Metrik RF LoRa
- Terbuka: 100 m @ −71 dBm PDR 100%. LFT 177 m PDR 100%. Gerbang Utara 242 m PDR 100%. STEI 200 m PDR 87%. Batas: −112 dBm PDR 26%.
- Antena RX 6 m memperbaiki link area gedung+pohon (−81 dBm PDR 100%).

## Metrik AI & data
- Dataset GLD-F001: **14.477 sampel**, 9 sesi, 8 kanal MQ, 4 jenis gas (~2,7 jam).
- TCN LPG 8 model: semua **≥92%**, terbaik **MQ4V 93,9%** (F1 0,923), TFLite int8 ~72 KB.

## Bobot sub-sistem (untuk % dashboard)
net 20 · ai 22 · power 15 · chamber 12 · sw 13 · integ 10 · ruprep 8 · (inisiasi 10 — bila dipakai). Baseline 12-aktivitas → lihat `overview.md`.

## Meeting 24 Jul 2026 — update & catatan rekonsiliasi
> Sumber: `Notulen Meeting GLD 24 Juli 2026.docx` (LGU–Pertamina, 09:32–11:00 WIB).

- **Target battery baru:** konsumsi sensor MQ ~10W (1A/8 sensor) → target diturunkan ke **<100mA**; lifetime min **30 hari**, desain baru berpotensi **6–8 bulan** (rechargeable). Ini **target/arah**, bukan pengganti angka terukur `blk:power` (draw ON 5,75 W, 7P=1,76 hari) — belum ada data pengujian baru yang mengonfirmasi <100mA tercapai.
- **24V (power supply): siap sertifikasi**, proses administratif jalan via biro di Shanghai — jalur deployment ini **tidak menunggu** battery version (dec:16).
- **Gas capability gate baru:** minimum 6 kelas (H₂, LPG, Metana, CO₂, Clean Air) harus terverifikasi sebelum deployment (dec:17) — status verifikasi: **action item terbuka** (PIC Pak Farhan/Ilma, deadline 10 Agu 2026).
- **Gate administratif baru (RU Cilacap):** izin visitor (maks 3 hari) utk survey; izin kerja + surat masuk barang utk instalasi; dokumen HSE (APD non-merah, template dari RU). Melengkapi `gate:jsa` yang sudah ada.
- **Risiko baru dari meeting** (belum ada di daftar 8 isu/risiko existing):
  - Data alarm hilang saat transmisi → mitigasi: retry/recovery mechanism + local buffering + heartbeat monitoring (action item PIC Beni, deadline 15 Agu 2026).
  - Perizinan masuk kilang terlambat/ditolak → mitigasi: koordinasi early dgn HSE & PIC RU Cilacap, dokumen lengkap jauh-jauh hari.
- **Action items meeting:** 18 item dengan PIC & deadline (Agustus 2026, next meeting RAP ~15 Agu). ⚠️ **Belum direkonsiliasi** satu-per-satu dengan angka "25 action items (5 berjalan/15 terbuka/1 selesai)" di atas — kemungkinan overlap sebagian, perlu verifikasi sebelum dashboard diupdate.

### Klaim dari notulen 24 Jul — status rekonsiliasi
| Klaim di notulen 24 Jul | Status | Catatan |
|---|---|---|
| Model **"CNN 1D" akurasi 97,6%** | ✅ **DIREKONSILIASI** (30 Jul, ditemukan source pptx) | Bukan konflik dgn TCN ≥92% — **model berbeda**: CNN 1D = klasifikasi jenis gas 3-kelas (Clean Air/LPG/CO2), TCN = prediksi leak LPG time-series per-sensor. Sumber: `Sumber Dokumen/Deteksi_Gas_CNN_Presentasi.pptx` (Lab IoT ITB) — 97,6% akurasi test (374 holdout, F1-macro 97,55%), versi ESP32-S3 int8 97,3%. Detail lengkap → `entities.md` bagian Model AI. **Boleh dipakai di deliverable** sebagai model AI kedua (klasifikasi gas), terpisah dari TCN (prediksi leak). |
| **Flame detection (camera-based)**: model develop 79%, hardware Jetson Nano (sudah dibeli), dataset dari Google + kamera infrared | ⚠️ **Masih belum dikonfirmasi** | Tidak ada file sumber pendukung ditemukan di repo (beda dgn OGI/`LangGas_Top6000_Progress.pptx` yang eksplisit dihapus). Teknologi berbeda dari OGI tapi domain mirip. **Status: pengembangan tambahan terpisah, BELUM masuk scope dashboard/report** (dec:18) — perlu arahan user. |
| **Sensor arah angin** untuk early warning (prediksi dispersi gas/flame) | ⚠️ Rencana masa depan | Tidak ada di scope/sub-sistem manapun saat ini; belum ada timeline/PIC konkret di notulen. |
