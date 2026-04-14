# main.py - Archivo principal del juego Hundir la Flota
# Este archivo contiene la lógica principal del juego, integrando todas las funciones
# de los módulos auxiliares para crear una experiencia de juego completa.

# Importaciones de módulos auxiliares
from Constantes import *  # Importa todas las constantes del juego (símbolos, tamaños, flota)
from tablero import crear_tablero, mostrar_tablero  # Funciones para crear y mostrar tableros
from barcos import colocar_flota_aleatoria  # Función para colocar barcos automáticamente
from interfaz import pedir_coordenadas, pedir_orientacion, mostrar_resultado, mostrar_turno  # Funciones de interfaz de usuario
from cpu import cpu_disparo  # Función para que la CPU realice disparos
from juego import iniciar_partida, comprobar_fin, turno, jugar_partida  # Funciones del núcleo del juego
from ranking import guardar_partida, mostrar_ranking  # Funciones para guardar y mostrar estadísticas
import copy  # Para crear copias profundas de objetos complejos

def obtener_opcion_menu():
    """
    Solicita y valida la opción del menú principal.

    Returns:
        int: El modo seleccionado (1: vs CPU, 2: vs Jugador, 3: Ver ranking)
    """
    print("Bienvenido a Hundir la Flota!")  # Mensaje de bienvenida
    print("Elige el modo de juego:")
    print("1. Jugador vs CPU")      # Opción 1: jugar contra la computadora
    print("2. Jugador vs Jugador")  # Opción 2: jugar contra otro jugador
    print("3. Ver ranking")         # Opción 3: ver estadísticas de partidas anteriores

    # Solicitar opción numérica con validación
    opcion_valida = False
    opcion = None

    while not opcion_valida:
        try:
            opcion = int(input("Selecciona una opción (1-3): "))  # Solicitar opción numérica
            if opcion in [1, 2, 3]:  # Verificar que sea una opción válida
                opcion_valida = True
            else:
                print("Opción no válida. Elige 1, 2 o 3.")  # Mensaje de error
        except ValueError:  # Capturar errores de conversión a int
            print("Por favor, introduce un número válido.")  # Mensaje de error

    return opcion  # Devolver la opción seleccionada

def elegir_modo_juego():
    """
    Función que muestra el menú principal y permite al usuario elegir el modo de juego.

    Returns:
        int: El modo seleccionado (1: vs CPU, 2: vs Jugador, 3: Ver ranking)
    """
    return obtener_opcion_menu()

def obtener_dimensiones_tablero():
    """
    Solicita y valida las dimensiones del tablero.

    Returns:
        tuple: Tupla con (filas, columnas) validadas
    """
    print("\nConfiguración del tablero:")

    filas_validadas = False
    columnas_validadas = False
    filas = 0
    columnas = 0

    # Validar filas
    while not filas_validadas:
        try:
            filas = int(input(f"Número de filas ({TAMAÑO_MIN_FILAS}-{TAMAÑO_MAX_FILAS}): "))
            if TAMAÑO_MIN_FILAS <= filas <= TAMAÑO_MAX_FILAS:
                filas_validadas = True
            else:
                print(f"El número de filas debe estar entre {TAMAÑO_MIN_FILAS} y {TAMAÑO_MAX_FILAS}.")
        except ValueError:
            print("Por favor, introduce un número válido.")

    # Validar columnas
    while not columnas_validadas:
        try:
            columnas = int(input(f"Número de columnas ({TAMAÑO_MIN_COLUMNAS}-{TAMAÑO_MAX_COLUMNAS}): "))
            if TAMAÑO_MIN_COLUMNAS <= columnas <= TAMAÑO_MAX_COLUMNAS:
                columnas_validadas = True
            else:
                print(f"El número de columnas debe estar entre {TAMAÑO_MIN_COLUMNAS} y {TAMAÑO_MAX_COLUMNAS}.")
        except ValueError:
            print("Por favor, introduce un número válido.")

    return filas, columnas

