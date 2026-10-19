import React from 'react';
import {AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {ASSETS} from '../assets';
import {AssetSlot} from '../components/AssetSlot';
import {Caption} from '../components/Caption';
import {SceneFrame} from '../components/SceneFrame';
import {Sfx} from '../components/Sfx';
import {useT} from '../i18n';
import {useLayout} from '../layout';
import {progress, useNarration} from '../motion';
import {COLORS} from '../theme';
import {ConceptBadge, InfoCard, SceneTitle} from './common';

// 01 — Pembuka: b-roll kilang malam + judul.
export const OgiHook: React.FC = () => {
  const frame = useCurrentFrame();
  const {portrait, padX, title} = useLayout();
  const t = useT();
  const at = useNarration('ogi_hook');
  const t2 = at(['Kebocoran', 'Hydrocarbon']);
  return (
    <SceneFrame theme="night">
      <AssetSlot asset={ASSETS.refinery} kind="video" />
      <AbsoluteFill style={{background: 'linear-gradient(90deg, rgba(10,18,32,0.88) 0%, rgba(10,18,32,0.35) 60%, rgba(10,18,32,0.1))'}} />
      <AbsoluteFill style={{padding: portrait ? `0 ${padX}px` : `0 ${padX}px`, justifyContent: 'center'}}>
        <div style={{fontSize: 24, fontWeight: 800, letterSpacing: 4, color: COLORS.blueLight, opacity: progress(frame, 6, 16)}}>GLD NEXT</div>
        <Caption text="Optical Gas Imaging" from={10} size={title(96)} color="#F2F5FA" style={{marginTop: 6}} />
        <Caption text="Mid-Wave Infrared (MWIR)" from={22} size={title(44)} color={COLORS.gas} weight={600} style={{marginTop: 8}} />
        <div style={{height: 4, width: 220 * progress(frame, 30, 20), background: COLORS.gas, marginTop: 26, borderRadius: 2}} />
        <Caption
          text={t('Kebocoran hidrokarbon tidak kasatmata.', 'Hydrocarbon leaks are invisible.')}
          from={t2}
          size={title(40)}
          color="#E3E8F0"
          weight={600}
          style={{marginTop: 26, maxWidth: 900}}
        />
      </AbsoluteFill>
      <ConceptBadge />
      <Sfx name="rise" at={0} volume={0.3} />
    </SceneFrame>
  );
};

// 02 — Mengapa penting: tiga risiko + perbandingan GWP metana (IPCC AR6).
const RiskIcon: React.FC<{kind: string; color: string}> = ({kind, color}) => {
  const s = {fill: 'none', stroke: color, strokeWidth: 4, strokeLinecap: 'round' as const, strokeLinejoin: 'round' as const};
  return (
    <svg width={64} height={64} viewBox="0 0 64 64">
      {kind === 'safety' && <path {...s} d="M32 6 L54 14 V30 C54 44 44 54 32 58 C20 54 10 44 10 30 V14 Z M22 32 L29 39 L42 25" />}
      {kind === 'ops' && (
        <g {...s}>
          <circle cx={32} cy={32} r={10} />
          <path d="M32 8 V16 M32 48 V56 M8 32 H16 M48 32 H56 M15 15 L21 21 M43 43 L49 49 M15 49 L21 43 M43 21 L49 15" />
        </g>
      )}
      {kind === 'emis' && <path {...s} d="M14 50 C14 28 30 12 52 12 C52 34 36 50 14 50 Z M14 50 L36 28" />}
    </svg>
  );
};

export const OgiStakes: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const {portrait, padX} = useLayout();
  const t = useT();
  const at = useNarration('ogi_stakes');
  const RISKS = [
    {kind: 'safety', k: t('Keselamatan', 'Safety'), v: t('Pekerja dan aset', 'People and assets'), c: COLORS.alarm, at: at(['keselamatan', 'the safety'])},
    {kind: 'ops', k: t('Keberlangsungan operasi', 'Operational continuity'), v: t('Unit tetap beroperasi', 'Units keep running'), c: COLORS.blue, at: at(['keberlangsungan', 'operational'])},
    {kind: 'emis', k: t('Emisi', 'Emissions'), v: t('Emisi fugitif & ESG', 'Fugitive emissions & ESG'), c: COLORS.ok, at: at(['serta emisi', 'and emissions'])},
  ];
  const gwpAt = at(['Metana', 'Methane']);
  const g = progress(frame, gwpAt + 10, 40);
  const barW = portrait ? 640 : 1100;
  return (
    <SceneFrame theme="light">
      <SceneTitle kicker={t('MENGAPA PENTING', 'WHY IT MATTERS')} title={t('Satu kebocoran, tiga risiko', 'One leak, three risks')} />
      <div style={{position: 'absolute', left: padX, right: padX, top: portrait ? 420 : 240, display: 'grid', gridTemplateColumns: portrait ? '1fr' : '1fr 1fr 1fr', gap: 24}}>
        {RISKS.map((r) => {
          const p = spring({frame: frame - r.at, fps, config: {damping: 16}});
          return (
            <div
              key={r.kind}
              style={{
                opacity: p,
                transform: `translateY(${24 * (1 - p)}px)`,
                display: 'flex',
                gap: 20,
                alignItems: 'center',
                padding: '28px 28px',
                borderRadius: 16,
                backgroundColor: COLORS.surface,
                border: `1px solid ${COLORS.line}`,
                borderTop: `6px solid ${r.c}`,
                boxShadow: '0 8px 24px rgba(20,33,58,0.10)',
              }}
            >
              <RiskIcon kind={r.kind} color={r.c} />
              <div>
                <div style={{fontSize: 30, fontWeight: 800}}>{r.k}</div>
                <div style={{fontSize: 22, color: COLORS.muted, marginTop: 2}}>{r.v}</div>
              </div>
            </div>
          );
        })}
      </div>
      {/* GWP100: CO2 = 1, CH4 fosil = 29,8 (IPCC AR6) */}
      <div style={{position: 'absolute', left: padX, top: portrait ? 900 : 420, width: barW + 300, opacity: progress(frame, gwpAt, 14)}}>
        <div style={{fontSize: 32, fontWeight: 800, marginBottom: 22}}>
          {t('Potensi pemanasan global (100 tahun)', 'Global warming potential (100-year)')}
        </div>
        {[
          {k: 'CO₂', v: 1, c: COLORS.muted},
          {k: t('CH₄ (metana)', 'CH₄ (methane)'), v: 29.8, c: COLORS.gas},
        ].map((b) => (
          <div key={b.k} style={{display: 'flex', alignItems: 'center', gap: 18, marginBottom: 16}}>
            <div style={{width: 200, fontSize: 28, fontWeight: 700}}>{b.k}</div>
            <div style={{height: 48, width: Math.max(8, (b.v / 29.8) * barW * g), backgroundColor: b.c, borderRadius: 6}} />
            <div style={{fontSize: 36, fontWeight: 800}}>{b.v === 1 ? '1×' : `≈${(1 + (b.v - 1) * g).toFixed(0)}×`}</div>
          </div>
        ))}
        <div style={{fontSize: 18, color: COLORS.muted, marginTop: 6}}>{t('Sumber: IPCC AR6 (2021), GWP100 metana fosil ≈ 29,8', 'Source: IPCC AR6 (2021), fossil methane GWP100 ≈ 29.8')}</div>
      </div>
      <ConceptBadge />
      {RISKS.map((r) => (
        <Sfx key={r.kind} name="pop" at={r.at} volume={0.22} />
      ))}
    </SceneFrame>
  );
};

