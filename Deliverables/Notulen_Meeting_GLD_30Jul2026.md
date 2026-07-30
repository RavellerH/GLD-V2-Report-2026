# NOTULEN MEETING — GAS LEAK DETECTION (GLD) TAHAP 2

**Tanggal:** 30 Juli 2026
**Waktu:** *(tidak tercantum di catatan mentah)*
**Project:** Gas Leak Detection (GLD) — Weekly Progress & Technical Discussion
**Peserta:** Tim LGU / Lab IoT ITB (weekly internal). Disebutkan permintaan dari **Pak Pindoan** (Pertamina) dan pertanyaan anggaran untuk **Pak Tresnandi** — daftar peserta lengkap tidak tercantum di catatan mentah yang diberikan.

---

## Agenda (disimpulkan dari pembahasan)
1. Arsitektur aplikasi (lokal vs cloud) & monitoring terpusat
2. Optimasi daya & duty-cycle GLD portable
3. Peran Wi-Fi vs LoRa dalam komunikasi data
4. Persiapan kunjungan lapangan RU IV Cilacap
5. Uji gas chamber & karakterisasi sensor MQ
6. Status & kekhawatiran model AI
7. Isu casing (kondensasi, antena)
8. Dokumentasi & simplifikasi konfigurasi
9. Anggaran & logistik

---

## Ringkasan Pembahasan

### 1. Arsitektur Aplikasi & Monitoring
- Aplikasi lokal + database dibuat penuh; **cloud hanya berperan sebagai gateway**.
- Instalasi di komputer site **dan** kantor Jakarta agar pusat bisa memonitor (**request Pak Pindoan**).
- Biaya bila hanya untuk GW: **USD 5** — satuan (per bulan/per device?) belum dikonfirmasi di catatan.

### 2. Daya & GLD Portable
- Target konsumsi **<100 mA** dengan on-off cepat — butuh **modifikasi hardware**.
- **Push alarm belum dicoba.**
- Untuk versi portable/baterai: perlu **magnet** untuk mounting — belum disourcing.
- Kekhawatiran: GLD portable berpotensi melewatkan gas saat tidak aktif (duty-cycle off). Perlu protokol: bila GLD tidak melapor rutin sesuai setting, cek kondisi (baterai, sensor, dll) — protokol detail belum didefinisikan.

### 3. Komunikasi: Wi-Fi vs LoRa
- Fasilitas Wi-Fi ESP dapat digunakan untuk serial wireless; perlu perintah untuk mengaktifkan/menonaktifkan Wi-Fi.
- **LoRa tetap digunakan selalu aktif** sebagai jalur komunikasi data utama.
- Problem: antena Wi-Fi 2,4G masih di dalam casing — **perlu dikeluarkan**.
- *Catatan interpretasi (dikonfirmasi 30 Jul): Wi-Fi berperan sebagai kanal konfigurasi/serial lokal, bukan pengganti LoRa sebagai jalur telemetri utama.*

### 4. Persiapan Kunjungan RU IV Cilacap
- Kunjungan minggu ke-2 Agustus: **Senin, 10 Agustus 2026** (berangkat 1 hari sebelumnya, **9 Agustus**).
- Tanggal 10 akan dipasang (instalasi) di Cilacap — **jadwal tim agar dikosongkan**.
- *Catatan: kunjungan ini menggabungkan survey + instalasi dalam satu kunjungan, menggantikan rencana sebelumnya (survey akhir Juli → instalasi September 2026).*

### 5. Gas Chamber & Karakterisasi Sensor MQ
- Gas chamber portable: mudah dibawa ke site, bisa langsung mencoba gas lain yang sulit diperoleh untuk percobaan di lab.
- Dimensi & berat test chamber **belum ditentukan** — sebaiknya portable/mudah dimobilisasi.
- MQ perlu dipanaskan (ada pemanas internal) hingga stabil sebelum mulai on-off. Info suhu **~200°C** (sumber: ChatGPT — **belum diverifikasi ke datasheet resmi**).
- Panaskan dulu **30 menit**, baru coba pertahankan dengan on-off.
- Saat disemprot oksigen, tegangan sensor **menurun (negatif)**.
- Alternatif: tambahan pengujian semprot oksigen; pendekatan memanaskan cepat atau menjaga panas sensor agar tidak meluruh cepat.
- Bila duty cycle memengaruhi temperatur kerja sensor, ini berpotensi jadi **data tambahan untuk ML**.
- Sensor temperatur tambahan **tidak memungkinkan** dipasang karena keterbatasan ruang.
- Saat di lapangan (kunjungan Agustus), perlu dicatat **temperatur lapangan** untuk melihat pengaruh variasi duty-cycle vs bacaan optimum pada temperatur kerja sensor.
- LoRa sudah dicoba (pengujian sebelumnya).

### 6. Model AI — Status & Kekhawatiran
- Saat ini baru **3 jenis gas**: Clean Air, LPG, CO2.
- Sudah dicoba semprot LPG langsung — hasil **OK**.
- Model yang di-deploy ke ESP32 **dipangkas 84%**, akurasi masih terjaga.
- Data sensitivitas sensor MQ terhadap gas telah ditambahkan ke dokumentasi.
- ⚠️ **Saat Jumat, muncul kekhawatiran** karena akurasi model dinilai tinggi — **disarankan cek ulang** (potensi overfitting/data leakage).

### 7. Casing & Perlindungan Hardware
- Potensi **genangan air dalam casing** akibat kondensasi.
- Perlu mekanisme pencegahan: lubang kecil sirkulasi, kipas yang dinyalakan sesekali, pemanas, dll — **opsi belum ditentukan**.

