"""Perangkat bergaya digital twin: node GLD, Cluster Head, Gateway, kamera OGI pan-tilt + kerucut pandang,
penanda lokasi (cincin), dan paket data LoRa yang melompat antar node. Satuan meter, tanpa merek/logo."""

from __future__ import annotations

import math

import bpy
from mathutils import Vector

import ht


def _m(key, **kw):
    name = "Dv_" + key
    return bpy.data.materials.get(name) or ht.twin(name, **kw)


def marker(name, loc, tok="holo", r=1.0, rate=0.6):
    """Cincin penanda di lantai + cincin luar putus-putus (lokasi perangkat terbaca dari udara)."""
    m = ht.pulse(name + "M", tok, rate=rate, base=0.8, amp=3.0, waves=1.0, sharp=5)
    a = ht.ring(name + "_R1", (loc[0], loc[1], 0.03), r * 0.55, 0.03 * r, m, seg=64)
    b = ht.ring(name + "_R2", (loc[0], loc[1], 0.03), r, 0.02 * r, m, seg=96, dash=6)
    return [a, b], m


def gld(name, loc, mount_h=1.0, scale=1.0, status_tok="ok"):
    """Node GLD: tiang pendek, badan die-cast (silinder + leher + tutup), antena atas, LED status."""
    x, y, z = loc
    s = scale
    body = _m("gld_body", body="blue", rim="holo2", rim_s=1.6, scan=False, rough=0.35)
    steel = _m("gld_steel", body="steel", rim="holo", rim_s=1.0, scan=False)
    cap = _m("gld_cap", body="body2", rim="holo", rim_s=1.8, scan=False)
    root = ht.empty(name, loc)
    parts = [
        ht.cyl(name + "_Pole", (0, 0, mount_h / 2), 0.03 * s, mount_h, steel, seg=12),
        ht.box(name + "_Plate", (0, 0.02 * s, mount_h + 0.05 * s), (0.18 * s, 0.01 * s, 0.18 * s), steel),
        ht.cyl(name + "_Body", (0, -0.06 * s, mount_h + 0.11 * s), 0.11 * s, 0.13 * s, body, axis="Y", seg=36),
        ht.cyl(name + "_Neck", (0, -0.17 * s, mount_h + 0.11 * s), 0.07 * s, 0.08 * s, body, axis="Y", seg=32),
        ht.cyl(name + "_Cap", (0, -0.23 * s, mount_h + 0.11 * s), 0.078 * s, 0.05 * s, cap, axis="Y", seg=32),
        ht.cyl(name + "_Ant", (0, -0.06 * s, mount_h + 0.32 * s), 0.008 * s, 0.32 * s, steel, seg=8),
    ]
    led = ht.emit(name + "_LedM", status_tok, 6.0)
    parts.append(ht.sphere(name + "_Led", (0.1 * s, -0.08 * s, mount_h + 0.2 * s), 0.025 * s, led, sub=2))
    ht.parent(parts, root)
    return root, led


def ch(name, loc, h=4.0):
    """Cluster Head: tiang 4 m, kotak elektronik, panel surya miring, antena."""
    steel = _m("ch_steel", body="steel", rim="holo", rim_s=1.0, scan=False)
    boxm = _m("ch_box", body="body2", rim="holo2", rim_s=1.6, scan=False)
    pv = ht.glossy("Dv_pv", "#0b2a5c", rough=0.15, metal=0.3, glow=0.25, glow_tok="blue")
    root = ht.empty(name, loc)
    parts = [
        ht.cyl(name + "_Pole", (0, 0, h / 2), 0.05, h, steel, seg=12),
        ht.box(name + "_Box", (0, -0.12, h * 0.62), (0.32, 0.16, 0.4), boxm),
        ht.cyl(name + "_Ant", (0, 0, h + 0.45), 0.012, 0.9, steel, seg=8),
    ]
    p = ht.box(name + "_PV", (0, 0.05, h - 0.2), (0.9, 0.04, 0.6), pv)
    p.rotation_euler = (math.radians(-35), 0, 0)
    parts.append(p)
    led = ht.emit(name + "_LedM", "holo", 5.0)
    parts.append(ht.sphere(name + "_Led", (0, -0.21, h * 0.62 + 0.12), 0.03, led, sub=2))
    ht.parent(parts, root)
    return root, led


