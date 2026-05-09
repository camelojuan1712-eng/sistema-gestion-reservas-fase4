# =====================================================================
#  ARCHIVO: utilidades.py
#  PROYECTO: Sistema de Gestión de Clientes, Servicios y Reservas
#  EMPRESA FICTICIA: Software FJ
#  CURSO: Programación 213023 - UNAD
#  DESCRIPCIÓN:
#    Este módulo reúne funciones auxiliares reutilizables que apoyan
#    el resto del sistema. Ninguna función aquí modifica el estado
#    del sistema; todas son de lectura/cálculo/formateo/exportación.
#
#    Funciones incluidas:
#      - exportar_resumen(reservas, archivo)
#      - formatear_dinero(valor, simbolo)
#      - generar_reporte_ingresos(reservas)
#      - validar_id(id_str)
#
#  DISEÑO: Separar utilidades en su propio módulo sigue el principio
#    de responsabilidad única (SRP): cada módulo hace una sola cosa.
#    Así, si necesitamos cambiar cómo se exporta el resumen, solo
#    tocamos este archivo, no los demás.
# =====================================================================

# ---------------------  IMPORTACIONES  ------------------------------
# Importamos la excepción personalizada del proyecto.
# La usamos en validar_id() y formatear_dinero() para señalar datos
# inválidos de manera coherente con el resto del sistema.
from excepciones import ErrorValidacion

# Importamos el logger centralizado del proyecto.
# Usamos el mismo logger en todos los módulos para que el archivo
# de log sea único y contenga toda la historia de eventos.
from logger_config import obtener_logger

# ---- Módulo de fechas para registrar cuándo se generaron los reportes ----
from datetime import datetime

# =====================================================================
#  CONFIGURACIÓN DEL LOGGER
# =====================================================================
logger = obtener_logger()


