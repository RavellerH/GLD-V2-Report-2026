#!/usr/bin/env bash
# Render final semua shot 3D untuk satu orientasi ke public/blender[/portrait]/.
#   bash run_final.sh landscape|portrait
set -u
ORIENT=${1:-landscape}
B="/c/Program Files/Blender Foundation/Blender 4.5/blender.exe"
HERE="$(cd "$(dirname "$0")" && pwd)"
OUT="$HERE/../public/blender"; [ "$ORIENT" = portrait ] && OUT="$OUT/portrait"
mkdir -p "$OUT" "$HERE/logs"
run() { local name=$1; shift; echo "[$(date +%H:%M)] mulai $name"; "$B" -b -P "$@" > "$HERE/logs/final_${ORIENT}_${name}.log" 2>&1; echo "[$(date +%H:%M)] selesai $name (exit $?)"; }
run leak     "$HERE/build_outro.py"     -- "$OUT" leak "$ORIENT" --final
run shot2    "$HERE/build_gld_model.py" -- "$OUT" final 24 "$ORIENT"
run chamber  "$HERE/build_chamber.py"   -- "$OUT" final 24 "$ORIENT"
run outro    "$HERE/build_outro.py"     -- "$OUT" anim "$ORIENT" --final
ls -la "$OUT"
