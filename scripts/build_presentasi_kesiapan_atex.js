/**
 * Generator deck presentasi internal: Kesiapan Sertifikasi ATEX/IECEx GLD V2.
 *
 * Output : Deliverables/Presentasi_Internal_Kesiapan_Sertifikasi_ATEX_Sep2026.pptx
 * Palet  : biru #2B5FCB + charcoal #262321 (aturan kerja repo).
 * Jalankan: NODE_PATH=<lokasi node_modules pptxgenjs> node scripts/build_presentasi_kesiapan_atex.js
 */

const path = require("path");
const PptxGenJS = require("pptxgenjs");

const OUT = path.resolve(__dirname, "..", "Deliverables",
  "Presentasi_Internal_Kesiapan_Sertifikasi_ATEX_Sep2026.pptx");

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
const WARN = "B4520F";   // belum / blocker
const WARN_BG = "FBEEE4";
const OK = "1F7A43";     // sudah ada
const OK_BG = "E6F2EB";
const HOLD = "7A6A18";   // sebagian
const HOLD_BG = "F6F1DC";

const FONT = "Calibri";
const SERIF = "Cambria";

const W = 13.333, H = 7.5;
const M = 0.62;            // margin kiri/kanan

const pres = new PptxGenJS();
pres.layout = "LAYOUT_WIDE";
pres.author = "LAPI Ganesha Utama";
pres.company = "PT LAPI Ganesha Utama";
pres.title = "Kesiapan Sertifikasi ATEX/IECEx — GLD V2";

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

/** Judul halaman + kicker kecil di atasnya. */
function heading(s, kicker, title, opts = {}) {
  const y = opts.y === undefined ? 0.46 : opts.y;
  s.addText(kicker.toUpperCase(), {
    x: M, y: y, w: 9.0, h: 0.26, isTextBox: true, margin: 0,
    fontFace: FONT, fontSize: 11, bold: true, charSpacing: 1.6, color: BLUE,
  });
  s.addText(title, {
    x: M, y: y + 0.28, w: opts.w || 11.9, h: opts.h || 0.66, isTextBox: true, margin: 0,
    fontFace: SERIF, fontSize: opts.size || 31, bold: true, color: CHAR, valign: "top",
  });
}

/** Catatan kaki di bawah slide. */
function footnote(s, text, y) {
  s.addText(text, {
    x: M, y: y === undefined ? 6.82 : y, w: W - 2 * M, h: 0.34, isTextBox: true, margin: 0,
    fontFace: FONT, fontSize: 10, italic: true, color: MUTED, valign: "top",
  });
}

/** Kartu latar lembut. */
function card(s, x, y, w, h, fill) {
  s.addShape(pres.ShapeType.roundRect, {
    x, y, w, h, rectRadius: 0.07,
    fill: { color: fill || SURF }, line: { color: LINE, width: 0.75 }, shadow: shadow(),
  });
}

/** Chip status kecil. */
function chip(s, x, y, label, fg, bg, w) {
  const width = w || 1.25;
  s.addShape(pres.ShapeType.roundRect, {
    x, y, w: width, h: 0.27, rectRadius: 0.13,
    fill: { color: bg }, line: { color: bg },
  });
  s.addText(label, {
    x, y, w: width, h: 0.27, isTextBox: true, margin: 0,
    fontFace: FONT, fontSize: 9.5, bold: true, color: fg, align: "center", valign: "middle",
  });
}

/** Badge angka bulat (motif deck). */
function badge(s, x, y, n, d) {
  const dia = d || 0.44;
  s.addShape(pres.ShapeType.ellipse, {
    x, y, w: dia, h: dia, fill: { color: BLUE }, line: { color: BLUE },
  });
  s.addText(String(n), {
    x, y, w: dia, h: dia, isTextBox: true, margin: 0,
    fontFace: FONT, fontSize: 14, bold: true, color: WHITE, align: "center", valign: "middle",
  });
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

  s.addText("PT LAPI GANESHA UTAMA  ·  LAB IoT ITB", {
    x: M, y: 0.92, w: 8.4, h: 0.3, isTextBox: true, margin: 0,
    fontFace: FONT, fontSize: 11.5, bold: true, charSpacing: 1.8, color: "9FB4E6",
  });

  s.addText("Kesiapan Sertifikasi\nATEX / IECEx — GLD V2", {
    x: M, y: 1.45, w: 8.6, h: 1.9, isTextBox: true, margin: 0,
    fontFace: SERIF, fontSize: 42, bold: true, color: WHITE, lineSpacing: 46,
  });

  s.addText("Pemeriksaan status per 17 September 2026 — apa yang sudah ada, apa yang menahan, dan keputusan yang perlu diambil tim.", {
    x: M, y: 3.55, w: 7.9, h: 0.75, isTextBox: true, margin: 0,
    fontFace: FONT, fontSize: 15, color: "CFD8EA", lineSpacing: 22,
  });

  s.addShape(pres.ShapeType.roundRect, {
    x: M, y: 4.62, w: 5.55, h: 0.84, rectRadius: 0.1,
    fill: { color: WARN }, line: { color: WARN },
  });
  s.addText([
    { text: "STATUS  ", options: { fontSize: 11, bold: true, color: "F6DCC8", charSpacing: 1.4 } },
    { text: "BELUM SIAP DIAJUKAN", options: { fontSize: 19, bold: true, color: WHITE } },
  ], {
    x: M + 0.22, y: 4.62, w: 5.1, h: 0.84, isTextBox: true, margin: 0, valign: "middle",
  });

  s.addText("Rapat internal tim  ·  Program GLD Tahap 2  ·  PT Pertamina Patra Niaga", {
    x: M, y: 5.95, w: 8.6, h: 0.3, isTextBox: true, margin: 0,
    fontFace: FONT, fontSize: 12.5, color: "8E9AB4",
  });
  s.addText("Sumber: dokumen teknis sertifikasi rev 0.1, Dashboard Sertifikasi 5 Sep 2026, audit kesiapan Termin 1 10 Sep 2026.", {
    x: M, y: 6.3, w: 8.6, h: 0.3, isTextBox: true, margin: 0,
    fontFace: FONT, fontSize: 10, italic: true, color: "6F7C96",
  });

  s.addNotes("Pembuka: tujuan rapat bukan melaporkan kemajuan, tapi mengambil 4 keputusan yang menahan jalur sertifikasi. Tegaskan di awal bahwa status resmi kita adalah BELUM SIAP DIAJUKAN, supaya tidak ada klaim berlebih ke Pertamina.");
})();