# =====================================================================
#  FUNCIÓN 1: exportar_resumen
#  Escribe un archivo de texto plano con el resumen de todas las
#  reservas recibidas. Si la lista está vacía, lo indica en el archivo.
#
#  ¿Por qué usamos try/except aquí?
#  Porque trabajar con archivos es una operación que puede fallar por
#  razones externas al programa: disco lleno, permisos denegados,
#  ruta inexistente, etc. Estas son excepciones de tipo OSError /
#  PermissionError / IOError y debemos capturarlas para no detener
#  el sistema.
# =====================================================================
def exportar_resumen(reservas, archivo="resumen.txt"):
    """
    Exporta un resumen detallado de las reservas a un archivo de texto.

    Escribe número de reserva, cliente, servicio, duración, estado y
    costo total para cada reserva. Si la lista está vacía, escribe un
    mensaje indicándolo.

    Args:
        reservas (list): Lista de objetos Reserva del sistema.
        archivo (str): Nombre o ruta del archivo de salida.
                       Por defecto es "resumen.txt" en el directorio actual.

    Returns:
        bool: True si la exportación fue exitosa, False si hubo un error.

    Raises:
        No lanza excepciones hacia afuera; las captura internamente.
    """
    # Registramos en el log que se está llamando a esta función
    logger.info(f"Iniciando exportación de resumen a '{archivo}'.")

    # Obtenemos la fecha y hora actual para incluirla en el encabezado
    fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Usamos try/except/else/finally para el manejo completo del archivo
    try:
        # Abrimos el archivo en modo escritura ('w').
        # Si ya existe, lo sobreescribe. Si no existe, lo crea.
        # Usamos encoding='utf-8' para soportar tildes y caracteres especiales.
        with open(archivo, "w", encoding="utf-8") as f:

            # ---- Encabezado del archivo ----
            f.write("=" * 65 + "\n")
            f.write("  RESUMEN DEL SISTEMA - SOFTWARE FJ\n")
            f.write(f"  Generado el: {fecha_actual}\n")
            f.write("=" * 65 + "\n\n")

            # ---- Caso especial: lista vacía ----
            if not reservas:
                f.write("No hay reservas registradas en el sistema.\n")
                logger.info("Resumen exportado: lista de reservas vacía.")

            else:
                # ---- Escribir cada reserva ----
                f.write(f"  Total de reservas: {len(reservas)}\n\n")
                f.write("-" * 65 + "\n")

                for i, reserva in enumerate(reservas, start=1):
                    # Usamos un try interior para que si UN objeto tiene
                    # datos faltantes, solo ese ítem falle, no todo el archivo.
                    try:
                        nombre_cliente = reserva.cliente.nombre
                        id_cliente = reserva.cliente.id_cliente
                        nombre_servicio = reserva.servicio.nombre
                        duracion = reserva.duracion_horas
                        estado = reserva.estado

                        # Intentamos obtener costo_total (puede no estar calculado)
                        try:
                            costo = reserva.costo_total
                            costo_str = formatear_dinero(costo)
                        except (AttributeError, TypeError, ErrorValidacion):
                            costo_str = "No disponible"

                        f.write(f"  Reserva #{i}\n")
                        f.write(f"    Cliente   : {nombre_cliente} (ID: {id_cliente})\n")
                        f.write(f"    Servicio  : {nombre_servicio}\n")
                        f.write(f"    Duración  : {duracion} hora(s)\n")
                        f.write(f"    Estado    : {estado}\n")
                        f.write(f"    Costo     : {costo_str}\n")
                        f.write("-" * 65 + "\n")

                    except AttributeError as e:
                        # El objeto Reserva no tiene todos los atributos esperados
                        f.write(f"  Reserva #{i}: [Datos incompletos - {e}]\n")
                        f.write("-" * 65 + "\n")
                        logger.error(
                            f"AttributeError al exportar reserva #{i}: {e}"
                        )

                # ---- Pie del archivo ----
                f.write("\n  Fin del resumen.\n")
                f.write("=" * 65 + "\n")

    except PermissionError as e:
        # El sistema operativo no nos permite escribir en esa ruta
        print(f"  [ERROR] Sin permiso para escribir en '{archivo}': {e}")
        logger.error(
            f"PermissionError al exportar resumen a '{archivo}': {e}"
        )
        return False  # Indicamos falla

    except FileNotFoundError as e:
        # La ruta especificada no existe (por ejemplo, una carpeta inexistente)
        print(f"  [ERROR] Ruta no encontrada '{archivo}': {e}")
        logger.error(
            f"FileNotFoundError al exportar resumen a '{archivo}': {e}"
        )
        return False

    except OSError as e:
        # OSError es la clase base de los errores de sistema de archivos.
        # Captura casos como disco lleno, nombre de archivo inválido, etc.
        print(f"  [ERROR] Error del sistema de archivos: {e}")
        logger.error(f"OSError al exportar resumen: {e}")
        return False

    except Exception as e:
        # Cualquier otro error inesperado
        print(f"  [ERROR INESPERADO] al exportar resumen: {e}")
        logger.error(f"Error inesperado en exportar_resumen: {e}", exc_info=True)
        return False

    else:
        # Este bloque SOLO se ejecuta si NO hubo ninguna excepción en el try.
        # Aquí confirmamos el éxito de la operación.
        print(f"  [OK] Resumen exportado exitosamente a '{archivo}'.")
        logger.info(
            f"Resumen exportado con éxito a '{archivo}'. "
            f"Reservas procesadas: {len(reservas)}."
        )
        return True  # Indicamos éxito

    finally:
        # Este bloque se ejecuta SIEMPRE, sea éxito o error.
        # Es el lugar ideal para mensajes de cierre o liberación de recursos.
        logger.info(f"Operación exportar_resumen finalizada (archivo='{archivo}').")


