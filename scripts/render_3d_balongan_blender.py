# -*- coding: utf-8 -*-
"""Render 3D rencana instalasi GLD RU VI Balongan di atas citra peta (Blender Workbench, mode background).

Dua pass (ukuran perangkat dibesarkan untuk tampilan lebar, skala nyata untuk detail):
  blender -b -P scripts/render_3d_balongan_blender.py -- wide
  blender -b -P scripts/render_3d_balongan_blender.py -- detail
Output: scripts/assets/rab_balongan/render3d_<view>.png + render3d_pts_<pass>.json (proyeksi titik bernama)
"""
import json
import math
import os
import sys

import bpy
from bpy_extras.object_utils import world_to_camera_view
from mathutils import Vector

PASS = sys.argv[sys.argv.index("--") + 1] if "--" in sys.argv else "wide"
HERE = os.path.dirname(os.path.abspath(__file__))
RB = os.path.join(HERE, "assets", "rab_balongan")
MAP = os.path.join(RB, "peta_lokasi_balongan_26nov_crop2.png")
BOX = (560, 40, 1480, 800)   # crop piksel citra peta (diperluas: deret vessel & 2 kolom tinggi)
BOX0 = (760, 120)            # acuan piksel poligon lama
PPM = 5.8                    # px per meter — dikalibrasi ulang dari ukur Google Maps: CH-01→CH-02 ±20 m, CH-02→GW ±91 m (total 111,3 m)
S = 5.0 if PASS == "wide" else 1.0   # pembesaran ukuran perangkat (tinggi tiang selalu nyata)
ROOF = 4.0                   # asumsi tinggi atap kantor
CH1_H, CH2_H, GLD_H, JB_H = 1.5, 6.0, 1.0, 1.0


def w(px, py, z=0.0):
    return Vector(((px - BOX[0]) / PPM, (BOX[3] - py) / PPM, z))


P = {"GLD-01": w(1125, 195), "GLD-02": w(1210, 295), "CH-01": w(1167, 245), "CH-02": w(1332, 330),   # GLD: titik hijau peta user 27 Nov
     "JB": w(1160, 258), "GW-01": w(936, 680)}
NP = {}  # titik bernama untuk label/dimensi

# ------------------------------------------------------------------ scene
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.engine = "BLENDER_WORKBENCH"
sh = sc.display.shading
sh.light = "FLAT"; sh.color_type = "TEXTURE"
sh.show_shadows = True; sh.shadow_intensity = 0.3
sh.show_cavity = True; sh.show_object_outline = True; sh.object_outline_color = (0.0, 0.0, 0.0)
sh.background_type = "WORLD"
sc.display.render_aa = "8"
sc.render.resolution_x, sc.render.resolution_y = 2200, 1400
world = bpy.data.worlds.new("W"); sc.world = world
world.color = (0.86, 0.9, 0.96)
sc.view_settings.view_transform = "Standard"


def mat(name, rgb, alpha=1.0):
    m = bpy.data.materials.new(name); m.use_nodes = True
    m.diffuse_color = (*rgb, alpha)
    m.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (*rgb, 1)
    return m


M = {"pole": mat("pole", (0.55, 0.57, 0.6)), "gld": mat("gld", (1.0, 0.45, 0.0)),
     "ch": mat("ch", (0.45, 0.12, 0.85)), "gw": mat("gw", (0.0, 0.75, 0.55)),
     "jb": mat("jb", (0.25, 0.27, 0.3)), "ant": mat("ant", (0.02, 0.02, 0.02)),
     "pv": mat("pv", (0.02, 0.15, 0.6)), "cable": mat("cable", (0.95, 0.0, 0.0)),
     "lora": mat("lora", (0.0, 0.35, 1.0)), "steel": mat("steel", (0.32, 0.34, 0.38)),
     "bldg": mat("bldg", (0.93, 0.88, 0.72)), "conc": mat("conc", (0.7, 0.7, 0.68)),
     "gland": mat("gland", (0.85, 0.7, 0.3))}


