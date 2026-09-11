# Persiapan Termin 1 Sertifikasi GLD

## Kesimpulan

Status paket per 10 September 2026 adalah **BELUM SIAP DIAJUKAN sebagai bukti pemenuhan Termin 1**.

Folder sudah mempunyai bukti bahwa prototipe GLD dan enclosure fisik tersedia, dokumentasi spesifikasi awal, foto tahapan perakitan, serta pembahasan desain bersama Pertamina. Namun belum ditemukan rangkaian bukti yang mengunci syarat pembayaran Termin 1, yaitu hasil pengujian enclosure, catatan iterasi perbaikan desain berdasarkan hasil uji, witness dan validasi eksplisit oleh Pertamina, berita acara yang ditandatangani, dan laporan pekerjaan khusus Termin 1.

Angka **Kesiapan Internal Pra-Submission sekitar 42%** pada dashboard sertifikasi adalah metrik kemajuan rekayasa. Angka tersebut **bukan** bukti bahwa milestone pembayaran Termin 1 telah diterima.

## Dasar penilaian

Termin 1 pada skema dua termin mensyaratkan seluruh kondisi berikut:

1. Tersedia prototipe enclosure gas leak detector.
2. Prototipe telah diuji.
3. Hasil pengujian telah menghasilkan atau menutup iterasi perbaikan desain.
4. Pengujian dan hasil iterasi disaksikan serta divalidasi oleh Pertamina.
5. Tahap tersebut selesai sebelum pengujian dan sertifikasi di laboratorium terakreditasi internasional.
6. Pelaksanaan dituangkan dalam berita acara dan laporan pekerjaan.

## Matriks kepatuhan bukti

| No | Syarat Termin 1 | Status | Bukti yang ditemukan | Kekurangan yang harus ditutup |
|---:|---|---|---|---|
| 1 | Prototipe enclosure GLD tersedia | **Sebagian** | Tujuh foto pada `Sumber Dokumen/sertifikasi-atex-gld-v2-2026/GLD/`. Tiga foto utama menunjukkan urutan motherboard, pemasangan delapan sensor, dan unit terakit. Metadata foto utama mencatat 26 Agustus 2026. | Belum ada identitas unit, nomor seri, revisi desain, konfigurasi hardware/firmware, kondisi siap uji, dan lembar identifikasi sampel yang ditandatangani. |
| 2 | Prototipe enclosure telah diuji | **Belum terbukti** | Ada bukti pengujian fungsi sistem, dataset gas, komunikasi LoRa, dan chamber. Proposal sertifikasi juga menetapkan jenis pre-compliance test. | Tidak ditemukan protokol dan hasil uji khusus enclosure: inspeksi mekanik, termal/hotspot, sealing atau IP pra-uji, fault condition, serta fungsi sebelum dan sesudah pengujian. |
| 3 | Ada iterasi perbaikan desain | **Belum terbukti** | Ada file bernama `ATEX CASING v2` dan desain bracket U-bolt. | `ATEX CASING v2` terutama memodelkan assembly mounting/bracket dan tidak cukup sebagai riwayat iterasi enclosure. Belum ada change log Rev A ke Rev B, temuan uji, tindakan koreksi, bukti implementasi, dan hasil uji ulang. |
| 4 | Disaksikan dan divalidasi Pertamina | **Belum terbukti** | Notulen 6 Agustus dan notulen RU IV menunjukkan keterlibatan Pertamina dalam pembahasan desain, pemasangan, dan sertifikasi. | Tidak ditemukan witness sheet, daftar hadir sesi uji enclosure, pernyataan hasil diterima, komentar dan penutupan komentar, atau tanda tangan pejabat/perwakilan Pertamina. |
| 5 | Dilakukan sebelum uji laboratorium terakreditasi | **Urutan masih memungkinkan** | Status proyek per 10 September menyatakan sertifikasi masih persiapan dokumen dan belum ada klaim pengujian lab. | Sesi pre-compliance dan witness harus dijadwalkan serta ditutup sebelum sampel dikirim ke laboratorium. Tanggal booking/pengiriman sampel perlu dicatat sebagai batas waktu. |
| 6 | Ada berita acara | **Belum ada** | Notulen rapat tersedia. | Notulen pembahasan tidak sama dengan berita acara validasi hasil uji. Diperlukan berita acara khusus, hasil keputusan yang eksplisit, lampiran, dan tanda tangan para pihak. |
| 7 | Ada laporan pekerjaan | **Belum ada** | Dashboard sertifikasi dan laporan analisis kekurangan tersedia. | Kedua dokumen tersebut adalah dashboard/status dan gap analysis, bukan laporan pelaksanaan pengujian serta iterasi enclosure untuk Termin 1. |

