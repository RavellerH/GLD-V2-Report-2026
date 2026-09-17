# -*- coding: utf-8 -*-
import base64, os, re

REPO = r"C:\Users\WIN10\Documents\GLD-V2-Report-2026"
PHOTO_DIR = os.path.join(REPO, ".tmp", "cert_doc_photos")
OUT_PATH = os.path.join(REPO, "Deliverables", "Dokumen_Teknis_Sertifikasi_GLD_IECEx_ATEX.html")
STYLE_SOURCE = os.path.join(REPO, "Deliverables", "Dashboard_Sertifikasi_GLD_ATEX_IECEx.html")

def b64(fn):
    with open(os.path.join(PHOTO_DIR, fn), "rb") as f:
        return base64.b64encode(f.read()).decode("ascii")

# ---- reuse the exact CSS block from the sibling certification dashboard ----
src = open(STYLE_SOURCE, encoding="utf-8").read()
style_start = src.find(":root{")
style_end = src.find("</style>")
css_body = src[style_start:style_end]

# extra utility classes needed for this document (photo grid, TOC checklist tree, field table)
extra_css = """
.photogrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:14px;margin:16px 0}
figure.photo{margin:0;background:var(--surface);border:1px solid var(--line);border-radius:var(--radius);box-shadow:var(--shadow);overflow:hidden;display:flex;flex-direction:column}
figure.photo img{width:100%;display:block;background:var(--surface-3);object-fit:contain;max-height:340px}
figure.photo figcaption{padding:10px 12px 12px}
figure.photo figcaption b{display:block;font-size:12.5px;color:var(--ink);margin-bottom:4px;line-height:1.4}
figure.photo figcaption span{display:block;font-size:11.8px;color:var(--ink-soft);line-height:1.55}
.checklist-toc{list-style:none;margin:0;padding:0;font-size:12.8px}
.checklist-toc li{margin:2px 0}
.checklist-toc a{display:flex;align-items:baseline;gap:7px;color:#B3BDC9;text-decoration:none;padding:5px 20px;border-left:3px solid transparent}
.checklist-toc a:hover{background:rgba(255,255,255,.05);color:#fff}
.checklist-toc .sub{padding-left:34px}
.checklist-toc .st{font-size:10px;flex:none}
.checklist-toc .st.done{color:var(--good)}
.checklist-toc .st.pending{color:#7C8896}
.doclabel{font-size:10.5px;font-weight:700;letter-spacing:.03em;text-transform:uppercase;color:var(--ink-soft);margin:0 0 4px}
.enchecklist{background:var(--surface-2);border:1px dashed var(--line-2);border-radius:var(--radius);padding:9px 12px;margin:10px 0;font-size:12px;color:var(--ink-soft);font-style:italic}
.scopebanner{background:var(--info-soft);border-left:3px solid var(--info);border-radius:var(--radius);padding:13px 16px;font-size:13.3px;line-height:1.65;color:var(--ink-2);margin:0 0 20px}
.scopebanner b{color:var(--ink)}
@media print{
  #gld-cross-nav{display:none !important}
  .tbl-scroll{overflow-x:visible !important;border:none !important}
  table{min-width:0 !important;table-layout:fixed !important;width:100% !important}
  table td,table th{word-break:break-word}
  .photogrid{grid-template-columns:repeat(3,1fr) !important}
  figure.photo{break-inside:avoid}
  .zone{break-inside:auto}
  .subhead{break-after:avoid}
}
"""

css_full = css_body + extra_css

