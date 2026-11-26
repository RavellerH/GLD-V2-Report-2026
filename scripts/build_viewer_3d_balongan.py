"""Viewer 3D interaktif (HTML mandiri) dari model Blender RU VI Balongan.
Sumber: scripts/assets/rab_balongan/model_3d_balongan.glb + _pts.json (render_3d_balongan_blender.py -- glb)."""
import base64
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
RB = os.path.join(HERE, "assets", "rab_balongan")
OUT = os.path.join(os.path.dirname(HERE), "Deliverables", "Model_3D_Instalasi_GLD_RU-VI_Balongan.html")

glb = base64.b64encode(open(os.path.join(RB, "model_3d_balongan.glb"), "rb").read()).decode()
pts = json.load(open(os.path.join(RB, "model_3d_balongan_pts.json")))

HTML = r"""<title>Model 3D GLD Balongan</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600&family=Inter:wght@400;500;600&display=swap">
<style>
/* VOICE work: rencana instalasi untuk tim lapangan & Pertamina
   IDEA meja model maket site: maket 3D yang bisa diputar, dengan tag perangkat seperti label maket
   PICTURE model 3D satu layar penuh (peta + struktur WHB + gedung kantor + perangkat)
   COLOUR biru LGU #2B5FCB, charcoal #262321, oranye GLD, ungu CH, teal GW
   TYPE Space Grotesk + Inter
   LAYOUT strip judul tipis; kanvas penuh; panel perangkat di kiri bawah (di ponsel: laci bawah) */
:root{color-scheme:light dark;--bg:light-dark(#eef2fb,#0d1018);--ink:light-dark(#262321,#eef0f6);--mut:light-dark(#5b6170,#a6acbb);--pan:light-dark(rgba(255,255,255,.94),rgba(22,26,36,.94));--line:light-dark(#d5dbea,#2d3445);--blue:#2B5FCB;--strip:#262321;--gld:#e8820c;--ch:#7a4fe0;--gw:#00897b;--lora:#1f6fe0}
:root[data-theme=light]{color-scheme:light}:root[data-theme=dark]{color-scheme:dark}
*{box-sizing:border-box;min-width:0}
[hidden]{display:none!important}
html,body{height:100%}
body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.45 Inter,system-ui,sans-serif;overflow:hidden}
.top{position:fixed;left:0;right:0;top:0;z-index:5;background:var(--strip);color:#fff;display:flex;flex-wrap:wrap;align-items:center;gap:8px 16px;padding-block:calc(env(safe-area-inset-top,0px) + 10px) 10px;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
.top h1{font:600 20px/1.1 "Space Grotesk",Inter,sans-serif;margin:0;letter-spacing:-.01em}
.top h1 small{display:block;font:400 12.5px/1.3 Inter,sans-serif;color:#c9cdd8;margin-top:3px}
.views{display:flex;flex-wrap:wrap;gap:6px;margin-left:auto}
.views button,.dev button{font:500 13px Inter,sans-serif;border-radius:6px;cursor:pointer}
.views button{background:transparent;color:#fff;border:1px solid #5d6372;padding:7px 11px}
.views button:hover,.views button.on{background:var(--blue);border-color:var(--blue)}
#c{position:fixed;inset:0;display:block;width:100%;height:100%;touch-action:none}
.lab{position:fixed;left:0;top:0;z-index:3;pointer-events:none;transform:translate(-50%,-100%);white-space:nowrap}
.lab span{display:block;padding:4px 8px;border-radius:5px;color:#fff;font:600 12.5px Inter,sans-serif;box-shadow:0 1px 3px rgba(0,0,0,.25)}
.lab i{display:block;width:2px;height:16px;margin:0 auto;background:currentColor}
.lab.env span{background:rgba(38,35,33,.82);font-weight:500}
.lab.dist{transform:translate(-50%,-50%)}
.lab.dist span{background:#fff;color:var(--lora);border:1.5px solid var(--lora);box-shadow:none}
.dev{position:fixed;z-index:4;left:max(16px,env(safe-area-inset-left,0px));bottom:calc(env(safe-area-inset-bottom,0px) + 16px);width:330px;background:var(--pan);border:1px solid var(--line);border-radius:10px;padding:12px 14px;backdrop-filter:blur(6px)}
.dev h2{font:600 14px "Space Grotesk",Inter,sans-serif;margin:0 0 8px}
.dev ul{list-style:none;margin:0;padding:0;display:grid;gap:4px}
.dev button{width:100%;display:grid;grid-template-columns:12px 1fr auto;align-items:center;gap:8px;text-align:left;background:transparent;color:var(--ink);border:1px solid transparent;padding:6px 8px}
.dev button:hover{border-color:var(--line);background:color-mix(in srgb,var(--blue) 8%,transparent)}
.dev b{width:12px;height:12px;border-radius:3px}
.dev em{font-style:normal;color:var(--mut);font-size:12.5px;white-space:nowrap}
.dev p{margin:10px 0 0;color:var(--mut);font-size:12.5px}
.tools{display:flex;gap:12px;margin-top:8px;font-size:13px;color:var(--mut)}
.tools label{display:flex;gap:6px;align-items:center;cursor:pointer}
.hint{position:fixed;z-index:4;right:max(16px,env(safe-area-inset-right,0px));bottom:calc(env(safe-area-inset-bottom,0px) + 16px);background:var(--pan);border:1px solid var(--line);border-radius:8px;padding:8px 12px;font-size:12.5px;color:var(--mut)}
#load{position:fixed;inset:0;display:grid;place-items:center;z-index:6;color:var(--mut);font:500 15px Inter,sans-serif;pointer-events:none}
@media(max-width:700px){.top h1{font-size:17px}.views{margin-left:0}.views button{padding:6px 9px;font-size:12.5px}.dev{left:0;right:0;bottom:0;width:auto;border-radius:12px 12px 0 0;padding-bottom:calc(env(safe-area-inset-bottom,0px) + 10px);max-height:42vh;overflow:auto}.dev p{display:none}.hint{display:none}.lab span{font-size:11.5px;padding:3px 6px}}
</style>

<header class="top">
  <h1>Model 3D Instalasi GLD · RU VI Balongan<small>Rencana titik GLD, Cluster Head, dan Gateway · draf 27 Nov 2026 · bentuk bangunan &amp; dimensi = estimasi</small></h1>
  <nav class="views" id="views">
    <button data-v="all" class="on">Seluruh lokasi</button>
    <button data-v="whb">Klaster WHB</button>
    <button data-v="GLD-01">GLD-01</button>
    <button data-v="GLD-02">GLD-02</button>
    <button data-v="CH-01">CH-01</button>
    <button data-v="CH-02">CH-02</button>
    <button data-v="GW-01">Gateway</button>
  </nav>
</header>
<canvas id="c"></canvas>
<div id="load">Memuat model 3D…</div>
<div id="labels"></div>
<aside class="dev">
  <h2>Perangkat &amp; jalur data</h2>
  <ul id="devlist"></ul>
  <div class="tools"><label><input type="checkbox" id="tl" checked> Label</label><label><input type="checkbox" id="te" checked> Label bangunan</label><label><input type="checkbox" id="tr"> Putar otomatis</label></div>
  <p>Jarak: CH-01→CH-02 dan CH-02→GW dari peta/ukur Google Maps; GLD–CH-01 dari peta. Semua perlu diverifikasi di lapangan.</p>
</aside>
<div class="hint">Seret untuk memutar · scroll/cubit untuk zoom · klik kanan / dua jari untuk geser</div>

<script src="https://cdn.jsdelivr.net/npm/three@0.128.0/build/three.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/loaders/GLTFLoader.js"></script>
<script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
<script id="pts" type="application/json">__PTS__</script>
<script>
{
const P = JSON.parse(document.getElementById('pts').textContent);
const V = (k) => new THREE.Vector3(...P[k]);
const DEV = [
  {k:'GLD-01', t:'TOP:GLD-01', txt:'GLD-01 · 24 VDC', c:'--gld', d:'± 11 m ke CH-01'},
  {k:'GLD-02', t:'TOP:GLD-02', txt:'GLD-02 · 24 VDC', c:'--gld', d:'± 11 m ke CH-01'},
  {k:'CH-01', t:'TOP:CH-01', txt:'CH-01 · 5 VDC, bawah struktur', c:'--ch', d:'± 32 m ke CH-02'},
  {k:'CH-02', t:'TOP:CH-02', txt:'CH-02 · panel surya', c:'--ch', d:'± 91 m ke GW-01'},
  {k:'GW-01', t:'TOP:GW-01', txt:'GW-01 · tepi atap carport', c:'--gw', d:'5 VDC dari kantor'},
];
const ENV = [['W:c','Struktur WHB',[0,24,0]],['VESSELS','Deret vessel'],['COL1','Kolom tinggi'],['BLDG','Gedung kantor'],['BLDG2','Gedung']];
const DIST = [['LORA:GLD-01>CH-01','± 11 m'],['LORA:GLD-02>CH-01','± 11 m'],['LORA:CH-01>CH-02','LoRa ± 32 m'],['LORA:CH-02>GW-01','LoRa ± 91 m']];
const css = (v) => getComputedStyle(document.documentElement).getPropertyValue(v).trim();

const canvas = document.getElementById('c');
const renderer = new THREE.WebGLRenderer({canvas, antialias:true});
renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
renderer.outputEncoding = THREE.sRGBEncoding;
const scene = new THREE.Scene();
const dark = matchMedia('(prefers-color-scheme: dark)').matches && document.documentElement.dataset.theme !== 'light' || document.documentElement.dataset.theme === 'dark';
scene.background = new THREE.Color(dark ? 0x141a26 : 0xe6ecf7);
scene.add(new THREE.HemisphereLight(0xffffff, 0x6f7480, 0.75));
const sun = new THREE.DirectionalLight(0xffffff, 0.55); sun.position.set(60, 120, 80); scene.add(sun);
const cam = new THREE.PerspectiveCamera(40, 1, 0.05, 3000);
const ctl = new THREE.OrbitControls(cam, canvas);
ctl.enableDamping = true; ctl.maxPolarAngle = Math.PI * 0.495; ctl.minDistance = 1; ctl.maxDistance = 600;

const mid = (a, b) => V(a).add(V(b)).multiplyScalar(0.5);
const gl = mid('GLD-01', 'GLD-02');
const VIEWS = {
  all: () => { const c = mid('W:c', 'GW-01'); return [c.clone().add(new THREE.Vector3(70, 95, 120)), c]; },
  whb: () => [gl.clone().add(new THREE.Vector3(26, 12, 34)), gl.clone().setY(2)],
  'GLD-01': () => { const t = V('TOP:GLD-01'); return [t.clone().add(new THREE.Vector3(2.2, 1.0, 2.8)), t.clone().setY(t.y - 0.3)]; },
  'GLD-02': () => { const t = V('TOP:GLD-02'); return [t.clone().add(new THREE.Vector3(2.2, 1.0, 2.8)), t.clone().setY(t.y - 0.3)]; },
  'CH-01': () => { const t = V('TOP:CH-01'); return [t.clone().add(new THREE.Vector3(2.5, 1.2, 3.2)), t.clone().setY(t.y - 0.5)]; },
  'CH-02': () => { const t = V('TOP:CH-02'); return [t.clone().add(new THREE.Vector3(6, 1.5, 8)), t.clone().setY(t.y - 3)]; },
  'GW-01': () => { const t = V('TOP:GW-01'); return [t.clone().add(new THREE.Vector3(5, 1.5, 6)), t.clone().setY(t.y - 1.5)]; },
};
let fly = null;
function go(v) {
  const [p, t] = VIEWS[v]();
  fly = {p0: cam.position.clone(), t0: ctl.target.clone(), p, t, s: performance.now()};
  document.querySelectorAll('#views button').forEach(b => b.classList.toggle('on', b.dataset.v === v));
}
{ const [p, t] = VIEWS.all(); cam.position.copy(p); ctl.target.copy(t); }
document.getElementById('views').addEventListener('click', e => { const b = e.target.closest('button'); if (b) go(b.dataset.v); });
document.getElementById('devlist').innerHTML = DEV.map(d => `<li><button data-v="${d.k}"><b style="background:var(${d.c})"></b><span>${d.txt}</span><em>${d.d}</em></button></li>`).join('');
document.getElementById('devlist').addEventListener('click', e => { const b = e.target.closest('button'); if (b) go(b.dataset.v); });

const L = document.getElementById('labels'); const items = [];
function lab(pos, html, cls, color) {
  const el = document.createElement('div'); el.className = 'lab ' + cls;
  el.innerHTML = html; if (color) { el.style.color = color; el.firstChild.style.background = color; }
  L.appendChild(el); items.push({el, pos, cls});
}
DEV.forEach(d => lab(V(d.t), `<span>${d.txt}</span><i></i>`, 'devl', css(d.c)));
ENV.forEach(([k, t, o]) => { if (P[k]) lab(V(k).add(new THREE.Vector3(...(o || [0, 2, 0]))), `<span>${t}</span><i></i>`, 'env'); });
DIST.forEach(([k, t]) => { if (P[k]) lab(V(k), `<span>${t}</span>`, 'dist'); });
const tl = document.getElementById('tl'), te = document.getElementById('te'), tr = document.getElementById('tr');

new THREE.GLTFLoader().parse(Uint8Array.from(atob(document.getElementById('glb').textContent.trim()), c => c.charCodeAt(0)).buffer, '', g => {
  g.scene.traverse(o => { if (o.isMesh && o.material) { o.material.side = THREE.DoubleSide; if (o.material.transparent) o.material.depthWrite = false; } });
  scene.add(g.scene); document.getElementById('load').hidden = true;
}, err => { document.getElementById('load').textContent = 'Model gagal dimuat: ' + err; });

function size() { const w = innerWidth, h = innerHeight; renderer.setSize(w, h, false); cam.aspect = w / h; cam.updateProjectionMatrix(); }
addEventListener('resize', size); size();
const v = new THREE.Vector3(), ease = x => x < .5 ? 2 * x * x : 1 - (-2 * x + 2) ** 2 / 2;
function tick(now) {
  if (fly) { const u = Math.min(1, (now - fly.s) / 900), e = ease(u);
    cam.position.lerpVectors(fly.p0, fly.p, e); ctl.target.lerpVectors(fly.t0, fly.t, e); if (u === 1) fly = null; }
  ctl.autoRotate = tr.checked; ctl.autoRotateSpeed = 0.8; ctl.update(); renderer.render(scene, cam);
  const W = innerWidth, H = innerHeight;
  for (const it of items) {
    const show = it.cls === 'env' ? te.checked : tl.checked;
    v.copy(it.pos).project(cam);
    if (!show || v.z > 1 || v.x < -1.05 || v.x > 1.05 || v.y < -1.05 || v.y > 1.05) { it.el.hidden = true; continue; }
    it.el.hidden = false; it.el.style.left = ((v.x + 1) / 2 * W) + 'px'; it.el.style.top = ((1 - v.y) / 2 * H) + 'px';
  }
  requestAnimationFrame(tick);
}
requestAnimationFrame(tick);
}
</script>
<script id="glb" type="application/octet-stream">__GLB__</script>
"""
# skrip pemuat dijalankan sebelum tag glb; pindahkan data glb ke depan agar tersedia saat parse
html = HTML.replace("__PTS__", json.dumps(pts))
data = '<script id="glb" type="application/octet-stream">' + glb + "</script>\n"
html = html.replace('<script id="glb" type="application/octet-stream">__GLB__</script>\n', "")
html = html.replace('<script id="pts"', data + '<script id="pts"', 1)
open(OUT, "w", encoding="utf-8").write(html)
print(OUT, round(os.path.getsize(OUT) / 1e6, 2), "MB")
