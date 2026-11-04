"""GLD — Inti perangkat (12 dtk). Model GLD V2 asli (gld_v2.blend, material PBR) di panggung kaca hitam:
0–3 dtk berputar utuh; 3–6 dtk terurai sepanjang sumbu depan (tutup, mesh, kipas ke depan; motherboard ke belakang);
6–9 dtk delapan sensor MQ menyala bergantian, aliran data menuju MCU; 9–12 dtk sidik jari 8-sumbu hologram
muncul di belakang perangkat (pola respons -> klasifikasi edge AI). Ilustrasi.
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import bpy  # noqa: E402
from mathutils import Vector  # noqa: E402
import ht  # noqa: E402

A = ht.args()
SEC = 12.0
ht.setup(SEC, samples=24)
ht.fog(1.0, 4.0)
N = bpy.context.scene.frame_end
BLEND = Path(__file__).resolve().parents[1] / "gld_v2.blend"

# --- muat model asli -------------------------------------------------------------------
with bpy.data.libraries.load(str(BLEND), link=False) as (src, dst):
    dst.objects = [n for n in src.objects]
root = ht.empty("GLD", (0, 0, 0))
groups = {}
for o in dst.objects:
    if o is None or o.name == "floor" or o.type not in ("MESH", "EMPTY"):
        continue
    bpy.context.scene.collection.objects.link(o)
for o in dst.objects:
    if o is None or o.name == "floor":
        continue
    if o.type == "EMPTY" and o.name.startswith("grp_"):
        groups[o.name] = o
        o.parent = root
    elif o.type == "EMPTY" and o.name == "GLD_V2":
        o.parent = root
for o in list(bpy.data.objects):
    if o.name == "floor":
        bpy.data.objects.remove(o)

T_EXP0, T_EXP1 = ht.sec(2.8), ht.sec(5.6)
T_MQ = ht.sec(6.0)
T_FP = ht.sec(8.8)
# semua komponen internal keluar lewat bukaan depan (-Y); body/base diam. Urutan depan->belakang:
# tutup, mesh, gasket, pengunci, kipas, O-ring, sensor board, motherboard.
EXP = {"grp_cover": -0.19, "grp_mesh": -0.145, "grp_mesh_gasket": -0.13, "grp_mesh_lock": -0.115, "grp_fan": -0.095,
       "grp_oring": -0.075, "grp_sensor_board": -0.06, "grp_motherboard": -0.045}
for g, dy in EXP.items():
    if g in groups:
        ht.key(groups[g], "location", [(T_EXP0, (0, 0, 0)), (T_EXP1, (0, dy, 0))])
# putar seluruh perangkat pelan
ht.key(root, "rotation_euler", [(1, (0, 0, math.radians(12))), (T_EXP0, (0, 0, math.radians(40))), (T_EXP1, (0, 0, math.radians(78))), (N, (0, 0, math.radians(92)))])

# --- panggung ----------------------------------------------------------------------------
fl = ht.floor(size=8, grid=0.06, line_s=0.55)
fl.location.z = -0.092
rings, _ = ht.scan_rings("Reticle", (0, 0, -0.091), radii=(0.12, 0.15, 0.19, 0.24), w=0.0022)
ht.area("Key", (-0.55, -0.65, 0.55), (52, 0, -38), 26, 0.5, (0.85, 0.92, 1.0))
ht.area("Rim", (0.6, 0.55, 0.35), (-65, 0, 135), 70, 0.4, (0.4, 0.75, 1.0))
ht.area("RimL", (-0.6, 0.45, 0.25), (-65, 0, -135), 40, 0.4, (0.55, 0.45, 1.0))
ht.area("Top", (0, 0, 0.7), (0, 0, 0), 25, 0.6)

# --- sensor MQ menyala bergantian --------------------------------------------------------
sb = groups["grp_sensor_board"]
mq_centers = []
for k in range(8):
    caps = [o for o in bpy.data.objects if o.name.startswith(f"mq{k}_") and o.type == "MESH"]
    if not caps:
        continue
    pts = []
    for o in caps:
        pts += [o.matrix_world @ Vector(c) for c in o.bound_box]
    c = sum(pts, Vector()) / len(pts)
    mq_centers.append(c)
order = sorted(range(len(mq_centers)), key=lambda i: math.atan2(mq_centers[i].z, mq_centers[i].x))
for rank, i in enumerate(order):
    c = mq_centers[i]
    m = ht.emit(f"MqGlow{i}", "holo", 0.0)
    r = ht.ring(f"MqRing{i}", (c.x, -0.006, c.z), 0.0085, 0.0012, m, seg=48, rot=(math.pi / 2, 0, 0))
    r.parent = sb
    t = T_MQ + rank * 8
    ht.keyin(m, "Emit", "Strength", [(1, 0.0), (t, 0.0), (t + 4, 14.0), (t + 14, 5.0)])
    ht.keyin(m, "Emit", "Color", [(1, ht.col("amber")), (t + 4, ht.col("amber")), (t + 16, ht.col("holo"))])

# aliran data dari tiap sensor ke MCU (posisi terurai)
mcu = Vector((-0.006, 0.025 + EXP["grp_motherboard"], 0.003))
sm = ht.pulse("StreamM", "holo", rate=1.4, base=0.3, amp=8.0, waves=2.0, sharp=10, hide=True)
for i, c in enumerate(mq_centers):
    a = Vector((c.x, 0.012 + EXP["grp_sensor_board"], c.z))
    mid = (a + mcu) / 2 + Vector((0, 0, 0.012))
    o = ht.tube(f"Stream{i}", [a, a.lerp(mid, 0.5), mid, mid.lerp(mcu, 0.5), mcu], 0.0007, sm, seg=5, step=0.004)
    o.parent = root
ht.keyv(sm, "Amp", [(1, 0.0), (T_MQ + 30, 0.0), (T_MQ + 45, 1.0)])
chip = ht.emit("ChipGlow", "holo2", 0.0)
cg = ht.box("ChipHalo", (mcu.x, mcu.y + 0.004, mcu.z), (0.022, 0.001, 0.03), chip)
cg.parent = root
ht.keyin(chip, "Emit", "Strength", [(1, 0.0), (T_MQ + 40, 0.0), (T_MQ + 60, 3.0)])

# --- sidik jari 8-sumbu hologram -----------------------------------------------------------
FP_C = Vector((-0.17, 0.06, 0.09))
R = 0.075
grid_m = ht.emit_fade("FpGridM", "blue2", 2.2)
poly_m = ht.emit_fade("FpPolyM", "amber", 3.0)
fill_m = ht.emit_fade("FpFillM", "amber", 0.8)
mb = ht.MB()
w = 0.0009
for ring_r in (0.33, 0.66, 1.0):
    for k in range(8):
        a0, a1 = 2 * math.pi * k / 8, 2 * math.pi * (k + 1) / 8
        p0 = Vector((math.cos(a0), 0, math.sin(a0))) * R * ring_r
        p1 = Vector((math.cos(a1), 0, math.sin(a1))) * R * ring_r
        d = (p1 - p0).normalized()
        n = Vector((-d.z, 0, d.x)) * w
        mb.poly([p0 - n, p1 - n, p1 + n, p0 + n])
for k in range(8):
    a = 2 * math.pi * k / 8
    p = Vector((math.cos(a), 0, math.sin(a))) * R
    n = Vector((-math.sin(a), 0, math.cos(a))) * w * 0.7
    mb.poly([-n, p - n, p + n, n])
grid = mb.finish("FpGrid", [grid_m], tuple(FP_C))
VALS = [0.35, 0.82, 0.55, 0.95, 0.4, 0.7, 0.3, 0.6]
pts = [Vector((math.cos(2 * math.pi * k / 8), 0, math.sin(2 * math.pi * k / 8))) * R * v for k, v in enumerate(VALS)]
mb = ht.MB()
for k in range(8):
    p0, p1 = pts[k], pts[(k + 1) % 8]
    d = (p1 - p0).normalized()
    n = Vector((-d.z, 0, d.x)) * w * 1.6
    mb.poly([p0 - n, p1 - n, p1 + n, p0 + n])
poly = mb.finish("FpPoly", [poly_m], tuple(FP_C))
mb = ht.MB()
for k in range(8):
    mb.poly([Vector((0, 0.0005, 0)), pts[k] + Vector((0, 0.0005, 0)), pts[(k + 1) % 8] + Vector((0, 0.0005, 0))])
fill = mb.finish("FpFill", [fill_m], tuple(FP_C))
for o in (grid, poly, fill):
    o.rotation_euler = (0, 0, 0.5)
for m in (grid_m, poly_m, fill_m):
    ht.keyv(m, "Vis", [(1, 0.0), (T_FP, 0.0), (T_FP + 18, 1.0)])
for o in (poly, fill):
    ht.key(o, "scale", [(T_FP, (0.2, 0.2, 0.2)), (T_FP + 24, (1, 1, 1)), (N, (1.06, 1.06, 1.06))])


if ht.portrait():
    cam, tgt = ht.camera((0.35, -0.6, 0.12), (0, -0.02, 0.01), lens=42)
else:
    cam, tgt = ht.camera((0.3, -0.42, 0.1), (0, -0.02, 0.01), lens=40)
ht.key(cam, "location", [(1, (0.22, -0.34, 0.06)), (T_EXP0, (0.26, -0.4, 0.08)), (T_EXP1, (0.42, -0.48, 0.13)), (T_FP, (0.38, -0.52, 0.12)), (N, (0.27, -0.64, 0.12))])
ht.key(tgt, "location", [(1, (0, 0, 0.01)), (T_EXP1, (0, -0.07, 0.01)), (T_FP, (0, -0.04, 0.02)), (N, (0, -0.01, 0.04))])
cam.data.clip_start = 0.005
ht.dof(cam, 0.5, 6.0)
cam.data.dof.focus_object = tgt
ht.render()
