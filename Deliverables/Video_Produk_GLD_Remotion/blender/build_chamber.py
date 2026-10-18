# Shot 3: gas test chamber (Adegan 5), dibangun dari LAPORAN PROGRESS CHAMBER GAS.pdf + foto chamber_*.
# Kotak akrilik bening (pintu depan, klem toggle merah, pegangan stainless), pelat belakang logam dengan GLD V2,
# kipas pengaduk 120 mm, papan sensor acuan di dalam (modul gas + modul suhu/tekanan/kelembapan),
# papan kontrol kayu di samping (PSU, terminal, mikrokontroler, relay, step-down, driver pompa,
# solenoid valve, pompa hisap), tabung gas generik + regulator, selang hijau (masuk) dan merah (buang).
# Tanpa tulisan/logo komponen. Sorotan biru #2B5FCB berurutan sesuai legenda Remotion (Scene05Trainable).
#
#   blender -b -P build_chamber.py -- <out_dir> [still|anim|frame:<detik>|none] [samples] [landscape|portrait]
import math
import runpy
import sys
from pathlib import Path

import bpy
from mathutils import Vector

HERE = Path(__file__).resolve().parent
ARGS = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
OUT = Path(ARGS[0]).resolve() if ARGS else HERE / "preview"
MODE = ARGS[1] if len(ARGS) > 1 else "still"
SAMPLES = int(ARGS[2]) if len(ARGS) > 2 else 24
ORIENT = ARGS[3] if len(ARGS) > 3 else "landscape"

# Bangun GLD + material + render setting dari skrip GLD (tanpa render).
sys.argv = [sys.argv[0], "--", str(OUT), "none", str(SAMPLES)]
G = runpy.run_path(str(HERE / "build_gld_model.py"))
MM, cyl, box, torus, finish, boolean, principled, add_bump, new_obj, apply_tf = (
    G[k] for k in ("MM", "cyl", "box", "torus", "finish", "boolean", "principled", "add_bump", "new_obj", "apply_tf"))
scene = bpy.context.scene
for name in ("floor", "key", "fill", "rim_blue", "rim_warm", "top", "cable24"):
    if name in bpy.data.objects:
        bpy.data.objects.remove(bpy.data.objects[name])

M_STEEL, M_STEEL_POL, M_RUBBER, M_PCB, M_IC, M_TERMINAL, M_NICKEL, M_GOLD, M_FAN, M_SHIELD = (
    G[k] for k in ("M_STEEL", "M_STEEL_POL", "M_RUBBER", "M_PCB", "M_IC", "M_TERMINAL", "M_NICKEL", "M_GOLD",
                   "M_FAN", "M_SHIELD"))
M_ACRYLIC = principled("acrylic", (0.96, 0.98, 1.0), 0, 0.02, **{"Transmission Weight": 1.0, "IOR": 1.49})
M_ALPLATE = add_bump(principled("back_plate", (0.55, 0.56, 0.58), 1, 0.38, **{"Anisotropic": 0.5}),
                     "noise", 2500, 0.05, stretch=(1, 1, 60))
M_WOOD = add_bump(principled("plywood", (0.42, 0.28, 0.16), 0, 0.6), "noise", 120, 0.15)
M_BENCH = add_bump(principled("lab_bench", (0.035, 0.036, 0.04), 0, 0.5), "noise", 400, 0.03)
M_RED_CLAMP = principled("clamp_red", (0.6, 0.02, 0.02), 0, 0.35)
M_GREEN_HOSE = principled("hose_green", (0.02, 0.35, 0.08), 0, 0.3, **{"Coat Weight": 0.4})
M_RED_HOSE = principled("hose_red", (0.45, 0.02, 0.02), 0, 0.25, **{"Transmission Weight": 0.25})
M_BLACK = principled("black_plastic", (0.02, 0.02, 0.022), 0, 0.4)
M_BRASS = principled("brass", (0.85, 0.62, 0.28), 1, 0.25)
M_PSU = add_bump(principled("psu_case", (0.75, 0.76, 0.78), 1, 0.35), "weave", 400, 0.4, distance=0.0008)
M_CYL = add_bump(principled("cylinder_paint", (0.17, 0.18, 0.20), 0.2, 0.35, **{"Coat Weight": 0.5}),
                 "noise", 800, 0.05)
