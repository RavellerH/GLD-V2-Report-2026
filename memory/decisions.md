# Decision Log

Keputusan yang membentuk deliverable & arah kerja. Format: ID · tanggal · keputusan · alasan.

| ID | Tgl | Keputusan | Alasan |
|---|---|---|---|
| dec:01 | 23 Jul | Deliverable utama = **dashboard HTML interaktif** | Paling pas untuk pemantauan/monitoring visual |
| dec:02 | 23 Jul | Bahasa = **Bahasa Indonesia** | Sesuai dokumen sumber & audiens |
| dec:03 | 23 Jul | Baseline Kurva-S = **diturunkan dari dokumen**, lalu dikalibrasi ke **Project Timeline 9 bulan (Deck Kick-Off)** | Sumber jadwal paling otoritatif |
| dec:04 | 23 Jul | Scope tracking = **melalui pilot RU IV Cilacap**, 5 RU lain roadmap | Scope aktif nyata hanya 1 RU |
| dec:05 | 23 Jul | **Hapus OGI** (YOLO/thermal) | Belum disetujui klien |
| dec:06 | 23 Jul | Site survey = **plan/workflow selesai, eksekusi pending**; **TRA/JSA jadi gate eksplisit** | Rencana siap; penahan nyata = TRA/JSA |
| dec:07 | 23 Jul | **Uji fungsional GLD-CH-GW-Server** ditandai **selesai** (rantai komunikasi 9 Jul, hingga inferensi AI 16 Jul) | Konfirmasi user |
| dec:08 | 23 Jul | Desain HTML = **korporat navy/steel**; tambah **Executive Summary + panel Progres vs Outstanding** | Client-facing; klien = partner → transparansi |
| dec:09 | 23 Jul | Blocker daya **di-reframe**: bukan "baterai tak bisa suplai" (2,43 W) tapi **"autonomi baterai GLD < target 30 hari"** (draw ON 5,75 W terverifikasi; 7P=1,76 hari) | Data update Juli mengklarifikasi anomali |
| dec:10 | 23 Jul | Buat **memory system** (CLAUDE.md + memory/ + graph) | Pemahaman folder lintas sesi & pencatatan terstruktur |
| dec:11 | 23 Jul | **Tema HTML → biru #2B5FCB + charcoal #262321** (logo Korporasi Kinarya ITB); tambah **navigasi sticky** di dashboard | Arahan user; tampilan klien lebih mudah dibaca |
| dec:12 | 23 Jul | **Koreksi klaim:** inferensi AI di PC+emulator (bukan on-device); **deviasi diturunkan 42→39% / +20** (jangan over-claim); **LoRa disiasati mesh**; **dataset konsisten** (isu resolved) | Klarifikasi user + pendalaman PDF Juli (uji mesh 8-CH) |
| dec:13 | 23 Jul | **Telemetri → "Evolusi Data & Metode Model"** (Tahap 1 → metode saat ini) | Arahan user: tampilkan perubahan demi perubahan |
| dec:14 | 24 Jul | **Flame Detection (kamera/Jetson Nano) DITAHAN** dari deliverable resmi | Mirip konsep OGI yang sudah dihapus; belum disetujui. Konsisten dengan dec:05 |
| dec:15 | 24 Jul | **Model AI headline → CNN 1D (97,6%)**, menggantikan TCN LPG (≥92%) sebagai model utama untuk pelaporan; TCN tetap dicatat sbg fondasi historis (15 Jul) | Konfirmasi user: "ya CNN 1D terbaru" |
| dec:16 | 24 Jul | Blocker daya **dipisah per mode**: mode 24V = **selesai/resolved** (siap sertifikasi); mode baterai = tetap blocker (target baru <100mA/≥30 hari/potensi 6–8 bln) | Meeting 24 Jul mengklarifikasi 2 jalur power berbeda status |
| dec:17 | 24 Jul | Tambah **blocker baru: verifikasi 6 kelas gas** (prioritas tinggi) | Model baru baru cakup 5 kelas; disyaratkan eksplisit di meeting |
| dec:18 | 24 Jul | Target instalasi Sep 2026 dicatat sebagai **"target internal, belum baseline formal"** — baseline resmi (Des 2026) TIDAK diubah di Kurva-S/Gantt | Jangan over-claim; beda sumber otoritas (internal meeting vs Deck Kick-Off resmi) |
| dec:19 | 24 Jul | Simpan notulen meeting sebagai `Notulen_Meeting_GLD_24Jul2026.md` di repo | Konsistensi dgn praktik arsip notulen/MoM lain (PDF) |

## Prinsip yang mengikat
- Klien = partner → selalu tampilkan progres **dan** outstanding; jangan over-claim (analisis ≠ resolusi blocker).
- Headline progres ditahan konservatif (39%) meski engineering di depan; keunggulan murni sisi lab.
- Cilacap = **RU IV** (bukan VI).
- JSA/HSE = **draft**, wajib disahkan HSE RU sebelum dipakai.
- **Baseline resmi vs target internal**: baseline Kurva-S/Gantt tetap dikalibrasi ke Deck Kick-Off (Des 2026); target internal dari rapat (mis. Sep 2026) dicatat terpisah, tidak menggantikan baseline formal kecuali ada instruksi eksplisit.
- **Flame detection / kamera thermal**: ditahan dari semua deliverable sampai ada arahan eksplisit — sama seperti OGI.