// 03 — GLD hari ini: peta titik sensor dengan radius deteksi; plume lewat celah antar-sensor.
export const OgiToday: React.FC = () => {
  const frame = useCurrentFrame();
  const {portrait, padX, width} = useLayout();
  const t = useT();
  const at = useNarration('ogi_today');
  const gapAt = at(['Namun', 'However']);
  const map = portrait ? {x: padX, y: 820, w: width - padX * 2, h: 680} : {x: 900, y: 220, w: 900, h: 640};
  const S = map.w / 900;
  const NODES = [
    [180, 160],
    [520, 130],
    [300, 430],
    [700, 420],
  ];
  const plumeP = progress(frame, gapAt, 140);
  const px = 60 + plumeP * 700;
  const py = 300 - plumeP * 40;
  const CHECKS = [
    {k: 'Edge AI', v: t('Identifikasi jenis gas di perangkat', 'Gas identification on the device'), at: at(['mengenali', 'it identifies'])},
    {k: 'Private mesh LoRa', v: t('Alarm tanpa kabel data', 'Alarms without data cables'), at: at(['mengirim alarm', 'sends alarms'])},
    {k: t('Sensor titik', 'Point sensor'), v: t('Hanya gas yang mencapai sensor', 'Only gas that reaches the sensor'), at: gapAt + 30, warn: true},
  ];
  return (
    <SceneFrame theme="light">
      <SceneTitle kicker={t('GLD HARI INI', 'GLD TODAY')} title={t('Deteksi titik berbasis edge AI', 'Point detection powered by edge AI')} />
      <div style={{position: 'absolute', left: padX, top: portrait ? 400 : 260, width: portrait ? width - padX * 2 : 700, display: 'flex', flexDirection: 'column', gap: 16}}>
        {CHECKS.map((c) => (
          <InfoCard key={c.k} at={c.at} k={c.k} v={c.v} color={c.warn ? COLORS.gas : COLORS.ok} />
        ))}
      </div>
      <div style={{position: 'absolute', left: map.x, top: map.y, width: map.w, height: map.h, borderRadius: 18, overflow: 'hidden', backgroundColor: COLORS.surface, border: `1px solid ${COLORS.line}`}}>
        <svg width={map.w} height={map.h} viewBox="0 0 900 640">
          {[120, 260, 400, 540].map((y) => (
            <rect key={y} x={40} y={y} width={820} height={12} rx={6} fill={COLORS.line} />
          ))}
          {NODES.map(([x, y], i) => {
            const p = progress(frame, 6 + i * 6, 18);
            return (
              <g key={i}>
                <circle cx={x} cy={y} r={95 * p} fill={COLORS.blue} fillOpacity={0.08} stroke={COLORS.blue} strokeOpacity={0.4} strokeDasharray="6 6" strokeWidth={2} />
                <circle cx={x} cy={y} r={14 * p} fill={COLORS.blue} />
              </g>
            );
          })}
          {/* plume terbawa angin melewati celah */}
          <g opacity={progress(frame, gapAt, 12) * (1 - progress(frame, gapAt + 160, 20))}>
            {[0, 1, 2, 3, 4].map((k) => (
              <circle key={k} cx={px - k * 38} cy={py + Math.sin((frame + k * 9) / 9) * 10} r={34 - k * 4} fill={COLORS.gas} fillOpacity={0.22} />
            ))}
          </g>
          <g opacity={progress(frame, gapAt + 40, 14)}>
            <path d="M 60 600 L 200 600" stroke={COLORS.muted} strokeWidth={4} markerEnd="url(#arr)" />
            <text x={60} y={588} fontSize={22} fill={COLORS.muted} fontWeight={700}>
              {t('Angin', 'Wind')}
            </text>
            <rect x={470} y={250} width={260} height={46} rx={10} fill={COLORS.gas} />
            <text x={600} y={281} fontSize={24} fontWeight={800} textAnchor="middle" fill="#14213A">
              {t('Tidak terpantau', 'Not monitored')}
            </text>
          </g>
          <defs>
            <marker id="arr" markerWidth={10} markerHeight={10} refX={6} refY={5} orient="auto">
              <path d="M0 0 L10 5 L0 10 Z" fill={COLORS.muted} />
            </marker>
          </defs>
        </svg>
        <div style={{position: 'absolute', left: 18, top: 12, fontSize: 20 * Math.min(1, S + 0.2), color: COLORS.muted}}>
          <span style={{color: COLORS.blue, fontWeight: 800}}>●</span> {t('GLD + radius deteksi', 'GLD + detection radius')}
        </div>
      </div>
      <ConceptBadge />
      <Sfx name="error" at={gapAt + 40} volume={0.15} />
    </SceneFrame>
  );
};

