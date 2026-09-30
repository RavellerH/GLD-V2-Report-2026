/**
 * Generator deck presentasi: Rapat Koordinasi Persiapan Instalasi RU IV Cilacap (29 Sep 2026).
 *
 * Output : Deliverables/Presentasi_Rapat_Koordinasi_Instalasi_29September2026.pptx
 * Palet  : biru #2B5FCB + charcoal #262321 (aturan kerja repo).
 * Jalankan: NODE_PATH=<lokasi node_modules pptxgenjs> node scripts/build_presentasi_rapat_koordinasi_29sep.js
 */

const path = require("path");
const PptxGenJS = require("pptxgenjs");

const OUT = path.resolve(__dirname, "..", "Deliverables",
  "Presentasi_Rapat_Koordinasi_Instalasi_29September2026.pptx");

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
pres.title = "Rapat Koordinasi Persiapan Instalasi RU IV Cilacap";

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
  s.addText("Rapat Koordinasi Persiapan\nInstalasi RU IV Cilacap", {
    x: M, y: 1.45, w: 10.5, h: 1.9, isTextBox: true, margin: 0,
    fontFace: SERIF, fontSize: 38, bold: true, color: WHITE, lineSpacing: 42,
  });
  s.addText("Tindak lanjut pasca site survey — field testing multi-modality gas leak detector, co-research Pertamina Patra Niaga & Institut Teknologi Bandung melalui LAPI Ganesha Utama.", {
    x: M, y: 3.5, w: 9.3, h: 0.85, isTextBox: true, margin: 0,
    fontFace: FONT, fontSize: 14, color: "CFD8EA", lineSpacing: 20,
  });
  s.addShape(pres.ShapeType.roundRect, {
    x: M, y: 4.58, w: 6.4, h: 0.6, rectRadius: 0.1, fill: { color: BLUE }, line: { color: BLUE },
  });
  s.addText("Selasa, 29 September 2026  ·  09.00–10.00 WIB  ·  Microsoft Teams", {
    x: M + 0.2, y: 4.58, w: 6.0, h: 0.6, isTextBox: true, margin: 0,
    fontFace: FONT, fontSize: 13, bold: true, color: WHITE, valign: "middle",
  });
  s.addText("Ref. Surat Perintah Kerja SP-002/KPI43400/2026-S0", {
    x: M, y: 5.35, w: 8.6, h: 0.3, isTextBox: true, margin: 0,
    fontFace: FONT, fontSize: 11, color: "8E9AB4",
  });
  s.addNotes("Pembuka: tegaskan tujuan rapat adalah koordinasi lanjutan pasca site survey untuk menyepakati langkah menuju mobilisasi & instalasi RU IV Cilacap. Sampaikan bahwa ada 4 keputusan konkret yang perlu diambil bersama hari ini.");
})();

// ================================================================ 2 · agenda
(function agenda() {
  const s = slideLight();
  heading(s, "Agenda", "Empat hal yang akan kita bahas");
  const items = [
    ["1", "Status proyek & sertifikasi", "Ringkas — posisi Kurva-S proyek keseluruhan, persiapan instalasi, dan sertifikasi ATEX/IECEx."],
    ["2", "Yang perlu disiapkan Pertamina RU IV", "Perizinan, HSE, lokasi, catu daya, jadwal — dengan prioritas jelas."],
    ["3", "Yang perlu disiapkan Vendor Instalasi", "Legalitas, personel, material, verifikasi lapangan, koordinasi hari-H."],
    ["4", "Keputusan yang diambil hari ini", "4 keputusan konkret yang menentukan jadwal mobilisasi."],
  ];
  items.forEach((it, i) => {
    const y = 1.75 + i * 1.15;
    badge(s, M, y, it[0], 0.5);
    s.addText(it[1], {
      x: M + 0.75, y: y - 0.06, w: 10.8, h: 0.4, isTextBox: true, margin: 0,
      fontFace: FONT, fontSize: 17, bold: true, color: CHAR,
    });
    s.addText(it[2], {
      x: M + 0.75, y: y + 0.34, w: 10.8, h: 0.55, isTextBox: true, margin: 0,
      fontFace: FONT, fontSize: 12.5, color: CHAR_SOFT, lineSpacing: 16,
    });
  });
  s.addNotes("Jelaskan urutan: mulai dari status singkat, lalu langsung ke action items per pihak, ditutup dengan keputusan konkret supaya rapat 1 jam ini efisien dan actionable.");
})();

