# Timeline — Kronologi Milestone

Legenda: ✅ selesai · 🔵 milestone · ⚠️ temuan/blocker · 🔧 engineering

## Fase 1 — Lab (20 Apr – 7 Jun 2026), rencana mingguan M1–M7
- **M1 (20–26 Apr)** ✅ Desain chamber · uji node GLD lama · uji routing CH (CH_Hello/CH_Config).
- **M2 (27 Apr–3 Mei)** ✅ Uji node GLD baru (#0001/#0002; ADS1115, MCP3208 8ch, LoRa ok) · uji baterai CH (3 CH + 1 node).
- **M3 (4–10 Mei)** 🔧 Uji fungsional dimulai · chamber · uji solar→CH · firmware CH power-recovery-guard + WDT.
- **M4 (11–17 Mei)** 🔧 Uji jarak/reliabilitas · konsumsi baterai node (aktif 2m37s/sleep 3m).
- **M5–M6 (18–31 Mei)** 🔧 Uji sistem kampus · Site Survey Technical Checklist · evaluasi.
- **CH test (Mei)** 🔵 Topologi star-mesh Node→CH1→CH2→CH3/GW; **failover terbukti** (CH2 mati→CH1 re-parent ke GW, 0 loss).
- **RF LoRa (Mei–Jun)** ⚠️ Area terbuka 100 m @ −71 dBm PDR 100%; batas jangkauan −112 dBm PDR 26%.
- **M7 (1–7 Jun)** 🔧 Persiapan pemasangan.

## Fase 2 — Kick-off & menuju field (12 Jun – 23 Jul 2026)
- **12 Jun** 🔵 **Kick-Off Pertamina** — baseline 9 bulan, scope 6 RU, target Des, field test RU-VII Kasim.
- **18 Jun** Prinsip AI: fingerprint 8-sensor; TRL-7.
- **26 Jun** ⚠️ Antena LoRa 6 m maks ±100 m (spec 1–2 km); TCNN mulai.
- **30 Jun** Project Report June: PCB v1/v2 done; chamber assembly & dataset progress.
- **2 Jul** Repo tersebar → rencana konsolidasi.
- **6 Jul** 🔵 Uji 2 CH; charging 3,0→3,4 V; PJ chamber didapat.
- **6–8 Jul** Uji baterai CH LitoKala: 1 batt ~40 jam; lapangan CH3 8 hari.
- **9 Jul** 🔵 **Rantai komunikasi GLD-CH-GW-Server tersambung** (MQTT). Solar Vp 7,25 V belum optimal→rooftop.
- **13 Jul** ⚠️ Profil beban daya; catatan awal mode baterai (kelak diklarifikasi 16 Jul). Frontend: MapLibre + default RU IV.
- **14 Jul** Solar stabil ±4,17 V; discharge >14:00.
- **15 Jul** 🔵 Dataset 14.477 sampel; **TCN per-sensor 8 model ≥92%** (MQ4V 93,9%).
- **16 Jul** 🔵 **Uji fungsional GLD-CH-GW-Server hingga inferensi AI SELESAI.** Juga: **analisis daya lengkap** (GLD 7P=1,76 hari; CH 2 panel surplus; TPL5010 belum optimal), **uji mesh CH**, **uji downlink GLD** + fix firmware. Temuan O₂ vs CO₂; threshold per-MQ; aplikasi UI GLD.
- **17 Jul** Urutan kerja: LGU undang Pertamina ke lab → uji lab → RU.
- **20 Jul** Simulasi siklus ON 60/OFF 100/WAKE 160; arahan ganti DC converter; modifikasi baterai ditahan.
- **23 Jul** Repo server (PertaminaGLD) aktif: firmware + Operator Hub + TPL5010 + nulling. **Status per hari ini.**

## Rencana ke depan (baseline resmi)
Integration test (Sep) · HSE/permit (Nov) · **Field installation = target implementasi (Des)** · Field trial (Des–Jan) · Evaluation (Jan) · Industrialization roadmap (Feb 2027).
