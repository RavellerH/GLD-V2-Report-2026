import React from 'react';
import {AbsoluteFill, Img, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {ASSETS} from './assets';
import {Sfx} from './components/Sfx';
import {LangProvider, useT} from './i18n';
import {useLayout} from './layout';
import {EASE, progress} from './motion';
import {FONT, PALETTES, themeVars} from './theme';
import type {Lang} from './timeline';

// Intro motion graphic ±7 dtk: titik gas -> gelombang LoRa -> 8 sensor membentuk pola sidik jari ->
// mesh menjalar -> judul GLD -> kartu logo mitra. Berdiri sendiri (GLD-Intro*) agar bisa dipakai di video lain.
export const INTRO_FRAMES = 210;
const P = PALETTES.night;
const GAS = P.gas;
const BLUE = '#5B9BFF';

// Pola respons 8 sensor (bentuk ilustratif radar, bukan data ukur).
const SHAPE = [0.55, 0.95, 0.35, 0.6, 0.4, 0.85, 0.7, 0.5];

const IntroBody: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps, width, height} = useVideoConfig();
  const {portrait} = useLayout();
  const t = useT();
  const cx = width / 2;
  const cy = portrait ? height * 0.36 : height * 0.42;
  const R = portrait ? 230 : 190;

  // 1) titik gas & gelombang LoRa
  const dot = spring({frame: frame - 4, fps, config: {damping: 12}});
  const rings = [0, 14, 28, 42].map((d) => {
    const p = interpolate(frame, [10 + d, 70 + d], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: EASE});
    return {r: 20 + p * (portrait ? 520 : 620), o: (1 - p) * 0.55};
  });

  // 2) 8 sensor menyebar ke lingkaran lalu pola radar terbentuk
  const spread = progress(frame, 34, 26);
  const shape = progress(frame, 56, 26);
  const pts = SHAPE.map((v, i) => {
    const a = (Math.PI * 2 * i) / 8 - Math.PI / 2;
    const rr = R * (0.18 + spread * 0.82) * (1 - shape + shape * (0.35 + v * 0.65));
    return {x: cx + Math.cos(a) * rr, y: cy + Math.sin(a) * rr, ox: cx + Math.cos(a) * R, oy: cy + Math.sin(a) * R};
  });
  const poly = pts.map((p) => `${p.x},${p.y}`).join(' ');

  // mesh: node-node di sekitar, terhubung bertahap
  const nodes = (portrait
    ? [[0.12, 0.12], [0.85, 0.1], [0.08, 0.55], [0.92, 0.5], [0.2, 0.8], [0.8, 0.82], [0.5, 0.08]]
    : [[0.08, 0.2], [0.92, 0.16], [0.14, 0.78], [0.88, 0.8], [0.3, 0.1], [0.7, 0.92], [0.04, 0.5], [0.96, 0.48]]
  ).map(([x, y]) => ({x: x * width, y: y * height}));
  const meshP = (i: number) => progress(frame, 62 + i * 4, 22);

  // 3) judul
  const titleIn = progress(frame, 92, 22);
  const subIn = progress(frame, 108, 18);
  const tagIn = progress(frame, 120, 18);
  // grafik mengecil ke atas saat judul muncul
  const lift = progress(frame, 88, 26);
  const gScale = 1 - lift * 0.28;
  const gY = -lift * (portrait ? 170 : 150);

  // 4) logo & penutup
  const logos = spring({frame: frame - 140, fps, config: {damping: 200}});
  const out = 1 - progress(frame, INTRO_FRAMES - 14, 14);

  const titleY = height * 0.5;

  return (
    <AbsoluteFill style={{...themeVars('night'), backgroundColor: P.bg, fontFamily: FONT, opacity: out}}>
      {/* grid halus */}
      <AbsoluteFill
        style={{
          backgroundImage: `linear-gradient(rgba(91,155,255,0.07) 1px, transparent 1px), linear-gradient(90deg, rgba(91,155,255,0.07) 1px, transparent 1px)`,
          backgroundSize: '64px 64px',
          opacity: progress(frame, 0, 20),
          transform: `scale(${1.06 - 0.06 * progress(frame, 0, INTRO_FRAMES)})`,
        }}
      />
      <AbsoluteFill style={{background: `radial-gradient(circle at 50% ${portrait ? 36 : 42}%, rgba(43,95,203,0.28), transparent 60%)`}} />

      <svg width={width} height={height} style={{position: 'absolute'}}>
        {/* mesh ke node sekeliling */}
        {nodes.map((n, i) => {
          const p = meshP(i);
          const oy = cy + gY;
          const tx = cx + (n.x - cx) * p;
          const ty = oy + (n.y - oy) * p;
          return (
            <g key={i} opacity={(1 - lift * 0.75) * Math.min(1, p * 2)}>
              <line x1={cx} y1={oy} x2={tx} y2={ty} stroke={BLUE} strokeWidth={2} strokeOpacity={0.55} />
              <circle cx={tx} cy={ty} r={7 * p} fill={BLUE} />
              <circle cx={tx} cy={ty} r={18 * p} fill={BLUE} fillOpacity={0.15} />
            </g>
          );
        })}
        <g transform={`translate(${cx} ${cy}) scale(${gScale}) translate(${-cx} ${-cy + gY / gScale})`}>
          {/* gelombang LoRa */}
          {rings.map((r, i) => (
            <circle key={i} cx={cx} cy={cy} r={r.r} fill="none" stroke={BLUE} strokeWidth={2} strokeOpacity={r.o} />
          ))}
          {/* kisi radar */}
          {[0.33, 0.66, 1].map((k) => (
            <circle key={k} cx={cx} cy={cy} r={R * k} fill="none" stroke="rgba(242,245,250,0.12)" strokeWidth={1.5} opacity={spread} />
          ))}
          {pts.map((p, i) => (
            <line key={i} x1={cx} y1={cy} x2={p.ox} y2={p.oy} stroke="rgba(242,245,250,0.12)" strokeWidth={1.5} opacity={spread} />
          ))}
          {/* pola sidik jari gas */}
          <polygon points={poly} fill={GAS} fillOpacity={0.22 * shape} stroke={GAS} strokeWidth={4} strokeOpacity={Math.max(spread, 0.001)} strokeLinejoin="round" />
          {pts.map((p, i) => (
            <circle key={i} cx={p.x} cy={p.y} r={9 * Math.min(1, spread * 1.5)} fill={GAS} />
          ))}
          {/* titik gas pusat */}
          <circle cx={cx} cy={cy} r={14 * dot} fill={GAS} />
          <circle cx={cx} cy={cy} r={34 * dot} fill={GAS} fillOpacity={0.2} />
        </g>
      </svg>

      {/* judul */}
      <div style={{position: 'absolute', left: 0, right: 0, top: titleY, textAlign: 'center', color: '#F2F5FA'}}>
        <div
          style={{
            fontSize: portrait ? 190 : 200,
            fontWeight: 800,
            letterSpacing: 6,
            lineHeight: 1,
            clipPath: `inset(0 ${100 - titleIn * 100}% 0 0)`,
            transform: `translateY(${20 * (1 - titleIn)}px)`,
            background: `linear-gradient(90deg, #F2F5FA, ${BLUE})`,
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
          }}
        >
          GLD
        </div>
        <div style={{fontSize: portrait ? 52 : 50, fontWeight: 600, letterSpacing: 4, marginTop: 10, opacity: subIn, transform: `translateY(${14 * (1 - subIn)}px)`}}>
          GAS LEAK DETECTOR
        </div>
        <div style={{height: 3, width: 260 * subIn, margin: '18px auto 0', background: `linear-gradient(90deg, transparent, ${GAS}, transparent)`}} />
        <div style={{fontSize: portrait ? 34 : 32, fontWeight: 400, color: '#C9D2E0', marginTop: 16, opacity: tagIn * (1 - logos), padding: '0 48px'}}>
          {t('Deteksi multigas berbasis edge AI · jaringan private mesh LoRa', 'Edge-AI multi-gas detection · private LoRa mesh network')}
        </div>
      </div>

      {/* logo mitra */}
      <div
        style={{
          position: 'absolute',
          left: '50%',
          bottom: portrait ? 300 : 70,
          transform: `translate(-50%, ${30 * (1 - logos)}px)`,
          opacity: logos,
          display: 'flex',
          alignItems: 'center',
          gap: portrait ? 34 : 56,
          padding: portrait ? '16px 30px' : '18px 46px',
          borderRadius: 16,
          backgroundColor: '#FFFFFF',
          boxShadow: '0 12px 36px rgba(0,0,0,0.4)',
        }}
      >
        <Img src={staticFile(ASSETS.logoPertamina.path)} style={{height: portrait ? 46 : 52}} />
        <Img src={staticFile(ASSETS.logoLgu.path)} style={{height: portrait ? 62 : 68}} />
        <Img src={staticFile(ASSETS.logoItb.path)} style={{height: portrait ? 80 : 88}} />
      </div>

      <Sfx name="rise" at={0} volume={0.3} />
      <Sfx name="blip" at={4} volume={0.35} />
      {[62, 70, 78, 86].map((f) => (
        <Sfx key={f} name="tick" at={f} volume={0.25} />
      ))}
      <Sfx name="whoosh" at={88} volume={0.45} />
      <Sfx name="success" at={140} volume={0.3} />
    </AbsoluteFill>
  );
};

export const Intro: React.FC<{lang?: Lang}> = ({lang = 'id'}) => (
  <LangProvider lang={lang}>
    <IntroBody />
  </LangProvider>
);
