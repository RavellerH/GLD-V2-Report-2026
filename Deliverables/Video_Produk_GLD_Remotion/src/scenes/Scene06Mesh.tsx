import React from 'react';
import {AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {Caption} from '../components/Caption';
import {SceneFrame} from '../components/SceneFrame';
import {FAILED_NODE, FAILOVER_ROUTE, LINKS, NODES, PRIMARY_ROUTE, nodeById} from '../data/mesh';
import {COLORS} from '../theme';

// Frame relatif adegan. FAIL_AT diselaraskan dengan kalimat ketiga narasi ("Bila satu Cluster Head gagal").
const FAIL_AT = 560;
const REROUTE_AT = 680;
const SPAWN_EVERY = 40;
const TRAVEL = 80;

// Langkah pemulihan rute; parameter dari Technical Datasheet Rev 4.0 (firmware Cluster Head).
const RECOVERY_STEPS = [
  {at: FAIL_AT + 20, text: 'Induk tak terdengar → dinyatakan kedaluwarsa'},
  {at: FAIL_AT + 60, text: 'Evaluasi hingga 8 kandidat induk'},
  {at: FAIL_AT + 100, text: 'Pindah bila sinyal ≥ 15 dB lebih baik'},
  {at: FAIL_AT + 140, text: 'Loop guard & cek jalur ke gateway'},
];

const pointOnRoute = (route: string[], t: number) => {
  const pts = route.map(nodeById);
  const seg = Math.min(Math.floor(t * (pts.length - 1)), pts.length - 2);
  const local = t * (pts.length - 1) - seg;
  return {x: pts[seg].x + (pts[seg + 1].x - pts[seg].x) * local, y: pts[seg].y + (pts[seg + 1].y - pts[seg].y) * local};
};

const onRoute = (route: string[], a: string, b: string) =>
  route.some((n, i) => i < route.length - 1 && ((n === a && route[i + 1] === b) || (n === b && route[i + 1] === a)));

const isStarLink = (a: string, b: string) => nodeById(a).kind === 'gld' || nodeById(b).kind === 'gld';

const InfoPanel: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const show = (at: number) => spring({frame: frame - at, fps, config: {damping: 200}});
  const row = (color: string, title: string, sub: string, at: number, dashed = false) => (
    <div style={{display: 'flex', gap: 18, alignItems: 'center', opacity: show(at), marginTop: 18}}>
      <svg width={56} height={12}>
        <line x1={0} y1={6} x2={56} y2={6} stroke={color} strokeWidth={6} strokeDasharray={dashed ? '10 8' : undefined} />
      </svg>
      <div>
        <div style={{fontSize: 28, fontWeight: 600}}>{title}</div>
        <div style={{fontSize: 22, color: COLORS.muted}}>{sub}</div>
      </div>
    </div>
  );

  return (
    <div style={{position: 'absolute', left: 1330, top: 250, width: 500}}>
      <div style={{fontSize: 24, fontWeight: 800, color: COLORS.blueLight, letterSpacing: 1, opacity: show(60)}}>DUA LAPIS RADIO</div>
      {row(COLORS.gas, 'STAR · 920 MHz', 'node sensor → Cluster Head', 80, true)}
      {row(COLORS.blueLight, 'MESH · 921 MHz', 'Cluster Head ↔ Cluster Head → gateway', 110)}

      <div style={{fontSize: 24, fontWeight: 800, color: COLORS.ok, letterSpacing: 1, marginTop: 48, opacity: show(FAIL_AT)}}>PEMULIHAN RUTE OTOMATIS</div>
      {RECOVERY_STEPS.map((s, i) => (
        <div key={s.text} style={{display: 'flex', gap: 16, marginTop: 16, opacity: show(s.at), fontSize: 25, lineHeight: 1.3}}>
          <div
            style={{
              flex: '0 0 40px',
              height: 40,
              borderRadius: 20,
              backgroundColor: COLORS.ok,
              color: COLORS.charcoal,
              fontWeight: 800,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
            }}
          >
            {i + 1}
          </div>
          <div>{s.text}</div>
        </div>
      ))}
    </div>
  );
};

