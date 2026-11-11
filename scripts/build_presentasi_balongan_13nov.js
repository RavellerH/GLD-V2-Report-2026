/**
 * Generator deck presentasi: Koordinasi & Persiapan Implementasi GLD di RU VI Balongan (13 Nov 2026).
 *
 * Output : Deliverables/Presentasi_Koordinasi_Implementasi_GLD_RU-VI_Balongan_13November2026.pptx
 * Palet  : biru #2B5FCB + charcoal #262321 (aturan kerja repo).
 * Jalankan: NODE_PATH=<lokasi node_modules pptxgenjs> node scripts/build_presentasi_rapat_koordinasi_29sep.js
 */

const path = require("path");
const PptxGenJS = require("pptxgenjs");

const OUT = path.resolve(__dirname, "..", "Deliverables",
  "Presentasi_Koordinasi_Implementasi_GLD_RU-VI_Balongan_13November2026.pptx");

// ---------------------------------------------------------------- palet
const BLUE = "2B5FCB";
const BLUE_DK = "1E4499";
const CHAR = "262321";
const CHAR_SOFT = "4A4642";
const SURF = "F2F5FC";
const SURF_2 = "E7ECF8";
const LINE = "D5DCEC";
const WHITE = "FFFFFF";
const MUTED = "6E6A66";
const WARN = "B4520F";
const WARN_BG = "FBEEE4";
const OK = "1F7A43";
const OK_BG = "E6F2EB";
const HOLD = "7A6A18";
const HOLD_BG = "F6F1DC";
const PERTAMINA = "2E5F8A";
const PERTAMINA_BG = "E7EFF6";
const VENDOR = "8A4A15";
const VENDOR_BG = "F5EBE1";

const FONT = "Calibri";
const SERIF = "Cambria";

const W = 13.333, H = 7.5;
const M = 0.62;

const pres = new PptxGenJS();
pres.layout = "LAYOUT_WIDE";
pres.author = "LAPI Ganesha Utama";
pres.company = "PT LAPI Ganesha Utama";
pres.title = "Koordinasi & Persiapan Implementasi GLD — RU VI Balongan";

// ---------------------------------------------------------------- helper
function shadow() {
  return { type: "outer", color: "1A2740", blur: 10, offset: 2, angle: 90, opacity: 0.10 };
}
function slideLight() {
  const s = pres.addSlide();
  s.background = { color: WHITE };
  return s;
}
function slideDark() {
  const s = pres.addSlide();
  s.background = { color: CHAR };
  return s;
}
function heading(s, kicker, title, opts = {}) {
  const y = opts.y === undefined ? 0.46 : opts.y;
  s.addText(kicker.toUpperCase(), {
    x: M, y: y, w: 10.5, h: 0.26, isTextBox: true, margin: 0,
    fontFace: FONT, fontSize: 11, bold: true, charSpacing: 1.6, color: BLUE,
  });
  s.addText(title, {
    x: M, y: y + 0.28, w: opts.w || 11.9, h: opts.h || 0.66, isTextBox: true, margin: 0,
    fontFace: SERIF, fontSize: opts.size || 29, bold: true, color: CHAR, valign: "top",
  });
}
function footnote(s, text, y) {
  s.addText(text, {
    x: M, y: y === undefined ? 6.9 : y, w: W - 2 * M, h: 0.34, isTextBox: true, margin: 0,
    fontFace: FONT, fontSize: 9.5, italic: true, color: MUTED, valign: "top",
  });
}
function card(s, x, y, w, h, fill) {
  s.addShape(pres.ShapeType.roundRect, {
    x, y, w, h, rectRadius: 0.07,
    fill: { color: fill || SURF }, line: { color: LINE, width: 0.75 }, shadow: shadow(),
  });
}
function chip(s, x, y, label, fg, bg, w) {
  const width = w || 1.4;
  s.addShape(pres.ShapeType.roundRect, {
    x, y, w: width, h: 0.27, rectRadius: 0.13,
    fill: { color: bg }, line: { color: bg },
  });
  s.addText(label, {
    x, y, w: width, h: 0.27, isTextBox: true, margin: 0,
    fontFace: FONT, fontSize: 9.5, bold: true, color: fg, align: "center", valign: "middle",
  });
}
function badge(s, x, y, n, d, color) {
  const dia = d || 0.44;
  s.addShape(pres.ShapeType.ellipse, {
    x, y, w: dia, h: dia, fill: { color: color || BLUE }, line: { color: color || BLUE },
  });
  s.addText(String(n), {
    x, y, w: dia, h: dia, isTextBox: true, margin: 0,
    fontFace: FONT, fontSize: 14, bold: true, color: WHITE, align: "center", valign: "middle",
  });
}
/** Progress bar horizontal dengan penanda rencana (opsional). */
function progressBar(s, x, y, w, pct, planPct, color) {
  const h = 0.22;
  s.addShape(pres.ShapeType.roundRect, {
    x, y, w, h, rectRadius: 0.05, fill: { color: "E7EBEE" }, line: { color: "E7EBEE" },
  });
  s.addShape(pres.ShapeType.roundRect, {
    x, y, w: Math.max(w * (pct / 100), 0.06), h, rectRadius: 0.05,
    fill: { color: color || BLUE }, line: { color: color || BLUE },
  });
  if (planPct !== undefined) {
    const px = x + w * (planPct / 100);
    s.addShape(pres.ShapeType.line, {
      x: px, y: y - 0.05, w: 0, h: h + 0.1, line: { color: CHAR, width: 1.25, dashType: "dash" },
    });
  }
}
function prioTag(s, x, y, level) {
  const map = { P1: ["C0392B", "FCE7E4"], P2: [HOLD, HOLD_BG], P3: ["5B7A90", "E9EEF2"] };
  const [fg, bg] = map[level];
  chip(s, x, y, level, fg, bg, 0.5);
}

