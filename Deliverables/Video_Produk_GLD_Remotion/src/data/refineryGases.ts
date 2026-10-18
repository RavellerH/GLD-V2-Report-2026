// Gas yang umum dijumpai di kilang, beserta status kemampuan GLD saat ini.
// Status harus jujur: hanya 'validated' yang boleh disebut "dikenali model".
export type GasStatus = 'validated' | 'data' | 'target' | 'extra';

export type RefineryGas = {
  formula: string;
  name: string;
  sensor: string; // sensor MQ di larik GLD yang peka terhadap gas ini (menurut datasheet)
  status: GasStatus;
};

export const REFINERY_GASES: RefineryGas[] = [
  {formula: 'LPG', name: 'Propana/butana', sensor: 'MQ5 · MQ6 · MQ2', status: 'validated'},
  {formula: 'H₂', name: 'Hidrogen', sensor: 'MQ8', status: 'validated'},
  {formula: 'CO₂', name: 'Karbon dioksida', sensor: 'MQ135', status: 'data'},
  {formula: 'CH₄', name: 'Metana', sensor: 'MQ4', status: 'target'},
  {formula: 'CO', name: 'Karbon monoksida', sensor: 'MQ7', status: 'target'},
  {formula: 'NH₃', name: 'Amonia', sensor: 'MQ135', status: 'target'},
  {formula: 'C₆H₆', name: 'Benzena', sensor: 'MQ135', status: 'target'},
  // Belum ada sensor khusus H2S (mis. seri MQ136/elektrokimia) di larik 8 sensor saat ini.
  {formula: 'H₂S', name: 'Hidrogen sulfida', sensor: 'belum ada sensor khusus', status: 'extra'},
];

export const STATUS_LABEL: Record<GasStatus, string> = {
  validated: 'Dikenali model',
  data: 'Data chamber terkumpul',
  target: 'Target pelatihan di kilang',
  extra: 'Perlu sensor tambahan',
};
