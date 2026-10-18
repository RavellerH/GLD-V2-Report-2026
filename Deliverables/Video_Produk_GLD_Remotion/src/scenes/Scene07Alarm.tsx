import React from 'react';
import {AbsoluteFill, Img, spring, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {ASSETS} from '../assets';
import {AssetSlot} from '../components/AssetSlot';
import {Caption} from '../components/Caption';
import {SceneFrame} from '../components/SceneFrame';
import {Sfx} from '../components/Sfx';
import {useLayout} from '../layout';
import {progress, useNarration} from '../motion';
import {COLORS} from '../theme';

// Screenshot Alarm Console RU4 (1920x1080) diperkecil ke bingkai berikut.
// Portrait: screenshot selebar layar di bagian atas, kartu pull/push di bawahnya.
// `crop` = bagian screenshot yang ditampilkan (piksel screenshot). Portrait hanya menampilkan
// daftar alarm pada skala ~1:1 agar teksnya terbaca di layar HP.
const LAYOUTS = {
  landscape: {scale: 0.72, x: 120, y: 175, crop: {x: 0, y: 0, w: 1920, h: 1080}, cards: {x: 1180, y: 560, w: 600}, flow: {x: 1180, y: 300, w: 600}},
  portrait: {scale: 952 / 960, x: 64, y: 420, crop: {x: 236, y: 170, w: 960, h: 330}, cards: {x: 64, y: 1000, w: 952}, flow: {x: 64, y: 780, w: 952}},
};
// Baris alarm pertama pada screenshot asli (koordinat piksel screenshot).
const FIRST_ALERT = {x: 244, y: 241, w: 1651, h: 70};

type Layout = (typeof LAYOUTS)['landscape'];
const toFrame = (L: Layout, r: typeof FIRST_ALERT) => ({
  left: L.x + (r.x - L.crop.x) * L.scale,
  top: L.y + (r.y - L.crop.y) * L.scale,
  width: Math.min(r.w, L.crop.x + L.crop.w - r.x) * L.scale,
  height: r.h * L.scale,
});

// Alur data: GLD -> Cluster Head -> Gateway -> Dashboard. Data normal disimpan di CH dan diambil
// berkala (pull, hijau). Alarm dikirim segera (push, merah) langsung ke dashboard.
const STEPS = ['GLD', 'Cluster Head', 'Gateway', 'Dashboard'];
const Flow: React.FC<{alarmAt: number; w: number}> = ({alarmAt, w}) => {
  const frame = useCurrentFrame();
  const xs = STEPS.map((_, i) => 40 + (i * (w - 80)) / (STEPS.length - 1));
  const y = 46;
  // pull berkala: CH -> Dashboard, setiap 75 frame, berhenti saat alarm
  const pulls: number[] = [];
  for (let s = 10; s < Math.min(frame, alarmAt); s += 75) pulls.push(s);
  const push = progress(frame, alarmAt, 26);
  const along = (a: number, b: number, t: number) => a + (b - a) * t;
  return (
    <svg width={w} height={110} style={{overflow: 'visible'}}>
      <line x1={xs[0]} y1={y} x2={xs[3]} y2={y} stroke={COLORS.line} strokeWidth={4} />
      {pulls.map((s) => {
        const t = (frame - s) / 50;
        if (t < 0 || t > 1) return null;
        return <circle key={s} cx={along(xs[1], xs[3], t)} cy={y} r={8} fill={COLORS.ok} opacity={Math.sin(Math.PI * t)} />;
      })}
      {push > 0 && push < 1 && <circle cx={along(xs[0], xs[3], push)} cy={y} r={11} fill={COLORS.alarm} style={{filter: `drop-shadow(0 0 10px ${COLORS.alarm})`}} />}
      {push > 0 && <line x1={xs[0]} y1={y} x2={along(xs[0], xs[3], push)} y2={y} stroke={COLORS.alarm} strokeWidth={4} opacity={0.8} />}
      {STEPS.map((label, i) => {
        const hit = i === 3 ? progress(frame, alarmAt + 24, 10) : i === 0 ? progress(frame, alarmAt - 8, 8) : 0;
        return (
          <g key={label} transform={`translate(${xs[i]} ${y})`}>
            <circle r={18} fill={COLORS.surface} stroke={hit > 0 ? COLORS.alarm : COLORS.blue} strokeWidth={4} />
            <circle r={7} fill={hit > 0 ? COLORS.alarm : COLORS.blue} />
            <text y={48} fill={COLORS.text} fontSize={22} fontWeight={600} textAnchor="middle">
              {label}
            </text>
          </g>
        );
      })}
    </svg>
  );
};

export const Scene07Alarm: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const {portrait, padX, title} = useLayout();
  const at = useNarration('alarm');
  const L = portrait ? LAYOUTS.portrait : LAYOUTS.landscape;
  const ALARM_AT = at('alarm dikirim segera');
  const ring = spring({frame: frame - (ALARM_AT + 26), fps, config: {damping: 16}});
  const pulse = 0.5 + 0.5 * Math.abs(Math.sin((frame - ALARM_AT) / 8));
  const shot = progress(frame, 4, 24);

  return (
    <SceneFrame theme="light">
      <div
        style={{
          position: 'absolute',
          left: L.x,
          top: L.y,
          width: L.crop.w * L.scale,
          height: L.crop.h * L.scale,
          borderRadius: 14,
          overflow: 'hidden',
          boxShadow: '0 30px 80px rgba(20,33,58,0.35)',
          opacity: shot,
          transform: `translateY(${24 * (1 - shot)}px)`,
        }}
      >
        {ASSETS.dashboard.ready ? (
          <Img
            src={staticFile(ASSETS.dashboard.path)}
            style={{position: 'absolute', left: -L.crop.x * L.scale, top: -L.crop.y * L.scale, width: 1920 * L.scale, height: 1080 * L.scale}}
          />
        ) : (
          <AssetSlot asset={ASSETS.dashboard} kind="image" />
        )}
      </div>

      {/* Sorot alarm masuk, tepat setelah paket alarm tiba di dashboard */}
      <div
        style={{
          position: 'absolute',
          ...toFrame(L, FIRST_ALERT),
          borderRadius: 12,
          border: `4px solid ${COLORS.alarm}`,
          boxShadow: `0 0 ${36 * pulse}px ${COLORS.alarm}`,
          opacity: ring,
          transform: `scale(${1.04 - 0.04 * ring})`,
        }}
      />

      <Sfx name="blip" at={ALARM_AT} volume={0.35} />
      <Sfx name="alarm" at={ALARM_AT + 26} volume={0.45} />
      {/* Alur data GLD -> CH -> Gateway -> Dashboard */}
      <div
        style={{
          position: 'absolute',
          left: L.flow.x,
          top: L.flow.y,
          width: L.flow.w,
          padding: '16px 0 4px',
          borderRadius: 14,
          backgroundColor: COLORS.surface,
          border: `1px solid ${COLORS.line}`,
          boxShadow: '0 8px 24px rgba(20,33,58,0.12)',
          opacity: progress(frame, 12, 20),
        }}
      >
        <Flow alarmAt={ALARM_AT} w={L.flow.w} />
      </div>

      {/* Dua jalur data: normal (cache + pull berkala) vs alarm (push segera). */}
      <div style={{position: 'absolute', left: L.cards.x, top: L.cards.y, width: L.cards.w, display: 'flex', flexDirection: 'column', gap: 18}}>
        {[
          {label: 'Data normal', sub: 'disimpan pada Cluster Head, diambil secara berkala (pull)', color: COLORS.ok, at: at('Data normal')},
          {label: 'Alarm', sub: 'dikirim segera melalui mekanisme push, tanpa menunggu siklus pull', color: COLORS.alarm, at: ALARM_AT},
        ].map((r) => {
          const p = spring({frame: frame - r.at, fps, config: {damping: 200}});
          return (
            <div
              key={r.label}
              style={{
                opacity: p,
                transform: `translateX(${20 * (1 - p)}px)`,
                padding: '18px 22px',
                borderRadius: 14,
                backgroundColor: COLORS.surface,
                border: `1px solid ${COLORS.line}`,
                borderLeft: `8px solid ${r.color}`,
                boxShadow: '0 8px 24px rgba(20,33,58,0.12)',
              }}
            >
              <div style={{fontSize: 28, fontWeight: 800}}>{r.label}</div>
              <div style={{fontSize: 22, marginTop: 4, color: COLORS.muted}}>{r.sub}</div>
            </div>
          );
        })}
      </div>

      <AbsoluteFill style={{padding: portrait ? `200px ${padX}px` : `56px 120px`}}>
        <Caption text="Notifikasi alarm kepada operator" size={title(60)} />
      </AbsoluteFill>
      <div style={{position: 'absolute', right: portrait ? undefined : 120, left: portrait ? padX : undefined, top: portrait ? 365 : 88, fontSize: 22, color: COLORS.muted}}>
        Dashboard GLD · RU IV · data demonstrasi
      </div>
    </SceneFrame>
  );
};
