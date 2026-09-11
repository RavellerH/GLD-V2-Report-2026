# -*- coding: utf-8 -*-
import base64, os

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PHOTO_DIR = os.path.join(REPO, "scripts", "assets", "cert_doc_photos")
OUT_PATH = os.path.join(REPO, "Deliverables", "Dokumen_Teknis_Sertifikasi_GLD_IECEx_ATEX.html")
STYLE_SOURCE = os.path.join(REPO, "Deliverables", "Dashboard_Sertifikasi_GLD_ATEX_IECEx.html")

def b64(fn):
    with open(os.path.join(PHOTO_DIR, fn), "rb") as f:
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
@media print{
  .tbl-scroll{overflow-x:visible !important;border:none !important}
  table{min-width:0 !important;table-layout:fixed !important;width:100% !important}
  table td,table th{word-break:break-word}
  .status{white-space:normal !important;display:inline-block}
  .photogrid{grid-template-columns:repeat(3,1fr) !important}
  figure.photo{break-inside:avoid}
  .zone{break-inside:auto}
  .subhead{break-after:avoid}
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
    <li><a class="sub" href="#s2-5"><span class="st pending">&#9675;</span> 2.5 Installation Environment</a></li>
    <li><a class="sub" href="#s2-6"><span class="st pending">&#9675;</span> 2.6 Design &amp; Manufacturing (a&ndash;i)</a></li>
    <li><a href="#s3"><span class="st pending">&#9675;</span> 3. Sample Information</a></li>
  </ul>
  <div class="side-foot">
    <button class="themebtn" id="themebtn">&#9788; Toggle light/dark theme</button>
  </div>
</nav>
<main class="content">

<div class="masthead">
  <div class="tagrow">
    <span class="chip accent">Working document</span>
    <span class="chip">Items 1&ndash;4 of 6 (Section 2)</span>
    <span class="chip warn">Selected parameters pending confirmation</span>
  </div>
  <h1>IECEx/ATEX Technical Certification Document &mdash; Gas Leak Detector (GLD) V2</h1>
  <p class="subtitle">Prepared in direct reference to the <i>IECEx/ATEX Certification Information Requirements</i> issued by the certification body (ExCB) &mdash; Section <b>2, Technical Documentation</b>, Items 1&ndash;4: product description, product name/model/specification list, functional description and technical parameters, and product photographs. This document is being developed in stages; remaining items will follow in subsequent revisions.</p>
  <div class="docmeta-row">
    <div><span class="k">Certification subject</span><span class="v">Node Sensor (GLD) &mdash; V2</span></div>
    <div><span class="k">Manufacturer</span><span class="v">PT LAPI Ganesha Utama</span></div>
    <div><span class="k">Technical partner</span><span class="v">Institute of Technology Bandung</span></div>
    <div><span class="k">Reference checklist</span><span class="v">IECEx/ATEX Certification Info. Requirements</span></div>
  </div>
</div>

<section class="zone" id="about">
  <div class="zone-head"><span class="zn">&#8226;</span><h2>About this document</h2></div>
  <p class="lede">This document is a working technical file prepared to satisfy Section <b>&ldquo;2. Technical Documentation&rdquo;</b> of the official <i>IECEx/ATEX Certification Information Requirements</i> checklist issued by the certification body (ExCB). The table of contents on the left follows the complete structure of the original checklist (Sections 1&ndash;3); sections not yet completed are marked with a pending status and will follow in subsequent revisions.</p>

  <div class="enchecklist">Original excerpt, Section 2, Items 1&ndash;4 &mdash; source: <span class="mono">IECEx ATEX Certification Information Requirements</span> (ExCB):<br>
  &ldquo;1) Detailed product description; 2) Product name, model, and specification list; 3) Complete and clear functional description and technical parameters (electrical parameters, mechanical parameters, etc.); 4) Clear product photos (overall and key components).&rdquo;</div>
</section>

<section class="zone" id="s1">
  <div class="zone-head"><span class="zn">1</span><h2>Basic Information (Application and Organization)</h2></div>
  <p class="lede">Covers the application form, business license/company registration, organizational chart and contact information, manufacturing facility address and profile, and (where applicable) ISO 9001 certification.</p>
  <div class="banner info"><span class="ic">&#9675;</span><div><b>Not yet prepared in this revision.</b> To be completed in a subsequent revision.</div></div>
</section>

