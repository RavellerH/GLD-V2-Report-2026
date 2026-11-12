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
  footnote(s, "Lampiran A–H: detail teknis instalasi — pelat & U-bolt, tiang & pondasi, tinggi sensor, catu daya & kabel, terminasi, antena & jaringan, contoh penempatan, perkiraan BoQ.", 6.8);
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
  heading(s, "5 · Rencana", "Persiapan site survey awal");
  const cols = [
    ["Yang diperiksa tim LGU", BLUE, SURF, [
      "Kandidat titik GLD: sumber bocor (flange/valve), arah angin, tinggi pasang",
      "Klasifikasi area tiap titik (HAC)",
      "LoRa mapping: uji jangkauan (RSSI/SNR) titik GLD → CH → mast Gateway, untuk menetapkan jumlah & posisi CH/GW",
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
    "Jumlah unit final: 4 GLD; CH & GW setelah LoRa mapping",
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

// ================================================================ LAMPIRAN · detail teknis instalasi
const SRC_SPEK = "Sumber: Spesifikasi Material & Kebutuhan Instalasi GLD rev 1.5 (disusun untuk RU IV Cilacap) — angka USULAN dapat disesuaikan dengan standar RU VI.";
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
    ["A", "Pelat mounting & U-bolt GLD"], ["B", "Tiang & pondasi (GLD, CH, mast Gateway)"],
    ["C", "Tinggi sensor per jenis gas & mounting CH"], ["D", "Catu daya & kabel 24 VDC"],
    ["E", "Terminasi kabel di unit GLD"], ["F", "Antena Gateway & jaringan lokal"],
    ["G", "Contoh penempatan titik (RU IV, area SRU)"], ["H", "Perkiraan daftar material (BoQ) RU VI"],
  ];
  items.forEach((it, i) => {
    const col = i % 2, row = Math.floor(i / 2);
    const x = M + col * 6.15, y = 3.2 + row * 0.82;
    badge(s, x, y, it[0], 0.46, BLUE);
    s.addText(it[1], { x: x + 0.62, y: y - 0.04, w: 5.3, h: 0.54, isTextBox: true, margin: 0, fontFace: FONT, fontSize: 15, bold: true, color: WHITE, valign: "middle" });
  });
  s.addNotes("Lampiran ini tidak dipresentasikan satu per satu; dibuka saat diskusi teknis bila RU VI menanyakan detail bracket, tiang, kabel, atau jaringan.");
})();

// ---------------------------------------------------------------- A · pelat & U-bolt
(function lampA() {
  const s = slideLight();
  lampHead(s, "A", "Pelat mounting & U-bolt GLD");
  const ih = 5.05, iw = ih * 740 / 1372;
  card(s, M, 1.55, iw + 0.3, ih + 0.3, WHITE);
  s.addImage({ path: ASSET("balongan_13nov/pelat_ubolt_dimensi.png"), x: M + 0.15, y: 1.7, w: iw, h: ih });
  label(s, "Gambar kerja pelat 250 × 250 mm & posisi U-bolt (mm). Sumber: gambar CAD LGU 31/08/2026.", M, 6.95, iw + 0.3, 0.4, { size: 9.5, color: MUTED, valign: "top" });
  const x0 = M + iw + 0.6, w0 = W - M - x0;
  table(s, [
    ["Item", "Spesifikasi", "Per titik"],
    ["Pelat mounting", "Pelat baja 250 × 250 mm, dibuat pelaksana RU sesuai gambar LGU", "1"],
    ["U-bolt", "2\"/DN50 untuk pipa OD 60,3 mm; ulir M10; lebar dalam 62–65 mm; tinggi dalam 95–100 mm; panjang ulir 40 mm", "2"],
    ["Mur & ring", "M10: mur + ring datar + ring per; anti-karat (disarankan SS316 di dekat laut)", "4 set"],
    ["Spacer", "45–60 mm bila pelat lebih tebal", "sesuai kebutuhan"],
    ["Kabel ties", "Tahan UV, stainless atau nylon UV", "± 10"],
    ["Larangan", "Tanpa PVC pada housing/bracket; tanpa bor/las pada struktur existing kilang", "—"],
  ], { x: x0, y: 1.6, w: w0, colW: [1.6, w0 - 2.85, 1.25], size: 11, boldFirst: true, rowH: 0.48 });
  card(s, x0, 5.45, w0, 1.15, WARN_BG);
  s.addText("Perlu dicek sebelum fabrikasi: desain pelat saat ini paling sesuai untuk pipa horizontal (handrail). Bila GLD dipasang di tiang baru yang berdiri vertikal, orientasi pelat dicek bersama tim desain LGU & pelaksana RU sebelum pelat dibuat.", {
    x: x0 + 0.2, y: 5.45, w: w0 - 0.4, h: 1.15, isTextBox: true, margin: 0, fontFace: FONT, fontSize: 11.5, bold: true, color: WARN, valign: "middle",
  });
  s.addNotes("U-bolt dirancang khusus untuk pipa OD 60,3 mm (2 inci). Pipa ukuran lain tidak bisa dipakai tanpa mengganti U-bolt. Pelat dibuat oleh pelaksana RU berdasarkan gambar ini.");
})();

