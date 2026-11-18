# -*- coding: utf-8 -*-
"""Bangun ulang Deliverables/Dashboard_GLD_ProjectManagement_Laporan.html (versi cetak/laporan)
dari data Dashboard_GLD_ProjectManagement.html (dashboard interaktif).

Sumber data:
- array JS dashboard (ACT, DONE, OUT, AI, ISS, RECS, FEED, WSW, RES, RU, EVO, GASES, Kurva-S)
  diekstrak via scripts/extract_dashboard_data.js;
- teks ringkasan eksekutif, chip status, catatan baseline, dan catatan Kurva-S diambil dari HTML dashboard;
- <head> (CSS) dan blok arsitektur (bagian 03) dipertahankan dari file laporan yang ada.

Jalankan ulang setiap kali dashboard interaktif diperbarui:
    python3 scripts/build_dashboard_laporan_html.py
"""
import datetime as dt
import html
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DASH = ROOT / "Deliverables" / "Dashboard_GLD_ProjectManagement.html"
OUT = ROOT / "Deliverables" / "Dashboard_GLD_ProjectManagement_Laporan.html"

BULAN = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September",
         "Oktober", "November", "Desember"]
BLN3 = ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"]


def tgl(d, long=False):
    return f"{d.day} {(BULAN if long else BLN3)[d.month - 1]} {d.year}"


data = json.loads(subprocess.check_output(["node", str(ROOT / "scripts" / "extract_dashboard_data.js")]))
dash = DASH.read_text(encoding="utf-8")
old = OUT.read_text(encoding="utf-8")

y, m, d = (int(x) for x in data["TODAY"].split(","))
TODAY = dt.date(y, m + 1, d)


def D(s):
    return dt.date.fromisoformat(s)


plan = [(D(a), v) for a, v in data["SC"]["plan"]]
act = [(D(a), v) for a, v in data["SC"]["act"]]
fc = [(D(a), v) for a, v in data["SC"]["fc"]]


def plan_at(day):
    for (d0, v0), (d1, v1) in zip(plan, plan[1:]):
        if d0 <= day <= d1:
            return v0 + (day - d0).days / (d1 - d0).days * (v1 - v0)
    return plan[-1][1]


ACT_NOW = act[-1][1]
PLAN_NOW = round(plan_at(TODAY))
GAP = ACT_NOW - PLAN_NOW


def one(pattern, text=dash, flags=re.S):
    mm = re.search(pattern, text, flags)
    if not mm:
        raise SystemExit("pattern not found: " + pattern[:60])
    return mm.group(1).strip()


exec_h3 = one(r'<section class="exec".*?<h3>(.*?)</h3>')
exec_p = one(r'<section class="exec".*?<h3>.*?</h3>\s*<p>(.*?)</p>')
chips = re.findall(r'<span class="sc (g|w)">(.*?)</span>', dash)
baseline = one(r'<p class="baseline-note">(.*?)</p>')
baseline = re.sub(r"^📐\s*", "", baseline)
sc_hint = one(r'<div class="card-head"><h2>Kurva-S: Rencana vs Aktual vs Proyeksi</h2></div>\s*<p class="hint">(.*?)</p>')
ru_sub = one(r'<div class="lab">RU Aktif / Program</div>\s*<div class="val">.*?</div>\s*<div class="sub">(.*?)</div>')
gas_val = one(r'<div class="lab">Gas Capability Gate</div>\s*<div class="val">(.*?)</div>')
gas_sub = one(r'<div class="lab">Gas Capability Gate</div>\s*<div class="val">.*?</div>\s*<div class="sub">(.*?)</div>')
footer_src = one(r"<footer>\s*(.*?)\s*</footer>")

head = old[: old.index("<body>")]
arch = one(r'(<h3>Alur Data End-to-End.*?)\n\n<h3>Progres &amp; Kesehatan Sub-sistem</h3>', old)

e = html.escape
TAG_ST = {"good": ("good", "On/Ahead"), "accent": ("info", "Berjalan"), "warn": ("warn", "Menyusul"),
          "crit": ("crit", "Tertinggal"), "neutral": ("grey", "Belum mulai")}
AI_TAG = {"selesai": "good", "berjalan": "info", "terbuka": "crit", "menunggu": "warn", "terencana": "warn",
          "diusulkan": "warn"}
PRIO = {"t": "Tinggi", "s": "Sedang", "r": "Rendah"}


