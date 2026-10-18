import React from 'react';
import {AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig} from 'remotion';
import {EASE} from '../motion';
import {COLORS, FONT, ThemeName, themeVars} from '../theme';

// Panjang crossfade antar-adegan (frame). Explainer menumpangkan tiap adegan TRANSITION frame di atas
// akhir adegan sebelumnya, jadi adegan baru cukup fade-in di atasnya -> tidak ada kedipan ke latar kosong.
export const TRANSITION = 18;

export const SceneFrame: React.FC<{children: React.ReactNode; background?: string; theme?: ThemeName; drift?: boolean; last?: boolean}> = ({
  children,
  background,
  theme = 'night',
  drift,
  last = false,
}) => {
  const frame = useCurrentFrame();
  const {durationInFrames} = useVideoConfig();
  const opts = {easing: EASE, extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
  const fadeIn = interpolate(frame, [0, TRANSITION], [0, 1], opts);
  const fadeOut = last ? interpolate(frame, [durationInFrames - 20, durationInFrames], [1, 0], opts) : 1;
  const enter = interpolate(frame, [0, TRANSITION + 12], [1.025, 1], opts);
  // Drift: zoom sangat pelan sepanjang adegan agar layar informatif tidak terasa diam.
  const useDrift = drift ?? theme === 'light';
  const slow = useDrift ? interpolate(frame, [0, durationInFrames], [1, 1.03]) : 1;
  return (
    <AbsoluteFill style={{...themeVars(theme), opacity: fadeIn * fadeOut, backgroundColor: background ?? COLORS.bg, fontFamily: FONT, color: COLORS.text}}>
      <AbsoluteFill style={{transform: `scale(${enter * slow})`}}>{children}</AbsoluteFill>
    </AbsoluteFill>
  );
};