M_GAUGE = principled("gauge_face", (0.92, 0.92, 0.9), 0, 0.3)
M_MODULE_RED = principled("module_red", (0.65, 0.04, 0.03), 0, 0.35)
M_MODULE_PURPLE = principled("module_purple", (0.32, 0.08, 0.45), 0, 0.35)
M_MODULE_BLUE = principled("module_blue", (0.03, 0.12, 0.45), 0, 0.35)
M_PERF = add_bump(principled("perfboard", (0.05, 0.3, 0.12), 0, 0.4), "weave", 2000, 0.5)

ALL = []
HL = {1: [], 2: [], 3: [], 4: []}  # objek per sorotan


def add(obj, mat, hl=None, bevel=0.0):
    obj.data.materials.clear()
    obj.data.materials.append(mat)
    if obj.type == "MESH":
        finish(obj, bevel)
    ALL.append(obj)
    if hl:
        HL[hl].append(obj)
    return obj


def tube(name, pts, r, mat, hl=None):
    cu = bpy.data.curves.new(name, "CURVE")
    cu.dimensions = "3D"
    cu.bevel_depth = r * MM
    cu.bevel_resolution = 6
    cu.use_fill_caps = True
    sp = cu.splines.new("BEZIER")
    sp.resolution_u = 32
    sp.bezier_points.add(len(pts) - 1)
    for bp, p in zip(sp.bezier_points, pts):
        bp.co = Vector(p) * MM
        bp.handle_left_type = bp.handle_right_type = "AUTO"
    ob = new_obj(name, cu)
    ob.data.materials.append(mat)
    ALL.append(ob)
    if hl:
        HL[hl].append(ob)
    return ob


# ------------------------------------------------------------------ meja & chamber (mm, z=0 permukaan meja)
add(box("bench", (8000, 6000, 40), (-250, 1500, -20)), M_BENCH)

W, D, H, T = 460, 360, 560, 5
cx, cy = 0, 0
for name, size, loc in (("ac_left", (T, D, H), (-W / 2, 0, H / 2)),
                        ("ac_right", (T, D, H), (W / 2, 0, H / 2)),
                        ("ac_top", (W, D, T), (0, 0, H)),
                        ("ac_bottom", (W, D, T), (0, 0, T / 2)),
                        ("ac_door", (W - 4, T, H - 4), (0, -D / 2 - 3, H / 2))):
    add(box(name, size, loc), M_ACRYLIC, None, 1.0)
# rangka sudut aluminium siku
for sx in (-1, 1):
    for sy in (-1, 1):
        add(box(f"angle{sx}{sy}", (14, 14, H), (sx * (W / 2 - 7), sy * (D / 2 - 7), H / 2)), M_STEEL, 2, 0.5)
# pelat logam belakang (dudukan GLD)
# dinding belakang = pelat besi (bukan akrilik); semua lubang selang/udara ada di pelat ini
add(box("back_plate", (W + 4, 3, H), (0, D / 2 - 1.5, H / 2)), M_ALPLATE, 2, 0.5)
# klem toggle merah (kanan pintu) + engsel kiri + pegangan stainless di sisi
for z in (H - 70, 90):
    add(box(f"clamp_base{z}", (30, 18, 12), (W / 2 + 10, -D / 2 - 8, z)), M_STEEL, 2, 1.5)
    add(cyl(f"clamp_lever{z}", 5, 48, (W / 2 + 16, -D / 2 - 20, z + 6), "X", 32), M_RED_CLAMP, 2, 1.5)
    add(box(f"hinge{z}", (14, 10, 40), (-W / 2 + 4, -D / 2 - 8, z)), M_STEEL, 2, 1.0)
for sx in (-1, 1):
    add(cyl(f"handle_bar{sx}", 5, 110, (sx * (W / 2 + 28), 20, H / 2), "Z", 32), M_STEEL_POL, 2, 1.0)
    for dz in (-50, 50):
        add(cyl(f"handle_post{sx}{dz}", 4, 26, (sx * (W / 2 + 15), 20, H / 2 + dz), "X", 24), M_STEEL_POL, 2)
# karet seal pintu
add(box("door_seal", (W - 20, 4, 8), (0, -D / 2 + 1, H - 12)), M_RUBBER, 2)

# GLD V2 terpasang di pelat belakang, menghadap pintu
gld = G["ROOT"]
gld.location = Vector((0, D / 2 - 3 - 40, 335)) * MM
HL[2].extend(o for o in bpy.data.objects if o.type in ("MESH", "CURVE") and o.parent and
             (o.parent == gld or (o.parent.parent == gld)))