def configurar_tablero():
    """
    Permite al usuario configurar el tamaño personalizado del tablero.

    Returns:
        list: Una matriz 2D que representa el tablero vacío
    """
    filas, columnas = obtener_dimensiones_tablero()
    return crear_tablero(filas, columnas)

def colocar_barco_individual(tablero, barco):
    """
    Coloca un barco individual en el tablero con validación.

    Args:
        tablero (list): El tablero donde colocar el barco
        barco (dict): Diccionario con información del barco

    Returns:
        bool: True si se colocó exitosamente, False en caso contrario
    """
    print(f"\nColocando {barco['nombre']} (longitud: {barco['longitud']})")

    # Solicitar coordenadas al usuario
    fila, columna = pedir_coordenadas(tablero)
    # Solicitar orientación (horizontal/vertical)
    orientacion = pedir_orientacion()

    try:
        # Importar función de colocar barco (para evitar importaciones circulares)
        from barcos import colocar_barco
        # Intentar colocar el barco en la posición especificada
        colocar_barco(tablero, fila, columna, barco["longitud"], orientacion, barco)
        mostrar_tablero(tablero)  # Mostrar tablero actualizado
        return True  # Colocado exitosamente
    except ValueError as e:  # Capturar errores de colocación
        print(f"Error: {e}. Inténtalo de nuevo.")  # Mostrar error y repetir
        return False

def colocar_flota_manual(tablero, flota):
    """
    Permite al jugador colocar manualmente todos los barcos de su flota.

    Args:
        tablero (list): El tablero donde colocar los barcos
        flota (list): Lista de diccionarios con información de los barcos
    """
    print("\nColocación manual de la flota:")
    mostrar_tablero(tablero)  # Mostrar el tablero vacío inicialmente

    # Iterar sobre cada tipo de barco en la flota
    for barco in flota:
        # Algunos barcos pueden tener cantidad > 1 (como acorazados)
        barcos_colocados = 0
        while barcos_colocados < barco["cantidad"]:
            if colocar_barco_individual(tablero, barco):
                barcos_colocados += 1

def obtener_opcion_colocacion():
    """
    Solicita y valida la opción de colocación de flota.

    Returns:
        bool: True si elige colocación manual, False si automática
    """
    print("\n¿Quieres colocar la flota manualmente o automáticamente?")
    print("1. Manual")      # Opción manual: usuario coloca barcos
    print("2. Automática")  # Opción automática: sistema coloca barcos aleatoriamente

    opcion_valida = False
    opcion = None

    while not opcion_valida:
        try:
            opcion = int(input("Selecciona una opción (1-2): "))
            if opcion in [1, 2]:
                opcion_valida = True
            else:
                print("Opción no válida. Elige 1 o 2.")
        except ValueError:
            print("Por favor, introduce un número válido.")

    return opcion == 1  # Devolver True para manual (opción 1), False para automática

def elegir_colocacion_flota():
    """
    Pregunta al usuario si quiere colocar la flota manualmente o automáticamente.

    Returns:
        bool: True si elige colocación manual, False si automática
    """
    return obtener_opcion_colocacion()

def procesar_turno_jugador(tablero_rival, flota_rival, tablero_propio, turno_numero):
    """
    Procesa el turno de un jugador humano.

    Args:
        tablero_rival (list): Tablero del oponente
        flota_rival (list): Flota del oponente
        tablero_propio (list): Tablero propio del jugador
        turno_numero (int): Número del turno actual

    Returns:
        bool: True si el juego continúa, False si terminó
    """
    print(f"\n--- TURNO {turno_numero}: TU TURNO ---")
    fila, columna = pedir_coordenadas(tablero_rival)  # Pedir coordenadas de disparo

    try:
        # Procesar el disparo del jugador contra la flota rival
        resultado = turno(tablero_rival, flota_rival, fila, columna)
        mostrar_resultado(f"Resultado: {resultado.upper()}")  # Mostrar resultado

        # Verificar si el rival ha perdido (todos sus barcos hundidos)
        if comprobar_fin(flota_rival):
            print("\n¡FELICIDADES! Has ganado la partida.")
            return False  # Juego terminado

    except ValueError as e:  # Capturar errores de disparo (coordenada inválida o repetida)
        print(f"Error: {e}. Pierdes el turno.")

    return True  # Juego continúa