# ---- photos ----
photos = [
    ("3._Motherboard_ModulSensor_PenutupMesh_Casing_Antena_ModulAlarm.jpg",
     "Unit lengkap &mdash; tampak depan",
     "Node Sensor (GLD) terpasang lengkap: casing utama (biru) dengan penutup mesh sensor, antena LoRa eksternal, dan modul alarm visual (silinder, lampu merah) terpasang pada sisi kanan casing."),
    ("Casing_Belakang.jpg",
     "Unit lengkap &mdash; sudut lain",
     "Sudut pandang lain dari unit terakit, memperlihatkan posisi antena, modul alarm, dan sisi cable gland/kabel keluar dari casing."),
    ("PenutupMesh_Casing.jpg",
     "Unit lengkap &mdash; tampak depan (tanpa antena &amp; modul alarm)",
     "Casing utama dengan penutup mesh terpasang, sudut pandang datar menunjukkan bentuk enclosure dan 4 lubang baut dudukan (mounting)."),
    ("1._Motherboard_Casing.jpg",
     "Komponen utama &mdash; PCB dalam casing (sebelum modul sensor)",
     "PCB utama terpasang di dalam casing, sebelum modul sensor gas dipasang. Terlihat mikrokontroler ESP32-S3-WROOM-1U, modul radio LoRa, dan rangkaian daya."),
    ("2._Motherboard_ModulSensor_Casing.jpg",
     "Komponen utama &mdash; PCB dengan 8 modul sensor gas",
     "PCB yang sama dengan 8 kanal sensor gas seri MQ (MQ-2, MQ-3B, MQ-4, MQ-5, MQ-6, MQ-7B, MQ-8, MQ-135) terpasang mengelilingi mikrokontroler pusat."),
    ("ModulAlarm.jpg",
     "Komponen utama &mdash; modul alarm visual (close-up)",
     "Modul alarm visual (beacon/strobe) berbahan logam silinder dengan lensa merah, terhubung ke casing utama melalui cable gland terpisah."),
    ("PenutupMesh.jpg",
     "Komponen utama &mdash; penutup mesh sensor (close-up)",
     "Penutup mesh/kasa logam yang melindungi elemen sensor gas sekaligus berfungsi sebagai jalur difusi gas menuju sensor di baliknya."),
]
photo_cards = []
for fn, title, desc in photos:
    data = b64(fn)
    photo_cards.append(f'<figure class="photo">\n<img src="data:image/jpeg;base64,{data}" alt="{title}" loading="lazy">\n<figcaption><b>{title}</b><span>{desc}</span></figcaption>\n</figure>')
photos_html = "\n".join(photo_cards)

