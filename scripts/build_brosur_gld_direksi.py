# -*- coding: utf-8 -*-
"""Brosur produk GLD 4 halaman A4 untuk audiens umum (cetak kertas katalog).

Hierarki merek mengikuti arahan Pertamina (WA 4 Nov 2026): Pertamina Patra Niaga /
Pertamina Patra Niaga + produk GLD menonjol; LGU & Kinarya ITB hanya logo kecil.
Data teknis mengacu TDS R4.0 & hasil uji lab; materi umum (tanpa rujukan lokasi/MoC).

Run:  python3 scripts/build_brosur_gld_direksi.py
Out:  Deliverables/Brosur_GLD_A4_4Halaman.html  + .pdf (Chromium/Playwright)
"""
import base64
import io
import os

from PIL import Image

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_HTML = os.path.join(REPO, "Deliverables", "Brosur_GLD_A4_4Halaman.html")
OUT_PDF = os.path.join(REPO, "Deliverables", "Brosur_GLD_A4_4Halaman.pdf")


def img(rel, box=None, maxw=1400, fmt="JPEG"):
    im = Image.open(os.path.join(REPO, rel))
    if fmt == "JPEG":
        im = im.convert("RGB")
    if box:
        w, h = im.size
        im = im.crop((int(box[0] * w), int(box[1] * h), int(box[2] * w), int(box[3] * h)))
    if im.width > maxw:
        im = im.resize((maxw, int(im.height * maxw / im.width)), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, fmt, quality=90) if fmt == "JPEG" else im.save(buf, fmt)
    mime = "image/jpeg" if fmt == "JPEG" else "image/png"
    return f"data:{mime};base64,{base64.b64encode(buf.getvalue()).decode()}"


L_PPN = img("Sumber Dokumen/Logo/Logo_Pertamina_Patra_Niaga.png", fmt="PNG")
L_KIN = img("Sumber Dokumen/Logo/Logo_Korporasi_Kinarya_ITB.png", fmt="PNG")
L_LGU = img("Sumber Dokumen/Logo/Logo_LAPI_Ganesha_Utama.png", fmt="PNG")
P_GLD = img("scripts/assets/cert_doc_photos/3._Motherboard_ModulSensor_PenutupMesh_Casing_Antena_ModulAlarm.jpg",
            box=(0.02, 0.02, 0.98, 0.98))
P_MESH = img("scripts/assets/cert_doc_photos/PenutupMesh_Casing.jpg", box=(0.05, 0.25, 0.95, 0.75))
P_CHAMBER = img("scripts/assets/chamber_photos/chamber_gld_terpasang.jpeg", box=(0.05, 0.02, 0.95, 0.98))
P_CH = img("scripts/assets/ch_mount_photos/ch_bracket_solar_detail.jpg", box=(0.08, 0.12, 0.92, 0.70), maxw=1000)
P_DASH = img("Deliverables/Video_Produk_GLD_Remotion/public/images/dashboard.png", maxw=1600, fmt="PNG")

