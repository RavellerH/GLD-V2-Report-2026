"""
Generator deck HTML rapat 22 Oktober 2026 (09.00) — update progres GLD Tahap 2.

Output : Deliverables/Presentasi_Rapat_GLD_22Oktober2026.html (self-contained, gambar base64)
Palet  : biru #2B5FCB + charcoal #262321, light + dark.
Jalankan: python scripts/build_presentasi_rapat_22okt.py
"""

import base64
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "scripts" / "assets" / "rapat_22okt"
OUT = ROOT / "Deliverables" / "Presentasi_Rapat_GLD_22Oktober2026.html"


def img(name):
    data = base64.b64encode((ASSETS / name).read_bytes()).decode()
    return f"data:image/jpeg;base64,{data}"


# (perangkat, uji, margin dB, catatan)
EMC = [
    ("GLD", "Radiasi 30 MHz–1 GHz (QP)", 0.51, "117,9 MHz · polarisasi H"),
    ("GLD", "Konduksi AC L1/L2 (QP)", 6.03, "324 kHz"),
    ("GLD", "Radiasi 1–6 GHz (AV)", 33.97, "1,81 GHz"),
    ("CH besar", "Radiasi 30 MHz–1 GHz (QP)", 3.28, "978,9 MHz"),
    ("CH besar", "Radiasi 1–6 GHz (AV)", 5.56, "1,8425 GHz ≈ 2× LoRa"),
    ("CH besar", "Konduksi DC (QP/AV)", 42.41, "150 kHz"),
]


def emc_rows():
    out = []
    for dev, test, m, note in EMC:
        pct = min(m / 20.0, 1.0) * 100
        cls = "bad" if m < 3 else ("mid" if m < 6 else "good")
        out.append(
            f'<div class="emc-row"><div class="emc-lab"><b>{dev}</b><span>{test}</span></div>'
            f'<div class="emc-bar"><i class="{cls}" style="width:{pct:.1f}%"></i></div>'
            f'<div class="emc-val {cls}">{m:.2f} dB</div><div class="emc-note">{note}</div></div>'
        )
    return "\n".join(out)


