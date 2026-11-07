METODOLOGÍA DE SISTEMAS II | TRABAJO PRÁCTICO INTEGRADOR

# Evolución profesional de un sistema de solicitudes académicas

**Calidad interna, deuda técnica, refactoring y revisión técnica**

| Datos de portada | Estado |
| --- | --- |
| Estudiante | Axel Gomez - Cristian Ayala|
| Comisión | 4 |
| Fecha | 71 de noviembre de 2026 |

## Alcance de este material

Se creó un prototipo didáctico de consola para el caso sugerido en la consigna y se desarrolló una segunda implementación con responsabilidades separadas. No se presenta como un sistema heredado real ni como un producto en producción.

## Justificación de modalidad: propuesta a validar

El módulo tiene un alcance reducido, cinco operaciones y catálogos sintéticos, por lo que puede abordarse de forma individual. Esta razón técnica es una propuesta: la situación personal y la aprobación de la modalidad deben confirmarse antes de la entrega.

SÍNTESIS Y NAVEGACIÓN

# Resumen ejecutivo

Se trabaja sobre un prototipo de gestión de solicitudes académicas con tres entidades principales.

La versión inicial registra, asigna, cambia estados, filtra y reporta con persistencia JSON.

El diagnóstico identifica diez debilidades de diseño y almacenamiento, ordenadas por riesgo.

La versión final separa dominio, casos de uso, persistencia y reporte, conservando la interfaz.

Las 22 pruebas comunes pasan en cada versión y siete pruebas adicionales verifican robustez.

La publicación del repositorio, la portada definitiva y la defensa personal completan la entrega.

## Organización del informe

| Apartado | Contenido |
| --- | --- |
| 1-2 | Sistema base, alcance y calidad externa/interna |
| 3 | Diez debilidades con evidencia, riesgo y prioridad |
| 4 | SOLID, Clean Code y arquitectura |
| 5 | Refactorings con fragmentos antes/después |
| 6 | Pruebas, resultados y salida de ejecución |
| 7 | Revisión técnica, feedback y aceptación |
| 8 y anexos | Conclusiones, historia Git, defensa y pendientes |


ETAPA 1

# Sistema base y alcance

El SGSA registra solicitudes de estudiantes y facilita su seguimiento por personal administrativo. El actor operativo de esta versión es un operador de consola: representa las acciones de alumnado y responsables sin autenticar personas reales.

| Entidad | Atributos principales | Relación |
| --- | --- | --- |
| Estudiante | ID y nombre | Un estudiante puede originar muchas solicitudes. |
| Solicitud | ID, estudiante, tipo, prioridad, descripción, canal, sede, asunto, estado y responsable | Pertenece a un estudiante y puede tener un responsable. |
| Responsable | ID, nombre y área | Un responsable puede recibir muchas solicitudes. |

| Operación | Resultado verificable |
| --- | --- |
| Registrar solicitud | ID consecutivo, estado pendiente y responsable inicialmente vacío. |
| Cambiar estado | Acepta pendiente, en_proceso o resuelta; rechaza otros valores. |
| Asignar responsable | Vincula R001 o R002; rechaza referencias inexistentes. |
| Buscar y filtrar | Combina estado, prioridad y texto sin distinguir mayúsculas. |
| Reporte básico | Cuenta total y cantidad por cada estado. |

## Tecnología y exclusiones

Python 3.10 o superior, biblioteca estándar, consola y archivo JSON. Se verificó con Python 3.12.14 en Windows. No hay paquetes externos para ejecutar el proyecto. No incluye login, interfaz web, carga de documentos, notificaciones, múltiples escritores concurrentes ni gestión de catálogos.

Catálogos sintéticos: estudiantes E001/E002 y responsables R001/R002. Tipos: certificado, equivalencia y consulta. Prioridades: baja, media y alta. Se permite reabrir solicitudes: no se agregó una política de transición durante el refactoring.

ETAPA 2

# Calidad externa e interna

