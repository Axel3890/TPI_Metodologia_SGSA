"""Casos de uso independientes del formato de almacenamiento."""
from dataclasses import asdict, replace
from .dominio import CrearSolicitud, DatosInvalidos, Estado, NoEncontrado, Solicitud, ValidacionError
from .reportes import resumir
from .repositorios import Repositorio

class ServicioSolicitudes:
    def __init__(self, repositorio: Repositorio, estudiantes, responsables):
        self.repositorio = repositorio
        self.estudiantes = {estudiante.id: estudiante for estudiante in estudiantes}
        self.responsables = {responsable.id: responsable for responsable in responsables}
        # Detectar corrupción al abrir, antes de permitir nuevas escrituras.
        existentes = self.repositorio.listar()
        if any(s.estudiante_id not in self.estudiantes or
               (s.responsable_id is not None and s.responsable_id not in self.responsables)
               for s in existentes):
            raise DatosInvalidos("Referencias de catálogo inválidas; no se sobrescribió")

    def crear(self, comando: CrearSolicitud):
        if comando.estudiante_id not in self.estudiantes:
            raise NoEncontrado("Estudiante inexistente")
        comando.validar()
        solicitudes = self.repositorio.listar()
        solicitud = Solicitud(id=max((s.id for s in solicitudes), default=0) + 1, **asdict(comando))
        self.repositorio.guardar([*solicitudes, solicitud])
        return asdict(solicitud)

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
        try:
            Estado(estado)
        except ValueError as error:
            raise ValidacionError("Estado inválido") from error
        return self._actualizar(solicitud_id, estado=estado)

    def asignar(self, solicitud_id, responsable_id):
        if responsable_id not in self.responsables:
            raise NoEncontrado("Responsable inexistente")
        return self._actualizar(solicitud_id, responsable_id=responsable_id)

    def buscar(self, estado=None, prioridad=None, texto=""):
        return [asdict(s) for s in self.repositorio.listar()
                if (estado is None or s.estado == estado)
                and (prioridad is None or s.prioridad == prioridad)
                and texto.casefold() in (s.asunto + " " + s.descripcion).casefold()]

    def reporte(self):
        return resumir(self.repositorio.listar())
