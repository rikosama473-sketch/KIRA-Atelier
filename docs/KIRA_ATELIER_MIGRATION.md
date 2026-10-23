# KIRA Atelier — Registro de migración

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

## Estado inicial de la migración (actualizado abajo)

Esta sección registraba el corte inicial, cuando los PNG originales seguían en el repositorio anterior. La sincronización ampliada descrita al final reemplaza ese estado.

## Rebranding y conservación

- La identidad de marca del producto es KIRA Atelier, con los módulos KIRA Editor, KIRA Atlas y KIRA Forge. Los principales HTML fueron actualizados; quedan referencias históricas en código/datos donde son identificadores o procedencia.
- El editor usa como muestra una salida de personaje ya copiada en este repositorio.
- Los vínculos relativos del atlas se mantuvieron junto a los documentos de los que dependen.
- El antiguo repositorio no se borró, no se reescribió y no se dio por cerrado: queda como archivo de origen hasta completar la migración del material que siga siendo necesario.
- No se han cambiado licencias de terceros ni se han convertido candidatos de capa en assets “aprobados” por el solo hecho de migrarlos.

## Verificaciones de salida

Después de publicar el commit se comprobará que los archivos estén en la rama `main`, que el JSON del índice siga parseando, que sus 339 IDs/URLs sigan siendo únicos y que las rutas relativas internas del atlas resuelvan contra los archivos migrados. La ejecución visual completa del editor y las pruebas automatizadas deberán verificarse en un entorno de desarrollo; no se deben afirmar como ejecutadas hasta realizarlas.


## Migración ampliada — 23 de octubre de 2026

Se sincronizaron los módulos, scripts, pruebas, catálogos, manifiestos y archivos generados desde la rama main del repositorio image. Se copiaron además los 759 PNG originales de la raíz, manteniendo sus nombres y rutas para no romper las referencias del dataset. image se conserva intacto como respaldo hasta terminar las verificaciones de integración. La copia no equivale a una aprobación de licencias ni convierte máscaras candidatas en capas aprobadas.