// ---------------------------------------------------------------- helper tambahan
const ASSET = (p) => path.resolve(__dirname, "assets", p);
function bullets(s, x, y, w, h, items, size, color) {
  s.addText(items.map((t) => ({ text: t, options: { bullet: { indent: 14 }, breakLine: true } })), {
    x, y, w, h, isTextBox: true, margin: 0, valign: "top",
    fontFace: FONT, fontSize: size || 12, color: color || CHAR_SOFT, paraSpaceAfter: 5, lineSpacingMultiple: 1.05,
  });
}
function cardTitle(s, x, y, w, title, color) {
  s.addText(title, {
    x, y, w, h: 0.34, isTextBox: true, margin: 0,
    fontFace: FONT, fontSize: 14, bold: true, color: color || CHAR,
  });
}
function table(s, rows, opts) {
  const head = rows[0].map((t) => ({
    text: t, options: { bold: true, color: WHITE, fill: { color: opts.headColor || CHAR }, fontSize: opts.size || 11 },
  }));
  const body = rows.slice(1).map((r, i) => r.map((t, j) => ({
    text: t, options: {
      fill: { color: i % 2 ? WHITE : SURF }, fontSize: opts.size || 11,
      bold: opts.boldFirst && j === 0, color: CHAR,
    },
  })));
  s.addTable([head, ...body], {
    x: opts.x, y: opts.y, w: opts.w, colW: opts.colW, fontFace: FONT,
    border: { type: "solid", pt: 0.5, color: LINE }, margin: [3, 6, 3, 6], valign: "middle",
    rowH: opts.rowH,
  });
}
const SRC = "Sumber: dokumen teknis GLD V2 (TDS Rev 4.0 & dokumen teknis sertifikasi), Spesifikasi Material Instalasi rev 1.5, tabel alokasi perangkat per RU.";

// ================================================================ 1 · sampul
(function cover() {
  const s = slideDark();
  s.addShape(pres.ShapeType.ellipse, {
    x: 9.5, y: -1.9, w: 6.2, h: 6.2, fill: { color: BLUE_DK, transparency: 68 }, line: { color: BLUE_DK, transparency: 68 },
  });
  s.addShape(pres.ShapeType.ellipse, {
    x: 11.0, y: 3.6, w: 3.4, h: 3.4, fill: { color: BLUE, transparency: 80 }, line: { color: BLUE, transparency: 80 },
  });
  s.addText("PT LAPI GANESHA UTAMA  ·  LAB IoT & FISIKA ITB", {
    x: M, y: 0.92, w: 9.5, h: 0.3, isTextBox: true, margin: 0,
    fontFace: FONT, fontSize: 11.5, bold: true, charSpacing: 1.8, color: "9FB4E6",
  });
  s.addText("Koordinasi & Persiapan Implementasi\nGas Leak Detection (GLD) — RU VI Balongan", {
    x: M, y: 1.45, w: 11.5, h: 1.9, isTextBox: true, margin: 0,
    fontFace: SERIF, fontSize: 36, bold: true, color: WHITE, lineSpacing: 42,
  });
  s.addText("Pengenalan sistem & fitur GLD, kebutuhan instalasi di site, dan persiapan site survey awal — field testing multi-modality gas leak detector, co-research PT Pertamina Patra Niaga & Institut Teknologi Bandung melalui LAPI Ganesha Utama.", {
    x: M, y: 3.5, w: 10.2, h: 0.95, isTextBox: true, margin: 0,
    fontFace: FONT, fontSize: 14, color: "CFD8EA", lineSpacing: 20,
  });
  s.addShape(pres.ShapeType.roundRect, {
    x: M, y: 4.7, w: 6.6, h: 0.6, rectRadius: 0.1, fill: { color: BLUE }, line: { color: BLUE },
  });
  s.addText("Jumat, 13 November 2026  ·  09.00–11.00 WIB  ·  Zoom", {
    x: M + 0.2, y: 4.7, w: 6.2, h: 0.6, isTextBox: true, margin: 0,
    fontFace: FONT, fontSize: 13, bold: true, color: WHITE, valign: "middle",
  });
  s.addText("Terbuka juga untuk PIC RU II, RU III, RU V dan RU VII", {
    x: M, y: 5.45, w: 8.6, h: 0.3, isTextBox: true, margin: 0,
    fontFace: FONT, fontSize: 11, color: "8E9AB4",
  });
  s.addNotes("Pembuka: terima kasih kepada Bu Putu dan tim RU VI Balongan. Persiapan Balongan berjalan paralel sambil menunggu proses di RU IV Cilacap. Tujuan rapat: (1) memperkenalkan sistem dan fitur GLD, (2) menyampaikan kebutuhan instalasi di site, (3) menyepakati rencana site survey awal. Persiapan yang sama berlaku untuk RU lain, sehingga PIC RU lain dipersilakan menyimak.");
})();

// ================================================================ 2 · agenda
(function agenda() {
  const s = slideLight();
  heading(s, "Agenda", "Lima hal yang akan kita bahas");
  const items = [
    ["1", "Program GLD Tahap 2 & posisi RU VI", "Ringkas: cakupan 6 RU, alokasi perangkat, status RU IV Cilacap sebagai acuan."],
    ["2", "Sistem & fitur GLD", "Arsitektur, fitur unit GLD, Cluster Head, Gateway, dashboard, dan hasil pengujian."],
    ["3", "Kebutuhan instalasi di site", "Pembagian tanggung jawab, infrastruktur fisik, catu daya, server & jaringan."],
    ["4", "Penempatan titik & sertifikasi", "Klasifikasi area berbahaya, status sertifikasi Ex, penyesuaian gas per RU."],
    ["5", "Rencana site survey & hal yang perlu dikonfirmasi", "Tahapan, persiapan survey, daftar konfirmasi untuk RU VI (dan RU lain)."],
  ];
  items.forEach((it, i) => {
    const y = 1.65 + i * 1.0;
    badge(s, M, y, it[0], 0.5);
    s.addText(it[1], {
      x: M + 0.75, y: y - 0.06, w: 10.8, h: 0.4, isTextBox: true, margin: 0,
      fontFace: FONT, fontSize: 17, bold: true, color: CHAR,
    });
    s.addText(it[2], {
      x: M + 0.75, y: y + 0.34, w: 10.8, h: 0.45, isTextBox: true, margin: 0,
      fontFace: FONT, fontSize: 12.5, color: CHAR_SOFT,
    });
  });
  s.addNotes("Durasi 2 jam: ±50 menit presentasi LGU (bagian 1–4), ±40 menit diskusi kebutuhan & konfirmasi, ±20 menit penjadwalan site survey.");
})();