// ================================================================ 2 · bottom line
(function bottomLine() {
  const s = slideLight();
  heading(s, "Ringkasan", "Posisi kita hari ini");

  const stats = [
    { v: "≈42%", l: "Kesiapan internal\npra-submission", note: "bagian yang ada di tangan tim" },
    { v: "≈20%", l: "Progres keseluruhan\ns/d sertifikat terbit", note: "termasuk antrean uji lab" },
    { v: "6 dari 9", l: "Butir 2.6 checklist ExCB\nbelum tersedia", note: "3 sisanya baru sebagian" },
    { v: "0", l: "Komponen dengan\nsertifikat Ex", note: "FCC/CE/TELEC ≠ sertifikat Ex" },
  ];
  const cw = 2.92, gap = 0.28;
  stats.forEach((st, i) => {
    const x = M + i * (cw + gap);
    card(s, x, 1.62, cw, 2.05, i === 0 ? SURF_2 : SURF);
    s.addText(st.v, {
      x: x + 0.24, y: 1.78, w: cw - 0.4, h: 0.72, isTextBox: true, margin: 0,
      fontFace: SERIF, fontSize: 34, bold: true, color: i === 3 ? WARN : BLUE, valign: "middle",
    });
    s.addText(st.l, {
      x: x + 0.24, y: 2.52, w: cw - 0.4, h: 0.66, isTextBox: true, margin: 0,
      fontFace: FONT, fontSize: 12.5, bold: true, color: CHAR, lineSpacing: 16,
    });
    s.addText(st.note, {
      x: x + 0.24, y: 3.2, w: cw - 0.4, h: 0.32, isTextBox: true, margin: 0,
      fontFace: FONT, fontSize: 10, italic: true, color: MUTED,
    });
  });

  card(s, M, 3.92, 12.09, 2.36, WHITE);
  s.addText("Dua hal yang sering tertukar — pisahkan saat bicara ke Pertamina", {
    x: M + 0.3, y: 4.1, w: 11.5, h: 0.34, isTextBox: true, margin: 0,
    fontFace: FONT, fontSize: 14.5, bold: true, color: CHAR,
  });

  const rows = [
    ["A", "Berkas submission ke ExCB", "Dokumen teknis rev 0.1 sudah 23 halaman dan berformat korporat, tapi Bagian 1 (legalitas & organisasi) belum disusun dan mayoritas butir 2.6 belum ada. Belum bisa dikirim."],
    ["B", "Termin 1 SPK sertifikasi (40%)", "Butuh bukti uji enclosure, log iterasi desain, witness Pertamina, berita acara, dan laporan pekerjaan. Lima-limanya belum ada. Angka ≈42% bukan pengganti acceptance."],
  ];
  rows.forEach((r, i) => {
    const y = 4.55 + i * 0.92;
    s.addShape(pres.ShapeType.roundRect, {
      x: M + 0.3, y: y + 0.05, w: 0.34, h: 0.34, rectRadius: 0.07,
      fill: { color: BLUE }, line: { color: BLUE },
    });
    s.addText(r[0], {
      x: M + 0.3, y: y + 0.05, w: 0.34, h: 0.34, isTextBox: true, margin: 0,
      fontFace: FONT, fontSize: 12, bold: true, color: WHITE, align: "center", valign: "middle",
    });
    s.addText(r[1], {
      x: M + 0.78, y: y, w: 3.0, h: 0.8, isTextBox: true, margin: 0,
      fontFace: FONT, fontSize: 12.5, bold: true, color: CHAR, valign: "top", lineSpacing: 16,
    });
    s.addText(r[2], {
      x: M + 3.9, y: y, w: 7.85, h: 0.8, isTextBox: true, margin: 0,
      fontFace: FONT, fontSize: 11.5, color: CHAR_SOFT, valign: "top", lineSpacing: 15,
    });
  });

  footnote(s, "Audit independen 3 Sep 2026 atas checklist 26 butir yang sama: 0 butir “terbukti tersedia”, 11 sebagian, 12 belum terbukti, 3 tidak berlaku.");
  s.addNotes("Poin utama: kita maju secara rekayasa, tapi bukti formal untuk sertifikasi punya format sendiri dan belum terkumpul. Jangan campur angka 42% (kesiapan internal) dengan klaim milestone pembayaran.");
})();

