# Revisión de referencias modulares y licencias — 28 de octubre de 2026

**Proyecto:** KIRA Atelier  
**Módulo:** KIRA Atlas  
**Lote original:** tres fuentes oficiales para composición por capas; ampliado el 28/10 con dos referencias oficiales a texturas de cabello VRoid.  
**Objetivo:** añadir referencias trazables y separar su valor arquitectónico de su permiso de incorporación al editor.

## Resumen de decisiones

| ID | Fuente | Miniatura | Licencia y uso recomendado |
|---|---|---|---|
| `EXT-OGA-002` | [Anime Girl and Boy Portraits — stevenburrow](https://opengameart.org/content/anime-girl-and-boy-portraits) | La página no ofrece una miniatura propia del arte; se deja sin imagen en lugar de reutilizar el icono genérico de comentarios. | La página oficial marca CC0 y el autor declara dominio público. El ZIP lista muestras y archivo XCF; no se inspeccionó el archivo en esta tanda. **Candidato para extracción local**, pendiente de revisar el XCF, bordes y capas femeninas. |
| `EXT-BOOTH-011` | [Deformed Girl Mix-and-Match Standee Material — Mirror Image](https://booth.pm/ja/items/2720171) | **Inspeccionada visualmente el 28/10.** La portada muestra varios personajes chibi completos y texto japonés; no muestra piezas aisladas. | La ficha permite uso personal/comercial y modificaciones, no exige crédito, pero prohíbe redistribuir el material incluso tras modificarlo. **Solo referencia de arquitectura/estilo; no empaquetar capas en KIRA sin permiso expreso.** |
| `EXT-ITCH-012` | [Modular Pixel Characters — Character Creator Pack](https://riclmbr.itch.io/modular-pixel-characters-character-creator-pack-350-items-48x48) | La URL es la portada Open Graph oficial; el archivo exacto no se pudo abrir para inspección visual. **Pendiente.** | La página declara CC0 1.0, 350 piezas modulares, 700 hojas de cabello y un manifiesto de capas. Precio mínimo visible: USD 4,21. Es un **candidato técnico** para estudiar orden/manifiesto de capas, no arte final anime. No se ha descargado el ZIP. |
| `EXT-BOOTH-012` | [VRoid向け アニメ風髪テクスチャ — Team Aether Shop](https://booth.pm/ja/items/1280998) | **Inspeccionada visualmente el 28/10.** La portada muestra cabeza y rostro anime con texto japonés, no una textura aislada. | La ficha permite uso comercial y modificaciones, pero prohíbe redistribuir la textura. Referencia de color y capas base/sombra/brillo; **no empaquetar los archivos fuente**. |
| `EXT-BOOTH-013` | [アニメっぽい髪テクスチャ — Ruliyna Shop](https://booth.pm/en/items/2159602) | **Inspeccionada visualmente el 28/10.** El preview muestra una muestra de textura rosa/lila con la marca “SAMPLE”. | La ficha permite aplicar la textura a modelos comerciales, pero prohíbe redistribuir/vender el archivo y restringe modificarlo para distribución. **Solo referencia de pipeline VRoid**, no peinado PNG para KIRA Editor. |

## 1. OpenGameArt — Anime Girl and Boy Portraits (CC0)

La ficha oficial marca **CC0** y declara que el paquete contiene dos retratos femeninos, dos masculinos, variaciones de peinado, coleta, ojos y boca, junto con muestras y un proyecto XCF de GIMP. El autor aclara que todavía no ha extraído las partes individuales; habría que ocultar capas y exportar los recortes necesarios. La página no contiene una vista previa específica del recurso y solo enlaza el ZIP, por lo que no se ha empleado un logo/icono genérico como sustituto. El archivo no se ha descargado ni inspeccionado. Antes de incorporarlo como candidato técnico, revisar la jerarquía real de capas, exportar solo las piezas femeninas requeridas y comprobar los bordes, ya que los comentarios del propio recurso mencionan artefactos blancos tras rellenar colores.

Fuente primaria: [OpenGameArt — Anime Girl and Boy Portraits](https://opengameart.org/content/anime-girl-and-boy-portraits).

## 2. Mirror Image — material chibi combinable

La página oficial de BOOTH describe cabello, ropa y rostro combinables; un PSD compatible con PSDTool con variaciones por pieza, además de PNG de expresiones. La demo gratuita figura como 85,4 MB y 850×1204 px; la versión completa, ¥550 y 1771×2508 px. El propio anuncio indica que la diferencia principal entre ambas versiones es el tamaño.

La portada oficial se abrió y se comprobó visualmente: es una composición promocional con varios personajes completos, rótulos y vestuario. No se cuentan como capas independientes ni se usan para afirmar que cada elemento del PSD esté aprobado para distribución. La descripción oficial permite modificar el material y usarlo en obras comerciales, pero prohíbe redistribuirlo incluso después de modificarlo. Para KIRA es útil como estudio de flujo y combinación, no como recurso importable al paquete del editor.

Fuente primaria: [ficha oficial de BOOTH](https://booth.pm/ja/items/2720171).

## 3. Riclmbr — Modular Pixel Characters

La ficha actual declara 350 artículos en siete categorías, 50 peinados en catorce colores, capas traseras separadas y un archivo `layers.json` con cuadrícula, velocidad y orden de capas. El formato descrito es una hoja de sprites de 48×48, con cuatro direcciones y siete animaciones; incluye también 24 personajes ya fusionados.

La licencia mostrada en la ficha es **CC0 1.0**, con uso comercial y sin obligación de atribución. El precio mínimo que aparece en la página durante esta revisión es USD 4,21. No se descargó el ZIP: por eso no se han verificado los nombres reales de cada archivo ni el orden práctico del manifiesto. Además, la estética pixel-art chibi/top-down no coincide con el objetivo principal de KIRA de montar personajes anime de alta resolución. La recomendación queda limitada a un futuro fixture o prototipo técnico local, sujeto a inspección del paquete.

La imagen Open Graph fue identificada en los metadatos de la página oficial, pero no se pudo abrir el archivo exacto durante esta comprobación; su estado visual queda pendiente.

Fuente primaria: [ficha oficial de itch.io](https://riclmbr.itch.io/modular-pixel-characters-character-creator-pack-350-items-48x48).

## 4. Team Aether Shop — textura de cabello anime para VRoid

La ficha oficial ofrece una prueba gratuita con 9 PNG (3 patrones × 3 colores), un pack PNG de 35 variantes (5 patrones × 7 colores, ¥200) y un paquete PSD/CLIP de ¥400 con capas separadas de base, sombras y reflejos. La portada oficial se abrió y comprobó visualmente: muestra la cabeza de un personaje anime y un rótulo japonés grande. No es una lámina capilar aislada ni una prueba de que los archivos se puedan integrar en un creador redistribuible.

Las condiciones del vendedor permiten modificar y usar comercialmente las texturas, pero prohíben redistribuir la textura fuente. Por ello, este registro se conserva como **referencia de sombreado cel-shaded y separación de color base/sombra/brillo**, no como asset de producción.

Fuente primaria: [Team Aether Shop — ficha oficial en BOOTH](https://booth.pm/ja/items/1280998).

## 5. Ruliyna Shop — textura de cabello para VRoid

La ficha oficial ofrece una textura gratuita sin saturación y una versión de apoyo de ¥300 con 12 colores. La imagen visible fue inspeccionada: es una muestra pastel rosa/lila con marca de agua “SAMPLE”, no una ilustración de peinado con flequillo, laterales y parte trasera.

La ficha permite utilizar la textura en un modelo, también en contenido comercial, y distribuir ese modelo siempre que la textura no pueda extraerse. Prohíbe redistribuir o vender el archivo de textura y restringe su modificación cuando vaya a distribuirse/venderse. La compatibilidad es para material 3D/VRoid, no para las capas PNG 2D de KIRA. La decisión es **referencia del pipeline de texturas**, no asset reutilizable.

Fuente primaria: [Ruliyna Shop — ficha oficial en BOOTH](https://booth.pm/en/items/2159602).

## Estadísticas consolidadas tras añadir esta tanda

- **346** registros, IDs únicos y URLs de origen únicas, sincronizados entre JSON y HTML.
- **320** URLs de miniatura registradas; **319** URLs únicas.
- **26** fichas sin miniatura directa.
- **260** miniaturas pendientes de comprobación visual; las dos nuevas miniaturas BOOTH se verificaron visualmente y la cuenta no aumentó.
- **160** fichas con licencia ausente/pendiente o con alcance por revisar; **45** sin estado de licencia.
- **0** brechas del campo de aviso rojo en la validación estructural.
- La deduplicación perceptual entre URLs distintas sigue pendiente; el comparador nuevo registra decisiones humanas, no identifica imágenes automáticamente.

## Validación local

```bash
python scripts/audit_visual_census.py
python -m unittest discover -s tests -v
```

**Criterio de cierre:** las cinco fuentes quedan documentadas con términos y recomendación; tres miniaturas se comprobaron visualmente, una está pendiente de inspección visual y una fuente no ofrece miniatura específica. Ningún recurso fue importado automáticamente ni se infirieron derechos a partir de la mera existencia de una miniatura pública.
