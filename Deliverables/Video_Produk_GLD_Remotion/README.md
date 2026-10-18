# Video Produk GLD — Proyek Remotion

Video penjelasan produk GLD berdurasi 2 menit untuk **Digitalization Day**. Naskah dan storyboard ada di
[`../Storyboard_Video_Produk_GLD_DigitalizationDay.md`](../Storyboard_Video_Produk_GLD_DigitalizationDay.md).

Dua versi dari satu kode (30 fps, 3600 frame = 120 dtk):

| Komposisi | Ukuran | Untuk |
|---|---|---|
| `GLD-Explainer` | 1920×1080 (landscape) | layar presentasi, YouTube |
| `GLD-Explainer-Portrait` | 1080×1920 (portrait) | HP, Instagram/TikTok/WA Story |

## Menjalankan

Butuh Node.js LTS dan Python 3 (untuk skrip di `tools/`).

```bash
npm install
npm run dev               # Remotion Studio, preview di browser
npm run render            # out/GLD_Explainer_Landscape.mp4
npm run render:portrait   # out/GLD_Explainer_Portrait.mp4
npm run render:all        # keduanya
npm run typecheck
```

Di Studio, folder **Adegan-Landscape** dan **Adegan-Portrait** berisi tiap adegan secara terpisah supaya preview lebih cepat.
Font Inter sudah dibundel di `public/fonts`, jadi render bisa dilakukan tanpa internet.

## Langkah lanjutan di PC

### 1. Narasi dengan Gemini TTS

```bash
npm run vo:export
```

Perintah ini menulis naskah per adegan ke `tts/` (`01_hook.txt` … `08_outro.txt`, berisi instruksi gaya + naskah)
dan `tts/NASKAH_LENGKAP.md`. Tempel tiap file ke Gemini TTS, lalu simpan hasilnya sebagai WAV dengan nama yang sama:

```
public/audio/vo/01_hook.wav … public/audio/vo/08_outro.wav
```

Satu file per adegan, bukan satu file panjang, supaya narasi selalu mulai tepat di awal adegannya.
Pakai suara dan instruksi gaya yang sama untuk kedelapan file agar konsisten.

```bash
npm run vo:check
```

Perintah ini membandingkan durasi tiap WAV dengan slot adegannya. Kalau ada yang **TERLALU PANJANG**, minta Gemini
membaca sedikit lebih cepat, atau perpanjang adegan itu di `src/timeline.ts` (lalu kurangi adegan lain agar total tetap
120 dtk, atau biarkan video sedikit lebih panjang). Setelah semua OK, set `VO_READY = true` di `src/assets.ts`.

Subtitle tetap tampil dari naskah di `timeline.ts`. Kalau Gemini mengubah kata, samakan teks di `timeline.ts`.
Subtitle bisa dimatikan lewat `SHOW_SUBTITLES` di `assets.ts`. Musik latar: `public/audio/music.mp3`, lalu `ready: true`.

### 2. Render Blender

Tiga adegan memakai render Blender. Buat **dua kamera** di Blender, satu landscape dan satu portrait:

| File landscape (1920×1080) | File portrait (1080×1920) | Adegan | Durasi |
|---|---|---|---|
| `public/blender/scene01_refinery.mp4` | `public/blender/portrait/scene01_refinery.mp4` | 01 Hook, kilang + kebocoran | 7 dtk |
| `public/blender/scene03_hero_exploded.mp4` | `public/blender/portrait/scene03_hero_exploded.mp4` | 03 Hero shot + exploded view | 9 dtk |
| `public/blender/scene08_outro.mp4` | `public/blender/portrait/scene08_outro.mp4` | 08 GLD terpasang, kamera mundur | 10 dtk |

- Format: MP4 H.264 (atau ProRes 4444/MOV bila butuh latar transparan), **30 fps**, durasi persis seperti tabel.
- Area aman teks. Landscape: judul di kiri atas (adegan 3: label komponen di kanan). Portrait: judul di sepertiga atas,
  label komponen dan subtitle di sepertiga bawah. Letakkan objek GLD di tengah frame.
