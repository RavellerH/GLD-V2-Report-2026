"""
Generator dashboard interaktif rapat 22 Oktober 2026 (09.00) — update GLD Tahap 2.

Output : Deliverables/Dashboard_Rapat_GLD_22Oktober2026.html (self-contained; gambar base64,
         video demo HJKIR ditautkan relatif ke Sumber Dokumen/)
Data   : scripts/assets/rapat_22okt/emc_points.json (216 titik pre-scan EMC Telkom Test House)
Jalankan: python scripts/build_dashboard_rapat_22okt.py
"""

import base64
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "scripts" / "assets" / "rapat_22okt"
OUT = ROOT / "Deliverables" / "Dashboard_Rapat_GLD_22Oktober2026.html"

VID = "../Sumber Dokumen/3 macam gas dari MWIR thermal kamera HJKIR"
VIDEOS = {
    "butane": f"{VID}/Chat History_20261021_072244/Images, videos, and files in chat history/Weixin Video_202610201617_1.mp4",
    "propane": f"{VID}/Chat History_20261021_072434/Images, videos, and files in chat history/Weixin Video_202610201618_1.mp4",
    "cylinders": f"{VID}/Chat History_20261021_072520/Images, videos, and files in chat history/Weixin Video_202610201619_1.mp4",
}


def img(name):
    return "data:image/jpeg;base64," + base64.b64encode((ASSETS / name).read_bytes()).decode()


def vid(key):
    return VIDEOS[key].replace(" ", "%20")


EMC = (ASSETS / "emc_points.json").read_text(encoding="utf-8")

