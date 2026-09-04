# Paket Dokumen GLD Tahap 2 — untuk PT Pertamina Patra Niaga

Paket ini berisi dokumen laporan & dashboard proyek **Gas Leak Detection (GLD) Tahap 2**, disusun oleh LAPI Ganesha Utama (LGU) bersama Lab IoT & Lab Fisika ITB, per **5 September 2026**.

Isinya dikelompokkan menjadi **2 folder terpisah** karena proyek ini punya **2 jalur paralel** yang berbeda tujuan dan metrik progresnya:

| Folder | Isi | Progres resmi per 5 Sep |
|---|---|---|
| **`01_Pilot_Field_Testing/`** | Progres rekayasa & kesiapan lapangan program pilot/field testing — dashboard proyek, laporan progres kronologis, arsitektur sistem, draft JSA/HSE, desain mounting bracket | **44%** (vs baseline rencana 43%) |
| **`02_Sertifikasi_ATEX_IECEx/`** | Progres proyek sertifikasi kepatuhan area berbahaya (ATEX/IP/EMC/RF) untuk perangkat GLD | **≈20–43%** tergantung definisi — lihat catatan di folder tsb |

Setiap folder punya `README.md` sendiri yang merinci isi filenya.

### Cakupan program pilot/field testing — 6 Refinery Unit, bukan cuma Cilacap

Proyek GLD Tahap 2 mencakup **6 Refinery Unit (RU II–VII)** sesuai proposal formal, masing-masing dengan konfigurasi jumlah sensor/Cluster Head/Gateway sendiri (RU II Dumai, RU III Plaju, RU IV Cilacap, RU V Balikpapan, RU VI Balongan, RU VII Kasim/Sorong). **RU IV Cilacap adalah satu-satunya RU yang saat ini aktif dieksekusi** (survey lokasi selesai 9–10 Agustus 2026, instalasi fisik belum dimulai) — sehingga sebagian besar dokumen di `01_Pilot_Field_Testing/` (laporan progres, JSA, desain bracket) memang berfokus ke Cilacap krn itulah eksekusi yang sedang berjalan. **RU VII Kasim/Sorong** punya sejarah tersendiri: sistem **versi 1 (V1) sudah diuji di sana Desember 2025** (field test pertama, konfigurasi single-channel — beda dari V2 saat ini yang multi-channel), dan sesuai timeline program, **akan ada pengujian lapangan V2 juga di Kasim/Sorong ke depannya** — bukan sekadar "target implementasi Des 2026" tunggal seperti tertulis di ringkasan lama, melainkan kelanjutan dari kolaborasi yang sudah berjalan sejak V1. Belum tentu berstatus sama dengan Cilacap, perlu klarifikasi lebih lanjut ke tim proyek soal jadwal pasti V2. 4 RU lainnya (Dumai, Plaju, Balikpapan, Balongan) masih berstatus **roadmap program**, belum dimulai. Rincian cakupan 6 RU ada di `Dashboard_GLD_ProjectManagement.html` bagian 02.

## Cara pakai

- File `.html` — buka langsung di browser mana pun (Chrome/Edge/Firefox), **tidak perlu internet** (semua self-contained, termasuk gambar & — untuk beberapa file — model 3D interaktif). Ini versi paling lengkap/interaktif.
- File `.pdf` — versi cetak/statis dari file HTML yang sama, untuk dibaca offline atau dicetak. Beberapa elemen interaktif (model 3D, grafik kanvas) **tidak muncul** di versi PDF — dicatat per file di README masing-masing folder.

## Catatan penting sebelum dibagikan

- **Draft JSA/HSE** (`01_Pilot_Field_Testing/JSA_HSE_RU-IV_Cilacap_GLD.*`) **belum disahkan** oleh HSE RU — masih kerangka kerja internal, bukan prosedur resmi. Jelas ditandai "DRAFT" di dalam dokumen.
- Sebagian angka bersifat **estimasi interpretatif tim**, bukan hasil audit resmi — masing-masing dokumen menandai ini secara eksplisit di bagian metodologi/catatan.
- Skema klasifikasi sertifikasi (grup gas/kelas suhu/zona) di folder 02 adalah **rekomendasi tim penyusun**, bukan keputusan resmi dari notified body/lembaga sertifikasi (ExCB) — wajib dikonfirmasi lebih lanjut sebelum dipakai sebagai acuan pengujian final.

## Kontak

LAPI Ganesha Utama (LGU) & Lab IoT/Fisika ITB — Jl. Dederuk No.30, Bandung 40133.
