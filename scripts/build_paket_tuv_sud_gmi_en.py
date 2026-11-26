"""TÜV SÜD discussion package (GLD V2) — English version.

Reuses layout helpers from build_paket_tuv_sud_gmi.py; content translated here.
"""
import re
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt
from pypdf import PdfReader, PdfWriter

import build_paket_tuv_sud_gmi as g
from build_paket_tuv_sud_gmi import (A, FIG, NAVY, OUT, TW, UNIT, bullets, figure, flow_diagram, new_doc, note,
                                     page_break, para, table, title_block, to_pdf)

g.TR = {
    "   |   Diskusi Sertifikasi ATEX/IECEx — TÜV SÜD": "   |   ATEX/IECEx Certification Discussion — TÜV SÜD",
    "RAHASIA": "CONFIDENTIAL",
    "Halaman ": "Page ",
    "DOKUMEN PEMBUKA": "INTRODUCTORY DOCUMENT",
    "LAMPIRAN": "ATTACHMENT",
    "Produk": "Product",
    "Gas Leak Detector (GLD) V2 — detektor gas tipe titik (fixed point)": "Gas Leak Detector (GLD) V2 — fixed-point gas detector",
    "Nomor dokumen": "Document number",
    "Revisi / tanggal": "Revision / date",
    "Tujuan": "Purpose",
    "Sumber data": "Data source",
    "Dossier IECEx/ATEX Certification Information Requirements GLD V2 (Rev. 2.1–2.3) dan data proyek terkini":
        "IECEx/ATEX Certification Information Requirements dossier, GLD V2 (Rev. 2.1–2.3), and current project data",
    "Batas peralatan yang diajukan sertifikasi — Node Sensor GLD V2 (enclosure Ex db)":
        "Equipment boundary submitted for certification — GLD V2 sensor node (Ex db enclosure)",
    "Udara sekitar": "Ambient air", "masuk lewat mesh SS": "enters via SS mesh",
    "Kipas DC": "DC fan", "aliran ke sensor": "flow to sensors",
    "8 sensor MQ": "8 MQ sensors", "metal-oxide": "metal-oxide",
    "klasifikasi AI lokal": "on-device AI",
    "Alarm lokal": "Local alarm", "Radio LoRa": "LoRa radio",
    "maks. ±8 W, M20×1,5": "max. ±8 W, M20×1.5",
    "stud eksternal": "external stud", "Modbus RTU (opsional)": "Modbus RTU (optional)",
    "area aman / unclassified": "safe / unclassified area",
    "intranet lokasi": "site intranet",
    "Adaptor 220 VAC → 24 VDC": "Adaptor 220 VAC → 24 VDC", "di luar batas peralatan": "outside equipment boundary",
    "Di luar lingkup sertifikasi": "Outside certification scope",
}

FIG_EN = [
    "Base, main board, antenna lead and terminal board installation",
    "MQ sensor modules and DC fan",
    "Fan, beacon and prototype cable gland termination",
    "24 VDC supply connection, cover and grounding",
    "Cover closure and external views",
    "Rear view, nameplate location and antenna",
    "Antenna interface and neck wall measurement",
    "Thread height, bore and O-ring measurement",
    "Depth, O-ring diameter and thread length measurement",
    "Cover depth and target Ex parameters",
    "M-D1 — antenna, MQ sensor, body and cover",
    "M-D2/D3 — gasket location and part",
    "M-D4/D5 — mesh, beacon, main board",
    "M-D6/D7 — sensors and reference base drawing",
    "M-D8/D9 — exploded views",
    "M-D10/D11 — PCB and terminal board",
    "M-D12/D13 — components, block diagram, enclosure structure",
    "M-D14/D15 — 24 VDC terminal and grounding",
    "M-E1 — assembly exploded view",
    "M-E2 — casing cover",
    "M-E3 — sensor case and gasket (contains superseded battery detail)",
    "M-E4 — LED and buzzer",
    "M-E5 — 24 VDC power in",
    "M-E6 — motherboard into base casing",
    "M-E8 — current antenna position",
    "Main board and terminal board renders, V4",
    "Threaded joint measurement and estimation",
    "MS-01 — base and threaded neck sketch",
    "MS-02–04 — cover, threaded joint and O-ring",
    "MS-06 — terminals and field wiring",
    "M-C1 — supplier drawing BP18-1Z (candidate)",
    "M-F1 — MQ-2 and MQ-3 (MQ-3B variant to be confirmed)",
    "M-F2 — MQ-4 and MQ-5",
    "M-F3 — MQ-6 and MQ-7 (MQ-7B variant to be confirmed)",
    "M-F4 — MQ-8 and MQ-135",
]



