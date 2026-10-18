import React from 'react';
import {AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {Caption} from '../components/Caption';
import {SceneFrame} from '../components/SceneFrame';
import {FAILED_NODE, FAILOVER_ROUTE, LINKS, NODES, PRIMARY_ROUTE, nodeById} from '../data/mesh';
import {COLORS} from '../theme';

const FAIL_AT = 330; // frame relatif adegan saat Cluster Head mati
const SPAWN_EVERY = 40;
const TRAVEL = 80;

const pointOnRoute = (route: string[], t: number) => {
  const pts = route.map(nodeById);
  const seg = Math.min(Math.floor(t * (pts.length - 1)), pts.length - 2);
  const local = t * (pts.length - 1) - seg;
  return {x: pts[seg].x + (pts[seg + 1].x - pts[seg].x) * local, y: pts[seg].y + (pts[seg + 1].y - pts[seg].y) * local};
};

const onRoute = (route: string[], a: string, b: string) =>
  route.some((n, i) => i < route.length - 1 && ((n === a && route[i + 1] === b) || (n === b && route[i + 1] === a)));

export const Scene06Mesh: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const failed = frame >= FAIL_AT;
  const route = failed ? FAILOVER_ROUTE : PRIMARY_ROUTE;
  const blink = failed ? 0.5 + 0.5 * Math.sin((frame - FAIL_AT) / 3) : 1;

  // Paket yang sedang berjalan. Paket primer yang akan melewati node gagal tidak lagi dikirim.
  const packets: {x: number; y: number; key: number}[] = [];
  for (let s = 60; s <= frame; s += SPAWN_EVERY) {
    const t = (frame - s) / TRAVEL;
    if (t < 0 || t > 1) continue;
    const usesPrimary = s + TRAVEL < FAIL_AT;
    const usesFailover = s > FAIL_AT + 30;
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
          return (
            <line
              key={`${a}-${b}`}
              x1={na.x}
              y1={na.y}
              x2={nb.x}
              y2={nb.y}
              stroke={dead ? COLORS.alarm : active ? COLORS.blueLight : COLORS.line}
              strokeOpacity={dead ? 0.35 : 1}
              strokeWidth={active ? 6 : 3}
              strokeDasharray={dead ? '10 12' : undefined}
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
        <Caption text="tanpa internet · tanpa kabel data · multi-hop" from={25} size={36} weight={400} color={COLORS.muted} style={{marginTop: 8}} />
      </AbsoluteFill>

      {failed && (
        <AbsoluteFill style={{alignItems: 'flex-end', padding: '70px 120px'}}>
          <Caption text="Self-healing: rute berpindah otomatis" from={FAIL_AT + 20} size={44} color={COLORS.ok} />
        </AbsoluteFill>
      )}

      <div
        style={{
          position: 'absolute',
          left: 120,
          bottom: 140,
          fontSize: 24,
          color: COLORS.muted,
          opacity: interpolate(frame, [500, 530], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}),
        }}
      >
        Diuji dengan 8 Cluster Head multi-hop di kampus ITB
      </div>
    </SceneFrame>
  );
};
