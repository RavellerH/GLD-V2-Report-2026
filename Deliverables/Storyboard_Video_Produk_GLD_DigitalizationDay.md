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

---

## 2. Storyboard per adegan

Narasi ±260 kata ≈ 120 detik dengan tempo presentasi santai.

### Adegan 1 — Hook (0:00–0:10)
- **Visual (Blender):** kilang saat senja, kamera pelan menyusuri pipa. Gelombang distorsi transparan (gas) mulai keluar dari flange, tidak terlihat jelas.
- **Teks (Remotion):** *"Gas bocor tidak terlihat."*
- **VO:** "Di kilang, kebocoran gas tidak terlihat dan tidak menunggu. Beberapa detik bisa menentukan segalanya."

### Adegan 2 — Masalah (0:10–0:22)
- **Visual (Remotion, 2D flat):** ikon detektor konvensional, masing-masing berlabel satu gas; garis kabel panjang menuju ruang kontrol, lalu di-*strike* merah.
- **VO:** "Detektor konvensional umumnya hanya untuk satu jenis gas, dan perlu kabel data panjang ke ruang kontrol. Mahal, lambat dipasang, sulit diperluas."

### Adegan 3 — Perkenalan GLD (0:22–0:35)
- **Visual (Blender):** hero shot unit GLD berputar, lalu *exploded view*: casing terbuka, terlihat papan sensor 8× MQ, ESP32-S3, modul LoRa.
- **Teks:** **GLD — Gas Leak Detection** · LAPI Ganesha Utama × ITB
- **VO:** "Kami memperkenalkan GLD: satu unit dengan delapan sensor gas, prosesor AI, dan radio LoRa dalam satu casing."

### Adegan 4 — Multi-gas: sidik jari gas (0:35–0:58) ⭐ pesan inti 1
- **Visual (Remotion):** 8 batang/kanal sensor (MQ8, MQ135, MQ3, MQ5, MQ4, MQ7, MQ6, MQ2) beranimasi menjadi **radar chart 8-sumbu**. Tiap gas membentuk pola berbeda: LPG → pola A, H₂ → pola B, udara bersih → pola kecil. Label klasifikasi muncul: `LPG ● terdeteksi`.
- **Teks:** *"8 sensor → 1 sidik jari → AI mengenali gasnya"* · badge kecil **"AI on-device"**
- **VO:** "Setiap gas meninggalkan pola unik pada delapan sensor, seperti sidik jari. Model AI yang berjalan langsung di dalam perangkat membaca pola itu dan mengenali jenis gasnya, tanpa perlu server untuk berpikir."

### Adegan 5 — Bisa diajari gas baru (0:58–1:10)
- **Visual (Remotion + foto asli):** foto gas test chamber (`scripts/assets/chamber_photos/`) → panah ke ikon "dataset" → "model" → masuk ke unit GLD. Peta kecil 6 titik RU menyala satu per satu.
- **Teks:** *"Dilatih di lokasi, sesuai gas di setiap kilang"*
- **VO:** "Dan GLD bisa terus belajar. Chamber uji portable kami bawa ke kilang, data diambil di tempat, lalu model diperbarui sesuai gas yang dibutuhkan di lokasi tersebut."

### Adegan 6 — Private Mesh LoRa (1:10–1:35) ⭐ pesan inti 2
- **Visual (Remotion, peta kilang top-down 2D):** titik-titik GLD → Cluster Head → Gateway. Paket data berupa titik cahaya yang melompat antar-node (multi-hop). Lalu satu Cluster Head "mati" (merah, berkedip), dan paket **otomatis berbelok** lewat rute lain.
- **Teks:** *"Private Mesh LoRa · tanpa internet · tanpa kabel data"* → saat failover: *"Self-healing"*
- **VO:** "Data dikirim lewat jaringan mesh LoRa privat. Setiap Cluster Head meneruskan data, lompat demi lompat, sampai ke gateway, tanpa internet dan tanpa bergantung pada jaringan IT kilang. Jika satu titik mati, data otomatis mencari jalur lain."

### Adegan 7 — Alarm otomatis (1:35–1:48)
- **Visual (Remotion):** mock dashboard (gunakan tampilan asli aplikasi bila ada screenshot) → kartu alarm merah muncul dengan lokasi area & jenis gas; ikon notifikasi.
- **VO:** "Begitu kebocoran terdeteksi, alarm langsung dikirim ke dashboard operator, lengkap dengan lokasi dan jenis gasnya."

### Adegan 8 — Penutup (1:48–2:00)
- **Visual (Blender → Remotion):** unit GLD terpasang di tiang/pipa kilang, kamera mundur memperlihatkan banyak node terhubung garis cahaya. Fade ke logo.
- **Teks:** **GLD — Satu perangkat. Banyak gas. Jaringan yang tak terputus.** · logo LGU, ITB (Pertamina hanya jika diizinkan)
- **VO:** "GLD: satu perangkat, banyak gas, jaringan yang tak terputus. Teknologi deteksi kebocoran gas dari Indonesia, untuk kilang Indonesia."

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

1. File CAD desain casing terbaru (`.step`/`.obj`) untuk Blender.
2. Screenshot/rekaman dashboard aplikasi asli.
3. Klip video demo LPG (jika ada).
4. Izin penggunaan logo Pertamina.
5. Pengisi suara (atau TTS), serta musik bebas royalti.
