# Model 3D GLD V2 sesuai desain terdaftar di dossier sertifikasi (GTS, 29 Sep 2026):
# base die-cast BP18-1Z (ADC12, cat bubuk biru), tutup ulir dengan jendela mesh stainless,
# kipas DC, ring pengunci mesh, O-ring, papan sensor 8x MQ, motherboard, antena atas,
# cable gland 24 VDC (kiri), beacon LED/buzzer stainless (kanan), plug hex (bawah).
# Battery case di dossier tidak dimodelkan (unit produksi 7 Okt tidak memakainya).
# Ukuran dalam mm dari gambar BP18-1Z + ukur jangka sorong unit nyata; tanpa tulisan/logo komponen.
#
#   blender -b -P build_gld_model.py -- <out_dir> [assembled|exploded|both|anim|final|frame:<dtk>] [samples] [landscape|portrait]
#   anim = pratinjau Shot 2 (11 dtk, EEVEE, setengah resolusi): putar 0-4 dtk, terurai 4-7 dtk
import math
import random
import sys
from pathlib import Path

import bmesh
import bpy
from mathutils import Vector

MM = 0.001
ARGS = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
OUT = Path(ARGS[0]).resolve() if ARGS else Path(__file__).resolve().parent / "preview"
MODE = ARGS[1] if len(ARGS) > 1 else "both"
OUT.mkdir(parents=True, exist_ok=True)

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
random.seed(7)

# ------------------------------------------------------------------ material


def principled(name, color, metallic=0.0, rough=0.5, **kw):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    b = nt.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*color, 1)
    b.inputs["Metallic"].default_value = metallic
    b.inputs["Roughness"].default_value = rough
    for k, v in kw.items():
        b.inputs[k].default_value = v
    return m


def add_bump(m, kind, scale, strength, distance=0.0005, stretch=None, rough_var=None):
    nt = m.node_tree
    b = nt.nodes["Principled BSDF"]
    coord = nt.nodes.new("ShaderNodeTexCoord")
    src = coord.outputs["Object"]
    if stretch:
        mp = nt.nodes.new("ShaderNodeMapping")
        mp.inputs["Scale"].default_value = stretch
        nt.links.new(src, mp.inputs["Vector"])
        src = mp.outputs["Vector"]
    if kind == "noise":
        t = nt.nodes.new("ShaderNodeTexNoise")
        t.inputs["Scale"].default_value = scale
        t.inputs["Detail"].default_value = 8
        out = t.outputs["Fac"]
    elif kind == "voronoi":
        t = nt.nodes.new("ShaderNodeTexVoronoi")
        t.feature = "DISTANCE_TO_EDGE"
        t.inputs["Scale"].default_value = scale
        out = t.outputs["Distance"]
    else:  # weave: kotak-kotak halus seperti anyaman kawat
        t = nt.nodes.new("ShaderNodeTexChecker")
        t.inputs["Scale"].default_value = scale
        out = t.outputs["Fac"]
    nt.links.new(src, t.inputs["Vector"])
    bump = nt.nodes.new("ShaderNodeBump")
    bump.inputs["Strength"].default_value = strength
    bump.inputs["Distance"].default_value = distance
    nt.links.new(out, bump.inputs["Height"])
    nt.links.new(bump.outputs["Normal"], b.inputs["Normal"])
    if rough_var:
        ramp = nt.nodes.new("ShaderNodeMapRange")
        ramp.inputs["To Min"].default_value = rough_var[0]
        ramp.inputs["To Max"].default_value = rough_var[1]
        nt.links.new(out, ramp.inputs["Value"])
        nt.links.new(ramp.outputs["Result"], b.inputs["Roughness"])
    return m


# Cat bubuk biru (warna unit produksi), tekstur kulit jeruk halus + clearcoat tipis.
M_PAINT = add_bump(principled("powder_coat_blue", (0.020, 0.200, 0.620), 0, 0.38,
                              **{"Coat Weight": 0.25, "Coat Roughness": 0.25}), "noise", 2200, 0.08)
M_ALU = add_bump(principled("machined_aluminium", (0.80, 0.80, 0.82), 1, 0.22,
                            **{"Anisotropic": 0.6}), "noise", 4000, 0.05, stretch=(1, 1, 60))
M_STEEL = add_bump(principled("brushed_stainless", (0.72, 0.72, 0.74), 1, 0.28,
                              **{"Anisotropic": 0.7}), "noise", 3000, 0.06, stretch=(1, 1, 80))
M_STEEL_POL = principled("polished_stainless", (0.80, 0.80, 0.82), 1, 0.12)
M_SINTER = add_bump(principled("sintered_steel_mesh", (0.56, 0.52, 0.47), 0.85, 0.55),
                    "voronoi", 9000, 0.6, distance=0.0003, rough_var=(0.45, 0.7))
M_WIRE = add_bump(principled("wire_mesh", (0.70, 0.70, 0.72), 1, 0.35), "weave", 6000, 0.7, distance=0.0002)
M_RUBBER = add_bump(principled("rubber_black", (0.015, 0.015, 0.015), 0, 0.75), "noise", 1500, 0.15)
M_NYLON = principled("nylon_black", (0.02, 0.02, 0.022), 0, 0.42)
M_CABLE = principled("cable_pvc_black", (0.012, 0.012, 0.013), 0, 0.35)
M_RED_LENS = principled("red_lens", (0.85, 0.02, 0.02), 0, 0.08,
                        **{"Transmission Weight": 0.92, "IOR": 1.49})
M_LED = principled("led_core", (1, 0.15, 0.1), 0, 0.3,
                   **{"Emission Color": (1, 0.08, 0.05, 1), "Emission Strength": 0.0})
M_PCB = add_bump(principled("pcb_soldermask_green", (0.010, 0.18, 0.06), 0, 0.28,
                            **{"Coat Weight": 0.6, "Coat Roughness": 0.08}), "noise", 900, 0.04)
