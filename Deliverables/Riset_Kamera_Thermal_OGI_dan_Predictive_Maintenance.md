# Riset: Kamera Thermal untuk GLD — OGI Kebocoran Gas & Predictive Maintenance Pipa Kilang

*Dokumen kerja internal · 19 Oktober 2026 · bahan untuk video roadmap kamera thermal yang lebih panjang*

> **Status:** Semua isi dokumen ini adalah **roadmap/konsep**, belum diimplementasikan. Integrasi OGI Thermal Camera adalah proposal terpisah (Kontrak Payung, RAB Rp5.341.943.700, Feb 2026). Fungsi **predictive maintenance belum ada di proposal tersebut** — ini usulan perluasan yang perlu disepakati dulu.

---

## 1. Temuan utama (ringkas)

1. **Ada dua jenis kamera thermal yang berbeda fungsi** dan sering tertukar:
   - **OGI (Optical Gas Imaging)** — MWIR berpendingin, filter sempit ±3,3 µm. Fungsinya **memvisualisasikan plume gas hidrokarbon**. Tidak bisa membedakan jenis gas dan tidak mengukur konsentrasi.
   - **Termografi radiometrik** — umumnya LWIR 8–14 µm tanpa pendingin. Fungsinya **mengukur suhu permukaan per piksel**. Inilah yang dipakai untuk predictive maintenance (PdM).
2. **Proposal saat ini hanya mencakup OGI** (kebocoran gas, jangkauan target ±100 m, tiang ±10 m, PTZ ±60°, YOLOv8-seg di edge). PdM tidak disebut sama sekali.
3. **PdM berbasis termografi sudah dipraktikkan di kilang Pertamina**, tetapi secara **inspeksi berkala** (Pertamina Patra Niaga memakai termografi, UT thickness, sensor getaran, dan drone dalam program PdM kilang). Peluang GLD: **pemantauan kontinu dengan kamera tetap + analitik tren AI + satu dashboard dengan sensor GLD**, bukan menggantikan program inspeksi yang sudah ada.
4. **Satu kamera untuk dua fungsi tidak ideal.** Kamera usulan (HJK-MWIR MC11H) memang bisa mengukur suhu hingga 2000 °C dengan filter yang bisa diganti, tetapi pada operasi 24/7 filter gas harus terpasang terus. Pendingin Stirling juga punya umur servis terbatas (sumber menyebut rebuild sekitar 10.000–13.000 jam ≈ 14–18 bulan operasi kontinu). **Rekomendasi: arsitektur hibrida**, yaitu OGI berpendingin untuk zona prioritas kebocoran dan kamera radiometrik LWIR tanpa pendingin (lebih murah, tanpa cryocooler) untuk PdM.

## 2. OGI: apa yang bisa & tidak bisa

| Aspek | Fakta | Implikasi |
|---|---|---|
| Prinsip | Molekul ikatan C–H menyerap IR di ±3,3 µm sehingga plume tampak sebagai kontras terhadap latar | Cocok untuk metana, propana, butana, VOC |
| Sensitivitas | Kajian yang dihosting EPA: MWIR berpendingin (NETD 15 mK) mendeteksi propana ±11 ppm·m, LWIR tanpa pendingin (NETD 50 mK) ±1.060 ppm·m | OGI memang butuh kamera berpendingin |
| Batasan | Tidak membedakan jenis gas. Kinerja bergantung pada kontras termal, angin, laju bocor, kelembapan, dan garis pandang | Peran **GLD sebagai pengidentifikasi jenis gas tetap utama** |
| Gas non-hidrokarbon | H₂, CO, H₂S tidak terlihat di pita 3,3 µm | Kamera tidak menggantikan GLD untuk gas toksik dan hidrogen |
| Regulasi (AS) | EPA NSPS OOOOb Appendix K mengatur prosedur survei OGI. Menurut ringkasan vendor, saat ini berlaku untuk pengolahan gas alam, belum kilang | Bisa dikutip sebagai praktik baik, bukan kewajiban di Indonesia |

## 3. Predictive maintenance dengan termografi di kilang

Tingkat bukti: **[M]** = mapan/praktik umum industri · **[V]** = klaim vendor, belum terverifikasi independen · **[S]** = hanya cocok sebagai skrining awal.

