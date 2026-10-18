# Handoff — Video Produk GLD (Digitalization Day)

Dokumen ini untuk melanjutkan pekerjaan di PC yang punya **Blender** dan akses **Gemini TTS**.
Status per **18 Okt 2026**. Semua kode sudah ada di branch `main`.

---

## 1. Status saat ini

| Bagian | Status |
|---|---|
| Storyboard + naskah narasi formal-akademis | ✅ Selesai (`../Storyboard_Video_Produk_GLD_DigitalizationDay.md`) |
| Proyek Remotion, 8 adegan, ±151 dtk | ✅ Selesai, render penuh sudah diuji |
| Versi landscape 1920×1080 (`GLD-Explainer`) | ✅ Tata letak selesai |
| Versi portrait/HP 1080×1920 (`GLD-Explainer-Portrait`) | ✅ Tata letak selesai |
| Radar sidik jari gas (data chamber asli) | ✅ Selesai |
| Screenshot dashboard RU4 asli (adegan 7) | ✅ Terpasang (data demo) |
| **Render Blender: 4 shot × 2 orientasi** | ⏳ **Belum**: masih PLACEHOLDER |
| **Narasi Gemini TTS: 8 file WAV** | 🔶 **4/8** (01–04, suara Erinome); 05–08 menunggu kuota |
| Logo LGU & ITB | ⏳ Belum |
| Musik latar | ⏳ Opsional |
| Render final kedua versi | ⏳ Setelah semua di atas |

Draf tanpa Blender & suara bisa dirender kapan saja. Adegan yang belum punya aset menampilkan PLACEHOLDER berlabel.

---

## 2. Setup di PC (sekali saja)

