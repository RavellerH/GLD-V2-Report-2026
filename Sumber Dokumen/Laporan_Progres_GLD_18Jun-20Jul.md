# LAPORAN PROGRES PROYEK GAS LEAK DETECTION (GLD)
### Periode: 18 Juni – 20 Juli
**Sumber data:** Kompilasi catatan rapat mingguan dan diskusi tim (grup koordinasi GLD)
**Pihak terlibat:** LAPI Ganesha Utama (LGU) · Lab Fisika & Lab IoT ITB · PT Pertamina (Persero)

---

## 1. Ringkasan Eksekutif

Selama periode pelaporan, pekerjaan terkonsentrasi pada empat lini paralel: **(a)** karakterisasi jaringan LoRa dan strategi penempatan *Cluster Head* (CH), **(b)** pengembangan model AI berbasis *fingerprint* multi-sensor MQ, **(c)** validasi sistem catu daya solar–baterai beserta manajemen daya, dan **(d)** penyiapan *gas test chamber* serta QC perangkat.

Tiga capaian utama:
1. Uji coba komunikasi 2 CH telah dilaksanakan; strategi penempatan CH di titik tinggi telah dirumuskan sebagai prinsip desain.
2. Profil beban daya GLD telah terukur (8 sensor MQ ≈ 5,8–6 W @ 5 V) dan skema *duty cycling* (ON 60 s / OFF 100 s, interval WAKE 160 s) telah disimulasikan di board.
3. Arah pengembangan AI bergeser dari deteksi biner *gas/no-gas* menjadi pengenalan **pola relatif antar-8 sensor** dengan mempertimbangkan fase transien, stasioner, dan waktu saturasi.

Tiga isu kritis yang menahan progres:
1. **Mode baterai belum terbukti mampu menyuplai seluruh heater MQ** (terukur ~2,43 W vs kebutuhan ~6 W).
2. **Rangkaian DC converter perlu diganti atau dimodifikasi.**
3. **Keterbatasan jangkauan antena LoRa 6 m yang hanya mencapai ±100 m**, belum sebanding dengan kebutuhan cakupan area RU.

---

## 2. Perkembangan per Area Kerja

### 2.1 Jaringan LoRa & Penempatan Cluster Head

**Metodologi penempatan yang disepakati:**
Urutan kerja ditetapkan sebagai: survei lapangan Pertamina → penentuan posisi GLD → perancangan posisi dan jumlah CH optimum → penentuan posisi Gateway (GW). Perlu diidentifikasi CH mana yang bersifat dominan dan mana yang pendukung, serta apakah GW dapat dijangkau langsung atau memerlukan CH perantara.

**Prinsip desain yang dirumuskan:**
- CH ditempatkan **setinggi mungkin** agar sinyal hanya menembus kanopi pohon satu kali; penembusan berulang meningkatkan *data loss*.
- CH **tidak boleh** diletakkan di permukaan tanah.
- Prioritas kandidat lokasi saat survei: tempat tinggi, bangunan, tiang, dan tower.
- Daftar titik tinggi hasil survei akan diajukan ke Pertamina untuk konfirmasi lokasi mana yang diizinkan dipasangi CH.
- Secara modulasi, LoRa lebih unggul dari GSM karena memang dirancang untuk *long range*.

**Hasil dan aktivitas pengujian:**
- Karakterisasi PDR (*Packet Delivery Ratio*) telah divariasikan terhadap jarak, sudut LoS, dan tinggi antena untuk kombinasi TX–RX. Obstruksi berupa pohon, gedung, dan benda logam menjadi variabel amatan.
- Antena LoRa berukuran panjang telah dibeli dari China untuk jangkauan lebih jauh.
- **Temuan (26 Juni):** antena LoRa 6 m maksimum hanya mencapai ±100 m.
- Uji coba 2 CH dijadwalkan/dilaksanakan 6 Juli.
- Uji coba awal dilakukan di lingkungan ITB terlebih dahulu (area terbuka, belakang gedung) sebagai representasi variasi kondisi lapangan.

**Kebutuhan lanjutan (16 Juli):**
- Mengumpulkan **bukti empirik** bahwa komunikasi antar-CH ke CH1 Labtek XV lebih stabil bila ditempatkan di posisi tinggi.
- Merancang eksperimen untuk menentukan **jumlah CH minimum** yang dibutuhkan. Pengujian dapat dilakukan dengan GLD tanpa sensor terlebih dahulu.
- Pertanyaan terbuka: apakah diperlukan **peta 3D** untuk memastikan *line of sight* antar CH–GLD?

