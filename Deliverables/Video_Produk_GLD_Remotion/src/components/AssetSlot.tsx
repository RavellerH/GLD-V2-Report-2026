import React from 'react';
import {AbsoluteFill, Img, OffthreadVideo, staticFile} from 'remotion';
import type {Asset} from '../assets';
import {useLayout} from '../layout';
import {COLORS} from '../theme';

// Menampilkan aset bila sudah siap; bila belum, placeholder berlabel agar tim tahu apa yang harus diisi.
export const AssetSlot: React.FC<{asset: Asset; kind: 'video' | 'image'; style?: React.CSSProperties}> = ({asset, kind, style}) => {
  const {portrait, padX} = useLayout();
  const path = portrait && asset.portraitPath ? asset.portraitPath : asset.path;
  if (asset.ready) {
    const src = staticFile(path);
    const fill: React.CSSProperties = {width: '100%', height: '100%', objectFit: 'cover', ...style};
    return kind === 'video' ? <OffthreadVideo src={src} muted style={fill} /> : <Img src={src} style={fill} />;
  }
  return (
    <AbsoluteFill
      style={{
        // Label di kiri-tengah agar tidak bertabrakan dengan judul (atas) dan subtitle (bawah).
        alignItems: 'flex-start',
        justifyContent: 'center',
        paddingLeft: padX,
        paddingRight: padX,
        background: `repeating-linear-gradient(45deg, ${COLORS.surface} 0 24px, ${COLORS.bg} 24px 48px)`,
        border: `4px dashed ${COLORS.line}`,
        ...style,
      }}
    >
      <div style={{maxWidth: 900, color: COLORS.muted}}>
        <div style={{fontSize: 30, fontWeight: 800, color: COLORS.gas}}>PLACEHOLDER</div>
        <div style={{fontSize: 34, fontWeight: 600, marginTop: 12, color: COLORS.text}}>{asset.note}</div>
        <div style={{fontSize: 24, marginTop: 10}}>public/{path}</div>
      </div>
    </AbsoluteFill>
  );
};