// ---------------------------------------------------------------- B · tiang & pondasi
(function lampB() {
  const s = slideLight();
  lampHead(s, "B", "Tiang & pondasi — pipa galvanis 2\" Sch40, ditanam & dicor");
  // diagram
  const G = 5.15, U = 0.55; // garis tanah, inci per meter
  card(s, M, 1.55, 5.2, 5.2, WHITE);
  s.addShape(pres.ShapeType.rect, { x: M + 0.15, y: G, w: 4.9, h: 1.45, fill: { color: "EFE9E1" }, line: { color: "EFE9E1" } });
  line(s, M + 0.15, G, 4.9, 0, "8A7F72", 1.5);
  const poles = [
    { x: M + 0.95, up: 1.0, dn: 0.6, fw: 0.40, name: "Tiang GLD", sub: "1,6 m total" },
    { x: M + 2.55, up: 3.0, dn: 1.0, fw: 0.50, name: "Tiang CH", sub: "4,0 m total" },
    { x: M + 4.1, up: 4.8, dn: 1.2, fw: 0.50, name: "Mast antena GW", sub: "6,0 m total" },
  ];
  poles.forEach((p) => {
    const top = G - p.up * U, bot = G + p.dn * U;
    s.addShape(pres.ShapeType.rect, { x: p.x - p.fw * U / 2, y: G, w: p.fw * U, h: p.dn * U + 0.05, fill: { color: "B9B4AC" }, line: { color: "9A948B", width: 0.75 } });
    s.addShape(pres.ShapeType.rect, { x: p.x - 0.035, y: top, w: 0.07, h: bot - top, fill: { color: "7D8794" }, line: { color: "5E6773", width: 0.5 } });
    const isMast = p.name.startsWith("Mast");
    label(s, p.up.toLocaleString("id-ID") + " m", isMast ? p.x - 0.72 : p.x + 0.12, top + (G - top) / 2 - 0.14, 0.6, 0.28, { size: 9.5, bold: true, color: CHAR, align: isMast ? "right" : "left" });
    label(s, p.dn.toLocaleString("id-ID") + " m", p.x + 0.2, G + (bot - G) / 2 - 0.14, 0.6, 0.28, { size: 9, color: CHAR_SOFT });
    label(s, p.name, p.x - 0.75, 6.3, 1.5, 0.22, { size: 10, bold: true, color: CHAR, align: "center" });
    label(s, p.sub, p.x - 0.75, 6.5, 1.5, 0.2, { size: 9, color: MUTED, align: "center" });
  });
  // GLD unit (titik tengah sensor ± 0,5 m)
  const gx = poles[0].x;
  s.addShape(pres.ShapeType.roundRect, { x: gx - 0.24, y: G - 0.5 * U - 0.09, w: 0.2, h: 0.18, rectRadius: 0.03, fill: { color: BLUE }, line: { color: BLUE_DK } });
  label(s, "GLD ± 0,5 m", gx - 0.95, G - 0.5 * U - 0.13, 0.7, 0.26, { size: 8.5, color: BLUE, bold: true, align: "right" });
  // CH: unit + 2 panel surya
  const cx = poles[1].x, ctop = G - 3.0 * U;
  s.addShape(pres.ShapeType.rect, { x: cx - 0.45, y: ctop + 0.35, w: 0.38, h: 0.07, fill: { color: "2E3E66" }, line: { color: "2E3E66" }, rotate: -20 });
  s.addShape(pres.ShapeType.rect, { x: cx + 0.07, y: ctop + 0.35, w: 0.38, h: 0.07, fill: { color: "2E3E66" }, line: { color: "2E3E66" }, rotate: 20 });
  s.addShape(pres.ShapeType.roundRect, { x: cx - 0.09, y: ctop - 0.16, w: 0.18, h: 0.2, rectRadius: 0.03, fill: { color: BLUE }, line: { color: BLUE_DK } });
  line(s, cx, ctop - 0.42, 0, 0.26, CHAR, 1.5);
  // mast GW: antena + koaksial ke gedung
  const mx = poles[2].x, mtop = G - 4.8 * U;
  line(s, mx, mtop - 0.35, 0, 0.35, CHAR, 2);
  s.addShape(pres.ShapeType.rect, { x: M + 4.5, y: G - 1.3, w: 0.55, h: 1.3, fill: { color: SURF_2 }, line: { color: LINE } });
  label(s, "Ruang\nGateway", M + 4.5, G - 1.0, 0.55, 0.5, { size: 8, color: CHAR_SOFT, align: "center" });
  line(s, mx + 0.04, G - 0.4, 0.36, 0, WARN, 1.5, "dash");
  label(s, "koaksial\n≤ 15 m", M + 4.3, G - 1.85, 0.95, 0.45, { size: 8, color: WARN, align: "center" });
  // tabel
  const x0 = M + 5.45, w0 = W - M - x0;
  table(s, [
    ["", "Tiang GLD", "Tiang CH", "Mast antena GW"],
    ["Panjang batang", "1,6 m", "4,0 m", "6,0 m"],
    ["Di atas tanah", "1,0 m", "3,0 m", "± 4,8 m"],
    ["Tertanam", "0,6 m", "1,0 m", "1,2 m"],
    ["Pondasi cor", "40×40×60 cm", "50×50×100 cm", "50×50×120 cm"],
    ["Ujung atas", "Pipe cap", "Dudukan CH/antena", "Pipe cap + klem antena"],
    ["Yang dipasang", "Pelat U-bolt + GLD", "Bracket 2 panel surya + CH (dari LGU)", "Antena omni 8 dBi (dari LGU)"],
  ], { x: x0, y: 1.6, w: w0, colW: [1.55, (w0 - 1.55) / 3, (w0 - 1.55) / 3, (w0 - 1.55) / 3], size: 10.5, boldFirst: true, rowH: 0.44 });
  bullets(s, x0, 4.95, w0, 1.8, [
    "Material: baja karbon galvanis celup panas (mis. ASTM A53 / API 5L Gr.B), OD 60,3 mm, tebal 3,91 mm.",
    "Beton fc' ≥ 20 MPa; ujung bawah diberi angkur silang (2 × besi Ø12 mm) agar tiang tidak berputar; tegak ≤ 1°.",
    "Semua tiang di-bonding ke grounding RU dan diberi label nomor titik sesuai dashboard.",
    "Mast > 5 m atau angin kencang: tambah guy wire 3 arah atau klem ke dinding gedung.",
  ], 11);
  footnote(s, SRC_SPEK);
  s.addNotes("Diagram tidak berskala presisi. Bila RU VI punya standar tiang/pondasi sendiri, standar RU yang dipakai; syarat mutlak hanya OD pipa 60,3 mm untuk tiang GLD karena U-bolt.");
})();