ARCH_SVG = """
<svg style="width:100%;height:auto;max-height:52mm" viewBox="0 0 760 210" xmlns="http://www.w3.org/2000/svg" font-family="Inter, sans-serif">
  <defs><marker id="ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">
    <path d="M0,0 L10,5 L0,10 z" fill="#12357A"/></marker></defs>
  <g font-size="11.5">
    <rect x="4" y="40" width="130" height="96" rx="10" fill="#E8EEF9" stroke="#12357A"/>
    <text x="69" y="62" text-anchor="middle" font-weight="700" fill="#12357A" font-size="13">GLD</text>
    <text x="69" y="80" text-anchor="middle" fill="#262321">8 sensor gas</text>
    <text x="69" y="96" text-anchor="middle" fill="#262321">AI di ESP32-S3</text>
    <text x="69" y="112" text-anchor="middle" fill="#262321">Catu 24 VDC</text>
    <text x="69" y="128" text-anchor="middle" fill="#6B6B6B" font-size="10">Area proses</text>

    <line x1="136" y1="88" x2="186" y2="88" stroke="#12357A" stroke-width="2" marker-end="url(#ar)"/>
    <text x="161" y="78" text-anchor="middle" fill="#E3242B" font-size="10" font-weight="700">LoRa STAR</text>
    <text x="161" y="104" text-anchor="middle" fill="#6B6B6B" font-size="9.5">920 MHz</text>

    <rect x="190" y="40" width="130" height="96" rx="10" fill="#E8EEF9" stroke="#12357A"/>
    <text x="255" y="62" text-anchor="middle" font-weight="700" fill="#12357A" font-size="13">Cluster Head</text>
    <text x="255" y="80" text-anchor="middle" fill="#262321">Agregator nirkabel</text>
    <text x="255" y="96" text-anchor="middle" fill="#262321">Panel surya</text>
    <text x="255" y="112" text-anchor="middle" fill="#262321">Failover otomatis</text>
    <text x="255" y="128" text-anchor="middle" fill="#6B6B6B" font-size="10">Pagar unit</text>

    <line x1="322" y1="88" x2="372" y2="88" stroke="#12357A" stroke-width="2" marker-end="url(#ar)"/>
    <text x="347" y="78" text-anchor="middle" fill="#E3242B" font-size="10" font-weight="700">LoRa MESH</text>
    <text x="347" y="104" text-anchor="middle" fill="#6B6B6B" font-size="9.5">921 MHz</text>

    <rect x="376" y="40" width="130" height="96" rx="10" fill="#E8EEF9" stroke="#12357A"/>
    <text x="441" y="62" text-anchor="middle" font-weight="700" fill="#12357A" font-size="13">Gateway</text>
    <text x="441" y="80" text-anchor="middle" fill="#262321">Root jaringan mesh</text>
    <text x="441" y="96" text-anchor="middle" fill="#262321">Antena omni 8 dBi</text>
    <text x="441" y="112" text-anchor="middle" fill="#262321">Didukung UPS</text>
    <text x="441" y="128" text-anchor="middle" fill="#6B6B6B" font-size="10">Ruang kontrol</text>

    <line x1="508" y1="88" x2="558" y2="88" stroke="#12357A" stroke-width="2" marker-end="url(#ar)"/>
    <text x="533" y="78" text-anchor="middle" fill="#E3242B" font-size="10" font-weight="700">MQTT</text>
    <text x="533" y="104" text-anchor="middle" fill="#6B6B6B" font-size="9.5">lokal</text>

    <rect x="562" y="40" width="194" height="96" rx="10" fill="#12357A"/>
    <text x="659" y="62" text-anchor="middle" font-weight="700" fill="#fff" font-size="13">Server &amp; Dashboard</text>
    <text x="659" y="80" text-anchor="middle" fill="#fff">Validasi data AES-128-GCM</text>
    <text x="659" y="96" text-anchor="middle" fill="#fff">Riwayat &amp; alarm advisory</text>
    <text x="659" y="112" text-anchor="middle" fill="#fff">Akses ruang kontrol &amp; intranet</text>
    <text x="659" y="128" text-anchor="middle" fill="#C9D6F2" font-size="10">Tanpa koneksi internet</text>
  </g>
  <g font-size="10.5" fill="#262321">
    <rect x="4" y="160" width="752" height="40" rx="8" fill="#F4F6FA"/>
    <text x="16" y="185"><tspan font-weight="700" fill="#12357A">Standalone:</tspan> tidak terhubung ke panel F&amp;G maupun DCS eksisting — tidak ada perubahan wiring, logic alarm, trip atau interlock.</text>
  </g>
</svg>
"""

PIPE = [
    ("1", "Sampling udara", "Kipas DC aktif menarik udara melalui filter stainless wire mesh"),
    ("2", "Akuisisi 8 kanal", "ADC 24-bit ADS1256, pemindaian seluruh sensor setiap 500 ms"),
    ("3", "Pengolahan sinyal", "Kalibrasi otomatis &amp; moving average 10 sampel per kanal"),
    ("4", "Inferensi AI", "Klasifikasi jenis gas + nilai confidence langsung di perangkat"),
    ("5", "Pelaporan", "Data &amp; alarm dikirim terenkripsi; laporan berkala tiap 10 detik"),
]