## Bukti yang dapat dipakai sebagai lampiran pendukung

### Identitas dan foto prototipe

- `Sumber Dokumen/sertifikasi-atex-gld-v2-2026/GLD/1. Motherboard_Casing.jpg`
- `Sumber Dokumen/sertifikasi-atex-gld-v2-2026/GLD/2. Motherboard_ModulSensor_Casing.jpg`
- `Sumber Dokumen/sertifikasi-atex-gld-v2-2026/GLD/3. Motherboard_ModulSensor_PenutupMesh_Casing_Antena_ModulAlarm.jpg`
- `Sumber Dokumen/sertifikasi-atex-gld-v2-2026/GLD/Casing_Belakang.jpg`
- `Sumber Dokumen/sertifikasi-atex-gld-v2-2026/GLD/ModulAlarm.jpg`
- `Sumber Dokumen/sertifikasi-atex-gld-v2-2026/GLD/PenutupMesh_Casing.jpg`
- `Sumber Dokumen/sertifikasi-atex-gld-v2-2026/GLD/PenutupMesh.jpg`

### Desain dan spesifikasi

- `Sumber Dokumen/GLD U Bolt Bracket/ATEX CASING v2.step`
- `Sumber Dokumen/GLD U Bolt Bracket/ATEX CASING v2.obj`
- `Deliverables/Desain_Bracket_L_UBolt_GLD_Mounting.pdf`
- `Sumber Dokumen/sertifikasi-atex-gld-v2-2026/Dokumen_spesifikasi_input_2.docx`
- `Sumber Dokumen/sertifikasi-atex-gld-v2-2026/Parameter spesifikasi EMC_lengkap.docx`
- `Sumber Dokumen/Technical-Datasheets-Lab-IoT-ITB/Technical-Datasheet-GasleakDetector-ID.pdf`

### Dasar teknis pengujian

- `Sumber Dokumen/PROPOSAL SERTIFIKASI GAS LEAK DETECTION SYSTEM(Hazardous Area Compliance – ATEX, IP, EMC, RF) [21 FEB 2026].pdf`
  - Halaman 11: output redesign enclosure.
  - Halaman 12: uji termal, EMC, RF, dan IP pra-sertifikasi.
  - Halaman 15: pre-compliance, iterasi, dan pengiriman prototipe ke laboratorium.
  - Halaman 18: urutan pre-compliance sebelum pengujian resmi.

### Bukti pembahasan bersama Pertamina

- `Sumber Dokumen/Notulensi_KickOffMeeting 12 Juni 2026.pdf`
- `Deliverables/Notulen_Meeting_GLD_6Agustus2026.pdf`
- `Sumber Dokumen/Notulen_Meeting_Pertamina_RU4_Cilacap.pdf`

Dokumen di atas mendukung kronologi dan arah desain, tetapi tidak boleh diberi label sebagai witness atau acceptance apabila belum memuat keputusan penerimaan yang eksplisit dan tanda tangan pihak berwenang.

### Bukti kemajuan yang tidak boleh disamakan dengan uji enclosure

- Dataset gas pada `Dataset/`.
- `Sumber Dokumen/Test Sinyal LoRa.xlsx`.
- `Sumber Dokumen/GLD_serial_20260708T060449.log`.
- Dashboard progres, laporan field testing, dan laporan chamber.

Bukti tersebut berguna untuk menunjukkan kematangan fungsi sistem, tetapi tidak menggantikan pengujian mekanik, termal, sealing/IP, dan keselamatan enclosure yang menjadi objek Termin 1 sertifikasi.

## Paket minimum yang harus diselesaikan

### 1 Identitas prototipe dan design freeze

- Tetapkan ID sampel, misalnya `GLD-EX-P01`.
- Tetapkan revisi mekanik, revisi PCB, versi firmware, tanggal rakit, dan penanggung jawab.
- Ambil foto enam sisi, bagian internal, nameplate sementara, cable entry, seal/gasket, terminal, grounding, dan sensor cartridge.
- Buat daftar BOM aktual untuk unit yang diuji, bukan BOM rencana.
- Tetapkan drawing yang berlaku dan beri nomor dokumen serta revisi.