// ================================================================ 3 · dua angka
(function duaAngka() {
  const s = slideLight();
  heading(s, "Cara membaca angka", "Dua definisi angka — bukan kontradiksi");

  const cols = [
    {
      big: "≈42%", ttl: "Kesiapan internal pra-submission", bg: SURF_2, fg: BLUE,
      items: [
        "Mengukur pekerjaan yang murni ada di tangan tim: scoping, redesign 4 track, dan uji pre-compliance internal.",
        "Tidak menghitung antrean dan durasi pengujian di lab akreditasi eksternal.",
        "Konvergen dengan estimasi Pak Maman “~40%”.",
        "Pakai angka ini saat menjawab: “sejauh apa persiapan tim sudah berjalan?”",
      ],
    },
    {
      big: "≈20%", ttl: "Progres keseluruhan s/d sertifikat terbit", bg: SURF, fg: CHAR,
      items: [
        "Metodologi bottom-up: 5 fase × 4 track (ATEX/IP/EMC/RF).",
        "Termasuk fase Uji Lab Terakreditasi — bobot terbesar 41,7%, durasi 8–12 minggu, ditentukan jadwal lab.",
        "Angka paling konservatif, untuk proyeksi end-to-end.",
        "Pakai angka ini saat menjawab: “kapan sertifikat terbit?”",
      ],
    },
  ];

  cols.forEach((c, i) => {
    const x = M + i * 6.17;
    card(s, x, 1.68, 5.92, 3.75, c.bg);
    s.addText(c.big, {
      x: x + 0.34, y: 1.86, w: 2.4, h: 0.78, isTextBox: true, margin: 0,
      fontFace: SERIF, fontSize: 38, bold: true, color: c.fg, valign: "middle",
    });
    s.addText(c.ttl, {
      x: x + 0.34, y: 2.62, w: 5.2, h: 0.4, isTextBox: true, margin: 0,
      fontFace: FONT, fontSize: 13.5, bold: true, color: CHAR,
    });
    s.addText(c.items.map((t, j) => ({
      text: t, options: { bullet: true, breakLine: j !== c.items.length - 1 },
    })), {
      x: x + 0.34, y: 3.08, w: 5.24, h: 2.22, isTextBox: true, margin: 0,
      fontFace: FONT, fontSize: 11.5, color: CHAR_SOFT, lineSpacing: 15, paraSpaceAfter: 7,
    });
  });

  card(s, M, 5.62, 12.09, 1.0, WARN_BG);
  s.addText([
    { text: "Jangan dicampur tanpa menyebut definisinya.  ", options: { bold: true, color: WARN } },
    { text: "Menyebut “42% siap” tanpa konteks mudah terbaca sebagai “42% menuju sertifikat” — padahal fase uji lab yang paling panjang belum dimulai sama sekali.", options: { color: CHAR_SOFT } },
  ], {
    x: M + 0.3, y: 5.62, w: 11.5, h: 1.0, isTextBox: true, margin: 0,
    fontFace: FONT, fontSize: 12.5, valign: "middle", lineSpacing: 17,
  });

  s.addNotes("Kalau ada yang bertanya kenapa dua angka: jelaskan bahwa 42% adalah tiga fase pertama yang kita kendalikan, 20% adalah seluruh perjalanan termasuk uji lab yang durasinya bukan kecepatan kerja kita.");
})();

// ================================================================ 4 · target & track
(function targetTrack() {
  const s = slideLight();
  heading(s, "Sasaran sertifikasi", "Target klasifikasi & empat track paralel");

  card(s, M, 1.68, 5.42, 3.05, SURF_2);
  s.addText("Target klasifikasi", {
    x: M + 0.3, y: 1.85, w: 4.8, h: 0.32, isTextBox: true, margin: 0,
    fontFace: FONT, fontSize: 13.5, bold: true, color: CHAR,
  });
  const klas = [
    ["Zona 1", "Kategori 2G · Grup II", OK, OK_BG, "ditetapkan proposal 21 Feb 2026"],
    ["T4 (≤135 °C)", "kelas suhu", HOLD, HOLD_BG, "ditargetkan, belum diverifikasi"],
    ["Grup gas IIC", "mencakup H2", HOLD, HOLD_BG, "rekomendasi tim, bukan keputusan ExCB"],
    ["Ex d / Ex e / Ex i", "metode proteksi", WARN, WARN_BG, "belum diputuskan"],
  ];
  klas.forEach((k, i) => {
    const y = 2.25 + i * 0.58;
    s.addText([
      { text: k[0] + "  ", options: { bold: true, color: CHAR, fontSize: 12.5 } },
      { text: k[1], options: { color: MUTED, fontSize: 10.5 } },
    ], {
      x: M + 0.3, y: y, w: 3.1, h: 0.28, isTextBox: true, margin: 0, fontFace: FONT,
    });
    s.addText(k[4], {
      x: M + 0.3, y: y + 0.24, w: 3.2, h: 0.26, isTextBox: true, margin: 0,
      fontFace: FONT, fontSize: 9.5, italic: true, color: MUTED,
    });
    chip(s, M + 3.72, y + 0.06, k[2] === OK ? "Final" : (k[2] === HOLD ? "Sementara" : "Terbuka"), k[2], k[3], 1.3);
  });

  card(s, M + 5.72, 1.68, 6.37, 3.05, SURF);
  s.addText("Empat track paralel", {
    x: M + 6.02, y: 1.85, w: 5.8, h: 0.32, isTextBox: true, margin: 0,
    fontFace: FONT, fontSize: 13.5, bold: true, color: CHAR,
  });
  const tracks = [
    ["ATEX", "Directive 2014/34/EU", "Paling tertinggal — gambar teknik, BOM Ex, datasheet material, draft manual semua masih perlu disusun.", WARN, WARN_BG, "Tertinggal"],
    ["IP 66/67", "IEC 60529", "Bergantung desain selubung dari mitra casing; gasket & cable gland belum ditentukan.", WARN, WARN_BG, "Menunggu"],
    ["EMC", "EN 61000-6-2 / -4", "Paling matang — tabel parameter lengkap sejak 19 Agu. Belum ada pre-scan/uji lab.", HOLD, HOLD_BG, "Termatang"],
    ["RF", "ETSI / SDPPI", "Modul E22-900MM22S sudah bersertifikat RF; berkas pengajuan belum disusun.", HOLD, HOLD_BG, "Sebagian"],
  ];
  tracks.forEach((t, i) => {
    const x = M + 6.02 + (i % 2) * 3.06;
    const y = 2.28 + Math.floor(i / 2) * 1.16;
    s.addText(t[0], {
      x, y, w: 1.5, h: 0.26, isTextBox: true, margin: 0,
      fontFace: FONT, fontSize: 13, bold: true, color: BLUE,
    });
    chip(s, x + 1.52, y - 0.01, t[5], t[3], t[4], 1.12);
    s.addText(t[1], {
      x, y: y + 0.26, w: 2.8, h: 0.22, isTextBox: true, margin: 0,
      fontFace: FONT, fontSize: 9.5, italic: true, color: MUTED,
    });
    s.addText(t[2], {
      x, y: y + 0.5, w: 2.82, h: 0.62, isTextBox: true, margin: 0,
      fontFace: FONT, fontSize: 10, color: CHAR_SOFT, lineSpacing: 13,
    });
  });

  card(s, M, 4.94, 12.09, 1.6, WHITE);
  s.addText("Objek sertifikasi = Node Sensor (GLD) saja", {
    x: M + 0.3, y: 5.1, w: 6.0, h: 0.32, isTextBox: true, margin: 0,
    fontFace: FONT, fontSize: 13.5, bold: true, color: CHAR,
  });
  s.addText("Cluster Head dan Gateway diasumsikan selalu berada di safe area, sehingga tidak masuk cakupan submission. Asumsi ini berasal dari konfirmasi internal, bukan hasil kajian klasifikasi area formal oleh Pertamina — perlu dikunci tertulis sebelum submission, karena kalau meleset, cakupan sertifikasi bertambah dua perangkat.",
    {
      x: M + 0.3, y: 5.46, w: 11.5, h: 0.92, isTextBox: true, margin: 0,
      fontFace: FONT, fontSize: 11.5, color: CHAR_SOFT, lineSpacing: 16,
    });

  footnote(s, "Kick-off 12 Jun 2026 · estimasi durasi total 5–8 bulan (≈Nov 2026 – Feb 2027) menurut proposal sertifikasi terpadu ATEX/IP/EMC/RF.");
  s.addNotes("Tekankan: Zona 1/2G sudah ditetapkan proposal, jadi bukan nol. Yang benar-benar terbuka adalah metode proteksi dan verifikasi T4 — dua hal ini yang menahan sisa dokumen.");
})();