def fmt_range(s, en):
    a = dt.date(s[0], s[1] + 1, s[2])
    b = dt.date(en[0], en[1] + 1, en[2])
    return f"{a.day} {BLN3[a.month - 1]}&ndash;{b.day} {BLN3[b.month - 1]} {b.year}"


# ---------------------------------------------------------------- KPI counts
ai_counts = {}
for a in data["AI"]:
    ai_counts[a[3]] = ai_counts.get(a[3], 0) + 1
ai_break = " &middot; ".join(f"{v} {k}" for k, v in sorted(ai_counts.items(), key=lambda kv: -kv[1]))
iss_high = sum(1 for i in data["ISS"] if i[2] == "t")

parts = []
parts.append(f"""<body>

<div class="cover">
  <div class="eyebrow">Laporan Dashboard Proyek &middot; GLD Tahap 2</div>
  <h1>Sistem Gas Leak Detection — Laporan Progres &amp; Manajemen Proyek</h1>
  <div class="sub">Pemantauan progres, aktivitas, arsitektur sistem, dan risiko pengembangan GLD Point Sensor Network berbasis multi-sensor MQ, LoRa star-mesh, AI edge, dan catu daya 24 VDC — fokus aktif pilot RU IV Cilacap (area SRU), dengan roadmap rollout 6 Refinery Unit.</div>
  <div class="metaGrid">
    <div class="metaRow">
      <div class="metaCell"><div class="k">Proyek</div><div class="v">GLD Point Sensor Network</div></div>
      <div class="metaCell"><div class="k">Klien / Partner</div><div class="v">Pertamina Patra Niaga</div></div>
      <div class="metaCell"><div class="k">Scope Aktif</div><div class="v">Pilot RU IV Cilacap (SRU)</div></div>
      <div class="metaCell"><div class="k">Status Per</div><div class="v">{tgl(TODAY, True)}</div></div>
    </div>
    <div class="metaRow">
      <div class="metaCell"><div class="k">Survey &amp; MoC</div><div class="v">Survey 9&ndash;10 Agu &middot; MoC 15769 (3 Nov)</div></div>
      <div class="metaCell"><div class="k">Instalasi Fisik</div><div class="v">Belum dimulai &mdash; GLD menunggu sertifikat Ex</div></div>
      <div class="metaCell"><div class="k">Target Implementasi</div><div class="v">Desember 2026 &middot; bergantung sertifikat Ex</div></div>
      <div class="metaCell"><div class="k">Tingkat Kematangan</div><div class="v">TRL-7</div></div>
    </div>
  </div>
  <div class="orgline">LAPI Ganesha Utama &middot; Lab IoT &amp; Lab Fisika ITB &middot; PT Pertamina Patra Niaga / Kilang Pertamina Internasional</div>
</div>

<section id="s1">
<h2><span class="secnum">01</span>Ringkasan Eksekutif</h2>
<p class="intro">Status eksekutif, indikator kunci, dan pemetaan progres-vs-outstanding — dibaca dahulu sebelum masuk ke detail jadwal, arsitektur, atau risiko di bagian berikutnya.</p>

<h3>{exec_h3}</h3>
<p>{exec_p}</p>

<table class="kpi-table">
<tr>
  <td style="width:16.6%"><div class="kv">{ACT_NOW}%</div><div class="kl">Progres Pilot Cilacap</div><div class="kd">Rencana {PLAN_NOW}% ({TODAY.day} {BLN3[TODAY.month - 1]}) &middot; {GAP:+d} poin</div></td>
  <td style="width:16.6%"><div class="kv">1 / 6</div><div class="kl">RU Aktif / Program</div><div class="kd">{ru_sub}</div></td>
  <td style="width:16.6%"><div class="kv">0</div><div class="kl">Blocker Kritis Aktif</div><div class="kd">Gate eksternal (sertifikat Ex) dicatat di Outstanding</div></td>
</tr>
<tr>
  <td><div class="kv">{len(data['AI'])}</div><div class="kl">Action Items</div><div class="kd">{ai_break}</div></td>
  <td><div class="kv">{len(data['ISS'])}</div><div class="kl">Isu &amp; Risiko</div><div class="kd">{iss_high} prioritas tinggi</div></td>
  <td><div class="kv">{gas_val}</div><div class="kl">Gas Capability Gate</div><div class="kd">{gas_sub}</div></td>
</tr>
</table>

<h3>Status ringkas per topik</h3>
<ul class="plain done">
""")
for kind, txt in chips:
    if kind == "g":
        parts.append(f"<li>{re.sub(r'^✓ ', '', txt)}</li>\n")
