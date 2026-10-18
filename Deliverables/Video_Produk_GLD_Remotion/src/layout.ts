import {useVideoConfig} from 'remotion';

// Dua orientasi dari satu kode: landscape 1920x1080 dan portrait (HP) 1080x1920.
export const useLayout = () => {
  const {width, height} = useVideoConfig();
  const portrait = height > width;
  return {
    portrait,
    width,
    height,
    padX: portrait ? 64 : 120,
    // Portrait menyisakan ruang bawah untuk UI aplikasi HP (tombol, caption medsos).
    subtitleBottom: portrait ? 220 : 48,
    // Skala judul; portrait lebih sempit sehingga judul dikecilkan sedikit.
    title: (landscapeSize: number) => (portrait ? Math.round(landscapeSize * 0.82) : landscapeSize),
  };
};
