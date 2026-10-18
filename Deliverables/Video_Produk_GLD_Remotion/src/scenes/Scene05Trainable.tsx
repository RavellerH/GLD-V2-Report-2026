import React from 'react';
import {AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {ASSETS} from '../assets';
import {AssetSlot} from '../components/AssetSlot';
import {Caption} from '../components/Caption';
import {SceneFrame} from '../components/SceneFrame';
import {GasStatus, REFINERY_GASES, STATUS_LABEL} from '../data/refineryGases';
import {useLayout} from '../layout';
import {COLORS} from '../theme';

const STATUS_COLOR: Record<GasStatus, string> = {
  validated: COLORS.ok,
  data: COLORS.blueLight,
  target: COLORS.gas,
  extra: COLORS.muted,
};

// Landscape: foto kiri, kartu gas kanan. Portrait: foto atas, kartu gas bawah.
const LANDSCAPE = {photo: {x: 120, y: 200, w: 640, h: 500}, flowY: 720, grid: {x: 820, y: 200, colW: 490, rowH: 126, gap: 16}};
const PORTRAIT = {photo: {x: 64, y: 360, w: 952, h: 440}, flowY: 815, grid: {x: 64, y: 905, colW: 468, rowH: 112, gap: 16}};

export const Scene05Trainable: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const {portrait, padX, title} = useLayout();
  const L = portrait ? PORTRAIT : LANDSCAPE;
  const GRID = L.grid;
  const zoom = interpolate(frame, [0, 480], [1, 1.12]);

  return (
    <SceneFrame>
      <AbsoluteFill style={{padding: portrait ? `200px ${padX}px` : `70px ${padX}px`}}>
        <Caption text="Gas di kilang: dilatih di lokasi, sesuai kebutuhan" size={title(54)} />
      </AbsoluteFill>

      {/* Foto asli chamber, Ken Burns pelan */}
      <div style={{position: 'absolute', left: L.photo.x, top: L.photo.y, width: L.photo.w, height: L.photo.h, overflow: 'hidden', borderRadius: 20}}>
        <div style={{width: '100%', height: '100%', transform: `scale(${zoom})`}}>
          <AssetSlot asset={ASSETS.chamber} kind="image" />
        </div>
      </div>
      <div style={{position: 'absolute', left: L.photo.x, top: L.flowY, width: L.photo.w, fontSize: 24, color: COLORS.muted, lineHeight: 1.4}}>
        Chamber uji portabel → dataset on-site → latih ulang model → perbarui firmware GLD
      </div>

      {REFINERY_GASES.map((g, i) => {
        const col = i % 2;
        const row = Math.floor(i / 2);
        const p = spring({frame: frame - 40 - i * 12, fps, config: {damping: 200}});
        const color = STATUS_COLOR[g.status];
        return (
          <div
            key={g.formula}
            style={{
              position: 'absolute',
              left: GRID.x + col * (GRID.colW + GRID.gap),
              top: GRID.y + row * (GRID.rowH + GRID.gap),
              width: GRID.colW,
              height: GRID.rowH,
              borderRadius: 14,
              backgroundColor: COLORS.surface,
              border: `2px solid ${COLORS.line}`,
              borderLeft: `8px solid ${color}`,
              padding: '16px 22px',
              display: 'flex',
              alignItems: 'center',
              gap: 22,
              opacity: p,
              transform: `translateY(${interpolate(p, [0, 1], [16, 0])}px)`,
            }}
          >
            <div style={{width: portrait ? 96 : 110, fontSize: portrait ? 38 : 44, fontWeight: 800, color}}>{g.formula}</div>
            <div>
              <div style={{fontSize: portrait ? 25 : 28, fontWeight: 600}}>{g.name}</div>
              <div style={{fontSize: portrait ? 19 : 21, color: COLORS.muted, marginTop: 4}}>
                {STATUS_LABEL[g.status]} · {g.sensor}
              </div>
            </div>
          </div>
        );
      })}
    </SceneFrame>
  );
};
