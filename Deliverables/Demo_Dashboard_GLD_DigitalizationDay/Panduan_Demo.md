# Panduan Demo Dashboard GLD — Digitalization Day

Status: **siap latihan** (19 Okt 2026). Semua data di demo adalah **DATA SIMULASI** dan diberi label begitu di layar.

Ada dua cara mendemokan skenario yang sama. Pilih sesuai kondisi di lokasi.

| | A. Dashboard asli (aplikasi RU) | B. HTML mandiri |
|---|---|---|
| Apa | Backend + dashboard RU sungguhan, data masuk lewat MQTT seperti dari Node-RED | Satu file HTML yang memutar skenario |
| Butuh | Laptop dengan Node.js, repo `gasleakdetectionV2-April`, ±3 menit build pertama | Browser saja, bisa offline |
| Kelebihan | Membuktikan aplikasinya sendiri bekerja | Paling aman di panggung, tidak ada yang bisa gagal start |
| File | `demo/digitalization-day/start-demo.bat` (repo aplikasi) | `Demo_Dashboard_GLD.html` (folder ini) |
| Link | `http://localhost:3002` | Artifact: https://claude.ai/artifact/M6A7UFevy3X9qFPacFeDVe (privat, perlu dibagikan dulu lewat menu Share) |

Saran: tampilkan **A** bila laptop sudah dicoba di lokasi; siapkan **B** di tab lain sebagai cadangan.

## Skenario (5 langkah, ±2 menit)

Selaras dengan adegan 6–7 video (`../Video_Produk_GLD_Remotion/`).

| # | Langkah | Yang terjadi di layar | Aksi presenter |
|---|---|---|---|
| 1 | Operasi normal | 10 perangkat online, 3 GLD = Udara bersih | Buka Overview / Devices |
| 2 | Indikasi awal LPG di GLD 2 | GLD 2: LPG 74 %, risiko MIDDLE, peringatan kuning | Buka Alerts |
| 3 | Alarm: kebocoran LPG dikonfirmasi | GLD 2: LPG 93 %, alarm push CRITICAL | Klik **Acknowledge** / **Tindak lanjuti** |
| 4 | Gangguan jaringan: CH 2 mati | CH 2 OFFLINE (±20 dtk di dashboard asli), GLD 2 & CH 5 dialihkan lewat CH 3 | Buka Devices / Unit Layout |
| 5 | Pulih | GLD 2 kembali Udara bersih, CH 2 online | Klik **Resolve** / **Selesaikan** |

Naskah narasi tiap langkah tampil di jendela skenario (A) dan di bilah atas halaman (B).

## Cara menjalankan A (Windows)

1. Clone/pull repo `RavellerH/gasleakdetectionV2-April`.
2. Dobel-klik `demo\digitalization-day\start-demo.bat`. Pertama kali: install + build ±3 menit.
3. Browser terbuka ke `http://localhost:3002`. Login **demo@gld.local / demo-gld-2026** (akun lokal database demo).
4. Di jendela **GLD Demo - Skenario**: tekan **Enter** untuk langkah berikutnya, angka **1–5** untuk loncat.
5. Mengulang dari awal (mis. setelah latihan): tutup semua jendela, jalankan ulang `start-demo.bat` (database direset otomatis).

## Cara menjalankan B

Buka `Demo_Dashboard_GLD.html` di Chrome/Edge. Tombol **Langkah berikutnya** atau panah kanan / spasi. **Putar otomatis** menjalankan kelima langkah sendiri (±80 detik).

## Yang perlu dicek sebelum hari H

- [ ] **Peta (Map View) dashboard asli butuh token Mapbox dan internet.** Tanpa token, tab Map View menampilkan pesan "Set NEXT_PUBLIC_MAPBOX_TOKEN". Hindari tab ini atau isi token di `apps/ru-frontend/.env.local` sebelum build. Tab lain tidak butuh internet.
- [ ] Kolom **Signal** GLD tampil −100 dBm / Weak. Node-RED belum mengirim RSSI per GLD, jadi nilainya belum ada. Jangan disorot.
- [ ] Coba sekali penuh di laptop yang dipakai di lokasi.
- [ ] Untuk tim video: `screenshots/` berisi 14 tangkapan dashboard asli per langkah (2400×1350).

## Screenshot

| File | Langkah |
|---|---|
| `1a-normal-overview.png`, `1b-normal-devices.png`, `1c-normal-unit-layout.png` | 1 |
| `2a-indikasi-devices.png`, `2b-indikasi-alerts.png` | 2 |
| `3a-alarm-alerts.png`, `3b-alarm-overview.png`, `3c-alarm-acknowledged.png`, `3d-alarm-events.png` | 3 |
| `4a-ch2-offline-devices.png`, `4b-ch2-offline-unit-layout.png` | 4 |
| `5a-pulih-alerts.png`, `5b-pulih-devices.png`, `5c-pulih-overview.png` | 5 |

## Batasan yang perlu disampaikan jujur bila ditanya

- Data simulasi, bukan data lapangan RU IV (instalasi lapangan belum berjalan).
- Waktu dipercepat: data normal tiap 5 dtk (A) / 2 dtk (B), lapangan ±90 dtk; alarm tiap 3 dtk (A) / 2 dtk (B), lapangan ±10 dtk.
- Waktu dari deteksi sampai alarm di dashboard belum diukur resmi (KPI ≤30 dtk diukur saat SAT).
