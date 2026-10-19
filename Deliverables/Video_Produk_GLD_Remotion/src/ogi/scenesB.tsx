import React from 'react';
import {AbsoluteFill, Img, OffthreadVideo, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {ASSETS} from '../assets';
import {AssetSlot} from '../components/AssetSlot';
import {Caption} from '../components/Caption';
import {SceneFrame} from '../components/SceneFrame';
import {Sfx} from '../components/Sfx';
import {useT} from '../i18n';
import {useLayout} from '../layout';
import {progress, useNarration} from '../motion';
import {COLORS, FONT, PALETTES, themeVars} from '../theme';
import {InfoCard, SceneTitle} from './common';

// 06 — Sistem di lapangan: render 3D (14 dtk) diperlambat mengisi slot + kartu spesifikasi + HUD preset.
const OGI_3D_SEC = 14;
export const OgiField: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps, durationInFrames} = useVideoConfig();
  const {portrait, padX} = useLayout();
  const t = useT();
  const rate = OGI_3D_SEC / ((durationInFrames + 18) / fps);
  const at3d = (s: number) => Math.round((s / rate) * fps); // detik render 3D -> frame adegan
  const PRESETS = [
    {k: t('Preset 1 · Jalur pipa', 'Preset 1 · Pipe run'), a: at3d(0.6), b: at3d(4.0)},
    {k: t('Preset 2 · Manifold', 'Preset 2 · Manifold'), a: at3d(5.2), b: at3d(7.5)},
    {k: t('Preset 3 · Klaster valve', 'Preset 3 · Valve cluster'), a: at3d(8.8), b: durationInFrames + 20},
  ];
  const det = at3d(10.6);
  const SPECS = [
    {k: t('Pita spektral', 'Spectral band'), v: t('MWIR 3–5 µm · filter ≈3,3 µm', 'MWIR 3–5 µm · ≈3.3 µm filter')},
    {k: t('Detektor', 'Detector'), v: 'Cooled MCT 640×512'},
    {k: 'Frame rate · NETD', v: '100 Hz · ≤25 mK'},
    {k: t('Pemasangan', 'Mounting'), v: t('Tiang ≈10 m · pan-tilt ±60°', '≈10 m pole · pan-tilt ±60°')},
    {k: t('Target jangkauan', 'Target range'), v: t('≈100 m (divalidasi uji lapangan)', '≈100 m (to be field-validated)')},
  ];
  return (
    <SceneFrame theme="night">
      <AbsoluteFill>
        <OffthreadVideo
          src={staticFile(portrait ? 'blender/portrait/ogi_field.mp4' : 'blender/ogi_field.mp4')}
          playbackRate={rate}
          muted
          style={{width: '100%', height: '100%', objectFit: 'cover'}}
        />
      </AbsoluteFill>
      <AbsoluteFill style={{background: portrait ? 'linear-gradient(rgba(10,18,32,0.75), transparent 30%, transparent 55%, rgba(10,18,32,0.85))' : 'linear-gradient(90deg, transparent 55%, rgba(10,18,32,0.85))'}} />
      <SceneTitle kicker={t('SISTEM DI LAPANGAN', 'FIELD SYSTEM')} title={t('Patroli preset pada sektor kritis', 'Preset patrol over critical sectors')} color="#F2F5FA" from={at3d(3.6)} />
      {/* HUD preset */}
      <div style={{position: 'absolute', left: padX, top: portrait ? 470 : 230, display: 'flex', flexDirection: 'column', gap: 10}}>
        {PRESETS.map((p, i) => {
          const on = frame >= p.a && frame < p.b;
          const seen = frame >= p.a;
          const isDet = i === 2 && frame >= det;
          return (
            <div
              key={p.k}
              style={{
                opacity: seen ? (on ? 1 : 0.5) : 0,
                padding: '8px 16px',
                borderRadius: 10,
                fontSize: 24,
                fontWeight: 700,
                color: '#F2F5FA',
                backgroundColor: isDet ? 'rgba(245,165,36,0.85)' : on ? 'rgba(43,95,203,0.85)' : 'rgba(10,18,32,0.6)',
                border: `2px solid ${isDet ? COLORS.gas : '#5B9BFF'}`,
              }}
            >
              {p.k}
              {isDet && ` — ${t('plume terdeteksi', 'plume detected')}`}
            </div>
          );
        })}
      </div>
      <div style={{position: 'absolute', right: portrait ? padX : 60, left: portrait ? padX : undefined, top: portrait ? 1180 : 250, width: portrait ? undefined : 560, display: 'grid', gridTemplateColumns: portrait ? '1fr 1fr' : '1fr', gap: 12}}>
        {SPECS.map((s, i) => (
          <InfoCard key={s.k} at={at3d(5) + i * 10} k={s.k} v={s.v} color={i === 4 ? COLORS.gas : '#5B9BFF'} style={{backgroundColor: 'rgba(17,28,46,0.88)', color: '#F2F5FA', border: '1px solid #26354D'}} />
        ))}
      </div>
      <div style={{position: 'absolute', left: padX, top: portrait ? 1110 : 900, fontSize: 18, color: '#C9D2E0', opacity: progress(frame, at3d(5), 20)}}>
        {t('Spesifikasi: opsi kamera dalam proposal (belum final) · animasi ilustrasi', 'Specs: camera option in the proposal (not final) · illustrative animation')}
      </div>
      {PRESETS.map((p) => (
        <Sfx key={p.k} name="tick" at={p.a} volume={0.25} />
      ))}
      <Sfx name="alarm" at={det} volume={0.18} />
    </SceneFrame>
  );
};

