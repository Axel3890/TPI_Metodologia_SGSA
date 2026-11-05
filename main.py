"""Interfaz común para ejecutar y comparar las dos implementaciones."""
import argparse
import importlib
import json

def main():
    parser = argparse.ArgumentParser(description="Solicitudes académicas - prototipo TPI")
    parser.add_argument("--version", choices=["inicial", "refactorizada"], default="inicial")
    parser.add_argument("--datos", default="datos.json")
    commands = parser.add_subparsers(dest="comando", required=True)
    create = commands.add_parser("registrar")
    create.add_argument("--estudiante", default="E001")
    create.add_argument("--tipo", choices=["certificado", "equivalencia", "consulta"], default="certificado")
    create.add_argument("--prioridad", choices=["baja", "media", "alta"], default="media")
    create.add_argument("--descripcion", required=True)
    create.add_argument("--canal", default="consola")
    create.add_argument("--sede", default="central")
    create.add_argument("--asunto", required=True)
    change = commands.add_parser("cambiar")
    change.add_argument("id", type=int)
    change.add_argument("estado", choices=["pendiente", "en_proceso", "resuelta"])
    assign = commands.add_parser("asignar")
    assign.add_argument("id", type=int)
    assign.add_argument("responsable", choices=["R001", "R002"])
    search = commands.add_parser("buscar")
    search.add_argument("--estado", choices=["pendiente", "en_proceso", "resuelta"])
    search.add_argument("--prioridad", choices=["baja", "media", "alta"])
    search.add_argument("--texto", default="")
    commands.add_parser("reporte")
    args = parser.parse_args()
    try:
        sistema = importlib.import_module(args.version + ".sistema").Sistema(args.datos)
        if args.comando == "registrar":
            result = sistema.registrar(args.estudiante, args.tipo, args.prioridad,
                                        args.descripcion, args.canal, args.sede, args.asunto)
        elif args.comando == "cambiar":
            result = sistema.cambiar_estado(args.id, args.estado)
        elif args.comando == "asignar":
            result = sistema.asignar(args.id, args.responsable)
        elif args.comando == "buscar":
            result = sistema.buscar(args.estado, args.prioridad, args.texto)
        else:
            result = sistema.reporte()
    except (ValueError, OSError) as error:
        parser.exit(1, "Error: " + str(error) + "\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
