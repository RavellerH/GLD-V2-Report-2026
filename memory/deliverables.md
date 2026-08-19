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

> ⚠️ **File pindah folder 30 Jul** (root → `Deliverables/`). Redeploy **dalam sesi yang sama** yang mem-publish = pakai path baru (URL tetap otomatis). Redeploy dari **sesi/percakapan baru** (termasuk ini) **wajib** pass parameter `url` di atas ke tool Artifact — tanpa itu akan mint URL baru. Jangan andalkan path lama untuk mencocokkan artifact across sesi.
>
> **8 Agu:** Konten `Dashboard_GLD_ProjectManagement.html` & `Laporan_Progres_ByDate_GLD.{html,md}` diupdate (mounting/topologi vs Emerson, requirement gas/alarm/material baru 6 Agu, push alarm berhasil diuji 6–8 Agu) — **file lokal sudah diupdate**, belum di-republish ke Artifact URL di atas pada sesi ini (sesi ini dikonfigurasi tanpa akses publish artifact/PR — lihat catatan Git di bawah).

## Isi Datasheet Sistem (11 bagian, rev 0.4 — 19 Agu)
Ringkasan & cara baca (3 audiens) · **02 Kesiapan: Kilang vs LGU/ITB** (checklist 2 kolom — sudah disiapkan LGU/ITB vs perlu disiapkan Pertamina, dikelompokkan jaringan&server/instalasi&catu daya/perizinan&sertifikasi, ditambahkan atas permintaan user 19 Agu agar kebutuhan kilang jadi fokus di halaman awal) · arsitektur end-to-end (data flow lapangan→dashboard + sinkronisasi site↔HQ Jakarta) · datasheet perangkat (GLD/CH/Gateway, dari firmware config & final_design.md) · radio & protokol (STAR/MESH params, RF range, ringkas frame) · area berbahaya & ATEX (3-komponen Ex-proof, mounting, status BELUM sertifikasi) · deteksi gas & AI (CNN Dual-Branch, gap Benzena/CO/H2S) · **server & jaringan IT** (rangkuman `Gateway-to-Server-Site-IT-Pertamina.docx` + `Gateway-to-Server-Site-Technical-Datasheet.docx` dari repo `PertaminaGLD`, 13 Agu — dipertahankan sbg draft/requirement apa adanya) · catu daya & instalasi · status gate/blocker · lampiran sumber. Dibuat berdasarkan riset repo `PertaminaGLD` (firmware/docs) + `gasleakdetectionV2-April` (dashboard/arsitektur HQ sync) + notulen ATEX (`Sumber Dokumen/Summary recorder 081426.pdf`) + `memory/*`. User confirmed via AskUserQuestion: 1 dokumen master, network doc dipertahankan sbg draft bukan final.

**Desain (19 Agu, 2 iterasi setelah rev 0.1):** rev 0.2 = diagram-first, kurangi teks (feedback: "sulit dibaca, kurangi kata-kata, perbanyak diagram"). Rev 0.3 = ganti palet ke gaya admin dashboard **INSPINIA** (referensi: chuibility.github.io/inspinia) — sidebar navy #2F4050, aksen teal-hijau #1ABB9C, kartu flat border tipis, radius kecil (6px), font sans tanpa mono di label (feedback: "ganti kombinasi warna/desain/font, masih sulit dibaca").

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
