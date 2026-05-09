# ============================================================================
#  ARCHIVO: excepciones.py
#  PROPÓSITO: Definir excepciones personalizadas para el sistema.
#
#  ¿Por qué crear excepciones propias en lugar de usar las genéricas?
#  - Porque la rúbrica exige "excepciones personalizadas".
#  - Porque nos permiten identificar exactamente qué tipo de error ocurrió
#    y dar mensajes más claros al usuario o al programador.
#  - Porque podemos atraparlas selectivamente con "except ErrorValidacion"
#    y dejar que otros errores se manejen de forma diferente.
#
#  Las tres excepciones que defino acá son:
#    1. ErrorValidacion     → cuando los datos ingresados no cumplen las reglas.
#    2. ServicioNoDisponible → cuando se intenta reservar algo ocupado.
#    3. ReservaInvalida     → para errores en la lógica de la reserva.
# ============================================================================

# ---------------------------------------------------------------------------
#  Clase ErrorValidacion
# ---------------------------------------------------------------------------
#  Hereda de Exception, que es la clase base de todos los errores en Python.
#  La palabra "pass" indica que no agrego ningún método adicional;
#  solo quiero tener un tipo de error con este nombre específico.
#  La voy a lanzar (raise) cuando un email no tenga '@', un teléfono tenga
#  letras, un precio sea negativo, etc.
# ---------------------------------------------------------------------------
class ErrorValidacion(Exception):
    """Excepción lanzada cuando un dato de entrada no cumple las reglas de negocio."""
    pass  # No necesito código extra, solo el nombre de la clase


# ---------------------------------------------------------------------------
#  Clase ServicioNoDisponible
# ---------------------------------------------------------------------------
#  Esta excepción se lanza específicamente cuando un cliente intenta reservar
#  un servicio que ya está ocupado o marcado como no disponible.
#  La clase Reserva la usará dentro del método confirmar() para rechazar
#  la operación y notificar al usuario.
# ---------------------------------------------------------------------------
class ServicioNoDisponible(Exception):
    """Excepción lanzada cuando un servicio no está disponible para reserva."""
    pass


# ---------------------------------------------------------------------------
#  Clase ReservaInvalida
# ---------------------------------------------------------------------------
#  Esta excepción cubre casos como: intentar confirmar una reserva que ya fue
#  cancelada, o intentar cancelar una reserva que ya se procesó.
#  Es una forma de proteger la integridad del estado de la reserva.
# ---------------------------------------------------------------------------
class ReservaInvalida(Exception):
    """Excepción lanzada cuando una operación sobre una reserva es inválida."""
    pass