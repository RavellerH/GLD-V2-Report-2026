import {Easing, interpolate, useVideoConfig} from 'remotion';
import voDurations from './data/voDurations.json';
import {useLang} from './i18n';
import {OGI_SCENES} from './ogi/timeline';
import {SCENES} from './timeline';

// Semua adegan dari kedua video (id unik) untuk sinkron narasi & subtitle.
export const ALL_SCENES = [...SCENES, ...OGI_SCENES] as {id: string; vo: string; voEn: string}[];

// Kurva gerak standar: mulai tegas, berhenti lembut (dipakai semua transisi agar terasa konsisten).
export const EASE = Easing.bezier(0.33, 0, 0.2, 1);

// 0..1 dengan easing antara `start` dan `start + dur` (frame).
export const progress = (frame: number, start: number, dur: number) =>
  interpolate(frame, [start, start + dur], [0, 1], {easing: EASE, extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});

// Sinkron narasi: frame (relatif adegan) saat frasa diucapkan, diperkirakan dari posisi huruf frasa
// di naskah `vo` dibagi panjang naskah, dikali durasi adegan dikurangi jeda akhir. Bila durasi slot
// berubah, semua kejadian otomatis bergeser mengikuti narasi.
export const useNarration = (id: string) => {
  const {durationInFrames, fps} = useVideoConfig();
  const lang = useLang();
  const scene = ALL_SCENES.find((s) => s.id === id);
  const vo = scene ? (lang === 'en' ? scene.voEn : scene.vo) : '';
  // Lama narasi sebenarnya (tools/vo.py -> data/voDurations.json); cadangan: durasi adegan - 0,6 dtk.
  const voSec = (voDurations as Record<string, Record<string, number>>)[lang]?.[id];
  const speech = voSec ? Math.round(voSec * fps) : durationInFrames - Math.round(0.6 * fps);
  // `phrase` boleh berupa [frasa ID, frasa EN] agar sinkron di kedua bahasa.
  return (phrase: string | [string, string], offset = 0) => {
    const ph = Array.isArray(phrase) ? phrase[lang === 'en' ? 1 : 0] : phrase;
    const i = vo.indexOf(ph);
    if (i < 0) throw new Error(`Frasa tidak ada di narasi ${id} (${lang}): ${ph}`);
    return Math.round((i / vo.length) * speech) + offset;
  };
};
