#!/usr/bin/env bash
set -e

# Carpetas
mkdir -p estaticas interactivas animaciones/escenas animaciones/media web exportados

# Archivos raíz
touch CLAUDE.md README.md requirements.txt

# estaticas (Matplotlib / Seaborn)
touch estaticas/tema.py
echo '{"cells":[],"metadata":{},"nbformat":4,"nbformat_minor":5}' > estaticas/plantilla.ipynb

# interactivas (Plotly / Altair)
echo '{"cells":[],"metadata":{},"nbformat":4,"nbformat_minor":5}' > interactivas/plantilla.ipynb

# animaciones (Manim)
touch animaciones/escenas/.gitkeep animaciones/media/.gitkeep

# web (D3.js)
touch web/index.html

# exportados
touch exportados/.gitkeep


echo "Estructura creada correctamente."
