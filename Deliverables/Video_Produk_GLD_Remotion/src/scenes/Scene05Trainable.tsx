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

// Legenda komponen chamber (sumber: Laporan Progres Chamber Gas). `at` = frame relatif adegan;
// animasi Blender harus menyorot komponen bernomor yang sama pada detik yang sama.
const CHAMBER_PARTS = [
  {at: 15, text: 'Tabung gas uji + solenoid valve: aliran gas presisi'},
  {at: 90, text: 'Ruang uji akrilik berisi unit GLD: pengambilan dataset'},
  {at: 165, text: 'BME280 ×2 + TGS2610: kondisi udara & gas acuan'},
  {at: 240, text: 'Pompa hisap (duty cycle): sirkulasi & pembilasan'},
];

// Landscape: render chamber di kiri, kartu gas di kanan. Portrait: render di atas, kartu di bawah.
const LANDSCAPE = {media: {x: 120, y: 200, w: 640, h: 420}, legendY: 640, legendGap: 44, grid: {x: 820, y: 200, colW: 490, rowH: 126, gap: 16}};
const PORTRAIT = {media: {x: 64, y: 350, w: 952, h: 380}, legendY: 745, legendGap: 36, grid: {x: 64, y: 905, colW: 468, rowH: 112, gap: 16}};

export const Scene05Trainable: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const {portrait, padX, title} = useLayout();
  const L = portrait ? PORTRAIT : LANDSCAPE;
  const GRID = L.grid;

  return (
    <SceneFrame>
      <AbsoluteFill style={{padding: portrait ? `200px ${padX}px` : `70px ${padX}px`}}>
        <Caption text="Gas di kilang: dilatih di lokasi, sesuai kebutuhan" size={title(54)} />
      </AbsoluteFill>

      {/* Render Blender gas test chamber */}
      <div style={{position: 'absolute', left: L.media.x, top: L.media.y, width: L.media.w, height: L.media.h, overflow: 'hidden', borderRadius: 20}}>
        <AssetSlot asset={ASSETS.chamber} kind="video" />
      </div>

      {CHAMBER_PARTS.map((c, i) => {
        const p = spring({frame: frame - c.at, fps, config: {damping: 200}});
        return (
          <div
            key={c.text}
            style={{position: 'absolute', left: L.media.x, top: L.legendY + i * L.legendGap, width: L.media.w, display: 'flex', gap: 12, alignItems: 'center', opacity: p, fontSize: portrait ? 22 : 21}}
          >
            <div style={{flex: '0 0 30px', height: 30, borderRadius: 15, backgroundColor: COLORS.blue, fontWeight: 800, display: 'flex', alignItems: 'center', justifyContent: 'center'}}>{i + 1}</div>
            <div>{c.text}</div>
          </div>
        );
      })}

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