SENSORS = [
    ("MQ-8", "Hidrogen (H₂)"), ("MQ-135", "Kualitas udara (NH₃, benzena, asap)"),
    ("MQ-3", "Alkohol / etanol"), ("MQ-5", "LPG, gas alam"),
    ("MQ-4", "Metana (CH₄), CNG"), ("MQ-7", "Karbon monoksida (CO)"),
    ("MQ-6", "LPG, butana, propana"), ("MQ-2", "Gas mudah terbakar umum"),
]

SPEC_GLD = [
    ("Sensor gas", "8 kanal seri MQ (Winsen)"),
    ("Sensor lingkungan", "Sensirion SHT40 (suhu &amp; kelembapan)"),
    ("Akuisisi", "ADC 24-bit ADS1256, siklus 500 ms"),
    ("Prosesor", "ESP32-S3 — kontrol, komunikasi &amp; inferensi lokal"),
    ("Keluaran AI", "Label jenis gas + confidence; waktu inferensi &lt;166 ms"),
    ("Kelas model R4.0", "Clean Air, LPG, H₂"),
    ("Komunikasi", "LoRa STAR 920–923 MHz, AES-128-GCM, anti-replay"),
    ("Antarmuka lokal", "RS-485 Modbus RTU (read-only)"),
    ("Catu daya", "24 VDC hardwired; maks. terukur 7,995 W (±0,33 A)"),
    ("Keluaran alarm", "1 keluaran 24 V untuk buzzer/LED eksternal"),
    ("Housing", "Aluminium die-cast, mesh stainless, IP66 (target)"),
    ("Entry kabel", "Cable gland M20 × 1,5"),
    ("Pemasangan", "Pelat 250 × 250 mm + 2 U-bolt pada tiang 2\""),
]

SPEC_CH = [
    ("Fungsi", "Agregator LoRa STAR → penerus LoRa MESH multi-hop"),
    ("Radio", "2 × E22-900MM22S; antena 3 dBi &amp; 8 dBi"),
    ("Daya", "2 panel surya 6 W + baterai 18650; tanpa kabel"),
    ("Routing", "Parent dinamis, failover otomatis"),
]
SPEC_GW = [
    ("Fungsi", "Root jaringan mesh, jembatan ke jaringan IP"),
    ("Antena", "Omni 8 dBi di atap, koaksial LMR-400 ≤15 m + arrester"),
    ("Uplink", "Wi-Fi 2,4 GHz ke router lokal"),
    ("Daya", "220 VAC melalui adaptor, didukung UPS"),
]
SPEC_SRV = [
    ("Perangkat", "PC fisik 4 core / 8 GB / SSD 256 GB, 2 port LAN"),
    ("Aplikasi", "MQTT broker, Node-RED, basis data, dashboard web"),
    ("Jaringan", "LAN-1 ke jaringan GLD; LAN-2 ke intranet hanya untuk dashboard"),
]

ROLLOUT = [("RU II", 10, 3, 1), ("RU III", 4, 3, 1), ("RU IV", 3, 2, 1),
           ("RU V", 2, 1, 1), ("RU VI", 4, 2, 2), ("RU VII", 5, 11, 1)]


def rows(data):
    return "".join(f"<tr><th>{k}</th><td>{v}</td></tr>" for k, v in data)


def header(n, title):
    return f"""<div class="phead"><img src="{L_PPN}" class="ppn-s" alt="Pertamina Patra Niaga">
<div class="phead-r"><span>GLD · Multi-Modality Gas Leak Detector</span><b>{n}</b></div></div>
<h2>{title}</h2>"""


def footer():
    return f"""<div class="pfoot"><span>PT Pertamina Patra Niaga</span>
<span class="collab">Dikembangkan bersama <img src="{L_KIN}" alt="Kinarya ITB"><img src="{L_LGU}" alt="LGU"></span></div>"""


