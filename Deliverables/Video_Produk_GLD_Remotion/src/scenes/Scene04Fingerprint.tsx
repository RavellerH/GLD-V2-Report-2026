import React from 'react';
import {AbsoluteFill, Sequence, interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {Badge, Caption} from '../components/Caption';
import {SceneFrame} from '../components/SceneFrame';
import fingerprints from '../data/fingerprints.json';
import {useLayout} from '../layout';
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

// Label kanal di layar: S1–S8 (urutan sama dengan fingerprints.sensors). Nama seri sensor tidak ditampilkan.
const SENSORS = fingerprints.sensors.map((_, i) => `S${i + 1}`);
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

const Radar: React.FC<{values: number[]; color: string; size: number}> = ({values, color, size}) => {
  const R = 280;
  const c = 380;
  const pt = (i: number, r: number) => {
    const a = (Math.PI * 2 * i) / N - Math.PI / 2;
    return [c + Math.cos(a) * r * R, c + Math.sin(a) * r * R] as const;
  };
  const poly = values.map((v, i) => pt(i, Math.max(v, 0)).join(',')).join(' ');
  return (
    <svg width={size} height={size} viewBox="0 0 760 760">
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
  const {portrait, padX, title} = useLayout();
  const {values, state} = useMorph();
  const color = state?.color ?? COLORS.blue;
  const labelOpacity = state ? interpolate(frame - state.at, [10, 25], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}) : 0;
  const label = <div style={{marginTop: portrait ? 24 : 50, fontSize: title(52), fontWeight: 800, color, opacity: labelOpacity}}>{state?.label}</div>;

  return (
    <AbsoluteFill>
      <AbsoluteFill style={{padding: portrait ? `200px ${padX}px` : `70px ${padX}px`}}>
        <Caption text="8 sensor, sensitivitas berbeda → satu sidik jari gas" size={title(56)} />
        <Caption
          text="Prinsip hidung elektronik: sensor oksida logam tidak selektif, tetapi polanya khas"
          from={20}
          size={title(30)}
          weight={400}
          color={COLORS.muted}
          style={{marginTop: 12}}
        />
      </AbsoluteFill>

      {portrait ? (
        <AbsoluteFill style={{alignItems: 'center', paddingTop: 470}}>
          <Bars values={values} color={color} />
          {label}
          <Radar values={values} color={color} size={600} />
        </AbsoluteFill>
      ) : (
        <AbsoluteFill style={{flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', padding: `150px ${padX}px 140px`}}>
          <div>
            <Bars values={values} color={color} />
            {label}
          </div>
          <Radar values={values} color={color} size={760} />
        </AbsoluteFill>
      )}

      <div style={{position: 'absolute', left: padX, top: portrait ? 1600 : 880, fontSize: 22, color: COLORS.muted}}>
        Pola respons terukur · {fingerprints.source}
      </div>
    </AbsoluteFill>
  );
};

type Rect = {x: number; y: number; w: number; h: number};
type Box = {id: string; title: string; sub: string; at: number; accent?: string};

const BOXES: Box[] = [
  {id: 'in', title: 'Sinyal 8 sensor', sub: 'deret waktu · 24-bit', at: 10},
  {id: 'ds', title: 'Profil sensitivitas', sub: 'karakteristik tiap sensor', at: 25},
  {id: 'b1', title: 'Cabang 1 · Conv1D', sub: 'pola temporal sinyal', at: 60, accent: COLORS.blue},
  {id: 'b2', title: 'Cabang 2 · Dense', sub: 'fitur sensitivitas', at: 80, accent: COLORS.blue},
  {id: 'mg', title: 'Penggabungan', sub: 'fitur dua cabang', at: 130, accent: COLORS.blue},
];
const OUTPUTS = ['Udara bersih', 'LPG', 'H₂', '+ kelas per kilang'];
const ARROWS: [string, string][] = [
  ['in', 'b1'],
  ['ds', 'b2'],
  ['b1', 'mg'],
  ['b2', 'mg'],
];

// Geometri diagram per orientasi. Landscape mengalir kiri→kanan, portrait atas→bawah.
const GEOMETRY: Record<'landscape' | 'portrait', {boxes: Record<string, Rect>; outputs: Rect[]; softmax: {x: number; y: number}; badges: {x: number; y: number}}> = {
  landscape: {
    boxes: {
      in: {x: 120, y: 250, w: 340, h: 150},
      ds: {x: 120, y: 590, w: 340, h: 150},
      b1: {x: 580, y: 250, w: 380, h: 150},
      b2: {x: 580, y: 590, w: 380, h: 150},
      mg: {x: 1080, y: 420, w: 300, h: 150},
    },
    outputs: OUTPUTS.map((_, i) => ({x: 1500, y: 330 + i * 130, w: 300, h: 90})),
    softmax: {x: 1500, y: 280},
    badges: {x: 120, y: 800},
  },
  portrait: {
    boxes: {
      in: {x: 64, y: 420, w: 460, h: 150},
      ds: {x: 556, y: 420, w: 460, h: 150},
      b1: {x: 64, y: 660, w: 460, h: 150},
      b2: {x: 556, y: 660, w: 460, h: 150},
      mg: {x: 290, y: 900, w: 500, h: 140},
    },
    outputs: OUTPUTS.map((_, i) => ({x: i % 2 ? 556 : 64, y: 1150 + Math.floor(i / 2) * 110, w: 460, h: 90})),
    softmax: {x: 64, y: 1105},
    badges: {x: 64, y: 1390},
  },
};

const ModelPhase: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const {portrait, padX, width, height, title} = useLayout();
  const g = GEOMETRY[portrait ? 'portrait' : 'landscape'];
  const appear = (at: number) => spring({frame: frame - at, fps, config: {damping: 200}});
  const draw = (at: number) => interpolate(frame, [at, at + 25], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const highlight = frame >= 230; // LPG menyala sebagai contoh keluaran

  // Titik keluar/masuk panah: sisi kanan→kiri (landscape) atau bawah→atas (portrait).
  const exitPt = (r: Rect) => (portrait ? {x: r.x + r.w / 2, y: r.y + r.h} : {x: r.x + r.w, y: r.y + r.h / 2});
  const entryPt = (r: Rect) => (portrait ? {x: r.x + r.w / 2, y: r.y} : {x: r.x, y: r.y + r.h / 2});

  const arrow = (from: Rect, to: Rect, key: string, at: number, color: string, w: number) => {
    const a = exitPt(from);
    const b = entryPt(to);
    const len = Math.hypot(b.x - a.x, b.y - a.y);
    return <line key={key} x1={a.x} y1={a.y} x2={b.x} y2={b.y} stroke={color} strokeWidth={w} markerEnd="url(#arrow)" strokeDasharray={len} strokeDashoffset={len * (1 - draw(at))} />;
  };

  return (
    <AbsoluteFill>
      <AbsoluteFill style={{padding: portrait ? `200px ${padX}px` : `70px ${padX}px`}}>
        <Caption text="Jaringan saraf konvolusional dua cabang" size={title(56)} />
      </AbsoluteFill>

      <svg width={width} height={height} style={{position: 'absolute'}}>
        <defs>
          <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">
            <path d="M0,0 L10,5 L0,10 z" fill={COLORS.blueLight} />
          </marker>
        </defs>
        {ARROWS.map(([a, b], i) => arrow(g.boxes[a], g.boxes[b], `a${i}`, 40 + i * 25, COLORS.blueLight, 4))}
        {g.outputs.slice(0, 3).map((o, i) => arrow(g.boxes.mg, o, `o${i}`, 160, COLORS.line, 3))}
      </svg>

      {BOXES.map((b) => {
        const r = g.boxes[b.id];
        const p = appear(b.at);
        return (
          <div
            key={b.id}
            style={{
              position: 'absolute',
              left: r.x,
              top: r.y,
              width: r.w,
              height: r.h,
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
        const r = g.outputs[i];
        const extra = i === OUTPUTS.length - 1; // kelas tambahan dilatih per kilang (CH₄, CO, NH₃, ...)
        const on = o === 'LPG' && highlight;
        return (
          <div
            key={o}
            style={{
              position: 'absolute',
              left: r.x,
              top: r.y,
              width: r.w,
              height: r.h,
              borderRadius: 14,
              display: 'flex',
              alignItems: 'center',
              paddingLeft: 26,
              fontSize: extra ? 26 : 32,
              fontWeight: extra ? 400 : 600,
              opacity: appear(extra ? 250 : 170 + i * 10),
              backgroundColor: on ? COLORS.gas : extra ? 'transparent' : COLORS.surface,
              color: on ? COLORS.charcoal : extra ? COLORS.muted : COLORS.text,
              border: extra ? `3px dashed ${COLORS.muted}` : `3px solid ${on ? COLORS.gas : COLORS.line}`,
            }}
          >
            {o}
          </div>
        );
      })}
      <div style={{position: 'absolute', left: g.softmax.x, top: g.softmax.y, fontSize: 24, color: COLORS.muted, opacity: appear(160)}}>Softmax · kelas gas</div>

      <div style={{position: 'absolute', left: g.badges.x, top: g.badges.y, display: 'flex', flexWrap: 'wrap', gap: 20, width: portrait ? 952 : undefined}}>
        <Badge text="Kuantisasi int8" from={260} />
        <Badge text="Inferensi on-device" from={280} />
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
