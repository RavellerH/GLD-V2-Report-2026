// Rencana rollout 6 RU (roadmap program, bukan status terpasang). Koordinat lon/lat perkiraan.
export const REFINERIES = [
  {id: 'RU II', city: 'Dumai', lon: 101.45, lat: 1.67},
  {id: 'RU III', city: 'Plaju', lon: 104.8, lat: -3.0},
  {id: 'RU IV', city: 'Cilacap', lon: 109.0, lat: -7.7},
  {id: 'RU V', city: 'Balikpapan', lon: 116.8, lat: -1.27},
  {id: 'RU VI', city: 'Balongan', lon: 108.4, lat: -6.38},
  {id: 'RU VII', city: 'Kasim', lon: 131.3, lat: -1.0},
];

// Proyeksi equirectangular ke kotak w x h untuk wilayah Indonesia.
export const project = (lon: number, lat: number, w: number, h: number) => ({
  x: ((lon - 95) / (141 - 95)) * w,
  y: ((6 - lat) / (6 + 11)) * h,
});
