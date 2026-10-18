# Shot 4 (Adegan 8, penutup) + close-up alarm (Adegan 7, opsional).
# GLD V2 terpasang pada tiang galvanis 2" (OD 60,3 mm) dengan pelat datar 250x250 mm dan dua U-bolt,
# sensor +-0,5 m dari tanah (spesifikasi material instalasi RU IV). Kamera mundur & naik memperlihatkan
# node GLD lain di area pipe rack yang terhubung garis cahaya biru (mesh LoRa) menuju gateway.
# Render EEVEE (tanpa kaca/akrilik, jauh lebih cepat dari Cycles).
#
#   blender -b -P build_outro.py -- <out_dir> [still|anim|alarm|alarm_still|none] [landscape|portrait]
import math
import random
import runpy
import sys
from pathlib import Path

import bpy
from mathutils import Vector

HERE = Path(__file__).resolve().parent
ARGS = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
OUT = Path(ARGS[0]).resolve() if ARGS else HERE / "preview"
MODE = ARGS[1] if len(ARGS) > 1 else "still"
ORIENT = ARGS[2] if len(ARGS) > 2 else "landscape"

sys.argv = [sys.argv[0], "--", str(OUT), "none"]
G = runpy.run_path(str(HERE / "build_gld_model.py"))
MM, cyl, box, torus, finish, principled, add_bump, new_obj = (
    G[k] for k in ("MM", "cyl", "box", "torus", "finish", "principled", "add_bump", "new_obj"))
scene = bpy.context.scene
for name in ("floor", "key", "fill", "rim_blue", "rim_warm", "top", "cable24"):
    if name in bpy.data.objects:
        bpy.data.objects.remove(bpy.data.objects[name])
random.seed(11)

M_STEEL, M_NICKEL, M_RUBBER, M_CABLE, M_LED = (G[k] for k in ("M_STEEL", "M_NICKEL", "M_RUBBER", "M_CABLE", "M_LED"))
M_GALV = add_bump(principled("galvanized", (0.62, 0.63, 0.64), 1, 0.45), "voronoi", 300, 0.25, distance=0.0004,
                  rough_var=(0.35, 0.6))
M_PLATE = add_bump(principled("plate_stainless", (0.70, 0.70, 0.72), 1, 0.3, **{"Anisotropic": 0.5}),
                   "noise", 2500, 0.05, stretch=(1, 1, 60))
M_CONCRETE = add_bump(principled("concrete", (0.035, 0.036, 0.04), 0, 0.55), "noise", 40, 0.25, distance=0.002)
M_RACK = principled("rack_steel", (0.05, 0.055, 0.06), 0.6, 0.5)
M_PIPE = principled("pipe_dark", (0.12, 0.12, 0.13), 0.8, 0.35)
M_COLUMN = principled("column_dark", (0.04, 0.045, 0.05), 0.5, 0.5)
M_LAMP = principled("lamp_warm", (1, 0.7, 0.35), 0, 0.3,
                    **{"Emission Color": (1, 0.62, 0.3, 1), "Emission Strength": 25})
M_LINK = principled("mesh_link", (0.2, 0.45, 1.0), 0, 0.3,
                    **{"Emission Color": (0.22, 0.48, 1.0, 1), "Emission Strength": 6})
M_PULSE = principled("mesh_pulse", (0.7, 0.85, 1.0), 0, 0.3,
                     **{"Emission Color": (0.75, 0.88, 1.0, 1), "Emission Strength": 40})
M_GW = principled("gateway_box", (0.75, 0.76, 0.78), 0.3, 0.4)

GROUND = -500.0  # sensor +-0,5 m dari tanah

# ------------------------------------------------------------------ node: GLD + pelat U-bolt + tiang
node_objs = []
root = G["ROOT"]


def descendants(o):
    out = [o]
    for c in o.children:
        out += descendants(c)
    return out


node_objs += descendants(root)


def nadd(obj, mat, bevel=0.0):
    obj.data.materials.clear()
    obj.data.materials.append(mat)
    finish(obj, bevel)
    node_objs.append(obj)
    return obj


