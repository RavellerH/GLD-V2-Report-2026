import React from 'react';
import {AbsoluteFill, Audio, Sequence, staticFile} from 'remotion';
import {SHOW_SUBTITLES} from '../assets';
import {TRANSITION} from '../components/SceneFrame';
import {Sfx} from '../components/Sfx';
import {Subtitles} from '../components/Subtitles';
import {LangProvider} from '../i18n';
import {COLORS, themeVars} from '../theme';
import {FPS, Lang} from '../timeline';
import {OgiCooled, OgiHook, OgiPhysics, OgiStakes, OgiToday} from './scenesA';
import {OgiEdgeAI, OgiField, OgiFusion, OgiLimits, OgiOutro, OgiStrategy} from './scenesB';
import {OGI_SCENES, OgiSceneId} from './timeline';

const COMPONENTS: Record<OgiSceneId, React.FC> = {
  ogi_hook: OgiHook,
  ogi_stakes: OgiStakes,
  ogi_today: OgiToday,
  ogi_physics: OgiPhysics,
  ogi_cooled: OgiCooled,
  ogi_field: OgiField,
  ogi_edgeai: OgiEdgeAI,
  ogi_fusion: OgiFusion,
  ogi_limits: OgiLimits,
  ogi_strategy: OgiStrategy,
  ogi_outro: OgiOutro,
};

const from = (s: {startSec: number}) => Math.round(s.startSec * FPS);
const dur = (s: {startSec: number; endSec: number}) => Math.round((s.endSec - s.startSec) * FPS);
export const OGI_FRAMES = Math.round(OGI_SCENES[OGI_SCENES.length - 1].endSec * FPS);

export const OgiVideo: React.FC<{lang?: Lang}> = ({lang = 'id'}) => (
  <LangProvider lang={lang}>
    <AbsoluteFill style={{...themeVars('night'), backgroundColor: COLORS.bg}}>
      {OGI_SCENES.map((s, i) => {
        const Scene = COMPONENTS[s.id];
        const last = i === OGI_SCENES.length - 1;
        return (
          <Sequence key={s.id} name={s.title} from={from(s)} durationInFrames={dur(s) + (last ? 0 : TRANSITION)}>
            <Scene />
            {i > 0 && <Sfx name="whoosh" at={0} volume={0.3} />}
            {SHOW_SUBTITLES && !last && <Subtitles id={s.id} />}
            <Audio src={staticFile(`audio/vo_ogi${lang === 'en' ? '_en' : ''}/${String(i + 1).padStart(2, '0')}_${s.id}.wav`)} />
          </Sequence>
        );
      })}
      <Audio src={staticFile('audio/music_ogi.wav')} volume={0.07} />
    </AbsoluteFill>
  </LangProvider>
);