# ================================================================== 00
def build_00():
    no = "GLD/ATEX-IN/2026-001-EN"
    d = new_doc(no, "Product Introduction")
    title_block(d, "GLD V2 Product Introduction", "Product overview and map of the documents requested by TÜV SÜD", no,
                "Introductory material for the technical meeting with TÜV SÜD via Microsoft Teams, Thursday, 26 November 2026, 14:30 WIB (13:30 China Standard Time)")
    d.add_heading("1. Meeting agenda", level=1)
    para(d, "This document opens the discussion by describing the product to be certified and then mapping each item "
            "requested by TÜV SÜD to the attachment that addresses it.")
    table(d, [
        ["Part", "Content", "Document"],
        ["A. Product", "Function, operating principle, construction, specification, equipment boundary", "00 (this document) §2–5"],
        ["B. Certification scope", "Proposed Ex classification and applicable standards", "00 §6"],
        ["C. TÜV SÜD requests", "Assembly drawing, user manual, target Ex marking, IP66, ISO 9001", "Attachments 01–05"],
        ["D. Discussion", "Topics to agree the certification route", "00 §8"],
    ], [3.6, 9.0, 4.0])
    page_break(d)
    d.add_heading("2. Product overview", level=1)
    para(d, "The Gas Leak Detector (GLD) V2 is an IoT-based fixed-point gas leak detector for oil and gas refinery process "
            "areas — process units, tank farms, pipe racks and loading areas. Each unit continuously monitors the surrounding "
            "air, classifies the gas condition on the device itself, sounds a local alarm, and transmits status and alarms "
            "wirelessly to the monitoring system.")
    figure(d, UNIT, "Figure 1 — GLD V2 current production configuration, four views (antenna on top of the base, alarm beacon at the side).",
           max_h=9.5, crop=False)
    d.add_heading("3. Operating principle", level=1)
    dg = A / "diagram_flow_gld_en.png"; flow_diagram(dg)
    figure(d, dg, "Figure 2 — Signal flow and equipment boundary. Items inside the dashed line are the object of certification.", crop=False, max_h=8)
    bullets(d, [
        ("Sampling — ", "ambient air enters through the stainless-steel mesh in the front cover; a DC fan assists the flow to eight metal-oxide gas sensors (MQ-2, MQ-3B, MQ-4, MQ-5, MQ-6, MQ-7B, MQ-8, MQ-135)."),
        ("Processing — ", "sensor signals are digitised by a 24-bit ADC (ADS1256) every 500 ms and classified by an AI model on the ESP32-S3 as Clean Air, LPG or H₂."),
        ("Alarm — ", "two parallel paths: LED and buzzer on the unit, and a LoRa notification to the Cluster Head and Gateway. The alarm decision does not depend on the server connection."),
        ("Power — ", "24 VDC continuous only. There is no 220 VAC inside the GLD; the AC/DC adaptor is outside the equipment boundary."),
    ])
    d.add_heading("4. Construction", level=1)
    table(d, [
        ["Part", "Description"],
        ["Enclosure", "Die-cast aluminium (ADC12) with threaded cover and O-ring; based on a modified commercial gas detector housing HIREP HRP-T1000-A"],
        ["Gas inlet", "Stainless-steel wire-mesh plate in the front cover (replacing the original housing window)"],
        ["Electronics", "Main board V4 (ESP32-S3, ADC, LoRa E22-900MM22S, RS-485), terminal board, 8 MQ sensor modules, 5 V DC fan"],
        ["Alarm", "24 V alarm beacon (LED and buzzer) on the right-hand side"],
        ["Antenna", "LoRa antenna on the top face of the base, SMA connector"],
        ["Cable entry", "M20 × 1.5 for the 24 VDC cable (two cores L+/L−); Ex d gland to be specified"],
        ["Mounting", "250 × 250 mm U-bolt plate to a 2 in/DN50 pipe (OD 60.3 mm), M10 bolts"],
        ["Grounding", "External PE stud beside the cable gland"],
    ], [3.4, TW - 3.4])
    d.add_heading("5. Main specification", level=1)
    table(d, [
        ["Parameter", "Value", "Status"],
        ["Supply", "24 VDC; max. ±8 W (≈ 0.33 A)", "Measured"],
        ["Dimensions / mass", "200 × 90 × 290 mm / 2.378 kg", "Design data"],
        ["Sensors", "8 × MQ metal-oxide + SHT40 (temperature/humidity)", "Final"],
        ["On-device gas classes", "Clean Air, LPG, H₂", "Final (current model version)"],
        ["Communication", "LoRa 920–923 MHz; RS-485 Modbus RTU read-only 9600 8N1", "Final"],
        ["Operating temperature", "−20 °C to +60 °C", "Upper limit under review (base housing +55 °C)"],
        ["Humidity", "5–95 % RH, non-condensing", "Design data"],
        ["Ingress protection", "IP66", "Target, not yet tested"],
    ], [4.0, 7.1, 5.5])
    d.add_heading("6. Proposed certification scope", level=1)
    p = d.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("⟨Ex⟩ II 2G  Ex db IIC T4 Gb    −20 °C ≤ Ta ≤ +60 °C"); r.bold = True; r.font.size = Pt(14); r.font.color.rgb = NAVY
    table(d, [
        ["Element", "Proposal", "Rationale"],
        ["Object", "GLD V2 sensor node only", "Cluster Head and Gateway are installed in safe areas"],
        ["Area", "Zone 1 (Category 2G, EPL Gb)", "Installed in classified refinery process areas"],
        ["Protection", "Ex db — flameproof enclosure", "Die-cast enclosure; sensor heaters (±0.75 W/sensor) cannot be reconciled with intrinsic safety (Ex i) energy limits"],
        ["Gas group", "IIC", "Hydrogen is one of the target gases"],
        ["Temperature class", "T4 (≤ 135 °C)", "Preliminary internal measurement: hottest point ≈ 114 °C extrapolated to Ta +60 °C"],
        ["Dust", "Not applied for", "Gas atmospheres only"],
        ["Reference standards", "IEC/EN 60079-0, 60079-1; IEC 60529 (IP)", "Editions and additions as advised by TÜV SÜD"],
    ], [3.0, 5.3, 8.3])
    note(d, "All elements above are the applicant's proposal and are not certified. The final classification is determined by the certification body.")
    d.add_heading("7. Map of TÜV SÜD requests", level=1)
    table(d, [
        ["Request", "Attachment", "Content", "Status"],
        ["Assembly drawing", "01 Assembly Drawings", "Reference configuration, drawing register, assembly & measurement photos, component drawings, assembly sequence, terminals, grounding, sensors", "Partly available — controlled dimensioned drawing of the production unit to be issued"],
        ["User manual", "02 User Manual", "Safety, installation, commissioning, operation, alarms, inspection, maintenance, decommissioning", "Draft"],
        ["Target Ex marking", "03 Target Ex Marking", "Proposed marking, meaning of each element, nameplate, preliminary T4 evaluation", "Proposal available"],
        ["IP66", "04 IP66 Status", "Target, sealing interfaces, IEC 60529 verification plan", "Target, not yet tested"],
        ["ISO 9001 certificate", "05 ISO 9001 Status", "Manufacturer certification status, quality documents, QAR/QAN route", "In progress"],
    ], [3.0, 3.2, 6.4, 4.0], size=9)
    d.add_heading("8. Points for discussion with TÜV SÜD", level=1)
    bullets(d, [
        "Certification scheme: IECEx and ATEX in parallel, notified body and test location.",
        "Applicability of the base housing certificate after modification (front window replaced by mesh, electronics replaced).",
        "Method to prove the stainless-steel mesh as a flame-path element (flame transmission test) or need for a certified flame arrestor.",
        "Confirmation of maximum Ta +60 °C and the T4 temperature-class test method.",
        "IP66 testing for a device with an open gas inlet.",
        "Number of samples, test sequence, schedule, cost estimate, QAR/QAN route and the role of ISO 9001.",
        "Acceptable format and language of the technical documentation.",
    ], style="List Number")
    f = OUT / "00_Product_Introduction_GLD_V2_EN.docx"; d.save(f); return f


