# ===========================================================================
#  ARCHIVO: simulador.py
#  PROPÓSITO: Ejecutar 10 simulaciones que prueban el sistema.
#
#  La rúbrica exige al menos 10 operaciones completas, incluyendo casos
#  válidos e inválidos, demostrando que el sistema nunca se cae.
#
#  Cada simulación está envuelta en un bloque try/except para que un error
#  en una prueba no detenga la ejecución de las demás.
# ===========================================================================

import logging
from logger_config import obtener_logger

# Importamos todas las clases necesarias
from entidades import Cliente, Reserva
from servicios_especializados import (
    ServicioSala,
    AlquilerEquipo,
    AsesoriaEspecializada,
)
from excepciones import ErrorValidacion, ServicioNoDisponible, ReservaInvalida


def ejecutar_simulaciones():
    """
    Ejecuta una serie de 10 pruebas controladas y registra todo en el log.
    """
    logger = obtener_logger()
    logger.info("=" * 60)
    logger.info("INICIANDO LAS 10 SIMULACIONES DE PRUEBA")
    logger.info("=" * 60)

    # -----------------------------------------------------------------------
    #  SIMULACIÓN 1: Crear un cliente válido (debe funcionar)
    # -----------------------------------------------------------------------
    print("\n[Simulación 1] Creando cliente válido...")
    try:
        cliente1 = Cliente(101, "Carlos Mendoza", "carlos@email.com", "3105551234")
        print(f"   Cliente creado: {cliente1}")
        logger.info(f"Simulación 1 (OK): Cliente creado - {cliente1}")
    except Exception as e:
        print(f"   Error inesperado: {e}")
        logger.error(f"Simulación 1 (FALLO): {e}")

    # -----------------------------------------------------------------------
    #  SIMULACIÓN 2: Cliente con email inválido (DEBE FALLAR)
    # -----------------------------------------------------------------------
    print("\n[Simulación 2] Creando cliente con email inválido...")
    try:
        cliente_malo = Cliente(102, "Ana López", "correo_sin_arroba", "3205556789")
        logger.warning("Simulación 2: Se creó cliente con email inválido (no debería).")
    except ErrorValidacion as e:
        print(f"   Excepción capturada correctamente: {e}")
        logger.info(f"Simulación 2 (FALLÓ COMO SE ESPERABA): {e}")

    # -----------------------------------------------------------------------
    #  SIMULACIÓN 3: Cliente con teléfono inválido (DEBE FALLAR)
    # -----------------------------------------------------------------------
    print("\n[Simulación 3] Creando cliente con teléfono inválido...")
    try:
        cliente_malo2 = Cliente(103, "Pedro Ruiz", "pedro@mail.com", "abc123")
    except ErrorValidacion as e:
        print(f"   Excepción capturada: {e}")
        logger.info(f"Simulación 3 (FALLÓ OK): {e}")

    # -----------------------------------------------------------------------
    #  SIMULACIÓN 4: Crear varios servicios válidos
    # -----------------------------------------------------------------------
    print("\n[Simulación 4] Creando servicios válidos...")
    try:
        sala = ServicioSala("Sala de Juntas Premium", 75000, "reuniones")
        laptop = AlquilerEquipo("Laptop Dell XPS", 40000, "portátil")
        asesoria = AsesoriaEspecializada(
            "Asesoría en IA", 120000, "tecnología", horas_minimas=3
        )
        print(f"   Sala: {sala.describir()}")
        print(f"   Equipo: {laptop.describir()}")
        print(f"   Asesoría: {asesoria.describir()}")
        logger.info("Simulación 4 (OK): Servicios creados correctamente.")
    except Exception as e:
        print(f"   Error: {e}")
        logger.error(f"Simulación 4 (FALLO): {e}")

    # -----------------------------------------------------------------------
    #  SIMULACIÓN 5: Servicio con precio negativo (DEBE FALLAR)
    # -----------------------------------------------------------------------
    print("\n[Simulación 5] Creando servicio con precio negativo...")
    try:
        sala_mala = ServicioSala("Sala Fantasma", -5000, "reuniones")
    except ErrorValidacion as e:
        print(f"   Excepción capturada: {e}")
        logger.info(f"Simulación 5 (FALLÓ OK): {e}")

    # -----------------------------------------------------------------------
    #  SIMULACIÓN 6: Reserva válida y confirmación
    # -----------------------------------------------------------------------
    print("\n[Simulación 6] Creando reserva válida para la sala...")
    try:
        sala = ServicioSala("Sala de Juntas Premium", 75000, "reuniones")
        reserva1 = Reserva(cliente1, sala, 4)  # 4 horas
        costo = reserva1.confirmar(aplicar_iva=True)
        print(f"   Reserva confirmada. Total: ${costo:,.2f}")
        logger.info(f"Simulación 6 (OK): Reserva confirmada - Total ${costo:,.2f}")
    except Exception as e:
        print(f"   Error: {e}")
        logger.error(f"Simulación 6 (FALLO): {e}")

    # -----------------------------------------------------------------------
    #  SIMULACIÓN 7: Reservar el mismo servicio otra vez (DEBE FALLAR)
    # -----------------------------------------------------------------------
    print("\n[Simulación 7] Intentando reservar la misma sala (ya ocupada)...")
    try:
        cliente2 = Cliente(104, "Luisa Fernanda", "luisa@mail.com", "3112223344")
        sala2 = ServicioSala("Sala de Juntas Premium", 75000, "reuniones")
        reserva2 = Reserva(cliente2, sala2, 2)
        reserva2.confirmar()  # Esta debería funcionar
        # Intentar otra reserva sobre la misma sala para forzar error
        cliente3 = Cliente(105, "Otra Persona", "otra@mail.com", "3001112233")
        reserva3 = Reserva(cliente3, sala2, 1)
        reserva3.confirmar()
    except ServicioNoDisponible as e:
        print(f"   Excepción capturada: {e}")
        logger.info(f"Simulación 7 (FALLÓ OK): {e}")
    except Exception as e:
        print(f"   Error: {e}")
        logger.error(f"Simulación 7 (ERROR): {e}")

    # -----------------------------------------------------------------------
    #  SIMULACIÓN 8: Cancelar la reserva anterior
    # -----------------------------------------------------------------------
    print("\n[Simulación 8] Cancelando la reserva de la sala...")
    try:
        reserva1.cancelar()
        print(f"   Reserva cancelada. Estado: {reserva1.get_estado()}")
        logger.info("Simulación 8 (OK): Reserva cancelada exitosamente.")
    except Exception as e:
        print(f"   Error: {e}")
        logger.error(f"Simulación 8 (FALLO): {e}")

    # -----------------------------------------------------------------------
    #  SIMULACIÓN 9: Reserva de equipo con descuento (sobrecarga simulada)
    # -----------------------------------------------------------------------
    print("\n[Simulación 9] Reservando equipo portátil con descuento del 10%...")
    try:
        laptop = AlquilerEquipo("Laptop Dell XPS", 40000, "portátil")
        cliente5 = Cliente(107, "Ana Equipos", "ana@mail.com", "3115556666")
        reserva5 = Reserva(cliente5, laptop, 5)
        costo_est = laptop.calcular_costo_con_impuestos(5, impuesto=0.0, descuento=0.10)
        print(f"   Costo estimado (sin confirmar): ${costo_est:,.2f}")
        reserva5.confirmar(aplicar_iva=False)
        print(f"   Reserva confirmada. Total: ${reserva5.get_costo_total():,.2f}")
        logger.info("Simulación 9 (OK): Reserva de equipo confirmada con descuento.")
    except Exception as e:
        print(f"   Error: {e}")
        logger.error(f"Simulación 9 (FALLO): {e}")

    # -----------------------------------------------------------------------
    #  SIMULACIÓN 10: Asesoría con mínimo de horas (pide 1, cobra 3)
    # -----------------------------------------------------------------------
    print("\n[Simulación 10] Asesoría: solicitando 1 hora (mínimo 3)...")
    try:
        cliente3 = Cliente(105, "María Gómez", "maria@mail.com", "3001112233")
        reserva4 = Reserva(cliente3, asesoria, 1)
        reserva4.confirmar(aplicar_iva=True)
        print(f"   Asesoría confirmada. Costo (mínimo 3h): ${reserva4.get_costo_total():,.2f}")
        logger.info("Simulación 10 (OK): Asesoría confirmada con mínimo de horas.")
    except Exception as e:
        print(f"   Error: {e}")
        logger.error(f"Simulación 10 (FALLO): {e}")

    # -----------------------------------------------------------------------
    #  FIN DE LAS SIMULACIONES
    # -----------------------------------------------------------------------
    print("\n" + "=" * 60)
    print("  LAS 10 SIMULACIONES HAN FINALIZADO.")
    print("  Revisa el archivo 'logs/eventos.log'.")
    print("=" * 60)
    logger.info("=" * 60)
    logger.info("SIMULACIONES COMPLETADAS (10 ejecutadas).")
    logger.info("=" * 60)


# ===========================================================================
#  BLOQUE DE PRUEBA DIRECTA
# ===========================================================================
if __name__ == "__main__":
    from logger_config import configurar_logger
    configurar_logger()
    ejecutar_simulaciones()