import React from 'react';
import {AbsoluteFill, Audio, Sequence, staticFile} from 'remotion';
import {ASSETS, SHOW_SUBTITLES} from './assets';
import {Subtitles} from './components/Subtitles';
import {SCENE_COMPONENTS} from './scenes';
import {COLORS} from './theme';
import {SCENES, sceneDuration, sceneFrom} from './timeline';

// Komposisi utama 120 detik: tiap adegan berjalan di Sequence-nya sendiri,
// sehingga frame di dalam adegan selalu mulai dari 0.
export const Explainer: React.FC = () => (
  <AbsoluteFill style={{backgroundColor: COLORS.bg}}>
    {SCENES.map((s) => {
      const Scene = SCENE_COMPONENTS[s.id];
      return (
        <Sequence key={s.id} name={s.title} from={sceneFrom(s)} durationInFrames={sceneDuration(s)}>
          <Scene />
          {SHOW_SUBTITLES && <Subtitles vo={s.vo} />}
        </Sequence>
      );
    })}
    {ASSETS.voiceover.ready && <Audio src={staticFile(ASSETS.voiceover.path)} />}
    {ASSETS.music.ready && <Audio src={staticFile(ASSETS.music.path)} volume={0.18} />}
  </AbsoluteFill>
);
