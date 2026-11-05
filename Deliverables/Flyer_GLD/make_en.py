"""Buat versi English booklet OGI dari versi Indonesia (GLD EN sudah ditulis terpisah)."""
from pathlib import Path

D = Path(__file__).resolve().parent
s = (D / "Booklet_OGI_4hal.html").read_text(encoding="utf-8")
R = [
    ('lang="id"', 'lang="en"'),
    ('alt="Citra thermal kebocoran gas"', 'alt="Thermal image of a gas leak"'),
    ("GLD NEXT · KONSEP PENGEMBANGAN", "GLD NEXT · DEVELOPMENT CONCEPT"),
    ("Melihat kebocoran hidrokarbon yang tak kasatmata, dari titik ke area.", "Seeing invisible hydrocarbon leaks, from point to area."),
    ("PT Pertamina Patra Niaga (Fungsi Reliability)", "PT Pertamina Patra Niaga (Reliability Function)"),
    (">Ilustrasi 3D</div>", ">3D illustration</div>"),
    (">PRINSIP<", ">THE PRINCIPLE<"),
    ("Gas tak terlihat.<br>Kini tampak.", "Invisible gas.<br>Made visible."),
    ("Ikatan karbon-hidrogen menyerap radiasi inframerah di sekitar 3,3 µm. Kamera dengan filter spektral sempit pada pita itu menampilkan gas sebagai kontras terhadap latar.",
     "Carbon-hydrogen bonds absorb infrared radiation near 3.3 µm. A camera with a narrow spectral filter on that band renders the gas as contrast against the background."),
    ('alt="Struktur kamera MWIR berpendingin"', 'alt="Cooled MWIR camera structure"'),
    ("<b>Lensa MWIR</b><span>pita 3–5 µm</span>", "<b>MWIR optics</b><span>3–5 µm band</span>"),
    ("<b>Filter spektral</b><span>±3,3 µm, pita serapan C–H</span>", "<b>Spectral filter</b><span>~3.3 µm, C–H absorption band</span>"),
    ("<b>Detektor berpendingin</b>", "<b>Cooled detector</b>"),
    ("Ilustrasi 3D struktur umum kamera MWIR berpendingin.", "3D illustration of a generic cooled MWIR camera."),
    ("<b>Pita MWIR</b><p>Mid-Wave Infrared 3–5 µm, tempat hidrokarbon menyerap radiasi.</p>", "<b>MWIR band</b><p>Mid-Wave Infrared, 3–5 µm, where hydrocarbons absorb radiation.</p>"),
    ("<b>Filter sempit</b><p>Hanya meloloskan panjang gelombang serapan C–H.</p>", "<b>Narrow filter</b><p>Passes only the C–H absorption wavelength.</p>"),
    ("<b>Detektor dingin</b><p>Pendinginan menekan derau detektor, meningkatkan sensitivitas terhadap sinyal inframerah gas yang lemah.</p>", "<b>Cryogenic detector</b><p>Cooling reduces detector noise, improving sensitivity to weak infrared gas signatures.</p>"),
    (">SISTEM<", ">THE SYSTEM<"),
    ("Dari titik<br>ke area.", "From point<br>to area."),
    ("Kamera pada tiang ±10 m dengan pan-tilt berpatroli di sektor kritis: jalur pipa, manifold, dan klaster valve. Target jangkauan ±100 m.",
     "A pan-tilt camera on a ~10 m pole patrols critical sectors: pipe runs, manifolds and valve clusters. Target range ~100 m."),
    ('alt="Kamera OGI di lapangan"', 'alt="OGI camera in the field"'),
    ("<span>Kamera MWIR</span>", "<span>MWIR camera</span>"),
    ("<span>Edge server · AI segmentasi plume</span>", "<span>Edge server · AI plume segmentation</span>"),
    ("<b>GLD + OGI, satu sistem</b>", "<b>GLD + OGI, one system</b>"),
    ("<td>Gas apa &amp; seberapa pekat</td>", "<td>Which gas &amp; how concentrated</td>"),
    ("<td>Di mana &amp; ke arah mana menyebar</td>", "<td>Where it is &amp; which way it spreads</td>"),
    ("<td>Keduanya</td><td>Prioritas respons tertinggi</td>", "<td>Both</td><td>Highest response priority</td>"),
    ("<b>Alarm yang terkonfirmasi</b><p>Alarm dipicu hanya bila plume terdeteksi konsisten pada beberapa frame berturut-turut, sehingga gangguan flare dan pantulan panas ditekan.</p>",
     "<b>Confirmed alarms</b><p>An alarm is raised only when the plume is detected consistently over consecutive frames, suppressing flares and heat reflections.</p>"),
    ("Ilustrasi 3D konsep sistem.", "3D illustration of the system concept."),
    (">MELENGKAPI GLD<", ">COMPLEMENTING GLD<"),
    ("Melengkapi,<br>bukan menggantikan.", "Complementing,<br>not replacing."),
    ("<p>Pita Mid-Wave Infrared</p>", "<p>Mid-Wave Infrared band</p>"),
    ("<p>Suhu kerja detektor</p>", "<p>Detector operating temperature</p>"),
    ("<p>Target jangkauan visualisasi</p>", "<p>Target visualisation range</p>"),
    (">SPESIFIKASI TARGET<", ">TARGET SPECIFICATIONS<"),
    ("<td>Detektor</td><td>MCT berpendingin, 640 × 512 piksel</td>", "<td>Detector</td><td>Cooled MCT, 640 × 512 pixels</td>"),
    ("<td>Pemasangan</td><td>Tiang ±10 m, pan-tilt, patroli preset sektor</td>", "<td>Mounting</td><td>~10 m pole, pan-tilt, preset sector patrol</td>"),
    ("<td>Kecerdasan</td><td>Segmentasi plume di edge server, konfirmasi multi-frame</td>", "<td>Intelligence</td><td>Plume segmentation on edge server, multi-frame confirmation</td>"),
    ("<td>Validasi</td><td>Uji pelepasan gas terkontrol</td>", "<td>Validation</td><td>Controlled gas release tests</td>"),
    ("<td>Batasan</td><td>Sistem OGI yang diusulkan dioptimalkan untuk deteksi hidrokarbon pada ±3,3 µm dan tidak dirancang untuk mendeteksi H₂, CO, atau H₂S; dapat ditangani oleh sistem GLD.</td>", "<td>Limitations</td><td>The proposed OGI system is optimized for hydrocarbon detection near 3.3 µm and is not designed to detect H₂, CO, or H₂S; can be addressed by the GLD system.</td>"),
    (">ARAH PENGEMBANGAN<", ">ROADMAP<"),
    ("<p>Dirancang untuk direplikasi di seluruh kilang Pertamina.</p>", "<p>Designed for replication across Pertamina refineries.</p>"),
    ("<b>Emisi fugitif</b><p>Mendukung dokumentasi emisi fugitif.</p>", "<b>Fugitive emissions</b><p>Supports fugitive emission documentation.</p>"),
    ("<p>Termografi radiometrik: hot spot heater, isolasi rusak, steam trap.</p>", "<p>Radiometric thermography: heater hot spots, damaged insulation, steam traps.</p>"),
    ("Konsep pengembangan tahap berikutnya, belum termasuk ruang lingkup unit GLD saat ini. Spesifikasi merupakan target rancangan; seluruh gambar adalah ilustrasi 3D.",
     "Next-stage development concept, not part of the current GLD scope. Specifications are design targets; all images are 3D illustrations."),
    ("Lab Internet of Things<br>Institut Teknologi Bandung", "Internet of Things Laboratory<br>Institut Teknologi Bandung"),
]
for a, b in R:
    assert a in s, a
    s = s.replace(a, b)
(D / "Booklet_OGI_4hal_EN.html").write_text(s, encoding="utf-8")
print("ok")
