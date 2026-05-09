# ===========================================================================
#  ARCHIVO: entidades.py
#  PROPÓSITO: Contener las clases principales del modelo de negocio:
#             Cliente, Servicio (abstracta) y Reserva.
#
#  Este archivo es el corazón del sistema. Aquí aplico todos los conceptos
#  de Programación Orientada a Objetos que pide la rúbrica:
#    - Encapsulación (atributos privados en Cliente).
#    - Abstracción (clase Servicio con métodos abstractos).
#    - Herencia (las clases de servicios heredarán de Servicio).
#    - Polimorfismo (cada servicio implementa calcular_costo a su manera).
#    - Manejo de excepciones (try/except/else/finally en Reserva.confirmar).
# ===========================================================================

# ---------------------------------------------------------------------------
#  IMPORTACIONES NECESARIAS
# ---------------------------------------------------------------------------
import re                       # Para validar el formato del email con expresiones regulares
import logging                  # Para registrar eventos en el archivo de log
from abc import ABC, abstractmethod   # Para crear clases abstractas
from excepciones import ErrorValidacion, ServicioNoDisponible, ReservaInvalida


# ===========================================================================
#  CLASE CLIENTE
# ===========================================================================
#  Representa a una persona que usará los servicios de Software FJ.
#  Uso encapsulación estricta: los atributos son privados (doble guion bajo)
#  y solo se accede a ellos mediante getters y setters públicos.
#  Los setters incluyen validaciones para garantizar que los datos sean correctos.
# ===========================================================================

class Cliente:
    def __init__(self, id_cliente: int, nombre: str, email: str, telefono: str):
        """
        Constructor de Cliente.
        Recibe los datos básicos y los asigna a través de los setters,
        que ya incluyen las validaciones. Si algún dato es inválido,
        se lanzará ErrorValidacion y el objeto no se creará.
        """
        # Atributos privados (encapsulación)
        self.__id = id_cliente          # Identificador único del cliente
        self.__nombre = nombre          # Nombre completo
        self.__email = None             # Se asignará con el setter
        self.__telefono = None          # Se asignará con el setter

        # Llamo a los setters para validar desde el inicio
        self.set_email(email)
        self.set_telefono(telefono)

        # Registro en el log que el cliente se creó correctamente
        logging.info(f"Cliente creado correctamente: ID {id_cliente} - {nombre}")

    # -----------------------------------------------------------------------
    #  GETTERS: Métodos para leer los atributos privados desde fuera
    # -----------------------------------------------------------------------
    def get_id(self) -> int:
        """Retorna el ID del cliente."""
        return self.__id

    def get_nombre(self) -> str:
        """Retorna el nombre completo del cliente."""
        return self.__nombre

    def get_email(self) -> str:
        """Retorna el email del cliente."""
        return self.__email

    def get_telefono(self) -> str:
        """Retorna el teléfono del cliente."""
        return self.__telefono

    # -----------------------------------------------------------------------
    #  SETTERS: Métodos para modificar atributos CON VALIDACIÓN
    # -----------------------------------------------------------------------
    def set_email(self, email: str):
        """
        Valida que el email tenga un formato básico: texto@texto.texto
        Si no es válido, lanza ErrorValidacion. Si es válido, lo asigna.
        """
        # Expresión regular simple pero efectiva:
        # [^@]+  → uno o más caracteres que no sean @
        # @      → una arroba obligatoria
        # [^@]+  → uno o más caracteres que no sean @
        # \.     → un punto literal (escapado)
        # [^@]+  → uno o más caracteres que no sean @
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            # Levanto la excepción personalizada con un mensaje claro
            raise ErrorValidacion(f"❌ El email '{email}' no tiene un formato válido.")
        self.__email = email

    def set_telefono(self, telefono: str):
        """
        Valida que el teléfono contenga SOLO NÚMEROS y al menos 7 dígitos.
        Si no cumple, lanza ErrorValidacion.
        """
        telefono_str = str(telefono)
        # isdigit() verifica que todos los caracteres sean dígitos (0-9)
        if not telefono_str.isdigit() or len(telefono_str) < 7:
            raise ErrorValidacion(
                f"❌ El teléfono '{telefono}' debe contener solo números y al menos 7 dígitos."
            )
        self.__telefono = telefono_str

    # -----------------------------------------------------------------------
    #  Método especial __str__: representación legible del objeto
    # -----------------------------------------------------------------------
    def __str__(self) -> str:
        """Retorna una cadena con los datos del cliente para imprimirlos fácilmente."""
        return f"Cliente {self.__id}: {self.__nombre} | {self.__email} | Tel: {self.__telefono}"


# ===========================================================================
#  CLASE ABSTRACTA SERVICIO
# ===========================================================================
#  Esta clase NO se puede instanciar directamente. Sirve como "contrato"
#  para todas las clases hijas (ServicioSala, AlquilerEquipo, etc.).
#  Obliga a que todas las hijas implementen los métodos abstractos:
#    - calcular_costo(horas)
#    - describir()
#  También provee atributos y métodos comunes a todos los servicios.
# ===========================================================================

