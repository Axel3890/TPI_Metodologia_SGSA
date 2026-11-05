"""Prototipo didáctico inicial: funcional, con deuda técnica identificable."""
import json
from pathlib import Path

class Sistema:
    def __init__(self, ruta):
        self.ruta = Path(ruta)
        self.estudiantes = [{"id": "E001", "nombre": "Estudiante Uno"},
                            {"id": "E002", "nombre": "Estudiante Dos"}]
        self.responsables = [{"id": "R001", "nombre": "Responsable Uno", "area": "Alumnado"},
                             {"id": "R002", "nombre": "Responsable Dos", "area": "Secretaría"}]
        self.d = json.loads(self.ruta.read_text(encoding="utf-8")) if self.ruta.exists() else []

    def registrar(self, estudiante_id, tipo, prioridad, descripcion, canal, sede, asunto):
        if estudiante_id not in [x["id"] for x in self.estudiantes]:
            raise ValueError("Estudiante inexistente")
        if tipo not in ["certificado", "equivalencia", "consulta"]:
            raise ValueError("Tipo inválido")
        if prioridad not in ["baja", "media", "alta"]:
            raise ValueError("Prioridad inválida")
        if not descripcion.strip() or not canal.strip() or not sede.strip() or not asunto.strip():
            raise ValueError("Campos obligatorios vacíos")
        x = {"id": max([x["id"] for x in self.d], default=0) + 1,
             "estudiante_id": estudiante_id, "tipo": tipo, "prioridad": prioridad,
             "descripcion": descripcion, "canal": canal, "sede": sede, "asunto": asunto,
             "estado": "pendiente", "responsable_id": None}
        self.d.append(x)
        self.ruta.parent.mkdir(parents=True, exist_ok=True)
        self.ruta.write_text(json.dumps(self.d, ensure_ascii=False, indent=2), encoding="utf-8")
        return dict(x)

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

    def asignar(self, solicitud_id, responsable_id):
        if responsable_id not in [x["id"] for x in self.responsables]:
            raise ValueError("Responsable inexistente")
        for x in self.d:
            if x["id"] == solicitud_id:
                x["responsable_id"] = responsable_id
                self.ruta.parent.mkdir(parents=True, exist_ok=True)
                self.ruta.write_text(json.dumps(self.d, ensure_ascii=False, indent=2), encoding="utf-8")
                return dict(x)
        raise ValueError("Solicitud inexistente")

    def buscar(self, estado=None, prioridad=None, texto=""):
        return [dict(x) for x in self.d
                if (estado is None or x["estado"] == estado)
                and (prioridad is None or x["prioridad"] == prioridad)
                and (texto.casefold() in (x["asunto"] + " " + x["descripcion"]).casefold())]

    def reporte(self):
        return {"total": len(self.d), "pendiente": sum(x["estado"] == "pendiente" for x in self.d),
                "en_proceso": sum(x["estado"] == "en_proceso" for x in self.d),
                "resuelta": sum(x["estado"] == "resuelta" for x in self.d)}
