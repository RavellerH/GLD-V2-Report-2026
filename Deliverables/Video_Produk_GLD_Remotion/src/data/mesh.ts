// Topologi ilustrasi untuk Adegan 6 (koordinat kanvas 1920x1080).
// Bukan layout kilang sebenarnya; ubah posisi/route di sini tanpa menyentuh komponen.
export type MeshNode = {id: string; label: string; kind: 'gld' | 'ch' | 'gw'; x: number; y: number};

export const NODES: MeshNode[] = [
  {id: 'g1', label: 'GLD-01', kind: 'gld', x: 230, y: 300},
  {id: 'g2', label: 'GLD-02', kind: 'gld', x: 200, y: 640},
  {id: 'g3', label: 'GLD-03', kind: 'gld', x: 620, y: 860},
  {id: 'ch1', label: 'CH-1', kind: 'ch', x: 480, y: 460},
  {id: 'ch2', label: 'CH-2', kind: 'ch', x: 860, y: 330},
  {id: 'ch3', label: 'CH-3', kind: 'ch', x: 880, y: 690},
  {id: 'ch4', label: 'CH-4', kind: 'ch', x: 1250, y: 470},
  {id: 'ch5', label: 'CH-5', kind: 'ch', x: 1240, y: 820},
  {id: 'gw', label: 'Gateway', kind: 'gw', x: 1640, y: 560},
];

// Link radio yang mungkin (mesh). GLD -> CH memakai radio STAR, CH <-> CH memakai radio MESH.
export const LINKS: [string, string][] = [
  ['g1', 'ch1'],
  ['g2', 'ch1'],
  ['g3', 'ch3'],
  ['ch1', 'ch2'],
  ['ch1', 'ch3'],
  ['ch2', 'ch3'],
  ['ch2', 'ch4'],
  ['ch3', 'ch4'],
  ['ch3', 'ch5'],
  ['ch4', 'ch5'],
  ['ch4', 'gw'],
  ['ch5', 'gw'],
];

export const FAILED_NODE = 'ch2';
export const PRIMARY_ROUTE = ['g1', 'ch1', 'ch2', 'ch4', 'gw'];
export const FAILOVER_ROUTE = ['g1', 'ch1', 'ch3', 'ch4', 'gw'];

export const nodeById = (id: string) => {
  const n = NODES.find((x) => x.id === id);
  if (!n) throw new Error(`Node tidak dikenal: ${id}`);
  return n;
};
