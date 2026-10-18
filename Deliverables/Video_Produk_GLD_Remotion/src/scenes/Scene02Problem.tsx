import React from 'react';
import {AbsoluteFill, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {Caption} from '../components/Caption';
import {DetectorIcon} from '../components/Icons';
import {SceneFrame} from '../components/SceneFrame';
import {Sfx} from '../components/Sfx';
import {useLayout} from '../layout';
import {progress, useNarration} from '../motion';
import {COLORS} from '../theme';

// Lima gas yang umum dipantau di kilang: masing-masing butuh detektor sendiri.
const GASES = ['LPG', 'CH₄', 'H₂', 'H₂S', 'CO'];

export const Scene02Problem: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const {portrait, width, height, title} = useLayout();
  const at = useNarration('problem');
  const tCable = at('kabel data');
  const cable = (i: number) => progress(frame, tCable - 20 + i * 6, 45);
  const strike = progress(frame, at('sulit diperluas', 6), 22);
  const pop = (i: number) => spring({frame: frame - 6 - i * 5, fps, config: {damping: 20}});
  // Tiga masalah muncul tepat saat diucapkan narasi.
  const ISSUES = [
    {text: 'Satu detektor untuk satu jenis gas', at: at('satu jenis gas')},
    {text: 'Kabel data ke ruang kontrol', at: tCable},
    {text: 'Mahal dan sulit diperluas', at: at('mahal')},
  ];

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
    <SceneFrame theme="light">
      <svg width={width} height={height} style={{position: 'absolute'}}>
        {detectors.map((d, i) => (
          <path key={d.gas} d={cablePath(d)} fill="none" stroke={COLORS.muted} strokeWidth={6} strokeDasharray={1400} strokeDashoffset={1400 * (1 - cable(i))} />
        ))}
        <line {...strikeLine} stroke={COLORS.alarm} strokeWidth={14} strokeLinecap="round" strokeDasharray={strikeLen} strokeDashoffset={strikeLen * (1 - strike)} />
      </svg>

      {detectors.map((d, i) =>
        portrait ? (
          <div key={d.gas} style={{position: 'absolute', left: d.x - 60, top: d.y - 40, width: 120, display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 10, opacity: pop(i), transform: `scale(${0.8 + 0.2 * pop(i)})`}}>
            <DetectorIcon />
            <span style={{fontSize: 36, fontWeight: 800}}>{d.gas}</span>
          </div>
        ) : (
          <div key={d.gas} style={{position: 'absolute', left: d.x - 35, top: d.y - 35, display: 'flex', alignItems: 'center', gap: 20, opacity: pop(i), transform: `translateX(${-30 * (1 - pop(i))}px)`}}>
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
          backgroundColor: COLORS.surface,
          opacity: progress(frame, tCable - 30, 20),
        }}
      >
        Ruang kontrol
      </div>

      {/* Label masalah, muncul sesuai narasi */}
      <div style={{position: 'absolute', left: portrait ? 64 : 1360, top: portrait ? 1420 : 680, width: portrait ? 952 : 480, display: 'flex', flexDirection: 'column', gap: portrait ? 12 : 16}}>
        {ISSUES.map((it) => {
          const p = progress(frame, it.at, 18);
          return (
            <div key={it.text} style={{opacity: p, transform: `translateY(${16 * (1 - p)}px)`, padding: '12px 18px', borderRadius: 12, backgroundColor: COLORS.surface, border: `1px solid ${COLORS.line}`, borderLeft: `6px solid ${COLORS.alarm}`, fontSize: portrait ? 28 : 26, fontWeight: 600, boxShadow: '0 6px 18px rgba(20,33,58,0.10)'}}>
              {it.text}
            </div>
          );
        })}
      </div>

      <AbsoluteFill style={{alignItems: 'center', paddingTop: portrait ? 200 : 70, textAlign: 'center'}}>
        <Caption text="Pendekatan konvensional: satu detektor per jenis gas" from={8} size={title(56)} />
      </AbsoluteFill>
      {GASES.map((g, i) => <Sfx key={g} name="pop" at={6 + i * 5} volume={0.22} />)}
      {ISSUES.map((it) => <Sfx key={it.text} name="tick" at={it.at} volume={0.35} />)}
      <Sfx name="whoosh_short" at={at('sulit diperluas', 6)} volume={0.5} />
    </SceneFrame>
  );
};
