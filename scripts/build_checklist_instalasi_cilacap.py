"""
Generator checklist detail instalasi GLD RU IV Cilacap (LGU vs Pertamina).

Output : Deliverables/Checklist_Detail_Instalasi_GLD_RU-IV_Cilacap.html (interaktif, self-contained)
         PDF dicetak dari HTML yang sama (mode cetak) via Chrome headless.
Basis  : 3 GLD + 3 CH + 1 Gateway; block diagram lingkup final 8 Okt 2026; Spesifikasi Material
         Instalasi rev 1.5; pesan Pertamina 21 Okt 2026 (spek PC server). Tanggal instalasi belum ada,
         sehingga item disusun per tahap relatif (H-30 ... pasca).
Jalankan: python scripts/build_checklist_instalasi_cilacap.py
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "Deliverables" / "Checklist_Detail_Instalasi_GLD_RU-IV_Cilacap.html"

PHASES = [
    ("H30", "H-30", "Perencanaan, izin & keputusan desain"),
    ("H14", "H-14", "Pengadaan, pekerjaan sipil & kelistrikan"),
    ("H7", "H-7", "Persiapan mobilisasi"),
    ("HH", "Hari-H", "Pemasangan & energize"),
    ("COM", "Commissioning & SAT", "Uji fungsi di lokasi"),
    ("POST", "Pasca", "Serah terima & pemantauan awal"),
]

# (tahap, kategori, pihak, tugas, detail, perlu_konfirmasi)
# pihak: "LGU" | "Pertamina" | "Bersama"
I = [
    # ---------------- H-30
    ("H30", "Perizinan & HSE", "Pertamina", "Konfirmasi tertulis klasifikasi area titik pasang",
     "HSE RU IV menyatakan tertulis bahwa ketiga titik GLD, ketiga titik CH, dan lokasi mast Gateway berada di area non-ATEX (safe area). GLD belum bersertifikat ATEX, sehingga hanya boleh dipasang di area non-ATEX.", True),
    ("H30", "Lokasi & titik", "Bersama", "Penetapan titik final 3 GLD, 3 CH, 1 Gateway",
     "Kunjungan bersama HSE RU IV: posisi tiap titik (koordinat/foto), arah angin dominan, letak sumber bocor (flange/valve) terdekat. Penomoran: GLD-01…03, CH-01…03, GW-01, sama dengan nama di dashboard.", False),
    ("H30", "Lokasi & titik", "LGU", "Kajian jalur radio (line of sight) antar-titik",
     "Tim RF LGU memeriksa jalur GLD → CH → antena Gateway; menetapkan tinggi antena tiap CH dan mast Gateway. Hasil: peta jalur radio + tinggi final per titik.", False),
    ("H30", "Lokasi & titik", "Bersama", "Tinggi sensor GLD per titik",
     "Rekomendasi titik tengah sensor ± 0,5 m dari tanah (gas sasaran LPG/H₂S cenderung turun); untuk titik yang menyasar H₂/metana, tinggi mengikuti posisi sumber bocor. Disepakati bersama HSE RU IV.", True),
    ("H30", "Desain mekanik", "Bersama", "Orientasi pelat U-bolt pada tiang vertikal",
     "Pelat 250 × 250 mm + U-bolt 2\"/DN50 dirancang untuk pipa OD 60,3 mm. Kecocokan pada tiang baru yang berdiri vertikal dicek tim desain LGU bersama pelaksana RU IV sebelum pelat difabrikasi.", True),
    ("H30", "Daya & kabel", "Bersama", "Pilih skema PSU 24 VDC: per titik atau pusat",
     "Opsi A: PSU 220 VAC → 24 VDC di junction box dekat tiap GLD (kabel pendek 2 × 1,5 mm²). Opsi B: satu PSU pusat ≥ 5 A, kabel home-run ke tiap GLD (ukuran naik sesuai jarak). Block diagram saat ini menggambar Opsi A (junction box per GLD).", True),
    ("H30", "Daya & kabel", "Pertamina", "Ukur rute & sumber 220 VAC terdekat tiap titik GLD",
     "Jarak rute aktual (bukan garis lurus) dari local receptacle ke tiap junction box/GLD. Panjang kabel = rute × 1,10 + 3 m + 3 m.", False),
    ("H30", "Jaringan & server", "Pertamina", "Tunjuk ruang Gateway & ruang server lokal",
     "Gateway dan router Wi-Fi LGU satu ruangan (jarak 1–5 m, tanpa sekat logam); ruang server lokal untuk PC. Ukur jarak rute Cat6 router → PC (≤ 90 m per segmen).", False),
    ("H30", "Jaringan & server", "Pertamina", "Siapkan PC server fisik",
     "PC fisik (bukan VM), 2 port LAN (NIC kedua boleh USB-LAN), di ruang server lokal. Minimum 4 core / 8 GB RAM / SSD 256 GB. Konfirmasi OS yang dipakai & PIC IT RU IV.", False),
    ("H30", "Jaringan & server", "Pertamina", "Izin titik jaringan intranet untuk port LAN-2 PC",
     "IT RU IV menyediakan titik jaringan kantor + alamat IP untuk PC (akses dashboard/API dari kantor saja). PC tidak meneruskan lalu lintas antara jaringan GLD dan intranet.", True),
    ("H30", "Perizinan & HSE", "Pertamina", "Penunjukan pelaksana instalasi RU IV",
     "Tim/kontraktor RU IV yang mengerjakan sipil, tiang, mast, kabel, PSU, junction box, dan pemasangan fisik — termasuk K3 dan pekerjaan ketinggian (tiang CH 3 m, mast Gateway ± 5–6 m).", False),
    ("H30", "Perizinan & HSE", "Bersama", "Susun TRA/JSA instalasi",
     "TRA/JSA untuk: galian & pengecoran, pemasangan tiang/mast, pekerjaan ketinggian, kelistrikan 220 VAC/24 VDC, energize & uji alarm. LGU menyerahkan data teknis; RU IV mengesahkan.", False),
    ("H30", "Chamber gas", "Bersama", "Sepakati jenis gas yang dilatih di Cilacap",
     "Daftar gas yang diminta RU IV untuk dataset & model AI di lokasi. Model saat ini mengenali Udara Bersih, LPG, H₂; gas lain (mis. H₂S, metana, CO) perlu sampel di lokasi.", True),
    ("H30", "Chamber gas", "Pertamina", "Tunjuk ruang kantor untuk chamber gas",
     "Ruang di kantor kilang (bukan area proses), berventilasi, ada stop kontak 220 VAC, meja kerja, akses keluar-masuk tabung gas. Chamber tidak boleh masuk area proses.", False),
    ("H30", "Chamber gas", "Pertamina", "Penyediaan sampel gas bersertifikat",
     "Tabung gas acuan sesuai daftar gas yang disepakati, lengkap dengan regulator & sertifikat konsentrasi. Pengiriman gas berbahaya (mis. H₂S) memerlukan jasa hazmat berlisensi — kurir umum tidak dapat dipakai.", True),

    # ---------------- H-14
    ("H14", "Pengadaan", "Pertamina", "Pengadaan material tiang & mast",
     "Pipa baja galvanis 2\" Sch40 (OD 60,3 mm): 3 tiang GLD @ 1,6 m (1,0 m di atas tanah), 3 tiang CH @ 4,0 m (3,0 m di atas tanah), 1 mast Gateway 6 m (opsi berdiri sendiri). Pipe cap, angkur silang Ø12 mm.", False),
    ("H14", "Pengadaan", "Pertamina", "Pengadaan PSU, junction box & proteksi",
     "Per titik GLD (Opsi A): PSU 220 VAC → 24 VDC ≥ 1 A (disarankan 2,5 A DIN-rail), junction box SS316, MCB 2 A sisi AC, terminal block. Sesuaikan bila memilih Opsi B.", False),
    ("H14", "Pengadaan", "Pertamina", "Pengadaan kabel daya 24 VDC",
     "Kabel 2 inti tembaga berlabel L+/L−, ukuran sesuai panjang rute (2 × 1,5 mm² sampai 50 m pada desain 1 A). Jenis luar ruang/armor sesuai standar RU IV; gland armored bila kabel armor.", False),
    ("H14", "Pengadaan", "Pertamina", "Fabrikasi pelat mounting & fastener",
     "Pelat 250 × 250 mm sesuai gambar desain LGU, U-bolt 2\"/DN50 M10 (2 per titik), mur + ring datar + ring per M10 bahan anti-karat (disarankan SS316, dekat laut). Tanpa PVC; tanpa bor/las pada struktur existing.", False),
    ("H14", "Pengadaan", "Pertamina", "Pengadaan UPS ruang Gateway/server",
     "UPS ≥ 1 kVA untuk PC server, router, dan Gateway (melalui adaptor) agar alarm tetap tercatat saat listrik padam.", False),
    ("H14", "Pengadaan", "Pertamina", "Pengadaan kabel jaringan",
     "Cat6 router → PC server (sesuai rute, ≤ 90 m) dan PC (LAN-2) → titik intranet kantor; jalur kabel/conduit gedung.", False),
    ("H14", "Pengadaan", "Bersama", "Kabel koaksial & penangkal petir antena Gateway",
     "Koaksial 50 Ω low-loss LMR-400 (≤ 15 m; > 20 m pakai LMR-600), konektor N, coaxial lightning arrester 900 MHz di titik kabel masuk gedung, self-amalgamating tape. Penyedia disepakati (antena omni 8 dBi dari LGU).", True),
    ("H14", "Sipil", "Pertamina", "Galian & pengecoran pondasi tiang",
     "GLD: 40 × 40 × 60 cm; CH: 50 × 50 × 100 cm; mast Gateway: 50 × 50 × 120 cm. Beton fc' ≥ 20 MPa, permukaan miring menjauhi tiang, toleransi tegak ≤ 1°. Masa tunggu beton ≥ 3 hari sebelum unit dipasang.", False),
    ("H14", "Sipil", "Pertamina", "Grounding tiang & mast",
     "Setiap tiang/mast di-bonding ke grounding RU IV (mis. BC/NYA hijau-kuning 16 mm² + klem pipa). Nilai resistansi mengikuti standar RU IV; kebutuhan proteksi petir tambahan untuk tiang CH & mast ditetapkan HSE/elektrikal RU IV.", False),
    ("H14", "Daya & kabel", "Pertamina", "Penarikan kabel 220 VAC & 24 VDC",
     "Local receptacle → junction box (220 VAC) → GLD (24 VDC). Rute sesuai standar RU IV (tanam/conduit/cable tray). Ujung kabel di sisi GLD dibiarkan dengan cadangan 3 m, belum diterminasi.", False),
    ("H14", "Daya & kabel", "Pertamina", "Pemasangan PSU & junction box",
     "PSU + MCB + terminal block di junction box SS316; uji keluaran 24 VDC tanpa beban dan catat nilainya. Junction box di area aman.", False),
    ("H14", "Jaringan & server", "Pertamina", "Stop kontak & instalasi ruang Gateway/server",
     "Ruang Gateway: min. 2 stop kontak dari UPS (adaptor Gateway 5 VDC, adaptor router). Ruang server: min. 3 (PC, monitor, cadangan). Tarik Cat6 router → PC dan PC → intranet.", False),
    ("H14", "Perangkat LGU", "LGU", "Siapkan 3 GLD + 1 cadangan",
     "Burn-in di lab, firmware & model AI versi final, nomor seri dicatat, cable gland M20 × 1,5 terpasang, label GLD-01…03. Sertakan unit cadangan.", False),
    ("H14", "Perangkat LGU", "LGU", "Siapkan 3 CH + bracket surya",
     "CH varian yang dipakai, 2 panel surya per CH, bracket baja panel (diklem ke tiang 2\" tanpa las/bor), klem CH & antena untuk ujung atas tiang, baterai terisi. Label CH-01…03.", False),
    ("H14", "Perangkat LGU", "LGU", "Siapkan Gateway, router & antena",
     "Gateway + adaptor 5 VDC, router Wi-Fi 2,4 GHz (SSID khusus GLD, WPA2, tanpa WAN/SIM) sudah dikonfigurasi, antena fiber omni 8 dBi 920–923 MHz + pigtail ke konektor Gateway.", False),
    ("H14", "Perangkat LGU", "LGU", "Siapkan installer server",
     "Paket installer satu-paket: MQTT broker, backend, dashboard; uji instal di PC dengan OS yang sama seperti PC RU IV. Konfigurasi IP tetap PC (LAN-1) dan akses dashboard via LAN-2.", False),
    ("H14", "Perangkat LGU", "LGU", "Uji integrasi end-to-end di lab dengan konfigurasi Cilacap",
     "3 GLD → 3 CH → Gateway → router → PC, dengan nama titik & topologi Cilacap; uji alarm push dan failover CH sebelum dikemas.", False),
    ("H14", "Chamber gas", "LGU", "Siapkan chamber gas portable",
     "Chamber, pompa, solenoid valve, sensor referensi, laptop pelatihan model, kabel & adaptor; daftar periksa kebocoran chamber sebelum dikirim.", False),

    # ---------------- H-7
    ("H7", "Perizinan & HSE", "Pertamina", "Izin kerja (PTW) terbit",
     "Izin kerja untuk tiap jenis pekerjaan (sipil, ketinggian, kelistrikan, uji gas) atas TRA/JSA yang disahkan.", False),
    ("H7", "Perizinan & HSE", "Pertamina", "Izin masuk personel & barang",
     "Daftar nama tim LGU/ITB, kendaraan, dan daftar barang (perangkat GLD/CH/Gateway, chamber, laptop, alat ukur) untuk akses kilang.", False),
    ("H7", "Perizinan & HSE", "Bersama", "Safety induction & APD",
     "Jadwal induksi K3 RU IV untuk tim LGU. APD lengkap (helm, sepatu safety, kacamata, sarung tangan, coverall/FR sesuai ketentuan), detektor gas personal bila disyaratkan.", False),
    ("H7", "Perizinan & HSE", "Bersama", "Izin membawa tabung gas uji",
     "Tabung gas kecil untuk uji alarm (bump test) dan sampel chamber: izin masuk, penyimpanan, dan pengawalan sesuai prosedur RU IV.", True),
    ("H7", "Sipil", "Pertamina", "Inspeksi tiang & mast siap pasang",
     "Beton sudah cukup umur, tiang tegak (waterpass), pipe cap terpasang (GLD), grounding terhubung, label nomor titik terpasang.", False),
    ("H7", "Daya & kabel", "Pertamina", "Uji kabel & PSU sebelum unit dipasang",
     "Ukur 24 VDC di ujung kabel sisi GLD (dengan PSU aktif, tanpa unit), uji isolasi kabel, cek polaritas L+/L−. Catat di lembar uji.", False),
    ("H7", "Jaringan & server", "Pertamina", "PC server terpasang & menyala",
     "PC di ruang server, terhubung UPS, Cat6 dari router (LAN-1) dan ke intranet (LAN-2) sudah tersambung; akun admin lokal untuk tim LGU.", False),
    ("H7", "Logistik", "LGU", "Pengemasan & pengiriman perangkat",
     "Daftar packing per kotak (nomor seri), perangkat cadangan, toolkit (multimeter, kunci M10, crimping, laptop, kabel USB/serial), alat uji RF. Baterai Li-ion CH dikirim sesuai aturan angkut baterai.", False),
    ("H7", "Logistik", "LGU", "Dokumen yang dibawa",
     "Gambar mounting & desain bracket, Spesifikasi Material, Instruction Manual GLD, lembar uji commissioning (kosong), daftar IP & kredensial (amplop tertutup).", False),
    ("H7", "Logistik", "Bersama", "Rapat kesiapan (pre-mobilization meeting)",
     "Konfirmasi semua item H-30 s/d H-7 selesai, susunan tim & PIC lapangan kedua pihak, jadwal hari-H, jalur komunikasi darurat.", False),

    # ---------------- Hari-H
    ("HH", "Pemasangan", "Pertamina", "Pasang pelat U-bolt & unit GLD di tiang",
     "Pelaksana RU IV memasang pelat dan unit GLD sesuai tinggi yang disepakati; mur M10 dikencangkan. LGU mengawasi & memeriksa (QA).", False),
    ("HH", "Pemasangan", "Pertamina", "Pasang bracket surya, CH & antena di tiang CH",
     "Bracket 2 panel (arah berlawanan), unit CH & antena di ujung atas tiang (3 m). LGU mengawasi orientasi panel & antena.", False),
    ("HH", "Pemasangan", "Pertamina", "Pasang antena Gateway di mast & koaksial",
     "Antena di puncak mast (± 5–6 m), koaksial dengan drip loop, penangkal petir di titik masuk gedung, sambungan luar dibalut tape. Gateway di dalam ruangan dengan mounting support RU IV.", False),
    ("HH", "Elektrikal GLD", "LGU", "Terminasi kabel 24 VDC di unit GLD",
     "Kabel masuk lewat gland M20 × 1,5, ujung diberi ferrule/skun, terminasi L+/L−, gland dikencangkan, tutup enclosure ditutup rapat (O-ring terpasang).", False),
    ("HH", "Elektrikal GLD", "LGU", "Energize GLD",
     "Atas izin PTW: PSU diaktifkan, cek tegangan di terminal GLD (24 VDC ± 5 %), LED/status boot normal, warm-up sensor. Catat per titik.", False),
    ("HH", "Elektrikal GLD", "LGU", "Aktifkan CH & Gateway",
     "CH menyala dari baterai/panel; Gateway + router menyala dari UPS via adaptor. Cek Gateway terhubung ke router (Wi-Fi) dan ke broker di PC.", False),
    ("HH", "Jaringan & server", "LGU", "Instal & konfigurasi server",
     "Jalankan installer di PC; IP tetap LAN-1; dashboard bisa diakses dari LAN-2 (intranet). Sinkronisasi waktu PC. Nama titik di dashboard = label fisik.", False),
    ("HH", "Chamber gas", "LGU", "Pasang chamber di ruang kantor & uji kebocoran",
     "Chamber dirakit, uji kebocoran sambungan, ventilasi ruang aktif, APAR & detektor gas portable tersedia di ruang.", False),
    ("HH", "Pemasangan", "Bersama", "Housekeeping & foto as-built per titik",
     "Area kerja dibersihkan, sisa material diangkut. Foto setiap titik (jauh & dekat), koordinat, tinggi pasang aktual.", False),

    # ---------------- Commissioning & SAT
    ("COM", "Commissioning", "LGU", "Nulling/kalibrasi nol sensor di lokasi",
     "Mode nulling di udara bersih untuk ke-8 sensor tiap GLD setelah warm-up; catat baseline.", False),
    ("COM", "Commissioning", "LGU", "Uji link radio & jalur mesh",
     "RSSI/SNR tiap hop (GLD → CH, CH → CH, CH → Gateway), rute mesh terbentuk, paket diterima di server. Catat nilai per hop.", False),
    ("COM", "Commissioning", "LGU", "Uji failover CH",
     "Matikan satu CH; pastikan GLD terdampak berpindah rute ke CH lain dan data tetap masuk.", False),
    ("COM", "Commissioning", "Bersama", "Uji alarm push dengan gas uji (bump test)",
     "Atas izin PTW & disaksikan HSE RU IV: paparkan gas uji ke tiap GLD, ukur waktu sejak paparan sampai alarm tampil di dashboard (target ≤ 30 detik). Catat per GLD.", False),
    ("COM", "Commissioning", "Bersama", "Uji akses dashboard dari intranet kantor",
     "Dari komputer kantor RU IV: dashboard & riwayat data dapat dibuka; tidak ada akses dari jaringan GLD ke intranet.", False),
    ("COM", "Commissioning", "LGU", "Uji catu cadangan UPS",
     "Putus sumber 220 VAC ke UPS sesaat: Gateway, router & PC tetap hidup, data tidak hilang.", False),
    ("COM", "Chamber gas", "LGU", "Ambil dataset di chamber & latih model",
     "Dataset per gas yang disepakati, pelatihan model di lokasi, uji akurasi, inject model ke firmware GLD, verifikasi pengenalan gas setelah update.", False),
    ("COM", "Commissioning", "Bersama", "Uji kestabilan 24 jam",
     "Sistem berjalan 24 jam tanpa intervensi: semua titik melapor, tanpa alarm palsu, catat paket hilang.", False),
    ("COM", "Commissioning", "Bersama", "Berita acara SAT",
     "Lembar hasil uji tiap item commissioning ditandatangani LGU dan RU IV (dan Pertamina Patra Niaga bila disyaratkan).", False),

    # ---------------- Pasca
    ("POST", "Serah terima", "LGU", "Dokumen as-built",
     "Denah titik final, tinggi pasang, nomor seri per titik, foto, skema jaringan & daftar IP, versi firmware & model AI.", False),
    ("POST", "Serah terima", "LGU", "Pelatihan operator",
     "Pelatihan dashboard (baca alarm, riwayat, status perangkat), prosedur saat alarm, pemeriksaan visual rutin. Daftar hadir.", False),
    ("POST", "Serah terima", "Bersama", "Kredensial & akses",
     "Serahkan akun dashboard untuk RU IV; akun admin & kredensial router/PC disimpan sesuai prosedur keamanan RU IV.", False),
    ("POST", "Serah terima", "Bersama", "BAST instalasi",
     "Berita acara serah terima instalasi RU IV Cilacap ditandatangani kedua pihak.", False),
    ("POST", "Pemantauan", "LGU", "Pemantauan jarak jauh/berkala 2 minggu pertama",
     "Pantau status titik, baterai CH, kualitas link; laporan singkat mingguan ke RU IV.", False),
    ("POST", "Pemantauan", "Pertamina", "PIC pemeliharaan & jalur pelaporan gangguan",
     "PIC RU IV untuk pemeriksaan visual & pelaporan gangguan; kontak eskalasi LGU disepakati.", False),
]

CODE = {"H30": "H30", "H14": "H14", "H7": "H7", "HH": "HH", "COM": "SAT", "POST": "PS"}
ITEMS, cnt = [], {}
for p, c, w, t, d, k in I:
    cnt[p] = cnt.get(p, 0) + 1
    ITEMS.append(dict(id=f"{CODE[p]}.{cnt[p]:02d}", ph=p, cat=c, who=w, t=t, d=d, k=k))

HTML = r"""<!doctype html>
<html lang="id">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Checklist Instalasi GLD Cilacap</title>
<style>
:root{--blue:#2B5FCB;--blue-soft:#E7ECF8;--char:#262321;--bg:#F4F5F8;--card:#FFFFFF;--ink:#262321;--ink2:#5A5550;--line:#DDE2EC;
--ok:#1F7A43;--okbg:#E6F2EB;--mid:#9A6A08;--midbg:#F6F1DC;--bad:#B4520F;--badbg:#FBEEE4;--lgu:#2B5FCB;--ptm:#9A6A08;--both:#5A5550}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--blue:#7097F0;--blue-soft:#222A3D;--bg:#141312;--card:#1E1C1B;--ink:#ECEAE6;--ink2:#ADA7A0;
--line:#36322F;--ok:#5FC488;--okbg:#1C3124;--mid:#E0B24A;--midbg:#372E14;--bad:#F08A4B;--badbg:#3A2416;--lgu:#7097F0;--ptm:#E0B24A;--both:#ADA7A0}}
:root[data-theme="dark"]{--blue:#7097F0;--blue-soft:#222A3D;--bg:#141312;--card:#1E1C1B;--ink:#ECEAE6;--ink2:#ADA7A0;
--line:#36322F;--ok:#5FC488;--okbg:#1C3124;--mid:#E0B24A;--midbg:#372E14;--bad:#F08A4B;--badbg:#3A2416;--lgu:#7097F0;--ptm:#E0B24A;--both:#ADA7A0}
*{box-sizing:border-box;margin:0;padding:0}
html,body{overflow-x:hidden}
body{background:var(--bg);color:var(--ink);font:15px/1.5 "Segoe UI",Calibri,system-ui,sans-serif}
header{background:var(--char);color:#fff;border-bottom:3px solid #2B5FCB}
.wrap{max-width:1180px;margin:0 auto;padding:0 16px}
header .wrap{padding:14px 16px;display:flex;gap:14px;align-items:center;flex-wrap:wrap}
header h1{font-size:19px}header .m{font-size:13px;color:#C9C4BE}.sp{flex:1}
.btn{background:transparent;color:inherit;border:1px solid currentColor;border-radius:5px;padding:5px 11px;font:inherit;font-size:13px;cursor:pointer}
main{padding:18px 0 50px}
.card{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:16px}
.grid{display:grid;gap:12px;grid-template-columns:repeat(auto-fit,minmax(min(230px,100%),1fr))}
.grid>*{min-width:0}
.kpi .k{font-size:12px;font-weight:700;letter-spacing:.07em;text-transform:uppercase;color:var(--ink2)}
.kpi .v{font-size:28px;font-weight:700;margin:4px 0 2px}
.kpi .s{font-size:13px;color:var(--ink2)}
.bar{height:8px;background:var(--line);border-radius:4px;overflow:hidden;margin-top:6px}.bar i{display:block;height:100%;background:var(--ok)}
.intro{margin:14px 0;font-size:14px;color:var(--ink2)}
.intro b{color:var(--ink)}
.basis{display:flex;flex-wrap:wrap;gap:8px;margin-top:8px}
.pill{font-size:12.5px;padding:3px 10px;border-radius:999px;background:var(--blue-soft);color:var(--blue);font-weight:600}
.flt{position:sticky;top:0;z-index:5;background:var(--bg);padding:10px 0;border-bottom:1px solid var(--line);margin-bottom:12px;display:flex;flex-wrap:wrap;gap:8px 16px;align-items:center;font-size:14px}
.chips{display:flex;gap:6px;flex-wrap:wrap}
.chip{border:1px solid var(--line);background:var(--card);color:var(--ink);border-radius:999px;padding:4px 12px;font:inherit;font-size:13px;cursor:pointer}
.chip.on{background:var(--blue);border-color:var(--blue);color:#fff}
select,input[type=search]{font:inherit;font-size:13px;padding:5px 8px;border:1px solid var(--line);border-radius:5px;background:var(--card);color:var(--ink)}
.ph{margin:20px 0 8px;display:flex;align-items:baseline;gap:10px;flex-wrap:wrap}
.ph h2{font-size:19px;font-family:Cambria,Georgia,serif}.ph span{color:var(--ink2);font-size:13.5px}
.ph .pc{margin-left:auto;font-size:13px;color:var(--ink2)}
.it{display:grid;grid-template-columns:28px 1fr 130px;gap:10px;padding:12px 14px;border:1px solid var(--line);border-radius:8px;background:var(--card);margin-bottom:8px}
.it.done{background:var(--okbg);border-color:transparent}
.it.done .tt{text-decoration:line-through;text-decoration-color:var(--ok)}
.it.na{opacity:.55}
.it input[type=checkbox]{width:20px;height:20px;margin-top:2px;accent-color:#1F7A43;cursor:pointer}
.tt{font-weight:600;font-size:15px}
.meta{display:flex;gap:6px;flex-wrap:wrap;margin:3px 0 4px}
.tag{font-size:11.5px;font-weight:700;padding:1px 7px;border-radius:3px;border:1px solid currentColor}
.w-LGU{color:var(--lgu)}.w-Pertamina{color:var(--ptm)}.w-Bersama{color:var(--both)}
.cat{color:var(--ink2);border-color:var(--line);font-weight:600}
.konf{color:var(--bad);background:var(--badbg);border-color:transparent}
.id{font-size:11.5px;color:var(--ink2);font-variant-numeric:tabular-nums}
.d{font-size:13.5px;color:var(--ink2)}
.side{display:flex;flex-direction:column;gap:6px}
.side select{width:100%}
textarea{width:100%;font:inherit;font-size:13px;padding:5px 8px;border:1px solid var(--line);border-radius:5px;background:var(--bg);color:var(--ink);resize:vertical;min-height:32px;margin-top:6px}
.empty{padding:20px;text-align:center;color:var(--ink2)}
.konfbox h2{font-size:17px;margin-bottom:6px}.konfbox ol{padding-left:20px;font-size:14px}.konfbox li{margin:4px 0}
.konfbox li span{color:var(--ink2)}
footer{color:var(--ink2);font-size:12.5px;padding:0 16px 30px;max-width:1180px;margin:0 auto}
.sign{display:none}
@media (max-width:640px){.it{grid-template-columns:26px 1fr}.it .side{grid-column:2}}
@media print{
 :root{--bg:#fff;--card:#fff;--ink:#000;--ink2:#444;--line:#bbb;--okbg:#fff}
 body{font-size:10.5pt}header{background:#fff;color:#000;border-bottom:2px solid #000}header .m{color:#333}
 .flt,.btn,.noprint,textarea,#kpis{display:none!important}
 .it{break-inside:avoid;grid-template-columns:18px 1fr 120px;padding:6px 8px;margin-bottom:4px;border-radius:0}
 .it input[type=checkbox]{display:none}.it::before{content:"";width:12px;height:12px;border:1.5px solid #000;margin-top:3px}
 .it .side select{display:none}.it .side::after{content:"Status: ________\A Paraf: ________";white-space:pre;font-size:9pt;color:#444}
 .it.done{text-decoration:none}.it.done .tt{text-decoration:none}
 .ph{break-after:avoid}.d{font-size:9.5pt}.tt{font-size:10.5pt}
 .sign{display:block;break-inside:avoid;margin-top:16px}
 .sign table{width:100%;border-collapse:collapse}.sign td,.sign th{border:1px solid #000;padding:6px;font-size:9.5pt;vertical-align:top}.sign td{height:80px}
 @page{size:A4;margin:14mm}
}
</style>
</head>
<body>
<header><div class="wrap">
  <div><h1>Checklist Detail Instalasi GLD — RU IV Cilacap</h1>
  <div class="m">Pembagian LGU &amp; Pertamina per tahap · disusun PT LAPI Ganesha Utama bersama Lab IoT &amp; Fisika ITB · 22 Oktober 2026</div></div>
  <div class="sp"></div>
  <button class="btn" id="csv" type="button">Unduh CSV</button>
  <button class="btn" id="copy" type="button">Salin ringkasan</button>
  <button class="btn" id="theme" type="button">Tema</button>
</div></header>
<main class="wrap">
  <div class="grid" id="kpis"></div>
  <div class="intro card" style="margin-top:12px">
    <b>Basis checklist:</b> 3 GLD + 3 Cluster Head + 1 Gateway, mengikuti block diagram lingkup final (8 Oktober 2026).
    <b style="color:var(--lgu)">LGU</b> menyediakan GLD, Cluster Head, solar cell, Gateway, router Wi-Fi, server software, serta melakukan supervisi teknis, terminasi &amp; energize GLD, dan commissioning.
    <b style="color:var(--ptm)">Pertamina (RU IV)</b> menyediakan instalasi fisik, mounting support, tiang/mast, junction box + PSU 24 VDC, kabel, PC server, UPS, jaringan IT, perizinan, dan HSE.
    Tanggal instalasi belum ditetapkan, jadi item dikelompokkan per tahap relatif terhadap hari-H.
    <div class="basis"><span class="pill">Area non-ATEX saja</span><span class="pill">24 VDC ≥ 1 A per GLD</span><span class="pill">Tiang 2" Sch40 OD 60,3 mm</span><span class="pill">Jaringan lokal tanpa internet</span><span class="pill">Chamber di kantor kilang</span></div>
    <p class="noprint" style="margin-top:8px;font-size:13px">Centang, status, dan catatan tersimpan di browser ini saja. Gunakan “Unduh CSV” atau “Salin ringkasan” untuk berbagi progres.</p>
  </div>
  <div class="card konfbox" style="margin-top:12px"><h2>Butir yang perlu dikonfirmasi lebih dulu</h2><ol id="konf"></ol></div>
  <div class="flt" id="flt">
    <div class="chips" id="fWho"><button class="chip on" data-v="all" type="button">Semua pihak</button><button class="chip" data-v="LGU" type="button">LGU</button><button class="chip" data-v="Pertamina" type="button">Pertamina</button><button class="chip" data-v="Bersama" type="button">Bersama</button></div>
    <select id="fPh" aria-label="Tahap"><option value="all">Semua tahap</option></select>
    <select id="fCat" aria-label="Kategori"><option value="all">Semua kategori</option></select>
    <select id="fSt" aria-label="Status"><option value="all">Semua status</option><option value="open">Belum selesai</option><option value="done">Selesai</option><option value="konf">Perlu konfirmasi</option></select>
    <input type="search" id="fQ" placeholder="Cari…" aria-label="Cari item">
  </div>
  <div id="list"></div>
  <div class="sign"><h2 style="font-size:13pt;margin:10px 0 6px">Pengesahan</h2>
    <table><tr><th>Disusun — PT LAPI Ganesha Utama</th><th>Disetujui — Pertamina RU IV Cilacap</th><th>Mengetahui — PT Pertamina Patra Niaga</th></tr>
    <tr><td>Nama:<br>Jabatan:<br>Tanggal:</td><td>Nama:<br>Jabatan:<br>Tanggal:</td><td>Nama:<br>Jabatan:<br>Tanggal:</td></tr></table></div>
</main>
<footer>Sumber: block diagram lingkup RU IV final 8 Okt 2026; Spesifikasi Material Instalasi GLD RU IV Cilacap rev 1.5; Pembagian Persiapan Instalasi RU IV Cilacap; pesan Pertamina Patra Niaga 21 Okt 2026 (spesifikasi PC server).</footer>
<script>
const PH=__PH__,IT=__IT__;
const KEY='gld-checklist-cilacap-v1';let S={};try{S=JSON.parse(localStorage.getItem(KEY))||{}}catch(e){}
const save=()=>{try{localStorage.setItem(KEY,JSON.stringify(S))}catch(e){}};
const st=id=>(S[id]&&S[id].st)||'Belum';
let F={who:'all',ph:'all',cat:'all',st:'all',q:''};
PH.forEach(p=>fPh.insertAdjacentHTML('beforeend',`<option value="${p[0]}">${p[1]} — ${p[2]}</option>`));
[...new Set(IT.map(i=>i.cat))].forEach(c=>fCat.insertAdjacentHTML('beforeend',`<option>${c}</option>`));
konf.innerHTML=IT.filter(i=>i.k).map(i=>`<li><b>${i.t}</b> <span>(${i.who} · ${i.id})</span></li>`).join('');
const esc=s=>s.replace(/&/g,'&amp;').replace(/</g,'&lt;');
function kpis(){
  const g=w=>{const a=IT.filter(i=>(w==='all'||i.who===w)&&st(i.id)!=='N/A');const d=a.filter(i=>st(i.id)==='Selesai').length;return[d,a.length]};
  kpisEl.innerHTML=[['all','Total'],['LGU','LGU'],['Pertamina','Pertamina (RU IV)'],['Bersama','Bersama']].map(([w,l])=>{const[d,n]=g(w),p=n?Math.round(d/n*100):0;
    return `<div class="card kpi"><div class="k">${l}</div><div class="v">${p}%</div><div class="s">${d} dari ${n} item selesai</div><div class="bar"><i style="width:${p}%"></i></div></div>`}).join('');
}
const kpisEl=document.getElementById('kpis');
function render(){
  const q=F.q.toLowerCase();
  const m=i=>(F.who==='all'||i.who===F.who)&&(F.ph==='all'||i.ph===F.ph)&&(F.cat==='all'||i.cat===F.cat)&&
    (F.st==='all'||(F.st==='done'&&st(i.id)==='Selesai')||(F.st==='open'&&!['Selesai','N/A'].includes(st(i.id)))||(F.st==='konf'&&i.k))&&
    (!q||(i.t+' '+i.d+' '+i.cat+' '+i.id).toLowerCase().includes(q));
  let h='';
  PH.forEach(p=>{const a=IT.filter(i=>i.ph===p[0]&&m(i));if(!a.length)return;
    const all=IT.filter(i=>i.ph===p[0]&&st(i.id)!=='N/A'),d=all.filter(i=>st(i.id)==='Selesai').length;
    h+=`<div class="ph"><h2>${p[1]}</h2><span>${p[2]}</span><span class="pc">${d}/${all.length} selesai</span></div>`;
    a.forEach(i=>{const s=S[i.id]||{},v=st(i.id);
      h+=`<div class="it ${v==='Selesai'?'done':''} ${v==='N/A'?'na':''}" data-id="${i.id}">
        <input type="checkbox" ${v==='Selesai'?'checked':''} aria-label="Selesai: ${esc(i.t)}">
        <div><div class="tt">${i.t}</div><div class="meta"><span class="id">${i.id}</span><span class="tag w-${i.who}">${i.who}</span><span class="tag cat">${i.cat}</span>${i.k?'<span class="tag konf">Perlu konfirmasi</span>':''}</div>
        <div class="d">${i.d}</div><textarea placeholder="Catatan / PIC / tanggal…" aria-label="Catatan ${i.id}">${esc(s.nt||'')}</textarea></div>
        <div class="side"><select aria-label="Status ${i.id}">${['Belum','Proses','Selesai','N/A'].map(o=>`<option${v===o?' selected':''}>${o}</option>`).join('')}</select></div></div>`})});
  list.innerHTML=h||'<div class="empty">Tidak ada item yang cocok dengan filter.</div>';kpis();
}
list.addEventListener('change',e=>{const r=e.target.closest('.it');if(!r)return;const id=r.dataset.id;S[id]=S[id]||{};
  if(e.target.type==='checkbox')S[id].st=e.target.checked?'Selesai':'Belum';else if(e.target.tagName==='SELECT')S[id].st=e.target.value;else return;save();render()});
list.addEventListener('input',e=>{if(e.target.tagName!=='TEXTAREA')return;const id=e.target.closest('.it').dataset.id;(S[id]=S[id]||{}).nt=e.target.value;save()});
fWho.onclick=e=>{const b=e.target.closest('.chip');if(!b)return;[...fWho.children].forEach(c=>c.classList.toggle('on',c===b));F.who=b.dataset.v;render()};
fPh.onchange=()=>{F.ph=fPh.value;render()};fCat.onchange=()=>{F.cat=fCat.value;render()};fSt.onchange=()=>{F.st=fSt.value;render()};fQ.oninput=()=>{F.q=fQ.value;render()};
csv.onclick=()=>{const rows=[['ID','Tahap','Kategori','Pihak','Item','Detail','Perlu konfirmasi','Status','Catatan']].concat(IT.map(i=>[i.id,PH.find(p=>p[0]===i.ph)[1],i.cat,i.who,i.t,i.d,i.k?'Ya':'',st(i.id),(S[i.id]||{}).nt||'']));
  const t='﻿'+rows.map(r=>r.map(c=>'"'+String(c).replace(/"/g,'""')+'"').join(',')).join('\r\n');
  const a=document.createElement('a');a.href=URL.createObjectURL(new Blob([t],{type:'text/csv'}));a.download='Checklist_Instalasi_GLD_Cilacap.csv';a.click()};
copy.onclick=()=>{const g=w=>{const a=IT.filter(i=>i.who===w&&st(i.id)!=='N/A');return `${a.filter(i=>st(i.id)==='Selesai').length}/${a.length}`};
  const open=IT.filter(i=>!['Selesai','N/A'].includes(st(i.id)));
  const t=`Checklist instalasi GLD RU IV Cilacap\nLGU ${g('LGU')} · Pertamina ${g('Pertamina')} · Bersama ${g('Bersama')} selesai\n\nBelum selesai (${open.length}):\n`+
    PH.map(p=>{const a=open.filter(i=>i.ph===p[0]);return a.length?`${p[1]}:\n`+a.map(i=>`- ${i.t} [${i.who}]${(S[i.id]||{}).nt?' — '+S[i.id].nt:''}`).join('\n'):''}).filter(Boolean).join('\n');
  (navigator.clipboard?navigator.clipboard.writeText(t):Promise.reject()).then(()=>{copy.textContent='Tersalin';setTimeout(()=>copy.textContent='Salin ringkasan',1800)},()=>alert(t))};
theme.onclick=()=>{const r=document.documentElement,dk=r.dataset.theme?r.dataset.theme==='dark':matchMedia('(prefers-color-scheme: dark)').matches;r.dataset.theme=dk?'light':'dark'};
render();
</script>
</body>
</html>
"""

OUT.write_text(HTML.replace("__PH__", json.dumps(PHASES, ensure_ascii=False))
               .replace("__IT__", json.dumps(ITEMS, ensure_ascii=False)), encoding="utf-8")
print(OUT, len(ITEMS), "item", {w: sum(i["who"] == w for i in ITEMS) for w in ("LGU", "Pertamina", "Bersama")})
