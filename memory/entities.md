# Entities — Glosarium

## Organisasi (`org:`)
| ID | Nama | Peran |
|---|---|---|
| org:LGU | LAPI Ganesha Utama | Penyedia & pelaksana sistem |
| org:ITB-IoT | Lab IoT ITB | Engineering, firmware, AI/ML |
| org:ITB-Fisika | Lab Fisika ITB | Dukungan solar/energi |
| org:Pertamina | Pertamina Patra Niaga / Kilang Pertamina Internasional | Klien & partner |
| org:emerson | Emerson | Vendor sistem **Corrosion Monitoring** (protokol **WirelessHART**) yang sudah terpasang & teruji di kilang — jadi rujukan desain mounting/bracket & topologi jaringan GLD (6 Agu). Bukan vendor/bagian dari proyek GLD. **5 Sep**: user tautkan contoh produk konkret — Rosemount/Emerson **Panel/Pipe Bracket Kit 03031-0189-0004** (SST, 2" pipe bracket + panel bracket, dipakai transmitter 3051T) — bracket J/L melengkung dgn U-bolt di satu ujung (klem ke pipa 2") & pelat panel-mount berlubang di ujung lain. Ini konfirmasi visual konkret pertama utk istilah "L-bracket ref. Emerson" yg sudah dipakai sejak dec:27/40 — pola bentuknya (bracket melengkung + U-bolt + pelat mounting) konsisten dgn pendekatan desain `Desain_Bracket_L_UBolt_GLD_Mounting.html` (31 Agu), meski desain GLD pakai pelat datar bukan bracket melengkung/offset spt Emerson. |

## Kontrak & Proposal (`doc:`)
| ID | Nama | Isi ringkas |
|---|---|---|
| doc:kontrak-payung | Kontrak Payung SP-26015 | Referensi kontrak yg jadi basis perhitungan tarif personil (SBOB/SBOH, Lamp.No.02 KP–Inkindo 2021) di RAB `proposal_GLD_1906M_KONTRAK_PAYUNG_rev2204260830.pdf` (4 Sep, dec:50). Belum ada salinan dokumen kontrak itu sendiri di repo — hanya referensi nomornya di RAB. |
| doc:proposal-gld | Proposal GLD Point Sensor Network (Feb 2026) | `Sumber Dokumen/proposal_GLD_1906M_KONTRAK_PAYUNG_rev2204260830.pdf` — proposal formal ke Pertamina Patra Niaga, LGU+Korporasi Kinarya ITB, **fokus sensor titik GLD** 6 RU. RAB Rp1.906.638.909. Berisi ringkasan singkat integrasi OGI (bag. 10) — versi lengkapnya di `doc:proposal-ogi` (dokumen terpisah). Lih. dec:50–53. |
| doc:proposal-ogi | Proposal OGI Thermal Camera Integration (Feb/Mar 2026) | `Sumber Dokumen/[KONTRAK PAYUNG] PROPOSAL Gas Leak Detection System – Tahap 2 Integrasi Thermal Camera...(5340M).pdf` — proposal formal **terpisah** (44 hlm) khusus integrasi kamera OGI MWIR ke GLD Tahap 1. Kamera **HJK-MWIR MC11H** (3-5µm gas filter, cooled MCT 640×512, 100Hz, ±100m jarak deteksi, mounting ±10m). Model AI kamera: **YOLOv8-seg** (plume segmentation). RAB **Rp5.341.943.700** — terpisah dari RAB GLD Point Sensor. Ditemukan di `main` 4 Sep di luar sesi Claude. Lih. dec:53. |
| doc:proposal-sertifikasi | Proposal Sertifikasi GLD (21 Feb 2026) | `Sumber Dokumen/PROPOSAL SERTIFIKASI GAS LEAK DETECTION SYSTEM(...)[21 FEB 2026].pdf` — cakupan ATEX+IP+EMC+RF terpadu, RAB Rp2.099.240.000, estimasi 5–8 bulan. Tanggal dikonfirmasi via nama file asli (21 Feb 2026) — teks cover dokumen "Februari 2025" kemungkinan typo tahun. Lih. dec:50–53. |

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
| sub:integ | Integrasi Sistem (GLD-CH-GW-Server) | 68% — rantai komponen dan push alarm fungsional di lab; inferensi lokal/on-device terdokumentasi generik di TDS R4 dan dikonfirmasi user untuk CNN Dual-Branch, tetapi adapter MQTT→backend serta commissioning RU masih terbuka |
| sub:ruprep | Persiapan & Survei RU / HSE | 40% — plan siap, gate TRA/JSA |

