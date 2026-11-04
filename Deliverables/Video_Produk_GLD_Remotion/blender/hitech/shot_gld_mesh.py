"""GLD — Jaringan private mesh LoRa & push alarm (14 dtk). Kilang digital twin dengan 3 node GLD, 3 Cluster Head,
dan Gateway (ruang kontrol). 0–6 dtk: paket data normal (biru-es) dikirim berkala GLD -> CH -> Gateway.
6,5 dtk: kebocoran di dekat GLD-1 (plume amber) -> LED merah, pilar alarm, paket alarm merah langsung melompat
ke Gateway lewat jalur mesh; Gateway menyala. Ukuran perangkat dibesarkan agar terbaca (ilustrasi).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import bpy  # noqa: E402
import ht  # noqa: E402
import refinery as R  # noqa: E402
import devices as D  # noqa: E402

A = ht.args()
SEC = 14.0
ht.setup(SEC)
ht.fog(40, 180)
ht.light_rig(3.0)
ht.floor(size=260, grid=3.0, line_s=0.5)
P = R.build(thermal=False, flare_on=True)
N = bpy.context.scene.frame_end
S = 4.0  # skala tampilan perangkat

GLDS = {"G1": (5.0, -4.2), "G2": (-9.5, -6.0), "G3": (-14.5, -13.0)}
CHS = {"C1": (1.0, -12.0), "C2": (-12.0, -17.0), "C3": (9.0, -22.0)}
GW = (-1.0, -30.0)
leds = {}
for k, (x, y) in GLDS.items():
    root, led = D.gld(k, (x, y, 0), mount_h=0.6 * S, scale=S)
    leds[k] = led
    D.marker(k + "_Mk", (x, y, 0), tok="ok", r=1.6)
for k, (x, y) in CHS.items():
    D.ch(k, (x, y, 0), h=5.0)
    D.marker(k + "_Mk", (x, y, 0), tok="holo", r=1.8)
D.gateway("GW", (*GW, 0))
D.marker("GW_Mk", (*GW, 0), tok="blue2", r=4.0)

top = {k: (x, y, 0.6 * S + 1.2) for k, (x, y) in GLDS.items()}
top.update({k: (x, y, 5.9) for k, (x, y) in CHS.items()})
top["GW"] = (GW[0] + 1.8, GW[1] + 1.2, 9.9)
EDGES = [("G1", "C1"), ("G2", "C2"), ("G3", "C2"), ("C2", "C1"), ("C3", "C1"), ("C1", "GW"), ("C3", "GW")]
for a, b in EDGES:
    D.link(f"L_{a}{b}", top[a], top[b], tok="holo" if a[0] == "G" else "blue2", arc=3.4, r=0.09)

# paket normal berkala (pull): tiap GLD -> CH -> GW
ROUTE = {"G1": ["G1", "C1", "GW"], "G2": ["G2", "C2", "C1", "GW"], "G3": ["G3", "C2", "C1", "GW"]}
f = ht.sec(0.8)
n = 0
for rep in range(2):
    for g, route in ROUTE.items():
        t0 = f + rep * 75 + n * 10
        for i in range(len(route) - 1):
            D.hop(f"Pk{rep}{g}{i}", top[route[i]], top[route[i + 1]], t0 + i * 18, 18, tok="ice", arc=3.4, size=0.25)
        n += 1
    n = 0

# kebocoran di dekat GLD-1
T_LEAK = ht.sec(6.0)
T_ALARM = ht.sec(7.2)
leak = (GLDS["G1"][0] + 1.2, GLDS["G1"][1] + 2.4, 1.2)
blobs, pm = R.plume("Plume", leak, n=20, wind=(-0.2, -1.0, 0.15), length=4.5, f_start=T_LEAK, frames=N, tok="amber")
ht.keyv(pm, "Vis", [(1, 0.0), (T_LEAK, 0.0), (T_LEAK + 20, 0.9)])
ht.keyin(leds["G1"], "Emit", "Color", [(1, ht.col("ok")), (T_ALARM - 1, ht.col("ok")), (T_ALARM, ht.col("alarm"))], interp="CONSTANT")
ht.keyin(leds["G1"], "Emit", "Strength", [(T_ALARM, 6.0), (T_ALARM + 6, 30.0), (T_ALARM + 12, 6.0), (T_ALARM + 18, 30.0), (T_ALARM + 24, 8.0), (T_ALARM + 30, 30.0)])
beac, bmat = ht.beacon("Alarm", (*GLDS["G1"], 0), "alarm", r=0.9, h=18)
ht.keyv(bmat, "Amp", [(1, 0.0), (T_ALARM, 0.0), (T_ALARM + 12, 1.0)])
ring_m = ht.pulse("AlarmRingM", "alarm", rate=1.6, base=0.5, amp=5.0, waves=1.0, sharp=3, hide=True)
ar = ht.ring("AlarmRing", (*GLDS["G1"], 0.05), 3.0, 0.08, ring_m, seg=96)
ht.keyv(ring_m, "Amp", [(1, 0.0), (T_ALARM, 0.0), (T_ALARM + 8, 1.0)])
ht.key(ar, "scale", [(T_ALARM, (0.3, 0.3, 1)), (T_ALARM + 30, (1.6, 1.6, 1)), (T_ALARM + 31, (0.3, 0.3, 1)), (T_ALARM + 60, (1.6, 1.6, 1)), (T_ALARM + 61, (0.3, 0.3, 1)), (N, (1.6, 1.6, 1))], interp="LINEAR")
# paket alarm (push), cepat, berulang
for rep in range(3):
    t0 = T_ALARM + 6 + rep * 22
    for i, (a, b) in enumerate((("G1", "C1"), ("C1", "GW"))):
        D.hop(f"Al{rep}{i}", top[a], top[b], t0 + i * 9, 9, tok="alarm", arc=3.4, size=0.42)
gwin = bpy.data.materials["GW_WinM"]
ht.keyin(gwin, "Emit", "Color", [(1, ht.col("holo2")), (T_ALARM + 24, ht.col("holo2")), (T_ALARM + 25, ht.col("alarm"))], interp="CONSTANT")
ht.keyin(gwin, "Emit", "Strength", [(T_ALARM + 24, 2.0), (T_ALARM + 30, 6.0)])

ht.dust(center=(-2, -12, 6), extent=(70, 50, 14), n=600)
cam, tgt = ht.camera((30, -52, 26), (-2, -12, 3), lens=28)
ht.key(cam, "location", [(1, (34, -54, 28)), (T_LEAK, (20, -48, 22)), (N, (14, -34, 13))])
ht.key(tgt, "location", [(1, (-2, -14, 3)), (T_LEAK, (0, -14, 3)), (N, (3, -12, 2.5))])
ht.render()
