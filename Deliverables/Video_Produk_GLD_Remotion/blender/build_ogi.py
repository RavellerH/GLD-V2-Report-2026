# Video OGI (konsep pengembangan), adegan 6: kamera OGI MWIR pada pan-tilt di tiang +-10 m,
# berpatroli di 3 preset sektor kritis (jalur pipa, manifold, klaster valve). Kerucut pandang biru
# menyapu area; di preset ketiga plume terlihat (ilustrasi) -> kerucut berubah amber (terdeteksi).
# Kamera generik (tanpa merek/logo); bentuk mengikuti housing PTZ industri umum. Satuan meter, EEVEE.
#
#   blender -b -P build_ogi.py -- <out_dir> [still|anim] [landscape|portrait] [--preview] [--final]
import math
import random
import sys
from pathlib import Path

import bmesh
import bpy
from mathutils import Vector

HERE = Path(__file__).resolve().parent
ARGS = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
OUT = Path(ARGS[0]).resolve() if ARGS else HERE / "preview"
MODE = ARGS[1] if len(ARGS) > 1 else "still"
ORIENT = ARGS[2] if len(ARGS) > 2 else "landscape"
OUT.mkdir(parents=True, exist_ok=True)
FPS, SECONDS = 30, 14

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
rnd = random.Random(3)


def principled(name, color, metallic=0.0, rough=0.5, **kw):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*color, 1)
    b.inputs["Metallic"].default_value = metallic
    b.inputs["Roughness"].default_value = rough
    for k, v in kw.items():
        b.inputs[k].default_value = v
    return m


def noise_bump(m, scale, strength, stretch=None):
    nt = m.node_tree
    b = nt.nodes["Principled BSDF"]
    tc = nt.nodes.new("ShaderNodeTexCoord")
    src = tc.outputs["Object"]
    if stretch:
        mp = nt.nodes.new("ShaderNodeMapping")
        mp.inputs["Scale"].default_value = stretch
        nt.links.new(src, mp.inputs["Vector"])
        src = mp.outputs["Vector"]
    t = nt.nodes.new("ShaderNodeTexNoise")
    t.inputs["Scale"].default_value = scale
    t.inputs["Detail"].default_value = 8
    nt.links.new(src, t.inputs["Vector"])
    bu = nt.nodes.new("ShaderNodeBump")
    bu.inputs["Strength"].default_value = strength
    bu.inputs["Distance"].default_value = 0.0005
    nt.links.new(t.outputs["Fac"], bu.inputs["Height"])
    nt.links.new(bu.outputs["Normal"], b.inputs["Normal"])
    return m


def transparent_emit(name, color, strength):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    if hasattr(m, "surface_render_method"):
        m.surface_render_method = "BLENDED"
    else:
        m.blend_method = "BLEND"
    nt = m.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    mix = nt.nodes.new("ShaderNodeMixShader")
    tr = nt.nodes.new("ShaderNodeBsdfTransparent")
    em = nt.nodes.new("ShaderNodeEmission")
    em.name = "emit"
    em.inputs["Color"].default_value = (*color, 1)
    em.inputs["Strength"].default_value = strength
    val = nt.nodes.new("ShaderNodeValue")
    val.name = "alpha"
    val.outputs[0].default_value = 0.15
    nt.links.new(val.outputs[0], mix.inputs["Fac"])
    nt.links.new(tr.outputs[0], mix.inputs[1])
    nt.links.new(em.outputs[0], mix.inputs[2])
    nt.links.new(mix.outputs[0], out.inputs["Surface"])
    return m


M_GALV = noise_bump(principled("galvanized", (0.60, 0.61, 0.62), 1, 0.42), 300, 0.2)
M_SS = noise_bump(principled("stainless_housing", (0.62, 0.63, 0.65), 1, 0.38, **{"Anisotropic": 0.6}), 3000, 0.05,
                  stretch=(60, 1, 1))
