# Deliverables — yang sudah dibuat

| Deliverable | File (path baru per 30 Jul) | Artifact URL | Favicon |
|---|---|---|---|
| Dashboard manajemen proyek | `Deliverables/Dashboard_GLD_ProjectManagement.html` | https://claude.ai/code/artifact/507ba345-6cc4-48c1-b096-bfe7652696cd | 🛢️ |
| Laporan progres per tanggal | `Deliverables/Laporan_Progres_ByDate_GLD.html` (+`.md`) | https://claude.ai/code/artifact/6bf8efb7-c4a1-495d-b964-7ac4014e5a22 | 📅 |
| Draft JSA/HSE Cilacap | `Deliverables/JSA_HSE_RU-IV_Cilacap_GLD.html` (+`.md`) | https://claude.ai/code/artifact/2601ab9e-d32d-4e63-a06c-279278c96fb3 | 🦺 |
| Knowledge graph interaktif | `Deliverables/Knowledge_Graph_GLD.html` | https://claude.ai/code/artifact/cae0f3a3-65e5-4355-808a-d467dc6f9e16 | 🕸️ |
| Notulen meeting 30 Jul (disusun Claude) | `Deliverables/Notulen_Meeting_GLD_30Jul2026.md` | *(belum dipublikasi sbg artifact)* | — |
| Notulen meeting 6 Agustus, terkoreksi (disusun Claude) | `Deliverables/Notulen_Meeting_GLD_6Agustus2026.{docx,pdf}` | *(dikirim langsung ke user via file, belum dipublikasi sbg artifact)* | — |
| Datasheet Sistem — Arsitektur, Perangkat &amp; Kebutuhan Server/Jaringan | `Deliverables/Datasheet_Sistem_GLD_Arsitektur_ServerJaringan.html` | *(belum dipublikasi sbg artifact)* | — |
| Datasheet Sistem — versi slide PDF + PowerPoint editable (tema terang, 19 slide 16:9) | `Deliverables/Datasheet_Sistem_GLD_Slides.{pdf,pptx}` (`Datasheet_Sistem_GLD_Slides_source.html` masih arsip rev 0.6, bukan sumber rev 0.7) | *(file lokal, belum dipublikasi)* | — |

> ⚠️ **File pindah folder 30 Jul** (root → `Deliverables/`). Redeploy **dalam sesi yang sama** yang mem-publish = pakai path baru (URL tetap otomatis). Redeploy dari **sesi/percakapan baru** (termasuk ini) **wajib** pass parameter `url` di atas ke tool Artifact — tanpa itu akan mint URL baru. Jangan andalkan path lama untuk mencocokkan artifact across sesi.
>
> **8 Agu:** Konten `Dashboard_GLD_ProjectManagement.html` & `Laporan_Progres_ByDate_GLD.{html,md}` diupdate (mounting/topologi vs Emerson, requirement gas/alarm/material baru 6 Agu, push alarm berhasil diuji 6–8 Agu) — **file lokal sudah diupdate**, belum di-republish ke Artifact URL di atas pada sesi ini (sesi ini dikonfigurasi tanpa akses publish artifact/PR — lihat catatan Git di bawah).

## Isi Datasheet Sistem (11 bagian, rev 0.5 — 19 Agu)
Ringkasan & cara baca (3 audiens) · **02 Kesiapan: Kilang vs LGU/ITB** (checklist 2 kolom — sudah disiapkan LGU/ITB vs perlu disiapkan Pertamina, dikelompokkan jaringan&server/instalasi&catu daya/perizinan&sertifikasi, ditambahkan atas permintaan user 19 Agu agar kebutuhan kilang jadi fokus di halaman awal) · arsitektur end-to-end (data flow lapangan→dashboard + sinkronisasi site↔HQ Jakarta) · datasheet perangkat (GLD/CH/Gateway, dari firmware config & final_design.md) · radio & protokol (STAR/MESH params, RF range, ringkas frame) · area berbahaya & ATEX (3-komponen Ex-proof, mounting, status BELUM sertifikasi) · deteksi gas & AI (CNN Dual-Branch, gap Benzena/CO/H2S) · **server & jaringan IT** (rangkuman `Gateway-to-Server-Site-IT-Pertamina.docx` + `Gateway-to-Server-Site-Technical-Datasheet.docx` dari repo `PertaminaGLD`, 13 Agu — dipertahankan sbg draft/requirement apa adanya) · catu daya & instalasi · status gate/blocker · lampiran sumber. Dibuat berdasarkan riset repo `PertaminaGLD` (firmware/docs) + `gasleakdetectionV2-April` (dashboard/arsitektur HQ sync) + notulen ATEX (`Sumber Dokumen/Summary recorder 081426.pdf`) + `memory/*`. User confirmed via AskUserQuestion: 1 dokumen master, network doc dipertahankan sbg draft bukan final.