// ================================================================ 5 · sudah ada
(function sudahAda() {
  const s = slideLight();
  heading(s, "Modal yang sudah di tangan", "Bukti teknis yang sudah terkumpul");

  const items = [
    ["Dokumen teknis submission", "23 halaman, format korporat resmi (No. LGU/GLD/IECEX-TDF/2026-001). Bagian 2 butir 1–6 dan Bagian 3 sudah terisi."],
    ["Diagram blok skematik 9 lembar", "Hasil trace skematik EasyEDA asli — 204 komponen dengan bukti pin-to-net yang dapat ditelusuri."],
    ["PCB layout & model 3D", "Ekspor native EasyEDA/JLCPCB (routed copper) untuk papan utama, plus render 3D papan terpasang."],
    ["BOM elektronik dua papan", "Motherboard 89 baris / 214 komponen dan sensor board 14 baris / 24 komponen, lengkap manufacturer & part number."],
    ["Gambar CAD bertoleransi", "Model STEP dalam milimeter: leher selubung ⌀75 mm, tinggi probe 191,51 mm, pelat mounting 250×250 mm."],
    ["Prototipe fisik & foto produk", "Unit enclosure terakit (foto 26 Agu 2026) dan 7 foto produk yang sudah masuk dokumen submission."],
  ];
  const cw = 3.9, ch = 1.52, gx = 0.26, gy = 0.26;
  items.forEach((it, i) => {
    const x = M + (i % 3) * (cw + gx);
    const y = 1.72 + Math.floor(i / 3) * (ch + gy);
    card(s, x, y, cw, ch, SURF);
    badge(s, x + 0.26, y + 0.24, i + 1, 0.4);
    s.addText(it[0], {
      x: x + 0.76, y: y + 0.22, w: cw - 1.0, h: 0.44, isTextBox: true, margin: 0,
      fontFace: FONT, fontSize: 12.5, bold: true, color: CHAR, valign: "middle", lineSpacing: 15,
    });
    s.addText(it[1], {
      x: x + 0.26, y: y + 0.72, w: cw - 0.52, h: 0.68, isTextBox: true, margin: 0,
      fontFace: FONT, fontSize: 10.5, color: CHAR_SOFT, lineSpacing: 14,
    });
  });

  card(s, M, 5.32, 12.09, 1.18, OK_BG);
  s.addText([
    { text: "Artinya:  ", options: { bold: true, color: OK } },
    { text: "sisi rekayasa dan bukti perangkat keras sudah cukup kuat. Yang kurang bukan “barangnya belum ada”, melainkan dokumen berformat sertifikasi — kalkulasi, datasheet material, dan keputusan rekayasa yang harus diambil lebih dulu.", options: { color: CHAR_SOFT } },
  ], {
    x: M + 0.3, y: 5.32, w: 11.5, h: 1.18, isTextBox: true, margin: 0,
    fontFace: FONT, fontSize: 12.5, valign: "middle", lineSpacing: 17,
  });

  s.addNotes("Slide penyeimbang — supaya rapat tidak terasa hanya daftar kekurangan. Semua item di sini sudah tertanam sebagai gambar/tabel nyata di dokumen submission, bukan sekadar ada di folder.");
})();

