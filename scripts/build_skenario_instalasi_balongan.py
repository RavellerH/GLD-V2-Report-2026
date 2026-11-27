# -*- coding: utf-8 -*-
"""Skenario Instalasi GLD RU VI Balongan — urutan kerja harian, hold point, energize, peralatan, risiko.

Output: Deliverables/Skenario_Instalasi_GLD_RU-VI_Balongan.docx (+ PDF via Word COM)
"""
import os

import docx
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Inches, Pt, RGBColor

import build_rencana_instalasi_balongan as R

OUT = os.path.join(R.ROOT, "Deliverables", "Instalasi_GLD_RU-VI_Balongan", "Skenario_Instalasi_GLD_RU-VI_Balongan.docx")
DOC_NO = "LGU/GLD/SI-BLG/2026-001"
REV = "0.4 (Draf)"
TANGGAL = "27 November 2026"


def header(d):
    s = d.sections[0]
    s.page_width, s.page_height = Inches(8.27), Inches(11.69)
    s.left_margin = s.right_margin = Inches(0.7)
    s.top_margin = Inches(1.15); s.bottom_margin = Inches(0.8); s.header_distance = Inches(0.35)
    t = s.header.add_table(rows=1, cols=3, width=Inches(6.87)); t.alignment = WD_TABLE_ALIGNMENT.CENTER
    c0, c1, c2 = t.rows[0].cells
    for c, w in zip(t.rows[0].cells, [Inches(1.5), Inches(3.87), Inches(1.5)]):
        c.width = w
    c0.paragraphs[0].add_run().add_picture(os.path.join(R.ASSET, "logo_lgu.png"), height=Inches(0.42))
    p = c1.paragraphs[0]; p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("PT LAPI GANESHA UTAMA"); r.bold = True; r.font.size = Pt(11)
    p2 = c1.add_paragraph(); p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p2.add_run("Skenario Instalasi GLD · RU VI Balongan").font.size = Pt(8)
    c2.paragraphs[0].add_run().add_picture(os.path.join(R.ASSET, "logo_pertamina.png"), height=Inches(0.3))
    c2.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
    fp = s.footer.paragraphs[0]; fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    fp.add_run(f"{DOC_NO} · Rev {REV} · Halaman ").font.size = Pt(8)
    R.page_field(fp)


