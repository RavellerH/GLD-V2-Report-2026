# Files Catalog — isi setiap file di repo

## A. Deliverable yang dibuat oleh Claude (root)
| File | Isi |
|---|---|
| `Dashboard_GLD_ProjectManagement.html` | Dashboard manajemen proyek interaktif (navy korporat): exec summary, progres vs outstanding, KPI, Kurva-S, Gantt 12 aktivitas, cakupan 6 RU, arsitektur 3 repo, sub-sistem, resource readiness, activity feed, blocker, action items, isu, rekomendasi. |
| `Laporan_Progres_ByDate_GLD.html` / `.md` | Laporan progres kronologis (timeline Apr–Jul 2026). |
| `JSA_HSE_RU-IV_Cilacap_GLD.html` / `.md` | **DRAFT** JSA/TRA & HSE plan RU IV Cilacap (4 lembar JSA, ERP, tanda tangan). Belum disahkan. |
| `CLAUDE.md`, `memory/*` | Sistem memory ini. |

## B. Dokumen sumber (dari tim/klien)
| File | Isi ringkas |
|---|---|
| `Laporan_Progres_GLD_18Jun-20Jul.md` | Laporan progres periode 18 Jun–20 Jul (sumber teks utama). |
| `Notulensi_KickOffMeeting 12 Juni 2026.pdf` | Notulen kick-off Pertamina (scope, tanya-jawab, mode sistem). |
| `Deck Presentasi GLD KICKOFF MEETING - BPUDL Template.pptx_compressed (1).pdf` | Deck kick-off (66 hlm): **timeline 9 bulan, in/out scope, arsitektur, AI, HSE, org, resource plan, TKDN**. Sumber **baseline resmi**. |
| `Kebutuhan_Peralatan_GLD_per_RU_v2.pdf` | Spesifikasi & jumlah perangkat per RU (tabel 6 RU). |
| `Timeline_Kerjaan_Mingguan_GLD.pptx` | Timeline mingguan awal (M1–M7, 20 Apr–7 Jun). |
| `Timeline_Kerjaan_Mingguan_GLD_updated_Juli_2026.pdf` | **Update Juli (87 hlm):** analisis daya lengkap (baterai/solar/duty-cycle), uji mesh, uji downlink. |
| `mom_ruiv_cilacap_gld.pdf` / `(1).pdf` | MoM RU IV Cilacap (survei, penempatan CH, AI, chamber). |
| `POLE-BRACKET-GLD-CH-SOLAR.pdf.pdf` | Desain bracket tiang CH + solar. |
| `TCN_GasLPG_Presentation (2).pptx` | Presentasi model TCN LPG. |
| `Cadangan AI Kick of meeting.pptx` | Materi AI cadangan kick-off. |
| `Test Sinyal LoRa.xlsx` | Data uji RF LoRa (RSSI/SNR/PDR, orientasi antena, koordinat). |
| `GLD_serial_20260708T060449.log` | Log serial perangkat (8 Jul). |
| `Urutan ADS,.jpeg`, `Urutan Channel MCP.jpeg` | Diagram urutan channel ADC (ADS/MCP). |

## C. Dataset sensor (`Dataset/`) — perangkat GLD-F001, 15 Jul 2026
9 file CSV, **14.477 baris total**, 8 kanal tegangan (MQ8, MQ135, MQ3, MQ5, MQ4, MQ7, MQ6, MQ2). Sesi: Clean Air, LPG (×2), Oksigen, Carbon Dioxide, + baseline. Format: `timestamp_ms, wall_time, voltage_MQ*`.

> Catatan: file `TCN_GasLPG` = model LPG yang **disetujui**. Berkas OGI/YOLO (thermal) **tidak dipakai** dalam report (belum disetujui).
