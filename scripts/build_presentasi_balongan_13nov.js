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


const SRC_SPEK = "Sumber: Spesifikasi Material & Kebutuhan Instalasi GLD rev 1.5 (disusun untuk RU IV Cilacap) — angka USULAN dapat disesuaikan dengan standar RU VI.";
const SRC_MOC = "Sumber: MoC No. 15769/RU IV — Field Test Multi-Modality Gas Leak Detector Area SRU, RU IV Cilacap (Nov 2026).";
function seg(s, x1, y1, x2, y2, o = {}) {
  s.addShape(pres.ShapeType.line, {
    x: Math.min(x1, x2), y: Math.min(y1, y2), w: Math.abs(x2 - x1), h: Math.abs(y2 - y1),
    flipV: (x2 - x1) * (y2 - y1) < 0,
    line: { color: o.color || CHAR, width: o.width || 1.25, dashType: o.dash, endArrowType: o.arrow },
  });
}
function box(s, x, y, w, h, text, o = {}) {
  s.addShape(pres.ShapeType.roundRect, {
    x, y, w, h, rectRadius: 0.05, fill: { color: o.fill || WHITE }, line: { color: o.line || CHAR_SOFT, width: 1 },
  });
  s.addText(text, {
    x, y, w, h, isTextBox: true, margin: 0, fontFace: FONT, fontSize: o.size || 9.5, bold: true,
    color: o.color || CHAR, align: "center", valign: "middle",
  });
}
function imgCover(s, p, pw, ph, x, y, bw, bh) {
  const k = Math.max(bw / pw, bh / ph);
  s.addImage({ path: ASSET(p), x, y, w: pw * k, h: ph * k, sizing: { type: "cover", w: bw, h: bh } });
}

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

(function agenda() {
  const s = slideLight();
  heading(s, "Agenda", "Tujuh hal yang akan kita bahas");
  const items = [
    ["1", "Apa itu GLD", "Penjelasan fungsional & mekanisme pengukuran, arsitektur sistem jaringan, komponen, peta peran, supporting system."],
    ["2", "Mekanisme pemasangan", "Cara pemasangan GLD, Cluster Head, Gateway, dan server di site."],
    ["3", "Kebutuhan pemasangan GLD", "Catu daya 24 VDC, pelat mounting & U-bolt, tiang."],
    ["4", "Kebutuhan Cluster Head", "Tiang & U-bolt yang sesuai, tinggi 3–5 m."],
    ["5", "Kebutuhan Gateway", "Tiang di atas roof top; unit Gateway & antena terpasang bersama di tiang."],
    ["6", "Server & UPS", "PC server lokal, UPS, router & jaringan tanpa internet."],
    ["7", "Contoh map RU IV Cilacap", "Layout titik, klasifikasi area (HAC), dan jalur kabel dari MoC RU IV."],
  ];
  items.forEach((it, i) => {
    const y = 1.55 + i * 0.7;
    badge(s, M, y, it[0], 0.44);
    s.addText(it[1], { x: M + 0.66, y: y - 0.05, w: 11.4, h: 0.3, isTextBox: true, margin: 0, fontFace: FONT, fontSize: 15, bold: true, color: CHAR });
    s.addText(it[2], { x: M + 0.66, y: y + 0.25, w: 11.4, h: 0.28, isTextBox: true, margin: 0, fontFace: FONT, fontSize: 11.5, color: CHAR_SOFT });
  });
  footnote(s, "Dilanjutkan: klasifikasi area & sertifikasi, gas per RU, pembagian tanggung jawab, tahapan, site survey & hal yang perlu dikonfirmasi. Lampiran A–E: tiang & pondasi, tinggi sensor per gas, terminasi, antena & jaringan, perkiraan BoQ.", 6.62);
  s.addNotes("Urutan mengikuti hasil rapat persiapan: sistem dulu (apa itu GLD sampai server), lalu cara pemasangan, lalu kebutuhan per perangkat (GLD, CH, Gateway, server & UPS), ditutup contoh nyata dari RU IV Cilacap.");
})();

// ================================================================ 3 · program & posisi RU VI
(function program() {
  const s = slideLight();
  heading(s, "Pendahuluan", "GLD Tahap 2 — enam Refinery Unit, RU VI menyusul RU IV");
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
    ["RU VI Balongan", "4", "2*", "2*"],
    ["RU VII Kasim", "5", "11", "1"],
    ["Total", "28", "22", "7"],
  ], { x: 6.65, y: 2.1, w: 6.05, colW: [2.45, 1.1, 1.4, 1.1], size: 12, boldFirst: true, rowH: 0.42 });
  s.addShape(pres.ShapeType.rect, { x: 6.65, y: 2.1 + 0.42 * 5, w: 6.05, h: 0.42, fill: { color: BLUE, transparency: 85 }, line: { color: BLUE, width: 1.5 } });
  s.addText("* Jumlah CH & Gateway RU VI masih angka awal — ditetapkan dari LoRa mapping saat site survey dan bisa bertambah. Jumlah & lokasi final per RU ditetapkan setelah survey; tiap RU juga mendapat 1 PC server lokal (disediakan RU).", {
    x: 6.65, y: 5.6, w: 6.05, h: 0.7, isTextBox: true, margin: 0, fontFace: FONT, fontSize: 11, italic: true, color: MUTED,
  });
  footnote(s, "Sumber alokasi: tabel alokasi perangkat per RU (3 Nov 2026) & dokumen Kebutuhan Peralatan GLD per RU.");
  s.addNotes("RU VI Balongan direncanakan 4 GLD; angka 2 Cluster Head dan 2 Gateway hanya rencana awal. Jumlah CH/GW ditetapkan dari LoRa mapping (uji jangkauan) saat site survey dan kemungkinan bertambah, tergantung jarak dan halangan antar-titik. Pengalaman RU IV Cilacap menjadi acuan persiapan Balongan, terutama soal klasifikasi area dan MoC.");
})();

