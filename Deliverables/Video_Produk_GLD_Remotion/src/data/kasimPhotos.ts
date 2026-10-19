// Foto dokumentasi uji lapangan GLD generasi pertama di RU VII Kasim, di public/footage/kasim/.
// Sumber: foto tim (arsip lengkap: Sumber Dokumen/Foto_Uji_Lapangan_RU7_Kasim_2025/) + foto udara deck Kick-Off.
// Urutan = urutan tampil. Keterangan wajib faktual (hanya yang terlihat di foto).
export type KasimPhoto = {file: string; id: string; en: string};

export const KASIM_PHOTOS: KasimPhoto[] = [
  {
    file: 'footage/kasim/00_aerial_kickoff.jpeg',
    id: 'RU VII Kasim · lokasi uji lapangan · kolaborasi riset Fungsi Reliability PT KPI & ITB',
    en: 'RU VII Kasim · field test site · research collaboration of PT KPI Reliability Function & ITB',
  },
  {
    file: 'footage/kasim/01_persiapan.jpg',
    id: 'Pemeriksaan perangkat dan peralatan bersama petugas K3 sebelum masuk area · 28 November 2025',
    en: 'Equipment check with HSE personnel before site entry · 28 November 2025',
  },
  {
    file: 'footage/kasim/02_pemasangan_disaksikan.jpg',
    id: 'Pemasangan perangkat pada tiang, disaksikan personel kilang',
    en: 'Device installation on a pole, witnessed by refinery personnel',
  },
  {
    file: 'footage/kasim/03_pemasangan_panel_surya.jpg',
    id: 'Pemasangan perangkat pada tiang ber-panel surya',
    en: 'Installation on a solar-powered pole',
  },
  {
    file: 'footage/kasim/04_node_terpasang.jpg',
    id: 'Node bertenaga surya terpasang di tiang',
    en: 'Solar-powered node installed on a pole',
  },
  {
    file: 'footage/kasim/05_pemantauan_nodered.jpg',
    id: 'Pemantauan data pada server lokal (Node-RED)',
    en: 'Data monitoring on the local server (Node-RED)',
  },
  {
    file: 'footage/kasim/06_koordinasi_tim.jpg',
    id: 'Koordinasi tim di area proses RU VII Kasim',
    en: 'Team coordination in the RU VII Kasim process area',
  },
];