POLE_Y = 45 + 30.15 + 2
nadd(box("mount_plate", (250, 5, 250), (0, 42.5, 5)), M_PLATE, 1.5)
for k, (x, z) in enumerate(((0, 84), (-57.5, -42), (57.5, -42))):  # baut telinga GLD ke pelat
    nadd(G["hexagon"](f"ear_bolt{k}", 13, 5, (x, 31.5, z), "Y"), M_NICKEL, 0.4)
    nadd(cyl(f"ear_washer{k}", 8, 1.2, (x, 33.4, z), "Y", 32), M_NICKEL)
for zb in (108, -95):  # dua U-bolt M10 melingkari tiang
    u = torus(f"ubolt{zb}", 30.15 + 5, 5, (0, POLE_Y, zb), "Z")
    bpy.ops.object.select_all(action="DESELECT")
    cut = box(f"ucut{zb}", (200, 120, 30), (0, POLE_Y - 60, zb))
    G["boolean"](u, cut)
    nadd(u, M_GALV, 0)
    for sx in (-1, 1):
        nadd(cyl(f"uleg{zb}{sx}", 5, POLE_Y - 30, (sx * 35.15, (POLE_Y + 30) / 2, zb), "Y", 24), M_GALV)
        nadd(G["hexagon"](f"unut{zb}{sx}", 17, 8, (sx * 35.15, 36, zb), "Y"), M_GALV, 0.5)
pole_top = 450
nadd(cyl("pole", 30.15, pole_top - GROUND, (0, POLE_Y, (pole_top + GROUND) / 2), "Z", 64), M_GALV)
nadd(cyl("pole_cap", 32, 6, (0, POLE_Y, pole_top + 3), "Z", 64), M_RUBBER, 1.5)
nadd(cyl("pole_footing", 140, 60, (0, POLE_Y, GROUND + 30), "Z", 64), M_CONCRETE, 6)
# kabel 24 VDC dari gland turun mengikuti tiang ke conduit di tanah
cu = bpy.data.curves.new("cable_pole", "CURVE")
cu.dimensions = "3D"
cu.bevel_depth = 4 * MM
cu.bevel_resolution = 6
sp = cu.splines.new("BEZIER")
pts = [(-85, 20, 47), (-115, 30, 20), (-40, POLE_Y - 20, -60), (-36, POLE_Y, -200), (-36, POLE_Y, GROUND + 70)]
sp.bezier_points.add(len(pts) - 1)
for bp, p in zip(sp.bezier_points, pts):
    bp.co = Vector(p) * MM
    bp.handle_left_type = bp.handle_right_type = "AUTO"
cab = new_obj("cable_pole", cu)
cab.data.materials.append(M_CABLE)
node_objs.append(cab)
for k, z in enumerate((-160, -300, -420)):  # klem kabel
    nadd(torus(f"cable_clamp{k}", 33, 2.2, (0, POLE_Y, z), "Z"), M_STEEL)

col = bpy.data.collections.new("GLD_node")
scene.collection.children.link(col)
for o in node_objs:
    for c in list(o.users_collection):
        c.objects.unlink(o)
    col.objects.link(o)

# Urutan sistem: GLD -> Cluster Head / Routing Node (STAR 920 MHz) -> mesh antar-CH (921 MHz) -> gateway & server.
GLDS = {"main": (0, 0, 0), "g2": (-3600, 1800, 25), "g3": (3300, 2600, -20), "g4": (-6800, 5600, 15),
        "g5": (6400, 6800, -30), "g6": (-1200, 7600, 10)}
for name, (x, y, rot) in GLDS.items():
    if name == "main":
        continue
    inst = bpy.data.objects.new(f"gld_{name}", None)
    inst.instance_type = "COLLECTION"
    inst.instance_collection = col
    inst.location = Vector((x, y, 0)) * MM
    inst.rotation_euler = (0, 0, math.radians(rot))
    scene.collection.objects.link(inst)


def gld_tip(name):  # ujung antena GLD (rotasi instance diperhitungkan)
    x, y, rot = GLDS[name]
    v = Vector((-28, 20, 255))
    v.rotate(__import__("mathutils").Euler((0, 0, math.radians(rot))))
    return Vector((x, y, 0)) + v