// ================================================================ 3 · program & posisi RU VI
(function program() {
  const s = slideLight();
  heading(s, "1 · Program", "GLD Tahap 2 — enam Refinery Unit, RU VI menyusul RU IV");
  card(s, M, 1.65, 5.6, 4.95, SURF);
  cardTitle(s, M + 0.3, 1.85, 5.0, "Posisi program saat ini");
  const rows = [
    ["RU VII Kasim", "GLD V1 telah diuji di lapangan (Desember 2025)."],
    ["RU IV Cilacap", "Site survey selesai (Agu 2026); MoC field test area SRU terbit (Nov 2026). Infrastruktur pendukung disiapkan lebih dulu, pemasangan GLD menunggu sertifikat Ex."],
    ["RU VI Balongan", "Persiapan dimulai paralel — rapat ini, lalu site survey awal."],
    ["RU II, III, V", "Menyusul dengan pola persiapan yang sama."],
  ];
  rows.forEach((r, i) => {
    const y = 2.35 + i * 1.03;
    chip(s, M + 0.3, y, r[0], WHITE, i === 2 ? BLUE : CHAR_SOFT, 1.55);
    s.addText(r[1], {
      x: M + 2.0, y: y - 0.05, w: 3.45, h: 0.95, isTextBox: true, margin: 0,
      fontFace: FONT, fontSize: 11, color: CHAR_SOFT, valign: "top",
    });
  });
  cardTitle(s, 6.65, 1.7, 6.0, "Alokasi perangkat per RU (rencana)");
  table(s, [
    ["Refinery Unit", "GLD", "Cluster Head", "Gateway"],
    ["RU II Dumai", "10", "3", "1"],
    ["RU III Plaju", "4", "3", "1"],
    ["RU IV Cilacap", "3", "2", "1"],
    ["RU V Balikpapan", "2", "1", "1"],
    ["RU VI Balongan", "4", "2", "2"],
    ["RU VII Kasim", "5", "11", "1"],
    ["Total", "28", "22", "7"],
  ], { x: 6.65, y: 2.1, w: 6.05, colW: [2.45, 1.1, 1.4, 1.1], size: 12, boldFirst: true, rowH: 0.42 });
  s.addShape(pres.ShapeType.rect, { x: 6.65, y: 2.1 + 0.42 * 5, w: 6.05, h: 0.42, fill: { color: BLUE, transparency: 85 }, line: { color: BLUE, width: 1.5 } });
  s.addText("Jumlah dan lokasi final per RU ditetapkan setelah site survey; tiap RU juga mendapat 1 PC server lokal (disediakan RU).", {
    x: 6.65, y: 5.6, w: 6.05, h: 0.7, isTextBox: true, margin: 0, fontFace: FONT, fontSize: 11, italic: true, color: MUTED,
  });
  footnote(s, "Sumber alokasi: tabel alokasi perangkat per RU (3 Nov 2026) & dokumen Kebutuhan Peralatan GLD per RU.");
  s.addNotes("RU VI Balongan direncanakan 4 GLD, 2 Cluster Head, 2 Gateway. Angka ini rencana awal — jumlah CH/GW bisa berubah setelah survey jangkauan radio. Pengalaman RU IV Cilacap menjadi acuan persiapan Balongan, terutama soal klasifikasi area dan MoC.");
})();

// ================================================================ 4 · arsitektur
(function arsitektur() {
  const s = slideLight();
  heading(s, "2 · Sistem", "Arsitektur sistem — berjalan lokal, tanpa internet");
  s.addImage({ path: ASSET("rapat_22okt/block_diagram.jpg"), x: M, y: 1.6, w: 7.9, h: 7.9 * 819 / 1600 });
  s.addText("Block diagram final: area FIELD (lapangan) dan BUILDING (gedung). Biru = disuplai LGU, kuning = instalasi, mounting & infrastruktur oleh Pertamina.", {
    x: M, y: 1.6 + 7.9 * 819 / 1600 + 0.06, w: 8.3, h: 0.4, isTextBox: true, margin: 0, fontFace: FONT, fontSize: 10, italic: true, color: MUTED,
  });
  const steps = [
    ["GLD", "Deteksi gas & klasifikasi AI di dalam unit, alarm lokal"],
    ["Cluster Head", "Relay LoRa mesh, tenaga surya, tanpa kabel daya"],
    ["Gateway", "Di dalam ruangan; antena di mast luar"],
    ["Router → PC server", "Wi-Fi lokal → LAN; MQTT broker + dashboard"],
    ["Intranet kantor", "LAN kedua PC: akses dashboard/API saja"],
  ];
  steps.forEach((st, i) => {
    const y = 1.6 + i * 0.98;
    badge(s, 9.25, y, i + 1, 0.42);
    s.addText(st[0], { x: 9.8, y: y - 0.04, w: 3.0, h: 0.3, isTextBox: true, margin: 0, fontFace: FONT, fontSize: 13, bold: true, color: CHAR });
    s.addText(st[1], { x: 9.8, y: y + 0.27, w: 3.0, h: 0.6, isTextBox: true, margin: 0, fontFace: FONT, fontSize: 10.5, color: CHAR_SOFT, valign: "top" });
  });
  card(s, M, 6.25, 12.1, 0.55, OK_BG);
  s.addText("Sistem bersifat standalone & advisory — tidak tersambung ke F&G/DCS kilang dan tidak memerlukan koneksi internet.", {
    x: M + 0.25, y: 6.25, w: 11.6, h: 0.55, isTextBox: true, margin: 0, fontFace: FONT, fontSize: 12, bold: true, color: OK, valign: "middle",
  });
  s.addNotes("Alur data: GLD → LoRa → CH → LoRa mesh → antena Gateway → Gateway di dalam ruangan → Wi-Fi → router LGU → kabel Cat6 → PC server. PC punya port LAN kedua ke intranet kantor hanya untuk akses dashboard/API, tidak meneruskan lalu lintas antar jaringan. Posisi ini sama dengan yang tertulis di MoC RU IV.");
})();