**Perizinan internal:** pemasangan di Labtek XV lantai 8 memerlukan izin ke Kaprodi terlebih dahulu; kemungkinan tidak perlu sampai tingkat FMIPA.

---

### 2.2 Pengembangan AI & Pengolahan Data Sensor MQ

**Prinsip pemodelan yang ditetapkan (18 Juni & 16 Juli):**

Target utama adalah menghasilkan model AI yang lebih baik dari tahun sebelumnya. Saat ini masih menggunakan data Excel dari Tahap 1.

Pergeseran paradigma yang disepakati:

| Pendekatan Lama | Pendekatan Baru |
|---|---|
| Analisis per sensor MQ individual | *Fingerprint* gabungan seluruh 8 sensor |
| Grafik diplot per MQ | Grafik diplot **per jenis gas** (8 parameter) |
| Fokus pada amplitudo absolut | Fokus pada **pola / amplitudo relatif** |
| Output biner gas / no-gas (respons fungsi tangga) | Mempertimbangkan fase transien, stasioner, dan waktu saturasi |

**Rasional sensor fusion:**
Sensor MQ bersifat *multi-gas* dan tidak spesifik untuk satu gas. Karena itu perlu dipetakan MQ mana yang dominan untuk gas apa, lalu MQ yang kurang dominan digunakan sebagai pelengkap. Penamaan "sensor gas X" merujuk pada dominansi, bukan eksklusivitas — misalnya seluruh MQ dapat mendeteksi LPG, metana pada MQ2, dan satu MQ untuk alkohol juga dapat merespons LPG. Datasheet masing-masing sensor perlu dirujuk untuk pemetaan ini.

Redundansi antar-sensor yang mendeteksi gas sama justru menjadi kekuatan, dengan dua manfaat:
1. **Meningkatkan kepercayaan** terhadap identifikasi gas yang terdeteksi.
2. **Berfungsi sebagai validator kesehatan sensor** — bila suatu sensor sebelumnya dapat mendeteksi lalu tidak lagi, sensor lain dapat mengoreksi.

Amplitudo sinyal tahun lalu tidak dapat dibandingkan langsung dengan sekarang, namun urutan dan polanya seharusnya konsisten.

**Temuan eksperimental (16 Juli):**
- Pada pemaparan **CO₂**, respons seluruh sensor berkorelasi positif; namun **tidak demikian saat diberikan O₂**. Hal ini terkait mekanisme kerja sensor, di mana O₂ berperan menggantikan gas yang terdeteksi.
- **Baseline tiap sensor berbeda** karena pengujian dilakukan di udara terbuka; MQ135 lebih sensitif dibanding MQ8. Konsekuensinya, **threshold harus ditetapkan per MQ**, bukan seragam.
- Karakteristik baseline antar-sensor MQ dapat dijadikan **panduan QC**.
- Dimungkinkan penerapan **satu model per unit GLD** di lapangan, yang berimplikasi pada kebutuhan QC untuk setiap unit GLD.

**Isu konsistensi data (16 Juli):**
Ketidakkonsistenan akuisisi data perlu diinvestigasi lebih lanjut — apakah bersumber dari algoritma akuisisi atau dari proses pemberian gas yang masih manual. Perlu juga ditelusuri apakah ADC dan sensor masih merupakan faktor internal atau sudah eksternal. Karena kondisi lapangan bersifat *unpredictable* dan *uncontrollable*, perlu diuji apakah model AI tetap mampu menangani ketidakkonsistenan tersebut.

**Model TCNN (26 Juni – Pak Fahdzi):**
Pengembangan *Temporal CNN* dengan data yang tersedia. Data MQx merupakan data tegangan. Skema deteksi: memprediksi data 5 detik ke depan dari 5 detik sebelumnya.

---

### 2.3 Sistem Catu Daya & Manajemen Energi

#### a. Kinerja Solar Panel & Baterai

| Tanggal | Hasil Pengukuran |
|---|---|
| 6 Juli | Pengisian pukul 08:00–16:00 menaikkan baterai dari 3,0 V ke 3,4 V (±20%) |
| 9 Juli | Vp = 7,25 V; Ip = 0,05 A (matahari mulai redup); V baterai = 3,09 V* |
| 14 Juli | Pukul 11:00–15:00 tegangan stabil ±4,17 V dengan arus/daya mendekati nol → baterai kondisi penuh. Setelah ±14:00 arus dan daya negatif (mulai *discharge*) karena energi panel tidak lagi mencukupi beban; tegangan turun bertahap ke ±4,12 V |

*\*Catatan: pada catatan asli tertulis "309 V" — diasumsikan salah ketik untuk 3,09 V. Perlu konfirmasi ke pencatat data.*