tube("gld_cable", [(-62 - 23, D / 2 - 7.5 - 20, 335 + 47), (-125, D / 2 - 30, 335 + 30), (-150, D / 2 - 12, 290),
                   (-150, D / 2 - 9, 250), (-150, D / 2 + 20, 250), (-150, D / 2 + 52, 240)], 4, G["M_CABLE"])
for gy in (D / 2 - 3.2, D / 2 + 0.2):  # grommet karet lubang kabel di pelat besi (muka depan & belakang)
    add(torus(f"grommet_gld{gy}", 6.5, 2.2, (-150, gy, 250)), M_RUBBER)

# kipas pengaduk 120 mm di dasar, posisi tidur (meniup ke atas) agar udara di dalam chamber homogen
fan_c = Vector((20, 30, T + 32))
fr = box("mix_fan", (120, 120, 25), fan_c)
boolean(fr, cyl("mix_fan_hole", 57, 40, fan_c, "Z"))
for sx in (-1, 1):
    for sy in (-1, 1):
        boolean(fr, cyl(f"mix_fan_sc{sx}{sy}", 2.2, 40, fan_c + Vector((sx * 52.5, sy * 52.5, 0)), "Z", 24))
        add(cyl(f"mix_leg{sx}{sy}", 3, 20, fan_c + Vector((sx * 52.5, sy * 52.5, -22.5)), "Z", 24), M_NICKEL)
add(fr, M_FAN, None, 2.0)
add(cyl("mix_hub", 20, 22, fan_c, "Z", 64), M_FAN, None, 1.5)
for i in range(7):
    bl = box(f"mix_blade{i}", (36, 24, 1.5), (0, 0, 0))
    bl.rotation_euler = (math.radians(30), 0, 0)
    apply_tf(bl)
    bl.location = Vector((38, 0, 0)) * MM
    apply_tf(bl)
    bl.rotation_euler = (0, 0, math.radians(i * 360 / 7))
    apply_tf(bl)
    bl.location = fan_c * MM
    apply_tf(bl)
    add(bl, M_FAN, None, 0.5)
gd = cyl("mix_guard", 58, 2, fan_c + Vector((0, 0, 13.5)), "Z", 64)
boolean(gd, cyl("mg_cut", 54, 6, fan_c + Vector((0, 0, 13.5)), "Z"))
add(gd, M_STEEL)
for k in range(4):  # jari-jari pelindung
    sp = box(f"mix_spoke{k}", (112, 2, 1.6), fan_c + Vector((0, 0, 13.5)))
    sp.rotation_euler = (0, 0, math.radians(k * 45))
    apply_tf(sp)
    add(sp, M_STEEL)
tube("wire_mixfan", [tuple(fan_c + Vector((55, 50, -5))), (60, D / 2 - 20, 15), (-25, D / 2 - 12, 22),
                     (-25, D / 2 + 20, 22), (-25, D / 2 + 52, 22)], 1.2, M_IC)


def sensor_board(prefix, loc, hl, with_gas=True):
    x, y, z = loc
    add(box(prefix + "_perf", (70, 50, 1.6), (x, y, z + 0.8)), M_PERF, hl, 0.3)
    if with_gas:  # modul sensor gas acuan: PCB merah + tabung logam
        add(box(prefix + "_gasmod", (32, 22, 1.6), (x + 12, y + 10, z + 3)), M_MODULE_RED, hl, 0.3)
        add(cyl(prefix + "_gascan", 8, 9, (x + 12, y + 10, z + 8.3), "Z", 48), M_STEEL, hl, 0.6)
        add(cyl(prefix + "_gasmesh", 6, 0.4, (x + 12, y + 10, z + 12.9), "Z", 48), G["M_WIRE"], hl)
    add(box(prefix + "_thp", (15, 12, 1.6), (x + 12, y - 12, z + 3)), M_MODULE_PURPLE, hl, 0.2)
    add(box(prefix + "_thp_chip", (2.5, 2.5, 1), (x + 15, y - 12, z + 4.3)), M_SHIELD, hl)
    for k in range(2):
        add(box(f"{prefix}_term{k}", (10, 16, 10), (x - 25, y + 10 - k * 20, z + 6.6)), M_TERMINAL, hl, 0.5)


# papan sensor acuan di dalam chamber (kiri bawah) + kabel keluar
sensor_board("in", (-150, -90, T), 3)
# ------------------------------------------------------------------ casing kontrol akrilik hitam di belakang chamber
# Berisi PSU, PCB kendali (mikrokontroler, relay, step-down, driver pompa), solenoid valve, dan pompa hisap.
M_SMOKE = principled("acrylic_black_smoked", (0.45, 0.45, 0.48), 0, 0.03,
                     **{"Transmission Weight": 0.95, "IOR": 1.49})