// ================================================================ 6 · peta checklist
(function petaChecklist() {
  const s = slideLight();
  heading(s, "Peta checklist ExCB", "Status berkas vs daftar persyaratan ExCB");

  s.addChart(pres.ChartType.bar, [{
    name: "Butir",
    labels: ["Final / tersedia", "Sebagian tersedia", "Belum tersedia"],
    values: [21, 8, 10],
  }], {
    x: M, y: 1.72, w: 5.55, h: 2.5,
    barDir: "bar", barGrouping: "clustered",
    chartColors: [BLUE, HOLD, WARN], varyColors: true,
    showTitle: true, title: "Status butir di dokumen submission", titleFontSize: 12,
    titleColor: CHAR, titleFontFace: FONT,
    showValue: true, dataLabelPosition: "outEnd", dataLabelFontSize: 11,
    dataLabelColor: CHAR, dataLabelFontFace: FONT,
    showLegend: false,
    catAxisLabelColor: CHAR_SOFT, catAxisLabelFontSize: 11, catAxisLabelFontFace: FONT,
    valAxisLabelColor: MUTED, valAxisLabelFontSize: 10, valAxisLabelFontFace: FONT,
    valGridLine: { color: LINE, size: 0.75 }, catGridLine: { style: "none" },
    valAxisMinVal: 0, valAxisMaxVal: 24,
  });

  card(s, M + 5.82, 1.72, 6.27, 2.5, SURF);
  s.addText("Bagian 2.6 — desain & manufaktur (a–i)", {
    x: M + 6.1, y: 1.88, w: 5.7, h: 0.3, isTextBox: true, margin: 0,
    fontFace: FONT, fontSize: 13, bold: true, color: CHAR,
  });
  const b26 = [
    ["a", "Gambar lengkap", "Sebagian", HOLD, HOLD_BG],
    ["b", "BOM komponen Ex-critical", "Sebagian", HOLD, HOLD_BG],
    ["c", "Datasheet material non-logam", "Belum", WARN, WARN_BG],
    ["d", "Deskripsi proses manufaktur", "Belum", WARN, WARN_BG],
    ["e", "Kalkulasi proteksi ledakan", "Belum", WARN, WARN_BG],
    ["f", "Kalkulasi kelas suhu", "Belum", WARN, WARN_BG],
    ["g", "Instruksi pakai & instalasi", "Sebagian", HOLD, HOLD_BG],
    ["h", "Informasi nameplate", "Belum", WARN, WARN_BG],
    ["i", "Sertifikat komponen Ex", "Belum", WARN, WARN_BG],
  ];
  b26.forEach((r, i) => {
    const y = 2.26 + i * 0.205;
    s.addText(r[0] + ")", {
      x: M + 6.1, y, w: 0.28, h: 0.2, isTextBox: true, margin: 0,
      fontFace: FONT, fontSize: 10.5, bold: true, color: BLUE,
    });
    s.addText(r[1], {
      x: M + 6.4, y, w: 3.6, h: 0.2, isTextBox: true, margin: 0,
      fontFace: FONT, fontSize: 10.5, color: CHAR_SOFT,
    });
    s.addText(r[2], {
      x: M + 10.1, y, w: 1.1, h: 0.2, isTextBox: true, margin: 0,
      fontFace: FONT, fontSize: 10, bold: true, color: r[3],
    });
  });

  const notes = [
    ["Bagian 1 belum ada sama sekali", "Informasi dasar aplikasi & organisasi: formulir ExCB, izin usaha, struktur organisasi, profil fasilitas manufaktur, ISO 9001. Murni administratif — tidak menunggu siapa pun, bisa jalan minggu ini."],
    ["Bagian 2 & 3 sudah terisi", "Deskripsi produk, spesifikasi, parameter teknis, foto, lingkungan instalasi, dan informasi sampel sudah tertulis — dengan status apa adanya, tanpa mengarang angka."],
  ];
  notes.forEach((n, i) => {
    const x = M + i * 6.17;
    card(s, x, 4.42, 5.92, 1.95, i === 0 ? WARN_BG : WHITE);
    s.addText(n[0], {
      x: x + 0.3, y: 4.6, w: 5.3, h: 0.3, isTextBox: true, margin: 0,
      fontFace: FONT, fontSize: 13, bold: true, color: i === 0 ? WARN : CHAR,
    });
    s.addText(n[1], {
      x: x + 0.3, y: 4.96, w: 5.32, h: 1.28, isTextBox: true, margin: 0,
      fontFace: FONT, fontSize: 11.5, color: CHAR_SOFT, lineSpacing: 16,
    });
  });

  footnote(s, "Hitungan butir diambil dari badge status di dokumen teknis sertifikasi rev 0.1 (HTML/PDF/DOCX, 23 halaman).");
  s.addNotes("Pesan slide ini: bagian yang bisa kita tulis sendiri sudah ditulis. Yang tersisa hampir semuanya menunggu keputusan rekayasa atau mitra casing — kecuali Bagian 1 yang murni administratif dan bisa langsung dikerjakan.");
})();

// ================================================================ 7 · penghambat
(function penghambat() {
  const s = slideLight();
  heading(s, "Analisis", "Lima hal yang menahan");

  const rows = [
    ["Metode proteksi belum diputuskan", "Ex d, Ex e, atau Ex i belum dipilih dan belum dikonfirmasi ke ExCB.", "Menahan kalkulasi proteksi ledakan (2.6.e), dimensi flame-path pada gambar, dan arah desain ke mitra casing."],
    ["Kelas suhu T4 belum diverifikasi", "Nol pengukuran maupun kalkulasi hot-spot. Heater sensor MQ lazim bekerja di ~200–400 °C, sedangkan T4 berarti ≤135 °C.", "Risiko teknis terbesar: kalau hot-spot gagal, desain sensing head harus diubah — bukan sekadar revisi dokumen."],
    ["Bagian 1 belum disusun", "Formulir aplikasi, izin usaha, struktur organisasi, profil fasilitas, ISO 9001.", "Submission tidak bisa dibuka meski berkas teknis lengkap. Ini satu-satunya item yang tidak bergantung pihak lain."],
    ["Belum ada komponen bersertifikat Ex", "Flame arrestor sinter-metal di elemen sensing belum masuk BOM; baterai Li-ion 18650 di node belum diverifikasi Ex.", "Butir 2.6.i kosong. Sertifikat FCC/TELEC/CE pada ESP32-S3 dan modul LoRa tidak memenuhi syarat ini."],
    ["Item yang menunggu mitra casing", "Datasheet material non-logam, proses manufaktur, BOM Ex-critical (gasket, cable gland, potting), nameplate.", "Bukan pekerjaan yang berhenti, tapi jadwalnya di luar kendali kita — perlu komitmen tanggal dari mitra."],
  ];

  rows.forEach((r, i) => {
    const y = 1.66 + i * 1.02;
    card(s, M, y, 12.09, 0.92, i === 1 ? WARN_BG : SURF);
    badge(s, M + 0.24, y + 0.24, i + 1, 0.44);
    s.addText(r[0], {
      x: M + 0.82, y: y + 0.11, w: 3.25, h: 0.7, isTextBox: true, margin: 0,
      fontFace: FONT, fontSize: 12.5, bold: true, color: i === 1 ? WARN : CHAR, valign: "middle", lineSpacing: 15,
    });
    s.addText(r[1], {
      x: M + 4.18, y: y + 0.11, w: 3.95, h: 0.7, isTextBox: true, margin: 0,
      fontFace: FONT, fontSize: 10.5, color: CHAR_SOFT, valign: "middle", lineSpacing: 14,
    });
    s.addText(r[2], {
      x: M + 8.24, y: y + 0.11, w: 3.6, h: 0.7, isTextBox: true, margin: 0,
      fontFace: FONT, fontSize: 10.5, color: CHAR_SOFT, valign: "middle", lineSpacing: 14,
    });
  });

  s.addText("PENGHAMBAT", { x: M + 0.82, y: 1.42, w: 3.2, h: 0.22, isTextBox: true, margin: 0, fontFace: FONT, fontSize: 9, bold: true, charSpacing: 1.2, color: MUTED });
  s.addText("KONDISI SAAT INI", { x: M + 4.18, y: 1.42, w: 3.9, h: 0.22, isTextBox: true, margin: 0, fontFace: FONT, fontSize: 9, bold: true, charSpacing: 1.2, color: MUTED });
  s.addText("DAMPAK", { x: M + 8.24, y: 1.42, w: 3.6, h: 0.22, isTextBox: true, margin: 0, fontFace: FONT, fontSize: 9, bold: true, charSpacing: 1.2, color: MUTED });

  s.addNotes("Baris 2 disorot karena satu-satunya yang berpotensi memaksa perubahan desain, bukan hanya dokumen. Kalau waktu rapat terbatas, bahas baris 1 dan 2 saja — sisanya bisa diputuskan lewat chat.");
})();