| Dimensión | Versión inicial | Versión refactorizada |
| --- | --- | --- |
| Externa: operaciones | Las cinco operaciones son utilizables desde consola. | Conserva comandos, respuestas JSON y casos de uso. |
| Externa: validación | Rechaza tipos, prioridades, estados y referencias inválidas. | Mantiene los errores funcionales del contrato común. |
| Interna: responsabilidades | Una clase lee archivos, valida, actualiza, filtra y reporta. | Servicio, repositorio, dominio y reporte tienen funciones diferenciadas. |
| Interna: legibilidad | Nombres d/x y diccionarios con claves repetidas. | Entidades con atributos definidos y nombres descriptivos. |
| Interna: evolución | Otra persistencia exige cambiar el sistema. | El servicio recibe un repositorio de contrato mínimo. |
| Robustez del almacenamiento | Escritura directa y formato no validado al cargar. | Reemplazo desde temporal y rechazo temprano de datos inválidos. |

## Por qué funcionar no basta

Una solicitud puede registrarse correctamente aunque la estructura sea difícil de mantener. Por ejemplo, la misma escritura JSON aparece en tres operaciones: cambiar cómo se guarda exige revisar tres sitios. Un error omitido en uno de ellos produce un comportamiento inconsistente.

## Evidencia y límites de la comparación

El módulo inicial tiene 63 líneas físicas en un archivo; el final tiene 247 en cinco archivos, sin contar la consola ni las pruebas. El aumento es un costo de separar responsabilidades y explicitar contratos; no demuestra por sí solo una mejora. No se midió tiempo de mantenimiento, cobertura ni rendimiento.

ETAPA 3 | DIAGNÓSTICO 1/2

# Deuda técnica priorizada

## D01 | Responsabilidades mezcladas

**Ubicación:** inicial/sistema.py:5. **Prioridad:** Alta.

Reglas, lectura, escritura y reporte conviven. Un cambio de persistencia puede afectar operaciones no relacionadas.

## D02 | Código duplicado

**Ubicación:** inicial/sistema.py:29. **Prioridad:** Alta.

La escritura aparece en registrar, cambiar_estado y asignar. Riesgo de corregir solo uno de los caminos.

## D03 | Lista larga de parámetros

**Ubicación:** inicial/sistema.py:14. **Prioridad:** Media.

Siete datos de negocio como strings. Riesgo de intercambiar canal, sede o asunto sin fallo evidente.

## D04 | Nombres poco expresivos

**Ubicación:** inicial/sistema.py:12. **Prioridad:** Media.

d y x exigen reconstruir significado. Aumentan esfuerzo de lectura y revisión de cambios.

## D05 | Datos poco estructurados

**Ubicación:** inicial/sistema.py:23. **Prioridad:** Media.

La solicitud es un diccionario sin esquema explícito. Riesgo de claves erróneas y valores incoherentes.

Prioridades: alta cuando hay riesgo para datos o cambios transversales; media cuando domina el costo de evolución y comprensión. Son riesgos diagnosticados en el prototipo, no incidentes institucionales observados.

ETAPA 3 | DIAGNÓSTICO 2/2

# Riesgos y orden de corrección

## D06 | Búsqueda repetida

**Ubicación:** inicial/sistema.py:35. **Prioridad:** Media.

Dos operaciones repiten el recorrido para hallar un ID. Riesgo de divergencia ante una corrección.

## D07 | Escritura directa sobre archivo

**Ubicación:** inicial/sistema.py:29. **Prioridad:** Alta.

La actualización reemplaza contenido sin archivo temporal; una interrupción puede truncar datos.

## D08 | Ausencia de validación de esquema

**Ubicación:** inicial/sistema.py:12. **Prioridad:** Alta.

JSON válido pero mal estructurado se acepta al iniciar y falla después, al operar.

## D09 | Errores no diferenciados

**Ubicación:** inicial/sistema.py:16. **Prioridad:** Media.

Una interfaz integradora no distingue validación de entidad faltante por el tipo de excepción.

