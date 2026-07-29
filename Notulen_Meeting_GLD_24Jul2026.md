# Notulen Meeting: Gas Leak Detector Development

## Informasi Meeting
| | |
|---|---|
| **Tanggal** | 24 Juli 2026 |
| **Waktu** | 09:32 – 11:00 WIB |
| **Project** | Gas Leak Detector (GLD) — Real Testing & Certification |
| **Peserta (LGU)** | Pak Muhammad, Pak Farhan, Ilma, Fahmi, Beni |
| **Peserta (Pertamina)** | Pak Sena, Pak Maman, Pak Adit, Mas Roni, Mas Indra (RU Cilacap) |

## Agenda Meeting
- Progress update pengembangan Gas Leak Detector (GLD)
- Status sertifikasi perangkat
- Persiapan field testing di RU Cilacap
- Review teknis: sensor, jaringan, dan aplikasi manajemen
- Koordinasi jadwal dan persyaratan instalasi

## Ringkasan Pembahasan

### 1. Status Pengembangan dan Sertifikasi

**Versi 24V (Power Supply)**
- Status: Sudah selesai dan siap sertifikasi
- Proses administratif sertifikasi sudah disiapkan
- Akan menggunakan jasa biro sertifikasi di Shanghai

**Versi Battery**
- Status: Masih dalam pengembangan
- Tantangan utama: Konsumsi daya sensor MQ ~10W (1A total untuk 8 sensor)
- Target: Reduce konsumsi arus menjadi <100mA
- Lifetime battery: Sedang dioptimasi untuk mencapai minimal 30 hari
- Desain baru: Berpotensi mencapai lifetime 6-8 bulan dengan rechargeable battery

### 2. Teknologi dan Fitur

**Sensor Detection**
- Menggunakan teknologi fusi dari 8 sensor MQ
- Gas yang dapat dideteksi: H₂, LPG, Metana, CO₂, Clean Air
- Model CNN 1D dengan akurasi 97.6%
- Setiap unit GLD harus di-training khusus untuk gas yang akan dideteksi

**Networking (LoRa Mesh)**
- Topologi: GLD → Cluster Head (CH) → Gateway → Server
- Self-healing mesh network dengan automatic failover
- Sudah diuji hingga 3 hop-list dengan latency <5 detik (normal), 5-15 detik (kondisi ramai)
- Cluster Head: Konsumsi ~10W, sudah stabil 20 hari non-stop dengan solar panel

**Aplikasi Manajemen**
- Tools untuk konfigurasi Gateway, Cluster Head, dan GLD sensor
- Monitoring real-time: status koneksi, kekuatan sinyal (RSSI/SNR), heat map deteksi gas
- Fitur: remote re-calibration, alarm notification, data logging

### 3. Persiapan Field Testing - RU Cilacap

**Rencana Kunjungan**
- Target: Akhir Juli 2026 (survey) → September 2026 (instalasi)
- Perubahan strategi: Survey dan instalasi dalam 1 kunjungan (jika memungkinkan)
- Tujuan survey: Mapping area, penentuan posisi sensor/CH/Gateway, analisis coverage

**Persyaratan Administratif**
- Izin visitor (max 3 hari) untuk survey awal
- Izin kerja dan surat masuk barang untuk instalasi
- Dokumen HSE: APD (hindari warna merah), template dari RU Cilacap
- Koordinasi dengan tim HSE RU Cilacap wajib dilakukan

**Deployment Plan**
- Deploy 2 sistem paralel: Server lokal RU + Cloud untuk perbandingan performa
- Tools portable untuk mapping sinyal LoRa sudah disiapkan
- Test chamber portable akan dibawa untuk on-site calibration

### 4. Pengembangan Tambahan

**Flame Detection (Camera-based)**
- Status: Model sudah develop dengan akurasi 79% (belum optimal)
- Hardware: Jetson Nano (sudah dibeli)
- Dataset: Dari Google, menggunakan kamera infrared
- Rencana: Sourcing kamera di China saat perjalanan sertifikasi

> ⚠️ **Catatan internal:** fitur ini ditahan dari deliverable resmi (dashboard/laporan) — konsisten dengan keputusan sebelumnya untuk tidak memasukkan fitur berbasis kamera/thermal (OGI) yang belum disetujui. Lihat `memory/decisions.md`.

**Integrasi Sensor Arah Angin**
- Akan ditambahkan untuk early warning system
- Tujuan: Prediksi dispersi gas dan flame spread untuk emergency response

### 5. Feedback dan Diskusi Teknis
- Pertamina request: Frekuensi pengiriman data perlu disesuaikan dengan aspek keamanan
- Benchmark IoT monitoring: Lifetime battery 5 tahun dengan transmisi 2x/hari
- User experience: Sistem harus plug-and-play dengan minimal manual configuration
- Network management: Default configuration harus sudah optimal, manual tuning hanya untuk edge cases

## Action Items / Daftar Tugas

