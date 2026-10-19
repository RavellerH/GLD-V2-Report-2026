# Video "GLD Next: Optical Gas Imaging MWIR" — Naskah & Storyboard (Draft 1)

*Untuk pameran Pertamina di Cilacap · audiens: direksi/pengambil keputusan + tim teknis · 19 Okt 2026*

**Prinsip:**
- Strategis di awal dan akhir, fundamental teknis di tengah.
- Seluruh video berlabel **"Konsep pengembangan"** (badge kecil permanen di pojok).
- Tanpa angka kinerja yang belum diuji. Spesifikasi kamera dikutip dari proposal resmi. Jangkauan ±100 m disebut sebagai *target yang divalidasi di lapangan*.
- Cakupan: **seluruh kilang Pertamina**, bukan satu RU.
- Pameran sering tanpa suara, jadi semua poin penting juga muncul sebagai teks di layar dan subtitle selalu aktif.
- Versi **ID** (istilah teknis tetap bahasa Inggris) dan **EN**; landscape (layar pameran) + portrait.
- Durasi ±4 menit.

---

| # | Adegan | Durasi | Narasi (ID) | Visual |
|---|---|---|---|---|
| 1 | **Pembuka** | 0:00–0:14 | Kilang beroperasi tanpa henti. Kebocoran hidrokarbon tidak kasatmata, dan tidak selalu mengalir menuju sensor. | Intro motion graphic (gaya intro GLD) → b-roll kilang malam, plume tak terlihat bergerak menjauh dari titik sensor |
| 2 | **Mengapa penting** | 0:14–0:38 | Setiap kebocoran membawa tiga risiko sekaligus: keselamatan pekerja dan aset, keberlanjutan operasi, serta emisi. Metana, komponen utama gas proses, memiliki potensi pemanasan global hampir tiga puluh kali karbon dioksida. | Tiga kartu: Keselamatan · Kontinuitas operasi · Emisi/ESG. Angka "≈30× CO₂ (GWP100, IPCC AR6)" dengan sitasi kecil |
| 3 | **GLD hari ini** | 0:38–1:04 | GLD telah menghadirkan deteksi titik berbasis edge AI: mengenali jenis gas langsung di perangkat dan mengirim alarm melalui private mesh LoRa. Namun, sensor titik hanya mendeteksi gas yang mencapai lokasinya; hasilnya bergantung pada arah angin dan jarak sumber kebocoran. | Peta unit: titik GLD + lingkaran radius deteksi. Plume yang terbawa angin ke celah antar-sensor ditandai "tidak terpantau" |
| 4 | **Prinsip fisika OGI** | 1:04–1:44 | Optical Gas Imaging memanfaatkan sifat molekul hidrokarbon: ikatan karbon-hidrogen menyerap radiasi inframerah pada panjang gelombang sekitar tiga koma tiga mikrometer, dalam pita Mid-Wave Infrared. Dengan filter spektral sempit pada pita tersebut, gas yang semula tak terlihat tampak sebagai kontras terhadap radiasi latar belakang. | Animasi spektrum elektromagnetik → zoom ke MWIR 3–5 µm → kurva serapan C–H memuncak di 3,3 µm → filter bandpass "memotong" pita → plume muncul di citra |
| 5 | **Mengapa kamera berpendingin** | 1:44–2:08 | Agar kontras sekecil itu terdeteksi, detektor didinginkan hingga sekitar minus seratus sembilan puluh enam derajat Celsius. Derau termal sensor menjadi jauh lebih rendah daripada sinyal gas, sehingga kebocoran kecil pun dapat divisualisasikan. | Diagram detektor MCT + Stirling cooler, termometer turun ke ≈77 K (−196 °C). Perbandingan NETD: berpendingin vs tanpa pendingin |
| 6 | **Sistem kamera di lapangan** | 2:08–2:36 | Kamera dipasang pada tiang sekitar sepuluh meter dengan pan-tilt, berpatroli pada beberapa preset sektor kritis: jalur pipa, manifold, dan klaster valve. Target jangkauan visualisasi sekitar seratus meter, yang divalidasi melalui uji pelepasan gas terkontrol. | 3D/animasi kamera di tiang, kerucut pandang menyapu ±60° dengan 3 preset. Kartu spesifikasi: MWIR 3–5 µm (filter ±3,3 µm) · cooled MCT 640×512 · 100 Hz · NETD ≤25 mK (dari proposal) |
| 7 | **Edge AI** | 2:36–3:00 | Di edge server, model deep learning melakukan segmentasi plume secara otomatis. Alarm hanya dipicu bila plume terdeteksi konsisten pada beberapa frame berturut-turut, sehingga gangguan dari flare atau pantulan panas dapat ditekan. | Klip ilustrasi thermal + mask segmentasi + confidence bar. Timeline frame: alarm hanya bila deteksi persisten |
| 8 | **Satu sistem: GLD + OGI** | 3:00–3:30 | GLD menjawab gas apa dan seberapa pekat; kamera OGI menjawab di mana dan ke arah mana gas menyebar. Bila keduanya mendeteksi pada waktu dan lokasi yang sama, sistem menetapkan prioritas tertinggi untuk respons lapangan. | Dashboard terpadu: kartu GLD (jenis gas, konsentrasi) + feed OGI + peta. Matriks 3 skenario (GLD saja / kamera saja / keduanya = prioritas tinggi) |
| 9 | **Batasan & validasi** | 3:30–3:50 | Kinerja OGI dipengaruhi kontras termal, angin, laju kebocoran, dan garis pandang; hidrogen, karbon monoksida, dan hidrogen sulfida tidak tampak pada pita ini. Karena itu, kamera melengkapi GLD, bukan menggantikannya. | Ikon faktor lingkungan. Tabel "terlihat OGI: CH₄, C₃H₈, C₄H₁₀, VOC / tidak: H₂, CO, H₂S → tetap GLD" |
| 10 | **Nilai strategis & roadmap** | 3:50–4:12 | Dirancang modular untuk direplikasi di seluruh kilang Pertamina, sistem ini juga mendukung dokumentasi emisi fugitif. Pada tahap berikutnya, kamera termografi radiometrik berpotensi diperluas untuk predictive maintenance: hot spot heater, isolasi rusak, dan steam trap. | Peta Indonesia dengan RU II–VII menyala bertahap. Kartu "Potensi pengembangan: predictive maintenance" (berlabel jelas) |
| 11 | **Penutup** | 4:12–4:25 | Dari deteksi titik menuju pemantauan area. Dikembangkan oleh Lab Internet of Things, Institut Teknologi Bandung. | Kartu ringkasan 4 poin → layar logo Pertamina · LGU · ITB → fade out |

---

## Catatan klaim (jaga tetap aman)
- Semua kemampuan OGI disajikan sebagai **rencana/konsep**, bukan sistem terpasang.
- Spesifikasi kamera = **opsi dalam proposal** (HJK-MWIR MC11H), bukan pilihan final.
- Tidak memakai ROI >300% / pengurangan inspeksi 70% (belum terverifikasi).
- Angka GWP metana = fakta ilmiah (IPCC AR6, fosil ≈29,8 untuk 100 tahun), ditulis "hampir tiga puluh kali".
- Suhu detektor ≈77 K (−196 °C) = praktik umum detektor MWIR berpendingin.

## Aset yang dibutuhkan
- **Remotion (utama):** spektrum & serapan C–H, diagram detektor/pendingin, peta coverage, dashboard terpadu, matriks skenario, peta RU.
- **Blender (opsional, menambah kualitas):** kamera OGI di tiang dengan PTZ menyapu area pipa. Kira-kira 1–2 jam render.
- **Klip ilustrasi thermal** yang sudah ada (berlabel "ilustrasi konsep").
- **Narasi:** 1 permintaan TTS per bahasa (Erinome), setelah naskah disetujui.