## D10 | Dependencias concretas embebidas

**Ubicación:** inicial/sistema.py:6. **Prioridad:** Media.

Catálogos y almacenamiento se construyen dentro de Sistema, dificultando sustituirlos para probar.

## Secuencia de mejora

Primero se fijó el contrato con pruebas. Luego se separó la persistencia y se eliminó la escritura repetida; se introdujeron entidades, objetos de parámetros y búsquedas compartidas. Por último se verificaron robustez, compatibilidad y documentación. No se agregó funcionalidad de negocio para aumentar el tamaño del sistema.

ETAPA 4

# SOLID y Clean Code aplicados

| Principio | Aplicación y límite |
| --- | --- |
| SRP | ServicioSolicitudes coordina operaciones; JsonRepositorio carga/guarda; dominio valida valores; resumir calcula reportes. |
| OCP | Otro repositorio puede integrarse sin cambiar el servicio. No se afirma que todo cambio de negocio sea una extensión sin modificar código. |
| LSP | MemoriaRepositorio y JsonRepositorio se sustituyen bajo el mismo contrato estructural; una prueba ejecuta casos de uso con ambos. No hay herencia artificial. |
| ISP | Repositorio expone solo listar y guardar, las dos operaciones consumidas por el servicio. |
| DIP | ServicioSolicitudes recibe Repositorio; el adaptador Sistema compone JsonRepositorio y los catálogos concretos. |

## Relaciones de la arquitectura final

| Componente | Depende de | Responsabilidad |
| --- | --- | --- |
| main.py | Sistema compatible | Interpretar comandos y mostrar resultados. |
| Sistema | Servicio + JSON + catálogos | Componer dependencias y conservar API antigua. |
| ServicioSolicitudes | Repositorio + dominio + resumir | Coordinar reglas y casos de uso. |
| JsonRepositorio / MemoriaRepositorio | Solicitud / biblioteca estándar | Implementar el contrato de persistencia. |

Clean Code: solicitudes y solicitud reemplazan d/x; _obtener centraliza la búsqueda; las entidades son inmutables; los errores tienen nombres propios y mantienen compatibilidad con ValueError. Las funciones separan consola, cálculo y acceso a archivos.

ETAPA 5 | REFACTORING 1/3

# Extracción y reubicación

## R1. Extract Method: buscar y actualizar por identificador

Antes, cambiar_estado y asignar repiten un recorrido. Después, ambos delegan a _actualizar, que reutiliza _obtener. Se conserva el mensaje “Solicitud inexistente” y el formato del resultado.

**inicial/sistema.py | líneas 32-41**

```python
    def cambiar_estado(self, solicitud_id, estado):
        if estado not in ["pendiente", "en_proceso", "resuelta"]:
            raise ValueError("Estado inválido")
        for x in self.d:
            if x["id"] == solicitud_id:
                x["estado"] = estado
                self.ruta.parent.mkdir(parents=True, exist_ok=True)
                self.ruta.write_text(json.dumps(self.d, ensure_ascii=False, indent=2), encoding="utf-8")
                return dict(x)
        raise ValueError("Solicitud inexistente")
```

**refactorizada/servicio.py | líneas 28-41**

```python
    def _obtener(self, solicitudes, solicitud_id):
        for solicitud in solicitudes:
            if solicitud.id == solicitud_id:
                return solicitud
        raise NoEncontrado("Solicitud inexistente")

    def _actualizar(self, solicitud_id, **cambios):
        solicitudes = self.repositorio.listar()
        actual = self._obtener(solicitudes, solicitud_id)
        actualizada = replace(actual, **cambios)
        self.repositorio.guardar([actualizada if s.id == solicitud_id else s for s in solicitudes])
        return asdict(actualizada)

    def cambiar_estado(self, solicitud_id, estado):
```

## R2. Move Method: persistencia al repositorio