| No | Task Description | PIC | Deadline | Status |
|---|---|---|---|---|
| 1 | Optimasi konsumsi daya battery version (<100mA) dan testing lifetime minimal 30 hari | Tim LGU (Pak Muhammad) | 15 Aug 2026 | In Progress |
| 2 | Finalisasi desain baru battery version dengan target lifetime 6-8 bulan | Tim LGU | 15 Aug 2026 | In Progress |
| 3 | Sewa ulang tabung gas Hidrogen (H₂) untuk proses training/learning model GLD | Pak Farhan | 5 Aug 2026 | Pending |
| 4 | Verifikasi dan konfirmasi gas detection capability: H₂, LPG, Metana, CO₂, Clean Air (minimum 6 kelas) | Pak Farhan, Ilma | 10 Aug 2026 | In Progress |
| 5 | Testing multi-sensor simultan pada jaringan LoRa Mesh (stress test) | Beni, Fahmi | 10 Aug 2026 | In Progress |
| 6 | Implementasi mekanisme retry/recovery untuk data alarm yang hilang saat transmisi | Beni | 15 Aug 2026 | Not Started |
| 7 | Upload progress report dan timeline ke cloud platform (share login ke Pertamina) | Pak Farhan | 31 Jul 2026 | Pending |
| 8 | Persiapan VPS kecil untuk deployment cloud-based monitoring system | Pak Muhammad | 20 Aug 2026 | Not Started |
| 9 | Penyempurnaan aplikasi manajemen: default configuration optimization (plug-and-play) | Fahmi | 20 Aug 2026 | In Progress |
| 10 | Koordinasi jadwal survey ke RU Cilacap dengan Pak Maman/Pak Adit/Tim HSE | Pak Sena (Pertamina) | 31 Jul 2026 | Pending |
| 11 | Share template dokumen perizinan (izin kerja, surat masuk barang, HSE) dari RU Cilacap | Pak Maman (Pertamina) | 31 Jul 2026 | Pending |
| 12 | Persiapan dokumen HSE dan perizinan masuk kilang (termasuk CS Negara) | Tim LGU (Pak Muhammad) | 15 Aug 2026 | Not Started |
| 13 | Pengadaan APD dengan warna non-merah untuk tim LGU | Pak Farhan | 10 Aug 2026 | Pending |
| 14 | Persiapan tools portable untuk mapping sinyal LoRa di lapangan | Pak Farhan | 20 Aug 2026 | Ready |
| 15 | Persiapan test chamber portable dan tabung gas untuk on-site testing | Tim LGU | 20 Aug 2026 | In Progress |
| 16 | Komunikasi aktif di WhatsApp Group dengan tim Instrumen & Merchant Insurance Pertamina untuk technical feedback | All Parties | Ongoing | In Progress |
| 17 | Persiapan perjalanan ke China: sertifikasi (Shanghai) + sourcing kamera flame detection (Wuhan) | Pak Muhammad | TBD (setelah battery version ready) | On Hold |
| 18 | Meeting persiapan pre-deployment dengan tim RU Cilacap (RAP meeting) | Pak Sena, Pak Maman, Tim LGU | 15 Aug 2026 | Not Started |

## Keputusan Meeting
1. Deployment di RU Cilacap akan menggunakan strategi dual system: server lokal + cloud untuk evaluasi performa
2. Survey dan instalasi akan digabung dalam 1 kunjungan jika memungkinkan (target: September 2026)
3. Gas detection capability minimum: H₂, LPG, Metana, CO₂, Clean Air (6 kelas) harus dipastikan sebelum deployment
4. Battery version development akan dilanjutkan paralel, tidak menghambat deployment versi 24V
5. Koordinasi dengan tim HSE RU Cilacap wajib dilakukan sejak awal untuk menghindari rejection

## Risiko dan Mitigasi

| Risiko | Mitigasi |
|---|---|
| Battery lifetime tidak mencapai target minimal (30 hari) | Lanjutkan deployment dengan versi 24V (power supply); Battery version sebagai fase development berikutnya |
| Perizinan masuk kilang terlambat/ditolak | Koordinasi early dengan tim HSE dan PIC RU Cilacap; Persiapan dokumen lengkap jauh-jauh hari |
| Coverage area LoRa Mesh tidak optimal di lapangan | Survey mendalam dengan tools mapping sinyal; Penambahan Cluster Head jika diperlukan |
| Data alarm hilang saat transmisi | Implementasi retry mechanism dan local buffering; Monitoring heartbeat untuk deteksi koneksi loss |

## Next Meeting
- **Agenda:** RAP Meeting persiapan deployment RU Cilacap
- **Peserta:** Tim LGU + Tim RU Cilacap (termasuk HSE, Instrumen, Operasi)
- **Target:** 15 Agustus 2026

## Catatan Penting
- Koordinasi melalui WhatsApp Group harus lebih aktif untuk feedback teknis
- Progress report harus dapat diakses secara real-time oleh Pertamina
- Setiap perubahan scope atau timeline harus dikomunikasikan segera