| Aplikasi | Yang dideteksi | Bukti |
|---|---|---|
| **Fired heater / furnace tube** | Hot spot dinding tube, coking, flame impingement | [M] Di kilang Balikpapan, termografi video furnace/boiler dipakai sejak 2019 untuk mencegah tube pecah [V] |
| **Refraktori** (heater, reaktor, duct, stack) | Spalling, kerusakan lapisan tahan api sehingga panas tembus ke shell | [M] |
| **Isolasi pipa rusak/basah** | Kehilangan panas dan isolasi basah, indikator risiko **CUI (corrosion under insulation)** | [S] Termografi hanya menunjukkan isolasi basah, bukan korosinya. Konfirmasi tetap perlu UT/radiografi (rujukan API 583/570) |
| **Steam trap & steam tracing** | Trap gagal terbuka (uap bocor), gagal tertutup (dingin), tersumbat | [M]/[S] Untuk trap yang "passing", perlu dilengkapi ultrasonik |
| **Valve passing / PSV bocor ke flare header** | Pipa hilir yang seharusnya dingin menjadi hangat | [M] |
| **Tangki timbun** | Level cairan, lumpur (sludge), lapisan produk | [M] Studi kasus: kontraktor klaim 95% sludge terangkat, citra IR menunjukkan hanya ±60% |
| **Kelistrikan** (gardu, MCC, trafo, panel) | Sambungan longgar/panas berlebih | [M] Jurnal tentang Pertamina Hulu Mahakam: termografi efektif menekan biaya tak perlu |
| **Peralatan berputar** (pompa, motor, bearing, kopling) | Panas berlebih akibat gesekan atau misalignment | [M] |
| **AI tren termal kontinu** | Kenaikan suhu bertahap sebelum gagal, deteksi anomali per aset | [V] Banyak klaim vendor, belum ada data independen tentang lead time prediksi |

**Catatan teknis penting:**
- Pengukuran suhu IR dipengaruhi **emisivitas** permukaan (logam mengilap/berinsulasi aluminium memantul), sudut pandang, dan garis pandang.
- Untuk PdM, kamera **harus radiometrik** dan dikalibrasi. Interpretasinya idealnya oleh personel bersertifikasi termografi (ISO 18436-7).

## 4. Konsep integrasi dengan GLD (usulan)

```
              ┌──────────── Dashboard terpadu (ruang kontrol) ───────────┐
              │  Alarm gas GLD · Plume OGI · Tren suhu aset · Riwayat     │
              └───────▲───────────────────▲────────────────────▲─────────┘
                      │ event kecil        │ event + snapshot    │ tren suhu + alarm
     GLD ─► Cluster Head ─► Gateway    Edge server OGI       Edge server PdM
     (LoRa mesh, data kecil)          (Ethernet/fiber)      (Ethernet/fiber)
                                       ▲                     ▲
                              Kamera OGI MWIR        Kamera radiometrik LWIR
                              (zona prioritas bocor)  (heater, tangki, steam, listrik)
```

- **Video tidak lewat LoRa.** Bandwidth LoRa hanya cukup untuk data sensor dan event. Kamera butuh Ethernet/fiber ke edge server. Yang dikirim ke dashboard hanya event, snapshot, dan tren.
- **Korelasi lintas sumber (nilai tambah GLD):** alarm gas GLD + plume OGI + kenaikan suhu aset di lokasi yang sama memberi prioritas tinggi. Contoh: suhu flange naik bertahap lalu GLD mendeteksi LPG di dekatnya, menandakan bocor yang berawal dari kerusakan termal/seal.
- **Sertifikasi area berbahaya:** kamera di Zona 1/2 butuh housing Ex. Kamera tetap ber-ATEX/IECEx sudah tersedia di pasar, tetapi status radiometriknya perlu diverifikasi per produk.

## 5. Rancangan video roadmap kamera thermal (±3–4 menit)

Prinsip: jelas berlabel **"Pengembangan berikutnya / konsep"**, tanpa angka kinerja yang belum diuji (ROI >300% dan "pengurangan inspeksi 70%" di proposal **tidak dipakai** karena belum terverifikasi).

| # | Adegan | Durasi | Isi |
|---|---|---|---|
| 1 | Pembuka | 10 dtk | "GLD hari ini mendeteksi gas di titik. Berikutnya: melihat seluruh area." |
| 2 | Batas sensor titik | 20 dtk | Animasi: gas hanya terdeteksi bila sampai ke sensor; area di antara sensor tidak terpantau |
| 3 | Dua mata inframerah | 25 dtk | Perbedaan OGI (melihat gas) vs termografi radiometrik (mengukur suhu), dengan spektrum 3,3 µm vs 8–14 µm |
| 4 | OGI: melihat plume | 35 dtk | Kamera di tiang 10 m, patroli PTZ ±60°, AI segmentasi plume di edge, alarm terkonfirmasi visual |
| 5 | Orkestrasi alarm | 25 dtk | Tiga skenario: GLD saja / kamera saja / keduanya maka prioritas tinggi |
| 6 | Predictive maintenance | 45 dtk | Heater tube hot spot, isolasi basah (risiko CUI), steam trap, PSV passing, level/sludge tangki, panel listrik. Tren suhu naik, peringatan sebelum gagal |
| 7 | Satu dashboard | 20 dtk | Gas + plume + kesehatan aset dalam satu tampilan, terhubung ke program PdM yang sudah ada |
| 8 | Arsitektur & keselamatan | 20 dtk | LoRa untuk sensor, Ethernet/fiber untuk kamera, housing Ex, edge AI |
| 9 | Penutup | 15 dtk | Roadmap bertahap: pilot satu unit, lalu replikasi RU. Logo mitra |