# ---- Cluster Head v3: casing aluminium silinder polos (perkiraan dari foto: diameter 90 x 110 mm),
#      konektor N-type (antena fiberglass MESH) + SMA (antena karet STAR) di tutup atas, gland M12 di bawah,
#      di puncak tiang teleskopik 6 m (OD 33,4 mm), 2 panel surya 6 W miring di +-1,5 m, pelat dasar 240x240.
M_ALU_CASE = add_bump(principled("ch_case_alu", (0.80, 0.80, 0.82), 1, 0.3, **{"Anisotropic": 0.6}),
                      "noise", 3000, 0.05, stretch=(1, 1, 60))
M_FIBER = add_bump(principled("fiberglass_antenna", (0.82, 0.83, 0.80), 0, 0.45), "noise", 600, 0.08)
M_SOLAR = add_bump(principled("solar_cells", (0.01, 0.02, 0.06), 0.2, 0.15, **{"Coat Weight": 1.0}),
                   "weave", 90, 0.15, distance=0.0006)
M_SOLAR_FRAME = principled("solar_frame", (0.75, 0.76, 0.78), 1, 0.3)
CH_POLE_H = 6000
ch_col = bpy.data.collections.new("CH_node")
scene.collection.children.link(ch_col)


def chadd(obj, mat, bevel=0.0):
    obj.data.materials.clear()
    obj.data.materials.append(mat)
    finish(obj, bevel)
    for c in list(obj.users_collection):
        c.objects.unlink(obj)
    ch_col.objects.link(obj)
    return obj


base_z = GROUND
chadd(box("ch_baseplate", (240, 240, 10), (0, 0, base_z + 5)), M_GALV, 1.5)
for sx in (-1, 1):
    for sy in (-1, 1):
        chadd(G["hexagon"](f"ch_anchor{sx}{sy}", 19, 10, (sx * 100, sy * 100, base_z + 15), "Z"), M_GALV, 0.5)
for k, (r, z0, z1) in enumerate(((19.5, 0, 2000), (18.2, 1950, 4000), (16.7, 3950, CH_POLE_H))):  # teleskopik
    chadd(cyl(f"ch_pole{k}", r, z1 - z0, (0, 0, base_z + (z0 + z1) / 2), "Z", 48), M_GALV)
    if k:
        chadd(cyl(f"ch_pole_collar{k}", r + 4, 40, (0, 0, base_z + z0 + 20), "Z", 48), M_GALV, 1.0)
top = base_z + CH_POLE_H
chadd(cyl("ch_mount", 22, 30, (0, 0, top + 15), "Z", 48), M_GALV, 1.0)
chadd(cyl("ch_case", 45, 110, (0, 0, top + 30 + 55), "Z", 96), M_ALU_CASE, 1.5)
chadd(cyl("ch_lid", 47, 6, (0, 0, top + 30 + 113), "Z", 96), M_ALU_CASE, 1.0)
chadd(cyl("ch_bottom", 47, 6, (0, 0, top + 30 + 3), "Z", 96), M_ALU_CASE, 1.0)
lid = top + 30 + 116
chadd(box("ch_ntype_flange", (25, 25, 3), (14, 0, lid + 1.5)), M_NICKEL, 0.5)
chadd(cyl("ch_ntype", 8, 18, (14, 0, lid + 12), "Z", 32), M_NICKEL, 0.5)
chadd(cyl("ch_fiber", 11, 1100, (14, 0, lid + 21 + 550), "Z", 32, r2=9), M_FIBER, 3.0)
chadd(cyl("ch_fiber_base", 14, 60, (14, 0, lid + 51), "Z", 32), M_NICKEL, 1.5)
chadd(box("ch_sma_flange", (12, 12, 2), (-22, 0, lid + 1)), G["M_GOLD"], 0.3)
chadd(cyl("ch_sma_ant", 5, 190, (-22, 0, lid + 2 + 95), "Z", 32, r2=4), M_RUBBER, 1.5)
chadd(cyl("ch_gland", 8, 14, (0, -20, top + 26), "Z", 32), G["M_NYLON"], 1.0)
# 2 panel surya 6 W (masing-masing +-350 x 250 mm) di lengan silang, miring 30 derajat menghadap -Y
arm_z = base_z + 1500
chadd(box("ch_solar_arm", (820, 30, 30), (0, -60, arm_z)), M_GALV, 2.0)
chadd(box("ch_solar_clamp", (60, 60, 80), (0, -10, arm_z)), M_GALV, 2.0)
for sx in (-1, 1):
    for name, size, mat, dy in (("frame", (350, 250, 22), M_SOLAR_FRAME, 0), ("cells", (336, 236, 2), M_SOLAR, -12)):
        o = box(f"ch_solar_{name}{sx}", size, (0, 0, 0))
        o.rotation_euler = (math.radians(90 - 30), 0, 0)
        G["apply_tf"](o)
        o.location = Vector((sx * 205, -150 + dy * 0.5, arm_z + 90 + dy * 0.86)) * MM
        G["apply_tf"](o)
        chadd(o, mat, 1.0 if name == "frame" else 0)
