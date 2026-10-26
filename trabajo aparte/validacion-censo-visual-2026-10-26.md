# Auditoría estructural y de avisos rojos — 26 de octubre de 2026

**Proyecto:** KIRA Atelier  
**Módulo:** KIRA Atlas  
**Objetivo:** cerrar brechas estructurales encontradas en el censo y dejar un validador repetible para futuras incorporaciones.  
**Alcance:** JSON, registros integrados en HTML, campos de procedencia, miniaturas registradas, estado de licencia y metadatos de avisos rojos.  
**No cubre:** descarga de miniaturas, revisión visual de cada obra, deduplicación perceptual ni una determinación legal de permisos.

## 1. Corrección aplicada

La revisión localizó **49 fichas** que describían elementos ajenos al componente objetivo mediante `extras_red`, `irrelevant_elements_red` o metadatos de censo anidados, pero no tenían `red_warning_required: true`.

Se añadió el indicador a esas 49 fichas en ambos formatos:

- `trabajo aparte/indice-visual-componentes.json`
- `trabajo aparte/censo-visual-interactivo.html`

El conjunto corregido incluye fichas de pelo, ojos, ropa, accesorios, fuentes Pixivision, BOOTH y otras plataformas. No se eliminaron registros ni se alteraron las URLs de origen. Las advertencias rojas siguen siendo orientativas: no sustituyen la inspección de la ilustración original.

**Resultado posterior:** 0 fichas con contenido de elementos extra y sin el indicador rojo requerido.

## 2. Estado medido del censo

| Indicador | Resultado |
|---|---:|
| Entradas del JSON | 340 |
| Registros del HTML | 340 |
| IDs únicos en el JSON | 340 |
| IDs únicos en el HTML | 340 |
| URLs de origen únicas | 340 |
| IDs/URLs de origen/campos clave sincronizados | Sí |
| URLs de miniatura registradas | 315 |
| URLs de miniatura únicas | 314 |
| Registros sin miniatura directa | 25 |
| Estados de miniatura ausentes, candidatos o sin verificación | 244 |
| Estados de licencia ausentes | 45 |
| Estados de licencia ausentes, pendientes o no verificados | 144 |
| Brechas en `red_warning_required` | 0 |

Una URL de miniatura exacta se comparte entre dos fichas: `https://idrawfashion.com/wp-content/uploads/2019/11/fb1.png`. Se registra como **posible duplicado directo para revisión**, no se elimina automáticamente. Distintas URLs podrían seguir mostrando la misma obra; para encontrar esos casos sigue haciendo falta una comparación visual o por hash perceptual de las imágenes.

Las cifras de miniaturas y licencias describen el estado de los metadatos. No afirman que cada imagen cargue, corresponda visualmente con su obra, tenga permisos o esté libre de derechos.

## 3. Validador añadido

Archivo: `scripts/audit_visual_census.py`

Ejecutar desde la raíz del repositorio:

```bash
python scripts/audit_visual_census.py
```

Guardar un reporte estructurado opcional:

```bash
python scripts/audit_visual_census.py --json-output generated/visual-census-audit.json
```

El script no hace llamadas de red, no descarga imágenes y no modifica las fuentes. Comprueba:

- IDs ausentes o duplicados.
- URLs de origen ausentes, inválidas o repetidas.
- Sincronización del orden de registros y de los campos clave entre JSON y HTML.
- Fichas con elementos extra que carecen del indicador rojo.
- Miniaturas sin URL, con estados de verificación pendientes o con la misma URL repetida.
- Distribución del campo de estado de licencia, sin interpretar la etiqueta como una autorización legal.

## 4. Pruebas automáticas

Se añadió `tests/test_visual_census_audit.py` para comprobar el censo real y casos controlados de errores. Las pruebas cubren la detección de URL de origen duplicadas, avisos rojos ausentes, parseo seguro de la matriz JavaScript y detección de URLs de miniatura compartidas sin borrar registros automáticamente.

