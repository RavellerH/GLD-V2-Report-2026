# AGENTS.md — Entry Point & Memory Index

> **Baca file ini lebih dulu.** Ini adalah pintu masuk "memory system" repo GLD-V2-Report-2026.
> Detail terstruktur ada di folder [`memory/`](memory/). Perbarui memory saat ada info/keputusan baru.

---

## 1. Apa ini?

Repo dokumentasi & pelaporan proyek **Gas Leak Detection (GLD) Tahap 2** — sistem IoT deteksi kebocoran gas untuk **PT Pertamina Patra Niaga**, dikembangkan oleh **LAPI Ganesha Utama (LGU)** bersama **Lab IoT & Lab Fisika ITB**. Level kematangan **TRL-7** (industri).

- **Arsitektur:** sensor node (8× MQ + AI edge) → **LoRa star-mesh** → Cluster Head → Gateway → PC Server → Dashboard.
- **Program:** 9 bulan (Jun 2026 → Feb 2027), rollout **6 Refinery Unit (RU II–VII)**.
- **Scope aktif sekarang:** **pilot RU IV Cilacap** (5 RU lain = roadmap).
- **Field test kolaborasi:** RU-VII Kasim/Sorong. **Target implementasi:** Des 2026.

## 2. Status singkat (per 8 Agu 2026)

