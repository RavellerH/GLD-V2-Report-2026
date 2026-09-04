# Entities — Glosarium

## Organisasi (`org:`)
| ID | Nama | Peran |
|---|---|---|
| org:LGU | LAPI Ganesha Utama | Penyedia & pelaksana sistem |
| org:ITB-IoT | Lab IoT ITB | Engineering, firmware, AI/ML |
| org:ITB-Fisika | Lab Fisika ITB | Dukungan solar/energi |
| org:Pertamina | Pertamina Patra Niaga / Kilang Pertamina Internasional | Klien & partner |
| org:emerson | Emerson | Vendor sistem **Corrosion Monitoring** (protokol **WirelessHART**) yang sudah terpasang & teruji di kilang — jadi rujukan desain mounting/bracket & topologi jaringan GLD (6 Agu). Bukan vendor/bagian dari proyek GLD. |
| org:samindo | PT Samindo (ekosistem manufaktur Samsung Indonesia) | **Mitra manufaktur/skala** untuk permintaan volume besar (disebut 27 Agu di `Deliverables/GLD_Executive_Presentation.pptx`, instruksi langsung user — belum ada detail kontrak/kapasitas/status kerja sama tertulis di dokumen lain; disebut generik sbg "manufacturing/scale partner"). |

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
| p:nina | Bu Nina (Dr. Nina Siti Aminah, ITB Fisika) | Hazardous / standar pemasangan; penulis `Parameter spesifikasi EMC_lengkap.docx` (19 Agu) |
| p:beny | Kak Beny | Overall system architecture, AI |
| p:totong | Pak Totong | Diskusi peletakan tiang/rooftop |
| p:adit | Pak Adit | Pertamina — meeting 24 Jul |
| p:roni | Mas Roni | Pertamina — meeting 24 Jul |
| p:indra | Mas Indra | Pertamina, RU Cilacap — meeting 24 Jul |
| p:pinduan | Pak Pindoan | Pertamina — meminta instalasi aplikasi monitoring di kantor pusat Jakarta (selain site), weekly meeting 30 Jul |
| p:raihan | Raihan Fakhar ("Pak Raihan") | Pertamina, PIC **RU VII Kasim** — arahan mounting GLD/CH ikuti pola existing (rapat 6 Agu); **menanyakan kebutuhan solar panel** untuk GLD (baterai+solar) di rapat yang sama, diteruskan via WA ke Beny (ITB Fisika) utk dihitung |

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
| dev:node | GLD Gas Point Sensor Unit | ESP32-S3 · 8× MQ · ADS1256/ADS1115/MCP3208 · TFLite Micro · TPL5010 duty-cycle · **catu daya final: 24VDC ≥1A/unit (dec:39, direvisi dari ≥2A per dec:47)**, kabel+PSU disediakan RU/kilang · mounting L-bracket ref. Emerson (dec:40) · **spek EMC (dec:45)**: modul radio E22-900MM22S (TX maks 22dBm, dikonfigurasi 17dBm), antena omni 3dBi, dimensi 20×9×29cm, enclosure metal Ex-Proof, konsumsi maks 7,995W (versi 24VDC kontinu, beda dari draw ON 5,75W versi baterai duty-cycled), port USB/sensor/power/fan/antena/buzzer |
| dev:ch | Cluster Head | LoRa dual-channel (E22) · solar + 18650 · failover RSSI · IP66/67 · tiang 6 m · mounting L-bracket ref. Emerson bareng solar panel (dec:40) · gate terbuka: sertifikasi solar hazardous (gate:solar-cert) & keamanan baterai 18650 di kilang (gate:ch-batt-safety) · **spek EMC (dec:45)**: modul radio E22-900MM22S, antena fiber 3dBi(STAR)/8dBi(MESH), dimensi 8×8×21cm, enclosure metal, konsumsi maks 0,73W · ⚠️ spek EMC sebut input power **5VDC** — belum rekonsiliasi dgn solar+18650 lapangan, perlu klarifikasi |
| dev:gw | Gateway | Aggregator mesh · uplink WiFi/4G · MQTT · **spek EMC (dec:45)**: antena fiber 8dBi, dimensi 8×8×21cm (housing sama dgn CH), enclosure metal, konsumsi maks 0,73W, **port Ethernet tersedia selain Wi-Fi** (belum jelas apakah firmware sudah dukung) |
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
| repo:srv | fadlurrahmanf/PertaminaGLD | Firmware GLD/CH/GW + server Node-RED + Operator Hub | 23 Jul 2026 — berisi juga `Pertamina_GLD_Protocol_Reference.md` (spek frame protokol lengkap) dan 2 dokumen integrasi server/jaringan bertanggal **13 Agu 2026**: `docs/manual/Gateway-to-Server-Site-IT-Pertamina.docx` (kebutuhan jaringan utk tim IT Pertamina) & `Gateway-to-Server-Site-Technical-Datasheet.docx` (kontrak MQTT/topik/keamanan teknis); keduanya ditandai eksplisit "draft source-backed — belum bukti broker/deployment/hardware live". Dirangkum ke `Deliverables/Datasheet_Sistem_GLD_Arsitektur_ServerJaringan.html` bagian 07 (19 Agu). |
| repo:ml | RavellerH/gas-leak-ml-chamber-system | ML/AI edge (TFLite Micro, chamber training) | 24 Jun 2026 |

