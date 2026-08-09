# Entities — Glosarium

## Organisasi (`org:`)
| ID | Nama | Peran |
|---|---|---|
| org:LGU | LAPI Ganesha Utama | Penyedia & pelaksana sistem |
| org:ITB-IoT | Lab IoT ITB | Engineering, firmware, AI/ML |
| org:ITB-Fisika | Lab Fisika ITB | Dukungan solar/energi |
| org:Pertamina | Pertamina Patra Niaga / Kilang Pertamina Internasional | Klien & partner |
| org:emerson | Emerson | Vendor sistem **Corrosion Monitoring** (protokol **WirelessHART**) yang sudah terpasang & teruji di kilang — jadi rujukan desain mounting/bracket & topologi jaringan GLD (6 Agu). Bukan vendor/bagian dari proyek GLD. |

## Orang (`p:`) — dari notulen/laporan
| ID | Nama | Peran/konteks |
|---|---|---|
| p:maman | Pak Maman | Pemaparan GLD, arahan teknis, penataan lab, WDT eksternal |
| p:fahmi | Fahmi | Tim Elektronik — ruang lingkup, DC converter, simulasi daya |
| p:farhan | Farhan Budiman | Repositori kode & collaborator |
| p:fahdzi | Pak Fahdzi | Model TCNN/TCN |
| p:ryan | Ryan (Lab IoT) | Pengumpulan data solar |
| p:ilmania | Ilmania Syakira (disebut "Ilma"/"Ilmania") | Titik pengecasan; notulis; PIC verifikasi gas capability (dec 24 Jul); penulis/editor terakhir presentasi model **CNN Dual-Branch** (6 Agu) — kemungkinan lintas Lab Fisika & Lab IoT, belum dikonfirmasi |
| p:tresnandi | Pak Tresnandi | Dokumen JSA/TRA; ditanya soal sisa anggaran proyek (sudah didistribusikan) — pertanyaan terbuka dari weekly meeting 30 Jul |
| p:senna | Pak Senna | Pertamina — lokasi, mode, gateway |
| p:nina | Bu Nina | Hazardous / standar pemasangan |
| p:beny | Kak Beny | Overall system architecture, AI |
| p:totong | Pak Totong | Diskusi peletakan tiang/rooftop |
| p:adit | Pak Adit | Pertamina — meeting 24 Jul |
| p:roni | Mas Roni | Pertamina — meeting 24 Jul |
| p:indra | Mas Indra | Pertamina, RU Cilacap — meeting 24 Jul |
| p:pinduan | Pak Pindoan | Pertamina — meminta instalasi aplikasi monitoring di kantor pusat Jakarta (selain site), weekly meeting 30 Jul |
| p:raihan | Raihan Fakhar | Pertamina, PIC **RU VII Kasim** — arahan mounting GLD/CH ikuti pola existing (6 Agu); dicc Farhan utk contoh desain bracket/repeater Emerson |

> Catatan: "Pak Sena" (notulen 24 Jul) kemungkinan sama dengan `p:senna` (Pak Senna); "Pak Maman" konsisten dengan `p:maman`. "Pak Muhammad" (LGU, notulen 24 Jul) belum punya ID — kemungkinan overlap dengan `p:beny`/`p:maman`, perlu klarifikasi.

## Sub-sistem (`sub:`)
| ID | Nama | Status ringkas (24 Jul) |
|---|---|---|
| sub:net | Jaringan LoRa & Cluster Head | 65% — failover ok, jangkauan blocker. ⚠️ Requirement baru (6 Agu, belum dikerjakan): GLD mampu berfungsi sbg CH, topologi bypass-ke-GW ala mesh-tree, app "Gateway Manager" (lih. `decisions.md` dec:28, `blockers_metrics.md` § 6 Agu) |
| sub:ai | AI & Sensor MQ (TCN LPG) | 55% — TCN ≥92%, dataset konsisten |
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
| dev:jetson | Jetson Nano | **Tentatif/belum masuk scope resmi** — hardware flame detection camera-based (dibeli); model 79% akurasi, dataset dari Google + kamera infrared. Lih. `decisions.md` dec:18 |
| dev:windsensor | Sensor Arah Angin | **Rencana**, belum ada timeline/PIC — untuk early warning (prediksi dispersi gas/flame spread) |

## Repositori (`repo:`)
| ID | Repo | Lapisan | Update terakhir |
|---|---|---|---|
| repo:fe | RavellerH/gasleakdetectionV2-April | Frontend + backend dashboard (Next.js/MapLibre/NestJS-GraphQL) | 13 Jul 2026 |
| repo:srv | fadlurrahmanf/PertaminaGLD | Firmware GLD/CH/GW + server Node-RED + Operator Hub | 23 Jul 2026 |
| repo:ml | RavellerH/gas-leak-ml-chamber-system | ML/AI edge (TFLite Micro, chamber training) | 24 Jun 2026 |