# ================================================================== 01
def build_01():
    no = "GLD/ATEX-AD/2026-001-EN"
    d = new_doc(no, "01 Assembly Drawings")
    title_block(d, "Assembly Drawing Package", "Assembly drawing · assembly photos · component and reference drawings", no,
                "Response to TÜV SÜD request: Assembly drawing")
    note(d, "Technical draft — not controlled production drawings. Source sheets are reproduced with their original labels.")
    d.add_heading("1. Reference configuration", level=1)
    para(d, "The reference physical configuration is the production unit as photographed on 7 October 2026: continuous 24 VDC "
            "supply, stainless-steel mesh in the front cover, DC fan behind the mesh, eight MQ modules, main board V4 and "
            "terminal board, LoRa antenna on top of the base, alarm beacon at the side, and cable entry on the left. The "
            "prototype's bottom opening is closed with a blanking plug.")
    table(d, [
        ["Parameter", "Data / remarks"],
        ["Dimensions", "200 × 90 × 290 mm; to be re-checked against the latest configuration"],
        ["Mass", "2.378 kg; not yet weighed on a calibrated scale"],
        ["Material", "ADC12 (enclosure) + stainless steel (mesh); supplier material certificates to be provided"],
        ["Mounting", "250 × 250 mm plate; 2 in/DN50 U-bolt, M10"],
        ["Cable entry", "M20 × 1.5; prototype polymer gland to be replaced by an Ex d gland"],
    ], [3.4, TW - 3.4])
    d.add_heading("2. Drawing register", level=1)
    table(d, [
        ["Group", "Content", "Sheets"],
        ["Assembly & measurement photos", "Actual assembly, external views, thread, bore, O-ring and depth measurements", "1–10"],
        ["M-D1–D15", "Components, gasket, mesh, beacon, main board, exploded views, terminals, grounding", "11–18"],
        ["M-E1–E6, M-E8", "Assembly sequence; current antenna position in M-E8", "19–25"],
        ["PCB & measured sketches", "PCB V4 renders, threaded-joint sketches MS-01–04, terminals MS-06", "26–30"],
        ["M-C1, M-F1–F4", "Supplier drawing of base BP18-1Z (candidate) and MQ sensor dimensions", "31–35"],
    ], [4.2, 10.0, 2.4])
    d.add_heading("3. Design control notes", level=1)
    bullets(d, [
        "CAD drawings of casing v2 and alternative design V3 are not included because they show the superseded antenna position on the side of the base. Dimensioned drawings of the production unit (antenna on top) will be issued separately.",
        "M-E3 and M-D14 contain superseded details (battery configuration) that do not apply to the 24 VDC configuration.",
        "Controlled drawings are still required for flame-path gaps and lengths, thread tolerance and engagement, internal volume, mesh and its retention, gaskets, cable/antenna/alarm penetrations and torque values.",
        "Preliminary measurements: bore ≈ Ø84.7 mm; threaded neck height ≈ 14.8 mm; cover thread length ≈ 18.9 mm; O-ring cord 2.70 mm, OD ≈ 91 mm; estimated cover thread M96 × 1.5; gross volume ≈ 0.4 L. These are not approved production dimensions.",
        "BP18-1Z is a candidate/supplier reference only.",
    ])
    figs = [x for x in FIG if x["file"].startswith("a")]
    assert len(figs) == len(FIG_EN)
    for k, (fg, t) in enumerate(zip(figs, FIG_EN), 1):
        page_break(d)
        d.add_heading(f"Sheet {k} — {t}", level=2)
        m = re.search(r"halaman (\d+/\d+)", fg["caption"])
        figure(d, A / fg["file"], f"Source: CIR dossier, page {m.group(1)}" if m else "", max_h=21.5)
    f = OUT / "01_Assembly_Drawings_GLD_V2_EN.docx"; d.save(f); return f


