# -*- coding: utf-8 -*-
"""
pruebas_unitarias.py
Módulo de Itan Bautista - Fase 4

Pruebas unitarias con assert para verificar el correcto funcionamiento
de las excepciones personalizadas y los módulos de persistencia y reportes.

Cómo ejecutar:
    python pruebas_unitarias.py

Si todas las pruebas pasan, verás: "✅ Todas las pruebas pasaron correctamente."
Si alguna falla, Python lanzará un AssertionError con el mensaje de la prueba.
"""

import os
import sys

# Asegurar que el directorio padre esté en el path para importar los módulos
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from excepciones import ErrorValidacion, ServicioNoDisponible, ReservaInvalida
from persistencia import guardar_reservas, cargar_reservas, eliminar_archivo
from reportes import generar_reporte, _extraer_monto, _reporte_vacio


# ══════════════════════════════════════════════════════════════
# DATOS DE PRUEBA REUTILIZABLES
# ══════════════════════════════════════════════════════════════

ARCHIVO_PRUEBA = "reservas_test.txt"

RESERVAS_EJEMPLO = [
    {
        "id_reserva":      "R001",
        "id_cliente":      "C001",
        "nombre_cliente":  "Ana Torres",
        "email_cliente":   "ana@example.com",
        "nombre_servicio": "Habitación Doble",
        "precio":          150000.0,
        "fecha":           "2025-05-10",
    },
    {
        "id_reserva":      "R002",
        "id_cliente":      "C002",
        "nombre_cliente":  "Luis Gómez",
        "email_cliente":   "luis@example.com",
        "nombre_servicio": "Habitación Suite",
        "precio":          280000.0,
        "fecha":           "2025-05-11",
    },
]


# ══════════════════════════════════════════════════════════════
# SECCIÓN 1: Pruebas de las Excepciones Personalizadas
# ══════════════════════════════════════════════════════════════

def prueba_excepciones():
    """Verifica que las excepciones personalizadas se puedan lanzar y capturar."""
    print("  → Prueba: Excepciones personalizadas...", end=" ")

    # ErrorValidacion
    try:
        raise ErrorValidacion("Email inválido")
        assert False, "No se lanzó ErrorValidacion"
    except ErrorValidacion as e:
        assert str(e) == "Email inválido", "Mensaje de ErrorValidacion incorrecto"

    # ServicioNoDisponible
    try:
        raise ServicioNoDisponible("El servicio está lleno")
        assert False, "No se lanzó ServicioNoDisponible"
    except ServicioNoDisponible as e:
        assert "lleno" in str(e), "Mensaje de ServicioNoDisponible incorrecto"

    # ReservaInvalida
    try:
        raise ReservaInvalida("Fecha de reserva pasada")
        assert False, "No se lanzó ReservaInvalida"
    except ReservaInvalida as e:
        assert "Fecha" in str(e), "Mensaje de ReservaInvalida incorrecto"

    # Verificar herencia de Exception
    assert issubclass(ErrorValidacion, Exception), \
        "ErrorValidacion debe heredar de Exception"
    assert issubclass(ServicioNoDisponible, Exception), \
        "ServicioNoDisponible debe heredar de Exception"
    assert issubclass(ReservaInvalida, Exception), \
        "ReservaInvalida debe heredar de Exception"

    print("OK ✅")


# ══════════════════════════════════════════════════════════════
# SECCIÓN 2: Pruebas de Persistencia
# ══════════════════════════════════════════════════════════════

def prueba_guardar_reservas():
    """Verifica que guardar_reservas cree el archivo y escriba los datos."""
    print("  → Prueba: guardar_reservas()...", end=" ")

    try:
        cantidad = guardar_reservas(RESERVAS_EJEMPLO, ARCHIVO_PRUEBA)

        assert cantidad == 2, \
            f"Se esperaban 2 reservas guardadas, se guardaron {cantidad}"
        assert os.path.exists(ARCHIVO_PRUEBA), \
            f"El archivo '{ARCHIVO_PRUEBA}' no fue creado"
    finally:
        eliminar_archivo(ARCHIVO_PRUEBA)

    print("OK ✅")