M_GOLD = principled("pad_gold", (0.95, 0.72, 0.35), 1, 0.25)
M_IC = principled("ic_black", (0.025, 0.025, 0.028), 0, 0.45)
M_SHIELD = add_bump(principled("rf_shield", (0.78, 0.78, 0.80), 1, 0.32), "noise", 2500, 0.05)
M_BAKELITE = principled("bakelite", (0.06, 0.035, 0.02), 0, 0.5)
M_RED_PLASTIC = principled("red_plastic", (0.55, 0.02, 0.02), 0, 0.35)
M_TERMINAL = principled("terminal_blue", (0.05, 0.25, 0.75), 0, 0.4)
M_FAN = principled("fan_plastic", (0.02, 0.02, 0.022), 0, 0.5)
M_CERAMIC = principled("smd_cap", (0.45, 0.35, 0.22), 0, 0.5)
M_NICKEL = principled("nickel", (0.75, 0.74, 0.70), 1, 0.2)
M_WIRE_RED = principled("wire_red", (0.55, 0.02, 0.02), 0, 0.35)
M_WIRE_BLK = principled("wire_black", (0.015, 0.015, 0.017), 0, 0.35)

# ------------------------------------------------------------------ geometri dasar (mm)

PARTS = {}  # nama bagian -> list objek (untuk exploded view)


def link(obj, part, mat):
    obj.data.materials.clear()
    obj.data.materials.append(mat)
    PARTS.setdefault(part, []).append(obj)
    return obj


def new_obj(name, mesh):
    obj = bpy.data.objects.new(name, mesh)
    scene.collection.objects.link(obj)
    return obj


def cyl(name, r, depth, loc, axis="Z", verts=128, r2=None):
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, segments=verts, radius1=r * MM,
                          radius2=(r if r2 is None else r2) * MM, depth=depth * MM)
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    obj = new_obj(name, me)
    obj.rotation_euler = {"Z": (0, 0, 0), "Y": (math.pi / 2, 0, 0), "X": (0, math.pi / 2, 0)}[axis]
    obj.location = Vector(loc) * MM
    apply_tf(obj)
    return obj


def box(name, size, loc):
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1)
    bmesh.ops.scale(bm, vec=Vector(size) * MM, verts=bm.verts)
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    obj = new_obj(name, me)
    obj.location = Vector(loc) * MM
    apply_tf(obj)
    return obj


def torus(name, R, r, loc, axis="Y"):
    bpy.ops.mesh.primitive_torus_add(major_radius=R * MM, minor_radius=r * MM, major_segments=128,
                                     minor_segments=24, location=Vector(loc) * MM)
    obj = bpy.context.active_object
    obj.name = name
    obj.rotation_euler = {"Z": (0, 0, 0), "Y": (math.pi / 2, 0, 0), "X": (0, math.pi / 2, 0)}[axis]
    apply_tf(obj)
    return obj


def apply_tf(obj):
    obj.data.transform(obj.matrix_basis)
    obj.matrix_basis.identity()


def boolean(target, cutter, op="DIFFERENCE"):
    mod = target.modifiers.new("b", "BOOLEAN")
    mod.operation = op
    mod.object = cutter
    mod.solver = "EXACT"
    mod.material_mode = "TRANSFER"
    bpy.context.view_layer.objects.active = target
    bpy.ops.object.modifier_apply(modifier=mod.name)
    bpy.data.objects.remove(cutter)
    return target


def finish(obj, bevel=0.0, segs=3, angle=40):
    if bevel:
        m = obj.modifiers.new("bevel", "BEVEL")
        m.width = bevel * MM
        m.segments = segs
        m.limit_method = "ANGLE"
        m.angle_limit = math.radians(angle)
        m.harden_normals = True
    for p in obj.data.polygons:
        p.use_smooth = True
    obj.modifiers.new("ws", "WEIGHTED_NORMAL").keep_sharp = True
    return obj


# ------------------------------------------------------------------ base casing BP18-1Z
# Sumbu: X lebar, Y ke belakang (muka/tutup menghadap -Y), Z ke atas. Bahu body di y=0.


def build_base():
    body = cyl("base_body", 56, 40, (0, 20, 0), "Y")
    boolean(body, box("tb", (100, 40, 40), (0, 20, 47.75)), "UNION")          # pita atas
    boolean(body, cyl("boss_lr", 15, 124, (0, 20, 47), "X"), "UNION")          # boss kiri/kanan (2-M20)
    boolean(body, box("bb", (54, 40, 30), (0, 20, -57)), "UNION")             # boss bawah (M20)
    # telinga pemasangan (pelat belakang tebal 6, 3x Ø8)
    boolean(body, box("ear_t", (24, 6, 26), (0, 37, 73)), "UNION")
    boolean(body, cyl("ear_tr", 12, 6, (0, 37, 84), "Y"), "UNION")
    for s in (-1, 1):
        boolean(body, box(f"ear_b{s}", (28, 6, 22), (s * 46, 37, -42)), "UNION")
        boolean(body, cyl(f"ear_br{s}", 11, 6, (s * 57.5, 37, -42), "Y"), "UNION")
    # lubang
    for name, loc in (("h_t", (0, 37, 84)), ("h_l", (-57.5, 37, -42)), ("h_r", (57.5, 37, -42))):
        boolean(body, cyl(name, 4, 10, loc, "Y", verts=48))
    bore = cyl("bore", 42.6, 40, (0, 14, 0), "Y")
    bore.data.materials.append(M_ALU)
    boolean(body, bore)
    for s in (-1, 1):
        c = cyl(f"entry{s}", 10, 30, (s * 50, 20, 47), "X", verts=64)
        c.data.materials.append(M_ALU)
        boolean(body, c)
    c = cyl("entry_b", 10, 30, (0, 20, -62), "Z", verts=64)
    c.data.materials.append(M_ALU)
    boolean(body, c)
    # lubang antena di muka atas pita (unit produksi: antena di atas, bukan di samping)
    boolean(body, cyl("ant_hole", 3.5, 20, (-28, 20, 64), "Z", verts=48))
    body.data.materials.clear()
    body.data.materials.append(M_PAINT)
    body.data.materials.append(M_ALU)
    for p in body.data.polygons:  # permukaan hasil potong (lubang dalam) = aluminium mesin
        c = p.center / MM
        inside = Vector((c.x, 0, c.z)).length < 43.2 and c.y < 34.5
        p.material_index = 1 if inside else 0
    PARTS.setdefault("base", []).append(finish(body, 1.6, 3, 35))

    # leher berulir M95x1,5 (aluminium dibubut)
    neck = cyl("neck", 46.6, 13, (0, -6.5, 0), "Y")
    boolean(neck, cyl("neck_bore", 42.6, 16, (0, -6.5, 0), "Y"))
    link(finish(neck, 0.4), "base", M_ALU)
    thread = helix_thread("neck_thread", 46.6, 0.75, 1.5, -12.5, -1.5)
    link(thread, "base", M_ALU)
    # boss PCB di dasar bore (4-M4)
    for a in (45, 135, 225, 315):
        x, z = 32 * math.cos(math.radians(a)), 32 * math.sin(math.radians(a))
        link(finish(cyl(f"pcb_boss{a}", 3.5, 6, (x, 31, z), "Y", 32), 0.3), "base", M_ALU)