# ================================================================== 02
MANUAL = [
    ("g.1 Safety warnings", "Only trained and authorised personnel may install, operate, inspect or maintain the GLD. Isolate and verify the 24 VDC supply and apply lockout/tagout before opening the enclosure or changing wiring; confirm the area is safe. Use the 24 VDC supply configuration only. Test alarms according to site procedures, with hearing protection where needed. Perform nulling only in confirmed clean air; it must succeed 8/8. Do not drill, weld, enlarge openings, bypass protection or modify the enclosure without approval. Remove the unit from service if damaged, if water has entered, if a sensor fault is unresolved, if the alarm fails or if PE continuity is lost."),
    ("g.2 Installation environment", "Intended use is fixed installation in refinery process units, tank farms, pipe racks and loading areas: Group II, Category 2G/EPL Gb, Zone 1, IIC, T4, gas only — subject to approval by the certification body. Use only locations that meet the final certificate marking and conditions. Combustible dust is excluded. Protect the device against impact, unauthorised modification, contamination and out-of-limit conditions. Keep the inlet, joints, antenna and cable accessible."),
    ("g.3 Mechanical installation", "Use the approved U-bolt plate in accordance with the controlled drawings and BOM; do not modify supporting structures without the site owner's approval. Ensure the mounting does not loosen, rotate or shift under foreseeable vibration and loads. Follow the final orientation and torque values. Avoid impact, deformation, and an inlet obstructed by walls, pipes or plates."),
    ("g.4 Gas inlet and sensing area", "The front mesh, air path, DC fan and the eight MQ sensors must remain exposed to ambient air. Do not cover, paint, tape, add filters/membranes or alter the gas path without approval. Do not damage the sensors' built-in protective mesh. The protective function of the mesh is to be proven by type testing."),
    ("g.5 Electrical supply", "Use 24 VDC continuous; the 220 VAC/50 Hz to 24 VDC adaptor is outside the equipment boundary. Internal rails: 5 VDC for sensors/heaters and 3.3 VDC for logic. Verify polarity and connections of terminals, cable, PE and upstream protection. The circuit includes PTC, TVS and other protection. Input tolerance, inrush current, upstream fuse rating, conductor size and terminal data are set in the final specification."),
    ("g.6 Cable entry", "Thread M20 × 1.5. Use only glands, adaptors, blanking plugs and seals approved for the Ex concept, gas group, thread, IP rating, cable outer diameter and installation temperature. The prototype polymer gland is not a final component. Do not modify openings or leave openings unsealed. Follow the supplier's sealing/clamping sequence and torque; record the part number and certificate reference."),
    ("g.7 Grounding and bonding", "Connect the enclosure to protective earth (PE) via the approved stud and lug; ensure contact surfaces, washers and fasteners match the drawing. Verify continuity before energising and after servicing. Do not assume circuit GND is the same as PE."),
    ("g.8 Antenna installation", "The LoRa antenna is on top of the base with an SMA interface and internal RF cable. Use the position, model, seal and mounting per the approved BOM/drawing. Do not replace or alter penetrations, cables, fittings and antenna without review."),
    ("g.9 Commissioning", "Before energising, check area suitability, enclosure condition, mesh, fan, gland/plug/seal, 24 VDC polarity, PE continuity, antenna and mounting. After power-up, confirm that sensors, fan, alarm and communication initialise without faults. Perform nulling in clean air and accept only an 8/8 result. Verify the local alarm and reception of data/alarms at the Cluster Head/Gateway; perform gas tests only under an official procedure. Record model, serial, hardware, firmware/AI, date, voltage, nulling and alarm results."),
    ("g.10 Operating modes", "Inference Mode: normal operation, gas classification and local/LoRa alarms. Dataset Mode: data collection for controlled engineering work. Nulling Mode: sensor baseline adjustment in clean air, must be 8/8. Return to Inference Mode after the activity is complete and confirm there are no faults."),
    ("g.11 Normal operation", "After successful commissioning and nulling, run Inference Mode. Check power, enclosure condition, diagnostics, communication status and faults each operating period. Do not change firmware/model, thresholds, calibration parameters or Ex features without approval. If communication is lost or a fault is unresolved, inform the operator and apply the site impairment procedure."),
    ("g.12 Alarm and fault handling", "Alarms have two parallel paths: local LED/buzzer and LoRa notification. Loss of LoRa is not evidence that no gas is present. Treat every alarm as a real process safety event until site procedures prove otherwise. Do not disable, reset or change parameters to hide alarms/faults."),
    ("g.13 Cleaning", "Isolate per procedure. Use a soft lint-free cloth slightly moistened with clean water or an approved mild cleaner. Do not use abrasives, aggressive solvents, compressed air or high-pressure sprays; do not allow liquid ingress. Inspect the mesh, seals, gaskets and penetrations; do not pierce the mesh."),
    ("g.14 Periodic inspection and maintenance", "Authorised personnel follow the schedule below; intervals may be shortened according to site conditions. Isolate 24 VDC, apply LOTO and confirm the area is safe before opening. Record serial number, date, condition, findings, actions, replaced parts, nulling/test/PE results, software version and personnel."),
    ("g.15 Sensor nulling and calibration", "Perform after start-up and stabilisation, without faults, in confirmed clean air. The result must be 8/8; if not, find the cause, correct and repeat. Nulling is not a means to mask drift, contamination or faults. Gas calibration requires an approved procedure, reference gas and equipment."),
    ("g.16 Inspection of Ex-critical parts", "Inspect the enclosure, cover, mesh, joints/threads, gaskets, glands, adaptors/plugs, bonding, antenna, beacon, fan and MQ modules. Verify part numbers, materials, fitting, retention, engagement and sealing; there must be no corrosion, wear, cracks, deformation, contamination or unapproved modification."),
    ("g.17 Firmware and configuration control", "Only firmware and AI model versions approved for the relevant hardware revision may be used. Identify version/build/hash and record per unit. Changes to acquisition, classification, alarm, fan, power, communication and diagnostics must be evaluated, approved and capable of rollback."),
    ("g.18 Repair restrictions", "Repairs shall be carried out only by authorised personnel, following approved procedures and using approved replacement parts. Do not drill, weld, modify threads, enlarge openings, bypass protection or file/grind/coat flame paths. Inspect and function-test before returning the unit to service."),
    ("g.19 Storage and transport", "Use packaging that protects against impact, vibration, humidity, corrosion and dust. Protect the mesh, antenna, threads, sealing surfaces, cable entry and PE stud. Remove temporary inlet protection before operation and inspect the unit before energising."),
    ("g.20 Decommissioning", "Isolate and verify the supply is de-energised, apply LOTO and confirm the area is safe. Disconnect power, PE, antenna, communication and mounting; secure remaining cables. Mark the unit as decommissioned and dispose of electronics/metal/PCB according to site rules."),
]


