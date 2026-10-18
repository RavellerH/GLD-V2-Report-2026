import React from 'react';
import {AbsoluteFill, Img, spring, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {ASSETS} from '../assets';
import {AssetSlot} from '../components/AssetSlot';
import {Caption} from '../components/Caption';
import {SceneFrame} from '../components/SceneFrame';
import {COLORS} from '../theme';

// Screenshot Alarm Console RU4 (1920x1080) diperkecil ke bingkai berikut.
const SCALE = 0.8;
const FRAME = {x: 192, y: 150, w: 1920 * SCALE, h: 1080 * SCALE};
// Baris alarm pertama pada screenshot asli (koordinat piksel screenshot).
const FIRST_ALERT = {x: 244, y: 241, w: 1651, h: 70};

const toFrame = (r: typeof FIRST_ALERT) => ({
  left: FRAME.x + r.x * SCALE,
  top: FRAME.y + r.y * SCALE,
  width: r.w * SCALE,
  height: r.h * SCALE,
});

export const Scene07Alarm: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const ring = spring({frame: frame - 45, fps, config: {damping: 12}});
  const pulse = 0.5 + 0.5 * Math.abs(Math.sin(frame / 8));

  return (
    <SceneFrame>
      <div style={{position: 'absolute', left: FRAME.x, top: FRAME.y, width: FRAME.w, height: FRAME.h, borderRadius: 14, overflow: 'hidden', boxShadow: '0 30px 80px rgba(0,0,0,0.6)'}}>
        {ASSETS.dashboard.ready ? <Img src={staticFile(ASSETS.dashboard.path)} style={{width: '100%', height: '100%'}} /> : <AssetSlot asset={ASSETS.dashboard} kind="image" />}
      </div>

      {/* Sorot alarm masuk */}
      <div
        style={{
          position: 'absolute',
          ...toFrame(FIRST_ALERT),
          borderRadius: 12,
          border: `4px solid ${COLORS.alarm}`,
          boxShadow: `0 0 ${36 * pulse}px ${COLORS.alarm}`,
          opacity: ring,
          transform: `scale(${1.04 - 0.04 * ring})`,
        }}
      />

      {/* Dua jalur data: normal (cache + pull berkala) vs alarm (push segera). */}
      <div style={{position: 'absolute', left: 1180, top: 580, width: 500, display: 'flex', flexDirection: 'column', gap: 18}}>
        {[
          {label: 'Data normal', sub: 'disimpan di Cluster Head, diambil berkala (pull)', color: COLORS.ok, at: 120},
          {label: 'Alarm', sub: 'dikirim segera (push), tanpa menunggu siklus pull', color: COLORS.alarm, at: 150},
        ].map((r) => {
          const p = spring({frame: frame - r.at, fps, config: {damping: 200}});
          return (
            <div key={r.label} style={{opacity: p, padding: '18px 22px', borderRadius: 14, backgroundColor: COLORS.surface, border: `1px solid ${COLORS.line}`, borderLeft: `8px solid ${r.color}`, boxShadow: '0 8px 24px rgba(0,0,0,0.4)'}}>
              <div style={{fontSize: 28, fontWeight: 800}}>{r.label}</div>
              <div style={{fontSize: 22, marginTop: 4, color: COLORS.muted}}>{r.sub}</div>
            </div>
          );
        })}
      </div>

      <AbsoluteFill style={{padding: '50px 192px'}}>
        <Caption text="Alarm langsung ke operator" size={60} />
      </AbsoluteFill>
      <div style={{position: 'absolute', right: 192, top: 82, fontSize: 22, color: COLORS.muted}}>Dashboard GLD · RU IV · data demo</div>
    </SceneFrame>
  );
};
