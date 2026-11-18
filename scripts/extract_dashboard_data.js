// Ekstrak array data dari Deliverables/Dashboard_GLD_ProjectManagement.html ke JSON (stdout).
// Dipakai oleh build_dashboard_laporan_html.py agar versi cetak selalu sinkron dgn dashboard interaktif.
const fs = require('fs');
const path = require('path');
const src = fs.readFileSync(path.join(__dirname, '..', 'Deliverables', 'Dashboard_GLD_ProjectManagement.html'), 'utf8');
const names = ['ACT', 'GMILES', 'RU', 'WSW', 'RES', 'FEED', 'AI', 'ISS', 'RECS', 'DONE', 'OUT', 'EVO', 'GASES'];
const out = {};
for (const n of names) {
  const start = src.indexOf('const ' + n + '=[');
  if (start < 0) throw new Error('array not found: ' + n);
  const end = src.indexOf('\n];', start);
  const body = src.slice(start + ('const ' + n + '=').length, end + 2);
  out[n] = new Function('return ' + body)();
}
const grab = (re) => { const m = src.match(re); return m ? m[1] : null; };
out.TODAY = grab(/const TODAY=new Date\(([^)]*)\)/);
const act = src.slice(src.indexOf('const act=['), src.indexOf('].map', src.indexOf('const act=[')) + 1);
const plan = src.slice(src.indexOf('const plan=['), src.indexOf('].map', src.indexOf('const plan=[')) + 1);
const fc = src.slice(src.indexOf('const fc=['), src.indexOf('].map', src.indexOf('const fc=[')) + 1);
const toPts = (t) => new Function('return ' + t.replace(/^const \w+=/, ''))().map(([d, v]) => [d.toISOString().slice(0, 10), v]);
out.SC = { act: toPts(act), plan: toPts(plan), fc: toPts(fc) };
process.stdout.write(JSON.stringify(out));