def build_02():
    no = "GLD/ATEX-UM/2026-001-EN"
    d = new_doc(no, "02 User Manual")
    title_block(d, "GLD V2 User Manual", "Installation, operation, inspection and maintenance", no,
                "Response to TÜV SÜD request: User manual")
    note(d, "Draft for review. Not to be used for installation in explosive atmospheres before the certificate is issued.")
    d.add_heading("1. Product description", level=1)
    para(d, "GLD V2 is a fixed-point gas detector. Ambient air enters through a stainless-steel mesh; a DC fan assists the flow "
            "to eight MQ sensors. The ESP32-S3 performs on-device AI classification (Clean Air, LPG, H₂); visual/audible alarms "
            "and LoRa notifications are activated when the alarm criteria are met. The confidence threshold ≥ 30 % is not a gas "
            "concentration or %LEL. The GLD is not intended as the sole protection system.")
    table(d, [
        ["Parameter", "Specification"],
        ["Supply", "24 VDC continuous; max. ±8 W (≈ 0.33 A); PSU ≥ 1 A per unit"],
        ["Sensors", "MQ-2, MQ-3B, MQ-4, MQ-5, MQ-6, MQ-7B, MQ-8, MQ-135"],
        ["Acquisition", "ADS1256, 24-bit; scan interval 500 ms"],
        ["Communication", "LoRa E22-900MM22S, 920–923 MHz; routine report every 10 s, alarms immediately"],
        ["RS-485", "Modbus RTU read-only, 9600 bit/s, 8N1, Unit ID 1; 8 registers"],
        ["Environment", "−20 to +60 °C (upper limit under review); 5–95 % RH non-condensing; IP66 target"],
        ["Ex target", "II 2G Ex db IIC T4 Gb; gas only; not yet certified"],
    ], [3.4, TW - 3.4])
    d.add_heading("2. Safety, installation and operating instructions", level=1)
    for h, t in MANUAL:
        d.add_heading(h, level=2); para(d, t)
        if h.startswith("g.12"):
            table(d, [
                ["Condition", "Action"],
                ["Gas alarm", "Follow the site emergency gas response procedure"],
                ["Sensor fault / nulling not 8/8", "Investigate, repair, repeat nulling in clean air"],
                ["LoRa communication lost", "Inform the operator; apply the site impairment procedure"],
                ["Local alarm failure", "Remove from service, repair and verify"],
                ["Grounding fault", "Isolate until continuity is restored"],
                ["Water ingress / damaged enclosure", "Remove from service, inspect before re-commissioning"],
            ], [6.0, TW - 6.0])
        if h.startswith("g.14"):
            table(d, [
                ["Interval", "Minimum activities"],
                ["Daily / each shift", "Power, enclosure, diagnostics, faults, LoRa"],
                ["Every 3 months", "Mesh, MQ area, contamination/blockage, damage"],
                ["Every 6 months", "Alarm test, nulling 8/8, fan, threads and interfaces"],
                ["Annually", "Full inspection: PE/bonding, gland/terminals, gaskets, antenna, alarm, LoRa, sensor life"],
            ], [4.0, TW - 4.0])
    d.add_heading("3. Terminals and field wiring", level=1)
    para(d, "The BAT terminals are not used in the 24 VDC configuration. The service port and RS-485 are not production control paths.")
    m = [x for x in FIG if x["file"].startswith("m")][0]
    figure(d, A / m["file"], "MS-06 — terminals and field wiring, GLD V4 terminal board (not to scale).", max_h=12)
    d.add_heading("4. To be completed before the final manual", level=1)
    para(d, "Special conditions of the certificate, gas detection performance, calibration gases and intervals, torque values, "
            "supply limits, orientation/clearance, Ex components, IP66 evidence, approved firmware/AI versions.")
    f = OUT / "02_User_Manual_GLD_V2_EN.docx"; d.save(f); return f


