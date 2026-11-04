"""OGI 06 — Sistem kamera di lapangan (16 dtk). Kamera OGI pan-tilt di tiang ~10 m (digital twin) berpatroli:
preset 1 jalur pipa (pipe rack), preset 2 manifold, preset 3 klaster valve. Di preset 3 plume terlihat oleh kamera
(ilustrasi) -> kerucut pandang berubah amber + kotak deteksi. Ilustrasi konsep.
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import bpy  # noqa: E402
from mathutils import Vector  # noqa: E402
import ht  # noqa: E402
import refinery as R  # noqa: E402
import devices as D  # noqa: E402

A = ht.args()
SEC = 16.0
ht.setup(SEC)
ht.fog(35, 170)
ht.light_rig(3.0)
ht.floor(size=260, grid=3.0, line_s=0.55)
P = R.build(thermal=False)
N = bpy.context.scene.frame_end

CAM_XY = (-1.0, -17.0)
POLE_H = 10.0
root, pan, tilt = D.ogi_camera("OGI", (*CAM_XY, 0), POLE_H)
D.marker("OGI_Mk", (*CAM_XY, 0), r=1.6)
fr, fm, fem = D.frustum("Cone", tilt, length=26.0, half_w=4.6, half_h=3.0)
EYE = Vector((*CAM_XY, POLE_H + 0.85))
TARGETS = [Vector((-14.0, 0.0, 4.6)), Vector((R.MANIFOLD[0], R.MANIFOLD[1], 1.6)), Vector((R.VALVES[0], R.VALVES[1] - 0.8, 1.4))]


def aim(t):
    d = t - EYE
    th = math.atan2(d.x, -d.y)
    ph = math.atan2(-d.z, Vector((d.x, d.y)).length)
    return th, ph


S = [(1, 0), (ht.sec(3.8), 0), (ht.sec(5.0), 1), (ht.sec(8.2), 1), (ht.sec(9.4), 2), (N, 2)]
for f, k in S:
    th, ph = aim(TARGETS[k])
    pan.rotation_euler = (0, 0, th)
    pan.keyframe_insert("rotation_euler", frame=f)
    tilt.rotation_euler = (ph, 0, 0)
    tilt.keyframe_insert("rotation_euler", frame=f)
ht._interp(pan, "BEZIER"); ht._interp(tilt, "BEZIER")

# plume di klaster valve (preset 3), terlihat kamera
T_DET = ht.sec(11.0)
leak = (R.VALVES[0], R.VALVES[1] - 0.8, 1.7)
blobs, pm = R.plume("Plume", leak, n=22, wind=(1.0, 0.35, 0.3), length=5.0, f_start=ht.sec(7.5), frames=N, tok="amber")
ht.keyv(pm, "Vis", [(1, 0.0), (ht.sec(9.6), 0.0), (T_DET, 1.0)])
for m in (fm, fem):
    ht.keyv(m, "Alert", [(1, 0.0), (T_DET - 5, 0.0), (T_DET + 10, 1.0)])

# kotak deteksi 3D (bracket sudut) di sekitar plume
bm = ht.emit_fade("DetM", "amber", 4.0)
mb = ht.MB()
c = Vector((leak[0] + 2.0, leak[1] + 0.6, leak[2] + 0.8))
hx, hy, hz = 3.4, 2.0, 1.6
L = 0.9
w = 0.05
for sx in (-1, 1):
    for sy in (-1, 1):
        for sz in (-1, 1):
            p = c + Vector((sx * hx, sy * hy, sz * hz))
            mb.box(tuple(p - Vector((sx * L / 2, 0, 0))), (L, w, w))
            mb.box(tuple(p - Vector((0, sy * L / 2, 0))), (w, L, w))
            mb.box(tuple(p - Vector((0, 0, sz * L / 2))), (w, w, L))
det = mb.finish("DetBox", [bm])
ht.keyv(bm, "Vis", [(1, 0.0), (T_DET + 6, 0.0), (T_DET + 14, 1.0), (T_DET + 20, 0.6), (T_DET + 26, 1.0)])
beac, bmat = ht.beacon("Alarm", (leak[0], leak[1], 0), "amber", r=0.6, h=14)
ht.keyv(bmat, "Amp", [(1, 0.0), (T_DET + 12, 0.0), (T_DET + 24, 1.0)])

cam, tgt = ht.camera((-34, -30, 16), (-3, -8, 3), lens=26)
ht.key(cam, "location", [(1, (-36, -32, 17)), (ht.sec(9.0), (-31, -26, 14)), (N, (-19, -25, 9.5))])
ht.key(tgt, "location", [(1, (-3, -8, 4)), (ht.sec(9.0), (-4, -7, 3)), (N, (-7, -4, 2.2))])
ht.dust(center=(-6, -8, 5), extent=(50, 40, 12), n=500)
ht.render()
