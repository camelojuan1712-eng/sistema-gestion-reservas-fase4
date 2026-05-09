# =====================================================================
#  ARCHIVO: menu_interactivo.py
#  PROYECTO: Sistema de Gestión de Clientes, Servicios y Reservas
#  EMPRESA FICTICIA: Software FJ
#  CURSO: Programación 213023 - UNAD
#  DESCRIPCIÓN:
#    Este módulo implementa el menú principal de consola que permite
#    al usuario interactuar con el sistema de manera amigable.
#    Desde aquí se pueden registrar clientes, crear servicios,
#    realizar y cancelar reservas, y listar el estado del sistema.
#
#  IMPORTANTE: Este módulo NO usa base de datos. Todo se almacena
#    en listas de objetos en memoria mientras el programa esté activo.
# =====================================================================

# ---------------------  IMPORTACIONES  ------------------------------
# Importamos las clases de entidades base del sistema
from entidades import Cliente, Reserva

# Importamos los tres tipos de servicios especializados
# Cada uno hereda de Servicio (ABC) y tiene su propia lógica de costos
from servicios_especializados import ServicioSala, AlquilerEquipo, AsesoriaEspecializada

# Importamos las excepciones personalizadas del proyecto.
# Esto es POO aplicado a errores: en lugar de lanzar un ValueError genérico,
# lanzamos excepciones propias que describen con precisión qué salió mal.
from excepciones import ErrorValidacion, ServicioNoDisponible, ReservaInvalida

# Importamos la función que nos devuelve el logger configurado.
# Usamos el mismo logger en todo el sistema para que todos los eventos
# queden centralizados en el mismo archivo de log.
from logger_config import obtener_logger

# =====================================================================
#  CONFIGURACIÓN DEL LOGGER PARA ESTE MÓDULO
#  Llamamos a obtener_logger() para que nos devuelva la instancia
#  configurada. Registrará todo en el archivo de log del proyecto.
# =====================================================================
logger = obtener_logger()


# =====================================================================
#  LISTAS GLOBALES DE DATOS EN MEMORIA
#  En un sistema real estos datos estarían en base de datos.
#  Aquí los guardamos en listas de Python mientras el programa corre.
#  Son "globales" en el sentido de que las funciones del menú las
#  comparten; en un proyecto más grande las encapsularíamos en una clase.
# =====================================================================
clientes = []    # Lista que almacenará objetos de tipo Cliente
servicios = []   # Lista que almacenará objetos de tipo Servicio (y subclases)
reservas = []    # Lista que almacenará objetos de tipo Reserva


# =====================================================================
#  FUNCIÓN AUXILIAR: pedir_texto
#  Le pedimos al usuario que ingrese un texto y validamos que no esté
#  vacío. Si el usuario no escribe nada, le avisamos y le pedimos de
#  nuevo. Usamos un bucle while True para repetir hasta que sea válido.
# =====================================================================
def pedir_texto(mensaje, campo="campo"):
    """
    Solicita al usuario un texto no vacío con un mensaje personalizado.

    Args:
        mensaje (str): Texto que se muestra al usuario antes del input.
        campo (str): Nombre del campo, usado en el mensaje de error.

    Returns:
        str: El texto ingresado por el usuario (sin espacios al inicio/fin).
    """
    while True:
        try:
            # Leemos la entrada del usuario y quitamos espacios en blanco
            valor = input(mensaje).strip()

            # Validamos que no esté vacío
            if not valor:
                # Si está vacío, lanzamos nuestra excepción personalizada.
                # Usamos ErrorValidacion porque es un dato inválido del usuario.
                raise ErrorValidacion(f"El {campo} no puede estar vacío.")

            # Si llegamos aquí es porque el dato es válido → retornamos
            return valor

        except ErrorValidacion as e:
            # Capturamos nuestra propia excepción y mostramos mensaje amigable
            print(f"  [!] Error de validación: {e}")
            logger.warning(f"Dato vacío ingresado en campo '{campo}'.")
            # El bucle continúa → le pedimos de nuevo al usuario