CX0, CX1 = -340, 100                # rentang X casing
CY0, CY1 = D / 2 + 50, D / 2 + 170  # rentang Y casing (celah 50 mm dari dinding belakang chamber)
CZ1 = 300
ccx, ccy, cw, cd = (CX0 + CX1) / 2, (CY0 + CY1) / 2, CX1 - CX0, CY1 - CY0
for name, size, loc in (("cs_front", (cw, T, CZ1), (ccx, CY0, CZ1 / 2)), ("cs_back", (cw, T, CZ1), (ccx, CY1, CZ1 / 2)),
                        ("cs_left", (T, cd, CZ1), (CX0, ccy, CZ1 / 2)), ("cs_right", (T, cd, CZ1), (CX1, ccy, CZ1 / 2)),
                        ("cs_top", (cw + 6, cd + 6, T), (ccx, ccy, CZ1)), ("cs_base", (cw, cd, T), (ccx, ccy, T / 2))):
    add(box(name, size, loc), M_SMOKE, None, 1.0)
for sx in (CX0 + 8, CX1 - 8):  # baut sudut tutup
    for sy in (CY0 + 8, CY1 - 8):
        add(cyl(f"cs_bolt{sx}{sy}", 3, 2, (sx, sy, CZ1 + 3.5), "Z", 24), M_NICKEL)
zt = T
add(box("psu", (159, 97, 38), (20, ccy + 5, zt + 19)), M_PSU, None, 1.0)
add(box("ctrl_pcb", (150, 100, 1.6), (25, ccy, zt + 120)), M_PCB, None, 0.3)  # PCB kendali di rak atas
for k, (x, y) in enumerate(((-40, -35), (90, -35), (-40, 35), (90, 35))):
    add(cyl(f"pcb_standoff{k}", 2.5, 80, (x, ccy + y, zt + 79), "Z", 16), M_NICKEL)
add(box("mcu_module", (18, 25, 3), (-15, ccy - 10, zt + 122.3)), M_SHIELD, None, 0.3)
add(box("relay_can", (19, 15, 15), (30, ccy + 25, zt + 128.3)), M_MODULE_BLUE, None, 0.8)
add(cyl("stepdown_ind", 6, 7, (65, ccy - 25, zt + 124.3), "Z", 32), M_IC, None, 0.8)
hs = box("driver_heatsink", (36, 36, 16), (75, ccy + 20, zt + 129))
for k in range(6):
    boolean(hs, box(f"fin{k}", (2.5, 40, 12), (60 + k * 6, ccy + 20, zt + 133)))
add(hs, M_STEEL, None, 0.4)
for k in range(6):
    add(box(f"ctrl_ic{k}", (5, 4, 1), (-45 + k * 12, ccy + 40, zt + 121.3)), M_IC)
add(box("ctrl_term", (60, 10, 10), (25, ccy - 44, zt + 126)), M_TERMINAL, None, 0.5)
# solenoid valve (gas sampel) & pompa hisap di ujung kiri casing (terlihat dari samping)
sv = Vector((CX0 + 70, ccy, 215))
add(cyl("sv_coil", 16, 32, sv + Vector((0, 0, 14)), "Z", 48), M_BLACK, 1, 2.0)
add(box("sv_body", (40, 22, 18), sv - Vector((0, 0, 10))), M_BRASS, 1, 1.5)
for sx in (-1, 1):
    add(cyl(f"sv_port{sx}", 5, 14, sv + Vector((sx * 26, 0, -10)), "X", 32), M_BRASS, 1, 0.5)
