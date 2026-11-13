import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.colors import to_rgb

OUT = r"C:\Users\Win11\Documents\GLD-V2-Report-2026\scripts\assets\balongan_13nov"
N = 36

def box(x0, x1, y0, y1, z0, z1):
    v = np.array([[x0,y0,z0],[x1,y0,z0],[x1,y1,z0],[x0,y1,z0],[x0,y0,z1],[x1,y0,z1],[x1,y1,z1],[x0,y1,z1]], float)
    f = [[0,1,2,3],[4,5,6,7],[0,1,5,4],[2,3,7,6],[1,2,6,5],[0,3,7,4]]
    return [v[i] for i in f]

def frame(axis):
    a = np.array(axis, float); a /= np.linalg.norm(a)
    t = np.array([1, 0, 0]) if abs(a[0]) < 0.9 else np.array([0, 1, 0])
    u = np.cross(a, t); u /= np.linalg.norm(u); w = np.cross(a, u)
    return a, u, w

def cyl(c, axis, r, L, caps=True, n=N):
    a, u, w = frame(axis); c = np.array(c, float)
    th = np.linspace(0, 2 * np.pi, n + 1)
    ring = [r * (np.cos(t) * u + np.sin(t) * w) for t in th]
    polys = [np.array([c + ring[i], c + ring[i + 1], c + a * L + ring[i + 1], c + a * L + ring[i]]) for i in range(n)]
    if caps:
        polys.append(np.array([c + p for p in ring[:-1]]))
        polys.append(np.array([c + a * L + p for p in ring[:-1]]))
    return polys

def torus_half(c, axis_u, axis_v, R, r, n=24, m=12):
    # half torus: centerline arc from +u through -v... arc in plane (u, v), angle 0..pi, tube radius r
    c = np.array(c, float); u = np.array(axis_u, float); v = np.array(axis_v, float)
    nrm = np.cross(u, v)
    polys = []
    ph = np.linspace(0, np.pi, n + 1); ps = np.linspace(0, 2 * np.pi, m + 1)
    def P(i, j):
        cc = c + R * (np.cos(ph[i]) * u + np.sin(ph[i]) * v)
        rad = np.cos(ph[i]) * u + np.sin(ph[i]) * v
        return cc + r * (np.cos(ps[j]) * rad + np.sin(ps[j]) * nrm)
    for i in range(n):
        for j in range(m):
            polys.append(np.array([P(i, j), P(i + 1, j), P(i + 1, j + 1), P(i, j + 1)]))
    return polys

def ubolt(cx, along, pipe_c, R=33, r=5, leg_top=12):
    """U-bolt around pipe whose axis is `along` (unit vec in local x or y), located at offset cx along pipe.
    Plate is z in [0,5]; pipe centre at z = pipe_c (negative)."""
    along = np.array(along, float)
    side = np.cross([0, 0, 1], along)  # horizontal, perpendicular to pipe
    base = along * cx
    parts = []
    # semicircle below pipe centre: from +side through -z to -side
    parts += torus_half(base + np.array([0, 0, pipe_c]), side, [0, 0, -1], R, r)
    for sgn in (1, -1):
        p0 = base + sgn * side * R + np.array([0, 0, pipe_c])
        parts += cyl(p0, [0, 0, 1], r, -pipe_c + 5 + leg_top, caps=False, n=12)
        nut = base + sgn * side * R + np.array([0, 0, 5])
        parts += cyl(nut, [0, 0, 1], 9, 8, n=6)
    return parts

def tube(path, r=8, col="#3F4246"):
    P = []
    for a, b in zip(path[:-1], path[1:]):
        a, b = np.array(a, float), np.array(b, float)
        L = np.linalg.norm(b - a)
        P += cyl(a, b - a, r, L, caps=False, n=12)
    return P

def smooth(pts, k=10):
    pts = [np.array(p, float) for p in pts]
    pts = [pts[0]] + pts + [pts[-1]]
    out = []
    for i in range(1, len(pts) - 2):
        p0, p1, p2, p3 = pts[i - 1], pts[i], pts[i + 1], pts[i + 2]
        for t in np.linspace(0, 1, k, endpoint=False):
            out.append(0.5 * (2 * p1 + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t ** 2 + (-p0 + 3 * p1 - 3 * p2 + p3) * t ** 3))
    out.append(pts[-2])
    return out