# =====================================================================
#  FUNCIÓN AUXILIAR: pedir_entero
#  Solicita al usuario un número entero dentro de un rango opcional.
#  Repite hasta que el usuario ingrese algo válido.
# =====================================================================
def pedir_entero(mensaje, minimo=None, maximo=None):
    """
    Solicita al usuario un número entero, con validación de rango opcional.

    Args:
        mensaje (str): Texto que se muestra al usuario.
        minimo (int, optional): Valor mínimo permitido.
        maximo (int, optional): Valor máximo permitido.

    Returns:
        int: El número entero ingresado y validado.
    """
    while True:
        try:
            # Intentamos convertir la entrada a entero.
            # Si el usuario escribe "abc", int() lanzará ValueError.
            texto = input(mensaje).strip()
            numero = int(texto)

            # Validamos el rango si se especificó
            if minimo is not None and numero < minimo:
                raise ErrorValidacion(
                    f"El valor debe ser mayor o igual a {minimo}."
                )
            if maximo is not None and numero > maximo:
                raise ErrorValidacion(
                    f"El valor debe ser menor o igual a {maximo}."
                )

            # Todo bien → retornamos el número
            return numero

        except ValueError:
            # ValueError ocurre cuando int() no puede convertir el texto.
            # Lo transformamos en un mensaje amigable.
            print("  [!] Por favor ingrese un número entero válido.")
            logger.warning(f"Entrada no numérica recibida: '{texto}'")

        except ErrorValidacion as e:
            print(f"  [!] Error de validación: {e}")
            logger.warning(f"Entero fuera de rango: {e}")


# =====================================================================
#  FUNCIÓN AUXILIAR: pedir_flotante
#  Similar a pedir_entero pero para números decimales (float).
#  Útil para capturar precios.
# =====================================================================
def pedir_flotante(mensaje, minimo=0.0):
    """
    Solicita al usuario un número decimal (float) positivo.

    Args:
        mensaje (str): Texto que se muestra al usuario.
        minimo (float): Valor mínimo permitido (por defecto 0.0).

    Returns:
        float: El número decimal ingresado y validado.
    """
    while True:
        try:
            texto = input(mensaje).strip()
            numero = float(texto)

            if numero < minimo:
                raise ErrorValidacion(
                    f"El valor debe ser mayor o igual a {minimo}."
                )

            return numero

        except ValueError:
            print("  [!] Por favor ingrese un número decimal válido (ej: 50000.0).")
            logger.warning(f"Entrada no numérica flotante: '{texto}'")

        except ErrorValidacion as e:
            print(f"  [!] Error de validación: {e}")
            logger.warning(f"Flotante fuera de rango: {e}")