def add(o, m):
    o.data.materials.append(m)
    return o


def cyl(p, r, h, m, verts=24):
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=r, depth=h, location=(p.x, p.y, p.z + h / 2))
    return add(bpy.context.object, m)


def cube(p, sx, sy, sz, m, rot=(0, 0, 0)):
    """p = titik tengah bawah."""
    bpy.ops.mesh.primitive_cube_add(size=1, location=(p.x, p.y, p.z + sz / 2), rotation=rot)
    o = bpy.context.object; o.scale = (sx, sy, sz)
    return add(o, m)


def tube(points, r, m):
    cu = bpy.data.curves.new("c", "CURVE"); cu.dimensions = "3D"
    cu.bevel_depth = r; cu.bevel_resolution = 2
    sp = cu.splines.new("POLY"); sp.points.add(len(points) - 1)
    for i, q in enumerate(points):
        sp.points[i].co = (q.x, q.y, q.z, 1)
    o = bpy.data.objects.new("c", cu); sc.collection.objects.link(o)
    o.data.materials.append(m)
    return o


def arc(a, b, lift):
    n = max(24, int((a - b).length * 1.2))
    pts = []
    for i in range(n + 1):
        t = i / n
        q = a.lerp(b, t); q.z += lift * 4 * t * (1 - t)
        pts.append(q)
    return pts


# tanah bertekstur peta
W_, H_ = (BOX[2] - BOX[0]) / PPM, (BOX[3] - BOX[1]) / PPM
bpy.ops.mesh.primitive_plane_add(size=1, location=(W_ / 2, H_ / 2, 0))
g = bpy.context.object; g.scale = (W_, H_, 1)
gm = bpy.data.materials.new("map"); gm.use_nodes = True
nt = gm.node_tree; tex = nt.nodes.new("ShaderNodeTexImage"); tex.image = bpy.data.images.load(MAP)
nt.links.new(tex.outputs["Color"], nt.nodes["Principled BSDF"].inputs["Base Color"])
g.data.materials.append(gm)

TOP = {}
FACE = Vector((0, -1, 0))  # perangkat menghadap selatan (ke kamera)


def stanchion(p, h, name):
    cube(p, 0.24, 0.24, 0.01, M["steel"])            # pelat dasar 240×240×10
    cube(p, 0.4, 0.4, 0.05, M["conc"])               # pondasi/cor
    cyl(p + Vector((0, 0, 0.05)), 0.0302 * min(S, 2.5), h, M["pole"], 16)  # pipa 2" OD 60,3
    NP[name + ":base"] = p.copy()
    NP[name + ":top"] = p + Vector((0, 0, h))


# ---- model 3D GLD & CH dari video produk (Deliverables/Video_Produk_GLD_Remotion/blender/leak_landscape.blend)
VIDEO_BLEND = os.path.join(os.path.dirname(HERE), "Deliverables", "Video_Produk_GLD_Remotion", "blender", "leak_landscape.blend")
with bpy.data.libraries.load(VIDEO_BLEND, link=False) as (src, dst):
    dst.collections = ["GLD_node", "CH_node"]
C_GLD = bpy.data.collections["GLD_node"]
C_CH = bpy.data.collections["CH_node"]           # tiang ±6 m + panel surya + kotak CH (tanah di z = −0,5)
C_CHBOX = bpy.data.collections.new("CH_box")     # kotak CH + antena saja (untuk CH-01 di bawah struktur)
for o in C_CH.all_objects:
    if o.name.split(".")[0].startswith(("ch_mount", "ch_case", "ch_lid", "ch_bottom", "ch_ntype", "ch_fiber", "ch_sma", "ch_gland")):
        C_CHBOX.objects.link(o)
C_CHBOX.instance_offset = (0, 0, 5.5)
C_SOLAR = bpy.data.collections.new("CH_solar")   # panel surya CH (lengan, klem, rangka, sel)
for o in C_CH.all_objects:
    if o.name.split(".")[0].startswith(("ch_solar_arm", "ch_solar_clamp", "ch_solar_frame", "ch_solar_cells")):
        C_SOLAR.objects.link(o)
