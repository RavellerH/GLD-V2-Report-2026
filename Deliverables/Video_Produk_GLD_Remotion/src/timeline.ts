// Satu-satunya sumber timing video. Detik mengikuti
// Deliverables/Storyboard_Video_Produk_GLD_DigitalizationDay.md; ubah di sini saja.
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
    endSec: 7,
    vo: 'Kebocoran gas di kilang tidak kasatmata, dan setiap detik keterlambatan deteksi memperbesar risiko keselamatan.',
  },
  {
    id: 'problem',
    title: '02 Masalah',
    startSec: 7,
    endSec: 17,
    vo: 'Detektor konvensional umumnya dirancang untuk satu jenis gas dan bergantung pada kabel data menuju ruang kontrol, sehingga mahal dan sulit diperluas.',
  },
  {
    id: 'intro',
    title: '03 Perkenalan GLD',
    startSec: 17,
    endSec: 26,
    vo: 'GLD mengintegrasikan delapan sensor gas, akuisisi data dua puluh empat bit, prosesor ESP32-S3, dan radio LoRa dalam satu unit.',
  },
  {
    id: 'fingerprint',
    title: '04 Sidik jari gas & model AI',
    startSec: 26,
    endSec: 55,
    vo: 'Sensor semikonduktor oksida logam tidak sepenuhnya selektif; satu sensor dapat bereaksi terhadap banyak gas. Keterbatasan ini justru kami manfaatkan. Delapan sensor dengan sensitivitas berbeda membentuk satu vektor respons, layaknya sidik jari kimia, sesuai prinsip hidung elektronik. Jaringan saraf konvolusional dua cabang mempelajari pola temporal sinyal sensor sekaligus profil sensitivitasnya, kemudian dikuantisasi ke delapan bit dan dijalankan langsung di mikrokontroler, tanpa bergantung pada server.',
  },
  {
    id: 'trainable',
    title: '05 Dapat dilatih ulang',
    startSec: 55,
    endSec: 71,
    vo: 'Saat ini model mengenali udara bersih, LPG, dan hidrogen. Larik sensor yang sama juga peka terhadap metana, karbon monoksida, amonia, dan benzena; model untuk gas tersebut dilatih ulang dengan chamber uji portabel di lokasi kilang.',
  },
  {
    id: 'mesh',
    title: '06 Private mesh LoRa',
    startSec: 71,
    endSec: 100,
    vo: 'Komunikasi menggunakan jaringan mesh LoRa privat dua lapis pada pita sembilan ratus dua puluh megahertz. Node sensor terhubung ke Cluster Head, dan antar-Cluster Head membentuk mesh multi-hop menuju gateway, tanpa internet dan terpisah dari jaringan TI kilang. Bila satu Cluster Head gagal, node tetangga memilih induk baru secara otomatis, dengan histeresis sinyal dan pencegahan loop agar rute tetap stabil.',
  },
  {
    id: 'alarm',
    title: '07 Alarm otomatis',
    startSec: 100,
    endSec: 110,
    vo: 'Data normal diambil secara berkala, sedangkan alarm dikirim segera melalui mekanisme push ke dashboard operator, lengkap dengan identitas sensor dan tingkat risikonya.',
  },
  {
    id: 'outro',
    title: '08 Penutup',
    startSec: 110,
    endSec: 120,
    vo: 'GLD: deteksi multigas berbasis kecerdasan buatan di tepi jaringan, dengan komunikasi yang memulihkan dirinya sendiri. Dikembangkan di Indonesia, untuk kilang Indonesia.',
  },
];

export const sec = (s: number) => Math.round(s * FPS);
export const sceneFrom = (d: SceneDef) => sec(d.startSec);
export const sceneDuration = (d: SceneDef) => sec(d.endSec - d.startSec);
export const TOTAL_FRAMES = sec(SCENES[SCENES.length - 1].endSec);
