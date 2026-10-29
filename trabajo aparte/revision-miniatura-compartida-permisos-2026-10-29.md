# Revisión del grupo de miniatura compartida y permisos — 29 de octubre de 2026

**Proyecto:** KIRA Atelier  
**Módulo:** KIRA Atlas  
**Lote:** `THUMB-SHARED-001`  
**Estado:** candidato compartido documentado; comparación visual pendiente; sin fusión de registros.

## Resultado

El índice actual tiene **346 fichas**, 346 IDs y 346 URLs de origen únicas. Hay 320 registros con URL de miniatura y 319 URLs distintas: una URL se repite en dos fichas. La coincidencia se conserva como pista, no como prueba de que los temas o las ilustraciones de origen sean iguales.

| ID | Fuente | Qué sabemos | Estado |
|---|---|---|---|
| `ACC-CENSUS-F2` | [I Draw Fashion — Others ACC](https://idrawfashion.com/accessories/others/) | La página oficial se abrió el 29/10/2026 y lista tutoriales de lazos, coronas de flores, cadenas, gafas de sol, bolsos, cremalleras, coronas y cinturones. Esto confirma el tema de la página, no la correspondencia de la miniatura compartida. | Fuente localizada; la miniatura directa compartida no se pudo renderizar de forma independiente durante esta revisión. |
| `ACC-CENSUS-F3` | [I Draw Fashion — Jewelry](https://idrawfashion.com/accessories/jewelry/) | La página oficial se abrió el 29/10/2026 y describe tutoriales de pulseras, pendientes, anillos y collares; lista una guía de pulsera. La miniatura directa compartida sigue sin poder renderizarse de forma independiente. | Fuente localizada; correspondencia de la miniatura y objeto principal pendientes. |

Ambos registros usan la misma URL exacta de imagen: `https://idrawfashion.com/wp-content/uploads/2019/11/fb1.png`. No se puede afirmar solo por esto que la imagen represente correctamente ambas páginas. Tampoco se debe fusionar las dos fichas: siguen siendo páginas fuente distintas con contenidos distintos. El comparador visual por pares ya está disponible para registrar más adelante una decisión humana, pero no convierte coincidencias de URL en veredictos automáticos.

## Permisos y uso recomendado

La página oficial de [Términos de servicio de I Draw Fashion](https://idrawfashion.com/terms-of-service/) (vigentes según el propio sitio desde el 1/08/2024) dice que los productos vendidos tienen una licencia limitada, no transferible y de uso personal; prohíbe redistribuir públicamente esos productos y remite las consultas comerciales al titular. El texto consultado se centra en productos vendidos y no resuelve expresamente los permisos de reproducción o redistribución de cada ilustración de los tutoriales gratuitos ni de la miniatura de categoría. Por ello no debe interpretarse ni como autorización ni como prohibición específica de esas obras: su reutilización sigue sin estar establecida, y:

- **Uso en el Atlas:** mantener enlaces a las páginas fuente y estudiar el tema general del tutorial.
- **Uso dentro de KIRA Editor:** no empaquetar ni recortar las ilustraciones de los tutoriales como capas ni redistribuirlas mientras no exista una licencia específica o permiso explícito. El estado actual es **derechos no verificados**, no un dictamen de que toda imagen gratuita esté prohibida.
- **Duplicación:** marcar el grupo como pendiente de comparación visual; no descartar ni combinar registros por la coincidencia de miniatura.

## Datos corregidos en el índice

Se actualizaron JSON y HTML con los mismos campos de revisión para ambas fichas:

- `thumbnail_duplicate_group_id = THUMB-SHARED-001`
- `thumbnail_duplicate_review_status = candidate_pending_visual_comparison`
- `thumbnail_status` explica que la vista exacta no quedó verificada y que la coincidencia es solo una pista.
- `extras_red` mantiene el aviso de hub secundario y agrega la alerta de miniatura compartida.
- `license_status = reference_only_source_artwork_reuse_not_verified`
- `asset_use_recommendation` limita el uso a referencia/tutorial hasta obtener permiso o una licencia abierta específica.
- `rights_evidence_url` apunta a los términos oficiales consultados el 29 de octubre de 2026.

## Cifras del censo tras la revisión

- 346 fichas y 346 URLs fuente únicas.
- 320 URL de miniatura; 319 URLs distintas.
- 26 registros sin miniatura directa.
- 1 grupo de miniatura compartida entre 2 fichas; no hay URLs canónicas de fuente duplicadas.
- 260 miniaturas continúan pendientes de comprobación visual según el recuento conservador del informe general.
- 160 fichas permanecen sin licencia verificada, con licencia pendiente o con alcance de permisos por revisar. Tras añadir estados explícitos a estas dos fichas, 43 registros siguen sin el campo `license_status`.

## Criterio de cierre

Este lote **no** confirma un duplicado de ilustración. Confirma una colisión de URL y registra que el contenido temático de las dos páginas oficiales se pudo comprobar, mientras que el archivo fb1.png no pudo renderizarse de forma independiente. Para cerrar el caso habrá que inspeccionar esa imagen exacta y confirmar si corresponde a ambas páginas. La decisión de duplicación debe mantenerse separada de los derechos de uso.