C_SOLAR.instance_offset = (0, 0, 1.0)
C_GLDU = bpy.data.collections.new("GLD_unit")    # GLD + pelat U-bolt tanpa tiang/footing (untuk tampilan lebar)
for o in C_GLD.all_objects:
    if not o.name.split(".")[0].startswith(("pole", "cable_pole", "cable_clamp")):
        C_GLDU.objects.link(o)
for m in bpy.data.materials:                      # Workbench memakai diffuse_color
    if m.use_nodes and "Principled BSDF" in m.node_tree.nodes:
        bc = m.node_tree.nodes["Principled BSDF"].inputs["Base Color"]
        if not bc.is_linked:
            m.diffuse_color = bc.default_value
    if "solar_cells" in m.name:
        m.use_nodes = False
        m.diffuse_color = (0.04, 0.1, 0.35, 1)
    elif "solar_frame" in m.name or "galvanized" in m.name:
        m.use_nodes = False
        m.diffuse_color = (0.7, 0.72, 0.75, 1)


def inst(coll, loc, scale=1.0):
    o = bpy.data.objects.new(coll.name + "_inst", None)
    o.instance_type = "COLLECTION"; o.instance_collection = coll
    o.location = loc; o.scale = (scale, scale, scale)
    sc.collection.objects.link(o)
    return o


def gld(k):
    p = P[k]
    if S == 1.0:                                  # model video utuh: tiang ±0,95 m + footing + pelat U-bolt
        inst(C_GLD, p + Vector((0, 0, 0.5)))
        NP[k + ":base"] = p.copy(); NP[k + ":top"] = p + Vector((0, 0, 0.95))
        c = p + Vector((0, 0, 0.5))
    else:                                         # unit GLD (dibesarkan S×) di stanchion 1 m
        stanchion(p, GLD_H, k)
        c = p + Vector((0, -0.06 * S, GLD_H - 0.13 * S))
        inst(C_GLDU, c, S)
    TOP[k] = c + Vector((-0.028 * S, 0.02 * S, 0.256 * S))
    NP[k] = c + Vector((0, -0.05 * S, 0.02 * S))
    NP[k + ":gland"] = c + Vector((0, 0, -0.072 * S))


def ch(k, h, solar=False):
    p = P[k]
    if solar and S == 1.0:                        # model video utuh (tiang ±6 m + panel surya)
        inst(C_CH, p + Vector((0, 0, 0.5)))
        TOP[k] = p + Vector((0.014, 0, 7.27))
        NP[k] = p + Vector((0, 0, 6.09))
        NP[k + ":pv"] = p + Vector((0.2, -0.15, 1.6))
        NP[k + ":base"] = p.copy(); NP[k + ":top"] = p + Vector((0, 0, 6.0))
        return
    stanchion(p, h, k)
    sc_ = min(S, 2.5)
    inst(C_CHBOX, p + Vector((0, 0, h)), sc_)
    TOP[k] = p + Vector((0.014 * sc_, 0, h + 1.267 * sc_))
    NP[k] = p + Vector((0, 0, h + 0.09 * sc_))
    if solar:
        inst(C_SOLAR, p + Vector((0, 0, 1.5)), sc_)
        NP[k + ":pv"] = p + Vector((0.2 * sc_, -0.15 * sc_, 1.5 + 0.1 * sc_))