# =====================================================================
#  OPCIÓN 1: REGISTRAR UN CLIENTE
#  Esta función guía al usuario para crear un objeto Cliente.
#  La clase Cliente (en entidades.py) ya tiene validaciones internas
#  para el email y el teléfono, así que pueden lanzar ErrorValidacion.
#  Usamos un bucle que repite SOLO el dato inválido, no todo el formulario.
# =====================================================================
def registrar_cliente():
    """
    Solicita los datos de un nuevo cliente y lo agrega a la lista global.
    Maneja ErrorValidacion para cada campo que pueda fallar.
    """
    print("\n" + "=" * 55)
    print("  REGISTRAR NUEVO CLIENTE")
    print("=" * 55)
    logger.info("Iniciando registro de nuevo cliente.")

    # ---- ID del cliente ----
    # Pedimos el ID como texto y luego intentamos convertirlo a entero.
    # Usamos try/except para que un ID inválido no detenga el programa.
    while True:
        try:
            id_str = pedir_texto("  ID del cliente (número): ", "ID")
            id_cliente = int(id_str)
            if id_cliente <= 0:
                raise ErrorValidacion("El ID debe ser un número positivo.")
            # Verificamos que no exista ya un cliente con ese ID
            ids_existentes = [c.id_cliente for c in clientes]
            if id_cliente in ids_existentes:
                raise ErrorValidacion(
                    f"Ya existe un cliente con el ID {id_cliente}."
                )
            break  # Si llega aquí, el ID es válido → salimos del bucle
        except ValueError:
            print("  [!] El ID debe ser un número entero.")
            logger.warning("ID de cliente no numérico ingresado.")
        except ErrorValidacion as e:
            print(f"  [!] {e}")
            logger.warning(f"ID inválido: {e}")

    # ---- Nombre ----
    nombre = pedir_texto("  Nombre completo: ", "nombre")

    # ---- Email ----
    # La clase Cliente valida el formato del email internamente.
    # Si el formato es inválido, lanza ErrorValidacion.
    # Por eso envolvemos la creación del cliente en un try/except.
    while True:
        try:
            email = pedir_texto("  Email: ", "email")
            # Hacemos una validación previa simple antes de pasárselo al objeto
            if "@" not in email or "." not in email.split("@")[-1]:
                raise ErrorValidacion(
                    "El email debe tener formato válido (ej: usuario@dominio.com)."
                )
            break
        except ErrorValidacion as e:
            print(f"  [!] {e}")
            logger.warning(f"Email inválido ingresado: {e}")

    # ---- Teléfono ----
    # La clase Cliente también valida el teléfono, así que hacemos
    # algo similar: pedimos y dejamos que el constructor lo valide.
    while True:
        try:
            telefono = pedir_texto("  Teléfono (10 dígitos): ", "teléfono")
            if not telefono.isdigit() or len(telefono) != 10:
                raise ErrorValidacion(
                    "El teléfono debe tener exactamente 10 dígitos numéricos."
                )
            break
        except ErrorValidacion as e:
            print(f"  [!] {e}")
            logger.warning(f"Teléfono inválido: {e}")

    # ---- Crear el objeto Cliente ----
    # Aquí usamos try/except/else/finally para demostrar el patrón completo:
    # - try: intentamos crear el objeto (puede fallar si Cliente valida algo más)
    # - except: capturamos cualquier error de validación
    # - else: se ejecuta SOLO si NO hubo excepción (éxito total)
    # - finally: se ejecuta SIEMPRE (para limpieza o mensajes de cierre)
    try:
        nuevo_cliente = Cliente(
            id_cliente=id_cliente,
            nombre=nombre,
            email=email,
            telefono=telefono
        )
    except ErrorValidacion as e:
        # El constructor de Cliente detectó algo inválido
        print(f"\n  [ERROR] No se pudo registrar el cliente: {e}")
        logger.error(f"Fallo al crear Cliente id={id_cliente}: {e}")
    except Exception as e:
        # Capturamos cualquier otro error inesperado
        print(f"\n  [ERROR INESPERADO] {e}")
        logger.error(f"Error inesperado al crear cliente: {e}")
    else:
        # Este bloque SOLO se ejecuta si el try fue exitoso (sin excepciones)
        clientes.append(nuevo_cliente)
        print(f"\n  [OK] Cliente '{nombre}' registrado exitosamente con ID {id_cliente}.")
        logger.info(
            f"Cliente registrado exitosamente: id={id_cliente}, nombre={nombre}, "
            f"email={email}."
        )
    finally:
        # Este bloque se ejecuta SIEMPRE, haya o no excepción.
        # Sirve para acciones de limpieza o mensajes de cierre de operación.
        print("  --- Operación de registro de cliente finalizada. ---")
        logger.info("Operación registrar_cliente finalizada.")