// ================================================================ 3 · status proyek & kurva-s
(function statusProyek() {
  const s = slideLight();
  heading(s, "1 · Status", "Posisi hari ini — tiga jalur paralel");

  const tracks = [
    { label: "Proyek keseluruhan", pct: 49, plan: 52, note: "vs rencana 52% (data 17 Sep) — sisi rekayasa lab", color: BLUE },
    { label: "Sertifikasi ATEX/IECEx", pct: 20, plan: null, note: "estimasi 5 Sep, metodologi bottom-up 4-track", color: "1C93C6" },
    { label: "Persiapan instalasi RU IV", pct: 38, plan: null, note: "LGU&ITB 100% (rekayasa) · Pertamina & Vendor 0%", color: VENDOR },
    { label: "Dokumen Termin 1 — Field Testing", pct: 100, plan: null, note: "laporan pemenuhan & draf BAST lengkap; evaluasi oleh Pertamina", color: OK },
  ];
  tracks.forEach((t, i) => {
    const y = 1.7 + i * 0.98;
    s.addText(t.label, {
      x: M, y, w: 3.4, h: 0.3, isTextBox: true, margin: 0,
      fontFace: FONT, fontSize: 13, bold: true, color: CHAR,
    });
    s.addText(t.pct + "%", {
      x: M, y: y + 0.3, w: 1.3, h: 0.4, isTextBox: true, margin: 0,
      fontFace: SERIF, fontSize: 22, bold: true, color: t.color,
    });
    progressBar(s, M + 3.5, y + 0.06, 6.3, t.pct, t.plan, t.color);
    s.addText(t.note, {
      x: M + 3.5, y: y + 0.34, w: 6.3, h: 0.35, isTextBox: true, margin: 0,
      fontFace: FONT, fontSize: 10.5, italic: true, color: MUTED,
    });
  });
  footnote(s, "Tidak ada milestone lapangan baru tercatat sejak 17 September — dua minggu terakhir fokus ke penyusunan dokumen sertifikasi ATEX. Detail: Laporan_Kesiapan_Meeting_Pertamina_29September2026.pdf.");
  s.addNotes("Sampaikan bahwa keempat jalur berjalan paralel, bukan berurutan. Instalasi permanen di lokasi non-ATEX (perimeter SRU) tidak perlu menunggu sertifikasi ATEX selesai.");
})();

// ================================================================ 4 · status sertifikasi ringkas
(function statusSertifikasi() {
  const s = slideLight();
  heading(s, "1 · Status", "Sertifikasi ATEX/IECEx — ringkas");

  card(s, M, 1.7, 5.85, 4.4, SURF);
  s.addText("Sudah maju", { x: M + 0.3, y: 1.9, w: 5.2, h: 0.35, isTextBox: true, margin: 0, fontFace: FONT, fontSize: 14.5, bold: true, color: OK });
  const done = [
    "Manufacturer resmi dikonfirmasi: PT Galaksi Megatama Indonesia (legalitas lengkap)",
    "Berat 2,378 kg, IP66, cable gland M20×1,5, suhu −20°C s/d +60°C, kelembapan 5–95% RH — status Final",
    "Formulir aplikasi resmi diterima dari lembaga sertifikasi GTS (Shanghai)",
    "Metode proteksi direkomendasikan tim: Ex d (flameproof enclosure)",
  ];
  done.forEach((t, i) => {
    s.addText("•  " + t, {
      x: M + 0.3, y: 2.35 + i * 0.75, w: 5.25, h: 0.7, isTextBox: true, margin: 0,
      fontFace: FONT, fontSize: 11.5, color: CHAR_SOFT, lineSpacing: 14,
    });
  });

  card(s, M + 6.15, 1.7, 6.0, 4.4, WARN_BG);
  s.addText("Penghambat utama", { x: M + 6.45, y: 1.9, w: 5.4, h: 0.35, isTextBox: true, margin: 0, fontFace: FONT, fontSize: 14.5, bold: true, color: WARN });
  const blockers = [
    "Kelas suhu T4 (≤135°C) belum diverifikasi — nol pengukuran hot-spot heater sensor MQ (~200–400°C)",
    "BOM & kalkulasi proteksi ledakan menunggu data desain final dari mitra casing",
    "Bagian 1 (legalitas lengkap PT Galaksi) masih sebagian",
  ];
  blockers.forEach((t, i) => {
    s.addText("•  " + t, {
      x: M + 6.45, y: 2.35 + i * 0.85, w: 5.4, h: 0.8, isTextBox: true, margin: 0,
      fontFace: FONT, fontSize: 11.5, color: CHAR_SOFT, lineSpacing: 14,
    });
  });
  footnote(s, "Sertifikasi berjalan paralel dengan persiapan instalasi — tidak menghambat instalasi di lokasi non-ATEX (perimeter SRU).");
  s.addNotes("Jangan overclaim: metode proteksi Ex d masih rekomendasi tim, belum keputusan ExCB. T4 adalah temuan paling kritis karena bisa memaksa perubahan desain, bukan cuma dokumen.");
})();