SLIDES = [
    # 1 cover
    f"""
<section class="slide cover">
  <div class="cover-band"></div>
  <div class="cover-body">
    <div class="kicker">Rapat koordinasi · Rabu, 22 Oktober 2026 · 09.00 WIB</div>
    <h1>Gas Leak Detection (GLD) Tahap 2</h1>
    <p class="sub">Update progres: pre-scan EMC, persiapan field testing di setiap RU, demo kamera MWIR, dan status sertifikasi</p>
    <div class="cover-meta">PT LAPI Ganesha Utama · Lab IoT &amp; Lab Fisika ITB<br>untuk PT Pertamina Patra Niaga</div>
  </div>
</section>""",
    # 2 agenda
    """
<section class="slide">
  <div class="kicker">Agenda</div>
  <h2>Yang dibahas pagi ini</h2>
  <ol class="agenda">
    <li><b>Status ringkas</b><span>Posisi proyek, field testing, dan sertifikasi</span></li>
    <li><b>Update 13–21 Oktober</b><span>Apa yang bergerak minggu lalu</span></li>
    <li><b>Hasil pre-scan EMC</b><span>Telkom Test House — GLD &amp; Cluster Head</span></li>
    <li><b>Persiapan field testing setiap RU</b><span>PC server &amp; lingkup pekerjaan</span></li>
    <li><b>Demo kamera MWIR (HJKIR)</b><span>n-butana &amp; propana</span></li>
    <li><b>Sertifikasi ATEX/IECEx</b><span>Posisi berkas &amp; langkah berikut</span></li>
    <li><b>Butir yang perlu disepakati</b></li>
  </ol>
</section>""",
    # 3 status
    """
<section class="slide">
  <div class="kicker">Status ringkas</div>
  <h2>Posisi proyek per 21 Oktober</h2>
  <div class="kpis">
    <div class="kpi"><div class="k">Progres proyek</div><div class="v">61%</div><div class="s">rencana 62% (per 30 Sep) · selisih −1 poin</div></div>
    <div class="kpi"><div class="k">FAT lab</div><div class="v">7/7</div><div class="s">item FAT lulus di lab · laporan Termin 1 field testing sudah lengkap</div></div>
    <div class="kpi"><div class="k">Sertifikasi</div><div class="v">Berkas di GTS</div><div class="s">form aplikasi + dossier dikirim ±29 Sep · sampel GLD2-0x1001 disiapkan 12 Okt</div></div>
    <div class="kpi"><div class="k">EMC</div><div class="v">Pre-scan</div><div class="s">emisi GLD &amp; CH besar sudah diukur · belum laporan resmi</div></div>
  </div>
  <div class="note">Item yang menunggu Pertamina (izin, TRA/JSA, pelaksana instalasi, klasifikasi area) dicatat terpisah dan tidak dihitung di progres LGU.</div>
</section>""",
    # 4 update minggu ini
    """
<section class="slide">
  <div class="kicker">Update 13–21 Oktober</div>
  <h2>Yang bergerak minggu lalu</h2>
  <div class="tl">
    <div class="tl-i"><div class="d">Okt</div><div><b>Pre-scan EMC di Telkom Test House</b><p>Emisi EN 55032 Class A untuk GLD dan Cluster Head besar. Data mentah sudah diterima.</p></div></div>
    <div class="tl-i"><div class="d">18–21 Okt</div><div><b>Materi visual</b><p>Video produk GLD 2 menit (ID/EN, landscape &amp; portrait) dan video konsep kamera OGI MWIR untuk pameran Cilacap.</p></div></div>
    <div class="tl-i"><div class="d">20 Okt</div><div><b>Demo kamera MWIR dari HJKIR</b><p>Tiga video: n-butana dan propana terlihat di layar thermal, plus tabung &amp; sertifikat gas acuan.</p></div></div>
    <div class="tl-i"><div class="d">21 Okt</div><div><b>Kebutuhan field testing diteruskan ke setiap RU</b><p>Pertamina menyampaikan spesifikasi minimum PC server usulan LGU ke seluruh RU.</p></div></div>
  </div>
</section>""",
    # 5 EMC
    f"""
<section class="slide">
  <div class="kicker">Hasil pre-scan EMC · EN 55032 Class A</div>
  <h2>Semua titik di bawah batas, kecuali frekuensi kerja LoRa</h2>
  <p class="lead">Margin terkecil terhadap batas per uji (makin panjang makin aman; skala penuh = 20 dB). Puncak di 919,6–921 MHz tidak dimasukkan: itu sinyal pancar LoRa perangkat sendiri.</p>
  <div class="emc">{emc_rows()}</div>
  <div class="legend"><span><i class="bad"></i>&lt; 3 dB</span><span><i class="mid"></i>3–6 dB</span><span><i class="good"></i>&gt; 6 dB</span></div>
</section>""",
    # 6 EMC tindak lanjut
    """
<section class="slide">
  <div class="kicker">Pre-scan EMC · tindak lanjut</div>
  <h2>Tiga hal sebelum uji resmi</h2>
  <div class="cards3">
    <div class="card"><div class="tag warn">Konfirmasi lab</div><h3>Frekuensi LoRa 920–921 MHz</h3><p>Software menandai <i>Failed</i> di frekuensi kerja LoRa. Pada standar EMC, pita pemancar umumnya dikecualikan dan dinilai lewat standar radio (ETSI EN 300 220). Perlu konfirmasi Telkom Test House, atau ukur ulang dengan LoRa idle.</p></div>
    <div class="card"><div class="tag bad">Margin tipis</div><h3>GLD di 117–127 MHz</h3><p>Margin hanya <b>0,5–0,95 dB</b>. Sumber emisinya (clock / DC-DC) perlu dicari dan diredam sebelum uji di lab terakreditasi agar tidak gagal.</p></div>
    <div class="card"><div class="tag info">Belum tercakup</div><h3>Cakupan uji</h3><p>Belum ada uji imunitas (EN 61000-6-2), Gateway dan CH kecil belum diuji, dan file belum mencatat model/serial/kondisi operasi. GLD diuji konduksi lewat adaptor AC.</p></div>
  </div>
</section>""",
    # 7 PC server
    """
<section class="slide">
  <div class="kicker">Persiapan field testing setiap RU</div>
  <h2>Spesifikasi minimum PC server</h2>
  <div class="two">
    <div class="spec">
      <div class="spec-r"><span>Bentuk</span><b>PC fisik (bukan VM)</b></div>
      <div class="spec-r"><span>Lokasi</span><b>Ruang server lokal</b></div>
      <div class="spec-r"><span>CPU</span><b>4 core</b></div>
      <div class="spec-r"><span>RAM</span><b>8 GB</b></div>
      <div class="spec-r"><span>Penyimpanan</span><b>SSD 256 GB</b></div>
      <div class="spec-r"><span>Jaringan</span><b>2 port LAN</b> <em>(NIC kedua boleh USB-LAN)</em></div>
    </div>
    <div class="side">
      <h3>Fungsi dua port LAN</h3>
      <p><b>LAN-1</b> → router Wi-Fi 2,4 GHz dari LGU (jaringan field lokal, tanpa internet).</p>
      <p><b>LAN-2</b> → intranet kantor, agar dashboard bisa dibuka dari kantor kilang.</p>
      <h3>Yang perlu dari tiap RU</h3>
      <p>Unit PC aktual, sistem operasi, dan ruang server yang ditunjuk — agar installer LGU disesuaikan sebelum instalasi.</p>
    </div>
  </div>
</section>""",
    # 8 block diagram
    f"""
<section class="slide">
  <div class="kicker">Persiapan field testing setiap RU</div>
  <h2>Lingkup pekerjaan LGU dan Pertamina</h2>
  <div class="diag"><img src="{img('block_diagram.jpg')}" alt="Block diagram lingkup Field dan Building: GLD, CH, Gateway, router Wi-Fi, server, UPS"></div>
  <p class="cap"><b>Biru</b> = disuplai LGU (GLD, Cluster Head, solar cell, Gateway, router Wi-Fi). <b>Kuning</b> = Pertamina (instalasi, mounting support, junction box + PSU 24 VDC, kabel, server, UPS, jaringan IT). Versi final 8 Oktober, tidak berubah.</p>
</section>""",
    # 9 kamera
    f"""
<section class="slide">
  <div class="kicker">Demo kamera MWIR · HJKIR · 20 Oktober</div>
  <h2>Gas hidrokarbon terlihat sebagai gumpalan di citra thermal</h2>
  <div class="cam">
    <figure><img src="{img('butane.jpg')}" alt="Citra thermal kebocoran n-butana dari ujung selang"><figcaption>n-Butana</figcaption></figure>
    <figure><img src="{img('propane.jpg')}" alt="Citra thermal kebocoran propana dari ujung selang"><figcaption>Propana</figcaption></figure>
    <div class="side">
      <p>Gas dilepas dari tabung lewat selang; kamera menangkap gumpalan secara real-time (resolusi 640×512, 25 Hz).</p>
      <p>Video ketiga memperlihatkan tabung dan sertifikat gas acuan DATEN. Nama gas ketiga belum terbaca jelas.</p>
      <div class="note">Ini demo vendor di kantornya, bukan uji LGU/ITB. Konsentrasi, laju bocor, dan jarak tidak disebutkan.</div>
    </div>
  </div>
</section>""",
    # 10 sertifikasi
    """
<section class="slide">
  <div class="kicker">Sertifikasi ATEX / IECEx</div>
  <h2>Berkas sudah di GTS, masuk putaran revisi</h2>
  <div class="two">
    <div class="spec">
      <div class="spec-r"><span>Pemohon &amp; produsen</span><b>PT Galaksi Megatama Indonesia</b></div>
      <div class="spec-r"><span>Usulan marking</span><b>II 2G Ex db IIC T4 Gb</b></div>
      <div class="spec-r"><span>Metode proteksi</span><b>Ex d (flameproof)</b></div>
      <div class="spec-r"><span>Suhu operasi</span><b>−20 °C s/d +60 °C</b></div>
      <div class="spec-r"><span>Kelas suhu T4</span><b>indikasi ±114 °C</b> <em>vs batas efektif 130 °C</em></div>
      <div class="spec-r"><span>Sampel</span><b>GLD2-0x1001</b></div>
    </div>
    <div class="side">
      <h3>Langkah berikut</h3>
      <p>Revisi dossier pada putaran berikut dari GTS: samakan suhu operasi, hapus marking debu, samakan cable entry M20×1,5.</p>
      <p>Lengkapi pengukuran suhu yang belum (DC/DC, induktor, MOSFET; mode alarm/transmit).</p>
      <p>Uji internal di-<i>witness</i> Pertamina dan berita acara — syarat Termin 1 sertifikasi.</p>
    </div>
  </div>
</section>""",
    # 11 keputusan
    """
<section class="slide">
  <div class="kicker">Butir yang perlu disepakati</div>
  <h2>Mohon arahan dan konfirmasi</h2>
  <div class="asks">
    <div class="ask"><span class="n">1</span><div><b>PC server tiap RU</b><p>Unit, OS, dan ruang server yang ditunjuk per RU, beserta PIC IT.</p></div><span class="who">Pertamina / RU</span></div>
    <div class="ask"><span class="n">2</span><div><b>Lingkup "multi-modality"</b><p>Apakah kamera OGI ikut field testing tahap ini, dan di RU mana.</p></div><span class="who">Pertamina</span></div>
    <div class="ask"><span class="n">3</span><div><b>Jadwal instalasi RU IV Cilacap</b><p>Pelaksana instalasi dan konfirmasi tertulis HSE bahwa lokasi termasuk area non-ATEX.</p></div><span class="who">RU IV</span></div>
    <div class="ask"><span class="n">4</span><div><b>Witness uji internal sertifikasi</b><p>Tanggal witness dan format berita acara.</p></div><span class="who">Pertamina + LGU</span></div>
    <div class="ask"><span class="n">5</span><div><b>Tindak lanjut EMC</b><p>Konfirmasi lab soal pita LoRa dan perbaikan margin GLD di ±118 MHz.</p></div><span class="who">LGU</span></div>
  </div>
</section>""",
    # 12 penutup
    """
<section class="slide cover end">
  <div class="cover-band"></div>
  <div class="cover-body">
    <div class="kicker">Terima kasih</div>
    <h1>Diskusi &amp; tanya jawab</h1>
    <p class="sub">PT LAPI Ganesha Utama · Lab IoT &amp; Lab Fisika ITB</p>
  </div>
</section>""",
]