def cable(kind):
    if kind == "handrail":
        path = smooth([(-108, 25, 70), (-140, 45, 70), (-150, 140, 45), (-150, 165, -20), (-150, 120, -76), (-175, 40, -76), (-240, 30, -76), (-330, 30, -76)])
        ties = [cyl((x, 15, -55), (1, 0, 0), 44, 5, caps=False, n=24) for x in (-230, -300)]
    else:
        path = smooth([(-108, 25, 70), (-140, 45, 70), (-145, 145, 40), (-90, 172, -20), (-20, 150, -80), (0, 60, -80), (0, -100, -80), (0, -330, -80)])
        ties = [cyl((0, y, -52), (0, 1, 0), 42, 5, caps=False, n=24) for y in (-200, -280)]
    return tube(path), [q for t in ties for q in t]

def gld():
    P, C = [], []
    def add(ps, col):
        P.extend(ps); C.extend([col] * len(ps))
    blue, steel, dark, beige = "#2F7BD8", "#C4C9CF", "#26282B", "#CDBFA6"
    ears = [(0, 95), (-76, -62), (76, -62)]
    for x, y in ears:
        add(cyl((x, y, 5), (0, 0, 1), 6, 30, n=12), steel)
        add(cyl((x, y, 35), (0, 0, 1), 16, 8, n=20), blue)
    add(box(-12, 12, 60, 95, 35, 43), blue)
    for sx in (-1, 1):
        add(box(min(0, sx * 76), max(0, sx * 76), -70, -50, 35, 43), blue)
    add(cyl((0, 0, 35), (0, 0, 1), 72, 8, n=48), blue)
    add(cyl((0, 0, 43), (0, 0, 1), 66, 52, n=48), blue)
    add(cyl((0, 0, 95), (0, 0, 1), 74, 45, n=8), blue)
    add(cyl((0, 0, 140), (0, 0, 1), 48, 0.6, n=48), beige)
    add(box(-26, 26, -88, -55, 45, 88), blue)
    add(cyl((0, -88, 66), (0, -1, 0), 12, 10, n=6), steel)
    add(cyl((-60, 25, 70), (-1, 0, 0), 16, 24, n=24), blue)
    add(cyl((-84, 25, 70), (-1, 0, 0), 13, 26, n=12), dark)
    add(cyl((60, 25, 70), (1, 0, 0), 16, 24, n=24), blue)
    add(cyl((84, 25, 70), (1, 0, 0), 12, 16, n=6), steel)
    add(cyl((124, -40, 70), (0, 1, 0), 26, 100, n=32), steel)
    add(cyl((124, 60, 70), (0, 1, 0), 24, 30, n=32), "#C0392B")
    add(cyl((124, 90, 70), (0, 1, 0), 15, 8, n=24), "#C0392B")
    add(cyl((-15, 60, 70), (0, 1, 0), 5, 180, n=12), dark)
    return P, C

def scene(kind):
    P, C = [], []
    def add(ps, col):
        P.extend(ps); C.extend([col] * len(ps))
    add(box(-125, 125, -125, 125, 0, 5), "#D9DDE2")
    pipe_c = -36
    if kind == "handrail":
        add(cyl((-330, 0, pipe_c), (1, 0, 0), 30.15, 660), "#8C96A2")
        for cx in (-88, 88):
            add(ubolt(cx, (1, 0, 0), pipe_c), "#C8641E")
    else:
        add(cyl((0, -330, pipe_c), (0, 1, 0), 30.15, 660), "#8C96A2")
        for cx in (-95, 95):
            add(ubolt(cx, (0, 1, 0), pipe_c), "#C8641E")
    g, gc = gld(); P += g; C += gc
    cb, ti = cable(kind); add(cb, "#3F4246"); add(ti, "#111111")
    T = lambda p: np.stack([p[:, 0], -p[:, 2], p[:, 1]], axis=1)
    P = [T(np.asarray(p, float)) for p in P]
    return P, C

from PIL import Image, ImageFilter

