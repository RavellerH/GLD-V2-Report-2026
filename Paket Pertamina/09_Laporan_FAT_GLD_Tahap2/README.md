# Laporan Factory Acceptance Test (FAT) — Sistem GLD Tahap 2 (4 Oktober 2026)

Paket laporan FAT beserta lampiran bukti dan 3 laporan uji lab formal (lampiran 7–9), untuk pengajuan Termin 1 Field Testing (SPK: "laporan factory acceptance test"). Nomor lampiran sama dengan tabel "Lampiran — Daftar bukti" di laporan.

> **File gabungan (satu PDF):** `Laporan_FAT_GLD_Tahap2_Lengkap_dengan_Lampiran.pdf` — diawali halaman depan format laporan LGU (cover, kontrol dokumen, lembar pengesahan, kata pengantar, daftar isi), lalu Laporan FAT + lampiran 1–9 berurutan dengan halaman pemisah dan bookmark (129 hlm, ±5,5 MB). File-file di bawah adalah versi terpisahnya.

| File | Isi | Item FAT |
|---|---|---|
| `00_Laporan_FAT_GLD_Tahap2.pdf` | Laporan FAT rev 1.4: 7 item uji (tujuan, prosedur, kriteria lulus, hasil, bukti) + lembar pengesahan 3 pihak | — |
| `Lampiran_01_Notulen_Rapat_Witness_6Agustus2026.pdf` | Notulen rapat di Lab IoT ITB, 6 Agustus 2026, dihadiri PT Pertamina Patra Niaga (witness) | Witness, FAT-06, FAT-07 |
| `Lampiran_02_Hasil_Uji_Model_AI_CNN_DualBranch.pdf` / `.pptx` | Dataset pengembangan (LPG, CO₂, udara bersih): akurasi uji 99,73%, INT8 99,20%; uji real-time di perangkat (H2, udara bersih) 97,65% (slide 4, 8–10) | FAT-01, FAT-02 |
| `Lampiran_03_Uji_Sinyal_LoRa.pdf` / `.xlsx` | RSSI, SNR, dan PDR per titik uji di kampus ITB | FAT-03 |
| `Lampiran_04_Kutipan_Uji_CH_Failover_LoRa_Mesh_Downlink.pdf` | Kutipan 30 halaman dari catatan kerja Lab IoT ITB (Apr–Jul 2026): uji CH & failover, baseline LoRa, mesh 8 CH, downlink. Nomor halaman asal tercantum di tiap halaman | FAT-03, FAT-04, FAT-05 |
| `Lampiran_05_Technical_Datasheet_Rev4.0/` | 5 Technical Datasheet Rev 4.0 Lab IoT ITB (Whole System, Gas Leak Detector, CH, Gateway, Server) | FAT-02 (label model di perangkat), FAT-05, FAT-06, konfigurasi |
| `Lampiran_06_Foto_Unit_GLD_Terakit.jpg` | Foto unit GLD terakit | Perangkat uji |
| `Lampiran_07_Laporan_Uji_Lab_01_Model_AI.pdf` | Laporan uji lab formal: dataset, akurasi uji, kuantisasi INT8, uji real-time di perangkat | FAT-01, FAT-02 |
| `Lampiran_08_Laporan_Uji_Lab_02_Komunikasi_LoRa.pdf` | Laporan uji lab formal: RSSI, SNR, PDR per jarak dan kondisi lingkungan | FAT-03 |
| `Lampiran_09_Laporan_Uji_Lab_03_Mesh_Integrasi.pdf` | Laporan uji lab formal: mesh otomatis, failover, mesh 8 CH, downlink, end-to-end, alarm | FAT-04 s.d. FAT-07 |

File zip: `../09_Laporan_FAT_GLD_Tahap2.zip` (isi sama dengan folder ini).

## Rev 1.4 (4 Oktober 2026) — penegasan untuk evaluasi Termin 1

- **FAT-02**: validasi model pada dataset pengembangan (LPG, CO₂, udara bersih; 99,73% / INT8 99,20%) dipisahkan dari uji real-time di perangkat (label Clean Air, LPG, H2 sesuai Technical Datasheet Rev 4.0, 4 Sep 2026; 97,65%).
- **FAT-03**: kriteria lulus dinyatakan terukur (PDR 100% pada link jalur pandang bebas + batas jangkauan per hop teridentifikasi); jarak STEI diseragamkan 201 m.
- **FAT-06**: kriteria = alarm otomatis tanpa permintaan data. Waktu respons tidak diukur dengan pencatat waktu pada uji lab; pengukuran terhadap KPI ≤30 detik dilakukan pada SAT.
- **FAT-07**: masukan tampilan dari rapat 6 Agustus ditegaskan di luar kriteria FAT-07.
- Bagian 2 menyebut unit yang dipakai dalam uji; label "Draf" diganti "Untuk Pengesahan"; Lampiran 4 dipersempit jadi kutipan halaman bukti.
- Kata Pengantar menegaskan: Lembar Pengesahan depan = pengesahan dokumen; Lembar Pengesahan Uji (Bagian 5) = penerimaan hasil uji.
