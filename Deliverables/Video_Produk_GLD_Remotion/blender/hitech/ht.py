"""Gaya 'high-tech' bersama untuk shot 3D video GLD & OGI (Blender 5.2, EEVEE).

Diadaptasi dari gaya v3 RavTell Lab (seri Digital Twin / Mesin AI): dunia biru malam, lantai mengkilap
dengan grid & cincin pindai, objek 'digital twin' (badan gelap + tepi fresnel cyan + wireframe tipis),
aliran data berdenyut, panel HUD tanpa teks, bloom. Semua teks/label tetap di Remotion.

Pemakaian di skrip shot:
    import ht
    A = ht.args()                      # --orient landscape|portrait --out <mp4|png> [--still N] [--draft]
    ht.setup(seconds=12)
    ... bangun adegan ...
    ht.render()
"""

from __future__ import annotations

import argparse
import math
import random
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

import bmesh
import bpy
from mathutils import Matrix, Vector

FPS = 30
PAL = {
    # identitas 'black glass': hitam pekat, biru GLD + es, amber untuk alarm (beda dari palet navy RavTell)
    "bg": "#020409", "sky_top": "#050d1c", "sky_low": "#020409", "horizon": "#123a7a", "floor": "#020408",
    "body": "#05080f", "body2": "#0a1120", "steel": "#121c2c",
    "holo": "#5ab8ff", "holo2": "#d6f0ff", "ice": "#bfe6ff", "blue": "#2b5fcb", "blue2": "#4f86ff",
    "amber": "#ffae2b", "alarm": "#ff2e55", "ok": "#2dffa0", "violet": "#8a6bff",
    "t0": "#0b0630", "t1": "#4a0c86", "t2": "#b8237a", "t3": "#f0661c", "t4": "#ffe8a0",
    "white": "#f2f8ff",
}

A = None  # argumen CLI (diisi args())


# --- util warna & CLI ---------------------------------------------------------------------


def _lin(c: float) -> float:
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def col(tok: str, a: float = 1.0):
    h = (PAL.get(tok, tok)).lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    return (_lin(r), _lin(g), _lin(b), a)


def args():
    global A
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    p = argparse.ArgumentParser()
    p.add_argument("--orient", default="landscape")
    p.add_argument("--out", required=True)
    p.add_argument("--still", type=int, nargs="*")
    p.add_argument("--draft", action="store_true")
    p.add_argument("--pct", type=int, default=0)
    A = p.parse_args(argv)
    return A


def portrait() -> bool:
    return A is not None and A.orient == "portrait"


def sec(s: float) -> int:
    return int(round(s * FPS)) + 1


# --- scene setup ----------------------------------------------------------------------------


def setup(seconds: float, samples: int = 16) -> None:
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    sc.render.engine = "BLENDER_EEVEE"
    w, h = (1080, 1920) if portrait() else (1920, 1080)
    sc.render.resolution_x, sc.render.resolution_y = w, h
    pct = A.pct if A and A.pct else (50 if A and A.draft else (75 if portrait() else 100))
    sc.render.resolution_percentage = pct
    sc.render.fps = FPS
    sc.frame_start, sc.frame_end = 1, int(round(seconds * FPS))
    ee = sc.eevee
    ee.taa_render_samples = 8 if A and A.draft else samples
    ee.use_raytracing = True  # pantulan lantai kaca (screen-space)
    if hasattr(ee, "ray_tracing_method"):
        ee.ray_tracing_method = "SCREEN"
    opts = getattr(ee, "ray_tracing_options", None)
    if opts is not None:
        if hasattr(opts, "resolution_scale"):
            opts.resolution_scale = "2"
        if hasattr(opts, "use_denoise"):
            opts.use_denoise = True
    for attr, val in (("use_shadows", True), ("shadow_ray_count", 1), ("shadow_step_count", 4)):
        if hasattr(ee, attr):
            setattr(ee, attr, val)
    sc.view_settings.view_transform = "Standard"
    sc.view_settings.look = "None"
    sc.render.film_transparent = False
    sc.render.image_settings.file_format = "PNG"
    sc.render.image_settings.color_mode = "RGB"
    _sky()
    _compositor(sc)


def _sky(strength: float = 1.0) -> None:
    """Langit hitam dengan pita cahaya horizon biru tipis (bukan gradien navy)."""
    sc = bpy.context.scene
    wd = bpy.data.worlds.new("World")
    sc.world = wd
    nt = wd.node_tree
    nt.nodes.clear()
    tc = nt.nodes.new("ShaderNodeTexCoord")
    sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    nt.links.new(tc.outputs["Generated"], sep.inputs[0])
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    cr = ramp.color_ramp
    cr.elements[0].position, cr.elements[0].color = 0.0, col("sky_low")
    cr.elements[1].position, cr.elements[1].color = 1.0, col("sky_low")
    for pos, tk in ((0.46, "sky_low"), (0.5, "horizon"), (0.57, "sky_top")):
        e = cr.elements.new(pos); e.color = col(tk)
    mr = nt.nodes.new("ShaderNodeMapRange")
    mr.inputs["From Min"].default_value, mr.inputs["From Max"].default_value = -1.0, 1.0
    nt.links.new(sep.outputs["Z"], mr.inputs["Value"])
    nt.links.new(mr.outputs["Result"], ramp.inputs["Fac"])
    bg = nt.nodes.new("ShaderNodeBackground")
    bg.inputs["Strength"].default_value = strength
    nt.links.new(ramp.outputs["Color"], bg.inputs["Color"])
    out = nt.nodes.new("ShaderNodeOutputWorld")
    nt.links.new(bg.outputs["Background"], out.inputs["Surface"])
    wd.mist_settings.start, wd.mist_settings.depth, wd.mist_settings.falloff = 25.0, 140.0, "QUADRATIC"


def fog(start: float, depth: float) -> None:
    ms = bpy.context.scene.world.mist_settings
    ms.start, ms.depth = start, depth


