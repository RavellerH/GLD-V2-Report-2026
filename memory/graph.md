# Knowledge Graph — GLD V2

Graph relasi entitas proyek (Mermaid — render otomatis di GitHub & artifact). Versi machine-readable: [`graph.json`](graph.json).

## 1. Peta entitas (org → sub-sistem → perangkat/repo)

```mermaid
flowchart TD
  subgraph ORG[Organisasi]
    LGU[LAPI Ganesha Utama]
    ITBIOT[Lab IoT ITB]
    ITBFIS[Lab Fisika ITB]
    PTM[Pertamina Patra Niaga]
  end

  LGU -->|pelaksana| PROJ((Proyek GLD Tahap 2))
  ITBIOT -->|engineering/AI| PROJ
  ITBFIS -->|solar/energi| PROJ
  PTM -->|klien & partner| PROJ

  PROJ --> NET[Sub: Jaringan LoRa & CH]
  PROJ --> AI[Sub: AI & Sensor MQ]
  PROJ --> PWR[Sub: Catu Daya]
  PROJ --> CHM[Sub: Chamber/HW/QC]
  PROJ --> SW[Sub: Software/Server/Dashboard]
  PROJ --> INT[Sub: Integrasi Sistem]
  PROJ --> RUP[Sub: Survei RU / HSE]

  NET --> CH[CH: LoRa dual-channel + solar + 18650]
  NET --> GW[Gateway: MQTT uplink]
  AI --> NODE[GLD Node: ESP32-S3 + 8x MQ + TFLite]
  AI --> TCN[Model TCN LPG >=92%]
  PWR --> TPL[TPL5010 duty-cycle]
  PWR --> BQ[BQ25185 charger]
  PWR --> TPS[TPS63020 3V3]
  SW --> SRV[PC Server: Node-RED + Operator Hub]
  SW --> DASH[Dashboard: Next.js + MapLibre]

  NODE -. firmware .-> R_SRV
  CH -. firmware .-> R_SRV
  SRV -. flows .-> R_SRV
  DASH -. code .-> R_FE
  NODE -. edge ML .-> R_ML

  subgraph REPO[Repositori]
    R_FE[repo: gasleakdetectionV2-April]
    R_SRV[repo: PertaminaGLD]
    R_ML[repo: gas-leak-ml-chamber-system]
  end
```

## 2. Alur data end-to-end + pemetaan repo

```mermaid
flowchart LR
  NODE[GLD Node<br/>8x MQ + AI edge] -->|LoRa 915MHz STAR| CH[Cluster Head<br/>routing]
  CH -->|LoRa MESH| GW[Gateway<br/>aggregator]
  GW -->|WiFi/4G MQTT| SRV[PC Server<br/>Node-RED + Operator Hub]
  SRV -->|GraphQL| DASH[Dashboard<br/>MapLibre + Recharts]
  SRV -. downlink perintah/mode .-> NODE

  classDef ml fill:#E5E1F2,stroke:#6B54A6,color:#132A49;
  classDef net fill:#E0E9F4,stroke:#3E6EA5,color:#132A49;
  classDef app fill:#DBE5F1,stroke:#1D3B63,color:#132A49;
  class NODE ml
  class CH,GW,SRV net
  class DASH app
```
Repo: 🟪 ML edge (gas-leak-ml-chamber-system) · 🟦 firmware+server (PertaminaGLD) · 🟦navy dashboard (gasleakdetectionV2-April).

## 3. Dependensi blocker → kesiapan lapangan

```mermaid
flowchart TD
  BPWR[Blocker: autonomi baterai GLD<br/>7P = 1,76 hari] --> FIELD{Kesiapan Field<br/>RU IV Cilacap}
  BTPL[Blocker: TPL5010 belum optimal<br/>~0,4V saat off] --> FIELD
  BCONV[Blocker: DC converter] --> FIELD
  BLORA[Blocker: LoRa ~100m vs 1-2km] --> FIELD
  GATE[Gate: TRA/JSA belum disusun] --> SURVEY[Site survey fisik]
  SURVEY --> FIELD
  FIELD --> INSTALL[Field installation<br/>target Des 2026]

  DONE1[OK: uji fungsional + AI 16 Jul] -.penopang.-> FIELD
  DONE2[OK: CH power 2 panel surplus] -.penopang.-> FIELD

  classDef blk fill:#F5DEDB,stroke:#BC3B32,color:#3a1a16;
  classDef gate fill:#F4EAD3,stroke:#B0771B,color:#3a2e10;
  classDef ok fill:#DBEDE3,stroke:#2E7D57,color:#123227;
  class BPWR,BTPL,BCONV,BLORA blk
  class GATE gate
  class DONE1,DONE2 ok
```

## 4. Timeline milestone

```mermaid
timeline
  title Milestone GLD (2026)
  Apr–Mei : Uji node & routing CH : Failover star-mesh terbukti
  12 Jun : Kick-off Pertamina (baseline 9 bulan, 6 RU)
  6–9 Jul : Uji 2 CH : Rantai komunikasi GLD-CH-GW-Server
  15–16 Jul : TCN LPG >=92% : Uji fungsional + inferensi AI SELESAI : Analisis daya + mesh + downlink
  20–23 Jul : Simulasi duty-cycle : Repo Operator Hub/TPL5010
  Des 2026 : Target implementasi (field installation)
  Feb 2027 : Evaluasi & roadmap industrialisasi
```