La responsabilidad de escribir sale de las tres operaciones del sistema y pasa a JsonRepositorio.guardar. El servicio comunica una lista de entidades al contrato Repositorio. La prueba de sustitución verifica que las reglas puedan ejecutarse también en memoria.

**refactorizada/servicio.py | líneas 19-26**

```python
    def crear(self, comando: CrearSolicitud):
        if comando.estudiante_id not in self.estudiantes:
            raise NoEncontrado("Estudiante inexistente")
        comando.validar()
        solicitudes = self.repositorio.listar()
        solicitud = Solicitud(id=max((s.id for s in solicitudes), default=0) + 1, **asdict(comando))
        self.repositorio.guardar([*solicitudes, solicitud])
        return asdict(solicitud)
```

ETAPA 5 | REFACTORING 2/3

# Objeto de parámetros y entidades

## R3. Introduce Parameter Object

Antes: registrar recibe siete datos de negocio. Después: crear recibe un CrearSolicitud con campos nombrados. Sistema.registrar conserva la firma inicial como adaptador de compatibilidad; el objeto de parámetros se utiliza dentro del nuevo diseño.

**inicial/sistema.py | líneas 14-15**

```python
    def registrar(self, estudiante_id, tipo, prioridad, descripcion, canal, sede, asunto):
        if estudiante_id not in [x["id"] for x in self.estudiantes]:
```

**refactorizada/dominio.py | líneas 49-57**

```python
class CrearSolicitud:
    estudiante_id: str
    tipo: str
    prioridad: str
    descripcion: str
    canal: str
    sede: str
    asunto: str

```

**refactorizada/sistema.py | líneas 14-16**

```python
    def registrar(self, estudiante_id, tipo, prioridad, descripcion, canal, sede, asunto):
        return self.servicio.crear(CrearSolicitud(estudiante_id=estudiante_id, tipo=tipo,
            prioridad=prioridad, descripcion=descripcion, canal=canal, sede=sede, asunto=asunto))
```

## R4. Replace Data Value with Object

Solicitud reemplaza el diccionario interno mediante una dataclass inmutable. Al crear o reemplazar una entidad se verifican ID, tipos, prioridad, contenido y estado. Las respuestas públicas vuelven a diccionarios con asdict, de modo que el formato consumido por la consola se mantiene.

**refactorizada/dominio.py | líneas 70-82**

```python
class Solicitud:
    id: int
    estudiante_id: str
    tipo: str
    prioridad: str
    descripcion: str
    canal: str
    sede: str
    asunto: str
    estado: str = Estado.PENDIENTE.value
    responsable_id: str | None = None

    def __post_init__(self):
```

Validación de los refactorings: contrato común 01-22; compatibilidad de archivo: test_migracion_desde_inicial. Las respuestas no exponen alias mutables: contrato 21.

ETAPA 5 | REFACTORING 3/3

# Reporte y robustez diferenciada

## R5. Extract Function y Rename

El reporte deja de repetir un recorrido por cada estado y pasa a una función pura con nombres descriptivos. Mantiene exactamente las claves total, pendiente, en_proceso y resuelta.

**inicial/sistema.py | líneas 60-63**

```python
    def reporte(self):
        return {"total": len(self.d), "pendiente": sum(x["estado"] == "pendiente" for x in self.d),
                "en_proceso": sum(x["estado"] == "en_proceso" for x in self.d),
                "resuelta": sum(x["estado"] == "resuelta" for x in self.d)}
```

**refactorizada/reportes.py | líneas 4-8**

```python
def resumir(solicitudes):
    reporte = {"total": len(solicitudes), **{estado.value: 0 for estado in Estado}}
    for solicitud in solicitudes:
        reporte[solicitud.estado] += 1
    return reporte
```

## Mejora adicional: archivo temporal y reemplazo

Este cambio agrega garantías ante un escenario de falla y se documenta aparte del refactoring estructural. La escritura se completa en un temporal del mismo directorio, se sincroniza y luego se reemplaza el destino. Ante el fallo simulado de reemplazo, el archivo anterior queda intacto y el temporal se limpia.