HTML = r"""<!doctype html>
<html lang="id">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Dashboard Rapat GLD</title>
<style>
:root{--blue:#2B5FCB;--blue-soft:#E7ECF8;--char:#262321;--bg:#F4F5F8;--card:#FFFFFF;--ink:#262321;--ink2:#5A5550;--line:#DDE2EC;
--ok:#1F7A43;--okbg:#E6F2EB;--mid:#9A6A08;--midbg:#F6F1DC;--bad:#B4520F;--badbg:#FBEEE4;--gld:#2B5FCB;--ch:#138A7E;--grid:#E6E9F0}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--blue:#7097F0;--blue-soft:#222A3D;--bg:#141312;--card:#1E1C1B;--ink:#ECEAE6;--ink2:#ADA7A0;
--line:#36322F;--ok:#5FC488;--okbg:#1C3124;--mid:#E0B24A;--midbg:#372E14;--bad:#F08A4B;--badbg:#3A2416;--gld:#7097F0;--ch:#4CC7B6;--grid:#2C2927}}
:root[data-theme="dark"]{--blue:#7097F0;--blue-soft:#222A3D;--bg:#141312;--card:#1E1C1B;--ink:#ECEAE6;--ink2:#ADA7A0;
--line:#36322F;--ok:#5FC488;--okbg:#1C3124;--mid:#E0B24A;--midbg:#372E14;--bad:#F08A4B;--badbg:#3A2416;--gld:#7097F0;--ch:#4CC7B6;--grid:#2C2927}
*{box-sizing:border-box;margin:0;padding:0}
body{background:var(--bg);color:var(--ink);font:15px/1.5 "Segoe UI",Calibri,system-ui,sans-serif}
header{position:sticky;top:0;z-index:20;background:var(--char);color:#fff;border-bottom:3px solid #2B5FCB}
.hwrap{max-width:1320px;margin:0 auto;padding:12px 16px;display:flex;align-items:center;gap:16px;flex-wrap:wrap}
.hwrap h1{font-size:18px;font-weight:700}.hwrap .meta{font-size:13px;color:#C9C4BE}
.hwrap .sp{flex:1}
.btn{background:transparent;color:inherit;border:1px solid currentColor;border-radius:5px;padding:5px 11px;font:inherit;font-size:13px;cursor:pointer;opacity:.9}
.btn:hover{opacity:1}
nav{background:var(--card);border-bottom:1px solid var(--line);position:sticky;top:53px;z-index:15}
nav .nwrap{max-width:1320px;margin:0 auto;padding:0 16px;display:flex;gap:4px;overflow-x:auto}
nav a{white-space:nowrap;padding:10px 12px;color:var(--ink2);text-decoration:none;font-size:14px;border-bottom:2px solid transparent}
nav a.on,nav a:hover{color:var(--blue);border-bottom-color:var(--blue)}
main{max-width:1320px;margin:0 auto;padding:20px 16px 60px}
section{margin-bottom:34px;scroll-margin-top:110px}
.sh{display:flex;align-items:baseline;gap:12px;margin-bottom:12px;flex-wrap:wrap}
.sh .no{font-weight:700;color:var(--blue);font-size:13px;letter-spacing:.08em}
.sh h2{font-size:22px;font-family:Cambria,Georgia,serif}
.sh p{color:var(--ink2);font-size:14px;flex-basis:100%}
.card{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:16px}
.grid{display:grid;gap:14px}.grid>*{min-width:0}html,body{overflow-x:hidden}
.k4{grid-template-columns:repeat(auto-fit,minmax(min(220px,100%),1fr))}
.k2{grid-template-columns:repeat(auto-fit,minmax(min(340px,100%),1fr))}
.kpi .k{font-size:12px;font-weight:700;letter-spacing:.07em;text-transform:uppercase;color:var(--ink2)}
.kpi .v{font-size:30px;font-weight:700;color:var(--blue);line-height:1.2;margin:6px 0 4px}
.kpi .s{font-size:13px;color:var(--ink2)}
.bar{height:8px;background:var(--grid);border-radius:4px;position:relative;margin:8px 0 4px;overflow:hidden}
.bar i{position:absolute;left:0;top:0;bottom:0;background:var(--blue);border-radius:4px}
.bar b{position:absolute;top:-3px;bottom:-3px;width:2px;background:var(--ink)}
.note{border-left:4px solid var(--blue);background:var(--blue-soft);padding:10px 14px;border-radius:0 6px 6px 0;font-size:14px;margin-top:14px}
.note.warn{border-color:var(--bad);background:var(--badbg)}
.tl{display:grid;gap:10px}
.tl .it{display:grid;grid-template-columns:96px 1fr;gap:14px;align-items:start}
.tl .d{font-weight:700;color:var(--blue);font-size:14px;padding-top:2px}
.tl h3{font-size:15.5px}.tl p{font-size:14px;color:var(--ink2)}
.tag{display:inline-block;font-size:11px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;padding:2px 7px;border-radius:3px;margin-left:6px;vertical-align:2px}
.t-ok{background:var(--okbg);color:var(--ok)}.t-mid{background:var(--midbg);color:var(--mid)}.t-bad{background:var(--badbg);color:var(--bad)}.t-info{background:var(--blue-soft);color:var(--blue)}
.ctrl{display:flex;flex-wrap:wrap;gap:8px 18px;align-items:center;margin-bottom:12px;font-size:14px}
.chips{display:flex;gap:6px;flex-wrap:wrap}
.chip{border:1px solid var(--line);background:var(--card);color:var(--ink);border-radius:999px;padding:4px 12px;font:inherit;font-size:13px;cursor:pointer}
.chip.on{background:var(--blue);border-color:var(--blue);color:#fff}
select{font:inherit;font-size:13px;padding:4px 8px;border:1px solid var(--line);border-radius:5px;background:var(--card);color:var(--ink)}
label.ck{display:flex;gap:6px;align-items:center;cursor:pointer}
#chart{width:100%;height:auto;display:block;min-width:640px}.cwrap{overflow-x:auto}
#chart text{fill:var(--ink2);font-size:11px}
.legend{display:flex;gap:16px;flex-wrap:wrap;font-size:13px;color:var(--ink2);margin-top:6px}
.legend span{display:flex;gap:6px;align-items:center}
.dot{width:10px;height:10px;border-radius:50%;display:inline-block}
#tip{position:fixed;pointer-events:none;background:var(--char);color:#fff;font-size:12.5px;padding:8px 10px;border-radius:6px;display:none;z-index:50;max-width:260px;line-height:1.45}
table{width:100%;border-collapse:collapse;font-size:13.5px}
th,td{text-align:left;padding:7px 8px;border-bottom:1px solid var(--line);vertical-align:top}
th{font-size:12px;text-transform:uppercase;letter-spacing:.05em;color:var(--ink2);cursor:pointer;user-select:none;white-space:nowrap}
td.n,th.n{text-align:right;font-variant-numeric:tabular-nums}
.tbl{overflow-x:auto}
.m-bad{color:var(--bad);font-weight:700}.m-mid{color:var(--mid);font-weight:700}.m-ok{color:var(--ok)}
.spec{display:grid;grid-template-columns:170px 1fr;border-top:2px solid var(--ink2)}
.spec>div{padding:9px 0;border-bottom:1px solid var(--line)}
.spec>div:nth-child(odd){color:var(--ink2)}
.zoom{cursor:zoom-in;width:100%;border-radius:6px;border:1px solid var(--line);display:block;background:#fff}
#lb{position:fixed;inset:0;background:rgba(0,0,0,.85);display:none;align-items:center;justify-content:center;z-index:60;cursor:zoom-out;padding:16px}
#lb img{max-width:100%;max-height:100%}
.cam figure{margin:0}.cam img,.cam video{width:100%;border-radius:6px;display:block;background:#000}
.cam figcaption{display:flex;justify-content:space-between;align-items:center;margin-top:8px;font-weight:700}
.cam figcaption .btn{color:var(--blue)}
.asks{display:grid;gap:10px}
.ask{display:grid;grid-template-columns:34px 1fr 150px;gap:12px;align-items:start}
.ask .n{width:30px;height:30px;border-radius:50%;background:var(--blue);color:#fff;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:14px}
.ask h3{font-size:15.5px}.ask p{font-size:13.5px;color:var(--ink2)}
.ask .who{font-size:12px;font-weight:700;color:var(--blue);margin-top:4px}
.ask textarea{width:100%;margin-top:8px;font:inherit;font-size:13.5px;padding:6px 8px;border:1px solid var(--line);border-radius:5px;background:var(--bg);color:var(--ink);resize:vertical;min-height:34px}
.ask select{width:100%}
.ask.done{opacity:.75}
footer{max-width:1320px;margin:0 auto;padding:0 16px 30px;color:var(--ink2);font-size:12.5px}
@media (max-width:640px){.tl .it{grid-template-columns:1fr;gap:2px}.ask{grid-template-columns:30px 1fr}.ask .side{grid-column:2}
.spec{grid-template-columns:120px 1fr}nav{top:0;position:relative}header{position:relative}}
@media print{header,nav{position:static}#tip,#lb,.btn,.ctrl{display:none!important}section{break-inside:avoid}}
</style>
</head>
<body>
<header><div class="hwrap">
  <div><h1>Dashboard Rapat GLD Tahap 2</h1><div class="meta">Rabu, 22 Oktober 2026 · 09.00 WIB · PT LAPI Ganesha Utama · Lab IoT &amp; Lab Fisika ITB · untuk PT Pertamina Patra Niaga</div></div>
  <div class="sp"></div>
  <button class="btn" id="theme" type="button">Ganti tema</button>
</div></header>
<nav><div class="nwrap">
  <a href="#ringkasan">Ringkasan</a><a href="#update">Update 13–21 Okt</a><a href="#emc">Pre-scan EMC</a>
  <a href="#field">Field testing RU</a><a href="#kamera">Kamera MWIR</a><a href="#sertifikasi">Sertifikasi</a><a href="#keputusan">Butir keputusan</a>
</div></nav>
<main>

<section id="ringkasan">
  <div class="sh"><span class="no">01</span><h2>Status ringkas</h2><p>Posisi per 21 Oktober 2026. Angka progres adalah reassessment terakhir (30 September).</p></div>
  <div class="grid k4">
    <div class="card kpi"><div class="k">Progres proyek</div><div class="v">61%</div>
      <div class="bar" title="Aktual 61%, rencana 62%"><i style="width:61%"></i><b style="left:62%"></b></div>
      <div class="s">Rencana 62% per 30 Sep · selisih −1 poin</div></div>
    <div class="card kpi"><div class="k">Factory acceptance test</div><div class="v">7 / 7</div><div class="s">Item FAT lulus di lab · laporan Termin 1 field testing lengkap</div></div>
    <div class="card kpi"><div class="k">Sertifikasi ATEX/IECEx</div><div class="v">Berkas di GTS</div><div class="s">Form aplikasi + dossier dikirim ±29 Sep · sampel GLD2-0x1001 disiapkan 12 Okt</div></div>
    <div class="card kpi"><div class="k">Pre-scan EMC</div><div class="v" id="kpiEmc">–</div><div class="s" id="kpiEmcS"></div></div>
  </div>
  <div class="note">Item yang menunggu Pertamina (izin, TRA/JSA, pelaksana instalasi, klasifikasi area) dicatat terpisah dan tidak dihitung di progres LGU.</div>
</section>

<section id="update">
  <div class="sh"><span class="no">02</span><h2>Yang bergerak minggu lalu</h2></div>
  <div class="card tl">
    <div class="it"><div class="d">Okt</div><div><h3>Pre-scan EMC di Telkom Test House <span class="tag t-mid">Data mentah</span></h3><p>Emisi EN 55032 Class A untuk GLD dan Cluster Head besar — 7 pengukuran, 216 titik. Rincian di bagian 03.</p></div></div>
    <div class="it"><div class="d">18–21 Okt</div><div><h3>Materi visual <span class="tag t-ok">Selesai</span></h3><p>Video produk GLD 2 menit (ID/EN, landscape &amp; portrait) dan video konsep kamera OGI MWIR untuk pameran Cilacap.</p></div></div>
    <div class="it"><div class="d">20 Okt</div><div><h3>Demo kamera MWIR dari HJKIR <span class="tag t-info">Demo vendor</span></h3><p>n-butana dan propana terlihat di layar thermal, plus tabung &amp; sertifikat gas acuan. Rincian di bagian 05.</p></div></div>
    <div class="it"><div class="d">21 Okt</div><div><h3>Kebutuhan field testing diteruskan ke setiap RU <span class="tag t-info">Pertamina</span></h3><p>Spesifikasi minimum PC server usulan LGU disampaikan ke seluruh RU. Rincian di bagian 04.</p></div></div>
  </div>
</section>

<section id="emc">
  <div class="sh"><span class="no">03</span><h2>Pre-scan EMC — EN 55032 Class A</h2>
    <p>Margin = batas − level terukur (positif = di bawah batas). Arahkan kursor ke titik untuk detail. Titik merah bersilang ditandai <i>Failed</i> oleh software; semuanya di frekuensi kerja LoRa 919,6–921 MHz.</p></div>
  <div class="card">
    <div class="ctrl">
      <div class="chips" id="fDev"><button class="chip on" data-v="all" type="button">Semua</button><button class="chip" data-v="GLD" type="button">GLD</button><button class="chip" data-v="CH besar" type="button">CH besar</button></div>
      <label>Uji <select id="fTest"><option value="all">Semua uji</option></select></label>
      <label>Detektor <select id="fDet"><option value="all">Semua</option><option>Quasi-peak</option><option>Peak</option><option>Average</option></select></label>
      <label class="ck"><input type="checkbox" id="fLora"> Sembunyikan band LoRa (915–925 MHz)</label>
    </div>
    <div class="cwrap"><svg id="chart" viewBox="0 0 1000 380" role="img" aria-label="Grafik margin emisi terhadap frekuensi"></svg></div>
    <div class="legend"><span><i class="dot" style="background:var(--gld)"></i>GLD</span><span><i class="dot" style="background:var(--ch)"></i>CH besar</span>
      <span><i class="dot" style="background:var(--bad)"></i>Failed (band LoRa)</span><span>Pita kuning = margin &lt; 3 dB · garis putus = 6 dB</span></div>
  </div>
  <div class="grid k2" style="margin-top:14px">
    <div class="card"><h3 style="font-size:15.5px;margin-bottom:8px">Margin terkecil per pengukuran <span style="font-weight:400;color:var(--ink2);font-size:13px">(di luar band LoRa)</span></h3>
      <div class="tbl"><table id="sumT"><thead><tr><th>Perangkat</th><th>Uji</th><th class="n">Titik</th><th class="n">Margin min</th><th class="n">Frekuensi</th></tr></thead><tbody></tbody></table></div></div>
    <div class="card"><h3 style="font-size:15.5px;margin-bottom:8px">Catatan &amp; tindak lanjut</h3>
      <div class="tl">
        <div class="it"><div class="d"><span class="tag t-mid" style="margin:0">Konfirmasi</span></div><div><p><b>Band LoRa 920–921 MHz.</b> Pada standar EMC, pita pemancar umumnya dikecualikan dan dinilai lewat standar radio (ETSI EN 300 220). Perlu konfirmasi Telkom Test House, atau ukur ulang dengan LoRa idle.</p></div></div>
        <div class="it"><div class="d"><span class="tag t-bad" style="margin:0">Margin tipis</span></div><div><p><b>GLD 117–127 MHz: 0,5–0,95 dB.</b> Sumber emisi (clock/DC-DC) perlu dicari dan diredam sebelum uji di lab terakreditasi.</p></div></div>
        <div class="it"><div class="d"><span class="tag t-info" style="margin:0">Cakupan</span></div><div><p>Belum ada uji imunitas (EN 61000-6-2); Gateway dan CH kecil belum diuji; file tidak mencatat model/serial/kondisi operasi; GLD diuji konduksi lewat adaptor AC. Belum ada laporan resmi lab.</p></div></div>
      </div></div>
  </div>
  <div class="card" style="margin-top:14px">
    <div style="display:flex;justify-content:space-between;align-items:center;gap:10px;flex-wrap:wrap;margin-bottom:6px">
      <h3 style="font-size:15.5px">Data titik ukur <span id="cnt" style="font-weight:400;color:var(--ink2);font-size:13px"></span></h3>
      <button class="btn" id="more" type="button" style="color:var(--blue)">Tampilkan semua</button></div>
    <div class="tbl"><table id="ptT"><thead><tr>
      <th data-k="dev">Perangkat</th><th data-k="test">Uji</th><th data-k="det">Detektor</th><th data-k="f" class="n">Frekuensi</th>
      <th data-k="mag" class="n">Level</th><th data-k="lim" class="n">Batas</th><th data-k="margin" class="n">Margin ▲</th><th data-k="pol">Pol.</th></tr></thead><tbody></tbody></table></div>
  </div>
</section>

<section id="field">
  <div class="sh"><span class="no">04</span><h2>Persiapan field testing di setiap RU</h2><p>Pesan Pertamina Patra Niaga 21 Okt: kebutuhan field testing <i>multi-modality gas leak detection system</i> diteruskan ke setiap RU.</p></div>
  <div class="grid k2">
    <div class="card"><h3 style="font-size:15.5px;margin-bottom:10px">Spesifikasi minimum PC server</h3>
      <div class="spec">
        <div>Bentuk</div><div><b>PC fisik</b> (bukan VM)</div>
        <div>Lokasi</div><div>Ruang server lokal</div>
        <div>CPU</div><div><b>4 core</b></div>
        <div>RAM</div><div><b>8 GB</b></div>
        <div>Penyimpanan</div><div><b>SSD 256 GB</b></div>
        <div>Jaringan</div><div><b>2 port LAN</b> — NIC kedua boleh USB-LAN</div>
      </div>
      <div class="note"><b>LAN-1</b> → router Wi-Fi 2,4 GHz dari LGU (jaringan field lokal, tanpa internet). <b>LAN-2</b> → intranet kantor, agar dashboard bisa dibuka dari kantor kilang.</div>
      <div class="note warn">Perlu dari tiap RU: unit PC aktual, sistem operasi, ruang server, dan PIC IT — agar installer LGU disesuaikan sebelum instalasi.</div></div>
    <div class="card"><h3 style="font-size:15.5px;margin-bottom:10px">Lingkup pekerjaan (versi final 8 Okt) <span style="font-weight:400;color:var(--ink2);font-size:13px">klik untuk perbesar</span></h3>
      <img class="zoom" src="__DIAG__" alt="Block diagram lingkup Field dan Building: GLD, Cluster Head, Gateway, router Wi-Fi, server, UPS">
      <p style="font-size:13.5px;color:var(--ink2);margin-top:10px"><b style="color:var(--blue)">LGU</b>: GLD, Cluster Head, solar cell, Gateway, router Wi-Fi. <b style="color:var(--mid)">Pertamina</b>: instalasi, mounting support, junction box + PSU 24 VDC, kabel, server, UPS, jaringan IT.</p></div>
  </div>
</section>

<section id="kamera">
  <div class="sh"><span class="no">05</span><h2>Demo kamera MWIR — HJKIR, 20 Oktober</h2><p>Gas dilepas dari tabung lewat selang; kamera menangkap gumpalan secara real-time (640×512, 25 Hz). Klik “Putar video” untuk rekaman asli (dibuka dari folder Sumber Dokumen repo ini).</p></div>
  <div class="grid k4 cam">
    <figure class="card"><img src="__BUT__" alt="Citra thermal kebocoran n-butana" data-vid="__VBUT__"><figcaption>n-Butana <button class="btn play" type="button">Putar video</button></figcaption></figure>
    <figure class="card"><img src="__PRO__" alt="Citra thermal kebocoran propana" data-vid="__VPRO__"><figcaption>Propana <button class="btn play" type="button">Putar video</button></figcaption></figure>
    <div class="card"><h3 style="font-size:15.5px">Video ketiga</h3><p style="font-size:14px;color:var(--ink2);margin:6px 0 10px">Tabung dan sertifikat gas acuan DATEN (batch 202610171528). Nama gas ketiga belum terbaca jelas.</p>
      <a class="btn" style="color:var(--blue);text-decoration:none;display:inline-block" href="__VCYL__" target="_blank" rel="noopener">Buka video</a>
      <div class="note warn">Demo vendor di kantornya, bukan uji LGU/ITB. Konsentrasi, laju bocor, dan jarak tidak disebutkan.</div></div>
  </div>
</section>

<section id="sertifikasi">
  <div class="sh"><span class="no">06</span><h2>Sertifikasi ATEX / IECEx</h2><p>Berkas sudah di GTS (agen sertifikasi), masuk putaran revisi.</p></div>
  <div class="grid k2">
    <div class="card"><div class="spec">
      <div>Pemohon &amp; produsen</div><div><b>PT Galaksi Megatama Indonesia</b></div>
      <div>Usulan marking</div><div><b>II 2G Ex db IIC T4 Gb</b></div>
      <div>Metode proteksi</div><div>Ex d (flameproof)</div>
      <div>Suhu operasi</div><div>−20 °C s/d +60 °C</div>
      <div>Kelas suhu T4</div><div>Indikasi <b>±114 °C</b> vs batas efektif 130 °C <span class="tag t-mid">belum final</span></div>
      <div>Sampel</div><div>GLD2-0x1001</div>
    </div></div>
    <div class="card"><h3 style="font-size:15.5px;margin-bottom:6px">Langkah berikut</h3>
      <div class="tl">
        <div class="it"><div class="d">Dossier</div><div><p>Revisi pada putaran berikut dari GTS: samakan suhu operasi, hapus marking debu, samakan cable entry M20×1,5.</p></div></div>
        <div class="it"><div class="d">Suhu</div><div><p>Lengkapi titik ukur yang belum (DC/DC, induktor, MOSFET; mode alarm/transmit).</p></div></div>
        <div class="it"><div class="d">Termin 1</div><div><p>Uji internal di-<i>witness</i> Pertamina + berita acara.</p></div></div>
        <div class="it"><div class="d">EMC</div><div><p>Tindak lanjut pre-scan (bagian 03) sebelum uji resmi.</p></div></div>
      </div></div>
  </div>
</section>

<section id="keputusan">
  <div class="sh"><span class="no">07</span><h2>Butir yang perlu disepakati</h2><p>Status dan catatan bisa diisi selama rapat — tersimpan di browser ini saja. Tombol “Salin ringkasan” menyalin hasilnya sebagai teks untuk WA/notulen.</p></div>
  <div class="card">
    <div class="asks" id="asks"></div>
    <div style="display:flex;gap:10px;margin-top:14px;flex-wrap:wrap"><button class="btn" id="copy" type="button" style="color:var(--blue)">Salin ringkasan</button><button class="btn" id="reset" type="button" style="color:var(--ink2)">Kosongkan isian</button><span id="copied" style="font-size:13px;color:var(--ok);align-self:center"></span></div>
  </div>
</section>
</main>
<footer>Sumber: data mentah pre-scan EMC Telkom Test House (Okt 2026), pesan Pertamina Patra Niaga 21 Okt 2026, video HJKIR 20 Okt 2026, block diagram lingkup RU IV 8 Okt 2026, laporan status LGU 30 Sep 2026. Data pre-scan bukan laporan uji resmi.</footer>
<div id="tip"></div><div id="lb"><img alt=""></div>
<script>
const P=__EMC__;
const LORA=p=>p.f>=915e6&&p.f<=925e6;
const fmtF=f=>f>=1e9?(f/1e9).toFixed(4).replace(/\.?0+$/,'')+' GHz':f>=1e6?(f/1e6).toFixed(2)+' MHz':(f/1e3).toFixed(1)+' kHz';
const fmt=(n,d=2)=>n.toFixed(d).replace('.',',');
const mcls=m=>m<0?'m-bad':m<3?'m-bad':m<6?'m-mid':'m-ok';
const css=v=>getComputedStyle(document.documentElement).getPropertyValue(v).trim();
let st={dev:'all',test:'all',det:'all',lora:false,all:false,sk:'margin',sd:1};
[...new Set(P.map(p=>p.test))].forEach(t=>{const o=document.createElement('option');o.textContent=t;fTest.appendChild(o)});
function flt(){return P.filter(p=>(st.dev==='all'||p.dev===st.dev)&&(st.test==='all'||p.test===st.test)&&(st.det==='all'||p.det===st.det)&&!(st.lora&&LORA(p)))}
const W=1000,H=380,L=56,R=16,T=14,B=40,Y0=-60,Y1=60;
const xs=f=>L+(Math.log10(f)-Math.log10(1.5e5))/(Math.log10(6e9)-Math.log10(1.5e5))*(W-L-R);
const ys=m=>T+(Y1-Math.max(Y0,Math.min(Y1,m)))/(Y1-Y0)*(H-T-B);
function draw(){
  const d=flt(),g=css('--grid'),ink=css('--ink2');
  let s=`<rect x="${L}" y="${ys(3)}" width="${W-L-R}" height="${ys(0)-ys(3)}" fill="${css('--midbg')}"/>`;
  for(let m=Y0;m<=Y1;m+=20)s+=`<line x1="${L}" x2="${W-R}" y1="${ys(m)}" y2="${ys(m)}" stroke="${g}"/><text x="${L-8}" y="${ys(m)+4}" text-anchor="end">${m}</text>`;
  [[1e6,'1 MHz'],[1e7,'10 MHz'],[1e8,'100 MHz'],[1e9,'1 GHz'],[1.5e5,'150 kHz'],[6e9,'6 GHz']].forEach(([f,t])=>s+=`<line x1="${xs(f)}" x2="${xs(f)}" y1="${T}" y2="${H-B}" stroke="${g}"/><text x="${xs(f)}" y="${H-B+16}" text-anchor="middle">${t}</text>`);
  s+=`<line x1="${L}" x2="${W-R}" y1="${ys(0)}" y2="${ys(0)}" stroke="${css('--bad')}" stroke-width="1.5"/>`;
  s+=`<line x1="${L}" x2="${W-R}" y1="${ys(6)}" y2="${ys(6)}" stroke="${ink}" stroke-dasharray="4 4"/>`;
  s+=`<text x="14" y="${(H-B+T)/2}" transform="rotate(-90 14 ${(H-B+T)/2})" text-anchor="middle">Margin (dB)</text><text x="${W-R}" y="${H-6}" text-anchor="end">Frekuensi (skala log)</text>`;
  if(!st.lora)s+=`<rect x="${xs(915e6)}" y="${T}" width="${xs(925e6)-xs(915e6)}" height="${H-T-B}" fill="${css('--bad')}" opacity=".08"/>`;
  d.forEach((p,i)=>{const x=xs(p.f),y=ys(p.margin),c=p.dev==='GLD'?css('--gld'):css('--ch');
    s+=p.failed?`<g data-i="${P.indexOf(p)}" class="pt"><line x1="${x-6}" y1="${y-6}" x2="${x+6}" y2="${y+6}" stroke="${css('--bad')}" stroke-width="2.5"/><line x1="${x-6}" y1="${y+6}" x2="${x+6}" y2="${y-6}" stroke="${css('--bad')}" stroke-width="2.5"/><circle cx="${x}" cy="${y}" r="9" fill="transparent"/></g>`
      :`<circle class="pt" data-i="${P.indexOf(p)}" cx="${x}" cy="${y}" r="${p.margin<3?6:4.5}" fill="${c}" fill-opacity="${p.det==='Average'?.45:.85}" stroke="${css('--card')}" stroke-width="1"/>`});
  if(d.some(p=>p.margin<Y0))s+=`<text x="${W-R-4}" y="${H-B-6}" text-anchor="end">Titik di bawah −60 dB digambar di tepi bawah</text>`;
  chart.innerHTML=s;
}
chart.addEventListener('mousemove',e=>{const t=e.target.closest('.pt');if(!t){tip.style.display='none';return}const p=P[t.dataset.i];
  tip.innerHTML=`<b>${p.dev}</b> · ${p.test}<br>${fmtF(p.f)} · ${p.det}<br>Level ${fmt(p.mag)} / batas ${fmt(p.lim,0)}<br>Margin <b>${fmt(p.margin)} dB</b>${p.pol?` · pol ${p.pol}, ${p.h} cm, ${p.ang}°`:''}${p.failed?'<br><b>Failed</b> — frekuensi kerja LoRa':''}`;
  tip.style.display='block';tip.style.left=Math.min(e.clientX+14,innerWidth-270)+'px';tip.style.top=(e.clientY+14)+'px'});
chart.addEventListener('mouseleave',()=>tip.style.display='none');
function summary(){
  const groups={};P.filter(p=>!LORA(p)).forEach(p=>{const k=p.dev+'|'+p.test;(groups[k]=groups[k]||[]).push(p)});
  sumT.tBodies[0].innerHTML=Object.entries(groups).map(([k,a])=>{const m=a.reduce((x,y)=>y.margin<x.margin?y:x);const[d,t]=k.split('|');
    return `<tr><td>${d}</td><td>${t}</td><td class="n">${a.length}</td><td class="n ${mcls(m.margin)}">${fmt(m.margin)} dB</td><td class="n">${fmtF(m.f)}</td></tr>`}).join('');
  const out=P.filter(p=>!LORA(p)),mn=out.reduce((x,y)=>y.margin<x.margin?y:x);
  kpiEmc.textContent=P.length+' titik';kpiEmcS.innerHTML=`${P.filter(p=>p.failed).length} ditandai Failed, semuanya di band LoRa · margin terkecil di luar LoRa <b>${fmt(mn.margin)} dB</b> (${mn.dev}, ${fmtF(mn.f)})`;
}
function table(){
  const d=flt().sort((a,b)=>{const x=a[st.sk],y=b[st.sk];return(x>y?1:x<y?-1:0)*st.sd});
  const v=st.all?d:d.slice(0,15);
  cnt.textContent=`(${v.length} dari ${d.length} titik sesuai filter)`;more.textContent=st.all?'Tampilkan 15 teratas':'Tampilkan semua';
  ptT.tBodies[0].innerHTML=v.map(p=>`<tr><td>${p.dev}</td><td>${p.test}</td><td>${p.det}</td><td class="n">${fmtF(p.f)}</td><td class="n">${fmt(p.mag)}</td><td class="n">${fmt(p.lim,0)}</td><td class="n ${mcls(p.margin)}">${fmt(p.margin)}${p.failed?' ✕':''}</td><td>${p.pol||'—'}</td></tr>`).join('');
  [...ptT.tHead.rows[0].cells].forEach(c=>{c.textContent=c.textContent.replace(/ [▲▼]$/,'');if(c.dataset.k===st.sk)c.textContent+=st.sd>0?' ▲':' ▼'});
}
function upd(){draw();table()}
fDev.onclick=e=>{const b=e.target.closest('.chip');if(!b)return;[...fDev.children].forEach(c=>c.classList.toggle('on',c===b));st.dev=b.dataset.v;upd()};
fTest.onchange=()=>{st.test=fTest.value;upd()};fDet.onchange=()=>{st.det=fDet.value;upd()};fLora.onchange=()=>{st.lora=fLora.checked;upd()};
more.onclick=()=>{st.all=!st.all;table()};
ptT.tHead.onclick=e=>{const k=e.target.dataset.k;if(!k)return;st.sd=st.sk===k?-st.sd:1;st.sk=k;table()};
/* lightbox & video */
document.querySelectorAll('.zoom').forEach(i=>i.onclick=()=>{lb.firstElementChild.src=i.src;lb.style.display='flex'});
lb.onclick=()=>lb.style.display='none';
document.querySelectorAll('.cam .play').forEach(b=>b.onclick=()=>{const f=b.closest('figure'),im=f.querySelector('img');
  const v=document.createElement('video');v.src=im.dataset.vid;v.controls=true;v.autoplay=true;v.playsInline=true;v.poster=im.src;
  v.onerror=()=>{v.replaceWith(im);b.textContent='Video tidak ditemukan';b.disabled=true};im.replaceWith(v);b.remove()});
/* butir keputusan */
const ASKS=[
 ['PC server tiap RU','Unit, OS, ruang server yang ditunjuk per RU, beserta PIC IT.','Pertamina / RU'],
 ['Lingkup “multi-modality”','Apakah kamera OGI ikut field testing tahap ini, dan di RU mana.','Pertamina'],
 ['Jadwal instalasi RU IV Cilacap','Pelaksana instalasi dan konfirmasi tertulis HSE bahwa lokasi termasuk area non-ATEX.','RU IV'],
 ['Witness uji internal sertifikasi','Tanggal witness dan format berita acara.','Pertamina + LGU'],
 ['Tindak lanjut EMC','Konfirmasi lab soal band LoRa dan perbaikan margin GLD di ±118 MHz.','LGU']];
const KEY='gld-rapat-22okt';let S={};try{S=JSON.parse(localStorage.getItem(KEY))||{}}catch(e){}
const save=()=>{try{localStorage.setItem(KEY,JSON.stringify(S))}catch(e){}};
function asks(){asksEl.innerHTML=ASKS.map((a,i)=>{const s=S[i]||{};return `<div class="ask ${s.st==='Disepakati'?'done':''}"><span class="n">${i+1}</span><div><h3>${a[0]}</h3><p>${a[1]}</p>
  <textarea data-i="${i}" placeholder="Catatan rapat…" aria-label="Catatan butir ${i+1}">${(s.nt||'').replace(/</g,'&lt;')}</textarea></div>
  <div class="side"><select data-i="${i}" aria-label="Status butir ${i+1}">${['Terbuka','Disepakati','Ditunda'].map(o=>`<option${(s.st||'Terbuka')===o?' selected':''}>${o}</option>`).join('')}</select><div class="who">${a[2]}</div></div></div>`}).join('')}
const asksEl=document.getElementById('asks');asks();
asksEl.addEventListener('change',e=>{const i=e.target.dataset.i;if(e.target.tagName==='SELECT'){(S[i]=S[i]||{}).st=e.target.value;save();e.target.closest('.ask').classList.toggle('done',e.target.value==='Disepakati')}});
asksEl.addEventListener('input',e=>{if(e.target.tagName==='TEXTAREA'){(S[e.target.dataset.i]=S[e.target.dataset.i]||{}).nt=e.target.value;save()}});
copy.onclick=()=>{const t='Hasil rapat GLD — 22 Okt 2026\n'+ASKS.map((a,i)=>{const s=S[i]||{};return `${i+1}. ${a[0]} [${s.st||'Terbuka'}] (${a[2]})${s.nt?'\n   '+s.nt.replace(/\n/g,'\n   '):''}`}).join('\n');
  (navigator.clipboard?navigator.clipboard.writeText(t):Promise.reject()).then(()=>copied.textContent='Tersalin.',()=>{copied.textContent='Gagal menyalin — pilih teks manual.'});setTimeout(()=>copied.textContent='',2500)};
reset.onclick=()=>{if(confirm('Kosongkan semua status dan catatan?')){S={};save();asks()}};
/* tema & nav */
theme.onclick=()=>{const r=document.documentElement,dark=r.dataset.theme?r.dataset.theme==='dark':matchMedia('(prefers-color-scheme: dark)').matches;r.dataset.theme=dark?'light':'dark';draw()};
const links=[...document.querySelectorAll('nav a')];
if('IntersectionObserver' in window){const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting)links.forEach(a=>a.classList.toggle('on',a.getAttribute('href')==='#'+e.target.id))}),{rootMargin:'-120px 0px -60% 0px'});document.querySelectorAll('section').forEach(s=>io.observe(s))}
summary();upd();
</script>
</body>
</html>
"""

html = (HTML.replace("__EMC__", EMC)
        .replace("__DIAG__", img("block_diagram.jpg"))
        .replace("__BUT__", img("butane.jpg")).replace("__PRO__", img("propane.jpg"))
        .replace("__VBUT__", vid("butane")).replace("__VPRO__", vid("propane")).replace("__VCYL__", vid("cylinders")))
OUT.write_text(html, encoding="utf-8")
print(OUT, f"{OUT.stat().st_size / 1024:.0f} KB")