def structure(p, hx=14.0, hy=12.0, h=5.0):
    """Lantai dasar di bawah struktur WHB (foto survei 18 Nov): kolom beton persegi bersabuk hitam,
    girder baja & deck di atas. GLD-01, GLD-02, CH-01 berada di bawahnya; jarak kolom/tinggi = estimasi."""
    conc = mat("col_conc", (0.78, 0.8, 0.82)); band = mat("col_band", (0.08, 0.08, 0.08))
    deck = mat("deck", (0.55, 0.58, 0.62), 0.35); gird = mat("girder", (0.45, 0.48, 0.52))
    for dx in (-hx, 0, hx):
        for dy in (-hy, hy):
            c = p + Vector((dx, dy, 0))
            cube(c, 1.0, 1.0, 0.6, band)
            cube(c + Vector((0, 0, 0.6)), 1.0, 1.0, h - 0.6, conc)
    for dy in (-hy, hy):
        cube(p + Vector((0, dy, h)), 2 * hx + 1.0, 0.5, 0.8, gird)
    for dx in (-hx, -hx / 2, 0, hx / 2, hx):
        cube(p + Vector((dx, 0, h)), 0.5, 2 * hy + 1.0, 0.8, gird)
    cube(p + Vector((0, 0, h + 0.8)), 2 * hx + 1.0, 2 * hy + 1.0, 0.25, deck)
    NP["STRUCT"] = p + Vector((hx * 0.6, -hy, h + 0.9))
    # ---- bangunan WHB di atas lantai dasar (foto 17 Nov; tinggi/dimensi = estimasi visual)
    frame = mat("whb_frame", (0.36, 0.38, 0.42)); ins = mat("whb_ins", (0.86, 0.87, 0.89))
    casing = mat("whb_casing", (0.6, 0.62, 0.66)); grat = mat("whb_grat", (0.42, 0.45, 0.5), 0.55)
    yel = mat("gas_yellow", (1.0, 0.8, 0.0)); stk = mat("stack", (0.74, 0.76, 0.79))
    z0, TOPZ = h + 1.05, 22.0
    for dx in (-hx, -hx / 2, 0, hx / 2, hx):                      # kolom rangka baja
        for dy in (-hy, hy):
            cube(p + Vector((dx, dy, z0)), 0.35, 0.35, TOPZ - z0, frame)
    for lv in (10.0, 14.0, 18.0, TOPZ):                            # balok & grating tiap lantai
        for dy in (-hy, hy):
            cube(p + Vector((0, dy, lv - 0.3)), 2 * hx + 0.4, 0.3, 0.3, frame)
        for dx in (-hx, hx):
            cube(p + Vector((dx, 0, lv - 0.3)), 0.3, 2 * hy + 0.4, 0.3, frame)
        cube(p + Vector((0, -hy + 1.2, lv)), 2 * hx + 0.4, 2.4, 0.08, grat)   # platform sisi depan
        for dx in (-hx, -hx / 2, 0, hx / 2, hx):                  # railing
            cube(p + Vector((dx, -hy - 0.0, lv)), 0.06, 0.06, 1.1, frame)
        cube(p + Vector((0, -hy, lv + 1.05)), 2 * hx + 0.4, 0.06, 0.06, frame)
    cube(p + Vector((0, 1.0, z0)), 2 * hx * 0.75, 2 * hy * 0.6, TOPZ - 3.0 - z0, casing)   # casing boiler/HRSG
    for i in range(7):                                             # pipa vertikal berinsulasi (riser/downcomer)
        x = -hx + 1.5 + i * (2 * hx - 3.0) / 6
        r = 0.32 if i % 2 else 0.22
        y = -hy + 0.9 + (i % 2) * 0.6
        tube([p + Vector((x, y, z0)), p + Vector((x, y, TOPZ + 0.8)), p + Vector((x, y + 1.5, TOPZ + 1.8))], r, ins)
    g1, g2 = P["GLD-01"], P["GLD-02"]                              # pipa gas kuning lewat di atas kedua GLD (foto survei)
    dv = (g2 - g1).normalized(); pv = Vector((-dv.y, dv.x, 0))
    for off, zz, rr, mm in ((0.0, h - 0.9, 0.25, yel), (1.2, h - 1.4, 0.2, yel), (2.6, h - 1.2, 0.3, ins)):
        tube([g1 - dv * 6 + pv * off + Vector((0, 0, zz)), g2 + dv * 6 + pv * off + Vector((0, 0, zz))], rr, mm)
    # steam drum horizontal di puncak + saddle
    bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=1.2, depth=2 * hx + 1.5,
                                        location=(p.x, p.y + 1.0, TOPZ + 2.0), rotation=(0, math.pi / 2, 0))
    add(bpy.context.object, ins)
    for dx in (-hx * 0.6, hx * 0.6):
        cube(p + Vector((dx, 1.0, TOPZ)), 0.5, 1.6, 1.0, frame)
    # ducting gas buang ke cerobong (timur) + cerobong beralas kerucut
    sx = p + Vector((hx + 7.0, 2.0, 0))
    bpy.ops.mesh.primitive_cone_add(vertices=40, radius1=4.0, radius2=2.0, depth=10.0, location=(sx.x, sx.y, 5.0))
    add(bpy.context.object, stk)
    cyl(sx + Vector((0, 0, 10.0)), 2.0, 30.0, stk, 40)
    tube([p + Vector((hx * 0.3, 1.0, TOPZ - 3.0)), p + Vector((hx * 0.3, 1.0, TOPZ + 5.0)),
          p + Vector((hx + 3.0, 1.5, TOPZ + 7.5)), sx + Vector((-1.0, 0, TOPZ + 7.5))], 1.6, stk)
    NP["W:drum"] = p + Vector((hx + 0.75, 1.0, TOPZ + 2.0))
    NP["W:pipes"] = p + Vector((-hx + 1.5 + 2 * (2 * hx - 3.0) / 6, -hy + 0.9, 15.0))
    NP["W:casing"] = p + Vector((hx * 0.4, 1.0 - hy * 0.6, 13.0))
    NP["W:duct"] = p + Vector((hx + 2.0, 1.5, TOPZ + 7.0))
    NP["W:stack"] = sx + Vector((2.0, 0, 20.0))
    NP["W:stk_base"] = sx + Vector((-4.0, 0, 0)); NP["W:stk_top"] = sx + Vector((-4.0, 0, 40.0))
    NP["W:yellow"] = (g1 + g2) / 2 + Vector((0, 0, h - 0.9))
    NP["W:col"] = p + Vector((-hx, -hy - 0.5, 2.5))
    NP["W:base"] = p + Vector((-hx - 1.0, -hy - 0.5, 0)); NP["W:deck"] = p + Vector((-hx - 1.0, -hy - 0.5, h + 1.05))
    NP["W:top"] = p + Vector((-hx - 1.0, -hy - 0.5, TOPZ))
    NP["W:c"] = p.copy()