// ================================================================ 5 · fitur GLD
(function fitur() {
  const s = slideLight();
  heading(s, "2 · Sistem", "Fitur unit GLD (Node Sensor) V2");
  s.addImage({ path: ASSET("assembly_photos_0710/IMG_14.35.32.jpg"), x: M, y: 1.65, w: 4.3, h: 4.3 * 737 / 1000 });
  s.addText("GLD V2: housing aluminium die-cast, mesh sensor di depan, antena LoRa, beacon alarm.", {
    x: M, y: 1.65 + 4.3 * 737 / 1000 + 0.08, w: 4.3, h: 0.5, isTextBox: true, margin: 0, fontFace: FONT, fontSize: 10, italic: true, color: MUTED,
  });
  const feats = [
    ["Multi-sensor 8 kanal", "8 sensor gas MOS (MQ-2, 3B, 4, 5, 6, 7B, 8, 135) dibaca bersamaan — pola respons gabungan, bukan satu sensor tunggal."],
    ["AI di dalam perangkat", "Klasifikasi Clean Air / LPG / H₂ langsung di ESP32-S3; akurasi validasi lab >99%, waktu komputasi <166 ms."],
    ["Alarm lokal & ke server", "Beacon visual + audible di unit; alarm dikirim otomatis ke server (siklus ±10 detik) tanpa menunggu permintaan."],
    ["Komunikasi LoRa mesh", "920–923 MHz; jarak per-hop diperpanjang lewat Cluster Head multi-hop (teruji 8 CH)."],
    ["Antarmuka RS-485", "Modbus RTU read-only — status, hasil klasifikasi & confidence dapat dibaca sistem lain bila diperlukan."],
    ["Catu daya 24 VDC", "Konsumsi maks. ±8 W (≈0,33 A); unit tidak menerima 220 VAC — PSU di luar unit."],
  ];
  feats.forEach((f, i) => {
    const col = i % 2, row = Math.floor(i / 2);
    const x = 5.25 + col * 3.85, y = 1.65 + row * 1.6;
    card(s, x, y, 3.7, 1.45, SURF);
    s.addText(f[0], { x: x + 0.2, y: y + 0.12, w: 3.3, h: 0.3, isTextBox: true, margin: 0, fontFace: FONT, fontSize: 13, bold: true, color: BLUE });
    s.addText(f[1], { x: x + 0.2, y: y + 0.45, w: 3.3, h: 0.95, isTextBox: true, margin: 0, fontFace: FONT, fontSize: 11.5, color: CHAR_SOFT, valign: "top" });
  });
  footnote(s, "Kelas gas yang diklasifikasi saat ini: Clean Air, LPG, H₂. Gas lain (mis. H₂S, CO, metana) ditambahkan lewat pengambilan dataset di lokasi — lihat slide penyesuaian gas per RU.");
  s.addNotes("Tekankan keunggulan multi-sensor + AI: pola 8 sensor sekaligus untuk mengenali jenis gas dan mengurangi false alarm. Jujur bahwa kelas gas saat ini 3 (Clean Air, LPG, H2); gas tambahan per RU memerlukan dataset dari chamber di lokasi.");
})();

// ================================================================ 6 · spesifikasi
(function spesifikasi() {
  const s = slideLight();
  heading(s, "2 · Sistem", "Spesifikasi teknis GLD V2");
  const L = [
    ["Parameter", "Nilai"],
    ["Sensor gas", "8 kanal MOS: MQ-2, MQ-3B, MQ-4, MQ-5, MQ-6, MQ-7B, MQ-8, MQ-135"],
    ["Pemrosesan", "ESP32-S3-WROOM-1U (AI on-device)"],
    ["Kelas gas (AI)", "Clean Air, LPG, H₂"],
    ["Radio", "LoRa E22-900MM22S, 920–923 MHz, 17 dBm operasional"],
    ["Antena", "Eksternal 3 dBi omni, SMA"],
    ["Antarmuka kabel", "RS-485 / Modbus RTU (read-only)"],
    ["Alarm lokal", "Modul visual + audible (beacon)"],
  ];
  const R = [
    ["Parameter", "Nilai"],
    ["Catu daya", "24 VDC; konsumsi maks. ±8 W"],
    ["Housing", "Aluminium die-cast ADC12 + stainless steel"],
    ["Dimensi / berat", "200 × 90 × 290 mm / 2,378 kg"],
    ["Cable entry", "M20 × 1,5 (cable gland Ex d)"],
    ["Mounting", "Pelat U-bolt 250×250 mm ke pipa 2\" (OD 60,3 mm)"],
    ["Lingkungan", "−20 s/d +60 °C (rentang desain, dalam verifikasi); 5–95 %RH"],
    ["Proteksi", "IP66 (target, belum diuji)"],
  ];
  table(s, L, { x: M, y: 1.65, w: 5.95, colW: [1.7, 4.25], size: 11, boldFirst: true, rowH: 0.5 });
  table(s, R, { x: 6.75, y: 1.65, w: 5.95, colW: [1.6, 4.35], size: 11, boldFirst: true, rowH: 0.5 });
  card(s, M, 5.85, 12.1, 0.75, WARN_BG);
  s.addText("Usulan klasifikasi sertifikasi: II 2G Ex db IIC T4 Gb (Zona 1). Berkas sedang berproses di lembaga sertifikasi — sertifikat belum terbit; status lengkap di slide sertifikasi.", {
    x: M + 0.25, y: 5.85, w: 11.6, h: 0.75, isTextBox: true, margin: 0, fontFace: FONT, fontSize: 11.5, bold: true, color: WARN, valign: "middle",
  });
  footnote(s, SRC);
  s.addNotes("Angka mengikuti dokumen teknis terbaru. Item bertanda target/verifikasi (IP66, rentang suhu) disampaikan apa adanya.");
})();

// ================================================================ 7 · CH, GW, dashboard
(function chgw() {
  const s = slideLight();
  heading(s, "2 · Sistem", "Cluster Head, Gateway & dashboard");
  s.addImage({ path: ASSET("ch_mount_photos/ch_bracket_solar_detail.jpg"), x: M, y: 1.65, w: 3.4, h: 3.4 * 1600 / 1200 > 4.6 ? 4.6 : 3.4 * 1600 / 1200, sizing: { type: "cover", w: 3.4, h: 4.6 } });
  s.addText("Cluster Head dengan bracket 2 panel surya (foto uji LGU & ITB).", {
    x: M, y: 6.3, w: 3.4, h: 0.45, isTextBox: true, margin: 0, fontFace: FONT, fontSize: 10, italic: true, color: MUTED,
  });
  const cols = [
    ["Cluster Head (CH)", BLUE, [
      "Panel surya 2 panel + baterai internal — tidak perlu kabel daya",
      "Relay LoRa mesh multi-hop; failover parent teruji 8 CH",
      "Dipasang di tiang ±3 m di atas tanah, di area aman / unclassified",
      "Bracket panel & klem disediakan LGU (tanpa las/bor)",
    ]],
    ["Gateway (GW)", PERTAMINA, [
      "Di dalam ruangan, dekat ruang server",
      "Antena omni 8 dBi di mast luar (±5–6 m), koaksial ≤15 m + penangkal petir",
      "Ke router lokal via Wi-Fi 2,4 GHz (satu ruangan)",
      "Catu 220 VAC via adaptor, disarankan lewat UPS",
    ]],
    ["Server & dashboard", OK, [
      "PC server lokal: MQTT broker, Node-RED, aplikasi & database",
      "Pembacaan real-time per titik, kolom Area, riwayat & notifikasi alarm",
      "Alarm dikirim langsung (±10 dtk); data normal berkala",
      "Akses dari kantor lewat LAN kedua PC (dashboard/API saja)",
    ]],
  ];
  cols.forEach((c, i) => {
    const x = 4.3 + i * 2.85;
    card(s, x, 1.65, 2.7, 4.95, SURF);
    s.addShape(pres.ShapeType.rect, { x, y: 1.65, w: 2.7, h: 0.08, fill: { color: c[1] }, line: { color: c[1] } });
    cardTitle(s, x + 0.18, 1.85, 2.4, c[0], c[1]);
    bullets(s, x + 0.18, 2.3, 2.4, 4.2, c[2], 12.5);
  });
  s.addNotes("CH tidak membutuhkan kabel daya sehingga pekerjaan sipil-elektrikal di lapangan hanya untuk GLD. Gateway di dalam ruangan, antena di luar. Seluruh aplikasi berjalan di PC server lokal milik RU.");
})();

