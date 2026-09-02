from pathlib import Path

from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader


render_dir = Path(r"C:\Users\WIN10\Documents\GLD-V2-Report-2026\.tmp\datasheet_fix\pptx_render")
output = Path(r"C:\Users\WIN10\Documents\GLD-V2-Report-2026\Deliverables\Datasheet_Sistem_GLD_Slides.pdf")
slides = sorted(render_dir.glob("slide-*.png"))
if not slides:
    raise SystemExit("No rendered slide PNGs found")

page_w, page_h = 960, 540
pdf = canvas.Canvas(str(output), pagesize=(page_w, page_h), pageCompression=1)
pdf.setTitle("Datasheet Sistem GLD — Rev 0.8")
pdf.setAuthor("LAPI Ganesha Utama / Lab IoT & Fisika ITB")
for slide in slides:
    pdf.drawImage(ImageReader(str(slide)), 0, 0, width=page_w, height=page_h)
    pdf.showPage()
pdf.save()
print(f"Wrote {output} with {len(slides)} pages")