// ================================================================ 5 · status instalasi 3-track
(function statusInstalasi() {
  const s = slideLight();
  heading(s, "1 · Status", "Instalasi RU IV Cilacap");

  const rows = [
    ["Survey lokasi", "Selesai (9–10 Agustus 2026)", OK, OK_BG],
    ["Basis desain bracket mounting (CAD)", "Selesai — sudah diserahkan ke calon vendor", OK, OK_BG],
    ["Penugasan resmi vendor instalasi", "Belum — menunggu penunjukan Pertamina", "C0392B", "FCE7E4"],
    ["TRA/JSA spesifik titik pasang", "Belum disahkan — draft LGU tersedia sbg acuan awal", "C0392B", "FCE7E4"],
    ["Klasifikasi area tertulis resmi (perimeter SRU)", "Dalam proses — lokasi sudah pasti", HOLD, HOLD_BG],
    ["Orientasi bracket (vertikal/horizontal)", "Belum dikonfirmasi vendor", "C0392B", "FCE7E4"],
    ["Instalasi fisik & commissioning", "Belum dimulai", "C0392B", "FCE7E4"],
  ];
  const rowH = 0.5;
  rows.forEach((r, i) => {
    const y = 1.68 + i * rowH;
    if (i % 2 === 0) {
      s.addShape(pres.ShapeType.rect, { x: M, y, w: 12.1, h: rowH, fill: { color: SURF }, line: { color: SURF } });
    }
    s.addText(r[0], {
      x: M + 0.15, y, w: 6.6, h: rowH, isTextBox: true, margin: 0,
      fontFace: FONT, fontSize: 12, color: CHAR, valign: "middle",
    });
    chip(s, M + 6.9, y + (rowH - 0.27) / 2, r[1], r[2], r[3], 5.0);
  });
  s.addShape(pres.ShapeType.line, {
    x: M, y: 1.68, w: 0, h: rows.length * rowH, line: { color: "1ABB9C", width: 3 },
  });
  footnote(s, "Arah kerja yang sudah diputuskan: uji chamber gas di kantor kilang (non-area proses) + instalasi permanen di lokasi non-ATEX (perimeter SRU, dikonfirmasi Pertamina).");
  s.addNotes("3 item merah (vendor, TRA/JSA, orientasi bracket) adalah fokus keputusan slide berikutnya — ini yang paling menahan jadwal mobilisasi.");
})();

