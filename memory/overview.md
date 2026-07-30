# Overview — Proyek GLD Tahap 2

## Ringkasan
Sistem **Gas Leak Detection (GLD) Point Sensor Network** — deteksi dini kebocoran gas berbahaya secara real-time berbasis **multi-sensor MQ + AI edge**, komunikasi **LoRa low-power star-mesh**, dengan dashboard monitoring. Sistem bersifat **pelengkap** (bukan pengganti) sistem eksisting Pertamina. TRL-7 (level industri).

## Pihak
- **LAPI Ganesha Utama (LGU)** — penyedia & pelaksana (unit, casing, CH, GW, solar, instalasi via pihak ke-3).
- **Lab IoT ITB** (Instrumentation & Computation RG) — engineering, firmware, AI/ML, dataset.
- **Lab Fisika ITB** — dukungan (mis. solar/energi).
- **PT Pertamina Patra Niaga / Kilang Pertamina Internasional** — klien & partner; menentukan titik pasang, izin, HSE per RU.

## Scope (dari Deck Kick-Off 12 Jun 2026)
**In-scope:** deteksi kebocoran, peringatan & notifikasi, konektivitas LoRa, dashboard & monitoring, keselamatan/kepatuhan HSE, pengembangan+implementasi+testing, pelatihan & knowledge transfer.
**Out-of-scope:** perbaikan kebocoran fisik, analisa lab, infrastruktur non-elektrikal, integrasi DCS/SCADA/ERP (belum), pelatihan non-pengguna, perluasan di luar area disepakati, custom software di luar kebutuhan inti.

## Deployment (Dokumen Kebutuhan Peralatan per RU v1.0)
Total 6 RU: **28 gas sensor · 22 Cluster Head · 7 Gateway · 22 solar CH · 7 solar GW**.

| RU | Lokasi | Sensor | CH | GW | Status |
|---|---|--:|--:|--:|---|
| RU II | Dumai | 10 | 3 | 1 | Roadmap |
| RU III | Plaju | 4 | 3 | 1 | Roadmap |
| **RU IV** | **Cilacap** | **3** | **2** | **1** | **Aktif (pilot)** |
| RU V | Balikpapan | 2 | 1 | 1 | Roadmap |
| RU VI | Balongan | 4 | 2 | 2 | Roadmap |
| RU VII | Kasim/Sorong | 5 | 11 | 1 | Roadmap (field test) |

## Konsep operasi
Sensor mendeteksi gas → inferensi AI di edge → data via LoRa (STAR ke CH, MESH antar-CH) → Gateway → PC Server (Node-RED + backend) → Dashboard (peta, alarm, trend, health). Operator merespon & dokumentasi insiden. Downlink (server→node) untuk perintah/mode.

## Baseline & jadwal (official 9 bulan, dari Deck Kick-Off)
12 aktivitas: Kick-off → Site survey & data plan → Detailed design → Prototype build → Lab test → AI training/validation → Integration test → HSE review & permit → Field installation (target Des) → Field trial → Evaluation & final report → Industrialization roadmap. Mulai Jun 2026, selesai Feb 2027.

## Catatan manajerial
- Proyek TRL-7 (vs riset FI umumnya TRL-3). Prinsip: "lebih baik banyak bekerja daripada banyak rapat".
- Dua SPK: (1) compiler & sertifikasi hazardous area; (2) implementasi 6 unit kilang.
- Alur menuju RU: LGU undang Pertamina ke lab → uji lab → kunjungan RU.