# ================================================================== 03
def build_03():
    no = "GLD/ATEX-EX/2026-001-EN"
    d = new_doc(no, "03 Target Ex Marking")
    title_block(d, "Target Ex Marking", "Proposed ATEX/IECEx classification, nameplate and preliminary temperature-class evaluation", no,
                "Response to TÜV SÜD request: Target Ex marking")
    d.add_heading("1. Proposed marking", level=1)
    for line in ("ATEX:   ⟨Ex⟩ II 2G  Ex db IIC T4 Gb", "IECEx:   Ex db IIC T4 Gb", "−20 °C ≤ Ta ≤ +60 °C   ·   IP66 (target)"):
        p = d.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(line); r.bold = True; r.font.size = Pt(13); r.font.color.rgb = NAVY
        p.paragraph_format.space_after = Pt(2)
    d.add_paragraph()
    table(d, [
        ["Element", "Meaning", "Status"],
        ["II", "Group II equipment (non-mining)", "Proposed"],
        ["2G", "Category 2, gas atmospheres — Zone 1", "Proposed"],
        ["Ex db", "Flameproof enclosure", "Proposed"],
        ["IIC", "Gas group IIC (covers H₂)", "Proposed"],
        ["T4", "Maximum surface temperature 135 °C", "Proposed; preliminary evaluation in §3"],
        ["Gb", "Equipment Protection Level Gb", "Proposed"],
        ["Ta", "−20 to +60 °C", "Upper limit under review: base housing rating +55 °C"],
        ["Dust", "Not applied for", "Gas only"],
    ], [2.4, 7.5, 6.7])
    note(d, "Proposal — not certified. This marking must not be applied as a certification claim.")
    d.add_heading("2. Proposed nameplate", level=1)
    table(d, [
        ["Element", "Content / status"],
        ["Manufacturer", "Manufacturer name and address — to be entered once confirmed"],
        ["Product", "Gas Leak Detector — GLD V2"],
        ["Serial number / year", "Per unit; sample example GLD2-0x1001"],
        ["Marking", "Hexagon Ex symbol, II 2G; Ex db IIC T4 Gb — proposed"],
        ["Rating", "24 VDC, 8 W max.; Ta −20 to +60 °C; IP66 target"],
        ["Cable entry", "M20 × 1.5"],
        ["Certificate", "ATEX/IECEx and CE/notified body numbers entered after issue"],
        ["Warning", "WARNING – DO NOT OPEN WHEN AN EXPLOSIVE ATMOSPHERE MAY BE PRESENT, plus warnings per certificate"],
        ["Location & material", "Flat top face of the base beside the antenna; 80 × 55 mm stainless steel plate 0.5 mm, etched/engraved; 4 rivets or adhesive"],
    ], [3.6, TW - 3.6])
    x = [f for f in FIG if f["file"].startswith("x")][0]
    figure(d, A / "x00_en.jpg", "MS-05 — proposed nameplate artwork (not a certified marking).", max_h=7)
    figure(d, A / "nameplate_mockup_figure.jpg", "Illustration of the nameplate position on the unit: flat top face of the base beside the antenna (proposal, not a certified marking). Right: detail.", crop=False, max_h=7.8)
    d.add_heading("3. Preliminary T4 temperature-class evaluation", level=1)
    para(d, "The T4 limit is 135 °C; the evaluation uses an effective limit of 130 °C (5 K margin). Internal measurement with "
            "eight thermocouples, 180 minutes per condition, extrapolated to Ta +60 °C: T(Ta,max) = Ta,max + (T measured − Ta test).")
    table(d, [
        ["Condition", "MQ sensor body", "PCB", "Outer enclosure"],
        ["Normal", "44.2 → ≈ 79 °C", "52.4 → ≈ 88 °C", "32.1 → ≈ 67 °C"],
        ["Maximum load", "55.0 → ≈ 91 °C", "58.3 → ≈ 94 °C", "34.8 → ≈ 71 °C"],
        ["Fan stalled", "78.4 → ≈ 114 °C", "63.4 → ≈ 99 °C", "43.9 → ≈ 79 °C"],
    ], [4.1, 4.1, 4.1, 4.3])
    table(d, [
        ["Ref.", "Potential hot spot", "Status"],
        ["T-01", "MQ heater/body", "Measured"],
        ["T-02", "Fan motor/electronics", "Measured"],
        ["T-03–07", "5 V converter, 3.3 V regulator, inductor, MOSFET/protection", "Not yet measured"],
        ["T-08", "ESP32-S3 / PCB hot spot", "Measured; maximum load not yet stable"],
        ["T-09", "LoRa at maximum TX", "Not yet measured"],
        ["T-10", "Alarm LED/buzzer active", "Not yet measured"],
        ["T-11", "Outer enclosure surface", "Measured"],
        ["T-12", "Mesh/front cover", "Not yet measured"],
    ], [2.2, 8.7, 5.7])
    para(d, "These are preliminary internal test results, not certification results. The method and testing at maximum ambient are to be confirmed with the certification body.", size=9.5, italic=True)
    d.add_heading("4. Evidence still required", level=1)
    bullets(d, [
        "Controlled flame-path drawings, enclosure material data and Ex db IIC type testing.",
        "Proof of the front mesh as a flame-path element (certificate or test).",
        "Ex d IIC glands, plugs/adaptors, beacon and antenna feed-through that are suitable or covered by the equipment assessment.",
        "Certificate of the base housing HIREP HRP-T1000-A (supplier claim Ex d IIC T6 Gb, −20…+55 °C, IP66). The supplier's T6 rating applies to contents ≤ 3 W and is not claimed for the GLD (±8 W).",
        "IP66 evidence and final temperature test results.",
    ])
    f = OUT / "03_Target_Ex_Marking_GLD_V2_EN.docx"; d.save(f); return f


