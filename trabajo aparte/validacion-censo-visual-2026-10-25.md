# Revalidación focalizada del censo visual — 25 de octubre de 2026

**Proyecto:** KIRA Atelier  
**Módulo:** KIRA Atlas  
**Alcance:** contraste estructural JSON/HTML, corrección de una fuente localizada, registro de un índice curatorial de peinados y actualización de contadores.  
**Naturaleza del censo:** registro de referencias y fuentes; no equivale a una biblioteca de imágenes aprobadas para redistribución.

## 1. Resultado estructural

| Comprobación | Resultado |
|---|---:|
| Entradas en `indice-visual-componentes.json` | 340 |
| Registros integrados en `censo-visual-interactivo.html` | 340 |
| IDs únicos en JSON | 340/340 |
| IDs únicos en HTML | 340/340 |
| IDs coincidentes entre JSON y HTML | 340/340 |
| URLs de origen únicas en JSON | 340 |
| URLs de origen únicas en HTML | 340 |
| URLs de origen coincidentes entre JSON y HTML | 340/340 |
| URLs de miniatura registradas | 315 |
| Registros PixAI | 58 |

Las comprobaciones se realizaron sobre los contenidos publicados en `main` después de sincronizar los dos archivos. No se encontraron IDs duplicados ni diferencias entre los conjuntos de IDs o URLs de origen principales. La ficha nueva no tiene miniatura porque no se obtuvo una previsualización cuya carga pudiera confirmarse; por eso el total de miniaturas sigue siendo 315.

## 2. Corrección: Gothic Lolita

Se corrigió la URL de origen de la ficha `CENSUS-B-08` para que apunte a la edición inglesa:

- [Drawings Featuring Gothic Lolita Fashion — What We Wear in the Shadows](https://www.pixivision.net/en/a/10939)
- Fecha publicada por Pixivision: 25 de agosto de 2025.
- Elemento objetivo: ropa Gothic Lolita, encajes, volantes, cintas y tocados.
- Elementos fuera del objetivo: rostro, pelo y rasgos específicos de cada personaje.
- **Permisos:** la página es una referencia editorial. No se ha confirmado el permiso de redistribución de las ilustraciones que contiene.

La URL de miniatura existente se conserva, pero apunta al endpoint de metadata localizado bajo `/ms/`. Su carga y equivalencia con la edición inglesa **siguen sin verificarse visualmente**. La interfaz lo comunica en el estado de la miniatura; no se marca como comprobada.

## 3. Fuente añadida: índice de peinados de Pixivision

Se añadió `EXT-PXV-HAIR-TAG-001`:

- [Pixivision — artículos etiquetados #hairstyles](https://www.pixivision.net/en/t/85)
- La página mostraba 122 artículos al comprobarla el 25 de octubre de 2026.
- Categoría: `female_hair`.
- Tipo de registro: índice curatorial / hub de etiquetas, no ilustración individual.
- **Uso previsto:** descubrir temas como cortes, flequillos, trenzas, coletas, twin-tails y moños y seguir los enlaces a sus páginas de origen.
- **Uso no autorizado por este registro:** descargar, redistribuir, empaquetar o entrenar con las ilustraciones enlazadas sin comprobar por separado los derechos aplicables.

La ficha se marca como hub de etiquetas y requiere aviso rojo. No se genera una miniatura inventada, no se cuenta como asset reutilizable y no se atribuye permiso de entrenamiento.

## 4. Criterios que siguen pendientes

Esta revalidación **no** certifica que las 315 miniaturas carguen en el navegador final, que cada imagen corresponda visualmente a la obra de origen ni que URLs de plataformas distintas no muestren la misma ilustración. La deduplicación perceptual por huellas de imagen sigue pendiente.

Tampoco se confirma ninguna placa monocroma cuadrada como recurso con licencia de reutilización. Un enlace público o una vista previa no equivalen a permiso de incorporación, redistribución ni entrenamiento.

## 5. Archivos sincronizados

- `trabajo aparte/indice-visual-componentes.json`: metadatos del proyecto actualizados a **KIRA Atelier**, corrección de `CENSUS-B-08` y nueva entrada del índice de peinados.
- `trabajo aparte/censo-visual-interactivo.html`: los mismos registros, contadores actuales, estado de miniatura pendiente y enlace a este informe.
- `README.md`: contadores actualizados y enlace a la revalidación.

**Conclusión:** el índice y el atlas interactivo vuelven a estar sincronizados para 340 fuentes. Esto acredita coherencia estructural, no reutilización legal de cada imagen ni deduplicación visual completada.
