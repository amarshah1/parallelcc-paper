#!/usr/bin/env bash
#
# Assemble the FMCAD 2026 camera-ready upload for EasyChair (paper #180).
#
# Produces  paper180-camera-ready.zip  with exactly the structure the
# proceedings chair requires:
#
#   paper180.pdf       - camera-ready PDF
#   copyright180.pdf   - signed copyright form
#   artifact180.txt    - artifact DOI (10.5281/zenodo.20133810)
#   src/               - LaTeX sources (must compile without --shell-escape)
#
# Usage:  ./zip_camera_ready.sh
#
# The staged files live in ./camera-ready/.  Drop the signed copyright form
# in as  camera-ready/copyright180.pdf  before running.
set -euo pipefail

PAPER=180
ROOT="$(cd "$(dirname "$0")" && pwd)"
STAGE="$ROOT/camera-ready"
ZIP="$ROOT/paper${PAPER}-camera-ready.zip"

required=(
  "paper${PAPER}.pdf"
  "copyright${PAPER}.pdf"
  "artifact${PAPER}.txt"
  "src"
)

missing=0
for f in "${required[@]}"; do
  if [[ ! -e "$STAGE/$f" ]]; then
    echo "  MISSING: camera-ready/$f" >&2
    missing=1
  fi
done
if [[ $missing -ne 0 ]]; then
  {
    echo
    echo "Cannot build the zip until the items above exist."
    echo "In particular, save the signed copyright form as:"
    echo "    $STAGE/copyright${PAPER}.pdf"
  } >&2
  exit 1
fi

rm -f "$ZIP"
(
  cd "$STAGE"
  zip -r -X "$ZIP" \
    "paper${PAPER}.pdf" \
    "copyright${PAPER}.pdf" \
    "artifact${PAPER}.txt" \
    src \
    -x '*.DS_Store' \
       'src/*.aux' 'src/sections/*.aux' 'src/*.log' 'src/*.out' \
       'src/*.bbl' 'src/*.blg' 'src/*.synctex.gz' 'src/*.xmpdata' \
       'src/*.xmpi' 'src/*.fls' 'src/*.fdb_latexmk'
)

echo
echo "Built: $ZIP"
echo "=== contents ==="
unzip -l "$ZIP"