def _compositor(sc, bloom: float = 0.7, threshold: float = 0.75, size: float = 0.65) -> None:
    sc.view_layers[0].use_pass_mist = True
    ng = bpy.data.node_groups.new("Comp", "CompositorNodeTree")
    ng.interface.new_socket("Image", in_out="OUTPUT", socket_type="NodeSocketColor")
    sc.compositing_node_group = ng
    n, L = ng.nodes, ng.links
    rl = n.new("CompositorNodeRLayers")
    fogc = n.new("CompositorNodeRGB")
    fogc.outputs[0].default_value = col("bg")
    mix = n.new("ShaderNodeMix")
    mix.data_type = "RGBA"
    mist = n.new("ShaderNodeMath"); mist.operation = "MULTIPLY"; mist.inputs[1].default_value = 0.85
    L.new(rl.outputs["Mist"], mist.inputs[0])
    L.new(mist.outputs[0], mix.inputs["Factor"])
    L.new(rl.outputs["Image"], mix.inputs[6])
    L.new(fogc.outputs[0], mix.inputs[7])
    gl = n.new("CompositorNodeGlare")
    gl.name = "Bloom"
    gl.inputs["Type"].default_value = "Bloom"
    gl.inputs["Threshold"].default_value = threshold
    gl.inputs["Strength"].default_value = bloom
    gl.inputs["Size"].default_value = size
    L.new(mix.outputs[2], gl.inputs["Image"])
    last = gl.outputs["Image"]
    ld = n.new("CompositorNodeLensdist")  # aberasi kromatik halus di tepi frame
    for nm, v in (("Distortion", 0.0), ("Dispersion", 0.018)):
        if nm in ld.inputs:
            ld.inputs[nm].default_value = v
    L.new(last, ld.inputs[0])
    last = ld.outputs[0]
    out = n.new("NodeGroupOutput")
    L.new(last, out.inputs[0])


def light_rig(scale: float = 1.0, warm: bool = False) -> None:
    area("Key", (-8 * scale, -10 * scale, 12 * scale), (50, 0, -35), 2600 * scale ** 2, 8 * scale, (0.8, 0.9, 1.0))
    area("Rim", (10 * scale, 12 * scale, 9 * scale), (-60, 0, 140), 2400 * scale ** 2, 7 * scale, (0.4, 0.8, 1.0))
    area("RimL", (-11 * scale, 9 * scale, 7 * scale), (-60, 0, -140), 1500 * scale ** 2, 6 * scale,
         (1.0, 0.55, 0.35) if warm else (0.55, 0.45, 1.0))


def area(name, loc, rot_deg, energy, size, rgb=(1, 1, 1), shadow=False):
    d = bpy.data.lights.new(name, "AREA")
    d.energy, d.size, d.color = energy, size, rgb
    if hasattr(d, "use_shadow"):
        d.use_shadow = shadow
    o = bpy.data.objects.new(name, d)
    o.location = loc
    o.rotation_euler = tuple(math.radians(a) for a in rot_deg)
    bpy.context.scene.collection.objects.link(o)
    return o


def point(name, loc, energy, rgb=(1, 1, 1), radius=0.2):
    d = bpy.data.lights.new(name, "POINT")
    d.energy, d.color, d.shadow_soft_size = energy, rgb, radius
    if hasattr(d, "use_shadow"):
        d.use_shadow = False
    o = bpy.data.objects.new(name, d)
    o.location = loc
    bpy.context.scene.collection.objects.link(o)
    return o


# --- geometri -------------------------------------------------------------------------------

_BOX = ((0, 2, 3, 1), (4, 5, 7, 6), (0, 1, 5, 4), (2, 6, 7, 3), (0, 4, 6, 2), (1, 3, 7, 5))


class MB:
    """Mesh builder cepat (from_pydata) dengan atribut per-face 'phase' (0..1)."""

    def __init__(self):
        self.v, self.f, self.m, self.ph = [], [], [], []

    def poly(self, pts, mat=0, phase=0.0):
        i = len(self.v)
        self.v.extend(tuple(p) for p in pts)
        self.f.append(tuple(range(i, i + len(pts))))
        self.m.append(mat)
        self.ph.append(phase)

    def box(self, c, s, mat=0, phase=0.0, bottom=True):
        cx, cy, cz = c
        hx, hy, hz = s[0] / 2, s[1] / 2, s[2] / 2
        i = len(self.v)
        for k in range(8):
            self.v.append((cx + (hx if k & 1 else -hx), cy + (hy if k & 2 else -hy), cz + (hz if k & 4 else -hz)))
        for fi, f in enumerate(_BOX):
            if not bottom and fi == 0:
                continue
            self.f.append(tuple(i + j for j in f))
            self.m.append(mat)
            self.ph.append(phase)

    def finish(self, name, mats, loc=(0, 0, 0), smooth=False):
        me = bpy.data.meshes.new(name)
        me.from_pydata(self.v, [], self.f)
        me.update()
        for mt in mats:
            me.materials.append(mt)
        me.polygons.foreach_set("material_index", self.m)
        me.polygons.foreach_set("use_smooth", [smooth] * len(self.f))
        at = me.attributes.new("phase", "FLOAT", "FACE")
        at.data.foreach_set("value", self.ph)
        o = bpy.data.objects.new(name, me)
        o.location = loc
        bpy.context.scene.collection.objects.link(o)
        return o


def _bm_obj(name, bm, mat, loc=(0, 0, 0), smooth=True):
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    if mat is not None:
        me.materials.append(mat)
    me.polygons.foreach_set("use_smooth", [smooth] * len(me.polygons))
    o = bpy.data.objects.new(name, me)
    o.location = loc
    bpy.context.scene.collection.objects.link(o)
    return o


def box(name, loc, size, mat, bevel=0.0):
    mb = MB()
    mb.box((0, 0, 0), size)
    o = mb.finish(name, [mat], loc)
    if bevel:
        m = o.modifiers.new("Bev", "BEVEL"); m.width = bevel; m.segments = 2
    return o


def cyl(name, loc, r, h, mat, axis="Z", seg=32, r2=None, caps=True, smooth=True):
    bm = bmesh.new()
    rot = {"Z": Matrix.Identity(4), "X": Matrix.Rotation(math.pi / 2, 4, "Y"), "Y": Matrix.Rotation(math.pi / 2, 4, "X")}[axis]
    bmesh.ops.create_cone(bm, cap_ends=caps, segments=seg, radius1=r, radius2=r if r2 is None else r2, depth=h, matrix=rot)
    o = _bm_obj(name, bm, mat, loc, smooth)
    for p in o.data.polygons:  # tutup datar
        if len(p.vertices) > 4:
            p.use_smooth = False
    return o


def sphere(name, loc, r, mat, sub=3, scale=(1, 1, 1)):
    bm = bmesh.new()
    bmesh.ops.create_icosphere(bm, subdivisions=sub, radius=r)
    o = _bm_obj(name, bm, mat, loc)
    o.scale = scale
    return o


def uvsphere(name, loc, r, mat, seg=32, rings=16):
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=seg, v_segments=rings, radius=r)
    return _bm_obj(name, bm, mat, loc)


