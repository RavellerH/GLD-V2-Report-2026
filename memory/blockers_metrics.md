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
- ~~risiko "push alarm belum dicoba"~~ (dari 30 Jul) → **diuji & berhasil** 6–8 Agu: GLD disemprot LPG di uji mesh kampus (GW+CH1+CH2+CH3), status server berubah alarm **otomatis tanpa pull request**. Catatan: ini uji di **mesh kampus/lab**, bukan validasi di lapangan produksi RU — lih. `decisions.md` dec:34.

## Mesh LoRa (uji 8-CH, 16 Jul)
Deployment se-kampus ITB: GW ← Layer 1 (CH3/CH5/CH8) ← Layer 2 (CH1/CH4) ← Layer 3 (CH2). Route depth 1–3, status installed. Downlink (GW→CH→GLD 0xF020) tembus lewat mesh + fix firmware.

## Gate
| ID | Gate | Status |
|---|---|---|
| gate:jsa | TRA/JSA | Belum disusun → menahan eksekusi site survey fisik RU IV Cilacap |
| gate:cert-height | Sertifikasi ketinggian pemasangan | Percobaan di kilang baru setinggi orang; **belum tersertifikasi** utk pemasangan lebih tinggi (temuan 6 Agu) |
| gate:gas-extra | Requirement gas tambahan (Benzena/CO/H2S) | Belum direkonsiliasi dgn gate 6-kelas (dec:17/dec:30) — status verifikasi belum ada |

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

## Meeting mingguan 30 Jul 2026 — update lapangan, arsitektur & risiko baru
> Sumber: notulen mentah weekly meeting tim (belum ada file terpisah di `Sumber Dokumen/`).

**Jadwal (menggantikan tanggal 24 Jul — lihat `decisions.md` dec:22):**
- Kunjungan Cilacap **9–10 Agustus 2026** = survey + instalasi **digabung dalam satu kunjungan**. Berangkat Minggu 9 Agu, instalasi Senin 10 Agu. Jadwal tim wajib dikosongkan.

**Arsitektur diperjelas (bukan konflik — detail dari dec:14, lihat `decisions.md` dec:23–24):**
- **App + database penuh berjalan lokal** di site RU IV **dan** kantor pusat Jakarta (request Pak Pindoan, Pertamina, untuk monitoring terpusat). **Cloud hanya berperan sebagai gateway/relay ringan**, bukan sistem paralel penuh.
- **Wi-Fi ESP32** dikonfirmasi **hanya untuk config/serial lokal** (perintah enable/disable WiFi diperlukan). **LoRa tetap backbone telemetri utama, selalu aktif** — tidak ada perubahan arsitektur komunikasi data.
- ⚠️ **Hardware fix diperlukan:** antena Wi-Fi 2,4G masih di dalam casing — perlu dikeluarkan agar channel config berfungsi andal.
- Biaya cloud "hanya untuk GW" disebut **~USD 5** — satuan (per bulan? per device?) **belum jelas**, perlu konfirmasi sebelum dipakai di deliverable biaya.

**Risiko & gap baru:**
| Item | Catatan |
|---|---|
| Kondensasi/genangan air dalam casing | Perlu mekanisme pencegahan — opsi: lubang kecil sirkulasi, kipas berkala, pemanas. Belum dipilih. |
| Potensi data collision multi-sensor (LoRa) | Probabilitas kecil menurut tim, tapi **belum diuji** — perlu test eksplisit. |
| Push alarm | **Belum dicoba sama sekali** — perlu masuk rencana pengujian. |
| Protokol missed-report GLD portable | Kekhawatiran: GLD portable bisa melewatkan gas saat non-aktif (duty-cycle OFF). Perlu mekanisme/protokol: jika GLD tak lapor sesuai jadwal, cek kondisi (baterai, sensor, dll). **Perluasan** dari risiko "data alarm hilang" 24 Jul (retry/heartbeat, PIC Beni) — protokol spesifik ini belum didefinisikan. |
| Portable GLD versi baterai | Butuh **magnet** untuk mounting — belum disourcing. |
| Test chamber portable | Dimensi & berat **belum ditentukan** — target harus mudah dimobilisasi. Pertanyaan terbuka dari tim sendiri, belum ada jawaban. |
| Gas capability gate (dec:17, min 6 kelas) | Status: baru **3 dari 6 kelas tervalidasi** (Clean Air, LPG, CO2 — sesuai scope `model:cnn1d`). LPG sudah diuji semprot langsung, hasil OK. H₂, Metana, dan validasi CO₂/Clean Air lebih lanjut masih diperlukan. |
| ⚠️ **Akurasi model dipertanyakan ulang** (dibahas "hari Jumat") | Tim sendiri mengangkat kekhawatiran akurasi CNN 1D/TCN yang terlihat tinggi — **direkomendasikan cek ulang** (potensi data leakage/overfitting, terutama karena dataset lab relatif kecil). Perlu jadi action item verifikasi independen sebelum klaim akurasi dipakai lebih jauh ke client. |

