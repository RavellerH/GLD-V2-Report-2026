import React from 'react';
import {AbsoluteFill, OffthreadVideo, spring, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {Caption} from '../components/Caption';
import {useLayout} from '../layout';
import {progress} from '../motion';
import {COLORS} from '../theme';

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

// Latar render 3D high-tech layar penuh (landscape; portrait memotong bagian tengah), diregangkan mengisi adegan.
export const Bg3D: React.FC<{src: string; sec: number; shade?: string; label?: string}> = ({src, sec, shade, label}) => {
  const {fps, durationInFrames} = useVideoConfig();
  const frame = useCurrentFrame();
  const rate = Math.min(1, sec / ((durationInFrames + 6) / fps));
  return (
    <AbsoluteFill>
      <OffthreadVideo src={staticFile(src)} playbackRate={rate} muted style={{width: '100%', height: '100%', objectFit: 'cover'}} />
      {shade && <AbsoluteFill style={{background: shade}} />}
      {label && (
        <div style={{position: 'absolute', right: 28, top: 22, fontSize: 16, letterSpacing: 1.5, color: 'rgba(214,240,255,0.7)', opacity: progress(frame, 10, 20)}}>{label}</div>
      )}
    </AbsoluteFill>
  );
};

export const rate3D = (sec: number, durationInFrames: number, fps: number) => Math.min(1, sec / ((durationInFrames + 6) / fps));

// Panel gelap tembus pandang di atas render 3D.
export const glassPanel: React.CSSProperties = {
  backgroundColor: 'rgba(4,8,16,0.72)',
  border: '1px solid rgba(91,155,255,0.28)',
  borderRadius: 16,
  backdropFilter: 'blur(6px)',
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