CSS = """
:root{--blue:#2B5FCB;--blue-dk:#1E4499;--char:#262321;--ink:#262321;--ink-soft:#5A5550;--bg:#E9ECF2;--slide:#FFFFFF;
--surf:#F2F5FC;--line:#D5DCEC;--ok:#1F7A43;--mid:#B07A10;--bad:#B4520F;--okbg:#E6F2EB;--midbg:#F6F1DC;--badbg:#FBEEE4;--infobg:#E7ECF8}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--ink:#ECEAE6;--ink-soft:#B3ADA6;--bg:#121110;--slide:#1C1A19;
--surf:#262321;--line:#3A3633;--blue:#6E95F0;--okbg:#1E3326;--midbg:#3A3115;--badbg:#3D2516;--infobg:#22283A;--ok:#5FC488;--mid:#E0B24A;--bad:#F08A4B}}
:root[data-theme="dark"]{--ink:#ECEAE6;--ink-soft:#B3ADA6;--bg:#121110;--slide:#1C1A19;--surf:#262321;--line:#3A3633;--blue:#6E95F0;
--okbg:#1E3326;--midbg:#3A3115;--badbg:#3D2516;--infobg:#22283A;--ok:#5FC488;--mid:#E0B24A;--bad:#F08A4B}
*{box-sizing:border-box;margin:0;padding:0}
html,body{height:100%;background:var(--bg);color:var(--ink);font-family:"Segoe UI",Calibri,system-ui,sans-serif;overflow:hidden}
#stage{position:fixed;inset:0;display:flex;align-items:center;justify-content:center}
#deck{width:1280px;height:720px;position:relative;transform-origin:center}
.slide{position:absolute;inset:0;background:var(--slide);padding:56px 72px 48px;display:none;flex-direction:column;
border-radius:6px;box-shadow:0 8px 40px rgba(0,0,0,.18);overflow:hidden}
.slide.on{display:flex}
.slide::after{content:attr(data-n);position:absolute;right:28px;bottom:18px;font-size:13px;color:var(--ink-soft)}
.kicker{font-size:14px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--blue)}
h2{font-family:Cambria,Georgia,serif;font-size:38px;line-height:1.15;margin:8px 0 26px;color:var(--ink)}
h3{font-size:18px;margin:0 0 8px;color:var(--ink)}
p{font-size:17px;line-height:1.5;color:var(--ink-soft)}
.lead{margin:-10px 0 22px}
.note{margin-top:auto;padding:12px 16px;border-left:4px solid var(--blue);background:var(--infobg);font-size:15px;line-height:1.45;color:var(--ink);border-radius:0 4px 4px 0}
.cover{padding:0;background:var(--char)}
.cover .cover-band{position:absolute;left:0;top:0;bottom:0;width:22px;background:var(--blue)}
.cover-body{margin:auto 0;padding:0 110px}
.cover .kicker{color:#8FB0F5}
.cover h1{font-family:Cambria,Georgia,serif;font-size:60px;color:#fff;margin:18px 0 18px;line-height:1.1}
.cover .sub{color:#D8D4CF;font-size:22px;max-width:900px}
.cover-meta{margin-top:48px;color:#A9A39D;font-size:16px;line-height:1.6}
.cover::after{color:#8a847e}
.agenda{list-style:none;counter-reset:a;display:grid;grid-template-columns:1fr 1fr;gap:16px 40px}
.agenda li{counter-increment:a;display:flex;flex-direction:column;padding:14px 0 14px 58px;position:relative;border-top:1px solid var(--line)}
.agenda li::before{content:counter(a,decimal-leading-zero);position:absolute;left:0;top:12px;font-size:28px;font-weight:700;color:var(--blue)}
.agenda b{font-size:20px}.agenda span{font-size:15px;color:var(--ink-soft);margin-top:2px}
.kpis{display:grid;grid-template-columns:repeat(4,1fr);gap:18px}
.kpi{background:var(--surf);border:1px solid var(--line);border-radius:8px;padding:20px}
.kpi .k{font-size:13px;font-weight:700;text-transform:uppercase;letter-spacing:.08em;color:var(--ink-soft)}
.kpi .v{font-size:38px;font-weight:700;color:var(--blue);margin:10px 0 8px;line-height:1.1}
.kpi .s{font-size:14.5px;line-height:1.45;color:var(--ink-soft)}
.tl{display:flex;flex-direction:column;gap:4px}
.tl-i{display:grid;grid-template-columns:130px 1fr;gap:22px;padding:15px 0;border-top:1px solid var(--line)}
.tl-i .d{font-weight:700;color:var(--blue);font-size:18px}
.tl-i b{font-size:19px}.tl-i p{margin-top:4px;font-size:16px}
.emc{display:flex;flex-direction:column;gap:12px}
.emc-row{display:grid;grid-template-columns:300px 1fr 92px 200px;align-items:center;gap:18px}
.emc-lab b{display:block;font-size:16px}.emc-lab span{font-size:14px;color:var(--ink-soft)}
.emc-bar{height:18px;background:var(--surf);border:1px solid var(--line);border-radius:3px;overflow:hidden}
.emc-bar i{display:block;height:100%}
i.good{background:var(--ok)}i.mid{background:var(--mid)}i.bad{background:var(--bad)}
.emc-val{font-weight:700;font-size:18px;text-align:right}
.emc-val.good{color:var(--ok)}.emc-val.mid{color:var(--mid)}.emc-val.bad{color:var(--bad)}
.emc-note{font-size:14px;color:var(--ink-soft)}
.legend{display:flex;gap:22px;margin-top:auto;font-size:14px;color:var(--ink-soft)}
.legend i{display:inline-block;width:14px;height:14px;border-radius:2px;margin-right:6px;vertical-align:-2px}
.cards3{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}
.card{background:var(--surf);border:1px solid var(--line);border-radius:8px;padding:22px}
.card p{font-size:15.5px}
.tag{display:inline-block;font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:.08em;padding:4px 9px;border-radius:3px;margin-bottom:12px}
.tag.warn{background:var(--midbg);color:var(--mid)}.tag.bad{background:var(--badbg);color:var(--bad)}.tag.info{background:var(--infobg);color:var(--blue)}
.two{display:grid;grid-template-columns:1.05fr 1fr;gap:40px}
.spec{border-top:2px solid var(--char)}
:root[data-theme="dark"] .spec{border-top-color:var(--ink-soft)}
.spec-r{display:grid;grid-template-columns:190px 1fr;padding:13px 0;border-bottom:1px solid var(--line);font-size:17px}
.spec-r span{color:var(--ink-soft)}.spec-r em{color:var(--ink-soft);font-style:normal;font-size:15px}
.side h3{margin-top:4px}.side p{margin-bottom:12px;font-size:16px}.side h3+p{margin-top:0}
.side p+h3{margin-top:18px}
.diag{flex:1;min-height:0;display:flex;justify-content:center;margin-top:-8px}
.diag img{max-width:100%;max-height:100%;object-fit:contain;border:1px solid var(--line);border-radius:4px;background:#fff}
.cap{font-size:14.5px;margin-top:12px}
.cam{display:grid;grid-template-columns:1fr 1fr 0.95fr;gap:22px;align-items:start}
.cam figure img{width:100%;border-radius:6px;display:block}
.cam figcaption{font-weight:700;margin-top:8px;font-size:16px}
.cam .side p{font-size:15.5px}.cam .note{margin-top:10px}
.asks{display:flex;flex-direction:column;gap:2px}
.ask{display:grid;grid-template-columns:46px 1fr 190px;gap:16px;align-items:center;padding:12px 0;border-top:1px solid var(--line)}
.ask .n{width:36px;height:36px;border-radius:50%;background:var(--blue);color:#fff;display:flex;align-items:center;justify-content:center;font-weight:700}
.ask b{font-size:18px}.ask p{font-size:15.5px;margin-top:2px}
.who{font-size:14px;font-weight:700;color:var(--blue);text-align:right}
#bar{position:fixed;left:50%;bottom:10px;transform:translateX(-50%);display:flex;gap:8px;align-items:center;font-size:13px;color:var(--ink-soft);z-index:5}
#bar button{background:var(--slide);color:var(--ink);border:1px solid var(--line);border-radius:4px;padding:5px 12px;cursor:pointer;font:inherit}
@media print{@page{size:1280px 720px;margin:0}html,body{overflow:visible;background:#fff}#bar{display:none}
#stage{position:static;display:block}#deck{transform:none!important;width:auto;height:auto}
.slide{display:flex!important;position:relative;width:1280px;height:720px;border-radius:0;box-shadow:none;page-break-after:always}}
"""