def build():
    d = docx.Document()
    st = d.styles["Normal"]; st.font.name = "Calibri"; st.font.size = Pt(10)
    header(d)
    h, para, bullet, table, note, figure = R.h, R.para, R.bullet, R.table, R.note, R.figure

    tp = d.add_paragraph(); tp.alignment = WD_ALIGN_PARAGRAPH.CENTER; tp.paragraph_format.space_after = Pt(2)
    r = tp.add_run("SKENARIO INSTALASI"); r.bold = True; r.font.size = Pt(16); r.font.color.rgb = RGBColor.from_string(R.BLUE)
    tp = d.add_paragraph(); tp.alignment = WD_ALIGN_PARAGRAPH.CENTER; tp.paragraph_format.space_after = Pt(10)
    r = tp.add_run("Gas Leak Detection (GLD) Tahap 2 — Field Test RU VI Balongan"); r.bold = True; r.font.size = Pt(12)

    table(d, ["Item", "Keterangan"], [
        ("Nomor dokumen", DOC_NO), ("Revisi", REV), ("Tanggal", TANGGAL),
        ("Lokasi", "RU VI Balongan, Indramayu — lantai dasar struktur WHB, area terbuka di sisi WHB, atap carport gedung kantor"),
        ("Lingkup", "2 GLD (24 VDC), CH-01 (5 VDC, bawah struktur), CH-02 (panel surya, tiang 6 m), 1 Gateway (tepi atap carport), "
                    "1 junction box Ex d, PSU 24 VDC & 5 VDC di panel RU VI"),
        ("Acuan", "Rencana Instalasi GLD RU VI Balongan (LGU/GLD/RI-BLG/2026-001); daftar material/BoQ instalasi; "
                  "notulensi site survey 17 Nov 2026"),
    ], [1.6, 5.25])

    h(d, "1. Gambaran skenario")
    para(d, "Skenario ini menjabarkan urutan kerja instalasi dari persiapan di Bandung sampai serah terima di lokasi, termasuk prosedur langkah demi langkah per perangkat (bagian 6). "
            "Pekerjaan lapangan direncanakan 7 hari kerja setelah izin kerja terbit, dengan prinsip: pekerjaan mekanis dan "
            "pengkabelan selesai dan diperiksa lebih dulu, perangkat dipasang setelah jalur daya lolos uji, lalu energize "
            "bertahap dan commissioning per hop.")
    note(d, "Batasan keselamatan: GLD belum bersertifikat Ex. GLD hanya dipasang di titik yang disetujui HSE RU VI sebagai area "
            "risiko rendah (lantai dasar WHB, di bawah pipa gas kuning), tanpa baterai, catu 24 VDC saja. Seluruh pekerjaan "
            "mengikuti izin kerja (PTW) RU VI; pekerjaan panas, ketinggian dan kelistrikan memakai izin masing-masing.")
    figure(d, R.PLAN, "Gambar 1. Titik instalasi: GLD-01/02 & JB (lantai dasar WHB), CH-01 (bawah struktur), CH-02 (tiang 6 m), "
                      "GW-01 (tepi atap carport kantor).", Inches(6.6))

    h(d, "2. Tim dan peran di lapangan")
    table(d, ["Peran", "Jumlah", "Tugas utama"], [
        ("Supervisor LGU (pimpinan teknis)", "1", "Koordinasi dengan RU VI, toolbox meeting, QA tiap hold point, berita acara"),
        ("Engineer LGU (elektronik/IoT)", "1", "Terminasi di unit GLD/CH/GW, energize, konfigurasi, uji LoRa & server, commissioning"),
        ("Teknisi pelaksana", "2", "Pemasangan stanchion, bracket, JB, gland, penarikan & terminasi kabel, grounding"),
        ("Helper", "2", "Angkut material, bor/anchor, kebersihan area kerja"),
        ("Pendamping RU VI (operasi/HSE/listrik)", "sesuai PTW", "Penerbit izin kerja, gas test, LOTO panel, saksi uji & serah terima"),
    ], [2.3, 0.8, 3.75])
    para(d, "Pelaksana fisik dapat berasal dari RU VI/kontraktornya atau dari jasa instalasi LGU sesuai penawaran. LGU tetap "
            "melakukan supervisi teknis, QA dan pekerjaan elektrikal khusus GLD (terminasi unit, energize, commissioning).", size=9.5)

    h(d, "3. Persiapan sebelum mobilisasi (H-30 s/d H-1)")
    table(d, ["Waktu", "Kegiatan", "Keluaran", "PIC"], [
        ("H-30", "Konfirmasi final titik, rute kabel, jarak panel–JB, cara pasang CH-01, jalur data GW–PC server", "Rencana instalasi final disetujui RU VI", "LGU + RU VI"),
        ("H-30", "PO terminal box Helon HLBH31 (indent 2–4 minggu, satu-satunya item indent)", "JB tiba di gudang", "LGU"),
        ("H-10", "PO material lain ready stock (kirim 1–3 hari); fabrikasi stanchion, pelat U-bolt, bracket CH, siku GW di bengkel lokal 3–5 hari", "Material lengkap di gudang", "LGU / pelaksana"),
        ("H-21", "Pengajuan PTW, JSA, daftar personil & alat, sertifikat kompetensi (ketinggian, listrik)", "Draf izin kerja", "Pelaksana + RU VI"),
        ("H-14", "Uji fungsi perangkat di workshop: GLD, CH, GW, server — konfigurasi ID & kanal LoRa, burn-in 48 jam", "Perangkat siap pasang, log uji", "LGU"),
        ("H-7", "Pre-assembly: GLD ke pelat U-bolt, CH ke bracket, gland terpasang di entry JB; label kabel & titik", "Pekerjaan lapangan lebih singkat", "LGU + pelaksana"),
        ("H-3", "Packing & pengiriman ke RU VI; cek kelengkapan per titik (checklist Lampiran A)", "Material tiba di lokasi", "Pelaksana"),
        ("H-1", "Safety induction RU VI, pengecekan alat kerja, briefing tim", "Tim siap masuk area", "Semua"),
    ], [0.55, 3.3, 1.75, 1.25], size=8.4)

    h(d, "4. Urutan kerja di lapangan (7 hari kerja)")
    table(d, ["Hari", "Lokasi", "Kegiatan", "Hold point / cek QA"], [
        ("H1", "Semua titik", "Toolbox meeting, PTW aktif, gas test area. Verifikasi dan marking titik GLD-01, GLD-02, JB, CH-01, CH-02, GW-01; "
                              "ukur ulang rute kabel panel→JB→GLD/CH; cek ruang rel DIN & sumber 220 VAC di panel; cek utilitas di bawah lantai sebelum bor",
         "HP-1: titik & rute disetujui RU VI/HSE; panjang kabel aktual dicatat"),
        ("H2", "Lantai dasar WHB, sisi WHB", "Bor & chemical anchor pelat dasar stanchion GLD-01/02 (1 m), CH-01 (1,5 m) dan CH-02 (6 m); pasang JB di tengah antara GLD-01 & GLD-02",
         "Curing chemical anchor ± 24 jam sebelum stanchion dibebani; cek tegak lurus (waterpass)"),
        ("H3", "Atap carport kantor, panel RU VI", "Pasang siku L ± 0,5 m di tepi atap carport (kerja ketinggian ± 4 m); conduit & kabel NYY GW ke adaptor di dalam kantor. "
                                                   "Di panel (LOTO): pasang PSU 24 VDC & 5 VDC, fuse terminal F1 (24 VDC) & F2 (5 VDC), label",
         "HP-2: panel diperiksa listrik RU VI sebelum LOTO dilepas; siku GW kencang & kedap air"),
        ("H4", "Panel → JB → GLD/CH-01", "Tarik kabel armoured panel→JB (24 V & 5 V), JB→GLD-01, JB→GLD-02, JB→CH-01; klem kabel di struktur; "
                                         "pasang & kencangkan cable gland Ex d; terminasi di JB; grounding JB & stanchion",
         "HP-3: uji kontinuitas, polaritas & isolasi (megger 500 V) tiap jalur SEBELUM energize; semua entry JB terisi gland/plug"),
        ("H5", "Semua titik", "Mount GLD-01/02 ke stanchion, CH-01 ke bracket, CH-02 + 1 panel surya di tiang 6 m (kerja ketinggian), GW + antena di siku. "
                              "Energize bertahap sesuai bagian 5; terminasi & konfigurasi unit oleh LGU sesuai bagian 6",
         "HP-4: tegangan di terminal GLD 24 VDC ± 10 %, CH-01 5 VDC ± 5 %; tidak ada fuse putus"),
        ("H6", "Semua titik + PC server", "Commissioning C-1…C-7: RSSI per hop (GLD→CH-01→CH-02→GW), data normal sampai dashboard, alarm push "
                                         "dengan gas uji, temperature cut-off & fan sampling",
         "HP-5: seluruh kriteria C-1…C-7 terpenuhi dan disaksikan RU VI"),
        ("H7", "Semua titik", "Operasi kontinu 24 jam (C-8), perbaikan punch list, rapikan kabel & label, kebersihan area; "
                              "serah terima & berita acara",
         "HP-6: BA instalasi & commissioning ditandatangani; masa uji lapangan dimulai"),
    ], [0.45, 1.2, 3.25, 1.95], size=8.3)
    para(d, "Hari ke-2 dan ke-3 dapat dikerjakan paralel oleh dua regu bila izin kerja memungkinkan, sehingga pekerjaan lapangan "
            "bisa dipadatkan menjadi 6 hari.", size=9.5)

    h(d, "5. Urutan bring-up sistem")
    para(d, "Jaringan dihidupkan dari belakang ke depan: server → router → Gateway → CH-02 → CH-01 → GLD. Dengan urutan ini "
            "setiap perangkat yang baru dinyalakan langsung punya tujuan kirim data, sehingga gangguan dapat dilokalisasi per hop.")
    table(d, ["Urutan", "Perangkat", "Syarat sebelum lanjut ke perangkat berikutnya"], [
        ("1", "PC server", "Layanan broker MQTT, Node-RED, database dan dashboard berjalan; jam sistem benar"),
        ("2", "Router", "Wi-Fi 2,4 GHz aktif; PC server mendapat IP tetap dan dashboard dapat dibuka dari laptop"),
        ("3", "Gateway GW-01", "Terhubung ke Wi-Fi router dan tersambung ke broker; status online di dashboard"),
        ("4", "CH-02", "Bergabung ke mesh dan terlihat oleh Gateway; RSSI CH-02 → GW memenuhi kriteria"),
        ("5", "CH-01", "Terhubung ke CH-02; RSSI CH-01 → CH-02 memenuhi kriteria"),
        ("6", "GLD-01, GLD-02", "Data normal masuk dashboard lewat CH-01; nulling 8/8 selesai; alarm uji tampil di server"),
    ], [0.65, 1.3, 4.9], size=8.6)
    figure(d, os.path.join(R.RB, "skenario_S2_jaringan.png"), "Gambar S-2. Diagram jaringan dan alur data: GLD → CH-01 → CH-02 → GW-01 (LoRa) → router (Wi-Fi) → PC server (LAN).", Inches(6.6))
    figure(d, os.path.join(R.RB, "skenario_S1_satu_garis.png"), "Gambar S-1. Diagram satu garis catu daya: PSU & fuse di panel RU VI → 1 kabel NYFGbY 4×1,5 mm² (24 V & 5 V) → JB Ex d → GLD-01, GLD-02, CH-01.", Inches(6.6))
    figure(d, os.path.join(R.RB, "skenario_S8_cable_layout.png"), "Gambar S-8. Layout cable (isometrik) dan cable schedule format MoC — lembar 1/2 gambar LGU/GLD/CS-BLG/2026-001 (A3: Cable_Schedule_GLD_RU-VI_Balongan.pdf).", Inches(6.85))
    figure(d, os.path.join(R.RB, "skenario_S8_cable_schedule.png"), "Gambar S-9. Cable schedule rinci (jenis kabel, inti, gland asal/tujuan) dan diagram routing — lembar 2/2.", Inches(6.85))
    figure(d, os.path.join(R.RB, "skenario_S7_jb.png"), "Gambar S-7. Tata letak junction box (JB) 4-way dan entry kabel E1–E4.", Inches(5.6))
    para(d, "Urutan energize daya kabel di lapangan (panel → JB): HP-3 lulus → lepas LOTO di hadapan petugas listrik RU VI → "
            "PSU dinyalakan tanpa beban dan diukur → semua fuse dilepas, unit diterminasi di JB satu per satu (CH-01 dulu, lalu GLD-01, "
            "GLD-02); setiap kali satu unit tersambung, fuse dipasang dan tegangan diukur di terminal JB & unit, lalu fuse dilepas lagi "
            "sebelum menyambung unit berikutnya (F1 = 24 VDC, F2 = 5 VDC; percabangan di JB, lihat Gambar S-1).", size=9.5)

    def proc(title, intro, rows, fig=None, cap=None, w=6.6):
        h(d, title, 2)
        if intro:
            para(d, intro, size=9.5)
        if fig:
            figure(d, os.path.join(R.RB, fig), cap, Inches(w))
        table(d, ["No", "Langkah", "Detail & kriteria", "PIC"], rows, [0.35, 1.45, 3.9, 1.15], size=8.3)

    h(d, "6. Prosedur instalasi per perangkat")
    proc("6.1 GLD-01 dan GLD-02 (lantai dasar WHB, di bawah pipa gas kuning)",
         "Casing yang dipakai: tipe mesh sensor di depan (tutup depan bermesh); tipe mesh di bawah belum disetujui dan tidak dipakai. Dilakukan identik untuk kedua unit. JB berada di tengah antara GLD-01 dan GLD-02 (± 22 m antar-GLD); kabel JB → masing-masing GLD ± 16 m.", [
        ("1", "Persiapan di workshop", "Unit lolos uji fungsi & burn-in; catat nomor seri, versi firmware & model, ID perangkat, kanal LoRa "
                                       "(920–921 MHz) dan CH tujuan (CH-01); pre-assembly unit ke pelat U-bolt SS304; lindungi mesh depan saat transport", "LGU"),
        ("2", "Pemeriksaan kedatangan", "Casing, mesh sensor, antena, alarm lokal dan gland tidak rusak; kelengkapan sesuai Lampiran A; foto dokumentasi", "LGU"),
        ("3", "Marking & cek lantai", "Titik sesuai Rencana Instalasi (persetujuan HSE); deteksi utilitas di bawah lantai; jarak bebas dari sumber panas", "Pelaksana + RU VI"),
        ("4", "Pasang stanchion 1 m", "Bor lantai beton, chemical anchor 4 titik, pelat dasar 240×240×10; curing ± 24 jam; tegak lurus (waterpass); grounding stanchion", "Pelaksana"),
        ("5", "Pasang unit", "Pelat U-bolt diklem ke stanchion (U-bolt M10 dikencangkan merata); mesh sensor di tutup depan menghadap keluar (ke area pantau, menjauhi tiang), tidak tertutup; "
                             "antena tegak, tidak terhalang struktur logam", "Pelaksana, QA LGU"),
        ("6", "Kabel & gland", "Kabel armoured JB → GLD ditarik dan diklem; gland Ex d M20 di sisi GLD & JB, armour dijepit di cone gland; drip loop sebelum masuk unit", "Pelaksana"),
        ("7", "Terminasi di unit", "Konduktor L+ / L− ke terminal 24 VDC (ferrule), PE ke terminal earth; cek polaritas dengan multimeter; kencangkan dengan torsi yang ditetapkan; "
                                   "terminal BAT dibiarkan kosong (operasi tanpa baterai)", "LGU"),
        ("8", "Energize", "Fuse F1 (24 VDC) dipasang; tegangan di terminal 24 VDC ± 10 % saat fan aktif; tidak ada indikasi fault", "LGU"),
        ("9", "Warm-up & nulling", "Tunggu pemanasan sensor; jalankan mode Nulling di udara bersih — wajib hasil 8/8 sensor; ulangi bila ada sensor gagal", "LGU"),
        ("10", "Mode operasi", "Kembalikan ke mode Inference; pastikan data normal tampil di dashboard dengan ID & Area yang benar", "LGU"),
        ("11", "Uji alarm", "Paparan gas uji terkendali (sesuai izin RU VI) → alarm lokal menyala & alarm push masuk server tanpa pull request; catat waktu respons", "LGU, disaksikan RU VI"),
        ("12", "Uji cut-off & fan", "Temperature cut-off aktif sesuai setelan; fan hanya berputar saat sampling", "LGU"),
        ("13", "Penutupan", "Tutup cover rapat, cek seal; label titik & kabel; foto as-built; isi lembar commissioning per unit", "LGU + pelaksana"),
    ], fig="skenario_S3_gld.png", cap="Gambar S-3. Detail pemasangan GLD di stanchion 1 m: tampak samping dan tampak depan pelat U-bolt.", w=6.6)
    proc("6.2 CH-01 (di antara kedua GLD, bawah struktur, stanchion sendiri 1,5 m, catu 5 VDC)",
         "CH-01 menerima data dari GLD-01 dan GLD-02 lalu meneruskannya ke CH-02. Tidak memakai panel surya karena berada di bawah struktur.", [
        ("1", "Persiapan di workshop", "Konfigurasi ID, kanal, peran (serving CH untuk GLD-01/02) dan tujuan mesh (CH-02); uji fungsi", "LGU"),
        ("2", "Marking & cek lantai", "Titik di tengah antara GLD-01 dan GLD-02; deteksi utilitas di bawah lantai; ruang bebas di atas antena", "LGU + RU VI"),
        ("3", "Pasang stanchion & bracket", "Stanchion sendiri 2\" HDG 1,5 m: bor & chemical anchor pelat dasar, curing ± 24 jam, tegak lurus, grounding; bracket CH + 2 U-bolt M10 ke stanchion", "Pelaksana"),
        ("4", "Kabel & gland", "Kabel armoured JB → CH-01 (± 14 m) ditarik & diklem ke stanchion; gland Ex d di sisi JB dan gland di sisi CH", "Pelaksana"),
        ("5", "Terminasi & energize", "+5 V / 0 V ke terminal CH; fuse F2 (5 VDC) dipasang; tegangan 5 VDC ± 5 % saat transmit", "LGU"),
        ("6", "Uji link", "CH-01 bergabung ke mesh lewat CH-02; RSSI CH-01 → CH-02 dan GLD → CH-01 lebih baik dari −90 dBm; tidak ada paket hilang beruntun", "LGU"),
        ("7", "Penutupan", "Antena dikencangkan, cover rapat, label, foto as-built", "LGU + pelaksana"),
    ], fig="skenario_S4_ch01.png", cap="Gambar S-4. Detail pemasangan CH-01 di stanchion sendiri 1,5 m.", w=5.2)
    proc("6.3 CH-02 (luar struktur, tiang 6 m, panel surya)",
         "CH-02 menjadi jembatan antara klaster WHB dan Gateway (± 37 m ke CH-01, ± 78 m ke GW-01). Seluruh perakitan dilakukan di bawah, lalu tiang didirikan.", [
        ("1", "Persiapan di workshop", "Konfigurasi ID & tujuan mesh (GW-01); baterai CH diisi penuh; uji fungsi bersama panel surya", "LGU"),
        ("2", "Pondasi", "Pelat dasar tiang di-anchor ke beton (chemical anchor), curing ± 24 jam; grounding pelat/tiang", "Pelaksana"),
        ("3", "Uji link sebelum tiang permanen", "Pegang CH-02 di ketinggian kerja di titik rencana; cek RSSI ke GW-01 dan CH-01 — geser titik bila lemah", "LGU"),
        ("4", "Rakit di bawah", "Pada tiang yang masih rebah: pasang bracket CH (± 4,2 m) dan bracket + 1 panel surya DI BAWAH unit CH (± 2,5 m, agar tidak menghalangi antena LoRa); panel menghadap utara dengan kemiringan ± 10–15°; "
                                "kabel panel → CH dirapikan dengan klem UV", "Pelaksana, QA LGU"),
        ("5", "Dirikan tiang", "Tiang 6 m didirikan dengan izin kerja ketinggian, minimal 3 orang + tali pengarah; baut ke pelat dasar, cek tegak", "Pelaksana"),
        ("6", "Nyalakan & cek daya", "Tegangan pengisian dari panel surya dan tegangan baterai tercatat; status daya CH tampil di dashboard", "LGU"),
        ("7", "Uji link", "RSSI CH-02 → GW-01 dan CH-01 → CH-02 memenuhi kriteria; data dari CH-01 diteruskan sampai server", "LGU"),
        ("8", "Penutupan", "Label, foto as-built, catat orientasi & kemiringan panel", "LGU + pelaksana"),
    ], fig="skenario_S5_ch02.png", cap="Gambar S-5. Detail pemasangan CH-02 di stanchion 6 m: CH ± 4,2 m, 1 panel surya ± 2,5 m di bawahnya.", w=5.2)
    proc("6.4 Gateway GW-01 (tepi atap carport kantor, ± 4 m)",
         "Gateway menerima data dari mesh LoRa dan meneruskannya ke broker MQTT di PC server lewat router. Daya 5 VDC dari adaptor di dalam kantor.", [
        ("1", "Persiapan di workshop", "Konfigurasi ID Gateway, SSID/password Wi-Fi router, alamat IP & port broker, kredensial MQTT; catat MAC address", "LGU"),
        ("2", "Pasang siku", "Siku L ± 0,5 m + kaki dibaut ke tepi atap carport (baut/klem SS304 + sealant, tanpa las); kerja ketinggian dengan harness", "Pelaksana"),
        ("3", "Pasang Gateway & antena", "Enclosure GW di atas siku, antena tegak di atas GW, tidak terhalang atap/talang; konektor antena diberi pelindung cuaca", "Pelaksana, QA LGU"),
        ("4", "Kabel daya", "Kabel NYY 2×1,5 mm² (± 22 m) dalam conduit dari GW ke adaptor di dalam kantor; drip loop di GW; tembusan dinding disegel", "Pelaksana"),
        ("5", "Catu daya", "Adaptor 5 VDC ke stopkontak (sebaiknya UPS kantor); ukur 5 VDC di terminal GW", "LGU"),
        ("6", "Uplink", "GW terhubung ke Wi-Fi router (cek kuat sinyal Wi-Fi di posisi GW) dan ke broker; status online di dashboard", "LGU"),
        ("7", "Uji downlink LoRa", "GW menerima CH-02; uji pull data normal dan push alarm dari server sampai ke GLD", "LGU"),
    ], fig="skenario_S6_gateway_server.png", cap="Gambar S-6. Gateway di tepi atap carport, router dan PC server di dalam kantor (berlaku juga untuk 6.5 dan 6.6).", w=6.6)
    proc("6.5 Router jaringan lokal (di dalam kantor)",
         "Router disediakan LGU, membentuk jaringan lokal tertutup antara Gateway dan PC server tanpa akses internet.", [
        ("1", "Persiapan di workshop", "Firmware diperbarui; password admin diganti; Wi-Fi 2,4 GHz WPA2 dengan SSID proyek; DHCP reservation untuk MAC Gateway; "
                                       "IP tetap untuk PC server; WAN/internet tidak dipakai", "LGU"),
        ("2", "Penempatan", "Di dalam kantor sedekat mungkin dengan sisi carport (dekat jendela) agar sinyal Wi-Fi ke GW kuat; di atas meja/rak, bukan di lantai", "LGU + RU VI"),
        ("3", "Daya", "Ke UPS kantor bila tersedia", "LGU"),
        ("4", "Sambungan", "Router → PC server dengan kabel LAN Cat6", "LGU"),
        ("5", "Uji", "Laptop dapat membuka dashboard lewat Wi-Fi; Gateway mendapat IP sesuai reservasi; tidak ada jaringan lain yang terhubung", "LGU"),
    ])
    proc("6.6 PC server lokal",
         "PC server menjalankan broker MQTT, Node-RED, database dan aplikasi dashboard. Lokasi PC mengikuti kesepakatan dengan RU VI (kantor yang sama dengan router).", [
        ("1", "Persiapan di workshop", "Instal paket aplikasi (broker MQTT, Node-RED, backend & frontend dashboard, database); registrasi perangkat GLD-01, GLD-02, "
                                       "CH-01, CH-02, GW-01 dengan kolom Area; akun pengguna; uji end-to-end dengan perangkat yang sama", "LGU"),
        ("2", "Penempatan & daya", "Di ruang kantor yang disepakati, ke UPS; ventilasi cukup; label perangkat", "LGU + RU VI"),
        ("3", "Jaringan", "NIC-1 ke router proyek (IP tetap). NIC-2 ke intranet kantor RU VI hanya bila disetujui IT RU VI, dan hanya untuk akses dashboard", "LGU + IT RU VI"),
        ("4", "Nyalakan layanan", "Broker, Node-RED, database dan dashboard berjalan otomatis setelah reboot; jam sistem disinkronkan", "LGU"),
        ("5", "Uji data", "Data normal setiap GLD tampil sesuai interval; alarm push tampil dan memicu notifikasi; riwayat tersimpan di database", "LGU"),
        ("6", "Keamanan & backup", "Password default diganti; port hanya yang diperlukan; backup konfigurasi & database awal disimpan", "LGU"),
        ("7", "Serah terima", "Akun operator RU VI dibuat; panduan singkat dashboard diserahkan; kontak dukungan LGU", "LGU + RU VI"),
    ])

    h(d, "7. Peralatan kerja")
    table(d, ["Kelompok", "Peralatan"], [
        ("Mekanis", "Bor beton + mata bor, chemical anchor & dispenser, kunci torsi, kunci pas/ring, waterpass, meteran laser, gerinda (bila diizinkan PTW panas)"),
        ("Kelistrikan", "Multimeter, insulation tester (megger) 500 V, tang kabel & stripper armour, crimping tool & ferrule, heat gun, label printer"),
        ("Ketinggian", "Tangga/scaffold ringan untuk tiang 6 m dan atap carport ± 4 m, full body harness, tali penurun barang"),
        ("Uji & konfigurasi", "Laptop konfigurasi, kabel USB, LoRa tester/node uji, gas uji (sesuai izin RU VI), router & PC server"),
        ("K3", "APD lengkap (helm, kacamata, sarung tangan, sepatu safety, wearpack), gas detector portabel pendamping, P3K, rambu & barikade"),
    ], [1.4, 5.45], size=8.6)

    h(d, "8. Risiko dan antisipasi")
    table(d, ["Risiko", "Dampak", "Antisipasi"], [
        ("Izin kerja terlambat", "Jadwal mundur", "Ajukan PTW sejak H-21; pekerjaan non-area (pre-assembly, uji workshop) tetap jalan"),
        ("Jarak panel–JB lebih jauh dari asumsi", "Kabel kurang", "Ukur di H1; kabel dibeli dengan cadangan 10 % + 1 roll cadangan"),
        ("Hujan", "Pekerjaan atap & kabel terhenti", "Dahulukan pekerjaan di bawah struktur WHB yang beratap"),
        ("Utilitas di bawah lantai", "Bor mengenai kabel/pipa", "Cek gambar & detektor sebelum bor (HP-1); geser titik bila perlu"),
        ("RSSI hop CH-02→GW lemah", "Data hilang", "Uji link sebelum CH-02 dipasang permanen; tinggikan antena atau geser CH-02"),
        ("Panas/getaran dari WHB", "Sensor terganggu", "Titik GLD tetap di area bersuhu aman; temperature cut-off aktif"),
        ("Kerja ketinggian", "Jatuh", "Izin ketinggian, harness, pengawas; pasang panel surya di bawah lalu dinaikkan"),
    ], [1.8, 1.4, 3.65], size=8.6)

    h(d, "Lampiran A — Checklist material per titik")
    table(d, ["Titik", "Material & perangkat"], [
        ("Panel RU VI", "PSU 24 VDC 2,5 A, PSU 5 VDC, 3 terminal fuse, terminal block, label"),
        ("JB (tengah, antara GLD-01 & GLD-02)", "Terminal box Ex d 4 entry M20 (Helon HLBH31), 4 cable gland Ex d M20, terminal 4 kutub, earth tag"),
        ("GLD-01 / GLD-02", "Unit GLD, stanchion 2\" 1 m + pelat dasar & anchor, pelat U-bolt SS304 + 2 U-bolt M10, 1 cable gland, kabel armoured"),
        ("CH-01", "Unit CH, stanchion 2\" 1,5 m + pelat dasar & anchor, bracket CH + 2 U-bolt M10, 1 cable gland, kabel armoured, grounding"),
        ("CH-02", "Unit CH, 1 panel surya + bracket (di bawah CH), stanchion 2\" 6 m + pelat dasar & anchor, bracket CH"),
        ("GW-01", "Gateway + antena, adaptor 5 VDC, siku L ± 0,5 m + baut/klem SS304, kabel NYY ± 22 m, conduit & klem"),
        ("Server", "PC server lokal, router, kabel LAN"),
    ], [1.6, 5.25], size=8.6)

    d.save(OUT)
    print("written", OUT)


if __name__ == "__main__":
    build()