def prueba_cargar_reservas():
    """Verifica que cargar_reservas lea correctamente el archivo guardado."""
    print("  → Prueba: cargar_reservas()...", end=" ")

    # Cada prueba crea sus propios datos (sin depender de otra función)
    guardar_reservas(RESERVAS_EJEMPLO, ARCHIVO_PRUEBA)

    try:
        reservas = cargar_reservas(ARCHIVO_PRUEBA)

        assert isinstance(reservas, list), \
            "cargar_reservas debe retornar una lista"
        assert len(reservas) == 2, \
            f"Se esperaban 2 reservas cargadas, se cargaron {len(reservas)}"

        primera = reservas[0]
        assert primera["id_reserva"] == "R001", \
            "ID de reserva incorrecto"
        assert primera["nombre_cliente"] == "Ana Torres", \
            "Nombre de cliente incorrecto"
        assert primera["precio"] == 150000.0, \
            f"Precio incorrecto: {primera['precio']}"
        assert primera["nombre_servicio"] == "Habitación Doble", \
            "Nombre de servicio incorrecto"

        segunda = reservas[1]
        assert segunda["id_reserva"] == "R002", \
            "ID de segunda reserva incorrecto"
        assert segunda["precio"] == 280000.0, \
            f"Precio de segunda reserva incorrecto: {segunda['precio']}"
    finally:
        eliminar_archivo(ARCHIVO_PRUEBA)

    print("OK ✅")


def prueba_cargar_archivo_inexistente():
    """Verifica que cargar_reservas maneje correctamente un archivo que no existe."""
    print("  → Prueba: cargar_reservas() con archivo inexistente...", end=" ")

    resultado = cargar_reservas("archivo_que_no_existe_9999.txt")

    assert isinstance(resultado, list), \
        "Debe retornar lista aunque el archivo no exista"
    assert len(resultado) == 0, \
        "La lista debe estar vacía si el archivo no existe"

    print("OK ✅")


def prueba_eliminar_archivo():
    """Verifica que eliminar_archivo borre el archivo correctamente."""
    print("  → Prueba: eliminar_archivo()...", end=" ")

    # Crear archivo temporal para eliminar
    with open(ARCHIVO_PRUEBA, "w", encoding="utf-8") as f:
        f.write("temporal\n")

    resultado = eliminar_archivo(ARCHIVO_PRUEBA)
    assert resultado is True, \
        "eliminar_archivo debe retornar True al eliminar"
    assert not os.path.exists(ARCHIVO_PRUEBA), \
        "El archivo debe haberse eliminado"

    # Segunda llamada: el archivo ya no existe
    resultado2 = eliminar_archivo(ARCHIVO_PRUEBA)
    assert resultado2 is False, \
        "eliminar_archivo debe retornar False si el archivo no existe"

    print("OK ✅")


def prueba_persistencia_lista_vacia():
    """Verifica que guardar una lista vacía cree un archivo vacío."""
    print("  → Prueba: guardar lista vacía...", end=" ")

    archivo_vacio = "reservas_vacio_test.txt"

    try:
        cantidad = guardar_reservas([], archivo_vacio)

        assert cantidad == 0, \
            "No se deben contar reservas al guardar lista vacía"
        assert os.path.exists(archivo_vacio), \
            "El archivo debe crearse aunque esté vacío"

        reservas = cargar_reservas(archivo_vacio)
        assert len(reservas) == 0, \
            "La carga de archivo vacío debe retornar lista vacía"
    finally:
        eliminar_archivo(archivo_vacio)

    print("OK ✅")


# ══════════════════════════════════════════════════════════════
# SECCIÓN 3: Pruebas de Reportes
# ══════════════════════════════════════════════════════════════

def prueba_reporte_vacio():
    """Verifica la estructura del reporte vacío."""
    print("  → Prueba: _reporte_vacio()...", end=" ")

    reporte = _reporte_vacio()

    assert isinstance(reporte, dict), \
        "El reporte debe ser un diccionario"
    assert reporte["total_reservas"] == 0, \
        "total_reservas debe iniciar en 0"
    assert reporte["total_ingresos"] == 0.0, \
        "total_ingresos debe iniciar en 0.0"
    assert reporte["total_errores"] == 0, \
        "total_errores debe iniciar en 0"
    assert reporte["total_advertencias"] == 0, \
        "total_advertencias debe iniciar en 0"
    assert reporte["total_lineas"] == 0, \
        "total_lineas debe iniciar en 0"
    assert isinstance(reporte["reservas_detalle"], list), \
        "reservas_detalle debe ser una lista"

    print("OK ✅")


