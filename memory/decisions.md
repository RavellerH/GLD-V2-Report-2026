# Decision Log

Keputusan yang membentuk deliverable & arah kerja. Format: ID · tanggal · keputusan · alasan.

| ID | Tgl | Keputusan | Alasan |
|---|---|---|---|
| dec:01 | 23 Jul | Deliverable utama = **dashboard HTML interaktif** | Paling pas untuk pemantauan/monitoring visual |
| dec:02 | 23 Jul | Bahasa = **Bahasa Indonesia** | Sesuai dokumen sumber & audiens |
| dec:03 | 23 Jul | Baseline Kurva-S = **diturunkan dari dokumen**, lalu dikalibrasi ke **Project Timeline 9 bulan (Deck Kick-Off)** | Sumber jadwal paling otoritatif |
| dec:04 | 23 Jul | Scope tracking = **melalui pilot RU IV Cilacap**, 5 RU lain roadmap | Scope aktif nyata hanya 1 RU |
| dec:05 | 23 Jul | **Hapus OGI** (YOLO/thermal) | Belum disetujui klien |
| dec:06 | 23 Jul | Site survey = **plan/workflow selesai, eksekusi pending**; **TRA/JSA jadi gate eksplisit** | Rencana siap; penahan nyata = TRA/JSA |
| dec:07 | 23 Jul | **Uji fungsional GLD-CH-GW-Server** ditandai **selesai** (rantai komunikasi 9 Jul, hingga inferensi AI 16 Jul) | Konfirmasi user |
| dec:08 | 23 Jul | Desain HTML = **korporat navy/steel**; tambah **Executive Summary + panel Progres vs Outstanding** | Client-facing; klien = partner → transparansi |
| dec:09 | 23 Jul | Blocker daya **di-reframe**: bukan "baterai tak bisa suplai" (2,43 W) tapi **"autonomi baterai GLD < target 30 hari"** (draw ON 5,75 W terverifikasi; 7P=1,76 hari) | Data update Juli mengklarifikasi anomali |
| dec:10 | 23 Jul | Buat **memory system** (CLAUDE.md + memory/ + graph) | Pemahaman folder lintas sesi & pencatatan terstruktur |
| dec:11 | 23 Jul | **Tema HTML → biru #2B5FCB + charcoal #262321** (logo Korporasi Kinarya ITB); tambah **navigasi sticky** di dashboard | Arahan user; tampilan klien lebih mudah dibaca |
| dec:12 | 23 Jul | **Koreksi klaim:** inferensi AI di PC+emulator (bukan on-device); **deviasi diturunkan 42→39% / +20** (jangan over-claim); **LoRa disiasati mesh**; **dataset konsisten** (isu resolved) | Klarifikasi user + pendalaman PDF Juli (uji mesh 8-CH) |
| dec:13 | 23 Jul | **Telemetri → "Evolusi Data & Metode Model"** (Tahap 1 → metode saat ini) | Arahan user: tampilkan perubahan demi perubahan |
| dec:14 | 24 Jul | Deployment RU Cilacap = **dual system** (server lokal RU + cloud) untuk perbandingan performa | Keputusan meeting LGU–Pertamina 24 Jul |
| dec:15 | 24 Jul | Survey & instalasi RU Cilacap **digabung 1 kunjungan** bila memungkinkan (target instalasi **Sep 2026**) | Efisiensi kunjungan lapangan; keputusan meeting 24 Jul |
| dec:16 | 24 Jul | Battery version development **lanjut paralel**, TIDAK menghambat deployment versi 24V | 24V sudah siap sertifikasi; battery masih R&D |
| dec:17 | 24 Jul | Gas detection capability **minimum wajib dipastikan**: H₂, LPG, Metana, CO₂, Clean Air (6 kelas) sebelum deployment | Keputusan meeting 24 Jul |
| dec:18 | 24 Jul | **Flame detection (camera, Jetson Nano)** & **sensor arah angin** = pengembangan tambahan terpisah; **BELUM dikonfirmasi masuk scope** dashboard/report resmi | Berpotensi tumpang tindih dengan OGI yang sudah dihapus (dec:05); perlu arahan eksplisit user sebelum dimasukkan ke deliverable manapun |
| dec:19 | 30 Jul | **Reorganisasi folder root** menjadi `Deliverables/` (output Claude) + `Sumber Dokumen/` (dokumen tim/klien); `Dataset/` & `memory/` tetap di root | Root terlalu padat (30+ file bercampur); arahan user "kategorikan folder ini rapi" |
| dec:20 | 30 Jul | Hapus duplikat persis `TCN_GasLPG_Presentation (2) (1).pptx` (md5 identik dgn `(2).pptx`); rename `mom_ruiv_cilacap_gld (1).pdf` → `mom_ruiv_cilacap_gld_ringkasan-AI.pdf` (bukan duplikat, isi beda) | Kebersihan repo saat reorganisasi; arahan user |
| dec:21 | 30 Jul | Klaim **"CNN 1D 97,6%"** dari notulen 24 Jul **direkonsiliasi**: ditemukan `Deteksi_Gas_CNN_Presentasi.pptx` — model klasifikasi jenis gas (3 kelas), **berbeda** dari TCN (prediksi leak time-series). Kedua model sah & boleh dipakai di deliverable | Ditemukan saat kategorisasi file; bukan konflik data, hanya dua model dgn tugas berbeda |
| dec:22 | 30 Jul | Kunjungan Cilacap **9–10 Agustus = survey + instalasi digabung**, **MENGGANTIKAN** rencana 24 Jul (survey akhir Jul → instalasi Sep 2026). Berangkat 9 Agu (Minggu), instalasi 10 Agu (Senin) | Weekly meeting 30 Jul; jadwal tim wajib dikosongkan tanggal tsb |
| dec:23 | 30 Jul | **Wi-Fi ESP32 = HANYA untuk config/serial lokal** (enable/disable via command); **LoRa tetap backbone telemetri utama, selalu aktif** — bukan perubahan arsitektur komunikasi data | Klarifikasi user (weekly meeting 30 Jul), menjawab notulen mentah yang tampak kontradiktif ("gunakan LoRa selalu aktif" vs "komunikasi data lewat WiFi") |
| dec:24 | 30 Jul | Arsitektur deployment RU Cilacap diperjelas: **app + database penuh berjalan lokal** (site RU IV **dan** kantor Jakarta — request **Pak Pindoan** untuk monitoring pusat); **cloud HANYA berperan sebagai gateway/relay ringan**, bukan sistem paralel penuh | Memperjelas (bukan mengganti) dec:14 "dual system" — ini detail konkretnya |
| dec:25 | 30 Jul | Dokumentasi progres harus jadi **knowledge base internal tim**, bukan hanya untuk keperluan client | Prinsip kerja dari weekly meeting 30 Jul |
| dec:26 | 30 Jul | Parameter konfigurasi akan **disederhanakan**, namun operator tetap perlu memahami sejumlah konfigurasi inti (bukan zero-config) | Weekly meeting 30 Jul: keluhan "terlalu banyak parameter" |
| dec:27 | 6 Agu | Mounting GLD & CH mengikuti standar mounting existing di kilang (dibandingkan sistem **Corrosion Monitoring Emerson**): **bracket L / U-clamp** ke struktur existing, **TIDAK bikin struktur baru**, **hindari pengelasan & pengeboran** | Rapat resmi 6 Agu (Notulensi_Rapat_5Agustus2026_GLD.pdf, tanggal di badan dokumen typo — dikonfirmasi 6 Agu); instalasi harus mudah & cepat, tidak butuh struktur baru |
| dec:28 | 6 Agu | **GLD diharapkan bisa mengadopsi topologi sistem corrosion monitoring shg CH juga bisa berfungsi sebagai repeater.** Evaluasi kapasitas GW/CH terhadap jumlah sensor jadi **action item terbuka** (Tim Komunikasi ITB) — ⚠️ **BUKAN** angka pasti "<30 sensor" seperti sempat dicatat dari sumber informal; notulensi resmi tidak menyebut angka tsb | Rapat resmi 6 Agu — versi resmi lebih hati-hati/belum final dibanding catatan informal sebelumnya |
| dec:29 | 6 Agu | Logika alarm dibedakan per jenis gas: gas **mudah terbakar** → alarm berbasis **threshold** batas bahaya kebakaran; gas **toksik** (CO, H2S) → alarm **SEGERA** begitu melebihi ambang batas keselamatan, tanpa menunggu threshold kebakaran. Sistem juga wajib **menampilkan konsentrasi gas (ppm) real-time** (bukan cuma trigger alarm) | Requirement resmi Pertamina (rapat 6 Agu) — risiko kebakaran vs paparan toksik personel butuh penanganan beda; PIC Tim AI ITB |
| dec:30 | 6 Agu | Requirement deteksi gas **bertambah**: **Benzena, CO, H2S** wajib terdeteksi, di luar 6 kelas gate `dec:17` (H₂/LPG/Metana/CO₂/Clean Air) | Requirement resmi Pertamina (rapat 6 Agu) — ⚠️ **BELUM direkonsiliasi**: apakah ini menambah atau menggantikan sebagian gate 6-kelas, perlu klarifikasi ke Pertamina/tim sebelum diupdate ke deliverable gas-capability |
| dec:31 | 6 Agu | Material housing/bracket: **hindari PVC** — dinilai kurang sesuai untuk lingkungan kilang | Requirement resmi Pertamina, area kritis kilang |
| dec:32 | 6 Agu | Sampel gas **tidak diambil langsung di area kilang**; sampel disiapkan & dibawa oleh tim Pertamina ke lokasi pengujian | Requirement akses & keamanan kilang (rapat 6 Agu) |
| dec:33 | 6 Agu | Aplikasi dashboard akan ditambah informasi lokasi perangkat: kolom **"Area"** DAN **identitas Equipment** — bukan cuma "Area" saja | Requirement resmi Pertamina — PIC Tim UI ITB; setiap sensor harus mudah diidentifikasi |
| dec:34 | 6–8 Agu | **Push alarm dinyatakan berhasil diuji**: GLD disemprot LPG di uji mesh kampus (GW+CH1+CH2+CH3) → status server berubah jadi alarm otomatis **tanpa pull request** | Demo persiapan sebelum kunjungan Cilacap; **menyelesaikan** risiko "push alarm belum dicoba" (`decisions.md` konteks dec:22, `blockers_metrics.md` § 30 Jul) |
| dec:35 | 6 Agu | **8 action item resmi dgn PIC formal** ditetapkan (bukan lagi PIC generik "Tim Mekanik/Elektronik"): mounting/bracket→Tim Mekanik ITB; skenario instalasi+dimensi→Tim Mekanik & Vendor Mekanik; evaluasi kapasitas GW/CH→Tim Komunikasi ITB; fitur alarm threshold→Tim AI ITB; info Area+Equipment→Tim UI ITB; kajian pembuangan gas→Tim Instrumentasi ITB; studi banding Emerson/WirelessHART→Tim Komunikasi ITB; rencana sertifikasi→Tim ITB + Pertamina | Notulensi resmi 6 Agu menggantikan penamaan PIC generik yang sempat dipakai di action-item dashboard |