// ================================================================ 8 · hasil pengujian
(function pengujian() {
  const s = slideLight();
  heading(s, "2 · Sistem", "Hasil pengujian yang sudah dilakukan");
  const rows = [
    ["Factory Acceptance Test (FAT)", "7 dari 7 item lulus", "Uji laboratorium, Okt 2026", OK, OK_BG],
    ["Push alarm otomatis", "GLD disemprot LPG → alarm muncul di server tanpa permintaan", "Demo mesh kampus, Agu 2026", OK, OK_BG],
    ["Jaringan mesh multi-hop", "8 Cluster Head, failover parent berjalan", "Uji se-kampus ITB", OK, OK_BG],
    ["Ketahanan RF", "Stabil terhadap interferensi co-channel 10–25 dBm", "Hasil awal, Sep 2026", HOLD, HOLD_BG],
    ["Pre-scan EMC (EN 55032)", "Emisi di bawah batas kecuali frekuensi kerja LoRa sendiri", "Telkom Test House, Okt 2026 (pre-scan)", HOLD, HOLD_BG],
    ["Uji lapangan GLD V1", "Pengujian lapangan versi pertama", "RU VII Kasim, Des 2025", OK, OK_BG],
  ];
  rows.forEach((r, i) => {
    const y = 1.65 + i * 0.78;
    card(s, M, y, 12.1, 0.66, WHITE);
    s.addShape(pres.ShapeType.rect, { x: M, y, w: 0.1, h: 0.66, fill: { color: r[3] }, line: { color: r[3] } });
    s.addText(r[0], { x: M + 0.3, y, w: 3.4, h: 0.66, isTextBox: true, margin: 0, fontFace: FONT, fontSize: 13, bold: true, color: CHAR, valign: "middle" });
    s.addText(r[1], { x: 4.4, y, w: 5.2, h: 0.66, isTextBox: true, margin: 0, fontFace: FONT, fontSize: 11.5, color: CHAR_SOFT, valign: "middle" });
    chip(s, 9.75, y + 0.19, r[2], r[3], r[4], 2.8);
  });
  footnote(s, "Seluruh uji di atas adalah uji laboratorium/kampus atau pre-scan — validasi kinerja di lingkungan kilang dilakukan saat field test di RU.", 6.45);
  s.addNotes("Sampaikan bukti yang ada dengan jujur: lulus di lab/kampus, belum validasi lapangan kilang V2. Field test di RU justru bertujuan memvalidasi itu.");
})();

// ================================================================ 11 · pembagian tanggung jawab
(function raci() {
  const s = slideLight();
  heading(s, "3 · Kebutuhan", "Pembagian tanggung jawab");
  const cols = [
    ["LGU & ITB", BLUE, SURF, [
      "Unit GLD, Cluster Head, Gateway + antena",
      "Panel surya & bracket Cluster Head",
      "Router lapangan, konfigurasi jaringan, aplikasi & database di PC server",
      "Basis desain bracket/pelat U-bolt GLD",
      "Chamber gas, dataset & model AI per RU",
      "Supervisi teknis & QA instalasi",
      "Terminasi 24 VDC, energize, commissioning, pelatihan operator",
    ]],
    ["Pertamina RU VI", PERTAMINA, PERTAMINA_BG, [
      "PIC, akses site, safety induction, escort",
      "Penentuan titik bersama LGU & data HAC",
      "MoC, izin kerja, TRA/JSA",
      "Pelaksana instalasi fisik (internal/kontraktor), termasuk HSE kerja ketinggian",
      "Tiang, pondasi, pelat U-bolt, jalur kabel, grounding",
      "PSU 24 VDC & kabel ke tiap GLD",
      "PC server + UPS, kabel Cat6, titik intranet, stop kontak",
    ]],
  ];
  cols.forEach((c, i) => {
    const x = M + i * 6.15;
    card(s, x, 1.65, 5.95, 4.95, c[2]);
    s.addShape(pres.ShapeType.rect, { x, y: 1.65, w: 5.95, h: 0.5, fill: { color: c[1] }, line: { color: c[1] } });
    s.addText(c[0], { x: x + 0.25, y: 1.65, w: 5.5, h: 0.5, isTextBox: true, margin: 0, fontFace: FONT, fontSize: 15, bold: true, color: WHITE, valign: "middle" });
    bullets(s, x + 0.3, 2.35, 5.4, 4.2, c[3], 15, CHAR);
  });
  footnote(s, "Pola ini sama dengan yang disepakati untuk RU IV Cilacap; penyesuaian bisa dibahas sesuai praktik RU VI.");
  s.addNotes("Tekankan: instalasi fisik dilaksanakan RU (atau kontraktor yang ditunjuk RU), termasuk sertifikasi HSE ketinggian. LGU membawa perangkat, supervisi teknis/QA, dan pekerjaan elektrikal khusus GLD (terminasi, energize, commissioning).");
})();