rollout_rows = "".join(f"<tr><td>{r}</td><td>{g}</td><td>{c}</td><td>{w}</td></tr>" for r, g, c, w in ROLLOUT)
tot = [sum(x[i] for x in ROLLOUT) for i in (1, 2, 3)]

HTML = f"""<!doctype html><html lang="id"><head><meta charset="utf-8">
<title>Brosur GLD</title>
<style>
@page {{ size: A4; margin: 0; }}
:root {{ --navy:#12357A; --blue:#2B5FCB; --red:#E3242B; --green:#8DC63F; --ink:#262321; --mute:#5E6470; --line:#D9DFEA; --soft:#F4F6FA; }}
* {{ box-sizing:border-box; margin:0; padding:0; }}
html,body {{ background:#fff; }}
body {{ font-family: Inter, "Liberation Sans", sans-serif; color:var(--ink); font-size:9.2pt; line-height:1.38;
  -webkit-print-color-adjust:exact; print-color-adjust:exact; }}
.page {{ width:210mm; height:297mm; position:relative; overflow:hidden; padding:13mm 14mm 0; page-break-after:always; }}
.page:last-child {{ page-break-after:auto; }}
h2 {{ font-size:17pt; color:var(--navy); letter-spacing:-.01em; margin:4mm 0 2.5mm; }}
h3 {{ font-size:11pt; color:var(--navy); margin:4mm 0 2mm; }}
p {{ margin-bottom:2mm; }}
.phead {{ display:flex; align-items:center; justify-content:space-between; border-bottom:2px solid var(--navy); padding-bottom:2.5mm; }}
.ppn-s {{ height:13mm; }}
.phead-r {{ display:flex; align-items:center; gap:4mm; font-size:8.5pt; color:var(--mute); }}
.phead-r b {{ background:var(--navy); color:#fff; width:7mm; height:7mm; border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:9pt; }}
.pfoot {{ position:absolute; left:14mm; right:14mm; bottom:8mm; display:flex; justify-content:space-between; align-items:center;
  font-size:7.5pt; color:var(--mute); border-top:1px solid var(--line); padding-top:2mm; }}
.collab {{ display:flex; align-items:center; gap:2.5mm; }}
.collab img {{ height:7mm; }}
.stripe {{ position:absolute; left:0; right:0; height:3mm; bottom:0; background:linear-gradient(90deg,var(--navy) 0 60%,var(--red) 60% 80%,var(--green) 80%); }}

/* cover */
.cover {{ padding:0; background:#fff; }}
.cv-top {{ padding:12mm 14mm 0; display:flex; justify-content:space-between; align-items:flex-start; }}
.cv-top img {{ height:24mm; }}
.cv-top .unit {{ text-align:right; font-size:9pt; color:var(--navy); font-weight:600; line-height:1.5; padding-top:3mm; }}
.cv-hero {{ position:absolute; top:52mm; left:0; right:0; height:150mm; background:linear-gradient(135deg,#0E2A63 0%,#12357A 55%,#1E4FB3 100%); overflow:hidden; }}
.cv-hero::before {{ content:""; position:absolute; right:-40mm; top:-30mm; width:160mm; height:160mm; border-radius:50%; background:rgba(255,255,255,.05); }}
.cv-hero::after {{ content:""; position:absolute; left:0; bottom:0; width:100%; height:24mm; background:linear-gradient(170deg,transparent 0 45%,rgba(227,36,43,.9) 45% 60%,rgba(141,198,63,.9) 60%); opacity:.9; }}
.cv-txt {{ position:absolute; left:14mm; top:16mm; width:100mm; color:#fff; z-index:2; }}
.eyebrow {{ font-size:8.5pt; letter-spacing:.14em; text-transform:uppercase; color:#BFD0F5; font-weight:600; }}
.cv-txt h1 {{ font-size:66pt; line-height:1; font-weight:800; margin:4mm 0 1mm; letter-spacing:-.02em; }}
.cv-txt .sub {{ font-size:17pt; font-weight:600; line-height:1.2; margin-bottom:5mm; }}
.cv-txt .lead {{ font-size:10.5pt; color:#E3EAFA; line-height:1.5; }}
.cv-photo {{ position:absolute; right:12mm; top:10mm; width:72mm; height:118mm; border-radius:6mm; background:#fff; padding:3mm; z-index:2; box-shadow:0 6mm 14mm rgba(0,0,0,.35); }}
.cv-photo img {{ width:100%; height:100%; object-fit:cover; border-radius:4mm; }}
.kpis {{ position:absolute; top:210mm; left:14mm; right:14mm; display:grid; grid-template-columns:repeat(4,1fr); gap:3mm; }}
.kpi {{ border:1px solid var(--line); border-top:3px solid var(--navy); border-radius:2mm; padding:3mm; }}
.kpi b {{ display:block; font-size:16pt; color:var(--navy); line-height:1.1; }}
.kpi span {{ font-size:8.3pt; color:var(--mute); }}
.cv-note {{ position:absolute; top:247mm; left:14mm; right:14mm; font-size:9pt; color:var(--ink); background:var(--soft); border-left:3px solid var(--red); padding:3mm 4mm; }}

/* content */
.two {{ display:grid; grid-template-columns:1fr 1fr; gap:6mm; }}
.lead2 {{ font-size:10.5pt; color:var(--ink); }}
table.cmp, table.spec, table.ro {{ width:100%; border-collapse:collapse; font-size:8.5pt; }}
table.cmp th, table.cmp td {{ border-bottom:1px solid var(--line); padding:1.1mm 2mm; text-align:left; vertical-align:top; }}
table.cmp thead th {{ background:var(--navy); color:#fff; font-weight:600; }}
table.cmp thead th:last-child {{ background:var(--blue); }}
table.cmp tbody th {{ color:var(--navy); width:24%; font-weight:600; }}
table.spec th {{ width:33%; text-align:left; color:var(--navy); font-weight:600; padding:1mm 2mm; border-bottom:1px solid var(--line); vertical-align:top; }}
table.spec td {{ padding:1mm 2mm; border-bottom:1px solid var(--line); }}
table.spec tr:nth-child(even) td, table.spec tr:nth-child(even) th {{ background:var(--soft); }}
.pipe {{ display:grid; grid-template-columns:repeat(5,1fr); gap:2.5mm; }}
.pipe div {{ background:var(--soft); border-radius:2mm; padding:2.2mm; border-top:3px solid var(--blue); }}
.pipe b {{ display:block; color:var(--navy); font-size:9pt; margin-bottom:1mm; }}
.pipe i {{ font-style:normal; display:inline-block; background:var(--navy); color:#fff; width:5mm; height:5mm; border-radius:50%; text-align:center; line-height:5mm; font-size:7.5pt; margin-bottom:1.5mm; }}
.pipe span {{ font-size:8pt; color:var(--mute); }}
.sens {{ display:grid; grid-template-columns:repeat(4,1fr); gap:2mm; }}
.sens div {{ border:1px solid var(--line); border-radius:2mm; padding:1.3mm 2mm; font-size:7.8pt; }}
.sens b {{ color:var(--red); display:block; font-size:9pt; }}
.fig {{ border-radius:3mm; overflow:hidden; border:1px solid var(--line); background:#fff; }}
.fig img {{ width:100%; display:block; object-fit:cover; }}
.cap {{ font-size:7.6pt; color:var(--mute); padding:1.5mm 2mm; }}
.card {{ border:1px solid var(--line); border-radius:3mm; padding:3.5mm; }}
.card h4 {{ font-size:9.5pt; color:var(--navy); margin-bottom:1.5mm; }}
.tag {{ display:inline-block; font-size:7.5pt; font-weight:700; padding:.6mm 2mm; border-radius:10mm; }}
.t-ok {{ background:#E6F4EA; color:#1E7B34; }} .t-run {{ background:#FFF3DC; color:#9A6100; }}
ul.chk {{ list-style:none; }}
ul.chk li {{ padding-left:5mm; position:relative; margin-bottom:1.3mm; font-size:8.8pt; }}
ul.chk li::before {{ content:""; position:absolute; left:0; top:1.6mm; width:2.2mm; height:2.2mm; border-radius:50%; background:var(--blue); }}
table.ro th, table.ro td {{ padding:1.3mm 2mm; border-bottom:1px solid var(--line); text-align:center; }}
table.ro th {{ background:var(--navy); color:#fff; font-weight:600; }}
table.ro td:first-child {{ text-align:left; font-weight:600; color:var(--navy); }}
table.ro tr.hl td {{ background:#E8EEF9; }}
table.ro tr.tot td {{ font-weight:700; border-top:2px solid var(--navy); }}
.flow {{ display:flex; gap:2mm; align-items:stretch; }}
.flow div {{ flex:1; background:var(--soft); border-radius:2mm; padding:2.5mm; font-size:8pt; text-align:center; }}
.flow b {{ display:block; color:var(--navy); font-size:8.8pt; }}
</style></head><body>

<!-- ============ HALAMAN 1 : COVER ============ -->
<section class="page cover">
  <div class="cv-top"><img src="{L_PPN}" alt="Pertamina Patra Niaga">
    <div class="unit">Teknologi Deteksi Kebocoran Gas<br><span style="font-weight:400;color:var(--mute)">Berbasis AI &amp; IoT</span></div></div>
  <div class="cv-hero">
    <div class="cv-txt">
      <div class="eyebrow">Multi-Modality · AI on the Edge · LoRa Mesh</div>
      <h1>GLD</h1>
      <div class="sub">Multi-Modality<br>Gas Leak Detector</div>
      <div class="lead">Sistem deteksi kebocoran gas yang menggabungkan delapan sensor dalam satu unit,
      mengklasifikasikan jenis gas langsung di perangkat dengan kecerdasan buatan, dan mengirimkan
      hasilnya secara nirkabel ke dashboard pemantauan kilang secara real-time.</div>
    </div>
    <div class="cv-photo"><img src="{P_GLD}" alt="Unit GLD"></div>
  </div>
  <div class="kpis">
    <div class="kpi"><b>8</b><span>sensor gas dalam satu unit</span></div>
    <div class="kpi"><b>&lt;166 ms</b><span>inferensi AI langsung di perangkat</span></div>
    <div class="kpi"><b>99,31%</b><span>akurasi model pada data validasi laboratorium</span></div>
    <div class="kpi"><b>LoRa Mesh</b><span>920–923 MHz, terenkripsi AES-128</span></div>
  </div>
  <div class="cv-note"><b style="color:var(--navy)">Pelengkap sistem yang sudah ada.</b> GLD menambah informasi klasifikasi jenis gas
  sebagai lapisan pemantauan <i>advisory</i>, berjalan mandiri tanpa mengubah alarm, logic trip maupun interlock sistem F&amp;G dan DCS.</div>
  <div class="pfoot" style="bottom:8mm"><span>Dokumen informasi produk · November 2026</span>
    <span class="collab">Dikembangkan bersama <img src="{L_KIN}" alt="Kinarya ITB"><img src="{L_LGU}" alt="LGU"></span></div>
  <div class="stripe"></div>
</section>

<!-- ============ HALAMAN 2 : MENGAPA & CARA KERJA ============ -->
<section class="page">
  {header(2, "Mengapa GLD")}
  <p class="lead2">Kebocoran gas mudah terbakar dan beracun adalah salah satu risiko terbesar di fasilitas migas. Detektor gas konvensional umumnya bekerja dengan satu jenis sensor untuk satu jenis gas. Hasilnya berupa
  nilai konsentrasi, tetapi tidak menunjukkan <b>gas apa</b> yang sedang bocor. GLD membaca pola respons delapan sensor
  sekaligus, lalu model kecerdasan buatan di dalam perangkat menentukan jenis gasnya.</p>
  <table class="cmp" style="margin-top:3mm">
    <thead><tr><th>Aspek</th><th>Detektor konvensional</th><th>GLD Multi-Modality</th></tr></thead>
    <tbody>
      <tr><th>Jenis sensor</th><td>Industrial grade, satu modalitas per detektor (infrared untuk HC, elektrokimia untuk H₂S)</td><td>Larik 8 sensor semikonduktor dalam satu unit</td></tr>
      <tr><th>Keluaran</th><td>Nilai konsentrasi (%LEL / ppm), 4–20 mA</td><td>Label jenis gas beserta nilai confidence</td></tr>
      <tr><th>Infrastruktur data</th><td>Hardwired ke marshalling / panel F&amp;G</td><td>Catu 24 VDC; data nirkabel LoRa ke Gateway</td></tr>
      <tr><th>Peran</th><td>Lapisan proteksi utama</td><td>Lapisan pemantauan tambahan (advisory)</td></tr>
    </tbody>
  </table>

  <h2 style="margin-top:5mm">Cara Kerja</h2>
  <div class="pipe">{''.join(f'<div><i>{n}</i><b>{t}</b><span>{d}</span></div>' for n, t, d in PIPE)}</div>

  <h3 style="margin-top:4mm">Arsitektur sistem</h3>
  {ARCH_SVG}

  <h3 style="margin-top:3mm">Delapan sensor, satu sidik jari gas <span style="font-weight:400;font-size:7.6pt;color:var(--mute)">— sensitivitas umum menurut pabrikan sensor</span></h3>
  <div class="sens">{''.join(f'<div><b>{s}</b>{g}</div>' for s, g in SENSORS)}</div>
  {footer()}
</section>

<!-- ============ HALAMAN 3 : SPESIFIKASI ============ -->
<section class="page">
  {header(3, "Spesifikasi Teknis")}
  <div class="two" style="grid-template-columns:1.45fr 1fr">
    <div>
      <h3 style="margin-top:0">Gas Leak Detector (node sensor)</h3>
      <table class="spec">{rows(SPEC_GLD)}</table>
    </div>
    <div>
      <div class="fig"><img src="{P_GLD}" style="height:62mm" alt="GLD"><div class="cap">Unit GLD: housing aluminium, mesh stainless, beacon alarm &amp; antena LoRa</div></div>
      <div class="fig" style="margin-top:3mm"><img src="{P_MESH}" style="height:26mm" alt="Mesh"><div class="cap">Bukaan sensor dengan filter stainless wire mesh</div></div>
    </div>
  </div>
  <div class="two" style="margin-top:4mm;grid-template-columns:1fr 1fr 1fr;gap:4mm">
    <div><h3>Cluster Head</h3><table class="spec">{rows(SPEC_CH)}</table></div>
    <div><h3>Gateway</h3><table class="spec">{rows(SPEC_GW)}</table></div>
    <div><h3>Server lokal</h3><table class="spec">{rows(SPEC_SRV)}</table></div>
  </div>
  <div class="two" style="margin-top:4mm;grid-template-columns:1fr 2fr;gap:4mm">
    <div class="fig"><img src="{P_CH}" style="height:34mm" alt="Cluster Head"><div class="cap">Cluster Head bertenaga surya</div></div>
    <div class="card">
      <h4>Keamanan &amp; keandalan</h4>
      <ul class="chk">
        <li>Payload terenkripsi dan terautentikasi AES-128-GCM, dengan proteksi anti-replay di server.</li>
        <li>Jaringan GLD terpisah tanpa akses internet; server tidak meneruskan lalu lintas antar jaringan.</li>
        <li>Jalur alternatif otomatis bila salah satu Cluster Head tidak berfungsi.</li>
        <li>Gateway, router dan server didukung UPS agar data dan alarm tetap tercatat.</li>
      </ul>
    </div>
  </div>
  {footer()}
</section>

<!-- ============ HALAMAN 4 : STATUS & RENCANA ============ -->
<section class="page">
  {header(4, "Status &amp; Rencana Pengembangan")}
  <div class="two" style="grid-template-columns:1.25fr 1fr">
    <div>
      <div class="card">
        <h4>Siap diuji di lapangan <span class="tag t-run">Tahap berikutnya</span></h4>
        <p style="font-size:8.8pt">Setelah pengujian laboratorium, sistem memasuki tahap field testing di lingkungan kilang
        sebagai lapisan pemantauan tambahan, berdampingan dengan sistem deteksi gas yang sudah terpasang.</p>
      </div>
      <div class="card" style="margin-top:3mm">
        <h4>Hasil pengujian laboratorium <span class="tag t-ok">Selesai</span></h4>
        <ul class="chk">
          <li>Rantai GLD – Cluster Head – Gateway – Server berjalan end-to-end.</li>
          <li>Akurasi model 99,31% pada data validasi laboratorium (kelas Clean Air, LPG, H₂).</li>
          <li>Jaringan mesh diuji dengan 8 Cluster Head bertingkat hingga 3 lompatan.</li>
          <li>Alarm terkirim otomatis ke server tanpa permintaan (push alarm).</li>
          <li>Komunikasi stabil saat diuji dengan gangguan sinyal kanal yang sama (uji awal).</li>
          <li>Factory Acceptance Test laboratorium: 7 dari 7 butir uji lulus.</li>
          <li>Pre-scan emisi EMC (EN 55032) telah dilakukan.</li>
        </ul>
      </div>
      <div class="card" style="margin-top:3mm">
        <h4>Sertifikasi <span class="tag t-run">Dalam proses</span></h4>
        <p style="font-size:8.8pt">ATEX/IECEx dengan usulan skema II 2G Ex db IIC T4 Gb, perlindungan IP66/67,
        EMC EN 61000-6-2/-4, serta perangkat radio sesuai ketentuan SDPPI.</p>
      </div>
    </div>
    <div>
      <div class="fig"><img src="{P_CHAMBER}" style="height:62mm" alt="Chamber uji gas"><div class="cap">Chamber uji gas portabel untuk pengambilan dataset di lokasi</div></div>
      <h3>Model AI yang dilatih di tiap kilang</h3>
      <div class="flow">
        <div><b>1</b>Chamber dibawa ke kilang</div>
        <div><b>2</b>Ambil dataset gas setempat</div>
        <div><b>3</b>Latih model</div>
        <div><b>4</b>Pasang ke firmware GLD</div>
      </div>
      <p style="font-size:8.3pt;margin-top:2mm">Gas target pengembangan berikutnya, seperti H₂S, hidrokarbon C4–C5+, metana, CO dan benzena,
      ditambahkan melalui pengumpulan dataset dan pelatihan lanjutan sesuai kebutuhan tiap unit.</p>
    </div>
  </div>
  <div class="two" style="margin-top:4mm;grid-template-columns:1fr 1.35fr;gap:5mm">
    <div>
      <h3 style="margin-top:0">Rencana penerapan 6 Refinery Unit</h3>
      <table class="ro"><tr><th>Unit</th><th>GLD</th><th>Cluster Head</th><th>Gateway</th></tr>
      {rollout_rows.replace('<tr><td>RU IV', '<tr class="hl"><td>RU IV')}
      <tr class="tot"><td>Total</td><td>{tot[0]}</td><td>{tot[1]}</td><td>{tot[2]}</td></tr></table>
    </div>
    <div>
      <div class="fig"><img src="{P_DASH}" style="height:52mm;object-position:left top" alt="Dashboard"><div class="cap">Dashboard pemantauan: status perangkat, konsol alarm dan riwayat deteksi</div></div>
    </div>
  </div>
  {footer()}
</section>
</body></html>"""

with open(OUT_HTML, "w", encoding="utf-8") as f:
    f.write(HTML)
print(OUT_HTML)

import subprocess  # noqa: E402
subprocess.run(["google-chrome", "--headless", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer",
                f"--print-to-pdf={OUT_PDF}", "file://" + OUT_HTML], check=True, capture_output=True)
print(OUT_PDF)
