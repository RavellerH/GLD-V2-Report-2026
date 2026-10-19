import React from 'react';
import {AbsoluteFill, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {Caption} from '../components/Caption';
import {SceneFrame} from '../components/SceneFrame';
import {Sfx} from '../components/Sfx';
import {FAILED_NODE, FAILOVER_ROUTE, LINKS, NODES, PRIMARY_ROUTE, nodeById} from '../data/mesh';
import {useLang, useT} from '../i18n';
import {useLayout} from '../layout';
import {progress, useNarration} from '../motion';
import {COLORS} from '../theme';

const SPAWN_EVERY = 40;
const TRAVEL = 80;

// Waktu kejadian dari narasi: CH gagal saat "Bila satu Cluster Head gagal", rute pindah saat
// "memilih induk baru". Langkah pemulihan (Technical Datasheet Rev 4.0) tersebar mengikuti kalimat.
const useTimes = () => {
  const at = useNarration('mesh');
  const FAIL_AT = at(['Bila satu Cluster Head gagal', 'If a Cluster Head fails']);
  const REROUTE_AT = at(['memilih parent baru', 'select a new parent']);
  const HYS = at(['hysteresis', 'hysteresis']);
  const gap = Math.max(18, Math.round((HYS - FAIL_AT) / 3));
  return {
    at,
    FAIL_AT,
    REROUTE_AT,
    STEPS: [
      {at: FAIL_AT + 10, text: ['Parent tidak terdeteksi → dinyatakan kedaluwarsa', 'Parent not heard → marked as stale'] as [string, string]},
      {at: FAIL_AT + 10 + gap, text: ['Evaluasi hingga delapan kandidat parent', 'Evaluation of up to eight parent candidates'] as [string, string]},
      {at: HYS, text: ['Berpindah bila sinyal ≥ 15 dB lebih baik (hysteresis)', 'Switch only if the signal is ≥ 15 dB better (hysteresis)'] as [string, string]},
      {at: at(['loop prevention', 'loop prevention']), text: ['Loop prevention dan verifikasi jalur ke gateway', 'Loop prevention and gateway path verification'] as [string, string]},
    ],
  };
};

// Koordinat node di data/mesh.ts dibuat untuk landscape (alur kiri→kanan).
// Portrait memutar alurnya jadi atas→bawah dan memetakannya ke area 1080 lebar.
type Pt = {x: number; y: number};
const toPortrait = (p: Pt): Pt => ({x: 110 + ((p.y - 330) / 500) * 860, y: 380 + ((p.x - 150) / 1030) * 560});
const usePos = () => {
  const {portrait} = useLayout();
  return (id: string): Pt => {
    const n = nodeById(id);
    return portrait ? toPortrait(n) : {x: n.x, y: n.y};
  };
};

const pointOnRoute = (pos: (id: string) => Pt, route: string[], t: number) => {
  const pts = route.map(pos);
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
  const {portrait} = useLayout();
  const {at, FAIL_AT, STEPS} = useTimes();
  const t = useT();
  const show = (t: number) => spring({frame: frame - t, fps, config: {damping: 200}});
  const row = (color: string, title: string, sub: string, t: number, dashed = false) => (
    <div style={{display: 'flex', gap: 18, alignItems: 'center', opacity: show(t), transform: `translateX(${16 * (1 - show(t))}px)`, marginTop: 18}}>
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
    <div style={{position: 'absolute', left: portrait ? 64 : 1330, top: portrait ? 1020 : 250, width: portrait ? 952 : 500}}>
      <div style={{fontSize: 24, fontWeight: 800, color: COLORS.blueLight, letterSpacing: 1, opacity: show(at(['dua lapis', 'two-layer'], -10))}}>{t('ARSITEKTUR RADIO DUA LAPIS', 'TWO-LAYER RADIO ARCHITECTURE')}</div>
      {row(COLORS.gas, 'STAR · 920 MHz', t('node sensor → Cluster Head', 'sensor node → Cluster Head'), at(['Node sensor terhubung', 'Sensor nodes connect']), true)}
      {row(COLORS.blueLight, 'MESH · 921 MHz', t('antar-Cluster Head → gateway', 'Cluster Head to Cluster Head → gateway'), at(['antar-Cluster Head', 'the Cluster Heads form']))}

      <div style={{fontSize: 24, fontWeight: 800, color: COLORS.ok, letterSpacing: 1, marginTop: portrait ? 28 : 48, opacity: show(FAIL_AT)}}>{t('PEMULIHAN RUTE OTOMATIS', 'AUTOMATIC ROUTE RECOVERY')}</div>
      {STEPS.map((s, i) => (
        <div
          key={s.text[0]}
          style={{display: 'flex', gap: 16, marginTop: portrait ? 10 : 16, opacity: show(s.at), transform: `translateX(${16 * (1 - show(s.at))}px)`, fontSize: 25, lineHeight: 1.3}}
        >
          <div
            style={{
              flex: '0 0 40px',
              height: 40,
              borderRadius: 20,
              backgroundColor: COLORS.ok,
              color: '#FFFFFF',
              fontWeight: 800,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
            }}
          >
            {i + 1}
          </div>
          <div>{t(s.text[0], s.text[1])}</div>
        </div>
      ))}
    </div>
  );
};

export const Scene06Mesh: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const {portrait, padX, width, height, title} = useLayout();
  const pos = usePos();
  const {FAIL_AT, REROUTE_AT} = useTimes();
  const t = useT();
  const failP = progress(frame, FAIL_AT, 12); // CH gagal memudar ke merah
  const rerouteP = progress(frame, REROUTE_AT, 36); // rute baru digambar bertahap
  const blink = failP > 0 ? 0.6 + 0.4 * Math.cos((frame - FAIL_AT) / 4) : 1;

  // Paket yang sedang berjalan. Selama pemulihan rute tidak ada paket baru yang dikirim.
  const packets: {x: number; y: number; key: number; o: number}[] = [];
  for (let s = 60; s <= frame; s += SPAWN_EVERY) {
    const t = (frame - s) / TRAVEL;
    if (t < 0 || t > 1) continue;
    const usesPrimary = s + TRAVEL < FAIL_AT;
    const usesFailover = s >= REROUTE_AT + 36;
    if (!usesPrimary && !usesFailover) continue;
    packets.push({...pointOnRoute(pos, usesPrimary ? PRIMARY_ROUTE : FAILOVER_ROUTE, t), key: s, o: Math.min(1, Math.sin(Math.PI * t) * 3)});
  }

  return (
    <SceneFrame theme="light">
      <svg width={width} height={height} style={{position: 'absolute'}}>
        {LINKS.map(([a, b], i) => {
          const na = pos(a);
          const nb = pos(b);
          const dead = a === FAILED_NODE || b === FAILED_NODE;
          const star = isStarLink(a, b);
          const len = Math.hypot(nb.x - na.x, nb.y - na.y);
          const reveal = progress(frame, 10 + i * 4, 30); // tautan tergambar berurutan di awal
          const primary = onRoute(PRIMARY_ROUTE, a, b);
          const failover = onRoute(FAILOVER_ROUTE, a, b);
          const line = (props: React.SVGProps<SVGLineElement>) => <line x1={na.x} y1={na.y} x2={nb.x} y2={nb.y} {...props} />;
          return (
            <g key={`${a}-${b}`}>
              {/* dasar: STAR oranye putus-putus, MESH abu-abu */}
              {line({
                stroke: star ? COLORS.gas : COLORS.line,
                strokeOpacity: star ? 0.55 : 1,
                strokeWidth: 3,
                strokeDasharray: star ? '10 10' : `${len}`,
                strokeDashoffset: star ? 0 : len * (1 - reveal),
                opacity: reveal,
              })}
              {/* rute utama memudar saat CH gagal; tautan yang juga dipakai rute baru tetap menyala */}
              {primary && line({stroke: COLORS.blueLight, strokeWidth: 6, opacity: reveal * (failover ? 1 : 1 - failP)})}
              {/* tautan ke CH yang gagal: merah putus-putus */}
              {dead && line({stroke: COLORS.alarm, strokeWidth: 4, strokeDasharray: '10 10', opacity: failP * 0.6})}
              {/* rute baru digambar bertahap */}
              {failover && !primary && line({stroke: COLORS.blueLight, strokeWidth: 6, strokeDasharray: `${len}`, strokeDashoffset: len * (1 - rerouteP)})}
            </g>
          );
        })}

        {NODES.map((n, i) => {
          const p = spring({frame: frame - i * 5, fps, config: {damping: 18, mass: 0.7}});
          const isFailed = n.id === FAILED_NODE;
          const r = n.kind === 'gw' ? 34 : n.kind === 'ch' ? 24 : 16;
          const fill = n.kind === 'gld' ? COLORS.gas : COLORS.blue;
          return (
            <g key={n.id} transform={`translate(${pos(n.id).x} ${pos(n.id).y}) scale(${p})`} opacity={isFailed ? blink : 1}>
              <circle r={r + 14} fill={fill} fillOpacity={0.18} />
              <circle r={r} fill={fill} />
              {isFailed && <circle r={r + 2} fill={COLORS.alarm} opacity={failP} />}
              {isFailed && <path d="M -12 -12 L 12 12 M 12 -12 L -12 12" stroke="#FFFFFF" strokeWidth={5} strokeLinecap="round" opacity={failP} />}
              <text y={r + 36} fill={COLORS.text} fontSize={24} fontWeight={600} textAnchor="middle">
                {n.label}
              </text>
            </g>
          );
        })}

        {packets.map((pk) => (
          <circle key={pk.key} cx={pk.x} cy={pk.y} r={11} fill={COLORS.blue} opacity={pk.o} style={{filter: `drop-shadow(0 0 8px ${COLORS.blueLight})`}} />
        ))}
      </svg>

      <AbsoluteFill style={{padding: portrait ? `180px ${padX}px` : `60px ${padX}px`}}>
        <Caption text={t('Jaringan Private Mesh LoRa', 'Private LoRa Mesh Network')} size={title(70)} />
        <Caption text={t('multi-hop · independen dari internet dan jaringan TI kilang', 'multi-hop · independent of the internet and the refinery IT network')} from={25} size={title(34)} weight={400} color={COLORS.muted} style={{marginTop: 8}} />
      </AbsoluteFill>

      <InfoPanel />
      <Sfx name="error" at={FAIL_AT} volume={0.45} />
      <Sfx name="success" at={REROUTE_AT + 36} volume={0.4} />

      <div
        style={{
          position: 'absolute',
          left: portrait ? 64 : 1330,
          top: portrait ? 1500 : 880,
          fontSize: 22,
          color: COLORS.muted,
          opacity: progress(frame, REROUTE_AT + 50, 24),
        }}
      >
        {t('Mekanisme failover telah diuji pada 8 Cluster Head di kampus ITB', 'Failover mechanism tested on 8 Cluster Heads at the ITB campus')}
      </div>
    </SceneFrame>
  );
};
