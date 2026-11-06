"""Adaptador de compatibilidad: conserva métodos y respuestas del prototipo."""
from .dominio import CrearSolicitud, Estudiante, Responsable
from .repositorios import JsonRepositorio
from .servicio import ServicioSolicitudes

class Sistema:
    def __init__(self, ruta):
        self.servicio = ServicioSolicitudes(
            JsonRepositorio(ruta),
            [Estudiante("E001", "Estudiante Uno"), Estudiante("E002", "Estudiante Dos")],
            [Responsable("R001", "Responsable Uno", "Alumnado"),
             Responsable("R002", "Responsable Dos", "Secretaría")])

    def registrar(self, estudiante_id, tipo, prioridad, descripcion, canal, sede, asunto):
        return self.servicio.crear(CrearSolicitud(estudiante_id=estudiante_id, tipo=tipo,
            prioridad=prioridad, descripcion=descripcion, canal=canal, sede=sede, asunto=asunto))

    def cambiar_estado(self, solicitud_id, estado):
        return self.servicio.cambiar_estado(solicitud_id, estado)

    def asignar(self, solicitud_id, responsable_id):
        return self.servicio.asignar(solicitud_id, responsable_id)

    def buscar(self, estado=None, prioridad=None, texto=""):
        return self.servicio.buscar(estado, prioridad, texto)

    def reporte(self):
        return self.servicio.reporte()