def tube(name, pts, r, mat, seg=8, smooth_path=True, step=0.05):
    """Tabung mengikuti titik (Catmull-Rom); atribut 'phase' 0..1 sepanjang tabung."""
    pts = [Vector(p) for p in pts]
    if smooth_path and len(pts) > 2:
        dense = []
        for i in range(len(pts) - 1):
            p0, p1, p2, p3 = pts[max(0, i - 1)], pts[i], pts[i + 1], pts[min(len(pts) - 1, i + 2)]
            n = max(2, int((p2 - p1).length / step))
            for k in range(n):
                t = k / n
                dense.append(0.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t * t + (-p0 + 3 * p1 - 3 * p2 + p3) * t ** 3))
        dense.append(pts[-1])
        pts = dense
    total = sum((pts[i + 1] - pts[i]).length for i in range(len(pts) - 1)) or 1
    mb, rings, acc, prev = MB(), [], 0.0, None
    for i, p in enumerate(pts):
        d = (pts[min(i + 1, len(pts) - 1)] - pts[max(i - 1, 0)]).normalized()
        ref = Vector((0, 0, 1)) if abs(d.z) < 0.9 else Vector((1, 0, 0))
        nr = d.cross(ref).normalized() if prev is None else (prev - d * prev.dot(d)).normalized()
        prev = nr
        bn = d.cross(nr)
        if i:
            acc += (pts[i] - pts[i - 1]).length
        rings.append(([p + (nr * math.cos(a) + bn * math.sin(a)) * r for a in (2 * math.pi * k / seg for k in range(seg))], acc / total))
    for i in range(len(rings) - 1):
        (a, pa), (b, _) = rings[i], rings[i + 1]
        for k in range(seg):
            mb.poly([a[k], a[(k + 1) % seg], b[(k + 1) % seg], b[k]], 0, pa)
    return mb.finish(name, [mat], smooth=True)


def ring(name, loc, r, w, mat, seg=96, arc=1.0, rot=(0, 0, 0), dash=0):
    mb = MB()
    n = int(seg * arc)
    for i in range(n):
        if dash and i % dash == dash - 1:
            continue
        a0, a1 = 2 * math.pi * i / seg, 2 * math.pi * (i + 1) / seg
        mb.poly([(math.cos(a0) * (r - w), math.sin(a0) * (r - w), 0), (math.cos(a1) * (r - w), math.sin(a1) * (r - w), 0),
                 (math.cos(a1) * (r + w), math.sin(a1) * (r + w), 0), (math.cos(a0) * (r + w), math.sin(a0) * (r + w), 0)], 0, i / max(1, n))
    o = mb.finish(name, [mat], loc)
    o.rotation_euler = rot
    return o


def empty(name, loc=(0, 0, 0)):
    e = bpy.data.objects.new(name, None)
    e.location = loc
    bpy.context.scene.collection.objects.link(e)
    return e


def parent(objs, root):
    for o in objs:
        o.parent = root
    return root


# --- material -------------------------------------------------------------------------------


def _new(name):
    m = bpy.data.materials.new(name)
    nt = m.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    return m, nt, out


def blended(m, cull=False):
    for attr, val in (("surface_render_method", "BLENDED"), ("use_transparent_shadow", True), ("use_backface_culling", cull)):
        if hasattr(m, attr):
            setattr(m, attr, val)
    return m


def time_node(m, name="Time"):
    t = m.node_tree.nodes.new("ShaderNodeValue")
    t.name = t.label = name
    d = t.outputs[0].driver_add("default_value").driver
    d.expression = f"frame / {FPS}"
    return t


class _G:
    """Penulis graf node ringkas: op('ADD', a, b) dsb."""

    def __init__(self, nt):
        self.nt, self.n, self.L = nt, nt.nodes, nt.links

    def val(self, name, v):
        x = self.n.new("ShaderNodeValue"); x.name = x.label = name; x.outputs[0].default_value = v
        return x.outputs[0]

    def op(self, o, a, b=None, c=None, clamp=False):
        x = self.n.new("ShaderNodeMath"); x.operation = o; x.use_clamp = clamp
        for i, s in enumerate((a, b, c)):
            if s is None:
                continue
            if isinstance(s, (int, float)):
                x.inputs[i].default_value = s
            else:
                self.L.new(s, x.inputs[i])
        return x.outputs[0]

    def mixc(self, fac, a, b):
        x = self.n.new("ShaderNodeMix"); x.data_type = "RGBA"
        for sock, v in ((x.inputs["Factor"], fac), (x.inputs[6], a), (x.inputs[7], b)):
            if isinstance(v, tuple) or isinstance(v, float) or isinstance(v, int):
                sock.default_value = v
            else:
                self.L.new(v, sock)
        return x.outputs[2]


def emit(name, tok, strength=2.0):
    m, nt, out = _new(name)
    e = nt.nodes.new("ShaderNodeEmission"); e.name = "Emit"
    e.inputs["Color"].default_value = col(tok)
    e.inputs["Strength"].default_value = strength
    nt.links.new(e.outputs[0], out.inputs["Surface"])
    return m


def emit_fade(name, tok, strength=2.0):
    """Emission + Value 'Vis' (0 = tak terlihat): untuk objek yang muncul/hilang."""
    m, nt, out = _new(name)
    g = _G(nt)
    vis = g.val("Vis", 1.0)
    e = nt.nodes.new("ShaderNodeEmission"); e.name = "Emit"
    e.inputs["Color"].default_value = col(tok)
    nt.links.new(g.op("MULTIPLY", vis, strength), e.inputs["Strength"])
    tr = nt.nodes.new("ShaderNodeBsdfTransparent")
    mx = nt.nodes.new("ShaderNodeMixShader")
    nt.links.new(vis, mx.inputs["Fac"]); nt.links.new(tr.outputs[0], mx.inputs[1]); nt.links.new(e.outputs[0], mx.inputs[2])
    nt.links.new(mx.outputs[0], out.inputs["Surface"])
    return blended(m)


def glossy(name, tok, rough=0.3, metal=0.0, glow=0.0, glow_tok=None, coat=0.0):
    m, nt, out = _new(name)
    b = nt.nodes.new("ShaderNodeBsdfPrincipled"); b.name = "BSDF"
    b.inputs["Base Color"].default_value = col(tok)
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal
    b.inputs["Emission Color"].default_value = col(glow_tok or tok)
    b.inputs["Emission Strength"].default_value = glow
    if coat and "Coat Weight" in b.inputs:
        b.inputs["Coat Weight"].default_value = coat
    nt.links.new(b.outputs[0], out.inputs["Surface"])
    return m