def procesar_turno_cpu(tablero_jugador, flota_jugador, turno_numero):
    """
    Procesa el turno de la CPU.

    Args:
        tablero_jugador (list): Tablero del jugador humano
        flota_jugador (list): Flota del jugador humano
        turno_numero (int): Número del turno actual

    Returns:
        bool: True si el juego continúa, False si terminó
    """
    print(f"\n--- TURNO {turno_numero}: TURNO DE LA CPU ---")
    fila, columna = cpu_disparo(tablero_jugador)  # CPU elige coordenadas aleatorias

    try:
        # Procesar el disparo de la CPU contra la flota del jugador
        resultado = turno(tablero_jugador, flota_jugador, fila, columna)
        # Mostrar coordenadas y resultado del disparo de la CPU
        print(f"La CPU disparó a {chr(65 + fila)}{columna + 1} - Resultado: {resultado.upper()}")

        # Verificar si el jugador ha perdido
        if comprobar_fin(flota_jugador):
            print("\n¡HAS PERDIDO! La CPU ha ganado la partida.")
            return False  # Juego terminado

    except ValueError:
        # Esto no debería suceder con la CPU, pero se incluye por seguridad
        pass

    return True  # Juego continúa

def ejecutar_turnos_vs_cpu(tablero_jugador, tablero_cpu, flota_jugador, flota_cpu, turnos_maximos=100):
    """
    Ejecuta los turnos alternos del juego contra la CPU.

    Args:
        tablero_jugador (list): Tablero del jugador humano
        tablero_cpu (list): Tablero de la CPU
        flota_jugador (list): Flota del jugador humano
        flota_cpu (list): Flota de la CPU
        turnos_maximos (int): Número máximo de turnos para evitar bucles infinitos

    Returns:
        tuple: (ganador, turnos_totales) donde ganador es "Jugador", "CPU", o None si se alcanzó el límite
    """
    turno_actual = 1  # 1 = turno del jugador, 2 = turno de la CPU
    turnos_totales = 0

    # Ejecutar turnos hasta que alguien gane o se alcance el límite
    for turno_numero in range(1, turnos_maximos + 1):
        turnos_totales = turno_numero

        if turno_actual == 1:  # Turno del jugador humano
            if not procesar_turno_jugador(tablero_cpu, flota_cpu, tablero_jugador, turno_numero):
                guardar_partida("Jugador", "CPU", turnos_totales, "Jugador vs CPU")
                return "Jugador", turnos_totales

        else:  # Turno de la CPU
            if not procesar_turno_cpu(tablero_jugador, flota_jugador, turno_numero):
                guardar_partida("CPU", "Jugador", turnos_totales, "Jugador vs CPU")
                return "CPU", turnos_totales

        # Mostrar tableros actualizados después de ambos turnos
        print("\nTu tablero:")
        mostrar_tablero(tablero_jugador, ocultar_barcos=False)
        print("\nTablero del rival:")
        mostrar_tablero(tablero_cpu, ocultar_barcos=True)

        # Cambiar al siguiente turno (alternar entre 1 y 2)
        turno_actual = 2 if turno_actual == 1 else 1

    # Si se alcanzó el límite de turnos sin ganador
    print(f"\nSe alcanzó el límite de {turnos_maximos} turnos. Partida terminada en empate.")
    return None, turnos_totales