# =====================================================================
#  OPCIÓN 2: CREAR UN SERVICIO
#  Dependiendo del tipo elegido por el usuario (sala / equipo / asesoría),
#  pedimos datos distintos y creamos el objeto correspondiente.
#  Esto demuestra polimorfismo: misma lista 'servicios', distintos objetos.
# =====================================================================
def crear_servicio():
    """
    Muestra un submenú para que el usuario elija el tipo de servicio
    y luego solicita los datos específicos de ese tipo.
    """
    print("\n" + "=" * 55)
    print("  CREAR NUEVO SERVICIO")
    print("=" * 55)
    print("  Tipos de servicio disponibles:")
    print("    1. Sala de reuniones (ServicioSala)")
    print("    2. Alquiler de equipo (AlquilerEquipo)")
    print("    3. Asesoría especializada (AsesoriaEspecializada)")
    print("=" * 55)

    tipo = pedir_entero("  Seleccione tipo (1-3): ", minimo=1, maximo=3)

    # ---- Datos comunes a todos los servicios ----
    nombre_servicio = pedir_texto("  Nombre del servicio: ", "nombre del servicio")
    precio_hora = pedir_flotante("  Precio por hora ($): ", minimo=1.0)

    # ---- Datos específicos según el tipo ----
    # Usamos try/except/else/finally de nuevo para proteger la creación
    try:
        if tipo == 1:
            # ServicioSala necesita el tipo de sala (conferencias, coworking, etc.)
            print("\n  Tipos de sala: conferencias, coworking, auditorio, privada")
            tipo_sala = pedir_texto("  Tipo de sala: ", "tipo de sala")
            nuevo_servicio = ServicioSala(
                nombre=nombre_servicio,
                precio_hora=precio_hora,
                tipo_sala=tipo_sala
            )

        elif tipo == 2:
            # AlquilerEquipo necesita saber si es portátil (tiene recargo del 10%)
            print("\n  Tipos de equipo: portatil, proyector, camara, impresora, tablet")
            tipo_equipo = pedir_texto("  Tipo de equipo: ", "tipo de equipo")
            nuevo_servicio = AlquilerEquipo(
                nombre=nombre_servicio,
                precio_hora=precio_hora,
                tipo_equipo=tipo_equipo
            )

        else:
            # AsesoriaEspecializada necesita el tema y mínimo de horas
            tema = pedir_texto("  Tema de la asesoría: ", "tema")
            horas_minimas = pedir_entero(
                "  Horas mínimas de contratación: ", minimo=1
            )
            nuevo_servicio = AsesoriaEspecializada(
                nombre=nombre_servicio,
                precio_hora=precio_hora,
                tema=tema,
                horas_minimas=horas_minimas
            )

    except ErrorValidacion as e:
        print(f"\n  [ERROR] No se pudo crear el servicio: {e}")
        logger.error(f"Fallo al crear servicio tipo={tipo}: {e}")

    except Exception as e:
        print(f"\n  [ERROR INESPERADO] {e}")
        logger.error(f"Error inesperado al crear servicio: {e}")

    else:
        # Solo si no hubo excepción, agregamos el servicio a la lista
        servicios.append(nuevo_servicio)
        print(f"\n  [OK] Servicio '{nombre_servicio}' creado exitosamente.")
        logger.info(
            f"Servicio creado: tipo={tipo}, nombre={nombre_servicio}, "
            f"precio_hora={precio_hora}."
        )

    finally:
        print("  --- Operación de creación de servicio finalizada. ---")
        logger.info("Operación crear_servicio finalizada.")