def prueba_extraer_monto():
    """Verifica que _extraer_monto detecte correctamente los montos en líneas de log."""
    print("  → Prueba: _extraer_monto()...", end=" ")

    # Casos que SÍ deben detectar monto
    casos_positivos = [
        ("2025-05-01 10:00:00 - INFO - precio: 50000",   50000.0),
        ("monto: 120000 registrado",                      120000.0),
        ("ingreso: 75000.50 procesado",                   75000.50),
        ("valor: 200000",                                 200000.0),
    ]
    for linea, esperado in casos_positivos:
        resultado = _extraer_monto(linea)
        assert resultado is not None, \
            f"Debería detectar monto en: '{linea}'"
        assert abs(resultado - esperado) < 0.01, \
            f"Monto esperado {esperado}, obtenido {resultado}"

    # Casos que NO deben detectar monto
    casos_negativos = [
        "2025-05-01 - INFO - cliente creado",
        "ERROR - Reserva no encontrada",
        "sin numeros aqui",
    ]
    for linea in casos_negativos:
        resultado = _extraer_monto(linea)
        assert resultado is None, \
            f"No debería detectar monto en: '{linea}'"

    print("OK ✅")


def prueba_reporte_log_inexistente():
    """Verifica que generar_reporte maneje correctamente un log inexistente."""
    print("  → Prueba: generar_reporte() con log inexistente...", end=" ")

    resultado = generar_reporte("log_que_no_existe_9999.log")

    assert isinstance(resultado, dict), \
        "Debe retornar un diccionario"
    assert resultado["total_lineas"] == 0, \
        "Líneas deben ser 0 si no hay log"
    assert resultado["total_reservas"] == 0, \
        "Reservas deben ser 0 si no hay log"

    print("OK ✅")


def prueba_reporte_con_log_simulado():
    """Crea un log de prueba y verifica que el reporte lo analice correctamente."""
    print("  → Prueba: generar_reporte() con log simulado...", end=" ")

    log_prueba = "log_prueba_test.log"
    contenido_log = (
        "2025-05-10 09:00:01,000 - sistema - INFO - Reserva creada para Ana Torres\n"
        "2025-05-10 09:01:00,000 - sistema - INFO - precio: 150000\n"
        "2025-05-10 09:02:00,000 - sistema - INFO - Nueva reserva registrada para Luis\n"
        "2025-05-10 09:03:00,000 - sistema - ERROR - Servicio no disponible\n"
        "2025-05-10 09:04:00,000 - sistema - WARNING - Capacidad casi llena\n"
    )

    with open(log_prueba, "w", encoding="utf-8") as f:
        f.write(contenido_log)

    try:
        resultado = generar_reporte(log_prueba)

        assert resultado["total_lineas"] == 5, \
            f"Esperadas 5 líneas, obtenidas {resultado['total_lineas']}"
        assert resultado["total_errores"] == 1, \
            f"Esperado 1 error, obtenidos {resultado['total_errores']}"
        assert resultado["total_advertencias"] == 1, \
            f"Esperada 1 advertencia, obtenidas {resultado['total_advertencias']}"
        assert resultado["total_reservas"] == 2, \
            f"Esperadas 2 reservas, detectadas {resultado['total_reservas']}"
        assert resultado["total_ingresos"] == 150000.0, \
            f"Ingreso esperado 150000.0, obtenido {resultado['total_ingresos']}"
    finally:
        os.remove(log_prueba)

    print("OK ✅")


# ══════════════════════════════════════════════════════════════
# PUNTO DE ENTRADA - Ejecutar todas las pruebas
# ══════════════════════════════════════════════════════════════

def ejecutar_todas_las_pruebas():
    """Ejecuta todas las pruebas unitarias en orden."""
    print("\n" + "=" * 55)
    print("  PRUEBAS UNITARIAS - Sistema de Reservas Fase 4")
    print("  Módulo: Itan Bautista")
    print("=" * 55)

    print("\n[1] Excepciones personalizadas:")
    prueba_excepciones()

    print("\n[2] Módulo de persistencia:")
    prueba_guardar_reservas()
    prueba_cargar_reservas()
    prueba_cargar_archivo_inexistente()
    prueba_eliminar_archivo()
    prueba_persistencia_lista_vacia()

    print("\n[3] Módulo de reportes:")
    prueba_reporte_vacio()
    prueba_extraer_monto()
    prueba_reporte_log_inexistente()
    prueba_reporte_con_log_simulado()

    print("\n" + "=" * 55)
    print("  ✅ Todas las pruebas pasaron correctamente.")
    print("=" * 55 + "\n")


if __name__ == "__main__":
    ejecutar_todas_las_pruebas()