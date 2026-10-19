import React from 'react';
import {AbsoluteFill} from 'remotion';
import {ASSETS} from '../assets';
import {AssetSlot} from '../components/AssetSlot';
import {Caption} from '../components/Caption';
import {SceneFrame} from '../components/SceneFrame';
import {useLang, useT} from '../i18n';
import {useLayout} from '../layout';

export const Scene01Hook: React.FC = () => {
  const {portrait, padX, title} = useLayout();
  const t = useT();
  return (
    <SceneFrame>
      <AssetSlot asset={ASSETS.refinery} kind="video" />
      {/* Portrait: teks di sepertiga atas agar tidak menutupi objek utama render Blender. */}
      <AbsoluteFill style={{justifyContent: portrait ? 'flex-start' : 'center', padding: portrait ? `260px ${padX}px` : `0 ${padX}px`}}>
        <Caption text={t('Kebocoran gas bersifat tak kasatmata.', 'Gas leaks are invisible.')} from={45} size={title(96)} />
        <Caption text={t('Kecepatan deteksi menentukan tingkat risiko.', 'Detection speed determines the level of risk.')} from={120} size={title(56)} weight={400} style={{marginTop: 20}} />
      </AbsoluteFill>
    </SceneFrame>
  );
};