# ================================================================== 04
def build_04():
    no = "GLD/ATEX-IP/2026-001-EN"
    d = new_doc(no, "04 IP66 Status")
    title_block(d, "IP66 Status and Verification Plan", "Ingress protection — design target and test evidence", no,
                "Response to TÜV SÜD request: IP66")
    note(d, "Summary: IP66 is a design target and has not yet been tested on GLD V2.")
    d.add_heading("1. Target and claim limits", level=1)
    para(d, "IP66 means dust-tight (IP6X) and protected against powerful water jets (IPX6) according to IEC 60529. The assessment "
            "covers the complete GLD unit, not only the gland or housing. The gas inlet is intentionally open to ambient air, so "
            "compatibility of the mesh with IP66 must be proven without impairing gas sampling.")
    d.add_heading("2. Sealing interfaces", level=1)
    table(d, [
        ["Interface", "Current condition / action"],
        ["Front mesh and retention", "Stainless steel; grade, pore size, thickness and retention to be specified and validated"],
        ["Cover / O-ring", "Rubber O-ring, cord 2.70 mm, OD ≈ 91 mm; material, hardness and temperature range to be specified"],
        ["24 VDC cable entry", "M20 × 1.5; prototype polymer gland to be replaced by a metal Ex d gland with a suitable IP rating"],
        ["Other penetrations", "Blanking plug, antenna feed-through, beacon to be verified against the final design"],
        ["Base housing", "Supplier claims IP66/67 for the original housing; not automatically valid after the front window is replaced by mesh and a fan is added"],
    ], [4.2, TW - 4.2])
    d.add_heading("3. Verification plan (proposed)", level=1)
    bullets(d, [
        "Freeze the sample configuration: BOM, drawing revision, gland/cable, seals, closing torque and orientation; document photos and serial numbers.",
        "Agree the test standard and edition (IEC 60529), sequence, conditions, number of samples and acceptance criteria with TÜV SÜD.",
        "A competent laboratory performs IP6X (dust) and IPX6 (water jet) tests.",
        "Post-test ingress inspection and function test: gas sampling, alarm and communication.",
    ], style="List Number")
    d.add_heading("4. Evidence to be submitted", level=1)
    para(d, "Laboratory report, sample identification, final sealing and assembly drawings, component datasheets/certificates, test photographs.")
    f = OUT / "04_IP66_Status_GLD_V2_EN.docx"; d.save(f); return f