parts.append('</ul>\n<ul class="plain out">\n')
for kind, txt in chips:
    if kind == "w":
        parts.append(f"<li>{re.sub(r'^⚠ ', '', txt)}</li>\n")
parts.append(f"""</ul>

<h3>Progres — Tercapai <span class="tag good">{len(data['DONE'])} item</span></h3>
<p class="intro">Capaian yang telah diverifikasi hingga {tgl(TODAY)}.</p>
<ol class="numbered">
""")
for (txt,) in data["DONE"]:
    parts.append(f"<li>{txt}</li>\n")
parts.append(f"""</ol>

<h3>Outstanding — Perlu Perhatian <span class="tag warn">{len(data['OUT'])} item</span></h3>
<p class="intro">Item terbuka, blocker, dan gate menuju kesiapan lapangan — disajikan terbuka untuk partner.</p>
<table>
<thead><tr><th style="width:8%">Kategori</th><th>Deskripsi</th></tr></thead>
<tbody>
""")
for txt, kind, lab in data["OUT"]:
    parts.append(f'<tr><td><span class="tag {"warn" if kind == "gate" else "info"}">{lab}</span></td><td>{txt}</td></tr>\n')
parts.append(f"""</tbody>
</table>

<div class="callout">
<b>Baseline resmi:</b> {re.sub(r"^<b>Baseline resmi:</b>\s*", "", baseline)}
</div>
</section>

<section id="s2">
<h2><span class="secnum">02</span>Jadwal &amp; Cakupan</h2>
<p class="intro">Progres kumulatif terhadap baseline resmi, timeline 12 aktivitas, dan cakupan perangkat di 6 Refinery Unit.</p>

<h3>Kurva-S: Rencana vs Aktual vs Proyeksi</h3>
<p>{sc_hint}</p>
<table>
<thead><tr><th>Tanggal</th><th class="num">Rencana / Baseline</th><th class="num">Aktual</th><th class="num">Proyeksi bersyarat</th><th>Catatan</th></tr></thead>
<tbody>
""")
dates = sorted({x for x, _ in plan} | {x for x, _ in act} | {x for x, _ in fc})
pmap, amap, fmap = dict(plan), dict(act), dict(fc)
for day in dates:
    pv = f"{pmap[day]}%" if day in pmap else (f"{round(plan_at(day))}%" if day == TODAY else "&mdash;")
    av = f"<b>{amap[day]}%</b>" if day == TODAY else (f"{amap[day]}%" if day in amap else "&mdash;")
    fv = f"{fmap[day]}%" if day in fmap and day != TODAY else "&mdash;"
    note = ""
    if day == TODAY:
        note = f"Hari ini &middot; {GAP:+d} poin"
    elif day == dt.date(2026, 6, 1):
        note = "Kick-off"
    elif day == dt.date(2026, 12, 31):
        note = "Target implementasi program"
    elif day == dt.date(2027, 2, 28):
        note = "Akhir program 9 bulan"
    elif day in amap and day not in pmap:
        note = "Titik assessment"
    parts.append(f'<tr><td>{tgl(day)}</td><td class="num">{pv}</td><td class="num">{av}</td><td class="num">{fv}</td><td>{note}</td></tr>\n')
parts.append("""</tbody>
</table>

<h3>Timeline Resmi 9 Bulan &amp; Milestone (12 Aktivitas)</h3>
<p>Rentang mengikuti Deck Kick-Off (Jun 2026 &ndash; Feb 2027). Kolom target = progres yang semestinya tercapai per tanggal laporan menurut rentang rencana.</p>
<table>
<thead><tr><th style="width:4%">#</th><th>Aktivitas</th><th>Periode Rencana</th><th class="num">% Target</th><th class="num">% Aktual</th><th>Status</th></tr></thead>
<tbody>
""")
for a in data["ACT"]:
    cls, lab = TAG_ST[a["st"]]
    parts.append(f'<tr><td>{a["id"]:02d}</td><td>{e(a["name"])}</td><td>{fmt_range(a["s"], a["e"])}</td>'
                 f'<td class="num">{a["plan"]}%</td><td class="num">{a["act"]}%</td><td><span class="tag {cls}">{lab}</span></td></tr>\n')
