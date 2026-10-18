import {loadFont} from '@remotion/fonts';
import {staticFile} from 'remotion';

// Font Inter dibundel di public/fonts (lisensi OFL) supaya render tidak butuh internet.
const FAMILY = 'Inter';
for (const weight of ['400', '600', '800']) {
  loadFont({family: FAMILY, url: staticFile(`fonts/inter-latin-${weight}-normal.woff2`), weight});
}

// Palet resmi deliverable GLD: biru #2B5FCB + charcoal #262321.
export const COLORS = {
  blue: '#2B5FCB',
  blueLight: '#5B86E5',
  charcoal: '#262321',
  bg: '#141210',
  surface: '#1F1C1A',
  line: '#3A3532',
  text: '#F4F2EF',
  muted: '#A8A29E',
  gas: '#F5A524',
  alarm: '#E5484D',
  ok: '#30A46C',
} as const;

export const FONT = `${FAMILY}, sans-serif`;
