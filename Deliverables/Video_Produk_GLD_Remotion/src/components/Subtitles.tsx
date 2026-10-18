import React from 'react';
import {AbsoluteFill, useCurrentFrame, useVideoConfig} from 'remotion';
import {COLORS, FONT} from '../theme';

// Narasi dipecah per kalimat; tiap kalimat tampil sebanding panjang hurufnya.
export const Subtitles: React.FC<{vo: string}> = ({vo}) => {
  const frame = useCurrentFrame();
  const {durationInFrames} = useVideoConfig();
  const parts = vo.match(/[^.!?]+[.!?]+/g)?.map((s) => s.trim()) ?? [vo];
  const total = parts.reduce((n, s) => n + s.length, 0);

  let acc = 0;
  let current = parts[parts.length - 1];
  for (const p of parts) {
    acc += p.length;
    if (frame < (acc / total) * durationInFrames) {
      current = p;
      break;
    }
  }

  return (
    <AbsoluteFill style={{justifyContent: 'flex-end', alignItems: 'center', paddingBottom: 48}}>
      <div
        style={{
          maxWidth: 1500,
          padding: '12px 28px',
          borderRadius: 12,
          backgroundColor: 'rgba(20,18,16,0.78)',
          color: COLORS.text,
          fontFamily: FONT,
          fontSize: 34,
          fontWeight: 400,
          textAlign: 'center',
          lineHeight: 1.35,
        }}
      >
        {current}
      </div>
    </AbsoluteFill>
  );
};