// 04 — Prinsip fisika: spektrum -> pita MWIR -> serapan C–H di 3,3 µm -> filter bandpass -> plume tampak.
export const OgiPhysics: React.FC = () => {
  const frame = useCurrentFrame();
  const {portrait, padX, width} = useLayout();
  const t = useT();
  const at = useNarration('ogi_physics');
  const tBond = at(['ikatan karbon', 'the carbon-hydrogen']);
  const tBand = at(['Mid-Wave', 'Mid-Wave']);
  const tFilter = at(['Dengan filter', 'With a narrow']);
  const W = width - padX * 2;
  const chartH = portrait ? 520 : 470;
  const top = portrait ? 430 : 230;
  // sumbu x: 2..14 µm
  const xOf = (um: number) => ((um - 2) / 12) * W;
  const zoom = progress(frame, tBand - 10, 30);
  const curve = progress(frame, tBond, 40);
  const filt = progress(frame, tFilter, 24);
  // kurva serapan ilustratif (C–H stretch kuat di ~3,3 µm, pita lebih lemah ~6,8 µm)
  const pts: string[] = [];
  for (let i = 0; i <= 240 * curve; i++) {
    const um = 2 + (i / 240) * 12;
    const a = 0.95 * Math.exp(-(((um - 3.31) / 0.11) ** 2)) + 0.25 * Math.exp(-(((um - 6.85) / 0.25) ** 2)) + 0.12 * Math.exp(-(((um - 7.7) / 0.2) ** 2));
    pts.push(`${xOf(um)},${chartH - 40 - a * (chartH - 110)}`);
  }
  const bands = [
    {a: 2, b: 3, k: 'SWIR', c: 'rgba(242,245,250,0.06)'},
    {a: 3, b: 5, k: 'MWIR', c: 'rgba(91,155,255,0.20)'},
    {a: 5, b: 8, k: '', c: 'rgba(242,245,250,0.03)'},
    {a: 8, b: 14, k: 'LWIR', c: 'rgba(242,245,250,0.06)'},
  ];
  return (
    <SceneFrame theme="night">
      <SceneTitle kicker={t('PRINSIP FISIKA', 'PHYSICAL PRINCIPLE')} title={t('Ikatan C–H menyerap inframerah di ±3,3 µm', 'C–H bonds absorb infrared at ≈3.3 µm')} />
      <div style={{position: 'absolute', left: padX, top, width: W, height: chartH}}>
        <svg width={W} height={chartH}>
          {bands.map((b) => (
            <g key={b.a}>
              <rect x={xOf(b.a)} y={20} width={xOf(b.b) - xOf(b.a)} height={chartH - 60} fill={b.k === 'MWIR' ? `rgba(91,155,255,${0.08 + 0.17 * zoom})` : b.c} />
              {b.k && (
                <text x={(xOf(b.a) + xOf(b.b)) / 2} y={48} textAnchor="middle" fontSize={24} fontWeight={800} fill={b.k === 'MWIR' ? COLORS.blueLight : COLORS.muted}>
                  {b.k}
                </text>
              )}
            </g>
          ))}
          {/* filter bandpass 3,2–3,4 µm */}
          <rect x={xOf(3.2)} y={20} width={(xOf(3.42) - xOf(3.2))} height={(chartH - 60) * filt} fill={COLORS.gas} fillOpacity={0.35} />
          <polyline points={pts.join(' ')} fill="none" stroke={COLORS.gas} strokeWidth={5} strokeLinejoin="round" />
          <line x1={0} y1={chartH - 40} x2={W} y2={chartH - 40} stroke={COLORS.muted} strokeWidth={2} />
          {[2, 3, 4, 5, 6, 8, 10, 12, 14].map((u) => (
            <text key={u} x={xOf(u)} y={chartH - 10} textAnchor="middle" fontSize={20} fill={COLORS.muted}>
              {u}
            </text>
          ))}
          <text x={W} y={chartH - 46} textAnchor="end" fontSize={20} fill={COLORS.muted}>
            {t('panjang gelombang (µm)', 'wavelength (µm)')}
          </text>
          <g opacity={progress(frame, tBond + 30, 16)}>
            <line x1={xOf(3.31)} y1={78} x2={xOf(3.31) + 120} y2={110} stroke="#F2F5FA" strokeWidth={2} />
            <text x={xOf(3.31) + 128} y={116} fontSize={24} fontWeight={800} fill="#F2F5FA">
              {t('Serapan C–H ≈ 3,3 µm', 'C–H absorption ≈ 3.3 µm')}
            </text>
          </g>
          <g opacity={filt}>
            <text x={xOf(3.42) + 12} y={chartH - 80} fontSize={22} fontWeight={700} fill={COLORS.gas}>
              {t('Filter spektral sempit', 'Narrow spectral filter')}
            </text>
          </g>
        </svg>
        <div style={{fontSize: 17, color: COLORS.muted, marginTop: 6}}>
          {t('Kurva serapan ilustratif hidrokarbon (bukan data ukur).', 'Illustrative hydrocarbon absorption curve (not measured data).')}
        </div>
      </div>
      <Sfx name="whoosh_short" at={tBand - 10} volume={0.25} />
      <Sfx name="blip" at={tFilter} volume={0.25} />
      <ConceptBadge />
    </SceneFrame>
  );
};