// ================================================================ 8 · jalur kritis
(function jalurKritis() {
  const s = slideLight();
  heading(s, "Urutan kerja", "Jalur kritis — apa yang harus lebih dulu");

  const steps = [
    ["Putuskan metode proteksi", "Ex d vs Ex i, dikonfirmasi ke ExCB", "Membuka 4 pekerjaan sekaligus"],
    ["Ukur hot-spot sensor", "Kondisi terburuk, terdokumentasi", "Konfirmasi atau koreksi klaim T4"],
    ["Susun kalkulasi & gambar", "Flame-path, kelas suhu, drawing pack", "Menutup 2.6.a, e, f"],
    ["Lengkapi BOM Ex & material", "Bersama mitra casing + flame arrestor", "Menutup 2.6.b, c, d, h, i"],
    ["Sesi uji ber-witness", "Disaksikan & divalidasi Pertamina", "Menutup Termin 1 sekaligus"],
  ];

  const cw = 2.24, gap = 0.22;
  steps.forEach((st, i) => {
    const x = M + i * (cw + gap);
    card(s, x, 1.9, cw, 2.45, i === 0 ? SURF_2 : SURF);
    badge(s, x + 0.24, 2.12, i + 1, 0.42);
    s.addText(st[0], {
      x: x + 0.22, y: 2.66, w: cw - 0.44, h: 0.66, isTextBox: true, margin: 0,
      fontFace: FONT, fontSize: 12.5, bold: true, color: CHAR, lineSpacing: 15,
    });
    s.addText(st[1], {
      x: x + 0.22, y: 3.3, w: cw - 0.44, h: 0.52, isTextBox: true, margin: 0,
      fontFace: FONT, fontSize: 10, color: CHAR_SOFT, lineSpacing: 13,
    });
    s.addText(st[2], {
      x: x + 0.22, y: 3.86, w: cw - 0.44, h: 0.4, isTextBox: true, margin: 0,
      fontFace: FONT, fontSize: 9.5, italic: true, color: BLUE, lineSpacing: 12,
    });
    if (i < steps.length - 1) {
      s.addShape(pres.ShapeType.rightArrow, {
        x: x + cw + 0.03, y: 3.03, w: 0.17, h: 0.2,
        fill: { color: LINE }, line: { color: LINE },
      });
    }
  });

  card(s, M, 4.62, 5.92, 1.86, WHITE);
  s.addText("Yang bisa jalan paralel sekarang", {
    x: M + 0.3, y: 4.8, w: 5.3, h: 0.3, isTextBox: true, margin: 0,
    fontFace: FONT, fontSize: 13, bold: true, color: OK,
  });
  s.addText([
    { text: "Berkas Bagian 1 (legalitas, struktur organisasi, ISO 9001) — tidak bergantung keputusan rekayasa.", options: { bullet: true, breakLine: true } },
    { text: "Draft safety warning & instruksi instalasi Ex (2.6.g butir a).", options: { bullet: true, breakLine: true } },
    { text: "Penguncian tertulis asumsi CH/Gateway berada di safe area.", options: { bullet: true } },
  ], {
    x: M + 0.3, y: 5.16, w: 5.32, h: 1.2, isTextBox: true, margin: 0,
    fontFace: FONT, fontSize: 11, color: CHAR_SOFT, lineSpacing: 14, paraSpaceAfter: 5,
  });

  card(s, M + 6.17, 4.62, 5.92, 1.86, WARN_BG);
  s.addText("Yang tidak bisa dipercepat", {
    x: M + 6.47, y: 4.8, w: 5.3, h: 0.3, isTextBox: true, margin: 0,
    fontFace: FONT, fontSize: 13, bold: true, color: WARN,
  });
  s.addText([
    { text: "Fase Uji Lab Terakreditasi: 8–12 minggu, bobot 41,7% dari total perjalanan.", options: { bullet: true, breakLine: true } },
    { text: "Antrean & penjadwalan lab eksternal — bukan fungsi kecepatan kerja tim.", options: { bullet: true, breakLine: true } },
    { text: "Karena itu setiap minggu tertunda di hulu menggeser tanggal sertifikat satu-untuk-satu.", options: { bullet: true } },
  ], {
    x: M + 6.47, y: 5.16, w: 5.32, h: 1.2, isTextBox: true, margin: 0,
    fontFace: FONT, fontSize: 11, color: CHAR_SOFT, lineSpacing: 14, paraSpaceAfter: 5,
  });

  s.addNotes("Inti slide: langkah 1 bukan pekerjaan besar, tapi selama belum diputuskan, empat pekerjaan di belakangnya tidak bisa dimulai. Ini alasan kenapa rapat hari ini sebaiknya menghasilkan keputusan, bukan tugas riset lanjutan.");
})();

