#!/bin/bash

# --- Script para aumentar velocidad de un MP4 a 1.2x ---
# Uso: ./speed archivo.mp4

if [ -z "$1" ]; then
  echo "Uso: $0 archivo.mp4"
  exit 1
fi

INPUT="$1"

# Quitar extensión y generar nuevo nombre
BASENAME="${INPUT%.mp4}"
OUTPUT="${BASENAME}_1.2x.mp4"

echo "Procesando..."
echo "Archivo de entrada: $INPUT"
echo "Archivo de salida:  $OUTPUT"

# Velocidad de video y audio
VIDEO_SPEED="1.25"
AUDIO_SPEED="1.25"

ffmpeg -i "$INPUT" \
  -filter:v "setpts=PTS/${VIDEO_SPEED}" \
  -filter:a "atempo=${AUDIO_SPEED}" \
  "$OUTPUT"

echo "Listo. Archivo generado: $OUTPUT"
