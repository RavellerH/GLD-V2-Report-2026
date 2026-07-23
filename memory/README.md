# Memory System — GLD V2 Report

Sistem memory terstruktur agar folder ini mudah dipahami lintas sesi, dan semua konteks/keputusan tercatat rapi.

## Struktur

```
CLAUDE.md              ← entry point (dibaca pertama)
memory/
├── README.md          ← file ini (cara pakai & pemeliharaan)
├── overview.md        ← latar belakang, scope, konsep sistem
├── files_catalog.md   ← katalog semua file sumber & deliverable
├── entities.md        ← glosarium entitas (orang/org/subsistem/perangkat/repo/RU)
├── timeline.md        ← kronologi milestone
├── decisions.md       ← decision log (keputusan + alasan + tanggal)
├── blockers_metrics.md← blocker/isu/gate + angka kunci
├── deliverables.md    ← daftar deliverable + URL artifact
├── graph.md           ← knowledge graph (Mermaid): entitas, data-flow, dependensi
└── graph.json         ← graph machine-readable (nodes + edges)
```

## Prinsip

1. **Satu sumber kebenaran per topik.** Angka progres/daya/RF hanya "hidup" di `blockers_metrics.md` & `graph.json`; file lain merujuk, tidak menduplikasi diam-diam.
2. **Human-readable + machine-readable.** MD untuk manusia & Claude; `graph.json` untuk parsing/relasi.
3. **Append, jangan hapus histori.** Milestone/keputusan lama tetap dicatat (dengan tanggal); yang berubah diberi catatan "diperbarui".
4. **Jujur & seimbang.** Catat progres DAN outstanding. Analisis ≠ resolusi.

## Cara memperbarui (checklist saat ada info baru)

- [ ] Milestone/aktivitas baru → tambah ke `timeline.md` (dan feed dashboard bila relevan).
- [ ] Keputusan baru → tambah baris di `decisions.md` (ID, tanggal, keputusan, alasan).
- [ ] Angka/metrik baru → `blockers_metrics.md`.
- [ ] Entitas/relasi baru → `entities.md` **dan** `graph.md` + `graph.json`.
- [ ] File baru di repo → `files_catalog.md`.
- [ ] Deliverable baru/di-update → `deliverables.md`.
- [ ] Ringkas ulang "Status singkat" di `CLAUDE.md`.

## Konvensi ID (untuk graph)

- Orang: `p:<nama>` · Organisasi: `org:<kode>` · Sub-sistem: `sub:<kode>` · Perangkat: `dev:<kode>`
- Repo: `repo:<nama>` · RU: `ru:<kode>` · Milestone: `ms:<kode>` · Blocker: `blk:<kode>` · Keputusan: `dec:<id>`

*Dibuat 23 Juli 2026.*