# =====================================================================
#  FUNCIÓN 2: formatear_dinero
#  Convierte un número a formato de moneda colombiana.
#  Ejemplo: 1234567.5 → "$1,234,567.50"
#
#  ¿Por qué lanzamos ErrorValidacion en vez de ValueError?
#  Porque en nuestro sistema, ErrorValidacion es la excepción estándar
#  para datos inválidos del dominio del negocio. Así el código que
#  llama a esta función solo necesita capturar UN tipo de excepción
#  para todos los errores de validación del sistema.
# =====================================================================
def formatear_dinero(valor, simbolo="$"):
    """
    Convierte un valor numérico a formato de moneda colombiana.

    Formato: $1,234,567.00 (separador de miles con coma, dos decimales).

    Args:
        valor (int | float): Cantidad a formatear. Debe ser >= 0.
        simbolo (str): Símbolo de moneda. Por defecto "$".

    Returns:
        str: El valor formateado como cadena de moneda.

    Raises:
        ErrorValidacion: Si el valor es None, negativo o no numérico.
    """
    logger.info(f"Formateando valor monetario: {valor}")

    try:
        # ---- Validación de None ----
        # None no es un número válido para representar dinero.
        if valor is None:
            raise ErrorValidacion(
                "El valor monetario no puede ser None."
            )

        # ---- Convertimos a float ----
        # Lo hacemos explícitamente para capturar el caso en que alguien
        # pase un string no numérico como "abc".
        valor_float = float(valor)

        # ---- Validación de negativo ----
        # En el contexto del negocio, los costos nunca son negativos.
        # Si alguien pasa un valor negativo, es un error lógico.
        if valor_float < 0:
            raise ErrorValidacion(
                f"El valor monetario no puede ser negativo: {valor_float}"
            )

        # ---- Formateo con separadores de miles ----
        # Python tiene soporte nativo para esto con los f-strings y format.
        # {:,.2f} significa: separador de miles con coma, 2 decimales.
        valor_formateado = f"{simbolo}{valor_float:,.2f}"

        logger.info(f"Valor formateado exitosamente: {valor_formateado}")
        return valor_formateado

    except ErrorValidacion as e:
        # Re-lanzamos la excepción para que quien llame a esta función
        # pueda decidir qué hacer con ella.
        # Usamos "raise ... from e" para encadenar excepciones:
        # el traceback mostrará tanto el error original como éste.
        logger.error(f"ErrorValidacion en formatear_dinero: {e}")
        raise  # Re-lanzamos la misma excepción sin modificarla

    except (TypeError, ValueError) as e:
        # TypeError: valor no es numérico en absoluto (ej: una lista)
        # ValueError: float() no pudo convertir el valor (ej: "abc")
        mensaje = (
            f"El valor '{valor}' no es un número válido para formatear: {e}"
        )
        logger.error(f"TypeError/ValueError en formatear_dinero: {mensaje}")
        # Encadenamos la excepción original con nuestra ErrorValidacion
        # usando "raise ... from e". Esto es "encadenamiento de excepciones"
        # y permite ver la causa raíz en el traceback.
        raise ErrorValidacion(mensaje) from e

    except Exception as e:
        # Captura cualquier otro error inesperado
        logger.error(
            f"Error inesperado en formatear_dinero(valor={valor}): {e}"
        )
        raise ErrorValidacion(f"Error inesperado al formatear dinero: {e}") from e


# =====================================================================
#  FUNCIÓN 3: generar_reporte_ingresos
#  Analiza la lista de reservas y devuelve un diccionario con
#  estadísticas del sistema: ingresos totales, conteos por estado, etc.
#
#  ¿Por qué devolvemos un diccionario en vez de imprimir directamente?
#  Porque así la función es reutilizable: el menú puede mostrar el
#  reporte en consola, el exportador puede guardarlo en un archivo,
#  y otro módulo puede usarlo para calcular algo más.
# =====================================================================
def generar_reporte_ingresos(reservas):
    """
    Analiza una lista de reservas y genera estadísticas de ingresos.

    Calcula el total de ingresos (solo reservas confirmadas), la cantidad
    total de reservas, y el conteo por estado (confirmadas, canceladas,
    pendientes).

    Args:
        reservas (list): Lista de objetos Reserva del sistema.

    Returns:
        dict: Diccionario con las siguientes claves:
            - "total_ingresos" (float): Suma de costos de reservas confirmadas.
            - "total_reservas" (int): Cantidad total de reservas.
            - "reservas_confirmadas" (int): Cantidad con estado "confirmada".
            - "reservas_canceladas" (int): Cantidad con estado "cancelada".
            - "reservas_pendientes" (int): Cantidad con otros estados.
    """
    logger.info("Iniciando generación de reporte de ingresos.")

    # ---- Inicializamos los contadores ----
    # Empezamos en cero y vamos acumulando en el bucle.
    total_ingresos = 0.0
    total_reservas = 0
    confirmadas = 0
    canceladas = 0
    pendientes = 0

    # Verificamos si la lista está vacía antes de iterar
    if not reservas:
        logger.info("Reporte generado con lista vacía.")
        return {
            "total_ingresos": 0.0,
            "total_reservas": 0,
            "reservas_confirmadas": 0,
            "reservas_canceladas": 0,
            "reservas_pendientes": 0
        }

    # ---- Iterar sobre cada reserva ----
    for i, reserva in enumerate(reservas):
        # Incrementamos el contador total siempre
        total_reservas += 1

        try:
            # Intentamos leer el estado de la reserva
            estado = reserva.estado

            # Clasificamos la reserva según su estado
            if estado == "confirmada":
                confirmadas += 1

                # Intentamos sumar el costo total al ingreso acumulado.
                # Lo hacemos en un try interno porque costo_total puede no
                # estar calculado (ej: reserva creada pero no confirmada aún).
                try:
                    costo = reserva.costo_total
                    if costo is not None:
                        total_ingresos += float(costo)
                    else:
                        logger.warning(
                            f"Reserva #{i} confirmada pero costo_total es None."
                        )

                except AttributeError:
                    # La reserva no tiene el atributo costo_total
                    logger.error(
                        f"Reserva #{i} no tiene atributo 'costo_total'. "
                        f"Se omite del total de ingresos."
                    )

                except (TypeError, ValueError) as e:
                    # costo_total tiene un valor que no se puede convertir a float
                    logger.error(
                        f"costo_total inválido en reserva #{i}: {e}. Se omite."
                    )

            elif estado == "cancelada":
                canceladas += 1
                # Las reservas canceladas NO suman ingresos

            else:
                # Estados como "pendiente", "en proceso", etc.
                pendientes += 1

        except AttributeError as e:
            # La reserva no tiene el atributo 'estado'
            # La contamos como pendiente para no perderla del total
            pendientes += 1
            logger.error(
                f"Reserva #{i} no tiene atributo 'estado': {e}. "
                f"Contada como pendiente."
            )

        except Exception as e:
            # Cualquier otro error en el procesamiento de esta reserva
            # No detenemos el ciclo; simplemente registramos y continuamos.
            pendientes += 1
            logger.error(
                f"Error inesperado al procesar reserva #{i} en reporte: {e}",
                exc_info=True
            )

    # ---- Construimos el diccionario de resultados ----
    reporte = {
        "total_ingresos": total_ingresos,
        "total_reservas": total_reservas,
        "reservas_confirmadas": confirmadas,
        "reservas_canceladas": canceladas,
        "reservas_pendientes": pendientes
    }

    logger.info(
        f"Reporte generado: total={total_reservas}, "
        f"confirmadas={confirmadas}, canceladas={canceladas}, "
        f"pendientes={pendientes}, ingresos={total_ingresos}."
    )

    return reporte


