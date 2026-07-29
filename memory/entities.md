# Entities — Glosarium

## Organisasi (`org:`)
| ID | Nama | Peran |
|---|---|---|
| org:LGU | LAPI Ganesha Utama | Penyedia & pelaksana sistem |
| org:ITB-IoT | Lab IoT ITB | Engineering, firmware, AI/ML |
| org:ITB-Fisika | Lab Fisika ITB | Dukungan solar/energi |
| org:Pertamina | Pertamina Patra Niaga / Kilang Pertamina Internasional | Klien & partner |

## Orang (`p:`) — dari notulen/laporan
| ID | Nama | Peran/konteks |
|---|---|---|
| p:maman | Pak Maman | Pemaparan GLD, arahan teknis, penataan lab, WDT eksternal |
| p:fahmi | Fahmi | Tim Elektronik — ruang lingkup, DC converter, simulasi daya |
| p:farhan | Farhan Budiman | Repositori kode & collaborator |
| p:fahdzi | Pak Fahdzi | Model TCNN/TCN |
| p:ryan | Ryan (Lab IoT) | Pengumpulan data solar |
| p:ilmania | Ilmania (Lab Fisika) | Titik pengecasan; notulis |
| p:tresnandi | Pak Tresnandi | Dokumen JSA/TRA |
| p:senna | Pak Senna / Pak Sena | Pertamina — lokasi, mode, gateway, koordinasi jadwal survey |
| p:nina | Bu Nina | Hazardous / standar pemasangan |
| p:beny | Kak Beny / Beni | Overall system architecture, AI; testing multi-sensor LoRa Mesh; retry/recovery alarm |
| p:totong | Pak Totong | Diskusi peletakan tiang/rooftop |
| p:muhammad | Pak Muhammad (LGU) | PIC utama meeting 24 Jul — optimasi baterai, VPS, dokumen HSE, perjalanan sertifikasi |
| p:adit | Pak Adit (Pertamina) | Peserta meeting 24 Jul, RU Cilacap |
| p:roni | Mas Roni (Pertamina) | Peserta meeting 24 Jul, RU Cilacap |
| p:indra | Mas Indra (Pertamina, RU Cilacap) | Peserta meeting 24 Jul |

*Catatan: "Ilma" (notulen 24 Jul) = Ilmania; "Beni" = Beny; "Pak Sena" = Pak Senna — variasi ejaan pada sumber berbeda.*

## Sub-sistem (`sub:`)
| ID | Nama | Status ringkas (24 Jul) |
|---|---|---|
| sub:net | Jaringan LoRa & Cluster Head | 65% — failover ok, jangkauan blocker |
| sub:ai | AI & Sensor MQ (CNN 1D 97,6%) | 62% — model CNN 1D 97,6%, dataset konsisten, verifikasi 6 kelas gas berjalan |
| sub:power | Catu Daya & Manajemen Energi | 50% — CH ok (2 panel), autonomi GLD blocker |
| sub:chamber | Gas Chamber, Hardware & QC | 35% — fitur chamber: solenoid valve, pompa duty-cycle, BME280 ganda (eksternal/internal), TGS2610 via ADS1115. Next: PCB layout, pompa senyap, mounting dinding |
| sub:sw | Perangkat Lunak, Server & Dashboard | 58% — MapLibre, Operator Hub, CRUD |
| sub:integ | Integrasi Sistem (GLD-CH-GW-Server) | 68% — fungsional ok; AI on-device pending |
| sub:ruprep | Persiapan & Survei RU / HSE | 40% — plan siap, gate TRA/JSA |

## Perangkat & hardware (`dev:`)
| ID | Nama | Detail |
|---|---|---|
| dev:node | GLD Gas Point Sensor Unit | ESP32-S3 · 8× MQ · ADS1256/ADS1115/MCP3208 · TFLite Micro · TPL5010 duty-cycle |
| dev:ch | Cluster Head | LoRa dual-channel (E22) · solar + 18650 · failover RSSI · IP66/67 · tiang 6 m |
| dev:gw | Gateway | Aggregator mesh · uplink WiFi/4G · MQTT |
| dev:server | PC Server | Node-RED · Operator Hub · backend GraphQL |
| dev:tpl5010 | TPL5010 | Timer nanopower duty-cycle (belum optimal) |
| dev:bq25185 | BQ25185 | Charger + power path solar/baterai |
| dev:tps63020 | TPS63020 | Buck-boost 3,3 V |
| dev:ina219 | INA219 | Sensor arus untuk validasi energi panel |
| dev:solenoid | Solenoid Valve | Pengendalian aliran gas chamber |
| dev:pump | Pompa Chamber | Hisap duty-cycle untuk dinamika udara chamber |
| dev:bme280 | BME280 (×2) | Suhu/tekanan/kelembapan eksternal & internal chamber (I2C addr 0x76/0x77) |
| dev:tgs2610 | TGS2610 | Sensor gas spesifik di dalam chamber (output analog via ADS1115) |
| dev:ads1115 | ADS1115 | ADC eksternal 16-bit untuk TGS2610 (atasi noise ADC internal ESP32) |
| dev:lm2596 | LM2596 | Step-down regulator 5V untuk ESP32/BME280/TGS2610/relay/BTS7960 |
| dev:bts7960 | BTS7960 | Driver motor pompa chamber |

## Repositori (`repo:`)
| ID | Repo | Lapisan | Update terakhir |
|---|---|---|---|
| repo:fe | RavellerH/gasleakdetectionV2-April | Frontend + backend dashboard (Next.js/MapLibre/NestJS-GraphQL) | 13 Jul 2026 |
| repo:srv | fadlurrahmanf/PertaminaGLD | Firmware GLD/CH/GW + server Node-RED + Operator Hub | 23 Jul 2026 |
| repo:ml | RavellerH/gas-leak-ml-chamber-system | ML/AI edge (TFLite Micro, chamber training) | 24 Jun 2026 |

## Refinery Unit (`ru:`)
RU II Dumai · RU III Plaju · **RU IV Cilacap (pilot aktif)** · RU V Balikpapan · RU VI Balongan · RU VII Kasim/Sorong (field test). Detail jumlah → `overview.md`.

## Model AI
- **CNN 1D (fusi 8-sensor MQ) — TERBARU (24 Jul):** akurasi **97,6%**. Gas: H₂, LPG, Metana, CO₂, Clean Air (5 kelas; minimum 6 kelas disyaratkan, verifikasi berjalan). Tiap unit GLD di-training khusus untuk gas target.
- **TCN per-sensor (LPG, Board12, 15 Jul):** 8 model univariat, semua ≥92% (MQ4V 93,9%, F1 0,923), TFLite int8 ~72 KB — fondasi awal sebelum CNN 1D.
- **Multi-task NN:** jenis gas / leak / severity / PPM (repo ML).
- **TCNN:** prediksi 5 dtk dari 5 dtk (Pak Fahdzi).
- ~~OGI YOLOv8-seg (thermal)~~ — **dihapus, belum disetujui.**
- ~~Flame Detection (kamera/Jetson Nano, infrared, 79%)~~ — **ditahan** (disebut di meeting 24 Jul, mirip konsep OGI; belum dimasukkan ke deliverable, menunggu arahan).