# ============================================================
# BODY
# ============================================================
body = f'''<meta charset="utf-8">
<title>Dokumen Teknis Sertifikasi IECEx/ATEX &mdash; GLD V2</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
{css_full}
</style>
<div class="shell">
<nav class="side" id="side">
  <div class="side-brand">
    <span class="brandmark"></span>
    <div class="brandtext"><b>Dokumen Teknis Sertifikasi</b><small>IECEx/ATEX &middot; GLD V2</small></div>
  </div>
  <div class="side-meta">
    <div class="sm-row"><span class="k">Versi</span><span class="v">Draf 0.1</span></div>
    <div class="sm-row"><span class="k">Tanggal</span><span class="v">11 Sep 2026</span></div>
    <div class="sm-row"><span class="k">Status</span><span class="v">Working document</span></div>
    <div class="sm-row"><span class="k">Cakupan</span><span class="v">Node Sensor (GLD)</span></div>
  </div>
  <ul class="checklist-toc">
    <li><a href="#tentang"><span class="st done">&#9679;</span> Tentang dokumen ini</a></li>
    <li><a href="#s1"><span class="st pending">&#9675;</span> 1. Informasi Dasar</a></li>
    <li><a href="#s2"><span class="st done">&#9679;</span> 2. Dokumentasi Teknis</a></li>
    <li><a class="sub" href="#s2-1"><span class="st done">&#9679;</span> 2.1 Deskripsi produk</a></li>
    <li><a class="sub" href="#s2-2"><span class="st done">&#9679;</span> 2.2 Nama, model &amp; spesifikasi</a></li>
    <li><a class="sub" href="#s2-3"><span class="st done">&#9679;</span> 2.3 Fungsional &amp; parameter teknis</a></li>
    <li><a class="sub" href="#s2-4"><span class="st done">&#9679;</span> 2.4 Foto produk</a></li>
    <li><a class="sub" href="#s2-5"><span class="st pending">&#9675;</span> 2.5 Lingkungan instalasi</a></li>
    <li><a class="sub" href="#s2-6"><span class="st pending">&#9675;</span> 2.6 Desain &amp; manufaktur (a&ndash;i)</a></li>
    <li><a href="#s3"><span class="st pending">&#9675;</span> 3. Informasi Sampel</a></li>
  </ul>
  <div class="side-foot">
    <button class="themebtn" id="themebtn">&#9788; Ganti tema terang/gelap</button>
  </div>
</nav>
<main class="content">

<div class="masthead">
  <div class="tagrow">
    <span class="chip accent">Working document</span>
    <span class="chip">Butir 1&ndash;4 dari 6 (Bagian 2)</span>
    <span class="chip warn">Beberapa parameter menunggu konfirmasi</span>
  </div>
  <h1>Dokumen Teknis Sertifikasi IECEx/ATEX &mdash; Gas Leak Detector (GLD) V2</h1>
  <p class="subtitle">Disusun mengacu langsung pada <i>IECEx/ATEX Certification Information Requirements</i> (dokumen asli ExCB, Inggris/Mandarin) &mdash; bagian <b>2. Technical Documentation</b>, butir 1&ndash;4: deskripsi produk, nama/model/spesifikasi, deskripsi fungsional &amp; parameter teknis, serta foto produk. Disusun bertahap; butir lain pada daftar isi menyusul.</p>
  <div class="docmeta-row">
    <div><span class="k">Objek sertifikasi</span><span class="v">Node Sensor (GLD) &mdash; V2</span></div>
    <div><span class="k">Produsen</span><span class="v">LAPI Ganesha Utama (LGU)</span></div>
    <div><span class="k">Mitra teknis</span><span class="v">Lab IoT &amp; Lab Fisika ITB</span></div>
    <div><span class="k">Acuan checklist</span><span class="v">IECEx/ATEX Certification Info. Requirements</span></div>
  </div>
</div>

<section class="zone" id="tentang">
  <div class="zone-head"><span class="zn">&#8226;</span><h2>Tentang dokumen ini</h2></div>
  <p class="lede">Dokumen ini adalah berkas teknis kerja (working document) yang disusun untuk memenuhi bagian <b>&ldquo;2. Technical Documentation&rdquo;</b> pada checklist resmi <i>IECEx/ATEX Certification Information Requirements</i> yang diberikan oleh lembaga sertifikasi (ExCB). Daftar isi di sisi kiri mengikuti struktur asli checklist tersebut secara lengkap (bagian 1&ndash;3); bagian yang belum disusun ditandai status &#9675; dan akan menyusul pada revisi berikutnya, sesuai permintaan penyusunan bertahap.</p>

  <div class="scopebanner">
    <b>Ruang lingkup sertifikasi saat ini &mdash; hanya Node Sensor (GLD).</b> Sesuai konfirmasi tim proyek, Cluster Head dan LoRa Gateway diasumsikan selalu beroperasi di area aman (safe area) dan berada <b>di luar</b> ruang lingkup sertifikasi IECEx/ATEX ini &mdash; ini asumsi kerja proyek, bukan hasil kajian klasifikasi area formal dari Pertamina. Tabel spesifikasi Cluster Head dan Gateway tetap disertakan di bagian 2.2&ndash;2.3 sebagai <b>konteks sistem</b> (karena ketiganya berbagi banyak komponen &amp; arsitektur), bukan sebagai objek yang diajukan sertifikasi.
  </div>

  <div class="enchecklist">Kutipan asli (EN), bagian 2, butir 1&ndash;4 &mdash; sumber: <span class="mono">IECEx ATEX Certification Information Requirements_EN.pdf</span>:<br>
  &ldquo;1) Detailed product description; 2) Product name, model, and specification list; 3) Complete and clear functional description and technical parameters (electrical parameters, mechanical parameters, etc.); 4) Clear product photos (overall and key components).&rdquo;</div>
</section>

<section class="zone" id="s1">
  <div class="zone-head"><span class="zn">1</span><h2>Informasi Dasar (Application and Organization)</h2></div>
  <p class="lede">Mencakup formulir aplikasi, izin usaha/registrasi perusahaan, struktur organisasi &amp; kontak, alamat &amp; profil fasilitas manufaktur, serta (bila berlaku) sertifikat ISO 9001. Sudah tercatat sebagai <span class="mono">gate:atex-basic-info</span> pada <i>Dashboard Sertifikasi GLD &mdash; ATEX/IECEx</i>.</p>
  <div class="banner info"><span class="ic">&#9675;</span><div><b>Belum disusun pada revisi ini.</b> Akan dilengkapi pada tahap berikutnya sesuai permintaan penyusunan bertahap.</div></div>
</section>

<section class="zone" id="s2">
  <div class="zone-head"><span class="zn">2</span><h2>Dokumentasi Teknis (Technical Documentation)</h2></div>
  <p class="lede">Sembilan butir menurut checklist asli (1&ndash;9, dengan butir 6 memiliki sub-butir a&ndash;i). Revisi ini menyusun butir 1&ndash;4; butir 5&ndash;9 menyusul.</p>

  <div class="subhead" id="s2-1"><h3>2.1 &middot; Deskripsi produk detail (Detailed product description)</h3></div>
  <p class="lede">Node Sensor Gas Leak Detector (GLD) adalah perangkat deteksi kebocoran gas multi-sensor berbasis IoT, dirancang untuk deteksi dini gas mudah terbakar dan gas proses di lingkungan kilang minyak &amp; gas (unit proses, tangki timbun/tank farm, pipe rack, dan area penyimpanan &amp; bongkar-muat). Perangkat ini adalah satu dari tiga jenis perangkat dalam sistem GLD V2 yang lebih luas &mdash; Node Sensor (GLD), Cluster Head, dan LoRa Gateway &mdash; namun <b>hanya Node Sensor yang menjadi objek sertifikasi IECEx/ATEX saat ini</b> (lihat catatan ruang lingkup di atas).</p>
  <p class="lede">Secara fungsional, Node Sensor mengintegrasikan delapan kanal sensor gas semikonduktor oksida logam seri MQ, sebuah mikrokontroler/prosesor edge-AI (ESP32-S3), dan modul radio LoRa (topologi star ke Cluster Head terdekat) dalam satu unit yang dipasang tetap (fixed-point) di lokasi berisiko kebocoran gas. Model klasifikasi gas berbasis AI (CNN Dual-Branch) berjalan langsung pada perangkat (on-device/edge inference) &mdash; <i>dikonfirmasi tim proyek secara langsung, belum diverifikasi dari dokumen firmware tertulis</i> &mdash; sehingga keputusan deteksi tidak bergantung koneksi berkelanjutan ke server pusat. Saat konsentrasi gas melewati ambang tertentu, perangkat memicu alarm lokal (modul alarm visual/strobe terpasang pada unit) sekaligus mengirim notifikasi alarm melalui jaringan LoRa ke Cluster Head dan diteruskan ke dashboard operator.</p>
  <p class="lede">Enclosure dirancang untuk lingkungan area berbahaya (hazardous area) di kilang &mdash; menggunakan material logam (aluminium alloy dan stainless steel, bukan plastik/PVC) dan dipasang menggunakan L-bracket ke struktur existing tanpa pengeboran atau pengelasan. <b>Penting:</b> pernyataan &ldquo;dirancang untuk&rdquo; ini menggambarkan niat desain (design intent), <b>bukan</b> klaim bahwa enclosure sudah lulus uji/tersertifikasi Ex &mdash; skema proteksi ledakan, kelompok gas, kelas temperatur, dan zona instalasi target akan diuraikan pada bagian 2.5 (menyusul).</p>
  <p class="lede">Catu daya versi produksi saat ini adalah 24 VDC kontinu (adaptor AC/DC dari jaringan listrik lokasi); jalur catu daya baterai portabel (Li-ion 18650) masih berstatus pengembangan (R&amp;D), belum menjadi versi produksi yang dideploy.</p>

  <div class="subhead" id="s2-2"><h3>2.2 &middot; Nama produk, model, &amp; daftar spesifikasi (Product name, model, and specification list)</h3></div>
  <div class="speclist">
    <div class="spec"><span class="k">Nama produk</span><span class="v">Gas Leak Detector (GLD) &mdash; Node Sensor</span></div>
    <div class="spec"><span class="k">Model / versi</span><span class="v">GLD V2 (Versi 2)</span></div>
    <div class="spec"><span class="k">Jenis perangkat pendukung sistem</span><span class="v">LoRa Cluster Head, LoRa Gateway (di luar cakupan sertifikasi)</span></div>
    <div class="spec"><span class="k">Produsen</span><span class="v">PT LAPI Ganesha Utama (LGU)</span></div>
    <div class="spec"><span class="k">Pengembang teknis</span><span class="v">Lab IoT &amp; Lab Fisika, Institut Teknologi Bandung</span></div>
    <div class="spec"><span class="k">Klien / pengguna akhir program</span><span class="v">PT Pertamina Patra Niaga (pilot RU IV Cilacap)</span></div>
  </div>
  <p class="lede">Tabel berikut merangkum spesifikasi ringkas ketiga jenis perangkat dalam sistem GLD V2, untuk konteks arsitektur sistem. <b>Objek sertifikasi = kolom &ldquo;Node Sensor (GLD)&rdquo; saja.</b></p>
  <div class="tbl-scroll">
  <table>
    <tr><th>Parameter</th><th>Node Sensor (GLD)</th><th>Cluster Head</th><th>LoRa Gateway</th></tr>
    <tr><td><b>Fungsi utama</b></td><td>Akuisisi data 8 sensor gas + transmisi LoRa</td><td>Mengumpulkan data beberapa Node Sensor &amp; meneruskan ke Gateway</td><td>Jembatan jaringan LoRa lapangan ke server</td></tr>
    <tr><td><b>Model/versi</b></td><td>V2</td><td>V2</td><td>V2</td></tr>
    <tr><td><b>Mikrokontroler</b></td><td>ESP32-S3-WROOM-1U</td><td>ESP32-S3-WROOM-1U</td><td>ESP32-S3-WROOM-1U</td></tr>
    <tr><td><b>Modul radio LoRa</b></td><td>E22-900MM22S</td><td>E22-900MM22S</td><td>E22-900MM22S</td></tr>
    <tr><td><b>Input daya</b></td><td>24 VDC, &#8776;0,33 A</td><td>5 VDC (baterai + solar)</td><td>5 VDC, adaptor AC/DC</td></tr>
    <tr><td><b>Konsumsi daya maks.</b></td><td>7,995 W</td><td>0,73 W</td><td>0,73 W</td></tr>
    <tr><td><b>Dimensi (P&times;L&times;T)</b></td><td>200 &times; 90 &times; 290 mm</td><td>80 &times; 80 &times; 210 mm</td><td>80 &times; 80 &times; 210 mm</td></tr>
    <tr><td><b>Material enclosure</b></td><td>Aluminium alloy + stainless steel</td><td>Aluminium alloy + stainless steel</td><td>Aluminium alloy + stainless steel</td></tr>
    <tr><td><b>IP Rating</b></td><td><span class="status wip">Menunggu konfirmasi</span></td><td><span class="status ok">IP66/67</span></td><td><span class="status wip">Kemungkinan sama CH, belum terpisah</span></td></tr>
    <tr class="hl"><td><b>Objek sertifikasi ATEX/IECEx?</b></td><td><b>Ya &mdash; cakupan dokumen ini</b></td><td>Tidak (asumsi: safe area)</td><td>Tidak (asumsi: safe area)</td></tr>
  </table>
  </div>
  <p class="lede" style="font-size:12px">Sumber: <span class="mono">Dokumen_spesifikasi_input_2.docx</span> (working document internal, direvisi 27 Agu 2026, disinkronkan dengan repo proyek) dan <span class="mono">Parameter spesifikasi EMC_lengkap.docx</span> (Dr. Nina Siti Aminah, Lab Fisika ITB).</p>

  <div class="subhead" id="s2-3"><h3>2.3 &middot; Deskripsi fungsional &amp; parameter teknis (electrical, mechanical, etc.)</h3></div>
  <p class="lede"><b>Alur kerja fungsional (mode operasi normal):</b> sensing &rarr; processing &rarr; transmit. Kedelapan sensor gas membaca kondisi udara secara kontinu &rarr; data dinormalisasi &amp; diklasifikasi oleh model AI on-device (ESP32-S3) &rarr; hasil dikirim melalui LoRa ke Cluster Head (topologi star) sesuai interval terkonfigurasi (default 10 detik), atau segera (event-driven) saat status alarm terdeteksi. Alarm gas dipicu sekaligus melalui dua jalur: modul alarm visual/strobe lokal pada unit, dan notifikasi push melalui jaringan LoRa ke dashboard &mdash; jalur alarm push sudah diuji berhasil pada mesh kampus (belum divalidasi pada instalasi lapangan RU produksi).</p>

  <p class="doclabel">2.3.a &middot; Parameter kelistrikan (Electrical parameters) &mdash; Node Sensor (GLD)</p>
  <div class="tbl-scroll">
  <table>
    <tr><th>Parameter</th><th>Spesifikasi</th><th>Status</th><th>Catatan</th></tr>
    <tr><td>Input daya utama</td><td>24 VDC</td><td><span class="status ok">Final &mdash; versi produksi</span></td><td>Catu daya kontinu dari adaptor AC/DC lokasi.</td></tr>
    <tr><td>Input adaptor AC/DC</td><td>220 VAC, 50 Hz</td><td><span class="status ok">Final</span></td><td>Mengikuti standar jaringan listrik PLN Indonesia.</td></tr>
    <tr><td>Output adaptor AC/DC</td><td>24 VDC</td><td><span class="status ok">Final</span></td><td>&nbsp;</td></tr>
    <tr><td>Tegangan operasi internal</td><td>5 VDC &amp; 3,3 VDC</td><td><span class="status ok">Final</span></td><td>5 VDC untuk rangkaian sensor/pemanas (heater) MQ; 3,3 VDC untuk logika ESP32-S3. Rincian arus tiap jalur belum didokumentasikan terpisah.</td></tr>
    <tr><td>Arus input maksimum</td><td>&#8776;0,33 A @ 24 VDC</td><td><span class="status ok">Dihitung</span></td><td>Dihitung dari konsumsi daya maksimum terukur (7,995 W) dibagi 24 VDC.</td></tr>
    <tr><td>Konsumsi daya maksimum</td><td>7,995 W @ 24 VDC</td><td><span class="status ok">Terukur &mdash; versi produksi</span></td><td>Berlaku untuk versi catu daya kontinu. Versi baterai (R&amp;D) tercatat terpisah 5,75 W &mdash; mode operasi berbeda, bukan kontradiksi data.</td></tr>
    <tr><td>Jalur baterai cadangan (R&amp;D, belum produksi)</td><td>Li-ion 18650 (LiitoKala), 7 sel paralel, 4,2 V/sel, &#8776;28.000 mAh total</td><td><span class="status wip">Jalur pengembangan</span></td><td>Belum menjadi versi produksi/dideploy. Belum ada sertifikasi keamanan sel/BMS (mis. UN 38.3, IEC 62133).</td></tr>
    <tr><td>Proteksi kelistrikan (fuse, polaritas terbalik, tegangan lebih, arus lebih)</td><td>&mdash;</td><td><span class="status gap">Menunggu konfirmasi</span></td><td>Cakupan proteksi elektrikal belum ditentukan/didokumentasikan.</td></tr>
  </table>
  </div>

  <p class="doclabel">2.3.b &middot; Parameter sensor &amp; komunikasi &mdash; Node Sensor (GLD)</p>
  <div class="tbl-scroll">
  <table>
    <tr><th>Parameter</th><th>Spesifikasi</th><th>Status</th><th>Catatan</th></tr>
    <tr><td>Sensor gas</td><td>MQ-2, MQ-3B, MQ-4, MQ-5, MQ-6, MQ-7B, MQ-8, MQ-135 (8 kanal)</td><td><span class="status ok">Final</span></td><td>Sensor semikonduktor oksida logam (metal-oxide), elemen sensing terekspos langsung ke udara (tidak tersembunyi).</td></tr>
    <tr><td>Model AI klasifikasi gas</td><td>CNN Dual-Branch &mdash; 4 kelas: LPG, CO&#8322;, Udara Bersih, H&#8322;</td><td><span class="status wip">Dikonfirmasi tim, belum terverifikasi dari dokumen firmware tertulis</span></td><td>Akurasi on-chip 99,20% (int8, ESP32-S3, ukuran model 9,14 KB). Belum mencakup Benzena, CO, H&#8322;S (requirement tambahan Pertamina, masih terbuka).</td></tr>
    <tr><td>Sensor lingkungan (suhu/kelembapan)</td><td>Tidak terpasang pada unit produksi</td><td><span class="status wip">Rig lab saja</span></td><td>Hanya digunakan pada rig pengujian laboratorium, bukan unit lapangan.</td></tr>
    <tr><td>Unit pemroses</td><td>ESP32-S3-WROOM-1U</td><td><span class="status ok">Final</span></td><td>Bersertifikat FCC (2AC7Z-ESPS3WROOM1U), TELEC, CE (data produsen Espressif) &mdash; sertifikasi RF/EMC, <b>bukan</b> sertifikat &ldquo;Ex component&rdquo;.</td></tr>
    <tr><td>Modul komunikasi</td><td>LoRa, modul E22-900MM22S</td><td><span class="status ok">Final</span></td><td>Bersertifikat CE, FCC, RoHS (data produsen Ebyte) &mdash; sertifikasi RF/EMC, <b>bukan</b> sertifikat &ldquo;Ex component&rdquo;.</td></tr>
    <tr><td>Frekuensi operasi</td><td>920 MHz</td><td><span class="status ok">Final</span></td><td>Topologi star ke Cluster Head; dalam pita ISM regional 920&ndash;923 MHz Indonesia.</td></tr>
    <tr><td>Daya pancar (konfigurasi firmware)</td><td>17 dBm</td><td><span class="status ok">Final</span></td><td>Modul radio mampu hingga 22 dBm &mdash; nilai 17 dBm adalah konfigurasi operasional, bukan batas modul.</td></tr>
    <tr><td>Bandwidth / Spreading Factor</td><td>125 kHz / SF7</td><td><span class="status ok">Final</span></td><td>Sumber: tabel parameter EMC.</td></tr>
    <tr><td>Antena</td><td>Eksternal, omnidirectional, konektor SMA Male, gain 3 dBi</td><td><span class="status ok">Final</span></td><td>Pada sebagian unit, antena Wi-Fi 2,4 GHz masih di dalam casing &mdash; perlu dikeluarkan agar konfigurasi kanal optimal.</td></tr>
    <tr><td>Interval pengiriman data</td><td>Dapat dikonfigurasi, default 10 detik</td><td><span class="status ok">Final</span></td><td>Event alarm dikirim segera (di luar interval periodik).</td></tr>
    <tr><td>Interface lain</td><td>SPI, LoRa</td><td><span class="status ok">Final</span></td><td>Port/konektor eksternal: USB, sensor, power, fan, antena, buzzer alarm.</td></tr>
  </table>
  </div>

  <p class="doclabel">2.3.c &middot; Parameter mekanik (Mechanical parameters) &mdash; Node Sensor (GLD)</p>
  <div class="tbl-scroll">
  <table>
    <tr><th>Parameter</th><th>Spesifikasi</th><th>Status</th><th>Catatan</th></tr>
    <tr><td>Material enclosure</td><td>Aluminium alloy + stainless steel</td><td><span class="status wip">Grade spesifik belum ditentukan</span></td><td>Material PVC tidak digunakan pada housing maupun bracket mana pun. Grade spesifik (seri aluminium, grade stainless 304/316L) masih dalam proses penentuan.</td></tr>
    <tr><td>Dimensi (P &times; L &times; T)</td><td>200 &times; 90 &times; 290 mm</td><td><span class="status ok">Final</span></td><td>Konsisten antara dokumen spesifikasi &amp; tabel parameter EMC.</td></tr>
    <tr><td>Berat total</td><td>&mdash;</td><td><span class="status gap">Menunggu konfirmasi</span></td><td>Belum ditimbang/didokumentasikan.</td></tr>
    <tr><td>Metode pemasangan</td><td>L-bracket, mengacu desain yang sudah terpasang di kilang</td><td><span class="status ok">Final</span></td><td>Dipasang ke struktur existing tanpa pengeboran atau pengelasan (keputusan rapat 6 Agu 2026).</td></tr>
    <tr><td>Tingkat proteksi (IP Rating)</td><td>&mdash;</td><td><span class="status gap">Menunggu konfirmasi</span></td><td>Belum diuji/ditentukan untuk Node Sensor (Cluster Head sudah IP66/67).</td></tr>
    <tr><td>Cable entry (gland)</td><td>&mdash;</td><td><span class="status gap">Menunggu konfirmasi</span></td><td>Spesifikasi cable gland belum ditentukan.</td></tr>
    <tr><td>Pemasangan antena</td><td>Eksternal, konektor SMA Male</td><td><span class="status ok">Final</span></td><td>&nbsp;</td></tr>
    <tr><td>Suhu operasi</td><td>&mdash;</td><td><span class="status gap">Menunggu konfirmasi</span></td><td>Rentang suhu lingkungan operasi belum ditentukan &mdash; termasuk parameter kunci untuk penentuan kelas temperatur (T1&ndash;T6) pada bagian 2.5.</td></tr>
    <tr><td>Kelembapan operasi</td><td>&mdash;</td><td><span class="status gap">Menunggu konfirmasi</span></td><td>&nbsp;</td></tr>
  </table>
  </div>
  <p class="lede" style="font-size:12px">Sumber: <span class="mono">Dokumen_spesifikasi_input_2.docx</span> &sect;1.1&ndash;1.3 (Node Sensor), disilangkan dengan <span class="mono">Parameter spesifikasi EMC_lengkap.docx</span> dan verifikasi sertifikasi komponen (<span class="mono">memory/decisions.md</span> dec:72).</p>

  <div class="banner warn"><span class="ic">&#9888;</span><div><b>Baris &ldquo;Menunggu konfirmasi&rdquo; di atas bukan kelalaian dokumentasi &mdash; ini status jujur.</b> Field tersebut sengaja belum diisi karena memang belum ada data resmi (belum diukur/diuji/diputuskan). Jangan mengisi dengan perkiraan pada revisi berikutnya tanpa sumber data yang jelas.</div></div>

  <div class="subhead" id="s2-4"><h3>2.4 &middot; Foto produk &mdash; keseluruhan &amp; komponen utama (Clear product photos)</h3></div>
  <p class="lede">Tujuh foto berikut diambil langsung dari unit prototipe Node Sensor (GLD) V2 (folder sumber: <span class="mono">GLD/</span>, tanpa metadata tanggal pengambilan pada file). Tiga foto pertama menunjukkan unit terakit secara keseluruhan dari sudut berbeda; empat foto berikutnya menunjukkan komponen utama secara close-up.</p>
  <div class="photogrid">
{photos_html}
  </div>
  <div class="banner info"><span class="ic">&#9432;</span><div><b>Kelengkapan foto &mdash; status apa adanya.</b> Ketujuh foto di atas mencakup unit keseluruhan dan komponen utama (PCB, modul sensor, modul alarm, penutup mesh) sehingga butir 2.4 checklist <b>terpenuhi secara substansi</b>. Yang <b>masih belum ada</b>: (a) foto berlabel resmi per-sisi (depan/belakang/kiri/kanan/atas/bawah) dengan skala/penggaris seperti lazimnya paket submission ExCB; (b) foto komponen individual seperti baterai, gasket/seal, terminal, dan cable gland secara terpisah; (c) foto Cluster Head &amp; Gateway (di luar cakupan sertifikasi saat ini, lihat catatan ruang lingkup).</div></div>

  <div class="subhead" id="s2-5"><h3>2.5 &middot; Deskripsi penggunaan &amp; lingkungan instalasi (gas group, temperature class, area classification)</h3></div>
  <div class="banner info"><span class="ic">&#9675;</span><div><b>Belum disusun pada revisi ini.</b> Menyusul &mdash; skema klasifikasi rekomendasi tim (grup gas IIC, kelas T4, Zona 1) sudah dicatat pada <i>Dashboard Sertifikasi GLD &mdash; ATEX/IECEx</i> (belum keputusan resmi ExCB/notified body).</div></div>

  <div class="subhead" id="s2-6"><h3>2.6 &middot; Informasi desain &amp; manufaktur (a&ndash;i: gambar teknik, BOM, datasheet material, proses manufaktur, perhitungan, draft manual, nameplate, sertifikat komponen Ex)</h3></div>
  <div class="banner info"><span class="ic">&#9675;</span><div><b>Belum disusun pada revisi ini.</b> Ringkasan gap per sub-butir sudah tersedia pada <span class="mono">ANALISIS-KEKURANGAN.md</span> &sect;2.2&ndash;2.8 (repo <span class="mono">sertifikasi-atex-gld-v2-2026</span>) sebagai acuan awal.</div></div>
</section>

<section class="zone" id="s3">
  <div class="zone-head"><span class="zn">3</span><h2>Informasi Sampel (Sample Information)</h2></div>
  <p class="lede">Model, nomor seri, dan status sampel uji (dapat dinyalakan/dioperasikan) serta fixture pengujian yang diperlukan.</p>
  <div class="banner info"><span class="ic">&#9675;</span><div><b>Belum disusun pada revisi ini.</b></div></div>
</section>

<footer>
  Dokumen kerja (working document) &mdash; disusun bertahap sesuai permintaan, mengacu langsung pada <i>IECEx/ATEX Certification Information Requirements</i> (versi asli EN/ZH dari ExCB). Sumber data: <span class="mono">Dokumen_spesifikasi_input_2.docx</span> (27 Agu 2026), <span class="mono">Parameter spesifikasi EMC_lengkap.docx</span>, foto folder <span class="mono">GLD/</span>, <span class="mono">ANALISIS-KEKURANGAN.md</span>, dan <span class="mono">memory/decisions.md</span> repo <span class="mono">GLD-V2-Report-2026</span> (dec:36, 45, 69, 72). Field bertanda &ldquo;Menunggu konfirmasi&rdquo; belum final &mdash; jangan dijadikan acuan pengadaan/sertifikasi tanpa verifikasi lebih lanjut. Lihat juga <i>Dashboard Sertifikasi GLD &mdash; ATEX/IECEx</i> untuk status &amp; Kurva-S keseluruhan proses sertifikasi.
</footer>

</main>
</div>
<script>
(function(){{
  const btn=document.getElementById('themebtn');
  btn.addEventListener('click',()=>{{
    const cur=document.documentElement.getAttribute('data-theme');
    const sysDark=window.matchMedia('(prefers-color-scheme:dark)').matches;
    const now=cur?cur:(sysDark?'dark':'light');
    document.documentElement.setAttribute('data-theme',now==='dark'?'light':'dark');
  }});
}})();
</script>
'''

with open(OUT_PATH, "w", encoding="utf-8") as f:
    f.write(body)

print("written", OUT_PATH, len(body), "chars")
