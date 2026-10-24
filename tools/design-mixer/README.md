# KIRA Design Mixer — biblioteca, recortes y prompts

**Módulo de KIRA Atelier** para explorar muchas referencias, seleccionar rasgos visuales y combinarlos en un tablero conceptual antes de dibujar o generar una variante con IA.

## Abrirlo

Abrí `tools/design-mixer/index.html` en un navegador moderno. No requiere instalar paquetes ni conectarse a un servicio externo. Para carpetas completas, usá Chrome, Edge u otro navegador Chromium que admita el selector de directorios.

## Flujo de trabajo

1. **Cargar referencias.** Elegí imágenes sueltas o una carpeta con `Abrir carpeta`. El índice permanece en memoria durante esa sesión. La galería muestra hasta 72 imágenes por página; no intenta decodificar todas las miniaturas a la vez.
2. **Recortar una pieza.** Seleccioná una imagen y arrastrá un rectángulo alrededor de la zona que te inspira. También podés añadir la imagen entera como referencia.
3. **Clasificar y describir.** Elegí categoría —cabello, flequillo, ojos, rostro, silueta, proporciones del pecho, ropa, piernas, accesorios, paleta, etc.— y agregá una nota con el rasgo concreto que querés conservar.
4. **Mezclar.** Las piezas recortadas aparecen en la mesa de trabajo y en un tablero visual ordenado. La nota se puede editar después.
5. **Sacar el prompt.** Indicá idea del personaje, dirección de estilo y paleta. El módulo produce un prompt editable que reúne las descripciones de las piezas.
6. **Exportar.** Guardá el tablero como PNG, el prompt como TXT o la mezcla como JSON. El JSON incluye los recortes en PNG codificados dentro del archivo, para poder volver a abrir el diseño sin volver a localizar todas las fuentes.

## Privacidad y consumo

- Las imágenes seleccionadas se leen en el navegador del equipo. El módulo no tiene una función de subida, cuenta, telemetría ni llamada de IA.
- El directorio original no se modifica. Los recortes son nuevas imágenes de trabajo.
- Se crean miniaturas sólo para la página visible; para grandes bibliotecas conviene explorar por tandas y guardar un proyecto por personaje o grupo de rasgos.
- Los objetos de recorte se mantienen en memoria hasta que se exporta el proyecto. Cerrá o recargá la página solo después de guardar lo que querés conservar.

## Qué hace y qué todavía no hace

**Implementado en esta versión:** carga local de muchas imágenes, búsqueda por nombre/ruta, paginación, recorte rectangular asistido, etiquetas de categoría, notas editables, composición de tablero, exportación PNG, prompt editable/descargable y proyecto JSON importable.

**Pendiente, no simulado:** encontrar automáticamente cabello, ojos, ropa o extremidades en miles de imágenes; crear máscaras transparentes precisas; estimar proporciones reales; quitar fondos complejos; deduplicar visualmente obras repetidas; y convertir una pieza recortada en una capa que encaje anatómicamente con las demás.

## Próximas etapas recomendadas

1. Construir un índice persistente con dimensiones, tamaño, huella/hash, miniaturas y procedencia por referencia. Añadir detección de duplicados exactos antes de la deduplicación visual.
2. Integrar de manera opcional un segmentador local para proponer máscaras de pelo, cara, ropa y cuerpo. Las máscaras deben mostrarse como **candidatas**, con confianza/revisión manual; no se aprobarían como capas finales automáticamente.
3. Añadir pincel de corrección de máscara, transparencia y alineación por guías para separar mechones, ropa y anatomía tapada.
4. Construir un mezclador de personaje por capas semánticas —base/cuerpo, cara, ojos, pelo trasero, pelo delantero, ropa, accesorios— distinto del tablero de inspiración.
5. Exportar una ficha de diseño que incluya prompt, paleta, rasgos obligatorios, variaciones permitidas, referencias y notas de procedencia.

## Derechos de las referencias

Una miniatura visible o una imagen publicada no implica permiso para redistribuirla ni para entrenar un modelo con ella. Conservá la fuente y registrá licencia, atribución, precio/restricciones y permiso de uso antes de integrar cualquier referencia como asset del producto. El tablero sirve para diseñar y comparar ideas; no cambia los derechos de las obras originales.
