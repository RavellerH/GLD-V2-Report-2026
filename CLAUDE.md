# CLAUDE.md — Entry Point & Memory Index

> **Baca file ini lebih dulu.** Ini adalah pintu masuk "memory system" repo GLD-V2-Report-2026.
> Detail terstruktur ada di folder [`memory/`](memory/). Perbarui memory saat ada info/keputusan baru.

---

## 1. Apa ini?

Repo dokumentasi & pelaporan proyek **Gas Leak Detection (GLD) Tahap 2** — sistem IoT deteksi kebocoran gas untuk **PT Pertamina Patra Niaga**, dikembangkan oleh **LAPI Ganesha Utama (LGU)** bersama **Lab IoT & Lab Fisika ITB**. Level kematangan **TRL-7** (industri).

- **Arsitektur:** sensor node (8× MQ + AI edge) → **LoRa star-mesh** → Cluster Head → Gateway → PC Server → Dashboard.
- **Program:** 9 bulan (Jun 2026 → Feb 2027), rollout **6 Refinery Unit (RU II–VII)**.
- **Scope aktif sekarang:** **pilot RU IV Cilacap** (5 RU lain = roadmap).
- **Field test kolaborasi:** RU-VII Kasim/Sorong. **Target implementasi:** Des 2026.

## 2. Status singkat (per 23 Jul 2026)

- **Progres pilot Cilacap ≈ 42%** vs baseline resmi 19% → **+23 poin di depan jadwal** (murni sisi engineering).
- ✅ **Uji fungsional GLD-CH-GW-Server hingga inferensi AI SELESAI (16 Jul).**
- ✅ TCN LPG 8-sensor ≥92%; failover CH; dataset 14.477 sampel; CH power teratasi dgn 2 panel.
- ⚠️ **Blocker/gate:** autonomi baterai GLD (7P=1,76 hari vs target 30 hari) + TPL5010 belum optimal; DC converter; jangkauan LoRa ~100 m vs 1–2 km; **gate TRA/JSA** untuk site survey.

## 3. Peta memory (`memory/`)

| File | Isi |
|---|---|
| [`memory/README.md`](memory/README.md) | Cara pakai & aturan pemeliharaan memory |
| [`memory/overview.md`](memory/overview.md) | Latar belakang, scope, pihak, konsep sistem |
| [`memory/files_catalog.md`](memory/files_catalog.md) | Katalog SEMUA file di repo + isinya |
| [`memory/entities.md`](memory/entities.md) | Glosarium entitas: orang, org, sub-sistem, perangkat, repo, RU |
| [`memory/timeline.md`](memory/timeline.md) | Kronologi milestone (Apr–Jul 2026) |
| [`memory/decisions.md`](memory/decisions.md) | Decision log (keputusan + alasan) |
| [`memory/blockers_metrics.md`](memory/blockers_metrics.md) | Blocker, isu, gate, & angka kunci (daya/RF/AI) |
| [`memory/deliverables.md`](memory/deliverables.md) | Deliverable yang sudah dibuat + URL artifact |
| [`memory/graph.md`](memory/graph.md) | **Knowledge graph (Mermaid)**: entitas, data-flow, dependensi |
| [`memory/graph.json`](memory/graph.json) | Graph versi machine-readable (nodes + edges) |

## 4. Deliverable utama (file HTML/MD di root)

- `Dashboard_GLD_ProjectManagement.html` — dashboard manajemen proyek (navy korporat).
- `Laporan_Progres_ByDate_GLD.{html,md}` — laporan progres kronologis.
- `JSA_HSE_RU-IV_Cilacap_GLD.{html,md}` — draft JSA/HSE Cilacap (belum disahkan).

URL artifact & detail → [`memory/deliverables.md`](memory/deliverables.md).

## 5. Aturan kerja penting (jangan dilupakan)

- **Bahasa:** Bahasa Indonesia untuk semua deliverable.
- **Desain HTML:** palet korporat **navy/steel** (client-facing), light+dark, self-contained.
- **Baseline Kurva-S:** dikalibrasi ke **Project Timeline 9 bulan (Deck Kick-Off)**.
- **Transparansi:** klien = partner → selalu tampilkan **progres + outstanding** secara jujur; jangan over-claim (analisis ≠ resolusi blocker).
- **OGI (YOLO/thermal) DIHAPUS** — belum disetujui. Jangan dimasukkan lagi tanpa arahan.
- **Cilacap = RU IV** (bukan VI). Scope aktif hanya 1 RU.
- **Git:** kerja di branch `claude/project-management-tracking-5l8ypx`; PR aktif = **PR #1**. Push = update PR.

## 6. Cara memelihara memory ini

Setiap ada informasi/keputusan/milestone baru: perbarui file `memory/` yang relevan **dan** `graph.json` bila menambah entitas/relasi, lalu ringkas ulang bagian "Status singkat" di atas. Lihat [`memory/README.md`](memory/README.md).