def helix_thread(name, r, depth, pitch, y0, y1):
    # profil segitiga diputar sepanjang heliks (Screw modifier) -> ulir nyata
    bm = bmesh.new()
    v = [bm.verts.new(Vector((r * MM, 0, (-pitch * 0.42) * MM))),
         bm.verts.new(Vector(((r + depth) * MM, 0, 0))),
         bm.verts.new(Vector((r * MM, 0, (pitch * 0.42) * MM)))]
    bm.edges.new((v[0], v[1]))
    bm.edges.new((v[1], v[2]))
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    obj = new_obj(name, me)
    turns = (y1 - y0) / pitch
    scr = obj.modifiers.new("screw", "SCREW")
    scr.axis = "Z"
    scr.screw_offset = pitch * MM
    scr.iterations = int(turns)
    scr.steps = 96
    scr.render_steps = 96
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.modifier_apply(modifier="screw")
    obj.rotation_euler = (math.pi / 2, 0, 0)
    obj.location = (0, y1 * MM, 0)
    apply_tf(obj)
    for p in obj.data.polygons:
        p.use_smooth = True
    return obj


# ------------------------------------------------------------------ tutup + jendela mesh


def build_cover():
    y_front, y_rim = -52.0, -1.5
    L = y_rim - y_front
    cov = cyl("cover", 55, L, (0, (y_front + y_rim) / 2, 0), "Y")
    boolean(cov, cyl("cov_in", 48.0, L, (0, (y_front + y_rim) / 2 + 6, 0), "Y"))   # rongga + ulir dalam
    boolean(cov, cyl("cov_win", 37, 20, (0, y_front, 0), "Y"))                    # jendela depan
    boolean(cov, cyl("cov_seat", 40.5, 3, (0, y_front + 6.2, 0), "Y"))            # dudukan mesh
    for i in range(8):  # 8 takik kunci di tepi depan
        a = math.radians(22.5 + i * 45)
        t = box(f"notch{i}", (16, 18, 9), (0, 0, 0))
        t.rotation_euler = (0, a, 0)
        t.location = Vector((55 * math.sin(a), y_front + 8, 55 * math.cos(a))) * MM
        apply_tf(t)
        boolean(cov, t)
    boolean(cov, torus("cov_groove", 55.4, 0.9, (0, -20, 0)))                     # alur garis tengah
    link(finish(cov, 1.4, 3, 35), "cover", M_PAINT)
    link(helix_thread("cover_thread", 47.2, -0.7, 1.5, -21, -3), "cover", M_ALU)

    link(finish(cyl("mesh_plate", 40.2, 1.6, (0, y_front + 6.2, 0), "Y"), 0.3), "mesh", M_SINTER)
    gk = cyl("mesh_gasket", 40.4, 1.2, (0, y_front + 7.6, 0), "Y")
    boolean(gk, cyl("mg_in", 35.5, 3, (0, y_front + 7.6, 0), "Y"))
    link(finish(gk, 0.3), "mesh_gasket", M_RUBBER)
    ring = cyl("mesh_lock_ring", 40.0, 2.0, (0, y_front + 9.4, 0), "Y")
    boolean(ring, cyl("mr_in", 34, 4, (0, y_front + 9.4, 0), "Y"))
    for a in (0, 120, 240):  # tab pengunci
        t = box(f"tab{a}", (6, 2, 5), (0, 0, 41.5))
        t.rotation_euler = (0, math.radians(a), 0)
        apply_tf(t)
        t.location = Vector((0, y_front + 9.4, 0)) * MM
        apply_tf(t)
        boolean(ring, t, "UNION")
    link(finish(ring, 0.3), "mesh_lock", M_STEEL)
    build_fan((0, y_front + 16.5, 0))
    oring = torus("cover_oring", 45.5 - 1.35, 1.35, (0, -1.0, 0))
    link(finish(oring), "oring", M_RUBBER)


