import React from 'react';
import {COLORS} from '../theme';

// Ikon vektor sederhana agar proyek tidak bergantung pada aset eksternal.
export const GldIcon: React.FC<{size?: number; color?: string}> = ({size = 80, color = COLORS.blue}) => (
  <svg width={size} height={size * 1.4} viewBox="0 0 50 70">
    <rect x="3" y="2" width="44" height="56" rx="8" fill={COLORS.surface} stroke={color} strokeWidth="3" />
    <circle cx="25" cy="22" r="9" fill="none" stroke={color} strokeWidth="3" />
    <rect x="12" y="38" width="26" height="4" rx="2" fill={color} />
    <rect x="12" y="46" width="18" height="4" rx="2" fill={color} opacity={0.6} />
    <rect x="17" y="58" width="16" height="10" rx="2" fill={color} />
  </svg>
);

export const DetectorIcon: React.FC<{size?: number}> = ({size = 70}) => (
  <svg width={size} height={size} viewBox="0 0 50 50">
    <circle cx="25" cy="25" r="21" fill={COLORS.surface} stroke={COLORS.muted} strokeWidth="3" />
    <circle cx="25" cy="25" r="8" fill={COLORS.muted} />
  </svg>
);