// ================================================================ 9 · termin 1
(function termin1() {
  const s = slideLight();
  heading(s, "Kontraktual", "Termin 1 sertifikasi (40%) — belum layak diajukan", { size: 28 });

  const syarat = [
    ["1", "Prototipe enclosure tersedia", "Sebagian", HOLD, "Foto perakitan 26 Agu ada; identitas unit, nomor seri, dan lembar identifikasi sampel belum."],
    ["2", "Prototipe telah diuji", "Belum terbukti", WARN, "Ada uji fungsi sistem & LoRa, tapi bukan uji enclosure (mekanik, termal, sealing, fault)."],
    ["3", "Ada iterasi perbaikan desain", "Belum terbukti", WARN, "“ATEX Casing v2” adalah model mounting, bukan riwayat iterasi berbasis hasil uji."],
    ["4", "Disaksikan & divalidasi Pertamina", "Belum terbukti", WARN, "Notulen rapat ada, witness sheet dan pernyataan penerimaan hasil belum ada."],
    ["5", "Sebelum uji lab terakreditasi", "Urutan aman", OK, "Belum ada klaim pengujian lab, jadi urutan kerja masih memungkinkan."],
    ["6", "Berita acara", "Belum ada", WARN, "Notulen pembahasan tidak setara berita acara validasi hasil uji."],
    ["7", "Laporan pekerjaan Termin 1", "Belum ada", WARN, "Dashboard & gap analysis bukan laporan pelaksanaan pengujian."],
  ];

  syarat.forEach((r, i) => {
    const y = 1.66 + i * 0.6;
    if (i % 2 === 0) {
      s.addShape(pres.ShapeType.roundRect, {
        x: M, y: y - 0.04, w: 12.09, h: 0.56, rectRadius: 0.05,
        fill: { color: SURF }, line: { color: SURF },
      });
    }
    s.addText(r[0], {
      x: M + 0.2, y: y + 0.03, w: 0.3, h: 0.4, isTextBox: true, margin: 0,
      fontFace: FONT, fontSize: 12, bold: true, color: BLUE, valign: "middle",
    });
    s.addText(r[1], {
      x: M + 0.58, y: y + 0.03, w: 3.3, h: 0.4, isTextBox: true, margin: 0,
      fontFace: FONT, fontSize: 12, bold: true, color: CHAR, valign: "middle",
    });
    chip(s, M + 3.98, y + 0.1, r[2], r[3], r[3] === OK ? OK_BG : (r[3] === HOLD ? HOLD_BG : WARN_BG), 1.48);
    s.addText(r[4], {
      x: M + 5.62, y: y + 0.03, w: 6.3, h: 0.44, isTextBox: true, margin: 0,
      fontFace: FONT, fontSize: 10.5, color: CHAR_SOFT, valign: "middle", lineSpacing: 13,
    });
  });

  card(s, M, 5.96, 12.09, 0.82, WARN_BG);
  s.addText([
    { text: "Angka “≈42% kesiapan internal” bukan bukti acceptance milestone pembayaran. ", options: { bold: true, color: WARN } },
    { text: "Tiga template kerja (log uji & iterasi, berita acara validasi, laporan pekerjaan) sudah tersedia di Paket Pertamina/02_Sertifikasi_ATEX_IECEx/ — tinggal diisi setelah sesi uji.", options: { color: CHAR_SOFT } },
  ], {
    x: M + 0.3, y: 5.96, w: 11.5, h: 0.82, isTextBox: true, margin: 0,
    fontFace: FONT, fontSize: 11.5, valign: "middle", lineSpacing: 15,
  });

  s.addNotes("Bedakan dengan Termin 1 field testing 20% yang paketnya sudah final. Yang ini termin sertifikasi 40% dan kuncinya satu: sesi uji enclosure yang disaksikan Pertamina. Begitu sesi itu terjadi, lima dari tujuh baris tertutup sekaligus.");
})();

