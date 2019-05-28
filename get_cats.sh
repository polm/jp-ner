#!/bin/bash
set -euo pipefail

cd $(dirname "$0")
outfile="$1"
infile="$2"

# generate pattern from file
pat=$(grep -v '^#' $infile | tr '\n' '|' | sed 's/.$//')
echo "$pat"
grep -E '^\[\[Category:.*の('$pat')\]\]$' jawiki.xml | \
  sed -e 's/..Category://' -e 's/..$//' | sort -u > $outfile

