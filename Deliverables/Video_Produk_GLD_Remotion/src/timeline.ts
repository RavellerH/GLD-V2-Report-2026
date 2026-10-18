// Satu-satunya sumber timing video. Detik mengikuti
// Deliverables/Storyboard_Video_Produk_GLD_DigitalizationDay.md; ubah di sini saja.
export const FPS = 30;
export const WIDTH = 1920;
export const HEIGHT = 1080;

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
    endSec: 10,
    vo: 'Di kilang, kebocoran gas tidak terlihat dan tidak menunggu. Beberapa detik bisa menentukan segalanya.',
  },
  {
    id: 'problem',
    title: '02 Masalah',
    startSec: 10,
    endSec: 22,
    vo: 'Detektor konvensional umumnya hanya untuk satu jenis gas, dan perlu kabel data panjang ke ruang kontrol. Mahal, lambat dipasang, sulit diperluas.',
  },
  {
    id: 'intro',
    title: '03 Perkenalan GLD',
    startSec: 22,
    endSec: 35,
    vo: 'Kami memperkenalkan GLD: satu unit dengan delapan sensor gas, prosesor AI, dan radio LoRa dalam satu casing.',
  },
  {
    id: 'fingerprint',
    title: '04 Sidik jari gas',
    startSec: 35,
    endSec: 58,
    vo: 'Setiap gas meninggalkan pola unik pada delapan sensor, seperti sidik jari. Model AI yang berjalan langsung di dalam perangkat membaca pola itu dan mengenali jenis gasnya, tanpa perlu server untuk berpikir.',
  },
  {
    id: 'trainable',
    title: '05 Bisa diajari',
    startSec: 58,
    endSec: 70,
    vo: 'Dan GLD bisa terus belajar. Chamber uji portable kami bawa ke kilang, data diambil di tempat, lalu model diperbarui sesuai gas yang dibutuhkan di lokasi tersebut.',
  },
  {
    id: 'mesh',
    title: '06 Private mesh LoRa',
    startSec: 70,
    endSec: 95,
    vo: 'Data dikirim lewat jaringan mesh LoRa privat. Setiap Cluster Head meneruskan data, lompat demi lompat, sampai ke gateway, tanpa internet dan tanpa bergantung pada jaringan IT kilang. Jika satu titik mati, data otomatis mencari jalur lain.',
  },
  {
    id: 'alarm',
    title: '07 Alarm otomatis',
    startSec: 95,
    endSec: 108,
    vo: 'Begitu kebocoran terdeteksi, alarm langsung dikirim ke dashboard operator, lengkap dengan lokasi dan jenis gasnya.',
  },
  {
    id: 'outro',
    title: '08 Penutup',
    startSec: 108,
    endSec: 120,
    vo: 'GLD: satu perangkat, banyak gas, jaringan yang tak terputus. Teknologi deteksi kebocoran gas dari Indonesia, untuk kilang Indonesia.',
  },
];

export const sec = (s: number) => Math.round(s * FPS);
export const sceneFrom = (d: SceneDef) => sec(d.startSec);
export const sceneDuration = (d: SceneDef) => sec(d.endSec - d.startSec);
export const TOTAL_FRAMES = sec(SCENES[SCENES.length - 1].endSec);
