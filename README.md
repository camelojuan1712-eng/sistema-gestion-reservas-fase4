
# Sistema de Gestión de Clientes, Servicios y Reservas

**🏢 Empresa:** Software FJ  
**📚 Curso:** Programación (213023) – UNAD  
**📝 Fase 4 – Componente Práctico Simulado**  
**📅 Fecha de entrega:** 12 de mayo de 2026

---

## 👥 Integrantes del equipo

| Nombre | Rol | GitHub |
|:---|:---|:---|
| Juan David | Líder de desarrollo, arquitectura del sistema | https://github.com/camelojuan1712-eng |
| Paula | Servicios especializados, logging | https://github.com/Pau-lalala |
| Itan Bautista | Pruebas unitarias, reportes, persistencia | https://github.com/bautisyoser21-cell |
| Cristhian Jair Cano Villate | Menú interactivo, utilidades (código integrado por el equipo)

> ⚠️ **Nota:** De los 5 integrantes originales del grupo, cuatro participaron activamente. Cristhian no pudo usar Git directamente por dificultades técnicas, pero envió su código al equipo, que fue integrado al repositorio. El quinto integrante nunca estableció comunicación.

---

## 📋 Descripción del proyecto

Sistema integral orientado a objetos para gestionar clientes, servicios y reservas de la empresa **Software FJ**. No utiliza bases de datos: toda la información se maneja en memoria mediante objetos y listas.

### 🛠️ Servicios disponibles

- 🏢 **Reserva de salas** (reuniones, conferencias, capacitación)
- 💻 **Alquiler de equipos** (portátiles, proyectores, etc.)
- 🧠 **Asesorías especializadas** (tecnología, derecho, contabilidad)

### ✅ Características técnicas

- 🧬 Clases abstractas, herencia y polimorfismo
- 🔐 Encapsulación con validaciones estrictas
- 📦 Métodos sobrecargados (cálculo de costos con/sin impuestos y descuentos)
- ❗ Excepciones personalizadas (`ErrorValidacion`, `ServicioNoDisponible`, `ReservaInvalida`)
- 🛡️ Manejo avanzado: `try/except/else/finally`, encadenamiento (`raise ... from e`)
- 📝 Registro de todos los eventos y errores en `logs/eventos.log`
- 🧪 Simulación de 10 operaciones (válidas e inválidas) sin detener el sistema
- 🧾 Pruebas unitarias, reportes y persistencia simple en archivos

---

## 📁 Estructura del proyecto
SistemaGestion/
├── main.py
├── entidades.py
├── servicios_especializados.py
├── excepciones.py
├── logger_config.py
├── simulador.py
├── menu_interactivo.py
├── utilidades.py
├── pruebas_unitarias.py
├── reportes.py
├── persistencia.py
├── logs/
│ └── eventos.log
└── README.md

---

## 🚀 Cómo ejecutar

1. Clonar el repositorio:
   ```bash
   git clone https://github.com/camelojuan1712-eng/sistema-gestion-reservas-fase4
   cd sistema-gestion-reservas-fase4
2. Ejecutar el programa principal:
   python main.py
4. Para usar el menú interactivo:
   python menu_interactivo.py
   
---

🧪 Simulaciones
El sistema ejecuta 10 operaciones automáticas que incluyen:

✅ Clientes válidos e inválidos (email, teléfono)

✅ Servicios correctos y con errores (precio negativo)

✅ Reservas exitosas y fallidas (servicio no disponible, horas inválidas)

✅ Cancelación de reservas

✅ Cálculo de costos con impuestos y descuentos

🛡️ El programa nunca se detiene ante errores. Todos los incidentes quedan registrados en logs/eventos.log.

🔀 Flujo de trabajo en Git
Ramas por integrante:

🌿 feature/cliente-reserva (Juan David)

🌿 feature/servicios-logging (Paula)

🌿 feature/itan-pruebas-reportes (Itan Bautista)

🔄 Pull Requests hacia main con revisión mutua.

📌 Commits frecuentes con mensajes descriptivos.

🌐 Repositorio público para trazabilidad con la tutora.

📄 Documento PDF final
Incluye portada, introducción, enlace al repositorio, conclusiones y referencias en formato APA.
