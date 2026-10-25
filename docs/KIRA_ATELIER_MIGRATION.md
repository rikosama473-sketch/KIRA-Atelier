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
- README anterior de IMAGE y nota de diseño archivados en `docs/legacy/` para conservar el contexto previo.
- Las 46 entradas de `generated/character-assets/pibara/` y `generated/character-layers/pibara/` presentes en el árbol de origen, incluidos PNG/JPG, manifiestos y prompts. Cada archivo binario transferido se comparó por SHA contra el original.

## Estado inicial de la migración (actualizado abajo)

Esta sección registraba el corte inicial, cuando los PNG originales seguían en el repositorio anterior. La sincronización ampliada descrita al final reemplaza ese estado.

## Rebranding y conservación

- La identidad de marca del producto es KIRA Atelier, con los módulos KIRA Editor, KIRA Atlas y KIRA Forge. Los principales HTML fueron actualizados; quedan referencias históricas en código/datos donde son identificadores o procedencia.
- El editor usa como muestra una salida de personaje ya copiada en este repositorio.
- Los vínculos relativos del atlas se mantuvieron junto a los documentos de los que dependen.
- El repositorio `image` se conserva como respaldo de origen: su historial no se reescribió ni se borraron los archivos originales. Solo se añadió un aviso a su README para dirigir al repositorio principal.
- No se han cambiado licencias de terceros ni se han convertido candidatos de capa en assets “aprobados” por el solo hecho de migrarlos.

## Verificaciones realizadas

- La migración principal terminó correctamente en [GitHub Actions #39986868929](https://github.com/rikosama473-sketch/KIRA-Atelier/actions/runs/39986868929).
- Tras la sincronización del 25 de octubre, KIRA Atelier contiene **1006 archivos** y cubre las **989 rutas de archivo** de `image/main`; no queda ninguna ruta de archivo del origen ausente. En rutas comunes donde el SHA difiere se conserva la versión específica de KIRA Atelier cuando protege el branding o los ajustes del editor.
- Se verifican **816 PNG** en la raíz del destino. La colección original de 759 PNG citada al inicio de la migración sigue incluida, junto con imágenes de tandas posteriores.
- La comprobación de migración compiló Python y parseó correctamente los JSON cubiertos por el validador.
- La suite principal actualizada pasó **125 pruebas** en [GitHub Actions #39988426029](https://github.com/rikosama473-sketch/KIRA-Atelier/actions/runs/39988426029). La validación del constructor también pasó en [#39988188266](https://github.com/rikosama473-sketch/KIRA-Atelier/actions/runs/39988188266), y la validación del editor manual pasó en [#39988057952](https://github.com/rikosama473-sketch/KIRA-Atelier/actions/runs/39988057952).
- La construcción de hojas de contacto pasó en [#39987627148](https://github.com/rikosama473-sketch/KIRA-Atelier/actions/runs/39987627148).
- Esto valida estructura, archivos y pruebas automatizadas; no es una revisión visual humana de cada miniatura ni una aprobación de licencias de terceros. Los 96 registros con licencias/precios por confirmar siguen marcados como pendientes.



## Migración ampliada — 23 de octubre de 2026

Se sincronizaron los módulos, scripts, pruebas, catálogos, manifiestos, imágenes de salida y 759 PNG originales desde la rama `main` del repositorio `image`. Se incorporaron los cuatro workflows auxiliares que faltaban, preservando la configuración programada/manual del runner de lotes de `main`. Todos los nombres y rutas del origen tienen correspondencia en KIRA Atelier. El repositorio original sigue como respaldo; la transferencia no aprueba licencias ni convierte máscaras candidatas en capas aprobadas.


## Sincronización final de rutas faltantes — 25 de octubre de 2026

Se añadieron las 12 rutas de `image/main` que faltaban en KIRA Atelier: cinco archivos de la tanda de anatomía de Pibara `run-40104589145` (prompts, hoja de contacto, manifiesto y dos PNG) y siete archivos de `tools/sprite-layer-cropper` (herramienta, ejemplo de configuración, guía, dependencias y pruebas). Tras esta sincronización, las 989 rutas del origen tienen correspondencia en KIRA Atelier. La igualdad de rutas no implica una revisión visual humana de cada imagen ni aprobación de licencias.
