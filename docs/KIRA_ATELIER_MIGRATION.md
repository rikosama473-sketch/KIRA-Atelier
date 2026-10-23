# Migración inicial a KIRA Atelier

**Fecha:** 2026-10-23  
**Destino principal:** `rikosama473-sketch/KIRA-Atelier`, rama `main`  
**Origen revisado:** `rikosama473-sketch/image`, rama `work/interactive-hairstyle-atlas-2026-10`, commit `2d8cfcbb96602bef8be7b128e870254799da5ea3`.

## Copiado a este repositorio

- Editor manual de capas y su lanzador de escritorio local.
- Revisor de dataset/fuentes.
- Atlas interactivo de peinados, censo visual e índice JSON con sus auditorías e investigaciones enlazadas.
- Scripts de construcción de capas, separación de spritesheets, preparación de packs y variantes.
- Flujos de trabajo y pruebas relacionadas con la fábrica de assets.
- Guías de recursos, proveniencia, fabricación de capas y validación.
- Las 46 entradas de `generated/character-assets/pibara/` y `generated/character-layers/pibara/` presentes en el árbol de origen, incluidos PNG/JPG, manifiestos y prompts. Cada archivo binario transferido se comparó por SHA contra el original.

## Pendiente de una migración completa de los archivos gráficos

No es honesto declarar que se trasladó toda la colección de imágenes: la transferencia inicial no incluyó los 759 PNG originales del inventario (aprox. 706,4 MB) ni el resto de archivos gráficos sueltos de `generated/`. Esos originales permanecen intactos en el repositorio `image`. Algunos manifests y el catálogo describen archivos de ese repositorio antiguo; se deberá actualizar esa procedencia cuando los originales tengan un destino definitivo.

No se copió automáticamente la colección completa de imágenes porque los archivos deben revisarse por su utilidad para el editor, sus duplicados y los derechos aplicables. El censo contiene 339 referencias; 96 tienen licencia/precio pendientes y las miniaturas almacenadas son candidatas, no prueba de que cada fuente se haya inspeccionado visualmente.

## Rebranding y conservación

- La identidad visible de las interfaces principales se cambió a KIRA Atelier / KIRA Atlas.
- El editor usa como muestra una salida de personaje ya copiada en este repositorio.
- Los vínculos relativos del atlas se mantuvieron junto a los documentos de los que dependen.
- El antiguo repositorio no se borró, no se reescribió y no se dio por cerrado: queda como archivo de origen hasta completar la migración del material que siga siendo necesario.
- No se han cambiado licencias de terceros ni se han convertido candidatos de capa en assets “aprobados” por el solo hecho de migrarlos.

## Verificaciones de salida

Después de publicar el commit se comprobará que los archivos estén en la rama `main`, que el JSON del índice siga parseando, que sus 339 IDs/URLs sigan siendo únicos y que las rutas relativas internas del atlas resuelvan contra los archivos migrados. La ejecución visual completa del editor y las pruebas automatizadas deberán verificarse en un entorno de desarrollo; no se deben afirmar como ejecutadas hasta realizarlas.
