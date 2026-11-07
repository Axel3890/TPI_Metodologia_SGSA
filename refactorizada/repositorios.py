"""Contrato mínimo de persistencia y dos implementaciones intercambiables."""
from dataclasses import asdict
import json
import os
from pathlib import Path
import tempfile
from typing import Protocol
from .dominio import DatosInvalidos, Solicitud

class Repositorio(Protocol):
    def listar(self) -> list[Solicitud]: ...
    def guardar(self, solicitudes: list[Solicitud]) -> None: ...

class MemoriaRepositorio:
    def __init__(self):
        self._solicitudes = []

    def listar(self):
        return list(self._solicitudes)

    def guardar(self, solicitudes):
        self._solicitudes = list(solicitudes)

class JsonRepositorio:
    def __init__(self, ruta):
        self.ruta = Path(ruta)

    def listar(self):
        if not self.ruta.exists():
            return []
        try:
            datos = json.loads(self.ruta.read_text(encoding="utf-8"))
            if not isinstance(datos, list):
                raise ValueError("Se esperaba una lista")
            solicitudes = [Solicitud(**item) for item in datos]
            ids = [solicitud.id for solicitud in solicitudes]
            if len(set(ids)) != len(ids):
                raise ValueError("Identificadores duplicados")
            return solicitudes
        except (ValueError, TypeError, UnicodeError) as error:
            raise DatosInvalidos("Archivo de solicitudes inválido; no se sobrescribió") from error

    def guardar(self, solicitudes):
        contenido = json.dumps([asdict(solicitud) for solicitud in solicitudes], ensure_ascii=False, indent=2)
        self.ruta.parent.mkdir(parents=True, exist_ok=True)
        temporal = None
        try:
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
