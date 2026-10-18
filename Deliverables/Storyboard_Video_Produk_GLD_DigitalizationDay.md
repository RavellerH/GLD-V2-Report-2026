# Storyboard Video Penjelasan Produk GLD (2 menit)

**Acara:** Digitalization Day · **Durasi:** 120 detik · **Rasio:** 16:9, 1920×1080, 30 fps
**Alat:** Blender (3D perangkat) + Remotion (motion graphic, teks, diagram, komposisi akhir)
**Pesan inti (2 saja):** (1) **satu perangkat, banyak gas**; (2) **jaringan mesh LoRa privat**: tanpa internet, tanpa kabel data, dan tetap berjalan meski satu node mati.

---

## 1. Catatan klaim (baca dulu)

"Mendeteksi semua jenis gas" **tidak bisa dipakai apa adanya**: model AI yang tervalidasi saat ini baru mengklasifikasikan **Udara Bersih / LPG / H₂** (TDS Rev 4.0), dan H₂S/Benzena/CO yang diminta Pertamina belum tercakup. Kalau ditonton tim Pertamina yang tahu requirement tersebut, klaim "semua gas" bisa jadi bumerang.

Versi yang tetap kuat dan jujur: **"multi-gas yang bisa diajari"**. 8 sensor membaca *sidik jari* gas, AI di perangkat mengenalinya, dan chamber portable bisa dibawa ke tiap kilang untuk **melatih gas baru sesuai kebutuhan lokasi**. Ini justru pembeda yang lebih menarik daripada sekadar "semua gas".

| ✅ Aman dipakai | ❌ Jangan dipakai |
|---|---|
| 8 sensor gas dalam satu unit | "Mendeteksi semua gas" |
| AI berjalan langsung di perangkat (edge) | "Sudah bersertifikat ATEX" (masih proses) |
| Mengenali LPG, H₂, udara bersih; gas lain bisa dilatih di lokasi | "Mendeteksi H₂S / Benzena / CO" |
| Mesh LoRa multi-hop, terbukti 8 Cluster Head se-kampus ITB | "Sudah terpasang/beroperasi di kilang" |
| Rute otomatis berpindah saat Cluster Head mati (failover teruji) | Jarak dalam kilometer per hop |
| Alarm dikirim otomatis (push), tanpa menunggu polling | Akurasi "99%" (angka model masih direkonsiliasi) |
| Jaringan privat, tidak butuh internet atau jaringan IT kilang | Logo Pertamina tanpa izin humas/klien |
| Arsitektur CNN dua cabang, int8, inferensi di ESP32-S3 | Pemulihan rute "seketika" / dalam X detik (belum diukur) |

---

## 2. Storyboard per adegan

**Revisi 18 Okt — narasi formal-akademis.** ±250 kata dalam 120 detik (≈2 kata/detik, tempo presentasi formal). Porsi waktu digeser ke dua pesan inti: AI/ML (30 dtk) dan mesh *self-healing* (30 dtk). Naskah yang dipakai Remotion ada di `Video_Produk_GLD_Remotion/src/timeline.ts`; bila naskah diubah, ubah di sana.

**Dasar teknis narasi** (agar bisa dipertanggungjawabkan saat tanya-jawab):
- *Sensor & akuisisi:* 8 sensor MOX seri MQ (MQ8/MQ135/MQ3/MQ5/MQ4/MQ7/MQ6/MQ2), ADC ADS1256 24-bit, ESP32-S3 — TDS Rev 4.0.
- *Model:* CNN dua cabang — Conv1D atas sinyal sensor + Dense atas profil sensitivitas sensor, dikuantisasi int8, inferensi di ESP32-S3 — presentasi model 6 Agu (lampiran FAT). Kelas yang disebut mengikuti TDS Rev 4.0: udara bersih, LPG, H₂. Angka akurasi sengaja tidak disebut.
- *Mesh:* Cluster Head dua radio — STAR 920 MHz (sensor→CH) dan MESH 921 MHz (CH↔CH); pemilihan induk dinamis, ≤8 kandidat induk, margin pindah 15 dB, *loop guard*, cek jangkauan ke gateway — TDS Rev 4.0. Failover diuji pada mesh 8-CH di kampus ITB. Waktu pemulihan **tidak** disebut karena belum diukur (ambang induk kedaluwarsa di firmware bisa sampai belasan menit), jadi narasi tidak memakai kata "seketika".
- *Alarm:* data normal disimpan di CH dan diambil berkala (*pull*), alarm dikirim *push* — TDS Rev 4.0, push alarm teruji 6–8 Agu.