- Model 3D: pakai CAD desain casing **terbaru** (bukan versi antena-samping lama).
- Setelah file ada, ubah `ready: false` → `true` di `src/assets.ts`, lalu selaraskan waktu label exploded view
  di `Scene03Intro.tsx` (prop `from`) dengan animasi Blender.

Selama aset belum siap, video tetap bisa dirender dan menampilkan **PLACEHOLDER** berlabel nama file yang dibutuhkan.

### 3. Aset lain

Logo LGU dan ITB (`public/images/logo_lgu.png`, `logo_itb.png`, PNG transparan), lalu `ready: true`.
Untuk logo Pertamina, tambahkan hanya kalau sudah ada izin.

Screenshot dashboard (`public/images/dashboard.png`) sudah diisi: Alarm Console dari aplikasi `ru-frontend`
di repo `RavellerH/gasleakdetectionV2-April` (RU4, data demo hasil seed, 1920×1080). Versi portrait memotong
bagian daftar alarm saja. Kalau ingin diganti dengan data nyata, ambil screenshot baru di ukuran yang sama; posisi
sorotan baris alarm diatur oleh `FIRST_ALERT` dan potongan portrait oleh `LAYOUTS.portrait.crop` di `Scene07Alarm.tsx`.

## Struktur

```
src/
  timeline.ts        ← SATU-SATUNYA tempat timing & naskah narasi (per adegan)
  assets.ts          ← aset eksternal (Blender landscape/portrait, foto, logo, audio) + flag ready / VO_READY
  layout.ts          ← useLayout(): orientasi, padding, ukuran judul, posisi subtitle
  theme.ts           ← palet (#2B5FCB + #262321) & font
  Explainer.tsx      ← komposisi 120 dtk: adegan + subtitle + narasi per adegan + musik
  Root.tsx           ← registrasi komposisi landscape & portrait
  scenes/            ← Scene01Hook … Scene08Outro (tiap adegan punya tata letak landscape & portrait)
  components/        ← SceneFrame (fade), Caption/Badge, AssetSlot, Subtitles, Icons
  data/
    fingerprints.json ← sidik jari gas dari DATASET ASLI (lihat bawah)
    mesh.ts           ← topologi node/route untuk adegan mesh (koordinat landscape; portrait diputar otomatis)
    refineryGases.ts  ← 8 gas kilang + status jujur per gas (adegan 5)
tools/
  extract_fingerprints.py
  vo.py              ← export naskah ke Gemini TTS & cek durasi WAV
tts/                 ← naskah per adegan hasil `npm run vo:export`
public/              ← aset statis (blender/, images/, audio/, fonts/)
```

## Mengubah timing atau naskah

Ubah `startSec`/`endSec`/`vo` di `src/timeline.ts`. Kedua komposisi, subtitle, dan durasi per adegan mengikuti
otomatis. Jalankan ulang `npm run vo:export` agar naskah TTS ikut terbarui.

## Data sidik jari gas (Adegan 4)

Radar chart **bukan pola karangan**. Datanya diambil dari rekaman chamber asli di `Dataset/`
(13–15 Jul 2026): Udara Bersih, LPG (rata-rata 2 sesi), dan CO₂. Respons tiap sensor =
persentil-95 tegangan dikurangi baseline; bentuk pola dinormalisasi per gas, dan besarnya pakai
skala log supaya respons kecil tidak dibesar-besarkan.

```bash
npm run fingerprints   # buat ulang src/data/fingerprints.json bila dataset bertambah
```

H₂ belum ditampilkan karena belum ada dataset H₂ di repo. Kalau rekamannya sudah ada,
tambahkan entri ke `RECORDINGS` di `tools/extract_fingerprints.py`, lalu tambahkan state di `Scene04Fingerprint.tsx`.

## Batasan klaim

Ikuti tabel klaim di storyboard. Ringkasnya, jangan menulis "deteksi semua gas", "bersertifikat ATEX",
"sudah terpasang di kilang", angka akurasi, atau waktu pemulihan rute. Label "Klasifikasi AI" hanya dipakai untuk LPG;
CO₂ ditampilkan sebagai "pola" respons sensor; status per gas di adegan 5 diatur di `refineryGases.ts`.
Topologi mesh di Adegan 6 adalah ilustrasi, bukan layout kilang sebenarnya.
