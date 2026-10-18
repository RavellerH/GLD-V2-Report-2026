// Daftar aset eksternal. Taruh file di public/<path>, lalu ubah `ready` jadi true.
// Selama `ready: false`, video menampilkan placeholder berlabel sehingga tetap bisa dirender.
export type Asset = {path: string; ready: boolean; note: string};

export const ASSETS = {
  // Render Blender: MP4/MOV (ProRes 4444 bila butuh alpha) 1920x1080, 30 fps, durasi = durasi adegan.
  refinery: {path: 'blender/scene01_refinery.mp4', ready: false, note: 'Blender: kilang senja + kebocoran gas (10 dtk)'},
  hero: {path: 'blender/scene03_hero_exploded.mp4', ready: false, note: 'Blender: hero shot GLD berputar lalu exploded view (13 dtk)'},
  outro: {path: 'blender/scene08_outro.mp4', ready: false, note: 'Blender: GLD terpasang, kamera mundur ke jaringan node (12 dtk)'},

  // Gambar
  chamber: {path: 'images/chamber_setup_lengkap.jpeg', ready: true, note: 'Foto asli gas test chamber'},
  dashboard: {path: 'images/dashboard.png', ready: false, note: 'Screenshot dashboard aplikasi asli (1920x1080)'},
  logoLgu: {path: 'images/logo_lgu.png', ready: false, note: 'Logo LAPI Ganesha Utama (PNG transparan)'},
  logoItb: {path: 'images/logo_itb.png', ready: false, note: 'Logo ITB (PNG transparan)'},

  // Audio
  voiceover: {path: 'audio/voiceover.mp3', ready: false, note: 'Narasi 120 dtk, mengikuti timeline.ts'},
  music: {path: 'audio/music.mp3', ready: false, note: 'Musik latar bebas royalti'},
} satisfies Record<string, Asset>;

// Matikan bila narasi sudah direkam dan subtitle tidak diinginkan.
export const SHOW_SUBTITLES = true;