| dec:36 | 9 Agu | Model **CNN Dual-Branch** ✅ **RESMI MENGGANTIKAN CNN 1D** di semua deliverable (dikonfirmasi user). **Akurasi resmi dipakai: 99,20%** (on-chip ESP32-S3 int8) — bukan 99,73% pre-kuantisasi. Kelas kini **LPG/CO2/Udara Bersih/H2** (H2 dikonfirmasi user termasuk meski dokumentasi slide belum lengkap). **Masih TIDAK mencakup H2S/Benzena** (dikonfirmasi user) | File ditemukan di `Sumber Dokumen/` (push langsung Farhan Budiman ke main, 9 Agu, di luar sesi Claude); user konfirmasi eksplisit 9 Agu utk semua poin di atas — update ke Dashboard & Laporan Progres |

## Prinsip yang mengikat
- Klien = partner → selalu tampilkan progres **dan** outstanding; jangan over-claim (analisis ≠ resolusi blocker).
- Headline progres ditahan konservatif (42%) meski engineering di depan; keunggulan murni sisi lab.
- Cilacap = **RU IV** (bukan VI).
- JSA/HSE = **draft**, wajib disahkan HSE RU sebelum dipakai.
- Flame detection (Jetson Nano, camera) **≠** OGI YOLO-thermal (sudah dihapus), tapi statusnya sama: **belum masuk scope resmi report** sampai ada arahan eksplisit user.
- **CNN 1D (klasifikasi gas 3-kelas)** dan **TCN (prediksi leak time-series)** adalah **dua model berbeda, keduanya sah** — jangan disatukan atau dianggap konflik angka (dec:21).
- File di `Sumber Dokumen/` adalah **arsip mentah dari tim/klien** — sebelum mengutip angka baru dari sana ke deliverable, cek dulu apakah sudah tercatat/direkonsiliasi di `memory/` (blockers_metrics.md, entities.md).
- Tanggal Cilacap 9–10 Agustus (dec:22) **menggantikan sepenuhnya** tanggal survey/instalasi versi 24 Jul — jangan tampilkan dua tanggal berbeda di deliverable yang sama tanpa keterangan "revisi".
- Wi-Fi ≠ jalur telemetri utama (dec:23) — jangan gambarkan arsitektur komunikasi data GLD berubah dari LoRa mesh ke WiFi di deliverable manapun.
- Gate gas capability (dec:17, 6 kelas) dan requirement baru Benzena/CO/H2S (dec:30) **belum direkonsiliasi** — jangan tampilkan sebagai daftar tunggal final di deliverable manapun sampai dikonfirmasi apakah bertambah atau menggantikan.
- Sebelum 6 Agu, "push alarm" berstatus **belum dicoba**; per dec:34 sudah **diuji & berhasil** (uji mesh kampus, bukan lapangan RU) — status di deliverable harus dibedakan dari "sudah tervalidasi di lapangan produksi".
- Tanggal rapat mounting/topologi = **6 Agustus 2026 (Kamis)**, dikonfirmasi user — badan teks notulensi resmi (`Notulensi_Rapat_5Agustus2026_GLD.pdf`) salah tulis "5 Agustus", nama file & konfirmasi user jadi acuan yang benar.
- Kapasitas jaringan GW/CH terhadap jumlah sensor **belum ada angka resmi** (action item terbuka, dec:28) — jangan kutip "<30 sensor" sbg spesifikasi established di deliverable manapun.
- **CNN Dual-Branch (dec:36) = model resmi saat ini**, kelas LPG/CO2/Udara Bersih/H2. **Belum menutup H2S/Benzena** (dec:30/gate:gas-extra) — jangan klaim requirement itu terpenuhi berdasarkan model ini. Headline akurasi di deliverable = **99,20%** (on-chip), bukan 99,73%.
- CNN 1D dianggap **superseded** per dec:36 — mention lama boleh tetap ada di histori/notulen (append-only), tapi listing "model AI saat ini" di deliverable harus CNN Dual-Branch.