export const Scene06Mesh: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const failed = frame >= FAIL_AT;
  const rerouted = frame >= REROUTE_AT;
  const route = rerouted ? FAILOVER_ROUTE : PRIMARY_ROUTE;
  const blink = failed ? 0.5 + 0.5 * Math.sin((frame - FAIL_AT) / 3) : 1;

  // Paket yang sedang berjalan. Selama pemulihan rute tidak ada paket baru yang dikirim.
  const packets: {x: number; y: number; key: number}[] = [];
  for (let s = 60; s <= frame; s += SPAWN_EVERY) {
    const t = (frame - s) / TRAVEL;
    if (t < 0 || t > 1) continue;
    const usesPrimary = s + TRAVEL < FAIL_AT;
    const usesFailover = s >= REROUTE_AT;
    if (!usesPrimary && !usesFailover) continue;
    packets.push({...pointOnRoute(usesPrimary ? PRIMARY_ROUTE : FAILOVER_ROUTE, t), key: s});
  }

  return (
    <SceneFrame>
      <svg width={1920} height={1080} style={{position: 'absolute'}}>
        {LINKS.map(([a, b]) => {
          const na = nodeById(a);
          const nb = nodeById(b);
          const active = onRoute(route, a, b);
          const dead = failed && (a === FAILED_NODE || b === FAILED_NODE);
          const star = isStarLink(a, b);
          const base = star ? COLORS.gas : COLORS.line;
          return (
            <line
              key={`${a}-${b}`}
              x1={na.x}
              y1={na.y}
              x2={nb.x}
              y2={nb.y}
              stroke={dead ? COLORS.alarm : active ? COLORS.blueLight : base}
              strokeOpacity={dead ? 0.35 : star && !active ? 0.5 : 1}
              strokeWidth={active ? 6 : 3}
              strokeDasharray={dead || star ? '10 10' : undefined}
            />
          );
        })}

        {NODES.map((n, i) => {
          const p = spring({frame: frame - i * 5, fps, config: {damping: 14}});
          const isFailed = failed && n.id === FAILED_NODE;
          const r = n.kind === 'gw' ? 34 : n.kind === 'ch' ? 24 : 16;
          const fill = isFailed ? COLORS.alarm : n.kind === 'gld' ? COLORS.gas : COLORS.blue;
          return (
            <g key={n.id} transform={`translate(${n.x} ${n.y}) scale(${p})`} opacity={isFailed ? blink : 1}>
              <circle r={r + 14} fill={fill} fillOpacity={0.18} />
              <circle r={r} fill={fill} />
              {isFailed && <path d="M -12 -12 L 12 12 M 12 -12 L -12 12" stroke={COLORS.text} strokeWidth={5} strokeLinecap="round" />}
              <text y={r + 36} fill={COLORS.text} fontSize={24} fontWeight={600} textAnchor="middle">
                {n.label}
              </text>
            </g>
          );
        })}

        {packets.map((pk) => (
          <circle key={pk.key} cx={pk.x} cy={pk.y} r={11} fill={COLORS.text} style={{filter: `drop-shadow(0 0 10px ${COLORS.blueLight})`}} />
        ))}
      </svg>

      <AbsoluteFill style={{padding: '60px 120px'}}>
        <Caption text="Private Mesh LoRa" size={70} />
        <Caption text="tanpa internet · terpisah dari jaringan TI kilang · multi-hop" from={25} size={34} weight={400} color={COLORS.muted} style={{marginTop: 8}} />
      </AbsoluteFill>

      <InfoPanel />

      <div
        style={{
          position: 'absolute',
          left: 1330,
          top: 880,
          fontSize: 22,
          color: COLORS.muted,
          opacity: interpolate(frame, [REROUTE_AT + 60, REROUTE_AT + 90], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}),
        }}
      >
        Failover diuji dengan 8 Cluster Head multi-hop di kampus ITB
      </div>
    </SceneFrame>
  );
};