gld("GLD-01"); gld("GLD-02")
structure((P["GLD-01"] + P["GLD-02"] + P["CH-01"]) / 3 + Vector((0.3, 0.2, 0)))
ch("CH-01", CH1_H)
ch("CH-02", CH2_H, solar=True)

# gedung kantor + gateway di tepi atap
gw = P["GW-01"]
nrm = Vector((280, 165, 0)).normalized()               # normal sisi NE gedung kantor (menghadap klaster WHB)


# ---- lingkungan 3D ditelusuri dari citra peta (piksel crop; tinggi = estimasi visual)
def prism(poly_px, h, wall, name=None):
    import bmesh
    me = bpy.data.meshes.new("b"); ob = bpy.data.objects.new("b", me); sc.collection.objects.link(ob)
    bm = bmesh.new()
    vs = [bm.verts.new(w(px + BOX0[0], py + BOX0[1])) for px, py in poly_px]
    f = bm.faces.new(vs)
    bmesh.ops.recalc_face_normals(bm, faces=[f])
    if f.normal.z < 0:
        f.normal_flip()
    ext = bmesh.ops.extrude_face_region(bm, geom=[f])
    top = [e for e in ext["geom"] if isinstance(e, bmesh.types.BMFace)][0]
    bmesh.ops.translate(bm, verts=top.verts, vec=(0, 0, h))
    uv = bm.loops.layers.uv.new("UVMap")
    for fc in bm.faces:
        fc.material_index = 1 if fc.normal.z > 0.9 else 0
        for lp in fc.loops:
            lp[uv].uv = (lp.vert.co.x / W_, lp.vert.co.y / H_)
    bm.to_mesh(me); bm.free()
    me.materials.append(wall); me.materials.append(gm)
    if name:
        c = Vector((sum(p[0] for p in poly_px) / len(poly_px) + BOX0[0], sum(p[1] for p in poly_px) / len(poly_px) + BOX0[1]))
        NP[name] = w(c.x, c.y, h * 0.6)
    return ob


