import React from 'react';
import {AbsoluteFill, Sequence, interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {Badge, Caption} from '../components/Caption';
import {SceneFrame} from '../components/SceneFrame';
import fingerprints from '../data/fingerprints.json';
import {COLORS} from '../theme';

// Fase A: sidik jari gas (data chamber asli). Fase B: arsitektur model.
const PHASE_B_AT = 480;
const CROSSFADE = 20;

type GasKey = keyof typeof fingerprints.gases;

// Urutan pola yang ditampilkan (frame relatif fase A). Data dari tools/extract_fingerprints.py.
const STATES: {gas: GasKey; at: number; label: string; color: string}[] = [
  {gas: 'clean', at: 60, label: 'Udara bersih · normal', color: COLORS.ok},
  {gas: 'lpg', at: 180, label: 'Klasifikasi AI: LPG', color: COLORS.gas},
  {gas: 'co2', at: 330, label: 'Pola CO₂', color: COLORS.blueLight},
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
  if (idx < 0) return {values: cur, state: null};
  const p = spring({frame: frame - STATES[idx].at, fps, config: {damping: 18, mass: 0.8}});
  return {values: cur.map((c, i) => prev[i] + (c - prev[i]) * p), state: STATES[idx]};
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

const FingerprintPhase: React.FC = () => {
  const frame = useCurrentFrame();
  const {values, state} = useMorph();
  const color = state?.color ?? COLORS.blue;
  const labelOpacity = state ? interpolate(frame - state.at, [10, 25], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}) : 0;

  return (
    <AbsoluteFill>
      <AbsoluteFill style={{padding: '70px 120px'}}>
        <Caption text="8 sensor, sensitivitas berbeda → satu sidik jari gas" size={56} />
        <Caption
          text="Prinsip hidung elektronik: sensor oksida logam tidak selektif, tetapi polanya khas"
          from={20}
          size={30}
          weight={400}
          color={COLORS.muted}
          style={{marginTop: 12}}
        />
      </AbsoluteFill>

      <AbsoluteFill style={{flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', padding: '150px 120px 140px'}}>
        <div>
          <Bars values={values} color={color} />
          <div style={{marginTop: 50, fontSize: 52, fontWeight: 800, color, opacity: labelOpacity}}>{state?.label}</div>
        </div>
        <Radar values={values} color={color} />
      </AbsoluteFill>

      <div style={{position: 'absolute', left: 120, top: 880, fontSize: 22, color: COLORS.muted}}>
        Pola respons terukur · {fingerprints.source}
      </div>
    </AbsoluteFill>
  );
};

type Box = {id: string; x: number; y: number; w: number; h: number; title: string; sub: string; at: number; accent?: string};

const BOXES: Box[] = [
  {id: 'in', x: 120, y: 250, w: 340, h: 150, title: 'Sinyal 8 sensor', sub: 'deret waktu · 24-bit', at: 10},
  {id: 'ds', x: 120, y: 590, w: 340, h: 150, title: 'Profil sensitivitas', sub: 'karakteristik tiap sensor', at: 25},
  {id: 'b1', x: 580, y: 250, w: 380, h: 150, title: 'Cabang 1 · Conv1D', sub: 'pola temporal sinyal', at: 60, accent: COLORS.blue},
  {id: 'b2', x: 580, y: 590, w: 380, h: 150, title: 'Cabang 2 · Dense', sub: 'fitur sensitivitas', at: 80, accent: COLORS.blue},
  {id: 'mg', x: 1080, y: 420, w: 300, h: 150, title: 'Penggabungan', sub: 'fitur dua cabang', at: 130, accent: COLORS.blue},
];
const OUTPUTS = ['Udara bersih', 'LPG', 'H₂'];
const OUT_X = 1500;
const ARROWS: [string, string][] = [
  ['in', 'b1'],
  ['ds', 'b2'],
  ['b1', 'mg'],
  ['b2', 'mg'],
];
const box = (id: string) => BOXES.find((b) => b.id === id)!;

const ModelPhase: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const appear = (at: number) => spring({frame: frame - at, fps, config: {damping: 200}});
  const draw = (at: number) => interpolate(frame, [at, at + 25], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const highlight = frame >= 230 ? 1 : 0; // LPG menyala sebagai contoh keluaran

  return (
    <AbsoluteFill>
      <AbsoluteFill style={{padding: '70px 120px'}}>
        <Caption text="Jaringan saraf konvolusional dua cabang" size={56} />
      </AbsoluteFill>

      <svg width={1920} height={1080} style={{position: 'absolute'}}>
        <defs>
          <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">
            <path d="M0,0 L10,5 L0,10 z" fill={COLORS.blueLight} />
          </marker>
        </defs>
        {ARROWS.map(([a, b], i) => {
          const A = box(a);
          const B = box(b);
          const x1 = A.x + A.w;
          const y1 = A.y + A.h / 2;
          const x2 = B.x;
          const y2 = B.y + B.h / 2;
          const len = Math.hypot(x2 - x1, y2 - y1);
          return (
            <line key={i} x1={x1} y1={y1} x2={x2} y2={y2} stroke={COLORS.blueLight} strokeWidth={4} markerEnd="url(#arrow)" strokeDasharray={len} strokeDashoffset={len * (1 - draw(40 + i * 25))} />
          );
        })}
        {OUTPUTS.map((_, i) => {
          const M = box('mg');
          const y2 = 330 + i * 130 + 45;
          const x1 = M.x + M.w;
          const y1 = M.y + M.h / 2;
          const len = Math.hypot(OUT_X - x1, y2 - y1);
          return (
            <line key={`o${i}`} x1={x1} y1={y1} x2={OUT_X} y2={y2} stroke={COLORS.line} strokeWidth={3} markerEnd="url(#arrow)" strokeDasharray={len} strokeDashoffset={len * (1 - draw(160))} />
          );
        })}
      </svg>

      {BOXES.map((b) => {
        const p = appear(b.at);
        return (
          <div
            key={b.id}
            style={{
              position: 'absolute',
              left: b.x,
              top: b.y,
              width: b.w,
              height: b.h,
              borderRadius: 16,
              backgroundColor: COLORS.surface,
              border: `3px solid ${b.accent ?? COLORS.line}`,
              padding: '24px 26px',
              opacity: p,
              transform: `scale(${interpolate(p, [0, 1], [0.9, 1])})`,
            }}
          >
            <div style={{fontSize: 32, fontWeight: 800}}>{b.title}</div>
            <div style={{fontSize: 24, color: COLORS.muted, marginTop: 8}}>{b.sub}</div>
          </div>
        );
      })}

      {OUTPUTS.map((o, i) => {
        const p = appear(170 + i * 10);
        const on = o === 'LPG' && highlight;
        return (
          <div
            key={o}
            style={{
              position: 'absolute',
              left: OUT_X,
              top: 330 + i * 130,
              width: 300,
              height: 90,
              borderRadius: 14,
              display: 'flex',
              alignItems: 'center',
              paddingLeft: 26,
              fontSize: 32,
              fontWeight: 600,
              opacity: p,
              backgroundColor: on ? COLORS.gas : COLORS.surface,
              color: on ? COLORS.charcoal : COLORS.text,
              border: `3px solid ${on ? COLORS.gas : COLORS.line}`,
            }}
          >
            {o}
          </div>
        );
      })}
      <div style={{position: 'absolute', left: OUT_X, top: 280, fontSize: 24, color: COLORS.muted, opacity: appear(160)}}>Softmax · kelas gas</div>

      <div style={{position: 'absolute', left: 120, top: 800, display: 'flex', gap: 20}}>
        <Badge text="Kuantisasi int8" from={260} />
        <Badge text="Inferensi di ESP32-S3" from={280} />
        <Badge text="Tanpa server" from={300} color={COLORS.ok} />
      </div>
    </AbsoluteFill>
  );
};

export const Scene04Fingerprint: React.FC = () => {
  const frame = useCurrentFrame();
  const fadeA = interpolate(frame, [PHASE_B_AT - CROSSFADE, PHASE_B_AT], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const fadeB = interpolate(frame, [PHASE_B_AT, PHASE_B_AT + CROSSFADE], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});

  return (
    <SceneFrame>
      <Sequence durationInFrames={PHASE_B_AT} name="A · Sidik jari">
        <AbsoluteFill style={{opacity: fadeA}}>
          <FingerprintPhase />
        </AbsoluteFill>
      </Sequence>
      <Sequence from={PHASE_B_AT} name="B · Arsitektur model">
        <AbsoluteFill style={{opacity: fadeB}}>
          <ModelPhase />
        </AbsoluteFill>
      </Sequence>
    </SceneFrame>
  );
};
