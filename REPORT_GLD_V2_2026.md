# 📋 LAPORAN LENGKAP PROYEK GAS LEAK DETECTION (GLD) V2 2026

**Proyek:** Gas Leak Detection System untuk PT Pertamina (Persero)  
**Periode:** Juni – Juli 2026  
**Tim Pelaksana:** LAPI Ganesha Utama (LGU) · Lab Fisika & Lab IoT ITB · PT Pertamina  

---

## 📌 Daftar Isi

1. [Ringkasan Proyek](#1-ringkasan-proyek)
2. [Struktur Repositori](#2-struktur-repositori)
3. [Analisis Dataset](#3-analisis-dataset)
4. [Capaian & Temuan Utama](#4-capaian--temuan-utama)
5. [Isu Kritis & Risiko](#5-isu-kritis--risiko)
6. [Rekomendasi Tindak Lanjut](#6-rekomendasi-tindak-lanjut)
7. [Data Pendukung](#7-data-pendukung)

---

## 1. Ringkasan Proyek

### 1.1 Tujuan
Sistem deteksi kebocoran gas berbasis sensor MQ multi-sensor dengan komunikasi LoRa dan kecerdasan buatan untuk monitoring area Refinery Unit (RU) Pertamina.

### 1.2 Komponen Utama

| Komponen | Spesifikasi |
|----------|-------------|
| **Sensor** | 8 sensor MQ (MQ2, MQ3, MQ4, MQ5, MQ6, MQ7, MQ8, MQ135) |
| **MCU** | ESP32 dengan modul LoRa |
| **Konektivitas** | LoRa (long-range) dengan Cluster Head (CH) |
| **Catu Daya** | Solar Panel + Baterai 3.7V |
| **AI/ML** | Temporal CNN (TCNN) untuk deteksi pola gas |
| **Target** | Deteksi gas LPG, Metana, CO₂, O₂, dan gas lainnya |

### 1.3 Arsitektur Sistem

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   GLD Sensor    │────▶│  Cluster Head    │────▶│    Gateway      │
│   Unit (8 MQ)   │ LoRa│  (CH) - High     │ LoRa│    (GW)         │
└─────────────────┘     │  Position        │     └────────┬────────┘
                        └──────────────────┘              │
                                                          ▼
                                                ┌─────────────────┐
                                                │   Server/Cloud  │
                                                │   (Dashboard)   │
                                                └─────────────────┘
```

---

## 2. Struktur Repositori

```
GLD-V2-Report-2026/
├── 📊 Dataset/                          # Data sensor CSV
│   ├── gld_F001_20260713_063648.csv     # Baseline data
│   ├── gld_F001_20260715_034213.csv     # Data testing
│   ├── gld_F001_20260715_035005 - [CLEAN AIR].csv  # Udara bersih
│   ├── gld_F001_20260715_041830 - [LPG].csv        # Deteksi LPG
│   ├── gld_F001_20260715_075226_OKSIGEN.csv        # Deteksi Oksigen
│   └── gld_F001_20260715_075820_CARBON DIOXIDE.csv # Deteksi CO₂
│
├── 📄 Dokumen & Laporan
│   ├── Laporan_Progres_GLD_18Jun-20Jul.md     # Laporan progres
│   ├── Notulensi_KickOffMeeting 12 Juni 2026.pdf  # Notulensi rapat
│   ├── mom_ruiv_cilacap_gld.pdf               # MOM RU IV Cilacap
│   └── Kebutuhan_Peralatan_GLD_per_RU_v2.pdf  # Kebutuhan peralatan
│
├── 📊 Presentasi & Presentasi
│   ├── Deck Presentasi GLD KICKOFF MEETING - BPUDL Template.pdf
│   ├── Cadangan AI Kick of meeting.pptx
│   ├── Deteksi_Gas_CNN_Presentasi.pptx
│   ├── TCN_GasLPG_Presentation (2).pptx
│   ├── Board12_TCN_PerSensor.pptx
│   └── Timeline_Kerjaan_Mingguan_GLD.pptx
│
├── 🔧 Hardware & Desain
│   ├── POLE-BRACKET-GLD-CH-SOLAR.pdf.pdf    # Desain bracket
│   ├── Urutan ADS,.jpeg                      # Diagram ADS
│   ├── Urutan Channel MCP.jpeg               # Diagram MCP
│   └── Test Sinyal LoRa.xlsx                 # Hasil uji LoRa
│
├── 📈 Dashboard
│   └── Dashboard_GLD_ProjectManagement.html   # Dashboard monitoring
│
├── 📝 Log & Data
│   └── GLD_serial_20260708T060449.log        # Log serial
│
└── 📄 README.md                              # Dokumentasi repository
```

---

## 3. Analisis Dataset

### 3.1 Format Data
Dataset tersimpan dalam format CSV dengan struktur:

| Kolom | Deskripsi | Satuan |
|-------|-----------|--------|
| `timestamp_ms` | Waktu dalam milidetik | ms |
| `wall_time` | Waktu absolut (ISO 8601) | UTC |
| `voltage_MQ2` - `voltage_MQ135` | Tegangan sensor MQ | V |

### 3.2 Data Tersedia

| File | Jenis Gas | Jumlah Sampel | Durasi |
|------|-----------|---------------|--------|
| `[CLEAN AIR].csv` | Udara Bersih (Baseline) | 400+ | ~3 menit |
| `[LPG].csv` | LPG | 2400+ | ~15 menit |
| `_OKSIGEN.csv` | Oksigen (O₂) | - | - |
| `_CARBON DIOXIDE.csv` | Karbon Dioksida (CO₂) | - | - |

### 3.3 Karakteristik Sensor

**Urutan channel MCP (sesuai diagram):**
1. MQ8 (Hidrogen)
2. MQ135 (Gas Udara/Kualitas Udara)
3. MQ3 (Alkohol)
4. MQ5 (LPG/Alam)
5. MQ4 (Metana)
6. MQ7 (Karbon Monoksida)
7. MQ6 (LPG/Alam)
8. MQ2 (Gas Umum/LPG)

**Temuan Penting:**
- **Baseline berbeda** antar sensor (MQ135 lebih sensitif dari MQ8)
- **Threshold harus per MQ**, tidak seragam
- **Redundansi sensor** meningkatkan kepercayaan deteksi

### 3.4 Pola Respons Gas

| Gas | Sensor Dominan | Pola Respons |
|-----|----------------|--------------|
| **LPG** | MQ5, MQ6 | Peningkatan signifikan |
| **Metana** | MQ4 | Peningkatan moderat |
| **CO₂** | Semua sensor | Korelasi positif (respons seragam) |
| **O₂** | - | Tidak korelasi (mekanisme penggantian gas) |
| **Alkohol** | MQ3 | Peningkatan spesifik |

---

## 4. Capaian & Temuan Utama

### 4.1 Jaringan LoRa & Cluster Head

✅ **Capaian:**
- Uji coba komunikasi 2 CH berhasil dilaksanakan
- Prinsip desain CH ditempatkan **setinggi mungkin** telah dirumuskan
- Karakterisasi PDR (Packet Delivery Ratio) terhadap jarak, sudut, dan tinggi antena

⚠️ **Temuan Kritis:**
- **Antena LoRa 6m hanya mencapai ±100m** (belum optimal)
- Perlu eksperimen untuk menentukan **jumlah CH minimum**

### 4.2 Pengembangan AI & Sensor Fusion

✅ **Capaian:**
- Pergeseran paradigma dari deteksi biner ke **fingerprint multi-sensor**
- Pengembangan model **Temporal CNN (TCNN)** dengan prediksi 5 detik ke depan

| Pendekatan Lama | Pendekatan Baru |
|-----------------|-----------------|
| Analisis per sensor individual | Fingerprint gabungan 8 sensor |
| Grafik per MQ | Grafik **per jenis gas** |
| Fokus amplitudo absolut | Fokus **pola/relatif** |
| Output biner gas/no-gas | Mempertimbangkan fase transien & saturasi |

### 4.3 Sistem Catu Daya

✅ **Capaian:**
- Profil beban daya GLD terukur: **8 sensor MQ ≈ 5,8–6W @ 5V**
- Skema duty cycling tersimulasi: **ON 60s / OFF 100s, interval WAKE 160s**
- Data solar-baterai terkumpul 10 hari

| Parameter | Nilai |
|-----------|-------|
| Durasi ON (setelah WAKE + boot) | 60 detik |
| Durasi OFF | 100 detik |
| Interval pulsa WAKE | 160 detik |

⚠️ **Isu Kritis:**
- **Mode baterai hanya menghasilkan ~2,43W** vs kebutuhan ~6W
- **DC converter perlu diganti/dimodifikasi**

### 4.4 Gas Test Chamber & QC

✅ **Capaian:**
- Mahasiswa PJ chamber telah didapatkan (6 Juli)
- Sambungan, selang, dan komponen terpasang di dinding chamber
- Metode aliran gas (sedot vs dorong) perlu diuji

### 4.5 Perangkat Lunak

✅ **Capaian:**
- Aplikasi UI GLD dengan antarmuka per sensor
- Fitur capture, save, download dataset
- Koneksi USB untuk pembangunan model langsung di PC

---

## 5. Isu Kritis & Risiko

### 5.1 Isu Prioritas Tinggi

| No | Isu | Dampak | Prioritas |
|----|-----|--------|-----------|
| 1 | **Mode baterai belum terbukti menyuplai 8 heater MQ penuh** (2,43W vs 6W) | GLD tidak dapat beroperasi mandiri di lapangan | 🔴 **Tinggi** |
| 2 | **Circuit DC converter perlu diganti/dimodifikasi** | Menahan finalisasi desain catu daya | 🔴 **Tinggi** |
| 3 | **Jangkauan antena LoRa 6m hanya ±100m** | Berpotensi meningkatkan jumlah CH signifikan | 🔴 **Tinggi** |
| 4 | **Ketidakkonsistenan akuisisi data** | Kualitas dataset pelatihan AI | 🔴 **Tinggi** |

### 5.2 Isu Prioritas Sedang

| No | Isu | Dampak | Prioritas |
|----|-----|--------|-----------|
| 5 | Data solar-baterai baru 10 hari (min. 1 bulan) | Belum cukup validasi energy budget | 🟡 **Sedang** |
| 6 | Dokumen JSA/TRA belum dikonfirmasi | Menahan jadwal site visit | 🟡 **Sedang** |
| 7 | Izin pemasangan CH Labtek XV lt.8 belum diperoleh | Menahan eksperimen jaringan | 🟡 **Sedang** |
| 8 | Keputusan solder vs soket belum diambil | Dampak strategi maintenance | 🟡 **Sedang** |

---

## 6. Rekomendasi Tindak Lanjut

### 6.1 Action Items

| No | Tindakan | Penanggung Jawab | Status |
|----|----------|------------------|--------|
| 1 | Ganti/modifikasi circuit DC converter | Tim Elektronik (Fahmi) | 🔴 Terbuka |
| 2 | Pengukuran ulang beban mode baterai + data tegangan | Fahmi | 🔴 Terbuka |
| 3 | Eksperimen stabilitas CH di posisi tinggi → CH1 Labtek XV | Tim Jaringan | 🔴 Terbuka |
| 4 | Eksperimen jumlah CH minimum (tanpa sensor) | Tim Jaringan | 🔴 Terbuka |
| 5 | Investigasi akar penyebab ketidakkonsistenan data | Tim GLD & AI | 🔴 Terbuka |
| 6 | Penetapan threshold per MQ berbasis baseline | Tim GLD & AI | 🔴 Terbuka |
| 7 | Pemetaan MQ dominan per jenis gas (datasheet) | Tim GLD & AI | 🟡 Berjalan |
| 8 | Replot grafik per jenis gas (8 parameter) | Tim GLD & AI | 🔴 Terbuka |
| 9 | Pengembangan model TCNN (prediksi 5s) | Pak Fahdzi | 🟡 Berjalan |
| 10 | Penyelesaian gas test chamber (pompa, valve) | Mahasiswa PJ Chamber | 🟡 Berjalan |
| 11 | Uji metode aliran gas: sedot vs dorong | Tim Chamber | 🔴 Terbuka |
| 12 | Melanjutkan pengumpulan data solar (10/30 hari) | Lab IoT (Ryan) | 🟡 Berjalan |
| 13 | Pindahkan titik pengecasan ke rooftop | Ilmania / Lab Fisika | 🔴 Terbuka |
| 14 | Konsolidasi repositori menjadi satu repo utama | Farhan Budiman | 🔴 Terencana |
| 15 | Tambahkan collaborator GitHub dari Pertamina | Farhan Budiman | ⏳ Menunggu |
| 16 | Penyiapan dokumen JSA/TRA | Pak Tresnandi / LGU | 🔴 Terbuka |
| 17 | Penjadwalan site visit Pertamina ke lab | LGU | 🔴 Terbuka |
| 18 | Penyusunan SOP pengujian | Tim Lab | 🔴 Terbuka |
| 19 | Evaluasi keputusan solder vs soket | Tim Elektronik | 🔴 Terbuka |
| 20 | Penataan ulang lab | Pak Maman | 🟡 Berjalan |

### 6.2 Rekomendasi Strategis

1. **Prioritaskan Penyelesaian Catu Daya**
   - Selisih 2,43W vs 6W adalah *blocker* fungsional
   - Pengukuran ulang dengan data tegangan lengkap bersamaan penggantian DC converter

2. **Kuantifikasi Ulang Jangkauan LoRa**
   - Konversi 100m menjadi estimasi jumlah CH untuk area RU
   - Tinjau ulang opsi antena, tinggi mounting, atau parameter LoRa

3. **Formalkan SOP Sebelum Site Visit Pertamina**
   - SOP, dokumen JSA/TRA, dan penataan lab sebagai satu paket kesiapan

4. **Isolasi Penyebab Inkonsistensi Data**
   - Selesaikan chamber untuk isolasi variabel eksternal
   - Pisahkan penyebab internal (ADC/sensor) vs eksternal (prosedur)

5. **Tetapkan Protokol QC Per Unit GLD**
   - Karakterisasi baseline tiap unit menjadi bagian proses produksi
   - Satu model AI per unit GLD

---

## 7. Data Pendukung

### 7.1 Log Serial
- File: `GLD_serial_20260708T060449.log`
- Status: Kosong (belum ada data terekam)

### 7.2 Uji Sinyal LoRa
- File: `Test Sinyal LoRa.xlsx`
- Hasil: Antena 6m maksimum ±100m

### 7.3 Diagram Sistem
- **Urutan ADS** (`Urutan ADS,.jpeg`): Diagram rangkaian ADS
- **Urutan Channel MCP** (`Urutan Channel MCP.jpeg`): Diagram channel MCP

### 7.4 Dashboard Monitoring
- File: `Dashboard_GLD_ProjectManagement.html`
- Fungsi: Monitoring progres proyek secara real-time

---

## 📅 Timeline Progres

| Periode | Pencapaian |
|---------|------------|
| **12 Juni 2026** | Kick-off Meeting |
| **18 Juni** | Penetapan prinsip pemodelan AI baru |
| **26 Juni** | Temuan jangkauan LoRa 6m ±100m |
| **2 Juli** | Evaluasi repositori kode |
| **6 Juli** | Uji coba 2 CH; Mahasiswa PJ chamber didapatkan |
| **9 Juli** | Pengukuran solar-baterai (belum optimal) |
| **13 Juli** | Profil beban daya GLD terukur |
| **14 Juli** | Pengukuran status baterai penuh |
| **16 Juli** | Eksperimen sensor MQ (CO₂ & O₂); Aplikasi UI GLD selesai |
| **17 Juli** | Urutan kerja dengan Pertamina disepakati |
| **18 Juni – 20 Juli** | Laporan progres periode ini |

---

## 📊 Status Proyek Saat Ini

```
Overall Progress: ████████████░░░░░░░░░░░░░░░░░░  40%

Hardware:     ████████████░░░░░░░░  60%
Software:     ████████░░░░░░░░░░░░  40%
AI/ML:        ████████░░░░░░░░░░░░  40%
Jaringan:     ████████████░░░░░░░░  60%
Daya:         ████████░░░░░░░░░░░░  40%
Dokumentasi:  ████████░░░░░░░░░░░░  40%
```

---

## 📞 Kontak Tim

| Peran | Institusi | Kontak |
|-------|-----------|--------|
| Project Manager | LGU | - |
| Hardware Lead | Lab IoT ITB | Fahmi |
| AI Lead | Lab Fisika ITB | Pak Fahdzi |
| Network Lead | Lab IoT ITB | Tim Jaringan |
| Chamber PJ | Mahasiswa | - |
| Admin | LGU | Farhan Budiman |
| Collab Pertamina | PT Pertamina | anita.rohmawati@gmail.com |

---

**Dokumen ini disusun berdasarkan:**
- Laporan Progres GLD 18 Juni – 20 Juli 2026
- Dataset sensor MQ (Juli 2026)
- Notulensi rapat dan diskusi tim
- Data uji jaringan LoRa
- Dokumen pendukung lainnya

---

*Last Updated: 23 Juli 2026*  
*Repository: https://github.com/RavellerH/GLD-V2-Report-2026*
