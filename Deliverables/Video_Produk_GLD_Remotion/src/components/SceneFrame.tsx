import React from 'react';
import {AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig} from 'remotion';
import {COLORS, FONT} from '../theme';

const FADE = 10;

// Latar + fade masuk/keluar untuk setiap adegan.
export const SceneFrame: React.FC<{children: React.ReactNode; background?: string}> = ({children, background}) => {
  const frame = useCurrentFrame();
  const {durationInFrames} = useVideoConfig();
  const opacity = interpolate(frame, [0, FADE, durationInFrames - FADE, durationInFrames], [0, 1, 1, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  return (
    <AbsoluteFill style={{backgroundColor: background ?? COLORS.bg, fontFamily: FONT, color: COLORS.text}}>
      <AbsoluteFill style={{opacity}}>{children}</AbsoluteFill>
    </AbsoluteFill>
  );
};
