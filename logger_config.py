# ===========================================================================
# ARCHIVO: logger_config.py
# PROPÓSITO:
# Configurar el sistema de logs para guardar eventos y errores.
#
# Se crea la carpeta "logs" y el archivo "eventos.log".
# ===========================================================================

import logging
import os


def configurar_logger():
    # Crear carpeta logs si no existe
    if not os.path.exists("logs"):
        os.makedirs("logs")

    # Configuración del log
    logging.basicConfig(
        filename="logs/eventos.log",
        level=logging.DEBUG,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

    return logging.getLogger()


def obtener_logger():
    return logging.getLogger()