// 07 — Edge AI: segmentasi plume + logika persistensi multi-frame.
const CLIP_RATE = 0.55; // klip 10 dtk diperlambat agar mengisi adegan
export const OgiEdgeAI: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const {portrait, padX, width} = useLayout();
  const t = useT();
  const at = useNarration('ogi_edgeai');
  const tSeg = at(['segmentasi', 'segments']);
  const tPers = at(['Alarm hanya', 'An alarm']);
  const tFlare = at(['flare', 'flares']);
  const panel = portrait ? {x: padX, y: 400, w: width - padX * 2, h: 540} : {x: padX, y: 230, w: 980, h: 552};
  const segP = progress(frame, tSeg, 20);
  // 10 frame berurutan: frame 2 = gangguan sesaat (diabaikan), frame 5–10 = plume konsisten -> alarm
  const N = 10;
  const step = 9;
  const stripAt = tPers;
  const shown = Math.max(0, Math.min(N, Math.floor((frame - stripAt) / step) + 1));
  const DET = [false, true, false, false, true, true, true, true, true, true];
  const alarmAt = stripAt + step * 7;
  // mask mengikuti plume pada klip (posisi diukur dari frame klip: t=1,25 / 5 / 8,3 dtk)
  const tc = (frame / fps) * CLIP_RATE;
  const lerp3 = (a: number[]) => interpolate(tc, [1.25, 5, 8.3], a, {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const cx = lerp3([0.75, 0.75, 0.74]) * 980;
  const cy = lerp3([0.52, 0.47, 0.38]) * 552;
  const sc = lerp3([0.8, 1.1, 1.55]);
  const rw = 95 * sc;
  const rh = 42 * sc;
  const wob = (k: number) => Math.sin(frame / 10 + k) * 6;
  const blob = `M ${cx - rw} ${cy + rh * 0.6} C ${cx - rw * 0.8} ${cy - rh + wob(1)}, ${cx - rw * 0.1} ${cy - rh * 1.3 + wob(2)}, ${cx + rw * 0.5} ${cy - rh + wob(3)} C ${cx + rw * 1.1} ${cy - rh * 0.6}, ${cx + rw * 1.05} ${cy + rh * 0.5 + wob(4)}, ${cx + rw * 0.4} ${cy + rh * 0.8} C ${cx - rw * 0.2} ${cy + rh * 1.1 + wob(5)}, ${cx - rw * 0.9} ${cy + rh}, ${cx - rw} ${cy + rh * 0.6} Z`;
  const bx = cx - rw * 1.1;
  const by = cy - rh * 1.45;
  const bw = rw * 2.25;
  const bh = rh * 2.7;
  return (
    <SceneFrame theme="night">
      <SceneTitle kicker="EDGE AI" title={t('Segmentasi plume otomatis di edge server', 'Automatic plume segmentation on the edge server')} />
      <div style={{position: 'absolute', left: panel.x, top: panel.y, width: panel.w, height: panel.h, borderRadius: 16, overflow: 'hidden', border: '1px solid #26354D'}}>
        <OffthreadVideo src={staticFile(ASSETS.thermal.path)} playbackRate={CLIP_RATE} muted style={{width: '100%', height: '100%', objectFit: 'cover', filter: 'grayscale(1) contrast(1.15)'}} />
        <svg width={panel.w} height={panel.h} viewBox="0 0 980 552" preserveAspectRatio="xMidYMid slice" style={{position: 'absolute', inset: 0}}>
          <path d={blob} fill={COLORS.gas} fillOpacity={0.38 * segP} stroke={COLORS.gas} strokeWidth={3} strokeOpacity={segP} />
          <rect x={bx} y={by} width={bw} height={bh} fill="none" stroke="#5B9BFF" strokeWidth={3} strokeDasharray="10 6" opacity={segP} />
          <g opacity={segP}>
            <rect x={bx} y={by - 36} width={210} height={34} fill="#5B9BFF" />
            <text x={bx + 10} y={by - 12} fontSize={22} fontWeight={800} fill="#0A1220">
              plume · {(0.6 + 0.3 * progress(frame, tSeg, 60)).toFixed(2)}
            </text>
          </g>
        </svg>
        <div style={{position: 'absolute', right: 14, top: 12, padding: '4px 12px', borderRadius: 8, backgroundColor: 'rgba(10,18,32,0.7)', fontSize: 18, color: '#E3E8F0'}}>
          {t('Ilustrasi konsep — bukan rekaman produk', 'Concept illustration — not product footage')}
        </div>
      </div>
      {/* strip frame + logika persistensi */}
      <div style={{position: 'absolute', left: portrait ? padX : 1140, top: portrait ? 990 : 250, width: portrait ? width - padX * 2 : 660, opacity: progress(frame, stripAt - 8, 14)}}>
        <div style={{fontSize: 24, fontWeight: 800, color: '#F2F5FA', marginBottom: 14}}>{t('Logika persistensi', 'Persistence logic')}</div>
        <div style={{display: 'grid', gridTemplateColumns: `repeat(${N}, 1fr)`, gap: 8}}>
          {DET.map((d, i) => {
            const vis = i < shown;
            const ignored = i === 1;
            return (
              <div
                key={i}
                style={{
                  height: 62,
                  borderRadius: 8,
                  opacity: vis ? 1 : 0.15,
                  backgroundColor: d ? (ignored ? 'rgba(229,72,77,0.25)' : 'rgba(245,165,36,0.85)') : '#111C2E',
                  border: `2px solid ${d ? (ignored ? COLORS.alarm : COLORS.gas) : '#26354D'}`,
                  color: '#F2F5FA',
                  fontSize: 15,
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  fontWeight: 700,
                }}
              >
                f{i + 1}
              </div>
            );
          })}
        </div>
        <div style={{fontSize: 20, color: '#C9D2E0', marginTop: 10, opacity: progress(frame, Math.max(tFlare, stripAt + step * 2), 14)}}>
          <span style={{color: COLORS.alarm, fontWeight: 800}}>f2</span> {t('gangguan sesaat (flare/pantulan) → diabaikan', 'momentary interference (flare/reflection) → ignored')}
        </div>
        <div
          style={{
            marginTop: 18,
            display: 'inline-block',
            padding: '12px 22px',
            borderRadius: 12,
            backgroundColor: COLORS.alarm,
            color: '#FFFFFF',
            fontSize: 28,
            fontWeight: 800,
            opacity: progress(frame, alarmAt, 8),
          }}
        >
          {t('ALARM: plume konsisten', 'ALARM: consistent plume')}
        </div>
      </div>
      <Sfx name="blip" at={tSeg} volume={0.25} />
      <Sfx name="alarm" at={alarmAt} volume={0.2} />
    </SceneFrame>
  );
};

// 08 — Satu sistem: GLD (apa & seberapa pekat) + OGI (di mana & ke mana) + matriks orkestrasi alarm.
export const OgiFusion: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const {portrait, padX, width} = useLayout();
  const t = useT();
  const at = useNarration('ogi_fusion');
  const tGld = at(['GLD menjawab', 'GLD answers']);
  const tOgi = at(['kamera OGI', 'the OGI camera']);
  const tBoth = at(['Bila keduanya', 'When both']);
  const W = width - padX * 2;
  const ROWS = [
    {g: true, c: false, r: t('Investigasi berbasis sensor', 'Sensor-led investigation'), col: COLORS.blue},
    {g: false, c: true, r: t('Verifikasi sensor terdekat', 'Check nearest sensor'), col: COLORS.blue},
    {g: true, c: true, r: t('Prioritas tertinggi', 'Highest priority'), col: COLORS.alarm},
  ];
  return (
    <SceneFrame theme="light">
      <SceneTitle kicker={t('INTEGRASI', 'INTEGRATION')} title={t('GLD + OGI dalam satu dashboard', 'GLD + OGI in one dashboard')} />
      <div style={{position: 'absolute', left: padX, top: portrait ? 400 : 230, width: W, display: 'grid', gridTemplateColumns: portrait ? '1fr' : '1fr 1fr', gap: 22}}>
        <InfoCard at={tGld} big k={t('GLD · sensor titik', 'GLD · point sensor')} v={t('Gas apa & seberapa pekat', 'Which gas & how concentrated')} color={COLORS.gas} />
        <InfoCard at={tOgi} big k={t('Kamera OGI · area', 'OGI camera · area')} v={t('Di mana & ke arah mana menyebar', 'Where & which way it spreads')} color={COLORS.blue} />
      </div>
      <div style={{position: 'absolute', left: padX, top: portrait ? 760 : 470, width: portrait ? W : 1200}}>
        <div style={{display: 'grid', gridTemplateColumns: '180px 180px 1fr', gap: 10, fontSize: 22, fontWeight: 800, color: COLORS.muted, opacity: progress(frame, tBoth - 30, 14)}}>
          <div>GLD</div>
          <div>OGI</div>
          <div>{t('Respons', 'Response')}</div>
        </div>
        {ROWS.map((r, i) => {
          const a = tBoth - 30 + i * 14;
          const p = spring({frame: frame - a, fps, config: {damping: 200}});
          const hl = i === 2 && frame > tBoth + 20;
          return (
            <div
              key={i}
              style={{
                display: 'grid',
                gridTemplateColumns: '180px 180px 1fr',
                gap: 10,
                alignItems: 'center',
                marginTop: 10,
                padding: '14px 0',
                borderRadius: 12,
                opacity: p,
                transform: `translateX(${20 * (1 - p)}px) scale(${hl ? 1.02 : 1})`,
                backgroundColor: hl ? 'rgba(209,52,56,0.10)' : COLORS.surface,
                border: `2px solid ${hl ? COLORS.alarm : COLORS.line}`,
              }}
            >
              {[r.g, r.c].map((on, k) => (
                <div key={k} style={{paddingLeft: 20, fontSize: 28, fontWeight: 800, color: on ? COLORS.ok : COLORS.muted}}>
                  {on ? '● ' + t('aktif', 'active') : '○ —'}
                </div>
              ))}
              <div style={{fontSize: 28, fontWeight: 800, color: r.col}}>{r.r}</div>
            </div>
          );
        })}
      </div>
      <Sfx name="pop" at={tGld} volume={0.22} />
      <Sfx name="pop" at={tOgi} volume={0.22} />
      <Sfx name="alarm" at={tBoth + 20} volume={0.18} />
    </SceneFrame>
  );
};