def glass(name, tok="holo2", alpha=0.18, glow=0.15):
    m, nt, out = _new(name)
    b = nt.nodes.new("ShaderNodeBsdfPrincipled")
    b.inputs["Base Color"].default_value = col(tok)
    b.inputs["Roughness"].default_value = 0.05
    b.inputs["Alpha"].default_value = alpha
    b.inputs["Emission Color"].default_value = col(tok)
    b.inputs["Emission Strength"].default_value = glow
    nt.links.new(b.outputs[0], out.inputs["Surface"])
    return blended(m)


def twin(name, body="body", rim="holo", rim_s=2.2, scan=True, rough=0.25, dots=4.0):
    """Material digital twin 'black glass + LiDAR': badan hitam mengkilap, tepi fresnel biru-es,
    pola titik LiDAR di permukaan (kisi 3D pada koordinat objek) + sapuan laser yang melintas (sumbu X dunia)
    dan menyalakan titik. Value 'Rim' & 'Glow' bisa di-keyframe; 'Sweep' = kecerahan sapuan."""
    m, nt, out = _new(name)
    g = _G(nt)
    b = nt.nodes.new("ShaderNodeBsdfPrincipled")
    b.inputs["Base Color"].default_value = col(body)
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = 0.6
    b.inputs["Emission Color"].default_value = col(rim)
    if "Coat Weight" in b.inputs:
        b.inputs["Coat Weight"].default_value = 0.6
    lw = nt.nodes.new("ShaderNodeLayerWeight"); lw.inputs["Blend"].default_value = 0.3
    fres = g.op("POWER", lw.outputs["Facing"], 2.6)
    rimv = g.val("Rim", rim_s)
    glow = g.val("Glow", 0.0)
    e = g.op("MULTIPLY", fres, rimv)
    if scan:
        t = time_node(m)
        tc = nt.nodes.new("ShaderNodeTexCoord")
        vm = nt.nodes.new("ShaderNodeVectorMath"); vm.operation = "SCALE"
        g.L.new(tc.outputs["Object"], vm.inputs[0]); vm.inputs["Scale"].default_value = dots
        fr = nt.nodes.new("ShaderNodeVectorMath"); fr.operation = "FRACTION"
        g.L.new(vm.outputs[0], fr.inputs[0])
        sub = nt.nodes.new("ShaderNodeVectorMath"); sub.operation = "SUBTRACT"
        g.L.new(fr.outputs[0], sub.inputs[0]); sub.inputs[1].default_value = (0.5, 0.5, 0.5)
        ln = nt.nodes.new("ShaderNodeVectorMath"); ln.operation = "LENGTH"
        g.L.new(sub.outputs[0], ln.inputs[0])
        dot = g.op("LESS_THAN", ln.outputs["Value"], 0.56)
        geo = nt.nodes.new("ShaderNodeNewGeometry")
        sep = nt.nodes.new("ShaderNodeSeparateXYZ"); g.L.new(geo.outputs["Position"], sep.inputs[0])
        center = g.op("MULTIPLY_ADD", g.op("FRACT", g.op("MULTIPLY", t.outputs[0], 0.09)), 140.0, -70.0)
        dx = g.op("DIVIDE", g.op("SUBTRACT", sep.outputs["X"], center), 2.2)
        band = g.op("EXPONENT", g.op("MULTIPLY", g.op("MULTIPLY", dx, dx), -1.0))
        sw = g.val("Sweep", 1.0)
        e = g.op("ADD", e, g.op("MULTIPLY", dot, g.op("MULTIPLY_ADD", g.op("MULTIPLY", band, sw), 5.0, 0.35)))
        e = g.op("ADD", e, g.op("MULTIPLY", g.op("MULTIPLY", band, sw), 0.25))
    g.L.new(g.op("ADD", e, glow), b.inputs["Emission Strength"])
    g.L.new(b.outputs[0], out.inputs["Surface"])
    return m


def holo(name, tok="holo", base=0.05, rim=2.6, scan=0.18):
    """Cangkang hologram transparan (fresnel + garis pindai). Value 'Vis' memudarkan."""
    m, nt, out = _new(name)
    g = _G(nt)
    t = time_node(m)
    geo = nt.nodes.new("ShaderNodeNewGeometry")
    sep = nt.nodes.new("ShaderNodeSeparateXYZ"); g.L.new(geo.outputs["Position"], sep.inputs[0])
    lw = nt.nodes.new("ShaderNodeLayerWeight"); lw.inputs["Blend"].default_value = 0.5
    fres = g.op("POWER", lw.outputs["Facing"], 1.8)
    ln = g.op("GREATER_THAN", g.op("FRACT", g.op("MULTIPLY_ADD", sep.outputs["Z"], 9.0, g.op("MULTIPLY", t.outputs[0], -0.8))), 0.88)
    vis = g.val("Vis", 1.0)
    alpha = g.op("MINIMUM", g.op("MULTIPLY", g.op("ADD", g.op("ADD", g.op("MULTIPLY", fres, 0.85), base), g.op("MULTIPLY", ln, scan)), vis), 1.0)
    stren = g.op("MULTIPLY", g.op("ADD", g.op("MULTIPLY", fres, rim), g.op("ADD", 0.3, g.op("MULTIPLY", ln, 1.0))), vis)
    e = nt.nodes.new("ShaderNodeEmission"); e.inputs["Color"].default_value = col(tok)
    g.L.new(stren, e.inputs["Strength"])
    tr = nt.nodes.new("ShaderNodeBsdfTransparent")
    mx = nt.nodes.new("ShaderNodeMixShader")
    g.L.new(alpha, mx.inputs["Fac"]); g.L.new(tr.outputs[0], mx.inputs[1]); g.L.new(e.outputs[0], mx.inputs[2])
    g.L.new(mx.outputs[0], out.inputs["Surface"])
    return blended(m, cull=False)


