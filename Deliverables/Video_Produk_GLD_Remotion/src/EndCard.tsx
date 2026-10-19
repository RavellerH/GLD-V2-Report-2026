import React from 'react';
import {AbsoluteFill, Img, spring, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {ASSETS} from './assets';
import {Sfx} from './components/Sfx';
import {useT} from './i18n';
import {useLayout} from './layout';
import {progress} from './motion';
import {FONT, PALETTES, themeVars} from './theme';

// Penutup tanpa narasi: kartu ringkasan (±5,5 dtk) lalu layar logo mitra di latar putih, fade out.
const LOGO_AT = 165;
export const ENDCARD_FRAMES = 270;
const P = PALETTES.night;

const Icon: React.FC<{kind: string; color: string}> = ({kind, color}) => {
  const s = {fill: 'none', stroke: color, strokeWidth: 3.5, strokeLinecap: 'round' as const, strokeLinejoin: 'round' as const};
  return (
    <svg width={68} height={68} viewBox="0 0 56 56">
      {kind === 'ai' && (
        <g {...s}>
          <rect x={14} y={14} width={28} height={28} rx={4} />
          <rect x={22} y={22} width={12} height={12} rx={2} />
          {[20, 28, 36].map((v) => (
            <g key={v}>
              <line x1={v} y1={6} x2={v} y2={14} />
              <line x1={v} y1={42} x2={v} y2={50} />
              <line x1={6} y1={v} x2={14} y2={v} />
              <line x1={42} y1={v} x2={50} y2={v} />
            </g>
          ))}
        </g>
      )}
      {kind === 'early' && (
        <g {...s}>
          <polyline points="6,44 18,38 28,30 38,18 50,10" />
          <line x1={6} y1={50} x2={50} y2={50} />
          <circle cx={50} cy={10} r={3} fill={color} />
        </g>
      )}
      {kind === 'mesh' && (
        <g {...s}>
          <circle cx={28} cy={10} r={5} />
          <circle cx={10} cy={44} r={5} />
          <circle cx={46} cy={44} r={5} />
          <circle cx={28} cy={32} r={4} fill={color} />
          <line x1={28} y1={15} x2={28} y2={28} />
          <line x1={14} y1={41} x2={25} y2={34} />
          <line x1={42} y1={41} x2={31} y2={34} />
          <line x1={15} y1={44} x2={41} y2={44} strokeDasharray="4 5" />
        </g>
      )}
      {kind === 'field' && (
        <g {...s}>
          <path d="M28 50 C28 50 12 34 12 22 A16 16 0 0 1 44 22 C44 34 28 50 28 50 Z" />
          <polyline points="21,23 26,28 35,18" />
        </g>
      )}
    </svg>
  );
};

export const EndCard: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const {portrait, padX} = useLayout();
  const t = useT();
  const ITEMS = [
    {
      kind: 'ai',
      color: P.gas,
      k: t('8 sensor gas + edge AI', '8 gas sensors + edge AI'),
      v: t('Klasifikasi gas langsung di perangkat', 'Gas classification directly on the device'),
    },
    {
      kind: 'early',
      color: P.alarm,
      k: t('Peringatan dini', 'Early warning'),
      v: t('Confidence score deteksi meningkat sebelum gas pekat', 'Detection confidence score rises before the gas becomes concentrated'),
    },
    {
      kind: 'mesh',
      color: P.blueLight,
      k: 'Private mesh LoRa',
      v: t('Self-healing, tanpa kabel data dan internet', 'Self-healing, no data cables or internet'),
    },
    {
      kind: 'field',
      color: P.ok,
      k: t('Teruji di RU VII Kasim', 'Tested at RU VII Kasim'),
      v: t('November–Desember 2025 · GLD generasi pertama', 'November–December 2025 · first-generation GLD'),
    },
  ];
  const head = progress(frame, 0, 18);
  const foot = spring({frame: frame - 92, fps, config: {damping: 200}});
  const toLogo = progress(frame, LOGO_AT - 10, 20);
  const logoIn = spring({frame: frame - LOGO_AT, fps, config: {damping: 200}});
  const out = 1 - progress(frame, ENDCARD_FRAMES - 24, 24);

  return (
    <AbsoluteFill style={{...themeVars('night'), backgroundColor: P.bg, fontFamily: FONT, color: P.text, opacity: out}}>
      <AbsoluteFill style={{opacity: Math.min(head * 1.4, 1) * (1 - toLogo)}}>
      <AbsoluteFill
        style={{
          backgroundImage: `linear-gradient(rgba(91,155,255,0.06) 1px, transparent 1px), linear-gradient(90deg, rgba(91,155,255,0.06) 1px, transparent 1px)`,
          backgroundSize: '64px 64px',
        }}
      />
      <AbsoluteFill style={{background: 'radial-gradient(circle at 50% 30%, rgba(43,95,203,0.25), transparent 65%)'}} />

      <AbsoluteFill style={{padding: portrait ? `260px ${padX}px` : `90px ${padX}px`, display: 'flex', flexDirection: 'column'}}>
        <div style={{opacity: head, transform: `translateY(${16 * (1 - head)}px)`}}>
          <div style={{fontSize: portrait ? 26 : 24, fontWeight: 700, letterSpacing: 4, color: P.blueLight}}>GAS LEAK DETECTOR</div>
          <div style={{fontSize: portrait ? 64 : 62, fontWeight: 800, marginTop: 6}}>{t('GLD dalam ringkas', 'GLD at a glance')}</div>
          <div style={{height: 4, width: 140 * head, marginTop: 16, background: P.gas, borderRadius: 2}} />
        </div>

        <div style={{flex: 1, display: 'flex', flexDirection: 'column', justifyContent: 'center'}}>
        <div
          style={{
            display: 'grid',
            gridTemplateColumns: portrait ? '1fr' : '1fr 1fr',
            gap: portrait ? 30 : 36,
          }}
        >
          {ITEMS.map((it, i) => {
            const p = spring({frame: frame - 16 - i * 14, fps, config: {damping: 16}});
            return (
              <div
                key={it.k}
                style={{
                  opacity: p,
                  transform: `translateY(${28 * (1 - p)}px) scale(${0.96 + 0.04 * p})`,
                  display: 'flex',
                  gap: 28,
                  alignItems: 'center',
                  padding: portrait ? '32px 30px' : '40px 38px',
                  borderRadius: 18,
                  backgroundColor: 'rgba(17,28,46,0.85)',
                  border: `1px solid ${P.line}`,
                  borderLeft: `8px solid ${it.color}`,
                }}
              >
                <div style={{flex: '0 0 auto', width: 104, height: 104, borderRadius: 22, backgroundColor: 'rgba(255,255,255,0.05)', display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
                  <Icon kind={it.kind} color={it.color} />
                </div>
                <div>
                  <div style={{fontSize: portrait ? 40 : 42, fontWeight: 800}}>{it.k}</div>
                  <div style={{fontSize: portrait ? 29 : 30, color: '#C9D2E0', marginTop: 4, lineHeight: 1.3}}>{it.v}</div>
                </div>
              </div>
            );
          })}
        </div>
        </div>

        <div style={{ display: 'flex', flexDirection: portrait ? 'column' : 'row', alignItems: 'center', justifyContent: 'center', gap: 24, opacity: foot, transform: `translateY(${20 * (1 - foot)}px)`}}>
          <div style={{fontSize: portrait ? 26 : 24, color: P.muted, textAlign: portrait ? 'center' : 'left'}}>
            {t('Berikutnya: integrasi kamera thermal untuk pemantauan area', 'Next: thermal camera integration for area monitoring')}
          </div>
        </div>
      </AbsoluteFill>
      </AbsoluteFill>

      {/* layar akhir: logo Pertamina, LGU, ITB */}
      <AbsoluteFill style={{backgroundColor: '#FFFFFF', opacity: toLogo, alignItems: 'center', justifyContent: 'center'}}>
        <div
          style={{
            display: 'flex',
            flexDirection: portrait ? 'column' : 'row',
            alignItems: 'center',
            gap: portrait ? 90 : 120,
            opacity: logoIn,
            transform: `scale(${0.94 + 0.06 * logoIn})`,
          }}
        >
          <Img src={staticFile(ASSETS.logoPertamina.path)} style={{height: portrait ? 110 : 100}} />
          <Img src={staticFile(ASSETS.logoLgu.path)} style={{height: portrait ? 140 : 130}} />
          <Img src={staticFile(ASSETS.logoItb.path)} style={{height: portrait ? 190 : 170}} />
        </div>
      </AbsoluteFill>

      {[16, 30, 44, 58].map((f) => (
        <Sfx key={f} name="pop" at={f} volume={0.2} />
      ))}
      <Sfx name="whoosh" at={LOGO_AT - 10} volume={0.3} />
      <Sfx name="success" at={LOGO_AT + 6} volume={0.25} />
    </AbsoluteFill>
  );
};