# kabel surya naik mengikuti tiang ke gland CH
cu = bpy.data.curves.new("ch_solar_cable", "CURVE")
cu.dimensions = "3D"
cu.bevel_depth = 3 * MM
cu.bevel_resolution = 4
spl = cu.splines.new("BEZIER")
pts = [(0, -120, arm_z + 60), (0, -40, arm_z + 120), (0, -24, arm_z + 400), (0, -24, top - 200), (0, -20, top + 19)]
spl.bezier_points.add(len(pts) - 1)
for bp, pv in zip(spl.bezier_points, pts):
    bp.co = Vector(pv) * MM
    bp.handle_left_type = bp.handle_right_type = "AUTO"
co = new_obj("ch_solar_cable", cu)
co.data.materials.append(M_CABLE)
for c in list(co.users_collection):
    c.objects.unlink(co)
ch_col.objects.link(co)

CHS = {"ch1": (-2400, 4400), "ch2": (3600, 5600), "ch3": (500, 11000)}
for name, (x, y) in CHS.items():
    inst = bpy.data.objects.new(name, None)
    inst.instance_type = "COLLECTION"
    inst.instance_collection = ch_col
    inst.location = Vector((x, y, 0)) * MM
    scene.collection.objects.link(inst)
ch_col.hide_render = False
bpy.context.view_layer.layer_collection.children["CH_node"].exclude = True  # hanya lewat instance


def ch_star_tip(name):
    x, y = CHS[name]
    return Vector((x - 22, y, lid + 190))


def ch_mesh_tip(name):
    x, y = CHS[name]
    return Vector((x + 14, y, lid + 700))


# ---- Gateway & server: ruang kontrol (jendela menyala) + mast antena 6 m di atap (gateway di dalam, dekat server)
GW = (4800, 15500)
gx, gy = GW
M_BUILDING = add_bump(principled("building", (0.10, 0.10, 0.11), 0, 0.7), "noise", 50, 0.2, distance=0.002)
M_WINDOW = principled("window_lit", (1, 0.85, 0.6), 0, 0.2,
                      **{"Emission Color": (1, 0.82, 0.55, 1), "Emission Strength": 2.2})
box("gw_building", (5000, 3500, 3200), (gx, gy, GROUND + 1600)).data.materials.append(M_BUILDING)
box("gw_roof", (5300, 3800, 200), (gx, gy, GROUND + 3300)).data.materials.append(M_BUILDING)
for k in range(3):
    box(f"gw_window{k}", (900, 20, 700), (gx - 1500 + k * 1500, gy - 1760, GROUND + 1800)).data.materials.append(M_WINDOW)
