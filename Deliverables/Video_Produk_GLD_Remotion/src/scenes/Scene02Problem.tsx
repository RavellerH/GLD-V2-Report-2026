import React from 'react';
import {AbsoluteFill, interpolate, useCurrentFrame} from 'remotion';
import {Caption} from '../components/Caption';
import {DetectorIcon} from '../components/Icons';
import {SceneFrame} from '../components/SceneFrame';
import {useLayout} from '../layout';
import {COLORS} from '../theme';

// Lima gas yang umum dipantau di kilang: masing-masing butuh detektor sendiri.
const GASES = ['LPG', 'CH₄', 'H₂', 'H₂S', 'CO'];

export const Scene02Problem: React.FC = () => {
  const frame = useCurrentFrame();
  const {portrait, width, height, title} = useLayout();
  const cable = interpolate(frame, [30, 120], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const strike = interpolate(frame, [230, 260], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});

  // Landscape: detektor berjajar vertikal di kiri, ruang kontrol di kanan.
  // Portrait: detektor berjajar horizontal di atas, ruang kontrol di bawah.
  const detectors = GASES.map((gas, i) =>
    portrait ? {gas, x: 140 + i * 200, y: 560} : {gas, x: 235, y: 240 + i * 145},
  );
  const control = portrait ? {x: width / 2, y: 1300, w: 360, h: 150} : {x: 1530, y: 520, w: 300, h: 160};
  const cablePath = (d: {x: number; y: number}) =>
    portrait
      ? `M ${d.x} ${d.y + 90} C ${d.x} ${d.y + 450}, ${control.x} ${control.y - 350}, ${control.x} ${control.y - control.h / 2}`
      : `M 360 ${d.y} C 900 ${d.y}, 1000 ${control.y}, ${control.x - control.w / 2} ${control.y}`;
  const strikeLine = portrait ? {x1: 80, y1: 420, x2: 1000, y2: 1440} : {x1: 300, y1: 160, x2: 1650, y2: 900};
  const strikeLen = Math.hypot(strikeLine.x2 - strikeLine.x1, strikeLine.y2 - strikeLine.y1);

  return (
    <SceneFrame>
      <svg width={width} height={height} style={{position: 'absolute'}}>
        {detectors.map((d) => (
          <path key={d.gas} d={cablePath(d)} fill="none" stroke={COLORS.muted} strokeWidth={6} strokeDasharray={1400} strokeDashoffset={1400 * (1 - cable)} />
        ))}
        <line {...strikeLine} stroke={COLORS.alarm} strokeWidth={14} strokeLinecap="round" strokeDasharray={strikeLen} strokeDashoffset={strikeLen * (1 - strike)} />
      </svg>

      {detectors.map((d) =>
        portrait ? (
          <div key={d.gas} style={{position: 'absolute', left: d.x - 60, top: d.y - 40, width: 120, display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 10}}>
            <DetectorIcon />
            <span style={{fontSize: 36, fontWeight: 800}}>{d.gas}</span>
          </div>
        ) : (
          <div key={d.gas} style={{position: 'absolute', left: d.x - 35, top: d.y - 35, display: 'flex', alignItems: 'center', gap: 20}}>
            <DetectorIcon />
            <span style={{fontSize: 40, fontWeight: 800}}>{d.gas}</span>
          </div>
        ),
      )}

      <div
        style={{
          position: 'absolute',
          left: control.x - control.w / 2,
          top: control.y - control.h / 2,
          width: control.w,
          height: control.h,
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

      <AbsoluteFill style={{alignItems: 'center', paddingTop: portrait ? 200 : 70, textAlign: 'center'}}>
        <Caption text="5 gas = 5 detektor + 5 kabel data" from={130} size={title(56)} />
      </AbsoluteFill>
    </SceneFrame>
  );
};
