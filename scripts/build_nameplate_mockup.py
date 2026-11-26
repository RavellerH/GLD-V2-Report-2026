"""Mockup: nameplate GLD V2 ditempel di permukaan atas base (samping antena) pada foto unit."""
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "Sumber Dokumen/Foto_Assembly_GLD_07Okt2026/Nameplate_position_beside_antenna.jpg"
OUT = ROOT / "Paket Meeting TUV SUD 26November2026/Mockup_Nameplate_Position_GLD_V2.jpg"
FR, FB = r"C:\Windows\Fonts\arial.ttf", r"C:\Windows\Fonts\arialbd.ttf"

# ---------------------------------------------------------------- plate artwork (80 x 55 mm, 20 px/mm)
W, H = 1600, 1100
rng = np.random.default_rng(3)
base = np.full((H, W), 196.0)
base += np.repeat(rng.normal(0, 7, (1, W)), H, 0) * 0.6 + rng.normal(0, 4, (H, W))  # brushed steel
base += np.linspace(10, -14, W)[None, :]
plate = Image.fromarray(np.clip(np.stack([base, base + 2, base + 5], -1), 0, 255).astype("uint8"))
mask = Image.new("L", (W, H), 0); ImageDraw.Draw(mask).rounded_rectangle([0, 0, W - 1, H - 1], 70, fill=255)
d = ImageDraw.Draw(plate)
d.rounded_rectangle([30, 30, W - 31, H - 31], 50, outline=(40, 40, 45), width=6)
for x, y in ((90, 90), (W - 90, 90), (90, H - 90), (W - 90, H - 90)):
    d.ellipse([x - 26, y - 26, x + 26, y + 26], fill=(150, 150, 155), outline=(80, 80, 85), width=4)
    d.ellipse([x - 9, y - 9, x + 9, y + 9], fill=(110, 110, 115))
ink = (25, 25, 30)
f = lambda s, b=False: ImageFont.truetype(FB if b else FR, s)
y = 120
d.text((170, y), "[Manufacturer name and address]", font=f(56, True), fill=ink); y += 100
d.text((170, y), "GAS LEAK DETECTOR   Model: GLD V2", font=f(72, True), fill=ink); y += 112
d.text((170, y), "S/N: GLD2-0x________     Year: ______", font=f(54), fill=ink); y += 110
# Ex hexagon
cx, cy, r = 225, y + 52, 58
hexpts = [(cx + r * np.cos(np.radians(a)), cy + r * np.sin(np.radians(a))) for a in range(0, 360, 60)]
d.polygon(hexpts, outline=ink, width=7)
d.text((cx, cy + 2), "Ex", font=f(52, True), fill=ink, anchor="mm")
d.text((310, y), "II 2G   Ex db IIC T4 Gb", font=f(86, True), fill=ink)
y += 140
d.text((170, y), "−20 °C ≤ Ta ≤ +60 °C      IP66", font=f(58), fill=ink)
d.text((W - 170, y - 4), "CE xxxx", font=f(64, True), fill=ink, anchor="ra"); y += 88
d.text((170, y), "24 VDC, 8 W max.      Cable entry M20 × 1.5", font=f(58), fill=ink); y += 88
d.text((170, y), "ATEX: ______________     IECEx: ______________", font=f(54), fill=ink); y += 100
d.text((170, y), "WARNING – DO NOT OPEN WHEN AN EXPLOSIVE", font=f(54, True), fill=ink); y += 66
d.text((170, y), "ATMOSPHERE MAY BE PRESENT", font=f(54, True), fill=ink)
plate.putalpha(mask)

# ---------------------------------------------------------------- perspective onto top face
photo = Image.open(SRC).convert("RGB")
s = photo.width / 525.0  # koordinat diukur pada pratinjau lebar 525 px
dst = [(347, 293), (467, 318), (453, 392), (318, 363)]  # TL, TR, BR, BL
dst = [(x * s, y * s) for x, y in dst]
srcpts = [(0, 0), (W, 0), (W, H), (0, H)]


def coeffs(out_pts, in_pts):
    A, B = [], []
    for (x, y), (u, v) in zip(out_pts, in_pts):
        A += [[x, y, 1, 0, 0, 0, -u * x, -u * y], [0, 0, 0, x, y, 1, -v * x, -v * y]]
        B += [u, v]
    return np.linalg.solve(np.array(A, float), np.array(B, float))


warped = plate.transform(photo.size, Image.PERSPECTIVE, coeffs(dst, srcpts), Image.BICUBIC)
alpha = warped.split()[3].filter(ImageFilter.GaussianBlur(1.2))
# bayangan tipis di bawah pelat
shadow = Image.new("L", photo.size, 0)
ImageDraw.Draw(shadow).polygon([(x + 6, y + 10) for x, y in dst], fill=110)
shadow = shadow.filter(ImageFilter.GaussianBlur(10))
photo = Image.composite(Image.new("RGB", photo.size, (15, 35, 70)), photo, shadow)
# sesuaikan cahaya: sedikit lebih gelap ke arah depan
rgb = warped.convert("RGB")
grad = Image.linear_gradient("L").resize(photo.size)
rgb = Image.composite(rgb.point(lambda v: int(v * 0.88)), rgb, grad)
photo.paste(rgb, (0, 0), alpha)
photo.save(OUT, quality=92)
pv = photo.copy(); pv.thumbnail((1000, 1000)); pv.save(OUT.with_name("_preview_nameplate.jpg"))
print(OUT)

# ---------------------------------------------------------------- figure untuk dokumen: foto utuh + detail
full = Image.open(OUT).convert("RGB")
left = full.resize((1200, 1600))
xs = [p[0] for p in dst]; ys = [p[1] for p in dst]
pad = 0.35 * (max(xs) - min(xs))
box = (int(min(xs) - pad), int(min(ys) - pad * 0.8), int(max(xs) + pad * 0.5), int(max(ys) + pad * 0.8))
det = full.crop(box); det = det.resize((1200, int(1200 * det.height / det.width)))
fig = Image.new("RGB", (2440, 1600), "white")
fig.paste(left, (0, 0)); fig.paste(det, (1240, (1600 - det.height) // 2))
dr = ImageDraw.Draw(fig); k = 1200 / full.width
dr.rectangle([box[0] * k, box[1] * k, box[2] * k, box[3] * k], outline=(192, 96, 26), width=6)
dr.rectangle([1240, (1600 - det.height) // 2, 2439, (1600 + det.height) // 2], outline=(192, 96, 26), width=6)
FIG = ROOT / "scripts/assets/tuv_sud_gmi/nameplate_mockup_figure.jpg"
fig.save(FIG, quality=90)
print(FIG)