def gateway(name, loc):
    """Gateway: ruang kontrol kecil + mast antena 6 m."""
    bm = _m("gw_bld", body="body2", rim="blue2", rim_s=1.3)
    steel = _m("ch_steel", body="steel", rim="holo", rim_s=1.0, scan=False)
    root = ht.empty(name, loc)
    b = ht.box(name + "_Bld", (0, 0, 1.6), (5.0, 3.6, 3.2), bm)
    win = ht.emit(name + "_WinM", "holo2", 2.0)
    mb = ht.MB()
    for i in range(4):
        x = -1.8 + i * 1.2
        mb.poly([(x - 0.4, -1.81, 1.4), (x + 0.4, -1.81, 1.4), (x + 0.4, -1.81, 2.4), (x - 0.4, -1.81, 2.4)])
    w = mb.finish(name + "_Win", [win])
    mast = ht.cyl(name + "_Mast", (1.8, 1.2, 3.2 + 3.0), 0.06, 6.0, steel, seg=10)
    ant = ht.cyl(name + "_Ant", (1.8, 1.2, 9.6), 0.02, 0.9, steel, seg=8)
    ht.parent([b, w, mast, ant], root)
    return root


def ogi_camera(name, loc, pole_h=10.0):
    """Kamera OGI pan-tilt di tiang. Kembalikan (root, pan, tilt): pan = rotasi Z, tilt = rotasi X."""
    steel = _m("ogi_steel", body="steel", rim="holo", rim_s=1.0, scan=False)
    house = _m("ogi_house", body="#d8dee8", rim="holo2", rim_s=1.2, scan=False, rough=0.3)
    dark = _m("ogi_dark", body="body", rim="holo", rim_s=1.5, scan=False)
    root = ht.empty(name, loc)
    pole = ht.cyl(name + "_Pole", (0, 0, pole_h / 2), 0.14, pole_h, steel, seg=16)
    arm = ht.box(name + "_Arm", (0, 0, pole_h + 0.15), (0.5, 0.5, 0.3), steel)
    pole.parent = arm.parent = root
    pan = ht.empty(name + "_Pan", (0, 0, pole_h + 0.3))
    pan.parent = root
    yoke = ht.box(name + "_Yoke", (0, 0, 0.25), (0.75, 0.3, 0.5), dark)
    yoke.parent = pan
    tilt = ht.empty(name + "_Tilt", (0, 0, 0.55))
    tilt.parent = pan
    parts = [
        ht.box(name + "_House", (0, 0.05, 0), (0.42, 0.95, 0.4), house, bevel=0.03),
        ht.cyl(name + "_Hood", (0, -0.5, 0), 0.16, 0.18, dark, axis="Y", seg=32),
        ht.cyl(name + "_Lens", (0, -0.6, 0), 0.12, 0.03, ht.glass("Dv_lens", "holo", 0.5, 1.2), axis="Y", seg=32),
        ht.box(name + "_Cool", (0, 0.62, 0), (0.3, 0.25, 0.32), dark),
    ]
    ht.parent(parts, tilt)
    return root, pan, tilt


