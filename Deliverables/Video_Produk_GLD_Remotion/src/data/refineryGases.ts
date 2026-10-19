// Gas yang umum dijumpai di kilang, beserta status kemampuan GLD saat ini.
// Status harus jujur: hanya 'validated' yang boleh disebut "dikenali model".
export type GasStatus = 'validated' | 'data' | 'target' | 'extra';

export type RefineryGas = {
  formula: string;
  name: string;
  // Kanal sensor yang peka terhadap gas ini, ditulis sebagai spesifikasi (tanpa nama/seri produk).
  // Pemetaan internal (datasheet): LPG=MQ5/MQ6/MQ2, H₂=MQ8, CO₂/NH₃/benzena=MQ135, CH₄=MQ4, CO=MQ7.
  sensor: string;
  nameEn: string;
  sensorEn: string;
  status: GasStatus;
};

export const REFINERY_GASES: RefineryGas[] = [
  {formula: 'LPG', name: 'Propana/butana', sensor: 'tiga kanal sensitif LPG', nameEn: 'Propane/butane', sensorEn: 'three LPG-sensitive channels', status: 'validated'},
  {formula: 'H₂', name: 'Hidrogen', sensor: 'kanal spesifik hidrogen', nameEn: 'Hydrogen', sensorEn: 'hydrogen-specific channel', status: 'validated'},
  {formula: 'CO₂', name: 'Karbon dioksida', sensor: 'kanal kualitas udara', nameEn: 'Carbon dioxide', sensorEn: 'air-quality channel', status: 'data'},
  {formula: 'CH₄', name: 'Metana', sensor: 'kanal spesifik metana', nameEn: 'Methane', sensorEn: 'methane-specific channel', status: 'target'},
  {formula: 'CO', name: 'Karbon monoksida', sensor: 'kanal spesifik CO', nameEn: 'Carbon monoxide', sensorEn: 'CO-specific channel', status: 'target'},
  {formula: 'NH₃', name: 'Amonia', sensor: 'kanal kualitas udara', nameEn: 'Ammonia', sensorEn: 'air-quality channel', status: 'target'},
  {formula: 'C₆H₆', name: 'Benzena', sensor: 'kanal kualitas udara', nameEn: 'Benzene', sensorEn: 'air-quality channel', status: 'target'},
  // Belum ada sensor khusus H2S (mis. sel elektrokimia) di rangkaian 8 sensor saat ini.
  {formula: 'H₂S', name: 'Hidrogen sulfida', sensor: 'kanal spesifik belum tersedia', nameEn: 'Hydrogen sulfide', sensorEn: 'no specific channel yet', status: 'extra'},
];

export const STATUS_LABEL_EN: Record<GasStatus, string> = {
  validated: 'Classified by the model',
  data: 'Chamber data available',
  target: 'On-site training target',
  extra: 'Requires an additional sensor',
};

export const STATUS_LABEL: Record<GasStatus, string> = {
  validated: 'Terklasifikasi oleh model',
  data: 'Data chamber tersedia',
  target: 'Sasaran pelatihan di kilang',
  extra: 'Memerlukan sensor tambahan',
};
