import React from 'react';
import {AbsoluteFill, Img, spring, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {ASSETS, Asset} from '../assets';
import {AssetSlot} from '../components/AssetSlot';
import {Caption} from '../components/Caption';
import {SceneFrame} from '../components/SceneFrame';
import {Sfx} from '../components/Sfx';
import {useLayout} from '../layout';
import {COLORS} from '../theme';

// Logo di kartu putih (file logo berlatar putih); bila file belum ada, tampil teks nama.
const Logo: React.FC<{asset: Asset; fallback: string; h: number}> = ({asset, fallback, h}) =>
  asset.ready ? (
    <Img src={staticFile(asset.path)} style={{height: h, width: 'auto', objectFit: 'contain'}} />
  ) : (
    <div style={{fontSize: 30, fontWeight: 800, color: '#14213A', whiteSpace: 'nowrap'}}>{fallback}</div>
  );

export const Scene08Outro: React.FC = () => {
  const {portrait, padX, title} = useLayout();
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const logos = spring({frame: frame - 205, fps, config: {damping: 200}});
  return (
    <SceneFrame last>
      <AssetSlot asset={ASSETS.outro} kind="video" />
      <AbsoluteFill style={{background: `linear-gradient(transparent 40%, ${COLORS.overlay} 75%)`}} />
      <AbsoluteFill style={{justifyContent: 'flex-end', alignItems: 'center', padding: `0 ${padX}px ${portrait ? 400 : 170}px`, textAlign: 'center'}}>
        <Caption text="GLD" from={150} size={title(120)} color={COLORS.blueLight} />
        <Caption text="Deteksi multigas berbasis AI dengan jaringan yang memulihkan diri" from={175} size={portrait ? title(52) : 46} />
        <div
          style={{
            display: 'flex',
            flexDirection: portrait ? 'column' : 'row',
            gap: portrait ? 26 : 70,
            marginTop: 40,
            alignItems: 'center',
            padding: portrait ? '26px 40px' : '22px 56px',
            borderRadius: 18,
            backgroundColor: '#FFFFFF',
            boxShadow: '0 12px 36px rgba(0,0,0,0.35)',
            opacity: logos,
            transform: `translateY(${20 * (1 - logos)}px)`,
          }}
        >
          <div style={{display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 6}}>
            <Logo asset={ASSETS.logoPertamina} fallback="PT Pertamina Patra Niaga" h={portrait ? 64 : 58} />
            <div style={{fontSize: 20, fontWeight: 600, color: '#55627A', letterSpacing: 0.5}}>Fungsi Reliability</div>
          </div>
          <Logo asset={ASSETS.logoLgu} fallback="LAPI Ganesha Utama" h={portrait ? 92 : 84} />
          <Logo asset={ASSETS.logoItb} fallback="Institut Teknologi Bandung" h={portrait ? 118 : 108} />
        </div>
      </AbsoluteFill>
      {/* selaras render Blender: tautan STAR mulai 4,5 dtk, mesh mencapai gateway ~10 dtk */}
      <Sfx name="rise" at={135} volume={0.35} />
      <Sfx name="success" at={300} volume={0.3} />
    </SceneFrame>
  );
};