- **Progres pilot Cilacap ≈ 39%** vs baseline resmi 19% → **+20 poin** (murni sisi engineering lab, **bukan** kesiapan lapangan).
- ✅ Rantai **GLD-CH-GW-Server end-to-end**; **inferensi AI kini di PC + emulator ESP32** (belum on-device — langkah berikutnya).
- ✅ TCN LPG 8-sensor ≥92%; **dataset konsisten & siap pakai**; failover CH; **mesh 8-CH multi-hop se-kampus** (menyiasati jangkauan LoRa); CH power teratasi dgn 2 panel.
- ✅ **Progress chamber gas**: solenoid valve, BME280 ganda (I2C 0x76/0x77), TGS2610 via ADS1115, LM2596 step-down, BTS7960 driver pompa. Next: PCB layout, pompa senyap, mounting dinding.
- ⚠️ **Blocker/gate:** autonomi baterai GLD (7P=1,76 hari vs 30 hari); TPL5010 belum memutus daya (~0,4 V); DC converter; deploy AI on-device ESP32; **gate TRA/JSA** untuk site survey. Jangkauan LoRa per-hop **disiasati mesh** (bukan blocker keras).
- 🔵 **Meeting LGU–Pertamina 24 Jul**: 24V **siap sertifikasi** (biro Shanghai); battery version target **<100mA**/min 30 hari (desain baru berpotensi 6–8 bulan) — **paralel, tidak menghambat** deployment 24V; gate baru **gas capability min 6 kelas** (H₂/LPG/Metana/CO₂/Clean Air, baru **3/6 tervalidasi**); 18 action items; next **RAP Meeting ~15 Agu 2026**. ⚠️ **Belum dikonfirmasi masuk scope**: flame detection camera (Jetson Nano, 79%). ✅ Klaim "CNN 1D 97,6%" **direkonsiliasi**: model nyata klasifikasi jenis gas 3-kelas, terpisah & tidak konflik dgn TCN ≥92% (prediksi leak time-series). Detail → `memory/blockers_metrics.md`, `memory/decisions.md` dec:14–21.
- 🔴 **PENTING — jadwal berubah (weekly meeting 30 Jul):** kunjungan Cilacap **maju & digabung jadi 9–10 Agustus** (survey + instalasi sekaligus), **menggantikan** rencana 24 Jul (survey akhir Jul → instalasi Sep). Arsitektur diperjelas: **app+DB penuh lokal** (site + kantor Jakarta, request Pak Pindoan), **cloud hanya gateway/relay ringan**. **Wi-Fi ESP32 = config lokal saja**, LoRa tetap backbone (bukan perubahan arsitektur). Risiko baru: kondensasi casing, LoRa data-collision belum diuji, push alarm belum dicoba, protokol missed-report GLD portable, **akurasi model dipertanyakan ulang** (perlu verifikasi independen). Detail → `memory/blockers_metrics.md` § Meeting mingguan 30 Jul, `memory/decisions.md` dec:22–26.
- 📁 **Struktur folder dirapikan (30 Jul):** root kini `Deliverables/` (output Codex) + `Sumber Dokumen/` (dokumen tim/klien) + `Dataset/` + `memory/`. Lihat bagian 4 & `memory/files_catalog.md`.
- 🔵 **Diskusi mounting/topologi 6 Agu** (rujukan sistem **Corrosion Monitoring Emerson**, WirelessHART, sudah terpasang & teruji di kilang): mounting GLD/CH pakai **bracket L + U-clamp** ke struktur existing, **tanpa pole baru, tanpa las/bor**; GLD diminta bisa **berfungsi juga sebagai CH**; instalasi kilang baru dicoba **setinggi orang** (belum tersertifikasi lebih tinggi → `gate:cert-height`). **Requirement baru Pertamina:** wajib deteksi **Benzena, CO, H2S** (⚠️ belum direkonsiliasi dgn gate 6-kelas 24 Jul → `gate:gas-extra`); **alarm toksik (CO/H2S) langsung**, gas mudah-terbakar tetap berbasis threshold; **chamber tak boleh masuk kilang**; **hindari PVC**; kolom **"Area"** perlu ditambah di aplikasi. Status produksi: **CH 16 unit** (9 besar+7 kecil), **GLD 4 unit** diminta. Detail → `memory/blockers_metrics.md` § Meeting 6 Agustus, `memory/decisions.md` dec:27–33.
- ✅ **Push alarm berhasil diuji (6–8 Agu):** demo mesh kampus (GW+CH1+CH2+CH3, semua CH terhubung ke GW) — GLD disemprot LPG → server alarm **otomatis tanpa pull request**. Menyelesaikan risiko "push alarm belum dicoba" dari 30 Jul (uji di lab/kampus, **belum** validasi lapangan RU). `memory/decisions.md` dec:34.
- 🔴 **H-1 kunjungan Cilacap:** sesuai dec:22, tim berangkat **9 Agustus**, instalasi **10 Agustus** (survey+instalasi digabung). Urutan demo: aktifkan server → pasang GW → pasang CH → pasang GLD 24V.
- ✅ **Model AI resmi kini: CNN Dual-Branch** (ditemukan 9 Agu di `Sumber Dokumen/`, push langsung Farhan di luar sesi Codex; **dikonfirmasi user 9 Agu menggantikan CNN 1D**). Klasifikasi **4 kelas: LPG/CO2/Udara Bersih/H2**, arsitektur 2-cabang (Conv1D sensor + Dense datasheet-sensitivity). **Akurasi resmi dipakai: 99,20%** (on-chip ESP32-S3 int8, 9,14 KB — bukan 99,73% pre-kuantisasi) vs 97,3% CNN 1D lama. ⚠️ **Masih TIDAK mencakup H2S/Benzena** (dikonfirmasi user) — `gate:gas-extra` belum tertutup sepenuhnya. Detail → `memory/entities.md` § Model AI, `memory/decisions.md` dec:36.
- 🆕 **19 Agu — Datasheet Sistem konsolidasi dibuat** (`Deliverables/Datasheet_Sistem_GLD_Arsitektur_ServerJaringan.html`, redesain diagram-first rev 0.2): gabungan arsitektur end-to-end, spesifikasi hardware GLD/CH/Gateway, protokol radio, status ATEX/area berbahaya, kapabilitas gas/AI, **kebutuhan server & jaringan untuk tim IT Pertamina** (bag. 07), catu daya/instalasi, status gate. Ditemukan: repo `PertaminaGLD` sudah punya 2 dokumen integrasi jaringan siap pakai (`docs/manual/Gateway-to-Server-Site-IT-Pertamina.docx` & `...Technical-Datasheet.docx`, 13 Agu) — dirangkum apa adanya (masih berstatus draft/requirement, bukan konfigurasi live) ke bag. 07, bukan ditulis ulang dari nol. Detail sumber → `memory/entities.md` (repo:srv), `memory/deliverables.md`.
- ⚠️ **AI on-device: dikonfirmasi user (19 Agu), tapi BELUM diverifikasi dokumen tertulis** (audit sumber 19 Agu). Inferensi CNN Dual-Branch diklaim **sudah berjalan on-board di ESP32-S3 GLD**, bukan lagi PC+emulator — ini menggantikan status lama `blk:ai-edge`. Namun re-fetch source firmware terbaru yg bisa diperiksa (`PertaminaGLD/docs/design/gld/final_design.md`, mirror 29 Jun 2026) masih describe skema klasifikasi lama 6-kelas (clear/LPG/methane/propane/butane/anomaly), BUKAN 4-kelas CNN Dual-Branch — kemungkinan doc mirror belum update sejak integrasi CNN Dual-Branch (~29 Jul–9 Agu), tapi ini dugaan, bukan fakta terverifikasi. **Boleh dipakai di deliverable dengan catatan "dikonfirmasi user, belum dari dokumen tertulis"** (sudah diterapkan di Datasheet Sistem rev 0.5) — jangan hapus caveat itu sampai ada commit firmware/dokumen yg mengonfirmasi tertulis.
- 🆕 **19 Agu — Update besar Datasheet Sistem (rev 0.3):** (1) **Catu daya GLD final = 24VDC ≥2A/unit**, siap pasang; kabel+PSU disediakan RU/kilang; jalur baterai portable tetap berjalan terpisah, tidak menahan deployment (dec:39). (2) **Bracket GLD & CH+solar = L-bracket ref. Emerson** ke struktur existing; kilang siap bikin tiang baru bila perlu (dec:40). (3) **Gate baru**: sertifikasi solar panel hazardous (`gate:solar-cert`), keamanan baterai 18650 CH di kilang (`gate:ch-batt-safety`), tools/fastener bracket (`gate:bracket-tools`) — semua PIC LGU (dec:41). (4) **Arsitektur jaringan GW↔Server diperjelas**: MAC Gateway didaftarkan utk IP stabil, GW+server wajib satu jaringan, server/VM jadi web server intranet; pembagian kerja LGU (install broker+backend+frontend, installer satu-paket) vs Pertamina (sediakan server/VM + satukan jaringan) — `gate:net-registration` terbuka menunggu jawaban Pertamina (dec:42). (5) **Payload GW→broker**: alarm&normal <1KB, alarm push ~10 dtk / normal pull ~90 dtk (dec:43). (6) **Rekomendasi spek server/VM** diusulkan LGU (4 vCore/8GB/100GB/Ubuntu/PostgreSQL) — `gate:server-spec` menunggu konfirmasi Pertamina (dec:44). Detail lengkap → `memory/decisions.md` dec:38–44, `memory/blockers_metrics.md`.

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

