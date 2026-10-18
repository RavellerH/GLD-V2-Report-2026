import React from 'react';
import {interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {COLORS} from '../theme';

type Props = {
  text: string;
  from?: number; // frame relatif adegan
  size?: number;
  color?: string;
  weight?: number;
  style?: React.CSSProperties;
};

// Teks yang naik + fade-in dengan spring.
export const Caption: React.FC<Props> = ({text, from = 0, size = 64, color = COLORS.text, weight = 800, style}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const p = spring({frame: frame - from, fps, config: {damping: 200}});
  return (
    <div
      style={{
        fontSize: size,
        fontWeight: weight,
        color,
        lineHeight: 1.15,
        letterSpacing: -0.5,
        opacity: p,
        transform: `translateY(${interpolate(p, [0, 1], [30, 0])}px)`,
        ...style,
      }}
    >
      {text}
    </div>
  );
};

export const Badge: React.FC<{text: string; color?: string; from?: number}> = ({text, color = COLORS.blue, from = 0}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const p = spring({frame: frame - from, fps, config: {damping: 14}});
  return (
    <div
      style={{
        display: 'inline-block',
        padding: '10px 22px',
        borderRadius: 999,
        backgroundColor: color,
        color: COLORS.text,
        fontSize: 28,
        fontWeight: 600,
        transform: `scale(${p})`,
      }}
    >
      {text}
    </div>
  );
};
