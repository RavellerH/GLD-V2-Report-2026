import React from 'react';
import {AbsoluteFill} from 'remotion';
import {ASSETS} from '../assets';
import {AssetSlot} from '../components/AssetSlot';
import {Caption} from '../components/Caption';
import {SceneFrame} from '../components/SceneFrame';
import {COLORS} from '../theme';

const Logo: React.FC<{asset: (typeof ASSETS)['logoLgu']; fallback: string}> = ({asset, fallback}) =>
  asset.ready ? (
    <div style={{width: 220, height: 110, position: 'relative'}}>
      <AssetSlot asset={asset} kind="image" style={{objectFit: 'contain'}} />
    </div>
  ) : (
    <div style={{fontSize: 34, fontWeight: 800, color: COLORS.muted}}>{fallback}</div>
  );

export const Scene08Outro: React.FC = () => (
  <SceneFrame>
    <AssetSlot asset={ASSETS.outro} kind="video" />
    <AbsoluteFill style={{background: 'linear-gradient(transparent 40%, rgba(20,18,16,0.92) 75%)'}} />
    <AbsoluteFill style={{justifyContent: 'flex-end', alignItems: 'center', paddingBottom: 170, textAlign: 'center'}}>
      <Caption text="GLD" from={150} size={120} color={COLORS.blueLight} />
      <Caption text="Satu perangkat. Banyak gas. Jaringan yang tak terputus." from={175} size={52} />
      <div style={{display: 'flex', gap: 60, marginTop: 40, alignItems: 'center'}}>
        <Logo asset={ASSETS.logoLgu} fallback="LAPI Ganesha Utama" />
        <Logo asset={ASSETS.logoItb} fallback="ITB" />
      </div>
    </AbsoluteFill>
  </SceneFrame>
);