def frustum(name, parent, length=60.0, half_w=12.0, half_h=6.0, origin=(0, -0.62, 0)):
    """Kerucut pandang (piramida) dari lensa ke depan (-Y lokal). Material: Value 'Alert' 0 biru -> 1 amber,
    'Vis' = keterlihatan. Tepi piramida diberi garis lebih terang."""
    m, nt, out = ht._new(name + "M")
    g = ht._G(nt)
    a = nt.nodes.new("ShaderNodeAttribute"); a.attribute_name = "phase"; a.attribute_type = "GEOMETRY"
    t = ht.time_node(m)
    alert = g.val("Alert", 0.0)
    vis = g.val("Vis", 1.0)
    c = g.mixc(alert, ht.col("holo"), ht.col("amber"))
    # gelombang pindai menjalar dari lensa ke ujung
    wave = g.op("POWER", g.op("SUBTRACT", 1.0, g.op("FRACT", g.op("SUBTRACT", g.op("MULTIPLY", t.outputs[0], 0.7), a.outputs["Fac"]))), 14.0)
    fade = g.op("SUBTRACT", 1.0, g.op("POWER", a.outputs["Fac"], 1.5))
    alpha = g.op("MULTIPLY", g.op("MULTIPLY", g.op("ADD", 0.14, g.op("MULTIPLY", wave, 0.35)), fade), vis)
    e = nt.nodes.new("ShaderNodeEmission")
    g.L.new(c, e.inputs["Color"])
    g.L.new(g.op("MULTIPLY", g.op("ADD", 0.8, g.op("MULTIPLY", wave, 3.0)), fade), e.inputs["Strength"])
    tr = nt.nodes.new("ShaderNodeBsdfTransparent")
    mx = nt.nodes.new("ShaderNodeMixShader")
    g.L.new(alpha, mx.inputs["Fac"]); g.L.new(tr.outputs[0], mx.inputs[1]); g.L.new(e.outputs[0], mx.inputs[2])
    g.L.new(mx.outputs[0], out.inputs["Surface"])
    ht.blended(m)
    O = Vector(origin)
    corners = [Vector((sx * half_w, -length, sz * half_h)) + O for sx, sz in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
    mb = ht.MB()
    S = 20
    for k in range(4):
        c0, c1 = corners[k], corners[(k + 1) % 4]
        for j in range(S):
            u0, u1 = j / S, (j + 1) / S
            mb.poly([O.lerp(c0, u0), O.lerp(c1, u0), O.lerp(c1, u1), O.lerp(c0, u1)], 0, u0)
    fr = mb.finish(name, [m])
    fr.parent = parent
    # garis tepi
    em, ent, eout = ht._new(name + "EdgeM")
    eg = ht._G(ent)
    al2 = eg.val("Alert", 0.0)
    vis2 = eg.val("Vis", 1.0)
    ee = ent.nodes.new("ShaderNodeEmission")
    eg.L.new(eg.mixc(al2, ht.col("holo"), ht.col("amber")), ee.inputs["Color"])
    eg.L.new(eg.op("MULTIPLY", vis2, 2.5), ee.inputs["Strength"])
    tr2 = ent.nodes.new("ShaderNodeBsdfTransparent")
    mx2 = ent.nodes.new("ShaderNodeMixShader")
    eg.L.new(vis2, mx2.inputs["Fac"]); eg.L.new(tr2.outputs[0], mx2.inputs[1]); eg.L.new(ee.outputs[0], mx2.inputs[2])
    eg.L.new(mx2.outputs[0], eout.inputs["Surface"])
    ht.blended(em)
    edges = []
    for k, cc in enumerate(corners):
        o = ht.tube(f"{name}_E{k}", [O, cc], 0.03, em, seg=5, smooth_path=False)
        o.parent = parent
        edges.append(o)
    return fr, m, em


def hop(name, a, b, f0, dur, tok="holo", arc=1.5, size=0.18):
    """Paket data: bola bercahaya yang melompat dari a ke b (lengkung) pada frame f0..f0+dur, plus jejak."""
    m = ht.emit(name + "M", tok, 8.0)
    p = ht.sphere(name, a, size, m, sub=2)
    A_, B_ = Vector(a), Vector(b)
    keys = []
    for i in range(7):
        u = i / 6
        q = A_.lerp(B_, u) + Vector((0, 0, arc * 4 * u * (1 - u)))
        keys.append((f0 + int(dur * u), tuple(q)))
    ht.key(p, "location", keys, interp="LINEAR")
    ht.show([p], f0, f0 + dur + 1)
    return p


def link(name, a, b, tok="holo", arc=1.2, r=0.035, rate=0.8):
    """Tautan mesh: tabung lengkung tipis dengan denyut menjalar dari a ke b. Value 'Amp' 0 = mati."""
    m = ht.pulse(name + "M", tok, rate=rate, base=0.5, amp=5.0, waves=2.0, sharp=10, hide=True)
    A_, B_ = Vector(a), Vector(b)
    mid = (A_ + B_) / 2 + Vector((0, 0, arc))
    o = ht.tube(name, [A_, A_.lerp(mid, 0.5) + Vector((0, 0, arc * 0.25)), mid, mid.lerp(B_, 0.5) + Vector((0, 0, arc * 0.25)), B_], r, m, seg=6)
    return o, m
