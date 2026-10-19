"""Isi formulir resmi TTH TLKM02/F/013 v02 langsung di atas PDF aslinya
(logo, watermark, footer TTH tetap utuh). Atas nama PT LAPI Ganesha Utama,
pemohon & TTD Dr. Nina Siti Aminah. Output:
Deliverables/Permohonan_Uji_CT_TTH_EMC_GLD_LGU.pdf
"""
import io
from pathlib import Path

from pypdf import PdfReader, PdfWriter
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "Sumber Dokumen" / "Telkom Test House" / "TLKM02F013_v2_Permohonan_Uji_Conformance_Test_CT_template.pdf"
SIGNATURE = ROOT / "scripts" / "assets" / "ttd_nina_siti_aminah.png"
OUT = ROOT / "Deliverables" / "Permohonan_Uji_CT_TTH_EMC_GLD_LGU.pdf"
H = 792  # tinggi halaman (pt); koordinat di bawah = dari atas, seperti pdftotext -bbox

FONT, BOLD = "Helvetica", "Helvetica-Bold"


def text(c, x, y_top, s, size=8.5, font=FONT, center=False):
    c.setFont(font, size)
    (c.drawCentredString if center else c.drawString)(x, H - y_top, s)


def white_out(c, x0, y0, x1, y1):
    c.setFillColorRGB(1, 1, 1)
    c.rect(x0 - 1, H - y1 - 1, x1 - x0 + 2, y1 - y0 + 2, stroke=0, fill=1)
    c.setFillColorRGB(0, 0, 0)


def page1(c):
    white_out(c, 465.4, 96.8, 511.9, 107.2)  # RCT-YYXXX dikosongkan (diisi TTH)
    # Data Pelanggan (baseline sedikit di atas garis isian)
    text(c, 168, 149, "PT LAPI Ganesha Utama")
    text(c, 168, 164, "Jl. Dederuk No. 30, Kel. Sadang Serang, Kec. Coblong, Kota Bandung 40133", 8)
    text(c, 168, 179, "Dr. Nina Siti Aminah")
    text(c, 168, 194.5, "081214295251")
    text(c, 168, 209.5, "nina@itb.ac.id")
    # Data Perangkat (2 unit)
    text(c, 168, 254.5, "Gas Leak Detection (GLD): (1) Node Sensor GLD  &  (2) LoRa Cluster Head", 8)
    text(c, 168, 270, "GLD (prototipe)", 8)
    text(c, 398, 270, "(1) GLD V2  /  (2) CH V2", 8)
    text(c, 168, 285.5, "LoRa 920/921 MHz, maks. 22 dBm", 7)
    text(c, 398, 285.5, "(1) GLD-V2-001  /  (2) CH-V3-003", 7)
    text(c, 168, 301.5, "Indonesia", 8)
    text(c, 398, 301.5, "EMC: emisi radiasi & konduksi", 7)
    # Agenda CT: Lainnya
    text(c, 74.2, 433.2, "X", 10, BOLD)
    text(c, 152, 448.5, "Sewa chamber (semi-anechoic) untuk uji EMC radiated & conducted emission", 8)
    text(c, 93, 462, "pada prototipe Node Sensor GLD dan LoRa Cluster Head (2 unit), sebagai data pendukung sertifikasi.", 8)
    # Periode CT
    text(c, 168, 532, "1 (satu) hari kerja")
    text(c, 168, 546.5, "Kamis, 15 Oktober 2026")


def page2(c):
    white_out(c, 247.2, 244.6, 336, 255.1)
    text(c, 291.6, 253, "Bandung, 19 Oktober 2026", 9, center=True)
    # TTD pemohon menggantikan label "Tanda tangan"
    white_out(c, 103.1, 302.7, 159.3, 313.1)
    img = ImageReader(str(SIGNATURE))
    iw, ih = img.getSize()
    h = 46
    w = h * iw / ih
    c.drawImage(img, 131.2 - w / 2, H - 336, w, h, mask="auto")
    white_out(c, 92.7, 341.8, 169.7, 352.2)
    text(c, 131.2, 350.5, "Dr. Nina Siti Aminah", 9, center=True)
    # placeholder nama TTH dikosongkan (diisi TTH)
    white_out(c, 236.8, 341.8, 345.1, 353.6)
    white_out(c, 398.9, 341.8, 479.9, 353.6)


def main():
    reader = PdfReader(str(TEMPLATE))
    writer = PdfWriter()
    for i, page in enumerate(reader.pages):
        buf = io.BytesIO()
        c = canvas.Canvas(buf, pagesize=(612, H))
        (page1 if i == 0 else page2)(c)
        c.save()
        buf.seek(0)
        page.merge_page(PdfReader(buf).pages[0])
        writer.add_page(page)
    writer.add_metadata({"/Title": "Permohonan Uji Conformance Test (CT) - GLD - PT LAPI Ganesha Utama",
                         "/Author": "PT LAPI Ganesha Utama"})
    with open(OUT, "wb") as f:
        writer.write(f)
    print(OUT)


if __name__ == "__main__":
    main()
