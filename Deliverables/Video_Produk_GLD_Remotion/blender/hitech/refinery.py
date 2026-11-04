"""Kilang 'digital twin' generik (tanpa merek/data klien) untuk shot high-tech.

Tata letak (meter, origin di tengah unit proses):
  - jalur pipe rack utama sepanjang sumbu X di y = 0 (tinggi 5 m, 3 tingkat pipa)
  - kolom distilasi di utara rack (y > 0), tangki bola & tangki timbun di selatan (y < 0)
  - flare stack di pojok timur laut; manifold + klaster valve di sekitar LEAK (titik bocor demo)
Setiap material bisa diberi mode thermal (ht.thermal_mix) agar sapuan kamera OGI mengubah tampilan.
"""

from __future__ import annotations

import math
import random

import bpy
from mathutils import Vector

import ht

LEAK = (6.0, -1.2, 2.4)          # flange bocor di manifold (dekat rack)
MANIFOLD = (6.0, -2.4)
VALVES = (-9.0, -2.6)
RACK_Y, RACK_H = 0.0, 5.0

_rnd = random.Random(11)


class Plant:
    def __init__(self, thermal=False):
        self.thermal = thermal
        self.mats = {}
        self.objs = []
        self.hot = []  # objek panas (temp tinggi)

    def mat(self, key, body="body", rim="holo", rim_s=2.0, temp=None):
        if key not in self.mats:
            m = ht.twin("Tw_" + key, body=body, rim=rim, rim_s=rim_s)
            if self.thermal:
                ht.thermal_mix(m)
            self.mats[key] = m
        return self.mats[key]

    def add(self, o, temp=0.35, edge=True, edge_tok="holo", edge_s=1.2, thick=0.02, angle=35):
        ht.set_temp(o, temp)
        self.objs.append(o)
        if edge:
            em = self.mats.get("_edge_" + edge_tok)
            if em is None:
                em = ht.emit("Edge_" + edge_tok, edge_tok, edge_s)
                if self.thermal:
                    ht.thermal_mix(em)
                self.mats["_edge_" + edge_tok] = em
            e = ht.edges(o, thick=thick, angle=angle, mat=em)
            ht.set_temp(e, temp)
            self.objs.append(e)
        return o