def juego_vs_cpu():
    """
    Implementa el modo de juego Jugador vs CPU.
    Gestiona la colocación de flotas, turnos alternos y verificación de fin de partida.
    """
    print("\n=== MODO: Jugador vs CPU ===")

    # Configuración de tableros para ambos jugadores
    tablero_jugador = configurar_tablero()  # Tablero del jugador humano
    tablero_cpu = copy.deepcopy(tablero_jugador)  # Tablero de la CPU (mismo tamaño)

    # Crear copias independientes de la flota para cada jugador
    flota_jugador = copy.deepcopy(FLOTA)  # Flota del jugador
    flota_cpu = copy.deepcopy(FLOTA)      # Flota de la CPU

    # Colocación de la flota del jugador
    if elegir_colocacion_flota():  # Si elige colocación manual
        colocar_flota_manual(tablero_jugador, flota_jugador)
    else:  # Si elige colocación automática
        colocar_flota_aleatoria(tablero_jugador, flota_jugador)

    # La CPU siempre coloca su flota automáticamente
    colocar_flota_aleatoria(tablero_cpu, flota_cpu)

    # Mostrar mensaje de inicio y tableros iniciales
    print("\n¡Comienza el juego!")
    print("Tu tablero:")
    mostrar_tablero(tablero_jugador, ocultar_barcos=False)  # Mostrar barcos del jugador
    print("\nTablero del rival:")
    mostrar_tablero(tablero_cpu, ocultar_barcos=True)      # Ocultar barcos de la CPU

    # Ejecutar los turnos del juego
    ejecutar_turnos_vs_cpu(tablero_jugador, tablero_cpu, flota_jugador, flota_cpu)

def procesar_turno_jugador_vs_jugador(tablero_rival, flota_rival, tablero_propio, turno_numero, numero_jugador):
    """
    Procesa el turno de un jugador en el modo jugador vs jugador.

    Args:
        tablero_rival (list): Tablero del oponente
        flota_rival (list): Flota del oponente
        tablero_propio (list): Tablero propio del jugador
        turno_numero (int): Número del turno actual
        numero_jugador (int): Número del jugador (1 o 2)

    Returns:
        bool: True si el juego continúa, False si terminó
    """
    print(f"\n--- TURNO {turno_numero}: JUGADOR {numero_jugador} ---")
    print("Tu tablero:")
    mostrar_tablero(tablero_propio, ocultar_barcos=False)  # Mostrar su propio tablero
    print("\nTablero del rival:")
    mostrar_tablero(tablero_rival, ocultar_barcos=True)   # Ocultar barcos del rival

    fila, columna = pedir_coordenadas(tablero_rival)  # Pedir disparo contra el rival

    try:
        resultado = turno(tablero_rival, flota_rival, fila, columna)
        mostrar_resultado(f"Resultado: {resultado.upper()}")

        if comprobar_fin(flota_rival):  # Verificar si el rival perdió
            print(f"\n¡FELICIDADES JUGADOR {numero_jugador}! Has ganado la partida.")
            return False  # Juego terminado

    except ValueError as e:
        print(f"Error: {e}. Pierdes el turno.")

    return True  # Juego continúa

def ejecutar_turnos_vs_jugador(tablero_j1, tablero_j2, flota_j1, flota_j2, turnos_maximos=100):
    """
    Ejecuta los turnos alternos del juego entre dos jugadores.

    Args:
        tablero_j1 (list): Tablero del Jugador 1
        tablero_j2 (list): Tablero del Jugador 2
        flota_j1 (list): Flota del Jugador 1
        flota_j2 (list): Flota del Jugador 2
        turnos_maximos (int): Número máximo de turnos para evitar bucles infinitos

    Returns:
        tuple: (ganador, turnos_totales) donde ganador es "Jugador 1", "Jugador 2", o None si se alcanzó el límite
    """
    turno_actual = 1  # 1 = Jugador 1, 2 = Jugador 2
    turnos_totales = 0

    # Ejecutar turnos hasta que alguien gane o se alcance el límite
    for turno_numero in range(1, turnos_maximos + 1):
        turnos_totales = turno_numero

        if turno_actual == 1:  # Turno del Jugador 1
            if not procesar_turno_jugador_vs_jugador(tablero_j2, flota_j2, tablero_j1, turno_numero, 1):
                guardar_partida("Jugador 1", "Jugador 2", turnos_totales, "Jugador vs Jugador")
                return "Jugador 1", turnos_totales

        else:  # Turno del Jugador 2
            if not procesar_turno_jugador_vs_jugador(tablero_j1, flota_j1, tablero_j2, turno_numero, 2):
                guardar_partida("Jugador 2", "Jugador 1", turnos_totales, "Jugador vs Jugador")
                return "Jugador 2", turnos_totales

        # Simular cambio de jugador entre turnos
        print("\n" * 50)  # "Limpiar" pantalla
        print("Pasa el turno al otro jugador...")

        # Cambiar turno
        turno_actual = 2 if turno_actual == 1 else 1

    # Si se alcanzó el límite de turnos sin ganador
    print(f"\nSe alcanzó el límite de {turnos_maximos} turnos. Partida terminada en empate.")
    return None, turnos_totales