## 4. Deliverable utama (`Deliverables/`)

- `Deliverables/Dashboard_GLD_ProjectManagement.html` — dashboard manajemen proyek (biru #2B5FCB + charcoal).
- `Deliverables/Laporan_Progres_ByDate_GLD.{html,md}` — laporan progres kronologis.
- `Deliverables/JSA_HSE_RU-IV_Cilacap_GLD.{html,md}` — draft JSA/HSE Cilacap (belum disahkan).
- `Deliverables/Knowledge_Graph_GLD.html` — knowledge graph interaktif (force-directed) dari `memory/graph.json`.
- `Deliverables/Datasheet_Sistem_GLD_Arsitektur_ServerJaringan.html` — datasheet konsolidasi untuk kilang/lapangan/IT: arsitektur, hardware, radio, ATEX, gas/AI, **server & jaringan**, catu daya, gate.
- `Deliverables/GLD_V2_Progress_Report_Jul2026.pptx`, `Deliverables/REPORT_GLD_V2_2026.md` — laporan pendukung lain.

Dokumen sumber (dari tim/klien) ada di `Sumber Dokumen/` — katalog lengkap → [`memory/files_catalog.md`](memory/files_catalog.md).
URL artifact & detail → [`memory/deliverables.md`](memory/deliverables.md).

## 5. Aturan kerja penting (jangan dilupakan)

- **Bahasa:** Bahasa Indonesia untuk semua deliverable.
- **Desain HTML:** palet **biru #2B5FCB + charcoal #262321** (client-facing), light+dark, self-contained.
- **Baseline Kurva-S:** dikalibrasi ke **Project Timeline 9 bulan (Deck Kick-Off)**.
- **Transparansi:** klien = partner → selalu tampilkan **progres + outstanding** secara jujur; jangan over-claim (analisis ≠ resolusi blocker).
- **OGI (YOLO/thermal) DIHAPUS** — belum disetujui. Jangan dimasukkan lagi tanpa arahan.
- **Inferensi AI**: ✅ **on-device dikonfirmasi (19 Agu)** — CNN Dual-Branch berjalan langsung di ESP32-S3 GLD (int8, 9,14 KB), bukan lagi PC/emulator. Boleh diklaim "AI di edge/on-device" untuk model ini. (Aturan lama di baris ini sebelumnya melarang klaim tsb — sudah supersede, lihat status singkat §2 dan `memory/blockers_metrics.md` blk:ai-edge.)
- **Jangkauan LoRa**: keterbatasan per-hop **disiasati mesh multi-hop** (sudah terbukti 8-CH). Bukan blocker keras.
- **Deviasi jadwal**: jangan over-claim. Selisih vs baseline = **sisi lab saja**; framing harus jujur & bersyarat.
- **Tema HTML (baru)**: biru **#2B5FCB** + charcoal **#262321** (logo Korporasi Kinarya ITB), bukan navy lagi.
- **Cilacap = RU IV** (bukan VI). Scope aktif hanya 1 RU.
- **Git:** kerja di branch `Codex/project-management-tracking-5l8ypx`; PR aktif = **PR #1**. Push = update PR.

## 6. Cara memelihara memory ini

Setiap ada informasi/keputusan/milestone baru: perbarui file `memory/` yang relevan **dan** `graph.json` bila menambah entitas/relasi, lalu ringkas ulang bagian "Status singkat" di atas. Lihat [`memory/README.md`](memory/README.md).