**Catatan teknis chamber/sensor (belum tentu actionable, tapi relevan utk R&D & ML):**
- MQ perlu dipanaskan dulu (~30 menit) sampai stabil sebelum mulai siklus on-off duty-cycle.
- Heater MQ berfungsi menstabilkan permukaan sensor; referensi suhu **~200°C disebut dari ChatGPT** — **belum diverifikasi ke datasheet MQ resmi**, jangan dikutip sebagai fakta terverifikasi.
- Semprot O₂ langsung → tegangan sensor turun (negatif) — melengkapi temuan 16 Jul (O₂ vs CO₂ pada baseline).
- Ide R&D: jika duty-cycle terbukti memengaruhi temperatur kerja sensor, ini bisa jadi **fitur tambahan untuk model ML** (bukan hanya gangguan). Pendekatan alternatif: panaskan cepat, atau jaga panas sensor agar tak meluruh cepat.
- Sensor suhu tambahan **tidak bisa dipasang** — keterbatasan ruang dalam housing chamber.
- Saat kunjungan lapangan (9–10 Agu), perlu **catat suhu lapangan manual** untuk melihat pengaruh variasi duty-cycle vs temperatur optimum kerja sensor.
- Model ESP32-S3 dipangkas **~84%** menurut catatan verbal tim — **konsisten** dengan angka 83% di `Deteksi_Gas_CNN_Presentasi.pptx` (selisih kecil, wajar untuk catatan verbal vs angka presisi pptx).

**Prinsip kerja tambahan (lihat `decisions.md` dec:25–26):**
- Dokumentasi progres harus jadi **knowledge base tim internal**, bukan hanya untuk client.
- Parameter konfigurasi akan disederhanakan, tapi operator tetap perlu memahami sejumlah konfigurasi inti.

**Item administratif terbuka (bukan blocker teknis):**
- Tanya **Pak Tresnandi** soal sisa anggaran proyek (sudah didistribusikan) — belum ada jawaban di notulen.
- Kabel HDMI panjang tersedia di lab untuk sesi berikutnya (logistik minor).
- Disebutkan rencana proyek berikutnya pasca-GLD, kemungkinan "susi-sensor proposal" — **nama tidak jelas/kemungkinan salah transkrip**, perlu klarifikasi bila relevan untuk dicatat lebih lanjut.

## Meeting/diskusi teknis 6 Agustus 2026 — instalasi, mounting & requirement tambahan
> Sumber: diskusi tim (dibandingkan sistem Corrosion Monitoring Emerson di kilang) + requirement list Pertamina; belum ada file terpisah di `Sumber Dokumen/`.

**Mounting & instalasi (rujukan: sistem Corrosion Monitoring Emerson, protokol WirelessHART, sudah terpasang & teruji di kilang):**
- Mounting GLD/CH di kilang mengikuti pola existing — arahan **Raihan Fakhar (RU VII Kasim)**. Owner umumnya ingin tampilan alat **tidak besar/mencolok**.
- CH terlihat besar karena perlu: jangkauan LoRa lebih luas, transfer data lebih banyak, kapasitas menampung perluasan lain (bukan cuma GLD). Versi Kasim sebelumnya single-channel, sekarang **multi-channel** — dua alat berpotensi **di-combine**.
- **Bracket L + U-clamp**, ditempelkan ke tiang/struktur existing — **tidak perlu bikin pole baru**; bracket biasanya **sepaket** dgn device yang dipesan. CH besar diberi **dudukan L**, disambungkan ke bracket.
- **Hindari pengelasan & pengeboran** — instalasi harus mudah dilakukan (juga mencegah kondisi "produksi sudah banyak tapi sulit diinstal di lapangan").
- **CH == repeater**. Instalasi harus **aman dan terlihat aman** (persepsi awam) — sertifikasi penting krn area kritis kilang. Saat dicoba di kilang, instalasi baru **setinggi orang**, belum boleh lebih tinggi krn **belum tersertifikasi** (`gate:cert-height`).
- Referensi lapangan: ada installed device dgn **hanya 3 CH/repeater** menembak ke server, jangkauan luas — posisinya jadi rujukan penempatan krn sudah teruji.
- Diminimalkan jumlah CH/repeater sebisa mungkin. Percobaan di ITB: area seluas kampus **cukup 2 CH**.
- Vendor mekanik akan dilibatkan utk persiapan instalasi (baut, mur, kunci-kunci).
- Cilacap dinilai **jauh lebih besar & lebih strict** dibanding Kasim.