def build_fan(c):
    cx, cy, cz = c
    fr = box("fan_frame", (40, 10, 40), c)
    boolean(fr, cyl("fan_hole", 19, 14, c, "Y"))
    for sx in (-1, 1):
        for sz in (-1, 1):
            boolean(fr, cyl(f"fan_sc{sx}{sz}", 1.7, 14, (cx + sx * 16, cy, cz + sz * 16), "Y", 24))
    link(finish(fr, 1.2), "fan", M_FAN)
    hub = cyl("fan_hub", 8.5, 8, (cx, cy, cz), "Y")
    link(finish(hub, 0.8), "fan", M_FAN)
    for i in range(7):
        b = box(f"fan_blade{i}", (11, 0.9, 7), (0, 0, 0))
        b.rotation_euler = (0, 0, math.radians(32))
        apply_tf(b)
        b.location = Vector((13.5, 0, 0)) * MM
        apply_tf(b)
        b.rotation_euler = (0, math.radians(i * 360 / 7), 0)
        apply_tf(b)
        b.location = Vector(c) * MM
        apply_tf(b)
        link(finish(b, 0.3), "fan", M_FAN)
    for sx, sz in ((1, 1), (-1, 1), (1, -1), (-1, -1)):  # jari-jari penyangga motor
        s = box("fan_strut", (1.4, 3, 14), (0, 0, 0))
        s.rotation_euler = (0, math.atan2(sx, sz), 0)
        s.location = Vector((cx + sx * 9.5 * 0.707 * 1.4, cy + 3.5, cz + sz * 9.5 * 0.707 * 1.4)) * MM
        apply_tf(s)
        link(s, "fan", M_FAN)


# ------------------------------------------------------------------ elektronik

TERM = {}  # label terminal -> titik masuk kabel (mm)


def mq_sensor(name, loc, red=False):
    x, y, z = loc  # y = permukaan papan; sensor menghadap -Y
    objs = []
    if red:  # varian tutup plastik merah dengan jendela mesh
        body = cyl(name + "_cap", 9.6, 13, (x, y - 6.5, z), "Y")
        boolean(body, cyl(name + "_win", 6, 3, (x, y - 13, z), "Y"))
        objs.append(link(finish(body, 1.0), "sensor_board", M_RED_PLASTIC))
        objs.append(link(cyl(name + "_mesh", 6.2, 0.6, (x, y - 12.2, z), "Y", 48), "sensor_board", M_WIRE))
        objs.append(link(finish(cyl(name + "_base", 10, 1.8, (x, y - 0.9, z), "Y", 64), 0.3), "sensor_board", M_PCB))
    else:  # varian standar: alas bakelit + flens krimp + tutup mesh stainless ganda
        objs.append(link(finish(cyl(name + "_base", 9.5, 4, (x, y - 2, z), "Y", 64), 0.5), "sensor_board", M_BAKELITE))
        objs.append(link(finish(cyl(name + "_crimp", 9.9, 1.0, (x, y - 4.5, z), "Y", 64), 0.3), "sensor_board", M_STEEL))
        objs.append(link(finish(cyl(name + "_capwall", 8.4, 10, (x, y - 10, z), "Y", 64), 0.8), "sensor_board", M_WIRE))
        objs.append(link(finish(cyl(name + "_captop", 8.1, 0.5, (x, y - 15.1, z), "Y", 64), 0.2), "sensor_board", M_WIRE))
    for k in range(6):  # 6 pin pada lingkaran Ø9,5
        a = math.radians(30 + k * 60)
        objs.append(link(cyl(name + f"_pin{k}", 0.5, 6, (x + 4.75 * math.cos(a), y + 3, z + 4.75 * math.sin(a)),
                             "Y", 12), "sensor_board", M_NICKEL))
    return objs


def scatter_smd(board_y, r_max, n, avoid, part, face=-1):
    for i in range(n):
        for _ in range(40):
            a, rr = random.uniform(0, 2 * math.pi), r_max * math.sqrt(random.random())
            x, z = rr * math.cos(a), rr * math.sin(a)
            if all((x - ax) ** 2 + (z - az) ** 2 > ar ** 2 for ax, az, ar in avoid):
                break
        kind = random.random()
        if kind < 0.45:
            sx, sz, h, mat = 1.6, 0.8, 0.5, M_CERAMIC
        elif kind < 0.75:
            sx, sz, h, mat = random.choice([(3, 3, 0.9), (5, 4.4, 1.0), (2.9, 1.6, 1.0)]) + (M_IC,)
        else:
            sx, sz, h, mat = 2.0, 1.25, 0.6, M_IC
        if random.random() < 0.5:
            sx, sz = sz, sx
        link(box(f"{part}_smd{i}", (sx, h, sz), (x, board_y + face * (0.8 + h / 2), z)), part, mat)


