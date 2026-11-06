"""Entidades, valores y errores del dominio académico."""
from dataclasses import dataclass
from enum import Enum

class ErrorDominio(ValueError):
    """Compatible con ValueError de la API inicial."""

class ValidacionError(ErrorDominio):
    pass

class NoEncontrado(ErrorDominio):
    pass

class DatosInvalidos(ValueError):
    pass

class Estado(str, Enum):
    PENDIENTE = "pendiente"
    EN_PROCESO = "en_proceso"
    RESUELTA = "resuelta"

class Tipo(str, Enum):
    CERTIFICADO = "certificado"
    EQUIVALENCIA = "equivalencia"
    CONSULTA = "consulta"

class Prioridad(str, Enum):
    BAJA = "baja"
    MEDIA = "media"
    ALTA = "alta"

@dataclass(frozen=True)
class Estudiante:
    id: str
    nombre: str

@dataclass(frozen=True)
class Responsable:
    id: str
    nombre: str
    area: str

def validar_campos(descripcion, canal, sede, asunto):
    if any(not isinstance(value, str) or not value.strip()
           for value in (descripcion, canal, sede, asunto)):
        raise ValidacionError("Campos obligatorios vacíos")

@dataclass(frozen=True)
class CrearSolicitud:
    estudiante_id: str
    tipo: str
    prioridad: str
    descripcion: str
    canal: str
    sede: str
    asunto: str

    def validar(self):
        try:
            Tipo(self.tipo)
        except ValueError as error:
            raise ValidacionError("Tipo inválido") from error
        try:
            Prioridad(self.prioridad)
        except ValueError as error:
            raise ValidacionError("Prioridad inválida") from error
        validar_campos(self.descripcion, self.canal, self.sede, self.asunto)

@dataclass(frozen=True)
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
        if type(self.id) is not int or self.id < 1:
            raise ValidacionError("Identificador inválido")
        if not isinstance(self.estudiante_id, str) or not self.estudiante_id:
            raise ValidacionError("Estudiante inválido")
        if self.responsable_id is not None and (not isinstance(self.responsable_id, str) or not self.responsable_id):
            raise ValidacionError("Responsable inválido")
        CrearSolicitud(self.estudiante_id, self.tipo, self.prioridad,
                       self.descripcion, self.canal, self.sede, self.asunto).validar()
        try:
            Estado(self.estado)
        except ValueError as error:
            raise ValidacionError("Estado inválido") from error