pump = Vector((CX0 + 85, ccy, 70))
add(cyl("pump_body", 26, 90, pump, "X", 64), M_BLACK, 4, 3.0)
add(cyl("pump_head", 22, 20, pump + Vector((-55, 0, 0)), "X", 64), M_BLACK, 4, 2.0)
add(cyl("pump_nip_in", 3.5, 16, pump + Vector((-60, 0, 22)), "Z", 24), M_BRASS, 4, 0.4)
add(cyl("pump_nip_out", 3.5, 16, pump + Vector((-72, 0, -6)), "X", 24), M_BRASS, 4, 0.4)
add(box("pump_mount", (70, 50, 6), (pump.x, pump.y, zt + 3)), M_STEEL, 4, 0.5)
# kipas pendingin casing (12 V) di muka belakang + kisi
add(box("cs_fan", (60, 12, 60), (40, CY1 - 9, 210)), M_FAN, None, 1.0)
add(cyl("cs_fan_grille", 28, 2, (40, CY1 + 3.5, 210), "Y", 48), M_STEEL)
# sensor suhu/tekanan/kelembapan acuan LUAR: di sisi kanan luar casing
mod = Vector((CX1 + 4, ccy, 200))
add(box("out_perf", (2, 50, 40), mod + Vector((1, 0, 0))), M_PERF, 3, 0.3)
add(box("out_thp", (1.6, 15, 12), mod + Vector((3, -8, 5))), M_MODULE_PURPLE, 3, 0.2)
add(box("out_thp_chip", (1, 2.5, 2.5), mod + Vector((4.3, -10, 5))), M_SHIELD, 3)
add(box("out_term", (10, 16, 10), mod + Vector((6, 12, -8))), M_TERMINAL, 3, 0.5)

# ------------------------------------------------------------------ lubang chamber
# BAWAH dinding belakang: (a) gas sampel masuk dari valve, (b) udara masuk (bukaan ber-filter, tanpa selang).
# ATAS (atap, dekat belakang): exhaust, dihisap pompa lalu dibuang lewat selang ke titik aman.
PORT_IN = Vector((-150, D / 2, 32))
PORT_AIR = Vector((60, D / 2, 32))
PORT_EXH = Vector((-150, D / 2, H - 35))
add(cyl("port_in", 5, 26, PORT_IN, "Y", 32), M_BRASS, 1, 0.5)
add(cyl("port_in_nut", 8, 4, PORT_IN + Vector((0, 6, 0)), "Y", 6), M_BRASS, 1, 0.4)
add(cyl("nozzle_in", 4, 40, PORT_IN - Vector((0, 26, 0)), "Y", 24), M_STEEL, 1, 0.4)
add(cyl("port_air", 12, 12, PORT_AIR + Vector((0, 4, 0)), "Y", 48), M_STEEL, None, 0.6)
add(cyl("port_air_filter", 10, 2, PORT_AIR + Vector((0, 11, 0)), "Y", 48), G["M_WIRE"])
add(cyl("port_exh", 5, 26, PORT_EXH, "Y", 32), M_BRASS, 4, 0.5)
add(cyl("port_exh_nut", 8, 4, PORT_EXH + Vector((0, 6, 0)), "Y", 6), M_BRASS, 4, 0.4)
# fitting & grommet casing
add(cyl("cs_fit_gasin", 5, 14, (CX0 - 6, ccy, 205), "X", 24), M_BRASS, 1, 0.4)
add(cyl("cs_fit_gasout", 5, 14, (-150, CY0 - 6, 32), "Y", 24), M_BRASS, 1, 0.4)
add(cyl("cs_fit_exhin", 5, 14, (-200, ccy, CZ1 + 6), "Z", 24), M_BRASS, 4, 0.4)
add(cyl("cs_fit_exhout", 5, 14, (CX0 - 6, ccy, 64), "X", 24), M_BRASS, 4, 0.4)
add(torus("cs_grm_gld", 6.5, 2.2, (-150, CY0 - 3, 240)), M_RUBBER)
add(torus("cs_grm_sensor", 4.5, 1.8, (-60, CY0 - 3, 22)), M_RUBBER)
add(torus("cs_grm_power", 6.5, 2.2, (CX1 + 3, ccy + 30, 40), "X"), M_RUBBER)

# tabung gas generik + regulator (tanpa label/warna kode), di kiri chamber
gc = Vector((-600, -170, 0))
add(cyl("gas_cyl", 75, 420, gc + Vector((0, 0, 210)), "Z", 96), M_CYL, 1, 25.0)
add(cyl("gas_ring", 76, 8, gc + Vector((0, 0, 30)), "Z", 96), M_STEEL, 1, 1.0)
add(cyl("gas_neck", 22, 30, gc + Vector((0, 0, 432)), "Z", 64), M_BRASS, 1, 2.0)
add(cyl("gas_valve", 14, 40, gc + Vector((0, 0, 465)), "Z", 48), M_BRASS, 1, 2.0)
add(cyl("gas_handwheel", 24, 6, gc + Vector((0, 0, 490)), "Z", 48), M_BLACK, 1, 1.5)
reg = gc + Vector((30, 0, 460))
add(cyl("reg_body", 20, 46, reg, "X", 48), M_BRASS, 1, 2.0)
for k, off in enumerate((Vector((10, -22, 15)), Vector((-10, -22, 15)))):
    add(cyl(f"gauge{k}", 22, 14, reg + off + Vector((0, -8, 10)), "Y", 64), M_STEEL_POL, 1, 1.5)
    add(cyl(f"gauge_face{k}", 19, 1, reg + off + Vector((0, -15.6, 10)), "Y", 64), M_GAUGE, 1)
    add(box(f"gauge_needle{k}", (1.2, 0.6, 14), reg + off + Vector((3, -16.3, 14))), M_IC, 1)