**refactorizada/repositorios.py | líneas 48-57**

```python
            with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=self.ruta.parent,
                                             prefix=self.ruta.name + ".", suffix=".tmp", delete=False) as archivo:
                temporal = Path(archivo.name)
                archivo.write(contenido)
                archivo.flush()
                os.fsync(archivo.fileno())
            os.replace(temporal, self.ruta)
        finally:
            if temporal is not None:
                temporal.unlink(missing_ok=True)
```

También cambia deliberadamente el tratamiento de JSON corrupto o de esquema inválido: se informa DatosInvalidos al abrir y no se sobrescribe. No se prueba recuperación absoluta ante cortes eléctricos ni se resuelve la concurrencia entre procesos.

ETAPA 6 | VERIFICACIÓN

# Pruebas antes y después

| Grupo | Escenarios | Resultado real |
| --- | --- | --- |
| Contrato inicial | Registro, IDs, validaciones, estados, asignación, filtros, reporte, reinicio, aislamiento y Unicode. | 22/22 métodos de prueba |
| Contrato final | La misma suite y el mismo contrato observable. | 22/22 métodos de prueba |
| Robustez final | JSON corrupto; esquema inválido; fallo de reemplazo; memoria/JSON; IDs duplicados; referencias; migración. | 7/7 métodos de prueba |
| Consola | Registrar, asignar, cambiar, buscar, resolver, reportar y rechazar responsable fuera del catálogo. | 7/7 pasos idénticos |
| Compilación | Módulos, consola, verificador y pruebas con compileall. | Correcta |

## Cómo se verificó la preservación del comportamiento

Las 22 pruebas se escribieron sobre la versión base antes de agregar la implementación final. Se ejecutan por separado mediante SGSA_VERSION, contra archivos temporales nuevos. Incluyen resultados esperados, no solo comparación entre dos programas que podrían equivocarse igual. La migración verifica que el JSON inicial pueda abrirse, modificarse y releerse con ambas versiones.

Son 51 ejecuciones de métodos de prueba (22 + 22 + 7); los subcasos de cada método no se cuentan como pruebas independientes. La equivalencia demostrada está limitada a los escenarios cubiertos; no es una prueba formal para toda entrada posible.

## Reproducción y evidencias

```python
python verificar.py
python -m compileall -q inicial refactorizada tests main.py verificar.py
```

Consultar docs/evidencias/pruebas-inicial.txt, pruebas-refactorizada.txt, robustez.txt, demo-consola.txt y validacion.txt. No se midieron cobertura, carga ni latencia.

ETAPA 6 | EVIDENCIA VISUAL

# Salida de ejecución reproducible

La imagen reproduce texto de la ejecución real, conservado en los archivos de evidencia. Se renderizó para facilitar su lectura en el informe; no se presenta como una captura de una interfaz gráfica.

![Salida real renderizada](evidencias/salida-ejecucion.png)

## Qué permite concluir

El flujo de demostración creó una solicitud, la asignó, cambió su estado, la buscó, la resolvió y obtuvo un reporte consistente. La consola rechazó un responsable fuera del catálogo con código de salida 2 de argparse. Las pruebas del servicio, por separado, verificaron los errores de referencias y solicitudes inexistentes.

## Qué queda fuera de esta evidencia

No acredita rendimiento bajo carga, disponibilidad de un servicio web, autorización de usuarios, pruebas de usabilidad ni bloqueo concurrente. La CLI es suficiente para el prototipo académico, pero no representa una solución lista para la institución.

ETAPA 7

# Revisión técnica y aceptación