def pulse(name, tok, rate=0.6, base=0.5, amp=5.0, waves=1.0, sharp=8.0, hide=False):
    """Emission yang menjalar sepanjang atribut 'phase' (aliran data). Value 'Amp' 0 = mati."""
    m, nt, out = _new(name)
    g = _G(nt)
    a = nt.nodes.new("ShaderNodeAttribute"); a.attribute_name = "phase"; a.attribute_type = "GEOMETRY"
    t = time_node(m)
    tr_ = g.op("MULTIPLY", t.outputs[0], g.val("Rate", rate))
    fr = g.op("FRACT", g.op("SUBTRACT", tr_, g.op("MULTIPLY", a.outputs["Fac"], waves)))
    pw = g.op("POWER", g.op("SUBTRACT", 1.0, fr), sharp)
    ampv = g.val("Amp", 1.0)
    tot = g.op("MULTIPLY", g.op("MULTIPLY_ADD", pw, amp, base), ampv)
    e = nt.nodes.new("ShaderNodeEmission"); e.inputs["Color"].default_value = col(tok); e.name = "Emit"
    g.L.new(tot, e.inputs["Strength"])
    if hide:
        trn = nt.nodes.new("ShaderNodeBsdfTransparent")
        mx = nt.nodes.new("ShaderNodeMixShader")
        g.L.new(g.op("MINIMUM", ampv, 1.0), mx.inputs["Fac"]); g.L.new(trn.outputs[0], mx.inputs[1]); g.L.new(e.outputs[0], mx.inputs[2])
        g.L.new(mx.outputs[0], out.inputs["Surface"])
        blended(m)
    else:
        g.L.new(e.outputs[0], out.inputs["Surface"])
    return m


def reveal(name, tok, strength=2.5, soft=0.03):
    """Emission yang muncul bertahap sepanjang 'phase' saat Value 'Progress' naik 0->1 (sisa transparan)."""
    m, nt, out = _new(name)
    g = _G(nt)
    a = nt.nodes.new("ShaderNodeAttribute"); a.attribute_name = "phase"; a.attribute_type = "GEOMETRY"
    prog = g.val("Progress", 0.0)
    mr = nt.nodes.new("ShaderNodeMapRange"); mr.interpolation_type = "SMOOTHSTEP"
    g.L.new(prog, mr.inputs["Value"])
    g.L.new(g.op("SUBTRACT", a.outputs["Fac"], soft), mr.inputs["From Min"])
    g.L.new(a.outputs["Fac"], mr.inputs["From Max"])
    on = mr.outputs["Result"]
    e = nt.nodes.new("ShaderNodeEmission"); e.inputs["Color"].default_value = col(tok); e.name = "Emit"
    g.L.new(g.op("MULTIPLY", on, strength), e.inputs["Strength"])
    trn = nt.nodes.new("ShaderNodeBsdfTransparent")
    mx = nt.nodes.new("ShaderNodeMixShader")
    g.L.new(on, mx.inputs["Fac"]); g.L.new(trn.outputs[0], mx.inputs[1]); g.L.new(e.outputs[0], mx.inputs[2])
    g.L.new(mx.outputs[0], out.inputs["Surface"])
    return blended(m)


def floor(size=200.0, grid=2.0, tok_line="blue", line_s=0.9, rough=0.08, spokes=48):
    """Lantai kaca hitam (memantul) dengan grid polar ala radar: cincin konsentris + jari-jari, memudar ke tepi."""
    m, nt, out = _new("FloorM")
    g = _G(nt)
    b = nt.nodes.new("ShaderNodeBsdfPrincipled")
    b.inputs["Base Color"].default_value = col("floor")
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = 0.7
    b.inputs["Emission Color"].default_value = col(tok_line)
    geo = nt.nodes.new("ShaderNodeNewGeometry")
    sep = nt.nodes.new("ShaderNodeSeparateXYZ"); g.L.new(geo.outputs["Position"], sep.inputs[0])
    x, y = sep.outputs["X"], sep.outputs["Y"]
    r = g.op("SQRT", g.op("ADD", g.op("MULTIPLY", x, x), g.op("MULTIPLY", y, y)))
    rf = g.op("FRACT", g.op("DIVIDE", r, grid))
    rings = g.op("LESS_THAN", g.op("MINIMUM", rf, g.op("SUBTRACT", 1.0, rf)), 0.018)
    ang = g.op("DIVIDE", g.op("ARCTAN2", y, x), 2 * math.pi / spokes)
    af = g.op("FRACT", ang)
    wd = g.op("DIVIDE", 0.035 * spokes / (2 * math.pi), g.op("MAXIMUM", r, 0.5))
    sp = g.op("LESS_THAN", g.op("MINIMUM", af, g.op("SUBTRACT", 1.0, af)), wd)
    lines = g.op("MAXIMUM", rings, g.op("MULTIPLY", sp, 0.55))
    fade = g.op("SUBTRACT", 1.0, g.op("MINIMUM", g.op("DIVIDE", r, size * 0.32), 1.0))
    g.L.new(g.op("MULTIPLY", g.op("MULTIPLY", lines, g.op("POWER", fade, 1.5)), line_s), b.inputs["Emission Strength"])
    g.L.new(b.outputs[0], out.inputs["Surface"])
    mb = MB()
    s = size / 2
    mb.poly([(-s, -s, 0), (s, -s, 0), (s, s, 0), (-s, s, 0)])
    return mb.finish("Floor", [m])


def scan_rings(name, loc, radii=(1.0, 1.35, 1.8, 2.4), tok="holo", w=0.02, rate=0.4, spokes=24):
    """Reticle HUD di lantai: busur bersegmen yang berputar berlawanan arah + garis tick (bukan cincin polos)."""
    mat = pulse(name + "M", tok, rate=rate, base=1.0, amp=2.0, waves=1.0, sharp=4)
    tick = emit(name + "TickM", "ice", 2.2)
    objs = []
    f_end = bpy.context.scene.frame_end
    for k, rr in enumerate(radii):
        mb = MB()
        n = 120
        segs = (3, 5, 2, 7)[k % 4]
        for i in range(n):
            ang = i / n
            if k % 2 == 0 and (int(ang * segs * 2) % 2) == 1:
                continue
            if k % 2 == 1 and (i % 6) > 3:
                continue
            a0, a1 = 2 * math.pi * i / n, 2 * math.pi * (i + 1) / n
            ww = w * (1.0 if k % 2 == 0 else 0.5)
            mb.poly([(math.cos(a) * (rr + s_), math.sin(a) * (rr + s_), 0.004) for a, s_ in ((a0, -ww), (a1, -ww), (a1, ww), (a0, ww))], 0, ang)
        o = mb.finish(f"{name}_{k}", [mat], loc)
        key(o, "rotation_euler", [(1, (0, 0, 0)), (f_end, (0, 0, (1 if k % 2 else -1) * (0.6 + 0.3 * k)))], interp="LINEAR")
        objs.append(o)
    mb = MB()
    R0 = radii[-1] * 1.04
    for i in range(spokes * 3):
        a = 2 * math.pi * i / (spokes * 3)
        d = Vector((math.cos(a), math.sin(a), 0))
        sd = Vector((-d.y, d.x, 0)) * w * 0.25
        L = w * (8 if i % 3 == 0 else 3)
        z = Vector((0, 0, 0.004))
        mb.poly([d * R0 - sd + z, d * (R0 + L) - sd + z, d * (R0 + L) + sd + z, d * R0 + sd + z])
    objs.append(mb.finish(name + "_Ticks", [tick], loc))
    return objs[0], mat