**Topologi jaringan (rujukan corrosion monitoring, GLD diminta mengikuti — lih. `decisions.md` dec:28):**
- Sistem corrosion monitoring bisa cari jalur terbaik & **langsung ke GW tanpa lewat CH** bila memungkinkan. **GW mengunci CH & sensor apapun** di bawahnya. Metode **discover node dgn mesh-tree sudah diterapkan** (di sistem corr-mon).
- **GLD diminta bisa mengikuti topologi ini & GLD sendiri diminta bisa berfungsi sebagai CH.**
- Kapasitas jaringan referensi: **< 30 sensor** per beban/kapasitas gateway.
- Kebutuhan berbeda: **corr-mon kirim data hanya 2×/hari** (jauh lebih sedikit dari GLD yang real-time/safety-critical). Chip corr-mon sudah pakai **stack siap pakai** (mudah diimplementasi) vs GLD yang **dibangun from scratch**.
- Perlu info/indikator kebutuhan tambahan GW & CH — koordinasi ke **Pak Maman**.
- Menarik dibandingkan kinerja network dgn sistem Emerson (WirelessHART) sbg benchmark.
- Rencana saat ini: **tiang GLD mengikuti tiang Emerson** yang sudah ada.

**Status produksi unit (per 6 Agu):**
| Item | Jumlah |
|---|---|
| CH besar | 9 |
| CH kecil | 7 |
| GLD (diminta) | 4 |

**Requirement tambahan dari Pertamina (14 poin, sebagian besar masih terbuka):**
1. Komunikasi antar-sensor: diinginkan sensor bisa "menitip" data ke sensor lain (relay antar-node) — **belum ada di desain saat ini**.
2. Deteksi gas tambahan **wajib**: **Benzena, CO, H2S** — lih. `decisions.md` dec:30, **belum direkonsiliasi** dgn `gate:gas-extra`/gate 6-kelas dec:17.
3. Chamber **tidak boleh dibawa masuk kilang** — sampel gas dibawa keluar oleh tim Pertamina (dec:32).
4. **Alarm dibedakan** per jenis gas: gas mudah terbakar = threshold ppm risiko kebakaran; gas toksik (CO, H2S) = alarm langsung (dec:29).
5. Pemilihan bracket harus disesuaikan utk pemasangan CH **dan** GLD sekaligus.
6. Perlu **skenario instalasi lengkap dgn ukuran-ukuran konkret** — **belum dibuat**.
7. **Hindari pengelasan & pengeboran.**
8. ⚠️ Pertanyaan terbuka: gas hasil sedotan pompa chamber keluar ke mana? Apakah ke udara bebas (risiko paparan user)? — **belum dijawab**.
9. Aplikasi perlu kolom **"Area"** pada data equipment/sensor (dec:33).
10. Alarm diatur dari nilai-nilai **threshold** per jenis gas.
11. **Hindari material PVC** (dec:31).
12. CH besar → dudukan L → sambung ke bracket.
13. ⚠️ Pertanyaan terbuka: gateway bisa pakai **kabel**? Bisa dipasang **indoor** dgn hanya antena di luar? — **belum dijawab**.

**Follow-up WhatsApp (6–8 Agustus 2026):**
- **6 Agu 12:00** (Farhan Budiman): contoh desain repeater & bracket Emerson utk memudahkan mounting pada struktur existing, cc **Raihan Fakhar (RU VII Kasim)**.
- **6 Agu 12:12 & 12:17** (Farhan Budiman): contoh app **"Gateway Manager"** — jumlah device terdaftar/terhubung per GW, kapasitas GW, device tak terhubung, & visualisasi jaringan → **requirement fitur baru** utk dashboard/Operator Hub, belum ada di scope sw saat ini.
- **8 Agu 09:16** (Farhan Budiman): pertanyaan Pertamina soal kebutuhan **solar panel** bila GLD pakai baterai+solar — ukuran besar tidak masalah bagi mereka (contoh: seukuran panel lampu PJU atau lebih).
- **8 Agu 12:49** (Beny Agustirandi, ITB Fisika): **belum ada perhitungan Wp** solar panel. Diskusi sebelumnya: solar panel dinilai **menyulitkan instalasi & sempat tidak diizinkan Pertamina**; akan dihitung kebutuhan Wp bila ternyata tidak masalah.

**Demo persiapan sebelum kunjungan Cilacap (6–8 Agu, mesh kampus):**
- Tiang **GW, CH1, CH2, CH3** disiapkan; **semua CH sudah masuk/terhubung ke GW**.
- Uji star GLD di **CH1 & CH2**: data masuk saat direquest (pull) — OK.
- Uji alarm real-time: GLD disemprot LPG → status server jadi **alarm otomatis tanpa pull request** — **push alarm berhasil** (lih. `decisions.md` dec:34, resolved di atas).
- Urutan demo: **aktifkan server → pasang GW → pasang CH → pasang GLD 24V.**
