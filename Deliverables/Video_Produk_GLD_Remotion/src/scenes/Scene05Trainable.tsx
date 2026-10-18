import React from 'react';
import {AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {ASSETS} from '../assets';
import {AssetSlot} from '../components/AssetSlot';
import {Caption} from '../components/Caption';
import {SceneFrame} from '../components/SceneFrame';
import {REFINERIES, project} from '../data/refineries';
import {COLORS} from '../theme';

const STEPS = ['Chamber di kilang', 'Dataset on-site', 'Latih model', 'Update GLD'];
const MAP = {x: 1000, y: 470, w: 820, h: 300};

export const Scene05Trainable: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const zoom = interpolate(frame, [0, 360], [1, 1.12]);

  return (
    <SceneFrame>
      {/* Foto asli chamber, Ken Burns pelan */}
      <div style={{position: 'absolute', left: 120, top: 200, width: 760, height: 600, overflow: 'hidden', borderRadius: 20}}>
        <div style={{width: '100%', height: '100%', transform: `scale(${zoom})`}}>
          <AssetSlot asset={ASSETS.chamber} kind="image" />
        </div>
      </div>

      <AbsoluteFill style={{padding: '70px 120px'}}>
        <Caption text="Dilatih di lokasi, sesuai gas di setiap kilang" size={56} />
      </AbsoluteFill>

      <div style={{position: 'absolute', left: MAP.x, top: 220, display: 'flex', gap: 14, flexWrap: 'wrap', width: 820}}>
        {STEPS.map((s, i) => {
          const p = spring({frame: frame - 30 - i * 22, fps, config: {damping: 200}});
          return (
            <div key={s} style={{display: 'flex', alignItems: 'center', gap: 14, opacity: p}}>
              <div style={{padding: '14px 20px', borderRadius: 12, backgroundColor: COLORS.surface, border: `2px solid ${COLORS.blue}`, fontSize: 28, fontWeight: 600}}>{s}</div>
              {i < STEPS.length - 1 && <span style={{fontSize: 32, color: COLORS.blueLight}}>→</span>}
            </div>
          );
        })}
      </div>

      <svg width={MAP.w} height={MAP.h + 40} style={{position: 'absolute', left: MAP.x, top: MAP.y}}>
        {REFINERIES.map((r, i) => {
          const {x, y} = project(r.lon, r.lat, MAP.w, MAP.h);
          const p = spring({frame: frame - 150 - i * 15, fps, config: {damping: 12}});
          return (
            <g key={r.id} opacity={p}>
              <circle cx={x} cy={y} r={16 * p} fill={COLORS.gas} fillOpacity={0.25} />
              <circle cx={x} cy={y} r={7} fill={COLORS.gas} />
              <text x={x} y={y - 24} fill={COLORS.text} fontSize={22} fontWeight={600} textAnchor="middle">
                {r.id}
              </text>
            </g>
          );
        })}
      </svg>
      <div style={{position: 'absolute', left: MAP.x, top: MAP.y + MAP.h + 40, fontSize: 22, color: COLORS.muted}}>Rencana rollout 6 Refinery Unit</div>
    </SceneFrame>
  );
};