// ================================================================ 12 · infrastruktur
(function infrastruktur() {
  const s = slideLight();
  heading(s, "3 · Kebutuhan", "Infrastruktur fisik & catu daya yang disiapkan RU");
  table(s, [
    ["Item", "Spesifikasi acuan", "Jumlah (rencana RU VI)"],
    ["Tiang GLD", "Pipa galvanis 2\" Sch40 (OD 60,3 mm, wajib untuk U-bolt), ditanam & dicor; tinggi pasang disesuaikan gas target", "4 titik"],
    ["Pelat & U-bolt GLD", "Pelat 250×250 mm sesuai gambar LGU; U-bolt 2\"/DN50 M10, mur/ring anti-karat", "4 set"],
    ["Tiang Cluster Head", "Pipa galvanis 2\" Sch40, ±4 m (±3 m di atas tanah)", "2 titik"],
    ["Mast antena Gateway", "Pipa 2\" ±6 m dekat ruang Gateway; koaksial LMR-400 ≤15 m + penangkal petir", "2 (sesuai jumlah GW)"],
    ["Catu daya GLD", "PSU 24 VDC ≥1 A per GLD (lokal per titik, atau terpusat ≥5 A + proteksi per jalur)", "4 beban"],
    ["Kabel 24 VDC", "2 inti tembaga, berarmor, ukuran mengikuti jarak (drop ≤5 %); masuk unit via cable gland M20×1,5", "Setelah survey"],
    ["Grounding & label", "Bonding tiang/mast ke grounding RU; label nomor titik sama dengan dashboard", "Semua titik"],
  ], { x: M, y: 1.6, w: 12.1, colW: [2.3, 7.4, 2.4], size: 11, boldFirst: true, rowH: 0.52 });
  footnote(s, "Spesifikasi detail (pondasi, tabel ukuran kabel vs jarak, BoQ) mengikuti dokumen Spesifikasi Material Instalasi yang disusun untuk RU IV — versi RU VI dibuat setelah site survey.", 6.45);
  s.addNotes("Hanya GLD yang memerlukan kabel daya. Ukuran kabel bergantung jarak dari sumber 24 VDC; untuk >195 m disarankan PSU lokal. Jumlah final setelah titik ditetapkan.");
})();

// ================================================================ 13 · server & jaringan
(function jaringan() {
  const s = slideLight();
  heading(s, "3 · Kebutuhan", "Ruang Gateway, PC server & jaringan lokal");
  const nodes = [["Antena GW\n(mast luar)", BLUE], ["Gateway\n(dalam ruangan)", BLUE], ["Router LGU\n(Wi-Fi 2,4 GHz)", BLUE], ["PC server\n(LAN 1)", PERTAMINA], ["Intranet kantor\n(LAN 2)", PERTAMINA]];
  const links = ["Koaksial ≤15 m", "Wi-Fi", "Cat6", "Cat6"];
  nodes.forEach((n, i) => {
    const x = M + i * 2.48;
    s.addShape(pres.ShapeType.roundRect, { x, y: 1.75, w: 1.9, h: 0.95, rectRadius: 0.08, fill: { color: n[1] }, line: { color: n[1] } });
    s.addText(n[0], { x, y: 1.75, w: 1.9, h: 0.95, isTextBox: true, margin: 0, fontFace: FONT, fontSize: 11.5, bold: true, color: WHITE, align: "center", valign: "middle" });
    if (i < links.length) {
      s.addShape(pres.ShapeType.line, { x: x + 1.92, y: 2.22, w: 0.54, h: 0, line: { color: CHAR, width: 1.5, endArrowType: "triangle" } });
      s.addText(links[i], { x: x + 1.75, y: 2.75, w: 0.9, h: 0.3, isTextBox: true, margin: 0, fontFace: FONT, fontSize: 9, color: MUTED, align: "center" });
    }
  });
  table(s, [
    ["Kebutuhan", "Spesifikasi acuan", "Oleh"],
    ["PC server", "PC fisik, 4 core / 8 GB RAM / SSD 256 GB, 2 port LAN (boleh USB-LAN)", "RU VI"],
    ["UPS", "≥1 kVA untuk PC + router + Gateway", "RU VI"],
    ["Lokasi", "Ruang Gateway dekat ruang server/kontrol; Gateway & router satu ruangan", "RU VI"],
    ["Stop kontak 220 VAC", "Ruang Gateway min. 2; ruang server min. 3", "RU VI"],
    ["Kabel Cat6 & titik intranet", "Router ↔ PC (≤90 m/segmen); PC ↔ intranet kantor", "RU VI / IT RU VI"],
    ["Router & aplikasi", "Router tanpa WAN/SIM; MQTT broker, Node-RED, dashboard & database dipasang LGU", "LGU"],
  ], { x: M, y: 3.25, w: 12.1, colW: [2.6, 7.4, 2.1], size: 11, boldFirst: true, rowH: 0.42 });
  footnote(s, "Tanpa internet. PC tidak meneruskan lalu lintas antara jaringan GLD dan intranet; dari kantor hanya dashboard/API yang diakses.", 6.45);
  s.addNotes("Minta RU VI menunjukkan kandidat ruang Gateway & ruang server saat survey, termasuk rute kabel antar-ruang dan titik intranet terdekat. Perlu keterlibatan tim IT RU VI.");
})();

// ================================================================ 9 · penempatan & sertifikasi
(function sertifikasi() {
  const s = slideLight();
  heading(s, "4 · Penempatan", "Klasifikasi area menentukan di mana GLD bisa dipasang");
  card(s, M, 1.65, 5.9, 4.6, SURF);
  cardTitle(s, M + 0.3, 1.85, 5.3, "Status sertifikasi Ex GLD");
  bullets(s, M + 0.3, 2.3, 5.3, 3.9, [
    "Usulan klasifikasi: II 2G Ex db IIC T4 Gb (Zona 1, flameproof).",
    "Berkas aplikasi & dokumen teknis sudah diajukan melalui agen sertifikasi; sampel unit telah dikirim.",
    "Sertifikat belum terbit — selama itu, GLD belum boleh dipasang permanen di area terklasifikasi.",
    "Cluster Head & Gateway ditempatkan di area aman / unclassified.",
  ], 14.5);
  card(s, 6.75, 1.65, 5.95, 4.6, PERTAMINA_BG);
  cardTitle(s, 7.05, 1.85, 5.4, "Pelajaran dari RU IV Cilacap", PERTAMINA);
  bullets(s, 7.05, 2.3, 5.4, 3.9, [
    "Titik GLD yang dipilih ternyata berada di area Class I Div. 2 (kajian HAC SRU).",
    "MoC RU IV: infrastruktur pendukung (tiang, jalur kabel, JB, server, jaringan) boleh disiapkan lebih dulu; pemasangan GLD menunggu sertifikat Ex — atau dipindah ke titik unclassified.",
    "Untuk Balongan: cek HAC sejak survey agar titik dan jadwal realistis sejak awal.",
  ], 14.5);
  card(s, M, 6.35, 12.1, 0.5, WARN_BG);
  s.addText("Permintaan ke RU VI: gambar Hazardous Area Classification (HAC) & plot plan area kandidat, sebelum atau saat site survey.", {
    x: M + 0.25, y: 6.35, w: 11.6, h: 0.5, isTextBox: true, margin: 0, fontFace: FONT, fontSize: 12, bold: true, color: WARN, valign: "middle",
  });
  s.addNotes("Bagian penting untuk Balongan: belajar dari Cilacap, titik GLD harus dicek terhadap HAC sejak awal. Dua pilihan realistis: titik di area unclassified untuk field test lebih awal, atau infrastruktur disiapkan dulu dan GLD dipasang setelah sertifikat terbit.");
})();

