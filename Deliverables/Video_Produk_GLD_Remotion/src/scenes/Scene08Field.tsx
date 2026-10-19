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

// Penanda unit GLD pada foto: lingkaran berdenyut + label.
const FocusRing: React.FC<{x: number; y: number; local: number}> = ({x, y, local}) => {
  const {fps} = useVideoConfig();
  const p = spring({frame: local - 14, fps, config: {damping: 14}});
  const pulse = (local % 36) / 36;
  return (
    <div style={{position: 'absolute', left: `${x * 100}%`, top: `${y * 100}%`, opacity: p}}>
      {[0, 1].map((k) => {
        const q = (pulse + k * 0.5) % 1;
        return <div key={k} style={{position: 'absolute', width: 150 + q * 90, height: 150 + q * 90, left: -(75 + q * 45), top: -(75 + q * 45), borderRadius: '50%', border: `3px solid ${COLORS.gas}`, opacity: 1 - q}} />;
      })}
      <div style={{position: 'absolute', width: 150, height: 150, left: -75, top: -75, borderRadius: '50%', border: `5px solid ${COLORS.gas}`, transform: `scale(${0.6 + 0.4 * p})`, boxShadow: '0 0 18px rgba(0,0,0,0.45)'}} />
      <div style={{position: 'absolute', left: 82, top: -96, padding: '4px 12px', borderRadius: 8, backgroundColor: COLORS.gas, color: '#14213A', fontSize: 24, fontWeight: 800, whiteSpace: 'nowrap'}}>GLD</div>
    </div>
  );
};

// Rangkaian foto dokumentasi sebagai tumpukan kartu beranimasi: tiap foto meluncur masuk sambil
// berputar sedikit lalu mendarat; foto sebelumnya terdorong ke belakang (mengecil, miring, meredup).
const PhotoReel: React.FC = () => {
  const frame = useCurrentFrame();
  const {durationInFrames, fps} = useVideoConfig();
  const lang = useLang();
  const n = KASIM_PHOTOS.length;
  const per = (durationInFrames - 12) / n;
  const enterOf = (i: number) => spring({frame: frame - i * per, fps, config: {damping: 15, mass: 0.9}});
  const active = Math.min(n - 1, Math.max(0, Math.floor(frame / per)));
  return (
    <AbsoluteFill>
      {KASIM_PHOTOS.map((ph, i) => {
        const local = frame - i * per;
        if (local < 0) return null;
        const enter = enterOf(i);
        // seberapa jauh kartu ini sudah "tertimpa" kartu-kartu sesudahnya (0..2)
        let pushed = 0;
        for (let j = i + 1; j < n; j++) pushed += enterOf(j);
        if (pushed > 2.6) return null;
        const side = i % 2 ? -1 : 1;
        const x = interpolate(enter, [0, 1], [side * 70, 0]);
        const y = interpolate(enter, [0, 1], [12, 0]) - 2.2 * Math.min(pushed, 2);
        const rot = interpolate(enter, [0, 1], [side * 9, 0]) + side * 3.2 * Math.min(pushed, 1.5);
        const scale = interpolate(enter, [0, 1], [0.86, 1]) * (1 - 0.06 * Math.min(pushed, 2));
        const dim = 1 - 0.28 * Math.min(pushed, 2);
        const kb = interpolate(local, [0, per * 1.6], [1.0, 1.1], {extrapolateRight: 'clamp'});
        const capP = spring({frame: local - 10, fps, config: {damping: 200}});
        return (
          <AbsoluteFill
            key={ph.file}
            style={{
              transform: `translate(${x}%, ${y}%) rotate(${rot}deg) scale(${scale})`,
              opacity: Math.min(1, enter * 1.6),
              filter: `brightness(${dim})`,
              padding: 10,
              backgroundColor: '#FFFFFF',
              borderRadius: 12,
              boxShadow: '0 22px 50px rgba(20,33,58,0.35)',
            }}
          >
            <div style={{position: 'relative', width: '100%', height: '100%', overflow: 'hidden', borderRadius: 6}}>
              <div style={{position: 'absolute', inset: 0, transform: `scale(${kb})`, transformOrigin: ph.focus ? `${ph.focus.x * 100}% ${ph.focus.y * 100}%` : '50% 50%'}}>
                <Img src={staticFile(ph.file)} style={{width: '100%', height: '100%', objectFit: 'cover'}} />
                {ph.focus && <FocusRing x={ph.focus.x} y={ph.focus.y} local={local} />}
              </div>
              <div
                style={{
                  position: 'absolute',
                  left: 0,
                  right: 0,
                  bottom: 0,
                  padding: '16px 20px 14px',
                  background: 'linear-gradient(transparent, rgba(10,18,32,0.88))',
                  color: '#F2F5FA',
                  fontSize: 22,
                  fontWeight: 600,
                  opacity: capP,
                  transform: `translateY(${16 * (1 - capP)}px)`,
                }}
              >
                {lang === 'en' ? ph.en : ph.id}
              </div>
            </div>
          </AbsoluteFill>
        );
      })}
      {/* indikator urutan foto */}
      <div style={{position: 'absolute', right: 22, top: 22, display: 'flex', gap: 8}}>
        {KASIM_PHOTOS.map((ph, i) => (
          <div key={ph.file} style={{width: i === active ? 26 : 10, height: 10, borderRadius: 5, backgroundColor: i <= active ? '#FFFFFF' : 'rgba(255,255,255,0.45)', boxShadow: '0 1px 4px rgba(0,0,0,0.4)'}} />
        ))}
      </div>
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
      v: t('RU VII Kasim · Nov–Des 2025', 'RU VII Kasim · Nov–Dec 2025'),
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
          overflow: ASSETS.kasim.ready ? 'hidden' : 'visible',
          boxShadow: ASSETS.kasim.ready ? '0 24px 60px rgba(20,33,58,0.30)' : 'none',
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
          {t('Dokumentasi uji lapangan · RU VII Kasim · November–Desember 2025 · GLD generasi pertama', 'Field test documentation · RU VII Kasim · November–December 2025 · first-generation GLD')}
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