box("gw_door", (1000, 20, 2100), (gx + 1900, gy - 1760, GROUND + 1050)).data.materials.append(M_RACK)
cyl("gw_mast", 30, 6000, (gx - 1800, gy, GROUND + 3400 + 3000), "Z", 32).data.materials.append(M_GALV)
cyl("gw_fiber", 11, 1100, (gx - 1800, gy, GROUND + 9400 + 550), "Z", 32, r2=9).data.materials.append(M_FIBER)
GW_TIP = Vector((gx - 1800, gy, GROUND + 9400 + 500))
for name, (x, y) in CHS.items():  # cahaya lembut ke casing CH agar terbaca di malam hari
    ld = bpy.data.lights.new(f"{name}_key", "AREA")
    ld.size = 0.4
    ld.energy = 25
    ld.color = (1.0, 0.92, 0.85)
    lo = bpy.data.objects.new(f"{name}_key", ld)
    lo.location = Vector((x - 700, y - 900, top + 400)) * MM
    lo.rotation_euler = (Vector((x, y, top + 90)) - Vector((x - 700, y - 900, top + 400))).to_track_quat("-Z", "Y").to_euler()
    lo.visible_camera = False
    scene.collection.objects.link(lo)

# ------------------------------------------------------------------ lingkungan kilang (siluet gelap)
box("ground", (60000, 60000, 20), (0, 15000, GROUND - 10)).data.materials.append(M_CONCRETE)
for i in range(9):  # pipe rack di belakang area node: portal baja + pipa memanjang
    yy = 16000 + i * 2200
    for sx in (-1, 1):
        box(f"rack_col{i}{sx}", (250, 250, 5200), (sx * 9000, yy, GROUND + 2600)).data.materials.append(M_RACK)
    box(f"rack_beam{i}", (18500, 250, 300), (0, yy, GROUND + 5100)).data.materials.append(M_RACK)
    box(f"rack_beam_lo{i}", (18500, 250, 300), (0, yy, GROUND + 3300)).data.materials.append(M_RACK)
for k in range(7):
    r = random.choice((80, 110, 160, 220))
    for z in (GROUND + 3300 + 150 + r, GROUND + 5100 + 150 + r):
        cyl(f"rack_pipe{k}{z}", r, 19000, (-7500 + k * 2400, 24800, z), "Y", 32).data.materials.append(M_PIPE)
for k, (x, y, r, h) in enumerate(((-16000, 40000, 1600, 30000), (-7000, 46000, 1200, 38000), (5000, 42000, 2000, 26000),
                                  (14000, 48000, 1400, 34000), (24000, 38000, 900, 22000))):
    cyl(f"column{k}", r, h, (x, y, GROUND + h / 2), "Z", 48).data.materials.append(M_COLUMN)
    for j in range(4):  # lampu platform kolom
        cyl(f"column_lamp{k}{j}", 120, 120, (x + r * 0.7, y - r * 0.7, GROUND + h * (0.3 + j * 0.18)), "Z", 16
            ).data.materials.append(M_LAMP)
for k in range(10):  # lampu jalan hangat di pipe rack
    lx, ly = random.uniform(-9000, 9000), random.uniform(16000, 33000)
    cyl(f"rack_lamp{k}", 90, 60, (lx, ly, GROUND + 3000), "Z", 16).data.materials.append(M_LAMP)
    ld = bpy.data.lights.new(f"rack_lamp_light{k}", "POINT")
    ld.energy = 900
    ld.color = (1, 0.65, 0.35)
    ld.shadow_soft_size = 0.3
    lo = bpy.data.objects.new(f"rack_lamp_light{k}", ld)
    lo.location = Vector((lx, ly, GROUND + 2900)) * MM
    scene.collection.objects.link(lo)

world = scene.world
bg = world.node_tree.nodes["Background"]
sky = world.node_tree.nodes.new("ShaderNodeTexGradient")
mapn = world.node_tree.nodes.new("ShaderNodeMapping")
coord = world.node_tree.nodes.new("ShaderNodeTexCoord")
ramp = world.node_tree.nodes.new("ShaderNodeValToRGB")
ramp.color_ramp.elements[0].color = (0.004, 0.006, 0.012, 1)
ramp.color_ramp.elements[1].color = (0.02, 0.04, 0.09, 1)
mapn.inputs["Rotation"].default_value = (0, math.radians(-90), 0)
world.node_tree.links.new(coord.outputs["Generated"], mapn.inputs["Vector"])
world.node_tree.links.new(mapn.outputs["Vector"], sky.inputs["Vector"])
world.node_tree.links.new(sky.outputs["Fac"], ramp.inputs["Fac"])
world.node_tree.links.new(ramp.outputs["Color"], bg.inputs["Color"])
bg.inputs["Strength"].default_value = 1.0

