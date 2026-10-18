import React from 'react';
import {Composition, Folder} from 'remotion';
import {Explainer} from './Explainer';
import {SCENE_COMPONENTS} from './scenes';
import {FPS, SCENES, TOTAL_FRAMES, sceneDuration} from './timeline';

const FORMATS = [
  {id: 'GLD-Explainer', label: 'Landscape', width: 1920, height: 1080},
  {id: 'GLD-Explainer-Portrait', label: 'Portrait', width: 1080, height: 1920},
];

export const RemotionRoot: React.FC = () => (
  <>
    {FORMATS.map((f) => (
      <Composition key={f.id} id={f.id} component={Explainer} durationInFrames={TOTAL_FRAMES} fps={FPS} width={f.width} height={f.height} />
    ))}
    {/* Tiap adegan juga tersedia terpisah per orientasi supaya cepat di-preview di Studio. */}
    {FORMATS.map((f) => (
      <Folder key={f.label} name={`Adegan-${f.label}`}>
        {SCENES.map((s, i) => (
          <Composition
            key={s.id}
            id={`${f.label}-${String(i + 1).padStart(2, '0')}-${s.id}`}
            component={SCENE_COMPONENTS[s.id]}
            durationInFrames={sceneDuration(s)}
            fps={FPS}
            width={f.width}
            height={f.height}
          />
        ))}
      </Folder>
    ))}
  </>
);
