import React from 'react';
import {AbsoluteFill, interpolate, useCurrentFrame} from 'remotion';
import {Caption} from '../components/Caption';
import {DetectorIcon} from '../components/Icons';
import {SceneFrame} from '../components/SceneFrame';
import {COLORS} from '../theme';

// Lima gas yang umum dipantau di kilang: masing-masing butuh detektor sendiri.
const DETECTORS = ['LPG', 'CH₄', 'H₂', 'H₂S', 'CO'].map((gas, i) => ({gas, y: 240 + i * 145}));
const CONTROL = {x: 1500, y: 520};

export const Scene02Problem: React.FC = () => {
  const frame = useCurrentFrame();
  const cable = interpolate(frame, [30, 120], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const strike = interpolate(frame, [230, 260], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});

  return (
    <SceneFrame>
      <svg width={1920} height={1080} style={{position: 'absolute'}}>
        {DETECTORS.map((d) => {
          const path = `M 360 ${d.y} C 900 ${d.y}, 1000 ${CONTROL.y}, ${CONTROL.x - 120} ${CONTROL.y}`;
          return (
            <path
              key={d.gas}
              d={path}
              fill="none"
              stroke={COLORS.muted}
              strokeWidth={6}
              strokeDasharray={1400}
              strokeDashoffset={1400 * (1 - cable)}
            />
          );
        })}
        <line x1={300} y1={160} x2={1650} y2={900} stroke={COLORS.alarm} strokeWidth={14} strokeLinecap="round" strokeDasharray={1550} strokeDashoffset={1550 * (1 - strike)} />
      </svg>

      {DETECTORS.map((d) => (
        <div key={d.gas} style={{position: 'absolute', left: 200, top: d.y - 35, display: 'flex', alignItems: 'center', gap: 20}}>
          <DetectorIcon />
          <span style={{fontSize: 40, fontWeight: 800}}>{d.gas}</span>
        </div>
      ))}

      <div
        style={{
          position: 'absolute',
          left: CONTROL.x - 120,
          top: CONTROL.y - 80,
          width: 300,
          height: 160,
          borderRadius: 16,
          border: `4px solid ${COLORS.muted}`,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          fontSize: 34,
          fontWeight: 600,
          textAlign: 'center',
        }}
      >
        Ruang kontrol
      </div>

      <AbsoluteFill style={{alignItems: 'center', paddingTop: 70}}>
        <Caption text="5 gas = 5 detektor + 5 kabel data" from={130} size={56} />
      </AbsoluteFill>
    </SceneFrame>
  );
};
