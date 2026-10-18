import React from 'react';
import {AbsoluteFill} from 'remotion';
import {ASSETS} from '../assets';
import {AssetSlot} from '../components/AssetSlot';
import {Caption} from '../components/Caption';
import {SceneFrame} from '../components/SceneFrame';
import {COLORS} from '../theme';

const PARTS = ['8 sensor gas oksida logam (MQ)', 'ADC 24-bit (ADS1256)', 'ESP32-S3 · inferensi AI', 'Radio LoRa 920 MHz'];

export const Scene03Intro: React.FC = () => (
  <SceneFrame>
    <AssetSlot asset={ASSETS.hero} kind="video" />
    <AbsoluteFill style={{justifyContent: 'flex-start', padding: '90px 120px'}}>
      <Caption text="GLD — Gas Leak Detection" from={20} size={88} />
      <Caption text="LAPI Ganesha Utama × Institut Teknologi Bandung" from={45} size={36} weight={400} color={COLORS.muted} style={{marginTop: 14}} />
    </AbsoluteFill>
    {/* Label exploded view; selaraskan waktu `from` dengan render Blender. */}
    <AbsoluteFill style={{justifyContent: 'center', alignItems: 'flex-end', paddingRight: 140, gap: 26}}>
      {PARTS.map((p, i) => (
        <Caption key={p} text={p} from={120 + i * 20} size={40} weight={600} style={{borderLeft: `6px solid ${COLORS.blue}`, paddingLeft: 18}} />
      ))}
    </AbsoluteFill>
  </SceneFrame>
);
