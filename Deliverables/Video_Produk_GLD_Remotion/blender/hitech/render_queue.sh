#!/usr/bin/env bash
# Antrean render shot high-tech (landscape). bash render_queue.sh shot1 shot2 ...
B="/c/Program Files/Blender Foundation/Blender 5.2/blender.exe"
cd "$(dirname "$0")"
mkdir -p logs ../../public/blender/ht
for s in "$@"; do
  echo "[$(date +%H:%M)] mulai $s"
  "$B" -b --factory-startup -P "shot_$s.py" -- --out "../../public/blender/ht/$s.mp4" > "logs/$s.log" 2>&1
  echo "[$(date +%H:%M)] selesai $s: $(grep RENDER logs/$s.log | tail -1)"
done