### Adegan 1 — Hook (0:00–0:08)
- **Visual (Blender):** kilang saat senja, gas keluar dari flange, nyaris tak terlihat.
- **Teks:** *"Gas bocor tidak terlihat."*
- **VO:** "Kebocoran gas di kilang tidak kasatmata, dan setiap detik keterlambatan deteksi memperbesar risiko keselamatan."

### Adegan 2 — Masalah (0:08–0:18)
- **Visual (Remotion):** detektor konvensional berlabel satu gas, kabel panjang ke ruang kontrol, lalu dicoret.
- **VO:** "Detektor konvensional umumnya dirancang untuk satu jenis gas dan bergantung pada kabel data menuju ruang kontrol, sehingga mahal dan sulit diperluas."

### Adegan 3 — Perkenalan GLD (0:18–0:28)
- **Visual (Blender):** hero shot lalu exploded view; label: *8 sensor gas oksida logam (MQ) · ADC 24-bit (ADS1256) · ESP32-S3 · inferensi AI · Radio LoRa 920 MHz*.
- **VO:** "GLD mengintegrasikan delapan sensor gas, akuisisi data dua puluh empat bit, prosesor ESP32-S3, dan radio LoRa dalam satu unit."

### Adegan 4 — Sidik jari gas & model AI (0:28–0:58) ⭐ pesan inti 1
- **Visual fase A (0:28–0:44, Remotion):** batang 8 sensor + radar chart dari **data chamber asli** berganti pola: udara bersih → LPG (*Klasifikasi AI: LPG*) → CO₂. Judul: *"8 sensor, sensitivitas berbeda → satu sidik jari gas"*, sub-judul: prinsip hidung elektronik.
- **Visual fase B (0:44–0:58, Remotion):** diagram arsitektur: *Sinyal 8 sensor → Cabang 1 Conv1D (pola temporal)*; *Profil sensitivitas → Cabang 2 Dense*; keduanya → *Penggabungan* → *Softmax: Udara bersih / LPG / H₂*. Badge: *Kuantisasi int8 · Inferensi di ESP32-S3 · Tanpa server*.
- **VO:** "Sensor semikonduktor oksida logam tidak sepenuhnya selektif; satu sensor dapat bereaksi terhadap banyak gas. Keterbatasan ini justru kami manfaatkan. Delapan sensor dengan sensitivitas berbeda membentuk satu vektor respons, layaknya sidik jari kimia, sesuai prinsip hidung elektronik. Jaringan saraf konvolusional dua cabang mempelajari pola temporal sinyal sensor sekaligus profil sensitivitasnya, kemudian dikuantisasi ke delapan bit dan dijalankan langsung di mikrokontroler, tanpa bergantung pada server."
- **Mengapa ini lebih kaya** (poin untuk tanya-jawab): detektor konvensional mengandalkan selektivitas *satu* sensor terhadap *satu* gas. GLD memakai informasi gabungan dari delapan sensor yang saling tumpang-tindih sensitivitasnya, sehingga satu perangkat bisa membedakan beberapa gas. Cabang Conv1D menangkap dinamika respons terhadap waktu (bukan hanya nilai sesaat), sedangkan cabang kedua menyuntikkan pengetahuan fisik tentang karakter tiap sensor. Kuantisasi int8 membuat model cukup kecil untuk mikrokontroler, sehingga keputusan diambil di perangkat tanpa ketergantungan pada jaringan.

### Adegan 5 — Dapat dilatih ulang (0:58–1:10)
- **Visual (Remotion + foto asli):** foto chamber → *Chamber di kilang → Dataset on-site → Latih model → Update GLD*; peta 6 RU (*Rencana rollout*).
- **VO:** "Saat ini model mengenali udara bersih, LPG, dan hidrogen. Untuk gas lain, data dikumpulkan dengan chamber uji portabel di lokasi kilang, lalu model dilatih ulang."

### Adegan 6 — Private mesh LoRa & pemulihan rute (1:10–1:40) ⭐ pesan inti 2
- **Visual (Remotion):** topologi GLD → CH → Gateway. Tautan STAR (oranye, putus-putus) dan MESH (biru) dibedakan. Panel kanan: *Dua lapis radio* (STAR 920 MHz / MESH 921 MHz). Saat CH-2 mati, panel menampilkan 4 langkah pemulihan: (1) induk tak terdengar → kedaluwarsa, (2) evaluasi hingga 8 kandidat induk, (3) pindah bila sinyal ≥ 15 dB lebih baik (histeresis), (4) *loop guard* & cek jalur ke gateway; lalu paket mengalir lewat CH-3. Catatan: *Failover diuji dengan 8 Cluster Head multi-hop di kampus ITB*.
- **VO:** "Komunikasi menggunakan jaringan mesh LoRa privat dua lapis pada pita sembilan ratus dua puluh megahertz. Node sensor terhubung ke Cluster Head, dan antar-Cluster Head membentuk mesh multi-hop menuju gateway, tanpa internet dan terpisah dari jaringan TI kilang. Bila satu Cluster Head gagal, node tetangga memilih induk baru secara otomatis, dengan histeresis sinyal dan pencegahan loop agar rute tetap stabil."
- **Mengapa histeresis dan loop guard penting** (poin untuk tanya-jawab): tanpa histeresis, node bisa bolak-balik berganti induk setiap kali sinyal berfluktuasi (*route flapping*). Margin 15 dB memastikan perpindahan hanya terjadi bila jalur baru jelas lebih baik. *Loop guard* mencegah paket berputar di antara dua CH yang saling menjadikan induk.

