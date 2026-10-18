# Prompt Seedance — b-roll video GLD

Seedance **hanya untuk b-roll suasana kilang**. Perangkat GLD, chamber, dan dashboard tetap dari Blender/Remotion,
karena AI video mengarang bentuk produk.

Aturan umum (sudah dimasukkan ke tiap prompt):
- Tanpa teks, logo, merek, atau seragam berlogo (tidak boleh ada logo Pertamina/perusahaan lain).
- Tanpa orang yang wajahnya terlihat.
- Tanpa api, ledakan, atau kesan kecelakaan (video untuk klien; cukup kesan risiko tak kasatmata).
- Latar agak gelap supaya teks putih Remotion terbaca.
- Generate 10 dtk, potong sesuai slot di Remotion. Buat versi **16:9** dan **9:16**.

Simpan hasil di `public/broll/` lalu kabari supaya disambungkan ke adegan.

---

## B1 — Hook: kilang senja, kebocoran tak kasatmata (Adegan 1, slot 8 dtk)

File: `public/broll/b1_hook.mp4` · `public/broll/portrait/b1_hook.mp4`

```
Cinematic slow dolly shot along a large oil refinery pipe rack at dusk. Dense steel pipes, valves and bolted flanges in the foreground, distillation columns and stacks silhouetted against a deep orange and blue sky. Warm sodium lights starting to glow. From one bolted flange, a barely visible transparent heat-haze shimmer leaks out, subtle refraction distortion only, no smoke, no color. Camera moves slowly and steadily, shallow depth of field, photorealistic, 35mm lens, moody industrial atmosphere. No people, no text, no logos, no fire.
```
Komposisi: kosongkan **kiri-tengah** (16:9) / **sepertiga atas** (9:16) untuk teks.

## B2 — Masalah: kabel panjang ke ruang kontrol (Adegan 2, opsional, slot 13 dtk)

File: `public/broll/b2_cables.mp4`

```
Slow tracking shot following long industrial cable trays running along a refinery pipe rack into the distance toward a distant control building, overcast evening light, steel structures, many cables bundled in trays, sense of long distance and complexity. Photorealistic, muted colors, slightly dark, 50mm lens. No people, no text, no logos.
```

## B3 — Mesh LoRa: kilang dari udara saat blue hour (Adegan 6, slot 32 dtk, dipakai sebagai latar peta mesh)

File: `public/broll/b3_aerial.mp4`

```
High aerial drone shot slowly orbiting over a large oil refinery at blue hour. Tank farms, process units and pipe racks spread across the frame, scattered warm lights, dark blue sky, calm and stable camera motion, top-down three-quarter angle, photorealistic, wide lens, slightly dark exposure so overlays remain readable. No people, no text, no logos, no fire, no smoke plumes.
```
Remotion akan menaruh node & garis mesh di atasnya, jadi gerak kamera harus pelan dan rata.

## B4 — Penutup: latar kilang malam (Adegan 8, slot 14 dtk, latar di belakang render GLD Blender)

File: `public/broll/b4_outro_bg.mp4`

```
Static wide shot of an oil refinery at night with soft bokeh lights, pipe racks and columns softly out of focus, gentle atmospheric haze, deep blue and amber tones, very slow push-in, photorealistic, dark lower third. No people, no text, no logos, no fire.
```

---

## Jangan dibuat dengan Seedance

| Bagian | Alasan | Sumber |
|---|---|---|
| Unit GLD (hero, exploded, terpasang) | Bentuk produk harus sesuai desain terdaftar | Blender `blender/gld_v2.blend` |
| Gas test chamber | Peralatan nyata, bentuk harus sesuai laporan chamber | Blender |
| Dashboard / alarm | Harus screenshot aplikasi asli | Remotion |
| Klaim teknis apa pun | AI video tidak bisa jadi bukti | — |
