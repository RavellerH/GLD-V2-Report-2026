import React from 'react';
import {AbsoluteFill, Img, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {ASSETS} from '../assets';
import {AssetSlot} from '../components/AssetSlot';
import {Caption} from '../components/Caption';
import {SceneFrame} from '../components/SceneFrame';
import {Sfx} from '../components/Sfx';
import {KASIM_PHOTOS} from '../data/kasimPhotos';
import {useLang} from '../i18n';
import {useT} from '../i18n';
import {useLayout} from '../layout';
import {progress, useNarration} from '../motion';
import {COLORS} from '../theme';

// Bukti pengujian. Klaim dijaga: uji lapangan = GLD generasi pertama (V1) di RU VII Kasim, Des 2025;
// generasi kedua (V2) = FAT 7/7 di laboratorium + uji mesh/failover/push alarm 8 Cluster Head (kampus ITB).

// Rangkaian foto dokumentasi (zoom/pan halus + crossfade) bila video Kasim belum ada.
const PhotoReel: React.FC = () => {
  const frame = useCurrentFrame();
  const {durationInFrames} = useVideoConfig();
  const lang = useLang();
  const n = KASIM_PHOTOS.length;
  const per = durationInFrames / n;
  const fade = 15;
  return (
    <AbsoluteFill>
      {KASIM_PHOTOS.map((ph, i) => {
        const start = i * per;
        const local = frame - start;
        if (local < -fade || local > per + fade) return null;
        const o = i === 0 ? interpolate(local, [per, per + fade], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'})
          : interpolate(local, [-fade, 0, per, per + fade], [0, 1, 1, i === n - 1 ? 1 : 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
        const k = interpolate(local, [0, per], [1.0, 1.08], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
        const dx = (i % 2 ? -1 : 1) * interpolate(local, [0, per], [0, 2.5], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
        return (
          <AbsoluteFill key={ph.file} style={{opacity: o}}>
            <Img src={staticFile(ph.file)} style={{width: '100%', height: '100%', objectFit: 'cover', transform: `scale(${k}) translateX(${dx}%)`}} />
            <div style={{position: 'absolute', left: 0, right: 0, bottom: 0, padding: '14px 20px', background: 'linear-gradient(transparent, rgba(10,18,32,0.85))', color: '#F2F5FA', fontSize: 22, fontWeight: 600}}>
              {lang === 'en' ? ph.en : ph.id}
            </div>
          </AbsoluteFill>
        );
      })}
    </AbsoluteFill>
  );
};
export const Scene08Field: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const {portrait, padX, title} = useLayout();
  const t = useT();
  const at = useNarration('field');
  const media = portrait ? {x: 64, y: 360, w: 952, h: 536} : {x: 120, y: 210, w: 1000, h: 563};
  const shot = progress(frame, 6, 24);
  const CARDS = [
    {
      k: t('Uji lapangan', 'Field test'),
      v: t('RU VII Kasim · Desember 2025', 'RU VII Kasim · December 2025'),
      sub: t('GLD generasi pertama', 'First-generation GLD'),
      at: at('RU VII Kasim'),
      color: COLORS.gas,
    },
    {
      k: 'Factory Acceptance Test',
      v: t('7 dari 7 butir lulus', '7 of 7 items passed'),
      sub: t('GLD generasi kedua · laboratorium', 'Second-generation GLD · laboratory'),
      at: at('Factory Acceptance Test'),
      color: COLORS.ok,
    },
    {
      k: 'Multi-hop mesh',
      v: t('8 Cluster Head', '8 Cluster Heads'),
      sub: t('jaringan multi-hop teruji', 'multi-hop network tested'),
      at: at('multi-hop mesh'),
      color: COLORS.blue,
    },
    {
      k: 'Failover & push alarm',
      v: t('Teruji', 'Tested'),
      sub: t('pemulihan rute & alarm otomatis', 'route recovery & automatic alarm'),
      at: at('failover'),
      color: COLORS.blue,
    },
  ];
  const cardsBox = portrait ? {x: 64, y: 940, w: 952} : {x: 1180, y: 210, w: 620};

  return (
    <SceneFrame theme="light">
      <AbsoluteFill style={{padding: portrait ? `200px ${padX}px` : `70px ${padX}px`}}>
        <Caption text={t('Teruji di lapangan dan laboratorium', 'Tested in the field and in the laboratory')} size={title(56)} />
      </AbsoluteFill>

      <div
        style={{
          position: 'absolute',
          left: media.x,
          top: media.y,
          width: media.w,
          height: media.h,
          borderRadius: 16,
          overflow: 'hidden',
          boxShadow: '0 24px 60px rgba(20,33,58,0.30)',
          opacity: shot,
          transform: `translateY(${20 * (1 - shot)}px)`,
        }}
      >
        {ASSETS.kasim.ready ? <AssetSlot asset={ASSETS.kasim} kind="video" /> : <PhotoReel />}
        {ASSETS.kasim.ready && <div
          style={{
            position: 'absolute',
            left: 0,
            right: 0,
            bottom: 0,
            padding: '14px 20px',
            background: 'linear-gradient(transparent, rgba(10,18,32,0.85))',
            color: '#F2F5FA',
            fontSize: 22,
            fontWeight: 600,
          }}
        >
          {t('Dokumentasi uji lapangan · RU VII Kasim · Desember 2025 · GLD generasi pertama', 'Field test documentation · RU VII Kasim · December 2025 · first-generation GLD')}
        </div>}
      </div>

      <div style={{position: 'absolute', left: cardsBox.x, top: cardsBox.y, width: cardsBox.w, display: 'grid', gridTemplateColumns: portrait ? '1fr 1fr' : '1fr', gap: portrait ? 14 : 18}}>
        {CARDS.map((c) => {
          const p = spring({frame: frame - c.at, fps, config: {damping: 200}});
          return (
            <div
              key={c.k}
              style={{
                opacity: p,
                transform: `translateX(${18 * (1 - p)}px)`,
                padding: '16px 20px',
                borderRadius: 14,
                backgroundColor: COLORS.surface,
                border: `1px solid ${COLORS.line}`,
                borderLeft: `8px solid ${c.color}`,
                boxShadow: '0 8px 24px rgba(20,33,58,0.10)',
              }}
            >
              <div style={{fontSize: 20, fontWeight: 700, color: COLORS.muted, letterSpacing: 0.5, textTransform: 'uppercase'}}>{c.k}</div>
              <div style={{fontSize: portrait ? 30 : 32, fontWeight: 800, marginTop: 4}}>{c.v}</div>
              <div style={{fontSize: 21, color: COLORS.muted, marginTop: 2}}>{c.sub}</div>
            </div>
          );
        })}
      </div>
      {CARDS.map((c) => (
        <Sfx key={c.k} name="pop" at={c.at} volume={0.22} />
      ))}
    </SceneFrame>
  );
};