## Refinery Unit (`ru:`)
RU II Dumai · RU III Plaju · **RU IV Cilacap (pilot aktif)** · RU V Balikpapan · RU VI Balongan · RU VII Kasim/Sorong (field test). Detail jumlah → `overview.md`.

## Model AI
- **TCN per-sensor (LPG):** 8 model univariat, semua ≥92% (MQ4V 93,9%, F1 0,923), TFLite int8 ~72 KB. Prediksi **leak LPG 5 detik ke depan** dari 15 dtk lookback (Board12, 3.234 baris). Sumber: `Board12_TCN_PerSensor.pptx`.
- **CNN 1D (klasifikasi jenis gas):** model **terpisah** dari TCN — tugasnya klasifikasi 3 kelas (Clean Air/LPG/CO2), bukan prediksi leak time-series. 5 layer (Conv1D 16 filter→MaxPool→Dense 16→Softmax), 1.155 parameter. **Model PC** (`cnn_gas_model.keras`, 43 KB): **97,6% akurasi test** (374 data holdout, F1-macro 97,55%; per-kelas F1 Clean Air 0,99/LPG 0,98/CO2 0,96). **Model ESP32-S3** (`cnn_gas_model_data.h`, int8, 7,4 KB): 97,3% akurasi (kompresi 83%, turun 0,27 poin). Validasi lapangan: 3.466 pembacaan device F001 (20 Jul 2026), keyakinan rata-rata 98,6%, 34 baris (1%) ditandai untuk tinjauan manual. Sumber: `Deteksi_Gas_CNN_Presentasi.pptx` (Lab IoT ITB). **Ini yang dimaksud "CNN 1D 97,6%" di notulen 24 Jul — sudah direkonsiliasi, bukan konflik dgn TCN.**
- **CNN Dual-Branch (klasifikasi jenis gas) — ✅ MODEL RESMI SAAT INI, MENGGANTIKAN CNN 1D** (dikonfirmasi user 9 Agu). Kelas: **LPG, CO2, Udara Bersih**, **+ H2 (Hidrogen)** — H2 memang dilatih/diuji model ini (dikonfirmasi user), hanya **belum didokumentasikan lengkap di slide utama** (baru muncul di slide uji-lapangan). Arsitektur 2 cabang: **Cabang A** (Conv1D 16 filter k=3→MaxPool→Flatten, dari 8 sensor MQ mentah) + **Cabang B** (Dense 8, dari 7 fitur "evidence" sensitivitas datasheet MQ per gas — tabel statis, bukan data sensor) → Concatenate → Dense 16 → Dense 3 Softmax. **1.347 parameter.** **Akurasi resmi dipakai (headline): 99,20%** — angka **on-chip ESP32-S3 (TFLite int8, 9,14 KB)**, yaitu yang benar-benar berjalan di perangkat (dikonfirmasi user: pakai angka ESP32-S3 walau turun tipis dari versi PC, penurunan tidak signifikan). Angka pendukung lain: Keras/PC 99,73% (F1 rata-rata 99,56%; per-kelas presisi LPG 100%/220, CO2 100%/109, Udara Bersih 98%/45), TFLite float32 99,73% (11,29 KB) — **kedua angka ini pre-kuantisasi, bukan yg dipakai untuk klaim ke client**. Dataset: 1.870 pembacaan unik (1.496 train/374 test, LPG 1099/CO2 545/Udara Bersih 226). Uji lapangan real-time on-device (device 1001, ~11,7 menit, 1.176 pembacaan): **97,65% akurasi** (kelas H2 termasuk di sini). Slide 11 eksplisit menyebut CNN 1D sbg "model CNN satu-cabang sebelumnya". Sumber: `Sumber Dokumen/06 Aguatus Deteksi_Kebocoran_Gas_CNN_DualBranch (2)  -  Repaired.pptx` (Lab IoT ITB; dibuat 29 Jul, diedit terakhir 6 Agu oleh **Ilmania Syakira**; di-push ke repo oleh Farhan Budiman 9 Agu — commit "AI update", di luar sesi Claude ini). ⚠️ **Masih TIDAK mencakup H2S maupun Benzena** (dikonfirmasi user) — requirement wajib baru dari rapat 6 Agustus (`decisions.md` dec:30) — jadi **belum menutup `gate:gas-extra`** sepenuhnya, meski H2 (bagian dari gate 6-kelas lama dec:17) kini tercakup. Status **CO** (karbon monoksida, beda dari CO2) belum eksplisit dikonfirmasi — perlu klarifikasi lanjut ke tim bila relevan.
- **Multi-task NN:** jenis gas / leak / severity / PPM (repo ML).
- **TCNN:** prediksi 5 dtk dari 5 dtk (Pak Fahdzi).
- ~~OGI YOLOv8-seg (thermal)~~ — **dihapus, belum disetujui.** Materi sumber: `LangGas_Top6000_Progress.pptx` (arsip, jangan dipakai lagi tanpa arahan).
