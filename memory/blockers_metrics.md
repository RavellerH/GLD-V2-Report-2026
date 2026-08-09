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
| gate:cert-height | Sertifikasi ketinggian pemasangan | Percobaan di kilang baru setinggi orang; **belum tersertifikasi** utk instalasi permanen (rapat resmi 6 Agu) |
| gate:gas-extra | Requirement gas tambahan (Benzena/CO/H2S) | Belum direkonsiliasi dgn gate 6-kelas (dec:17/dec:30) — status verifikasi belum ada. Model AI terbaru (**CNN Dual-Branch**, 9 Agu) masih 3-kelas LPG/CO2/Udara Bersih, **tidak menutup gate ini** |
| gate:capacity | Kapasitas GW/CH vs jumlah sensor | **Belum ada angka resmi** — action item terbuka (Tim Komunikasi ITB), lih. dec:28 |

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
- **CNN Dual-Branch (9 Agu, penerus CNN 1D):** 1.870 pembacaan unik (1.496 train/374 test); akurasi **99,73% PC / 99,20% on-chip int8** (9,14 KB); 1.347 parameter; masih 3-kelas LPG/CO2/Udara Bersih (bukan CO/H2S). Detail lengkap → `entities.md` § Model AI.

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

## Rapat resmi 6 Agustus 2026 — instalasi, mounting & requirement tambahan
> Sumber: `Sumber Dokumen/Notulensi_Rapat_5Agustus2026_GLD.pdf` (Labtek XV ITB; Tim ITB + PT Pertamina + PT LAPI Ganesha Utama), diverifikasi 9 Agu terhadap catatan informal sebelumnya.
>
> ⚠️ **Catatan tanggal:** badan teks notulensi resmi tertulis "Tanggal: 5 Agustus 2026" — namun ini **typo pada dokumen**; tanggal rapat yang benar dikonfirmasi **6 Agustus 2026 (Kamis)**, sesuai nama file sumber (`NOTULENSI_RAPAT_060826` = 06-08-26) dan konfirmasi user. Beberapa detail konten di bawah tetap direvisi (ditandai ⚠️) karena versi notulensi resmi lebih presisi/berbeda dari catatan informal awal — itu terlepas dari isu tanggal.

**Mounting & instalasi (dibandingkan sistem Corrosion Monitoring Emerson, konsep WirelessHART, sudah terpasang di kilang):**
- Mounting GLD/CH mengikuti standar mounting existing di kilang — **tidak memerlukan desain struktur baru**.
- CH besar karena: jangkauan LoRa lebih luas, kapasitas komunikasi lebih besar, mendukung pengembangan sistem masa depan. Sistem sekarang **multi-channel** (vs implementasi Kasim sebelumnya yang single-channel).
- **Bracket tipe L / U-clamp** dipasang pada struktur existing, **tanpa pengeboran maupun pengelasan**. Pemilihan bracket disesuaikan dgn kebutuhan Gateway, CH, **maupun** sensor GLD.
- Vendor mekanik dilibatkan **sejak awal** proses desain & instalasi.
- Tim diminta menyusun **skenario instalasi lengkap** (dimensi pemasangan, kebutuhan bracket, baut, mur, komponen pendukung) — **belum dibuat**.
- **Material PVC dihindari** — dinilai kurang sesuai utk lingkungan kilang.
- Jumlah CH diupayakan **seminimal mungkin** utk kurangi kompleksitas instalasi; pengujian di ITB: **2 CH** sudah cukup mencakup area pengujian.
- **3 repeater** yang sudah terpasang di kilang jadi referensi penempatan (terbukti memberi cakupan baik).
- Instalasi harus perhatikan keselamatan **teknis maupun visual** (cegah persepsi negatif operator/personel lapangan). Krn lokasi di area kilang, perangkat harus penuhi **persyaratan sertifikasi**. Tahap uji coba: pemasangan **dibatasi setinggi manusia** — perangkat belum bersertifikasi utk **instalasi permanen** (`gate:cert-height`).

**Topologi jaringan & evaluasi teknologi:**
- **Sistem GLD diharapkan dapat mengadopsi topologi tsb sehingga CH juga dapat berfungsi sebagai repeater** (lih. `decisions.md` dec:28). ⚠️ **Catatan revisi:** notulensi resmi TIDAK menyatakan sistem corrosion monitoring "sudah terbukti bypass-ke-GW" atau "mesh-tree sudah diterapkan" sbg fakta established seperti sempat dicatat dari sumber informal — itu simplifikasi berlebih. Yang resmi: **tim diminta mengevaluasi** kapasitas GW/CH thd jumlah sensor yg bisa dilayani & sediakan indikator bila perlu tambah perangkat (action item, PIC Tim Komunikasi ITB) — **BELUM ada angka pasti** (bukan "<30 sensor" seperti sempat dicatat).
- Kebutuhan berbeda: **GLD berorientasi safety**, perlu komunikasi lebih intensif; **corrosion monitoring** menekankan keandalan alat, kirim data **~2×/hari** (jauh lebih jarang).
- Pemilihan teknologi komunikasi ke depan perlu pertimbangkan **chipset** yg dipakai shg implementasi tak perlu dibangun sepenuhnya dari awal.
- **Menarik dibandingkan** dgn performa jaringan sistem corrosion monitoring komersial (mis. Emerson), termasuk kemungkinan pakai konsep **WirelessHART** — action item studi banding (PIC Tim Komunikasi ITB), **belum dilakukan**.