def dust(name="Dust", center=(0, 0, 3), extent=(40, 40, 10), n=400, size=0.03, tok="ice", strength=4.0, seed=4, drift=(0.6, 0.2, 0.25)):
    """Partikel debu/data bercahaya yang melayang pelan (kedalaman & skala futuristik)."""
    rnd = random.Random(seed)
    mb = MB()
    for i in range(n):
        c = (center[0] + rnd.uniform(-1, 1) * extent[0] / 2, center[1] + rnd.uniform(-1, 1) * extent[1] / 2, center[2] + rnd.uniform(-1, 1) * extent[2] / 2)
        s_ = size * rnd.uniform(0.4, 1.4)
        mb.box(c, (s_, s_, s_), 0, rnd.random())
    o = mb.finish(name, [pulse(name + "M", tok, rate=0.3, base=strength * 0.4, amp=strength, waves=1.0, sharp=6)])
    key(o, "location", [(1, (0, 0, 0)), (bpy.context.scene.frame_end, drift)], interp="LINEAR")
    return o


def wire(obj, tok="holo", strength=1.2, thick=0.012, decimate=1.0, name=None):
    """Salinan wireframe bercahaya dari objek (garis tepi digital twin)."""
    w = obj.copy()
    w.data = obj.data.copy()
    w.name = name or obj.name + "_Wire"
    w.animation_data_clear()
    bpy.context.scene.collection.objects.link(w)
    w.data.materials.clear()
    w.data.materials.append(emit(w.name + "M", tok, strength))
    for md in list(w.modifiers):
        w.modifiers.remove(md)
    if decimate < 1.0:
        d = w.modifiers.new("Dec", "DECIMATE"); d.decimate_type = "DISSOLVE"; d.angle_limit = math.radians(decimate * 90)
    wf = w.modifiers.new("WF", "WIREFRAME"); wf.thickness = thick; wf.use_replace = True; wf.use_even_offset = True
    w.parent = obj.parent
    w.matrix_parent_inverse = obj.matrix_parent_inverse.copy()
    return w


def edges(obj, tok="holo", strength=1.5, thick=0.01, angle=30.0, name=None, mat=None):
    """Garis bercahaya hanya di tepi tajam (sudut > angle): tampilan digital twin yang bersih.
    Tiap tepi jadi prisma tipis; atribut 'phase' = tinggi relatif (untuk material pulse/reveal)."""
    me = obj.data
    bm = bmesh.new()
    bm.from_mesh(me)
    mw = obj.matrix_world if obj.parent is None else Matrix.Identity(4)
    mb = MB()
    zs = [v.co.z for v in bm.verts] or [0.0]
    z0, z1 = min(zs), max(zs)
    for e in bm.edges:
        if len(e.link_faces) == 2 and e.calc_face_angle(0) < math.radians(angle):
            continue
        a, b = e.verts[0].co.copy(), e.verts[1].co.copy()
        d = b - a
        if d.length < 1e-6:
            continue
        dn = d.normalized()
        ref = Vector((0, 0, 1)) if abs(dn.z) < 0.9 else Vector((1, 0, 0))
        u = dn.cross(ref).normalized() * thick
        v = dn.cross(u).normalized() * thick
        c = [a + u + v, a - u + v, a - u - v, a + u - v]
        cb = [p + d for p in c]
        ph = ((a.z + b.z) / 2 - z0) / max(1e-6, z1 - z0)
        for k in range(4):
            mb.poly([c[k], c[(k + 1) % 4], cb[(k + 1) % 4], cb[k]], 0, ph)
    bm.free()
    w = mb.finish(name or obj.name + "_Edge", [mat or emit((name or obj.name) + "_EdgeM", tok, strength)])
    w.parent = obj.parent
    w.matrix_world = obj.matrix_world.copy() if obj.parent is None else w.matrix_world
    if obj.parent is not None:
        w.location, w.rotation_euler, w.scale = obj.location, obj.rotation_euler, obj.scale
    return w


# --- thermal (palet 'iron') -------------------------------------------------------------------


def thermal_mix(m, temp_attr="temp", axis="X", wipe_prop="wipe", softness=0.6, invert=False):
    """Bungkus material `m`: sisi < scene[wipe] (sepanjang axis dunia) tampil sebagai emisi palet iron
    berdasarkan obj[temp_attr] (0..1) + sedikit noise. Dipakai untuk efek 'sapuan kamera thermal'."""
    nt = m.node_tree
    g = _G(nt)
    out = next(x for x in nt.nodes if x.bl_idname == "ShaderNodeOutputMaterial")
    src = out.inputs["Surface"].links[0].from_socket
    at = nt.nodes.new("ShaderNodeAttribute"); at.attribute_type = "OBJECT"; at.attribute_name = temp_attr
    tc = nt.nodes.new("ShaderNodeTexCoord")
    nz = nt.nodes.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = 1.4
    g.L.new(tc.outputs["Object"], nz.inputs["Vector"])
    geo = nt.nodes.new("ShaderNodeNewGeometry")
    sep = nt.nodes.new("ShaderNodeSeparateXYZ"); g.L.new(geo.outputs["Position"], sep.inputs[0])
    # gradien vertikal halus: bagian bawah sedikit lebih dingin
    tz = g.op("MULTIPLY_ADD", g.op("MINIMUM", sep.outputs["Z"], 6.0), 0.01, -0.03)
    t = g.op("ADD", g.op("ADD", at.outputs["Fac"], g.op("MULTIPLY_ADD", nz.outputs["Fac"], 0.14, -0.07)), tz, clamp=True)
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    els = ramp.color_ramp.elements
    stops = [(0.0, "t0"), (0.3, "t1"), (0.55, "t2"), (0.78, "t3"), (1.0, "t4")]
    els[0].position, els[0].color = 0.0, col("t0")
    els[1].position, els[1].color = 1.0, col("t4")
    for p, tk in stops[1:-1]:
        e = els.new(p); e.color = col(tk)
    g.L.new(t, ramp.inputs["Fac"])
    em = nt.nodes.new("ShaderNodeEmission"); em.inputs["Strength"].default_value = 1.0
    g.L.new(ramp.outputs["Color"], em.inputs["Color"])
    wv = nt.nodes.new("ShaderNodeValue"); wv.name = "Wipe"
    d = wv.outputs[0].driver_add("default_value").driver
    d.type = "AVERAGE"
    v = d.variables.new(); v.type = "SINGLE_PROP"
    v.targets[0].id_type = "SCENE"; v.targets[0].id = bpy.context.scene; v.targets[0].data_path = f'["{wipe_prop}"]'
    coord = sep.outputs[axis]
    diff = g.op("SUBTRACT", coord, wv.outputs[0]) if invert else g.op("SUBTRACT", wv.outputs[0], coord)
    fac = g.op("MULTIPLY", diff, 1.0 / softness, clamp=True)
    mx = nt.nodes.new("ShaderNodeMixShader")
    g.L.new(fac, mx.inputs["Fac"]); g.L.new(src, mx.inputs[1]); g.L.new(em.outputs[0], mx.inputs[2])
    g.L.new(mx.outputs[0], out.inputs["Surface"])
    return m


