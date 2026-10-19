// Satu-satunya sumber timing & naskah video; ubah di sini saja.
// Dua bahasa dari satu timeline: `vo` (Indonesia, istilah teknis tetap bahasa Inggris) dan `voEn` (Inggris).
// Adegan 3/5/7/10 mengikuti panjang render 3D; adegan lain mengikuti narasi (cek: npm run vo:check).
export const FPS = 30;

export type SceneId =
  | 'hook'
  | 'problem'
  | 'intro'
  | 'fingerprint'
  | 'trainable'
  | 'mesh'
  | 'alarm'
  | 'field'
  | 'roadmap'
  | 'outro';

export type SceneDef = {
  id: SceneId;
  title: string;
  startSec: number;
  endSec: number;
  vo: string; // narasi Indonesia; dipakai juga sebagai subtitle
  voEn: string; // narasi Inggris
};

export const SCENES: SceneDef[] = [
  {
    id: 'hook',
    title: '01 Hook',
    startSec: 0,
    endSec: 8,
    vo: 'Kebocoran gas di kilang tidak kasatmata, dan setiap detik keterlambatan deteksi memperbesar risiko keselamatan.',
    voEn: 'Gas leaks in a refinery are invisible, and every second of delayed detection increases the safety risk.',
  },
  {
    id: 'problem',
    title: '02 Masalah',
    startSec: 8,
    endSec: 19,
    vo: 'Detektor konvensional umumnya dirancang untuk satu jenis gas dan bergantung pada kabel data menuju ruang kontrol, sehingga mahal dan sulit diperluas.',
    voEn: 'Conventional detectors are typically designed for a single gas and rely on data cables to the control room, which makes them costly and difficult to scale.',
  },
  {
    id: 'intro',
    title: '03 Perkenalan GLD',
    startSec: 19,
    endSec: 30,
    vo: 'GLD mengintegrasikan delapan sensor gas, data acquisition dua puluh empat bit, prosesor edge AI, dan radio LoRa dalam satu unit.',
    voEn: 'GLD integrates eight gas sensors, twenty-four-bit data acquisition, an edge AI processor, and a LoRa radio in a single unit.',
  },
  {
    id: 'fingerprint',
    title: '04 Sidik jari gas & model AI',
    startSec: 30,
    endSec: 65,
    vo: 'Sensor metal-oxide semiconductor tidak sepenuhnya selektif; satu sensor dapat merespons berbagai jenis gas. Keterbatasan tersebut justru dimanfaatkan sebagai keunggulan. Delapan sensor dengan sensitivitas berbeda membentuk satu vektor respons, layaknya sidik jari kimia, sesuai prinsip electronic nose. Convolutional Neural Network dua cabang mempelajari pola temporal sinyal sensor sekaligus profil sensitivitasnya, kemudian dikuantisasi ke delapan bit dan dijalankan langsung pada mikrokontroler sebagai edge AI, tanpa bergantung pada server.',
    voEn: 'Metal-oxide semiconductor sensors are not fully selective; a single sensor responds to many gases. GLD turns this limitation into an advantage. Eight sensors with different sensitivities form one response vector, a chemical fingerprint, following the electronic-nose principle. A dual-branch Convolutional Neural Network learns the temporal pattern of the sensor signals together with their sensitivity profile; the model is then quantized to eight bits and runs directly on the microcontroller as edge AI, with no dependence on a server.',
  },
  {
    id: 'trainable',
    title: '05 Dapat dilatih ulang',
    startSec: 65,
    endSec: 85,
    vo: 'Saat ini, model telah mengklasifikasikan udara bersih, LPG, dan hidrogen. Delapan sensor yang sama juga sensitif terhadap metana, karbon monoksida, amonia, dan benzena; model untuk gas tersebut dilatih ulang menggunakan portable test chamber di lokasi kilang.',
    voEn: 'At present, the model classifies clean air, LPG, and hydrogen. The same eight sensors are also sensitive to methane, carbon monoxide, ammonia, and benzene; models for these gases are retrained on site using a portable test chamber at the refinery.',
  },
  {
    id: 'mesh',
    title: '06 Private mesh LoRa',
    startSec: 85,
    endSec: 113,
    vo: 'Komunikasi menggunakan private mesh LoRa dua lapis pada pita sembilan ratus dua puluh megahertz. Node sensor terhubung ke Cluster Head, dan antar-Cluster Head membentuk jaringan multi-hop menuju gateway, tanpa internet dan terpisah dari jaringan TI kilang. Bila satu Cluster Head gagal, node tetangga memilih parent baru secara otomatis, dengan signal hysteresis dan loop prevention agar rute tetap stabil.',
    voEn: 'Communication runs on a private two-layer LoRa mesh in the nine-hundred-twenty megahertz band. Sensor nodes connect to Cluster Heads, and the Cluster Heads form a multi-hop network to the gateway, without internet access and separate from the refinery IT network. If a Cluster Head fails, neighbouring nodes automatically select a new parent, with signal hysteresis and loop prevention to keep the routes stable.',
  },
  {
    id: 'alarm',
    title: '07 Alarm otomatis',
    startSec: 113,
    endSec: 132,
    vo: 'Saat terjadi kebocoran, perubahan pola respons sensor langsung dikenali, dan GLD membunyikan alarm lokal. Data normal diambil secara berkala, sedangkan alarm dikirim segera melalui mekanisme push ke dashboard operator, lengkap dengan identitas sensor dan tingkat risikonya.',
    voEn: 'When a leak occurs, the change in the sensor response pattern is recognised immediately, and GLD triggers a local alarm. Normal data is polled periodically, while alarms are pushed instantly to the operator dashboard, together with the sensor identity and risk level.',
  },
  {
    id: 'field',
    title: '08 Teruji lapangan',
    startSec: 132,
    endSec: 153,
    vo: 'GLD telah melalui pengujian lapangan: generasi pertama diuji di RU VII Kasim pada Desember 2025. Generasi kedua lulus seluruh tujuh butir Factory Acceptance Test di laboratorium, serta pengujian multi-hop mesh, failover, dan push alarm pada delapan Cluster Head.',
    voEn: 'GLD has undergone field testing: the first generation was tested at RU VII Kasim in December 2025. The second generation passed all seven Factory Acceptance Test items in the laboratory, together with multi-hop mesh, failover, and push-alarm tests on eight Cluster Heads.',
  },
  {
    id: 'roadmap',
    title: '09 Pengembangan berikutnya',
    startSec: 153,
    endSec: 164,
    vo: 'Tahap pengembangan berikutnya adalah integrasi kamera thermal untuk pemantauan area, sebagai pelengkap deteksi titik GLD dalam satu dashboard terpadu.',
    voEn: 'The next development stage integrates thermal cameras for area monitoring, complementing GLD point detection within a single unified dashboard.',
  },
  {
    id: 'outro',
    title: '10 Penutup',
    startSec: 164,
    endSec: 178,
    vo: 'GLD: deteksi multigas berbasis edge AI dengan komunikasi self-healing. Dikembangkan di Indonesia untuk industri kilang nasional.',
    voEn: 'GLD: multi-gas detection powered by edge AI, with self-healing communication. Developed in Indonesia for the national refining industry.',
  },
];

export type Lang = 'id' | 'en';
export const voOf = (s: SceneDef, lang: Lang) => (lang === 'en' ? s.voEn : s.vo);

export const sec = (s: number) => Math.round(s * FPS);
export const sceneFrom = (d: SceneDef) => sec(d.startSec);
export const sceneDuration = (d: SceneDef) => sec(d.endSec - d.startSec);
export const TOTAL_FRAMES = sec(SCENES[SCENES.length - 1].endSec);