1. Install **Node.js LTS** (https://nodejs.org) dan **Python 3**.
2. Ambil repo:
   ```bash
   git clone https://github.com/RavellerH/GLD-V2-Report-2026.git
   cd GLD-V2-Report-2026/Deliverables/Video_Produk_GLD_Remotion
   npm install
   ```
   (Kalau repo sudah ada: `git checkout main && git pull`.)
3. Cek berjalan:
   ```bash
   npm run dev
   ```
   Browser terbuka ke Remotion Studio. Pilih `GLD-Explainer` atau `GLD-Explainer-Portrait`.
   Saat render pertama kali, Remotion mengunduh Chrome headless sendiri (butuh internet sekali).

---

## 3. Urutan kerja yang disarankan

1. **Narasi dulu** (§4). Durasi suara menentukan apakah timing adegan perlu digeser, dan itu memengaruhi panjang render Blender.
2. Jalankan `npm run vo:check`. Kalau ada yang perlu digeser, ubah `src/timeline.ts`, lalu **catat durasi final tiap adegan**.
3. **Render Blender** (§5) dengan durasi final tersebut.
4. Logo & musik (§6).
5. Render final kedua versi (§7) dan cek daftar periksa (§8).

---

## 4. Narasi — Gemini TTS

Naskah per adegan sudah ada di `tts/01_hook.txt` … `tts/08_outro.txt`. Tiap file berisi instruksi gaya baca + naskahnya.
Ringkasan semuanya ada di `tts/NASKAH_LENGKAP.md`. Kalau naskah di `src/timeline.ts` diubah, jalankan ulang `npm run vo:export`.

**Cara utama (otomatis, 1 panggilan API):**
```bash
npm run vo:generate
```
Kedelapan naskah dikirim dalam **satu** request (suara Erinome), rekaman utuh disimpan di `public/audio/vo/_full.wav`,
lalu otomatis dipotong per adegan di 7 jeda terpanjang dan langsung dicek durasinya. Key dibaca dari file `env` di root repo.
Kalau potongan meleset, coba `npm run vo:split` (tanpa API) atau generate ulang.

**Cara manual (AI Studio):**
1. Pilih **satu suara** Gemini TTS (nada formal, tenang). Pakai suara dan instruksi gaya yang sama untuk kedelapan file.
2. Tempel isi tiap `tts/NN_xxx.txt`, generate, lalu simpan sebagai **WAV**:
   ```
   public/audio/vo/01_hook.wav
   public/audio/vo/02_problem.wav
   public/audio/vo/03_intro.wav
   public/audio/vo/04_fingerprint.wav
   public/audio/vo/05_trainable.wav
   public/audio/vo/06_mesh.wav
   public/audio/vo/07_alarm.wav
   public/audio/vo/08_outro.wav
   ```
3. Cek durasi:
   ```bash
   npm run vo:check
   ```
   Tiap file harus ≤ (durasi adegan − 0,5 dtk). Kalau **TERLALU PANJANG**: generate ulang dengan instruksi "tempo sedikit lebih cepat",
   atau perpanjang adegan di `src/timeline.ts` (`startSec`/`endSec`, adegan sesudahnya ikut digeser).
4. Kalau semua OK, buka `src/assets.ts` dan set `VO_READY = true`.
5. Kalau Gemini membaca kata berbeda dari naskah, samakan teks `vo` di `src/timeline.ts`, karena subtitle diambil dari situ.

Slot durasi saat ini:

| # | Adegan | Detik | Slot | Narasi Erinome |
|---|---|---|---|---|
| 01 | Hook | 0–8 | 8 dtk | 7,3 dtk ✅ |
| 02 | Masalah | 8–21 | 13 dtk | 11,7 dtk ✅ |
| 03 | Perkenalan GLD | 21–32 | 11 dtk | 10,5 dtk ✅ |
| 04 | Sidik jari gas & model AI | 32–72 | 40 dtk | 38,6 dtk ✅ |
| 05 | Gas kilang & chamber | 72–92 | 20 dtk | estimasi, belum direkam |
| 06 | Private mesh LoRa | 92–124 | 32 dtk | estimasi, belum direkam |
| 07 | Alarm | 124–137 | 13 dtk | estimasi, belum direkam |
| 08 | Penutup | 137–151 | 14 dtk | estimasi, belum direkam |

Suara terpilih: **Erinome** (Gemini TTS, `gemini-2.5-flash-preview-tts`). Slot diperpanjang mengikuti narasi (18 Okt), total ±151 dtk.
Slot 05–08 masih estimasi; setelah WAV-nya ada, jalankan `npm run vo:check` dan sesuaikan.
Kuota gratis: 3 permintaan/menit, 10/hari.

---

## 5. Render Blender

### 5.1 Ketentuan umum

- **Dua kamera per shot**: landscape dan portrait. Objek utama di tengah frame.
- **30 fps**, durasi **persis** sesuai slot adegan (cek ulang setelah langkah narasi).
- Format: MP4 H.264. ProRes 4444/MOV hanya kalau butuh latar transparan.
- Warna aksen proyek: biru `#2B5FCB`, charcoal `#262321`, oranye gas `#F5A524`. Latar gelap, supaya teks putih Remotion terbaca.
- Teks/label **tidak** dibuat di Blender. Semua teks ditambahkan Remotion, jadi sisakan area kosong sesuai keterangan tiap shot.
- Setelah file ada, ubah `ready: false` → `true` di `src/assets.ts` untuk aset tersebut.

### 5.2 Model 3D GLD: perhatikan posisi antena

- Geometri casing tersedia di `Sumber Dokumen/GLD U Bolt Bracket/ATEX CASING v2.obj` (+ `.mtl`, `.step` dalam mm) dan gambar berdimensi `Sumber Dokumen/GLD CASE ATEX V3.pdf`.
- ⚠️ **CAD v2 dan v3 masih menaruh antena di samping. Unit produksi sekarang antenanya di muka ATAS base.** Gambar antena samping sudah disembunyikan dari dokumen sertifikasi. Jangan tampilkan versi antena samping di video.
- Acuan bentuk unit terbaru: foto di `Sumber Dokumen/Foto_Assembly_GLD_07Okt2026/` (mis. `Antenna_interface_outside.jpg`, `IMG_14.*.jpg`). Pakai CAD v2 sebagai dasar, pindahkan antena ke atas sesuai foto.
- Mounting: pelat datar 250×250 mm dengan U-bolt ke pipa 2" (bukan bracket siku/L). Acuan: `GLD U-Bolt Bracket V2.png` dan render 6 sisi (`atas/bawah/depan/belakang/kiri/kanan.png`) di folder yang sama.
- Isi untuk exploded view (referensi internal): papan sensor dengan 8 sensor gas (seri MQ), main board (ESP32-S3), ADC (ADS1256), modul radio LoRa + antena.
- ⚠️ **Jangan tampilkan nama/seri produk komponen.** Tulisan, logo, dan nomor seri pada chip/sensor/modul (mis. cetakan "MQ-x", logo Espressif) harus dihilangkan atau dibuat tidak terbaca di render. Video hanya menyebut spesifikasi. Detail PCB: `Sumber Dokumen/EasyEDA Source/` (ada model 3D PCB).

### 5.3 Daftar shot

| Aset | File landscape (1920×1080) | File portrait (1080×1920) | Durasi |
|---|---|---|---|
| Hook: kilang | `public/blender/scene01_refinery.mp4` | `public/blender/portrait/scene01_refinery.mp4` | 8 dtk |
| Hero + exploded GLD | `public/blender/scene03_hero_exploded.mp4` | `public/blender/portrait/scene03_hero_exploded.mp4` | 11 dtk |
| Gas test chamber | `public/blender/scene05_chamber.mp4` | `public/blender/portrait/scene05_chamber.mp4` | 20 dtk (estimasi) |
| Penutup | `public/blender/scene08_outro.mp4` | `public/blender/portrait/scene08_outro.mp4` | 14 dtk (estimasi) |

**Shot 1 — Hook (Adegan 1, 8 dtk).** Kilang saat senja, kamera pelan menyusuri pipa. Gas keluar dari flange sebagai distorsi transparan yang nyaris tak terlihat.
Area teks: landscape **kiri-tengah**, portrait **sepertiga atas**. Jangan taruh objek penting di sana.

**Shot 2 — Hero + exploded view (Adegan 3, 11 dtk).**
- 0–4 dtk: unit GLD berputar pelan (turntable).
- 4–11 dtk: casing terbuka/exploded, memperlihatkan 4 komponen. Label Remotion muncul pada detik **4,0 · 4,7 · 5,3 · 6,0** berurutan:
  (1) 8 sensor gas semikonduktor oksida logam, (2) akuisisi data presisi 24-bit, (3) prosesor AI dual-core 240 MHz, (4) radio LoRa 920 MHz.
  Kalau timing animasi berbeda, ubah prop `from` di `src/scenes/Scene03Intro.tsx` (frame = detik × 30).
- Area teks: judul di **kiri atas**. Label komponen di **kanan** (landscape) atau **sepertiga bawah** (portrait). Letakkan unit di tengah-kiri (landscape) / tengah (portrait).

**Shot 3 — Gas test chamber (Adegan 5, 20 dtk, estimasi).** Menggantikan foto chamber yang kurang informatif.
- Ukuran tampil di layar: kotak **640×420** (landscape) dan **952×380** (portrait), memakai *object-fit: cover*. Render di 1920×1080 dan 1080×1920 tetap boleh, tapi **komposisi objek harus muat di tengah** dengan rasio ±3:2 (landscape) / ±5:2 (portrait).
- Model chamber, dengan acuan `Sumber Dokumen/LAPORAN PROGRESS CHAMBER GAS.pdf` (Gambar 2 tampak samping/depan, Gambar 3 diagram blok, Gambar 4–5 rangkaian):
  kotak akrilik bening, unit GLD di dalam, tabung gas uji + **solenoid valve** di jalur masuk, **pompa hisap** di jalur buang,
  2 sensor suhu/tekanan/kelembapan (satu di dalam, satu di luar), 1 sensor gas acuan di dalam, panel kontrol (mikrokontroler, regulator, driver pompa, kipas pendingin).
  Referensi internal: BME280 ×2, TGS2610, ESP32, LM2596, BTS7960. Sama seperti GLD, nama/logo komponen tidak boleh terbaca di render.
- **Sorot komponen berurutan** (glow/outline biru `#2B5FCB`), selaras dengan legenda bernomor di Remotion:

  | Detik | # | Sorot |
  |---|---|---|
  | 0,5 | 1 | Tabung gas + solenoid valve (gas mengalir masuk) |
  | 3,0 | 2 | Ruang uji akrilik + unit GLD |
  | 5,5 | 3 | Sensor acuan suhu, tekanan, kelembapan & gas |
  | 8,0 | 4 | Pompa hisap (udara keluar, pembilasan) |
  | 10–20 | – | Kamera mundur pelan, semua komponen terlihat |

  Kalau detik berbeda, ubah `CHAMBER_PARTS[].at` di `src/scenes/Scene05Trainable.tsx`.

**Shot 4 — Penutup (Adegan 8, 14 dtk, estimasi).** GLD terpasang di pipa kilang dengan pelat U-bolt, lalu kamera mundur memperlihatkan beberapa node yang terhubung garis cahaya (mesh).
Area teks: **sepertiga bawah** (tagline + logo). Bagian bawah frame akan digelapkan gradasi oleh Remotion.

---

## 6. Logo & musik

- `public/images/logo_lgu.png`, `public/images/logo_itb.png`: PNG transparan, lalu `ready: true` di `src/assets.ts`.
- Logo Pertamina **hanya kalau sudah ada izin** dari klien.
- Musik: `public/audio/music.mp3` (bebas royalti), lalu `ready: true`. Volume diatur 0,18 di `src/Explainer.tsx`.

---

## 7. Render final

```bash
npm run typecheck
npm run render:all
```

Hasil:
- `out/GLD_Explainer_Landscape.mp4`: layar presentasi.
- `out/GLD_Explainer_Portrait.mp4`: HP / media sosial.

Untuk mempercepat iterasi, render satu adegan saja dari Studio (folder **Adegan-Landscape** / **Adegan-Portrait**),
atau draf setengah resolusi: `npx remotion render GLD-Explainer out/draft.mp4 --scale=0.5`.

---

## 8. Daftar periksa sebelum tayang

- [ ] Kedelapan WAV ada, `npm run vo:check` semua OK, `VO_READY = true`.
- [ ] Subtitle sama dengan ucapan narasi.
- [ ] Tidak ada PLACEHOLDER tersisa (cek kedua versi).
- [ ] Antena GLD di render Blender ada di **atas**, bukan di samping.
- [ ] Tidak ada nama/seri/logo produk komponen yang terbaca (layar, narasi, render Blender).
- [ ] Label exploded view (adegan 3) dan sorotan chamber (adegan 5) muncul bersamaan dengan animasi Blender.
- [ ] Versi portrait: teks tidak tertutup area tombol aplikasi HP (bawah ±220 px).
- [ ] Logo Pertamina hanya dipakai kalau sudah diizinkan.
- [ ] Klaim aman (lihat §9).

---

## 9. Batasan klaim (wajib)

Video ini akan ditonton pihak Pertamina, jadi klaim harus sesuai bukti:

| ✅ Boleh | ❌ Jangan |
|---|---|
| 8 sensor gas dalam satu unit; AI on-device | "Mendeteksi semua gas" |
| Spesifikasi: sensor semikonduktor oksida logam, akuisisi 24-bit, prosesor AI dual-core 240 MHz | Nama/seri produk komponen (MQ…, ESP32, ADS1256, BME280, TGS…) di layar, narasi, atau render |
| Model mengenali udara bersih, LPG, H₂ | "Mendeteksi CH₄/CO/NH₃/benzena" sebagai kemampuan saat ini (statusnya target pelatihan) |
| H₂S: "perlu sensor tambahan" (tak ada sensor khusus H₂S) | Klaim deteksi H₂S |
| CNN dua cabang, kuantisasi int8 | Angka akurasi (masih direkonsiliasi) |
| Mesh LoRa multi-hop, failover diuji 8 CH di kampus ITB | Pemulihan rute "seketika" / dalam X detik (belum diukur) |
| Alarm push teruji di lab | "Sudah terpasang / beroperasi di kilang" |
| Sertifikasi ATEX sedang berjalan (kalau disebut) | "Bersertifikat ATEX" |

Status per gas diatur di `src/data/refineryGases.ts`. Ubah hanya kalau ada bukti baru, misalnya data uji metana.

---

## 10. Peta file penting

| File | Isi |
|---|---|
| `src/timeline.ts` | Timing & naskah per adegan (sumber tunggal) |
| `src/assets.ts` | Daftar aset + flag `ready`, `VO_READY`, `SHOW_SUBTITLES` |
| `src/layout.ts` | Logika landscape vs portrait |
| `src/scenes/Scene0N*.tsx` | Tiap adegan (tata letak kedua orientasi) |
| `src/data/refineryGases.ts` | 8 gas kilang & statusnya |
| `src/data/fingerprints.json` | Sidik jari gas dari `Dataset/` (via `tools/extract_fingerprints.py`) |
| `src/data/mesh.ts` | Topologi mesh ilustrasi |
| `tools/vo.py` | `export` naskah TTS & `check` durasi WAV |
| `tts/` | Naskah siap tempel ke Gemini TTS |
| `README.md` | Dokumentasi teknis proyek |
| `../Storyboard_Video_Produk_GLD_DigitalizationDay.md` | Storyboard, dasar teknis narasi, poin tanya-jawab |

Sumber data: screenshot dashboard dari repo `RavellerH/gasleakdetectionV2-April` (aplikasi `ru-frontend`, RU4, data demo);
parameter mesh dari Technical Datasheet Rev 4.0; arsitektur model dari presentasi model 6 Agu.

---

## 11. Saran lanjutan (opsional)

- **Screenshot dashboard versi HP**: buka dashboard di ukuran layar ponsel, simpan, lalu pakai khusus untuk komposisi portrait (tulisan lebih terbaca).
- **Data uji metana**: kalau sudah ada rekaman dari board, status CH₄ bisa naik ke "data chamber terkumpul" dan polanya ditambahkan ke radar chart (`tools/extract_fingerprints.py`).
- **Klip demo nyata 5 dtk** (semprot LPG → alarm muncul) bisa disisipkan di adegan 7.
