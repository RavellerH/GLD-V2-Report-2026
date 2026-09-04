# Pilot / Field Testing — RU IV Cilacap

Dokumen progres rekayasa & kesiapan lapangan untuk pilot Gas Leak Detection (GLD) Tahap 2 di RU IV Cilacap. **Progres resmi per 5 September 2026: 44%** (vs baseline rencana 43% pada tanggal yang sama) — angka ini murni progres sisi rekayasa/lab, **bukan** bukti kesiapan instalasi fisik di lapangan (survey lokasi sudah selesai 9–10 Agustus 2026, instalasi fisik belum dimulai, akan dieksekusi oleh vendor Pertamina dengan supervisi teknis LGU/ITB).

## Isi folder

| File | Isi | Catatan |
|---|---|---|
| `Dashboard_GLD_ProjectManagement.{html,pdf}` | Dashboard manajemen proyek — Kurva-S, Gantt 12 aktivitas, status gate/blocker, action items, arsitektur sistem | Dokumen utama untuk melihat status proyek secara keseluruhan |
| `Laporan_Progres_ByDate_GLD.{html,pdf}` | Laporan progres kronologis (20 Apr–31 Agustus 2026), berisi heatmap navigasi tanggal | PDF 12 halaman |
| `Laporan_Detail_Progres_Assessment_FieldTesting_Sep2026.{html,pdf}` | Rincian breakdown progres Assessment (sertifikasi, estimasi) vs Field Testing (pilot RU IV, angka resmi), termasuk bukti pendukung desain bracket | — |
| `Datasheet_Sistem_GLD_Arsitektur_ServerJaringan.{html,pdf}` | Datasheet konsolidasi: arsitektur end-to-end, spesifikasi hardware GLD/Cluster Head/Gateway, protokol radio, kapabilitas gas/AI, kebutuhan server & jaringan untuk tim IT, status gate | Referensi teknis utama untuk tim lapangan/IT Pertamina |
| `JSA_HSE_RU-IV_Cilacap_GLD.{html,pdf}` | Job Safety Analysis (JSA) & HSE Plan draft untuk instalasi RU IV Cilacap | ⚠️ **DRAFT — belum disahkan HSE RU.** Kerangka awal untuk mempercepat penyusunan TRA/JSA resmi, bukan pengganti prosedur HSE RU |
| `Knowledge_Graph_GLD.html` | Peta pengetahuan proyek interaktif (70 node, 83 relasi) — entitas, sub-sistem, dependensi | **Hanya tersedia HTML** — kontennya kanvas interaktif (force-directed graph) yang tidak tercetak statis ke PDF |
| `Desain_Bracket_L_UBolt_GLD_Mounting.{html,pdf}` | Desain mounting bracket L + U-bolt: standar industri + spesifikasi desain aktual "ATEX Casing v2", termasuk model 3D interaktif | Versi HTML punya **viewer 3D interaktif** (drag/zoom/putar) — tidak muncul di PDF, hanya gambar teknis statis |

## Cara pakai

- Mulai dari `Dashboard_GLD_ProjectManagement.html` untuk gambaran umum.
- Semua file HTML saling tertaut lewat nav bar di bagian atas — bisa berpindah antar dokumen tanpa kembali ke file explorer.
- Untuk model 3D bracket dan grafik interaktif, gunakan versi `.html` (buka di browser) — versi `.pdf` hanya untuk referensi cetak statis.
