import React from 'react';
import {AbsoluteFill, useCurrentFrame, useVideoConfig} from 'remotion';
import {COLORS, FONT} from '../theme';

const MAX_CHARS = 95;

// Pecah narasi per kalimat, lalu kalimat panjang dipecah lagi di koma/titik koma
// supaya subtitle paling banyak dua baris.
const chunk = (vo: string) => {
  const sentences = vo.match(/[^.!?;]+[.!?;]+/g)?.map((s) => s.trim()) ?? [vo];
  const out: string[] = [];
  for (const sentence of sentences) {
    let line = '';
    for (const clause of sentence.split(/(?<=,)\s+/)) {
      if (line && line.length + clause.length + 1 > MAX_CHARS) {
        out.push(line);
        line = clause;
      } else {
        line = line ? `${line} ${clause}` : clause;
      }
    }
    if (line) out.push(line);
  }
  return out;
};

// Tiap potongan tampil sebanding panjang hurufnya.
export const Subtitles: React.FC<{vo: string}> = ({vo}) => {
  const frame = useCurrentFrame();
  const {durationInFrames} = useVideoConfig();
  const parts = chunk(vo);
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