**Status produksi unit (per 6 Agu):**
| Item | Jumlah |
|---|---|
| CH besar | 9 |
| CH kecil | 7 |
| GLD (sesuai permintaan saat ini) | 4 |

**Requirement resmi pengembangan sistem GLD (Bab 4 notulensi):**
1. Sistem dirancang mampu deteksi **Benzene, Carbon Monoxide (CO), Hydrogen Sulfide (H2S)** — lih. dec:30, **belum direkonsiliasi** dgn `gate:gas-extra`/gate 6-kelas dec:17.
2. Sampel gas **tidak diambil langsung di area kilang** — disiapkan & dibawa tim Pertamina ke lokasi pengujian (dec:32).
3. ⚠️ **Sistem harus menampilkan nilai konsentrasi gas (ppm) secara real-time** — requirement eksplisit yang sempat terlewat dari catatan informal awal.
4. **Alarm dikonfigurasi berdasarkan threshold**: gas mudah terbakar → alarm setelah lewat batas bahaya kebakaran; gas toksik (CO, H2S) → alarm **segera** begitu lewat ambang batas keselamatan (dec:29).
5. Aplikasi perlu tampilkan info lokasi perangkat: kolom **Area DAN identitas Equipment** (dec:33) — ⚠️ bukan cuma "Area" seperti sempat dicatat.
6. **Jalur pembuangan gas** pasca-sampling perlu dievaluasi agar tak timbulkan paparan ke pengguna/lingkungan — action item (PIC Tim Instrumentasi ITB), **belum dijawab**.

**8 Tindak Lanjut resmi (dengan PIC) — menggantikan PIC generik yang sempat dipakai:**
| # | Tindak Lanjut | PIC |
|---|---|---|
| 1 | Menyusun desain mounting & bracket sesuai standar kilang | Tim Mekanik ITB |
| 2 | Menyusun skenario instalasi lengkap + dimensi pemasangan | Tim Mekanik & Vendor Mekanik |
| 3 | Mengevaluasi kapasitas Gateway & Cluster Head | Tim Komunikasi ITB |
| 4 | Mengembangkan fitur alarm berbasis threshold gas | Tim AI ITB |
| 5 | Menambahkan info Area & Equipment pada dashboard | Tim UI ITB |
| 6 | Mengkaji sistem pembuangan gas pasca-sampling | Tim Instrumentasi ITB |
| 7 | Studi perbandingan topologi dgn sistem Emerson/WirelessHART | Tim Komunikasi ITB |
| 8 | Menyusun rencana sertifikasi perangkat utk kilang | Tim ITB bersama Pertamina |

**Follow-up WhatsApp (6–8 Agustus 2026, setelah rapat 6 Agu):**
- **6 Agu 12:00** (Farhan Budiman): contoh desain repeater & bracket Emerson utk memudahkan mounting pada struktur existing, cc **Raihan Fakhar (RU VII Kasim)** — ⚠️ nama ini dari WA, **tidak disebut** di notulensi resmi (peserta ditulis generik "Tim ITB, PT Pertamina, PT LAPI Ganesha Utama").
- **6 Agu 12:12 & 12:17** (Farhan Budiman): contoh app **"Gateway Manager"** — jumlah device terdaftar/terhubung per GW, kapasitas GW, device tak terhubung, & visualisasi jaringan → **requirement fitur baru** utk dashboard/Operator Hub, belum ada di scope sw saat ini.
- **8 Agu 09:16** (Farhan Budiman): pertanyaan Pertamina soal kebutuhan **solar panel** bila GLD pakai baterai+solar — ukuran besar tidak masalah bagi mereka (contoh: seukuran panel lampu PJU atau lebih).
- **8 Agu 12:49** (Beny Agustirandi, ITB Fisika): **belum ada perhitungan Wp** solar panel. Diskusi sebelumnya: solar panel dinilai **menyulitkan instalasi & sempat tidak diizinkan Pertamina**; akan dihitung kebutuhan Wp bila ternyata tidak masalah.

**Demo persiapan sebelum kunjungan Cilacap (6–8 Agu, mesh kampus):**
- Tiang **GW, CH1, CH2, CH3** disiapkan; **semua CH sudah masuk/terhubung ke GW**.
- Uji star GLD di **CH1 & CH2**: data masuk saat direquest (pull) — OK.
- Uji alarm real-time: GLD disemprot LPG → status server jadi **alarm otomatis tanpa pull request** — **push alarm berhasil** (lih. `decisions.md` dec:34, resolved di atas).
- Urutan demo: **aktifkan server → pasang GW → pasang CH → pasang GLD 24V.**