### Adegan 7 — Alarm otomatis (1:40–1:50)
- **Visual (Remotion):** screenshot asli **Alarm Console dashboard RU4** (repo `RavellerH/gasleakdetectionV2-April`, aplikasi `ru-frontend`, data demo dari seed) dengan baris alarm pertama disorot merah, ditambah dua kartu: *Data normal — disimpan di CH, diambil berkala (pull)* vs *Alarm — dikirim segera (push)*.
- **VO:** "Data normal diambil secara berkala, sedangkan alarm dikirim segera melalui mekanisme push ke dashboard operator, lengkap dengan identitas sensor dan tingkat risikonya."

### Adegan 8 — Penutup (1:50–2:00)
- **Visual (Blender → Remotion):** GLD terpasang, kamera mundur ke jaringan node; tagline dan logo.
- **Teks:** **GLD — Satu perangkat. Banyak gas. Jaringan yang tak terputus.**
- **VO:** "GLD: deteksi multigas berbasis kecerdasan buatan di tepi jaringan, dengan komunikasi yang memulihkan dirinya sendiri. Dikembangkan di Indonesia, untuk kilang Indonesia."

---

## 3. Pembagian kerja Blender vs Remotion

| Bagian | Alat | Catatan |
|---|---|---|
| Hero shot & exploded view GLD (Adg. 3, 8) | Blender | Pakai model CAD asli **desain terbaru** (bukan versi antena-samping yang sudah tidak dipakai). Render PNG sequence + alpha. |
| Kilang senja + efek gas (Adg. 1) | Blender | Gas = volume/displacement transparan. Alternatif cepat: b-roll Runway/Seedance (lihat §4). |
| Teks, radar chart, ikon, peta mesh, dashboard (Adg. 2, 4–7) | Remotion | Semua data-driven: `interpolate()` + `spring()`. Peta mesh = SVG dengan node dari array JSON, mudah diubah. |
| Komposisi akhir, musik, VO, subtitle | Remotion | Impor render Blender via `<OffthreadVideo>` / sequence gambar. |

Struktur Remotion yang disarankan: satu `<Composition>` 3600 frame, tiap adegan jadi `<Sequence from={…} durationInFrames={…}>` dengan komponen sendiri (`SceneHook`, `SceneProblem`, `SceneFingerprint`, `SceneTrainable`, `SceneMesh`, `SceneAlarm`, `SceneOutro`), sehingga timing tiap adegan bisa digeser tanpa membongkar yang lain.

## 4. Soal Runway / Seedance

Cocok untuk **b-roll suasana** (establishing shot kilang, pipa, senja). **Jangan dipakai untuk perangkat GLD-nya**: AI video akan "mengarang" bentuk casing dan antena, jadi produk yang tampil bukan produk asli. Perangkat tetap dari Blender/CAD atau foto asli.

## 5. Ide tambahan (opsional, jika waktu cukup)

- **Live demo cut 5 detik:** potongan video asli saat GLD disemprot LPG lalu alarm muncul di server (uji 6–8 Agu). Satu klip nyata sering lebih meyakinkan daripada animasi.
- **Counter "dari deteksi ke alarm"** di Adegan 7, **hanya** jika sudah ada angka terukur (KPI ≤30 detik baru akan diukur saat SAT).
- **Versi 30 detik** dari Adegan 4 + 6 + 8 untuk diputar berulang di booth.

## 6. Yang perlu disiapkan tim

Proyek Remotion: [`Video_Produk_GLD_Remotion/`](Video_Produk_GLD_Remotion/README.md).


1. File CAD desain casing terbaru (`.step`/`.obj`) untuk Blender.
2. ~~Screenshot dashboard aplikasi asli~~ — sudah: Alarm Console RU4 dari repo dashboard.
3. Klip video demo LPG (jika ada).
4. Izin penggunaan logo Pertamina.
5. Pengisi suara (atau TTS), serta musik bebas royalti.
