# Video Produk GLD — Proyek Remotion

Video penjelasan produk GLD berdurasi 2 menit untuk **Digitalization Day**. Naskah dan storyboard ada di
[`../Storyboard_Video_Produk_GLD_DigitalizationDay.md`](../Storyboard_Video_Produk_GLD_DigitalizationDay.md).

Spesifikasi: 1920×1080, 30 fps, 3600 frame (120 dtk).

## Menjalankan

```bash
npm install
npm run dev        # Remotion Studio, preview di browser
npm run render     # hasil akhir -> out/GLD_Explainer.mp4
npm run typecheck
```

Di Studio, komposisi utamanya `GLD-Explainer`. Tiap adegan juga tersedia terpisah di folder **Adegan**
(`Scene-01-hook` … `Scene-08-outro`) supaya preview dan iterasi lebih cepat.

Font Inter sudah dibundel di `public/fonts`, jadi render bisa dilakukan tanpa internet.

## Struktur

```
src/
  timeline.ts        ← SATU-SATUNYA tempat timing & naskah narasi (per adegan)
  assets.ts          ← daftar aset eksternal (Blender, foto, logo, audio) + flag ready
  theme.ts           ← palet (#2B5FCB + #262321) & font
  Explainer.tsx      ← komposisi 120 dtk: adegan + subtitle + audio
  Root.tsx           ← registrasi komposisi
  scenes/            ← Scene01Hook … Scene08Outro
  components/        ← SceneFrame (fade), Caption/Badge, AssetSlot, Subtitles, Icons
  data/
    fingerprints.json ← sidik jari gas dari DATASET ASLI (lihat bawah)
    mesh.ts           ← topologi node/route untuk adegan mesh
    refineries.ts     ← 6 RU (rencana rollout)
tools/extract_fingerprints.py
public/              ← aset statis (blender/, images/, audio/, fonts/)
```

## Alur kerja Blender → Remotion

1. Render dari Blender ke **MP4 H.264** (atau **ProRes 4444/MOV** bila butuh latar transparan),
   1920×1080, **30 fps**, dengan durasi yang sama seperti adegannya:

   | File | Adegan | Durasi |
   |---|---|---|
   | `public/blender/scene01_refinery.mp4` | 01 Hook, kilang + kebocoran | 8 dtk |
   | `public/blender/scene03_hero_exploded.mp4` | 03 Hero shot + exploded view | 10 dtk |
   | `public/blender/scene08_outro.mp4` | 08 GLD terpasang, kamera mundur | 10 dtk |

2. Di `src/assets.ts`, ubah `ready: false` menjadi `true` untuk aset tersebut.
3. Selaraskan waktu label exploded view di `Scene03Intro.tsx` (prop `from`) dengan render Blender.

Selama aset belum siap, video tetap bisa dirender dan menampilkan **PLACEHOLDER** berlabel nama file yang dibutuhkan.

Screenshot dashboard (`public/images/dashboard.png`) sudah diisi: Alarm Console dari aplikasi `ru-frontend`
di repo `RavellerH/gasleakdetectionV2-April` (RU4, data demo hasil seed, 1920×1080). Kalau ingin diganti dengan
tampilan data nyata, ambil screenshot baru di ukuran yang sama; posisi sorotan baris alarm diatur oleh `FIRST_ALERT`
di `Scene07Alarm.tsx`.

Aset lain yang ditunggu (semuanya di `assets.ts`): logo LGU & ITB,
rekaman narasi, dan musik. Untuk logo Pertamina, tambahkan hanya kalau sudah ada izin.

## Mengubah timing atau naskah

Cukup ubah `startSec`/`endSec`/`vo` di `src/timeline.ts`. Komposisi, subtitle, dan durasi per adegan
mengikuti otomatis. Kalau narasi sudah direkam, cocokkan detik di sini dengan rekamannya.
Subtitle dapat dimatikan lewat `SHOW_SUBTITLES` di `assets.ts`.

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
"sudah terpasang di kilang", atau angka akurasi. Label "Klasifikasi AI" hanya dipakai untuk LPG;
CO₂ ditampilkan sebagai "pola" respons sensor. Topologi mesh di Adegan 6 adalah ilustrasi,
bukan layout kilang sebenarnya.
