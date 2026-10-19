# Panduan Demo Dashboard GLD — Digitalization Day

Status: **siap latihan** (19 Okt 2026, diperbarui: peta tanpa token, riwayat 7 hari, tema Pertamina). Semua data di demo adalah **DATA SIMULASI** dan diberi label begitu di layar.

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
5. Mengulang dari awal (mis. setelah latihan): **tutup dulu semua jendela demo** (Backend, Dashboard, Broker, Skenario), lalu jalankan ulang `start-demo.bat` (database direset otomatis). Kalau jendela Backend lama masih terbuka, launcher berhenti dengan pesan — tutup jendelanya lalu ulangi.

## Cara menjalankan B

Buka `Demo_Dashboard_GLD.html` di Chrome/Edge. Tombol **Langkah berikutnya** atau panah kanan / spasi. **Putar otomatis** menjalankan kelima langkah sendiri (±80 detik).

## Yang sudah tersedia di dashboard demo (A)

- **Map View tanpa token**: peta MapLibre. Basemap diambil dari tile lokal (`public/tiles`, diunduh otomatis oleh `start-demo.bat` saat pertama kali ada internet), atau OSM online, atau latar polos sesuai tema bila offline total. Perangkat, garis topologi, dan panel tren 24 jam tetap tampil di ketiga kondisi.
- **Heatmap & Analytics terisi**: `reset-db.js` membuat riwayat simulasi 7 hari (udara bersih tiap 10 menit per GLD) + 3 kejadian lampau yang sudah diselesaikan operator (H2 di GLD 3 lima hari lalu, alarm LPG di GLD 1 dua hari lalu, LPG MIDDLE di GLD 2 enam jam lalu). Grafik 24 jam dan 7 hari, heatmap, dan log kejadian langsung berisi saat demo dibuka.
- **Tema terang & gelap berpalet Pertamina Patra Niaga** (biru, merah, hijau logo) + logo di sidebar dan halaman login. Ganti tema dengan tombol **Terang/Gelap** di header (juga ada di halaman login dan di HTML mandiri); pilihan diingat browser.

## Menampilkan peta dengan benar

- **Peta jalan (OSM)** tampil otomatis bila laptop terhubung internet. Jalankan `start-demo.bat` sekali dengan internet: tile peta RU4 diunduh dan setelah itu peta tetap tampil **offline**.
- **Citra satelit**: klik tombol **PETA** di kanan atas peta (berubah jadi **SATELIT**). Hanya bisa online; tampil dengan atribusi Esri.
- **Taruh sensor di posisi sebenarnya** sebelum hari H: geser pin tiap perangkat di Map View, lalu jalankan `node save-positions.js` di folder `demo\digitalization-day`. Posisi disimpan dan dipakai lagi setiap demo direset. Koordinat bawaan hanya contoh di sekitar titik tengah RU4, jadi tanpa langkah ini pin bisa tampak di lokasi yang salah di peta asli.

## Yang perlu dicek sebelum hari H

- [ ] Jalankan `start-demo.bat` sekali **saat ada internet** supaya tile peta RU4 terunduh (±560 tile). Setelah itu peta bisa offline. Tanpa itu, peta tetap jalan tapi latarnya polos.
- [ ] Kolom **Signal** GLD tampil −100 dBm / Weak. Node-RED belum mengirim RSSI per GLD, jadi nilainya belum ada. Jangan disorot.
- [ ] Coba sekali penuh di laptop yang dipakai di lokasi.
- [ ] Untuk tim video: `screenshots/` berisi 14 tangkapan per langkah skenario, `screenshots/tema_peta_analytics/` berisi 10 tangkapan peta, Analytics 24 jam/7 hari, dan tema terang/gelap (2400×1350). Peta di tangkapan ini berlatar polos karena dibuat tanpa akses tile.

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