def column(cx, cy, r_px, h, m, name=None):
    o = cyl(w(cx + BOX0[0], cy + BOX0[1]), r_px / PPM, h, m, 32)
    if name:
        NP[name] = w(cx + BOX0[0], cy + BOX0[1], h)
    return o


WALL = mat("wall", (0.9, 0.88, 0.82)); PROC = mat("proc", (0.62, 0.64, 0.68)); VESS = mat("vess", (0.85, 0.86, 0.88))
# gedung kantor 1 lantai + carport beratap seng di sisi NE (foto survei: GW di tepi atap carport)
CP = 6.0 * PPM                                                                           # lebar carport ± 6 m (px)
nin = (-0.861 * CP, 0.508 * CP)                                                          # arah ke dalam gedung (px)
A_, B_ = (50, 360), (215, 640)
A2, B2 = (A_[0] + nin[0], A_[1] + nin[1]), (B_[0] + nin[0], B_[1] + nin[1])
prism([A2, B2, (87, 719), (-78, 439)], 3.5, WALL, "BLDG")                              # gedung kantor
ROOFM = mat("seng", (0.72, 0.74, 0.76))
cp = prism([A_, B_, B2, A2], 0.12, ROOFM); cp.location.z = ROOF - 0.12                # atap carport (seng)
POST = mat("post", (0.88, 0.89, 0.9)); YEL = mat("post_y", (1.0, 0.82, 0.0)); BLK = mat("post_k", (0.05, 0.05, 0.05))
for i in range(12):
    t = (i + 0.5) / 12
    q = w(A_[0] + (B_[0] - A_[0]) * t + BOX0[0] + nin[0] * 0.03, A_[1] + (B_[1] - A_[1]) * t + BOX0[1] + nin[1] * 0.03)
    cyl(q, 0.08, ROOF - 0.12, POST, 12)
    for k in range(4):
        cyl(q + Vector((0, 0, k * 0.25)), 0.085, 0.25, YEL if k % 2 else BLK, 12)
    if i == 9:
        NP["CARPORT"] = q - Vector((280, 165, 0)).normalized() * 3.0 + Vector((0, 0, ROOF)); NP["POSTBAND"] = q + Vector((0, 0, 0.5))
prism([(382, 455), (520, 365), (562, 440), (425, 537)], 9.0, WALL, "BLDG2")            # gedung tengah
# deret vessel vertikal + walkway di atas (foto 18 Nov) — posisi dari citra, dimensi estimasi
va, vb = w(880, 85), w(928, 245)
for i in range(8):
    q = va.lerp(vb, (i + 0.5) / 8)
    cyl(q, 1.6, 13.0, VESS, 32)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=1.6, location=(q.x, q.y, 13.0)); o = bpy.context.object; o.scale.z = 0.4; add(o, VESS)
vd = (vb - va); vn = vd.normalized()
wk = cube((va + vb) / 2 + Vector((0, 0, 13.6)), 3.6, vd.length + 3, 0.15, M["steel"])
wk.rotation_euler.z = math.atan2(vn.y, vn.x) - math.pi / 2
for t in (0.0, 0.5, 1.0):
    q = va.lerp(vb, t) + Vector((2.2, 0, 0)); cube(q, 0.4, 0.4, 13.6, M["steel"])
NP["VESSELS"] = va.lerp(vb, 0.5) + Vector((0, 0, 14.0))
# dua kolom tinggi (bayangan panjang di citra)
for (cx, cy) in ((992, 245), (922, 318)):
    q = w(cx, cy); cyl(q, 2.1, 40.0, VESS, 40)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=2.1, location=(q.x, q.y, 40.0)); o = bpy.context.object; o.scale.z = 0.35; add(o, VESS)