def juego_vs_jugador():
    """
    Implementa el modo de juego Jugador vs Jugador.
    Gestiona turnos alternos entre dos jugadores humanos.
    """
    print("\n=== MODO: Jugador vs Jugador ===")

    # Configuración de tableros para ambos jugadores
    tablero_j1 = configurar_tablero()  # Tablero del Jugador 1
    tablero_j2 = copy.deepcopy(tablero_j1)  # Tablero del Jugador 2 (mismo tamaño)

    # Crear copias independientes de la flota para cada jugador
    flota_j1 = copy.deepcopy(FLOTA)  # Flota del Jugador 1
    flota_j2 = copy.deepcopy(FLOTA)  # Flota del Jugador 2

    # Colocación de flota del Jugador 1
    print("\n--- JUGADOR 1 ---")
    if elegir_colocacion_flota():
        colocar_flota_manual(tablero_j1, flota_j1)
    else:
        colocar_flota_aleatoria(tablero_j1, flota_j1)

    # Simular cambio de jugador (limpiar pantalla)
    print("\n" * 50)  # Imprimir muchas líneas para "limpiar" la pantalla
    print("Pasa el turno al Jugador 2...")

    # Colocación de flota del Jugador 2
    print("\n--- JUGADOR 2 ---")
    if elegir_colocacion_flota():
        colocar_flota_manual(tablero_j2, flota_j2)
    else:
        colocar_flota_aleatoria(tablero_j2, flota_j2)

    print("\n¡Comienza el juego!")

    # Ejecutar los turnos del juego
    ejecutar_turnos_vs_jugador(tablero_j1, tablero_j2, flota_j1, flota_j2)

def obtener_respuesta_continuar():
    """
    Pregunta al usuario si quiere continuar jugando y valida la respuesta.

    Returns:
        bool: True si quiere continuar, False si quiere terminar
    """
    respuesta_valida = False
    respuesta = ""

    while not respuesta_valida:
        respuesta = input("\n¿Quieres jugar otra partida? (s/n): ").lower()
        if respuesta in ['s', 'si', 'sí', 'y', 'yes']:  # Respuestas afirmativas
            respuesta_valida = True
            return True  # Quiere continuar
        elif respuesta in ['n', 'no']:  # Respuestas negativas
            respuesta_valida = True
            return False  # Quiere terminar
        else:
            print("Respuesta no válida. Responde 's' para sí o 'n' para no.")

def main():
    """
    Función principal que controla el flujo general del programa.
    Muestra el menú principal y permite jugar múltiples partidas.
    """
    continuar_jugando = True

    while continuar_jugando:  # Bucle controlado por flag
        modo = elegir_modo_juego()  # Mostrar menú y obtener modo de juego

        if modo == 1:      # Modo Jugador vs CPU
            juego_vs_cpu()
        elif modo == 2:    # Modo Jugador vs Jugador
            juego_vs_jugador()
        elif modo == 3:    # Ver ranking/estadísticas
            print("\n=== RANKING ===")
            mostrar_ranking()

        # Preguntar si el usuario quiere jugar otra partida
        continuar_jugando = obtener_respuesta_continuar()

    # Mensaje de despedida cuando el usuario decide terminar
    print("¡Gracias por jugar!")

# Punto de entrada del programa
# Esta condición asegura que main() solo se ejecute si el archivo se ejecuta directamente
if __name__ == "__main__":
    main()