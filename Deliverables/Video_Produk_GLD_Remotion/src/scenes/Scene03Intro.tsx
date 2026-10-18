import React from 'react';
import {AbsoluteFill} from 'remotion';
import {ASSETS} from '../assets';
import {AssetSlot} from '../components/AssetSlot';
import {Caption} from '../components/Caption';
import {SceneFrame} from '../components/SceneFrame';
import {Sfx} from '../components/Sfx';
import {useLayout} from '../layout';
import {COLORS} from '../theme';

// Sebut spesifikasi, bukan nama/seri produk komponen.
// Frame kemunculan label: sensor, akuisisi (motherboard), prosesor (motherboard), radio (antena).
const LABEL_AT = [205, 222, 238, 254];
const PARTS = ['8 sensor gas semikonduktor oksida logam', 'Akuisisi data presisi 24-bit', 'Prosesor AI dual-core 240 MHz', 'Radio LoRa 920 MHz'];

export const Scene03Intro: React.FC = () => {
  const {portrait, padX, title} = useLayout();
  return (
    <SceneFrame>
      <AssetSlot asset={ASSETS.hero} kind="video" />
      <AbsoluteFill style={{justifyContent: 'flex-start', padding: portrait ? `200px ${padX}px` : `90px ${padX}px`}}>
        <Caption text="GLD — Gas Leak Detection" from={20} size={title(88)} />
        <Caption text="LAPI Ganesha Utama × Institut Teknologi Bandung" from={45} size={title(36)} weight={400} color={COLORS.muted} style={{marginTop: 14}} />
      </AbsoluteFill>
      {/* Label exploded view, selaras render Blender: tutup lepas 4,0 dtk, kabel dicabut 4,9 dtk,
          bagian lain terurai mulai 5,7 dtk (papan sensor & motherboard keluar ~6,6-7,6 dtk).
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
          <Caption key={p} text={p} from={LABEL_AT[i]} size={title(40)} weight={600} style={{borderLeft: `6px solid ${COLORS.blue}`, paddingLeft: 18}} />
        ))}
      </AbsoluteFill>
      {/* selaras render Blender: tutup lepas 4,0 dtk, kabel dicabut 4,9 dtk, terurai 5,7 dtk */}
      <Sfx name="clank" at={120} volume={0.35} />
      <Sfx name="unplug" at={147} volume={0.5} />
      <Sfx name="unplug" at={154} volume={0.4} />
      <Sfx name="whoosh_short" at={171} volume={0.35} />
      {LABEL_AT.map((f) => <Sfx key={f} name="pop" at={f} volume={0.2} />)}
    </SceneFrame>
  );
};
