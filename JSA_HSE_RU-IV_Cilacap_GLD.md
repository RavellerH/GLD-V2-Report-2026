# DRAFT — JSA / TRA & HSE PLAN: INSTALASI GAS LEAK DETECTION (GLD) — RU IV CILACAP

> 📝 **DOKUMEN DRAFT — Rev 0.** Kerangka awal untuk mempercepat penyusunan TRA/JSA. **Belum disahkan.** Wajib direview, dilengkapi (klasifikasi area, nomor izin, kontak darurat), dan ditandatangani **Tim HSE RU IV Cilacap** serta mengikuti sistem Permit-to-Work Pertamina sebelum dipakai di lapangan. Bukan pengganti prosedur HSE resmi RU.

| | |
|---|---|
| **Lokasi** | RU IV Cilacap (PT Kilang Pertamina Internasional) |
| **Scope** | Survei · Instalasi · Pengujian GLD (3 sensor · 2 CH · 1 GW) |
| **Pelaksana** | LGU / pihak ke-3 + ITB |
| **Klasifikasi area** | ⚠ Dikonfirmasi RU (Zona 0/1/2) |
| **Izin kerja (PTW)** | Cold · Hot · Work-at-Height (No: ____) |
| **Disusun / Revalidasi** | 23 Jul 2026 / bila task, lokasi, cuaca, atau crew berubah |

**Matriks risiko (L×S):** Rendah 1–4 · Sedang 5–9 · Tinggi 10–15 · Ekstrem 16–25.

---

## A. Prasyarat & Persyaratan HSE Umum

Tidak ada pekerjaan dimulai sebelum seluruh prasyarat terpenuhi dan izin kerja disahkan RU.

- **Permit-to-Work (PTW)** disahkan RU per jenis kerja: cold work (survei), work-at-height (tiang/rooftop), hot work (pengeboran/energized di area terklasifikasi).
- **Konfirmasi klasifikasi area** tiap titik pasang ke HSE RU. Di zona terklasifikasi gunakan alat/perangkat **Ex / Intrinsically-Safe**; energize & commissioning di area aman atau di bawah izin energized-work — selaras SPK sertifikasi hazardous area.
- **Gas test** sebelum & selama kerja; monitoring kontinu **personal 4-gas detector** (LEL/O₂/H₂S/CO). Stop bila LEL melewati ambang izin.
- **Kompetensi:** personel bersertifikat kerja di ketinggian, kelistrikan, penanganan gas. **Toolbox talk** + sign-on JSA tiap shift.
- **Escort & komunikasi RU;** check-in radio/HP; **dilarang lone working** di ketinggian & zona terklasifikasi.
- **SIMOPS:** koordinasi control room sebelum & selama kerja yang dapat memicu alarm/operasi.
- **APD dasar:** coverall anti-statik, safety helmet, safety shoes, safety glasses; ditambah per tugas (harness, sarung tangan, ear/dust protection, H₂S escape set).
- **Cuaca & heat stress:** batas angin untuk kerja ketinggian; hidrasi & rotasi (iklim tropis Cilacap).
- **Housekeeping & limbah;** penutupan izin setelah selesai.

---

## B. Lembar JSA per Aktivitas

Kolom: Langkah · Bahaya · Risiko Awal (L×S) · Pengendalian · APD/PJ · Risiko Sisa.

### JSA-01 · Survei Lapangan & Walkdown RF
*Cold work permit · gas monitoring kontinu · escort RU*

| # | Langkah | Bahaya | Awal | Pengendalian | Sisa |
|---|---|---|:--:|---|:--:|
| 1 | Mobilisasi & masuk area RU | Akses tanpa izin; disorientasi; lalu-lintas plant | 6 | Safety induction; ID/escort; PTW cold work; jalur pejalan & rambu | 2 |
| 2 | Walkdown area proses (zona gas) | Atmosfer mudah terbakar/toksik (H₂, LPG, H₂S) | **20** | Gas test kontinu (4-gas); stop bila LEL > ambang; hindari sumber nyala; upwind | 8 |
| 3 | Uji RF LoRa (perangkat portabel) | Perangkat non-Ex = sumber nyala di area terklasifikasi | **20** | Konfirmasi zona; perangkat Ex/IS atau uji di area aman; izin energized | 8 |
| 4 | Penandaan titik & ukur ketinggian | Kejatuhan benda; struktur tinggi | 6 | Barikade; no work di bawah beban; spotter | 2 |
| 5 | Dokumentasi foto | Kamera non-Ex = sumber nyala | 15 | Izin foto; kamera Ex / area aman | 3 |
| 6 | Demobilisasi | Barang tertinggal; izin tak ditutup | 2 | Housekeeping; lapor selesai; tutup PTW | 1 |

### JSA-02 · Instalasi Cluster Head & Tiang 6 m (Kerja di Ketinggian)
*Work-at-height + hot work permit · rescue plan · batas angin*

