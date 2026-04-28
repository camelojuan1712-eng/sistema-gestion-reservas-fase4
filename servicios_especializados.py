# ===========================================================================
#  ARCHIVO: servicios_especializados.py
#  PROPÓSITO: Definir los diferentes tipos de servicios del sistema.
#
#  Este archivo contiene las clases que heredan de "Servicio"
#  (definida en entidades.py).
#
#  Cada clase implementa:
#   - Su propia forma de calcular el costo
#   - Su propia descripción
# ===========================================================================

# ---------------------------------------------------------------------------
# IMPORTACIONES
# ---------------------------------------------------------------------------
from entidades import Servicio
from excepciones import ErrorValidacion


# ===========================================================================
#  CLASE: ServicioSala
# ===========================================================================
# Representa el servicio de alquiler de salas (reuniones, conferencias, etc.)
# ===========================================================================

class ServicioSala(Servicio):
    def __init__(self, nombre: str, precio_base: float, tipo: str):
        # Primero se inicializa la clase padre
        super().__init__(nombre, precio_base)

        # Luego se agregan atributos propios
        self.tipo = tipo  # Ej: reuniones, conferencias

    def calcular_costo(self, horas: int) -> float:
        # Validación heredada
        super().calcular_costo(horas)

        # Cálculo simple: precio base por horas
        return self._precio_base * horas

    def describir(self) -> str:
        return f"Sala tipo {self.tipo}: {self._nombre}"


# ===========================================================================
#  CLASE: AlquilerEquipo
# ===========================================================================
# Representa el alquiler de equipos tecnológicos
# ===========================================================================

class AlquilerEquipo(Servicio):
    def __init__(self, nombre: str, precio_base: float, tipo_equipo: str):
        super().__init__(nombre, precio_base)

        self.tipo_equipo = tipo_equipo  # Ej: portátil, proyector

    def calcular_costo(self, horas: int) -> float:
        super().calcular_costo(horas)

        # Ejemplo: pequeño recargo del 5%
        costo = self._precio_base * horas
        return costo * 1.05

    def describir(self) -> str:
        return f"Equipo tipo {self.tipo_equipo}: {self._nombre}"


# ===========================================================================
#  CLASE: AsesoriaEspecializada
# ===========================================================================
# Representa asesorías profesionales con mínimo de horas
# ===========================================================================

class AsesoriaEspecializada(Servicio):
    def __init__(self, nombre: str, precio_base: float, area: str, horas_minimas: int = 1):
        super().__init__(nombre, precio_base)

        # Validación del mínimo
        if horas_minimas <= 0:
            raise ErrorValidacion("❌ Las horas mínimas deben ser mayores a 0.")

        self.area = area  # Ej: tecnología, marketing
        self.horas_minimas = horas_minimas

    def calcular_costo(self, horas: int) -> float:
        super().calcular_costo(horas)

        # Si pide menos horas, se cobra el mínimo
        horas_cobradas = max(horas, self.horas_minimas)

        return self._precio_base * horas_cobradas

    def describir(self) -> str:
        return f"Asesoría en {self.area}: {self._nombre} (mínimo {self.horas_minimas}h)"