# cahaya: bulan dingin + key hangat lembut ke GLD utama + rim biru
for name, kind, loc, energy, color, size in (("moon", "SUN", (-3000, -2000, 6000), 0.25, (0.6, 0.7, 1.0), 2),
                                             ("key_gld", "AREA", (-900, -1000, 700), 40, (1.0, 0.9, 0.8), 600),
                                             ("rim_gld", "AREA", (700, 900, 600), 25, (0.4, 0.6, 1.0), 400)):
    ld = bpy.data.lights.new(name, kind)
    ld.energy = energy
    ld.color = color
    if kind == "AREA":
        ld.size = size * MM
    else:
        ld.angle = math.radians(size)
    lo = bpy.data.objects.new(name, ld)
    scene.collection.objects.link(lo)
    lo.location = Vector(loc) * MM
    lo.rotation_euler = (Vector((0, 0, 0)) - Vector(loc)).to_track_quat("-Z", "Y").to_euler()
    lo.visible_camera = False

# ------------------------------------------------------------------ tautan: STAR (GLD -> CH) & MESH (CH -> gateway)
M_STAR = principled("star_link", (1.0, 0.65, 0.15), 0, 0.3,
                    **{"Emission Color": (0.96, 0.65, 0.14, 1), "Emission Strength": 2.5})  # #F5A524
LINKS = [("star", gld_tip("main"), ch_star_tip("ch1")), ("star", gld_tip("g2"), ch_star_tip("ch1")),
         ("star", gld_tip("g4"), ch_star_tip("ch1")), ("star", gld_tip("g3"), ch_star_tip("ch2")),
         ("star", gld_tip("g5"), ch_star_tip("ch2")), ("star", gld_tip("g6"), ch_star_tip("ch3")),
         ("mesh", ch_mesh_tip("ch1"), ch_mesh_tip("ch2")), ("mesh", ch_mesh_tip("ch1"), ch_mesh_tip("ch3")),
         ("mesh", ch_mesh_tip("ch2"), ch_mesh_tip("ch3")), ("mesh", ch_mesh_tip("ch3"), GW_TIP),
         ("mesh", ch_mesh_tip("ch2"), GW_TIP)]
LINK_OBJS = []
for i, (kind, pa, pb) in enumerate(LINKS):
    mid = (pa + pb) / 2 + Vector((0, 0, 250 + (pa - pb).length * 0.04))
    cu = bpy.data.curves.new(f"link{i}", "CURVE")
    cu.dimensions = "3D"
    cu.bevel_depth = (4 if kind == "mesh" else 2.2) * MM
    cu.bevel_resolution = 4
    cu.bevel_factor_mapping_end = "SPLINE"
    sp = cu.splines.new("BEZIER")
    sp.bezier_points.add(2)
    for bp, pv in zip(sp.bezier_points, (pa, mid, pb)):
        bp.co = pv * MM
        bp.handle_left_type = bp.handle_right_type = "AUTO"
    lo = new_obj(f"link{i}", cu)
    lo.data.materials.append(M_LINK if kind == "mesh" else M_STAR)
    lo["kind"] = kind
    LINK_OBJS.append(lo)

PULSES = []
for i, lo in enumerate(LINK_OBJS):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=(30 if lo["kind"] == "mesh" else 22) * MM, segments=16, ring_count=8)
    sph = bpy.context.active_object
    sph.name = f"pulse{i}"
    sph.data.materials.append(M_PULSE)
    c = sph.constraints.new("FOLLOW_PATH")
    c.target = lo
    c.use_fixed_location = True
    lo.data.use_path = True
    PULSES.append((sph, c))


