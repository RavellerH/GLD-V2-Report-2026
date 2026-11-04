# Konten Brosur GLD — A4, 4 Halaman (Versi Visual)

**Untuk:** brosur/katalog produk umum (pengunjung pameran, manajemen, mitra, direksi)
**Format:** A4 portrait, 4 halaman, kertas katalog
**Prinsip:** **±70% gambar/simulasi, ±30% teks.** Setiap halaman punya satu visual besar sebagai cerita utama. Teks dibatasi pada judul, satu kalimat penjelas, dan label pendek pada gambar.
**Revisi:** v2, 4 November 2026 (menggantikan versi teks-padat)

---

## Panduan umum

**Hierarki merek:** Pertamina Patra Niaga paling besar, lalu nama produk GLD. Logo Korporasi Kinarya ITB dan LAPI Ganesha Utama kecil di kaki halaman dengan teks "Dikembangkan bersama".

**Warna:** biru tua #12357A, biru #2B5FCB, aksen merah #E3242B dan hijau #8DC63F, latar putih.

**Gaya visual (pakai untuk semua gambar agar seragam):**
`clean 3D product visualization, Pertamina corporate colors (deep blue, red, lime green on white), soft studio lighting, industrial refinery context, high detail, no text in image`

**Ciri unit GLD asli (sertakan di setiap prompt yang memuat GLD):**
`blue die-cast aluminium explosion-proof style housing with four mounting lugs, round stainless steel mesh window on the front, red dome beacon on a short stainless cylinder at the side, short black antenna on top, silver cylindrical sensor head at the bottom, mounted with a flat square plate and two U-bolts on a 2-inch galvanized pole`

Lampirkan foto asli sebagai referensi bila tool-nya mendukung:
- Unit GLD: `scripts/assets/cert_doc_photos/3._Motherboard_ModulSensor_PenutupMesh_Casing_Antena_ModulAlarm.jpg`
- Chamber: `scripts/assets/chamber_photos/chamber_gld_terpasang.jpeg`
- Cluster Head: `scripts/assets/ch_mount_photos/ch_bracket_solar_detail.jpg`
- Dashboard: `Deliverables/Video_Produk_GLD_Remotion/public/images/dashboard.png`
- Logo: `Sumber Dokumen/Logo/`

> **Catatan:** AI hampir selalu salah menggambar logo dan tulisan. Buat gambar **tanpa teks**, lalu tambahkan logo dan label di tool layout.

---

## HALAMAN 1 — Sampul: "Mengenali Jenis Gas, Bukan Sekadar Mendeteksinya"

**Komposisi:** satu gambar penuh (full-bleed) unit GLD di kilang saat senja. Logo Pertamina Patra Niaga di kiri atas. Judul besar di sepertiga kiri.

**Visual utama — prompt:**
```
Hero shot of an industrial gas leak detector mounted on a short galvanized pole in the
foreground of an oil refinery at dusk, [ciri unit GLD], refinery towers and pipe racks
softly out of focus behind it, faint glowing blue wireless signal waves radiating from
the antenna toward a distant small solar-powered relay node, deep blue twilight sky with
warm refinery lights, cinematic low angle, shallow depth of field, clean empty space on
the left third for a headline, no text
```

**Teks:**
- Label kecil: MULTI-MODALITY · AI ON THE EDGE · LORA MESH
- Judul: **GLD**
- Sub-judul: Multi-Modality Gas Leak Detector
- Tagline: *Mengenali jenis gas, bukan sekadar mendeteksinya.*

**Strip ikon di bawah gambar (4 ikon + angka, tanpa kalimat):**
| Ikon | Angka | Label |
|---|---|---|
| 8 lingkaran sensor | **8** | sensor dalam satu unit |
| chip / otak | **< 166 ms** | AI di perangkat |
| target / centang | **99,31%** | akurasi uji lab |
| gelombang radio | **LoRa Mesh** | nirkabel terenkripsi |

**Kaki:** "Dikembangkan bersama" + logo Kinarya ITB + logo LGU (kecil)

---

## HALAMAN 2 — Simulasi: "Dari Kebocoran ke Dashboard dalam Hitungan Detik"

**Komposisi:** **storyboard 4 panel** (2 × 2 atau satu baris memanjang) sebagai simulasi kejadian. Setiap panel hanya diberi nomor dan satu baris keterangan.

