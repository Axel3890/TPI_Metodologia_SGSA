# Diagnóstico de la versión base

Origen: prototipo didáctico creado en esta sesión; no es un sistema heredado de una institución.
Las debilidades se introdujeron en un módulo funcional acotado para poder analizar su evolución.
No se afirma un incidente ni una auditoría externa. El tag estado-inicial contiene código y pruebas.

| ID | Evidencia en inicial/sistema.py | Impacto y riesgo | Prioridad | Tratamiento |
|---|---|---|---|---|
| D01 | Sistema: registro, persistencia, filtros y reporte | Cambiar formato de archivo afecta reglas funcionales; regresiones cruzadas | Alta | Repositorio, servicio y reporte separados |
| D02 | mkdir/write_text repetidos en registrar, cambiar_estado y asignar | Una corrección puede omitirse en uno de los caminos | Alta | Move Method hacia JsonRepositorio.guardar |
| D03 | registrar: siete argumentos de negocio | Inversión accidental de strings válidos | Media | CrearSolicitud y método crear; adaptador conserva registrar |
| D04 | self.d y x | Lectura lenta y baja expresividad al mantener el módulo | Media | solicitudes, solicitud, solicitudes_guardadas |
| D05 | Diccionarios de solicitud con claves repetidas | Errores de claves o estados incoherentes en modificaciones futuras | Media | dataclasses y Estado, Tipo, Prioridad |
| D06 | Bucles de búsqueda de ID repetidos | Diferencias al modificar el caso inexistente | Media | Extract Method _obtener |
| D07 | write_text directo sobre archivo final | Interrupción puede truncar datos; memoria ya modificada si falla | Alta | Escritura temporal, fsync y reemplazo; verificar fallo |
| D08 | __init__: json.loads sin validar estructura | JSON válido con esquema incorrecto falla tarde | Alta | Validación de esquema y DatosInvalidos al abrir |
| D09 | ValueError genérico en reglas | No distingue validación de entidad faltante al integrar otras interfaces | Media | ErrorDominio, ValidacionError y NoEncontrado |
| D10 | Catálogos y almacenamiento ligados al constructor | Pruebas y otra persistencia requieren tocar el servicio | Media | Inyección de Repositorio y catálogos tipados |

Orden de trabajo: caracterización, D01/D02/D07, D03/D04/D05/D06, D08/D09/D10 y verificación.
No se corrige una falla observada en usuarios reales: se reduce riesgo identificado en el código.