M_DARK = principled("ptz_dark", (0.03, 0.032, 0.035), 0.2, 0.45)
M_GLASS = principled("germanium_window", (0.02, 0.02, 0.025), 1, 0.05)  # jendela germanium tampak gelap mengilap
M_CONCRETE = noise_bump(principled("concrete", (0.045, 0.047, 0.052), 0, 0.75), 8, 0.3)
M_PIPE = noise_bump(principled("pipe_painted", (0.42, 0.43, 0.44), 0.6, 0.45), 30, 0.15)
M_PIPE_Y = principled("pipe_yellow", (0.75, 0.55, 0.06), 0.2, 0.45)
M_VALVE = principled("valve_red", (0.55, 0.05, 0.04), 0.3, 0.4)
M_RACK = principled("rack_steel", (0.10, 0.11, 0.12), 0.6, 0.5)
M_COLUMN = principled("column", (0.30, 0.31, 0.33), 0.5, 0.45)
M_TANK = principled("tank_white", (0.70, 0.71, 0.72), 0.2, 0.5)
M_LAMP = principled("lamp", (1, 0.7, 0.35), 0, 0.3, **{"Emission Color": (1, 0.62, 0.3, 1), "Emission Strength": 30})
M_CONE = transparent_emit("view_cone", (0.25, 0.55, 1.0), 2.5)
M_RING = transparent_emit("sector_ring", (0.25, 0.55, 1.0), 6)
M_GAS = transparent_emit("gas", (0.96, 0.62, 0.14), 2.2)


def obj_from_bm(name, bm, mat):
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    o = bpy.data.objects.new(name, me)
    scene.collection.objects.link(o)
    o.data.materials.append(mat)
    for p in o.data.polygons:
        p.use_smooth = True
    return o


def cyl(name, r, h, loc, mat, axis="Z", seg=48, r2=None):
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, segments=seg, radius1=r, radius2=r if r2 is None else r2, depth=h)
    o = obj_from_bm(name, bm, mat)
    o.rotation_euler = {"Z": (0, 0, 0), "Y": (math.pi / 2, 0, 0), "X": (0, math.pi / 2, 0)}[axis]
    o.location = loc
    return o


def box(name, size, loc, mat, bevel=0.0):
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1)
    bmesh.ops.scale(bm, vec=size, verts=bm.verts)
    o = obj_from_bm(name, bm, mat)
    o.location = loc
    if bevel:
        m = o.modifiers.new("bev", "BEVEL")
        m.width = bevel
        m.segments = 3
    return o


# ------------------------------------------------------------------ tiang 10 m + kepala PTZ
POLE_H = 10.0
cyl("pole", 0.084, POLE_H, (0, 0, POLE_H / 2), M_GALV, seg=64)
cyl("pole_base", 0.25, 0.03, (0, 0, 0.015), M_GALV)
cyl("footing", 0.5, 0.3, (0, 0, -0.1), M_CONCRETE)
for k in range(4):
    a = k * math.pi / 2 + math.pi / 4
    cyl(f"anchor{k}", 0.018, 0.08, (0.18 * math.cos(a), 0.18 * math.sin(a), 0.06), M_GALV, seg=6)
cyl("pole_top", 0.12, 0.04, (0, 0, POLE_H + 0.02), M_GALV)
box("junction_box", (0.3, 0.16, 0.4), (0, -0.16, 2.2), M_SS, 0.01)  # kotak sambungan daya/data di tiang
cyl("conduit", 0.02, 7.6, (0, -0.1, 6.1), M_GALV, seg=16)

pan = bpy.data.objects.new("pan", None)
scene.collection.objects.link(pan)
pan.location = (0, 0, POLE_H + 0.04)
tilt = bpy.data.objects.new("tilt", None)
scene.collection.objects.link(tilt)
tilt.parent = pan
tilt.location = (0, 0, 0.36)


def child(o, parent):
    o.parent = parent
    o.matrix_parent_inverse = parent.matrix_world.inverted()
    return o


bpy.context.view_layer.update()
child(cyl("pan_base", 0.11, 0.12, (0, 0, POLE_H + 0.1), M_DARK), pan)
child(cyl("pan_ring", 0.115, 0.015, (0, 0, POLE_H + 0.165), M_SS), pan)
for s in (-1, 1):  # lengan yoke
    child(box(f"yoke{s}", (0.04, 0.12, 0.32), (s * 0.2, 0, POLE_H + 0.32), M_DARK, 0.008), pan)
    child(cyl(f"yoke_hub{s}", 0.055, 0.03, (s * 0.2, 0, POLE_H + 0.4), M_SS, axis="X"), pan)
child(box("yoke_bridge", (0.44, 0.12, 0.04), (0, 0, POLE_H + 0.18), M_DARK, 0.008), pan)
# housing kamera (menghadap +Y), sunshield, jendela germanium, gland belakang
HZ = POLE_H + 0.4
child(box("housing", (0.34, 0.5, 0.22), (0, 0.02, HZ), M_SS, 0.02), tilt)
child(box("sunshield", (0.4, 0.62, 0.012), (0, 0.04, HZ + 0.135), M_SS, 0.004), tilt)
for s in (-1, 1):
    child(box(f"shield_side{s}", (0.012, 0.62, 0.05), (s * 0.2, 0.04, HZ + 0.11), M_SS), tilt)
