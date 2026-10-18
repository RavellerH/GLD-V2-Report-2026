import React from 'react';
import {AbsoluteFill} from 'remotion';
import {ASSETS} from '../assets';
import {AssetSlot} from '../components/AssetSlot';
import {Caption} from '../components/Caption';
import {SceneFrame} from '../components/SceneFrame';
import {useLayout} from '../layout';
import {COLORS} from '../theme';

const PARTS = ['8 sensor gas oksida logam (MQ)', 'ADC 24-bit (ADS1256)', 'ESP32-S3 · inferensi AI', 'Radio LoRa 920 MHz'];

export const Scene03Intro: React.FC = () => {
  const {portrait, padX, title} = useLayout();
  return (
    <SceneFrame>
      <AssetSlot asset={ASSETS.hero} kind="video" />
      <AbsoluteFill style={{justifyContent: 'flex-start', padding: portrait ? `200px ${padX}px` : `90px ${padX}px`}}>
        <Caption text="GLD — Gas Leak Detection" from={20} size={title(88)} />
        <Caption text="LAPI Ganesha Utama × Institut Teknologi Bandung" from={45} size={title(36)} weight={400} color={COLORS.muted} style={{marginTop: 14}} />
      </AbsoluteFill>
      {/* Label exploded view; selaraskan waktu `from` dengan render Blender.
          Portrait: label di bawah, di atas area subtitle. */}
      <AbsoluteFill
        style={{
          justifyContent: portrait ? 'flex-end' : 'center',
          alignItems: portrait ? 'flex-start' : 'flex-end',
          padding: portrait ? `0 ${padX}px 420px` : `0 140px 0 0`,
          gap: portrait ? 18 : 26,
        }}
      >
        {PARTS.map((p, i) => (
          <Caption key={p} text={p} from={120 + i * 20} size={title(40)} weight={600} style={{borderLeft: `6px solid ${COLORS.blue}`, paddingLeft: 18}} />
        ))}
      </AbsoluteFill>
    </SceneFrame>
  );
};