| # | Langkah | Bahaya | Awal | Pengendalian | Sisa |
|---|---|---|:--:|---|:--:|
| 1 | Inspeksi alat angkat/tangga/harness | Alat rusak → gagal saat kerja | 12 | Inspeksi pre-use bertag; alat tersertifikasi; afkir alat cacat | 3 |
| 2 | Manual handling tiang & panel | Cedera punggung; terjepit | 9 | Team-lift; teknik angkat; batas beban | 4 |
| 3 | Base plate & anchor (pengeboran) | Spark/hot work; debu; bising | **20** | Hot work permit + gas test; exclusion; masker; ear protection; fire watch | 8 |
| 4 | Mendirikan tiang 6 m | Jatuh; tiang roboh; kontak overhead line | **20** | Work-at-height permit; tag line; exclusion; cek overhead; stop bila angin > batas | 8 |
| 5 | Pasang CH & bracket solar di atas | Jatuh personel/alat | **20** | 100% tie-off ke anchor sah; tool lanyard; MEWP/scaffold; rescue plan | 8 |
| 6 | Wiring solar & charge controller | Listrik DC/arc; baterai 18650 | 12 | LOTO; insulated tools; tutup PV saat wiring; cegah short | 3 |
| 7 | Grounding & sealing IP66/67 | Grounding buruk; ingress air | 6 | Verifikasi kontinuitas grounding; cable gland IP68 | 2 |

### JSA-03 · Pemasangan Sensor Node & Elektrikal/Kabel
*Cold/energized-work permit · gas test · Ex compliance*

| # | Langkah | Bahaya | Awal | Pengendalian | Sisa |
|---|---|---|:--:|---|:--:|
| 1 | Pasang enclosure sensor (valve/flange) | Dekat sumber bocor; atmosfer eksplosif | **20** | Gas test; PTW; Ex compliance; jangan ganggu sumber bocor; koordinasi operasi | 8 |
| 2 | Penarikan kabel & conduit | Trip; manual handling; dekat piping | 6 | Routing di-clamp; gland IP68; barikade; housekeeping | 2 |
| 3 | Koneksi PSU 24/5 VDC | Sengatan listrik; arc | 12 | LOTO; verifikasi dead; insulated tools | 3 |
| 4 | Energize & commissioning | Spark saat energize di zona | **20** | Energize di area aman / izin energized-work; pastikan no-gas | 8 |
| 5 | Uji fungsional & alarm | False trigger ganggu operasi | 6 | Koordinasi control room; jadwalkan; kelola SIMOPS | 2 |

### JSA-04 · Pengujian Gas & Kalibrasi
*Ventilasi · no ignition · handling tabung bertekanan*

| # | Langkah | Bahaya | Awal | Pengendalian | Sisa |
|---|---|---|:--:|---|:--:|
| 1 | Handling tabung gas uji (LPG/test gas) | Tekanan tinggi; kebocoran; flammable | **20** | Tabung tegak & terikat; regulator sesuai; leak check sabun; no ignition; ventilasi | 8 |
| 2 | Aliran gas ke chamber/sensor | Pelepasan gas flammable; penumpukan | **20** | Ventilasi/exhaust; gas monitor; volume minimum; no rokok/hot work | 8 |
| 3 | Purging & pembuangan | Sisa gas terperangkap | 12 | Purge udara/inert; buang ke area aman berventilasi | 3 |
| 4 | Penyimpanan tabung | Jatuh; panas; dekat oxidizer | 8 | Berventilasi; tegak terikat; jauh oxidizer & sumber panas | 2 |

---

## C. Rencana Tanggap Darurat (ERP)

- **🟥 Alarm gas / kebocoran:** hentikan kerja; isolasi sumber nyala; evakuasi **upwind** ke muster; lapor control room & HSE; jangan kembali sebelum aman.
- **🟧 Kebakaran:** bunyikan alarm; evakuasi; APAR sesuai kelas — **baterai lithium pakai media Class D/khusus**; serahkan ke ERT bila di luar kendali.
- **🟨 Cedera / jatuh:** aktifkan **rescue plan** ketinggian (rescue < batas waktu suspensi); P3K; jangan pindahkan korban cedera tulang tanpa medis.
- **📞 Kontak darurat (isi per RU):** Control Room RU IV ____ · HSE/ERT ____ · Medical ____ · Project Lead LGU ____ · Muster point ____.

---

## D. Persetujuan & Tanda Tangan

| Peran | Pihak | Nama · Tanda tangan · Tgl |
|---|---|---|
| Disusun | Tim LGU / ITB | __________ |
| Ditinjau | Field / Engineering Lead | __________ |
| Disahkan HSE | HSE RU IV Cilacap | __________ |
| Permit Issuer | Area Authority RU IV | __________ |

---

*Kerangka disusun sebagai input percepatan berdasarkan dokumen proyek GLD (Deck Kick-Off — HSE Philosophy, PTW Plan, Task Risk Assessment; Dokumen Kebutuhan Peralatan per RU; MoM RU IV Cilacap). Nilai risiko indikatif & wajib divalidasi tim HSE RU. DRAFT Rev 0 · 23 Juli 2026.*