**Panel 1 — Kebocoran terjadi**
```
Isometric 3D illustration of a refinery pipe flange with a small visible gas leak plume
(soft semi-transparent orange-yellow vapour cloud) drifting toward an industrial gas leak
detector on a pole a few meters away, [ciri unit GLD], clean stylized refinery
environment, Pertamina corporate colors, no text
```
Keterangan: **1 · Gas bocor terbawa angin ke arah GLD**

**Panel 2 — GLD menghirup dan mengenali**
```
Cutaway 3D illustration of the same gas detector: vapour particles drawn in through the
round stainless steel mesh by a small fan, eight small cylindrical gas sensors inside glow
in different colours as they react, a small glowing AI chip next to them, clean technical
visualization, transparent housing effect, no text
```
Keterangan: **2 · 8 sensor bereaksi, AI mengenali jenis gas dalam < 1 detik**

**Panel 3 — Data melompat lewat jaringan mesh**
```
Isometric 3D map of a refinery site seen from above, several gas detectors at process
areas, solar-powered relay nodes on poles along the perimeter fence, glowing blue data
pulses hopping from detector to relay to relay toward a control building with a rooftop
antenna, one alternative route highlighted, Pertamina corporate colors, no text
```
Keterangan: **3 · Data terenkripsi melompat antar Cluster Head menuju Gateway**

**Panel 4 — Alarm di ruang kontrol**
```
Modern refinery control room, an operator looking at a large wall screen showing a dark
blue monitoring dashboard with a site map and one sensor marker flashing red, an alert
card popping up, calm professional atmosphere, Pertamina corporate colors, no readable
text on screen
```
Keterangan: **4 · Dashboard menampilkan jenis gas, lokasi, dan tingkat keyakinan**

> Tempel tangkapan layar dashboard asli di layar panel 4 agar sesuai kenyataan.

**Teks penutup halaman (satu kalimat, di bawah storyboard):**
Berjalan mandiri sebagai lapisan pemantauan tambahan, tanpa mengubah sistem deteksi gas dan kontrol yang sudah ada.

---

## HALAMAN 3 — Produk: "Kenali Komponennya"

**Komposisi:** setengah atas berisi **exploded view GLD** dengan 5 label penunjuk. Setengah bawah berisi **3 kartu foto** komponen jaringan.

**Visual utama — exploded view, prompt:**
```
Exploded view 3D technical illustration of an industrial gas detector, parts floating
apart along a vertical axis on a clean white background: front cover with round stainless
steel mesh, eight small cylindrical gas sensors on a round sensor board, a main circuit
board with a processor chip and LoRa radio module, a small cooling fan, blue die-cast
aluminium housing body, red dome beacon, black antenna, silver sensor head at the bottom,
thin leader lines space for callouts, soft studio lighting, no text
```

**5 label penunjuk (pendek):**
1. **Mesh stainless** — udara masuk, partikel tertahan
2. **8 sensor gas** — satu "sidik jari" untuk tiap jenis gas
3. **AI di perangkat** — klasifikasi langsung tanpa server
4. **Radio LoRa** — kirim data nirkabel terenkripsi
5. **Beacon alarm** — tanda visual di lapangan

**3 kartu foto komponen jaringan (foto asli + 1 baris):**
| Kartu | Gambar | Keterangan |
|---|---|---|
| Cluster Head | foto CH dengan 2 panel surya | Penghubung nirkabel bertenaga surya, tanpa kabel listrik |
| Gateway | render antena omni di atap ruang kontrol | Pintu data ke jaringan lokal, didukung UPS |
| Dashboard | tangkapan layar dashboard asli | Status perangkat, alarm, dan riwayat deteksi |

Prompt pendukung untuk kartu Gateway (bila tidak ada foto):
```
Slim white omni-directional antenna on a short mast on the flat roof of a refinery control
building, coaxial cable running down the wall, clear blue sky, clean industrial look, no text
```

**Strip spesifikasi kunci (ikon kecil, satu baris):**
24 VDC · ±8 W · LoRa 920–923 MHz · AES-128 · RS-485 Modbus · IP66 (target) · pemasangan U-bolt tiang 2"

---

## HALAMAN 4 — Teruji & Terus Belajar