// ================================================================ 6 · yang harus disiapkan pertamina
(function pertaminaPrep() {
  const s = slideLight();
  heading(s, "2 · Pertamina RU IV", "Yang harus disiapkan");
  const rows = [
    ["P1", "Mengesahkan TRA/JSA spesifik titik pasang", "SIMOPS, listrik 24VDC, kerja tinggi, energize/commissioning"],
    ["P1", "Menerbitkan izin kerja (SIKA/PTW), izin masuk personel & barang", "Wajib sebelum mobilisasi"],
    ["P1", "Menugaskan resmi vendor instalasi", "Termasuk konfirmasi kompetensi HSE kerja di ketinggian"],
    ["P1", "Menerbitkan dokumen klasifikasi area tertulis resmi", "Untuk titik pasang di perimeter SRU"],
    ["P2", "Menyepakati daftar kontak PIC & jalur stop-work", "Operasi, HSE, control room, IT"],
    ["P2", "Penetapan titik pasang detail & akses struktur existing", "Rute kabel, tinggi kerja, akses"],
    ["P2", "Menyediakan kabel & PSU 24VDC ≥1A per unit", "Sampai ke titik pasang"],
    ["P3", "Menyepakati jadwal mobilisasi & fastener grade", "Bersama LGU & vendor"],
  ];
  const rowH = 0.58;
  rows.forEach((r, i) => {
    const y = 1.68 + i * rowH;
    if (i % 2 === 0) {
      s.addShape(pres.ShapeType.rect, { x: M, y, w: 12.1, h: rowH, fill: { color: PERTAMINA_BG }, line: { color: PERTAMINA_BG } });
    }
    prioTag(s, M + 0.15, y + (rowH - 0.27) / 2, r[0]);
    s.addText(r[1], {
      x: M + 0.85, y, w: 5.6, h: rowH, isTextBox: true, margin: 0,
      fontFace: FONT, fontSize: 11.5, bold: true, color: CHAR, valign: "middle", lineSpacing: 13,
    });
    s.addText(r[2], {
      x: M + 6.55, y, w: 5.4, h: rowH, isTextBox: true, margin: 0,
      fontFace: FONT, fontSize: 10.5, italic: true, color: CHAR_SOFT, valign: "middle", lineSpacing: 12,
    });
  });
  footnote(s, "Detail lengkap 5 kategori: Laporan_Kesiapan_Meeting_Pertamina_29September2026.pdf §4.");
  s.addNotes("Empat item P1 di atas adalah blocker keras untuk mobilisasi — tanpa vendor ditunjuk dan TRA/JSA disahkan, tanggal instalasi tidak bisa ditetapkan.");
})();

// ================================================================ 7 · yang harus disiapkan vendor
(function vendorPrep() {
  const s = slideLight();
  heading(s, "3 · Vendor Instalasi", "Yang harus disiapkan");
  const rows = [
    ["P1", "Personel bersertifikat kerja di ketinggian", "Sertifikasi HSE ketinggian — tanggung jawab vendor, bukan LGU"],
    ["P1", "Berpartisipasi dalam pengesahan TRA/JSA", "Sebagai pelaksana fisik"],
    ["P1", "Verifikasi lapangan & konfirmasi tertulis orientasi bracket", "Vertikal vs handrail horizontal — sebelum fabrikasi massal"],
    ["P1", "Tanpa pengelasan/pengeboran struktur permanen", "Kecuali disetujui tertulis RU IV"],
    ["P2", "Fabrikasi bracket L+U-bolt sesuai basis desain LGU", "2\"/DN50, plat 250×250mm — menunggu shop drawing"],
    ["P2", "Verifikasi pra-mobilisasi unit GLD & jalur kabel", "3 unit + 1 cadangan, serial number, firmware"],
    ["P2", "Menunjuk supervisor lapangan", "Jalur komunikasi ke QA LGU & PIC HSE RU IV"],
    ["P3", "Menyepakati jadwal mobilisasi & rencana rollback", "Bersama RU IV dan LGU"],
  ];
  const rowH = 0.58;
  rows.forEach((r, i) => {
    const y = 1.68 + i * rowH;
    if (i % 2 === 0) {
      s.addShape(pres.ShapeType.rect, { x: M, y, w: 12.1, h: rowH, fill: { color: VENDOR_BG }, line: { color: VENDOR_BG } });
    }
    prioTag(s, M + 0.15, y + (rowH - 0.27) / 2, r[0]);
    s.addText(r[1], {
      x: M + 0.85, y, w: 5.6, h: rowH, isTextBox: true, margin: 0,
      fontFace: FONT, fontSize: 11.5, bold: true, color: CHAR, valign: "middle", lineSpacing: 13,
    });
    s.addText(r[2], {
      x: M + 6.55, y, w: 5.4, h: rowH, isTextBox: true, margin: 0,
      fontFace: FONT, fontSize: 10.5, italic: true, color: CHAR_SOFT, valign: "middle", lineSpacing: 12,
    });
  });
  footnote(s, "Detail lengkap 6 kategori: Laporan_Kesiapan_Meeting_Pertamina_29September2026.pdf §5 & Daftar_Persiapan_Vendor_Instalasi_RU-IV_Cilacap.pdf.");
  s.addNotes("Tegaskan prinsip pembagian kerja: vendor eksekusi fisik + HSE ketinggian, LGU supervisi teknis/QA + elektrikal spesifik GLD.");
})();

