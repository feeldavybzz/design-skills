# Kit técnico: logos vectoriales y propuestas en HTML

El ejemplo funcional está en `strategies/v2/src/`:
- `logos.py` genera los SVG.
- `build.py` arma las páginas.
- `template.html` y `template-inversion.html` son las plantillas.

## Tipografías de Google como contornos

- Descarga el TTF estático de un peso y ancho concretos desde la API de CSS: `curl "https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@125,600"` y toma la URL `.ttf`. Funciona por el proxy del entorno.
- Guarda el TTF junto al generador. Las fuentes de Google tienen licencia OFL y se pueden incluir en el repo.
- Usa `uharfbuzz` para el shaping (kerning real) y `fontTools` (`SVGPathPen` con `TransformPen(1,0,0,-1,dx,0)`) para convertir cada glifo en un `path`. Instala ambos con `pip install fonttools uharfbuzz`.
- Para personalizar letras, reemplaza el glifo por un dibujo propio usando la caja del glifo original (`BoundsPen`) como medida, así el ritmo del nombre no se rompe.
- Calcula el `viewBox` con los límites reales. Los acentos (É) y los descendentes (g) necesitan más alto.
- Exporta los negativos con área de protección: márgenes de la mitad de la altura del isotipo.

## Trampas de SVG y CSS que ya costaron tiempo

- **Recorte con `<symbol>` y `<use>`:** si el símbolo tiene `viewBox="20 0 60 100"`, el SVG que lo usa debe llevar `viewBox="0 0 60 100"`. Si repite el origen del símbolo, el logo sale recortado.
- **Colorear el nodo dentro de un `<use>`:** usa `style="fill:var(--node,#EE8A22)"` en el símbolo y declara `--node` en el propio `<svg>`, con un color concreto. `--node:currentColor` declarado en un div padre no se resolvió como se esperaba.
- **Reglas que también tocan al SVG:** reglas como `.panel .art svg{height:auto}` pisan el tamaño de los logos anidados. Usa el combinador hijo (`>`).
- **Selectores de grilla:** `.toc div` también atrapa los div internos. Usa `.toc>div`.

## Revisar antes de publicar

- Usa Playwright con el Chromium preinstalado: `require('/opt/node22/lib/node_modules/playwright')`.
- Captura la página en segmentos de 1.500 a 3.000 px a 1280 (tema claro) y a 390 (tema oscuro), y revisa `scrollWidth`: no debe haber desborde horizontal.
- Para abrir páginas externas en Chromium, lánzalo con `proxy:{server:process.env.HTTPS_PROXY}`. Aun así, muchos dominios están bloqueados por política.

## Publicar

- **Artifact privado:** es para revisión interna. El usuario lo comparte desde el menú Share.
- **Carpeta `publico/`:** contiene solo la propuesta, envuelta en un documento completo, con `<meta name="robots" content="noindex">` y `_headers` con `X-Robots-Tag: noindex`. La página de precios no va ahí.
- **Cloudflare, opción 1 (subida manual):** Workers & Pages → Create → "Upload your static files" → nombre del proyecto → arrastrar la carpeta. El archivo debe llamarse exactamente `index.html` y estar en la raíz de la carpeta; si no, da HTTP 404, que es el error que nos pasó. Para actualizar, usa "Nueva implementación".
- **Cloudflare, opción 2 (desde Git):** conectar el repo, sin build command, con output directory `publico`. Cada push vuelve a publicar.
- **Si el repo es público**, todo lo que está en él (precios incluidos) es visible. Conviene que sea privado.
