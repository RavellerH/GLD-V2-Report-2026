// Gas yang umum dijumpai di kilang, beserta status kemampuan GLD saat ini.
// Status harus jujur: hanya 'validated' yang boleh disebut "dikenali model".
export type GasStatus = 'validated' | 'data' | 'target' | 'extra';

export type RefineryGas = {
  formula: string;
  name: string;
  // Kanal sensor yang peka terhadap gas ini, ditulis sebagai spesifikasi (tanpa nama/seri produk).
  // Pemetaan internal (datasheet): LPG=MQ5/MQ6/MQ2, H₂=MQ8, CO₂/NH₃/benzena=MQ135, CH₄=MQ4, CO=MQ7.
  sensor: string;
  status: GasStatus;
};

export const REFINERY_GASES: RefineryGas[] = [
  {formula: 'LPG', name: 'Propana/butana', sensor: 'tiga kanal sensitif LPG', status: 'validated'},
  {formula: 'H₂', name: 'Hidrogen', sensor: 'kanal spesifik hidrogen', status: 'validated'},
  {formula: 'CO₂', name: 'Karbon dioksida', sensor: 'kanal kualitas udara', status: 'data'},
  {formula: 'CH₄', name: 'Metana', sensor: 'kanal spesifik metana', status: 'target'},
  {formula: 'CO', name: 'Karbon monoksida', sensor: 'kanal spesifik CO', status: 'target'},
  {formula: 'NH₃', name: 'Amonia', sensor: 'kanal kualitas udara', status: 'target'},
  {formula: 'C₆H₆', name: 'Benzena', sensor: 'kanal kualitas udara', status: 'target'},
  // Belum ada sensor khusus H2S (mis. sel elektrokimia) di larik 8 sensor saat ini.
  {formula: 'H₂S', name: 'Hidrogen sulfida', sensor: 'kanal spesifik belum tersedia', status: 'extra'},
];

export const STATUS_LABEL: Record<GasStatus, string> = {
  validated: 'Terklasifikasi oleh model',
  data: 'Data chamber tersedia',
  target: 'Sasaran pelatihan di kilang',
  extra: 'Memerlukan sensor tambahan',
};