| Control aplicado | Resultado | Evidencia |
| --- | --- | --- |
| Entidades y operaciones | Conforme | 3 entidades; 5 operaciones verificadas. |
| Contrato externo | Conforme | 22/22 casos en ambas versiones; 7 pasos CLI. |
| Separación y abstracción | Conforme en alcance | Servicio + Repositorio; memoria y JSON. |
| Validación y datos sintéticos | Conforme | Catálogos de ejemplo y pruebas de entradas inválidas. |
| Fallo de reemplazo / corrupción | Conforme en escenarios probados | 7 pruebas de robustez. |
| Imports en cabecera | Corregido | DatosInvalidos movido del constructor al encabezado. |
| Comprensión y revisión humana | Pendiente | Requiere validación del estudiante. |
| GitHub, video y comisión | Pendiente | Son recursos de entrega externos a la prueba local. |

## Feedback registrado y acciones

**R01:** conservar registrar aunque cambie el diseño interno. Se resolvió con un adaptador y contrato común. **R02:** separar las garantías nuevas del refactoring; se documentaron y probaron como robustez. **R03:** evitar un import local innecesario; se corrigió y se repitieron las suites. **R04:** no presentar más líneas como evidencia de calidad; se declararon costo y límites.

La revisión fue asistida por ChatGPT/Codex; no se inventa un compañero, una aprobación humana ni una validación de la cátedra. El checklist completo y el feedback están en docs/code-review.md.

**Aceptación técnica propuesta:** compilación correcta, contrato inicial/final completo, robustez sin fallos en los casos probados, datos sintéticos y documentación trazable. Se cumple en la ejecución registrada. La aceptación académica sigue pendiente.

ETAPA 8

# Conclusiones y trabajo futuro

La comparación muestra que el mismo comportamiento puede sostenerse con estructuras internas diferentes. En la versión inicial, las operaciones son visibles y utilizables, pero escribir, validar y reportar dentro de una sola clase concentra motivos de cambio. La versión final distribuye esas responsabilidades y permite sustituir el almacenamiento sin rehacer los casos de uso.

Las pruebas de caracterización ofrecen una referencia concreta para evaluar cambios: incluyen valores esperados y escenarios de error. La escritura temporal y la validación del archivo agregan comportamiento de robustez; explicitar esa diferencia evita llamar refactoring a toda modificación.

## Costos y dificultades

Separar componentes aumentó archivos y líneas. Para un módulo pequeño, esa estructura solo se justifica por el aprendizaje y por cambios previsibles. El adaptador mantiene compatibilidad, aunque duplica parte de las firmas. Durante la ejecución se ajustó el directorio temporal de pruebas a una ubicación escribible del entorno; no fue un defecto del dominio ni se ocultó una falla funcional.

## Pendientes técnicos

Para uso real harían falta autenticación, permisos, catálogos administrables, auditoría de cambios y una persistencia transaccional si hay varios procesos. La conservación del archivo ante un fallo simulado no equivale a garantizar integridad absoluta frente a hardware o cortes de energía.

## Reflexión individual: guía para redactar

Reflexión individual

Al realizar este trabajo comprendimos que un sistema puede funcionar y, aun así, ser difícil de mantener. Comparar las dos versiones nos permitió ver cómo separar responsabilidades y escribir pruebas ayuda a modificar el código con más seguridad. También aprendimos que las mejoras deben justificarse con ejemplos y verificaciones.


## Ubicaciones documentales

README.md explica ejecución e instalación; docs/diagnostico.md prioriza smells; docs/decisiones.md justifica diseño; docs/code-review.md registra feedback; docs/guion-defensa.md organiza la demostración; docs/informe.md permite editar el texto; docs/entrega-pendiente.md controla la finalización.


## Declaración de asistencia

Se utilizó ChatGPT para interpretar ayudar a realizar el tp, no se le pidio realizar completamente si no como guia.
Todo se revisó manualmente.

Prompts de apoyo para corregir el trabajo

- «Revisá si el informe cumple todas las etapas de la consigna y señalá qué falta, sin reescribirlo».
- «Indicá qué afirmaciones del informe no están respaldadas por el código o las pruebas».
- «Revisá si los casos de prueba realmente comparan el comportamiento de las dos versiones».
- «Marcá errores de redacción y explicá cómo corregirlos».
