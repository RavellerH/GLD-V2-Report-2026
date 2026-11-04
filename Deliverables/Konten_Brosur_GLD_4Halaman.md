# Konten Brosur GLD — A4, 4 Halaman

**Untuk:** brosur/katalog produk umum (pengunjung pameran, manajemen, mitra, direksi)
**Format:** A4 portrait, 4 halaman, kertas katalog (art paper)
**Status:** konten final untuk di-layout di tool desain lain
**Disusun:** 4 November 2026

---

## Panduan umum

**Hierarki merek**
1. **Pertamina Patra Niaga** paling menonjol (logo besar di sampul dan kepala halaman).
2. **GLD — Multi-Modality Gas Leak Detector** sebagai nama produk (judul utama).
3. **Korporasi Kinarya ITB** dan **LAPI Ganesha Utama** hanya logo kecil dengan teks "Dikembangkan bersama", di sampul bawah dan kaki halaman.

**Warna:** biru tua Pertamina (#12357A), biru (#2B5FCB), aksen merah (#E3242B) dan hijau (#8DC63F), latar putih.

**Gaya:** teknologi industri, bersih, banyak ruang putih, foto produk asli.

**File pendukung di repo**
- Logo: `Sumber Dokumen/Logo/` (Pertamina Patra Niaga, Kinarya ITB, LGU)
- Foto unit GLD: `scripts/assets/cert_doc_photos/3._Motherboard_ModulSensor_PenutupMesh_Casing_Antena_ModulAlarm.jpg`
- Foto mesh sensor: `scripts/assets/cert_doc_photos/PenutupMesh_Casing.jpg`
- Foto chamber uji gas: `scripts/assets/chamber_photos/chamber_gld_terpasang.jpeg`
- Foto Cluster Head + panel surya: `scripts/assets/ch_mount_photos/ch_bracket_solar_detail.jpg`
- Tangkapan layar dashboard: `Deliverables/Video_Produk_GLD_Remotion/public/images/dashboard.png`

---

## HALAMAN 1 — Sampul

**Logo atas:** Pertamina Patra Niaga (besar)

**Label kecil:** Multi-Modality · AI on the Edge · LoRa Mesh

**Judul:** GLD

**Sub-judul:** Multi-Modality Gas Leak Detector

**Tagline (pilih satu):**
- "Mengenali jenis gas, bukan sekadar mendeteksinya."
- "Delapan sensor. Satu kecerdasan. Deteksi kebocoran gas yang lebih cerdas."
- "Deteksi kebocoran gas berbasis AI untuk kilang yang lebih aman."

**Paragraf pembuka:**
GLD adalah sistem deteksi kebocoran gas yang menggabungkan delapan sensor gas dalam satu unit. Kecerdasan buatan di dalam perangkat mengenali jenis gas dari pola respons kedelapan sensor itu. Hasilnya dikirim secara nirkabel melalui jaringan LoRa Mesh ke dashboard pemantauan, secara real-time.

**4 angka kunci (kotak/ikon):**
| Angka | Keterangan |
|---|---|
| **8** | sensor gas dalam satu unit |
| **< 166 ms** | waktu inferensi AI langsung di perangkat |
| **99,31%** | akurasi model pada data validasi laboratorium |
| **LoRa Mesh** | komunikasi nirkabel 920–923 MHz, terenkripsi AES-128 |

**Kotak pesan:**
**Pelengkap sistem deteksi gas yang sudah ada.** GLD menambah informasi jenis gas sebagai lapisan pemantauan tambahan. Sistem berjalan mandiri dan tidak mengubah alarm, logic trip, maupun interlock sistem Fire & Gas dan DCS yang sudah terpasang.

**Kaki halaman:** "Dikembangkan bersama" + logo Kinarya ITB + logo LGU (kecil)

**Arahan visual:** foto unit GLD (housing biru, mesh stainless, beacon merah, antena) sebagai gambar utama, di atas latar biru tua bergradasi dengan siluet kilang samar dan garis jaringan bercahaya.

---

## HALAMAN 2 — Mengapa GLD & Cara Kerjanya

### Judul: Mengapa GLD

**Paragraf:**
Kebocoran gas mudah terbakar dan beracun adalah salah satu risiko terbesar di fasilitas migas. Detektor konvensional umumnya memakai satu jenis sensor untuk satu jenis gas. Hasilnya berupa nilai konsentrasi, tetapi tidak menunjukkan gas apa yang sedang bocor. GLD membaca pola respons delapan sensor sekaligus, lalu model kecerdasan buatan menentukan jenis gasnya. Dengan begitu, petugas mendapat informasi yang lebih lengkap untuk mengambil tindakan.

**Tabel perbandingan:**
| Aspek | Detektor konvensional | GLD Multi-Modality |
|---|---|---|
| Sensor | Satu jenis sensor per detektor | Delapan sensor dalam satu unit |
| Keluaran | Nilai konsentrasi gas | Label jenis gas + tingkat keyakinan (confidence) |
| Pengolahan data | Di panel kontrol | AI langsung di perangkat (edge computing) |
| Pengiriman data | Kabel ke panel | Nirkabel LoRa Mesh, cukup kabel daya |
| Peran | Lapisan proteksi utama | Lapisan pemantauan tambahan |

### Judul: Cara Kerja

**5 langkah (ikon berurutan):**
1. **Sampling udara** — kipas kecil menarik udara masuk melalui filter mesh stainless steel.
2. **Pembacaan 8 sensor** — konverter analog-digital 24-bit membaca kedelapan sensor setiap 500 milidetik.
3. **Pengolahan sinyal** — kalibrasi otomatis dan perataan data menghilangkan gangguan pembacaan.
4. **Inferensi AI** — model di dalam perangkat mengenali jenis gas dan menghitung tingkat keyakinannya.
5. **Pelaporan** — hasil dikirim terenkripsi ke server; kondisi normal dilaporkan berkala, alarm dikirim segera.

### Judul kecil: Arsitektur Sistem

**Diagram alir (kiri ke kanan):**
**GLD** (node sensor di area proses) → *LoRa STAR 920 MHz* → **Cluster Head** (penghubung nirkabel bertenaga surya) → *LoRa MESH 921 MHz, multi-hop* → **Gateway** (di ruang kontrol) → *jaringan lokal* → **Server & Dashboard** (ruang kontrol dan intranet kantor)

**Keterangan di bawah diagram:**
Jaringan mesh memungkinkan data melompat dari satu Cluster Head ke Cluster Head lain hingga mencapai Gateway, sehingga jangkauan bisa diperluas ke seluruh area kilang. Bila satu Cluster Head terganggu, data otomatis mencari jalur lain.

### Judul kecil: Delapan Sensor, Satu Sidik Jari Gas

| Sensor | Sensitif terhadap |
|---|---|
| MQ-8 | Hidrogen (H₂) |
| MQ-135 | Kualitas udara (NH₃, benzena, asap) |
| MQ-3 | Alkohol / etanol |
| MQ-5 | LPG, gas alam |
| MQ-4 | Metana (CH₄) |
| MQ-7 | Karbon monoksida (CO) |
| MQ-6 | LPG, butana, propana |
| MQ-2 | Gas mudah terbakar umum |

*Catatan kecil:* Sensitivitas umum menurut pabrikan sensor. Jenis gas yang dikenali ditentukan oleh model AI yang dilatih untuk lokasi pemasangan.

**Arahan visual:** infografis alur 5 langkah dengan ikon; diagram arsitektur sederhana dengan ikon perangkat; grid 8 sensor sebagai "sidik jari" berwarna.

---

## HALAMAN 3 — Komponen & Spesifikasi

### Judul: Komponen Sistem

**1. Gas Leak Detector (GLD) — node sensor**
Perangkat lapangan yang memuat delapan sensor gas, prosesor AI, radio LoRa, dan keluaran alarm.

| Parameter | Spesifikasi |
|---|---|
| Sensor gas | 8 kanal seri MQ (Winsen) |
| Sensor lingkungan | Suhu & kelembapan (Sensirion SHT40) |
| Akuisisi data | ADC 24-bit, pemindaian 8 kanal setiap 500 ms |
| Prosesor | ESP32-S3: kontrol, komunikasi & inferensi AI lokal |
| Keluaran AI | Label jenis gas + confidence, waktu inferensi < 166 ms |
| Kelas model saat ini | Udara bersih, LPG, hidrogen (H₂) |
| Komunikasi | LoRa 920–923 MHz, enkripsi AES-128-GCM, anti-replay |
| Antarmuka lokal | RS-485 Modbus RTU (baca saja) |
| Catu daya | 24 VDC, konsumsi maks. ±8 W |
| Keluaran alarm | Keluaran 24 V untuk buzzer/lampu eksternal |
| Housing | Aluminium die-cast dengan filter mesh stainless steel |
| Entry kabel | Cable gland M20 × 1,5 |
| Pemasangan | Pelat 250 × 250 mm dengan 2 U-bolt pada tiang pipa 2 inci |

**2. Cluster Head — penghubung nirkabel**
| Parameter | Spesifikasi |
|---|---|
| Fungsi | Mengumpulkan data dari GLD dan meneruskannya lewat jaringan mesh |
| Radio | 2 modul LoRa (jalur STAR & jalur MESH) |
| Daya | 2 panel surya + baterai, tanpa kabel listrik |
| Keandalan | Pemilihan jalur otomatis dan failover |

**3. Gateway — pintu ke jaringan lokal**
| Parameter | Spesifikasi |
|---|---|
| Fungsi | Akar jaringan mesh, meneruskan data ke server |
| Antena | Omni 8 dBi di atap gedung |
| Koneksi | Wi-Fi lokal ke router jaringan GLD |
| Daya | 220 VAC melalui adaptor, didukung UPS |

**4. Server & Dashboard**
| Parameter | Spesifikasi |
|---|---|
| Perangkat | PC lokal (4 core, 8 GB RAM, SSD 256 GB, 2 port LAN) |
| Fungsi | Validasi data, penyimpanan riwayat, alarm, status perangkat |
| Akses | Dashboard web dari ruang kontrol dan intranet kantor |
| Keamanan | Jaringan terpisah tanpa internet; tidak ada routing antar jaringan |

### Kotak: Keamanan & Keandalan
- Data dienkripsi dan diautentikasi AES-128-GCM, dengan proteksi anti-replay.
- Jaringan GLD terpisah dan tidak terhubung ke internet.
- Jalur alternatif otomatis bila salah satu Cluster Head tidak berfungsi.
- Gateway, router, dan server didukung UPS agar data dan alarm tetap tercatat saat listrik padam.
- Desain modular: daya, komunikasi, pengolahan data, dan sensor terpisah, sehingga perawatan bisa per bagian.

**Arahan visual:** foto unit GLD besar + foto close-up mesh sensor; foto Cluster Head dengan panel surya; ikon untuk Gateway dan server.

---

## HALAMAN 4 — Pengujian, Sertifikasi & Pengembangan

### Judul: Teruji di Laboratorium, Siap Diuji di Lapangan

**Hasil pengujian laboratorium:**
- Rantai lengkap GLD – Cluster Head – Gateway – Server berjalan end-to-end.
- Akurasi model 99,31% pada data validasi laboratorium.
- Jaringan mesh diuji dengan 8 Cluster Head bertingkat hingga 3 lompatan (hop).
- Alarm terkirim otomatis ke server tanpa perlu diminta (push alarm).
- Factory Acceptance Test laboratorium: 7 dari 7 butir uji lulus.
- Komunikasi tetap stabil saat diuji dengan gangguan sinyal pada kanal yang sama (uji awal).
- Pengukuran awal emisi elektromagnetik (pre-scan EMC EN 55032) telah dilakukan.

### Judul kecil: Sertifikasi (dalam proses)
| Bidang | Target |
|---|---|
| Area berbahaya | ATEX / IECEx — usulan II 2G Ex db IIC T4 Gb |
| Perlindungan debu & air | IP66 / IP67 |
| Kompatibilitas elektromagnetik | EMC EN 61000-6-2 / -4 |
| Perangkat radio | Sesuai ketentuan SDPPI (pita 920–923 MHz) |

### Judul kecil: AI yang Belajar dari Lokasinya
**Paragraf:**
Setiap kilang memiliki jenis gas yang perlu diawasi. Karena itu, GLD dilengkapi metode pelatihan model di lokasi menggunakan chamber uji gas portabel.

**Alur 4 langkah:**
1. Chamber uji gas dibawa ke lokasi kilang.
2. Dataset gas setempat diambil dengan unit GLD di dalam chamber.
3. Model AI dilatih dengan data tersebut.
4. Model baru dipasang ke firmware GLD.

**Paragraf penutup:**
Gas target pengembangan berikutnya, seperti H₂S, hidrokarbon berat, metana, CO, dan benzena, ditambahkan melalui pengumpulan dataset dan pelatihan lanjutan sesuai kebutuhan tiap lokasi.

### Judul kecil: Rencana Penerapan di 6 Refinery Unit
| Unit | GLD | Cluster Head | Gateway |
|---|---|---|---|
| RU II | 10 | 3 | 1 |
| RU III | 4 | 3 | 1 |
| RU IV | 3 | 2 | 1 |
| RU V | 2 | 1 | 1 |
| RU VI | 4 | 2 | 2 |
| RU VII | 5 | 11 | 1 |
| **Total** | **28** | **22** | **7** |

**Kaki halaman:** "Dikembangkan bersama" + logo Kinarya ITB + logo LGU (kecil)

**Arahan visual:** foto chamber uji gas (kotak akrilik bening, unit GLD di pelat aluminium, kipas di lantai chamber); tangkapan layar dashboard; infografis 4 langkah pelatihan; tabel rollout dengan peta Indonesia dan titik 6 RU (opsional).

---

## Hal yang sengaja TIDAK dicantumkan (dan alasannya)

| Jangan tulis | Alasan |
|---|---|
| "Bersertifikat ATEX" / "explosion-proof certified" | Sertifikasi masih dalam proses. Tulis "dalam proses sertifikasi". |
| Nilai konsentrasi ppm/%LEL untuk H₂S, CO, benzena | GLD saat ini mengeluarkan label jenis gas + confidence, bukan nilai konsentrasi. Model saat ini mengenali udara bersih, LPG, dan H₂. |
| "Mendeteksi H₂S/benzena" sebagai kemampuan saat ini | Masih tahap pengembangan dataset. Tulis sebagai "gas target pengembangan". |
| "Menggantikan detektor/FGDS yang ada" | GLD adalah lapisan tambahan (advisory), bukan pengganti. |
| Nomor kontrak, nilai anggaran, lokasi titik pemasangan spesifik | Bukan untuk materi umum. |
| Tanggal selesai sertifikasi | Jadwal ditentukan lembaga sertifikasi. |

## Glosarium singkat (opsional, untuk boks kecil)
- **LoRa** — teknologi radio jarak jauh berdaya rendah untuk perangkat IoT.
- **Mesh** — jaringan di mana data bisa melompat antar-perangkat hingga sampai tujuan.
- **Edge AI** — kecerdasan buatan yang berjalan langsung di perangkat, bukan di server.
- **ATEX / IECEx** — skema sertifikasi peralatan untuk area berpotensi ledakan.
- **Confidence** — tingkat keyakinan model terhadap hasil klasifikasinya.