# =====================================================================
#  FUNCIÓN 4: validar_id
#  Convierte una cadena de texto a un entero positivo válido.
#  Si no es posible, lanza ErrorValidacion con un mensaje descriptivo.
#
#  ¿Por qué existe esta función si Python ya tiene int()?
#  Porque int() lanza ValueError con mensajes técnicos como
#  "invalid literal for int() with base 10: 'abc'", que no le dicen
#  nada útil al usuario. Nuestra función lanza ErrorValidacion con
#  un mensaje claro y además registra en el log.
# =====================================================================
def validar_id(id_str):
    """
    Valida y convierte una cadena de texto a un ID entero positivo.

    Un ID válido para este sistema es un número entero mayor que cero.

    Args:
        id_str (str): La cadena de texto que se desea validar como ID.

    Returns:
        int: El ID convertido a entero positivo.

    Raises:
        ErrorValidacion: Si la cadena no es un entero, es cero o negativa,
                         o si es None o está vacía.
    """
    logger.info(f"Validando ID: '{id_str}'")

    try:
        # ---- Validación de None ----
        if id_str is None:
            raise ErrorValidacion("El ID no puede ser None.")

        # ---- Limpiamos espacios ----
        id_limpio = str(id_str).strip()

        # ---- Validación de cadena vacía ----
        if not id_limpio:
            raise ErrorValidacion("El ID no puede estar vacío.")

        # ---- Conversión a entero ----
        # int() lanzará ValueError si id_limpio no es numérico.
        # Nosotros encadenamos ese error con ErrorValidacion.
        id_entero = int(id_limpio)

        # ---- Validación de positivo ----
        # Los IDs en nuestro sistema empiezan desde 1.
        if id_entero <= 0:
            raise ErrorValidacion(
                f"El ID debe ser un número positivo mayor que cero. "
                f"Se recibió: {id_entero}"
            )

        logger.info(f"ID validado exitosamente: {id_entero}")
        return id_entero

    except ErrorValidacion as e:
        # Re-lanzamos sin modificar para que el llamador la maneje
        logger.error(f"ErrorValidacion en validar_id('{id_str}'): {e}")
        raise

    except ValueError as e:
        # int() no pudo convertir el string a entero.
        # Encadenamos la excepción original con ErrorValidacion.
        # "raise X from Y" preserva el traceback original para depuración.
        mensaje = (
            f"'{id_str}' no es un ID válido. "
            f"Debe ser un número entero positivo."
        )
        logger.error(f"ValueError en validar_id('{id_str}'): {e}")
        raise ErrorValidacion(mensaje) from e

    except Exception as e:
        # Cualquier otro error inesperado
        mensaje = f"Error inesperado al validar ID '{id_str}': {e}"
        logger.error(mensaje, exc_info=True)
        raise ErrorValidacion(mensaje) from e


