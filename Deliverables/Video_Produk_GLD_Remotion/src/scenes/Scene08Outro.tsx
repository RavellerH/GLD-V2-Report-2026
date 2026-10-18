import React from 'react';
import {AbsoluteFill} from 'remotion';
import {ASSETS} from '../assets';
import {AssetSlot} from '../components/AssetSlot';
import {Caption} from '../components/Caption';
import {SceneFrame} from '../components/SceneFrame';
import {Sfx} from '../components/Sfx';
import {useLayout} from '../layout';
import {COLORS} from '../theme';

const Logo: React.FC<{asset: (typeof ASSETS)['logoLgu']; fallback: string}> = ({asset, fallback}) =>
  asset.ready ? (
    <div style={{width: 220, height: 110, position: 'relative'}}>
      <AssetSlot asset={asset} kind="image" style={{objectFit: 'contain'}} />
    </div>
  ) : (
    <div style={{fontSize: 34, fontWeight: 800, color: COLORS.muted}}>{fallback}</div>
  );

export const Scene08Outro: React.FC = () => {
  const {portrait, padX, title} = useLayout();
  return (
    <SceneFrame last>
      <AssetSlot asset={ASSETS.outro} kind="video" />
      <AbsoluteFill style={{background: `linear-gradient(transparent 40%, ${COLORS.overlay} 75%)`}} />
      <AbsoluteFill style={{justifyContent: 'flex-end', alignItems: 'center', padding: `0 ${padX}px ${portrait ? 400 : 170}px`, textAlign: 'center'}}>
        <Caption text="GLD" from={150} size={title(120)} color={COLORS.blueLight} />
        <Caption text="Deteksi multigas berbasis AI dengan jaringan yang memulihkan diri" from={175} size={portrait ? title(52) : 46} />
        <div style={{display: 'flex', flexDirection: portrait ? 'column' : 'row', gap: portrait ? 20 : 60, marginTop: 40, alignItems: 'center'}}>
          <Logo asset={ASSETS.logoLgu} fallback="LAPI Ganesha Utama" />
          <Logo asset={ASSETS.logoItb} fallback="ITB" />
        </div>
      </AbsoluteFill>
      {/* selaras render Blender: tautan STAR mulai 4,5 dtk, mesh mencapai gateway ~10 dtk */}
      <Sfx name="rise" at={135} volume={0.35} />
      <Sfx name="success" at={300} volume={0.3} />
    </SceneFrame>
  );
};