**Analisis penyebab pengisian belum optimal (9 Juli):**
Lokasi pengecasan hanya menerima sinar optimal sekitar pukul 10:00–13:00; di luar rentang tersebut sebagian area tertutup bayangan pohon/gedung. **Rekomendasi:** memindahkan titik pengecasan ke lokasi yang lebih optimal seperti rooftop.

#### b. Profil Beban Daya GLD (13 Juli)

| Jalur | Pengukuran | Daya | Status |
|---|---|---|---|
| 5V 20A GLD | 1,15–1,19 A @ 5 V | ±5,8–6 W | Normal & konsisten |
| Board Pemanas 5V 20A | 1,15–1,19 A @ 5 V | ±5,8–6 W | Normal & konsisten |
| 24V 5A | 0,29 A @ 24 V | ±6,96 W | Wajar (setelah rugi konverter) |
| Battery 3,8 V | 0,64 A @ 3,8 V | ±2,43 W | **Tidak sesuai** — jauh di bawah kebutuhan ±6 W |

**Kesimpulan:** jalur 5 V dan 24 V aman dan masuk akal, namun **mode baterai belum mampu atau belum terbukti menyuplai seluruh heater MQ secara penuh**. Tiga hipotesis penyebab:
1. Heater MQ tidak menerima 5 V penuh saat mode baterai;
2. Tidak seluruh heater aktif;
3. Arus baterai yang terukur bukan merupakan total beban board.

*Tindak lanjut yang diusulkan:* pengukuran ulang dengan menyertakan data tegangan pada tiap titik ukur.

#### c. Strategi Manajemen Daya (16 & 20 Juli)

**Arahan konseptual:**
- Meminimalkan **T_on** dengan mengobservasi kapan sensor benar-benar mencapai saturasi (estimasi sementara 15 s).
- Membedakan waktu kesiapan sensor pada ***cold boot*** vs ***warm boot*** — kondisi kedua semestinya lebih singkat karena sensor sudah hangat.
- Diperlukan **kontroler daya** agar sensor tidak perlu selalu menyala.
- Inferensi tidak perlu dijalankan terus-menerus, misalnya saat tidak terdeteksi kenaikan atau *peak*.
- Saat inferensi, daya ke MQ dimatikan; **ESP tetap menyala**, hanya suplai ke MQ yang diputus.
- Pertanyaan terbuka: apakah seluruh sensor perlu aktif selama inferensi, dan apakah model dapat belajar hanya dari data 10–15 detik awal?

**Implementasi simulasi (20 Juli – Fahmi):**
Program sederhana diunggah langsung ke board GLD sebagai simulasi sementara siklus operasi (warm-up sensor → akuisisi data → inference → transmit LoRa):

| Parameter | Nilai |
|---|---|
| Durasi ON (setelah WAKE + boot) | 60 detik |
| Durasi OFF | 100 detik |
| Interval pulsa WAKE | 160 detik |

**Arahan tindak lanjut (20 Juli):** rangkaian sudah dinilai berfungsi, namun **circuit DC converter harus diganti atau dimodifikasi**. Pekerjaan modifikasi baterai ditahan sementara; fokus dialihkan ke pekerjaan lain.

**Catatan durasi data:** data solar-baterai baru terkumpul 10 hari, sementara kebutuhan minimum adalah 1 bulan. Opsi pengembangan berikutnya adalah **GLD berbasis solar panel** — saat ini implementasi solar baru diterapkan pada CH.

---

### 2.4 Gas Test Chamber, Hardware & QC

**Gas Test Chamber:**
- Mahasiswa penanggung jawab penyelesaian chamber telah didapatkan (6 Juli).
- Sambungan, selang, dan komponen terkait telah ditempelkan ke dinding chamber. Pompa, valve, dan alat lain menyusul.
- Konstruksi harus **kompak dan *fixed*** karena chamber akan dibawa berpindah lokasi.
- Metode aliran gas (**disedot vs didorong**) sebaiknya diuji keduanya untuk menentukan mana yang lebih baik.

**Hardware & QC:**
- **Grounding** casing, antena, dan PCB telah diperiksa; kondisi saat ini baik. Perlu diputuskan apakah perlu disatukan.
- **Solder vs soket** untuk sensor perlu dievaluasi: risiko korosi pada koneksi soket vs kemudahan perbaikan modular dibanding penggantian *full board*.
- **QC untuk setiap sensor perlu dipastikan**, dengan karakteristik baseline sebagai acuan.
- **Praktik keselamatan:** mencabut komponen dalam keadaan menyala harus dihindari. Eksperimen yang tidak relevan dengan kondisi lapangan sebaiknya tidak dilakukan. Kedua hal ini perlu dicantumkan dalam **SOP** untuk mencegah *human error*.
- **Penataan ulang lab** (Pak Maman) agar lebih nyaman dan rapi, sekaligus persiapan menerima tamu/kunjungan.