parts.append("""</tbody>
</table>
<p class="intro">Milestone: """ + " &middot; ".join(
    f'{dt.date(g["d"][0], g["d"][1] + 1, g["d"][2]).day} {BLN3[g["d"][1]]} — {e(g["lab"])}{"" if g["done"] or "✓" in g["lab"] else " (belum)"}'
    for g in data["GMILES"]) + """</p>

<h3>Cakupan Deployment &middot; Pilot Cilacap + Roadmap 6 RU</h3>
<p>Kebutuhan perangkat per RU (scope LGU, tabel alokasi). Untuk RU IV, MoC 15769 menetapkan lingkup field test SRU 4 GLD / 5 CH / 1 GW — berbeda dengan tabel alokasi (3 GLD / 2 CH), perlu disepakati. Rollout berikutnya disiapkan untuk RU VI Balongan (rapat koordinasi 13 Nov).</p>
<table>
<thead><tr><th>RU</th><th>Lokasi</th><th class="num">Gas Sensor</th><th class="num">Cluster Head</th><th class="num">Gateway</th><th class="num">Solar CH</th><th class="num">Solar GW</th><th>Status</th></tr></thead>
<tbody>
""")
tot = [0] * 5
for r in data["RU"]:
    for i in range(5):
        tot[i] += r[2 + i]
    st = '<span class="tag good">Aktif &middot; Pilot</span>' if r[7] == "active" else (
        '<span class="tag info">Roadmap &middot; persiapan</span>' if r[0] == "RU VI" else '<span class="tag info">Roadmap</span>')
    name = f"<b>{r[0]} &#9679;</b>" if r[7] == "active" else r[0]
    parts.append(f'<tr><td>{name}</td><td>{r[1]}</td>' + "".join(f'<td class="num">{r[2 + i]}</td>' for i in range(5)) + f"<td>{st}</td></tr>\n")
parts.append('<tr><td><b>TOTAL</b></td><td><b>6 RU</b></td>' + "".join(f'<td class="num"><b>{t}</b></td>' for t in tot) + "<td></td></tr>\n")
parts.append(f"""</tbody>
</table>
</section>

<section id="s3">
<h2><span class="secnum">03</span>Arsitektur &amp; Kesiapan</h2>
<p class="intro">Alur data end-to-end, pemetaan repositori, kesehatan tiap sub-sistem, dan kesiapan sumber daya program.</p>

{arch}

<h3>Progres &amp; Kesehatan Sub-sistem</h3>
<p>Lensa teknis (kesiapan sub-sistem) sebagai pelengkap timeline aktivitas.</p>
<table>
<thead><tr><th>Sub-sistem</th><th class="num">Bobot</th><th class="num">Aktual</th><th class="num">Rencana</th><th>Status</th></tr></thead>
<tbody>
""")
for w in data["WSW"]:
    cls, lab = {"good": ("good", "On/Ahead"), "accent": ("info", "Berjalan"), "warn": ("warn", "Tertinggal"),
                "crit": ("crit", "Kritis")}[w["st"]]
    parts.append(f'<tr><td>{e(w["n"])}</td><td class="num">{w["w"]}%</td><td class="num">{w["act"]}%</td><td class="num">{w["plan"]}%</td><td><span class="tag {cls}">{lab}</span></td></tr>\n')
parts.append("""</tbody>
</table>

<h3>Kesiapan Sumber Daya (Resource Readiness)</h3>
<p>Matriks kesiapan sumber daya dari Deck Kick-Off — dikonfirmasi saat kickoff &amp; dimonitor via milestone review.</p>
<table>
<thead><tr><th>Kategori</th><th>Status</th><th>Dependensi</th></tr></thead>
<tbody>
""")
for r in data["RES"]:
    cls = {"ready": "good", "confirm": "warn", "prep": "info"}[r[2]]
    parts.append(f'<tr><td>{r[0]}</td><td><span class="tag {cls}">{r[3]}</span></td><td>{r[1]}</td></tr>\n')
parts.append("""</tbody>
</table>
</section>

<section id="s4">
<h2><span class="secnum">04</span>Aktivitas &amp; Model AI</h2>
<p class="intro">Kronologi kegiatan terbaru, dan evolusi dataset &amp; metode model AI.</p>

<h3>Log Aktivitas Terbaru</h3>
<div class="actlog">
""")
for f in data["FEED"][:16]:
    title = f.get("t") or "Catatan"
    tag = f" &middot; {f['tag']}" if f.get("tag") else ""
    parts.append(f'<div class="actitem"><div><span class="ad">{f["d"]}{tag}</span><span class="ah">{title}</span></div><div class="ab">{f["b"]}</div></div>\n')