# ------------------------------------------------------------------ selang (satu warna per fungsi, tanpa persilangan)
# HIJAU = gas sampel: regulator -> solenoid valve (dalam casing) -> lubang bawah dinding belakang
tube("hose_gas1", [tuple(reg + Vector((25, 0, 0))), (-500, -60, 470), (-430, CY0 - 10, 330),
                   (CX0 - 13, ccy, 205)], 5, M_GREEN_HOSE, 1)
tube("hose_gas_int1", [tuple(sv + Vector((-33, 0, -10))), (CX0 + 15, ccy, 205), (CX0 + 1, ccy, 205)], 3,
     M_GREEN_HOSE, 1)
tube("hose_gas_int2", [tuple(sv + Vector((33, 0, -10))), (-170, ccy, 150), (-150, ccy - 20, 40),
                       (-150, CY0 + 2, 32)], 3, M_GREEN_HOSE, 1)
tube("hose_gas2", [(-150, CY0 - 13, 32), (-150, (CY0 + D / 2) / 2, 32), (-150, D / 2 + 13, 32)], 5,
     M_GREEN_HOSE, 1)
# MERAH = exhaust: lubang atap -> pompa (dalam casing)
tube("hose_exh", [tuple(PORT_EXH + Vector((0, 13, 0))), (-150, D / 2 + 55, H - 50), (-190, CY0 + 30, CZ1 + 90),
                  (-200, ccy, CZ1 + 13)], 5, M_RED_HOSE, 4)
tube("hose_exh_int", [(-200, ccy, CZ1 - 2), (-220, ccy, 200), tuple(pump + Vector((-60, 0, 30)))], 3, M_RED_HOSE, 4)
# HITAM = buangan pompa: keluar casing -> lantai -> jauh ke titik pembuangan aman (keluar frame)
tube("hose_out", [(CX0 - 13, ccy, 64), (CX0 - 60, ccy + 20, 30), (CX0 - 120, ccy + 120, 5),
                  (CX0 - 500, ccy + 900, 5), (CX0 - 1400, ccy + 2400, 5)], 5, M_BLACK, 4)
tube("hose_out_int", [tuple(pump + Vector((-80, 0, -6))), (CX0 + 1, ccy, 64)], 3, M_BLACK, 4)

# ------------------------------------------------------------------ kabel (hitam tipis, tidak berbagi jalur dengan selang)
tube("wire_sensor_in", [(-178, -80, T + 8), (-178, D / 2 - 30, T + 6), (-60, D / 2 - 12, 22), (-60, D / 2 + 20, 22),
                        (-60, CY0 - 2, 22)], 1.8, M_IC)
for gy in (D / 2 - 3.2, D / 2 + 0.2):
    add(torus(f"grommet_sensor{gy}", 4.5, 1.8, (-60, gy, 22)), M_RUBBER)
    add(torus(f"grommet_fan{gy}", 3.5, 1.4, (-25, gy, 22)), M_RUBBER)
tube("wire_power", [(CX1 + 6, ccy + 30, 40), (CX1 + 60, ccy + 60, 6), (CX1 + 200, ccy + 300, 3),
                    (CX1 + 700, ccy + 1200, 3)], 3.0, G["M_CABLE"])
tube("wire_pump", [(25, ccy - 40, zt + 118), (-100, ccy - 40, 80), tuple(pump + Vector((45, 0, 0)))], 1.2, M_IC)
tube("wire_valve", [(-10, ccy - 30, zt + 121), (-120, ccy - 30, 220), tuple(sv + Vector((0, 0, 30)))], 1.2, M_IC)
tube("wire_out_sensor", [(85, ccy - 35, zt + 121), (CX1 - 4, ccy - 10, 200), tuple(mod + Vector((2, 12, -8)))],
     1.2, M_IC)