---

### 2.5 Perangkat Lunak & Pengelolaan Repositori

**Aplikasi UI GLD (16 Juli):**
Telah dibuat aplikasi dengan antarmuka untuk GLD bagi tiap-tiap sensor, dilengkapi tab untuk pengambilan dataset, *capture*, *save*, dan *download*. Koneksi menggunakan USB (perlu konfirmasi). Aplikasi memungkinkan pembangunan model langsung di PC tanpa perlu ekspor data manual — persiapan untuk satu titik uji di lapangan.

**Repositori kode (2 Juli):**
Source code saat ini masih tersebar di beberapa repositori sesuai pembagian tim: **GLD & AI**, **jaringan**, dan **server**. Rencana ke depan adalah konsolidasi menjadi **satu repositori utama** agar pengelolaan lebih mudah.

**Akses kolaborator Pertamina:** tim LGU meminta daftar username GitHub rekan-rekan Pertamina untuk ditambahkan sebagai collaborator. Kontak yang telah diajukan: `anita.rohmawati@gmail.com`.

---

### 2.6 Koordinasi dengan Pertamina & Perizinan

**Urutan pekerjaan yang disepakati (17 Juli):**
Sebelum langsung menuju Cilacap, alur kerja mengikuti urutan berikut:

1. **LGU mengundang Pertamina** ke workshop/laboratorium untuk melihat progres dan hasil pembuatan;
2. **Pelaksanaan pengujian** di lab;
3. **Baru kemudian** kunjungan ke RU.

**Kebutuhan dokumen:** dokumen pengurusan izin **JSA/TRA** perlu dikonfirmasi kesiapannya. Persiapan site visit Pertamina ke lab diminta untuk segera diatur.

**Persiapan pengujian Cilacap:** jenis gas yang akan diuji perlu dicatat. Chamber diperlukan segera (dalam proses penyiapan). Tabung gas yang ditawarkan perlu dicek.

**Catatan manajerial (18 Juni):**
- Proyek ini merupakan contoh **TRL-7 (level industri)**, sementara riset di lingkungan FI umumnya berada pada TRL-3.
- Sharing problem antar peserta lab didorong — melihat masalah orang lain sering terasa lebih mudah dan menumbuhkan kesadaran bahwa persoalan teknis dihadapi bersama, sehingga saling mendukung.
- Prinsip kerja: **lebih baik banyak bekerja daripada banyak rapat**; rapat cukup 1 jam.

---

## 3. Isu Terbuka & Risiko

| No | Isu | Dampak | Prioritas |
|---|---|---|---|
| 1 | Mode baterai belum terbukti menyuplai 8 heater MQ penuh (2,43 W vs 6 W) | GLD tidak dapat beroperasi mandiri di lapangan | **Tinggi** |
| 2 | Circuit DC converter perlu diganti/dimodifikasi | Menahan finalisasi desain catu daya | **Tinggi** |
| 3 | Jangkauan antena LoRa 6 m hanya ±100 m | Berpotensi meningkatkan jumlah CH yang dibutuhkan secara signifikan | **Tinggi** |
| 4 | Ketidakkonsistenan akuisisi data belum diketahui akar penyebabnya | Kualitas dataset pelatihan AI | **Tinggi** |
| 5 | Data solar-baterai baru 10 hari dari minimum 1 bulan | Belum cukup untuk validasi *energy budget* | Sedang |
| 6 | Dokumen JSA/TRA belum dikonfirmasi | Menahan jadwal site visit dan kunjungan RU | Sedang |
| 7 | Izin pemasangan CH di Labtek XV lt.8 belum diperoleh | Menahan eksperimen jaringan | Sedang |
| 8 | Keputusan solder vs soket belum diambil | Berdampak pada strategi maintenance jangka panjang | Sedang |
| 9 | Anomali pencatatan data tegangan baterai (tertulis 309 V) | Integritas dokumentasi pengukuran | Rendah |

---

## 4. Daftar Tindak Lanjut (Action Items)