def build_electronics():
    # motherboard (belakang): modul prosesor & radio dengan pelindung RF polos (tanpa tulisan)
    yb = 26.0
    mb = cyl("motherboard", 41.5, 1.6, (0, yb, 0), "Y")
    for a in (45, 135, 225, 315):
        boolean(mb, cyl(f"mbh{a}", 1.8, 4, (32 * math.cos(math.radians(a)), yb, 32 * math.sin(math.radians(a))),
                        "Y", 24))
    link(finish(mb, 0.3), "motherboard", M_PCB)
    link(finish(box("mcu_shield", (18, 3.1, 19.5), (-6, yb - 2.35, 6)), 0.3), "motherboard", M_SHIELD)
    link(box("mcu_pcb", (18, 0.8, 25.5), (-6, yb - 1.2, 3.2)), "motherboard", M_PCB)
    link(finish(box("radio_shield", (14, 2.6, 16), (16, yb - 2.1, -8)), 0.3), "motherboard", M_SHIELD)
    link(cyl("ufl", 1.3, 1.2, (20, yb - 4, 2), "Y", 24), "motherboard", M_GOLD)
    link(box("adc", (6.5, 1.1, 4.4), (8, yb - 1.35, 16)), "motherboard", M_IC)
    for i, (x, z) in enumerate(((-24, -10), (-20, -18), (-28, 2))):  # induktor daya
        link(finish(box(f"ind{i}", (6, 3.2, 6), (x, yb - 2.4, z)), 0.5), "motherboard", M_IC)
    for i, (x, z) in enumerate(((-12, -26), (2, -28))):  # kapasitor elektrolit
        link(finish(cyl(f"ecap{i}", 3.2, 5.5, (x, yb - 3.55, z), "Y", 32), 0.4), "motherboard", M_STEEL_POL)
    scatter_smd(yb, 36, 70, [(-6, 3, 15), (16, -8, 11), (-24, -10, 9), (-6, -27, 10), (8, 16, 5)], "motherboard")

    # papan sensor (depan): 8 sensor MQ melingkar + blok terminal di tengah
    ys = 14.0
    sb = cyl("sensor_board", 41.5, 1.6, (0, ys, 0), "Y")
    for a in (45, 135, 225, 315):
        boolean(sb, cyl(f"sbh{a}", 1.8, 4, (32 * math.cos(math.radians(a)), ys, 32 * math.sin(math.radians(a))),
                        "Y", 24))
    link(finish(sb, 0.3), "sensor_board", M_PCB)
    for i in range(8):
        a = math.radians(90 + i * 45)
        mq_sensor(f"mq{i}", (28 * math.cos(a), ys - 0.8, 28 * math.sin(a)), red=i in (2, 6))
    labels = (["A", "B", "FAN5V", "FAN0V", "AL-", "AL+"], ["BAT-", "BAT+", "24V-", "24V+"])
    for row, (z, n) in enumerate(((4.5, 6), (-4.5, 4))):  # blok terminal RS485/FAN/ALARM & BAT/24V
        w = n * 5.0
        for k, lab in enumerate(labels[row]):  # titik masuk kabel: sisi atas (baris 1) / bawah (baris 2)
            TERM[lab] = (-w / 2 + 2.5 + k * 5, ys - 4.8, z + (4.6 if row == 0 else -4.6))
        tb = box(f"terminal{row}", (w, 8, 7.5), (0, ys - 4.8, z))
        for k in range(n):
            boolean(tb, cyl(f"tscrew{row}{k}", 1.4, 4, (-w / 2 + 2.5 + k * 5, ys - 8.8, z), "Y", 24))
        link(finish(tb, 0.4), "sensor_board", M_TERMINAL)
        for k in range(n):
            link(cyl(f"tsc{row}{k}", 1.3, 0.6, (-w / 2 + 2.5 + k * 5, ys - 7.4, z), "Y", 24),
                 "sensor_board", M_NICKEL)
    scatter_smd(ys, 38, 28, [(28 * math.cos(math.radians(90 + i * 45)), 28 * math.sin(math.radians(90 + i * 45)),
                              11.5) for i in range(8)] + [(0, 0, 15)], "sensor_board")


# ------------------------------------------------------------------ periferal


def hexagon(name, af, length, loc, axis):
    return cyl(name, af / math.sqrt(3), length, loc, axis, verts=6)


def build_antenna():
    x, y, top = -28, 20, 67.5
    link(finish(hexagon("ant_nut", 8, 2.5, (x, y, top + 1.25), "Z"), 0.3), "antenna", M_NICKEL)
    link(finish(cyl("ant_washer", 5.5, 0.8, (x, y, top + 0.4), "Z", 48), 0.1), "antenna", M_RUBBER)
    link(finish(cyl("ant_sma", 3.2, 6, (x, y, top + 5.5), "Z", 48), 0.3), "antenna", M_NICKEL)
    link(finish(cyl("ant_base", 5.2, 14, (x, y, top + 15.5), "Z", 64), 1.0), "antenna", M_RUBBER)
    knuckle = cyl("ant_knuckle", 5.0, 6, (x, y, top + 25.5), "X", 64)
    link(finish(knuckle, 1.5), "antenna", M_RUBBER)
    link(finish(cyl("ant_whip", 4.6, 160, (x, y, top + 108.5), "Z", 64, r2=3.6), 1.4), "antenna", M_RUBBER)


def build_gland_left():
    x0 = -62
    link(finish(cyl("gl_gasket", 12.5, 1.5, (x0 - 0.75, 20, 47), "X", 64), 0.3), "gland", M_RUBBER)
    link(finish(hexagon("gl_hex", 24, 8, (x0 - 5.5, 20, 47), "X"), 0.6), "gland", M_NYLON)
    dome = cyl("gl_dome", 11.5, 13, (x0 - 16, 20, 47), "X", 64, r2=None)
    link(finish(dome, 2.5), "gland", M_NYLON)
    for k in range(12):  # rusuk cengkeram dome
        a = k * math.pi / 6
        link(box(f"gl_rib{k}", (11, 1.2, 1.2), (x0 - 16, 20 + 11.6 * math.sin(a), 47 + 11.6 * math.cos(a))),
             "gland", M_NYLON)
    link(finish(cyl("gl_seal", 6.0, 2, (x0 - 23, 20, 47), "X", 48), 0.4), "gland", M_RUBBER)


