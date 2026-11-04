import React from 'react';
import {AbsoluteFill, OffthreadVideo, Sequence, interpolate, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {useT} from '../i18n';
import {useLayout} from '../layout';
import {progress} from '../motion';
import {COLORS} from '../theme';

// Penjelajahan dashboard RU IV (rekaman layar aplikasi asli, data demonstrasi; diputar 2x).
// Rentang dalam detik rekaman footage/dashboard_walk.mp4.
const RATE = 2;
const SEGMENTS = [
  {a: 1.0, b: 12.0, id: ['Ringkasan sistem', 'System overview'], sub: ['Status unit, sensor aktif, tren gas', 'Unit status, active sensors, gas trend']},
  {a: 22.8, b: 31.8, id: ['Daftar perangkat', 'Device fleet'], sub: ['Gateway, Cluster Head, sensor GLD', 'Gateway, Cluster Heads, GLD sensors']},
  {a: 36.4, b: 45.4, id: ['Topologi unit', 'Unit topology'], sub: ['Sensor per Cluster Head', 'Sensors per Cluster Head']},
  {a: 50.6, b: 63.6, id: ['Konsol alarm', 'Alarm console'], sub: ['Alarm masuk → acknowledge oleh operator', 'Incoming alarm → operator acknowledges']},
  {a: 66.2, b: 73.2, id: ['Log kejadian', 'Event log'], sub: ['Jejak audit setiap alarm', 'Audit trail of every alarm']},
  {a: 77.4, b: 91.4, id: ['Analitik', 'Analytics'], sub: ['Tren, heatmap, sensor berisiko', 'Trends, heatmap, risky sensors']},
];
export const TOUR_SEC = SEGMENTS.reduce((s, g) => s + (g.b - g.a) / RATE, 0) + 0.5;

export const DashboardTour: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const {portrait, padX, width, height} = useLayout();
  const t = useT();
  const W = portrait ? width - 40 : 1560;
  const H = (W * 1080) / 1920;
  const X = (width - W) / 2;
  const Y = portrait ? 620 : 180;
  let acc = 0;
  const seq = SEGMENTS.map((g) => {
    const d = Math.round(((g.b - g.a) / RATE) * fps);
    const s = {...g, from: acc, d};
    acc += d;
    return s;
  });
  const cur = seq.findIndex((s) => frame >= s.from && frame < s.from + s.d);
  const enter = progress(frame, 0, 18);
  return (
    <AbsoluteFill style={{background: 'radial-gradient(ellipse at 50% 40%, #0B1A33 0%, #03070F 70%)', opacity: enter}}>
      <div style={{position: 'absolute', left: padX, top: portrait ? 200 : 52, color: '#F2F5FA'}}>
        <div style={{fontSize: 22, fontWeight: 800, letterSpacing: 3, color: COLORS.blueLight}}>{t('DASHBOARD OPERATOR · RU IV', 'OPERATOR DASHBOARD · RU IV')}</div>
        <div style={{fontSize: portrait ? 48 : 46, fontWeight: 800, marginTop: 4}}>{t('Dari alarm hingga analitik, dalam satu layar', 'From alarm to analytics, on one screen')}</div>
      </div>
      {/* bab */}
      <div style={{position: 'absolute', left: portrait ? padX : X, right: portrait ? padX : undefined, top: portrait ? 400 : Y + H + 22, display: 'flex', flexWrap: 'wrap', gap: 10}}>
        {seq.map((s, i) => (
          <div
            key={s.id[0]}
            style={{
              padding: '8px 16px',
              borderRadius: 999,
              fontSize: portrait ? 22 : 20,
              fontWeight: 700,
              color: i === cur ? '#fff' : i < cur ? '#9FB3D1' : '#5A6B86',
              backgroundColor: i === cur ? (i === 3 ? COLORS.alarm : COLORS.blue) : 'rgba(17,28,46,0.8)',
              border: `1px solid ${i === cur ? 'transparent' : '#26354D'}`,
            }}
          >
            {t(s.id[0], s.id[1])}
          </div>
        ))}
      </div>
      {/* layar */}
      <div style={{position: 'absolute', left: X, top: Y, width: W, height: H, borderRadius: 14, overflow: 'hidden', boxShadow: '0 0 0 1px #2B3D5C, 0 30px 90px rgba(0,0,0,0.6), 0 0 60px rgba(43,95,203,0.25)'}}>
        {seq.map((s) => (
          <Sequence key={s.id[0]} from={s.from} durationInFrames={s.d} layout="none">
            <Seg s={s} W={W} H={H} />
          </Sequence>
        ))}
      </div>
      {cur >= 0 && (
        <div
          style={{
            position: 'absolute',
            left: portrait ? padX : X + W - 560,
            top: portrait ? Y + H + 30 : Y + 24,
            width: portrait ? width - padX * 2 : 520,
            padding: '14px 20px',
            borderRadius: 12,
            backgroundColor: 'rgba(4,8,16,0.85)',
            border: `1px solid ${cur === 3 ? COLORS.alarm : '#2B3D5C'}`,
            color: '#E3E8F0',
            fontSize: portrait ? 26 : 22,
            opacity: interpolate(frame - seq[cur].from, [0, 10, seq[cur].d - 10, seq[cur].d], [0, 1, 1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}),
          }}
        >
          <b style={{color: '#fff'}}>{t(seq[cur].id[0], seq[cur].id[1])}</b> — {t(seq[cur].sub[0], seq[cur].sub[1])}
        </div>
      )}
      <div style={{position: 'absolute', left: portrait ? padX : X, top: portrait ? height - 140 : Y + H + 74, fontSize: 18, color: '#7F90AB'}}>
        {t('Rekaman layar aplikasi dashboard GLD · data demonstrasi · dipercepat 2×', 'Screen recording of the GLD dashboard app · demonstration data · 2× speed')}
      </div>
    </AbsoluteFill>
  );
};

const Seg: React.FC<{s: {a: number; b: number; d: number}; W: number; H: number}> = ({s, W, H}) => {
  const frame = useCurrentFrame();
  const z = interpolate(frame, [0, s.d], [1, 1.035]);
  const fade = interpolate(frame, [0, 6], [0, 1], {extrapolateRight: 'clamp'});
  return (
    <AbsoluteFill style={{opacity: fade}}>
      <OffthreadVideo
        src={staticFile('footage/dashboard_walk.mp4')}
        startFrom={Math.round(s.a * 30)}
        endAt={Math.round(s.b * 30)}
        playbackRate={RATE}
        muted
        style={{width: W, height: H, transform: `scale(${z})`, transformOrigin: '50% 40%'}}
      />
    </AbsoluteFill>
  );
};