// 09 — Batasan: faktor lingkungan + gas yang terlihat/tidak terlihat di pita 3,3 µm.
export const OgiLimits: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const {portrait, padX, width} = useLayout();
  const t = useT();
  const at = useNarration('ogi_limits');
  const tGas = at(['hidrogen,', 'hydrogen,']);
  const tComp = at(['Karena itu', 'The camera therefore']);
  const W = width - padX * 2;
  const FACTORS = [
    {k: t('Kontras termal', 'Thermal contrast'), a: at(['kontras', 'thermal contrast'])},
    {k: t('Angin', 'Wind'), a: at(['angin', 'wind'])},
    {k: t('Laju kebocoran', 'Leak rate'), a: at(['laju', 'leak rate'])},
    {k: t('Garis pandang', 'Line of sight'), a: at(['garis pandang', 'line of sight'])},
  ];
  return (
    <SceneFrame theme="light">
      <SceneTitle kicker={t('BATASAN', 'LIMITATIONS')} title={t('Kamera melengkapi GLD, bukan menggantikannya', 'The camera complements GLD rather than replacing it')} />
      <div style={{position: 'absolute', left: padX, top: portrait ? 420 : 240, width: W, display: 'grid', gridTemplateColumns: portrait ? '1fr 1fr' : 'repeat(4, 1fr)', gap: 16}}>
        {FACTORS.map((f) => (
          <InfoCard key={f.k} at={f.a} k={t('Faktor', 'Factor')} v={f.k} color={COLORS.gas} />
        ))}
      </div>
      <div style={{position: 'absolute', left: padX, top: portrait ? 760 : 440, width: W, display: 'grid', gridTemplateColumns: portrait ? '1fr' : '1fr 1fr', gap: 22}}>
        {[
          {h: t('Tampak pada pita ≈3,3 µm', 'Visible in the ≈3.3 µm band'), items: ['CH₄', 'C₃H₈', 'C₄H₁₀', 'VOC'], c: COLORS.ok, a: tGas - 20},
          {h: t('Tidak tampak → tetap andalkan GLD', 'Not visible → GLD remains essential'), items: ['H₂', 'CO', 'H₂S'], c: COLORS.alarm, a: tGas},
        ].map((col) => {
          const p = spring({frame: frame - col.a, fps, config: {damping: 200}});
          return (
            <div key={col.h} style={{opacity: p, transform: `translateY(${18 * (1 - p)}px)`, padding: '22px 26px', borderRadius: 16, backgroundColor: COLORS.surface, border: `2px solid ${col.c}`}}>
              <div style={{fontSize: 26, fontWeight: 800, color: col.c}}>{col.h}</div>
              <div style={{display: 'flex', gap: 14, marginTop: 14, flexWrap: 'wrap'}}>
                {col.items.map((g) => (
                  <div key={g} style={{padding: '8px 18px', borderRadius: 10, backgroundColor: COLORS.bg, fontSize: 30, fontWeight: 800}}>
                    {g}
                  </div>
                ))}
              </div>
            </div>
          );
        })}
      </div>
      <div style={{position: 'absolute', left: padX, top: portrait ? 1240 : 760, fontSize: 30, fontWeight: 800, color: COLORS.blue, opacity: progress(frame, tComp, 16)}}>
        {t('GLD: identifikasi jenis gas · OGI: visualisasi spasial', 'GLD: gas identification · OGI: spatial visualisation')}
      </div>
    </SceneFrame>
  );
};

