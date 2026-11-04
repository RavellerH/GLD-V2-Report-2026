"""OGI 01 — Hook (10 dtk). Kilang digital twin biru malam, kamera melayang rendah menyusuri pipe rack.
Sapuan pindai (garis cahaya) bergerak; sisi yang sudah tersapu tampil palet thermal 'iron' dan plume gas
dari flange bocor mulai terlihat (gas tak kasatmata di mata, tampak di pita MWIR). Ilustrasi konsep.

  blender -b -P shot_ogi_hook.py -- --orient landscape --out ../../public/blender/ht_ogi_hook.mp4 [--still 1 150 300] [--draft]
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import bpy  # noqa: E402
import ht  # noqa: E402
import refinery as R  # noqa: E402

A = ht.args()
SEC = 10.0
ht.setup(SEC)
ht.fog(30, 160)
ht.light_rig(3.0)
ht.floor(size=260, grid=3.0, line_s=0.7)
P = R.build(thermal=True)
N = bpy.context.scene.frame_end

# sapuan thermal: dari barat ke timur, 2.5 s -> 6.5 s
sc = bpy.context.scene
ht.key_prop(sc, "wipe", [(1, -60.0), (ht.sec(2.3), -45.0), (ht.sec(6.8), 40.0), (N, 60.0)])
# tirai laser: bidang tipis transparan + garis terang di lantai & atas (tidak menyilaukan saat menghadap kamera)
curtain = ht.emit_fade("ScanM", "t3", 1.2)
curtain.node_tree.nodes["Vis"].outputs[0].default_value = 0.1
mb = ht.MB()
mb.poly([(0, -45, 0), (0, 45, 0), (0, 45, 16), (0, -45, 16)])
scan = mb.finish("ScanPlane", [curtain])
mb = ht.MB()
mb.box((0, 0, 0.02), (0.15, 90, 0.04))
mb.box((0, 0, 16), (0.08, 90, 0.08))
lines = mb.finish("ScanLines", [ht.emit("ScanLineM", "t4", 4.0)])
for o in (scan, lines):
    d = o.driver_add("location", 0).driver
    d.type = "AVERAGE"
    v = d.variables.new(); v.type = "SINGLE_PROP"
    v.targets[0].id_type = "SCENE"; v.targets[0].id = sc; v.targets[0].data_path = '["wipe"]'

# plume dari flange bocor, terlihat setelah sapuan melewati x = 6 (~5.3 dtk)
blobs, pm = R.plume("Plume", R.LEAK, n=28, length=7.0, f_start=ht.sec(4.6), frames=N)
ht.keyv(pm, "Vis", [(1, 0.0), (ht.sec(5.0), 0.0), (ht.sec(6.2), 1.0)])

# kamera: dari atas pipe rack menyusur ke arah manifold
if ht.portrait():
    cam, tgt = ht.camera((-14, -26, 9.0), (2, 0, 4), lens=24)
    ht.key(cam, "location", [(1, (-14, -26, 9.0)), (N, (0.5, -15, 5.0))])
    ht.key(tgt, "location", [(1, (2, 0, 5)), (N, (6, -1.5, 2.6))])
else:
    cam, tgt = ht.camera((-22, -24, 10.0), (0, 0, 5), lens=26)
    ht.key(cam, "location", [(1, (-22, -24, 10.0)), (N, (-3.5, -14.5, 4.6))])
    ht.key(tgt, "location", [(1, (0, 0, 5)), (N, (6, -1.6, 2.6))])
ht.shake(cam, 0.02, 50)
ht.render()
