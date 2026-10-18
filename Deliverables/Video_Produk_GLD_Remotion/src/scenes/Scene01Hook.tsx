import React from 'react';
import {AbsoluteFill} from 'remotion';
import {ASSETS} from '../assets';
import {AssetSlot} from '../components/AssetSlot';
import {Caption} from '../components/Caption';
import {SceneFrame} from '../components/SceneFrame';

export const Scene01Hook: React.FC = () => (
  <SceneFrame>
    <AssetSlot asset={ASSETS.refinery} kind="video" />
    <AbsoluteFill style={{justifyContent: 'center', paddingLeft: 140}}>
      <Caption text="Gas bocor tidak terlihat." from={45} size={96} />
      <Caption text="Dan tidak menunggu." from={120} size={56} weight={400} style={{marginTop: 20}} />
    </AbsoluteFill>
  </SceneFrame>
);