gas_rows = "".join(f'<tr><td>{n}</td><td class="num">{v:,}</td></tr>\n'.replace(",", ".") for n, v in data["GASES"])
parts.append(f"""</div>

<h3>Evolusi Data &amp; Metode Model</h3>
<p>Rekap dataset GLD-F001 (15 Jul) dan perkembangan metode AI — dari Tahap 1 hingga metode saat ini.</p>
<table>
<thead><tr><th>Jenis Gas / Sesi</th><th class="num">Jumlah Sampel</th></tr></thead>
<tbody>
{gas_rows}</tbody>
</table>
<table>
<thead><tr><th style="width:4%">#</th><th>Tahap</th><th>Tanggal</th><th>Status</th><th>Keterangan</th></tr></thead>
<tbody>
""")
for i, ev in enumerate(data["EVO"], 1):
    cls = {"done": "good", "now": "info"}.get(ev["tagcls"], "grey")
    parts.append(f'<tr><td>{i}</td><td>{ev["n"]}</td><td>{ev["d"]}</td><td><span class="tag {cls}">{ev["tag"]}</span></td><td>{ev["b"]}</td></tr>\n')
parts.append(f"""</tbody>
</table>
</section>

<section id="s5">
<h2><span class="secnum">05</span>Risiko &amp; Tindak Lanjut</h2>
<p class="intro">Register action item, daftar isu &amp; risiko, serta rekomendasi tindak lanjut.</p>

<h3>Blocker Kritis</h3>
<div class="callout good">
<b>&#10003; Tidak ada blocker teknis kritis aktif.</b> Autonomi baterai GLD, TPL5010, dan DC converter dideprioritaskan (fokus 24 VDC). Jalur kritis jadwal lapangan saat ini adalah <b>gate eksternal sertifikat Ex</b> untuk titik GLD di area SRU (HAC/MoC 15769) — dicatat di Outstanding dan Isu &amp; Risiko, bukan blocker teknis.
</div>

<h3>Action Item Register <span class="tag info">{len(data['AI'])} item</span></h3>
<table>
<thead><tr><th style="width:4%">#</th><th>Tindakan</th><th>Penanggung Jawab</th><th>Prioritas</th><th>Status</th></tr></thead>
<tbody>
""")
for i, a in enumerate(data["AI"], 1):
    lab = a[4]
    cls = "grey" if "Dideprioritaskan" in lab else AI_TAG.get(a[3], "info")
    parts.append(f'<tr><td>{i}</td><td>{e(a[0])}</td><td>{e(a[1])}</td><td>{PRIO[a[2]]}</td><td><span class="tag {cls}">{e(lab)}</span></td></tr>\n')
parts.append(f"""</tbody>
</table>

<h3>Daftar Isu &amp; Risiko <span class="tag info">{len(data['ISS'])} item</span></h3>
<table>
<thead><tr><th style="width:4%">#</th><th>Isu / Risiko</th><th>Keterangan</th><th>Prioritas</th></tr></thead>
<tbody>
""")
for i, s in enumerate(data["ISS"], 1):
    cls = {"t": "crit", "s": "warn", "r": "grey"}[s[2]]
    parts.append(f'<tr><td>{i}</td><td>{e(s[0])}</td><td>{e(s[1])}</td><td><span class="tag {cls}">{s[3]}</span></td></tr>\n')
parts.append("""</tbody>
</table>

<h3>Rekomendasi</h3>
<ol class="numbered">
""")
for r in data["RECS"]:
    parts.append(f"<li>{r}</li>\n")
parts.append(f"""</ol>
</section>

<footer>
{footer_src}<br><br>
Dokumen ini adalah versi laporan tertulis (report-format) dari Dashboard Proyek GLD interaktif (Dashboard_GLD_ProjectManagement.html), dibangun otomatis dari data dashboard tersebut oleh scripts/build_dashboard_laporan_html.py — disusun sebagai teks/tabel untuk kebutuhan cetak &amp; distribusi, bukan tangkapan layar.
</footer>

</body>
</html>
""")

OUT.write_text(head + "".join(parts), encoding="utf-8")
print("written", OUT)
