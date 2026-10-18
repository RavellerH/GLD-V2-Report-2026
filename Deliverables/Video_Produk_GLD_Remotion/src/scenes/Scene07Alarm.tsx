import React from 'react';
import {AbsoluteFill, Img, spring, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {ASSETS} from '../assets';
import {AssetSlot} from '../components/AssetSlot';
import {Caption} from '../components/Caption';
import {SceneFrame} from '../components/SceneFrame';
import {useLayout} from '../layout';
import {COLORS} from '../theme';

// Screenshot Alarm Console RU4 (1920x1080) diperkecil ke bingkai berikut.
// Portrait: screenshot selebar layar di bagian atas, kartu pull/push di bawahnya.
// `crop` = bagian screenshot yang ditampilkan (piksel screenshot). Portrait hanya menampilkan
// daftar alarm pada skala ~1:1 agar teksnya terbaca di layar HP.
const LAYOUTS = {
  landscape: {scale: 0.8, x: 192, y: 150, crop: {x: 0, y: 0, w: 1920, h: 1080}, cards: {x: 1180, y: 580, w: 500}},
  portrait: {scale: 952 / 960, x: 64, y: 420, crop: {x: 236, y: 170, w: 960, h: 330}, cards: {x: 64, y: 820, w: 952}},
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

export const Scene07Alarm: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const {portrait, padX, title} = useLayout();
  const L = portrait ? LAYOUTS.portrait : LAYOUTS.landscape;
  const ring = spring({frame: frame - 45, fps, config: {damping: 12}});
  const pulse = 0.5 + 0.5 * Math.abs(Math.sin(frame / 8));

  return (
    <SceneFrame>
      <div style={{position: 'absolute', left: L.x, top: L.y, width: L.crop.w * L.scale, height: L.crop.h * L.scale, borderRadius: 14, overflow: 'hidden', boxShadow: '0 30px 80px rgba(0,0,0,0.6)'}}>
        {ASSETS.dashboard.ready ? (
          <Img
            src={staticFile(ASSETS.dashboard.path)}
            style={{position: 'absolute', left: -L.crop.x * L.scale, top: -L.crop.y * L.scale, width: 1920 * L.scale, height: 1080 * L.scale}}
          />
        ) : (
          <AssetSlot asset={ASSETS.dashboard} kind="image" />
        )}
      </div>

      {/* Sorot alarm masuk */}
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

      {/* Dua jalur data: normal (cache + pull berkala) vs alarm (push segera). */}
      <div style={{position: 'absolute', left: L.cards.x, top: L.cards.y, width: L.cards.w, display: 'flex', flexDirection: 'column', gap: 18}}>
        {[
          {label: 'Data normal', sub: 'disimpan pada Cluster Head, diambil secara berkala (pull)', color: COLORS.ok, at: 120},
          {label: 'Alarm', sub: 'dikirim segera melalui mekanisme push, tanpa menunggu siklus pull', color: COLORS.alarm, at: 150},
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

      <AbsoluteFill style={{padding: portrait ? `200px ${padX}px` : '50px 192px'}}>
        <Caption text="Notifikasi alarm kepada operator" size={title(60)} />
      </AbsoluteFill>
      <div style={{position: 'absolute', right: portrait ? undefined : 192, left: portrait ? padX : undefined, top: portrait ? 365 : 82, fontSize: 22, color: COLORS.muted}}>
        Dashboard GLD · RU IV · data demonstrasi
      </div>
    </SceneFrame>
  );
};