Kebutuhan aset: render 3D kamera di tiang dan heater/tangki/pipa berinsulasi (Blender), klip ilustrasi plume dan citra thermal, narasi baru (1 permintaan TTS per bahasa).

## 6. Yang perlu diputuskan sebelum membuat video

1. **Apakah PdM resmi diusulkan masuk lingkup?** Saat ini belum ada di proposal OGI. Kalau masuk video tanpa kesepakatan, framing-nya harus "potensi pengembangan".
2. **Arsitektur kamera:** hibrida (OGI + radiometrik LWIR) atau satu kamera MWIR saja?
3. **Prioritas aplikasi PdM** yang paling relevan untuk RU IV (misalnya heater tube, steam trap, tangki).
4. **Audiens video:** manajemen Pertamina (strategis, ringan teknis) atau tim teknik/reliability (lebih detail)?

---

### Sumber
- Proposal internal: `Sumber Dokumen/[KONTRAK PAYUNG] PROPOSAL ... Integrasi Thermal Camera dan Multi-Modality ... (5340M).pdf` (44 hlm)
- [Pertamina Patra Niaga andalkan predictive maintenance kilang — JawaPos](https://www.jawapos.com/energi/2604010191/pertamina-patra-niaga-andalkan-predictive-maintenance-kilang-makin-andal-dan-efisien)
- [DURAG — Indonesian refinery optimizes burner operation (Balikpapan)](https://durag.com/en/optimization-of-burner-operation-in-refinery-4227.htm)
- [Jurnal: predictive maintenance termografi peralatan listrik PT PHM](https://journal.aritekin.or.id/index.php/Venus/article/view/960)
- [EPA — Detection limits of OGI (cooled vs uncooled)](https://19january2021snapshot.epa.gov/sites/static/files/2020-12/documents/detection_limits_of_ogi.pdf)
- [Opgal — Cooled vs uncooled OGI](https://www.opgal.com/blog/optical-gas-imaging-ogi/which-optical-gas-imaging-ogi-camera-should-i-use-cooled-vs-uncooled-ogi-technology/)
- [FLIR — NSPS OOOOb Appendix K](https://www.flir.com/discover/industrial/nsps-oooob-leak-detection/)
- [EPA — Appendix K presentation (2021)](https://www.epa.gov/system/files/documents/2021-12/appendix-k-presentation_final.12.14.21.pdf)
- [FLIR — Fixed-mount OGI camera](https://flir.asia/browse/industrial/gas-detection-cameras/fixed-cameras)
- [Infrared Training Center — Positive IR results in the refining industry](https://www.infraredtraining.com/en-US/home/resources/blog/positive-ir-results-in-the-refining-industry/)
- [FLIR — IR thermography inspection for extending asset lifetime](https://prodindustrial.flir.com/globalassets/industrial/instruments/ogi/infrared-thermography-inspection-for-extending-asset-lifetime-and-keeping-shutdowns-under-control/infrared-thermography-inspection-for-extending-asset-lifetime-and-keeping-shutdowns-under-control.pdf)
- [Acuren — Infrared thermography inspection services](https://www.acuren.com/wp-content/uploads/2023/08/Acuren-Infrared-Thermography-Inspection.pdf)
- [Infrared thermography in steam trap inspection (2021)](https://hrcak.srce.hr/289131)
- [SPIE — Nondestructive evaluation of steam traps](https://spiedigitallibrary.org/conference-proceedings-of-spie/3700/0000/Nondestructive-evaluation-of-steam-traps/10.1117/12.342296.full)
- [Inspenet — Thermal monitoring in industrial furnaces](https://inspenet.com/en/?p=323390)
- [iFactory — Thermal AI for refractory hot spot detection (vendor)](https://ifactoryapp.com/ai-vision-camera/thermal-ai-boiler-refractory-shell-hot-spot-detection)
- [Paten — CUI detection with thermography & machine learning](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11162888)
- [AMPP — CUI publications](https://store.ampp.org/producttag/124/corrosion-under-insulation)
- [Hikvision explosion-proof thermographic camera (contoh produk Ex)](https://www.securitywholesalers.com.au/product/hikvision-ds-2td2537t-10-q-explosion-proof-thermographic-network-bullet-camera/)
