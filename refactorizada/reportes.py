"""Cálculo puro del reporte, sin acceso a archivos ni salida de consola."""
from .dominio import Estado

def resumir(solicitudes):
    reporte = {"total": len(solicitudes), **{estado.value: 0 for estado in Estado}}
    for solicitud in solicitudes:
        reporte[solicitud.estado] += 1
    return reporte