def render(kind, fn, cam_dir, W=1800, H=1500, ss=2):
    P, C = scene(kind)
    W2, H2 = W * ss, H * ss
    allp = np.concatenate([np.asarray(p) for p in P]); ctr = (allp.min(0) + allp.max(0)) / 2
    d = np.array(cam_dir, float); d /= np.linalg.norm(d)
    eye = ctr + d * 2600
    f = (ctr - eye); f /= np.linalg.norm(f)
    r = np.cross(f, [0, 0, 1]); r /= np.linalg.norm(r); u = np.cross(r, f)
    light = np.array([-0.3, -0.8, 0.9]); light /= np.linalg.norm(light)
    tris, cols = [], []
    for p, c in zip(P, C):
        p = np.asarray(p, float)
        n = np.cross(p[1] - p[0], p[2] - p[0])
        if np.linalg.norm(n) < 1e-9 and len(p) > 3: n = np.cross(p[2] - p[0], p[3] - p[0])
        n = n / (np.linalg.norm(n) + 1e-12)
        if np.dot(n, eye - p.mean(0)) < 0: n = -n
        k = 0.45 + 0.55 * max(0.0, np.dot(n, light)) + 0.12 * max(0.0, np.dot(n, -f))
        col = np.clip(np.array(to_rgb(c)) * min(k, 1.15), 0, 1)
        for t in range(1, len(p) - 1):
            tris.append(np.array([p[0], p[t], p[t + 1]])); cols.append(col)
    tris = np.array(tris); cols = np.array(cols)
    rel = tris - eye
    x = rel @ r; y = rel @ u; z = rel @ f
    foc = 1.0 / np.tan(np.radians(11))
    sx = x / z * foc; sy = y / z * foc
    allx, ally = sx.ravel(), sy.ravel()
    sc = 0.9 * min(W2 / (allx.max() - allx.min()), H2 / (ally.max() - ally.min()))
    ox = W2 / 2 - sc * (allx.max() + allx.min()) / 2; oy = H2 / 2 + sc * (ally.max() + ally.min()) / 2
    px = ox + sc * sx; py = oy - sc * sy
    img = np.ones((H2, W2, 3)); zb = np.full((H2, W2), np.inf)
    for t in range(len(tris)):
        X, Y, Z = px[t], py[t], z[t]
        x0, x1 = int(max(0, np.floor(X.min()))), int(min(W2 - 1, np.ceil(X.max())))
        y0, y1 = int(max(0, np.floor(Y.min()))), int(min(H2 - 1, np.ceil(Y.max())))
        if x1 < x0 or y1 < y0: continue
        gx, gy = np.meshgrid(np.arange(x0, x1 + 1) + 0.5, np.arange(y0, y1 + 1) + 0.5)
        den = (Y[1] - Y[2]) * (X[0] - X[2]) + (X[2] - X[1]) * (Y[0] - Y[2])
        if abs(den) < 1e-9: continue
        a = ((Y[1] - Y[2]) * (gx - X[2]) + (X[2] - X[1]) * (gy - Y[2])) / den
        b = ((Y[2] - Y[0]) * (gx - X[2]) + (X[0] - X[2]) * (gy - Y[2])) / den
        cc = 1 - a - b
        m = (a >= -1e-6) & (b >= -1e-6) & (cc >= -1e-6)
        if not m.any(): continue
        zz = a * Z[0] + b * Z[1] + cc * Z[2]
        sub = zb[y0:y1 + 1, x0:x1 + 1]
        upd = m & (zz < sub)
        sub[upd] = zz[upd]
        img[y0:y1 + 1, x0:x1 + 1][upd] = cols[t]
    # outline via depth discontinuity
    zf = np.where(np.isinf(zb), zb[~np.isinf(zb)].max() * 1.5, zb)
    gxz = np.abs(np.diff(zf, axis=1, prepend=zf[:, :1])); gyz = np.abs(np.diff(zf, axis=0, prepend=zf[:1, :]))
    edge = (gxz + gyz) > 12
    img[edge] = img[edge] * 0.35
    im = Image.fromarray((img * 255).astype(np.uint8)).resize((W, H), Image.LANCZOS)
    a = np.asarray(im.convert("L")); ys, xs = np.where(a < 250); pad = 30
    im = im.crop((max(0, xs.min() - pad), max(0, ys.min() - pad), min(W, xs.max() + pad), min(H, ys.max() + pad)))
    im.save(fn)

render("handrail", OUT + "/sim3d_handrail.png", (0.75, -1.0, 0.45))
render("pole", OUT + "/sim3d_tiang.png", (0.75, -1.0, 0.45))
render("handrail", OUT + "/sim3d_handrail_belakang.png", (0.9, 1.0, 0.35))
render("pole", OUT + "/sim3d_tiang_belakang.png", (0.9, 1.0, 0.35))
render("handrail", OUT + "/sim3d_handrail_kiri.png", (-1.0, -0.35, 0.3))
render("pole", OUT + "/sim3d_tiang_kiri.png", (-1.0, -0.35, 0.3))
print("ok")