def build_beacon_right():
    x0 = 62
    link(finish(cyl("bc_gasket", 12.5, 1.5, (x0 + 0.75, 20, 47), "X", 64), 0.3), "beacon", M_RUBBER)
    link(finish(hexagon("bc_hex", 24, 8, (x0 + 5.5, 20, 47), "X"), 0.5), "beacon", M_STEEL)
    link(finish(cyl("bc_nipple", 8, 16, (x0 + 16, 20, 47), "X", 64), 0.4), "beacon", M_STEEL)
    link(finish(hexagon("bc_hex2", 22, 6, (x0 + 22, 20, 47), "X"), 0.5), "beacon", M_STEEL)
    cx, z0, h = x0 + 47, 0, 82
    body = cyl("bc_body", 21.5, h, (cx, 20, z0 + h / 2), "Z")
    link(finish(body, 1.2), "beacon", M_STEEL)
    for k in range(3):  # garis bubut dekorasi
        link(torus(f"bc_line{k}", 21.55, 0.25, (cx, 20, z0 + h - 6 - k * 2.2), "Z"), "beacon", M_STEEL_POL)
    # kisi buzzer di ujung bawah
    gr = cyl("bc_grille", 19, 1.5, (cx, 20, z0 - 0.2), "Z")
    for k in range(-6, 7):
        boolean(gr, box(f"slot{k}", (30, 1.4, 4), (cx, 20 + k * 2.6, z0 - 0.2)))
    link(finish(gr, 0.2), "beacon", M_STEEL)
    link(cyl("bc_buzzer", 17, 0.5, (cx, 20, z0 + 1.2), "Z"), "beacon", M_IC)
    # kubah lensa merah bertekstur rusuk + inti LED
    link(finish(cyl("bc_lens_ring", 20.5, 4, (cx, 20, z0 + h + 2), "Z"), 0.6), "beacon", M_RED_LENS)
    bpy.ops.mesh.primitive_uv_sphere_add(segments=96, ring_count=48, radius=19.5 * MM,
                                         location=Vector((cx, 20, z0 + h + 4)) * MM)
    dome = bpy.context.active_object
    dome.name = "bc_lens_dome"
    dome.scale = (1, 1, 1.25)
    apply_tf(dome)
    boolean(dome, box("cut_dome", (60, 60, 40), (cx, 20, z0 + h + 4 - 20)))
    disp_tex = bpy.data.textures.new("ribs", "WOOD")
    disp_tex.wood_type = "BANDS"
    disp_tex.noise_basis_2 = "SIN"
    disp_tex.noise_scale = 0.12
    d = dome.modifiers.new("ribs", "DISPLACE")
    d.texture = disp_tex
    d.strength = 0.0006
    d.texture_coords = "OBJECT"
    sub = dome.modifiers.new("sub", "SUBSURF")
    sub.levels = sub.render_levels = 1
    dome.modifiers.move(1, 0)
    link(finish(dome), "beacon", M_RED_LENS)
    link(cyl("bc_led", 7, 14, (cx, 20, z0 + h + 9), "Z", 48), "beacon", M_LED)


def build_bottom_plug():
    link(finish(cyl("plug_gasket", 12.5, 1.5, (0, 20, -72.75), "Z", 64), 0.3), "plug", M_RUBBER)
    link(finish(hexagon("plug_hex", 24, 9, (0, 20, -78), "Z"), 0.8), "plug", M_STEEL)
    link(finish(cyl("plug_flange", 13.5, 2, (0, 20, -74.5), "Z", 64), 0.3), "plug", M_STEEL)


# ------------------------------------------------------------------ rakit

build_base()
build_cover()
build_electronics()
build_antenna()
build_gland_left()
build_beacon_right()
build_bottom_plug()

# arah & jarak exploded view (mm): tumpukan internal ditarik ke depan (-Y) sepanjang sumbu tutup
EXPLODE = {
    "motherboard": (0, -55, 0), "sensor_board": (0, -100, 0),
    "oring": (0, -135, 0), "fan": (0, -165, 0), "mesh_lock": (0, -185, 0),
    "mesh_gasket": (0, -200, 0), "mesh": (0, -215, 0), "cover": (0, -255, 0),
    "antenna": (0, 0, 70), "gland": (-45, 0, 0),
    "beacon": (55, 0, 0), "plug": (0, 0, -40), "base": (0, 0, 0),
}
ROOT = bpy.data.objects.new("GLD_V2", None)
scene.collection.objects.link(ROOT)
GROUPS = {}
for part, objs in PARTS.items():
    e = bpy.data.objects.new(f"grp_{part}", None)
    scene.collection.objects.link(e)
    e.parent = ROOT
    e["explode"] = EXPLODE.get(part, (0, 0, 0))
    for o in objs:
        o.parent = e
    GROUPS[part] = e


# ------------------------------------------------------------------ kabel (terhubung ke terminal, ikut meregang saat exploded)


def wire(name, pts, hooks, mat, radius):
    # pts: titik bezier (mm); hooks: nama grup per titik (None = diam di lantai)
    cu = bpy.data.curves.new(name, "CURVE")
    cu.dimensions = "3D"
    cu.bevel_depth = radius * MM
    cu.bevel_resolution = 4
    cu.use_fill_caps = True
    sp = cu.splines.new("BEZIER")
    sp.resolution_u = 24
    sp.bezier_points.add(len(pts) - 1)
    for bp, p in zip(sp.bezier_points, pts):
        bp.co = Vector(p) * MM
        bp.handle_left_type = bp.handle_right_type = "AUTO"
    cu.bevel_factor_mapping_end = "SPLINE"  # faktor = proporsi panjang kabel
    ob = new_obj(name, cu)
    ob.data.materials.append(mat)
    ob.parent = ROOT
    for part in set(h for h in hooks if h):
        m = ob.modifiers.new(f"hook_{part}", "HOOK")
        m.object = GROUPS[part]
        m.vertex_indices_set([3 * i + k for i, h in enumerate(hooks) if h == part for k in range(3)])
    return ob