// ================================================================ 10 · gas per RU / chamber
(function chamber() {
  const s = slideLight();
  heading(s, "4 · Penyesuaian", "Gas target disesuaikan per RU — dataset diambil di lokasi");
  s.addImage({ path: ASSET("chamber_photos/chamber_setup_lengkap.jpeg"), x: M, y: 1.65, w: 3.9, h: 3.9 * 639 / 573 });
  s.addText("Gas test chamber portable dengan unit GLD terpasang.", {
    x: M, y: 1.65 + 3.9 * 639 / 573 + 0.06, w: 3.9, h: 0.35, isTextBox: true, margin: 0, fontFace: FONT, fontSize: 10, italic: true, color: MUTED,
  });
  const steps = [
    ["Chamber dibawa ke kilang", "Ditempatkan di kantor kilang (bukan area proses)."],
    ["Pengambilan dataset", "Sampel gas sesuai permintaan RU dialirkan ke GLD di dalam chamber."],
    ["Training model AI", "Model dilatih ulang dengan dataset lokasi."],
    ["Pemasangan model ke GLD", "Model baru dimasukkan ke firmware unit di tempat."],
    ["Verifikasi", "Uji respons sebelum unit dipasang di titik."],
  ];
  steps.forEach((st, i) => {
    const y = 1.65 + i * 0.86;
    badge(s, 4.85, y, i + 1, 0.44);
    s.addText(st[0], { x: 5.45, y: y - 0.04, w: 7.2, h: 0.32, isTextBox: true, margin: 0, fontFace: FONT, fontSize: 13.5, bold: true, color: CHAR });
    s.addText(st[1], { x: 5.45, y: y + 0.29, w: 7.2, h: 0.4, isTextBox: true, margin: 0, fontFace: FONT, fontSize: 11.5, color: CHAR_SOFT });
  });
  card(s, 4.85, 6.0, 7.85, 0.8, HOLD_BG);
  s.addText("Pertanyaan untuk RU VI: gas apa yang paling relevan di area kandidat (mis. LPG, H₂, H₂S, metana)? Dapatkah RU membantu menyediakan sampel gas? Sampel gas berbahaya tidak dapat dikirim lewat kurir umum.", {
    x: 5.05, y: 6.0, w: 7.5, h: 0.8, isTextBox: true, margin: 0, fontFace: FONT, fontSize: 11, bold: true, color: HOLD, valign: "middle",
  });
  s.addNotes("Pola ini standar untuk semua RU: chamber dibawa ke lokasi, sehingga tidak perlu mengirim sampel gas berbahaya ke Bandung. Gas tambahan seperti H2S belum tercakup model saat ini dan memerlukan sampel gas dari/di lokasi.");
})();

// ================================================================ 14 · tahapan
(function tahapan() {
  const s = slideLight();
  heading(s, "5 · Rencana", "Tahapan implementasi di RU VI Balongan");
  const steps = [
    ["Rapat koordinasi", "13 Nov 2026", "LGU & RU VI"],
    ["Site survey awal", "Jadwal disepakati hari ini", "LGU & RU VI"],
    ["Penetapan titik & desain", "Titik GLD/CH/GW, jarak kabel, BoQ", "LGU & RU VI"],
    ["MoC & perizinan", "MoC, TRA/JSA, izin kerja", "RU VI"],
    ["Persiapan infrastruktur", "Tiang, kabel, PSU, PC server, jaringan", "RU VI"],
    ["Dataset gas & model", "Chamber di kantor kilang", "LGU"],
    ["Instalasi & commissioning", "Pemasangan, energize, uji alarm", "RU VI + LGU"],
    ["Field test & monitoring", "Operasi advisory, evaluasi", "RU VI + LGU"],
  ];
  const n = steps.length, gap = 0.1, w = (12.1 - gap * (n - 1)) / n;
  s.addShape(pres.ShapeType.line, { x: M + 0.2, y: 2.12, w: 11.7, h: 0, line: { color: LINE, width: 2 } });
  steps.forEach((st, i) => {
    const x = M + i * (w + gap);
    badge(s, x + w / 2 - 0.25, 1.87, i + 1, 0.5, i === 0 ? OK : BLUE);
    card(s, x, 2.6, w, 2.6, i === 0 ? OK_BG : SURF);
    s.addText(st[0], { x: x + 0.1, y: 2.72, w: w - 0.2, h: 0.75, isTextBox: true, margin: 0, fontFace: FONT, fontSize: 12, bold: true, color: CHAR, valign: "top" });
    s.addText(st[1], { x: x + 0.1, y: 3.5, w: w - 0.2, h: 1.0, isTextBox: true, margin: 0, fontFace: FONT, fontSize: 11.5, color: CHAR_SOFT, valign: "top" });
    s.addText(st[2], { x: x + 0.1, y: 4.65, w: w - 0.2, h: 0.45, isTextBox: true, margin: 0, fontFace: FONT, fontSize: 11, bold: true, color: BLUE, valign: "top" });
  });
  card(s, M, 5.5, 12.1, 0.95, PERTAMINA_BG);
  s.addText("Langkah 4–6 dapat berjalan paralel. Bila titik GLD berada di area terklasifikasi, langkah 7 untuk GLD menunggu sertifikat Ex terbit; infrastruktur (langkah 5) tetap dapat disiapkan lebih dulu, seperti di RU IV.", {
    x: M + 0.25, y: 5.5, w: 11.6, h: 0.95, isTextBox: true, margin: 0, fontFace: FONT, fontSize: 12, color: PERTAMINA, bold: true, valign: "middle",
  });
  s.addNotes("Tidak menjanjikan tanggal instalasi: tanggal bergantung hasil survey, MoC dan klasifikasi area. Target hari ini adalah tanggal site survey.");
})();

