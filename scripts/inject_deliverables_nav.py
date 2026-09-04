# -*- coding: utf-8 -*-
import re, os

BASE = r"c:\Users\Win11\OneDrive\Desktop\Documents\GitHub\GLD-V2-Report-2026\Deliverables"

FILES = [
    ("Dashboard_GLD_ProjectManagement.html", "Dashboard Proyek", False),
    ("Datasheet_Sistem_GLD_Arsitektur_ServerJaringan.html", "Datasheet Sistem", False),
    ("JSA_HSE_RU-IV_Cilacap_GLD.html", "Draft JSA/HSE", False),
    ("Knowledge_Graph_GLD.html", "Knowledge Graph", False),
    ("Laporan_Progres_ByDate_GLD.html", "Laporan Progres", False),
    ("Laporan_Detail_Progres_Assessment_FieldTesting_Sep2026.html", "Detail Assessment/Field Testing", False),
    ("Desain_Bracket_L_UBolt_GLD_Mounting.html", "Desain Bracket U-Bolt", False),
    ("Dashboard_Sertifikasi_GLD_ATEX_IECEx.html", "Dashboard Sertifikasi", False),
]

# Dikeluarkan dari navigasi atas permintaan user (4 Sep) - tidak perlu ditampilkan/dinavigasikan:
# Datasheet_Sistem_GLD_Slides_source.html, Notulen_Meeting_GLD_24Jul2026.html, Notulen_Meeting_GLD_30Jul2026.html

NAV_START = "<!-- GLD-NAV-START -->"
NAV_END = "<!-- GLD-NAV-END -->"

def build_nav(current_file):
    items = []
    for fname, label, archived in FILES:
        archived_txt = " <span style=\"opacity:.6;font-size:11px\">(arsip)</span>" if archived else ""
        if fname == current_file:
            items.append(
                f'<span style="background:#1ABB9C;color:#fff;padding:4px 10px;border-radius:5px;'
                f'font-weight:700;white-space:nowrap;">{label}{archived_txt}</span>'
            )
        else:
            items.append(
                f'<a href="{fname}" style="color:#D5DEE7;text-decoration:none;padding:4px 10px;'
                f'border-radius:5px;white-space:nowrap;transition:background .15s;" '
                f'onmouseover="this.style.background=\'#3A4C5E\'" onmouseout="this.style.background=\'transparent\'">'
                f'{label}{archived_txt}</a>'
            )
    items_html = '<span style="opacity:.35;color:#8A97A6">&middot;</span>'.join(items)
    nav = (
        f'{NAV_START}\n'
        f'<div style="background:#2F4050;border-bottom:3px solid #1ABB9C;padding:9px 16px;'
        f'display:flex;flex-wrap:wrap;align-items:center;gap:3px 2px;'
        f'font-family:-apple-system,\'Segoe UI\',Roboto,Arial,sans-serif;font-size:13px;'
        f'position:relative;z-index:99999;">\n'
        f'<span style="font-weight:700;color:#7FE8CC;margin-right:8px;white-space:nowrap;">'
        f'GLD Tahap 2 &mdash; Deliverables</span>\n'
        f'{items_html}\n'
        f'</div>\n'
        f'{NAV_END}\n'
    )
    return nav

def inject(fname):
    path = os.path.join(BASE, fname)
    with open(path, encoding="utf-8") as f:
        data = f.read()

    # remove any previously injected nav (idempotent re-run)
    data = re.sub(re.escape(NAV_START) + r".*?" + re.escape(NAV_END) + r"\n?", "", data, flags=re.S)

    nav_html = build_nav(fname)

    if re.search(r"<body[^>]*>", data, flags=re.I):
        # standalone html file with real <body>
        data = re.sub(r"(<body[^>]*>)", lambda m: m.group(1) + "\n" + nav_html, data, count=1, flags=re.I)
    else:
        # fragment-style artifact body: insert after first </style>
        idx = data.find("</style>")
        if idx == -1:
            raise RuntimeError(f"No </style> or <body> found in {fname}")
        insert_at = idx + len("</style>")
        data = data[:insert_at] + "\n" + nav_html + data[insert_at:]

    with open(path, "w", encoding="utf-8") as f:
        f.write(data)
    print("updated", fname)

for fname, _, _ in FILES:
    inject(fname)
