import React from 'react';
import {AbsoluteFill, Audio, Sequence, staticFile} from 'remotion';
import {ASSETS, SHOW_SUBTITLES, VO_READY, voPath} from './assets';
import {Subtitles} from './components/Subtitles';
import {SCENE_COMPONENTS} from './scenes';
import {COLORS} from './theme';
import {SCENES, sceneDuration, sceneFrom} from './timeline';

// Komposisi utama 120 detik: tiap adegan berjalan di Sequence-nya sendiri,
// sehingga frame di dalam adegan selalu mulai dari 0. Dipakai untuk landscape maupun portrait.
export const Explainer: React.FC = () => (
  <AbsoluteFill style={{backgroundColor: COLORS.bg}}>
    {SCENES.map((s, i) => {
      const Scene = SCENE_COMPONENTS[s.id];
      return (
        <Sequence key={s.id} name={s.title} from={sceneFrom(s)} durationInFrames={sceneDuration(s)}>
          <Scene />
          {SHOW_SUBTITLES && <Subtitles vo={s.vo} />}
          {/* Narasi per adegan: mulai di awal adegan, otomatis terpotong di akhir adegan. */}
          {VO_READY && <Audio src={staticFile(voPath(i, s.id))} />}
        </Sequence>
      );
    })}
    {ASSETS.music.ready && <Audio src={staticFile(ASSETS.music.path)} volume={0.18} />}
  </AbsoluteFill>
);
