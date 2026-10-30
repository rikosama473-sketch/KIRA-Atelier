# KIRA Atelier — punto de continuidad

**Fecha:** 2026-10-30  
**Rama objetivo:** `main`  
**Último commit de main comprobado:** `34e9cf85c3e0e6933b4ec547bc38fa6587a63fc9`

Este documento conserva el punto exacto para retomar el trabajo sin repetir auditorías ya cerradas. Distingue validación de código, ejecución real del generador y revisión de los resultados visuales.

## Estado confirmado

- `main` apunta a `34e9cf85c3e0e6933b4ec547bc38fa6587a63fc9`.
- CI del commit: [run 40987846553](https://github.com/rikosama473-sketch/KIRA-Atelier/actions/runs/40987846553), conclusión `success`.
- La ejecución cubrió compilación de Python, comprobaciones de sintaxis JavaScript de las herramientas y **162 pruebas unitarias aprobadas**.
- Las tres regresiones recientes de la cola comprueban que un manifiesto parcial, un render ausente o una referencia fuente cuyo hash cambió no marquen el paquete como terminado.
- La CI anterior no ejecuta el generador de imágenes. No equivale a una generación real ni a aprobación visual.

## Próxima tarea del generador

El selector vigente es `scripts/select_next_character_asset_task.py`. Lee `data/character-prompt-registry.json`, verifica la referencia y su SHA-256 y recorre `PACK_ORDER`; no usa `data/anatomy-generation-queue.json`.

Referencia de Pibara confirmada por los manifiestos existentes:

- Personaje: `pibara`
- Imagen: `from-PixAI-2034984086876227343-0.png`
- SHA-256 de la fuente registrado en los manifiestos: `f3777be442119b85a9ddab6c59a576f37761248a902e13289c3ff520ebcb67c0`
- Siguiente paquete automático: **`anatomy-back-1`**
- Fondo solicitado recomendado para el lote: `transparent`
- Semilla base configurada: `1201`

La secuencia anterior tiene manifiestos completos para `anatomy-sheet-4`, `anatomy-guide-1`, `anatomy-front-v2-1` y `anatomy-side-1`; también están completos `hair-core-5` y `expressions-core-5`. Los manifiestos parciales antiguos de esos paquetes no invalidan las ejecuciones completas posteriores.

### Cómo retomar

En GitHub Actions, abrir **Generate character assets without an API key** y ejecutar manualmente con:

1. Character: `pibara`
2. Reference image: `from-PixAI-2034984086876227343-0.png`
3. Asset pack: `anatomy-back-1`
4. Background: `transparent`
5. Base seed: `1201`

Después verificar el run y confirmar en `generated/character-assets/pibara/` que el manifiesto indique `pack_status: complete`, que todos los IDs requeridos tengan archivos render existentes y que el resultado se registre en `tools/avatar-maker/assets/image-library.json`. Los registros nuevos deben seguir pendientes de revisión visual de identidad y de permisos; no convertirlos automáticamente en capas aprobadas.

## Bloqueo y discrepancias pendientes

- No se ha confirmado una ejecución satisfactoria del generador después de corregir la cola y la persistencia en la biblioteca. El último intento fallido conocido fue el run `40900758962`, que terminó con `Unsupported asset pack.` sobre un SHA anterior a las correcciones.
- El workflow admite `schedule` y `workflow_dispatch`, pero todavía falta iniciar y comprobar un nuevo run real. La CI verde de `34e9cf8` solo valida el código.
- `data/anatomy-generation-queue.json` conserva instrucciones antiguas: apunta a `work/easy-avatar-maker-2026-10` y prohíbe escribir en `main`. La búsqueda de referencias no encontró consumidores en el código indexado y el selector actual no lo lee. Tratarlo como archivo heredado sin autoridad sobre la cola actual; no modificarlo ni obedecerlo como estado vigente hasta verificar quién lo necesita.
- `docs/DEVELOPMENT_STATUS.md` sigue siendo un informe heredado de IMAGE del 21/10. No usarlo como estado actual de KIRA Atelier ni sobrescribir su historial sin una migración deliberada.

## Orden de continuación

1. Ejecutar manualmente el paquete `anatomy-back-1` con los parámetros indicados.
2. Revisar el resultado real del run, manifiesto, archivos renderizados y persistencia en la galería.
3. Si falla, corregir el motivo concreto y añadir una regresión antes de volver a ejecutar.
4. Inspeccionar visualmente identidad, anatomía, recortes y transparencia. Mantener cualquier salida no aprobada como candidata.
5. Solo después elegir el siguiente paquete mediante `scripts/select_next_character_asset_task.py`; no saltar paquetes ni declarar completado un lote parcial.

## Referencias de trabajo

- [Commit actual](https://github.com/rikosama473-sketch/KIRA-Atelier/commit/34e9cf85c3e0e6933b4ec547bc38fa6587a63fc9)
- [CI aprobada](https://github.com/rikosama473-sketch/KIRA-Atelier/actions/runs/40987846553)
- [Workflow de generación gratuita](https://github.com/rikosama473-sketch/KIRA-Atelier/actions/workflows/generate-character-assets-free.yml)
- [Selector automático](../scripts/select_next_character_asset_task.py)
- [Fábrica de assets](CHARACTER_LAYER_ASSET_FACTORY.md)
