# ===========================================================================
#  ARCHIVO: main.py
#  PROPÓSITO: Punto de entrada principal del sistema Software FJ.
#
#  Este archivo es el que se ejecuta para iniciar la aplicación.
#  Su función es:
#    1. Configurar el sistema de logging.
#    2. Mostrar un mensaje de bienvenida.
#    3. Ejecutar las 10 simulaciones requeridas por la rúbrica.
#    4. Finalizar correctamente.
#
#  Al ser el punto de entrada, mantiene el código organizado y separado
#  de la lógica de negocio (entidades) y de las pruebas (simulador).
# ===========================================================================

# Importamos la función que configura el logger
from logger_config import configurar_logger

# Importamos la función que ejecuta las 10 simulaciones
from simulador import ejecutar_simulaciones


def main():
    """
    Función principal que orquesta la ejecución del programa.
    """
    # 1. Configurar el logger (crea carpeta logs y archivo eventos.log)
    logger = configurar_logger()

    # 2. Mostrar mensaje de bienvenida en consola
    print("\n" + "=" * 70)
    print("  SISTEMA INTEGRAL DE GESTIÓN DE CLIENTES, SERVICIOS Y RESERVAS")
    print("  Empresa: Software FJ")
    print("  Curso: Programación 213023 - UNAD - Fase 4")
    print("=" * 70)

    # 3. Ejecutar las 10 simulaciones (cada una maneja sus propios errores)
    ejecutar_simulaciones()

    # 4. Mensaje de despedida y registro en log
    print("\nPrograma finalizado. Gracias por usar el sistema.\n")
    logger.info("Aplicación finalizada correctamente.")


# ===========================================================================
#  PUNTO DE ENTRADA
# ===========================================================================
#  Esta condición asegura que main() solo se ejecute si este archivo
#  se corre directamente (python main.py) y no cuando es importado.
if __name__ == "__main__":
    main()