def animate_links(fps=30):
    n_star = sum(1 for lo in LINK_OBJS if lo["kind"] == "star")
    start = {}
    for i, lo in enumerate(LINK_OBJS):
        t0 = 4.5 + i * 0.35 if lo["kind"] == "star" else 7.4 + (i - n_star) * 0.45
        start[i] = t0
        for t, v in ((0, 0), (t0, 0), (t0 + 1.2, 1)):
            lo.data.bevel_factor_end = v
            lo.data.keyframe_insert("bevel_factor_end", frame=int(t * fps) + 1)
    for i, (s, c) in enumerate(PULSES):  # denyut berjalan ke arah gateway setelah tautan terbentuk
        t0 = start[i] + 1.2
        s.scale = (0, 0, 0)
        s.keyframe_insert("scale", frame=1)
        s.keyframe_insert("scale", frame=int(t0 * fps))
        s.scale = (1, 1, 1)
        s.keyframe_insert("scale", frame=int(t0 * fps) + 3)
        for k in range(4):
            fs = int((t0 + k * 1.6) * fps)
            c.offset_factor = 0.0
            c.keyframe_insert("offset_factor", frame=fs)
            c.offset_factor = 1.0
            c.keyframe_insert("offset_factor", frame=fs + int(1.5 * fps))
        if s.animation_data:
            for fc in s.animation_data.action.fcurves:
                for kp in fc.keyframe_points:
                    kp.interpolation = "LINEAR"


# ------------------------------------------------------------------ kamera
cam = bpy.data.objects["cam"]
cam_d = cam.data
cam_d.dof.use_dof = True
cam_d.dof.aperture_fstop = 2.8
TGT = bpy.data.objects.new("cam_target", None)
scene.collection.objects.link(TGT)
cam.constraints.clear()
tt = cam.constraints.new("TRACK_TO")
tt.target = TGT
tt.track_axis = "TRACK_NEGATIVE_Z"
tt.up_axis = "UP_Y"
cam_d.dof.focus_object = TGT
cam_d.clip_end = 200

if ORIENT == "portrait":
    scene.render.resolution_x, scene.render.resolution_y = 1080, 1920
    KEYS = [(0, (-380, -1050, 120), (0, 0, 40), 40), (4.5, (-1000, -2700, 700), (-600, 1500, 900), 28),
            (8.5, (-2950, 3550, 5800), (-2400, 4400, 5720), 40), (14, (-3200, -9500, 4200), (300, 6500, 2600), 18)]
else:
    scene.render.resolution_x, scene.render.resolution_y = 1920, 1080
    KEYS = [(0, (-420, -880, 140), (0, 0, 40), 55), (4.5, (-1100, -2600, 700), (-600, 1500, 900), 36),
            (8.5, (-3050, 3500, 5800), (-2400, 4400, 5720), 50), (14, (-3200, -9800, 3900), (400, 6800, 2300), 24)]


def animate_camera(fps=30, seconds=14):
    scene.render.fps = fps
    scene.frame_start, scene.frame_end = 1, fps * seconds
    for t, loc, tgt, lens in KEYS:
        f = int(t * fps) + 1
        cam.location = Vector(loc) * MM
        TGT.location = Vector(tgt) * MM
        cam_d.lens = lens
        cam.keyframe_insert("location", frame=f)
        TGT.keyframe_insert("location", frame=f)
        cam_d.keyframe_insert("lens", frame=f)
    cam_d.dof.aperture_fstop = 2.8
    cam_d.dof.keyframe_insert("aperture_fstop", frame=1)
    cam_d.dof.aperture_fstop = 11
    cam_d.dof.keyframe_insert("aperture_fstop", frame=int(7 * fps))