# ------------------------------------------------------------------ sorotan
# Salinan tiap objek didorong 1 mm ke luar (Displace) dengan material cahaya tepi biru #2B5FCB:
# transparan di bagian yang menghadap kamera, bercahaya di tepi. Nilai "glow" 0..1 dianimasikan.
HL_AT = {1: 0.5, 2: 3.0, 3: 5.5, 4: 8.0}  # detik, sama dengan CHAMBER_PARTS[].at di Scene05Trainable.tsx
HL_GLOW = {}
for k in HL:
    m = bpy.data.materials.new(f"highlight_{k}")
    m.use_nodes = True
    nt = m.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    mix = nt.nodes.new("ShaderNodeMixShader")
    tr = nt.nodes.new("ShaderNodeBsdfTransparent")
    em = nt.nodes.new("ShaderNodeEmission")
    em.inputs["Color"].default_value = (0.17, 0.37, 0.80, 1)
    em.inputs["Strength"].default_value = 10.0
    lw = nt.nodes.new("ShaderNodeLayerWeight")
    lw.inputs["Blend"].default_value = 0.25
    pw = nt.nodes.new("ShaderNodeMath")
    pw.operation = "POWER"
    pw.inputs[1].default_value = 2.0
    glow = nt.nodes.new("ShaderNodeValue")
    glow.outputs[0].default_value = 0.0
    mul = nt.nodes.new("ShaderNodeMath")
    mul.operation = "MULTIPLY"
    mul.use_clamp = True
    nt.links.new(lw.outputs["Facing"], pw.inputs[0])
    nt.links.new(pw.outputs[0], mul.inputs[0])
    nt.links.new(glow.outputs[0], mul.inputs[1])
    nt.links.new(mul.outputs[0], mix.inputs["Fac"])
    nt.links.new(tr.outputs[0], mix.inputs[1])
    nt.links.new(em.outputs[0], mix.inputs[2])
    nt.links.new(mix.outputs[0], out.inputs["Surface"])
    HL_GLOW[k] = glow
    for ob in HL[k]:
        if ob.type not in ("MESH", "CURVE") or (ob.type == "MESH" and not ob.data.polygons):
            continue
        dup = ob.copy()
        dup.data = ob.data.copy()
        dup.data.materials.clear()
        dup.data.materials.append(m)
        dup.parent = ob.parent
        dup.matrix_world = ob.matrix_world.copy()
        scene.collection.objects.link(dup)
        if ob.type == "CURVE":
            dup.data.bevel_depth = ob.data.bevel_depth + 1.0 * MM
        else:
            dup.modifiers.clear()
            d = dup.modifiers.new("push", "DISPLACE")
            d.mid_level = 0.0
            d.strength = 1.0 * MM
        dup.visible_shadow = False
        dup.visible_diffuse = dup.visible_glossy = False


def animate_highlights(fps=30):
    for k, glow in HL_GLOW.items():
        t0 = HL_AT[k]
        sock = glow.outputs[0]
        for t, v in ((0, 0), (t0, 0), (t0 + 0.35, 1), (t0 + 2.2, 1), (t0 + 2.7, 0)):
            sock.default_value = v
            sock.keyframe_insert("default_value", frame=int(t * fps) + 1)


# ------------------------------------------------------------------ studio, kamera, render
for name, loc, size, power, color in (("ch_key", (-500, -900, 900), 900, 26, (1, 0.96, 0.92)),
                                      ("ch_fill", (700, -700, 300), 900, 18, (0.85, 0.9, 1.0)),
                                      ("ch_rim", (200, 900, 900), 600, 40, (0.4, 0.6, 1.0)),
                                      ("ch_top", (-600, 300, 1500), 500, 7, (1, 1, 1))):
    ld = bpy.data.lights.new(name, "AREA")
    ld.size = size * MM
    ld.energy = power
    ld.color = color
    lo = bpy.data.objects.new(name, ld)
    scene.collection.objects.link(lo)
    lo.location = Vector(loc) * MM
    lo.rotation_euler = (Vector((-250, 0, 250)) - Vector(loc)).to_track_quat("-Z", "Y").to_euler()
    lo.visible_camera = False
    if name in ("ch_top", "ch_rim", "ch_fill"):  # cegah pantulan blok putih di akrilik
        lo.visible_glossy = False
        lo.visible_transmission = False

cam = bpy.data.objects["cam"]
cam_d = cam.data
cam_d.dof.use_dof = False


def aim(loc, target):
    cam.location = Vector(loc) * MM
    cam.rotation_euler = ((Vector(target) - Vector(loc)) * MM).to_track_quat("-Z", "Y").to_euler()