## Perangkat & hardware (`dev:`)
| ID | Nama | Detail |
|---|---|---|
| dev:node | GLD Gas Point Sensor Unit | ESP32-S3-WROOM-1U-N16R8 · 8× MQ dengan urutan kanonik MQ8/MQ135/MQ3/MQ5/MQ4/MQ7/MQ6/MQ2 · ADS1256 24-bit (30kSPS component setting, scan firmware 500ms, moving average 10 sampel, batch wajib 8/8 valid) · SHT40 · E22-900MM22S LoRa STAR · RS-485 Modbus RTU read-only 8 register · alarm eksternal steady 24V (AUTO default; MANUAL session-only) · laporan radio nominal 10s + receive window 2s · **catu daya final deployment: 24VDC ≥1A/unit** (dec:47), varian baterai nominal 4,2V; monitoring low/critical 3,50/3,30V hanya diagnostik, bukan active cutoff. TDS R4 mengonfirmasi pemrosesan/inferensi lokal secara generik, tetapi hanya mencantumkan Clean Air/LPG/H2 dan tidak menyebut CNN Dual-Branch/CO2/99,20%/int8 9,14KB — lihat dec:57/gate:tds-ai-profile. Spek fisik/EMC & mounting tetap mengikuti dec:40/45. |
| dev:ch | Cluster Head | ESP32-S3 + **2× E22-900MM22S**: Radio A STAR (920MHz/SF7/3dBi) dan Radio B MESH (921MHz/SF9/8dBi); serving CH sekaligus transit CH, dynamic parent discovery/root reachability/loop guard/failover. TDS R4 capacity: 8 kandidat parent, 32 cache node, 8 alarm queue, 8 TX queue, 16 pending downlink; parent stale 16min, min dwell 5min, switch margin 15dB, cache TTL 60min. Energi: 1–3 sel LiitoKala 18650 paralel + 2 panel 6W paralel melalui BQ25185; VBAT read-only tanpa low-power/cutoff otomatis. Varian PCB Rectangle/Circle wajib cocok dengan firmware. Spek fisik/EMC, mounting, serta gate solar/baterai tetap mengikuti dec:40/41/45. |
| dev:gw | Gateway | ESP32-S3 pada basis PCB CH Rectangle/Circle; **hanya Radio B/MESH aktif** (921MHz/SF9/8dBi), Radio A/STAR dinonaktifkan. Bridge MESH→**Wi-Fi STA native**→MQTT; firmware standard(non-TLS) dan CA-verified TLS terpisah. Gateway ID default 0x0001, configurable 0x0001–0x000F. Queue MQTT 8 publikasi volatil, payload 1–1023B; item baru ditolak saat penuh dan queue hilang saat restart. TDS R4 menyatakan **tidak ada Ethernet native** dan adapter Wi-Fi→Ethernet hanya aksesori eksternal; ini mempertegas konflik dengan spek EMC yang menyebut port Ethernet (`gate:gw-ethernet`). |
| dev:server | PC Server | Aplikasi **Node-RED** pada VM/PC customer: MQTT ingress, validasi struktur/panjang/CRC, dekode+autentikasi AES-128-GCM, anti-replay persisten, routing alarm, topologi engineering, dan limited high-level command. TLS Server↔broker adalah sesi terpisah dari Gateway↔broker. MySQL/CSV pada TDS R4 hanya untuk **dataset engineering**, bukan otomatis storage seluruh telemetri/alarm/topologi; backend GraphQL/dashboard dan baseline SQLite pilot adalah lapisan aplikasi lain yang perlu adapter MQTT (`gate:mqtt-adapter`) dan rekonsiliasi DB (`gate:db-baseline`). |
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
| repo:cert | RavellerH/sertifikasi-atex-gld-v2-2026 | **Repo sister khusus tracking sertifikasi IECEx/ATEX** — dihubungkan 4 Sep (`add_repo`, akses baca publik). **Aktif memakai gate ID repo ini** (`gate:cert-height`, `gate:solar-cert`, `gate:ch-batt-safety`, `gate:capacity`) sbg sumber, dan mengutip `Datasheet_Sistem_GLD_Arsitektur_ServerJaringan.html`, `Notulen_Meeting_GLD_6Agustus2026.pdf`, `Parameter spesifikasi EMC_lengkap.docx` sbg referensi eksternal — jadi ini benar konsumen aktif dari repo ini, bukan proyek independen. Isi: `ANALISIS-KEKURANGAN.md` (gap analysis vs `IECEx ATEX Certification Information Requirements_Ind.docx`), `CHECKLIST-PERSIAPAN.md`, `REFERENSI-KOMPONEN-BOM.md` (riset pembanding enclosure Ex-rated komersial), `Dokumen_spesifikasi_input_2.docx` (spek 3 perangkat, ~40/56 field terisi per 26 Agu), `Laporan-Sertifikasi-ATEX-GLD-V2-2026.pdf` (5 hlm), foto casing di `GLD/`, gambar teknik bracket. Lih. dec:54 utk temuan kunci. **5 Sep (dec:68): repo di-clone penuh & disalin ke `Sumber Dokumen/sertifikasi-atex-gld-v2-2026/`** (tidak ada commit baru sejak 27 Agu, snapshot masih akurat) — kini ada juga salinan lokal, tidak hanya rujukan; ditambah `IECEx ATEX Certification Information Requirements_EN.pdf` (versi asli Inggris/Mandarin dari ExCB, diberikan user langsung, menggantikan versi terjemahan Indonesia sbg acuan). | 5 Sep 2026 |

