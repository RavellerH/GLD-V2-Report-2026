# Blockers, Gates & Metrics (sumber angka)

> Ini **satu sumber kebenaran** untuk angka kunci. File lain merujuk ke sini.

## Status progres (per 24 Jul 2026)
- **Progres pilot Cilacap: 39%** vs baseline resmi **19%** → **+20 poin** (murni sisi engineering lab, BUKAN kesiapan lapangan; jangan over-claim).
- Action items: **42** (12 berjalan, 24 terbuka, 3 selesai). Isu & risiko: **12** (4 tinggi).
- **Koreksi penting:** inferensi AI kini di **PC + emulator ESP32**, belum on-device. **Dataset konsisten & siap pakai** (isu konsistensi resolved). **Jangkauan LoRa disiasati mesh** (bukan blocker keras).
- **Update meeting 24 Jul:** **versi 24V power supply selesai & siap sertifikasi** (Shanghai) — deployment dapat berjalan paralel tanpa menunggu versi baterai. **Model AI terbaru: CNN 1D (fusi 8-sensor) 97,6%**, menggantikan TCN sebagai model utama untuk pelaporan, namun baru mencakup 5 dari **minimum 6 kelas gas** yang disyaratkan (verifikasi berjalan). Target internal instalasi bergeser ke **September 2026** (vs baseline resmi Desember).

## Blocker kritis aktif (5)
| ID | Blocker | Metrik | Dampak |
|---|---|---|---|
| blk:gasclass | Verifikasi cakupan gas minimum 6 kelas belum tuntas | 5 kelas (H₂/LPG/Metana/CO₂/Clean Air) → butuh 6 | Syarat wajib sebelum deployment |
| blk:power | Autonomi baterai GLD (mode baterai) < target 30 hari | draw ON **5,75 W** (~10W/1A total 8 sensor); 7P(28Ah)=**1,76 hari**; target baru **<100mA & ≥30 hari**, potensi 6–8 bulan | GLD (mode baterai) tak mandiri 30 hari; **tidak menghambat mode 24V** yang sudah siap |
| blk:tpl | TPL5010 belum memutus daya | board ~**0,4 V** & cuplik data saat "off" | Duty-cycle belum efektif hemat daya |
| blk:conv | DC converter (mode baterai) perlu diganti/dimodifikasi | arahan 20 Jul | Menahan finalisasi catu daya versi baterai |
| blk:ai-edge | Deploy inferensi AI ke ESP32 on-device | kini di PC + emulator | Belum jalan di perangkat lapangan |

## Diminimalkan / resolved
- ~~blk:24v~~ → **versi 24V power supply selesai, siap sertifikasi** (Shanghai) — resolved, tidak lagi blocker untuk deployment via mode 24V.
- ~~blk:lora~~ → jangkauan LoRa ~100 m/hop **disiasati mesh multi-hop** (uji 8-CH se-kampus, Layer 3; meeting 24 Jul: diuji hingga 3 hop-list, latency <5s normal). Konsekuensi: butuh lebih banyak CH (mis. RU VII 11 CH). Risiko, bukan blocker.
- ~~isu konsistensi data~~ → **dataset konsisten & siap dipakai**.
- CH catu daya → **teratasi 2 panel** (surplus 1,5–4,4 Wh/hari); meeting 24 Jul konfirmasi **CH stabil 20 hari non-stop** dengan solar.

## Mesh LoRa (uji 8-CH, 16 Jul)
Deployment se-kampus ITB: GW ← Layer 1 (CH3/CH5/CH8) ← Layer 2 (CH1/CH4) ← Layer 3 (CH2). Route depth 1–3, status installed. Downlink (GW→CH→GLD 0xF020) tembus lewat mesh + fix firmware.

## Gate
| ID | Gate | Status |
|---|---|---|
| gate:jsa | TRA/JSA | Belum disusun → menahan eksekusi site survey fisik RU IV Cilacap |
| gate:hse-doc | Perizinan & template dokumen HSE RU Cilacap | Belum diterima (izin kerja, surat masuk barang, APD non-merah) — PIC Pak Maman, deadline 31 Jul |

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
- TCN LPG 8 model (15 Jul, fondasi awal): semua **≥92%**, terbaik **MQ4V 93,9%** (F1 0,923), TFLite int8 ~72 KB.
- **Model terbaru (24 Jul): CNN 1D, fusi 8-sensor MQ, akurasi 97,6%.** Target gas: H₂, LPG, Metana, CO₂, Clean Air (5 kelas; **minimum 6 disyaratkan**, verifikasi berjalan — PIC Pak Farhan/Ilma, deadline 10 Agu). Tiap unit GLD di-training khusus.

## Mesh & jaringan (Update meeting 24 Jul)
- Self-healing mesh, automatic failover; diuji hingga **3 hop-list**, latency **<5 dtk normal, 5–15 dtk kondisi ramai**.
- **Cluster Head: konsumsi ~10W, stabil 20 hari non-stop** dengan solar panel (mengonfirmasi temuan 2-panel-surplus sebelumnya).

## Target internal vs baseline resmi (meeting 24 Jul)
- **Baseline resmi (Deck Kick-Off):** field installation target **Desember 2026**.
- **Target internal (belum formal):** survei RU Cilacap **akhir Juli 2026** → instalasi **September 2026**, survei+instalasi digabung 1 kunjungan. RAP Meeting persiapan: **15 Agustus 2026**.
- Strategi deployment: **dual system — server lokal RU + cloud** untuk perbandingan performa.

## Bobot sub-sistem (untuk % dashboard)
net 20 · ai 22 · power 15 · chamber 12 · sw 13 · integ 10 · ruprep 8 · (inisiasi 10 — bila dipakai). Baseline 12-aktivitas → lihat `overview.md`.
