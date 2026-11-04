#!/usr/bin/env bash
# Render final semua versi (GLD & OGI, ID/EN, landscape/portrait) + salinan "_kirim" < 30 MB untuk WA.
#   bash tools/render_all.sh [GLD|OGI|all]
set -u
cd "$(dirname "$0")/.."
WHICH=${1:-all}
declare -a JOBS=()
[ "$WHICH" != OGI ] && JOBS+=("GLD-Explainer:GLD-Explainer_Landscape" "GLD-Explainer-EN:GLD-Explainer-EN_Landscape" "GLD-Explainer-Portrait:GLD-Explainer-Portrait" "GLD-Explainer-Portrait-EN:GLD-Explainer-Portrait-EN")
[ "$WHICH" != GLD ] && JOBS+=("OGI-Video:OGI-Video_Landscape" "OGI-Video-EN:OGI-Video-EN_Landscape" "OGI-Video-Portrait:OGI-Video-Portrait" "OGI-Video-Portrait-EN:OGI-Video-Portrait-EN")
for j in "${JOBS[@]}"; do
  id=${j%%:*}; name=${j##*:}
  echo "[$(date +%H:%M)] render $id"
  npx remotion render src/index.ts "$id" "out/$name.mp4" --log=error > "out/render_$name.log" 2>&1 || { echo "GAGAL $id"; tail -5 "out/render_$name.log"; continue; }
  dur=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "out/$name.mp4")
  # bitrate video agar total < 29 MB
  vb=$(python -c "print(int(29*8*1024/float('$dur') - 130))")
  ffmpeg -v error -y -i "out/$name.mp4" -c:v libx264 -preset medium -b:v ${vb}k -maxrate $((vb*2))k -bufsize $((vb*2))k -c:a aac -b:a 128k "out/${name}_kirim.mp4"
  echo "[$(date +%H:%M)] selesai $name ($(du -h "out/$name.mp4" | cut -f1), kirim $(du -h "out/${name}_kirim.mp4" | cut -f1))"
done