GitHub Actions ejecutó **Validate KIRA Atelier tools #49** tras la incorporación de las pruebas del validador, con resultado **completed successfully**. Más tarde, la ejecución **#59** también terminó correctamente tras incorporar el revisor visual; la suite completa informó **145 tests** y las pruebas nuevas de esa interfaz, incluida la sintaxis JavaScript con Node.js, pasaron.

## 5. Revisor visual manual de miniaturas

Se añadió [`tools/visual-reference-library/thumbnail-reviewer.html`](../tools/visual-reference-library/thumbnail-reviewer.html), accesible también desde la navegación de KIRA Atlas y el README principal.

El visor permite cargar el índice JSON localmente, seleccionar fichas con miniatura, abrir la obra original en otra pestaña y registrar uno de cinco resultados: coincide, no coincide, miniatura rota, duplicado probable o no confirmado. Incluye filtros por texto/categoría/estado, notas, navegación por teclado, guardado local cuando el navegador lo permite y exportación/importación de un archivo JSON auxiliar.

El progreso es un **informe separado**; no reescribe el índice, no sube imágenes del usuario y no da permisos de reutilización. Para ver las miniaturas, el navegador solicita las URL remotas a los sitios originales. La carga técnica de una imagen tampoco demuestra por sí sola que corresponda a la obra: esa comprobación sigue siendo manual. Una URL de miniatura repetida se muestra como señal de revisión, sin fusionar ni borrar fichas.

La interfaz tiene pruebas de contrato en `tests/test_thumbnail_reviewer.py`, que comprueban sus controles principales, el manejo conservador de permisos y la sintaxis JavaScript sin añadir dependencias externas.

## 6. Revisión selectiva de fuentes capilares

La primera tanda de cinco fichas se documenta en [Revisión de fuentes capilares — 26/10/2026](revision-fuentes-capilares-2026-10-26.md).

- **1 miniatura inspeccionada visualmente**: `EXT-HIR-015`, la lámina de seis peinados de AnimeOutline. La imagen corresponde al tema del tutorial, pero la política del sitio exige permiso previo para reutilizar contenido original; el permiso no se ha obtenido.
- **4 asociaciones de página confirmadas, con inspección visual directa pendiente**: `CENSUS-A-17`, `CENSUS-A-20`, `CENSUS-A-15` y `CENSUS-A-13`. En todas, la URL de miniatura coincide exactamente con el `og:image` de la fuente y el texto original es relevante para la ficha. No se confunde la portada de una colección con una ilustración individual.
- **Derechos separados del uso como referencia**: tres fichas AnimeOutline indican permiso previo requerido; dos fichas Pixivision mantienen pendiente la verificación de derechos de las obras individuales. Ninguna se considera un asset autorizado para incorporar o redistribuir.

Se corrigió además el criterio del validador para que frases como «no se ha verificado visualmente» sigan contabilizadas como pendientes. Estado recalculado tras esta corrección: **244 miniaturas pendientes de verificación** y **144 estados de licencia ausentes, pendientes o no verificados**.

## 7. Próximo trabajo requerido

1. Revisar las 244 miniaturas pendientes, empezando por las piezas que podrían servir de referencia para capas de cabello en KIRA Editor.
2. Investigar los 25 registros sin miniatura directa y decidir si conviene conservarlos como índices de búsqueda.
3. Resolver los 144 estados de licencia incompletos; distinguir referencia, uso dentro de la aplicación, modificación, redistribución de archivos y entrenamiento de modelos. Los registros con permiso previo requerido tampoco son assets aprobados.
4. Ejecutar deduplicación visual entre imágenes disponibles localmente y confirmar cada pareja antes de fusionar fichas.

**Conclusión:** la integridad estructural del censo se puede volver a comprobar con una herramienta local y 49 metadatos de aviso rojo quedaron normalizados. La primera tanda de fuentes capilares quedó documentada, pero la revisión visual de cuatro miniaturas y las decisiones de derechos siguen pendientes. No se declara completo el censo visual ni aprobados los recursos de terceros.
