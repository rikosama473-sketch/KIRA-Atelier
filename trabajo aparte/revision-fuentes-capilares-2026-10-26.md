# Revisión selectiva de fuentes capilares — 26 de octubre de 2026

**Proyecto:** KIRA Atelier  
**Módulo:** KIRA Atlas  
**Lote:** 5 registros capilares priorizados  
**Criterio:** verificar el contenido de la página original, comparar `thumbnail_url` con la imagen destacada declarada por la fuente y separar el uso como referencia de los permisos para incorporar, modificar o redistribuir imágenes.

## Resultado del lote

| ID | Fuente | Correspondencia de miniatura | Estado de derechos |
|---|---|---|---|
| `EXT-HIR-015` | [AnimeOutline — How to Draw Anime and Manga Hair (Female)](https://www.animeoutline.com/how-to-draw-anime-and-manga-hair-female/) | **Inspección visual completada.** La URL catalogada es la imagen destacada declarada por la página; la lámina visible muestra seis variantes de peinado anime. | Solo referencia. [La política de copyright de AnimeOutline](https://www.animeoutline.com/copyright/) exige permiso previo para reutilizar contenido original; no hay permiso concedido a KIRA Atelier. |
| `CENSUS-A-17` | [AnimeOutline — How to Draw Anime Pigtails Hair](https://www.animeoutline.com/how-to-draw-anime-pigtails-hair/) | La URL coincide exactamente con el `og:image` de la página y el texto confirma un tutorial de seis pasos sobre coletas. **La carga e inspección visual independiente de esta imagen destacada siguen pendientes.** | Solo referencia. Se exige permiso previo para el contenido original; no se ha obtenido. |
| `CENSUS-A-20` | [AnimeOutline — How to Draw an Anime Girl's Head and Face](https://www.animeoutline.com/how-to-draw-anime-girl-head-and-face/) | La URL coincide exactamente con el `og:image` de la página. El tutorial se centra en cabeza y rostro, con el cabello como elemento secundario. **La imagen destacada aún necesita inspección visual directa.** | Solo referencia. Se exige permiso previo para el contenido original; no se ha obtenido. |
| `CENSUS-A-15` | [Pixivision — Drawings of Short Hair - Short Stories](https://www.pixivision.net/en/a/10898) | La URL coincide exactamente con el `og:image` oficial y el contenido trata de peinados cortos. Es una portada editorial para una colección, no una prueba de identidad o licencia de cada obra que contiene. **La imagen de portada aún necesita inspección visual directa.** | Solo referencia editorial. El artículo es consultable, pero los derechos de las ilustraciones individuales no se han comprobado por separado. |
| `CENSUS-A-13` | [Pixivision — Hairstyle Illustration Roundup - A Trip to the Salon](https://www.pixivision.net/en/a/11971) | La URL coincide exactamente con el `og:image` oficial. El texto de la página confirma una colección de cortes cortos, bobs, ondas, coletas, ponytails y trenzas. La portada no es un asset modular. **La imagen de portada aún necesita inspección visual directa.** | Solo referencia editorial. Los derechos de las ilustraciones individuales no se han comprobado por separado. |

## Hallazgos y límites

1. **Una coincidencia de `og:image` confirma la asociación de una URL con la página, no que el archivo se haya cargado correctamente en el navegador del usuario.** Por eso cuatro registros siguen marcados con inspección visual pendiente.
2. La miniatura de `EXT-HIR-015` es una hoja de tutorial con seis peinados. Sirve para estudiar silueta y construcción, pero no debe tratarse como seis capas PNG independientes.
3. Las páginas de Pixivision son índices curatoriales útiles para descubrir estilos e ilustradores. La etiqueta de página gratuita o la disponibilidad de una portada no autoriza a copiar, recortar, redistribuir o entrenar con cada obra destacada.
4. Las tres fichas de AnimeOutline ahora señalan `reference_only_permission_required`; las dos fichas Pixivision señalan `reference_only_individual_artist_rights_unverified`. **Ningún recurso de este lote se declara aprobado para integrarse o redistribuirse como asset.**
5. Esta revisión no descarga ni altera imágenes fuente. La inspección visual directa completada en este lote se limita a la miniatura de `EXT-HIR-015`; los otros cuatro elementos tienen evidencia de página/URL, pero no una revisión visual final del archivo exacto.

## Cambios de datos

Se sincronizaron los metadatos de los cinco registros en:

- [Índice maestro JSON](indice-visual-componentes.json)
- [Atlas interactivo HTML](censo-visual-interactivo.html)

Se añadieron el título revisado de la página, la fecha de comprobación, el nivel/método de verificación y los enlaces de evidencia de derechos. El validador también se actualizó para reconocer formulaciones como «no se ha verificado visualmente», a fin de no descontar trabajo pendiente por diferencias de redacción.

## Fuentes consultadas

- [AnimeOutline — tutorial general de peinados femeninos](https://www.animeoutline.com/how-to-draw-anime-and-manga-hair-female/)
- [AnimeOutline — tutorial de coletas](https://www.animeoutline.com/how-to-draw-anime-pigtails-hair/)
- [AnimeOutline — cabeza y rostro femeninos](https://www.animeoutline.com/how-to-draw-anime-girl-head-and-face/)
- [AnimeOutline — política de copyright](https://www.animeoutline.com/copyright/)
- [Pixivision — peinados cortos](https://www.pixivision.net/en/a/10898)
- [Pixivision — recopilación de ilustraciones de peinados, publicada el 12 de septiembre de 2026](https://www.pixivision.net/en/a/11971)

**Conclusión:** se completó una inspección visual de miniatura y se verificó la asociación con la fuente en cinco registros; cuatro aún requieren cargar y revisar visualmente el archivo exacto. Los permisos se tratan por separado y ningún recurso se ha autorizado para reutilización.