**Komposisi:** tiga blok visual: (A) foto chamber dengan infografis melingkar, (B) peta Indonesia dengan titik 6 RU, (C) baris lencana hasil uji dan sertifikasi.

### Blok A — "AI yang belajar dari lokasinya"
**Visual:** foto chamber uji gas asli di tengah, dikelilingi **siklus 4 langkah berbentuk lingkaran** (ikon + 2–3 kata):
1. Chamber dibawa ke kilang
2. Ambil data gas setempat
3. Latih model AI
4. Pasang ke GLD

Prompt pendukung (bila ingin render, bukan foto):
```
Tall transparent clear acrylic gas test chamber on a white table, aluminium back plate
inside with a blue industrial gas detector mounted at the center and a silver cylindrical
sensor head below it, black square fan on the chamber floor, small gas tubing and valve on
the side, a laptop beside it showing a live sensor graph, clean bright lab setting, no text
```

Satu kalimat: *Gas target pengembangan, seperti H₂S, metana, CO dan benzena, ditambahkan sesuai kebutuhan tiap lokasi.*

### Blok B — "Menuju 6 Refinery Unit"
**Visual:** peta Indonesia sederhana (gaya flat, biru muda) dengan 6 titik: RU II Dumai, RU III Plaju, RU IV Cilacap, RU V Balikpapan, RU VI Balongan, RU VII Kasim.

Prompt pendukung:
```
Minimal flat vector map of Indonesia in light blue on white, six glowing location pins
with small radiating signal rings, clean corporate infographic style, no text
```

Label pada titik (opsional): jumlah unit per RU. GLD · CH · GW: RU II 10·3·1, RU III 4·3·1, RU IV 3·2·1, RU V 2·1·1, RU VI 4·2·2, RU VII 5·11·1.
*Gunakan hanya bila angka alokasi sudah final.*

### Blok C — Lencana (badge)
**Sudah teruji di laboratorium (ikon centang hijau):**
- Sistem end-to-end GLD → Server
- Akurasi model 99,31%
- Mesh 8 Cluster Head, 3 lompatan
- Push alarm otomatis
- FAT laboratorium 7/7 lulus

**Dalam proses sertifikasi (ikon jam/kuning):**
- ATEX / IECEx
- IP66 / IP67
- EMC
- Radio SDPPI

**Kaki:** "Dikembangkan bersama" + logo Kinarya ITB + logo LGU (kecil)

---

## Daftar visual yang perlu dibuat

| No | Halaman | Visual | Sumber |
|---|---|---|---|
| V1 | 1 | Hero GLD di kilang saat senja | Generate (prompt hal. 1) + foto GLD sbg referensi |
| V2 | 2 | Panel 1: kebocoran gas | Generate |
| V3 | 2 | Panel 2: cutaway GLD, sensor menyala | Generate |
| V4 | 2 | Panel 3: peta isometrik jaringan mesh | Generate |
| V5 | 2 | Panel 4: ruang kontrol + dashboard | Generate + tempel screenshot asli |
| V6 | 3 | Exploded view GLD | Generate + foto GLD sbg referensi |
| V7 | 3 | Foto Cluster Head | Foto asli |
| V8 | 3 | Antena Gateway di atap | Foto asli atau generate |
| V9 | 3 | Dashboard | Screenshot asli |
| V10 | 4 | Chamber uji gas | Foto asli (atau generate) |
| V11 | 4 | Peta Indonesia 6 RU | Generate / vektor |
| — | semua | Ikon (sensor, chip, radio, centang, jam) | Pustaka ikon tool desain |

---

## Hal yang sengaja TIDAK dicantumkan

| Jangan tampilkan | Alasan |
|---|---|
| "Bersertifikat ATEX" / logo Ex sebagai klaim | Sertifikasi masih dalam proses |
| Angka ppm/%LEL di layar dashboard simulasi | GLD mengeluarkan label jenis gas + confidence, bukan konsentrasi |
| H₂S / benzena sebagai kemampuan saat ini | Masih gas target pengembangan; model saat ini: udara bersih, LPG, H₂ |
| "Menggantikan detektor yang ada" | GLD adalah lapisan tambahan |
| Nomor kontrak, anggaran, titik pemasangan spesifik | Bukan materi umum |

> Di panel simulasi 1–4, kebocoran digambarkan sebagai "gas" secara umum. Hindari label "H₂S" pada awan gas.
