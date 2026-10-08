# -*- coding: utf-8 -*-
"""Add the LGU Wi-Fi router to Pertamina's RU IV scope block diagram (8 Oct 2026 version).

Input : Sumber Dokumen/Pertamina RU IV 8Okt2026/block_diagram_scope_rev_8Okt2026.jpg
Output: Deliverables/Block_Diagram_Lingkup_RU-IV_dengan_Router_LGU.png
Redraws the BUILDING section: Gateway -(Wi-Fi 2.4 GHz)-> Router (LGU) -(LAN Cat6)-> Server -> IT Network,
UPS feeding Gateway (5VDC via adaptor), Router (adaptor) and Server (220VAC); adds legend item 7.
"""
import os
from PIL import Image, ImageDraw, ImageFont

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(REPO, "Sumber Dokumen", "Pertamina RU IV 8Okt2026", "block_diagram_scope_rev_8Okt2026.jpg")
OUT = os.path.join(REPO, "Deliverables", "Block_Diagram_Lingkup_RU-IV_dengan_Router_LGU.png")

SC = 2  # work at 2x for cleaner text
im = Image.open(SRC).convert("RGB")
im = im.resize((im.width * SC, im.height * SC), Image.LANCZOS)
d = ImageDraw.Draw(im)
s = lambda *v: tuple(int(x * SC) for x in v)

BG = (254, 242, 197)
LGU = (207, 232, 252)
LGU_EDGE = (60, 120, 200)
INK = (25, 25, 25)
RED = (220, 30, 30)
BLUE = (30, 150, 225)
F = "/usr/share/fonts/truetype/crosextra/Carlito-Bold.ttf"
FR = "/usr/share/fonts/truetype/crosextra/Carlito-Regular.ttf"
fb = lambda n: ImageFont.truetype(F, n * SC)
fr = lambda n: ImageFont.truetype(FR, n * SC)

# clear building area to the right of the gateway dashed box, and below it
d.rectangle(s(878, 150, 1250, 470), fill=BG)
d.rectangle(s(690, 292, 878, 470), fill=BG)


def box(x0, y0, x1, y1, title, sub=None, fill="white", edge=INK, tsize=19):
    d.rectangle(s(x0, y0, x1, y1), fill=fill, outline=edge, width=2 * SC)
    cx = (x0 + x1) / 2
    if sub:
        d.text(s(cx, (y0 + y1) / 2 - 9), title, font=fb(tsize), fill=INK, anchor="mm")
        d.text(s(cx, (y0 + y1) / 2 + 12), sub, font=fr(13), fill=INK, anchor="mm")
    else:
        d.text(s(cx, (y0 + y1) / 2), title, font=fb(tsize), fill=INK, anchor="mm")


def arrow(x0, y0, x1, y1, col, dashed=False, w=2.5):
    if dashed:
        n = int(abs(x1 - x0) // 9) or 1
        for i in range(n):
            a = x0 + (x1 - x0) * i / n
            b = x0 + (x1 - x0) * (i + 0.55) / n
            d.line(s(a, y0, b, y1), fill=col, width=int(w * SC))
    else:
        d.line(s(x0, y0, x1, y1), fill=col, width=int(w * SC))
    # head
    if x1 != x0:
        dr = 1 if x1 > x0 else -1
        d.polygon([s(x1, y1), s(x1 - 10 * dr, y1 - 6), s(x1 - 10 * dr, y1 + 6)], fill=col)
    else:
        dr = 1 if y1 > y0 else -1
        d.polygon([s(x1, y1), s(x1 - 6, y1 - 10 * dr), s(x1 + 6, y1 - 10 * dr)], fill=col)


# boxes
box(893, 200, 1003, 278, "Router", "Wi-Fi 2.4 GHz", fill=LGU, edge=INK)
d.text(s(948, 290), "(Provided by LGU)", font=fr(12), fill=INK, anchor="mm")
box(1030, 203, 1120, 272, "Server")
box(1140, 203, 1240, 272, "IT Network", tsize=17)
box(760, 375, 1120, 440, "UPS", tsize=21)

# data paths
arrow(864, 239, 891, 239, BLUE, dashed=True)          # Gateway -> Router (Wi-Fi)
d.text(s(880, 222), "Wi-Fi", font=fb(12), fill=BLUE, anchor="mm")
arrow(1004, 239, 1028, 239, BLUE)                      # Router -> Server (LAN)
d.text(s(1016, 211), "LAN", font=fb(12), fill=BLUE, anchor="mm")
d.text(s(1016, 224), "Cat6", font=fb(12), fill=BLUE, anchor="mm")
arrow(1121, 239, 1138, 239, BLUE)                      # Server -> IT network

# power paths from UPS
arrow(787, 374, 787, 280, RED)
d.text(s(800, 330), "5VDC", font=fb(14), fill=INK, anchor="lm")
d.text(s(800, 347), "(adaptor)", font=fr(12), fill=INK, anchor="lm")
arrow(948, 374, 948, 299, RED)
d.text(s(958, 340), "Adaptor", font=fb(13), fill=INK, anchor="lm")
arrow(1075, 374, 1075, 274, RED)
d.text(s(1083, 330), "220VAC", font=fb(14), fill=INK, anchor="lm")

im = im.resize((im.width // SC, im.height // SC), Image.LANCZOS)

# legend item 7 + note (extend canvas at the bottom)
W, H = im.size
out = Image.new("RGB", (W, H + 40), "white")
out.paste(im, (0, 0))
d2 = ImageDraw.Draw(out)
d2.text((24, H + 8), "7.   Router Wi-Fi 2.4 GHz (Provided by LGU): Gateway → Router via Wi-Fi, Router → Server via LAN Cat6; "
        "lokal tanpa internet. Adaptor 5VDC Gateway & adaptor Router dari UPS.",
        font=ImageFont.truetype(FR, 15), fill=INK)
os.makedirs(os.path.dirname(OUT), exist_ok=True)
out.save(OUT)
print("written", OUT, out.size)