# =====================================================================
#  OPCIÓN 3: REALIZAR UNA RESERVA
#  Le mostramos al usuario los clientes y servicios disponibles.
#  El usuario elige cuál cliente, cuál servicio y cuántas horas.
#  Creamos el objeto Reserva y llamamos a su método confirmar().
# =====================================================================
def realizar_reserva():
    """
    Guía al usuario en la creación y confirmación de una nueva reserva.
    Captura ServicioNoDisponible, ReservaInvalida y ErrorValidacion.
    """
    print("\n" + "=" * 55)
    print("  REALIZAR NUEVA RESERVA")
    print("=" * 55)
    logger.info("Iniciando proceso de reserva.")

    # ---- Verificar que existan clientes y servicios ----
    # No tiene sentido continuar si no hay datos cargados.
    if not clientes:
        print("  [!] No hay clientes registrados. Registre uno primero.")
        logger.warning("Intento de reserva sin clientes registrados.")
        return  # Salimos de la función sin hacer nada más

    if not servicios:
        print("  [!] No hay servicios disponibles. Cree uno primero.")
        logger.warning("Intento de reserva sin servicios disponibles.")
        return

    # ---- Mostrar lista de clientes ----
    print("\n  CLIENTES REGISTRADOS:")
    print("  " + "-" * 45)
    for i, cliente in enumerate(clientes):
        # Accedemos a los atributos del cliente para mostrarlos
        # (asumimos que Cliente tiene propiedades id_cliente y nombre)
        print(f"  [{i}] ID: {cliente.id_cliente} - {cliente.nombre}")
    print("  " + "-" * 45)

    # Pedimos el índice del cliente en la lista
    indice_cliente = pedir_entero(
        "  Índice del cliente (número entre corchetes): ",
        minimo=0,
        maximo=len(clientes) - 1
    )
    cliente_seleccionado = clientes[indice_cliente]

    # ---- Mostrar lista de servicios ----
    print("\n  SERVICIOS DISPONIBLES:")
    print("  " + "-" * 45)
    for i, servicio in enumerate(servicios):
        # El método __str__ o descripcion() debería estar definido en Servicio
        # Si no existe, mostramos el nombre directamente
        try:
            descripcion = servicio.describir_servicio()
        except AttributeError:
            descripcion = servicio.nombre
        print(f"  [{i}] {descripcion}")
    print("  " + "-" * 45)

    indice_servicio = pedir_entero(
        "  Índice del servicio (número entre corchetes): ",
        minimo=0,
        maximo=len(servicios) - 1
    )
    servicio_seleccionado = servicios[indice_servicio]

    # ---- Duración de la reserva ----
    duracion = pedir_entero(
        "  Duración en horas: ",
        minimo=1
    )

    # ---- Crear y confirmar la reserva ----
    # Aquí usamos el patrón try/except/else/finally completo.
    # La clase Reserva usa este mismo patrón en su método confirmar(),
    # así que estamos anidando el manejo de excepciones.
    try:
        # Creamos el objeto Reserva con los datos seleccionados
        nueva_reserva = Reserva(
            cliente=cliente_seleccionado,
            servicio=servicio_seleccionado,
            duracion_horas=duracion
        )

        # Llamamos al método confirmar() que internamente usa try/except/else/finally
        # y puede lanzar ServicioNoDisponible o ReservaInvalida
        nueva_reserva.confirmar()

    except ServicioNoDisponible as e:
        # El servicio no está disponible (por ejemplo, ya está reservado)
        print(f"\n  [ERROR] Servicio no disponible: {e}")
        logger.error(
            f"ServicioNoDisponible al reservar '{servicio_seleccionado.nombre}': {e}"
        )

    except ReservaInvalida as e:
        # La reserva tiene parámetros inválidos (duración insuficiente, etc.)
        print(f"\n  [ERROR] Reserva inválida: {e}")
        logger.error(
            f"ReservaInvalida para cliente id={cliente_seleccionado.id_cliente}: {e}"
        )

    except ErrorValidacion as e:
        # Algún dato de la reserva no pasó la validación
        print(f"\n  [ERROR] Error de validación: {e}")
        logger.error(f"ErrorValidacion en reserva: {e}")

    except Exception as e:
        # Cualquier otro error inesperado
        print(f"\n  [ERROR INESPERADO] {e}")
        logger.error(f"Error inesperado en realizar_reserva: {e}")

    else:
        # Si llegamos aquí, la reserva se creó y confirmó sin problemas
        reservas.append(nueva_reserva)
        try:
            costo = nueva_reserva.costo_total
            print(
                f"\n  [OK] Reserva confirmada para '{cliente_seleccionado.nombre}'."
            )
            print(f"       Servicio: {servicio_seleccionado.nombre}")
            print(f"       Duración: {duracion} hora(s)")
            print(f"       Costo total: ${costo:,.2f}")
        except AttributeError:
            print(f"\n  [OK] Reserva confirmada para '{cliente_seleccionado.nombre}'.")

        logger.info(
            f"Reserva confirmada: cliente_id={cliente_seleccionado.id_cliente}, "
            f"servicio={servicio_seleccionado.nombre}, horas={duracion}."
        )

    finally:
        print("  --- Operación de reserva finalizada. ---")
        logger.info("Operación realizar_reserva finalizada.")