// 10 — Nilai strategis: replikasi di seluruh RU + dokumentasi emisi fugitif + potensi predictive maintenance.
const RUS = [
  {k: 'RU II Dumai', lat: 1.67, lon: 101.45},
  {k: 'RU III Plaju', lat: -2.99, lon: 104.8},
  {k: 'RU IV Cilacap', lat: -7.72, lon: 109.0},
  {k: 'RU V Balikpapan', lat: -1.27, lon: 116.83},
  {k: 'RU VI Balongan', lat: -6.38, lon: 108.37},
  {k: 'RU VII Kasim', lat: -1.3, lon: 131.1},
];
export const OgiStrategy: React.FC = () => {
  const frame = useCurrentFrame();
  const {portrait, padX, width} = useLayout();
  const t = useT();
  const at = useNarration('ogi_strategy');
  const tRep = at(['direplikasi', 'replicated']);
  const tEmis = at(['emisi fugitif', 'fugitive emissions']);
  const tPdm = at(['predictive maintenance', 'predictive maintenance']);
  const map = portrait ? {x: padX, y: 400, w: width - padX * 2, h: 440} : {x: padX, y: 230, w: 1000, h: 520};
  const X = (lon: number) => ((lon - 95) / 46) * map.w;
  const Y = (lat: number) => ((6 - lat) / 17) * map.h;
  return (
    <SceneFrame theme="night">
      <SceneTitle kicker={t('NILAI STRATEGIS', 'STRATEGIC VALUE')} title={t('Modular, siap direplikasi di seluruh kilang', 'Modular, ready to replicate across refineries')} />
      <div style={{position: 'absolute', left: map.x, top: map.y, width: map.w, height: map.h, borderRadius: 18, backgroundColor: '#0D1828', border: '1px solid #26354D', overflow: 'hidden'}}>
        <svg width={map.w} height={map.h}>
          {Array.from({length: 12}).map((_, i) => (
            <line key={`v${i}`} x1={(i / 11) * map.w} y1={0} x2={(i / 11) * map.w} y2={map.h} stroke="rgba(91,155,255,0.07)" />
          ))}
          {Array.from({length: 7}).map((_, i) => (
            <line key={`h${i}`} x1={0} y1={(i / 6) * map.h} x2={map.w} y2={(i / 6) * map.h} stroke="rgba(91,155,255,0.07)" />
          ))}
          {RUS.map((r, i) => {
            const p = progress(frame, tRep - 20 + i * 8, 16);
            const pulse = ((frame + i * 11) % 45) / 45;
            return (
              <g key={r.k} opacity={p}>
                <circle cx={X(r.lon)} cy={Y(r.lat)} r={10 + pulse * 26} fill="none" stroke={COLORS.gas} strokeOpacity={(1 - pulse) * 0.7} strokeWidth={2} />
                <circle cx={X(r.lon)} cy={Y(r.lat)} r={9} fill={COLORS.gas} />
                <text x={X(r.lon) + 16} y={Y(r.lat) + 7} fontSize={portrait ? 22 : 22} fontWeight={700} fill="#F2F5FA">
                  {r.k}
                </text>
              </g>
            );
          })}
        </svg>
        <div style={{position: 'absolute', left: 16, bottom: 12, fontSize: 17, color: '#9AA8BD'}}>{t('Posisi skematik (bukan peta skala)', 'Schematic positions (not to scale)')}</div>
      </div>
      <div style={{position: 'absolute', left: portrait ? padX : 1170, right: portrait ? padX : undefined, top: portrait ? 900 : 230, width: portrait ? undefined : 630, display: 'flex', flexDirection: 'column', gap: 16}}>
        <InfoCard at={tRep} big k={t('Arsitektur', 'Architecture')} v={t('Modular · desain standar per unit', 'Modular · standard design per unit')} color="#5B9BFF" style={{backgroundColor: '#111C2E', color: '#F2F5FA', border: '1px solid #26354D'}} />
        <InfoCard at={tEmis} big k="ESG" v={t('Dokumentasi emisi fugitif', 'Fugitive emission documentation')} color={COLORS.ok} style={{backgroundColor: '#111C2E', color: '#F2F5FA', border: '1px solid #26354D'}} />
        <InfoCard
          at={tPdm - 20}
          big
          k={t('Potensi pengembangan', 'Potential development')}
          v={t('Predictive maintenance: hot spot pada heater, isolasi rusak, steam trap', 'Predictive maintenance: heater hot spots, damaged insulation, steam traps')}
          color={COLORS.gas}
          style={{backgroundColor: '#111C2E', color: '#F2F5FA', border: `1px dashed ${COLORS.gas}`}}
        />
      </div>
    </SceneFrame>
  );
};

