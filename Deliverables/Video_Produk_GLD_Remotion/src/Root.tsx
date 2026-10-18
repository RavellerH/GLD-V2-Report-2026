import React from 'react';
import {Composition, Folder} from 'remotion';
import {Explainer} from './Explainer';
import {SCENE_COMPONENTS} from './scenes';
import {FPS, HEIGHT, SCENES, TOTAL_FRAMES, WIDTH, sceneDuration} from './timeline';

export const RemotionRoot: React.FC = () => (
  <>
    <Composition id="GLD-Explainer" component={Explainer} durationInFrames={TOTAL_FRAMES} fps={FPS} width={WIDTH} height={HEIGHT} />
    {/* Tiap adegan juga tersedia terpisah supaya cepat di-preview di Studio. */}
    <Folder name="Adegan">
      {SCENES.map((s, i) => (
        <Composition
          key={s.id}
          id={`Scene-${String(i + 1).padStart(2, '0')}-${s.id}`}
          component={SCENE_COMPONENTS[s.id]}
          durationInFrames={sceneDuration(s)}
          fps={FPS}
          width={WIDTH}
          height={HEIGHT}
        />
      ))}
    </Folder>
  </>
);
