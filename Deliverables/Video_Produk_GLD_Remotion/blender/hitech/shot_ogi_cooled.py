"""OGI 05 — Detektor berpendingin (14 dtk). Kamera MWIR generik terurai sepanjang sumbu optik (gaya hologram):
jendela depan, grup lensa, filter spektral sempit ~3,3 um, dewar vakum + cold finger, FPA (focal plane array),
Stirling cooler, papan readout. Lalu pendinginan: cahaya dingin menjalar ke FPA, piksel FPA dari berderau -> bersih,
berkas inframerah melewati lensa & filter menuju FPA. Ilustrasi struktur umum, bukan produk tertentu.
"""
import math
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import bpy  # noqa: E402
from mathutils import Vector  # noqa: E402
import ht  # noqa: E402

A = ht.args()
SEC = 14.0
ht.setup(SEC, samples=24)
ht.fog(12, 40)
ht.light_rig(0.6)
ht.floor(size=60, grid=0.75, line_s=0.22)
rings, _ = ht.scan_rings("Rings", (0, 0, 0), radii=(1.2, 1.6, 2.1, 2.8))
N = bpy.context.scene.frame_end
rnd = random.Random(5)

Z = 1.25          # tinggi sumbu optik
root = ht.empty("Cam", (0, 0, Z))
T_EXP0, T_EXP1 = ht.sec(2.6), ht.sec(6.0)
T_COOL0, T_COOL1 = ht.sec(7.0), ht.sec(10.5)
T_RAY = ht.sec(9.5)

parts = []  # (obj, y_assembled, y_exploded)


def place(o, y0, y1):
    o.parent = root
    o.location.y = y0
    ht.key(o, "location", [(T_EXP0, (o.location.x, y0, o.location.z)), (T_EXP1, (o.location.x, y1, o.location.z))])
    parts.append(o)
    return o


twin = ht.twin("Body", body="body", rim="holo", rim_s=2.2, scan=False)
twin2 = ht.twin("Body2", body="body2", rim="holo2", rim_s=1.8, scan=False)
steel = ht.twin("Steel", body="steel", rim="holo", rim_s=1.2, scan=False)
glass = ht.glass("Lens", "holo2", alpha=0.22, glow=0.25)
germ = ht.glass("Germ", "#7f8fb0", alpha=0.45, glow=0.15)

# housing: cangkang solid -> hologram saat terurai
house_solid = ht.twin("HouseSolid", body="#c9d3e2", rim="holo2", rim_s=1.0, scan=False, rough=0.3)
house = ht.box("Housing", (0, 0, 0), (0.62, 1.55, 0.6), house_solid, bevel=0.05)
house.parent = root
house.location.y = 0.1
hshell = ht.holo("HouseHolo", "holo", base=0.02, rim=2.0, scan=0.12)
hshell.node_tree.nodes["Vis"].outputs[0].default_value = 0.0
house2 = ht.box("HousingHolo", (0, 0, 0), (0.64, 1.57, 0.62), hshell, bevel=0.05)
house2.parent = root
house2.location.y = 0.1
ht.show([house], 1, T_EXP0 + 20)
ht.keyv(hshell, "Vis", [(T_EXP0, 0.0), (T_EXP0 + 25, 1.0), (T_EXP1, 0.55)])
ht.key(house2, "scale", [(T_EXP0, (1, 1, 1)), (T_EXP1, (1.15, 2.9, 1.15))])

# jendela germanium + tudung
place(ht.cyl("Hood", (0, 0, 0), 0.26, 0.2, twin, axis="Y", seg=48), -0.78, -2.6)
place(ht.cyl("Window", (0, 0, 0), 0.22, 0.03, germ, axis="Y", seg=48), -0.86, -2.85)
# grup lensa (3 elemen)
for i, (r, sy) in enumerate(((0.2, 0.08), (0.17, 0.06), (0.14, 0.05))):
    ln = ht.sphere(f"Lens{i}", (0, 0, 0), 1.0, glass, sub=3, scale=(r, sy, r))
    place(ln, -0.55 + i * 0.12, -1.9 + i * 0.32)
    rg = ht.ring(f"LensRing{i}", (0, 0, 0), r + 0.01, 0.012, ht.emit(f"LRM{i}", "holo", 2.0), seg=64, rot=(math.pi / 2, 0, 0))
    place(rg, -0.55 + i * 0.12, -1.9 + i * 0.32)