| No | Tindakan | Penanggung Jawab | Status |
|---|---|---|---|
| 1 | Mengganti/memodifikasi circuit DC converter | Tim Elektronik (Fahmi) | Terbuka |
| 2 | Menahan pekerjaan modifikasi baterai, alihkan ke pekerjaan lain | Tim Elektronik | Diarahkan 20 Juli |
| 3 | Pengukuran ulang beban mode baterai disertai data tegangan | Fahmi | Terbuka |
| 4 | Melanjutkan pengumpulan data solar hingga minimal 1 bulan | Lab IoT (Ryan) | Berjalan (10/30 hari) |
| 5 | Memindahkan titik pengecasan ke rooftop / area bebas bayangan | Ilmania / Lab Fisika | Diusulkan |
| 6 | Eksperimen bukti empirik stabilitas CH di posisi tinggi → CH1 Labtek XV | Tim Jaringan | Terbuka |
| 7 | Eksperimen penentuan jumlah CH minimum (dapat tanpa sensor) | Tim Jaringan | Terbuka |
| 8 | Mengajukan izin pemasangan CH Labtek XV lt.8 ke Kaprodi | — | Terbuka |
| 9 | Menyusun daftar titik tinggi hasil survei untuk diajukan ke Pertamina | Tim Survei | Terbuka |
| 10 | Pemetaan MQ dominan per jenis gas berbasis datasheet | Tim GLD & AI | Berjalan |
| 11 | Replot grafik per jenis gas (8 parameter), bukan per sensor | Tim GLD & AI | Terbuka |
| 12 | Pengembangan model TCNN (prediksi 5 s dari 5 s sebelumnya) | Pak Fahdzi | Berjalan |
| 13 | Investigasi akar penyebab ketidakkonsistenan akuisisi data | Tim GLD & AI | Terbuka |
| 14 | Penetapan threshold per MQ berbasis karakteristik baseline | Tim GLD & AI | Terbuka |
| 15 | Penyelesaian gas test chamber (pompa, valve, mounting) | Mahasiswa PJ Chamber | Berjalan |
| 16 | Uji metode aliran gas: disedot vs didorong | Tim Chamber | Terbuka |
| 17 | Konsolidasi repositori menjadi satu repo utama | Farhan Budiman | Terencana |
| 18 | Menambahkan collaborator GitHub dari Pertamina | Farhan Budiman | Menunggu daftar username |
| 19 | Penyiapan dokumen JSA/TRA | Pak Tresnandi / LGU | Terbuka |
| 20 | Penjadwalan site visit Pertamina ke workshop/lab LGU | LGU | Terbuka |
| 21 | Pencatatan jenis gas untuk pengujian Cilacap & cek tabung gas | Tim Pengujian | Terbuka |
| 22 | Penyusunan SOP (larangan cabut komponen saat on, ruang lingkup eksperimen) | Tim Lab | Terbuka |
| 23 | Evaluasi keputusan solder vs soket sensor | Tim Elektronik | Terbuka |
| 24 | Penataan ulang lab | Pak Maman | Berjalan |

---

## 5. Rekomendasi

1. **Prioritaskan penyelesaian isu catu daya mode baterai.** Selisih 2,43 W vs 6 W adalah *blocker* fungsional — tanpa kepastian ini, seluruh skema *duty cycling* dan target autonomi lapangan tidak dapat divalidasi. Pengukuran ulang dengan data tegangan lengkap sebaiknya dilakukan bersamaan dengan penggantian DC converter.

2. **Kuantifikasi ulang implikasi jangkauan LoRa 100 m terhadap desain jaringan.** Angka ini perlu segera dikonversi menjadi estimasi jumlah CH untuk area RU. Bila jumlahnya tidak realistis secara biaya, opsi antena, tinggi mounting, atau parameter LoRa perlu ditinjau ulang sebelum survei lapangan.

3. **Formalkan SOP pengujian sebelum site visit Pertamina.** Kunjungan Pertamina ke lab merupakan gerbang menuju tahap RU; SOP, dokumen JSA/TRA, dan penataan lab perlu tuntas sebagai satu paket kesiapan.

4. **Pisahkan penyebab internal dan eksternal pada isu konsistensi data.** Selama pemberian gas masih manual, sulit menyimpulkan apakah variabilitas berasal dari ADC/sensor atau dari prosedur. Penyelesaian chamber menjadi prasyarat untuk isolasi variabel ini.

5. **Tetapkan protokol QC per unit GLD sejak sekarang.** Bila arah pengembangan menuju satu model AI per unit GLD, karakterisasi baseline tiap unit menjadi bagian dari proses produksi, bukan sekadar pengujian akhir.

---

*Laporan disusun berdasarkan kompilasi catatan koordinasi periode 18 Juni – 20 Juli. Beberapa poin dalam catatan asli berupa pertanyaan terbuka atau bersifat estimasi dan telah ditandai sebagaimana adanya.*
