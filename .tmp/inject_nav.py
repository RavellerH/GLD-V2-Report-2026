# -*- coding: utf-8 -*-
import re, os

BASE = r"c:\Users\WIN10\Documents\GLD-V2-Report-2026\Deliverables"

FILES = [
    ("Dashboard_GLD_ProjectManagement.html", "Dashboard Proyek", False),
    ("Datasheet_Sistem_GLD_Arsitektur_ServerJaringan.html", "Datasheet Sistem", False),
    ("Datasheet_Sistem_GLD_Slides_source.html", "Slide Deck (Arsip)", True),
    ("JSA_HSE_RU-IV_Cilacap_GLD.html", "Draft JSA/HSE", False),
    ("Knowledge_Graph_GLD.html", "Knowledge Graph", False),
    ("Laporan_Progres_ByDate_GLD.html", "Laporan Progres", False),
    ("Notulen_Meeting_GLD_24Jul2026.html", "Notulen 24 Jul", False),
    ("Notulen_Meeting_GLD_30Jul2026.html", "Notulen 30 Jul", False),
]

NAV_START = "<!-- GLD-NAV-START -->"
NAV_END = "<!-- GLD-NAV-END -->"

def build_nav(current_file):
    items = []
    for fname, label, archived in FILES:
        archived_txt = " <span style=\"opacity:.6;font-size:11px\">(arsip)</span>" if archived else ""
        if fname == current_file:
            items.append(
                f'<span style="background:#2B5FCB;color:#fff;padding:4px 10px;border-radius:5px;'
                f'font-weight:700;white-space:nowrap;">{label}{archived_txt}</span>'
            )
        else:
            items.append(
                f'<a href="{fname}" style="color:#D8E2FA;text-decoration:none;padding:4px 10px;'
                f'border-radius:5px;white-space:nowrap;transition:background .15s;" '
                f'onmouseover="this.style.background=\'#39352F\'" onmouseout="this.style.background=\'transparent\'">'
                f'{label}{archived_txt}</a>'
            )
    items_html = '<span style="opacity:.35;color:#89827A">&middot;</span>'.join(items)
    nav = (
        f'{NAV_START}\n'
        f'<div style="background:#262321;border-bottom:3px solid #2B5FCB;padding:9px 16px;'
        f'display:flex;flex-wrap:wrap;align-items:center;gap:3px 2px;'
        f'font-family:-apple-system,\'Segoe UI\',Roboto,Arial,sans-serif;font-size:13px;'
        f'position:relative;z-index:99999;">\n'
        f'<span style="font-weight:700;color:#8FB3FF;margin-right:8px;white-space:nowrap;">'
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