def column(P, name, x, y, r, h, temp=0.55):
    m = P.mat("col", body="body", rim="holo", rim_s=2.4)
    body = P.add(ht.cyl(name, (x, y, h / 2), r, h, m, seg=40), temp)
    dome = P.add(ht.sphere(name + "_Dome", (x, y, h), r, m, sub=3, scale=(1, 1, 0.45)), temp, edge=False)
    band = P.mats.get("band")
    if band is None:
        band = ht.emit("Band", "holo", 1.6)
        if P.thermal:
            ht.thermal_mix(band)
        P.mats["band"] = band
    for k in range(1, int(h // 4) + 1):  # platform melingkar
        z = k * 4.0
        o = ht.ring(f"{name}_Plat{k}", (x, y, z), r + 0.45, 0.06, band, seg=64)
        ht.set_temp(o, temp - 0.1)
        P.objs.append(o)
    # saluran samping (overhead line) ke rack
    pm = P.mat("pipe", body="body2", rim="holo2", rim_s=1.6)
    o = P.add(ht.tube(name + "_OH", [(x, y, h * 0.9), (x, y - r - 0.8, h * 0.88), (x, (y + RACK_Y) / 2, (h * 0.9 + RACK_H) / 2), (x, RACK_Y + 0.5, RACK_H + 1.6)], 0.18, pm, seg=10), temp, edge=False)
    return body


def sphere_tank(P, name, x, y, r, temp=0.3):
    m = P.mat("sph", body="body", rim="blue2", rim_s=2.2)
    s = P.add(ht.uvsphere(name, (x, y, r + 1.4), r, m, seg=40, rings=20), temp, edge=False)
    sm = P.mat("steel", body="steel", rim="holo", rim_s=1.0)
    for k in range(8):
        a = 2 * math.pi * k / 8
        P.add(ht.cyl(f"{name}_Leg{k}", (x + math.cos(a) * r * 0.82, y + math.sin(a) * r * 0.82, (r + 1.4) / 2), 0.12, r + 1.4, sm, seg=8, smooth=False), temp - 0.1, edge=False)
    band = P.mats["band"] if "band" in P.mats else ht.emit("Band", "holo", 1.6)
    o = ht.ring(name + "_Eq", (x, y, r + 1.4), r + 0.03, 0.05, band, seg=96)
    ht.set_temp(o, temp)
    P.objs.append(o)
    return s


def storage_tank(P, name, x, y, r, h, temp=0.28):
    m = P.mat("tank", body="body", rim="holo", rim_s=1.8)
    t = P.add(ht.cyl(name, (x, y, h / 2), r, h, m, seg=56), temp)
    P.add(ht.cyl(name + "_Roof", (x, y, h + 0.6), r, 1.2, m, seg=56, r2=0.6), temp, edge=False)
    return t


def pipe_rack(P, x0=-26.0, x1=26.0, temp=0.42):
    sm = P.mat("steel", body="steel", rim="holo", rim_s=1.0)
    n = int((x1 - x0) // 6)
    for i in range(n + 1):
        x = x0 + i * (x1 - x0) / n
        for dy in (-1.6, 1.6):
            P.add(ht.box(f"Rk_Col{i}_{dy}", (x, RACK_Y + dy, RACK_H / 2), (0.3, 0.3, RACK_H), sm), temp - 0.15, thick=0.015)
        for z in (2.6, RACK_H):
            P.add(ht.box(f"Rk_Beam{i}_{z}", (x, RACK_Y, z), (0.25, 3.5, 0.25), sm), temp - 0.15, edge=False)
    pm = P.mat("pipe", body="body2", rim="holo2", rim_s=1.6)
    hotm = P.mat("pipehot", body="body2", rim="amber", rim_s=1.4)
    k = 0
    for z in (2.85, RACK_H + 0.3):
        for j, dy in enumerate((-1.2, -0.6, 0.0, 0.6, 1.2)):
            r = 0.16 + 0.08 * ((j + k) % 3 == 0)
            hot = (k % 4 == 1)
            o = P.add(ht.cyl(f"Rk_Pipe{k}", ((x0 + x1) / 2, RACK_Y + dy, z + r), r, x1 - x0, hotm if hot else pm, axis="X", seg=16), 0.62 if hot else 0.4, edge=False)
            if hot:
                P.hot.append(o)
            k += 1
    # aliran (garis data berdenyut) di atas pipa paling atas
    flow = ht.pulse("RackFlow", "holo", rate=0.25, base=0.15, amp=4.0, waves=6.0, sharp=12)
    if P.thermal:
        ht.thermal_mix(flow)
    for dy in (-0.6, 0.6):
        mb = ht.MB()
        N = 160
        for s in range(N):
            xa = x0 + (x1 - x0) * s / N
            xb = x0 + (x1 - x0) * (s + 0.8) / N
            z = RACK_H + 0.3 + 0.42
            mb.poly([(xa, RACK_Y + dy - 0.03, z), (xb, RACK_Y + dy - 0.03, z), (xb, RACK_Y + dy + 0.03, z), (xa, RACK_Y + dy + 0.03, z)], 0, s / N)
        o = mb.finish(f"RackFlow{dy}", [flow])
        ht.set_temp(o, 0.5)
        P.objs.append(o)


def manifold(P, temp=0.5):
    """Manifold + flange bocor (LEAK) di bawah rack."""
    mx, my = MANIFOLD
    pm = P.mat("pipe", body="body2", rim="holo2", rim_s=1.6)
    sm = P.mat("steel", body="steel", rim="holo", rim_s=1.0)
    P.add(ht.cyl("Man_Header", (mx, my, 1.2), 0.32, 7.0, pm, axis="X", seg=24), temp, edge=False)
    for i in range(5):
        x = mx - 2.8 + i * 1.4
        P.add(ht.cyl(f"Man_Riser{i}", (x, my, 1.2 + 0.85), 0.14, 1.7, pm, seg=14), temp, edge=False)
        P.add(ht.cyl(f"Man_Valve{i}", (x, my, 2.2), 0.26, 0.32, sm, axis="Y", seg=20), temp - 0.05)
        P.add(ht.cyl(f"Man_Wheel{i}", (x, my - 0.34, 2.2), 0.24, 0.04, sm, axis="Y", seg=20), temp - 0.05, edge=False)
        P.add(ht.cyl(f"Man_Up{i}", (x, my + 0.4, 2.4), 0.12, 1.0, pm, axis="Y", seg=12), temp, edge=False)
    # flange bocor: sedikit lebih hangat
    fl = P.add(ht.cyl("Leak_Flange", LEAK, 0.3, 0.16, sm, axis="Y", seg=24), temp + 0.05)
    for i in range(3):
        P.add(ht.box(f"Man_Support{i}", (mx - 2.5 + i * 2.5, my, 0.5), (0.25, 0.4, 1.0), sm), temp - 0.15, edge=False)
    return fl


def valve_cluster(P, temp=0.45):
    vx, vy = VALVES
    pm = P.mat("pipe", body="body2", rim="holo2", rim_s=1.6)
    sm = P.mat("steel", body="steel", rim="holo", rim_s=1.0)
    for i in range(3):
        for j in range(2):
            x, y = vx - 2 + i * 2, vy - j * 1.6
            P.add(ht.cyl(f"Vc_P{i}{j}", (x, y, 1.0), 0.18, 2.0, pm, seg=14), temp, edge=False)
            P.add(ht.box(f"Vc_B{i}{j}", (x, y, 1.6), (0.5, 0.5, 0.5), sm), temp)
            P.add(ht.cyl(f"Vc_W{i}{j}", (x, y, 2.05), 0.28, 0.05, sm, seg=20), temp, edge=False)


def flare(P, x=24.0, y=14.0, h=26.0):
    sm = P.mat("steel", body="steel", rim="holo", rim_s=1.0)
    P.add(ht.cyl("Flare", (x, y, h / 2), 0.5, h, sm, seg=20), 0.5)
    fm = ht.pulse("FlareM", "amber", rate=2.5, base=3.0, amp=4.0, waves=2.0, sharp=2)
    if P.thermal:
        ht.thermal_mix(fm)
    o = ht.sphere("Flare_Fire", (x, y, h + 0.8), 0.9, fm, sub=2, scale=(0.7, 0.7, 1.6))
    ht.set_temp(o, 1.0)
    P.objs.append(o)
    P.hot.append(o)
    ht.point("FlareL", (x, y, h + 1.5), 3500, (1.0, 0.6, 0.25), 1.0)


def exchangers(P):
    m = P.mat("hx", body="body", rim="holo", rim_s=1.6)
    for i in range(4):
        x = -18 + i * 3.2
        P.add(ht.cyl(f"HX{i}", (x, -7.5, 1.3), 0.7, 4.2, m, axis="Y", seg=28), 0.5 if i % 2 else 0.4)
        P.add(ht.box(f"HX_S{i}", (x, -7.5, 0.3), (1.0, 3.0, 0.6), P.mat("steel", body="steel")), 0.3, edge=False)


def ground_props(P):
    """Bangunan kecil & kontainer di pinggir (memberi skala)."""
    m = P.mat("bld", body="body2", rim="blue2", rim_s=1.2)
    for i, (x, y, w, d, h) in enumerate(((-30, 14, 8, 6, 5), (30, -14, 6, 5, 4), (-32, -16, 10, 6, 6), (14, 18, 6, 4, 3.5))):
        P.add(ht.box(f"Bld{i}", (x, y, h / 2), (w, d, h), m), 0.3, thick=0.03)


def build(thermal=False, flare_on=True):
    P = Plant(thermal)
    pipe_rack(P)
    column(P, "ColA", -6.0, 7.5, 1.5, 30.0, temp=0.6)
    column(P, "ColB", 1.5, 8.5, 1.1, 22.0, temp=0.55)
    column(P, "ColC", 8.0, 7.0, 0.9, 16.0, temp=0.5)
    column(P, "ColD", -14.0, 8.0, 1.0, 18.0, temp=0.45)
    sphere_tank(P, "SphA", 14.0, -9.0, 3.4)
    sphere_tank(P, "SphB", 22.5, -9.0, 3.4)
    storage_tank(P, "TkA", -24.0, -10.0, 5.0, 8.0)
    storage_tank(P, "TkB", -24.0, 6.0, 4.0, 7.0)
    manifold(P)
    valve_cluster(P)
    exchangers(P)
    ground_props(P)
    if flare_on:
        flare(P)
    return P


def plume(name, origin, n=26, wind=(1.0, -0.15, 0.25), length=6.0, seed=3, tok="t4", f_start=1, frames=300):
    """Plume gas: gumpalan noise transparan yang memanjang mengikuti angin dari titik bocor.
    Value 'Vis' (material) mengatur tampak/tidak (gas tak kasatmata di mata telanjang)."""
    rnd = random.Random(seed)
    m, nt, out = ht._new(name + "M")
    g = ht._G(nt)
    t = ht.time_node(m)
    tc = nt.nodes.new("ShaderNodeTexCoord")
    mp = nt.nodes.new("ShaderNodeMapping")
    g.L.new(tc.outputs["Object"], mp.inputs["Vector"])
    comb = nt.nodes.new("ShaderNodeCombineXYZ")
    g.L.new(g.op("MULTIPLY", t.outputs[0], -0.6), comb.inputs["X"])
    g.L.new(comb.outputs[0], mp.inputs["Location"])
    nz = nt.nodes.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = 2.2; nz.inputs["Detail"].default_value = 4
    g.L.new(mp.outputs["Vector"], nz.inputs["Vector"])
    lw = nt.nodes.new("ShaderNodeLayerWeight"); lw.inputs["Blend"].default_value = 0.6
    core = g.op("SUBTRACT", 1.0, lw.outputs["Facing"])
    dens = g.op("MULTIPLY", g.op("POWER", core, 1.6), g.op("MULTIPLY_ADD", nz.outputs["Fac"], 1.6, -0.35), clamp=True)
    vis = g.val("Vis", 0.0)
    alpha = g.op("MULTIPLY", g.op("MULTIPLY", dens, vis), 0.55, clamp=True)
    e = nt.nodes.new("ShaderNodeEmission"); e.inputs["Color"].default_value = ht.col(tok)
    g.L.new(g.op("MULTIPLY", dens, 2.2), e.inputs["Strength"])
    tr = nt.nodes.new("ShaderNodeBsdfTransparent")
    mx = nt.nodes.new("ShaderNodeMixShader")
    g.L.new(alpha, mx.inputs["Fac"]); g.L.new(tr.outputs[0], mx.inputs[1]); g.L.new(e.outputs[0], mx.inputs[2])
    g.L.new(mx.outputs[0], out.inputs["Surface"])
    ht.blended(m)
    W = Vector(wind).normalized()
    O = Vector(origin)
    blobs = []
    for i in range(n):
        u = i / (n - 1)
        s = 0.25 + 1.4 * u
        p = O + W * (length * u) + Vector((rnd.uniform(-0.3, 0.3), rnd.uniform(-0.3, 0.3), rnd.uniform(-0.1, 0.4))) * (0.4 + u)
        b = ht.sphere(f"{name}_{i}", p, s, m, sub=2, scale=(1.3, 1.0, 0.9))
        b.rotation_euler = (rnd.random() * 3, rnd.random() * 3, rnd.random() * 3)
        # menjalar: tiap gumpalan tumbuh dari kecil saat plume terbentuk + bergerak pelan searah angin
        f0 = f_start + int(u * 45)
        ht.key(b, "scale", [(1, (0.01, 0.01, 0.01)), (f0, (0.01, 0.01, 0.01)), (f0 + 25, (1.3, 1.0, 0.9))])
        ht.key(b, "location", [(f0, p), (frames, p + W * (0.6 + 1.2 * u) + Vector((0, 0, 0.5 * u)))], interp="LINEAR")
        blobs.append(b)
    return blobs, m