// 11 — Penutup: tagline, ringkasan, logo mitra, fade out.
const P = PALETTES.night;
export const OgiOutro: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps, durationInFrames} = useVideoConfig();
  const {portrait, padX, title} = useLayout();
  const t = useT();
  const logoAt = durationInFrames - 110;
  const toLogo = progress(frame, logoAt - 10, 20);
  const logoIn = spring({frame: frame - logoAt, fps, config: {damping: 200}});
  const out = 1 - progress(frame, durationInFrames - 24, 24);
  const ITEMS = [
    t('MWIR ≈3,3 µm: plume hidrokarbon tampak', 'MWIR ≈3.3 µm: hydrocarbon plumes made visible'),
    t('Edge AI: segmentasi plume & logika persistensi', 'Edge AI: plume segmentation & persistence logic'),
    t('GLD + OGI: jenis gas dan lokasi dalam satu dashboard', 'GLD + OGI: gas type and location in one dashboard'),
    t('Modular untuk seluruh kilang Pertamina', 'Modular for all Pertamina refineries'),
  ];
  return (
    <AbsoluteFill style={{...themeVars('night'), backgroundColor: P.bg, fontFamily: FONT, color: P.text, opacity: out * progress(frame, 0, 18)}}>
      <AbsoluteFill style={{opacity: 1 - toLogo, padding: portrait ? `280px ${padX}px` : `110px ${padX}px`}}>
        <div style={{fontSize: 24, fontWeight: 800, letterSpacing: 4, color: P.blueLight}}>GLD NEXT · OPTICAL GAS IMAGING</div>
        <Caption text={t('Dari deteksi titik menuju pemantauan area', 'From point detection to area monitoring')} from={6} size={title(60)} color="#F2F5FA" style={{marginTop: 10, maxWidth: 1400}} />
        <div style={{display: 'grid', gridTemplateColumns: portrait ? '1fr' : '1fr 1fr', gap: 20, marginTop: 50}}>
          {ITEMS.map((it, i) => {
            const p = spring({frame: frame - 30 - i * 12, fps, config: {damping: 16}});
            return (
              <div key={it} style={{opacity: p, transform: `translateY(${22 * (1 - p)}px)`, padding: '24px 28px', borderRadius: 16, backgroundColor: 'rgba(17,28,46,0.9)', border: `1px solid ${P.line}`, borderLeft: `8px solid ${[P.gas, P.blueLight, P.ok, P.alarm][i]}`, fontSize: portrait ? 32 : 32, fontWeight: 700}}>
                {it}
              </div>
            );
          })}
        </div>
      </AbsoluteFill>
      <AbsoluteFill style={{backgroundColor: '#FFFFFF', opacity: toLogo, alignItems: 'center', justifyContent: 'center'}}>
        <div style={{display: 'flex', flexDirection: portrait ? 'column' : 'row', alignItems: 'center', gap: portrait ? 90 : 120, opacity: logoIn, transform: `scale(${0.94 + 0.06 * logoIn})`}}>
          <Img src={staticFile(ASSETS.logoPertamina.path)} style={{height: portrait ? 110 : 100}} />
          <Img src={staticFile(ASSETS.logoLgu.path)} style={{height: portrait ? 140 : 130}} />
          <Img src={staticFile(ASSETS.logoItb.path)} style={{height: portrait ? 190 : 170}} />
        </div>
        <div style={{marginTop: 60, fontSize: portrait ? 30 : 30, fontWeight: 600, color: '#14213A', opacity: logoIn}}>
          {t('Dikembangkan oleh Lab Internet of Things, Institut Teknologi Bandung', 'Developed by the Internet of Things Laboratory, Institut Teknologi Bandung')}
        </div>
      </AbsoluteFill>
      <Sfx name="whoosh" at={logoAt - 10} volume={0.3} />
      <Sfx name="success" at={logoAt + 6} volume={0.25} />
    </AbsoluteFill>
  );
};
