# Strategies · Propuesta de identidad

Propuesta de MUKIWA DEPARTMENT para Strategies (soluciones empresariales). Sale del deck "Servicios Sept. 2026".

- `propuesta/index.html`: la propuesta completa. Incluye lectura del brief, tres rutas de isotipo, la construcción de la ruta A, versiones, color, tipografía, aplicaciones, preview web, índice del manual, inversión y lo que necesitamos del cliente.
- `logo/`: los isotipos en SVG (rutas A, B y C). Son geometría pura, sin fuentes.
- `tokens.css`: los colores, las tipografías y las medidas del logo.

El wordmark usa Archivo Expanded (Google Fonts). Hay que pasarlo a contornos cuando el cliente apruebe el nombre exacto (Strategies o Stratégies).

## Propuesta v2

La v2 sigue el método de `.claude/skills/branding/SKILL.md`: primero lo visual y después un cuestionario para que el cliente elija.

- `v2/index.html`: la propuesta publicada. Trae tres caminos (De S a S, Sello, Seis frentes), una tabla de puntuación, pruebas a escala real, el sistema, las aplicaciones, el mapa de la categoría, un cuestionario visual y la inversión por etapas.
- `v2/logo/`: el wordmark, el isotipo y las rutas en SVG, con sus versiones en negativo.
- `v2/src/`: los scripts que generan todo. `logos.py` traza el wordmark con Archivo Expanded SemiBold (licencia OFL) y dibuja las S propias; `build.py` arma la página a partir de `template.html`. Para regenerar: `pip install fonttools uharfbuzz && python3 v2/src/logos.py && python3 v2/src/build.py`.