// 05 — Detektor berpendingin: suhu turun ke 77 K; derau vs sinyal.
export const OgiCooled: React.FC = () => {
  const frame = useCurrentFrame();
  const {portrait, padX, width} = useLayout();
  const t = useT();
  const at = useNarration('ogi_cooled');
  const tCool = at(['didinginkan', 'is cooled']);
  const tNoise = at(['Derau', 'The thermal noise']);
  const cool = progress(frame, tCool, 60);
  const temp = Math.round(interpolate(cool, [0, 1], [25, -196]));
  const W = portrait ? width - padX * 2 : 820;
  const H = 300;
  const noiseAmp = interpolate(progress(frame, tNoise, 40), [0, 1], [70, 9]);
  const wave = (amp: number) => {
    const p: string[] = [];
    for (let i = 0; i <= 200; i++) {
      const x = (i / 200) * W;
      const sig = 55 * Math.exp(-(((i - 120) / 14) ** 2));
      const n = amp * (Math.sin(i * 1.7 + frame * 0.6) * 0.5 + Math.sin(i * 3.1 - frame * 0.9) * 0.3 + Math.sin(i * 5.3 + frame) * 0.2);
      p.push(`${x},${H / 2 + 40 - sig - n * 0.6}`);
    }
    return p.join(' ');
  };
  return (
    <SceneFrame theme="night">
      <SceneTitle kicker={t('DETEKTOR', 'DETECTOR')} title={t('Didinginkan hingga ≈ −196 °C (77 K)', 'Cooled to ≈ −196 °C (77 K)')} />
      {/* diagram detektor: chip FPA dalam dewar + cooler Stirling */}
      <div style={{position: 'absolute', left: padX, top: portrait ? 420 : 250, width: portrait ? W : 760}}>
        <svg width={portrait ? W : 760} height={360} viewBox="0 0 760 360">
          <rect x={40} y={60} width={300} height={220} rx={24} fill="#111C2E" stroke={COLORS.line} strokeWidth={3} />
          <text x={190} y={46} textAnchor="middle" fontSize={22} fill={COLORS.muted} fontWeight={700}>
            {t('Dewar vakum', 'Vacuum dewar')}
          </text>
          {Array.from({length: 8}).map((_, r) =>
            Array.from({length: 10}).map((__, c) => (
              <rect key={`${r}-${c}`} x={110 + c * 16} y={110 + r * 16} width={13} height={13} fill={COLORS.blueLight} fillOpacity={0.25 + 0.55 * cool * ((r + c) % 3 ? 1 : 0.7)} />
            )),
          )}
          <text x={190} y={262} textAnchor="middle" fontSize={20} fill="#F2F5FA" fontWeight={700}>
            MCT 640×512
          </text>
          <rect x={360} y={120} width={200} height={100} rx={14} fill="#1B2A44" stroke={COLORS.line} strokeWidth={3} />
          <text x={460} y={176} textAnchor="middle" fontSize={22} fill="#F2F5FA" fontWeight={700}>
            {t('Cooler Stirling', 'Stirling cooler')}
          </text>
          <line x1={340} y1={170} x2={360} y2={170} stroke={COLORS.blueLight} strokeWidth={6} />
          {/* termometer */}
          <rect x={620} y={44} width={40} height={246} rx={20} fill="#111C2E" stroke={COLORS.line} strokeWidth={3} />
          <rect x={628} y={48 + 234 * cool} width={24} height={234 * (1 - cool) + 6} rx={12} fill={cool > 0.9 ? COLORS.blueLight : COLORS.gas} />
          <circle cx={640} cy={300} r={30} fill={cool > 0.9 ? COLORS.blueLight : COLORS.gas} />
          <text x={640} y={30} textAnchor="middle" fontSize={28} fill="#F2F5FA" fontWeight={800}>
            {temp}°C
          </text>
        </svg>
      </div>
      {/* derau vs sinyal */}
      <div style={{position: 'absolute', left: portrait ? padX : 1000, top: portrait ? 860 : 280, width: W, opacity: progress(frame, tNoise - 6, 16)}}>
        <div style={{fontSize: 24, fontWeight: 800, color: '#F2F5FA', marginBottom: 6}}>{t('Sinyal gas vs derau termal', 'Gas signal vs thermal noise')}</div>
        <svg width={W} height={H}>
          <rect width={W} height={H} rx={14} fill="#111C2E" />
          <polyline points={wave(noiseAmp)} fill="none" stroke={COLORS.gas} strokeWidth={3} />
          <text x={W * 0.6} y={40} fontSize={20} fill={COLORS.muted}>
            {t('sinyal plume', 'plume signal')}
          </text>
        </svg>
        <div style={{display: 'flex', gap: 16, marginTop: 14}}>
          <InfoCard at={tNoise + 30} k="NETD" v={t('≤ 25 mK (spesifikasi opsi kamera)', '≤ 25 mK (camera option spec)')} color={COLORS.blueLight} style={{flex: 1, backgroundColor: '#111C2E', color: '#F2F5FA'}} />
        </div>
      </div>
      <Sfx name="hum" at={tCool} volume={0.2} />
      <ConceptBadge />
    </SceneFrame>
  );
};