# ------------------------------------------------------------------ alarm: lensa beacon berkedip merah
def animate_alarm(fps=30, seconds=4):
    scene.render.fps = fps
    scene.frame_start, scene.frame_end = 1, fps * seconds
    led = M_LED.node_tree.nodes["Principled BSDF"].inputs["Emission Strength"]
    pl = bpy.data.lights.new("alarm_light", "POINT")
    pl.color = (1, 0.1, 0.05)
    pl.shadow_soft_size = 0.01
    plo = bpy.data.objects.new("alarm_light", pl)
    beacon_top = Vector((109, 20, 82 + 12)) * MM  # di dalam kubah lensa (koordinat GLD utama)
    plo.location = beacon_top
    scene.collection.objects.link(plo)
    for k in range(int(seconds * 2.5)):  # 2,5 Hz
        f0 = int(k * fps / 2.5) + 1
        for df, v, e in ((0, 0, 0), (2, 60, 30), (int(fps / 5), 60, 30), (int(fps / 5) + 2, 0, 0)):
            led.default_value = v
            led.keyframe_insert("default_value", frame=f0 + df)
            pl.energy = e
            pl.keyframe_insert("energy", frame=f0 + df)
    if ORIENT == "portrait":
        cam.location = Vector((260, -420, 210)) * MM
        TGT.location = Vector((70, 0, 60)) * MM
        cam_d.lens = 45
    else:
        cam.location = Vector((330, -380, 200)) * MM
        TGT.location = Vector((60, 0, 55)) * MM
        cam_d.lens = 60
    for f, x in ((1, 330 if ORIENT != "portrait" else 260), (fps * seconds, 280 if ORIENT != "portrait" else 220)):
        cam.location.x = x * MM
        cam.keyframe_insert("location", frame=f)
    cam_d.dof.aperture_fstop = 2.8


# ------------------------------------------------------------------ render (EEVEE)
for eng in ("BLENDER_EEVEE_NEXT", "BLENDER_EEVEE"):
    try:
        scene.render.engine = eng
        break
    except TypeError:
        continue
ee = scene.eevee
for attr, val in (("shadow_pool_size", "1024"), ("taa_render_samples", 32), ("use_raytracing", True), ("use_shadows", True),
                  ("shadow_ray_count", 2), ("shadow_step_count", 8), ("use_gtao", True)):
    if hasattr(ee, attr):
        setattr(ee, attr, val)
if hasattr(ee, "ray_tracing_options"):
    ee.ray_tracing_options.resolution_scale = "2"
scene.use_nodes = True
nt = scene.node_tree
rl = nt.nodes.get("Render Layers") or nt.nodes.new("CompositorNodeRLayers")
comp = nt.nodes.get("Composite") or nt.nodes.new("CompositorNodeComposite")
glare = nt.nodes.new("CompositorNodeGlare")
glare.glare_type = "FOG_GLOW"
glare.quality = "HIGH"
glare.threshold = 1.0
glare.size = 8
nt.links.new(rl.outputs["Image"], glare.inputs["Image"])
nt.links.new(glare.outputs["Image"], comp.inputs["Image"])


def ffmpeg(path):
    scene.render.image_settings.file_format = "FFMPEG"
    scene.render.ffmpeg.format = "MPEG4"
    scene.render.ffmpeg.codec = "H264"
    scene.render.ffmpeg.constant_rate_factor = "HIGH"
    scene.render.filepath = str(path)


tag = "" if ORIENT == "landscape" else "_portrait"
if MODE in ("still", "anim"):
    animate_links()
    animate_camera()
    bpy.ops.wm.save_as_mainfile(filepath=str(HERE / f"outro_{ORIENT}.blend"))
    if MODE == "still":
        for t in (0.5, 6.0, 8.5, 13.5):
            scene.frame_set(int(t * 30) + 1)
            scene.render.filepath = str(OUT / f"outro{tag}_{t:g}s.png")
            bpy.ops.render.render(write_still=True)
    else:
        if "--preview" in ARGS:
            scene.render.resolution_percentage = 50
            scene.eevee.taa_render_samples = 16
        ffmpeg(OUT / f"outro{tag}{'_preview' if '--preview' in ARGS else ''}.mp4")
        bpy.ops.render.render(animation=True)
elif MODE in ("alarm", "alarm_still"):
    animate_alarm()
    bpy.ops.wm.save_as_mainfile(filepath=str(HERE / f"alarm_{ORIENT}.blend"))
    if MODE == "alarm_still":
        for f in (1, 4):
            scene.frame_set(f)
            scene.render.filepath = str(OUT / f"alarm{tag}_f{f}.png")
            bpy.ops.render.render(write_still=True)
    else:
        ffmpeg(OUT / f"alarm{tag}.mp4")
        bpy.ops.render.render(animation=True)
print("SELESAI")