child(cyl("front_bezel", 0.1, 0.03, (0, 0.285, HZ), M_SS, axis="Y"), tilt)
child(cyl("window", 0.08, 0.012, (0, 0.302, HZ), M_GLASS, axis="Y"), tilt)
child(cyl("rear_cap", 0.1, 0.02, (0, -0.24, HZ), M_DARK, axis="Y"), tilt)
for k, x in enumerate((-0.06, 0.06)):
    child(cyl(f"gland{k}", 0.018, 0.05, (x, -0.27, HZ - 0.04), M_SS, axis="Y", seg=6), tilt)

# kerucut pandang (frustum) dari jendela ke depan
L, HW, HH = 46.0, 7.5, 4.6
bm = bmesh.new()
v0 = [bm.verts.new((sx * 0.05, 0.31, sz * 0.035 + HZ)) for sx, sz in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
v1 = [bm.verts.new((sx * HW, 0.31 + L, sz * HH + HZ)) for sx, sz in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
for i in range(4):
    j = (i + 1) % 4
    bm.faces.new((v0[i], v0[j], v1[j], v1[i]))
cone = obj_from_bm("view_cone", bm, M_CONE)
cone.visible_shadow = False
child(cone, tilt)

# ------------------------------------------------------------------ area proses
cyl("ground", 400, 0.2, (0, 0, -0.1), M_CONCRETE, seg=64)
# pipe rack memanjang melintang di depan kamera
for i in range(10):
    x = -40 + i * 9
    for sy in (24, 30):
        box(f"rack_col{i}_{sy}", (0.3, 0.3, 6), (x, sy, 3), M_RACK)
    box(f"rack_beam{i}", (0.3, 6.3, 0.35), (x, 27, 6), M_RACK)
    box(f"rack_beam_lo{i}", (0.3, 6.3, 0.3), (x, 27, 3.8), M_RACK)
for k, (y, z, r, m) in enumerate(((25, 6.4, 0.25, M_PIPE), (26.2, 6.35, 0.18, M_PIPE_Y), (27.3, 6.45, 0.3, M_PIPE),
                                  (28.6, 6.3, 0.15, M_PIPE), (25.5, 4.15, 0.2, M_PIPE), (27.8, 4.2, 0.28, M_PIPE_Y))):
    cyl(f"rack_pipe{k}", r, 92, (5, y, z), m, axis="X", seg=32)
# manifold + klaster valve (preset 2 & 3)
MANIFOLD = Vector((-2, 40, 0))
for k in range(6):
    y = MANIFOLD.y + k * 1.4
    cyl(f"header_riser{k}", 0.12, 2.2, (MANIFOLD.x - 4, y, 1.1), M_PIPE, seg=24)
    cyl(f"header_valve{k}", 0.2, 0.25, (MANIFOLD.x - 4, y, 1.6), M_VALVE, axis="X", seg=24)
    cyl(f"handwheel{k}", 0.22, 0.03, (MANIFOLD.x - 3.75, y, 1.6), M_VALVE, axis="X", seg=24)
cyl("header", 0.22, 9, (MANIFOLD.x - 4, MANIFOLD.y + 3.5, 2.3), M_PIPE, axis="Y", seg=32)
VALVES = Vector((22, 38, 0))
for k in range(5):
    x = VALVES.x + (k - 2) * 1.6
    cyl(f"vc_pipe{k}", 0.15, 7, (x, VALVES.y, 0.9), M_PIPE, axis="Y", seg=24)
    cyl(f"vc_body{k}", 0.26, 0.6, (x, VALVES.y, 0.9), M_VALVE, axis="Y", seg=24)
    cyl(f"vc_stem{k}", 0.04, 0.8, (x, VALVES.y, 1.5), M_GALV, seg=12)
    cyl(f"vc_wheel{k}", 0.25, 0.03, (x, VALVES.y, 1.9), M_VALVE, seg=24)
    for dy in (-1.2, 1.2):
        cyl(f"vc_flange{k}{dy}", 0.27, 0.06, (x, VALVES.y + dy, 0.9), M_GALV, axis="Y", seg=24)
for k in range(3):
    box(f"vc_support{k}", (8.5, 0.3, 0.5), (VALVES.x, VALVES.y - 3 + k * 3, 0.25), M_CONCRETE)
# latar: kolom distilasi, tangki, lampu
for k, (x, y, r, h) in enumerate(((-30, 75, 2.2, 38), (-12, 85, 1.6, 46), (8, 80, 2.6, 32), (30, 90, 1.8, 42),
                                  (48, 72, 1.2, 28))):
    cyl(f"column{k}", r, h, (x, y, h / 2), M_COLUMN)
    for j in range(4):
        cyl(f"column_lamp{k}{j}", 0.15, 0.15, (x + r * 0.7, y - r * 0.7, h * (0.25 + j * 0.18)), M_LAMP, seg=12)
for k, (x, y) in enumerate(((55, 45), (65, 60), (-55, 50))):
    cyl(f"tank{k}", 9, 12, (x, y, 6), M_TANK)
for k in range(9):
    lx, ly = rnd.uniform(-35, 45), rnd.uniform(22, 32)
    cyl(f"rack_lamp{k}", 0.12, 0.08, (lx, ly, 5.6), M_LAMP, seg=12)
    ld = bpy.data.lights.new(f"rack_light{k}", "POINT")
    ld.energy = 1500
    ld.color = (1, 0.65, 0.35)
    lo = bpy.data.objects.new(f"rack_light{k}", ld)
    lo.location = (lx, ly, 5.4)
    scene.collection.objects.link(lo)

# ------------------------------------------------------------------ preset patroli
# sudut pan (derajat, 0 = lurus +Y) & tilt (negatif = menunduk) per preset
TARGETS = [Vector((-26, 27, 4)), MANIFOLD + Vector((-4, 3.5, 1.5)), VALVES + Vector((0, 0, 1))]


def aim(t):
    d = t - Vector((0, 0, HZ))
    p = -math.degrees(math.atan2(d.x, d.y))
    tl = math.degrees(math.atan2(d.z, math.hypot(d.x, d.y)))
    return p, tl


AIMS = [aim(t) for t in TARGETS]
# (waktu, preset) -> kamera diam (dwell) di tiap preset, bergerak halus di antaranya
SCHEDULE = [(0.0, 0), (3.8, 0), (5.2, 1), (7.4, 1), (8.8, 2), (SECONDS, 2)]
for t, i in SCHEDULE:
    f = int(t * FPS) + 1
    pan.rotation_euler = (0, 0, math.radians(AIMS[i][0]))
    tilt.rotation_euler = (math.radians(AIMS[i][1]), 0, 0)
    pan.keyframe_insert("rotation_euler", frame=f)
    tilt.keyframe_insert("rotation_euler", frame=f)
for o in (pan, tilt):
    for fc in o.animation_data.action.fcurves:
        for kp in fc.keyframe_points:
            kp.interpolation = "BEZIER"
            kp.easing = "EASE_IN_OUT"

# cincin sektor di tanah: menyala saat preset aktif
RINGS = []
for i, t in enumerate(TARGETS):
    bpy.ops.mesh.primitive_torus_add(major_radius=3.2, minor_radius=0.06, major_segments=96, minor_segments=8,
                                     location=(t.x, t.y, 0.05))
    r = bpy.context.active_object
    r.name = f"sector_ring{i}"
    r.data.materials.append(M_RING)
    r.visible_shadow = False
    RINGS.append(r)
for i, (a, b) in enumerate(((0.3, 4.0), (5.3, 7.6), (8.9, SECONDS + 1))):
    r = RINGS[i]
    for t, s in ((0, 0), (a, 0), (a + 0.4, 1), (b, 1), (b + 0.3, 0)):
        r.scale = (s, s, 1)
        r.keyframe_insert("scale", frame=max(1, int(t * FPS) + 1))

# ------------------------------------------------------------------ plume (ilustrasi) di klaster valve
SRC = VALVES + Vector((1.6, 1.2, 0.9))  # flange valve ke-4
for i in range(70):
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=3, radius=1)
    b = bpy.context.active_object
    b.name = f"gas{i}"
    b.data.materials.append(M_GAS)
    b.visible_shadow = False
    for p in b.data.polygons:
        p.use_smooth = True
    t0 = 8.4 + i * 0.07
    life = 3.0 + rnd.uniform(-0.4, 0.5)
    drift = Vector((rnd.uniform(3, 6), rnd.uniform(-1, 2), rnd.uniform(0.6, 2.2)))
    for t, u in ((t0, 0), (t0 + life * 0.3, 0.3), (t0 + life, 1)):
        b.location = SRC + drift * u
        s = 0.3 + 2.6 * u
        b.scale = (s, s * 0.9, s * 0.8)
        b.keyframe_insert("location", frame=int(t * FPS) + 1)
        b.keyframe_insert("scale", frame=int(t * FPS) + 1)
    b.hide_render = True
    b.keyframe_insert("hide_render", frame=1)
    b.hide_render = False
    b.keyframe_insert("hide_render", frame=int(t0 * FPS) + 1)
    if t0 + life < SECONDS:
        b.hide_render = True
        b.keyframe_insert("hide_render", frame=int((t0 + life) * FPS) + 1)
gas_a = M_GAS.node_tree.nodes["alpha"].outputs[0]
for t, v in ((0, 0), (8.4, 0), (9.6, 0.38), (SECONDS, 0.38)):
    gas_a.default_value = v
    gas_a.keyframe_insert("default_value", frame=int(t * FPS) + 1)
# kerucut & cincin preset 3 berubah amber setelah plume terdeteksi konsisten (+-1,4 dtk setelah tiba)
DET = 10.6
for mat in (M_CONE, M_RING):
    em = mat.node_tree.nodes["emit"].inputs["Color"]
    for t, c in ((0, (0.25, 0.55, 1.0, 1)), (DET, (0.25, 0.55, 1.0, 1)), (DET + 0.5, (1.0, 0.6, 0.12, 1)),
                 (SECONDS, (1.0, 0.6, 0.12, 1))):
        em.default_value = c
        em.keyframe_insert("default_value", frame=int(t * FPS) + 1)
cone_a = M_CONE.node_tree.nodes["alpha"].outputs[0]
for t, v in ((0, 0), (1.0, 0), (2.2, 0.13), (DET, 0.13), (DET + 0.5, 0.2), (SECONDS, 0.2)):
    cone_a.default_value = v
    cone_a.keyframe_insert("default_value", frame=int(t * FPS) + 1)

# ------------------------------------------------------------------ langit senja & cahaya
world = bpy.data.worlds.new("w")
scene.world = world
world.use_nodes = True
wn = world.node_tree
bg = wn.nodes["Background"]
grad = wn.nodes.new("ShaderNodeTexGradient")
mapn = wn.nodes.new("ShaderNodeMapping")
tc = wn.nodes.new("ShaderNodeTexCoord")
ramp = wn.nodes.new("ShaderNodeValToRGB")
ramp.color_ramp.elements[0].color = (0.006, 0.01, 0.03, 1)
ramp.color_ramp.elements[1].position = 0.62
ramp.color_ramp.elements[1].color = (0.03, 0.05, 0.12, 1)
e = ramp.color_ramp.elements.new(0.5)
e.color = (0.25, 0.12, 0.06, 1)
ramp.color_ramp.elements[0].position = 0.45
mapn.inputs["Rotation"].default_value = (0, math.radians(-90), 0)
wn.links.new(tc.outputs["Generated"], mapn.inputs["Vector"])
wn.links.new(mapn.outputs["Vector"], grad.inputs["Vector"])
wn.links.new(grad.outputs["Fac"], ramp.inputs["Fac"])
wn.links.new(ramp.outputs["Color"], bg.inputs["Color"])
bg.inputs["Strength"].default_value = 1.0
for name, kind, rot, energy, color in (("sun_low", "SUN", (math.radians(84), 0, math.radians(200)), 0.7, (1.0, 0.62, 0.38)),
                                       ("moon_fill", "SUN", (math.radians(50), 0, math.radians(40)), 0.35, (0.5, 0.65, 1.0))):
    ld = bpy.data.lights.new(name, kind)
    ld.energy = energy
    ld.color = color
    ld.angle = math.radians(3)
    lo = bpy.data.objects.new(name, ld)
    lo.rotation_euler = rot
    scene.collection.objects.link(lo)
# key lembut ke kepala PTZ
ld = bpy.data.lights.new("key_head", "AREA")
ld.energy = 30
ld.size = 2.5
ld.color = (1, 0.9, 0.82)
lo = bpy.data.objects.new("key_head", ld)
lo.location = (-1.0, 3.0, POLE_H + 1.4)
lo.rotation_euler = (Vector((0, 0, HZ)) - lo.location).to_track_quat("-Z", "Y").to_euler()
lo.visible_camera = False
scene.collection.objects.link(lo)

# ------------------------------------------------------------------ kamera render
cam_d = bpy.data.cameras.new("cam")
cam = bpy.data.objects.new("cam", cam_d)
scene.collection.objects.link(cam)
scene.camera = cam
cam_d.clip_end = 600
tgt = bpy.data.objects.new("cam_target", None)
scene.collection.objects.link(tgt)
tt = cam.constraints.new("TRACK_TO")
tt.target = tgt
tt.track_axis = "TRACK_NEGATIVE_Z"
tt.up_axis = "UP_Y"
if ORIENT == "portrait":
    scene.render.resolution_x, scene.render.resolution_y = 1080, 1920
    KEYS = [(0, (-0.5, 2.6, HZ + 0.2), (0, 0, HZ), 30), (3.6, (-3.5, -6.5, HZ - 0.6), (0, 6, HZ - 3), 22),
            (7.0, (-8, -15, 14), (10, 30, 1), 20), (SECONDS, (-4, -18, 15), (14, 32, 1), 20)]
else:
    scene.render.resolution_x, scene.render.resolution_y = 1920, 1080
    KEYS = [(0, (-0.4, 2.4, HZ + 0.15), (0, 0, HZ), 45), (3.6, (-3.8, -6.8, HZ - 0.8), (0, 6, HZ - 3), 32),
            (7.0, (-9, -14, 13), (10, 30, 1), 28), (SECONDS, (-5, -17, 14), (14, 32, 1), 28)]
for t, loc, tg, lens in KEYS:
    f = int(t * FPS) + 1
    cam.location = loc
    tgt.location = tg
    cam_d.lens = lens
    cam.keyframe_insert("location", frame=f)
    tgt.keyframe_insert("location", frame=f)
    cam_d.keyframe_insert("lens", frame=f)
for o in (cam, tgt, cam_d):
    for fc in o.animation_data.action.fcurves:
        for kp in fc.keyframe_points:
            kp.interpolation = "BEZIER"
            kp.easing = "EASE_IN_OUT"
scene.render.fps = FPS
scene.frame_start, scene.frame_end = 1, FPS * SECONDS

# ------------------------------------------------------------------ render EEVEE
for eng in ("BLENDER_EEVEE_NEXT", "BLENDER_EEVEE"):
    try:
        scene.render.engine = eng
        break
    except TypeError:
        continue
ee = scene.eevee
for attr, val in (("taa_render_samples", 32), ("shadow_pool_size", "1024"), ("use_raytracing", True), ("use_shadows", True), ("use_gtao", True)):
    if hasattr(ee, attr):
        setattr(ee, attr, val)
scene.view_settings.look = "AgX - Medium High Contrast" if "AgX - Medium High Contrast" in [
    i.identifier for i in bpy.types.ColorManagedViewSettings.bl_rna.properties["look"].enum_items] else "None"
scene.use_nodes = True
nt = scene.node_tree
rl = nt.nodes.get("Render Layers") or nt.nodes.new("CompositorNodeRLayers")
comp = nt.nodes.get("Composite") or nt.nodes.new("CompositorNodeComposite")
glare = nt.nodes.new("CompositorNodeGlare")
glare.glare_type = "FOG_GLOW"
glare.threshold = 1.0
glare.size = 8
nt.links.new(rl.outputs["Image"], glare.inputs["Image"])
nt.links.new(glare.outputs["Image"], comp.inputs["Image"])

tag = "" if ORIENT == "landscape" else "_portrait"
bpy.ops.wm.save_as_mainfile(filepath=str(HERE / f"ogi_{ORIENT}.blend"))
if MODE == "still":
    for t in (0.5, 3.6, 6.5, 12.0):
        scene.frame_set(int(t * FPS) + 1)
        scene.render.filepath = str(OUT / f"ogi{tag}_{t:g}s.png")
        bpy.ops.render.render(write_still=True)
else:
    if "--preview" in ARGS:
        scene.render.resolution_percentage = 50
        ee.taa_render_samples = 16
    scene.render.image_settings.file_format = "FFMPEG"
    scene.render.ffmpeg.format = "MPEG4"
    scene.render.ffmpeg.codec = "H264"
    scene.render.ffmpeg.constant_rate_factor = "PERC_LOSSLESS" if "--final" in ARGS else "HIGH"
    scene.render.filepath = str(OUT / ("ogi_field.mp4" if "--final" in ARGS else f"ogi{tag}_preview.mp4"))
    bpy.ops.render.render(animation=True)
print("SELESAI")