# =====================================================================
#  OPCIÓN 4: CANCELAR UNA RESERVA
#  Mostramos las reservas activas y permitimos cancelar una por índice.
# =====================================================================
def cancelar_reserva():
    """
    Permite al usuario cancelar una reserva existente seleccionándola
    por su índice en la lista de reservas activas.
    """
    print("\n" + "=" * 55)
    print("  CANCELAR RESERVA")
    print("=" * 55)
    logger.info("Iniciando proceso de cancelación de reserva.")

    # Filtramos solo las reservas que no estén ya canceladas
    # El atributo 'estado' debe existir en la clase Reserva
    try:
        reservas_activas = [
            (i, r) for i, r in enumerate(reservas)
            if r.estado != "cancelada"
        ]
    except AttributeError:
        # Si la clase Reserva no tiene atributo 'estado', mostramos todas
        reservas_activas = list(enumerate(reservas))
        logger.warning("Atributo 'estado' no encontrado en Reserva, mostrando todas.")

    if not reservas_activas:
        print("  [!] No hay reservas activas para cancelar.")
        logger.info("No hay reservas activas al intentar cancelar.")
        return

    # Mostramos las reservas activas con su índice original en la lista
    print("\n  RESERVAS ACTIVAS:")
    print("  " + "-" * 55)
    for idx_original, reserva in reservas_activas:
        try:
            info = (
                f"  [{idx_original}] Cliente: {reserva.cliente.nombre} | "
                f"Servicio: {reserva.servicio.nombre} | "
                f"Estado: {reserva.estado}"
            )
        except AttributeError:
            info = f"  [{idx_original}] Reserva #{idx_original}"
        print(info)
    print("  " + "-" * 55)

    # Pedimos el índice de la reserva a cancelar
    indices_validos = [i for i, _ in reservas_activas]
    while True:
        indice = pedir_entero(
            f"  Ingrese el índice de la reserva a cancelar "
            f"({indices_validos[0]}-{indices_validos[-1]}): ",
            minimo=indices_validos[0],
            maximo=indices_validos[-1]
        )
        if indice in indices_validos:
            break
        print(f"  [!] Índice {indice} no corresponde a una reserva activa.")

    # ---- Cancelar la reserva seleccionada ----
    try:
        reserva_a_cancelar = reservas[indice]
        reserva_a_cancelar.cancelar()

    except ReservaInvalida as e:
        # La clase Reserva puede lanzar esto si ya está cancelada o confirmada
        print(f"\n  [ERROR] No se pudo cancelar: {e}")
        logger.error(f"ReservaInvalida al cancelar reserva[{indice}]: {e}")

    except Exception as e:
        print(f"\n  [ERROR INESPERADO] {e}")
        logger.error(f"Error inesperado al cancelar reserva[{indice}]: {e}")

    else:
        print(f"\n  [OK] La reserva #{indice} fue cancelada exitosamente.")
        logger.info(f"Reserva[{indice}] cancelada exitosamente.")

    finally:
        print("  --- Operación de cancelación finalizada. ---")
        logger.info("Operación cancelar_reserva finalizada.")


# =====================================================================
#  OPCIÓN 5: LISTAR TODAS LAS RESERVAS
#  Muestra un resumen de todas las reservas con su estado y costo.
#  No modifica datos, es solo lectura. También usamos try/except por
#  si algún objeto tiene atributos faltantes o inesperados.
# =====================================================================
def listar_reservas():
    """
    Muestra en pantalla todas las reservas registradas en el sistema,
    con su estado actual y el costo total calculado.
    """
    print("\n" + "=" * 55)
    print("  LISTADO COMPLETO DE RESERVAS")
    print("=" * 55)
    logger.info("Listando todas las reservas del sistema.")

    if not reservas:
        print("  No hay reservas registradas en el sistema.")
        logger.info("Listado vacío: no hay reservas.")
        return

    print(f"  Total de reservas: {len(reservas)}\n")
    print("  " + "-" * 65)

    for i, reserva in enumerate(reservas):
        # Usamos try/except para que si algún objeto está incompleto
        # no se caiga todo el listado, sino que muestre lo que pueda
        try:
            nombre_cliente = reserva.cliente.nombre
            nombre_servicio = reserva.servicio.nombre
            duracion = reserva.duracion_horas
            estado = reserva.estado

            # Intentamos obtener el costo total
            try:
                costo = reserva.costo_total
                costo_str = f"${costo:,.2f}"
            except (AttributeError, TypeError):
                costo_str = "No calculado"

            print(f"  Reserva #{i + 1}:")
            print(f"    Cliente  : {nombre_cliente}")
            print(f"    Servicio : {nombre_servicio}")
            print(f"    Duración : {duracion} hora(s)")
            print(f"    Estado   : {estado}")
            print(f"    Costo    : {costo_str}")
            print("  " + "-" * 65)

        except AttributeError as e:
            # Si el objeto Reserva no tiene algún atributo esperado
            print(f"  Reserva #{i + 1}: [Datos incompletos - {e}]")
            logger.error(f"AttributeError al listar reserva[{i}]: {e}")

        except Exception as e:
            print(f"  Reserva #{i + 1}: [Error al mostrar - {e}]")
            logger.error(f"Error inesperado al listar reserva[{i}]: {e}")

    logger.info(f"Listado de {len(reservas)} reserva(s) completado.")


