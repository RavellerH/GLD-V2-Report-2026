"""OGI 04 — Prinsip fisika (14 dtk). Molekul metana hologram (C + 4 H). Gelombang inframerah dari kiri:
panjang gelombang lain lewat tanpa berubah, gelombang ~3,3 um (amber) diserap -> ikatan C-H bergetar lebih kuat
dan menyala, gelombang amber setelah molekul melemah. Lalu kamera mundur: awan molekul gas di depan latar hangat,
filter pita sempit hanya meloloskan pita amber -> awan tampak sebagai kontras. Ilustrasi konsep.
"""
import math
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import bpy  # noqa: E402
from mathutils import Matrix, Vector  # noqa: E402
import ht  # noqa: E402

A = ht.args()
SEC = 14.0
ht.setup(SEC, samples=24)
ht.fog(14, 50)
ht.light_rig(0.8)
ht.floor(size=80, grid=1.0, line_s=0.2)
N = bpy.context.scene.frame_end
rnd = random.Random(9)
Z = 1.6
T_ABS = ht.sec(3.2)
T_BACK0, T_BACK1 = ht.sec(7.4), ht.sec(10.5)

cm = ht.twin("Carbon", body="#1d2b3f", rim="holo2", rim_s=2.4, scan=False, rough=0.25)
hm = ht.twin("Hydro", body="#e8f2ff", rim="holo", rim_s=1.2, scan=False, rough=0.3)
bond_m, nt, out = ht._new("BondM")
g = ht._G(nt)
hot = g.val("Hot", 0.0)
e = nt.nodes.new("ShaderNodeEmission")
g.L.new(g.mixc(hot, ht.col("holo"), ht.col("amber")), e.inputs["Color"])
g.L.new(g.op("MULTIPLY_ADD", hot, 4.0, 1.4), e.inputs["Strength"])
g.L.new(e.outputs[0], out.inputs["Surface"])

TET = [Vector(v).normalized() for v in ((1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1))]


def molecule(name, loc, s=1.0, vib_from=None, phase=0.0, big=False):
    root = ht.empty(name, loc)
    c = ht.uvsphere(name + "_C", (0, 0, 0), 0.34 * s, cm, seg=32 if big else 16, rings=16 if big else 8)
    c.parent = root
    for i, d in enumerate(TET):
        piv = ht.empty(f"{name}_P{i}", (0, 0, 0))
        piv.parent = root
        piv.rotation_euler = d.to_track_quat("Z", "Y").to_euler()
        bnd = ht.cyl(f"{name}_B{i}", (0, 0, 0.5), 0.045 * s, 1.0, bond_m, seg=12 if big else 6)
        bnd.parent = piv
        h = ht.uvsphere(f"{name}_H{i}", (0, 0, 0.9 * s), 0.2 * s, hm, seg=24 if big else 12, rings=12 if big else 6)
        h.parent = piv
        L0 = 0.9 * s
        keys_h, keys_b = [], []
        for f in range(1, N + 1, 2):
            amp = 0.025
            if vib_from is not None and f > vib_from:
                amp = 0.025 + 0.11 * min(1.0, (f - vib_from) / 25)
            w = 0.9 if vib_from is None or f <= vib_from else 1.25
            L = L0 * (1 + amp * math.sin(f * w + i * 1.7 + phase))
            keys_h.append((f, (0, 0, L)))
            keys_b.append((f, (1, 1, L)))
        ht.key(h, "location", keys_h, interp="LINEAR")
        bnd.location = (0, 0, 0)
        bnd.data.transform(Matrix.Translation((0, 0, 0.5)))  # pangkal di C: skala z = panjang ikatan
        ht.key(bnd, "scale", keys_b, interp="LINEAR")
    return root


big = molecule("CH4", (0, 0, Z), 1.0, vib_from=T_ABS + 10, big=True)
ht.key(big, "rotation_euler", [(1, (0.3, 0, 0)), (N, (0.3, 0.6, math.radians(140)))], interp="LINEAR")
ht.keyv(bond_m, "Hot", [(1, 0.0), (T_ABS, 0.0), (T_ABS + 25, 1.0)])


# gelombang inframerah: tabung sinus, aliran berdenyut ke kanan
def wave(name, tok, lam, z_off, y_off, x0, x1, amp=0.18, rate=0.9, fade_after=None):
    m = ht.pulse(name + "M", tok, rate=rate, base=1.2, amp=3.5, waves=6.0, sharp=3, hide=True)
    pts = []
    n = int((x1 - x0) / (lam / 10)) + 2
    for k in range(n + 1):
        x = x0 + (x1 - x0) * k / n
        pts.append((x, y_off, Z + z_off + amp * math.sin(2 * math.pi * x / lam)))
    o = ht.tube(name, pts, 0.022, m, seg=6, smooth_path=False)
    return o, m