def set_temp(obj, t):
    obj["temp"] = t
    return obj


def key_prop(idblock, prop, keys, interp="BEZIER"):
    for f, v in keys:
        idblock[prop] = v
        idblock.keyframe_insert(f'["{prop}"]', frame=f)
    _interp(idblock, interp)


# --- animasi --------------------------------------------------------------------------------


def _fcurves(action):
    if hasattr(action, "layers") and action.layers:
        for layer in action.layers:
            for strip in layer.strips:
                for bag in strip.channelbags:
                    yield from bag.fcurves
    elif hasattr(action, "fcurves"):
        yield from action.fcurves


def _interp(idblock, interp, path=None):
    ad = getattr(idblock, "animation_data", None)
    if not ad or not ad.action:
        return
    for fc in _fcurves(ad.action):
        if path is None or fc.data_path == path:
            for kp in fc.keyframe_points:
                kp.interpolation = interp


def key(o, path, keys, interp="BEZIER"):
    """Keyframe atribut objek: key(o, 'location', [(1, (0,0,0)), (60, (1,0,0))])."""
    for f, v in keys:
        setattr(o, path, v)
        o.keyframe_insert(path, frame=f)
    _interp(o, interp, path)


def keyv(m, node, keys, interp="BEZIER"):
    """Keyframe Value node `node` di material m."""
    s = m.node_tree.nodes[node].outputs[0]
    for f, v in keys:
        s.default_value = v
        s.keyframe_insert("default_value", frame=f)
    _interp(m.node_tree, interp)


def keyin(m, node, inp, keys, interp="BEZIER"):
    s = m.node_tree.nodes[node].inputs[inp]
    for f, v in keys:
        s.default_value = v
        s.keyframe_insert("default_value", frame=f)
    _interp(m.node_tree, interp)


def show(objs, f_on=None, f_off=None):
    """Tampilkan objek hanya di rentang [f_on, f_off)."""
    for o in objs:
        seq = [(1, f_on is not None and f_on > 1)]
        if f_on and f_on > 1:
            seq.append((f_on, False))
        if f_off:
            seq.append((f_off, True))
        for f, h in seq:
            o.hide_render = h
            o.keyframe_insert("hide_render", frame=f)
        _interp(o, "CONSTANT", "hide_render")


def camera(loc, target, lens=35.0, name="Cam"):
    d = bpy.data.cameras.new(name)
    d.lens = lens
    d.clip_start, d.clip_end = 0.05, 600
    d.sensor_fit = "HORIZONTAL" if not portrait() else "VERTICAL"
    cam = bpy.data.objects.new(name, d)
    cam.location = loc
    bpy.context.scene.collection.objects.link(cam)
    tgt = empty(name + "_T", target)
    c = cam.constraints.new("TRACK_TO")
    c.target = tgt
    c.track_axis = "TRACK_NEGATIVE_Z"
    c.up_axis = "UP_Y"
    bpy.context.scene.camera = cam
    return cam, tgt


def lens(cam, keys, interp="BEZIER"):
    for f, v in keys:
        cam.data.lens = v
        cam.data.keyframe_insert("lens", frame=f)
    _interp(cam.data, interp)


def shake(obj, strength=0.015, scale=40.0):
    if not obj.animation_data or not obj.animation_data.action:
        obj.keyframe_insert("location", frame=1)
    for fc in _fcurves(obj.animation_data.action):
        if fc.data_path == "location":
            md = fc.modifiers.new("NOISE")
            md.strength, md.scale, md.phase = strength, scale, fc.array_index * 13.7


def dof(cam, dist, fstop=2.8):
    cam.data.dof.use_dof = True
    cam.data.dof.focus_distance = dist
    cam.data.dof.aperture_fstop = fstop


# --- elemen high-tech siap pakai ----------------------------------------------------------------


def streams(name, a, b, n=5, tok="holo", rate=0.9, spread=0.25, arc=0.6, r=0.012, seed=1, hide=False):
    """Berkas aliran data melengkung a -> b."""
    rnd = random.Random(seed)
    m = pulse(name + "M", tok, rate=rate, base=0.35, amp=7.0, waves=2.0, sharp=10, hide=hide)
    A_, B_ = Vector(a), Vector(b)
    out = []
    for i in range(n):
        off = Vector((rnd.uniform(-1, 1), rnd.uniform(-1, 1), rnd.uniform(-1, 1))) * spread
        mid = (A_ + B_) / 2 + off + Vector((0, 0, arc))
        out.append(tube(f"{name}_{i}", [A_ + off * 0.1, A_.lerp(mid, 0.5) + off * 0.3, mid, mid.lerp(B_, 0.5) + off * 0.3, B_ + off * 0.1], r, m, seg=6))
    return out, m