// ================================================================ 10 · keputusan
(function keputusan() {
  const s = slideLight();
  heading(s, "Yang diminta dari rapat ini", "Empat keputusan — bukan empat tugas riset");

  const dec = [
    ["Metode proteksi Ex", "Pilih Ex d atau Ex i untuk dikonfirmasi ke ExCB.", "Perlu: pemilik keputusan teknis + tanggal konfirmasi ke ExCB."],
    ["Uji hot-spot sensor", "Tetapkan PIC, alat ukur, dan tanggal pengukuran suhu titik terpanas.", "Perlu: PIC + ketersediaan alat ukur suhu terkalibrasi."],
    ["Sesi uji ber-witness", "Tetapkan tanggal usulan sesi uji enclosure bersama Pertamina.", "Perlu: tanggal usulan + nama perwakilan Pertamina yang berwenang."],
    ["Berkas Bagian 1", "Tunjuk PIC pengumpulan legalitas, struktur organisasi, dan ISO 9001.", "Perlu: PIC administratif + target selesai (bisa minggu ini)."],
  ];

  const cw = 2.92, gap = 0.28;
  dec.forEach((d, i) => {
    const x = M + i * (cw + gap);
    card(s, x, 1.78, cw, 3.1, WHITE);
    badge(s, x + 0.26, 2.0, i + 1, 0.46);
    s.addText(d[0], {
      x: x + 0.26, y: 2.58, w: cw - 0.52, h: 0.56, isTextBox: true, margin: 0,
      fontFace: FONT, fontSize: 14, bold: true, color: BLUE, lineSpacing: 17,
    });
    s.addText(d[1], {
      x: x + 0.26, y: 3.18, w: cw - 0.52, h: 0.9, isTextBox: true, margin: 0,
      fontFace: FONT, fontSize: 11.5, color: CHAR_SOFT, lineSpacing: 15,
    });
    s.addShape(pres.ShapeType.roundRect, {
      x: x + 0.26, y: 4.12, w: cw - 0.52, h: 0.62, rectRadius: 0.06,
      fill: { color: SURF_2 }, line: { color: SURF_2 },
    });
    s.addText(d[2], {
      x: x + 0.38, y: 4.12, w: cw - 0.76, h: 0.62, isTextBox: true, margin: 0,
      fontFace: FONT, fontSize: 9.5, color: CHAR, valign: "middle", lineSpacing: 12,
    });
  });

  card(s, M, 5.12, 12.09, 1.4, SURF);
  s.addText("Usulan kerangka empat minggu setelah keputusan diambil", {
    x: M + 0.3, y: 5.26, w: 8.0, h: 0.3, isTextBox: true, margin: 0,
    fontFace: FONT, fontSize: 13, bold: true, color: CHAR,
  });
  const wk = [
    ["Minggu 1", "Keputusan proteksi + Bagian 1 mulai dikumpulkan"],
    ["Minggu 2", "Pengukuran hot-spot + draft safety warning"],
    ["Minggu 3", "Kalkulasi & drawing pack; koordinasi mitra casing"],
    ["Minggu 4", "Dry run internal, lalu ajukan tanggal sesi witness"],
  ];
  wk.forEach((w, i) => {
    const x = M + 0.3 + i * 2.93;
    s.addText(w[0], {
      x, y: 5.64, w: 2.7, h: 0.24, isTextBox: true, margin: 0,
      fontFace: FONT, fontSize: 11, bold: true, color: BLUE,
    });
    s.addText(w[1], {
      x, y: 5.88, w: 2.78, h: 0.54, isTextBox: true, margin: 0,
      fontFace: FONT, fontSize: 10, color: CHAR_SOFT, lineSpacing: 13,
    });
  });

  footnote(s, "Kerangka ini usulan untuk dibahas, bukan komitmen jadwal — tanggal pasti bergantung ketersediaan alat ukur, mitra casing, dan perwakilan Pertamina.");
  s.addNotes("Tutup rapat dengan mengisi keempat kotak abu-abu: nama PIC dan tanggal. Kalau empat kotak itu terisi, rapat ini berhasil.");
})();

// ================================================================ 11 · penutup
(function penutup() {
  const s = slideDark();

  s.addShape(pres.ShapeType.ellipse, {
    x: 10.4, y: 4.4, w: 4.6, h: 4.6, fill: { color: BLUE_DK, transparency: 72 }, line: { color: BLUE_DK, transparency: 72 },
  });

  s.addText("PESAN YANG DIBAWA KELUAR", {
    x: M, y: 0.72, w: 8.0, h: 0.28, isTextBox: true, margin: 0,
    fontFace: FONT, fontSize: 11, bold: true, charSpacing: 1.8, color: "9FB4E6",
  });
  s.addText("Tiga kalimat untuk dipakai seragam", {
    x: M, y: 1.06, w: 9.5, h: 0.6, isTextBox: true, margin: 0,
    fontFace: SERIF, fontSize: 32, bold: true, color: WHITE,
  });

  const msg = [
    ["Perangkatnya matang, berkasnya belum", "Prototipe, skematik, PCB, BOM elektronik, dan gambar CAD sudah nyata. Yang belum adalah dokumen berformat sertifikasi dan dua keputusan rekayasa di hulu."],
    ["Satu keputusan membuka empat pekerjaan", "Metode proteksi (Ex d / Ex i) menahan kalkulasi, gambar flame-path, arah desain casing, dan sebagian BOM sekaligus."],
    ["Termin 1 sertifikasi butuh sesi uji, bukan dokumen tambahan", "Kuncinya satu sesi uji enclosure yang disaksikan Pertamina — bukan menambah laporan status."],
  ];
  msg.forEach((m, i) => {
    const y = 2.0 + i * 1.28;
    s.addShape(pres.ShapeType.roundRect, {
      x: M, y, w: 11.4, h: 1.12, rectRadius: 0.07,
      fill: { color: "34302C" }, line: { color: "413C37", width: 0.75 },
    });
    badge(s, M + 0.3, y + 0.34, i + 1, 0.44);
    s.addText(m[0], {
      x: M + 0.9, y: y + 0.16, w: 4.3, h: 0.8, isTextBox: true, margin: 0,
      fontFace: FONT, fontSize: 13, bold: true, color: WHITE, valign: "middle", lineSpacing: 16,
    });
    s.addText(m[1], {
      x: M + 5.35, y: y + 0.16, w: 5.85, h: 0.8, isTextBox: true, margin: 0,
      fontFace: FONT, fontSize: 11, color: "C8CEDA", valign: "middle", lineSpacing: 14,
    });
  });

  s.addShape(pres.ShapeType.roundRect, {
    x: M, y: 6.02, w: 11.4, h: 0.76, rectRadius: 0.07,
    fill: { color: "3A2A1C" }, line: { color: "5B4026", width: 0.75 },
  });
  s.addText([
    { text: "Jangan diklaim:  ", options: { bold: true, color: "F0B07A" } },
    { text: "perangkat sudah tersertifikasi · sudah lulus lab terakreditasi · Termin 1 sertifikasi sudah dipenuhi · grup gas IIC sudah disetujui ExCB.", options: { color: "E2D6C9" } },
  ], {
    x: M + 0.3, y: 6.02, w: 10.8, h: 0.76, isTextBox: true, margin: 0,
    fontFace: FONT, fontSize: 11.5, valign: "middle", lineSpacing: 15,
  });

  s.addNotes("Penutup: samakan bahasa satu tim. Kalau ada yang ditanya Pertamina di luar rapat, empat klaim di kotak bawah adalah yang tidak boleh keluar dari siapa pun.");
})();

pres.writeFile({ fileName: OUT }).then(() => console.log("Tersimpan:", OUT));