### 2 Protokol pengujian pra-sertifikasi

Protokol harus disetujui sebelum uji dan sekurang-kurangnya memuat:

- tujuan, ruang lingkup, lokasi, tanggal, personel, dan peran witness;
- identitas prototipe dan konfigurasi uji;
- alat ukur, nomor aset, status kalibrasi, dan ketidakpastian yang relevan;
- kondisi lingkungan;
- langkah uji dan kriteria lulus/gagal;
- inspeksi visual dan dimensi;
- uji fungsi sebelum dan sesudah;
- pengukuran suhu enclosure dan hotspot pada kondisi terburuk;
- simulasi sealing atau IP pra-uji yang dinyatakan jelas sebagai pre-compliance, bukan sertifikasi IP;
- pengujian fault condition yang aman dan disetujui;
- pre-scan EMC dan uji awal RF bila fasilitas tersedia;
- format pencatatan data mentah, foto, anomali, dan deviasi prosedur.

### 3 Log iterasi dan pengujian ulang

Setiap temuan harus mempunyai nomor, bukti, keputusan, PIC, tanggal target, revisi desain yang berubah, dan hasil retest. Jika tidak ada perubahan desain setelah uji, diperlukan disposisi formal yang menjelaskan alasan teknis dan persetujuan Pertamina; jangan mengklaim terjadi iterasi tanpa bukti.

### 4 Witness dan validasi Pertamina

- Tentukan nama dan kewenangan perwakilan Pertamina sebelum sesi uji.
- Gunakan daftar hadir dan witness sheet per pengujian.
- Catat komentar Pertamina serta status penutupannya.
- Nyatakan hasil akhir secara eksplisit: diterima, diterima dengan catatan, atau belum diterima.
- Pastikan pihak yang menandatangani memang berwenang untuk validasi milestone SPK.

### 5 Dokumen serah terima Termin 1

- Laporan pekerjaan Termin 1 dengan lampiran hasil uji dan log iterasi.
- Berita Acara Validasi Prototipe dan Hasil Pra-Uji.
- BAST Termin 1 atau format serah terima sesuai administrasi kontrak.
- Surat pengantar/tagihan dan dokumen pajak hanya setelah acceptance teknis ditandatangani.

## Kriteria keluar sebelum Termin 1 diajukan

- [ ] Satu prototipe teridentifikasi unik dan konfigurasi akhirnya terkunci.
- [ ] Drawing dan BOM aktual memiliki nomor dokumen serta revisi.
- [ ] Protokol uji disetujui sebelum pelaksanaan.
- [ ] Seluruh hasil uji memiliki data mentah, foto, dan keputusan lulus/gagal.
- [ ] Temuan dan perubahan desain dapat ditelusuri sampai hasil retest.
- [ ] Sesi uji disaksikan perwakilan Pertamina yang berwenang.
- [ ] Komentar Pertamina sudah ditutup atau dinyatakan sebagai catatan yang diterima.
- [ ] Berita acara validasi ditandatangani para pihak.
- [ ] Laporan pekerjaan Termin 1 selesai dan merujuk lampiran bukti yang sama.
- [ ] Tidak ada klaim bahwa perangkat sudah tersertifikasi atau sudah lulus laboratorium terakreditasi.

## Urutan kerja yang disarankan

1. **H-7 sampai H-5:** freeze identitas prototipe, drawing, BOM, dan protokol.
2. **H-4 sampai H-2:** dry run internal; tutup masalah keselamatan dan kesiapan alat ukur.
3. **H-1:** kirim agenda, protokol, dan daftar bukti kepada Pertamina.
4. **Hari H:** laksanakan witness test dan dokumentasikan semua deviasi.
5. **H+1 sampai H+3:** lakukan perubahan dan retest untuk temuan yang dapat ditutup cepat.
6. **H+4:** terbitkan laporan pekerjaan dan berita acara untuk review.
7. **H+5 atau setelah komentar ditutup:** tanda tangan berita acara dan proses BAST Termin 1.

## Template pendamping

- `Template_Log_Uji_dan_Iterasi_Enclosure.md`
- `Template_Berita_Acara_Validasi_Prototipe.md`
- `Template_Laporan_Pekerjaan_Termin_1.md`