class Servicio(ABC):
    def __init__(self, nombre: str, precio_base: float):
        """
        Constructor de Servicio.
        Valida que el precio_base sea positivo. Si no, lanza ErrorValidacion.
        Inicializa los atributos protegidos (prefijo _) que heredarán las hijas.
        """

        # Validación: ningún servicio puede costar 0 o negativo
        if precio_base <= 0:
            raise ErrorValidacion(f"❌ El precio base '{precio_base}' debe ser un valor positivo.")

        self._nombre = nombre
        self._precio_base = precio_base
        self._disponible = True

        # 🔴 CAMBIO IMPORTANTE:
        # No usar describir() aquí porque las clases hijas aún no están listas
        logging.info(f"Servicio creado: {nombre} - Precio base: ${precio_base:.2f}")

    # -----------------------------------------------------------------------
    #  MÉTODOS ABSTRACTOS (deben ser implementados por las hijas)
    # -----------------------------------------------------------------------
    @abstractmethod
    def calcular_costo(self, horas: int) -> float:
        if horas <= 0:
            raise ErrorValidacion(
                f"❌ La cantidad de horas '{horas}' no es válida. Debe ser un número positivo."
            )

    @abstractmethod
    def describir(self) -> str:
        pass

    # -----------------------------------------------------------------------
    #  MÉTODOS CONCRETOS (ya implementados, las hijas los heredan)
    # -----------------------------------------------------------------------
    def esta_disponible(self) -> bool:
        return self._disponible

    def set_disponible(self, estado: bool):
        self._disponible = estado

    def get_nombre(self) -> str:
        return self._nombre

    def get_precio_base(self) -> float:
        return self._precio_base

    # -----------------------------------------------------------------------
    #  SOBRECARGA SIMULADA
    # -----------------------------------------------------------------------
    def calcular_costo_con_impuestos(
        self, horas: int, impuesto: float = 0.0, descuento: float = 0.0
    ) -> float:

        if not (0.0 <= impuesto <= 1.0):
            raise ErrorValidacion("❌ Impuesto inválido.")

        if not (0.0 <= descuento <= 1.0):
            raise ErrorValidacion("❌ Descuento inválido.")

        try:
            costo_base = self.calcular_costo(horas)
        except ErrorValidacion as e:
            raise ErrorValidacion(f"Error en cálculo: {e}") from e

        subtotal = costo_base * (1 + impuesto)
        total = subtotal * (1 - descuento)

        return round(total, 2)

    def __str__(self) -> str:
        estado = "Disponible" if self._disponible else "No disponible"
        return f"{self._nombre} | ${self._precio_base:,.0f}/hora | {estado}"


# ===========================================================================
#  CLASE RESERVA
# ===========================================================================
#  Modela la acción de que un Cliente reserve un Servicio por ciertas horas.
#  Maneja el ciclo de vida de la reserva: pendiente → confirmada / cancelada.
#  Contiene el manejo robusto de excepciones que exige la rúbrica:
#    - try/except/else/finally
#    - excepciones personalizadas
#    - encadenamiento
#    - logging de errores
# ===========================================================================

