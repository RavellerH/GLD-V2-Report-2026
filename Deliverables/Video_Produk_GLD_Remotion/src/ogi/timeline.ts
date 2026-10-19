// Video "GLD Next: Optical Gas Imaging MWIR" (konsep pengembangan, untuk pameran).
// Satu-satunya sumber timing & naskah video ini; format sama dengan src/timeline.ts (dibaca tools/vo.py).
import type {SceneDef} from '../timeline';

export type OgiSceneId =
  | 'ogi_hook'
  | 'ogi_stakes'
  | 'ogi_today'
  | 'ogi_physics'
  | 'ogi_cooled'
  | 'ogi_field'
  | 'ogi_edgeai'
  | 'ogi_fusion'
  | 'ogi_limits'
  | 'ogi_strategy'
  | 'ogi_outro';

export const OGI_SCENES: (Omit<SceneDef, 'id'> & {id: OgiSceneId})[] = [
  {
    id: 'ogi_hook',
    title: '01 Pembuka',
    startSec: 0,
    endSec: 10,
    vo: 'Kilang beroperasi tanpa henti. Kebocoran hidrokarbon tidak kasatmata, dan tidak selalu mengalir menuju sensor.',
    voEn: 'A refinery never stops. Hydrocarbon leaks are invisible, and they do not always drift towards a sensor.',
  },
  {
    id: 'ogi_stakes',
    title: '02 Mengapa penting',
    startSec: 10,
    endSec: 31,
    vo: 'Setiap kebocoran membawa tiga risiko sekaligus: keselamatan pekerja dan aset, keberlangsungan operasi, serta emisi. Metana, komponen utama gas proses, memiliki potensi pemanasan global hampir tiga puluh kali karbon dioksida.',
    voEn: 'Every leak carries three risks at once: the safety of people and assets, operational continuity, and emissions. Methane, a major component of process gas, has a global warming potential nearly thirty times that of carbon dioxide.',
  },
  {
    id: 'ogi_today',
    title: '03 GLD hari ini',
    startSec: 31,
    endSec: 53,
    vo: 'GLD telah menghadirkan deteksi titik berbasis edge AI: mengenali jenis gas langsung di perangkat dan mengirim alarm melalui private mesh LoRa. Namun, sensor titik hanya mendeteksi gas yang mencapai lokasinya; hasilnya bergantung pada arah angin dan jarak sumber kebocoran.',
    voEn: 'GLD already delivers point detection powered by edge AI: it identifies the gas type directly on the device and sends alarms over a private LoRa mesh. However, a point sensor only detects gas that reaches its location; the result depends on wind direction and the distance to the leak source.',
  },
  {
    id: 'ogi_physics',
    title: '04 Prinsip fisika OGI',
    startSec: 53,
    endSec: 79,
    vo: 'Optical Gas Imaging memanfaatkan sifat molekul hidrokarbon: ikatan karbon-hidrogen menyerap radiasi inframerah pada panjang gelombang sekitar tiga koma tiga mikrometer, dalam pita Mid-Wave Infrared. Dengan filter spektral sempit pada pita tersebut, gas yang semula tak terlihat tampak sebagai kontras terhadap radiasi latar belakang.',
    voEn: 'Optical Gas Imaging exploits a property of hydrocarbon molecules: the carbon-hydrogen bond absorbs infrared radiation at a wavelength of about three point three micrometres, within the Mid-Wave Infrared band. With a narrow spectral filter on that band, an otherwise invisible gas appears as contrast against the background radiation.',
  },
  {
    id: 'ogi_cooled',
    title: '05 Detektor berpendingin',
    startSec: 79,
    endSec: 97,
    vo: 'Agar kontras sekecil itu terdeteksi, detektor didinginkan hingga sekitar minus seratus sembilan puluh enam derajat Celsius. Derau termal sensor menjadi jauh lebih rendah daripada sinyal gas, sehingga kebocoran kecil pun dapat divisualisasikan.',
    voEn: 'To detect such a small contrast, the detector is cooled to about minus one hundred ninety-six degrees Celsius. The thermal noise of the sensor falls far below the gas signal, so that even small leaks can be visualised.',
  },
  {
    id: 'ogi_field',
    title: '06 Sistem kamera di lapangan',
    startSec: 97,
    endSec: 117,
    vo: 'Kamera dipasang pada tiang sekitar sepuluh meter dengan pan-tilt, berpatroli pada beberapa preset sektor kritis: jalur pipa, manifold, dan klaster valve. Target jangkauan visualisasi sekitar seratus meter, yang divalidasi melalui uji pelepasan gas terkontrol.',
    voEn: 'The camera is mounted on a pole of about ten metres with pan-tilt, patrolling several presets over critical sectors: pipe runs, manifolds, and valve clusters. The target visualisation range is about one hundred metres, to be validated through controlled gas release tests.',
  },
  {
    id: 'ogi_edgeai',
    title: '07 Edge AI',
    startSec: 117,
    endSec: 135,
    vo: 'Di edge server, model deep learning melakukan segmentasi plume secara otomatis. Alarm hanya dipicu bila plume terdeteksi konsisten pada beberapa frame berturut-turut, sehingga gangguan dari flare atau pantulan panas dapat ditekan.',
    voEn: 'On the edge server, a deep learning model segments the plume automatically. An alarm is raised only when the plume is detected consistently over several consecutive frames, suppressing interference from flares or heat reflections.',
  },
  {
    id: 'ogi_fusion',
    title: '08 Satu sistem GLD dan OGI',
    startSec: 135,
    endSec: 152,
    vo: 'GLD menjawab gas apa dan seberapa pekat; kamera OGI menjawab di mana dan ke arah mana gas menyebar. Bila keduanya mendeteksi pada waktu dan lokasi yang sama, sistem menetapkan prioritas tertinggi untuk respons lapangan.',
    voEn: 'GLD answers which gas and how concentrated; the OGI camera answers where it is and which way it is spreading. When both detect at the same time and location, the system assigns the highest priority for field response.',
  },
  {
    id: 'ogi_limits',
    title: '09 Batasan dan validasi',
    startSec: 152,
    endSec: 170,
    vo: 'Kinerja OGI dipengaruhi kontras termal, angin, laju kebocoran, dan garis pandang; hidrogen, karbon monoksida, dan hidrogen sulfida tidak tampak pada pita ini. Karena itu, kamera melengkapi GLD, bukan menggantikannya.',
    voEn: 'OGI performance depends on thermal contrast, wind, leak rate, and line of sight; hydrogen, carbon monoxide, and hydrogen sulphide are not visible in this band. The camera therefore complements GLD rather than replacing it.',
  },
  {
    id: 'ogi_strategy',
    title: '10 Nilai strategis dan roadmap',
    startSec: 170,
    endSec: 190,
    vo: 'Dirancang modular untuk direplikasi di seluruh kilang Pertamina, sistem ini juga mendukung dokumentasi emisi fugitif. Pada tahap berikutnya, kamera termografi radiometrik berpotensi diperluas untuk predictive maintenance: hot spot heater, isolasi rusak, dan steam trap.',
    voEn: 'Designed to be modular and replicated across all Pertamina refineries, the system also supports the documentation of fugitive emissions. In a later stage, radiometric thermography cameras could be extended to predictive maintenance: heater hot spots, damaged insulation, and steam traps.',
  },
  {
    id: 'ogi_outro',
    title: '11 Penutup',
    startSec: 190,
    endSec: 202,
    vo: 'Dari deteksi titik menuju pemantauan area. Dikembangkan oleh Lab Internet of Things, Institut Teknologi Bandung.',
    voEn: 'From point detection to area monitoring. Developed by the Internet of Things Laboratory, Institut Teknologi Bandung.',
  },
];