// ================================================================ 5 · fitur GLD
(function fitur() {
  const s = slideLight();
  heading(s, "1 · Apa itu GLD", "Penjelasan fungsional — apa yang dilakukan GLD");
  s.addImage({ path: ASSET("assembly_photos_0710/IMG_14.35.32.jpg"), x: M, y: 1.65, w: 4.3, h: 4.3 * 737 / 1000 });
  s.addText("GLD (Gas Leak Detector) V2: alat deteksi kebocoran gas yang mengenali jenis gas, membunyikan alarm lokal, dan mengirim data ke server — standalone & advisory.", {
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

(function mekanisme() {
  const s = slideLight();
  heading(s, "1 · Apa itu GLD", "Mekanisme pengukuran — dari gas menjadi label jenis gas");
  const steps = [
    ["Gas masuk", "Udara sekitar berdifusi melalui wire mesh stainless; kipas DC kecil membantu mengalirkan udara ke ruang sensor."],
    ["8 sensor merespons", "Lapisan semikonduktor (MOS) tiap sensor MQ berubah resistansinya — tiap sensor punya kepekaan berbeda terhadap tiap gas."],
    ["Pembacaan sinyal", "Tegangan 8 kanal dibaca bersamaan oleh ADC 24-bit di papan sensor."],
    ["Pola gas", "Gabungan respons 8 sensor membentuk pola (sidik jari) yang khas untuk tiap jenis gas."],
    ["Klasifikasi AI di unit", "Model AI di ESP32-S3 mengenali pola → label jenis gas + nilai confidence, < 166 ms."],
    ["Alarm & kirim data", "Beacon di unit menyala; data dikirim lewat LoRa ke Cluster Head → Gateway → server."],
  ];
  steps.forEach((st, i) => {
    const y = 1.6 + i * 0.8;
    badge(s, M, y, i + 1, 0.42);
    s.addText(st[0], { x: M + 0.6, y: y - 0.05, w: 6.6, h: 0.3, isTextBox: true, margin: 0, fontFace: FONT, fontSize: 13.5, bold: true, color: CHAR });
    s.addText(st[1], { x: M + 0.6, y: y + 0.24, w: 6.6, h: 0.5, isTextBox: true, margin: 0, fontFace: FONT, fontSize: 11, color: CHAR_SOFT, valign: "top" });
  });
  const x0 = 8.05, pw = 2.0, ph = pw * 256 / 282;
  s.addImage({ path: ASSET("balongan_13nov/sensor_array_foto.jpg"), x: x0, y: 1.6, w: pw, h: ph });
  label(s, "Papan sensor: 8 sensor gas seri MQ dalam satu unit GLD — dibaca bersamaan, bukan satu per satu.", x0 + pw + 0.15, 1.6, W - M - x0 - pw - 0.15, ph, { size: 10.5, valign: "middle" });
  const cw = W - M - x0, ch = cw * 300 / 430;
  s.addImage({ path: ASSET("balongan_13nov/respons_sensor_h2.jpg"), x: x0, y: 3.65, w: cw, h: ch });
  label(s, "Contoh respons 8 sensor saat paparan H₂ (uji lab): kelas Hidrogen, confidence 99,81%.", x0, 3.7 + ch, cw, 0.4, { size: 9.5, color: MUTED, valign: "top" });
  card(s, M, 6.45, 7.2, 0.6, OK_BG);
  s.addText("Keluaran GLD: label jenis gas & confidence — bukan nilai konsentrasi (%LEL/ppm). GLD melengkapi detektor FGDS eksisting, tidak menggantikannya.", {
    x: M + 0.2, y: 6.45, w: 6.8, h: 0.6, isTextBox: true, margin: 0, fontFace: FONT, fontSize: 10.5, bold: true, color: OK, valign: "middle",
  });
  s.addNotes("Jelaskan perbedaan dengan detektor konvensional: detektor FGDS memberi angka konsentrasi satu jenis gas; GLD membaca 8 sensor sekaligus dan mengenali jenis gas dari polanya. Kelas gas saat ini Clean Air, LPG, H2; gas lain memerlukan dataset tambahan.");
})();

// ================================================================ 4 · arsitektur
(function arsitektur() {
  const s = slideLight();
  heading(s, "1 · Arsitektur sistem jaringan", "Dari GLD hingga server — berjalan lokal, tanpa internet");
  s.addImage({ path: ASSET("rapat_22okt/block_diagram.jpg"), x: M, y: 1.6, w: 7.9, h: 7.9 * 819 / 1600 });
  s.addText("Block diagram final: area FIELD (lapangan) dan BUILDING (gedung). Biru = disuplai LGU, kuning = instalasi, mounting & infrastruktur oleh Pertamina.", {
    x: M, y: 1.6 + 7.9 * 819 / 1600 + 0.06, w: 8.3, h: 0.4, isTextBox: true, margin: 0, fontFace: FONT, fontSize: 10, italic: true, color: MUTED,
  });
  const steps = [
    ["GLD", "Deteksi gas & klasifikasi AI di dalam unit, alarm lokal"],
    ["Cluster Head", "Relay LoRa mesh, tenaga surya, tanpa kabel daya"],
    ["Gateway", "Di tiang atap, menyatu dengan antena"],
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
  s.addNotes("Alur data: GLD → LoRa → CH → LoRa mesh → Gateway + antena di tiang atap → Wi-Fi → router LGU → kabel Cat6 → PC server. PC punya port LAN kedua ke intranet kantor hanya untuk akses dashboard/API, tidak meneruskan lalu lintas antar jaringan. Posisi ini sama dengan yang tertulis di MoC RU IV.");
})();

(function komponen() {
  const s = slideLight();
  heading(s, "1 · Komponen", "Komponen sistem — GLD, Cluster Head, Gateway & server");
  const cols = [
    ["GLD (Node Sensor)", BLUE, [
      "8 sensor gas MOS + AI di ESP32-S3",
      "Beacon alarm visual & audible",
      "Radio LoRa + antena 3 dBi",
      "Catu 24 VDC, maks. ± 8 W",
      "Housing aluminium die-cast",
    ]],
    ["Cluster Head (CH)", BLUE, [
      "Relay LoRa mesh multi-hop",
      "Failover parent teruji 8 CH",
      "Panel surya + baterai — tanpa kabel daya",
      "Di tiang 3–5 m, area aman",
    ]],
    ["Gateway (GW)", PERTAMINA, [
      "Jembatan LoRa mesh → jaringan IP",
      "Unit + antena omni 8 dBi di tiang atap",
      "Outdoor; daya dari UPS di ruangan",
      "Wi-Fi 2,4 GHz ke router lokal",
    ]],
    ["Server & dashboard", OK, [
      "PC server lokal: MQTT broker, Node-RED, aplikasi & database",
      "Dashboard real-time, kolom Area, riwayat & notifikasi alarm",
      "Alarm langsung (± 10 dtk); data normal berkala",
    ]],
  ];
  const cw = (12.1 - 3 * 0.15) / 4;
  cols.forEach((c, i) => {
    const x = M + i * (cw + 0.15);
    card(s, x, 1.6, cw, 3.7, SURF);
    s.addShape(pres.ShapeType.rect, { x, y: 1.6, w: cw, h: 0.08, fill: { color: c[1] }, line: { color: c[1] } });
    cardTitle(s, x + 0.18, 1.8, cw - 0.3, c[0], c[1]);
    bullets(s, x + 0.18, 2.3, cw - 0.32, 2.9, c[2], 13);
  });
  footnote(s, "Disuplai LGU: GLD, CH (termasuk panel & bracket), Gateway + antena, router, aplikasi server. Disiapkan RU: PC server, UPS, tiang, kabel & infrastruktur — lihat peta peran.", 5.5);
  s.addNotes("Empat komponen utama. Hanya GLD yang membutuhkan kabel daya di lapangan; CH mandiri; Gateway dan server di dalam gedung.");
})();

// ================================================================ 6 · spesifikasi
(function spesifikasi() {
  const s = slideLight();
  heading(s, "1 · Komponen", "Spesifikasi teknis GLD V2");
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

// ================================================================ 8 · hasil pengujian
(function pengujian() {
  const s = slideLight();
  heading(s, "1 · Komponen", "Hasil pengujian yang sudah dilakukan");
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
  heading(s, "1 · Peta peran", "Checklist tanggung jawab per pihak");
  const cols = [
    ["LGU & ITB", BLUE, SURF, [
      "Unit GLD, Cluster Head, dan Gateway (termasuk antena)",
      "Panel surya dan bracket Cluster Head",
      "Router lapangan, konfigurasi jaringan, aplikasi dan database server",
      "Basis desain bracket dan pelat U-bolt GLD",
      "Chamber gas, dataset, dan model AI per RU",
      "Supervisi teknis dan QA instalasi",
      "Terminasi 24 VDC, energize, commissioning, dan pelatihan operator",
    ]],
    ["Pertamina RU VI", PERTAMINA, PERTAMINA_BG, [
      "PIC, akses site, safety induction, dan pendampingan",
      "Penetapan titik pemasangan bersama LGU berdasarkan HAC",
      "MoC, izin kerja, dan TRA/JSA",
      "Pelaksana instalasi fisik, termasuk HSE kerja ketinggian",
      "Tiang, pondasi, pelat U-bolt, jalur kabel, dan grounding",
      "PSU 24 VDC dan kabel daya ke tiap GLD",
      "PC server, UPS, kabel Cat6, titik intranet, dan stop kontak",
    ]],
  ];
  cols.forEach((c, i) => {
    const x = M + i * 6.15;
    card(s, x, 1.65, 5.95, 4.95, c[2]);
    s.addShape(pres.ShapeType.rect, { x, y: 1.65, w: 5.95, h: 0.5, fill: { color: c[1] }, line: { color: c[1] } });
    s.addText(c[0], { x: x + 0.25, y: 1.65, w: 4.0, h: 0.5, isTextBox: true, margin: 0, fontFace: FONT, fontSize: 15, bold: true, color: WHITE, valign: "middle" });
    s.addText("Status", { x: x + 4.75, y: 1.65, w: 1.0, h: 0.5, isTextBox: true, margin: 0, fontFace: FONT, fontSize: 11, bold: true, color: WHITE, align: "center", valign: "middle" });
    c[3].forEach((t, k) => {
      const ry = 2.3 + k * 0.6;
      if (k > 0) s.addShape(pres.ShapeType.line, { x: x + 0.2, y: ry - 0.06, w: 5.55, h: 0, line: { color: LINE, width: 0.75 } });
      s.addShape(pres.ShapeType.rect, { x: x + 0.25, y: ry + 0.13, w: 0.24, h: 0.24, fill: { color: WHITE }, line: { color: c[1], width: 1.25 } });
      s.addText(t, { x: x + 0.65, y: ry, w: 4.0, h: 0.5, isTextBox: true, margin: 0, fontFace: FONT, fontSize: 12.5, color: CHAR, valign: "middle" });
      s.addShape(pres.ShapeType.roundRect, { x: x + 4.8, y: ry + 0.11, w: 0.9, h: 0.28, rectRadius: 0.05, fill: { color: WHITE }, line: { color: LINE, width: 0.75 } });
    });
  });
  footnote(s, "Mengacu pola RU IV Cilacap; dapat disesuaikan dengan praktik RU VI. Kolom status diisi saat rapat koordinasi.");
  s.addNotes("Instalasi fisik dilaksanakan RU atau kontraktor yang ditunjuk RU, termasuk HSE kerja ketinggian. LGU menyediakan perangkat, supervisi teknis/QA, serta pekerjaan elektrikal khusus GLD (terminasi, energize, commissioning).");
})();

(function supporting() {
  const s = slideLight();
  heading(s, "1 · Supporting system", "Sistem pendukung yang perlu disiapkan di site");
  const items = [
    ["Catu daya 24 VDC", "PSU 24 VDC, junction box & kabel armored ke tiap GLD", "RU VI", "Bagian 3"],
    ["Tiang & mounting", "Tiang GLD + pelat U-bolt, tiang CH 3–5 m, tiang Gateway di atap", "RU VI (desain LGU)", "Bagian 3–5"],
    ["Server & UPS", "PC server lokal, UPS ≥ 1 kVA, stop kontak", "RU VI", "Bagian 6"],
    ["Jaringan lokal", "Router Wi-Fi (LGU), kabel Cat6, titik intranet kantor, tanpa internet", "LGU + IT RU VI", "Bagian 6"],
    ["Daya GW & proteksi petir", "Kabel daya UPS → tiang atap, grounding tiang ke penangkal petir gedung", "RU VI", "Bagian 5 · Lampiran D"],
    ["Izin & keselamatan", "MoC, TRA/JSA, izin kerja, HSE kerja ketinggian & atap", "RU VI", "Penempatan & tahapan"],
  ];
  items.forEach((it, i) => {
    const col = i % 3, row = Math.floor(i / 3);
    const x = M + col * 4.1, y = 1.65 + row * 2.4, w = 3.9;
    card(s, x, y, w, 2.2, SURF);
    badge(s, x + 0.2, y + 0.2, i + 1, 0.42);
    s.addText(it[0], { x: x + 0.75, y: y + 0.18, w: w - 0.9, h: 0.45, isTextBox: true, margin: 0, fontFace: FONT, fontSize: 14, bold: true, color: CHAR, valign: "middle" });
    s.addText(it[1], { x: x + 0.2, y: y + 0.75, w: w - 0.4, h: 0.85, isTextBox: true, margin: 0, fontFace: FONT, fontSize: 11.5, color: CHAR_SOFT, valign: "top" });
    chip(s, x + 0.2, y + 1.72, it[2], WHITE, it[2].startsWith("LGU") ? BLUE : PERTAMINA, 1.85);
    s.addText(it[3], { x: x + 2.15, y: y + 1.72, w: w - 2.3, h: 0.27, isTextBox: true, margin: 0, fontFace: FONT, fontSize: 9.5, italic: true, color: MUTED, align: "right", valign: "middle" });
  });
  s.addNotes("Sistem pendukung adalah semua yang dibutuhkan agar GLD bisa beroperasi: daya, tiang, server & UPS, jaringan, antena, dan izin. Detail tiap butir ada di bagian 3–6.");
})();

(function penampang() {
  const s = slideLight();
  heading(s, "2 · Mekanisme pemasangan", "Gambaran pemasangan GLD, Cluster Head, Gateway & server");
  const G = 5.55, U = 0.5;
  const BX = 7.3, BW = W - M - BX, R = 2.95;
  s.addShape(pres.ShapeType.rect, { x: M, y: 1.5, w: BX - M - 0.2, h: G - 1.5, fill: { color: SURF }, line: { color: SURF } });
  label(s, "LAPANGAN (FIELD)", M + 0.15, 1.56, 3, 0.26, { size: 10, bold: true, color: BLUE });
  label(s, "GEDUNG (BUILDING)", BX + 0.15, 1.56, 3, 0.26, { size: 10, bold: true, color: PERTAMINA });
  s.addShape(pres.ShapeType.rect, { x: M, y: G, w: W - 2 * M, h: 0.36, fill: { color: "EFE9E1" }, line: { color: "EFE9E1" } });
  line(s, M, G, W - 2 * M, 0, "8A7F72", 1.5);
  // GLD + JB/PSU
  const gx = M + 0.9;
  s.addShape(pres.ShapeType.rect, { x: gx - 0.03, y: G - 0.62, w: 0.06, h: 0.62, fill: { color: "7D8794" }, line: { color: "5E6773", width: 0.5 } });
  box(s, gx - 0.22, G - 1.02, 0.44, 0.42, "GLD", { fill: BLUE, line: BLUE_DK, color: WHITE, size: 9 });
  box(s, M + 2.0, G - 0.6, 0.85, 0.5, "JB / PSU\n24 VDC", { size: 8.5 });
  seg(s, gx + 0.03, G - 0.3, M + 2.0, G - 0.3, { color: "C0392B", width: 2 });
  label(s, "kabel 24 VDC", gx + 0.1, G - 0.56, 1.0, 0.22, { size: 8, color: "C0392B" });
  // CH
  const cx = M + 4.1, ctop = G - 4.5 * U;
  s.addShape(pres.ShapeType.rect, { x: cx - 0.035, y: ctop, w: 0.07, h: G - ctop, fill: { color: "7D8794" }, line: { color: "5E6773", width: 0.5 } });
  s.addShape(pres.ShapeType.rect, { x: cx - 0.55, y: ctop + 0.45, w: 0.52, h: 0.08, fill: { color: "2E3E66" }, line: { color: "2E3E66" }, rotate: -12 });
  box(s, cx - 0.2, ctop - 0.05, 0.4, 0.34, "CH", { fill: BLUE, line: BLUE_DK, color: WHITE, size: 9 });
  line(s, cx, ctop - 0.4, 0, 0.35, CHAR, 1.5);
  seg(s, cx - 0.75, ctop, cx - 0.75, G, { color: MUTED, width: 0.75 });
  label(s, "3–5 m", cx - 1.45, ctop + (G - ctop) / 2 - 0.14, 0.65, 0.28, { size: 10, bold: true, color: CHAR, align: "right" });
  // building + rooftop mast
  s.addShape(pres.ShapeType.rect, { x: BX, y: R, w: BW, h: G - R, fill: { color: WHITE }, line: { color: CHAR_SOFT, width: 1.25 } });
  s.addShape(pres.ShapeType.rect, { x: BX - 0.05, y: R - 0.06, w: BW + 0.1, h: 0.08, fill: { color: CHAR_SOFT }, line: { color: CHAR_SOFT } });
  const mx = BX + BW - 0.8, mtop = R - 2.25 * U;
  s.addShape(pres.ShapeType.rect, { x: mx - 0.2, y: R - 0.12, w: 0.4, h: 0.06, fill: { color: CHAR }, line: { color: CHAR } });
  s.addShape(pres.ShapeType.rect, { x: mx - 0.035, y: mtop, w: 0.07, h: R - 0.12 - mtop, fill: { color: "7D8794" }, line: { color: "5E6773", width: 0.5 } });
  line(s, mx, mtop - 0.38, 0, 0.38, CHAR, 2.5);
  box(s, mx - 0.24, mtop - 0.02, 0.48, 0.34, "GW", { fill: PERTAMINA, line: PERTAMINA, color: WHITE, size: 9 });
  label(s, "tiang Gateway di atap\n(unit + antena, ± 2–2,5 m)", mx - 2.25, mtop + 0.05, 1.95, 0.5, { size: 9, bold: true, color: CHAR, align: "right" });
  // inside building
  box(s, BX + 2.0, R + 0.3, 1.15, 0.45, "Router Wi-Fi", { fill: SURF_2 });
  seg(s, mx - 0.1, mtop + 0.32, BX + 3.15, R + 0.4, { color: MUTED, width: 1.5, dash: "sysDot" });
  label(s, "Wi-Fi", BX + 3.25, R + 0.05, 0.6, 0.22, { size: 8, color: MUTED });
  box(s, BX + 0.25, R + 1.35, 1.3, 0.5, "PC server", { fill: PERTAMINA_BG });
  seg(s, BX + 2.0, R + 0.52, BX + 1.3, R + 0.52, { color: CHAR, width: 1.5 });
  seg(s, BX + 1.3, R + 0.52, BX + 1.3, R + 1.35, { color: CHAR, width: 1.5 });
  label(s, "Cat6", BX + 1.35, R + 0.8, 0.5, 0.22, { size: 8, color: CHAR });
  label(s, "LAN-2 → intranet kantor", BX + 0.15, R + 1.9, 1.5, 0.22, { size: 8, color: PERTAMINA, align: "center" });
  box(s, BX + 2.0, R + 1.9, 2.9, 0.45, "UPS", { fill: HOLD_BG, line: HOLD });
  seg(s, BX + 2.57, R + 0.75, BX + 2.57, R + 1.9, { color: "C0392B", width: 1.5 });
  seg(s, mx + 0.1, mtop + 0.32, mx + 0.1, R + 1.9, { color: "C0392B", width: 1.5 });
  seg(s, BX + 1.55, R + 1.6, BX + 2.0, R + 1.6, { color: "C0392B", width: 1.5 });
  seg(s, BX + 2.0, R + 1.6, BX + 2.0, R + 1.9, { color: "C0392B", width: 1.5 });
  label(s, "daya GW", mx + 0.15, R + 1.2, 0.8, 0.22, { size: 8, color: "C0392B" });
  // LoRa links
  seg(s, gx + 0.22, G - 0.9, cx - 0.22, ctop + 0.2, { color: BLUE, width: 1.75, dash: "dash" });
  label(s, "LoRa", M + 2.3, G - 2.2, 0.6, 0.22, { size: 9, bold: true, color: BLUE });
  seg(s, cx + 0.05, ctop - 0.4, mx - 0.1, mtop - 0.3, { color: BLUE, width: 1.75, dash: "dash" });
  label(s, "LoRa mesh", M + 5.0, ctop - 0.95, 1.1, 0.22, { size: 9, bold: true, color: BLUE });
  // names in ground strip
  label(s, "GLD (tiang ± 1–1,5 m)", gx - 0.6, G + 0.06, 1.7, 0.24, { size: 9, bold: true, color: CHAR });
  label(s, "Cluster Head", cx - 0.6, G + 0.06, 1.2, 0.24, { size: 9, bold: true, color: CHAR, align: "center" });
  label(s, "Gateway + antena di tiang atap; router, server & UPS di dalam gedung", BX + 0.1, G + 0.06, BW - 0.2, 0.24, { size: 9, bold: true, color: CHAR, align: "center" });
  // legend
  const leg = [["C0392B", undefined, "Daya (24 VDC / 220 VAC)"], [BLUE, "dash", "LoRa"], [MUTED, "sysDot", "Wi-Fi 2,4 GHz"], [CHAR, undefined, "LAN Cat6"]];
  leg.forEach((l, i) => {
    const x = M + i * 2.45;
    seg(s, x, 6.25, x + 0.5, 6.25, { color: l[0], width: 2, dash: l[1] });
    label(s, l[2], x + 0.6, 6.13, 1.8, 0.24, { size: 9.5 });
  });
  footnote(s, "Skema tidak berskala. Tinggi GLD mengikuti gas target & HSE (RU IV: ± 1,5 m); jumlah & posisi CH/Gateway ditetapkan dari LoRa mapping saat site survey.", 6.6);
  s.addNotes("Satu gambar untuk seluruh rantai: GLD di tiang dengan kabel 24 VDC dari JB/PSU; Cluster Head tenaga surya di tiang 3–5 m; unit Gateway beserta antenanya di tiang atap gedung; router, PC server dan UPS di ruang server/kontrol.");
})();

(function mounting4() {
  const s = slideLight();
  heading(s, "2 · Mekanisme pemasangan", "Cara pemasangan tiap perangkat");
  const cw = 2.9, gap = (W - 2 * M - 4 * cw) / 3;
  const cols = [
    { t: "GLD", c: BLUE, img: ["balongan_13nov/bracket_pelat_tampak_atas.jpg", 899, 1599], cap: "Foto asli: GLD pada pelat mounting & U-bolt.", b: [
      "Pelat 250 × 250 mm + 2 U-bolt 2\" ke tiang pipa 2\"",
      "Tiang baru, ditanam & dicor",
      "Kabel 24 VDC masuk lewat cable gland M20 × 1,5",
      "Tanpa las/bor ke struktur existing",
    ] },
    { t: "Cluster Head", c: BLUE, draw: "ch", cap: "Ilustrasi: unit CH + 1 panel surya di tiang (tidak berskala).", b: [
      "Tiang 3–5 m di atas tanah",
      "Unit + 1 panel surya (hadap Utara, miring 10–15°), diklem U-bolt sesuai diameter tiang",
      "Tanpa kabel daya (surya + baterai)",
      "Di area aman / unclassified",
    ] },
    { t: "Gateway", c: PERTAMINA, draw: "gw", cap: "Ilustrasi: Gateway + antena di tiang atap (tidak berskala).", b: [
      "Tiang di atas roof top (± 2–2,5 m di atas atap)",
      "Unit Gateway & antena terpasang bersama di tiang",
      "Kabel daya dari UPS di ruangan ke atap",
      "Wi-Fi ke router di ruangan bawah; grounding ke penangkal petir",
    ] },
    { t: "Server", c: OK, draw: "server", cap: "Di ruang server/kontrol (ilustrasi).", b: [
      "PC server fisik + router Wi-Fi",
      "Seluruhnya dicatu dari UPS",
      "LAN-1 ke router GLD, LAN-2 ke intranet kantor",
      "Tanpa koneksi internet",
    ] },
  ];
  cols.forEach((c, i) => {
    const x = M + i * (cw + gap), y = 1.55;
    card(s, x, y, cw, 5.3, SURF);
    s.addShape(pres.ShapeType.rect, { x, y, w: cw, h: 0.08, fill: { color: c.c }, line: { color: c.c } });
    const ix = x + 0.12, iy = y + 0.2, iw = cw - 0.24, ih = 2.2;
    if (c.img) {
      imgCover(s, c.img[0], c.img[1], c.img[2], ix, iy, iw, ih);
    } else {
      s.addShape(pres.ShapeType.rect, { x: ix, y: iy, w: iw, h: ih, fill: { color: SURF_2 }, line: { color: LINE } });
      const gy = iy + ih - 0.28, px = ix + iw / 2;
      if (c.draw === "server") {
        box(s, ix + 0.35, iy + 0.18, iw - 0.7, 0.45, "Router Wi-Fi (LGU)", { fill: WHITE, size: 9 });
        box(s, ix + 0.35, iy + 0.82, iw - 0.7, 0.55, "PC server", { fill: PERTAMINA_BG, size: 10 });
        box(s, ix + 0.35, iy + 1.56, iw - 0.7, 0.45, "UPS ≥ 1 kVA", { fill: HOLD_BG, line: HOLD, size: 9 });
      } else if (c.draw === "ch") {
        s.addShape(pres.ShapeType.rect, { x: ix, y: gy, w: iw, h: ih - (gy - iy), fill: { color: "EFE9E1" }, line: { color: "EFE9E1" } });
        s.addShape(pres.ShapeType.rect, { x: px - 0.035, y: iy + 0.45, w: 0.07, h: gy - iy - 0.45, fill: { color: "7D8794" }, line: { color: "5E6773", width: 0.5 } });
        box(s, px - 0.2, iy + 0.5, 0.4, 0.32, "CH", { fill: BLUE, line: BLUE_DK, color: WHITE, size: 9 });
        line(s, px, iy + 0.15, 0, 0.35, CHAR, 1.75);
        [iy + 0.95, iy + 1.15].forEach((yy) => s.addShape(pres.ShapeType.rect, { x: px - 0.09, y: yy, w: 0.18, h: 0.06, fill: { color: WARN }, line: { color: WARN } }));
        label(s, "U-bolt / klem", px + 0.15, iy + 0.95, 1.1, 0.26, { size: 8.5, color: WARN, bold: true });
        s.addShape(pres.ShapeType.rect, { x: px - 0.62, y: iy + 1.42, w: 0.58, h: 0.08, fill: { color: "2E3E66" }, line: { color: "2E3E66" }, rotate: -12 });
        label(s, "panel ×1 → U", px + 0.1, iy + 1.38, 1.1, 0.24, { size: 8.5, color: CHAR });
        seg(s, px - 0.5, iy + 0.5, px - 0.5, gy, { color: MUTED, width: 0.75 });
        label(s, "3–5 m", ix + 0.05, iy + 1.05, px - 0.6 - ix, 0.26, { size: 9.5, bold: true, color: CHAR, align: "right" });
      } else if (c.draw === "gw") {
        const rf = iy + 1.25;
        s.addShape(pres.ShapeType.rect, { x: ix + 0.2, y: rf, w: iw - 0.4, h: iy + ih - rf, fill: { color: WHITE }, line: { color: CHAR_SOFT, width: 1 } });
        const mx = ix + iw - 0.7;
        s.addShape(pres.ShapeType.rect, { x: mx - 0.035, y: iy + 0.45, w: 0.07, h: rf - iy - 0.45, fill: { color: "7D8794" }, line: { color: "5E6773", width: 0.5 } });
        line(s, mx, iy + 0.12, 0, 0.33, CHAR, 2);
        seg(s, mx - 0.3, iy + 0.45, mx - 0.3, rf, { color: MUTED, width: 0.75 });
        label(s, "± 2–2,5 m\ndi atas atap", ix + 0.1, iy + 0.5, mx - 0.4 - ix - 0.1, 0.5, { size: 9, bold: true, color: CHAR, align: "right" });
        box(s, mx - 0.22, iy + 0.42, 0.44, 0.32, "GW", { fill: PERTAMINA, line: PERTAMINA, color: WHITE, size: 9 });
        box(s, ix + 0.4, rf + 0.3, 1.0, 0.36, "Router", { fill: SURF_2, size: 9 });
        seg(s, mx - 0.22, iy + 0.7, ix + 1.4, rf + 0.4, { color: MUTED, width: 1.25, dash: "sysDot" });
        label(s, "ruang di bawah atap", ix + 0.3, rf + 0.65, iw - 0.6, 0.22, { size: 8.5, color: CHAR_SOFT, align: "center" });
      }
    }
    label(s, c.cap, x + 0.12, iy + ih + 0.04, cw - 0.24, 0.36, { size: 8.5, color: MUTED, valign: "top" });
    cardTitle(s, x + 0.15, iy + ih + 0.45, cw - 0.3, c.t, c.c);
    bullets(s, x + 0.15, iy + ih + 0.85, cw - 0.3, 2.0, c.b, 11);
  });
  s.addNotes("Empat perangkat, empat cara pasang. Hanya GLD yang butuh kabel daya di lapangan; CH mandiri tenaga surya; Gateway beserta antena di tiang atap; server dan UPS di ruang server.");
})();

(function gldMountFoto() {
  const s = slideLight();
  heading(s, "3 · Kebutuhan GLD", "Mounting GLD — foto asli bracket & pelat U-bolt");
  const pw = 5.3, fw = 2.6, fh = fw * 1599 / 899;
  s.addImage({ path: ASSET("balongan_13nov/bracket_pelat_tampak_atas.jpg"), x: M, y: 1.6, w: fw, h: fh });
  s.addImage({ path: ASSET("balongan_13nov/bracket_pelat_tampak_samping.jpg"), x: M + pw - fw, y: 1.6, w: fw, h: fh });
  label(s, "Foto asli bracket hasil fabrikasi: unit GLD dibaut ke pelat lewat spacer pada kuping mounting (kiri); batang ulir U-bolt menembus pelat untuk klem ke tiang (kanan).", M, 1.68 + fh, pw, 0.6, { size: 9.5, color: MUTED, valign: "top" });
  const ih = 5.0, iw = ih * 740 / 1372, cx = M + pw + 0.3;
  card(s, cx, 1.55, iw + 0.3, ih + 0.3, WHITE);
  s.addImage({ path: ASSET("balongan_13nov/pelat_ubolt_dimensi.png"), x: cx + 0.15, y: 1.7, w: iw, h: ih });
  label(s, "Gambar kerja pelat 250 × 250 mm & U-bolt (mm), CAD LGU 31/08/2026.", cx, 6.9, iw + 0.3, 0.4, { size: 9, color: MUTED, valign: "top" });
  const x0 = cx + iw + 0.55, w0 = W - M - x0;
  cardTitle(s, x0, 1.6, w0, "Cara pasang", BLUE);
  bullets(s, x0, 2.0, w0, 2.9, [
    "Pelat 250 × 250 mm dikunci ke tiang dengan 2 U-bolt 2\" (M10).",
    "Unit GLD dibaut ke pelat lewat 3 kuping mounting.",
    "Mesh sensor menghadap ke bawah/samping, antena tegak ke atas.",
    "Kabel 24 VDC masuk lewat cable gland M20 × 1,5.",
  ], 11);
  card(s, x0, 5.0, w0, 1.75, WARN_BG);
  s.addText("Pelat dirancang untuk tiang vertikal dan handrail horizontal (simulasi pada slide berikut). Pola lubang diverifikasi LGU dan pelaksana RU sebelum fabrikasi.", {
    x: x0 + 0.15, y: 5.0, w: w0 - 0.3, h: 1.75, isTextBox: true, margin: 0, fontFace: FONT, fontSize: 10.5, bold: true, color: WARN, valign: "middle",
  });
  s.addNotes("Foto asli bracket: pelat sudah difabrikasi, unit GLD dibaut ke pelat dengan spacer, U-bolt menembus pelat ke tiang. Pelat dan U-bolt dibuat pelaksana RU sesuai gambar LGU.");
})();

(function gldUnitViews() {
  const s = slideLight();
  heading(s, "3 · Kebutuhan GLD", "Bentuk casing GLD V2 — acuan simulasi pemasangan");
  const ih = 5.1, iw = ih * 1600 / 1200;
  s.addImage({ path: ASSET("balongan_13nov/unit_gld_4_tampak.jpg"), x: M, y: 1.5, w: iw, h: ih });
  const x0 = M + iw + 0.35, w0 = W - M - x0;
  table(s, [
    ["Tampak", "Yang terlihat"],
    ["Depan (kiri atas)", "Mesh sensor pada tutup depan; antena di atas; cable gland di sisi kiri atas; beacon di kanan"],
    ["Belakang (kanan atas)", "Bidang pasang dengan 3 kuping: 1 atas, 2 bawah"],
    ["Samping (bawah)", "Badan bulat, tutup bergerigi; cable gland & beacon pada dudukan sisi"],
  ], { x: x0, y: 1.55, w: w0, colW: [1.45, w0 - 1.45], size: 10.5, boldFirst: true, rowH: 0.75 });
  card(s, x0, 4.75, w0, 1.8, SURF);
  s.addText("Bidang belakang dibaut ke pelat mounting lewat spacer, sehingga mesh sensor selalu menghadap ke depan dan antena ke atas.", {
    x: x0 + 0.2, y: 4.75, w: w0 - 0.4, h: 1.8, isTextBox: true, margin: 0, fontFace: FONT, fontSize: 11.5, bold: true, color: BLUE, valign: "middle",
  });
  footnote(s, "Foto unit GLD V2 asli (Okt 2026).", 6.9);
  s.addNotes("Foto ini menjadi acuan bentuk casing pada simulasi 3D: mesh di tutup depan, cable gland di sisi kiri atas, beacon di sisi kanan, 3 kuping di belakang.");
})();

(function gldMountSim() {
  const s = slideLight();
  heading(s, "3 · Kebutuhan GLD", "Simulasi 3D pemasangan — tiang vertikal & handrail horizontal");
  const cw = (W - 2 * M - 0.3) / 2, y0 = 1.5, ch = 4.05;
  const IMG = (f) => "balongan_13nov/" + f + ".png";
  // A · tiang vertikal
  card(s, M, y0, cw, ch, WHITE);
  label(s, "A · Tiang vertikal (pipa 2\")", M + 0.2, y0 + 0.1, cw - 0.4, 0.3, { size: 12, bold: true, color: BLUE });
  const hA = 3.35;
  s.addImage({ path: ASSET(IMG("sim3d_tiang")), x: M + 0.2, y: y0 + 0.5, w: hA * 628 / 1411, h: hA });
  s.addImage({ path: ASSET(IMG("sim3d_tiang_belakang")), x: M + 0.35 + hA * 628 / 1411, y: y0 + 0.5, w: hA * 587 / 1411, h: hA });
  label(s, "depan", M + 0.2, y0 + 3.82, 1.3, 0.2, { size: 8.5, color: MUTED, align: "center" });
  label(s, "belakang", M + 0.35 + hA * 628 / 1411, y0 + 3.82, 1.3, 0.2, { size: 8.5, color: MUTED, align: "center" });
  bullets(s, M + 3.2, y0 + 0.55, cw - 3.35, 3.3, [
    "Pipa di tengah pelat, arah vertikal",
    "2 U-bolt horizontal: atas dan bawah",
    "Mesh sensor menghadap ke depan; antena ke atas",
  ], 11);
  // B · handrail horizontal
  const xb = M + cw + 0.3;
  card(s, xb, y0, cw, ch, WHITE);
  label(s, "B · Handrail horizontal (pipa 2\")", xb + 0.2, y0 + 0.1, cw - 0.4, 0.3, { size: 12, bold: true, color: BLUE });
  const wB = 3.0;
  s.addImage({ path: ASSET(IMG("sim3d_handrail")), x: xb + 0.15, y: y0 + 0.45, w: wB, h: wB * 1111 / 1681 });
  const wB2 = 1.75;
  s.addImage({ path: ASSET(IMG("sim3d_handrail_belakang")), x: xb + 0.75, y: y0 + 0.5 + wB * 1111 / 1681, w: wB2, h: wB2 * 1230 / 1681 });
  label(s, "depan", xb + 2.4, y0 + 0.45, 0.8, 0.2, { size: 8.5, color: MUTED });
  label(s, "belakang", xb + 2.8, y0 + 3.3, 0.8, 0.2, { size: 8.5, color: MUTED });
  bullets(s, xb + 3.3, y0 + 0.55, cw - 3.45, 3.3, [
    "Pipa di tengah pelat, arah horizontal",
    "2 U-bolt vertikal: kiri dan kanan",
    "Orientasi GLD sama dengan posisi A",
  ], 11);
  card(s, M, 5.7, 12.1, 0.95, OK_BG);
  s.addText([
    { text: "Rekomendasi desain: ", options: { bold: true } },
    { text: "satu pelat dengan lubang baut GLD tetap dan dua set lubang U-bolt yang saling tegak lurus di sekitar titik tengah pelat. Pola lubang CAD 31/08 diverifikasi, lalu dilakukan uji pasang pada kedua posisi sebelum fabrikasi." },
  ], { x: M + 0.25, y: 5.7, w: 11.6, h: 0.95, isTextBox: true, margin: 0, fontFace: FONT, fontSize: 11.5, color: OK, valign: "middle" });
  footnote(s, "Simulasi 3D LGU, dimensi pendekatan dari foto unit & bracket hasil fabrikasi serta gambar kerja pelat 250 × 250 mm (CAD 31/08/2026); U-bolt 2\" = OD 60,3 mm.", 6.9);
  s.addNotes("Pada kedua posisi pipa melewati titik tengah pelat, GLD tetap tegak dengan mesh sensor menghadap ke depan dan antena ke atas. Yang berubah hanya arah U-bolt: horizontal untuk tiang, vertikal untuk handrail. Simulasi konsep; perlu uji pasang nyata.");
})();

(function gldCableSim() {
  const s = slideLight();
  heading(s, "3 · Kebutuhan GLD", "Simulasi 3D tampak kiri — jalur kabel 24 VDC");
  const cw = (W - 2 * M - 0.3) / 2, y0 = 1.5, ch = 4.2, hI = 3.7;
  const IMG = (f) => ASSET("balongan_13nov/" + f + ".png");
  const cols = [
    ["A · Tiang vertikal", "sim3d_tiang_kiri", 578, [
      "Kabel keluar dari cable gland sisi kiri atas GLD",
      "Naik melewati tepi atas pelat ke sisi belakang",
      "Diikat cable tie sepanjang tiang menuju JB / PSU",
    ]],
    ["B · Handrail horizontal", "sim3d_handrail_kiri", 1348, [
      "Kabel keluar dari cable gland sisi kiri atas GLD",
      "Naik melewati tepi atas pelat ke sisi belakang",
      "Diikat cable tie sepanjang handrail menuju rute kabel",
    ]],
  ];
  cols.forEach((c, i) => {
    const x = M + i * (cw + 0.3), iw = hI * c[2] / 1411;
    card(s, x, y0, cw, ch, WHITE);
    label(s, c[0], x + 0.2, y0 + 0.1, cw - 0.4, 0.3, { size: 12, bold: true, color: BLUE });
    s.addImage({ path: IMG(c[1]), x: x + 0.2, y: y0 + 0.45, w: iw, h: hI });
    const tx = x + 0.4 + iw, tw = x + cw - tx - 0.15;
    bullets(s, tx, y0 + 0.55, tw, 3.4, c[3], 11);
  });
  card(s, M, 5.85, 12.1, 0.8, SURF);
  s.addText([
    { text: "Ketentuan umum: ", options: { bold: true } },
    { text: "kabel armored 2 inti dengan gland tipe armored; beri lengkung bawah (drip loop) sebelum cable gland agar air tidak mengalir ke gland; cable tie stainless/tahan UV; kabel tidak menghalangi mesh sensor dan tidak terjepit U-bolt." },
  ], { x: M + 0.25, y: 5.85, w: 11.6, h: 0.8, isTextBox: true, margin: 0, fontFace: FONT, fontSize: 11.5, color: CHAR, valign: "middle" });
  footnote(s, "Jalur kabel usulan LGU; rute akhir mengikuti standar instalasi kabel RU VI. Simulasi konsep, dimensi pendekatan.", 6.9);
  s.addNotes("Cable gland GLD ada di sisi kiri atas casing. Kabel naik melewati tepi atas pelat ke belakang, lalu diikat sepanjang tiang atau handrail menuju JB/PSU. Beri drip loop sebelum gland. Rute akhir disesuaikan standar RU.");
})();

(function gldTiang() {
  const s = slideLight();
  heading(s, "3 · Kebutuhan GLD", "Kebutuhan pemasangan GLD — catu 24 V, mounting & tiang");
  table(s, [
    ["Kebutuhan", "Spesifikasi", "Per titik", "Oleh"],
    ["Catu daya", "24 VDC, kapasitas sumber ≥ 1 A per GLD (konsumsi maks. ± 8 W ≈ 0,33 A); GLD tidak menerima 220 VAC", "1 jalur", "RU VI"],
    ["Kabel daya", "2 inti tembaga berarmor, ukuran mengikuti jarak (drop ≤ 5 %); home-run per GLD dari PSU/JB", "1", "RU VI"],
    ["Tiang", "Pipa galvanis 2\" Sch40, OD 60,3 mm (wajib — menyesuaikan U-bolt); tiang baru, ditanam & dicor", "1", "RU VI"],
    ["Tinggi", "Batang 1,6 m: 1,0 m di atas tanah + 0,6 m tertanam (RU IV: stanchion 1,5 m); tinggi sensor mengikuti gas target & HSE (Lampiran B)", "—", "RU VI + LGU"],
    ["Pondasi", "Cor 40 × 40 × 60 cm, fc' ≥ 20 MPa; angkur silang di ujung bawah; pipe cap di ujung atas", "1", "RU VI"],
    ["Pelat mounting", "Pelat baja 250 × 250 mm sesuai gambar LGU", "1", "RU VI"],
    ["U-bolt & mur", "2\"/DN50 untuk OD 60,3 mm, ulir M10; mur + ring datar + ring per, anti-karat (SS316 dekat laut)", "2 + 4 set", "RU VI"],
    ["Terminasi & energize", "Cable gland M20 × 1,5; terminasi L+/L−, energize & commissioning", "—", "LGU"],
  ], { x: M, y: 1.6, w: 12.1, colW: [1.9, 7.3, 1.3, 1.6], size: 10.5, boldFirst: true, rowH: 0.5 });
  footnote(s, "Larangan: tanpa PVC pada housing/bracket; tanpa bor/las ke struktur existing kilang. " + SRC_SPEK, 6.75);
  s.addNotes("Ringkasan kebutuhan per titik GLD. Detail ukuran kabel vs jarak di slide berikutnya; detail tiang & pondasi di Lampiran A.");
})();

// ---------------------------------------------------------------- D · catu daya & kabel
(function gldDaya() {
  const s = slideLight();
  heading(s, "3 · Kebutuhan GLD", "Catu daya 24 VDC — hanya GLD yang perlu kabel daya");
  const opts = [
    ["Opsi A — PSU per titik", "PSU 24 VDC ≥ 1 A (disarankan 2,5 A DIN-rail) per GLD, di box terdekat yang ada 220 VAC; MCB 2 A sisi AC.", "Kabel pendek (umumnya ≤ 50 m) → cukup 2 × 1,5 mm².", 1],
    ["Opsi B — PSU pusat", "Satu PSU 24 VDC ≥ 6 A (4 × 1 A + cadangan) di panel/ruang kontrol; MCB/sekring DC 2 A per jalur.", "Tiap GLD ditarik kabel sendiri (home-run), tidak berantai; ukuran kabel mengikuti jarak.", 4],
  ];
  opts.forEach((o, i) => {
    const x = M + i * 6.15, y = 1.55, w = 5.95;
    card(s, x, y, w, 2.55, SURF);
    cardTitle(s, x + 0.2, y + 0.12, w - 0.4, o[0], BLUE);
    // alur mini
    const fy = y + 0.6;
    const boxes = i === 0 ? ["220 VAC", "PSU 24 V", "GLD"] : ["220 VAC", "PSU 24 V ≥6 A", "GLD × 4"];
    boxes.forEach((b, k) => {
      const bx = x + 0.2 + k * 1.95;
      s.addShape(pres.ShapeType.roundRect, { x: bx, y: fy, w: 1.45, h: 0.42, rectRadius: 0.06, fill: { color: k === 2 ? BLUE : WHITE }, line: { color: k === 2 ? BLUE : LINE } });
      label(s, b, bx, fy, 1.45, 0.42, { size: 10, bold: true, color: k === 2 ? WHITE : CHAR, align: "center" });
      if (k < 2) {
        line(s, bx + 1.47, fy + 0.21, 0.46, 0, CHAR, 1.25);
        label(s, k === 0 ? "MCB" : "kabel 2 inti", bx + 1.3, fy + 0.43, 0.8, 0.2, { size: 8, color: MUTED, align: "center" });
      }
    });
    label(s, o[1], x + 0.2, y + 1.3, w - 0.4, 0.6, { size: 10.5, valign: "top" });
    label(s, o[2], x + 0.2, y + 1.9, w - 0.4, 0.55, { size: 10.5, bold: true, color: CHAR, valign: "top" });
  });
  table(s, [
    ["Luas penampang", "Resistansi (Ω/km)", "Maks. @ 1 A (desain)", "Maks. @ 0,33 A (aktual)"],
    ["2 × 1,5 mm²", "12,1", "50 m", "150 m"],
    ["2 × 2,5 mm²", "7,41", "80 m", "245 m"],
    ["2 × 4 mm²", "4,61", "130 m", "390 m"],
    ["2 × 6 mm²", "3,08", "195 m", "590 m"],
  ], { x: M, y: 4.3, w: 7.2, colW: [1.7, 1.7, 1.9, 1.9], size: 11, boldFirst: true, rowH: 0.4 });
  card(s, 8.05, 4.3, 4.67, 2.0, PERTAMINA_BG);
  s.addText([
    { text: "Panjang kabel per titik", options: { bold: true, color: PERTAMINA, fontSize: 12.5, breakLine: true } },
    { text: "= rute aktual × 1,10 + 3 m (sisi PSU) + 3 m (sisi GLD)", options: { bold: true, color: CHAR, fontSize: 12, breakLine: true } },
    { text: "Ukur rute kabel, bukan garis lurus. Pilih ukuran dari kolom 1 A (desain). Jarak > 195 m → pakai Opsi A untuk titik itu.", options: { color: CHAR_SOFT, fontSize: 10.5 } },
  ], { x: 8.25, y: 4.4, w: 4.3, h: 1.8, isTextBox: true, margin: 0, fontFace: FONT, valign: "top", paraSpaceAfter: 4 });
  footnote(s, "Panjang maksimum satu arah PSU → GLD agar drop tegangan ≤ 5 % (1,2 V dari 24 V), kabel tembaga 2 inti pada 20 °C. GLD tidak menerima 220 VAC; konsumsi maks. ± 8 W (≈ 0,33 A). " + SRC_SPEK, 6.6);
  s.addNotes("Pilihan Opsi A atau B diputuskan RU VI setelah survey, tergantung ketersediaan 220 VAC di dekat titik GLD. Di RU IV, MoC menyebut kabel 24 VDC armored lewat junction box — pola serupa bisa dipakai di RU VI.");
})();

(function chSlide() {
  const s = slideLight();
  heading(s, "4 · Kebutuhan Cluster Head", "Tiang & U-bolt sesuai, tinggi 3–5 m, 1 panel surya");
  card(s, M, 1.55, 4.3, 5.2, WHITE);
  const G = 6.15, px = M + 2.2, top = 2.05;
  s.addShape(pres.ShapeType.rect, { x: M + 0.15, y: G, w: 4.0, h: 0.45, fill: { color: "EFE9E1" }, line: { color: "EFE9E1" } });
  line(s, M + 0.15, G, 4.0, 0, "8A7F72", 1.5);
  s.addShape(pres.ShapeType.rect, { x: px - 0.06, y: top + 1.6, w: 0.12, h: G - top - 1.6 + 0.4, fill: { color: "6E7884" }, line: { color: "5E6773", width: 0.5 } });
  s.addShape(pres.ShapeType.rect, { x: px - 0.04, y: top, w: 0.08, h: 1.62, fill: { color: "7D8794" }, line: { color: "5E6773", width: 0.5 } });
  label(s, "bawah 3\"", px + 0.15, top + 2.6, 0.9, 0.24, { size: 8.5, color: CHAR_SOFT });
  label(s, "atas 2\"", px + 0.15, top + 0.9, 0.9, 0.24, { size: 8.5, color: CHAR_SOFT });
  box(s, px - 0.22, top + 0.05, 0.44, 0.36, "CH", { fill: BLUE, line: BLUE_DK, color: WHITE, size: 9 });
  line(s, px, top - 0.4, 0, 0.42, CHAR, 1.75);
  [top + 0.55, top + 0.75].forEach((yy) => s.addShape(pres.ShapeType.rect, { x: px - 0.11, y: yy, w: 0.22, h: 0.06, fill: { color: WARN }, line: { color: WARN } }));
  label(s, "U-bolt / klem sesuai OD pipa", px + 0.18, top + 0.5, 1.75, 0.4, { size: 8.5, color: WARN, bold: true });
  // 1 panel surya, sisi Utara (kiri), miring 10–15°
  seg(s, px - 0.25, top + 1.22, px - 0.04, top + 1.22, { color: CHAR_SOFT, width: 1.5 });
  s.addShape(pres.ShapeType.rect, { x: px - 1.15, y: top + 1.05, w: 0.95, h: 0.1, fill: { color: "2E3E66" }, line: { color: "1E2A47" }, rotate: -12 });
  label(s, "1 panel surya\nhadap Utara, miring 10–15°", px + 0.15, top + 1.15, 1.9, 0.45, { size: 8.5, bold: true, color: "2E3E66" });
  s.addShape(pres.ShapeType.line, { x: M + 0.3, y: top + 2.15, w: 0.55, h: 0, line: { color: CHAR, width: 1.5, beginArrowType: "triangle" } });
  label(s, "U", M + 0.9, top + 2.03, 0.3, 0.24, { size: 10, bold: true, color: CHAR });
  seg(s, M + 1.2, top + 0.05, M + 1.2, G, { color: MUTED, width: 0.75 });
  label(s, "3–5 m", M + 0.25, top + 2.7, 0.85, 0.3, { size: 11, bold: true, color: CHAR, align: "right" });
  label(s, "Ilustrasi, tidak berskala", M + 0.15, 1.65, 2.0, 0.22, { size: 8.5, color: MUTED });
  const x0 = M + 4.6, w0 = W - M - x0;
  table(s, [
    ["Item", "Ketentuan"],
    ["Tinggi pasang", "3–5 m di atas tanah; nilai final per titik dari LoRa mapping (line of sight ke GLD dan CH/Gateway berikutnya)"],
    ["Tiang", "Pipa baja galvanis celup panas; 2\" Sch40, atau sambungan bawah 3\" / atas 2\" untuk tiang tinggi (RU IV: total 5.000 mm)"],
    ["U-bolt / klem", "Ukuran mengikuti OD pipa di titik klem: 2\" = OD 60,3 mm; 3\" = OD 88,9 mm. Unit CH & panel dari LGU dipasang di bagian atas tiang 2\""],
    ["Pondasi", "Ditanam ± 1,0–1,2 m; cor 50 × 50 × 100–120 cm, fc' ≥ 20 MPa; guy wire bila tiang tinggi / angin kencang"],
    ["Daya", "Tanpa kabel daya — 1 panel surya + baterai di unit (dari LGU)"],
    ["Arah panel", "Menghadap Utara sejati (azimut 0°; lokasi di selatan khatulistiwa — Balongan ± 6,3° LS); kemiringan 10–15° agar bersih oleh air hujan; bebas bayangan 09.00–15.00"],
    ["Lokasi", "Area aman / unclassified (RU IV: pagar pembatas SRU); panel tidak terhalang bayangan, antena jauh dari halangan logam"],
    ["Grounding & label", "Bonding tiang ke grounding RU; label nomor CH sama dengan dashboard"],
  ], { x: x0, y: 1.6, w: w0, colW: [1.55, w0 - 1.55], size: 10, boldFirst: true, rowH: 0.56 });
  footnote(s, "Arah panel: praktik umum PV di selatan khatulistiwa (hadap Utara, kemiringan ≥ 10° untuk self-cleaning; optimum tetap di Jawa ± 7–8°). " + SRC_SPEK, 6.85);
  s.addNotes("Hasil rapat: CH memakai 1 panel surya. Karena Balongan dan Cilacap berada di selatan khatulistiwa, panel menghadap Utara sejati (pakai kompas, koreksi deklinasi kecil) dengan kemiringan 10–15°: sedikit di atas optimum ± 7–8° supaya debu luruh oleh hujan. Pastikan tidak ada bayangan tangki, pipa, atau unit CH sendiri pada jam 09.00–15.00. Tinggi CH 3–5 m, tiang dan U-bolt harus sesuai diameter pipa. Di RU IV tiang CH berupa pipa bawah 3 inci dan atas 2 inci setinggi 5 m. Tinggi final ditentukan dari LoRa mapping.");
})();

(function gwSlide() {
  const s = slideLight();
  heading(s, "5 · Kebutuhan Gateway", "Tiang di atas roof top — Gateway & antena menjadi satu");
  card(s, M, 1.55, 4.65, 5.2, WHITE);
  const bx = M + 0.25, bw = 4.15, R = 3.65;
  s.addShape(pres.ShapeType.rect, { x: bx, y: R, w: bw, h: 6.5 - R, fill: { color: SURF }, line: { color: CHAR_SOFT, width: 1 } });
  s.addShape(pres.ShapeType.rect, { x: bx - 0.05, y: R - 0.1, w: bw + 0.1, h: 0.1, fill: { color: CHAR_SOFT }, line: { color: CHAR_SOFT } });
  s.addShape(pres.ShapeType.rect, { x: bx - 0.05, y: R - 0.35, w: 0.12, h: 0.25, fill: { color: CHAR_SOFT }, line: { color: CHAR_SOFT } });
  s.addShape(pres.ShapeType.rect, { x: bx + bw - 0.07, y: R - 0.35, w: 0.12, h: 0.25, fill: { color: CHAR_SOFT }, line: { color: CHAR_SOFT } });
  const mx = bx + 3.1, mtop = 2.25;
  s.addShape(pres.ShapeType.rect, { x: mx - 0.3, y: R - 0.18, w: 0.6, h: 0.08, fill: { color: CHAR }, line: { color: CHAR } });
  s.addShape(pres.ShapeType.rect, { x: mx - 0.035, y: mtop, w: 0.07, h: R - 0.18 - mtop, fill: { color: "7D8794" }, line: { color: "5E6773", width: 0.5 } });
  line(s, mx, mtop - 0.5, 0, 0.5, CHAR, 2.5);
  box(s, mx - 0.3, mtop - 0.05, 0.6, 0.42, "GW", { fill: PERTAMINA, line: PERTAMINA, color: WHITE, size: 10 });
  label(s, "antena omni 8 dBi", mx + 0.12, mtop - 0.5, 1.2, 0.24, { size: 8.5, color: CHAR });
  label(s, "unit Gateway", mx + 0.36, mtop + 0.05, 1.0, 0.24, { size: 8.5, color: CHAR });
  seg(s, mx - 0.45, mtop - 0.5, mx - 0.45, R - 0.1, { color: MUTED, width: 0.75 });
  label(s, "± 2–2,5 m\ndi atas atap", mx - 1.6, mtop + 0.2, 1.1, 0.5, { size: 9.5, bold: true, color: CHAR, align: "right" });
  label(s, "base plate / ballast", mx - 1.75, R - 0.38, 1.4, 0.22, { size: 8, color: CHAR_SOFT, align: "right" });
  box(s, bx + 0.25, R + 0.95, 1.25, 0.45, "Router Wi-Fi", { fill: SURF_2 });
  seg(s, mx - 0.3, mtop + 0.3, bx + 1.5, R + 1.0, { color: MUTED, width: 1.5, dash: "sysDot" });
  label(s, "Wi-Fi 2,4 GHz", bx + 1.4, R + 0.55, 1.1, 0.22, { size: 8, color: MUTED });
  box(s, bx + 0.25, R + 2.05, 3.4, 0.4, "UPS", { fill: HOLD_BG, line: HOLD });
  seg(s, bx + 0.87, R + 1.4, bx + 0.87, R + 2.05, { color: "C0392B", width: 1.5 });
  seg(s, mx + 0.12, mtop + 0.37, mx + 0.12, R + 2.05, { color: "C0392B", width: 1.5 });
  label(s, "kabel daya GW", mx + 0.2, R + 1.2, 1.1, 0.22, { size: 8, color: "C0392B" });
  label(s, "Ruang di bawah atap", bx + 0.15, R + 0.05, 2.1, 0.24, { size: 8.5, bold: true, color: PERTAMINA });
  const x0 = M + 4.9, w0 = W - M - x0;
  table(s, [
    ["Item", "Ketentuan"],
    ["Tiang atap", "Pipa galvanis 2\"; puncak antena ± 2–2,5 m di atas atap dan lebih tinggi dari antena CH"],
    ["Unit Gateway", "Dipasang di tiang bersama antena (outdoor, enclosure tahan cuaca); tanpa kabel koaksial panjang"],
    ["Dudukan tiang", "Base plate dibaut ke struktur beton/parapet, atau pemberat (ballast) — tanpa merusak lapisan kedap air atap; guy wire bila perlu"],
    ["Antena", "Omni 8 dBi, 920–923 MHz (dari LGU), menyatu dengan unit Gateway"],
    ["Daya", "Kabel daya dari UPS di ruangan ke atap; sleeve disegel + drip loop di titik tembus"],
    ["Komunikasi", "Wi-Fi 2,4 GHz ke router di ruangan terdekat di bawah atap; kuat sinyal dicek saat survey"],
    ["Grounding", "Tiang & unit ke grounding; berada dalam zona lindung penangkal petir gedung"],
  ], { x: x0, y: 1.6, w: w0, colW: [1.5, w0 - 1.5], size: 10.5, boldFirst: true, rowH: 0.5 });
  card(s, x0, 5.7, w0, 0.95, PERTAMINA_BG);
  s.addText("Mohon RU VI menyiapkan akses & izin kerja di atap gedung kandidat. Gedung dan posisi tiang ditetapkan dari LoRa mapping; ruangan di bawahnya untuk router & UPS.", {
    x: x0 + 0.2, y: 5.7, w: w0 - 0.4, h: 0.95, isTextBox: true, margin: 0, fontFace: FONT, fontSize: 11, bold: true, color: PERTAMINA, valign: "middle",
  });
  footnote(s, "Dudukan tiang atap & rute kabel daya adalah usulan — disesuaikan standar sipil & bangunan RU VI. Skema tidak berskala.", 6.85);
  s.addNotes("Hasil rapat: Gateway memakai tiang di atas roof top, bukan tiang tanam di tanah. Unit Gateway dipasang di tiang bersama antenanya, tidak terpisah, jadi tidak perlu kabel koaksial panjang; yang ditarik ke atap hanya kabel daya dari UPS. Router diletakkan di ruangan tepat di bawah atap agar Wi-Fi dari Gateway kuat. Tiang atap tidak boleh merusak waterproofing tanpa persetujuan tim sipil RU.");
})();

(function serverUps() {
  const s = slideLight();
  heading(s, "6 · Server & UPS", "PC server lokal & UPS — tanpa internet");
  const nodes = [["Cluster Head\n(LoRa mesh)", BLUE], ["Gateway + antena\n(tiang atap)", BLUE], ["Router LGU\n(Wi-Fi 2,4 GHz)", BLUE], ["PC server\n(LAN 1)", PERTAMINA], ["Intranet kantor\n(LAN 2)", PERTAMINA]];
  const links = ["LoRa", "Wi-Fi", "Cat6", "Cat6"];
  nodes.forEach((n, i) => {
    const x = M + i * 2.48;
    s.addShape(pres.ShapeType.roundRect, { x, y: 1.65, w: 1.9, h: 0.85, rectRadius: 0.08, fill: { color: n[1] }, line: { color: n[1] } });
    s.addText(n[0], { x, y: 1.65, w: 1.9, h: 0.85, isTextBox: true, margin: 0, fontFace: FONT, fontSize: 11.5, bold: true, color: WHITE, align: "center", valign: "middle" });
    if (i < links.length) {
      s.addShape(pres.ShapeType.line, { x: x + 1.92, y: 2.07, w: 0.54, h: 0, line: { color: CHAR, width: 1.5, endArrowType: "triangle" } });
      s.addText(links[i], { x: x + 1.75, y: 2.55, w: 0.9, h: 0.3, isTextBox: true, margin: 0, fontFace: FONT, fontSize: 9, color: MUTED, align: "center" });
    }
  });
  // UPS bar under GW, router, PC
  s.addShape(pres.ShapeType.roundRect, { x: M + 2.48, y: 2.95, w: 2.48 * 2 + 1.9, h: 0.4, rectRadius: 0.06, fill: { color: HOLD_BG }, line: { color: HOLD } });
  s.addText("UPS ≥ 1 kVA — mencatu Gateway, router & PC server", { x: M + 2.48, y: 2.95, w: 2.48 * 2 + 1.9, h: 0.4, isTextBox: true, margin: 0, fontFace: FONT, fontSize: 11, bold: true, color: HOLD, align: "center", valign: "middle" });
  table(s, [
    ["Kebutuhan", "Spesifikasi acuan", "Oleh"],
    ["PC server", "PC fisik, 4 core / 8 GB RAM / SSD 256 GB, 2 port LAN (boleh USB-LAN); MQTT broker, Node-RED, aplikasi & database dipasang LGU", "RU VI (PC) · LGU (aplikasi)"],
    ["UPS", "≥ 1 kVA; mencatu PC server (220 VAC), router & Gateway (adaptor 5 VDC) agar data & alarm tetap berjalan saat listrik padam", "RU VI"],
    ["Lokasi", "Ruang server/kontrol; router di ruangan tepat di bawah tiang Gateway di atap", "RU VI"],
    ["Stop kontak dari UPS", "Ruang di bawah atap min. 2 (daya GW & router); ruang server min. 3", "RU VI"],
    ["Kabel Cat6 & intranet", "Router ↔ PC (≤ 90 m/segmen); PC LAN-2 ↔ titik intranet kantor", "RU VI / IT RU VI"],
    ["Router", "Wi-Fi 2,4 GHz tanpa WAN/SIM", "LGU"],
  ], { x: M, y: 3.55, w: 12.1, colW: [2.3, 7.4, 2.4], size: 10.5, boldFirst: true, rowH: 0.4 });
  footnote(s, "Tanpa internet. PC tidak meneruskan lalu lintas antara jaringan GLD dan intranet; dari kantor hanya dashboard/API yang diakses. Spesifikasi PC sama dengan MoC RU IV.", 6.75);
  s.addNotes("Minta RU VI menunjukkan kandidat ruang Gateway & ruang server saat survey, termasuk rute kabel antar-ruang dan titik intranet terdekat. Perlu keterlibatan tim IT RU VI. UPS penting agar alarm tetap terkirim saat listrik padam.");
})();

(function mapSatelit() {
  const s = slideLight();
  heading(s, "7 · Contoh map RU IV Cilacap", "Layout titik perangkat — area SRU");
  const iw = 8.1, ih = iw * 613 / 1182;
  s.addImage({ path: ASSET("balongan_13nov/cilacap_layout_satelit.jpg"), x: M, y: 1.6, w: iw, h: ih });
  label(s, "Rencana titik GLD, CH, JB & Gateway di citra satelit area SRU; garis = jalur komunikasi rencana.", M, 1.65 + ih, iw, 0.3, { size: 9.5, color: MUTED, valign: "top" });
  const x0 = M + iw + 0.25, w0 = W - M - x0;
  table(s, [
    ["Perangkat", "Jml", "Catu & tinggi"],
    ["GLD", "4", "24 VDC dari PSU via JB-01; ± 1,5 m, tiang 2\" baru"],
    ["Cluster Head", "5", "Surya + baterai; di pagar pembatas SRU"],
    ["Junction Box", "1", "Pipe support PS27"],
    ["Gateway + antena", "1", "220 VAC (UPS); antena ± 2–2,5 m di atas atap Control Room SRU"],
    ["PC server & router", "1 set", "Control Room SRU (ruang server lokal)"],
  ], { x: x0, y: 1.6, w: w0, colW: [1.35, 0.55, w0 - 1.9], size: 9.5, boldFirst: true, rowH: 0.55 });
  card(s, M, 6.15, 12.1, 0.55, PERTAMINA_BG);
  s.addText("Contoh referensi format layout. Titik dan layout RU VI ditetapkan RU VI setelah site survey dan LoRa mapping.", {
    x: M + 0.2, y: 6.15, w: 11.7, h: 0.55, isTextBox: true, margin: 0, fontFace: FONT, fontSize: 11.5, bold: true, color: PERTAMINA, valign: "middle",
  });
  footnote(s, SRC_MOC, 6.85);
  s.addNotes("Contoh nyata dari MoC RU IV. Di Balongan, layout dibuat setelah site survey dan LoRa mapping.");
})();

(function mapHac() {
  const s = slideLight();
  heading(s, "7 · Contoh map RU IV Cilacap", "Plot titik terhadap Hazardous Area Classification (HAC)");
  const iw = 7.2, ih = iw * 625 / 1118;
  s.addImage({ path: ASSET("balongan_13nov/cilacap_hac_plot.jpg"), x: M, y: 1.6, w: iw, h: ih });
  label(s, "Potongan plot HAC SRU (A21000-A1-90-609 Sheet 1): arsir = area terklasifikasi.", M, 1.65 + ih, iw, 0.3, { size: 9.5, color: MUTED, valign: "top" });
  const x0 = M + iw + 0.25, w0 = W - M - x0;
  table(s, [
    ["Perangkat", "Klasifikasi", "Status"],
    ["GLD-01 s.d. 04", "Class I, Groups C/D, Div. 2", "Menunggu sertifikat Ex"],
    ["JB-01 (PS27)", "Class I, Groups C/D, Div. 2", "Memenuhi"],
    ["CH-01 s.d. 05", "Unclassified", "Memenuhi"],
    ["Gateway", "Unclassified (antena di atap)", "Memenuhi"],
  ], { x: x0, y: 1.6, w: w0, colW: [1.4, 1.85, w0 - 3.25], size: 10, boldFirst: true, rowH: 0.55 });
  card(s, x0, 4.6, w0, 1.4, WARN_BG);
  s.addText("Contoh format verifikasi titik terhadap HAC. Penetapan titik dan klasifikasi area di RU VI merupakan kewenangan RU VI berdasarkan HAC dan kebijakan HSE RU VI.", {
    x: x0 + 0.2, y: 4.6, w: w0 - 0.4, h: 1.4, isTextBox: true, margin: 0, fontFace: FONT, fontSize: 10.5, bold: true, color: WARN, valign: "middle",
  });
  footnote(s, SRC_MOC, 6.85);
  s.addNotes("Contoh format verifikasi titik terhadap HAC dari RU IV. Keputusan di RU VI ditetapkan RU VI sendiri. Minta gambar HAC RU VI sebelum atau saat survey.");
})();

(function mapKabel() {
  const s = slideLight();
  heading(s, "7 · Contoh map RU IV Cilacap", "Layout jalur kabel 24 VDC & cable schedule");
  const ih = 5.15, iw = ih * 1743 / 1356;
  card(s, M, 1.5, iw + 0.2, ih + 0.1, WHITE);
  s.addImage({ path: ASSET("balongan_13nov/cilacap_layout_kabel.png"), x: M + 0.1, y: 1.55, w: iw, h: ih });
  label(s, "Overall layout cable GLD installation (isometrik, NTS): biru = kabel 1 pair ke GLD, magenta = multipair ke JB.", M, 6.7, iw + 0.2, 0.3, { size: 9, color: MUTED, valign: "top" });
  const x0 = M + iw + 0.45, w0 = W - M - x0;
  table(s, [
    ["Dari → ke", "Kabel", "Est. panjang"],
    ["Control Room → JB-01", "8 pair 14 AWG armored", "125 m"],
    ["Control Room → antena GW", "—", "105 m"],
    ["JB-01 → GLD-01", "1 pair 14 AWG armored", "82 m"],
    ["JB-01 → GLD-02", "1 pair 14 AWG armored", "165 m"],
    ["JB-01 → GLD-03", "1 pair 14 AWG armored", "200 m"],
    ["JB-01 → GLD-04", "1 pair 14 AWG armored", "265 m"],
  ], { x: x0, y: 1.55, w: w0, colW: [1.95, 1.75, w0 - 3.7], size: 9.5, boldFirst: true, rowH: 0.45 });
  bullets(s, x0, 5.0, w0, 1.6, [
    "PSU 24 VDC di Control Room → multipair ke JB-01 → 1 pair ke tiap GLD lewat cable tray eksisting/baru.",
    "Panjang = rute survey + allowance 5–10 %.",
    "Di RU VI, rute & panjang ditetapkan setelah titik dipilih (lihat slide catu daya GLD).",
  ], 10);
  footnote(s, SRC_MOC + " Drawing: DWG-LAYOUT-CABLE-GLD-001.", 7.0);
  s.addNotes("Cable schedule hasil survey RU IV. Panjang kabel GLD berkisar 82–265 m dari JB, sehingga ukuran kabel dan lokasi PSU perlu dihitung per titik.");
})();

// ================================================================ 9 · penempatan & sertifikasi
(function sertifikasi() {
  const s = slideLight();
  heading(s, "Sertifikasi & penempatan", "Progres sertifikasi Ex GLD dan penentuan lokasi pemasangan");
  card(s, M, 1.65, 5.9, 3.7, SURF);
  cardTitle(s, M + 0.3, 1.85, 5.3, "Progres sertifikasi Ex GLD (LGU)");
  bullets(s, M + 0.3, 2.3, 5.3, 3.9, [
    "Target klasifikasi: II 2G Ex db IIC T4 Gb (Zona 1, flameproof).",
    "Formulir aplikasi dan dokumen teknis telah diajukan melalui agen sertifikasi.",
    "Sampel unit GLD telah dikirim untuk pengujian.",
    "Pengukuran suhu internal dan pre-scan EMC telah dilakukan.",
    "Tahap berjalan: revisi dokumen teknis sesuai masukan agen; sertifikat belum terbit.",
  ], 14.5);
  card(s, 6.75, 1.65, 5.95, 3.7, PERTAMINA_BG);
  cardTitle(s, 7.05, 1.85, 5.4, "Lokasi pemasangan (kewenangan RU VI)", PERTAMINA);
  bullets(s, 7.05, 2.3, 5.4, 3.9, [
    "Penetapan titik pemasangan dan klasifikasi area merupakan kewenangan RU VI berdasarkan HAC.",
    "Keputusan mengikuti kebijakan HSE RU VI.",
    "LGU memberikan masukan teknis: jangkauan LoRa, tinggi sensor per jenis gas, kebutuhan daya dan mounting.",
    "Cluster Head dan Gateway ditempatkan di area aman / unclassified.",
  ], 14.5);
  card(s, M, 5.55, 12.1, 0.6, WARN_BG);
  s.addText("Permintaan ke RU VI: gambar Hazardous Area Classification (HAC) dan plot plan area kandidat, sebelum atau saat site survey.", {
    x: M + 0.25, y: 5.55, w: 11.6, h: 0.6, isTextBox: true, margin: 0, fontFace: FONT, fontSize: 12, bold: true, color: WARN, valign: "middle",
  });
  s.addNotes("Sertifikasi Ex adalah lingkup LGU dan sedang berjalan. Penentuan lokasi dan klasifikasi area adalah kewenangan RU VI; LGU hanya memberi masukan teknis.");
})();

// ================================================================ 10 · gas per RU / chamber
(function chamber() {
  const s = slideLight();
  heading(s, "Penyesuaian", "Gas target disesuaikan per RU — dataset diambil di lokasi");
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
  heading(s, "Rencana", "Tahapan implementasi di RU VI Balongan");
  const steps = [
    ["Rapat koordinasi", "13 Nov 2026", "LGU & RU VI"],
    ["Site survey & LoRa mapping", "Uji jangkauan → jumlah & posisi CH/GW", "LGU & RU VI"],
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
  heading(s, "Rencana", "Persiapan site survey awal");
  const cols = [
    ["Yang diperiksa tim LGU", BLUE, SURF, [
      "Kandidat titik GLD: sumber bocor (flange/valve), arah angin, tinggi pasang",
      "Klasifikasi area tiap titik (HAC)",
      "LoRa mapping: uji jangkauan (RSSI/SNR) titik GLD → CH → mast Gateway, untuk menetapkan jumlah & posisi CH/GW",
      "Sumber 220 VAC / 24 VDC terdekat & rute kabel",
      "Atap untuk tiang Gateway (unit + antena), jalur kabel daya dari UPS, ruang router & server, titik intranet",
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
    "Jumlah unit final: 4 GLD; CH & GW setelah LoRa mapping",
    "Mekanisme MoC & izin kerja, serta estimasi waktunya",
    "Pelaksana instalasi fisik (tim internal / kontraktor RU)",
    "Sumber 24 VDC/220 VAC & standar kabel/grounding",
    "Atap untuk tiang Gateway, ruang router, PC server & UPS",
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

// ================================================================ LAMPIRAN · detail teknis instalasi
function lampHead(s, huruf, title) { heading(s, "Lampiran " + huruf, title); }
function line(s, x, y, w, h, color, width, dash) {
  s.addShape(pres.ShapeType.line, { x, y, w, h, line: { color: color || CHAR, width: width || 1, dashType: dash } });
}
function label(s, text, x, y, w, h, o = {}) {
  s.addText(text, {
    x, y, w, h: h || 0.3, isTextBox: true, margin: 0, fontFace: FONT, fontSize: o.size || 10,
    bold: !!o.bold, color: o.color || CHAR_SOFT, align: o.align || "left", valign: o.valign || "middle",
  });
}

// ---------------------------------------------------------------- pembatas
(function lampiranCover() {
  const s = slideDark();
  s.addText("LAMPIRAN", { x: M, y: 0.92, w: 9, h: 0.3, isTextBox: true, margin: 0, fontFace: FONT, fontSize: 11.5, bold: true, charSpacing: 1.8, color: "9FB4E6" });
  s.addText("Detail teknis instalasi", { x: M, y: 1.3, w: 11, h: 0.8, isTextBox: true, margin: 0, fontFace: SERIF, fontSize: 34, bold: true, color: WHITE });
  s.addText("Acuan untuk pelaksana instalasi RU VI, diambil dari spesifikasi yang sudah disusun untuk RU IV Cilacap. Angka final RU VI ditetapkan setelah site survey.", {
    x: M, y: 2.15, w: 10.5, h: 0.7, isTextBox: true, margin: 0, fontFace: FONT, fontSize: 14, color: "CFD8EA",
  });
  const items = [
    ["A", "Tiang & pondasi (GLD, CH, tiang atap Gateway)"], ["B", "Tinggi sensor GLD per jenis gas"],
    ["C", "Terminasi kabel di unit GLD"], ["D", "Antena Gateway & jaringan lokal"],
    ["E", "Perkiraan daftar material (BoQ) RU VI"],
  ];
  items.forEach((it, i) => {
    const col = i % 2, row = Math.floor(i / 2);
    const x = M + col * 6.15, y = 3.2 + row * 0.82;
    badge(s, x, y, it[0], 0.46, BLUE);
    s.addText(it[1], { x: x + 0.62, y: y - 0.04, w: 5.3, h: 0.54, isTextBox: true, margin: 0, fontFace: FONT, fontSize: 15, bold: true, color: WHITE, valign: "middle" });
  });
  s.addNotes("Lampiran ini tidak dipresentasikan satu per satu; dibuka saat diskusi teknis bila RU VI menanyakan detail tiang, tinggi sensor, terminasi, antena, atau BoQ.");
})();

(function lampA() {
  const s = slideLight();
  lampHead(s, "A", "Tiang & pondasi — GLD, Cluster Head, tiang atap Gateway");
  const G = 5.75, U = 0.58;
  card(s, M, 1.55, 5.2, 5.25, WHITE);
  s.addShape(pres.ShapeType.rect, { x: M + 0.15, y: G, w: 4.9, h: 0.9, fill: { color: "EFE9E1" }, line: { color: "EFE9E1" } });
  line(s, M + 0.15, G, 4.9, 0, "8A7F72", 1.5);
  const poles = [
    { x: M + 0.75, up: 1.0, dn: 0.6, fw: 0.40, upTxt: "1,0 m", name: "Tiang GLD", sub: "1,6 m total" },
    { x: M + 2.15, up: 5.0, dn: 1.2, fw: 0.50, upTxt: "3–5 m", name: "Tiang CH", sub: "4,0–6,2 m total" },
  ];
  poles.forEach((p) => {
    const top = G - p.up * U, bot = G + p.dn * U;
    s.addShape(pres.ShapeType.rect, { x: p.x - p.fw * U / 2, y: G, w: p.fw * U, h: p.dn * U + 0.05, fill: { color: "B9B4AC" }, line: { color: "9A948B", width: 0.75 } });
    s.addShape(pres.ShapeType.rect, { x: p.x - 0.035, y: top, w: 0.07, h: bot - top, fill: { color: "7D8794" }, line: { color: "5E6773", width: 0.5 } });
    label(s, p.upTxt, p.x + 0.12, top + (G - top) / 2 - 0.14, 0.6, 0.28, { size: 9.5, bold: true, color: CHAR });
    const isCH = p.name === "Tiang CH";
    label(s, p.dn.toLocaleString("id-ID") + " m", isCH ? p.x - 0.8 : p.x + 0.2, G + (bot - G) / 2 - 0.14, 0.6, 0.28, { size: 9, color: CHAR_SOFT, align: isCH ? "right" : "left" });
    label(s, p.name, isCH ? p.x + 0.25 : p.x - 0.65, G + 0.42, 1.3, 0.2, { size: 9.5, bold: true, color: CHAR, align: isCH ? "left" : "center" });
    label(s, p.sub, isCH ? p.x + 0.25 : p.x - 0.65, G + 0.62, 1.3, 0.2, { size: 8.5, color: MUTED, align: isCH ? "left" : "center" });
  });
  const gx = poles[0].x;
  s.addShape(pres.ShapeType.roundRect, { x: gx - 0.24, y: G - 0.5 * U - 0.09, w: 0.2, h: 0.18, rectRadius: 0.03, fill: { color: BLUE }, line: { color: BLUE_DK } });
  const cx = poles[1].x, ctop = G - 5.0 * U;
  s.addShape(pres.ShapeType.roundRect, { x: cx - 0.09, y: ctop - 0.16, w: 0.18, h: 0.2, rectRadius: 0.03, fill: { color: BLUE }, line: { color: BLUE_DK } });
  s.addShape(pres.ShapeType.rect, { x: cx - 0.5, y: ctop + 0.37, w: 0.45, h: 0.07, fill: { color: "2E3E66" }, line: { color: "2E3E66" }, rotate: -12 });
  // gedung + tiang atap
  const bx = M + 3.1, bw = 1.85, R = G - 2.3;
  s.addShape(pres.ShapeType.rect, { x: bx, y: R, w: bw, h: G - R, fill: { color: SURF_2 }, line: { color: LINE } });
  label(s, "Gedung", bx, R + 0.9, bw, 0.3, { size: 9, color: CHAR_SOFT, align: "center" });
  const mx = bx + 1.3, mtop = R - 2.25 * U;
  s.addShape(pres.ShapeType.rect, { x: mx - 0.2, y: R - 0.06, w: 0.4, h: 0.06, fill: { color: CHAR }, line: { color: CHAR } });
  s.addShape(pres.ShapeType.rect, { x: mx - 0.035, y: mtop, w: 0.07, h: R - 0.06 - mtop, fill: { color: "7D8794" }, line: { color: "5E6773", width: 0.5 } });
  line(s, mx, mtop - 0.32, 0, 0.32, CHAR, 2);
  label(s, "± 2–2,5 m", bx - 0.05, mtop + 0.35, 1.2, 0.28, { size: 9.5, bold: true, color: CHAR, align: "right" });
  label(s, "Tiang atap GW", bx, G + 0.42, bw, 0.2, { size: 9.5, bold: true, color: CHAR, align: "right" });
  label(s, "base plate, tanpa cor", bx, G + 0.62, bw, 0.2, { size: 8.5, color: MUTED, align: "right" });
  const x0 = M + 5.45, w0 = W - M - x0;
  const c3 = (w0 - 1.55) / 3;
  table(s, [
    ["", "Tiang GLD", "Tiang CH", "Tiang Gateway (atap)"],
    ["Panjang batang", "1,6 m", "4,0–6,2 m", "± 2,5–3 m"],
    ["Tinggi", "1,0 m di atas tanah", "3–5 m di atas tanah", "± 2–2,5 m di atas atap"],
    ["Tertanam / dudukan", "0,6 m", "1,0–1,2 m", "Base plate dibaut ke struktur / ballast"],
    ["Pondasi", "Cor 40×40×60 cm", "Cor 50×50×100–120 cm", "Tanpa cor; ikuti struktur atap"],
    ["Ujung atas", "Pipe cap", "Dudukan CH & panel surya", "Pipe cap + klem Gateway"],
    ["Yang dipasang", "Pelat U-bolt + GLD", "Bracket 1 panel surya + CH (LGU)", "Gateway + antena omni 8 dBi (LGU)"],
  ], { x: x0, y: 1.6, w: w0, colW: [1.55, c3, c3, c3], size: 10, boldFirst: true, rowH: 0.44 });
  bullets(s, x0, 5.05, w0, 1.7, [
    "Material: baja karbon galvanis celup panas (mis. ASTM A53 / API 5L Gr.B); tiang GLD wajib OD 60,3 mm.",
    "Beton fc' ≥ 20 MPa; angkur silang (2 × besi Ø12 mm) di ujung bawah; tegak ≤ 1°.",
    "Tiang CH tinggi / angin kencang: guy wire 3 arah. Tiang atap tidak menembus lapisan kedap air tanpa persetujuan sipil RU.",
    "Semua tiang di-bonding ke grounding RU dan diberi label nomor titik sesuai dashboard.",
  ], 10.5);
  footnote(s, SRC_SPEK, 6.9);
  s.addNotes("Diagram tidak berskala presisi. Bila RU VI punya standar tiang/pondasi sendiri, standar RU yang dipakai; syarat mutlak hanya OD pipa 60,3 mm untuk tiang GLD karena U-bolt.");
})();

(function lampB() {
  const s = slideLight();
  lampHead(s, "B", "Tinggi sensor GLD menurut jenis gas");
  table(s, [
    ["Jenis gas", "Sifat", "Tinggi sensor ideal"],
    ["LPG (propana/butana), CO₂", "Jauh lebih berat dari udara, mengendap", "0,3–0,5 m dari tanah"],
    ["H₂S", "Sedikit lebih berat, toksik", "0,3–0,6 m (deteksi bocor); 1,2–1,8 m (zona napas)"],
    ["CO", "Hampir sama dengan udara", "Zona napas 1,5–1,8 m"],
    ["Metana", "Lebih ringan, naik", "± 0,5–1 m di atas sumber bocor"],
    ["H₂", "Sangat ringan, naik cepat", "Di atas sumber bocor / titik gas terperangkap"],
  ], { x: M, y: 1.6, w: 7.6, colW: [2.1, 2.6, 2.9], size: 11.5, boldFirst: true, rowH: 0.62 });
  card(s, 8.5, 1.6, W - M - 8.5, 4.6, SURF);
  bullets(s, 8.75, 1.8, W - M - 9.0, 4.3, [
    "Satu GLD membaca beberapa gas sekaligus, jadi tinggi pasang selalu kompromi — ditentukan dari gas prioritas & letak sumber bocor (flange/valve).",
    "Jangan di bawah ± 0,3 m: mesh sensor bisa terkena cipratan air, lumpur, dan genangan.",
    "RU IV memakai ± 1,5 m sesuai evaluasi HSSE.",
    "Tinggi final per titik disepakati bersama HSE RU saat penentuan titik.",
  ], 12);
  footnote(s, "Acuan tinggi: praktik umum industri (IEC 60079-29-2, ISA RP12.13 Part II). " + SRC_SPEK);
  s.addNotes("Tanyakan gas prioritas RU VI di area kandidat — ini menentukan tinggi pasang GLD.");
})();

// ---------------------------------------------------------------- E · terminasi di unit GLD
(function lampE() {
  const s = slideLight();
  lampHead(s, "C", "Terminasi kabel di unit GLD");
  const iw = 7.2, ih = iw * 1209 / 2008;
  card(s, M, 1.55, iw + 0.2, ih + 0.2, WHITE);
  s.addImage({ path: ASSET("measured_sketches/MS-06_terminal_wiring.png"), x: M + 0.1, y: 1.65, w: iw, h: ih });
  label(s, "Blok terminal di papan cover GLD V2 (sketsa, tidak berskala). Pada konfigurasi 24 VDC, terminal BAT tidak dipakai.", M, 1.8 + ih, iw + 0.2, 0.45, { size: 9.5, color: MUTED, valign: "top" });
  const x0 = M + iw + 0.45, w0 = W - M - x0;
  table(s, [
    ["Item", "Ketentuan"],
    ["Konduktor", "2 inti tembaga, label L+ / L− (24 VDC)"],
    ["Jenis kabel", "Kabel daya/instrumen luar ruang berarmor (mis. SWA), tahan UV & minyak; rute mengikuti standar RU"],
    ["Masuk unit", "Cable gland M20 × 1,5; diameter kabel harus masuk rentang klem; kabel armor perlu gland tipe armored"],
    ["Ujung kabel", "Ferrule/skun; terminasi ke 24V+ / 24V− dikerjakan teknisi LGU"],
    ["Grounding", "Sekrup PE eksternal di samping cable gland, ke grounding RU"],
    ["RS-485 (opsional)", "Terminal A/B untuk Modbus RTU read-only bila RU ingin membaca status GLD"],
  ], { x: x0, y: 1.6, w: w0, colW: [1.35, w0 - 1.35], size: 10.5, boldFirst: true, rowH: 0.62 });
  card(s, M, 6.15, 12.1, 0.55, OK_BG);
  s.addText("Penarikan kabel & PSU oleh pelaksana RU; terminasi akhir, energize, dan commissioning oleh LGU.", {
    x: M + 0.25, y: 6.15, w: 11.6, h: 0.55, isTextBox: true, margin: 0, fontFace: FONT, fontSize: 12, bold: true, color: OK, valign: "middle",
  });
  footnote(s, SRC_SPEK, 6.85);
  s.addNotes("Gland M20 x 1,5 bawaan unit; bila RU VI memakai kabel armor, gland harus tipe armored dan diameter kabel dicocokkan sebelum pembelian kabel.");
})();

// ---------------------------------------------------------------- F · antena GW & jaringan
(function lampF() {
  const s = slideLight();
  lampHead(s, "D", "Gateway di atap & jaringan lokal");
  table(s, [
    ["Item", "Ketentuan"],
    ["Antena", "Omni 8 dBi, 920–923 MHz (dari LGU); pada tiang di atap, puncak ± 2–2,5 m di atas atap & lebih tinggi dari antena CH"],
    ["Unit Gateway", "Dipasang di tiang atap bersama antena (tidak terpisah), enclosure tahan cuaca; tanpa koaksial panjang"],
    ["Daya", "Kabel daya dari stop kontak UPS di ruangan bawah ke tiang; kabel luar tahan UV, diklem ke tiang"],
    ["Masuk gedung", "Sleeve dinding/atap disegel + drip loop"],
    ["Proteksi petir", "Tiang di dalam zona lindung penangkal petir gedung; tiang & unit di-bonding ke grounding"],
    ["GW → router", "Wi-Fi 2,4 GHz dari atap ke router di ruangan tepat di bawahnya, WPA2, SSID khusus GLD"],
    ["Router → PC", "Cat6 ≤ 90 m per segmen; IP tetap untuk PC server (MQTT broker)"],
    ["PC → intranet", "LAN kedua, hanya akses dashboard/API; tanpa internet, router tanpa WAN/SIM"],
  ], { x: M, y: 1.6, w: 7.6, colW: [1.6, 6.0], size: 10.5, boldFirst: true, rowH: 0.5 });
  cardTitle(s, 8.55, 1.6, 4.2, "Kenapa Gateway menyatu dengan antena");
  bullets(s, 8.55, 2.0, 4.17, 2.0, [
    "Tanpa kabel koaksial antena → tidak ada redaman kabel & arrester koaksial",
    "Yang ditarik ke atap hanya kabel daya",
    "Pemasangan lebih sederhana: satu tiang, satu titik",
  ], 11);
  card(s, 8.55, 4.2, 4.17, 1.95, WARN_BG);
  s.addText("Yang perlu dicek saat survey: kuat sinyal Wi-Fi dari Gateway di atap ke router (plat atap beton meredam). Bila lemah, router dipindah ke ruangan lebih dekat atap atau ditambah access point outdoor.", {
    x: 8.75, y: 4.2, w: 3.8, h: 1.95, isTextBox: true, margin: 0, fontFace: FONT, fontSize: 11, bold: true, color: WARN, valign: "middle",
  });
  footnote(s, SRC_SPEK);
  s.addNotes("Jumlah Gateway RU VI ditetapkan dari LoRa mapping; lokasi tiang Gateway di atap dan ruang router di bawahnya dipilih saat survey. Bila kedua Gateway berjauhan, kebutuhan router/PC server dibahas ulang.");
})();

// ---------------------------------------------------------------- H · BoQ RU VI
(function lampH() {
  const s = slideLight();
  lampHead(s, "E", "Perkiraan BoQ RU VI — CH & GW per LoRa mapping");
  table(s, [
    ["No", "Item", "Spesifikasi", "Qty (perkiraan)", "Penyedia"],
    ["1", "Pipa tiang GLD", "Galvanis 2\" Sch40, 1,6 m per titik", "4 (± 2 batang 6 m)", "RU VI"],
    ["2", "Pipa tiang CH", "Galvanis 2\" Sch40 (atau 3\"/2\"), 3–5 m di atas tanah", "1 per CH (min. 2)", "RU VI"],
    ["3", "Tiang antena GW di atap", "Galvanis 2\", ± 2,5–3 m + base plate / ballast", "1 per GW (min. 2)", "RU VI"],
    ["4", "Pipe cap 2\"", "Ujung atas tiang GLD & tiang atap GW", "4 + 1 per GW", "RU VI"],
    ["5", "Beton cor", "fc' ≥ 20 MPa; per titik: GLD 0,10 · CH 0,25–0,30 m³", "± 1,0 m³ (4 GLD + 2 CH)", "RU VI"],
    ["6", "U-bolt + mur/ring", "GLD: 2\" M10; CH: sesuai OD tiang", "8 (GLD) + per CH", "RU VI"],
    ["7", "Pelat mounting 250 × 250 mm", "Sesuai gambar LGU", "4", "RU VI"],
    ["8", "PSU 24 VDC + box/MCB", "Opsi A: 4 × (≥ 1 A) · Opsi B: 1 × (≥ 6 A)", "4 atau 1 set", "RU VI"],
    ["9", "Kabel daya 2 inti berarmor", "Ukuran & panjang per slide catu daya GLD", "Σ setelah survey", "RU VI"],
    ["10", "Kabel daya Gateway (UPS → tiang atap)", "Lampiran D; panjang setelah survey", "1 jalur per GW", "RU VI"],
    ["11", "Grounding & label titik", "Standar RU VI; tiang atap ke penangkal petir gedung", "1 per tiang", "RU VI"],
    ["12", "PC server + UPS ≥ 1 kVA, Cat6, stop kontak", "Slide server & UPS", "1 set + 2 jalur Cat6", "RU VI"],
    ["13", "GLD, CH, Gateway (menyatu dengan antena), panel surya & bracket CH, router", "Perangkat sistem", "4 GLD; CH & GW per LoRa mapping", "LGU"],
  ], { x: M, y: 1.55, w: 12.1, colW: [0.5, 3.2, 4.6, 2.3, 1.5], size: 10.5, rowH: 0.34 });
  footnote(s, "Jumlah CH & Gateway ditetapkan dari LoRa mapping saat site survey (rencana awal 2 CH, 2 GW, bisa bertambah); item yang mengikutinya dihitung per unit. Panjang kabel dan kebutuhan router/PC ditetapkan setelah survey. " + SRC_SPEK, 6.7);
  s.addNotes("BoQ ini mengikuti pola BoQ RU IV untuk 4 GLD; item CH dan Gateway ditulis per unit karena jumlahnya baru pasti setelah LoRa mapping. Sampaikan bahwa angka final keluar setelah survey; RU VI bisa mulai memperkirakan anggaran dari tabel ini.");
})();

pres.writeFile({ fileName: OUT }).then(() => console.log("written", OUT));
