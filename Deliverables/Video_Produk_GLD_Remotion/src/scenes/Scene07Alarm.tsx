import React from 'react';
import {AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {ASSETS} from '../assets';
import {AssetSlot} from '../components/AssetSlot';
import {Caption} from '../components/Caption';
import {SceneFrame} from '../components/SceneFrame';
import {COLORS} from '../theme';

// Mock dashboard; diganti otomatis oleh screenshot asli bila ASSETS.dashboard.ready = true.
const MockDashboard: React.FC = () => (
  <AbsoluteFill style={{flexDirection: 'row', backgroundColor: '#F3F4F6'}}>
    <div style={{width: 280, backgroundColor: COLORS.charcoal, padding: 30, color: COLORS.text, fontSize: 26, fontWeight: 800}}>GLD Monitor</div>
    <div style={{flex: 1, padding: 40, display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 24, alignContent: 'start'}}>
      {['GLD-01', 'GLD-02', 'GLD-03', 'CH-1', 'CH-3', 'Gateway'].map((n) => (
        <div key={n} style={{height: 150, borderRadius: 14, backgroundColor: 'white', padding: 22, color: COLORS.charcoal, fontSize: 26, fontWeight: 600, boxShadow: '0 2px 8px rgba(0,0,0,0.08)'}}>
          {n}
          <div style={{marginTop: 14, fontSize: 20, color: COLORS.ok}}>● Online</div>
        </div>
      ))}
    </div>
  </AbsoluteFill>
);

export const Scene07Alarm: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const slide = spring({frame: frame - 60, fps, config: {damping: 15}});
  const pulse = 0.6 + 0.4 * Math.abs(Math.sin(frame / 8));

  return (
    <SceneFrame>
      <div style={{position: 'absolute', left: 160, top: 170, width: 1600, height: 760, borderRadius: 18, overflow: 'hidden', boxShadow: '0 30px 80px rgba(0,0,0,0.5)'}}>
        {ASSETS.dashboard.ready ? <AssetSlot asset={ASSETS.dashboard} kind="image" /> : <MockDashboard />}
        <div
          style={{
            position: 'absolute',
            right: 40,
            top: 40,
            width: 560,
            padding: 30,
            borderRadius: 16,
            backgroundColor: COLORS.alarm,
            color: 'white',
            transform: `translateX(${interpolate(slide, [0, 1], [700, 0])}px)`,
            boxShadow: `0 0 ${40 * pulse}px ${COLORS.alarm}`,
          }}
        >
          <div style={{fontSize: 24, fontWeight: 600, opacity: 0.9}}>ALARM · push otomatis</div>
          <div style={{fontSize: 46, fontWeight: 800, marginTop: 8}}>LPG terdeteksi</div>
          <div style={{fontSize: 26, marginTop: 12}}>Node GLD-03 · Area: Unit Proses</div>
        </div>
      </div>
      {/* Dua jalur data: normal (cache + pull berkala) vs alarm (push segera). */}
      <div style={{position: 'absolute', left: 1220, top: 520, width: 500, display: 'flex', flexDirection: 'column', gap: 18}}>
        {[
          {label: 'Data normal', sub: 'disimpan di Cluster Head, diambil berkala (pull)', color: COLORS.ok, at: 120},
          {label: 'Alarm', sub: 'dikirim segera (push), tanpa menunggu siklus pull', color: COLORS.alarm, at: 150},
        ].map((r) => {
          const p = spring({frame: frame - r.at, fps, config: {damping: 200}});
          return (
            <div key={r.label} style={{opacity: p, padding: '18px 22px', borderRadius: 14, backgroundColor: 'white', borderLeft: `8px solid ${r.color}`, color: COLORS.charcoal, boxShadow: '0 4px 16px rgba(0,0,0,0.12)'}}>
              <div style={{fontSize: 28, fontWeight: 800}}>{r.label}</div>
              <div style={{fontSize: 22, marginTop: 4}}>{r.sub}</div>
            </div>
          );
        })}
      </div>
      <AbsoluteFill style={{padding: '60px 160px'}}>
        <Caption text="Alarm langsung ke operator" size={60} />
      </AbsoluteFill>
    </SceneFrame>
  );
};