# =====================================================================
#  FUNCIÓN PRINCIPAL: main_menu
#  Este es el corazón del módulo. Muestra el menú y despacha al usuario
#  a la función correspondiente según su elección.
#  El bucle while True garantiza que el programa siga corriendo hasta
#  que el usuario elija explícitamente la opción "Salir".
# =====================================================================
def main_menu():
    """
    Ejecuta el bucle principal del menú interactivo de consola.
    El usuario puede navegar entre las opciones hasta elegir salir.
    El programa NUNCA se detiene por un error gracias al manejo de
    excepciones en cada operación.
    """
    # Mensaje de bienvenida
    print("\n" + "=" * 55)
    print("  BIENVENIDO AL SISTEMA - SOFTWARE FJ")
    print("  Gestión de Clientes, Servicios y Reservas")
    print("=" * 55)
    logger.info("Sistema iniciado: menú interactivo activo.")

    # El bucle while True mantiene el menú activo indefinidamente.
    # Solo salimos cuando el usuario elige la opción 6 (Salir).
    while True:
        # ---- Mostrar las opciones del menú ----
        print("\n" + "-" * 55)
        print("  MENÚ PRINCIPAL")
        print("-" * 55)
        print("  1. Registrar un cliente")
        print("  2. Crear un servicio")
        print("  3. Realizar una reserva")
        print("  4. Cancelar una reserva")
        print("  5. Listar todas las reservas")
        print("  6. Salir")
        print("-" * 55)

        # ---- Leer la opción del usuario ----
        # Envolvemos en try/except para manejar entradas completamente
        # inesperadas (como Ctrl+D en Linux que lanza EOFError).
        try:
            opcion = pedir_entero("  Seleccione una opción (1-6): ", minimo=1, maximo=6)

        except KeyboardInterrupt:
            # El usuario presionó Ctrl+C
            print("\n\n  [!] Interrupción del usuario. Saliendo del sistema...")
            logger.info("Sistema interrumpido por el usuario (Ctrl+C).")
            break  # Salimos del bucle while

        except EOFError:
            # El usuario cerró el stream de entrada
            print("\n\n  [!] Stream de entrada cerrado. Saliendo...")
            logger.warning("EOFError: stream de entrada cerrado.")
            break

        # ---- Despachar la opción seleccionada ----
        # Cada opción llama a su función correspondiente.
        # Si esa función falla internamente (aunque tiene su propio
        # manejo), este try/except exterior es el último recurso.
        try:
            if opcion == 1:
                registrar_cliente()

            elif opcion == 2:
                crear_servicio()

            elif opcion == 3:
                realizar_reserva()

            elif opcion == 4:
                cancelar_reserva()

            elif opcion == 5:
                listar_reservas()

            elif opcion == 6:
                # El usuario quiere salir → rompemos el bucle
                print("\n  ¡Hasta luego! Gracias por usar Software FJ.")
                logger.info("Usuario seleccionó salir. Sistema cerrando.")
                break  # Salimos del while True

        except Exception as e:
            # Última línea de defensa: si algo falla de forma completamente
            # inesperada en cualquiera de las funciones, el programa NO se cae.
            # Se muestra un mensaje amigable y el menú vuelve a aparecer.
            print(f"\n  [ERROR CRITICO] Ocurrió un error inesperado: {e}")
            print("  El sistema sigue funcionando. Por favor intente de nuevo.")
            logger.critical(
                f"Error crítico no controlado en opcion={opcion}: {e}",
                exc_info=True  # Esto guarda el traceback completo en el log
            )

    # ---- Mensaje de cierre ----
    print("\n" + "=" * 55)
    print("  Sistema finalizado correctamente.")
    print("=" * 55)
    logger.info("main_menu finalizado. Sistema cerrado normalmente.")


# =====================================================================
#  PUNTO DE ENTRADA DIRECTO
#  Si ejecutamos este archivo directamente (python menu_interactivo.py),
#  Python setea __name__ == "__main__" y llama a main_menu().
#  Si este archivo es importado por otro (como main.py), este bloque
#  NO se ejecuta, lo que evita que el menú arranque solo al importar.
# =====================================================================
if __name__ == "__main__":
    main_menu()