# ================================================================== 05
def build_05():
    no = "GLD/ATEX-QMS/2026-001-EN"
    d = new_doc(no, "05 ISO 9001 Status")
    title_block(d, "ISO 9001 Certification Status", "Manufacturer quality management system and QAR/QAN preparation", no,
                "Response to TÜV SÜD request: ISO 9001 certificate")
    note(d, "Summary: the manufacturer's ISO 9001 certification is in progress; a copy of the certificate will be submitted once issued.")
    d.add_heading("1. Manufacturer", level=1)
    table(d, [
        ["Item", "Description"],
        ["Manufacturer", "Applicant manufacturer — identity stated in the application form"],
        ["Production site", "Serial production site to be fixed after the prototype stage"],
        ["PCB assembly", "PCB fabrication and assembly by a contract PCB assembly provider"],
    ], [3.6, TW - 3.6])
    d.add_heading("2. ISO 9001 status", level=1)
    para(d, "The manufacturer's ISO 9001 certification is in progress; the certification audit was scheduled for October 2026. "
            "Certificate number, scope, issuing body and validity will be provided once the certificate is issued.")
    d.add_heading("3. Quality system documents", level=1)
    table(d, [
        ["Document", "Status / action"],
        ["ISO 9001 certificate", "Submitted once issued; scope and sites checked for consistency"],
        ["Quality manual and procedure index", "In preparation"],
        ["Ex production quality", "IECEx QAR and ATEX QAN/product verification route to be confirmed with TÜV SÜD"],
        ["Organisation", "Responsible persons for design, production and quality, and contacts, to be defined"],
    ], [5.0, TW - 5.0])
    para(d, "Note: under both IECEx and ATEX, the manufacturer must demonstrate an Ex production quality system (QAR/QAN) "
            "irrespective of ISO 9001; ISO 9001 generally shortens that assessment.", size=9.5, italic=True)
    f = OUT / "05_ISO_9001_Status_GLD_V2_EN.docx"; d.save(f); return f


if __name__ == "__main__":
    docs = [build_00(), build_01(), build_02(), build_03(), build_04(), build_05()]
    pdfs = [to_pdf(x) for x in docs]
    w = PdfWriter()
    labels = ["00 Product Introduction", "01 Assembly Drawings", "02 User Manual", "03 Target Ex Marking", "04 IP66 Status", "05 ISO 9001 Status"]
    for lab, pdf in zip(labels, pdfs):
        start = len(w.pages)
        for pg in PdfReader(str(pdf)).pages:
            w.add_page(pg)
        w.add_outline_item(title=lab, page_number=start)
    comb = OUT / "GLD_V2_TUV_SUD_Discussion_Package_Complete_EN.pdf"
    with open(comb, "wb") as f:
        w.write(f)
    for p in pdfs + [comb]:
        print(p.name, len(PdfReader(str(p)).pages), "pp", round(p.stat().st_size / 1e6, 1), "MB")