<section class="zone" id="s2">
  <div class="zone-head"><span class="zn">2</span><h2>Technical Documentation</h2></div>
  <p class="lede">Nine items per the original checklist (1&ndash;9, with Item 6 comprising sub-items a&ndash;i). This revision addresses Items 1&ndash;4; Items 5&ndash;9 will follow.</p>

  <div class="subhead" id="s2-1"><h3>2.1 &middot; Detailed Product Description</h3></div>
  <p class="lede">The Gas Leak Detector (GLD) is an IoT-based, multi-sensor gas leak detection device designed for the early detection of flammable and process gases in oil &amp; gas refinery environments (process units, tank farms, pipe racks, and storage/loading-unloading areas). This document addresses the GLD unit itself as the subject of the current IECEx/ATEX certification.</p>
  <p class="lede">Functionally, the GLD integrates eight channels of metal-oxide semiconductor gas sensors (MQ series), an edge-AI microcontroller/processor (ESP32-S3), and a LoRa radio module (star-topology wireless transmission) within a single fixed-point unit installed at locations with gas-leak risk. An on-device AI gas-classification model (CNN Dual-Branch architecture) runs directly on the unit &mdash; <i>confirmed by the engineering team; written verification within firmware documentation has not yet been completed</i> &mdash; so that detection decisions do not depend on a continuous connection to a central server. When gas concentration exceeds a defined threshold, the unit triggers a local alarm (an integrated visual/audible alarm module) and simultaneously transmits an alarm notification over the LoRa network to the operator dashboard.</p>
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
    <div class="spec"><span class="k">Microcontroller</span><span class="v">ESP32-S3-WROOM-1U</span></div>
    <div class="spec"><span class="k">LoRa radio module</span><span class="v">E22-900MM22S</span></div>
    <div class="spec"><span class="k">Dimensions (L&times;W&times;H)</span><span class="v">200 &times; 90 &times; 290 mm</span></div>
    <div class="spec"><span class="k">Enclosure material</span><span class="v">Aluminum alloy + stainless steel</span></div>
  </div>
  <p class="lede" style="font-size:12px">Source: internal technical specification documentation (Revision 27 August 2026) and EMC parameter measurement data (Institute of Technology Bandung, Physics Laboratory).</p>

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
    <tr><td>Backup battery path (R&amp;D, not yet in production)</td><td>Li-ion 18650 cells, 7 cells in parallel, 4.2 V/cell, &#8776;28,000 mAh total</td><td><span class="status wip">Development pathway</span></td><td>Not yet a deployed production configuration. Cell/BMS safety certification (e.g., UN 38.3, IEC 62133) has not yet been obtained.</td></tr>
    <tr><td>Electrical protection (fuse, reverse polarity, overvoltage, overcurrent)</td><td>&mdash;</td><td><span class="status gap">Pending confirmation</span></td><td>Scope of electrical protection has not yet been defined/documented.</td></tr>
  </table>
  </div>

  <p class="doclabel">2.3.b &middot; Sensor and Communication Parameters &mdash; Node Sensor (GLD)</p>
  <div class="tbl-scroll">
  <table>
    <tr><th>Parameter</th><th>Specification</th><th>Status</th><th>Remarks</th></tr>
    <tr><td>Gas sensors</td><td>MQ-2, MQ-3B, MQ-4, MQ-5, MQ-6, MQ-7B, MQ-8, MQ-135 (8 channels)</td><td><span class="status ok">Final</span></td><td>Metal-oxide semiconductor sensors; the sensing element is directly exposed to ambient air (not enclosed).</td></tr>
    <tr><td>AI gas-classification model</td><td>CNN Dual-Branch &mdash; 4 classes: LPG, CO&#8322;, Clean Air, H&#8322;</td><td><span class="status wip">Confirmed by the engineering team; written verification in firmware documentation pending</span></td><td>On-chip accuracy 99.20% (int8, ESP32-S3, model size 9.14 KB). Does not yet cover Benzene, CO, or H&#8322;S (an additional client requirement, still open).</td></tr>
    <tr><td>Environmental sensor (temperature/humidity)</td><td>Not installed on production units</td><td><span class="status wip">Laboratory test rig only</span></td><td>Used only on the laboratory test rig, not on field units.</td></tr>
    <tr><td>Processing unit</td><td>ESP32-S3-WROOM-1U</td><td><span class="status ok">Final</span></td><td>Certified under FCC (2AC7Z-ESPS3WROOM1U), TELEC, and CE (per manufacturer data, Espressif) &mdash; these are RF/EMC certifications, <b>not</b> an &ldquo;Ex component&rdquo; certification.</td></tr>
    <tr><td>Communication module</td><td>LoRa, E22-900MM22S module</td><td><span class="status ok">Final</span></td><td>Certified under CE, FCC, and RoHS (per manufacturer data, Ebyte) &mdash; RF/EMC certifications, <b>not</b> an &ldquo;Ex component&rdquo; certification.</td></tr>
    <tr><td>Operating frequency</td><td>920 MHz</td><td><span class="status ok">Final</span></td><td>Star-topology transmission; within the regional 920&ndash;923 MHz ISM band (Indonesia).</td></tr>
    <tr><td>Transmit power (firmware configuration)</td><td>17 dBm</td><td><span class="status ok">Final</span></td><td>The radio module supports up to 22 dBm &mdash; 17 dBm is an operational configuration, not the module&rsquo;s maximum limit.</td></tr>
    <tr><td>Bandwidth / spreading factor</td><td>125 kHz / SF7</td><td><span class="status ok">Final</span></td><td>Source: EMC parameter table.</td></tr>
    <tr><td>Antenna</td><td>External, omnidirectional, SMA male connector, 3 dBi gain</td><td><span class="status ok">Final</span></td><td>On some units, the 2.4 GHz Wi-Fi antenna remains inside the enclosure and must be relocated externally for optimal channel configuration.</td></tr>
    <tr><td>Data transmission interval</td><td>Configurable, default 10 seconds</td><td><span class="status ok">Final</span></td><td>Alarm events are transmitted immediately, independent of the periodic interval.</td></tr>
    <tr><td>Other interfaces</td><td>SPI, LoRa</td><td><span class="status ok">Final</span></td><td>External ports/connectors: USB, sensor, power, fan, antenna, alarm buzzer.</td></tr>
  </table>
  </div>

  <p class="doclabel">2.3.c &middot; Mechanical Parameters &mdash; Node Sensor (GLD)</p>
  <div class="tbl-scroll">
  <table>
    <tr><th>Parameter</th><th>Specification</th><th>Status</th><th>Remarks</th></tr>
    <tr><td>Enclosure material</td><td>Aluminum alloy + stainless steel</td><td><span class="status wip">Specific grade pending</span></td><td>PVC is not used in any housing or bracket component. The specific grade (aluminum series, stainless steel 304/316L) is still under determination.</td></tr>
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
  <p class="lede" style="font-size:12px">Source: internal technical specification documentation, Sections 1.1&ndash;1.3 (Node Sensor), cross-referenced with EMC parameter data and component certification verification (ESP32-S3-WROOM-1U, E22-900MM22S).</p>

  <div class="banner warn"><span class="ic">&#9888;</span><div><b>Rows marked &ldquo;Pending confirmation&rdquo; above do not reflect a documentation oversight &mdash; this is an honest status indicator.</b> These fields are intentionally left blank because no official data yet exists (not yet measured, tested, or decided). They must not be filled with estimates in future revisions without a clear supporting data source.</div></div>

  <div class="subhead" id="s2-4"><h3>2.4 &middot; Product Photographs &mdash; Overall and Key Components</h3></div>
  <p class="lede">The seven photographs below were taken directly from the Node Sensor (GLD) V2 prototype unit (no capture-date metadata is available in the source files). The first three photographs show the fully assembled unit from different angles; the remaining four show key components in close-up.</p>
  <div class="photogrid">
{photos_html}
  </div>
  <div class="banner info"><span class="ic">&#9432;</span><div><b>Photographic completeness &mdash; status as-is.</b> The seven photographs above cover the complete unit and its key components (PCB, sensor modules, alarm module, mesh cover), substantively satisfying checklist Item 2.4. Still outstanding: (a) formally labeled photographs of each face (front/back/left/right/top/bottom) with a scale reference, as is customary in ExCB submission packages; (b) separate photographs of individual components such as the battery, gaskets/seals, terminals, and cable glands.</div></div>

  <div class="subhead" id="s2-5"><h3>2.5 &middot; Description of Intended Use and Installation Environment (Gas Group, Temperature Class, Area Classification)</h3></div>
  <div class="banner info"><span class="ic">&#9675;</span><div><b>Not yet prepared in this revision.</b> The classification scheme (gas group, temperature class, installation zone) will be finalized based on further technical assessment and confirmed together with the certification body (ExCB / notified body).</div></div>

  <div class="subhead" id="s2-6"><h3>2.6 &middot; Design and Manufacturing Information (Items a&ndash;i: Technical Drawings, Bill of Materials, Material Datasheets, Manufacturing Process, Calculations, Draft Manual, Nameplate, Ex Component Certificates)</h3></div>
  <div class="banner info"><span class="ic">&#9675;</span><div><b>Not yet prepared in this revision.</b> To be completed in a subsequent revision, covering technical drawings, the bill of materials, material datasheets, a manufacturing process description, explosion-protection calculations, a draft operating/installation manual, nameplate information, and Ex component certificates.</div></div>
</section>

<section class="zone" id="s3">
  <div class="zone-head"><span class="zn">3</span><h2>Sample Information</h2></div>
  <p class="lede">Model, serial number, and sample status (whether the unit can be powered on and operated), together with any required test fixtures or auxiliary equipment.</p>
  <div class="banner info"><span class="ic">&#9675;</span><div><b>Not yet prepared in this revision.</b></div></div>
</section>

<footer>
  This is a working document, prepared in stages, drafted in direct reference to the <i>IECEx/ATEX Certification Information Requirements</i> (original English/Mandarin version issued by the certification body). Data sources: internal technical specification documentation (Revision 27 August 2026), EMC parameter measurement data (Institute of Technology Bandung, Physics Laboratory), and product photography. Fields marked &ldquo;Pending confirmation&rdquo; are not yet final and must not be relied upon for procurement or certification purposes without further verification.
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