JS = """
const S=[...document.querySelectorAll('.slide')];let i=0;
S.forEach((s,k)=>s.dataset.n=(k+1)+' / '+S.length);
function show(n){i=Math.max(0,Math.min(S.length-1,n));S.forEach((s,k)=>s.classList.toggle('on',k===i));
document.getElementById('pos').textContent=(i+1)+' / '+S.length;try{history.replaceState(null,'','#'+(i+1))}catch(e){}}
function fit(){const d=document.getElementById('deck');const k=Math.min(innerWidth/1300,(innerHeight-40)/740);d.style.transform='scale('+k+')'}
addEventListener('resize',fit);
addEventListener('keydown',e=>{if(['ArrowRight','PageDown',' ','Enter'].includes(e.key)){e.preventDefault();show(i+1)}
else if(['ArrowLeft','PageUp','Backspace'].includes(e.key)){e.preventDefault();show(i-1)}
else if(e.key==='Home')show(0);else if(e.key==='End')show(S.length-1);
else if(e.key==='f')document.documentElement.requestFullscreen&&document.documentElement.requestFullscreen()});
document.getElementById('prev').onclick=()=>show(i-1);document.getElementById('next').onclick=()=>show(i+1);
document.getElementById('theme').onclick=()=>{const r=document.documentElement;
const dark=r.dataset.theme?r.dataset.theme==='dark':matchMedia('(prefers-color-scheme: dark)').matches;r.dataset.theme=dark?'light':'dark'};
fit();show((parseInt(location.hash.slice(1))||1)-1);
"""

HTML = f"""<!doctype html>
<html lang="id">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Rapat GLD 22 Oktober</title>
<style>{CSS}</style>
</head>
<body>
<div id="stage"><div id="deck">
{"".join(SLIDES)}
</div></div>
<div id="bar"><button id="prev" aria-label="Slide sebelumnya">‹</button><span id="pos"></span><button id="next" aria-label="Slide berikutnya">›</button><button id="theme">Tema</button></div>
<script>{JS}</script>
</body>
</html>
"""

OUT.write_text(HTML, encoding="utf-8")
print(OUT, f"{OUT.stat().st_size/1024:.0f} KB", len(SLIDES), "slide")
