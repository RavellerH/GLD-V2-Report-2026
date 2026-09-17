# -*- coding: utf-8 -*-
import base64, os

PHOTO_DIR = r"C:\Users\WIN10\Documents\GLD-V2-Report-2026\.tmp\cert_doc_photos"
OUT_PATH = r"C:\Users\WIN10\Documents\GLD-V2-Report-2026\Deliverables\Dokumen_Teknis_Sertifikasi_GLD_IECEx_ATEX.html"

def b64(fn):
    with open(os.path.join(PHOTO_DIR, fn), "rb") as f:
        return base64.b64encode(f.read()).decode("ascii")

photos = [
    ("3._Motherboard_ModulSensor_PenutupMesh_Casing_Antena_ModulAlarm.jpg",
     "Unit lengkap — tampak depan",
     "Node Sensor (GLD) terpasang lengkap: casing utama (biru) dengan penutup mesh sensor, antena LoRa eksternal, dan modul alarm visual (silinder, lampu merah) terpasang pada sisi kanan casing."),
    ("Casing_Belakang.jpg",
     "Unit lengkap — tampak belakang/samping",
     "Sudut pandang lain dari unit terakit: memperlihatkan posisi antena, modul alarm, dan sisi cable gland/kabel keluar dari casing."),
    ("PenutupMesh_Casing.jpg",
     "Unit lengkap — tampak depan (tanpa antena &amp; modul alarm)",
     "Casing utama dengan penutup mesh terpasang, sudut pandang datar menunjukkan bentuk enclosure dan 4 lubang baut dudukan (mounting)."),
    ("1._Motherboard_Casing.jpg",
     "Komponen utama — PCB (motherboard) dalam casing, sebelum modul sensor",
     "PCB utama terpasang di dalam casing, sebelum modul sensor gas dipasang. Terlihat mikrokontroler ESP32-S3-WROOM-1U, modul LoRa, dan rangkaian daya."),
    ("2._Motherboard_ModulSensor_Casing.jpg",
     "Komponen utama — PCB dengan 8 modul sensor gas terpasang",
     "PCB yang sama dengan 8 kanal sensor gas seri MQ (MQ-2, MQ-3B, MQ-4, MQ-5, MQ-6, MQ-7B, MQ-8, MQ-135) terpasang mengelilingi mikrokontroler pusat."),
    ("ModulAlarm.jpg",
     "Komponen utama — modul alarm visual (close-up)",
     "Modul alarm visual (beacon/strobe) berbahan logam silinder dengan lensa merah, terhubung ke casing utama melalui cable gland."),
    ("PenutupMesh.jpg",
     "Komponen utama — penutup mesh sensor (close-up)",
     "Penutup mesh/kasa logam yang melindungi elemen sensor gas sekaligus berfungsi sebagai jalur difusi gas ke sensor di baliknya."),
]

photo_cards = []
for fn, title, desc in photos:
    data = b64(fn)
    photo_cards.append(f'''<figure class="photo">
<img src="data:image/jpeg;base64,{data}" alt="{title}">
<figcaption><b>{title}</b><span>{desc}</span></figcaption>
</figure>''')

photos_html = "\n".join(photo_cards)

with open(".tmp/photos_block.html", "w", encoding="utf-8") as f:
    f.write(photos_html)

print("photo block bytes:", len(photos_html))
print("done, total b64 approx KB:", sum(len(b64(fn)) for fn,_,_ in photos)//1024)
