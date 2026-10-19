import React from 'react';
import {Composition, Folder} from 'remotion';
import {EXPLAINER_FRAMES, Explainer} from './Explainer';
import {INTRO_FRAMES, Intro} from './Intro';
import {OGI_FRAMES, OgiVideo} from './ogi/OgiVideo';
import {SCENE_COMPONENTS} from './scenes';
import {FPS, SCENES, sceneDuration} from './timeline';

const FORMATS = [
  {id: 'GLD-Explainer', label: 'Landscape', width: 1920, height: 1080},
  {id: 'GLD-Explainer-Portrait', label: 'Portrait', width: 1080, height: 1920},
];
// Versi bahasa: ID (istilah teknis bahasa Inggris) dan EN.
const LANGS = [
  {suffix: '', lang: 'id' as const},
  {suffix: '-EN', lang: 'en' as const},
];

export const RemotionRoot: React.FC = () => (
  <>
    {LANGS.flatMap((l) =>
      FORMATS.map((f) => (
        <Composition
          key={f.id + l.suffix}
          id={f.id + l.suffix}
          component={Explainer}
          defaultProps={{lang: l.lang}}
          durationInFrames={EXPLAINER_FRAMES}
          fps={FPS}
          width={f.width}
          height={f.height}
        />
      )),
    )}
    {/* Video OGI MWIR (konsep pengembangan, pameran) */}
    {LANGS.flatMap((l) =>
      FORMATS.map((f) => (
        <Composition
          key={'ogi' + f.id + l.suffix}
          id={f.id.replace('GLD-Explainer', 'OGI-Video') + l.suffix}
          component={OgiVideo}
          defaultProps={{lang: l.lang}}
          durationInFrames={OGI_FRAMES}
          fps={FPS}
          width={f.width}
          height={f.height}
        />
      )),
    )}
    {/* Intro motion graphic (berdiri sendiri) */}
    {LANGS.flatMap((l) =>
      FORMATS.map((f) => (
        <Composition
          key={'intro' + f.id + l.suffix}
          id={f.id.replace('Explainer', 'Intro') + l.suffix}
          component={Intro}
          defaultProps={{lang: l.lang}}
          durationInFrames={INTRO_FRAMES}
          fps={FPS}
          width={f.width}
          height={f.height}
        />
      )),
    )}
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
