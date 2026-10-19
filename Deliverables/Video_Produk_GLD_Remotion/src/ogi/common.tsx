import React from 'react';
import {AbsoluteFill, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {Caption} from '../components/Caption';
import {useT} from '../i18n';
import {useLayout} from '../layout';
import {progress} from '../motion';
import {COLORS} from '../theme';

// Label permanen: seluruh video OGI adalah konsep pengembangan, bukan sistem terpasang.
export const ConceptBadge: React.FC = () => {
  const t = useT();
  const {portrait} = useLayout();
  return (
    <div
      style={{
        position: 'absolute',
        right: portrait ? 40 : 48,
        top: portrait ? 120 : 36,
        padding: '6px 14px',
        borderRadius: 8,
        border: `2px solid ${COLORS.gas}`,
        color: COLORS.gas,
        backgroundColor: 'rgba(10,18,32,0.55)',
        fontSize: 20,
        fontWeight: 800,
        letterSpacing: 2,
      }}
    >
      {t('KONSEP PENGEMBANGAN', 'DEVELOPMENT CONCEPT')}
    </div>
  );
};

// Judul adegan dengan label kecil di atasnya (nomor/tema).
export const SceneTitle: React.FC<{kicker: string; title: string; from?: number; color?: string}> = ({kicker, title, from = 4, color}) => {
  const {portrait, padX, title: ts} = useLayout();
  const frame = useCurrentFrame();
  return (
    <AbsoluteFill style={{padding: portrait ? `200px ${padX}px` : `64px ${padX}px`, pointerEvents: 'none'}}>
      <div style={{fontSize: 22, fontWeight: 800, letterSpacing: 3, color: COLORS.blueLight, opacity: progress(frame, from, 14)}}>{kicker}</div>
      <Caption text={title} from={from + 4} size={ts(52)} color={color} style={{marginTop: 8, maxWidth: portrait ? 950 : 1300}} />
    </AbsoluteFill>
  );
};

// Kartu informasi dengan aksen warna di kiri, muncul dengan spring pada frame `at`.
export const InfoCard: React.FC<{at: number; k: string; v: string; color?: string; style?: React.CSSProperties; big?: boolean}> = ({
  at,
  k,
  v,
  color = COLORS.blue,
  style,
  big,
}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const p = spring({frame: frame - at, fps, config: {damping: 200}});
  return (
    <div
      style={{
        opacity: p,
        transform: `translateY(${18 * (1 - p)}px)`,
        padding: big ? '22px 26px' : '16px 20px',
        borderRadius: 14,
        backgroundColor: COLORS.surface,
        border: `1px solid ${COLORS.line}`,
        borderLeft: `8px solid ${color}`,
        boxShadow: '0 8px 24px rgba(20,33,58,0.12)',
        ...style,
      }}
    >
      <div style={{fontSize: 19, fontWeight: 700, color: COLORS.muted, letterSpacing: 0.5, textTransform: 'uppercase'}}>{k}</div>
      <div style={{fontSize: big ? 32 : 28, fontWeight: 800, marginTop: 4, lineHeight: 1.2}}>{v}</div>
    </div>
  );
};
