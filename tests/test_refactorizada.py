from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from refactorizada.dominio import CrearSolicitud, DatosInvalidos, Estudiante, Responsable
from refactorizada.repositorios import JsonRepositorio, MemoriaRepositorio
from refactorizada.servicio import ServicioSolicitudes
from refactorizada.sistema import Sistema

class Robustez(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / "datos.json"

    def crear(self, sistema):
        return sistema.registrar("E001","consulta","baja","Descripción","consola","central","Asunto")

    def test_json_corrupto_se_conserva(self):
        self.path.write_text("{roto",encoding="utf-8")
        with self.assertRaises(DatosInvalidos): Sistema(self.path)
        self.assertEqual(self.path.read_text(encoding="utf-8"),"{roto")

    def test_esquema_incorrecto(self):
        for contenido in ('{}','[{}]','[1]'):
            with self.subTest(contenido=contenido):
                self.path.write_text(contenido,encoding="utf-8")
                with self.assertRaises(DatosInvalidos): Sistema(self.path)

    def test_error_de_reemplazo_conserva_archivo(self):
        sistema = Sistema(self.path); self.crear(sistema)
        original = self.path.read_bytes()
        with patch("refactorizada.repositorios.os.replace", side_effect=OSError("Fallo simulado")):
            with self.assertRaises(OSError): sistema.cambiar_estado(1,"resuelta")
        self.assertEqual(self.path.read_bytes(),original)
        self.assertEqual(sistema.buscar()[0]["estado"],"pendiente")
        self.assertEqual(list(self.path.parent.glob("*.tmp")),[])

    def test_sustitucion_memoria_por_json(self):
        for repo in (MemoriaRepositorio(),JsonRepositorio(self.path)):
            with self.subTest(repo=type(repo).__name__):
                servicio = ServicioSolicitudes(repo,[Estudiante("E001","Uno")],[Responsable("R001","Uno","Área")])
                result = servicio.crear(CrearSolicitud("E001","consulta","baja","Texto","consola","central","Asunto"))
                self.assertEqual(result["id"],1)
                self.assertEqual(servicio.asignar(1,"R001")["responsable_id"],"R001")
                servicio.cambiar_estado(1,"resuelta")
                self.assertEqual(servicio.reporte()["resuelta"],1)

    def test_ids_duplicados(self):
        sistema = Sistema(self.path); self.crear(sistema)
        import json
        fila = sistema.buscar()[0]
        self.path.write_text(json.dumps([fila,fila]),encoding="utf-8")
        with self.assertRaises(DatosInvalidos): Sistema(self.path)

    def test_referencia_invalida(self):
        sistema = Sistema(self.path); self.crear(sistema)
        import json
        fila = sistema.buscar()[0]; fila["estudiante_id"]="X"
        self.path.write_text(json.dumps([fila]),encoding="utf-8")
        with self.assertRaises(DatosInvalidos): Sistema(self.path)

    def test_migracion_desde_inicial(self):
        from inicial.sistema import Sistema as Inicial
        previo = Inicial(self.path); self.crear(previo); previo.asignar(1,"R002")
        nuevo = Sistema(self.path)
        self.assertEqual(nuevo.buscar(), previo.buscar())
        nuevo.cambiar_estado(1,"resuelta")
        self.assertEqual(Inicial(self.path).buscar(),nuevo.buscar())