def hud_panel(name, loc, w, h, kind="wave", tok="holo", face=None, seed=1, frame_tok="blue2"):
    """Panel HUD melayang tanpa teks: bingkai, latar tipis, grafik (wave/bars/ecg/ring)."""
    rnd = random.Random(seed)
    root = empty(name, loc)
    back = emit_fade(name + "_BgM", "body2", 0.35)
    fr = emit(name + "_FrM", frame_tok, 2.0)
    gr = pulse(name + "_GrM", tok, rate=0.35, base=1.4, amp=3.0, waves=1.0, sharp=4)
    objs = []
    mb = MB(); mb.poly([(-w / 2, 0, -h / 2), (w / 2, 0, -h / 2), (w / 2, 0, h / 2), (-w / 2, 0, h / 2)])
    objs.append(mb.finish(name + "_Bg", [back]))
    mb = MB(); t = 0.012 * max(w, h)
    c = 0.18 * min(w, h)
    for (x0, z0, x1, z1) in ((-w / 2, -h / 2, -w / 2 + c, -h / 2 + t), (-w / 2, -h / 2, -w / 2 + t, -h / 2 + c),
                             (w / 2 - c, -h / 2, w / 2, -h / 2 + t), (w / 2 - t, -h / 2, w / 2, -h / 2 + c),
                             (-w / 2, h / 2 - t, -w / 2 + c, h / 2), (-w / 2, h / 2 - c, -w / 2 + t, h / 2),
                             (w / 2 - c, h / 2 - t, w / 2, h / 2), (w / 2 - t, h / 2 - c, w / 2, h / 2)):
        mb.poly([(x0, -0.005, z0), (x1, -0.005, z0), (x1, -0.005, z1), (x0, -0.005, z1)])
    for (x0, z0, x1, z1) in ((-w / 2, -h / 2, w / 2, -h / 2 + t * 0.4), (-w / 2, h / 2 - t * 0.4, w / 2, h / 2)):
        mb.poly([(x0, -0.004, z0), (x1, -0.004, z0), (x1, -0.004, z1), (x0, -0.004, z1)])
    objs.append(mb.finish(name + "_Fr", [fr]))
    mb = MB()
    N = 60
    lw = 0.006 * max(w, h)
    if kind in ("wave", "ecg"):
        pts = []
        for k in range(N + 1):
            x = -w / 2 + 0.08 * w + 0.84 * w * k / N
            if kind == "ecg":
                ph = (k % 15) / 15
                y = 0.3 * h * (math.exp(-((ph - 0.5) / 0.03) ** 2) - 0.3 * math.exp(-((ph - 0.56) / 0.03) ** 2))
            else:
                y = 0.22 * h * math.sin(k * 0.32 + seed) * (0.6 + 0.4 * math.sin(k * 0.08))
            pts.append((x, y - 0.05 * h))
        for k in range(N):
            (xa, ya), (xb, yb) = pts[k], pts[k + 1]
            mb.poly([(xa, -0.006, ya - lw), (xb, -0.006, yb - lw), (xb, -0.006, yb + lw), (xa, -0.006, ya + lw)], 0, k / N)
    elif kind == "bars":
        for k in range(10):
            bh = h * (0.12 + 0.6 * rnd.random())
            x = -w / 2 + 0.1 * w + k * 0.8 * w / 10
            mb.poly([(x, -0.006, -h / 2 + 0.1 * h), (x + 0.05 * w, -0.006, -h / 2 + 0.1 * h), (x + 0.05 * w, -0.006, -h / 2 + 0.1 * h + bh), (x, -0.006, -h / 2 + 0.1 * h + bh)], 0, k / 10)
    elif kind == "ring":
        rr = 0.32 * min(w, h)
        for k in range(48):
            if k > 36:
                continue
            a0, a1 = 2 * math.pi * k / 48, 2 * math.pi * (k + 1) / 48
            mb.poly([(math.cos(a0) * rr, -0.006, math.sin(a0) * rr), (math.cos(a1) * rr, -0.006, math.sin(a1) * rr),
                     (math.cos(a1) * rr * 0.8, -0.006, math.sin(a1) * rr * 0.8), (math.cos(a0) * rr * 0.8, -0.006, math.sin(a0) * rr * 0.8)], 0, k / 48)
    objs.append(mb.finish(name + "_Gr", [gr]))
    parent(objs, root)
    if face is not None:
        dx, dy = face[0] - loc[0], face[1] - loc[1]
        root.rotation_euler = (0, 0, math.atan2(dx, -dy))
    return root, back


def beacon(name, loc, tok="alarm", r=0.4, h=12.0):
    """Pilar cahaya vertikal (penanda alarm/prioritas)."""
    m = pulse(name + "M", tok, rate=1.2, base=0.6, amp=2.5, waves=3.0, sharp=3, hide=True)
    mb = MB()
    seg = 24
    for i in range(seg):
        a0, a1 = 2 * math.pi * i / seg, 2 * math.pi * (i + 1) / seg
        mb.poly([(math.cos(a0) * r, math.sin(a0) * r, 0), (math.cos(a1) * r, math.sin(a1) * r, 0),
                 (math.cos(a1) * r * 0.6, math.sin(a1) * r * 0.6, h), (math.cos(a0) * r * 0.6, math.sin(a0) * r * 0.6, h)], 0, 0.0)
    # phase sepanjang tinggi tidak tersedia pada quad tunggal: gunakan banyak lapisan
    mb = MB()
    layers = 24
    for j in range(layers):
        z0, z1 = h * j / layers, h * (j + 1) / layers
        for i in range(seg):
            a0, a1 = 2 * math.pi * i / seg, 2 * math.pi * (i + 1) / seg
            r0, r1 = r * (1 - 0.4 * j / layers), r * (1 - 0.4 * (j + 1) / layers)
            mb.poly([(math.cos(a0) * r0, math.sin(a0) * r0, z0), (math.cos(a1) * r0, math.sin(a1) * r0, z0),
                     (math.cos(a1) * r1, math.sin(a1) * r1, z1), (math.cos(a0) * r1, math.sin(a0) * r1, z1)], 0, j / layers)
    return mb.finish(name, [m], loc), m


# --- render ---------------------------------------------------------------------------------


def render():
    sc = bpy.context.scene
    out = Path(A.out).resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    if A.still is not None:
        frames = A.still or [1, sc.frame_end // 2, sc.frame_end]
        paths = []
        for f in frames:
            sc.frame_set(f)
            p = out.with_name(f"{out.stem}_f{f:04d}.png")
            sc.render.filepath = str(p)
            bpy.ops.render.render(write_still=True)
            paths.append(p)
        print(f"STILLS {[str(p) for p in paths]} ({time.time() - t0:.1f}s)")
        return
    tmp = Path(tempfile.mkdtemp(prefix="ht_", dir=str(out.parent)))
    sc.render.filepath = str(tmp / "#####")
    bpy.ops.render.render(animation=True)
    w, h = (1080, 1920) if portrait() else (1920, 1080)
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-framerate", str(FPS), "-i", str(tmp / "%05d.png"),
                    "-vf", f"scale={w}:{h}:flags=lanczos", "-c:v", "libx264", "-preset", "slow", "-crf", "16",
                    "-pix_fmt", "yuv420p", str(out)], check=True)
    shutil.rmtree(tmp, ignore_errors=True)
    print(f"RENDER {out} {sc.frame_end} frame ({time.time() - t0:.0f}s, {(time.time() - t0) / sc.frame_end:.2f}s/frame)")
