# Decisiones y refactorings

1. Python estándar + CLI: alcance reducido, ejecución local y pruebas sin dependencias.
2. Tres entidades explícitas: Estudiante, Responsable, Solicitud. Estado es un valor enumerado.
3. SRP: ServicioSolicitudes coordina casos de uso, JsonRepositorio maneja archivos,
   dominio valida valores y reportes.resumir calcula el agregado.
4. DIP/ISP: servicio depende de Repositorio, con solo listar y guardar. MemoriaRepositorio
   permite probar reglas sin disco. El adaptador Sistema compone dependencias concretas.
5. OCP: agregar otro repositorio no requiere modificar reglas del servicio.
   Agregar un nuevo caso de uso sí puede requerir cambios; no se afirma apertura total.
6. LSP: sustitución estructural entre memoria y JSON para el contrato de persistencia usado.
   Una prueba ejerce crear, asignar, cambiar y reportar con ambas implementaciones.
   No se inventó una jerarquía de herencia para demostrar el principio.
7. Extract Method: _obtener y _actualizar eliminan búsquedas y actualizaciones repetidas.
8. Move Method: escritura de registrar/cambiar_estado/asignar a JsonRepositorio.guardar.
9. Introduce Parameter Object: CrearSolicitud agrupa siete datos; servicio.crear recibe uno.
   Sistema.registrar mantiene la firma original como adaptador para no romper clientes.
10. Replace Data Value with Object: Solicitud inmutable, catálogos tipados y enumeraciones.
11. Rename: self.d/x pasan a solicitudes/solicitud; mejora semántica, no funcionalidad nueva.
12. Extract Function: reporte se separa en resumir y deja de repetir recorridos por estado.
13. Escritura temporal y reemplazo: reduce riesgo de archivo truncado. Se prueba un fallo de
    os.replace; no se demuestra resistencia absoluta a cortes eléctricos o fallos de hardware.
14. Compatibilidad: idénticos métodos operativos, forma JSON, filtros, IDs y mensajes funcionales.
    Cambian deliberadamente los errores ante JSON corrupto o esquema inválido; no son simples
    renombrados. Se separan como mejoras de robustez y cuentan con pruebas específicas.
15. Fuera de alcance: concurrencia, autenticación, cifrado, auditoría de usuarios y despliegue.