// ================================================================ 15 · site survey
(function survey() {
  const s = slideLight();
  heading(s, "5 · Rencana", "Persiapan site survey awal");
  const cols = [
    ["Yang diperiksa tim LGU", BLUE, SURF, [
      "Kandidat titik GLD: sumber bocor (flange/valve), arah angin, tinggi pasang",
      "Klasifikasi area tiap titik (HAC)",
      "Jangkauan LoRa: posisi CH & mast antena Gateway (line of sight)",
      "Sumber 220 VAC / 24 VDC terdekat & rute kabel",
      "Ruang Gateway, ruang server, titik intranet",
      "Lokasi kerja chamber gas di kantor kilang",
    ]],
    ["Yang mohon disiapkan RU VI", PERTAMINA, PERTAMINA_BG, [
      "PIC lapangan (operasi, HSE, elektrikal/instrumen, IT)",
      "Izin masuk, safety induction, APD & escort",
      "Gambar HAC, plot plan, daftar kandidat area",
      "Izin dokumentasi foto/video untuk keperluan desain",
      "Informasi standar kabel, grounding & tiang RU VI",
      "Gas target yang diharapkan RU",
    ]],
  ];
  cols.forEach((c, i) => {
    const x = M + i * 6.15;
    card(s, x, 1.65, 5.95, 4.3, c[2]);
    s.addShape(pres.ShapeType.rect, { x, y: 1.65, w: 5.95, h: 0.5, fill: { color: c[1] }, line: { color: c[1] } });
    s.addText(c[0], { x: x + 0.25, y: 1.65, w: 5.5, h: 0.5, isTextBox: true, margin: 0, fontFace: FONT, fontSize: 15, bold: true, color: WHITE, valign: "middle" });
    bullets(s, x + 0.3, 2.35, 5.4, 3.5, c[3], 15, CHAR);
  });
  card(s, M, 6.1, 12.1, 0.65, OK_BG);
  s.addText("Hasil survey: titik GLD/CH/GW terpilih, jarak & rute kabel, kebutuhan material (BoQ) RU VI, dan dokumen persiapan instalasi.", {
    x: M + 0.25, y: 6.1, w: 11.6, h: 0.65, isTextBox: true, margin: 0, fontFace: FONT, fontSize: 12, bold: true, color: OK, valign: "middle",
  });
  s.addNotes("Usulkan durasi survey ±1–2 hari di site. Mohon dokumen HAC & plot plan dikirim sebelum survey jika memungkinkan, agar kandidat titik bisa disaring lebih dulu.");
})();

// ================================================================ 16 · hal yang perlu dikonfirmasi
(function konfirmasi() {
  const s = slideDark();
  s.addText("HAL YANG PERLU DIKONFIRMASI", { x: M, y: 0.46, w: 11, h: 0.26, isTextBox: true, margin: 0, fontFace: FONT, fontSize: 11, bold: true, charSpacing: 1.6, color: "9FB4E6" });
  s.addText("Untuk RU VI Balongan — berlaku juga untuk RU II, III, V, VII", { x: M, y: 0.74, w: 12, h: 0.66, isTextBox: true, margin: 0, fontFace: SERIF, fontSize: 27, bold: true, color: WHITE });
  const qs = [
    "PIC RU (operasi, HSE, elektrikal/instrumen, IT) & jalur komunikasi",
    "Tanggal site survey awal & persyaratan masuk site",
    "Area kandidat & gambar HAC / plot plan",
    "Gas target prioritas & ketersediaan sampel gas",
    "Jumlah unit final (rencana: 4 GLD, 2 CH, 2 GW)",
    "Mekanisme MoC & izin kerja, serta estimasi waktunya",
    "Pelaksana instalasi fisik (tim internal / kontraktor RU)",
    "Sumber 24 VDC/220 VAC & standar kabel/grounding",
    "Ruang Gateway, PC server, UPS & titik intranet",
    "Lokasi chamber gas di kantor kilang",
  ];
  qs.forEach((q, i) => {
    const col = i % 2, row = Math.floor(i / 2);
    const x = M + col * 6.15, y = 1.75 + row * 0.98;
    badge(s, x, y, i + 1, 0.46, i < 4 ? "1ABB9C" : BLUE);
    s.addText(q, { x: x + 0.62, y: y - 0.06, w: 5.35, h: 0.6, isTextBox: true, margin: 0, fontFace: FONT, fontSize: 13.5, bold: true, color: WHITE, valign: "middle" });
  });
  s.addText("Hijau = mohon dijawab/disepakati hari ini atau sebelum survey.", { x: M, y: 6.8, w: 11, h: 0.3, isTextBox: true, margin: 0, fontFace: FONT, fontSize: 10.5, italic: true, color: "8E9AB4" });
  s.addNotes("Ini menjawab permintaan Pak Senna: proses persiapan dan apa yang perlu dikonfirmasi dari RU dan LGU. Butir 1–4 diharapkan sudah ada jawaban/tanggal sebelum survey; PIC RU lain dipersilakan mengirimkan jawaban yang sama untuk RU masing-masing.");
})();

// ================================================================ 17 · penutup
(function penutup() {
  const s = slideLight();
  heading(s, "Penutup", "Terima kasih");
  card(s, M, 1.75, 12.1, 2.9, SURF);
  cardTitle(s, M + 0.35, 1.95, 11, "Tindak lanjut setelah rapat");
  bullets(s, M + 0.35, 2.4, 11.4, 2.2, [
    "RU VI: konfirmasi PIC, tanggal site survey, dan mengirim gambar HAC/plot plan area kandidat.",
    "LGU: mengirim daftar kebutuhan & checklist persiapan survey; menyiapkan tim survey.",
    "RU lain: menyampaikan PIC dan jawaban daftar konfirmasi melalui Pak Senna (Pertamina Patra Niaga).",
  ], 13.5, CHAR);
  s.addText("PT LAPI Ganesha Utama & Lab IoT / Fisika ITB — Jl. Dederuk No. 30, Bandung", {
    x: M, y: 5.0, w: 11, h: 0.3, isTextBox: true, margin: 0, fontFace: FONT, fontSize: 11, color: MUTED,
  });
  s.addNotes("Tutup dengan merangkum tanggal survey dan PIC yang disepakati.");
})();

pres.writeFile({ fileName: OUT }).then(() => console.log("written", OUT));
