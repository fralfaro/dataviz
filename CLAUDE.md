# CLAUDE.md

## Propósito
Biblioteca de gráficos, visualizaciones interactivas y animaciones para mis
clases (MAT281, ICS-294 y talleres). Cada pieza explica un solo concepto.

## Estructura
- `estaticas/`: Matplotlib y Seaborn (notebooks).
- `interactivas/`: Plotly y Altair (notebooks).
- `animaciones/`: escenas de Manim (.py).
- `web/`: visualizaciones con D3.js (HTML + JS puro, sin build).
- `exportados/`: archivos finales para slides.

## Estilo
- Español neutro y formal en títulos, ejes y comentarios.
- El título enuncia la conclusión, no el tema.
- Gris para el contexto, un solo color de acento para lo importante.
- Etiquetar series directamente; evitar leyendas y grillas pesadas.
- Tipografía grande (se proyecta en sala) y formato 16:9.
- Misma paleta en todas las herramientas.

## Convenciones
- Nombre de archivo = concepto que enseña, en minúsculas con guiones.
- Notebooks de `estaticas/` inician con `import tema; tema.aplicar()`.
- Última celda de cada notebook: exportar a `exportados/` (SVG y PNG).
- Semillas aleatorias fijas.
- D3: cada visualización en su propia carpeta, sin dependencias locales;
  D3 se carga desde CDN.

## Lo que me gusta
- 

## Lo que no me gusta
- 

## Pendientes
-