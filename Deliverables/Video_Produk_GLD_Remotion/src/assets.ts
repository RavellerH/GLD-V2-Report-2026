// Daftar aset eksternal. Taruh file di public/<path>, lalu ubah `ready` jadi true.
// Selama `ready: false`, video menampilkan placeholder berlabel sehingga tetap bisa dirender.
// `portraitPath` dipakai komposisi portrait (HP); bila kosong, `path` dipakai di kedua orientasi.
export type Asset = {path: string; portraitPath?: string; ready: boolean; note: string};

// Sound effect sintetis (tools/sfx.py). Matikan dengan SFX_ENABLED = false; SFX_VOLUME = pengali global.
export const SFX_ENABLED = true;
export const SFX_VOLUME = 1.0;

export const ASSETS = {
  // Render Blender: MP4/MOV (ProRes 4444 bila butuh alpha), 30 fps, durasi = durasi adegan.
  // Landscape 1920x1080, portrait 1080x1920 (render kamera terpisah di Blender).
  // B-roll Seedance (720p, 24 fps, 8 dtk); prompt di seedance/PROMPT_SEEDANCE.md (B1).
  refinery: {
    path: 'broll/b1_hook.mp4',
    portraitPath: 'broll/portrait/b1_hook.mp4',
    ready: true,
    note: 'Seedance: kilang senja + kebocoran gas (8 dtk)',
  },
  hero: {
    path: 'blender/scene03_hero_exploded.mp4',
    portraitPath: 'blender/portrait/scene03_hero_exploded.mp4',
    ready: false,
    note: 'Blender: hero shot GLD berputar lalu exploded view (9 dtk)',
  },
  chamber: {
    path: 'blender/scene05_chamber.mp4',
    portraitPath: 'blender/portrait/scene05_chamber.mp4',
    ready: false,
    note: 'Blender: gas test chamber, komponen disorot berurutan 1–4 (16 dtk)',
  },
  outro: {
    path: 'blender/scene08_outro.mp4',
    portraitPath: 'blender/portrait/scene08_outro.mp4',
    ready: false,
    note: 'Blender: GLD terpasang, kamera mundur ke jaringan node (10 dtk)',
  },

  // Gambar
  dashboard: {path: 'images/dashboard.png', ready: true, note: 'Alarm Console dashboard RU4 asli (repo gasleakdetectionV2-April, data demo)'},
  logoLgu: {path: 'images/logo_lgu.png', ready: false, note: 'Logo LAPI Ganesha Utama (PNG transparan)'},
  logoItb: {path: 'images/logo_itb.png', ready: false, note: 'Logo ITB (PNG transparan)'},

  // Musik latar (narasi per adegan diatur oleh VO_READY di bawah)
  music: {path: 'audio/music.mp3', ready: false, note: 'Musik latar bebas royalti'},
} satisfies Record<string, Asset>;

// Narasi per adegan: public/audio/vo/<nn>_<id>.wav (mis. 04_fingerprint.wav), hasil Gemini TTS.
// Nama file dibuat oleh tools/export_vo.py. Set true setelah kedelapan file tersedia.
export const VO_READY = false;
export const voPath = (index: number, id: string) => `audio/vo/${String(index + 1).padStart(2, '0')}_${id}.wav`;

// Matikan bila narasi sudah direkam dan subtitle tidak diinginkan.
export const SHOW_SUBTITLES = true;
