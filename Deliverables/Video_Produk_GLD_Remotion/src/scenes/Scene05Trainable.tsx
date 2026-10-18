import React from 'react';
import {AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {ASSETS} from '../assets';
import {AssetSlot} from '../components/AssetSlot';
import {Caption} from '../components/Caption';
import {SceneFrame} from '../components/SceneFrame';
import {GasStatus, REFINERY_GASES, STATUS_LABEL} from '../data/refineryGases';
import {COLORS} from '../theme';

const STATUS_COLOR: Record<GasStatus, string> = {
  validated: COLORS.ok,
  data: COLORS.blueLight,
  target: COLORS.gas,
  extra: COLORS.muted,
};

const GRID = {x: 820, y: 200, colW: 490, rowH: 126, gap: 16};

export const Scene05Trainable: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const zoom = interpolate(frame, [0, 480], [1, 1.12]);

  return (
    <SceneFrame>
      <AbsoluteFill style={{padding: '70px 120px'}}>
        <Caption text="Gas di kilang: dilatih di lokasi, sesuai kebutuhan" size={54} />
      </AbsoluteFill>

      {/* Foto asli chamber, Ken Burns pelan */}
      <div style={{position: 'absolute', left: 120, top: 200, width: 640, height: 500, overflow: 'hidden', borderRadius: 20}}>
        <div style={{width: '100%', height: '100%', transform: `scale(${zoom})`}}>
          <AssetSlot asset={ASSETS.chamber} kind="image" />
        </div>
      </div>
      <div style={{position: 'absolute', left: 120, top: 720, width: 640, fontSize: 24, color: COLORS.muted, lineHeight: 1.4}}>
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
            <div style={{width: 110, fontSize: 44, fontWeight: 800, color}}>{g.formula}</div>
            <div>
              <div style={{fontSize: 28, fontWeight: 600}}>{g.name}</div>
              <div style={{fontSize: 21, color: COLORS.muted, marginTop: 4}}>
                {STATUS_LABEL[g.status]} · {g.sensor}
              </div>
            </div>
          </div>
        );
      })}
    </SceneFrame>
  );
};