NP["COL1"] = w(992, 245, 40.0)
# pipe rack dgn pipa kuning dari area vessel ke WHB (± 5 m)
ra, rb = w(960, 300), w(1095, 245)
for t in [i / 6 for i in range(7)]:
    q = ra.lerp(rb, t)
    cube(q, 0.3, 0.3, 5.2, M["steel"])
for k, (off, mm) in enumerate(((0.0, "y"), (0.6, "y"), (1.2, "s"), (1.8, "y"))):
    tube([ra + Vector((0, off, 5.4)), rb + Vector((0, off, 5.4))], 0.18, bpy.data.materials["gas_yellow"] if mm == "y" else M["steel"])
column(520, 345, 11, 6.0, VESS)                                                          # tangki/vessel
NP["WHB"] = w(1300, 150, 10)
NP["ROOF:base"] = gw.copy(); NP["ROOF:top"] = gw + Vector((0, 0, ROOF))
# GW di tepi atap carport: titik peta diproyeksikan ke garis tepi A–B, 0,2 m ke dalam
ea, eb = w(A_[0] + BOX0[0], A_[1] + BOX0[1]), w(B_[0] + BOX0[0], B_[1] + BOX0[1])
ed = (eb - ea).normalized()
gw = ea + ed * (gw - ea).dot(ed) - Vector((280, 165, 0)).normalized() * 0.2
P["GW-01"] = gw
NP["ROOF:base"] = gw.copy(); NP["ROOF:top"] = gw + Vector((0, 0, ROOF))
# siku L: kaki 0,3 m dibaut di atap carport + batang tegak ± 0,5 m di tepi atap; GW di atasnya, antena di atas GW
nrm_ = Vector((280, 165, 0)).normalized()
foot = gw - nrm_ * 0.15
cube(foot + Vector((0, 0, ROOF)), 0.3 * abs(nrm_.x) + 0.05, 0.3 * abs(nrm_.y) + 0.05, 0.05, M["steel"])
cube(gw + Vector((0, 0, ROOF)), 0.05, 0.05, 0.5, M["steel"])
NP["SIKU"] = gw + Vector((0.03, 0, ROOF + 0.25))
NP["SIKU:base"] = gw + Vector((0, 0, ROOF)); NP["SIKU:top"] = gw + Vector((0, 0, ROOF + 0.5))
gwb = gw + Vector((0, 0, ROOF + 0.5))
cube(gwb, 0.15 * S, 0.1 * S, 0.22 * S, M["gw"])
ANT = mat("ant_lb", (0.45, 0.78, 1.0))
cyl(gwb + Vector((0, 0, 0.22 * S)), 0.008 * S, 0.9 * S, ANT, 8)
NP["ANT"] = gwb + Vector((0, 0, 0.22 * S + 0.6 * S))
TOP["GW-01"] = gwb + Vector((0, 0, 1.12 * S))
_t = Vector((-165, 280, 0)).normalized()
NP["CARPORT"] = gw - nrm_ * 3.0 - _t * 4.0 + Vector((0, 0, ROOF))
NP["CARPORT2"] = gw - nrm_ * 3.0 + _t * 4.0 + Vector((0, 0, ROOF))
NP["GW-01"] = gwb + Vector((0, 0, 0.11 * S))
tang = Vector((-nrm.y, nrm.x, 0))