class Reserva:
    # Constantes de clase para los estados (buenas prácticas)
    ESTADO_PENDIENTE = "pendiente"
    ESTADO_CONFIRMADA = "confirmada"
    ESTADO_CANCELADA = "cancelada"

    def __init__(self, cliente: Cliente, servicio: Servicio, duracion_horas: int):
        """
        Constructor de Reserva.
        Asigna cliente, servicio y duración, validando que duración > 0.
        Estado inicial: PENDIENTE.
        Costo total: 0.0 hasta que se confirme.
        """
        # Validación de duración (no puede ser negativa ni cero)
        if duracion_horas <= 0:
            raise ErrorValidacion(
                f"❌ La duración de la reserva ({duracion_horas}) debe ser un número positivo."
            )

        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion_horas
        self.estado = self.ESTADO_PENDIENTE
        self.costo_total = 0.0

        logging.info(
            f"Reserva creada (pendiente): Cliente {cliente.get_id()} - "
            f"Servicio '{servicio.get_nombre()}' - {duracion_horas} horas."
        )

    # -----------------------------------------------------------------------
    #  MÉTODO CONFIRMAR (contiene el manejo avanzado de excepciones)
    # -----------------------------------------------------------------------
    def confirmar(self, aplicar_iva: bool = True) -> float:
        """
        Confirma la reserva si el servicio está disponible.
        Calcula el costo total, cambia el estado a CONFIRMADA
        y marca el servicio como NO disponible.

        Retorna el costo total calculado.
        """
        try:
            # 1. Verificar que la reserva esté pendiente
            if self.estado != self.ESTADO_PENDIENTE:
                raise ReservaInvalida(
                    f"No se puede confirmar una reserva en estado '{self.estado}'."
                )

            # 2. Verificar disponibilidad del servicio
            if not self.servicio.esta_disponible():
                raise ServicioNoDisponible(
                    f"El servicio '{self.servicio.get_nombre()}' no está disponible."
                )

            # 3. Calcular costo usando el método con sobrecarga simulada
            #    Si aplicar_iva es True, pasamos 19% de impuesto.
            impuesto = 0.19 if aplicar_iva else 0.0
            self.costo_total = self.servicio.calcular_costo_con_impuestos(
                self.duracion, impuesto=impuesto
            )

            # 4. Actualizar estados
            self.estado = self.ESTADO_CONFIRMADA
            self.servicio.set_disponible(False)   # El servicio ya está ocupado

            # 5. Registrar éxito en el log
            logging.info(
                f"✅ Reserva CONFIRMADA: Cliente {self.cliente.get_id()} - "
                f"Servicio '{self.servicio.get_nombre()}' - "
                f"{self.duracion} horas - Total: ${self.costo_total:,.2f}"
            )

        except ServicioNoDisponible as e:
            # Error específico: servicio ocupado. Se registra y se relanza.
            logging.error(f"❌ Fallo al confirmar (servicio no disponible): {e}")
            raise

        except ReservaInvalida as e:
            # Error de lógica: la reserva ya fue confirmada o cancelada antes.
            logging.error(f"❌ Fallo al confirmar (estado inválido): {e}")
            raise

        except ErrorValidacion as e:
            # Error en el cálculo (ej. horas inválidas). Se encadena.
            logging.error(f"❌ Error de cálculo al confirmar: {e}")
            raise ErrorValidacion(
                f"No se pudo confirmar la reserva por error en cálculo: {e}"
            ) from e

        except Exception as e:
            # Cualquier otro error inesperado (ej. división por cero).
            # Lo convertimos en ReservaInvalida para mantener consistencia.
            logging.critical(f"❌ Error inesperado al confirmar: {e}", exc_info=True)
            raise ReservaInvalida(f"Error interno al procesar la reserva: {e}") from e

        else:
            # Este bloque SOLO se ejecuta si el try terminó sin excepciones.
            # Es el lugar ideal para poner código que depende del éxito.
            print(f"   [ÉXITO] Reserva confirmada. Costo total: ${self.costo_total:,.2f}")
            logging.info("   El bloque else se ejecutó: confirmación sin errores.")

        finally:
            # Este bloque se ejecuta SIEMPRE, haya error o no.
            # Útil para liberar recursos o dejar constancia de que se intentó.
            logging.debug(
                f"Finalizó el intento de confirmación para reserva de {self.cliente.get_nombre()}"
            )

        return self.costo_total

    # -----------------------------------------------------------------------
    #  MÉTODO CANCELAR
    # -----------------------------------------------------------------------
    def cancelar(self) -> None:
        """
        Cancela la reserva, liberando el servicio para otros clientes.
        """
        try:
            # Solo se puede cancelar si está pendiente o confirmada
            if self.estado not in (self.ESTADO_PENDIENTE, self.ESTADO_CONFIRMADA):
                raise ReservaInvalida(
                    f"No se puede cancelar una reserva en estado '{self.estado}'."
                )

            estado_anterior = self.estado
            self.estado = self.ESTADO_CANCELADA
            self.servicio.set_disponible(True)  # Liberar el servicio

            logging.info(
                f"❌ Reserva CANCELADA: Cliente {self.cliente.get_id()} - "
                f"Servicio '{self.servicio.get_nombre()}' (estado anterior: {estado_anterior})."
            )

        except ReservaInvalida as e:
            logging.error(f"Error al cancelar: {e}")
            raise
        except Exception as e:
            logging.critical(f"Error inesperado al cancelar: {e}", exc_info=True)
            raise
        else:
            print(f"   [OK] Reserva cancelada exitosamente.")
        finally:
            logging.debug("Finalizó el intento de cancelación.")

    # -----------------------------------------------------------------------
    #  MÉTODO PROCESAR (opcional, demuestra polimorfismo con confirmar)
    # -----------------------------------------------------------------------
    def procesar(self) -> float:
        """Procesa la reserva (la confirma con IVA por defecto)."""
        return self.confirmar(aplicar_iva=True)

    # -----------------------------------------------------------------------
    #  GETTERS
    # -----------------------------------------------------------------------
    def get_estado(self) -> str:
        return self.estado

    def get_costo_total(self) -> float:
        return self.costo_total

    # -----------------------------------------------------------------------
    #  REPRESENTACIÓN EN STRING
    # -----------------------------------------------------------------------
    def __str__(self) -> str:
        return (
            f"Reserva [{self.estado.upper()}] | "
            f"Cliente: {self.cliente.get_nombre()} | "
            f"Servicio: {self.servicio.get_nombre()} | "
            f"Duración: {self.duracion} h | "
            f"Costo: ${self.costo_total:,.2f}"
        )