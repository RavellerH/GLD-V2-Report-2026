import React from 'react';
import {AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {Badge, Caption} from '../components/Caption';
import {SceneFrame} from '../components/SceneFrame';
import fingerprints from '../data/fingerprints.json';
import {COLORS} from '../theme';

type GasKey = keyof typeof fingerprints.gases;

// Urutan pola yang ditampilkan (frame relatif adegan). Data dari tools/extract_fingerprints.py.
const STATES: {gas: GasKey; at: number; label: string; color: string}[] = [
  {gas: 'clean', at: 60, label: 'Udara bersih · normal', color: COLORS.ok},
  {gas: 'lpg', at: 220, label: 'Klasifikasi AI: LPG', color: COLORS.gas},
  {gas: 'co2', at: 440, label: 'Pola CO₂', color: COLORS.blueLight},
];

const SENSORS = fingerprints.sensors;
const N = SENSORS.length;

const radiiFor = (gas: GasKey) => {
  const g = fingerprints.gases[gas];
  // Lingkaran dasar 0.06 agar udara bersih tetap terlihat sebagai pola "tenang".
  return g.shape.map((s) => 0.06 + s * g.amplitude * 0.94);
};

const useMorph = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  let prev = new Array<number>(N).fill(0);
  let cur = prev;
  let idx = -1;
  STATES.forEach((s, i) => {
    if (frame >= s.at) {
      prev = idx >= 0 ? radiiFor(STATES[idx].gas) : prev;
      cur = radiiFor(s.gas);
      idx = i;
    }
  });
  if (idx < 0) return {values: cur, state: null, p: 0};
  const p = spring({frame: frame - STATES[idx].at, fps, config: {damping: 18, mass: 0.8}});
  return {values: cur.map((c, i) => prev[i] + (c - prev[i]) * p), state: STATES[idx], p};
};

const Radar: React.FC<{values: number[]; color: string}> = ({values, color}) => {
  const R = 280;
  const c = 380;
  const pt = (i: number, r: number) => {
    const a = (Math.PI * 2 * i) / N - Math.PI / 2;
    return [c + Math.cos(a) * r * R, c + Math.sin(a) * r * R] as const;
  };
  const poly = values.map((v, i) => pt(i, Math.max(v, 0)).join(',')).join(' ');
  return (
    <svg width={760} height={760}>
      {[0.25, 0.5, 0.75, 1].map((r) => (
        <polygon key={r} points={SENSORS.map((_, i) => pt(i, r).join(',')).join(' ')} fill="none" stroke={COLORS.line} strokeWidth={2} />
      ))}
      {SENSORS.map((s, i) => {
        const [x, y] = pt(i, 1);
        const [lx, ly] = pt(i, 1.2);
        return (
          <g key={s}>
            <line x1={c} y1={c} x2={x} y2={y} stroke={COLORS.line} strokeWidth={2} />
            <text x={lx} y={ly} fill={COLORS.muted} fontSize={26} fontWeight={600} textAnchor="middle" dominantBaseline="middle">
              {s}
            </text>
          </g>
        );
      })}
      <polygon points={poly} fill={color} fillOpacity={0.3} stroke={color} strokeWidth={5} strokeLinejoin="round" />
    </svg>
  );
};

const Bars: React.FC<{values: number[]; color: string}> = ({values, color}) => (
  <div style={{display: 'flex', alignItems: 'flex-end', gap: 18, height: 360}}>
    {values.map((v, i) => (
      <div key={SENSORS[i]} style={{display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 10}}>
        <div style={{width: 48, height: 320, display: 'flex', alignItems: 'flex-end', backgroundColor: COLORS.surface, borderRadius: 8}}>
          <div style={{width: '100%', height: `${Math.min(v, 1) * 100}%`, backgroundColor: color, borderRadius: 8}} />
        </div>
        <span style={{fontSize: 20, color: COLORS.muted}}>{SENSORS[i]}</span>
      </div>
    ))}
  </div>
);

export const Scene04Fingerprint: React.FC = () => {
  const frame = useCurrentFrame();
  const {values, state} = useMorph();
  const color = state?.color ?? COLORS.blue;
  const labelOpacity = state ? interpolate(frame - state.at, [10, 25], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}) : 0;

  return (
    <SceneFrame>
      <AbsoluteFill style={{padding: '70px 120px'}}>
        <Caption text="8 sensor → 1 sidik jari → AI mengenali gasnya" size={58} />
        <div style={{marginTop: 18}}>
          <Badge text="AI on-device" from={30} />
        </div>
      </AbsoluteFill>

      <AbsoluteFill style={{flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', padding: '120px 120px 140px'}}>
        <div>
          <Bars values={values} color={color} />
          <div style={{marginTop: 50, fontSize: 52, fontWeight: 800, color, opacity: labelOpacity}}>{state?.label}</div>
        </div>
        <Radar values={values} color={color} />
      </AbsoluteFill>

      <div style={{position: 'absolute', left: 120, top: 880, fontSize: 22, color: COLORS.muted}}>
        Pola respons terukur · {fingerprints.source}
      </div>
    </SceneFrame>
  );
};
