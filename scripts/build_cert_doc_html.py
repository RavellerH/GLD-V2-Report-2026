# -*- coding: utf-8 -*-
import base64, os

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PHOTO_DIR = os.path.join(REPO, "scripts", "assets", "cert_doc_photos")
SCHEMATIC_DIR = os.path.join(REPO, "scripts", "assets", "cert_doc_schematics")
OUT_PATH = os.path.join(REPO, "Deliverables", "Dokumen_Teknis_Sertifikasi_GLD_IECEx_ATEX.html")
STYLE_SOURCE = os.path.join(REPO, "Deliverables", "Dashboard_Sertifikasi_GLD_ATEX_IECEx.html")

def b64(fn):
    with open(os.path.join(PHOTO_DIR, fn), "rb") as f:
        return base64.b64encode(f.read()).decode("ascii")

def b64_schematic(fn):
    with open(os.path.join(SCHEMATIC_DIR, fn), "rb") as f:
        return base64.b64encode(f.read()).decode("ascii")

# ---- reuse the visual design system (CSS) already established for this document family ----
src = open(STYLE_SOURCE, encoding="utf-8").read()
style_start = src.find(":root{")
style_end = src.find("</style>")
css_body = src[style_start:style_end]

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
.letterhead{background:#1A2B3D;color:#fff;padding:14px 20px;margin:-30px -40px 26px;display:flex;flex-direction:column;gap:2px}
.letterhead b{font-size:16px;letter-spacing:.02em}
.letterhead span{font-size:11.5px;color:#C7D2E0}
.doccontrol{border:1px solid var(--line);border-radius:var(--radius);overflow:hidden;margin:14px 0 0}
.doccontrol .row{display:grid;grid-template-columns:170px 1fr;border-bottom:1px solid var(--line)}
.doccontrol .row:last-child{border-bottom:none}
.doccontrol .row .k{background:var(--surface-2);padding:8px 12px;font-size:11px;font-weight:700;color:var(--ink-soft);text-transform:uppercase;letter-spacing:.02em}
.doccontrol .row .v{padding:8px 12px;font-size:12.5px;color:var(--ink);background:var(--surface)}
.print-footer{display:none}
@media print{
  .tbl-scroll{overflow-x:visible !important;border:none !important}
  table{min-width:0 !important;table-layout:fixed !important;width:100% !important}
  table td,table th{word-break:break-word}
  .status{white-space:normal !important;display:inline-block}
  .photogrid{grid-template-columns:repeat(3,1fr) !important}
  figure.photo{break-inside:avoid}
  .zone{break-inside:auto}
  .subhead{break-after:avoid}
  .tagrow{display:none !important}
  .letterhead{margin:0 0 22px}
  .print-footer{display:block;position:fixed;bottom:0;left:0;right:0;font-size:8.5px;color:#8A97A6;
    border-top:1px solid #D7DADE;padding:6px 40px;background:#fff}
}
"""

css_full = css_body + extra_css

# ---- photographs ----
photos = [
    ("3._Motherboard_ModulSensor_PenutupMesh_Casing_Antena_ModulAlarm.jpg",
     "Complete unit &mdash; front view",
     "The fully assembled Node Sensor (GLD): the main enclosure (blue) with sensor mesh cover, external LoRa antenna, and a visual alarm module (cylindrical housing, red lens) mounted on the right side of the enclosure."),
    ("Casing_Belakang.jpg",
     "Complete unit &mdash; alternate angle",
     "An alternate view of the assembled unit, showing the position of the antenna, alarm module, and the cable-gland side of the enclosure."),
    ("PenutupMesh_Casing.jpg",
     "Complete unit &mdash; front view (without antenna and alarm module)",
     "The main enclosure with the sensor mesh cover installed, shown in a flat front view illustrating the enclosure shape and its four mounting bolt holes."),
    ("1._Motherboard_Casing.jpg",
     "Key component &mdash; PCB inside enclosure (before sensor modules)",
     "The main PCB installed inside the enclosure prior to gas sensor module installation. The ESP32-S3-WROOM-1U microcontroller, LoRa radio module, and power circuitry are visible."),
    ("2._Motherboard_ModulSensor_Casing.jpg",
     "Key component &mdash; PCB with eight gas sensor modules",
     "The same PCB with eight channels of MQ-series gas sensors (MQ-2, MQ-3B, MQ-4, MQ-5, MQ-6, MQ-7B, MQ-8, MQ-135) installed around the central microcontroller."),
    ("ModulAlarm.jpg",
     "Key component &mdash; visual alarm module (close-up)",
     "The visual alarm (beacon/strobe) module, constructed of metal with a red lens, connected to the main enclosure via a dedicated cable gland."),
    ("PenutupMesh.jpg",
     "Key component &mdash; sensor mesh cover (close-up)",
     "The metal mesh cover that protects the gas sensing elements while serving as a diffusion path for gas to reach the sensors beneath."),
]
photo_cards = []
for fn, title, desc in photos:
    data = b64(fn)
    photo_cards.append(f'<figure class="photo">\n<img src="data:image/jpeg;base64,{data}" alt="{title}" loading="lazy">\n<figcaption><b>{title}</b><span>{desc}</span></figcaption>\n</figure>')
photos_html = "\n".join(photo_cards)

schematic_sheets = [
    ("01-diagram.png", "Sheet 1 of 9 &mdash; Overall architecture",
     "Power input, power distribution, analog acquisition, sensor control, main control (ESP32-S3), and external interfaces (alarm, RS-485, LoRa antenna, programming/configuration)."),
    ("02-diagram.png", "Sheet 2 of 9 &mdash; Main power",
     "Main power input rails and distribution: +5 V / +5VA analog, 3.3 V, and +24 V for the alarm circuit."),
    ("03-diagram.png", "Sheet 3 of 9 &mdash; Always-on power",
     "The always-on power domain that remains active independent of the main control state."),
    ("04-diagram.png", "Sheet 4 of 9 &mdash; Sensor module",
     "The external gas sensor module: 8 analog channels with per-channel I2C enable, including the sensor, DAC, and power-switch sub-blocks."),
    ("05-diagram.png", "Sheet 5 of 9 &mdash; Analog acquisition",
     "The 8-channel analog acquisition front end: analog inputs, ADC (ADS1256), reference, and VMID biasing."),
    ("06-diagram.png", "Sheet 6 of 9 &mdash; I2C &amp; sensor control",
     "I2C channel selection (TCA9548A), per-channel sensor enable (PCF8574), and the temperature/humidity sensor (SHT40)."),
    ("07-diagram.png", "Sheet 7 of 9 &mdash; ESP32 connections",
     "Main controller (ESP32-S3) interface map: SPI to the ADC, I2C to sensor/control, UART for USB and RS-485, and GPIO for alarm, power, button, and LED."),
    ("08-diagram.png", "Sheet 8 of 9 &mdash; Alarm &amp; status",
     "Alarm output and status-indication circuitry driven from the main controller."),
    ("09-diagram.png", "Sheet 9 of 9 &mdash; System flow",
     "Overall signal and data flow across the board, summarizing how the preceding eight sheets connect end to end."),
]
schematic_cards = []
for fn, title, desc in schematic_sheets:
    data = b64_schematic(fn)
    schematic_cards.append(f'<figure class="photo">\n<img src="data:image/png;base64,{data}" alt="{title}" loading="lazy">\n<figcaption><b>{title}</b><span>{desc}</span></figcaption>\n</figure>')
schematics_html = "\n".join(schematic_cards)

pcb_layout_b64 = b64_schematic("10-pcb-layout.png")
pcb_3d_b64 = b64_schematic("11-pcb-3d-render.png")

DRAWING_DIR = os.path.join(REPO, "scripts", "assets", "cert_doc_drawings")
def b64_drawing(fn):
    with open(os.path.join(DRAWING_DIR, fn), "rb") as f:
        return base64.b64encode(f.read()).decode("ascii")
bracket_drawing_b64 = b64_drawing("bracket-mounting-drawing.png")

import csv
BOM_DIR = os.path.join(REPO, "scripts", "assets", "cert_doc_bom")

def load_bom(fn):
    with open(os.path.join(BOM_DIR, fn), encoding="utf-8") as f:
        rows = list(csv.reader(f))
    return rows[1:]  # skip header: ID,Name,Designator,Footprint,Quantity,Manufacturer Part,Manufacturer,Supplier,Supplier Part,Price

def bom_rows_html(rows):
    out = []
    for r in rows:
        _id, name, designator, footprint, qty, mpn, mfr, supplier, supplier_part, price = (r + [""] * 10)[:10]
        lcsc = supplier_part if supplier == "LCSC" and supplier_part else "&mdash;"
        mfr_disp = mfr.split("(")[0].strip() if mfr else "&mdash;"
        mpn_disp = mpn if mpn else "&mdash;"
        out.append(f"<tr><td>{designator}</td><td>{name}</td><td>{qty}</td><td>{mfr_disp}</td><td>{mpn_disp}</td><td>{lcsc}</td></tr>")
    return "\n".join(out)

mb_rows = load_bom("motherboard.csv")
sb_rows = load_bom("sensorboard.csv")
mb_bom_rows = bom_rows_html(mb_rows)
sb_bom_rows = bom_rows_html(sb_rows)
mb_lines, mb_qty = len(mb_rows), sum(int(r[4]) for r in mb_rows)
sb_lines, sb_qty = len(sb_rows), sum(int(r[4]) for r in sb_rows)

# ============================================================
# BODY (English, professional submission document)
# ============================================================
body = f'''<meta charset="utf-8">
<title>IECEx/ATEX Technical Certification Document &mdash; GLD V2</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
{css_full}
</style>
<div class="shell">
<nav class="side" id="side">
  <div class="side-brand">
    <span class="brandmark"></span>
    <div class="brandtext"><b>Technical Certification Document</b><small>IECEx/ATEX &middot; GLD V2</small></div>
  </div>
  <div class="side-meta">
    <div class="sm-row"><span class="k">Revision</span><span class="v">Draft 0.1</span></div>
    <div class="sm-row"><span class="k">Date</span><span class="v">11 Sep 2026</span></div>
    <div class="sm-row"><span class="k">Status</span><span class="v">Working document</span></div>
    <div class="sm-row"><span class="k">Scope</span><span class="v">Node Sensor (GLD)</span></div>
  </div>
  <ul class="checklist-toc">
    <li><a href="#about"><span class="st done">&#9679;</span> About this document</a></li>
    <li><a href="#s1"><span class="st pending">&#9675;</span> 1. Basic Information</a></li>
    <li><a href="#s2"><span class="st done">&#9679;</span> 2. Technical Documentation</a></li>
    <li><a class="sub" href="#s2-1"><span class="st done">&#9679;</span> 2.1 Product Description</a></li>
    <li><a class="sub" href="#s2-2"><span class="st done">&#9679;</span> 2.2 Name, Model &amp; Specification</a></li>
    <li><a class="sub" href="#s2-3"><span class="st done">&#9679;</span> 2.3 Functional &amp; Technical Parameters</a></li>
    <li><a class="sub" href="#s2-4"><span class="st done">&#9679;</span> 2.4 Product Photographs</a></li>
    <li><a class="sub" href="#s2-5"><span class="st done">&#9679;</span> 2.5 Installation Environment</a></li>
    <li><a class="sub" href="#s2-6"><span class="st done">&#9679;</span> 2.6 Design &amp; Manufacturing (a&ndash;i)</a></li>
    <li><a href="#s3"><span class="st done">&#9679;</span> 3. Sample Information</a></li>
  </ul>
  <div class="side-foot">
    <button class="themebtn" id="themebtn">&#9788; Toggle light/dark theme</button>
  </div>
</nav>
<main class="content">

<div class="letterhead">
  <b>PT LAPI GANESHA UTAMA</b>
  <span>In technical partnership with the Institute of Technology Bandung</span>
</div>

<div class="masthead">
  <p class="doclabel" style="margin-bottom:10px">Technical Certification Document</p>
  <h1>IECEx/ATEX Certification Document &mdash; Gas Leak Detector (GLD) V2</h1>
  <p class="subtitle">Prepared in direct reference to the <i>IECEx/ATEX Certification Information Requirements</i> issued by the certification body (ExCB) &mdash; covering Section <b>2, Technical Documentation</b> (Items 1&ndash;6: product description; name, model, and specification list; functional description and technical parameters; product photographs; intended use and installation environment; and design and manufacturing information) and Section <b>3, Sample Information</b>. Section 1, Basic Information (Application and Organization), remains to be completed in a subsequent revision.</p>
  <div class="doccontrol">
    <div class="row"><div class="k">Document no.</div><div class="v">LGU/GLD/IECEX-TDF/2026-001</div></div>
    <div class="row"><div class="k">Revision</div><div class="v">0.1</div></div>
    <div class="row"><div class="k">Date</div><div class="v">11 September 2026</div></div>
    <div class="row"><div class="k">Status</div><div class="v">Working Document &mdash; Draft for Internal Review</div></div>
    <div class="row"><div class="k">Classification</div><div class="v">Confidential &mdash; prepared for ATEX/IECEx certification body (ExCB) submission</div></div>
    <div class="row"><div class="k">Certification subject</div><div class="v">Node Sensor (GLD) &mdash; V2</div></div>
    <div class="row"><div class="k">Manufacturer</div><div class="v">PT LAPI Ganesha Utama</div></div>
    <div class="row"><div class="k">Technical partner</div><div class="v">Institute of Technology Bandung</div></div>
    <div class="row"><div class="k">Reference checklist</div><div class="v">IECEx/ATEX Certification Information Requirements</div></div>
  </div>
</div>
<div class="print-footer">LGU/GLD/IECEX-TDF/2026-001 &middot; Rev. 0.1 &mdash; IECEx/ATEX Certification Document, Gas Leak Detector (GLD) V2 &mdash; Confidential</div>

<section class="zone" id="about">
  <div class="zone-head"><span class="zn">&#8226;</span><h2>About this document</h2></div>
  <p class="lede">This document is a working technical file prepared to satisfy Section <b>&ldquo;2. Technical Documentation&rdquo;</b> and Section <b>&ldquo;3. Sample Information&rdquo;</b> of the official <i>IECEx/ATEX Certification Information Requirements</i> checklist issued by the certification body (ExCB). The table of contents on the left follows the complete structure of the original checklist (Sections 1&ndash;3); Section 1 (Basic Information) remains pending and will follow in a subsequent revision.</p>
  <div class="banner info"><span class="ic">&#9432;</span><div><b>Scope of this document.</b> This is a compilation of design evidence and an honest readiness assessment against the ExCB checklist, prepared in support of a future submission &mdash; it is not itself a certificate and does not constitute self-certification. The final enclosure/casing (material selection, manufacture, gasket, and cable entry) is being developed by an external mechanical/casing partner and is not yet in the authors&rsquo; possession; items that depend on that design (material datasheets, manufacturing process description, explosion-protection calculations) are reported as not yet available for that reason, not because the work has stalled. The product is still at from-scratch development/prototype stage &mdash; no finalized, serialized units exist yet, which is why a formal sample register (Section 3.1) is not yet available either.</div></div>

  <div class="enchecklist">Original excerpt, Section 2 &amp; 3 &mdash; source: <span class="mono">IECEx ATEX Certification Information Requirements</span> (ExCB):<br>
  &ldquo;1) Detailed product description; 2) Product name, model, and specification list; 3) Complete and clear functional description and technical parameters (electrical parameters, mechanical parameters, etc.); 4) Clear product photos (overall and key components); 5) Description of intended use and installation environment (e.g., gas group IIC/IIB/IIA if applicable, temperature group T1&ndash;T6, ambient temperature range, area classification 0/1/2 or 20/21/22); 6) Design and manufacturing information [a&ndash;i: drawings, BOM, material datasheets, manufacturing process, explosion-protection calculations, temperature group calculation, usage and installation instructions, nameplate information, Ex component certificates]. 3. Sample Information: 1) model, serial number, and status of the sample; 2) necessary test fixtures or auxiliary equipment.&rdquo;</div>
</section>

<section class="zone" id="s1">
  <div class="zone-head"><span class="zn">1</span><h2>Basic Information (Application and Organization)</h2></div>
  <p class="lede">Covers the application form, business license/company registration, organizational chart and contact information, manufacturing facility address and profile, and (where applicable) ISO 9001 certification.</p>
  <div class="banner info"><span class="ic">&#9675;</span><div><b>Not yet prepared in this revision.</b> To be completed in a subsequent revision.</div></div>
</section>

<section class="zone" id="s2">
  <div class="zone-head"><span class="zn">2</span><h2>Technical Documentation</h2></div>
  <p class="lede">Six items per the original checklist (1&ndash;6, with Item 6 comprising sub-items a&ndash;i). This revision addresses the complete section: Items 1&ndash;6.</p>

  <div class="subhead" id="s2-1"><h3>2.1 &middot; Detailed Product Description</h3></div>
  <p class="lede">The Gas Leak Detector (GLD) is an IoT-based, multi-sensor gas leak detection device designed for the early detection of flammable and process gases in oil &amp; gas refinery environments (process units, tank farms, pipe racks, and storage/loading-unloading areas). This document addresses the GLD unit itself as the subject of the current IECEx/ATEX certification.</p>
  <p class="lede">Functionally, the GLD integrates eight channels of metal-oxide semiconductor gas sensors (MQ series), an edge-AI microcontroller/processor (ESP32-S3), and a LoRa radio module (star-topology wireless transmission) within a single fixed-point unit installed at locations with gas-leak risk. An on-device AI gas-classification model runs directly on the unit so that detection decisions do not depend on a continuous connection to a central server. When gas concentration exceeds a defined threshold, the unit triggers a local alarm (an integrated visual/audible alarm module) and simultaneously transmits an alarm notification over the LoRa network to the operator dashboard.</p>
  <p class="lede">The enclosure is designed for hazardous-area deployment at refinery sites, using metal materials (aluminum alloy and stainless steel &mdash; no plastic or PVC) and mounted via an L-bracket to existing structures without drilling or welding. <b>Important:</b> this design-intent statement does not constitute a claim that the enclosure has passed testing or has been Ex-certified &mdash; the explosion-protection scheme, gas group, temperature class, and target installation zone will be addressed in Section 2.5 (to follow).</p>
  <p class="lede">The current production power configuration is continuous 24 VDC, supplied via an AC/DC adapter connected to the site electrical supply. A portable battery power path (Li-ion 18650) remains under development (R&amp;D) and has not become a deployed production configuration.</p>

  <div class="subhead" id="s2-2"><h3>2.2 &middot; Product Name, Model, and Specification List</h3></div>
  <div class="speclist">
    <div class="spec"><span class="k">Product name</span><span class="v">Gas Leak Detector (GLD) &mdash; Node Sensor</span></div>
    <div class="spec"><span class="k">Model / version</span><span class="v">GLD V2 (Version 2)</span></div>
    <div class="spec"><span class="k">Manufacturer</span><span class="v">PT LAPI Ganesha Utama</span></div>
    <div class="spec"><span class="k">Technical development partner</span><span class="v">Institute of Technology Bandung &mdash; IoT Laboratory &amp; Physics Laboratory</span></div>
    <div class="spec"><span class="k">End client / program owner</span><span class="v">PT Pertamina Patra Niaga (initial deployment site: Refinery Unit IV, Cilacap)</span></div>
    <div class="spec"><span class="k">Primary function</span><span class="v">Acquisition of 8-channel gas sensor data and LoRa transmission</span></div>
    <div class="spec"><span class="k">Microcontroller</span><span class="v">ESP32-S3-WROOM-1U-N16R8</span></div>
    <div class="spec"><span class="k">LoRa radio module</span><span class="v">E22-900MM22S</span></div>
    <div class="spec"><span class="k">Dimensions (L&times;W&times;H)</span><span class="v">200 &times; 90 &times; 290 mm</span></div>
    <div class="spec"><span class="k">Enclosure material</span><span class="v">Aluminum alloy + stainless steel</span></div>
  </div>
  <p class="lede" style="font-size:12px">Source: official product technical datasheet (Institute of Technology Bandung, Revision 4.0), cross-referenced with internal technical specification documentation and EMC parameter measurement data.</p>

  <div class="subhead" id="s2-3"><h3>2.3 &middot; Functional Description and Technical Parameters (Electrical, Mechanical, etc.)</h3></div>
  <p class="lede"><b>Functional workflow (normal operating mode):</b> sense &rarr; process &rarr; transmit. Each of the eight gas sensors continuously samples ambient conditions &rarr; data is normalized and classified by the on-device AI model (ESP32-S3) &rarr; the result is transmitted over the LoRa network (star-topology transmission) at a configurable interval (default 10 seconds), or immediately (event-driven) when an alarm condition is detected. Gas alarms are triggered through two parallel channels: a local visual/audible alarm module on the unit itself, and a push notification transmitted over the LoRa network to the dashboard &mdash; the alarm-push pathway has been successfully tested on a campus mesh network (field validation at a production refinery installation is still pending).</p>

  <p class="doclabel">2.3.a &middot; Electrical Parameters &mdash; Node Sensor (GLD)</p>
  <div class="tbl-scroll">
  <table>
    <tr><th>Parameter</th><th>Specification</th><th>Status</th><th>Remarks</th></tr>
    <tr><td>Main power input</td><td>24 VDC</td><td><span class="status ok">Final &mdash; production configuration</span></td><td>Continuous power supply from a site AC/DC adapter.</td></tr>
    <tr><td>AC/DC adapter input</td><td>220 VAC, 50 Hz</td><td><span class="status ok">Final</span></td><td>Compliant with the Indonesian national electrical grid standard (PLN).</td></tr>
    <tr><td>AC/DC adapter output</td><td>24 VDC</td><td><span class="status ok">Final</span></td><td>&nbsp;</td></tr>
    <tr><td>Internal operating voltage</td><td>5 VDC &amp; 3.3 VDC</td><td><span class="status ok">Final</span></td><td>5 VDC for the MQ sensor/heater circuitry; 3.3 VDC for ESP32-S3 logic. Per-rail current has not yet been documented separately.</td></tr>
    <tr><td>Maximum input current</td><td>&#8776;0.33 A @ 24 VDC</td><td><span class="status ok">Calculated</span></td><td>Calculated from measured maximum power consumption (7.995 W) divided by 24 VDC.</td></tr>
    <tr><td>Maximum power consumption</td><td>7.995 W @ 24 VDC</td><td><span class="status ok">Measured &mdash; production configuration</span></td><td>Applies to the continuous-power configuration. The battery (R&amp;D) configuration is recorded separately at 5.75 W &mdash; a different operating mode, not a data conflict.</td></tr>
    <tr><td>Electrical protection (fuse, reverse polarity, overvoltage, overcurrent)</td><td>2&times; resettable PPTC fuse (F1/F2); TVS/ESD suppression diodes (D1, D4/D5/D11, D6); Schottky diodes (D7/D13, D8/D9, D12)</td><td><span class="status wip">Partially available &mdash; component-level evidence</span></td><td>Real components exist per the EasyEDA/JLCPCB bill of materials (Section 2.6.b): 2&times; Littelfuse MINISMDC260F/16 resettable fuses (designators F1, F2, overcurrent), a Ruilong SMBJ33A TVS diode (D1) and 3&times; UMW LESD5D5.0CT1G / 1&times; DOWO SM712 ESD-protection arrays (D4, D5, D11, D6), and multiple Schottky diodes &mdash; MDD SS54 (D7, D13), MDD SS14 (D8, D9), GOOD-ARK SK36 (D12). This is genuine evidence that overcurrent and transient/ESD protection circuitry exists on the board; which specific rail each component protects and its exact circuit role (e.g., reverse-polarity blocking vs. flyback) has not yet been cross-checked against the schematic net list, and no consolidated protection-scheme write-up (clamp voltages, protection scope per interface) has been produced for ExCB review.</td></tr>
  </table>
  </div>

  <p class="doclabel">2.3.b &middot; Sensor and Communication Parameters &mdash; Node Sensor (GLD)</p>
  <div class="tbl-scroll">
  <table>
    <tr><th>Parameter</th><th>Specification</th><th>Status</th><th>Remarks</th></tr>
    <tr><td>Gas sensors</td><td>MQ-2, MQ-3B, MQ-4, MQ-5, MQ-6, MQ-7B, MQ-8, MQ-135 (8 channels)</td><td><span class="status ok">Final</span></td><td>Metal-oxide semiconductor sensors; the sensing element is directly exposed to ambient air (not enclosed).</td></tr>
    <tr><td>AI gas-classification model</td><td>On-device classifier &mdash; 3 classes: Clean Air, LPG, H&#8322;</td><td><span class="status ok">Final</span></td><td>Runs locally on the ESP32-S3 (Running/Inference mode); outputs a class label and a confidence value. Does not yet cover CO&#8322;, Benzene, CO, or H&#8322;S.</td></tr>
    <tr><td>Environmental sensor (temperature/humidity)</td><td>SHT40-AD1B-R2 (I2C)</td><td><span class="status ok">Final</span></td><td>Auxiliary temperature/humidity input included in the primary hardware design; values are available for status/telemetry.</td></tr>
    <tr><td>Analog-to-digital converter</td><td>ADS1256IDBR</td><td><span class="status ok">Final</span></td><td>24-bit multi-channel analog acquisition for the 8 sensor channels; 30,000 SPS, firmware SPI clock 1.92 MHz.</td></tr>
    <tr><td>Processing unit</td><td>ESP32-S3-WROOM-1U-N16R8</td><td><span class="status ok">Final</span></td><td>Certified under FCC (2AC7Z-ESPS3WROOM1U), TELEC, and CE (per manufacturer data, Espressif) &mdash; these are RF/EMC certifications, <b>not</b> an &ldquo;Ex component&rdquo; certification.</td></tr>
    <tr><td>Communication module</td><td>LoRa, E22-900MM22S module</td><td><span class="status ok">Final</span></td><td>Certified under CE, FCC, and RoHS (per manufacturer data, Ebyte) &mdash; RF/EMC certifications, <b>not</b> an &ldquo;Ex component&rdquo; certification.</td></tr>
    <tr><td>Operating frequency</td><td>920 MHz</td><td><span class="status ok">Final</span></td><td>Star-topology transmission; within the regional 920&ndash;923 MHz ISM band (Indonesia).</td></tr>
    <tr><td>Transmit power (firmware configuration)</td><td>17 dBm</td><td><span class="status ok">Final</span></td><td>The radio module supports up to 22 dBm &mdash; 17 dBm is an operational configuration, not the module&rsquo;s maximum limit.</td></tr>
    <tr><td>Bandwidth / spreading factor / coding rate</td><td>125 kHz / SF7 / CR 4&#8260;5</td><td><span class="status ok">Final</span></td><td>Source: EMC parameter table and official product technical datasheet.</td></tr>
    <tr><td>Antenna</td><td>External, omnidirectional, SMA male connector, 3 dBi gain</td><td><span class="status ok">Final</span></td><td>On some units, the 2.4 GHz Wi-Fi antenna remains inside the enclosure and must be relocated externally for optimal channel configuration.</td></tr>
    <tr><td>Data transmission interval</td><td>Configurable, default 10 seconds</td><td><span class="status ok">Final</span></td><td>Alarm events are transmitted immediately, independent of the periodic interval.</td></tr>
    <tr><td>Other interfaces</td><td>SPI, LoRa</td><td><span class="status ok">Final</span></td><td>External ports/connectors: USB, sensor, power, fan, antenna, alarm buzzer.</td></tr>
    <tr><td>RS-485 / Modbus interface</td><td>Read-only Modbus RTU slave, 9600 bit/s 8N1, Unit ID 1 (THVD1410DR transceiver)</td><td><span class="status ok">Final</span></td><td>Provides 8 read-only registers (device status word, classification result, confidence, battery voltage, power source, external power, LoRa transmission counter, node ID) for integration with an external controller or acquisition system; not used for product control.</td></tr>
  </table>
  </div>

  <p class="doclabel">2.3.c &middot; Mechanical Parameters &mdash; Node Sensor (GLD)</p>
  <div class="tbl-scroll">
  <table>
    <tr><th>Parameter</th><th>Specification</th><th>Status</th><th>Remarks</th></tr>
    <tr><td>Enclosure material</td><td>Aluminum alloy + stainless steel</td><td><span class="status wip">Partially available &mdash; specific grade pending</span></td><td>Per project confirmation, the production enclosure is sourced from a commercially available CE/ATEX-marketed explosion-proof gas-detector housing product line (referenced supplier listing: Alibaba.com, &ldquo;CE ATEX Explosion Proof H2 Sensor&rdquo;), consistent with the cast-metal housing, threaded &ldquo;Ex&rdquo;-marked cable entry, and sensor mesh cover shown in the product photography (Section 2.4). This is corroborated by an internal case CAD drawing (&ldquo;GLD ATEX CASE v3,&rdquo; dated 8 September 2026) specifying a cylindrical sensor-case body (&Oslash;102 mm outer housing ring, &Oslash;90/&Oslash;80 mm internal bores) that incorporates a stainless-steel filter mesh disc, a small DC cooling fan, and a transparent viewing window. The specific alloy/grade of the aluminum body and the supplier listing&rsquo;s own certification claims have not been independently verified &mdash; the listing&rsquo;s specification text could not be retrieved for cross-check, so this should be treated as project-confirmed sourcing context, not a verified datasheet citation. PVC is not used in any housing or bracket component.</td></tr>
    <tr><td>Dimensions (L &times; W &times; H)</td><td>200 &times; 90 &times; 290 mm</td><td><span class="status ok">Final</span></td><td>Consistent between the technical specification documentation and the EMC parameter table.</td></tr>
    <tr><td>Total weight</td><td>&mdash;</td><td><span class="status gap">Pending confirmation</span></td><td>Not yet weighed/documented.</td></tr>
    <tr><td>Mounting method</td><td>L-bracket, following the design already installed at the refinery</td><td><span class="status ok">Final</span></td><td>Mounted to existing structures without drilling or welding.</td></tr>
    <tr><td>Ingress protection (IP rating)</td><td>&mdash;</td><td><span class="status gap">Pending confirmation</span></td><td>Not yet tested/determined.</td></tr>
    <tr><td>Cable entry (gland)</td><td>&mdash;</td><td><span class="status gap">Pending confirmation</span></td><td>Cable gland specification not yet determined.</td></tr>
    <tr><td>Antenna mounting</td><td>External, SMA male connector</td><td><span class="status ok">Final</span></td><td>&nbsp;</td></tr>
    <tr><td>Operating temperature</td><td>&mdash;</td><td><span class="status gap">Pending confirmation</span></td><td>Ambient operating temperature range not yet determined &mdash; a key parameter for temperature class (T1&ndash;T6) determination in Section 2.5.</td></tr>
    <tr><td>Operating humidity</td><td>&mdash;</td><td><span class="status gap">Pending confirmation</span></td><td>&nbsp;</td></tr>
  </table>
  </div>
  <p class="lede" style="font-size:12px">Source: internal technical specification documentation, Sections 1.1&ndash;1.3 (Node Sensor), cross-referenced with the official product technical datasheet (Revision 4.0) and component certification verification (ESP32-S3-WROOM-1U, E22-900MM22S).</p>

  <div class="banner warn"><span class="ic">&#9888;</span><div><b>Rows marked &ldquo;Pending confirmation&rdquo; above do not reflect a documentation oversight &mdash; this is an honest status indicator.</b> These fields are intentionally left blank because no official data yet exists (not yet measured, tested, or decided). They must not be filled with estimates in future revisions without a clear supporting data source.</div></div>

  <div class="subhead" id="s2-4"><h3>2.4 &middot; Product Photographs &mdash; Overall and Key Components</h3></div>
  <p class="lede">The seven photographs below were taken directly from the Node Sensor (GLD) V2 prototype unit (no capture-date metadata is available in the source files). The first three photographs show the fully assembled unit from different angles; the remaining four show key components in close-up.</p>
  <div class="photogrid">
{photos_html}
  </div>
  <div class="banner info"><span class="ic">&#9432;</span><div><b>Photographic completeness &mdash; status as-is.</b> The seven photographs above cover the complete unit and its key components (PCB, sensor modules, alarm module, mesh cover), substantively satisfying checklist Item 2.4. Still outstanding: (a) formally labeled photographs of each face (front/back/left/right/top/bottom) with a scale reference, as is customary in ExCB submission packages; (b) separate photographs of individual components such as the battery, gaskets/seals, terminals, and cable glands.</div></div>

  <div class="subhead" id="s2-5"><h3>2.5 &middot; Description of Intended Use and Installation Environment (Gas Group, Temperature Class, Area Classification)</h3></div>
  <p class="lede">The GLD is intended for continuous, fixed-point monitoring of flammable and toxic gas leaks in oil &amp; gas refinery hazardous areas &mdash; process units, tank farms, pipe racks, and loading/unloading areas. The specific Ex classification parameters below reflect the project engineering team&rsquo;s <b>current recommendation</b>, developed from the intended deployment envelope and the gases the device is designed to detect; <b>none of these parameters has yet been confirmed with the certification body (ExCB) or a notified body</b>, and none should be treated as final.</p>
  <div class="tbl-scroll">
  <table>
    <tr><th>Parameter</th><th>Recommended value</th><th>Status</th><th>Rationale / remarks</th></tr>
    <tr><td>Gas group</td><td>IIC</td><td><span class="status wip">Team recommendation &mdash; pending ExCB confirmation</span></td><td>Hydrogen (H&#8322;) is one of the three gases the classifier is designed to detect (Section 2.3.b); IIC is required for hydrogen and inherently covers IIB and IIA.</td></tr>
    <tr><td>Temperature class</td><td>T4 (&#8804;135&#176;C)</td><td><span class="status wip">Team recommendation &mdash; pending verification</span></td><td>Not yet substantiated by measurement. The MQ-series metal-oxide sensors used in this product rely on an internal heating element as their normal operating principle; a hot-spot temperature measurement specific to the sensor models and enclosure configuration used here has not yet been performed. This is the top-priority open verification item before the temperature class can be confirmed (see 2.6.f).</td></tr>
    <tr><td>Ambient temperature range</td><td>&mdash;</td><td><span class="status gap">Pending confirmation</span></td><td>Not yet measured or specified.</td></tr>
    <tr><td>Area classification (zone)</td><td>Zone 1</td><td><span class="status wip">Team recommendation &mdash; pending ExCB confirmation</span></td><td>Assessed as sufficient for the general refinery deployment envelope, including areas near storage. Zone 0 would only apply if the detector were installed directly inside a tank vapor space, which is not the intended use case.</td></tr>
  </table>
  </div>
  <div class="banner warn"><span class="ic">&#9888;</span><div><b>These are engineering recommendations, not a certification decision.</b> An independent readiness assessment of the same checklist item, prepared separately from the underlying firmware/hardware repository, reached the same conclusion &mdash; gas group, temperature class, ambient range, and zone are not yet formally established. Final classification requires explicit agreement with the ExCB.</div></div>

  <div class="subhead" id="s2-6"><h3>2.6 &middot; Design and Manufacturing Information</h3></div>
  <p class="lede">Nine sub-items (a&ndash;i) per the original checklist. Status is reported item by item below; most sub-items are <b>not yet available</b> &mdash; this is reported plainly rather than implied to be complete.</p>

  <p class="doclabel">2.6.a &middot; Complete Drawings (Assembly, Component, Electrical Schematic, PCB Layout, Enclosure Structure, Junction Box, Terminal, Grounding)</p>
  <p class="lede">An electrical schematic capture and a corresponding PCB layout exist for the GLD V2 main board as native EasyEDA/JLCPCB source design files (not just a derived summary). From the schematic&rsquo;s traced net list, a supporting block-diagram set (9 sheets, functional/block level, 204 components mapped with documented pin-to-net traceability) has been produced and is reproduced in full below. Field labels in the source diagrams are in Indonesian; English captions are provided under each sheet.</p>
  <div class="photogrid">
{schematics_html}
  </div>
  <div class="photogrid">
  <figure class="photo">
    <img src="data:image/png;base64,{pcb_layout_b64}" alt="Main board PCB copper layout, top view" loading="lazy">
    <figcaption><b>Main board PCB layout &mdash; top copper layer</b><span>Routed layout exported directly from the EasyEDA/JLCPCB source project (production-intent board, circular outline with six mounting holes).</span></figcaption>
  </figure>
  <figure class="photo">
    <img src="data:image/png;base64,{pcb_3d_b64}" alt="3D rendered view of the main board, populated, from the EasyEDA/JLCPCB solid model" loading="lazy">
    <figcaption><b>Main board &mdash; 3D populated render</b><span>Rendered directly from the same EasyEDA/JLCPCB 3D solid model (OBJ/MTL) as the layout above &mdash; ESP32-S3-WROOM module, micro-USB connector, power inductors, and 8-channel I2C header block visible in their real placed positions. Illustrative render, not a dimensioned drawing.</span></figcaption>
  </figure>
  </div>
  <p class="lede">A dimensioned mechanical drawing sheet also exists for the enclosure&rsquo;s external envelope and its mounting hardware, drafted from a solid CAD model (STEP format, millimeter units) with a formal title block, orthographic and isometric views, and a parts table &mdash; reproduced below.</p>
  <figure class="photo" style="max-width:820px;margin:0 auto 14px">
    <img src="data:image/png;base64,{bracket_drawing_b64}" alt="Dimensioned CAD drawing sheet of the enclosure external envelope and mounting bracket" loading="lazy">
    <figcaption><b>Enclosure envelope &amp; mounting bracket &mdash; dimensioned drawing sheet</b><span>Orthographic and isometric views with real dimensions (enclosure neck &Oslash;75&nbsp;mm, overall probe height 191.51&nbsp;mm, mounting plate 250&times;250&nbsp;mm with toleranced hole pattern), a U-bolt parameter table (2&Prime;/DN50, M10 thread), and a title block (drafted 31 Aug 2026). Source: dimensioned CAD drawing derived from a STEP solid model of the enclosure and bracket assembly.</span></figcaption>
  </figure>
  <table>
    <tr><th>Drawing type</th><th>Status</th><th>Remarks</th></tr>
    <tr><td>Electrical schematic (component-level) / block diagram</td><td><span class="status wip">Partially available</span></td><td>Schematic capture and a derived 9-sheet block-diagram set exist with traceability evidence (pin-to-net mapping). Not yet issued in a released, revision-controlled drawing format with a formal drawing number.</td></tr>
    <tr><td>PCB layout</td><td><span class="status wip">Partially available</span></td><td>Native EasyEDA/JLCPCB layout export (routed copper) and a 3D solid model exist for the same board revision. Not yet issued as a dimensioned, toleranced, released drawing with a formal drawing number.</td></tr>
    <tr><td>Assembly drawing</td><td><span class="status wip">Partially available</span></td><td>A dimensioned drawing sheet exists for the enclosure/bracket mounting assembly (title block, orthographic + isometric views, parts table). It covers the external envelope and mounting hardware, not the internal PCB/component assembly sequence.</td></tr>
    <tr><td>Component drawing</td><td><span class="status gap">Not yet available</span></td><td>&nbsp;</td></tr>
    <tr><td>Enclosure structure drawing (gap, length, volume)</td><td><span class="status wip">Partially available</span></td><td>External envelope is dimensioned (from a real STEP solid model, millimeter units) in the drawing above. The Ex-d-specific flame-path parameters &mdash; joint gap, length, and free internal volume &mdash; are <b>not</b> called out; that dimensioning has to be added deliberately once a protection concept is confirmed (Section 2.5), not derived automatically from the CAD export.</td></tr>
    <tr><td>Junction box / terminal / grounding connection drawings</td><td><span class="status gap">Not yet available</span></td><td>&nbsp;</td></tr>
  </table>
  <div class="banner info"><span class="ic">&#9432;</span><div>Real dimensioned CAD drawings now exist for the enclosure&rsquo;s external envelope and mounting hardware, and native PCB layout/schematic source files exist for the electronics. What is still missing for a certifiable drawing package: internal component/assembly drawings, junction box and grounding-connection drawings, and &mdash; specific to explosion protection &mdash; flame-path gap/length/volume dimensioning, which requires a confirmed protection concept before it can be drawn.</div></div>

  <p class="doclabel">2.6.b &middot; Bill of Materials (BOM) for Explosion-Safety-Relevant Components</p>
  <p class="lede">A complete, itemized electronic-component BOM for both the main board and the external sensor board now exists, exported directly from the EasyEDA/JLCPCB source project (manufacturer, manufacturer part number, and LCSC supplier part number for each line item; {mb_lines} line items / {mb_qty} placed components on the main board, {sb_lines} line items / {sb_qty} placed components on the sensor board &mdash; full tables below). This is real, traceable sourcing data and materially improves on the previous status.</p>
  <p class="lede">It does <b>not</b>, however, satisfy this checklist item as written. The checklist asks specifically for the <b>explosion-safety-relevant</b> BOM &mdash; enclosure, gaskets, terminals, cable entry devices, switches, light sources, battery, potting compound, and plastic parts, each with material grade and Ex/UL/CCC certification status. None of those mechanical/safety items appear in an electronic CAD BOM: the enclosure is present only as a placeholder mechanical symbol (designator <span class="mono">U50</span>, no manufacturer or dimensional data attached), and the gas sensor itself (<span class="mono">MQ2</span>, designator <span class="mono">I1</span>) has no manufacturer or supplier part number recorded &mdash; it is sourced outside the LCSC/JLCPCB supply chain and its Ex status is unverified. Comparative research on Ex-rated enclosure products from other manufacturers exists internally as a reference for target specifications only &mdash; it describes third-party products, not this product&rsquo;s actual components, and is not included here.</p>
  <div class="tbl-scroll">
  <table>
    <tr><th>Designator</th><th>Value / part</th><th>Qty</th><th>Manufacturer</th><th>Manufacturer part no.</th><th>LCSC #</th></tr>
{mb_bom_rows}
  </table>
  </div>
  <p class="lede" style="margin-top:14px">External sensor board (gas-sensing front end):</p>
  <div class="tbl-scroll">
  <table>
    <tr><th>Designator</th><th>Value / part</th><th>Qty</th><th>Manufacturer</th><th>Manufacturer part no.</th><th>LCSC #</th></tr>
{sb_bom_rows}
  </table>
  </div>
  <div class="banner warn"><span class="ic">&#9888;</span><div><b>Status: Partially available.</b> Full electronic-component BOM with real manufacturer/supplier data now exists (source: EasyEDA/JLCPCB export, 11 Sep 2026). The explosion-safety-relevant subset the checklist actually asks for &mdash; enclosure, gasket, cable entry device, battery, potting compound, and the gas sensor itself, with material grade and Ex/UL/CCC certification for each &mdash; remains not yet compiled. These are mechanical/safety parts, not electronic components: the enclosure itself is under design by an external mechanical/casing development partner and its bill of materials has not yet been provided to the authors.</div></div>

  <p class="doclabel">2.6.c &middot; Material Specification Sheets / Datasheets (Non-Metallic Materials)</p>
  <p class="lede">Datasheets or supplier conformity declarations for non-metallic materials (enclosure components, seals, insulators, potting compounds) &mdash; covering heat/cold resistance, anti-aging, anti-static, flame retardancy, CTI value, and chemical resistance &mdash; have not yet been collected.</p>
  <div class="banner info"><span class="ic">&#9432;</span><div><b>Status: Not yet available.</b> Dependent on the enclosure design and material selection, which sits with the external casing development partner rather than the authors.</div></div>

  <p class="doclabel">2.6.d &middot; Manufacturing Process Description</p>
  <p class="lede">A description of manufacturing processes relevant to explosion-protection safety (enclosure machining accuracy control, explosion-proof surface treatment, welding, potting, die-casting, bonding) has not yet been documented.</p>
  <div class="banner info"><span class="ic">&#9432;</span><div><b>Status: Not yet available.</b> This describes the casing partner&rsquo;s manufacturing process, not an internal electronics process &mdash; it will need to be obtained from that partner once their process is finalized.</div></div>

  <p class="doclabel">2.6.e &middot; Explosion-Protection Calculations and Explanations (if applicable)</p>
  <p class="lede">Calculations depend on the explosion-protection concept selected (e.g., Ex d, Ex e, Ex i), which has not yet been confirmed with the ExCB, and on final enclosure geometry from the casing development partner. No calculations have been performed.</p>
  <div class="banner info"><span class="ic">&#9432;</span><div><b>Status: Not yet available &mdash; pending protection-concept confirmation and final enclosure design.</b></div></div>

  <p class="doclabel">2.6.f &middot; Temperature Group Calculation (Hottest-Point Temperature Estimation)</p>
  <p class="lede">No hottest-point temperature calculation or measurement has been performed for this product. As general context: MQ-series metal-oxide gas sensors operate using an internal heating element, a class of sensor commonly associated with published operating temperatures in the approximate 200&ndash;400&#176;C range &mdash; however, this is a general characteristic of the sensor class, <b>not</b> a measured value for the specific sensor models, drive circuitry, and enclosure configuration used in this product. A worst-case hot-spot measurement is identified as the top-priority action required to substantiate the recommended T4 classification in Section 2.5.</p>
  <div class="banner info"><span class="ic">&#9432;</span><div><b>Status: Not yet available.</b></div></div>

  <p class="doclabel">2.6.g &middot; Usage and Installation Instructions (Draft)</p>
  <table>
    <tr><th>Sub-item</th><th>Status</th><th>Remarks</th></tr>
    <tr><td>a) Safety warnings</td><td><span class="status gap">Not yet available</span></td><td>No Ex-specific safety warnings have been drafted.</td></tr>
    <tr><td>b) Installation requirements (cable entry, torque, grounding, cleaning)</td><td><span class="status wip">Partially available</span></td><td>A mechanical mounting method exists separately (L-bracket, installed to existing structures without drilling or welding &mdash; see Section 2.3.c), but cable-entry method, torque values, grounding requirements, and cleaning requirements have not yet been formally specified.</td></tr>
    <tr><td>c) Operating instructions and maintenance requirements</td><td><span class="status wip">Partially available</span></td><td>A firmware command/operation reference exists (Serial, MQTT, and LoRa command protocol for engineering use), but it covers software operation and commissioning &mdash; not Ex-specific maintenance or inspection requirements (frequency, content, precautions).</td></tr>
  </table>
  <div class="banner info"><span class="ic">&#9432;</span><div><b>Status: Partially available &mdash; not yet consolidated into an Ex-specific installation and operation manual for ExCB review.</b></div></div>

  <p class="doclabel">2.6.h &middot; Nameplate Information</p>
  <p class="lede">Nameplate artwork cannot yet be finalized: it depends on the certificate number, protection marking, temperature class, ambient range, IP rating, and serialization scheme &mdash; none of which has been assigned yet.</p>
  <div class="banner info"><span class="ic">&#9432;</span><div><b>Status: Not yet available.</b></div></div>

  <p class="doclabel">2.6.i &middot; Ex Component Certificates</p>
  <p class="lede">No components in this design currently hold an Ex component certificate. As noted in Section 2.3.b, the processing unit (ESP32-S3-WROOM-1U-N16R8) and the communication module (E22-900MM22S) hold RF/EMC certifications (FCC, TELEC, CE, RoHS) &mdash; these are <b>not</b> Ex component certificates and do not satisfy this item.</p>
  <div class="banner info"><span class="ic">&#9432;</span><div><b>Status: Not yet available.</b></div></div>
</section>

<section class="zone" id="s3">
  <div class="zone-head"><span class="zn">3</span><h2>Sample Information</h2></div>
  <p class="lede">Model, serial number, and sample status (whether the unit can be powered on and operated), together with any required test fixtures or auxiliary equipment.</p>

  <p class="doclabel">3.1 &middot; Model, Serial Number, and Status</p>
  <p class="lede">No formal sample register or dossier for ExCB submission has been established. Internal engineering and bench testing reference the &ldquo;GLD V2&rdquo; board configuration under firmware environment <span class="mono">gld_v2</span>; a discrete unit serial-numbering scheme for certification samples has not yet been implemented.</p>
  <div class="banner info"><span class="ic">&#9432;</span><div><b>Status: Not yet available.</b> The product is still being built from scratch at prototype/development stage; no finalized, serialized unit yet exists to register as a submission sample. This item becomes actionable once a build reaches a stable, submission-ready configuration.</div></div>

  <p class="doclabel">3.2 &middot; Test Fixtures and Auxiliary Equipment</p>
  <p class="lede">A draft internal functional test plan identifies the minimum equipment anticipated for bench-level verification (this plan has not yet been executed and is not evidence of lab readiness):</p>
  <div class="tbl-scroll">
  <table>
    <tr><th>Test group</th><th>Minimum equipment</th></tr>
    <tr><td>Firmware / serial</td><td>Engineering commissioning tool or serial terminal; firmware package with recorded version</td></tr>
    <tr><td>I2C / ADC / DAC</td><td>No additional equipment for protocol-level acknowledgement/readback; multimeter or oscilloscope where physical voltage must be substantiated</td></tr>
    <tr><td>Power / watchdog timer</td><td>Controlled 24&nbsp;V supply, an applicable battery source, multimeter, and oscilloscope/logic analyzer</td></tr>
    <tr><td>Alarm</td><td>The actual alarm load, multimeter/oscilloscope, and hearing protection if an audible buzzer is fitted</td></tr>
    <tr><td>LoRa</td><td>At least one counterpart Cluster Head/Gateway device with recorded configuration</td></tr>
    <tr><td>RS-485 / Modbus</td><td>An RS-485/USB-RS485 master with proper termination and the agreed register map</td></tr>
  </table>
  </div>
  <div class="banner info"><span class="ic">&#9432;</span><div><b>Status: Draft plan only &mdash; not yet executed, and not evidence of ExCB/laboratory test readiness.</b></div></div>
</section>

<footer>
  This is a working document, prepared in stages, drafted in direct reference to the <i>IECEx/ATEX Certification Information Requirements</i> (original English/Mandarin version issued by the certification body). Data sources: the official product technical datasheet (Institute of Technology Bandung, Revision 4.0), internal technical specification documentation, EMC parameter measurement data, and product photography. Fields marked &ldquo;Pending confirmation&rdquo; are not yet final and must not be relied upon for procurement or certification purposes without further verification.
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