# filter spektral (amber, berdenyut)
filt_m = ht.pulse("FilterM", "amber", rate=0.5, base=1.2, amp=1.5, waves=1.0, sharp=3)
flt = ht.cyl("Filter", (0, 0, 0), 0.16, 0.025, filt_m, axis="Y", seg=48)
place(flt, -0.12, -0.75)
place(ht.ring("FilterRing", (0, 0, 0), 0.175, 0.012, ht.emit("FRM", "amber", 3.0), seg=64, rot=(math.pi / 2, 0, 0)), -0.12, -0.75)
# dewar vakum (cangkang tembus pandang) + cold finger
dew = ht.cyl("Dewar", (0, 0, 0), 0.19, 0.42, ht.holo("DewarM", "holo2", base=0.04, rim=2.2, scan=0.1), axis="Y", seg=48)
place(dew, 0.18, 0.15)
place(ht.cyl("DewarWin", (0, 0, 0), 0.15, 0.02, germ, axis="Y", seg=40), -0.04, -0.12)
cold = ht.pulse("ColdM", "#9fe8ff", rate=0.9, base=0.5, amp=6.0, waves=2.0, sharp=6)
cf = ht.cyl("ColdFinger", (0, 0, 0), 0.045, 0.62, cold, axis="Y", seg=20)
# phase sepanjang cold finger (dari belakang -> depan) untuk gelombang dingin
ph = cf.data.attributes["phase"] if "phase" in cf.data.attributes else cf.data.attributes.new("phase", "FLOAT", "FACE")
for p in cf.data.polygons:
    ph.data[p.index].value = 1.0 - (p.center.y + 0.31) / 0.62
place(cf, 0.36, 0.55)
# FPA: chip + kisi piksel
chip = ht.box("FPA_Chip", (0, 0, 0), (0.2, 0.02, 0.16), twin2)
place(chip, 0.02, -0.05)
pix_m, nt, out = ht._new("PixM")
g = ht._G(nt)
a = nt.nodes.new("ShaderNodeAttribute"); a.attribute_name = "phase"; a.attribute_type = "GEOMETRY"
t = ht.time_node(pix_m)
noise = g.op("FRACT", g.op("MULTIPLY", g.op("SINE", g.op("MULTIPLY_ADD", a.outputs["Fac"], 917.3, g.op("MULTIPLY", t.outputs[0], 23.0))), 4375.5))
clean = g.val("Clean", 0.0)
img = g.op("POWER", g.op("SUBTRACT", 1.0, g.op("ABSOLUTE", g.op("SUBTRACT", a.outputs["Fac"], 0.5))), 3.0)
v = g.op("ADD", g.op("MULTIPLY", noise, g.op("SUBTRACT", 1.0, clean)), g.op("MULTIPLY", img, clean))
e = nt.nodes.new("ShaderNodeEmission")
g.L.new(g.mixc(clean, ht.col("t2"), ht.col("holo")), e.inputs["Color"])
g.L.new(g.op("MULTIPLY", v, 3.0), e.inputs["Strength"])
g.L.new(e.outputs[0], out.inputs["Surface"])
mb = ht.MB()
NX, NZ = 16, 12
for i in range(NX):
    for k in range(NZ):
        x = -0.085 + i * 0.17 / NX
        z = -0.065 + k * 0.13 / NZ
        cx, cz = (i + 0.5) / NX - 0.5, (k + 0.5) / NZ - 0.5
        mb.poly([(x, -0.012, z), (x + 0.0095, -0.012, z), (x + 0.0095, -0.012, z + 0.0095), (x, -0.012, z + 0.0095)], 0,
                (i * NZ + k) / (NX * NZ) if False else min(1.0, math.hypot(cx, cz) * 1.4))
pix = mb.finish("FPA_Pix", [pix_m])
place(pix, 0.02, -0.05)
ht.keyv(pix_m, "Clean", [(1, 0.0), (T_COOL1 - 10, 0.0), (T_COOL1 + 20, 1.0)])
# Stirling cooler: badan + sirip + piston berosilasi
cool = ht.cyl("Cooler", (0, 0, 0), 0.17, 0.36, steel, axis="Y", seg=40)
place(cool, 0.62, 1.35)
for i in range(6):
    place(ht.ring(f"Fin{i}", (0, 0, 0), 0.2, 0.02, ht.emit(f"FinM{i}", "blue2", 1.2), seg=64, rot=(math.pi / 2, 0, 0)), 0.5 + i * 0.05, 1.23 + i * 0.05)
