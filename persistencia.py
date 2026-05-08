# -*- coding: utf-8 -*-
"""
persistencia.py
Módulo de Itan Bautista - Fase 4

Guarda y carga reservas desde un archivo de texto plano usando
el separador '|'. No requiere base de datos.

Funciones:
    guardar_reservas(lista_reservas, archivo) -> int
    cargar_reservas(archivo) -> list[dict]
    eliminar_archivo(archivo) -> bool
"""

import os

# Separador de campos en el archivo de texto
SEPARADOR = "|"

# Orden de los campos en cada línea del archivo
CAMPOS = [
    "id_reserva",
    "id_cliente",
    "nombre_cliente",
    "email_cliente",
    "nombre_servicio",
    "precio",
    "fecha",
]


# ──────────────────────────────────────────────
# GUARDAR
# ──────────────────────────────────────────────

def guardar_reservas(lista_reservas, archivo="reservas.txt"):
    """
    Guarda una lista de reservas en un archivo de texto.

    Cada reserva ocupa una línea. Los campos se separan con '|'.
    Si la lista está vacía, crea el archivo vacío de todas formas.

    Parámetros:
        lista_reservas (list[dict]): Lista de reservas a guardar.
        archivo (str): Ruta del archivo destino.

    Retorna:
        int: Cantidad de reservas guardadas.
    """
    contador = 0
    with open(archivo, "w", encoding="utf-8") as f:
        for reserva in lista_reservas:
            linea = SEPARADOR.join([
                str(reserva.get("id_reserva", "")),
                str(reserva.get("id_cliente", "")),
                str(reserva.get("nombre_cliente", "")),
                str(reserva.get("email_cliente", "")),
                str(reserva.get("nombre_servicio", "")),
                str(reserva.get("precio", "0.0")),
                str(reserva.get("fecha", "")),
            ])
            f.write(linea + "\n")
            contador += 1
    return contador


# ──────────────────────────────────────────────
# CARGAR
# ──────────────────────────────────────────────

def cargar_reservas(archivo="reservas.txt"):
    """
    Lee el archivo de texto y reconstruye la lista de reservas.

    Si el archivo no existe, retorna una lista vacía sin lanzar error.
    Las líneas en blanco se ignoran automáticamente.

    Parámetros:
        archivo (str): Ruta del archivo a leer.

    Retorna:
        list[dict]: Lista de reservas como diccionarios.
    """
    if not os.path.exists(archivo):
        return []

    reservas = []
    with open(archivo, "r", encoding="utf-8") as f:
        for linea in f:
            linea = linea.strip()
            if not linea:
                continue  # saltar líneas vacías

            partes = linea.split(SEPARADOR)

            # Si la línea no tiene todos los campos esperados, se ignora
            if len(partes) < len(CAMPOS):
                continue

            reserva = {
                "id_reserva":      partes[0],
                "id_cliente":      partes[1],
                "nombre_cliente":  partes[2],
                "email_cliente":   partes[3],
                "nombre_servicio": partes[4],
                "precio":          float(partes[5]),
                "fecha":           partes[6],
            }
            reservas.append(reserva)

    return reservas


# ──────────────────────────────────────────────
# ELIMINAR
# ──────────────────────────────────────────────

def eliminar_archivo(archivo):
    """
    Elimina el archivo indicado si existe.

    Parámetros:
        archivo (str): Ruta del archivo a eliminar.

    Retorna:
        bool: True si se eliminó correctamente, False si no existía.
    """
    if os.path.exists(archivo):
        os.remove(archivo)
        return True
    return False