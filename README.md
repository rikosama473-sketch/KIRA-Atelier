# KIRA Atelier — Anime Character Studio

KIRA Atelier es el taller personal para investigar, diseñar y montar personajes anime con **assets visuales reales y capas PNG**, no una promesa de generar capas perfectas con IA. Su dirección principal es un editor modular inspirado en los creadores de personajes tipo Picrew, acompañado por un atlas de referencias y herramientas locales de preparación.

## Los tres módulos

### KIRA Editor
Editor manual para abrir una imagen local, seleccionar zonas, extraer capas y preparar PNG. El procesamiento de píxeles sucede en el navegador del equipo. Todavía requiere trabajo para convertirse en un editor de personaje completo con categorías, biblioteca de capas independientes, previsualización y guardado de proyectos; no se debe confundir un recorte del personaje entero con una capa semántica de cabello, ojos o ropa.

- Interfaz: [tools/manual-character-editor](tools/manual-character-editor/)
- Guía: [README del editor](tools/manual-character-editor/README.md)
- Capas generadas de prueba: [generated/character-layers](generated/character-layers/)

### KIRA Atlas
Censo de fuentes visuales y peinados, con documentación de procedencia, calidad y licencias.

- [Atlas interactivo de peinados](trabajo%20aparte/atlas-peinados-interactivo.html)
- [Censo visual interactivo](trabajo%20aparte/censo-visual-interactivo.html)
- [Índice de referencias en JSON](trabajo%20aparte/indice-visual-componentes.json)
- [Segunda validación del censo](trabajo%20aparte/validacion-segunda-pasada-2026-10-22.md)

La última validación estructural registró 339 referencias canónicas, 315 URL de miniaturas y 58 registros PixAI. Las URL de miniatura son candidatas extraídas de las fuentes: no significa que todas se hayan cargado y revisado individualmente en el navegador del usuario. La deduplicación perceptual entre plataformas sigue pendiente.

### KIRA Forge
Herramientas auxiliares para preparar recortes, separar spritesheets y experimentar con variantes. Son opcionales: la ruta principal del editor no requiere entrenar una LoRA. Algunos flujos de variantes llaman servicios remotos y, por tanto, no deben presentarse como totalmente offline ni con disponibilidad garantizada.

- [Separación de capas](docs/CHARACTER_LAYER_SEPARATION.md)
- [Fábrica de assets](docs/CHARACTER_LAYER_ASSET_FACTORY.md)
- [Preparación de spritesheets](docs/SPRITE_LAYER_FACTORY.md)
- [Investigación de fuentes y recursos](docs/RESOURCE_HUNT.md)

## Puesta en marcha del editor

Usa Python 3 instalado y ejecuta desde la raíz del repositorio:

```bash
python tools/manual-character-editor/run_editor.py
```

El script abre un servidor local para la interfaz. Para comenzar, abre una imagen propia o una referencia cuyo uso tengas permitido. El editor puede preparar selecciones y exportarlas a PNG, pero la calidad y separación de cada región deben revisarse visualmente.

## Estado comprobado — 23 de octubre de 2026

- El código, las interfaces, los catálogos, las auditorías, las pruebas y 46 archivos de salida bajo `generated/character-assets/` y `generated/character-layers/` se trasladaron desde la rama de trabajo del repositorio anterior.
- Los PNG originales de la colección principal **todavía no están migrados**: los 759 archivos rasterizados del inventario anterior (aprox. 706,4 MB) permanecen en [el repositorio anterior `image`](https://github.com/rikosama473-sketch/image). Se conserva allí el original como fuente de respaldo y no se borró ni alteró.
- La licencia/precio de 96 registros del censo sigue sin confirmar. No existe una afirmación de que las imágenes de terceros sean redistribuibles o entrenables solo por aparecer en el catálogo.
- Las salidas en `generated/character-layers/pibara/39474458754/` son candidatas de trabajo. Sus propios nombres/manifiestos las identifican como candidatos: aún deben revisarse antes de considerarlas capas de producción.
- El proyecto prioriza el editor de capas y la biblioteca visual. La generación por modelo y el entrenamiento LoRA quedan como vías auxiliares, no como requisito para usar el editor.

## Derechos y conservación

No se debe redistribuir una referencia solo porque la miniatura sea pública. Cada asset incorporado al producto necesita una fuente, una licencia compatible, atribución cuando corresponda y una revisión separada para uso en la aplicación, redistribución y entrenamiento de IA. Los originales del usuario deben conservarse intactos.