### 8. Reliabilitas Sistem
- Perlu kepastian potensi **data collision** karena multi-sensor (LoRa) — probabilitas kecil menurut tim, tapi **tetap perlu dicoba/diuji**.

### 9. Dokumentasi & Konfigurasi
- Progres harus didokumentasikan dengan baik sehingga menjadi **knowledge base tim**, bukan hanya untuk keperluan client.
- Terlalu banyak parameter yang perlu di-setting — **akan disederhanakan**, namun operator tetap perlu memahami konfigurasi inti yang tersisa.

### 10. Anggaran & Logistik
- Perlu tanyakan ke **Pak Tresnandi** soal sisa anggaran (sudah didistribusikan, seharusnya ada sisa).
- Di lab tersedia kabel HDMI panjang untuk sesi berikutnya.
- Harapan agar GLD segera selesai supaya tim dapat bergerak ke proyek lain (disebutkan contoh: "**susi-sensor proposal**" — nama belum jelas/kemungkinan salah transkrip, perlu klarifikasi bila relevan).

---

## Action Items
*(disarikan dari catatan mentah — PIC & deadline belum dicantumkan di sumber, perlu dilengkapi)*

| # | Task | Catatan |
|---|---|---|
| 1 | Modifikasi hardware untuk reduksi konsumsi <100 mA dengan on-off cepat | |
| 2 | Uji coba push alarm | Belum pernah diuji |
| 3 | Buat perintah enable/disable Wi-Fi (mode config/serial lokal) | |
| 4 | Keluarkan antena Wi-Fi 2,4G dari dalam casing | |
| 5 | Cari magnet untuk mounting GLD portable versi baterai | |
| 6 | Uji potensi data collision multi-sensor (LoRa) | Probabilitas kecil, tetap perlu diuji |
| 7 | Definisikan protokol missed-report untuk GLD portable (cek baterai/sensor bila tidak lapor rutin) | |
| 8 | Sederhanakan parameter konfigurasi (tanpa menghilangkan kontrol inti operator) | |
| 9 | Tentukan dimensi & berat test chamber portable | |
| 10 | Tanyakan sisa anggaran ke Pak Tresnandi | |
| 11 | Verifikasi ulang akurasi model (CNN 1D/TCN) — cek potensi data leakage/overfitting | Kekhawatiran diangkat "hari Jumat" |
| 12 | Rancang mekanisme anti-kondensasi casing (lubang sirkulasi/kipas/pemanas) | Opsi belum difinalisasi |
| 13 | Catat temperatur lapangan saat kunjungan Cilacap untuk analisis duty-cycle vs temperatur sensor | Saat kunjungan 9–10 Agustus |
| 14 | Instalasi aplikasi lokal + database di site RU IV Cilacap dan kantor Jakarta | Request Pak Pindoan |
| 15 | Konfirmasi satuan biaya cloud gateway-only (USD 5) | Per bulan/per device belum jelas |

---

## Keputusan Meeting
- Arsitektur: **app + database penuh berjalan lokal** (site RU IV Cilacap **dan** kantor Jakarta); **cloud hanya berperan sebagai gateway/relay**.
- **Wi-Fi** dipakai untuk config/serial lokal; **LoRa tetap jadi jalur komunikasi data utama**, selalu aktif.
- Kunjungan RU IV Cilacap **dimajukan & digabung**: survey + instalasi pada **10 Agustus 2026** (berangkat 9 Agustus) — **menggantikan** rencana sebelumnya (survey akhir Juli → instalasi September).
- Dokumentasi progres diarahkan juga menjadi **knowledge base internal tim**.
- Parameter konfigurasi akan **disederhanakan**, namun tetap ada konfigurasi inti yang perlu dipahami operator.

## Risiko & Mitigasi (baru, dari meeting ini)
| Risiko | Mitigasi |
|---|---|
| Genangan air dalam casing akibat kondensasi | Lubang sirkulasi kecil / kipas berkala / pemanas (opsi, belum final) |
| Data collision multi-sensor LoRa (probabilitas kecil) | Perlu pengujian eksplisit |
| GLD portable melewatkan gas saat non-aktif | Protokol missed-report: cek baterai/sensor bila tak lapor rutin |
| Akurasi model dinilai tinggi/mencurigakan | Verifikasi ulang independen (cek data leakage/overfitting) |
| Antena Wi-Fi 2,4G di dalam casing | Keluarkan antena agar channel config andal |

## Next Meeting
- **Kunjungan lapangan RU IV Cilacap: Senin, 10 Agustus 2026** (berangkat 9 Agustus).

## Catatan Penting
- Beberapa item dalam catatan mentah bersifat pertanyaan terbuka tanpa jawaban tercatat (dimensi chamber, sisa anggaran, satuan biaya cloud) — perlu tindak lanjut.
- Nama "susi-sensor proposal" kemungkinan salah transkrip/belum jelas — perlu klarifikasi bila proyek ini relevan untuk dicatat lebih lanjut.
- Daftar peserta lengkap tidak tercantum di catatan mentah yang diberikan; dokumen ini disusun murni dari poin-poin notula tanpa rekayasa informasi yang tidak ada.

---
*Disusun oleh Claude dari catatan mentah weekly meeting tim, 30 Juli 2026. Lihat juga `memory/blockers_metrics.md` § Meeting mingguan 30 Jul dan `memory/decisions.md` dec:22–26 untuk rekonsiliasi dengan status proyek sebelumnya.*