# Kamera mengorbit dari depan-kiri (GLD terlihat) ke kiri-belakang (casing kontrol, valve, pompa terlihat).
# (detik, azimut deg [0 = depan, negatif = kiri], elevasi deg, jarak mm, target, lensa)
if ORIENT == "portrait":  # kotak tampil 952x380 di Remotion portrait; render 1,5x
    scene.render.resolution_x, scene.render.resolution_y = 1428, 570
    KEYS = [(0, -38, 16, 2000, (-220, 0, 250), 30), (3.5, -14, 12, 1800, (-80, 40, 290), 32),
            (6.5, -40, 16, 1800, (-120, 60, 230), 32), (9.5, -132, 24, 1800, (-150, 230, 200), 30),
            (20, -100, 26, 2000, (-200, 120, 230), 34)]
else:  # kotak tampil 640x420 di Remotion landscape; render 1,5x
    scene.render.resolution_x, scene.render.resolution_y = 960, 630
    KEYS = [(0, -38, 16, 1850, (-220, 0, 250), 34), (3.5, -14, 12, 1650, (-80, 40, 290), 38),
            (6.5, -40, 16, 1650, (-120, 60, 230), 36), (9.5, -132, 24, 1650, (-150, 230, 200), 34),
            (20, -100, 26, 1950, (-200, 120, 230), 38)]
TGT = bpy.data.objects.new("cam_target", None)
scene.collection.objects.link(TGT)
cam.constraints.clear()
tt = cam.constraints.new("TRACK_TO")
tt.target = TGT
tt.track_axis = "TRACK_NEGATIVE_Z"
tt.up_axis = "UP_Y"


def animate_camera(fps=30, seconds=20):
    scene.render.fps = fps
    scene.frame_start, scene.frame_end = 1, fps * seconds
    for t, az, el, dist, tgt, lens in KEYS:
        f = int(t * fps) + 1
        a, e = math.radians(az), math.radians(el)
        tv = Vector(tgt)
        pos = tv + Vector((dist * math.cos(e) * math.sin(a), -dist * math.cos(e) * math.cos(a), dist * math.sin(e)))
        cam.location = pos * MM
        TGT.location = tv * MM
        cam_d.lens = lens
        cam.keyframe_insert("location", frame=f)
        TGT.keyframe_insert("location", frame=f)
        cam_d.keyframe_insert("lens", frame=f)


# glow lembut untuk sorotan
scene.use_nodes = True
nt = scene.node_tree
rl = nt.nodes.get("Render Layers") or nt.nodes.new("CompositorNodeRLayers")
comp = nt.nodes.get("Composite") or nt.nodes.new("CompositorNodeComposite")
glare = nt.nodes.new("CompositorNodeGlare")
glare.glare_type = "FOG_GLOW"
glare.quality = "HIGH"
glare.threshold = 1.2
glare.size = 7
nt.links.new(rl.outputs["Image"], glare.inputs["Image"])
nt.links.new(glare.outputs["Image"], comp.inputs["Image"])

scene.cycles.samples = SAMPLES
animate_highlights()
animate_camera()
bpy.ops.wm.save_as_mainfile(filepath=str(HERE / f"chamber_{ORIENT}.blend"))

tag = "" if ORIENT == "landscape" else "_portrait"
if MODE == "still":
    for t in (1.5, 4.0, 6.5, 9.5, 19.0):
        scene.frame_set(int(t * 30) + 1)
        scene.render.filepath = str(OUT / f"chamber{tag}_{t:g}s.png")
        bpy.ops.render.render(write_still=True)
elif MODE.startswith("frame"):
    t = float(MODE.split(":")[1])
    scene.frame_set(int(t * 30) + 1)
    scene.render.filepath = str(OUT / f"chamber{tag}_cycles_{t:g}s.png")
    bpy.ops.render.render(write_still=True)
elif MODE in ("anim", "animc"):  # animc = Cycles (akrilik tampil benar), anim = EEVEE (cepat, akrilik gelap)
    if MODE == "anim":
        for eng in ("BLENDER_EEVEE_NEXT", "BLENDER_EEVEE"):
            try:
                scene.render.engine = eng
                break
            except TypeError:
                continue
    else:
        scene.render.resolution_percentage = 50
    scene.render.image_settings.file_format = "FFMPEG"
    scene.render.ffmpeg.format = "MPEG4"
    scene.render.ffmpeg.codec = "H264"
    scene.render.ffmpeg.constant_rate_factor = "HIGH"
    scene.render.filepath = str(OUT / f"chamber{tag}_preview.mp4")
    bpy.ops.render.render(animation=True)
print("SELESAI")