**Desain (19 Agu, 2 iterasi setelah rev 0.1):** rev 0.2 = diagram-first, kurangi teks (feedback: "sulit dibaca, kurangi kata-kata, perbanyak diagram"). Rev 0.3 = ganti palet ke gaya admin dashboard **INSPINIA** (referensi: chuibility.github.io/inspinia) — sidebar navy #2F4050, aksen teal-hijau #1ABB9C, kartu flat border tipis, radius kecil (6px), font sans tanpa mono di label (feedback: "ganti kombinasi warna/desain/font, masih sulit dibaca"). Rev 0.4 = tambah bagian 02 "Kesiapan: Kilang vs LGU/ITB" (checklist 2 sisi), 10→11 bagian.

**Audit verifikasi (19 Agu, → rev 0.5):** user minta "verifikasi dari sumber dokumen" — dijalankan via subagent yang re-fetch fresh semua source (PDF ATEX, protocol reference, final_design.md ×3, firmware config ×5, 2 docx integrasi, Architecture.md, docker-compose.vps.yml) dan cocokkan tiap klaim numerik/faktual di datasheet. Hasil: **~45+ klaim MATCH persis** (radio params, timing, battery threshold, port 1884, topic MQTT, RF range, jumlah unit CH, metrik daya — semua cocok source). **2 klaim diperbaiki:**
1. **"3 kompartemen ATEX"** → dikoreksi jadi "2 kompartemen + seal/gland" — notulen tertulis cuma merinci 2 kompartemen fisik (elektronik+sensor); "3 komponen" di transkrip verbal ambigu/tidak lengkap.
2. **AI on-device** → ditambah catatan verifikasi eksplisit: klaim ini dari konfirmasi user langsung, BUKAN dari dokumen. Source firmware tertulis terbaru yg bisa dicek (`docs/design/gld/final_design.md`, mirror 29 Jun 2026) masih describe skema klasifikasi lama 6-kelas (clear/LPG/methane/propane/butane/anomaly), bukan 4-kelas CNN Dual-Branch — kemungkinan doc mirror belum update sejak integrasi CNN Dual-Branch (~29 Jul–9 Agu), tapi **belum diverifikasi tertulis**. Perlu commit firmware terbaru utk konfirmasi final sebelum diklaim ke klien tanpa catatan ini.

Item session-only lain (bukan error, cuma belum ada di dokumen tertulis): payload GW <1KB & periode 10/90 dtk, GW power 5V adaptor, bracket Emerson/L-bracket, MAC registration — semua ini legitimate krn berasal dari instruksi langsung user (LGU/ITB), bukan fabrikasi, tapi ditandai apa adanya di datasheet (banyak sudah pakai chip `TBD`/`gap`).

**Rev 0.6 (19 Agu, datasheet HTML utama):** user minta "review it" thd file baru `Sumber Dokumen/Parameter spesifikasi EMC_lengkap.docx` (Dr. Nina Siti Aminah/ITB Fisika) — dirangkum ke bagian 04: tambah spek EMC (modul radio E22-900MM22S, TX power maks, antena, dimensi fisik, enclosure metal, konsumsi daya, port) ke 3 devcard + **3 foto produk aktual di-embed base64** (self-contained). Ditemukan 2 hal butuh klarifikasi (dicatat sbg gate baru, bukan disembunyikan): input power CH 5VDC vs solar+18650, dan port Ethernet Gateway blm jelas didukung firmware. TX power 22dBm(modul)/7,995W(24VDC) direkonsiliasi eksplisit sbg BUKAN kontradiksi dgn 17dBm firmware/5,75W baterai — beda hal, dijelaskan berdampingan.

