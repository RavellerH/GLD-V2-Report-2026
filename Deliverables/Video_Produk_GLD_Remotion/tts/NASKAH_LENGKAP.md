# Naskah narasi GLD (Gemini TTS)

Instruksi gaya: Bacakan dalam Bahasa Indonesia baku dengan nada formal, tenang, dan meyakinkan, seperti narator video teknologi industri. Tempo sedang, jeda singkat di setiap koma.

## 01_hook — 01 Hook (8 dtk, 14 kata)

Simpan hasil sebagai `public/audio/vo/01_hook.wav`

Kebocoran gas di kilang tidak kasatmata, dan setiap detik keterlambatan deteksi memperbesar risiko keselamatan.

## 02_problem — 02 Masalah (13 dtk, 21 kata)

Simpan hasil sebagai `public/audio/vo/02_problem.wav`

Detektor konvensional umumnya dirancang untuk satu jenis gas dan bergantung pada kabel data menuju ruang kontrol, sehingga mahal dan sulit diperluas.

## 03_intro — 03 Perkenalan GLD (11 dtk, 20 kata)

Simpan hasil sebagai `public/audio/vo/03_intro.wav`

GLD mengintegrasikan delapan sensor gas, akuisisi data dua puluh empat bit, prosesor AI tertanam, dan radio LoRa dalam satu unit.

## 04_fingerprint — 04 Sidik jari gas & model AI (40 dtk, 64 kata)

Simpan hasil sebagai `public/audio/vo/04_fingerprint.wav`

Sensor semikonduktor oksida logam tidak sepenuhnya selektif; satu sensor dapat bereaksi terhadap banyak gas. Keterbatasan tersebut justru dimanfaatkan sebagai keunggulan. Delapan sensor dengan sensitivitas berbeda membentuk satu vektor respons, layaknya sidik jari kimia, sesuai prinsip hidung elektronik. Jaringan saraf konvolusional dua cabang mempelajari pola temporal sinyal sensor sekaligus profil sensitivitasnya, kemudian dikuantisasi ke delapan bit dan dijalankan langsung di mikrokontroler, tanpa bergantung pada server.

## 05_trainable — 05 Dapat dilatih ulang (20 dtk, 36 kata)

Simpan hasil sebagai `public/audio/vo/05_trainable.wav`

Saat ini, model telah mengklasifikasikan udara bersih, LPG, dan hidrogen. Delapan sensor yang sama juga sensitif terhadap metana, karbon monoksida, amonia, dan benzena; model untuk gas tersebut dilatih ulang menggunakan chamber uji portabel di lokasi kilang.

## 06_mesh — 06 Private mesh LoRa (32 dtk, 59 kata)

Simpan hasil sebagai `public/audio/vo/06_mesh.wav`

Komunikasi menggunakan jaringan mesh LoRa privat dua lapis pada pita sembilan ratus dua puluh megahertz. Node sensor terhubung ke Cluster Head, dan antar-Cluster Head membentuk mesh multi-hop menuju gateway, tanpa internet dan terpisah dari jaringan TI kilang. Bila satu Cluster Head gagal, node tetangga memilih induk baru secara otomatis, dengan histeresis sinyal dan pencegahan loop agar rute tetap stabil.

## 07_alarm — 07 Alarm otomatis (13 dtk, 22 kata)

Simpan hasil sebagai `public/audio/vo/07_alarm.wav`

Data normal diambil secara berkala, sedangkan alarm dikirim segera melalui mekanisme push ke dashboard operator, lengkap dengan identitas sensor dan tingkat risikonya.

## 08_outro — 08 Penutup (14 dtk, 22 kata)

Simpan hasil sebagai `public/audio/vo/08_outro.wav`

GLD: deteksi multigas berbasis kecerdasan buatan di tepi jaringan, dengan komunikasi yang memulihkan dirinya sendiri. Dikembangkan di Indonesia untuk industri kilang nasional.
