// Satu-satunya sumber timing video; ubah di sini saja.
// Slot = durasi narasi Gemini TTS (suara Erinome) + jeda, dibulatkan ke atas.
// 01-04 dari WAV final; 05-08 masih estimasi (±13,3 huruf/dtk), cek ulang dengan `npm run vo:check`.
export const FPS = 30;

export type SceneId = 'hook' | 'problem' | 'intro' | 'fingerprint' | 'trainable' | 'mesh' | 'alarm' | 'outro';

export type SceneDef = {
  id: SceneId;
  title: string;
  startSec: number;
  endSec: number;
  vo: string; // narasi; dipakai juga sebagai subtitle
};

export const SCENES: SceneDef[] = [
  {
    id: 'hook',
    title: '01 Hook',
    startSec: 0,
    endSec: 8,
    vo: 'Kebocoran gas di kilang tidak kasatmata, dan setiap detik keterlambatan deteksi memperbesar risiko keselamatan.',
  },
  {
    id: 'problem',
    title: '02 Masalah',
    startSec: 8,
    endSec: 21,
    vo: 'Detektor konvensional umumnya dirancang untuk satu jenis gas dan bergantung pada kabel data menuju ruang kontrol, sehingga mahal dan sulit diperluas.',
  },
  {
    id: 'intro',
    title: '03 Perkenalan GLD',
    startSec: 21,
    endSec: 32,
    vo: 'GLD mengintegrasikan delapan sensor gas, akuisisi data dua puluh empat bit, prosesor AI tertanam, dan radio LoRa dalam satu unit.',
  },
  {
    id: 'fingerprint',
    title: '04 Sidik jari gas & model AI',
    startSec: 32,
    endSec: 72,
    vo: 'Sensor semikonduktor oksida logam tidak sepenuhnya selektif; satu sensor dapat bereaksi terhadap banyak gas. Keterbatasan tersebut justru dimanfaatkan sebagai keunggulan. Delapan sensor dengan sensitivitas berbeda membentuk satu vektor respons, layaknya sidik jari kimia, sesuai prinsip hidung elektronik. Jaringan saraf konvolusional dua cabang mempelajari pola temporal sinyal sensor sekaligus profil sensitivitasnya, kemudian dikuantisasi ke delapan bit dan dijalankan langsung di mikrokontroler, tanpa bergantung pada server.',
  },
  {
    id: 'trainable',
    title: '05 Dapat dilatih ulang',
    startSec: 72,
    endSec: 92,
    vo: 'Saat ini, model telah mengklasifikasikan udara bersih, LPG, dan hidrogen. Delapan sensor yang sama juga sensitif terhadap metana, karbon monoksida, amonia, dan benzena; model untuk gas tersebut dilatih ulang menggunakan chamber uji portabel di lokasi kilang.',
  },
  {
    id: 'mesh',
    title: '06 Private mesh LoRa',
    startSec: 92,
    endSec: 124,
    vo: 'Komunikasi menggunakan jaringan mesh LoRa privat dua lapis pada pita sembilan ratus dua puluh megahertz. Node sensor terhubung ke Cluster Head, dan antar-Cluster Head membentuk mesh multi-hop menuju gateway, tanpa internet dan terpisah dari jaringan TI kilang. Bila satu Cluster Head gagal, node tetangga memilih induk baru secara otomatis, dengan histeresis sinyal dan pencegahan loop agar rute tetap stabil.',
  },
  {
    id: 'alarm',
    title: '07 Alarm otomatis',
    startSec: 124,
    endSec: 137,
    vo: 'Data normal diambil secara berkala, sedangkan alarm dikirim segera melalui mekanisme push ke dashboard operator, lengkap dengan identitas sensor dan tingkat risikonya.',
  },
  {
    id: 'outro',
    title: '08 Penutup',
    startSec: 137,
    endSec: 151,
    vo: 'GLD: deteksi multigas berbasis kecerdasan buatan di tepi jaringan, dengan komunikasi yang memulihkan dirinya sendiri. Dikembangkan di Indonesia untuk industri kilang nasional.',
  },
];

export const sec = (s: number) => Math.round(s * FPS);
export const sceneFrom = (d: SceneDef) => sec(d.startSec);
export const sceneDuration = (d: SceneDef) => sec(d.endSec - d.startSec);
export const TOTAL_FRAMES = sec(SCENES[SCENES.length - 1].endSec);