// ================================================================ 8 · keputusan diminta
(function keputusan() {
  const s = slideDark();
  heading(s, "4 · Keputusan", "Yang diambil hari ini");
  s.getSlide ? null : null;
  // override heading color for dark bg
  s.addText("KEPUTUSAN", {
    x: M, y: 0.46, w: 10.5, h: 0.26, isTextBox: true, margin: 0,
    fontFace: FONT, fontSize: 11, bold: true, charSpacing: 1.6, color: "7FE0C8",
  });
  s.addText("Yang diambil hari ini", {
    x: M, y: 0.74, w: 11.9, h: 0.66, isTextBox: true, margin: 0,
    fontFace: SERIF, fontSize: 29, bold: true, color: WHITE, valign: "top",
  });

  const decisions = [
    "Penunjukan resmi vendor instalasi + konfirmasi kompetensi HSE kerja di ketinggian",
    "Jadwal pengesahan TRA/JSA — PIC review dari RU IV/HSE dan target tanggal",
    "Konfirmasi tertulis klasifikasi area untuk titik pasang di perimeter SRU",
    "Target tanggal mobilisasi & instalasi permanen",
  ];
  decisions.forEach((t, i) => {
    const y = 1.75 + i * 1.1;
    badge(s, M, y, i + 1, 0.5, "1ABB9C");
    s.addText(t, {
      x: M + 0.75, y: y - 0.05, w: 11.0, h: 0.9, isTextBox: true, margin: 0,
      fontFace: FONT, fontSize: 16, bold: true, color: WHITE, valign: "top", lineSpacing: 20,
    });
  });
  s.addNotes("Ini adalah output konkret yang harus dibawa keluar dari rapat ini. Jangan tutup rapat tanpa jawaban/tanggal untuk keempatnya, sekalipun jawabannya 'perlu waktu N hari'.");
})();

// ================================================================ 9 · penutup / kontak
(function penutup() {
  const s = slideLight();
  heading(s, "Penutup", "Terima kasih");
  card(s, M, 1.8, 12.1, 3.2, SURF);
  s.addText("Dokumen pendukung lengkap (9 file, pdf+html) telah dibagikan sebelum rapat:", {
    x: M + 0.35, y: 2.1, w: 11.4, h: 0.4, isTextBox: true, margin: 0,
    fontFace: FONT, fontSize: 13.5, bold: true, color: CHAR,
  });
  const links = [
    "Laporan_Kesiapan_Meeting_Pertamina_29September2026.pdf (dokumen utama)",
    "Dashboard_GLD_ProjectManagement.pdf, Dashboard_Sertifikasi_GLD_ATEX_IECEx.pdf",
    "Checklist_Kesiapan_Instalasi_RU-IV_Cilacap.pdf, Pembagian_Persiapan_Instalasi_RU-IV_Cilacap.pdf",
    "Daftar_Persiapan_Vendor_Instalasi_RU-IV_Cilacap.pdf, Draf_Permintaan_Penyediaan_Material...pdf",
  ];
  links.forEach((t, i) => {
    s.addText("•  " + t, {
      x: M + 0.35, y: 2.6 + i * 0.42, w: 11.2, h: 0.4, isTextBox: true, margin: 0,
      fontFace: FONT, fontSize: 11.5, color: CHAR_SOFT,
    });
  });
  s.addText("PT LAPI Ganesha Utama & Lab IoT/Fisika ITB — Jl. Dederuk No. 30, Bandung 40133", {
    x: M, y: 5.4, w: 10, h: 0.3, isTextBox: true, margin: 0,
    fontFace: FONT, fontSize: 11, color: MUTED,
  });
  s.addNotes("Tutup dengan menegaskan kembali 4 keputusan dan siapa PIC masing-masing tindak lanjut.");
})();

pres.writeFile({ fileName: OUT }).then(() => console.log("written", OUT));
