#!/usr/bin/env bash
# Copia a una carpeta (por defecto dist/) solo los ficheros que necesita la app.
# Lista blanca: nada de key, Demo docs ni material interno.
# En local el Makefile pasa una carpeta fuera de OneDrive, que no tolera carpetas que se crean y borran al momento.
set -euo pipefail
cd "$(dirname "$0")/.."
OUT="${1:-dist}"
rm -rf "$OUT" && mkdir -p "$OUT"
cp index.html "$OUT"/
for d in js locales prompts data "AI Use Case Suite — Logicalis_files"; do
  cp -R "$d" "$OUT"/
done
find "$OUT" -name '.DS_Store' -delete
find "$OUT" -name '*MacBook Air*' -delete
echo "$OUT: $(find "$OUT" -type f | wc -l | tr -d ' ') ficheros, $(du -sh "$OUT" | cut -f1)"
