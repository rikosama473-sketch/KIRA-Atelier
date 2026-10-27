# Revisión de creadores 2D, arquitectura por capas y permisos — 27 de octubre de 2026

**Proyecto:** KIRA Atelier  
**Módulo:** KIRA Atlas  
**Lote:** seis referencias de packs modulares y creadores de personajes  
**Objetivo:** separar lo que sirve como referencia de arquitectura, lo que puede ser candidato a asset y lo que no se debe incorporar sin permiso.

## 1. Resumen del lote

| ID | Fuente | Miniatura | Decisión de uso |
|---|---|---|---|
| `EXT-ITCH-009` | [Awfully Sweet — Butter Milk](https://butterymilk.itch.io/awfully-sweet) | La URL registrada coincide con la imagen Open Graph de la página; el archivo exacto no cargó en la inspección. **Pendiente visual.** | Solo referencia de arquitectura. La autora permite usar y editar sprites generados con el pack, pero prohíbe revender los sprites o las versiones editadas. Hace falta permiso explícito antes de redistribuir piezas dentro del editor. |
| `EXT-ITCH-010` | [Customize Your Waifu — Kikeluzi](https://kikeluzi.itch.io/cyw) | **Inspección visual completada.** La miniatura muestra tres personajes con cambios de piel, cabello y vestuario; es una composición promocional, no una carpeta de capas. | **Candidato condicional.** La página declara CC BY 4.0 para los assets, pero el pack cuesta USD 4 o más y hay que confirmar que los archivos/componentes incluidos están cubiertos. Se exige atribución y aviso de cambios al compartir el material licenciado o adaptaciones. La página también declara asistencia de IA en código/gráficos. |
| `EXT-ITCH-011` | [Character Creator VN — Sutemo / yuripourre](https://yuripourre.itch.io/character-creator-sutemo) | **Inspección visual completada.** La miniatura es un retrato anime que funciona como portada del producto, no una captura de la interfaz. | Referencia de flujo de trabajo. El programa es gratuito, pero los sprites son obra de terceros y las condiciones dependen del pack; no se deben empaquetar con KIRA sin revisar cada licencia por separado. |
| `EXT-TOOL-001` | [Mannequin Character Generator — AR14](https://ar14.itch.io/mannequin) | La URL coincide con la imagen Open Graph de la ficha; la imagen exacta no se renderizó directamente. **Pendiente visual.** | Referencia de arquitectura únicamente. El anuncio consultado presenta una herramienta de retratos 2D y VTuber con precio desde USD 20,09. El alcance de la declaración CC0 anotada en el censo no se pudo establecer para software, ilustraciones, salida exportada y todos los assets; se conserva como no resuelto. |
| `EXT-TOOL-002` | [Mannequin 0.3.12 — estructura de plantillas de cabello](https://ar14.itch.io/mannequin/devlog/256706/0312-update-reworked-hairstyle-templates) | **Inspección visual completada y URL corregida.** Se sustituyó la miniatura anterior por la imagen exacta del devlog que muestra las piezas de cabello etiquetadas. | Referencia de arquitectura, no asset artístico. El esquema separa Primary Hairstyle, Bangs, Sideburns/Wisps, Additional Hair Parts y Hair Accessories; es una guía útil para el modelo de capas de KIRA Editor. No se encontró permiso para redistribuir la captura ni el arte de ejemplo. |
| `EXT-BOOTH-003` | [Marumori — PSD gratuito con cabello separado](https://booth.pm/ja/items/4997076) | La URL coincide con la imagen Open Graph de BOOTH, pero el archivo exacto no cargó en la inspección. **Pendiente visual.** | **No importar ni modificar sin permiso.** La página permite ilustraciones para MV, videos de canto y tutoriales; prohíbe modificación, redistribución, reventa y entrenamiento de IA. Otros usos requieren consultar a la creadora, aunque el PSD incluya flequillo/cabello lateral/cabello posterior en capas. |

### Interpretación

- **Referencia de arquitectura** significa aprender la organización de la interfaz o de las piezas; no da derecho a copiar la captura ni las ilustraciones.
- **Candidato condicional** significa que hay una licencia publicada que parece compatible en principio, pero falta obtener/comprobar el pack completo y revisar componentes de terceros antes de incorporarlo.
- **No aprobado para incorporar** es el estado de los materiales cuyo alcance prohíbe o no aclara el uso como piezas intercambiables dentro de otro editor.
- Una portada, una página pública o un archivo descargable no convierten un PSD/PNG en un recurso de libre redistribución.

## 2. Cambio estructural del censo

Se corrigió la miniatura de `EXT-TOOL-002`: en vez de una URL de imagen que no aparecía entre las imágenes actuales extraídas del devlog, ahora apunta a la ilustración etiquetada verificada visualmente en la propia página. La imagen enumera las piezas de pelo y sus accesorios y coincide directamente con el propósito de la ficha.

Las seis fichas recibieron metadatos de revisión: título de fuente, fecha, método/nivel de verificación, enlace de evidencia de derechos y recomendación de uso. JSON y HTML se actualizaron para mantener la misma fuente y miniatura por ID.

## 3. Validador: recuentos conservadores

La regla de miniaturas ahora detecta estados como «pendiente», «no se cargó», «no visualmente comprobado» y «falló la carga», no solo etiquetas que contienen literalmente «metadata» o «unverified». La regla de licencias también incluye afirmaciones que todavía requieren revisar la página original, alcances de licencia no resueltos, dependencias de terceros y licencias diferentes por pack.

| Indicador actual | Resultado |
|---|---:|
| Entradas JSON / HTML | 340 / 340 |
| IDs únicos | 340 |
| URLs de fuente únicas | 340 |
| URLs de miniatura registradas | 315 |
| URLs de miniatura únicas | 314 |
| Registros sin miniatura directa | 25 |
| Miniaturas aún pendientes de comprobación visual/archivo | 257 |
| Licencias ausentes, pendientes o con alcance sin resolver | 160 |
| De ellas, sin ningún estado de licencia | 45 |
| Grupos de URL de miniatura compartida | 1 |
| Brechas en avisos rojos obligatorios | 0 |
| Diferencias entre campos clave JSON/HTML | 0 |

Los conteos de pendiente no equivalen a errores confirmados. Una URL puede corresponder a la página y, aun así, no haberse cargado la imagen exacta. De igual forma, que una ficha incluya un número de licencia no demuestra por sí solo que todos los archivos del pack estén cubiertos por ella.

## 4. Validación automática

Se ampliaron las pruebas para asegurar que:
- las portadas con fallos de carga continúan pendientes;
- la inspección de una imagen marcada como visualmente comprobada permite que salga de la lista pendiente;
- las licencias declaradas «verificadas» pero que todavía requieren revisar la página original siguen en el recuento de revisión;
- el censo conserve IDs, orden, URLs y avisos rojos sincronizados entre JSON y HTML.

Comando local:

```bash
python scripts/audit_visual_census.py
python -m unittest discover -s tests -p "test_visual_census_audit.py" -v
```

## 5. Fuentes oficiales consultadas en esta tanda

- [Awfully Sweet — página y condiciones de Butter Milk](https://butterymilk.itch.io/awfully-sweet)
- [Customize Your Waifu — ficha y metadatos de licencia CC BY 4.0](https://kikeluzi.itch.io/cyw)
- [Texto legal oficial de CC BY 4.0](https://creativecommons.org/licenses/by/4.0/legalcode)
- [Character Creator VN — descripción del programa y atribución de sprites](https://yuripourre.itch.io/character-creator-sutemo)
- [Mannequin Character Generator — ficha oficial](https://ar14.itch.io/mannequin)
- [Mannequin 0.3.12 — devlog con las piezas de cabello](https://ar14.itch.io/mannequin/devlog/256706/0312-update-reworked-hairstyle-templates)
- [Marumori — términos japoneses de uso del PSD](https://booth.pm/ja/items/4997076)

**Conclusión:** las seis fichas se investigaron y documentaron; tres miniaturas quedaron inspeccionadas visualmente en esta tanda, y otras tres siguen pendientes de renderizado/inspección directa. Solo Kikeluzi queda como candidato condicional bajo CC BY 4.0, sujeto a adquirir el pack y comprobar el alcance de cada componente. Los demás se conservan como referencia técnica o se excluyen de la incorporación directa mientras no exista permiso compatible.