## Refinery Unit (`ru:`)
RU II Dumai · RU III Plaju · **RU IV Cilacap (pilot aktif)** · RU V Balikpapan · RU VI Balongan · RU VII Kasim/Sorong (field test). Detail jumlah → `overview.md`.

## Model AI
- **TCN per-sensor (LPG):** 8 model univariat, semua ≥92% (MQ4V 93,9%, F1 0,923), TFLite int8 ~72 KB. Prediksi **leak LPG 5 detik ke depan** dari 15 dtk lookback (Board12, 3.234 baris). Sumber: `Board12_TCN_PerSensor.pptx`.
- **CNN 1D (klasifikasi jenis gas):** model **terpisah** dari TCN — tugasnya klasifikasi 3 kelas (Clean Air/LPG/CO2), bukan prediksi leak time-series. 5 layer (Conv1D 16 filter→MaxPool→Dense 16→Softmax), 1.155 parameter. **Model PC** (`cnn_gas_model.keras`, 43 KB): **97,6% akurasi test** (374 data holdout, F1-macro 97,55%; per-kelas F1 Clean Air 0,99/LPG 0,98/CO2 0,96). **Model ESP32-S3** (`cnn_gas_model_data.h`, int8, 7,4 KB): 97,3% akurasi (kompresi 83%, turun 0,27 poin). Validasi lapangan: 3.466 pembacaan device F001 (20 Jul 2026), keyakinan rata-rata 98,6%, 34 baris (1%) ditandai untuk tinjauan manual. Sumber: `Deteksi_Gas_CNN_Presentasi.pptx` (Lab IoT ITB). **Ini yang dimaksud "CNN 1D 97,6%" di notulen 24 Jul — sudah direkonsiliasi, bukan konflik dgn TCN.**
- **CNN Dual-Branch (klasifikasi jenis gas, versi baru/penerus CNN 1D):** 3 kelas sama dgn CNN 1D (**LPG/CO2/Udara Bersih** — **BUKAN** CO atau H2S). Arsitektur 2 cabang: **Cabang A** (Conv1D 16 filter k=3→MaxPool→Flatten, dari 8 sensor MQ mentah) + **Cabang B** (Dense 8, dari 7 fitur "evidence" sensitivitas datasheet MQ per gas — tabel statis, bukan data sensor) → Concatenate → Dense 16 → Dense 3 Softmax. **1.347 parameter.** Akurasi: **Keras/PC 99,73%** (F1 rata-rata 99,56%; per-kelas presisi LPG 100%/220, CO2 100%/109, Udara Bersih 98%/45), **TFLite float32 99,73%** (11,29 KB), **TFLite int8 di ESP32-S3 99,20%** (9,14 KB — headline slide 1 "99,73%" **keliru mengutip angka pre-kuantisasi**, bukan angka on-chip yg sebenarnya dipakai). Dataset: 1.870 pembacaan unik (1.496 train/374 test, LPG 1099/CO2 545/Udara Bersih 226). Uji lapangan real-time on-device (device 1001, ~11,7 menit, 1.176 pembacaan): **97,65% akurasi** — ⚠️ slide ini menyebut kelas **"H2"** yg **tidak konsisten** dgn skema 3-kelas yg dideklarasikan (LPG/CO2/Udara Bersih) di slide lain — **belum diverifikasi ke tim sumber**, jangan dikutip sbg fakta sebelum klarifikasi. Slide 11 eksplisit menyebut model lama (CNN 1D) sbg "model CNN satu-cabang sebelumnya" → **CNN Dual-Branch = penerus/evolusi CNN 1D**, bukan model tak terkait; namun **belum ada arahan resmi** apakah ini menggantikan CNN 1D di deliverable atau berjalan paralel. Sumber: `Sumber Dokumen/06 Aguatus Deteksi_Kebocoran_Gas_CNN_DualBranch (2)  -  Repaired.pptx` (Lab IoT ITB; dibuat 29 Jul, diedit terakhir 6 Agu oleh **Ilmania Syakira**; di-push ke repo oleh Farhan Budiman 9 Agu — commit "AI update", di luar sesi Claude ini). ⚠️ **PENTING:** model ini (spt CNN 1D) **masih TIDAK mencakup CO, H2S, atau Benzena** — gas yg jadi requirement wajib baru dari rapat 6 Agustus (`decisions.md` dec:30) — jadi **belum menutup `gate:gas-extra`** meski akurasinya naik signifikan dari CNN 1D.
- **Multi-task NN:** jenis gas / leak / severity / PPM (repo ML).
- **TCNN:** prediksi 5 dtk dari 5 dtk (Pak Fahdzi).
- ~~OGI YOLOv8-seg (thermal)~~ — **dihapus, belum disetujui.** Materi sumber: `LangGas_Top6000_Progress.pptx` (arsip, jangan dipakai lagi tanpa arahan).