// ---------------------------------------------------------------- C · tinggi sensor & mounting CH
(function lampC() {
  const s = slideLight();
  lampHead(s, "C", "Tinggi sensor menurut jenis gas & mounting Cluster Head");
  table(s, [
    ["Jenis gas", "Sifat", "Tinggi sensor ideal"],
    ["LPG (propana/butana), CO₂", "Jauh lebih berat dari udara, mengendap", "0,3–0,5 m dari tanah"],
    ["H₂S", "Sedikit lebih berat, toksik", "0,3–0,6 m (deteksi bocor); 1,2–1,8 m (zona napas)"],
    ["CO", "Hampir sama dengan udara", "Zona napas 1,5–1,8 m"],
    ["Metana", "Lebih ringan, naik", "± 0,5–1 m di atas sumber bocor"],
    ["H₂", "Sangat ringan, naik cepat", "Di atas sumber bocor / titik gas terperangkap"],
  ], { x: M, y: 1.6, w: 7.0, colW: [1.9, 2.4, 2.7], size: 11, boldFirst: true, rowH: 0.5 });
  card(s, M, 4.85, 7.0, 1.75, SURF);
  bullets(s, M + 0.25, 5.0, 6.55, 1.55, [
    "Satu GLD membaca beberapa gas sekaligus, jadi tinggi pasang selalu kompromi — ditentukan dari gas prioritas & letak sumber bocor (flange/valve).",
    "Jangan di bawah ± 0,3 m: mesh sensor bisa terkena cipratan air, lumpur, dan genangan.",
    "Tinggi final per titik disepakati bersama HSE RU saat penentuan titik.",
  ], 11.5);
  const pw = 2.35, ph = pw * 1600 / 1200;
  s.addImage({ path: ASSET("ch_mount_photos/ch_bracket_solar_detail.jpg"), x: 7.95, y: 1.6, w: pw, h: ph });
  s.addImage({ path: ASSET("ch_mount_photos/ch_mast_antena_lapangan.jpg"), x: 7.95 + pw + 0.1, y: 1.6, w: pw, h: ph });
  label(s, "Bracket 2 panel surya diklem ke tiang 2\" tanpa las/bor (kiri); unit CH & antena di ujung atas tiang (kanan). Foto uji LGU & ITB — di site, tiang ditanam & dicor.", 7.95, 1.7 + ph, 2 * pw + 0.1, 0.65, { size: 9.5, color: MUTED, valign: "top" });
  footnote(s, "Acuan tinggi: praktik umum industri (IEC 60079-29-2, ISA RP12.13 Part II). " + SRC_SPEK);
  s.addNotes("Tanyakan gas prioritas RU VI di area kandidat — ini menentukan tinggi tiang GLD. Cluster Head tidak memerlukan kabel daya; tinggi final CH ditentukan tim RF LGU saat survey (line of sight).");
})();