def build_wiring():
    # kabel 24 VDC: dari lantai (keluar frame) naik ke gland kiri, jaket berakhir di dalam boss
    wire("cable24", [(-1500, 300, -88), (-700, 160, -88), (-320, 70, -88), (-185, 34, -86), (-140, 24, -40),
                     (-110, 20, 30), (-80, 20, 47), (-56, 20, 47)],
         [None, None, None, None, None, "gland", "gland", "gland"], M_CABLE, 4.0)
    # Kabel internal berpangkal di perangkat asalnya: inti 24 VDC keluar dari jaket kabel hitam di dalam gland,
    # kabel LED/buzzer dari beacon, kabel kipas dari kipas. Seluruh titik ikut perangkat asal (hook), dan sebelum
    # exploded kabel "dicabut" dari terminal lalu tertarik keluar lewat lubang entri (bevel_factor_end mengecil),
    # menyisakan ujung pendek -> tidak ada kabel yang meregang menembus casing atau sensor MQ.
    for lab, mat, dz in (("24V+", M_WIRE_RED, 0), ("24V-", M_WIRE_BLK, 1.6)):
        x, y, z = TERM[lab]
        pts = [(-58, 20, 47 - dz), (-44, 20, 46 - dz), (-30, 12, 36 - dz), (-25, 2, 30 - dz), (-22, -8, 26 - dz),
               (x - 4, -8, -13), (x, 6, -12.5), (x, y, z - 2.5), (x, y, z)]
        RETRACT.append((wire(f"core_{lab}", pts, ["gland"] * len(pts), mat, 0.6), pts, 38))
    for lab, mat, dx in (("FAN5V", M_WIRE_RED, 0), ("FAN0V", M_WIRE_BLK, 1.5)):
        x, y, z = TERM[lab]
        pts = [(x, -30.5, 13), (x, -24, 13), (x, -8, 13), (x, 6, 12.5), (x, y, z + 2.5), (x, y, z)]
        RETRACT.append((wire(f"fan_{lab}", pts, ["fan"] * len(pts), mat, 0.5), pts, 30))
    for lab, mat, dz in (("AL+", M_WIRE_RED, 0), ("AL-", M_WIRE_BLK, 1.6)):
        x, y, z = TERM[lab]
        pts = [(92, 20, 47 - dz), (66, 20, 46 - dz), (44, 12, 36 - dz), (26, 2, 30 - dz), (22, -8, 26 - dz),
               (x + 1, -8, 13), (x, 6, 12.5), (x, y, z + 2.5), (x, y, z)]
        RETRACT.append((wire(f"alarm_{lab}", pts, ["beacon"] * len(pts), mat, 0.6), pts, 52))


RETRACT = []  # (objek kabel, titik, panjang ujung yang tersisa setelah dicabut [mm])
build_wiring()


def set_explode(t):
    for part, e in GROUPS.items():
        e.location = Vector(e["explode"]) * MM * t



# urutan terlepas (mulai detik ke-4): bagian luar dulu, lalu tumpukan internal
# Fase 1 (detik 4): tutup & mesh lepas -> detik 4,9-5,6: kabel dicabut dari terminal (terlihat)
# -> fase 2 (detik 5,7): bagian lain terurai.
PHASE1 = ["cover", "mesh", "mesh_gasket", "mesh_lock"]
ORDER = PHASE1 + ["fan", "oring", "antenna", "gland", "beacon", "plug", "sensor_board", "motherboard"]
UNPLUG_AT = 4.9
PHASE2_AT = 5.7


def animate_shot2(fps=30, seconds=11):
    scene.render.fps = fps
    scene.frame_start, scene.frame_end = 1, fps * seconds
    ROOT.rotation_mode = "XYZ"
    for f, deg in ((1, 22), (4 * fps, 2), (fps * seconds, -14)):
        ROOT.rotation_euler = (0, 0, math.radians(deg))
        ROOT.keyframe_insert("rotation_euler", frame=f)
    for e in GROUPS.values():
        e.location = (0, 0, 0)
        e.keyframe_insert("location", frame=1)
    for ob, pts, stub in RETRACT:  # cabut dari terminal, tarik keluar lewat lubang entri
        length = sum((Vector(p1) - Vector(p0)).length for p0, p1 in zip(pts, pts[1:])) * 1.08
        for t, v in ((0, 1.0), (UNPLUG_AT, 1.0), (UNPLUG_AT + 0.15, 0.97), (UNPLUG_AT + 0.7, min(1.0, stub / length))):
            ob.data.bevel_factor_end = v
            ob.data.keyframe_insert("bevel_factor_end", frame=int(t * fps) + 1)
    step = int(0.15 * fps)
    for i, part in enumerate(p for p in ORDER if p in GROUPS):
        e = GROUPS[part]
        k = PHASE1.index(part) if part in PHASE1 else ORDER.index(part) - len(PHASE1)
        f0 = int((4.0 if part in PHASE1 else PHASE2_AT) * fps) + k * step
        e.location = (0, 0, 0)
        e.keyframe_insert("location", frame=f0)
        e.location = Vector(e["explode"]) * MM
        e.keyframe_insert("location", frame=f0 + int(1.2 * fps))
    for ob in [ROOT] + list(GROUPS.values()):
        if ob.animation_data and ob.animation_data.action:
            for fc in ob.animation_data.action.fcurves:
                for kp in fc.keyframe_points:
                    kp.interpolation = "BEZIER"
                    kp.easing = "EASE_IN_OUT"

# ------------------------------------------------------------------ studio & render

world = bpy.data.worlds.new("studio")
world.use_nodes = True
bg = world.node_tree.nodes["Background"]
bg.inputs["Color"].default_value = (0.012, 0.013, 0.016, 1)
bg.inputs["Strength"].default_value = 1.0
scene.world = world

floor = cyl("floor", 30000, 1, (0, 0, -95), "Z")
floor.data.materials.append(add_bump(principled("floor", (0.03, 0.031, 0.035), 0, 0.45), "noise", 300, 0.02))


def area(name, loc, size, power, color, target=(0, 0, 0)):
    ld = bpy.data.lights.new(name, "AREA")
    ld.size = size * MM
    ld.energy = power
    ld.color = color
    lo = bpy.data.objects.new(name, ld)
    scene.collection.objects.link(lo)
    lo.location = Vector(loc) * MM
    d = (Vector(target) - Vector(loc)) * MM
    lo.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()
    lo.visible_camera = False  # panel lampu tidak ikut terlihat di frame