# =====================================================================
#  FUNCIÓN EXTRA: imprimir_reporte_consola
#  Esta función usa generar_reporte_ingresos() y muestra el resultado
#  formateado en consola. Es un ejemplo de cómo reutilizar las
#  funciones anteriores combinándolas.
# =====================================================================
def imprimir_reporte_consola(reservas):
    """
    Genera el reporte de ingresos y lo muestra formateado en consola.
    Combina generar_reporte_ingresos() y formatear_dinero() para
    producir una salida legible.

    Args:
        reservas (list): Lista de objetos Reserva del sistema.
    """
    logger.info("Imprimiendo reporte de ingresos en consola.")

    try:
        # Obtenemos el diccionario del reporte
        reporte = generar_reporte_ingresos(reservas)

        # Formateamos el total de ingresos con símbolo de pesos colombianos
        try:
            ingresos_str = formatear_dinero(reporte["total_ingresos"])
        except ErrorValidacion:
            ingresos_str = str(reporte["total_ingresos"])

        # Mostramos el reporte en consola
        print("\n" + "=" * 55)
        print("  REPORTE DE INGRESOS - SOFTWARE FJ")
        print("=" * 55)
        print(f"  Total de reservas      : {reporte['total_reservas']}")
        print(f"  Reservas confirmadas   : {reporte['reservas_confirmadas']}")
        print(f"  Reservas canceladas    : {reporte['reservas_canceladas']}")
        print(f"  Reservas pendientes    : {reporte['reservas_pendientes']}")
        print(f"  Ingresos totales       : {ingresos_str}")
        print("=" * 55)

        logger.info("Reporte impreso en consola exitosamente.")

    except Exception as e:
        print(f"  [ERROR] No se pudo generar el reporte: {e}")
        logger.error(f"Error al imprimir reporte en consola: {e}", exc_info=True)


# =====================================================================
#  BLOQUE DE PRUEBA LOCAL
#  Si ejecutamos este archivo directamente (python utilidades.py),
#  Python corre este bloque para verificar que las funciones funcionen.
#  En producción, este archivo se importa y este bloque no se ejecuta.
# =====================================================================
if __name__ == "__main__":
    print("\n" + "=" * 55)
    print("  PRUEBAS LOCALES - utilidades.py")
    print("=" * 55)

    # ---- Prueba de formatear_dinero ----
    print("\n[PRUEBA] formatear_dinero:")
    casos_dinero = [150000, 0, 1234567.89, 50.5]
    for valor in casos_dinero:
        try:
            resultado = formatear_dinero(valor)
            print(f"  formatear_dinero({valor}) = {resultado}")
        except ErrorValidacion as e:
            print(f"  formatear_dinero({valor}) ERROR: {e}")

    # Casos inválidos
    casos_invalidos = [None, -100, "abc"]
    for valor in casos_invalidos:
        try:
            resultado = formatear_dinero(valor)
            print(f"  formatear_dinero({valor}) = {resultado}")
        except ErrorValidacion as e:
            print(f"  formatear_dinero({valor!r}) -> ErrorValidacion: {e}")

    # ---- Prueba de validar_id ----
    print("\n[PRUEBA] validar_id:")
    casos_id = ["1", "42", "0", "-5", "abc", None, "  7  "]
    for caso in casos_id:
        try:
            resultado = validar_id(caso)
            print(f"  validar_id({caso!r}) = {resultado}")
        except ErrorValidacion as e:
            print(f"  validar_id({caso!r}) -> ErrorValidacion: {e}")

    # ---- Prueba de generar_reporte_ingresos con lista vacía ----
    print("\n[PRUEBA] generar_reporte_ingresos con lista vacía:")
    reporte = generar_reporte_ingresos([])
    print(f"  Resultado: {reporte}")

    # ---- Prueba de exportar_resumen con lista vacía ----
    print("\n[PRUEBA] exportar_resumen con lista vacía:")
    exportar_resumen([], archivo="resumen_prueba.txt")

    print("\n  Pruebas locales completadas.")
    print("=" * 55)