## Refinery Unit (`ru:`)
RU II Dumai · RU III Plaju · **RU IV Cilacap (pilot aktif)** · RU V Balikpapan · RU VI Balongan · RU VII Kasim/Sorong (field test). Detail jumlah → `overview.md`.

## Model AI
- **TCN per-sensor (LPG):** 8 model univariat, semua ≥92% (MQ4V 93,9%, F1 0,923), TFLite int8 ~72 KB. Prediksi **leak LPG 5 detik ke depan** dari 15 dtk lookback (Board12, 3.234 baris). Sumber: `Board12_TCN_PerSensor.pptx`.
- **CNN 1D (klasifikasi jenis gas):** model **terpisah** dari TCN — tugasnya klasifikasi 3 kelas (Clean Air/LPG/CO2), bukan prediksi leak time-series. 5 layer (Conv1D 16 filter→MaxPool→Dense 16→Softmax), 1.155 parameter. **Model PC** (`cnn_gas_model.keras`, 43 KB): **97,6% akurasi test** (374 data holdout, F1-macro 97,55%; per-kelas F1 Clean Air 0,99/LPG 0,98/CO2 0,96). **Model ESP32-S3** (`cnn_gas_model_data.h`, int8, 7,4 KB): 97,3% akurasi (kompresi 83%, turun 0,27 poin). Validasi lapangan: 3.466 pembacaan device F001 (20 Jul 2026), keyakinan rata-rata 98,6%, 34 baris (1%) ditandai untuk tinjauan manual. Sumber: `Deteksi_Gas_CNN_Presentasi.pptx` (Lab IoT ITB). **Ini yang dimaksud "CNN 1D 97,6%" di notulen 24 Jul — sudah direkonsiliasi, bukan konflik dgn TCN.**
- **CNN Dual-Branch (klasifikasi jenis gas) — ✅ MODEL RESMI SAAT INI, MENGGANTIKAN CNN 1D** (dikonfirmasi user 9 Agu). Kelas: **LPG, CO2, Udara Bersih**, **+ H2 (Hidrogen)** — H2 memang dilatih/diuji model ini (dikonfirmasi user), hanya **belum didokumentasikan lengkap di slide utama** (baru muncul di slide uji-lapangan). Arsitektur 2 cabang: **Cabang A** (Conv1D 16 filter k=3→MaxPool→Flatten, dari 8 sensor MQ mentah) + **Cabang B** (Dense 8, dari 7 fitur "evidence" sensitivitas datasheet MQ per gas — tabel statis, bukan data sensor) → Concatenate → Dense 16 → Dense 3 Softmax. **1.347 parameter.** **Akurasi resmi dipakai (headline): 99,20%** — angka **on-chip ESP32-S3 (TFLite int8, 9,14 KB)**, yaitu yang benar-benar berjalan di perangkat (dikonfirmasi user: pakai angka ESP32-S3 walau turun tipis dari versi PC, penurunan tidak signifikan). Angka pendukung lain: Keras/PC 99,73% (F1 rata-rata 99,56%; per-kelas presisi LPG 100%/220, CO2 100%/109, Udara Bersih 98%/45), TFLite float32 99,73% (11,29 KB) — **kedua angka ini pre-kuantisasi, bukan yg dipakai untuk klaim ke client**. Dataset: 1.870 pembacaan unik (1.496 train/374 test, LPG 1099/CO2 545/Udara Bersih 226). Uji lapangan real-time on-device (device 1001, ~11,7 menit, 1.176 pembacaan): **97,65% akurasi** (kelas H2 termasuk di sini). Slide 11 eksplisit menyebut CNN 1D sbg "model CNN satu-cabang sebelumnya". Sumber: `Sumber Dokumen/06 Aguatus Deteksi_Kebocoran_Gas_CNN_DualBranch (2)  -  Repaired.pptx` (Lab IoT ITB; dibuat 29 Jul, diedit terakhir 6 Agu oleh **Ilmania Syakira**; di-push ke repo oleh Farhan Budiman 9 Agu — commit "AI update", di luar sesi Claude ini). ⚠️ **Masih TIDAK mencakup H2S maupun Benzena** (dikonfirmasi user) — requirement wajib baru dari rapat 6 Agustus (`decisions.md` dec:30) — jadi **belum menutup `gate:gas-extra`** sepenuhnya, meski H2 (bagian dari gate 6-kelas lama dec:17) kini tercakup. Status **CO** (karbon monoksida, beda dari CO2) belum eksplisit dikonfirmasi — perlu klarifikasi lanjut ke tim bila relevan.
- **Multi-task NN:** jenis gas / leak / severity / PPM (repo ML).
- **TCNN:** prediksi 5 dtk dari 5 dtk (Pak Fahdzi).
- ~~OGI YOLOv8-seg (thermal)~~ — **dihapus, belum disetujui.** Materi sumber: `LangGas_Top6000_Progress.pptx` (arsip, jangan dipakai lagi tanpa arahan).