// ---------------------------------------------------------------- D · catu daya & kabel
(function lampD() {
  const s = slideLight();
  lampHead(s, "D", "Catu daya & kabel 24 VDC — hanya GLD yang perlu kabel daya");
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

// ---------------------------------------------------------------- E · terminasi di unit GLD
(function lampE() {
  const s = slideLight();
  lampHead(s, "E", "Terminasi kabel di unit GLD");
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
  lampHead(s, "F", "Antena Gateway & jaringan lokal");
  table(s, [
    ["Item", "Ketentuan"],
    ["Antena", "Omni 8 dBi, 920–923 MHz (dari LGU); puncak ≥ 2 m di atas atap terdekat & lebih tinggi dari antena CH"],
    ["Kabel antena", "Koaksial 50 Ω LMR-400 atau setara, tahan UV, target ≤ 15 m (rute × 1,10 + 1 m)"],
    ["Konektor", "Tipe N di sisi antena & penangkal petir; adaptor ke konektor Gateway disiapkan LGU"],
    ["Penangkal petir", "Coaxial arrester 50 Ω 900 MHz (gas discharge), di titik kabel masuk gedung, di-grounding"],
    ["Masuk gedung", "Sleeve dinding disegel + drip loop; sambungan luar dibalut self-amalgamating tape"],
    ["GW → router", "Wi-Fi 2,4 GHz, satu ruangan (± 1–5 m), WPA2, SSID khusus GLD"],
    ["Router → PC", "Cat6 ≤ 90 m per segmen; IP tetap untuk PC server (MQTT broker)"],
    ["PC → intranet", "LAN kedua, hanya akses dashboard/API; tanpa internet, router tanpa WAN/SIM"],
  ], { x: M, y: 1.6, w: 7.6, colW: [1.6, 6.0], size: 10.5, boldFirst: true, rowH: 0.5 });
  cardTitle(s, 8.55, 1.6, 4.2, "Redaman koaksial pada 921 MHz");
  table(s, [
    ["Panjang", "LMR-240", "LMR-400", "LMR-600"],
    ["5 m", "1,2 dB", "0,6 dB", "0,4 dB"],
    ["10 m", "2,5 dB", "1,3 dB", "0,8 dB"],
    ["15 m", "3,7 dB", "1,9 dB", "1,2 dB"],
    ["25 m", "6,2 dB", "3,2 dB", "2,1 dB"],
  ], { x: 8.55, y: 2.0, w: 4.17, colW: [1.05, 1.04, 1.04, 1.04], size: 10.5, boldFirst: true, rowH: 0.4 });
  card(s, 8.55, 4.2, 4.17, 1.95, WARN_BG);
  s.addText("Setiap 3 dB redaman memangkas setengah daya sinyal dari dan ke seluruh CH. Rute > 20 m: pakai LMR-600 atau pindahkan Gateway ke ruangan yang lebih dekat dengan mast. Hindari RG-58 (± 0,5 dB/m).", {
    x: 8.75, y: 4.2, w: 3.8, h: 1.95, isTextBox: true, margin: 0, fontFace: FONT, fontSize: 11, bold: true, color: WARN, valign: "middle",
  });
  footnote(s, "Nilai redaman: katalog umum, belum termasuk ± 0,5 dB rugi konektor. " + SRC_SPEK);
  s.addNotes("RU VI direncanakan 2 Gateway; lokasi kedua ruang Gateway dan mast antena dipilih saat survey. Bila kedua Gateway berjauhan, kebutuhan router/PC server dibahas ulang.");
})();

// ---------------------------------------------------------------- G · contoh penempatan RU IV
(function lampG() {
  const s = slideLight();
  lampHead(s, "G", "Contoh penempatan titik — RU IV Cilacap, area SRU");
  const ih = 4.75, iw = ih * 1440 / 803;
  s.addImage({ path: ASSET("ppn_design/layout_titik.jpg"), x: M, y: 1.6, w: iw, h: ih });
  label(s, "Gambar kerja kandidat titik saat persiapan RU IV (citra satelit + foto lokasi).", M, 1.65 + ih, iw, 0.3, { size: 9.5, color: MUTED, valign: "top" });
  const x0 = M + iw + 0.3, w0 = W - M - x0;
  const legend = [
    ["GLD", "Titik deteksi, dekat sumber bocor; kabel 24 VDC dari junction box (JB)", "E8A317"],
    ["JB", "Junction box / sumber 24 VDC terdekat untuk GLD", "E8A317"],
    ["CH", "Di tepi area, tiang tinggi, tanpa kabel daya", BLUE],
    ["GW", "Di dalam gedung; antena di mast luar", BLUE],
  ];
  legend.forEach((l, i) => {
    const y = 1.65 + i * 1.0;
    chip(s, x0, y, l[0], WHITE, l[2] === BLUE ? BLUE : CHAR_SOFT, 0.75);
    label(s, l[1], x0 + 0.9, y - 0.08, w0 - 0.9, 0.85, { size: 10.5, valign: "top" });
  });
  card(s, x0, 5.7, w0, 0.9, PERTAMINA_BG);
  s.addText("Lingkup MoC RU IV: 4 GLD + 5 CH + JB-01 + 1 GW + PC server. Titik GLD di area terklasifikasi menunggu sertifikat Ex.", {
    x: x0 + 0.15, y: 5.7, w: w0 - 0.3, h: 0.9, isTextBox: true, margin: 0, fontFace: FONT, fontSize: 10, bold: true, color: PERTAMINA, valign: "middle",
  });
  s.addNotes("Contoh ini menunjukkan pola yang sama yang diharapkan di Balongan: GLD dekat sumber bocor dengan kabel ke JB, CH di tepi area, Gateway di gedung. Layout RU VI dibuat setelah survey.");
})();

// ---------------------------------------------------------------- H · BoQ RU VI
(function lampH() {
  const s = slideLight();
  lampHead(s, "H", "Perkiraan BoQ RU VI — CH & GW per LoRa mapping");
  table(s, [
    ["No", "Item", "Spesifikasi", "Qty (perkiraan)", "Penyedia"],
    ["1", "Pipa tiang GLD", "Galvanis 2\" Sch40, 1,6 m per titik", "4 (± 2 batang 6 m)", "RU VI"],
    ["2", "Pipa tiang CH", "Galvanis 2\" Sch40, 4,0 m", "1 per CH (min. 2)", "RU VI"],
    ["3", "Pipa mast antena GW", "Galvanis 2\" Sch40, 6,0 m (+ guy wire bila perlu)", "1 per GW (min. 2)", "RU VI"],
    ["4", "Pipe cap 2\"", "Ujung atas tiang GLD & mast GW", "4 + 1 per GW", "RU VI"],
    ["5", "Beton cor", "fc' ≥ 20 MPa; per titik: GLD 0,10 · CH 0,25 · GW 0,30 m³", "± 1,8 m³ (untuk 2 CH + 2 GW)", "RU VI"],
    ["6", "U-bolt 2\" M10 + mur/ring", "Lampiran A", "8 U-bolt, 16 set mur", "RU VI"],
    ["7", "Pelat mounting 250 × 250 mm", "Sesuai gambar LGU", "4", "RU VI"],
    ["8", "PSU 24 VDC + box/MCB", "Opsi A: 4 × (≥ 1 A) · Opsi B: 1 × (≥ 6 A)", "4 atau 1 set", "RU VI"],
    ["9", "Kabel daya 2 inti berarmor", "Ukuran & panjang per Lampiran D", "Σ setelah survey", "RU VI"],
    ["10", "Koaksial LMR-400 + konektor N + arrester", "Lampiran F", "1 jalur per GW", "RU VI"],
    ["11", "Grounding & label titik", "Standar RU VI", "1 per tiang/mast", "RU VI"],
    ["12", "PC server + UPS, Cat6, stop kontak", "Slide kebutuhan server & jaringan", "1 set + 2 jalur Cat6", "RU VI"],
    ["13", "GLD, CH, Gateway + antena, panel surya & bracket CH, router", "Perangkat sistem", "4 GLD; CH & GW per LoRa mapping", "LGU"],
  ], { x: M, y: 1.55, w: 12.1, colW: [0.5, 3.2, 4.6, 2.3, 1.5], size: 10.5, rowH: 0.34 });
  footnote(s, "Jumlah CH & Gateway ditetapkan dari LoRa mapping saat site survey (rencana awal 2 CH, 2 GW, bisa bertambah); item yang mengikutinya dihitung per unit. Panjang kabel dan kebutuhan router/PC ditetapkan setelah survey. " + SRC_SPEK, 6.7);
  s.addNotes("BoQ ini mengikuti pola BoQ RU IV untuk 4 GLD; item CH dan Gateway ditulis per unit karena jumlahnya baru pasti setelah LoRa mapping. Sampaikan bahwa angka final keluar setelah survey; RU VI bisa mulai memperkirakan anggaran dari tabel ini.");
})();

pres.writeFile({ fileName: OUT }).then(() => console.log("written", OUT));