# link LoRa (biru putus-putus)
for a, b, lift in (("GLD-01", "CH-01", 0.6), ("GLD-02", "CH-01", 0.6), ("CH-01", "CH-02", 1.0), ("CH-02", "GW-01", 10.0)):
    pts = arc(TOP[a], TOP[b], lift)
    for i in range(0, len(pts) - 1, 2):
        tube(pts[i:i + 2], (0.03 if lift > 5 else 0.02) * S if S > 1 else 0.015, M["lora"])
    NP[f"LORA:{a}>{b}"] = pts[len(pts) // 2]


def render(name, loc, target, lens):
    cam_d = bpy.data.cameras.new(name); cam_d.lens = lens; cam_d.clip_end = 2000; cam_d.clip_start = 0.05
    cam = bpy.data.objects.new(name, cam_d); sc.collection.objects.link(cam)
    cam.location = loc
    cam.rotation_euler = (Vector(target) - Vector(loc)).to_track_quat("-Z", "Y").to_euler()
    sc.camera = cam
    bpy.context.view_layer.update()
    sc.render.filepath = os.path.join(RB, f"render3d_{name}.png")
    bpy.ops.render.render(write_still=True)
    res = {}
    for k, v in NP.items():
        c = world_to_camera_view(sc, cam, v)
        if c.z > 0:
            res[k] = (c.x * sc.render.resolution_x, (1 - c.y) * sc.render.resolution_y)
    return res


if PASS == "glb":                                  # ekspor model interaktif (skala nyata) untuk viewer HTML
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.duplicates_make_real()
    for o in list(sc.objects):
        if o.type == "CURVE":
            bpy.ops.object.select_all(action="DESELECT"); o.select_set(True)
            bpy.context.view_layer.objects.active = o; bpy.ops.object.convert(target="MESH")
    nf = sorted(((len(o.data.polygons), o.name) for o in sc.objects if o.type == "MESH"), reverse=True)
    print("TOPFACES", nf[:8], sum(n for n, _ in nf))
    for o in sc.objects:                                # ringankan mesh berat (model video) untuk web
        if o.type == "MESH" and len(o.data.polygons) > 400:
            md = o.modifiers.new("dec", "DECIMATE"); md.ratio = max(0.05, 400 / len(o.data.polygons))
    for m in bpy.data.materials:
        if not m.use_nodes:
            m.use_nodes = True
        b = m.node_tree.nodes.get("Principled BSDF")
        if b and not b.inputs["Base Color"].is_linked:
            b.inputs["Base Color"].default_value = (*m.diffuse_color[:3], 1)
            if m.diffuse_color[3] < 1:
                b.inputs["Alpha"].default_value = m.diffuse_color[3]; m.blend_method = "BLEND"
    out_glb = os.path.join(RB, "model_3d_balongan.glb")
    bpy.ops.export_scene.gltf(filepath=out_glb, export_format="GLB", use_visible=True, export_apply=True,
                              export_yup=True, export_image_format="JPEG")
    pts = {k: [v.x, v.z, -v.y] for k, v in NP.items()}
    pts.update({"TOP:" + k: [v.x, v.z, -v.y] for k, v in TOP.items()})
    with open(os.path.join(RB, "model_3d_balongan_pts.json"), "w") as f:
        json.dump(pts, f, indent=1)
    print("GLB_OK", os.path.getsize(out_glb))
    sys.exit(0)
out = {}
if PASS == "wide":
    out["overview"] = render("overview", (166, -24, 60), (85, 64, 3.5), 24)
    c0 = (P["GLD-01"] + P["GLD-02"]) / 2
    out["whb"] = render("whb", (c0.x + 4, c0.y - 46, 13), (c0.x + 12, c0.y - 5, 2.5), 30)
    wc = NP["W:c"]
    out["struct"] = render("struct", (wc.x - 38, wc.y - 52, 24), (wc.x + 2, wc.y, 9), 26)
else:
    g2 = P["GLD-02"]
    out["gld"] = render("gld", (g2.x + 1.6, g2.y - 2.4, 1.6), (g2.x, g2.y, 0.75), 30)
    cam = gw + nrm * 7.0 + tang * 3.5
    out["gw"] = render("gw", (cam.x, cam.y, 6.8), (gw.x - nrm.x * 1.0, gw.y - nrm.y * 1.0, ROOF - 0.8), 28)
with open(os.path.join(RB, f"render3d_pts_{PASS}.json"), "w") as f:
    json.dump(out, f, indent=1)
print("RENDER_OK", PASS)
