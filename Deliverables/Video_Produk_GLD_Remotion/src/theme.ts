import type React from 'react';
import {loadFont} from '@remotion/fonts';
import {staticFile} from 'remotion';

// Font Inter dibundel di public/fonts (lisensi OFL) supaya render tidak butuh internet.
const FAMILY = 'Inter';
for (const weight of ['400', '600', '800']) {
  loadFont({family: FAMILY, url: staticFile(`fonts/inter-latin-${weight}-normal.woff2`), weight});
}

// Dua tema korporat, aksen tetap sama (biru #2B5FCB, oranye gas/STAR #F5A524, merah alarm, hijau OK):
// - night: adegan sinematik (b-roll & render 3D malam) -> navy gelap, menyatu dengan render.
// - light: adegan informatif (diagram, grafik, dashboard) -> terang, bersih, gaya korporat.
// Komponen memakai COLORS (CSS variable); nilainya ditentukan SceneFrame lewat prop `theme`.
export type ThemeName = 'night' | 'light';
export const PALETTES: Record<ThemeName, Record<string, string>> = {
  night: {
    blue: '#2B5FCB', blueLight: '#5B9BFF', charcoal: '#0A1220', bg: '#0A1220', surface: '#111C2E',
    line: '#26354D', text: '#F2F5FA', muted: '#9AA8BD', gas: '#F5A524', alarm: '#E5484D', ok: '#30A46C',
    overlay: 'rgba(10,18,32,0.92)', subtitleBg: 'rgba(10,18,32,0.80)', subtitleText: '#F2F5FA',
  },
  light: {
    blue: '#2B5FCB', blueLight: '#1F4FB8', charcoal: '#262321', bg: '#F3F5F9', surface: '#FFFFFF',
    line: '#D3DAE5', text: '#14213A', muted: '#55627A', gas: '#D98700', alarm: '#D13438', ok: '#1E8A55',
    overlay: 'rgba(243,245,249,0.92)', subtitleBg: 'rgba(10,18,32,0.80)', subtitleText: '#F2F5FA',
  },
};
const KEYS = Object.keys(PALETTES.night);
export const themeVars = (t: ThemeName): React.CSSProperties =>
  Object.fromEntries(KEYS.map((k) => [`--gld-${k}`, PALETTES[t][k]])) as React.CSSProperties;
export const COLORS = Object.fromEntries(KEYS.map((k) => [k, `var(--gld-${k})`])) as Record<
  'blue' | 'blueLight' | 'charcoal' | 'bg' | 'surface' | 'line' | 'text' | 'muted' | 'gas' | 'alarm' | 'ok' |
  'overlay' | 'subtitleBg' | 'subtitleText',
  string
>;

export const FONT = `${FAMILY}, sans-serif`;
