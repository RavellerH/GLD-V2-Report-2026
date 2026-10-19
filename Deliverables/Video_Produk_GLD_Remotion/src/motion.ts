import {Easing, interpolate, useVideoConfig} from 'remotion';
import voDurations from './data/voDurations.json';
import {SCENES, SceneId} from './timeline';

// Kurva gerak standar: mulai tegas, berhenti lembut (dipakai semua transisi agar terasa konsisten).
export const EASE = Easing.bezier(0.33, 0, 0.2, 1);

// 0..1 dengan easing antara `start` dan `start + dur` (frame).
export const progress = (frame: number, start: number, dur: number) =>
  interpolate(frame, [start, start + dur], [0, 1], {easing: EASE, extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});

// Sinkron narasi: frame (relatif adegan) saat frasa diucapkan, diperkirakan dari posisi huruf frasa
// di naskah `vo` dibagi panjang naskah, dikali durasi adegan dikurangi jeda akhir. Bila durasi slot
// berubah, semua kejadian otomatis bergeser mengikuti narasi.
export const useNarration = (id: SceneId) => {
  const {durationInFrames, fps} = useVideoConfig();
  const vo = SCENES.find((s) => s.id === id)?.vo ?? '';
  // Lama narasi sebenarnya (tools/vo.py -> data/voDurations.json); cadangan: durasi adegan - 0,6 dtk.
  const voSec = (voDurations as Record<string, number>)[id];
  const speech = voSec ? Math.round(voSec * fps) : durationInFrames - Math.round(0.6 * fps);
  return (phrase: string, offset = 0) => {
    const i = vo.indexOf(phrase);
    if (i < 0) throw new Error(`Frasa tidak ada di narasi ${id}: ${phrase}`);
    return Math.round((i / vo.length) * speech) + offset;
  };
};
