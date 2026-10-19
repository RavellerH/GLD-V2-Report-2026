# Naskah narasi GLD (Gemini TTS)

Instruksi gaya: Bacakan dalam Bahasa Indonesia baku dengan nada formal, tenang, dan meyakinkan, seperti narator video teknologi industri. Tempo sedang, jeda singkat di setiap koma. Istilah bahasa Inggris dibaca dengan pelafalan bahasa Inggris.

## 01_hook — 01 Hook (8 dtk, 14 kata)

Simpan hasil sebagai `public/audio/vo/01_hook.wav`

Kebocoran gas di kilang tidak kasatmata, dan setiap detik keterlambatan deteksi memperbesar risiko keselamatan.

## 02_problem — 02 Masalah (10 dtk, 21 kata)

Simpan hasil sebagai `public/audio/vo/02_problem.wav`

Detektor konvensional umumnya dirancang untuk satu jenis gas dan bergantung pada kabel data menuju ruang kontrol, sehingga mahal dan sulit diperluas.

## 03_intro — 03 Perkenalan GLD (11 dtk, 20 kata)

Simpan hasil sebagai `public/audio/vo/03_intro.wav`

GLD mengintegrasikan delapan sensor gas, data acquisition dua puluh empat bit, prosesor edge AI, dan radio LoRa dalam satu unit.

## 04_fingerprint — 04 Sidik jari gas & model AI (33 dtk, 66 kata)

Simpan hasil sebagai `public/audio/vo/04_fingerprint.wav`

Sensor metal-oxide semiconductor tidak sepenuhnya selektif; satu sensor dapat merespons berbagai jenis gas. Keterbatasan tersebut justru dimanfaatkan sebagai keunggulan. Delapan sensor dengan sensitivitas berbeda membentuk satu vektor respons, layaknya sidik jari kimia, sesuai prinsip electronic nose. Convolutional Neural Network dua cabang mempelajari pola temporal sinyal sensor sekaligus profil sensitivitasnya, kemudian dikuantisasi ke delapan bit dan dijalankan langsung pada mikrokontroler sebagai edge AI, tanpa bergantung pada server.

## 05_trainable — 05 Dapat dilatih ulang (20 dtk, 36 kata)

Simpan hasil sebagai `public/audio/vo/05_trainable.wav`

Saat ini, model telah mengklasifikasikan udara bersih, LPG, dan hidrogen. Delapan sensor yang sama juga sensitif terhadap metana, karbon monoksida, amonia, dan benzena; model untuk gas tersebut dilatih ulang menggunakan portable test chamber di lokasi kilang.

## 06_mesh — 06 Private mesh LoRa (25 dtk, 58 kata)

Simpan hasil sebagai `public/audio/vo/06_mesh.wav`

Komunikasi menggunakan private mesh LoRa dua lapis pada pita sembilan ratus dua puluh megahertz. Node sensor terhubung ke Cluster Head, dan antar-Cluster Head membentuk jaringan multi-hop menuju gateway, tanpa internet dan terpisah dari jaringan TI kilang. Bila satu Cluster Head gagal, node tetangga memilih parent baru secara otomatis, dengan signal hysteresis dan loop prevention agar rute tetap stabil.

## 07_alarm — 07 Alarm otomatis (19 dtk, 36 kata)

Simpan hasil sebagai `public/audio/vo/07_alarm.wav`

Saat terjadi kebocoran, perubahan pola respons sensor langsung dikenali, dan GLD membunyikan alarm lokal. Data normal diambil secara berkala, sedangkan alarm dikirim segera melalui mekanisme push ke dashboard operator, lengkap dengan identitas sensor dan tingkat risikonya.

## 08_field — 08 Teruji lapangan (14 dtk, 38 kata)

Simpan hasil sebagai `public/audio/vo/08_field.wav`

GLD telah melalui pengujian lapangan: generasi pertama diuji di RU VII Kasim pada Desember 2025. Generasi kedua lulus seluruh tujuh butir Factory Acceptance Test di laboratorium, serta pengujian multi-hop mesh, failover, dan push alarm pada delapan Cluster Head.

## 09_roadmap — 09 Pengembangan berikutnya (10 dtk, 19 kata)

Simpan hasil sebagai `public/audio/vo/09_roadmap.wav`

Tahap pengembangan berikutnya adalah integrasi kamera thermal untuk pemantauan area, sebagai pelengkap deteksi titik GLD dalam satu dashboard terpadu.

## 10_outro — 10 Penutup (14 dtk, 16 kata)

Simpan hasil sebagai `public/audio/vo/10_outro.wav`

GLD: deteksi multigas berbasis edge AI dengan komunikasi self-healing. Dikembangkan di Indonesia untuk industri kilang nasional.
