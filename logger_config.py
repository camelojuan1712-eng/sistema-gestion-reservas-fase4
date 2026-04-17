# -*- coding: utf-8 -*-
"""Configuración de logging."""
import logging

def configurar_logger():
    logging.basicConfig(
        filename='logs/eventos.log',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