pist = ht.cyl("Piston", (0, 0, 0), 0.09, 0.16, twin2, axis="Y", seg=24)
place(pist, 0.86, 1.68)
pist.location.z = 0.0
# osilasi piston (setelah terurai)
keys = []
for f in range(T_EXP1, N + 1, 3):
    keys.append((f, (0, 1.68 + 0.035 * math.sin((f - T_EXP1) * 0.9), 0)))
ht.key(pist, "location", [(1, (0, 0.86, 0)), (T_EXP0, (0, 0.86, 0))] + keys, interp="LINEAR")
# papan readout
board = ht.box("Readout", (0, 0, 0), (0.5, 0.03, 0.42), ht.twin("Pcb", body="#0d3b2c", rim="ok", rim_s=1.2, scan=False))
place(board, 0.68, 2.2)
for i in range(5):
    c = ht.box(f"Ic{i}", (0, 0, 0), (0.08, 0.02, 0.06), twin2)
    c.parent = root
    c.location = (-0.15 + (i % 3) * 0.15, 0.68, -0.08 + (i // 3) * 0.15)
    ht.key(c, "location", [(T_EXP0, (c.location.x, 0.66, c.location.z)), (T_EXP1, (c.location.x, 2.18, c.location.z))])

# pendinginan: gelombang dingin menjalar sepanjang cold finger, cincin embun beku di dewar
ht.keyv(cold, "Amp", [(1, 0.0), (T_COOL0, 0.0), (T_COOL0 + 20, 1.0)])
frost = ht.emit_fade("FrostM", "#bff4ff", 3.0)
fr = ht.ring("Frost", (0, 0, 0), 0.2, 0.025, frost, seg=72, rot=(math.pi / 2, 0, 0))
place(fr, 0.18, 0.15)
ht.keyv(frost, "Vis", [(1, 0.0), (T_COOL0 + 10, 0.0), (T_COOL1, 1.0)])
ht.point("ColdLight", (0, 0.2, Z), 0, (0.6, 0.9, 1.0))
cl = bpy.data.objects["ColdLight"]
cl.data.energy = 0
for f, en in ((1, 0), (T_COOL0, 0), (T_COOL1, 25)):
    cl.data.energy = en
    cl.data.keyframe_insert("energy", frame=f)

# berkas inframerah: dari depan menembus lensa & filter ke FPA (setelah terurai)
rays = ht.pulse("RayM", "t3", rate=1.1, base=0.2, amp=6.0, waves=3.0, sharp=8, hide=True)
ray_objs = []
for i in range(5):
    dz = (i - 2) * 0.05
    pts = [(dz * 3, -4.5, dz * 3), (dz * 2.2, -2.85, dz * 2.2), (dz * 1.2, -1.5, dz * 1.2), (dz * 0.5, -0.75, dz * 0.5), (dz * 0.15, -0.12, dz * 0.15), (dz * 0.08, -0.06, dz * 0.08)]
    o = ht.tube(f"Ray{i}", pts, 0.008, rays, seg=5)
    o.parent = root
    ray_objs.append(o)
ht.keyv(rays, "Amp", [(1, 0.0), (T_RAY, 0.0), (T_RAY + 15, 1.0)])

# rotasi pelan seluruh kamera
ht.key(root, "rotation_euler", [(1, (0, 0, math.radians(-38))), (T_EXP0, (0, 0, math.radians(-20))), (T_EXP1, (0, 0, math.radians(-62))), (N, (0, 0, math.radians(-72)))])

if ht.portrait():
    cam, tgt = ht.camera((3.4, -5.6, 2.4), (0, 0, Z), lens=34)
    ht.key(cam, "location", [(1, (2.4, -3.6, 1.9)), (T_EXP1, (3.6, -6.4, 2.5)), (N, (3.0, -5.6, 2.2))])
else:
    cam, tgt = ht.camera((2.4, -3.6, 1.9), (0, 0, Z), lens=30)
    ht.key(cam, "location", [(1, (1.5, -2.2, 1.55)), (T_EXP1, (2.7, -3.9, 1.8)), (N, (2.25, -3.35, 1.6))])
ht.key(tgt, "location", [(1, (0, 0, Z)), (T_EXP1, (0.2, 0, Z)), (N, (0.1, 0, Z))])
ht.render()
