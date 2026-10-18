import React from 'react';
import {Audio, Sequence, staticFile} from 'remotion';
import {SFX_ENABLED, SFX_VOLUME} from '../assets';

// Sound effect sintetis (tools/sfx.py -> public/audio/sfx). `at` = frame relatif adegan.
export type SfxName = 'whoosh' | 'whoosh_short' | 'pop' | 'blip' | 'tick' | 'alarm' | 'error' | 'success' | 'unplug' | 'clank' | 'hum' | 'rise';

export const Sfx: React.FC<{name: SfxName; at: number; volume?: number; loopFor?: number}> = ({name, at, volume = 0.3, loopFor}) =>
  SFX_ENABLED ? (
    <Sequence from={Math.max(0, Math.round(at))} durationInFrames={loopFor ?? 90} layout="none" name={`sfx ${name}`}>
      <Audio src={staticFile(`audio/sfx/${name}.wav`)} volume={volume * SFX_VOLUME} loop={Boolean(loopFor)} />
    </Sequence>
  ) : null;
