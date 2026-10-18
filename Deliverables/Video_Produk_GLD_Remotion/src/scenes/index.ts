import type React from 'react';
import type {SceneId} from '../timeline';
import {Scene01Hook} from './Scene01Hook';
import {Scene02Problem} from './Scene02Problem';
import {Scene03Intro} from './Scene03Intro';
import {Scene04Fingerprint} from './Scene04Fingerprint';
import {Scene05Trainable} from './Scene05Trainable';
import {Scene06Mesh} from './Scene06Mesh';
import {Scene07Alarm} from './Scene07Alarm';
import {Scene08Outro} from './Scene08Outro';

export const SCENE_COMPONENTS: Record<SceneId, React.FC> = {
  hook: Scene01Hook,
  problem: Scene02Problem,
  intro: Scene03Intro,
  fingerprint: Scene04Fingerprint,
  trainable: Scene05Trainable,
  mesh: Scene06Mesh,
  alarm: Scene07Alarm,
  outro: Scene08Outro,
};