area("key", (-450, -500, 420), 500, 14, (1.0, 0.96, 0.92))
area("fill", (500, -350, 80), 600, 4, (0.85, 0.9, 1.0))
area("rim_blue", (250, 450, 350), 250, 10, (0.35, 0.55, 1.0))
area("rim_warm", (-400, 350, 150), 250, 5, (1.0, 0.75, 0.45))
area("top", (0, -50, 650), 400, 4, (1, 1, 1))

cam_d = bpy.data.cameras.new("cam")
cam_d.lens = 85
cam_d.dof.use_dof = True
cam_d.dof.aperture_fstop = 8
cam = bpy.data.objects.new("cam", cam_d)
scene.collection.objects.link(cam)
scene.camera = cam


def aim(loc, target, focus=None):
    cam.location = Vector(loc) * MM
    d = (Vector(target) - Vector(loc)) * MM
    cam.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()
    cam_d.dof.focus_distance = (focus or d.length / MM) * MM


scene.render.engine = "CYCLES"
prefs = bpy.context.preferences.addons["cycles"].preferences
for dev_type in ("OPTIX", "CUDA"):
    try:
        prefs.compute_device_type = dev_type
        prefs.get_devices()
        if any(d.type == dev_type for d in prefs.devices):
            for d in prefs.devices:
                d.use = d.type == dev_type
            scene.cycles.device = "GPU"
            break
    except TypeError:
        continue
print("Cycles device:", scene.cycles.device, prefs.compute_device_type)
scene.cycles.samples = int(ARGS[2]) if len(ARGS) > 2 else 24  # + OIDN kualitas tinggi; setara 48 sampel tanpa optimasi
scene.cycles.use_denoising = True
# Optimasi waktu render: adaptive sampling, pantulan secukupnya, tanpa caustics, denoiser GPU, data persisten.
scene.cycles.use_adaptive_sampling = True
scene.cycles.adaptive_threshold = 0.05
scene.cycles.adaptive_min_samples = 16
scene.cycles.max_bounces = 8
scene.cycles.diffuse_bounces = 3
scene.cycles.glossy_bounces = 4
scene.cycles.transmission_bounces = 8
scene.cycles.transparent_max_bounces = 8
scene.cycles.volume_bounces = 0
scene.cycles.caustics_reflective = scene.cycles.caustics_refractive = False
scene.cycles.blur_glossy = 1.0
scene.cycles.denoiser = "OPENIMAGEDENOISE"
scene.cycles.denoising_input_passes = "RGB_ALBEDO_NORMAL"
scene.cycles.denoising_prefilter = "ACCURATE"
scene.cycles.denoising_quality = "HIGH"
if hasattr(scene.cycles, "denoising_use_gpu"):
    scene.cycles.denoising_use_gpu = True
scene.render.use_persistent_data = True
scene.render.resolution_x, scene.render.resolution_y = 1920, 1080
scene.view_settings.view_transform = "AgX"
scene.view_settings.look = "AgX - Medium High Contrast"
scene.render.film_transparent = False

bpy.ops.wm.save_as_mainfile(filepath=str(Path(__file__).resolve().parent / "gld_v2.blend"))

if MODE in ("assembled", "both"):
    set_explode(0)
    aim((-470, -800, 300), (15, -10, 45))
    scene.render.filepath = str(OUT / "gld_assembled.png")
    bpy.ops.render.render(write_still=True)
if MODE in ("exploded", "both"):
    set_explode(1)
    aim((-980, -860, 560), (15, -110, 45))
    cam_d.lens = 70
    cam_d.dof.aperture_fstop = 16
    scene.render.filepath = str(OUT / "gld_exploded.png")
    bpy.ops.render.render(write_still=True)
if MODE.startswith("frame"):  # frame:<detik> = satu frame Shot 2 dengan Cycles kualitas penuh
    animate_shot2()
    aim((-1080, -980, 700), (10, -110, 110))
    cam_d.lens = 74
    cam_d.dof.use_dof = False
    scene.frame_set(int(float(MODE.split(":")[1]) * scene.render.fps) + 1)
    scene.render.filepath = str(OUT / f"shot2_cycles_{MODE.split(':')[1]}s.png")
    bpy.ops.render.render(write_still=True)
if MODE == "final":  # render final Shot 2 (Cycles, resolusi penuh) -> <out_dir>/scene03_hero_exploded.mp4
    animate_shot2()
    aim((-1080, -980, 700), (10, -110, 110))
    cam_d.lens = 74
    cam_d.dof.use_dof = False
    if len(ARGS) > 3 and ARGS[3] == "portrait":
        scene.render.resolution_x, scene.render.resolution_y = 1080, 1920
        cam_d.lens = 52
    scene.render.image_settings.file_format = "FFMPEG"
    scene.render.ffmpeg.format = "MPEG4"
    scene.render.ffmpeg.codec = "H264"
    scene.render.ffmpeg.constant_rate_factor = "PERC_LOSSLESS"
    scene.render.filepath = str(OUT / "scene03_hero_exploded.mp4")
    bpy.ops.render.render(animation=True)
if MODE == "anim":
    animate_shot2()
    aim((-1080, -980, 700), (10, -110, 110))
    cam_d.lens = 74
    cam_d.dof.use_dof = False
    for eng in ("BLENDER_EEVEE_NEXT", "BLENDER_EEVEE"):
        try:
            scene.render.engine = eng
            break
        except TypeError:
            continue
    scene.render.resolution_percentage = 50
    scene.render.image_settings.file_format = "FFMPEG"
    scene.render.ffmpeg.format = "MPEG4"
    scene.render.ffmpeg.codec = "H264"
    scene.render.ffmpeg.constant_rate_factor = "HIGH"
    scene.render.filepath = str(OUT / "shot2_preview.mp4")
    bpy.ops.wm.save_as_mainfile(filepath=str(Path(__file__).resolve().parent / "gld_v2.blend"))
    bpy.ops.render.render(animation=True)
print("SELESAI")
