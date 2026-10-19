import React from 'react';
import {AbsoluteFill, Audio, Sequence, staticFile} from 'remotion';
import {ASSETS, SHOW_SUBTITLES, VO_READY, voPath} from './assets';
import {TRANSITION} from './components/SceneFrame';
import {Sfx} from './components/Sfx';
import {Subtitles} from './components/Subtitles';
import {SCENE_COMPONENTS} from './scenes';
import {COLORS, themeVars} from './theme';
import {LangProvider} from './i18n';
import {INTRO_FRAMES, Intro} from './Intro';
import {Lang, SCENES, TOTAL_FRAMES, sceneDuration, sceneFrom} from './timeline';

// Intro motion graphic di depan; adegan 1 crossfade di atas akhir intro.
export const INTRO_OFFSET = INTRO_FRAMES - TRANSITION;
export const EXPLAINER_FRAMES = INTRO_OFFSET + TOTAL_FRAMES;

// Komposisi utama (durasi dari timeline.ts): tiap adegan berjalan di Sequence-nya sendiri,
// sehingga frame di dalam adegan selalu mulai dari 0. Dipakai untuk landscape maupun portrait.
export const Explainer: React.FC<{lang?: Lang}> = ({lang = 'id'}) => (
  <LangProvider lang={lang}>
  <AbsoluteFill style={{...themeVars('night'), backgroundColor: COLORS.bg}}>
    <Sequence name="00 Intro" durationInFrames={INTRO_FRAMES}>
      <Intro lang={lang} />
    </Sequence>
    {SCENES.map((s, i) => {
      const Scene = SCENE_COMPONENTS[s.id];
      return (
        // Adegan diperpanjang TRANSITION frame (kecuali terakhir) supaya adegan berikutnya crossfade di atasnya.
        <Sequence key={s.id} name={s.title} from={INTRO_OFFSET + sceneFrom(s)} durationInFrames={sceneDuration(s) + (i < SCENES.length - 1 ? TRANSITION : 0)}>
          <Scene />
          {/* whoosh lembut di setiap peralihan adegan */}
          {i > 0 && <Sfx name="whoosh" at={0} volume={0.35} />}
          {SHOW_SUBTITLES && <Subtitles id={s.id} />}
          {/* Narasi per adegan: mulai di awal adegan, otomatis terpotong di akhir adegan. */}
          {VO_READY && <Audio src={staticFile(voPath(i, s.id, lang))} />}
        </Sequence>
      );
    })}
    {ASSETS.music.ready && <Audio src={staticFile(ASSETS.music.path)} volume={0.07} />}
  </AbsoluteFill>
  </LangProvider>
);
