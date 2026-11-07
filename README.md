# SGSA - Sistema de Gestión de Solicitudes Académicas

Prototipo académico de Metodología de Sistemas II. Python 3.10 o superior.
No necesita dependencias externas, acceso a internet ni una base de datos.
Interfaz de consola y persistencia JSON local. Todos los datos de prueba son sintéticos.

## Inicio rápido

Abrir una terminal en esta carpeta. Usar `python`, `python3` o `py` según la instalación.

```powershell
python main.py --version refactorizada --datos datos-demo.json registrar --asunto "Certificado de alumno regular" --descripcion "Presentación de beca" --prioridad alta
python main.py --version refactorizada --datos datos-demo.json asignar 1 R001
python main.py --version refactorizada --datos datos-demo.json cambiar 1 en_proceso
python main.py --version refactorizada --datos datos-demo.json buscar --estado en_proceso --prioridad alta
python main.py --version refactorizada --datos datos-demo.json reporte
python verificar.py
```

El ID 1 supone un archivo nuevo. Si ya existen datos, usar el ID devuelto al registrar.
Para comparar, repetir con `--version inicial` y otro archivo nuevo.
Se mantiene el default `inicial` para conservar compatibilidad de la CLI.
Los argumentos globales `--version` y `--datos` van antes del comando.

## Catálogos

- Estudiantes: E001 y E002.
- Responsables: R001 (Alumnado), R002 (Secretaría).
- Tipos: certificado, equivalencia, consulta.
- Prioridades: baja, media, alta.
- Estados: pendiente, en_proceso, resuelta.

Los estados permiten cualquier transición entre valores válidos, incluida reapertura;
no se agregaron restricciones nuevas durante el refactoring.
No incluye autenticación, administración de catálogos, adjuntos ni notificaciones.
Una solicitud conserva su contenido original, incluyendo espacios y mayúsculas.

## Estructura

- inicial/: versión base monolítica, conservada como evidencia.
- refactorizada/: dominio, servicio, repositorios, reporte y adaptador compatible.
- main.py: consola compartida.
- tests/: contrato común y robustez.
- docs/: diagnóstico, decisiones, revisión, informe editable y evidencias.
- verificar.py: ejecuta y registra las tres suites.

## Pruebas

`python verificar.py`: 22 pruebas para cada versión y 7 pruebas adicionales para la final.
Las pruebas usan directorios temporales, no modifican tus datos de trabajo.
Los .txt de docs/evidencias son resultados de ejecuciones reales en Python 3.12.14.
Las duraciones varían por equipo. No se afirma un porcentaje de cobertura.