> ⚠️ **Paragraf slide di bawah ditulis dari sesi paralel lain** (commit `493be06`, bukan sesi yang menulis rev 0.6 HTML di atas) — riwayat slide deck berkembang independen dari datasheet HTML utama sejak titik ini. `Datasheet_Sistem_GLD_Slides_source.html` disebut sbg arsip rev 0.6 dan **bukan lagi sumber deck terbaru** setelah pindah ke PPTX.

**Versi slide (rev 0.6, 19 Agu):** PDF 14 halaman 16:9 dan source HTML telah diperbaiki agar sinkron dengan audit rev 0.5. Koreksi utama: cover tidak lagi salah menampilkan rev 0.4; status TRA/JSA menjadi **draft tersedia tetapi belum disahkan**; klaim AI on-device tetap membawa caveat bukti firmware tertulis; paket server dibedakan dari bukti commissioning; istilah teknis/Indonesia dirapikan. Ditambahkan `Deliverables/Datasheet_Sistem_GLD_Slides.pptx` sebagai versi PowerPoint editable, dengan objek native dan blok `[Sources]` pada speaker notes tiap slide. PPTX dirender penuh dan lolos `slides_test.py` tanpa overflow; PDF dirender ulang via headless Chrome dan diverifikasi 14 halaman.

**Versi slide (rev 0.7, 19 Agu):** PPTX/PDF diperluas menjadi 19 halaman untuk menjawab kebutuhan Kilang secara eksplisit. Tambahan utama: baseline server/VM dan tanggung jawab jaringan/operasi yang harus disediakan Kilang; DFD lapangan→dashboard RU; batas repo PertaminaGLD vs aplikasi; integration gap adapter MQTT→backend; datasheet frontend (Next.js/React/Mapbox/Recharts, GraphQL polling, mode RU/HQ); datasheet backend (NestJS/Apollo/Prisma, entity dan alert logic); serta sinkronisasi opsional RU→VPS/HQ. Audit repo dikunci pada commit `gasleakdetectionV2-April@660febbf` dan `PertaminaGLD@69a493c3`. Deck membedakan kondisi aktual RU (**SQLite**) dari target produksi PostgreSQL/TimescaleDB yang belum diputuskan. PPTX lolos `slides_test.py` tanpa overflow; PDF dibuat dari render slide yang sama agar visual identik (19 halaman). HTML tetap arsip rev 0.6 dan tidak boleh dianggap sumber deck terbaru.

**Versi slide (rev 0.8, 19 Agu):** seluruh visible copy diubah untuk audience teknis Pertamina. Judul menggunakan format specification/status/DFD/acceptance criteria; wording persuasif dihapus. Status implementasi dinyatakan eksplisit menggunakan `PASS`, `IMPLEMENTED`, `NOT IMPLEMENTED`, `OPEN`, `NOT COMMISSIONED`, dan `MANDATORY`. Requirement Kilang, interface boundary, production parameters, database baseline, firewall policy, hazardous-area hold, commissioning prerequisites, dan mandatory evidence ditulis sebagai pernyataan teknis langsung. PPTX kembali lolos `slides_test.py` tanpa overflow; PDF 19 halaman dibuat dari render PPTX yang sama.

## Isi dashboard (bagian)
Identity band · doc-meta · **Executive Summary** · KPI · **Progres vs Outstanding** · baseline note · Kurva-S · Gantt 12 aktivitas · cakupan 6 RU · **arsitektur 3 repo** · sub-sistem · resource readiness · activity feed · telemetri · blocker · action items · isu/risiko · rekomendasi.

## Konvensi desain
- Palet **korporat navy/steel** (light+dark, theme-toggle). Font: system sans + mono untuk data. Self-contained (CSP-safe).
- Tone: transparansi progres + outstanding untuk partner.

## Git / GitHub
- Branch: `claude/project-management-tracking-5l8ypx`. **PR aktif: #1**. Push = update PR.
- Repo scope sesi: `ravellerh/gld-v2-report-2026` (+ 3 repo kode dibaca via web).

## Riwayat commit besar (branch)
Dashboard awal → rebuild baseline 9 bulan + 6 RU + arsitektur → hapus OGI + reframe Cilacap → progress report + JSA → uji fungsional selesai → redesign navy + exec/outstanding + repo updates → PDF Juli + power/mesh/downlink → memory system.
