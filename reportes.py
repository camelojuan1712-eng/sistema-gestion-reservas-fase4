# -*- coding: utf-8 -*-
"""
reportes.py
Módulo de Itan Bautista - Fase 4

Lee el archivo de logs generado por el sistema y produce un resumen
con el total de reservas registradas, ingresos, errores y advertencias.

Funciones públicas:
    generar_reporte(archivo_log) -> dict

Funciones internas (prefijo _):
    _reporte_vacio()          -> dict
    _extraer_monto(linea)     -> float | None
"""

import os
import re

# Palabras clave que indican que una línea de log contiene un monto
_PALABRAS_MONTO = re.compile(
    r"(?:precio|monto|ingreso|valor)\s*:\s*(\d+(?:\.\d+)?)",
    re.IGNORECASE,
)

# Palabras clave que indican que una línea registra una reserva nueva
_PALABRAS_RESERVA = re.compile(
    r"(?:nueva\s+)?reserva\s+(?:creada|registrada)",
    re.IGNORECASE,
)


# ──────────────────────────────────────────────
# FUNCIONES INTERNAS
# ──────────────────────────────────────────────

def _reporte_vacio():
    """
    Retorna un diccionario con la estructura base de un reporte vacío.

    Retorna:
        dict con las claves:
            total_reservas    (int)
            total_ingresos    (float)
            total_errores     (int)
            total_advertencias(int)
            total_lineas      (int)
            reservas_detalle  (list)
    """
    return {
        "total_reservas":     0,
        "total_ingresos":     0.0,
        "total_errores":      0,
        "total_advertencias": 0,
        "total_lineas":       0,
        "reservas_detalle":   [],
    }


def _extraer_monto(linea):
    """
    Busca un monto numérico en una línea de log.

    Solo detecta montos que estén precedidos por las palabras clave:
    precio, monto, ingreso o valor (seguidas de ':').

    Parámetros:
        linea (str): Línea de texto del log.

    Retorna:
        float: El monto encontrado.
        None:  Si la línea no contiene ninguna de las palabras clave.
    """
    coincidencia = _PALABRAS_MONTO.search(linea)
    if coincidencia:
        return float(coincidencia.group(1))
    return None


# ──────────────────────────────────────────────
# FUNCIÓN PRINCIPAL
# ──────────────────────────────────────────────

def generar_reporte(archivo_log):
    """
    Lee el archivo de logs y genera un resumen estadístico.

    Analiza cada línea del log para detectar:
      - Reservas creadas o registradas
      - Montos/ingresos (precio, monto, ingreso, valor)
      - Errores (nivel ERROR)
      - Advertencias (nivel WARNING)

    Si el archivo no existe, retorna un reporte vacío sin lanzar error.

    Parámetros:
        archivo_log (str): Ruta al archivo .log a analizar.

    Retorna:
        dict: Reporte con totales y detalle de reservas.
    """
    reporte = _reporte_vacio()

    if not os.path.exists(archivo_log):
        return reporte

    with open(archivo_log, "r", encoding="utf-8") as f:
        for linea in f:
            linea_limpia = linea.strip()
            if not linea_limpia:
                continue

            reporte["total_lineas"] += 1

            # Detectar nivel ERROR
            if " - ERROR - " in linea_limpia or linea_limpia.startswith("ERROR"):
                reporte["total_errores"] += 1

            # Detectar nivel WARNING
            elif " - WARNING - " in linea_limpia or linea_limpia.startswith("WARNING"):
                reporte["total_advertencias"] += 1

            # Detectar reservas creadas/registradas
            if _PALABRAS_RESERVA.search(linea_limpia):
                reporte["total_reservas"] += 1
                reporte["reservas_detalle"].append(linea_limpia)

            # Detectar montos e ingresarlos al total
            monto = _extraer_monto(linea_limpia)
            if monto is not None:
                reporte["total_ingresos"] += monto

    return reporte