waves = [("Wv_a", "blue2", 1.3, 0.55, 0.0), ("Wv_b", "violet", 0.55, -0.55, 0.2), ("Wv_c", "holo", 0.9, 0.0, -0.4)]
for nm, tk, lam, zo, yo in waves:
    _, m = wave(nm + "_in", tk, lam, zo, yo, -9.0, 0.0)
    _, m2 = wave(nm + "_out", tk, lam, zo, yo, 0.0, 9.0)
    ht.keyv(m, "Amp", [(1, 0.0), (ht.sec(0.4), 1.0), (T_BACK0, 1.0), (T_BACK0 + 30, 0.0)])
    ht.keyv(m2, "Amp", [(1, 0.0), (ht.sec(1.2), 1.0), (T_BACK0, 1.0), (T_BACK0 + 30, 0.0)])
# gelombang amber (~3,3 um) menuju molekul, setelahnya melemah
_, ma = wave("Wv_abs_in", "t3", 0.42, 0.22, 0.1, -9.0, -0.3, amp=0.2)
_, mb_ = wave("Wv_abs_out", "t3", 0.42, 0.22, 0.1, 0.3, 9.0, amp=0.2)
ht.keyv(ma, "Amp", [(1, 0.0), (ht.sec(1.6), 0.0), (ht.sec(2.4), 1.0), (T_BACK0, 1.0), (T_BACK0 + 30, 0.0)])
ht.keyv(mb_, "Amp", [(1, 0.0), (ht.sec(2.4), 0.0), (ht.sec(3.0), 1.0), (T_ABS + 20, 0.12), (T_BACK0, 0.12), (T_BACK0 + 30, 0.0)])
# kilatan penyerapan
flash = ht.emit_fade("FlashM", "amber", 6.0)
fl = ht.sphere("Flash", (0, 0, Z), 0.75, flash, sub=3)
ht.keyv(flash, "Vis", [(1, 0.0), (T_ABS, 0.0), (T_ABS + 6, 0.1), (T_ABS + 24, 0.0)])

# tahap 2: awan molekul + latar hangat + filter pita sempit
cloud = []
for i in range(36):
    p = Vector((rnd.uniform(4.0, 9.0), rnd.uniform(-2.5, 2.5), rnd.uniform(0.6, 3.6)))
    mo = molecule(f"M{i}", tuple(p), 0.32, vib_from=T_BACK0 + rnd.randint(0, 30), phase=rnd.random() * 6)
    mo.rotation_euler = (rnd.random() * 6, rnd.random() * 6, rnd.random() * 6)
    cloud.append(mo)
    ht.show([o for o in mo.children_recursive if o.type == "MESH"], T_BACK0 + rnd.randint(0, 25))
warm = ht.emit("WarmWall", "t2", 0.9)
wall = ht.box("Wall", (13.5, 0, 2.2), (0.1, 9, 4.4), warm)
filt = ht.pulse("FiltM", "amber", rate=0.4, base=1.0, amp=1.5, waves=1.0, sharp=3)
fd = ht.cyl("Filter", (-3.2, 0, Z + 0.4), 0.9, 0.05, ht.glass("FiltGlass", "amber", alpha=0.35, glow=0.9), axis="X", seg=64)
fr = ht.ring("FilterRing", (-3.2, 0, Z + 0.4), 0.92, 0.03, ht.emit("FRingM", "amber", 3.0), seg=96, rot=(0, math.pi / 2, 0))
ht.show([fd, fr], T_BACK0 + 20)
# berkas dari dinding hangat, menembus awan, ke filter
beams = ht.pulse("BeamM", "t3", rate=-0.8, base=0.3, amp=5.0, waves=3.0, sharp=8, hide=True)
for i in range(7):
    z = 0.8 + i * 0.45
    y = (i - 3) * 0.55
    o = ht.tube(f"Beam{i}", [(13.3, y, z), (8, y * 0.7, z * 0.9 + 0.2), (2, y * 0.3, (z + Z + 0.4) / 2), (-3.1, y * 0.08, Z + 0.4 + (z - 2.1) * 0.08)], 0.015, beams, seg=5)
ht.keyv(beams, "Amp", [(1, 0.0), (T_BACK1 - 20, 0.0), (T_BACK1 + 10, 1.0)])

if ht.portrait():
    cam, tgt = ht.camera((-1.5, -6.5, Z + 1.0), (0, 0, Z), lens=30)
    ht.key(cam, "location", [(1, (-1.2, -5.2, Z + 0.8)), (T_BACK0, (-0.4, -4.4, Z + 0.6)), (T_BACK1, (-9.5, -9.5, Z + 3.0)), (N, (-10.5, -9.0, Z + 3.2))])
    ht.key(tgt, "location", [(1, (0, 0, Z)), (T_BACK0, (0, 0, Z)), (T_BACK1, (4.5, 0, Z + 0.4)), (N, (5.0, 0, Z + 0.4))])
else:
    cam, tgt = ht.camera((-1.5, -4.6, Z + 0.7), (0, 0, Z), lens=32)
    ht.key(cam, "location", [(1, (-1.8, -4.4, Z + 0.7)), (T_BACK0, (-0.6, -3.4, Z + 0.45)), (T_BACK1, (-8.0, -7.0, Z + 2.2)), (N, (-8.8, -6.4, Z + 2.4))])
    ht.key(tgt, "location", [(1, (0, 0, Z)), (T_BACK0, (0, 0, Z)), (T_BACK1, (4.0, 0, Z + 0.3)), (N, (4.6, 0, Z + 0.3))])
ht.render()
