import React from 'react';
import {AbsoluteFill, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {ASSETS} from '../assets';
import {AssetSlot} from '../components/AssetSlot';
import {Caption} from '../components/Caption';
import {SceneFrame} from '../components/SceneFrame';
import {Sfx} from '../components/Sfx';
import {useT} from '../i18n';
import {useLayout} from '../layout';
import {progress, useNarration} from '../motion';
import {COLORS} from '../theme';

// Pengembangan berikutnya (roadmap, belum diimplementasikan): integrasi kamera thermal untuk
// pemantauan area, melengkapi deteksi titik GLD dalam satu dashboard. Konsep dari proposal resmi.
const GLDS = [
  {x: 170, y: 150},
  {x: 360, y: 300},
  {x: 560, y: 170},
  {x: 260, y: 430},
  {x: 640, y: 400},
];
const CAM = {x: 760, y: 520};
const INTRO_SEC = 3.4; // klip ilustrasi thermal layar penuh di awal adegan

export const Scene09Roadmap: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const {portrait, padX, title} = useLayout();
  const t = useT();
  const at = useNarration('roadmap');
  const INTRO_END = Math.round(INTRO_SEC * fps);
  const tCam = Math.max(at(['kamera thermal', 'thermal cameras']), INTRO_END);
  const tDash = at(['satu dashboard', 'single unified dashboard']);
  const area = portrait ? {x: 64, y: 400, w: 952, h: 640} : {x: 120, y: 230, w: 820, h: 560};
  const dash = portrait ? {x: 64, y: 1110, w: 952} : {x: 1060, y: 300, w: 740};
  const cam = progress(frame, tCam - 6, 18);
  const sweep = Math.sin((frame - tCam) / 40) * 16; // kerucut menyapu area perlahan

  const ROWS = [
    {k: t('Deteksi titik', 'Point detection'), v: t('GLD multigas + edge AI', 'Multi-gas GLD + edge AI'), c: COLORS.gas, at: INTRO_END + 4},
    {k: t('Pemantauan area', 'Area monitoring'), v: t('Kamera thermal', 'Thermal camera'), c: COLORS.alarm, at: tCam},
    {k: t('Satu dashboard terpadu', 'Single unified dashboard'), v: t('Alarm titik & citra area terkorelasi', 'Correlated point alarms & area imagery'), c: COLORS.blue, at: tDash},
  ];

  return (
    <SceneFrame theme="light">
      <AbsoluteFill style={{padding: portrait ? `200px ${padX}px` : `70px ${padX}px`}}>
        <div
          style={{
            display: 'inline-flex',
            alignSelf: 'flex-start',
            padding: '6px 16px',
            borderRadius: 999,
            border: `2px solid ${COLORS.blue}`,
            color: COLORS.blue,
            fontSize: 22,
            fontWeight: 800,
            letterSpacing: 2,
            opacity: progress(frame, 4, 14),
            marginBottom: 14,
          }}
        >
          ROADMAP
        </div>
        <Caption text={t('Pengembangan berikutnya: integrasi kamera thermal', 'Next development: thermal camera integration')} from={INTRO_END - 6} size={title(54)} />
      </AbsoluteFill>

      {/* Denah area: titik GLD (deteksi titik) + kerucut pandang kamera thermal (pemantauan area) */}
      <div
        style={{
          position: 'absolute',
          left: area.x,
          top: area.y,
          width: area.w,
          height: area.h,
          borderRadius: 18,
          backgroundColor: COLORS.surface,
          border: `1px solid ${COLORS.line}`,
          overflow: 'hidden',
          boxShadow: '0 12px 36px rgba(20,33,58,0.10)',
        }}
      >
        <svg width={area.w} height={area.h} viewBox="0 0 820 560" preserveAspectRatio="xMidYMid meet">
          <defs>
            <radialGradient id="thermal" cx={CAM.x} cy={CAM.y} r={560} gradientUnits="userSpaceOnUse">
              <stop offset="0" stopColor={COLORS.alarm} stopOpacity={0.45} />
              <stop offset="0.6" stopColor={COLORS.gas} stopOpacity={0.22} />
              <stop offset="1" stopColor={COLORS.gas} stopOpacity={0} />
            </radialGradient>
          </defs>
          {[110, 250, 390].map((y) => (
            <rect key={y} x={60} y={y} width={640} height={14} rx={7} fill={COLORS.line} />
          ))}
          <g opacity={cam} transform={`rotate(${sweep - 152} ${CAM.x} ${CAM.y})`}>
            <path d={`M ${CAM.x} ${CAM.y} L ${CAM.x + 600} ${CAM.y - 210} A 640 640 0 0 1 ${CAM.x + 600} ${CAM.y + 210} Z`} fill="url(#thermal)" />
          </g>
          {GLDS.map((g, i) => {
            const p = spring({frame: frame - INTRO_END - i * 5, fps, config: {damping: 18}});
            return (
              <g key={i} transform={`translate(${g.x} ${g.y}) scale(${p})`}>
                <circle r={36} fill={COLORS.gas} fillOpacity={0.15} />
                <circle r={13} fill={COLORS.gas} />
              </g>
            );
          })}
          <g opacity={cam} transform={`translate(${CAM.x} ${CAM.y})`}>
            <rect x={-34} y={-20} width={50} height={40} rx={8} fill={COLORS.text} />
            <rect x={16} y={-12} width={18} height={24} rx={4} fill={COLORS.text} />
            <circle cx={-9} cy={0} r={11} fill={COLORS.alarm} />
          </g>
        </svg>
        <div style={{position: 'absolute', left: 20, bottom: 16, display: 'flex', gap: 22, fontSize: 21, color: COLORS.muted}}>
          <span>
            <span style={{color: COLORS.gas, fontWeight: 800}}>●</span> {t('GLD: deteksi titik', 'GLD: point detection')}
          </span>
          <span style={{opacity: cam}}>
            <span style={{color: COLORS.alarm, fontWeight: 800}}>◢</span> {t('Kamera thermal: pemantauan area', 'Thermal camera: area monitoring')}
          </span>
        </div>
      </div>

      {/* Satu dashboard terpadu */}
      <div style={{position: 'absolute', left: dash.x, top: dash.y, width: dash.w, display: 'flex', flexDirection: 'column', gap: 16}}>
        {ROWS.map((r) => {
          const p = spring({frame: frame - r.at, fps, config: {damping: 200}});
          return (
            <div
              key={r.k}
              style={{
                opacity: p,
                transform: `translateX(${18 * (1 - p)}px)`,
                padding: '18px 22px',
                borderRadius: 14,
                backgroundColor: COLORS.surface,
                border: `1px solid ${COLORS.line}`,
                borderLeft: `8px solid ${r.c}`,
                boxShadow: '0 8px 24px rgba(20,33,58,0.10)',
              }}
            >
              <div style={{fontSize: 20, fontWeight: 700, color: COLORS.muted, letterSpacing: 0.5, textTransform: 'uppercase'}}>{r.k}</div>
              <div style={{fontSize: 30, fontWeight: 800, marginTop: 4}}>{r.v}</div>
            </div>
          );
        })}
      </div>
      <div style={{position: 'absolute', left: portrait ? 64 : dash.x, top: portrait ? 1560 : 860, fontSize: 21, color: COLORS.muted, opacity: progress(frame, tDash + 20, 20)}}>
        {t('Tahap pengembangan berikutnya · belum termasuk ruang lingkup unit saat ini', 'Next development stage · not part of the current unit scope')}
      </div>
      {/* Klip ilustrasi konsep (layar penuh), memudar ke diagram */}
      {frame < INTRO_END + 16 && (
        <AbsoluteFill style={{opacity: 1 - progress(frame, INTRO_END - 8, 20)}}>
          <AssetSlot asset={ASSETS.thermal} kind="video" />
          <AbsoluteFill style={{background: 'linear-gradient(rgba(10,18,32,0.75), transparent 45%, transparent 60%, rgba(10,18,32,0.7))'}} />
          <div style={{position: 'absolute', left: padX, top: portrait ? 200 : 70, maxWidth: portrait ? 952 : 1300}}>
            <div style={{display: 'inline-flex', padding: '6px 16px', borderRadius: 999, border: '2px solid #F2F5FA', color: '#F2F5FA', fontSize: 22, fontWeight: 800, letterSpacing: 2, marginBottom: 14}}>ROADMAP</div>
            <Caption text={t('Pengembangan berikutnya: integrasi kamera thermal', 'Next development: thermal camera integration')} from={6} size={title(54)} color="#F2F5FA" />
          </div>
          <div style={{position: 'absolute', right: padX, top: portrait ? 120 : 40, padding: '6px 14px', borderRadius: 8, backgroundColor: 'rgba(10,18,32,0.6)', fontSize: 22, color: '#E3E8F0', opacity: progress(frame, 8, 16)}}>
            {t('Ilustrasi konsep — bukan rekaman produk', 'Concept illustration — not product footage')}
          </div>
        </AbsoluteFill>
      )}
      <Sfx name="pop" at={tCam} volume={0.22} />
      <Sfx name="success" at={tDash} volume={0.25} />
    </SceneFrame>
  );
};
