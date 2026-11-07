"""Mismo contrato observable para la versión base y la refactorizada."""
import importlib
import os
from pathlib import Path
import tempfile
import unittest

VERSION = os.environ.get("SGSA_VERSION", "inicial")
Sistema = importlib.import_module(VERSION + ".sistema").Sistema

class Contrato(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / "solicitudes.json"
        self.s = Sistema(self.path)

    def registrar(self, **cambios):
        values = dict(estudiante_id="E001", tipo="certificado", prioridad="alta",
                      descripcion="Necesito constancia", canal="consola", sede="central", asunto="Certificado")
        values.update(cambios)
        return self.s.registrar(**values)

    def test_01_registrar(self):
        row = self.registrar()
        self.assertEqual((row["id"], row["estado"], row["responsable_id"]), (1, "pendiente", None))
    def test_02_ids(self):
        self.registrar()
        self.assertEqual(self.registrar()["id"], 2)
    def test_03_estudiante_inexistente(self):
        with self.assertRaisesRegex(ValueError, "Estudiante inexistente"): self.registrar(estudiante_id="X")
    def test_04_tipo_invalido(self):
        with self.assertRaisesRegex(ValueError, "Tipo inválido"): self.registrar(tipo="otro")
    def test_05_prioridad_invalida(self):
        with self.assertRaisesRegex(ValueError, "Prioridad inválida"): self.registrar(prioridad="urgente")
    def test_06_campos_vacios(self):
        for key in ("descripcion", "canal", "sede", "asunto"):
            with self.subTest(key=key):
                with self.assertRaisesRegex(ValueError, "Campos obligatorios vacíos"): self.registrar(**{key:"  "})
        self.assertEqual(self.s.reporte()["total"], 0)
    def test_07_cambiar_estado(self):
        self.registrar()
        self.assertEqual(self.s.cambiar_estado(1,"en_proceso")["estado"], "en_proceso")
    def test_08_estado_invalido(self):
        self.registrar()
        with self.assertRaisesRegex(ValueError, "Estado inválido"): self.s.cambiar_estado(1,"borrada")
        self.assertEqual(self.s.buscar()[0]["estado"], "pendiente")
    def test_09_cambio_inexistente(self):
        with self.assertRaisesRegex(ValueError, "Solicitud inexistente"): self.s.cambiar_estado(9,"resuelta")
    def test_10_asignar(self):
        self.registrar()
        self.assertEqual(self.s.asignar(1,"R001")["responsable_id"], "R001")
    def test_11_responsable_invalido(self):
        self.registrar()
        with self.assertRaisesRegex(ValueError, "Responsable inexistente"): self.s.asignar(1,"X")
    def test_12_asignacion_inexistente(self):
        with self.assertRaisesRegex(ValueError, "Solicitud inexistente"): self.s.asignar(99,"R001")
    def test_13_filtro_estado(self):
        self.registrar(); self.registrar(); self.s.cambiar_estado(2,"resuelta")
        self.assertEqual([x["id"] for x in self.s.buscar(estado="resuelta")], [2])
    def test_14_filtro_prioridad(self):
        self.registrar(); self.registrar(prioridad="baja")
        self.assertEqual([x["id"] for x in self.s.buscar(prioridad="baja")], [2])
    def test_15_busqueda_texto(self):
        self.registrar()
        self.assertEqual(len(self.s.buscar(texto="CONSTANCIA")), 1)
    def test_16_filtros_combinados(self):
        self.registrar(); self.registrar(prioridad="baja")
        self.assertEqual(len(self.s.buscar("pendiente","alta","certificado")), 1)
    def test_17_sin_resultados(self):
        self.registrar()
        self.assertEqual(self.s.buscar(texto="inexistente"), [])
    def test_18_reporte_vacio(self):
        self.assertEqual(self.s.reporte(), {"total":0,"pendiente":0,"en_proceso":0,"resuelta":0})
    def test_19_reporte_estados(self):
        for _ in range(3): self.registrar()
        self.s.cambiar_estado(2,"en_proceso"); self.s.cambiar_estado(3,"resuelta")
        self.assertEqual(self.s.reporte(), {"total":3,"pendiente":1,"en_proceso":1,"resuelta":1})
    def test_20_persistencia_y_reinicio(self):
        self.registrar(); self.s.asignar(1,"R002"); self.s.cambiar_estado(1,"resuelta")
        reloaded = Sistema(self.path)
        self.assertEqual(reloaded.buscar(), self.s.buscar())
        self.assertEqual(reloaded.registrar("E002","consulta","baja","Texto","consola","central","Asunto")["id"],2)
    def test_21_aislamiento_de_resultados(self):
        row = self.registrar(); row["estado"]="inventado"
        results = self.s.buscar(); results[0]["estado"]="inventado"
        self.assertEqual(self.s.buscar()[0]["estado"],"pendiente")
    def test_22_catalogos_y_unicode(self):
        for tipo in ("certificado","equivalencia","consulta"):
            for prioridad in ("baja","media","alta"):
                self.registrar(estudiante_id="E002",tipo=tipo,prioridad=prioridad,asunto="Inscripción")
        self.assertEqual(len(self.s.buscar(texto="INSCRIPCIÓN")),9)
