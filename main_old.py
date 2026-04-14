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

def elegir_modo_juego():
    """
    Función que muestra el menú principal y permite al usuario elegir el modo de juego.

    Returns:
        int: El modo seleccionado (1: vs CPU, 2: vs Jugador, 3: Ver ranking)
    """
    print("Bienvenido a Hundir la Flota!")  # Mensaje de bienvenida
    print("Elige el modo de juego:")
    print("1. Jugador vs CPU")      # Opción 1: jugar contra la computadora
    print("2. Jugador vs Jugador")  # Opción 2: jugar contra otro jugador
    print("3. Ver ranking")         # Opción 3: ver estadísticas de partidas anteriores

    # Bucle para validar la entrada del usuario
    while True:
        try:
            opcion = int(input("Selecciona una opción (1-3): "))  # Solicitar opción numérica
            if opcion in [1, 2, 3]:  # Verificar que sea una opción válida
                return opcion  # Devolver la opción seleccionada
            else:
                print("Opción no válida. Elige 1, 2 o 3.")  # Mensaje de error
        except ValueError:  # Capturar errores de conversión a int
            print("Por favor, introduce un número válido.")  # Mensaje de error

def configurar_tablero():
    """
    Permite al usuario configurar el tamaño personalizado del tablero.

    Returns:
        list: Una matriz 2D que representa el tablero vacío
    """
    print("\nConfiguración del tablero:")
    # Bucle para validar las dimensiones del tablero
    while True:
        try:
            # Solicitar número de filas con límites definidos en constantes
            filas = int(input(f"Número de filas ({TAMAÑO_MIN_FILAS}-{TAMAÑO_MAX_FILAS}): "))
            # Solicitar número de columnas con límites definidos en constantes
            columnas = int(input(f"Número de columnas ({TAMAÑO_MIN_COLUMNAS}-{TAMAÑO_MAX_COLUMNAS}): "))
            # Intentar crear el tablero con las dimensiones especificadas
            tablero = crear_tablero(filas, columnas)
            return tablero  # Devolver el tablero creado
        except ValueError as e:  # Capturar errores de validación de dimensiones
            print(f"Error: {e}. Inténtalo de nuevo.")  # Mostrar mensaje de error

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
        for i in range(barco["cantidad"]):
            colocado = False  # Bandera para controlar si el barco se colocó correctamente
            while not colocado:  # Bucle hasta que se coloque correctamente
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
                    colocado = True  # Marcar como colocado exitosamente
                except ValueError as e:  # Capturar errores de colocación
                    print(f"Error: {e}. Inténtalo de nuevo.")  # Mostrar error y repetir

def elegir_colocacion_flota():
    """
    Pregunta al usuario si quiere colocar la flota manualmente o automáticamente.

    Returns:
        bool: True si elige colocación manual, False si automática
    """
    while True:
        print("\n¿Quieres colocar la flota manualmente o automáticamente?")
        print("1. Manual")      # Opción manual: usuario coloca barcos
        print("2. Automática")  # Opción automática: sistema coloca barcos aleatoriamente
        try:
            opcion = int(input("Selecciona una opción (1-2): "))
            if opcion in [1, 2]:
                return opcion == 1  # Devolver True para manual (opción 1), False para automática
            else:
                print("Opción no válida. Elige 1 o 2.")
        except ValueError:
            print("Por favor, introduce un número válido.")

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

    turno_actual = 1  # 1 = turno del jugador, 2 = turno de la CPU
    turnos_totales = 0  # Contador de turnos para estadísticas

    # Bucle principal del juego
    while True:
        turnos_totales += 1  # Incrementar contador de turnos

        if turno_actual == 1:  # Turno del jugador humano
            print(f"\n--- TURNO {turnos_totales}: TU TURNO ---")
            fila, columna = pedir_coordenadas(tablero_cpu)  # Pedir coordenadas de disparo

            try:
                # Procesar el disparo del jugador contra la flota de la CPU
                resultado = turno(tablero_cpu, flota_cpu, fila, columna)
                mostrar_resultado(f"Resultado: {resultado.upper()}")  # Mostrar resultado

                # Verificar si la CPU ha perdido (todos sus barcos hundidos)
                if comprobar_fin(flota_cpu):
                    print("\n¡FELICIDADES! Has ganado la partida.")
                    # Guardar resultado en el ranking
                    guardar_partida("Jugador", "CPU", turnos_totales, "Jugador vs CPU")
                    return  # Terminar la función

            except ValueError as e:  # Capturar errores de disparo (coordenada inválida o repetida)
                print(f"Error: {e}. Pierdes el turno.")
                continue  # Saltar al siguiente turno sin cambiar

        else:  # Turno de la CPU
            print(f"\n--- TURNO {turnos_totales}: TURNO DE LA CPU ---")
            fila, columna = cpu_disparo(tablero_jugador)  # CPU elige coordenadas aleatorias

            try:
                # Procesar el disparo de la CPU contra la flota del jugador
                resultado = turno(tablero_jugador, flota_jugador, fila, columna)
                # Mostrar coordenadas y resultado del disparo de la CPU
                print(f"La CPU disparó a {chr(65 + fila)}{columna + 1} - Resultado: {resultado.upper()}")

                # Verificar si el jugador ha perdido
                if comprobar_fin(flota_jugador):
                    print("\n¡HAS PERDIDO! La CPU ha ganado la partida.")
                    # Guardar resultado en el ranking
                    guardar_partida("CPU", "Jugador", turnos_totales, "Jugador vs CPU")
                    return  # Terminar la función

            except ValueError:
                # Esto no debería suceder con la CPU, pero se incluye por seguridad
                continue

        # Mostrar tableros actualizados después de ambos turnos
        print("\nTu tablero:")
        mostrar_tablero(tablero_jugador, ocultar_barcos=False)
        print("\nTablero del rival:")
        mostrar_tablero(tablero_cpu, ocultar_barcos=True)

        # Cambiar al siguiente turno (alternar entre 1 y 2)
        turno_actual = 2 if turno_actual == 1 else 1

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
    turno_actual = 1  # 1 = Jugador 1, 2 = Jugador 2
    turnos_totales = 0  # Contador de turnos

    # Bucle principal del juego
    while True:
        turnos_totales += 1

        if turno_actual == 1:  # Turno del Jugador 1
            print(f"\n--- TURNO {turnos_totales}: JUGADOR 1 ---")
            print("Tu tablero:")
            mostrar_tablero(tablero_j1, ocultar_barcos=False)  # Mostrar su propio tablero
            print("\nTablero del rival:")
            mostrar_tablero(tablero_j2, ocultar_barcos=True)   # Ocultar barcos del rival

            fila, columna = pedir_coordenadas(tablero_j2)  # Pedir disparo contra Jugador 2

            try:
                resultado = turno(tablero_j2, flota_j2, fila, columna)
                mostrar_resultado(f"Resultado: {resultado.upper()}")

                if comprobar_fin(flota_j2):  # Verificar si Jugador 2 perdió
                    print("\n¡FELICIDADES JUGADOR 1! Has ganado la partida.")
                    guardar_partida("Jugador 1", "Jugador 2", turnos_totales, "Jugador vs Jugador")
                    return

            except ValueError as e:
                print(f"Error: {e}. Pierdes el turno.")
                continue

        else:  # Turno del Jugador 2
            print(f"\n--- TURNO {turnos_totales}: JUGADOR 2 ---")
            print("Tu tablero:")
            mostrar_tablero(tablero_j2, ocultar_barcos=False)  # Mostrar su propio tablero
            print("\nTablero del rival:")
            mostrar_tablero(tablero_j1, ocultar_barcos=True)   # Ocultar barcos del rival

            fila, columna = pedir_coordenadas(tablero_j1)  # Pedir disparo contra Jugador 1

            try:
                resultado = turno(tablero_j1, flota_j1, fila, columna)
                mostrar_resultado(f"Resultado: {resultado.upper()}")

                if comprobar_fin(flota_j1):  # Verificar si Jugador 1 perdió
                    print("\n¡FELICIDADES JUGADOR 2! Has ganado la partida.")
                    guardar_partida("Jugador 2", "Jugador 1", turnos_totales, "Jugador vs Jugador")
                    return

            except ValueError as e:
                print(f"Error: {e}. Pierdes el turno.")
                continue

        # Simular cambio de jugador entre turnos
        print("\n" * 50)  # "Limpiar" pantalla
        print("Pasa el turno al otro jugador...")

        # Cambiar turno
        turno_actual = 2 if turno_actual == 1 else 1

def main():
    """
    Función principal que controla el flujo general del programa.
    Muestra el menú principal y permite jugar múltiples partidas.
    """
    while True:  # Bucle infinito para permitir múltiples partidas
        modo = elegir_modo_juego()  # Mostrar menú y obtener modo de juego

        if modo == 1:      # Modo Jugador vs CPU
            juego_vs_cpu()
        elif modo == 2:    # Modo Jugador vs Jugador
            juego_vs_jugador()
        elif modo == 3:    # Ver ranking/estadísticas
            print("\n=== RANKING ===")
            mostrar_ranking()

        # Preguntar si el usuario quiere jugar otra partida
        while True:
            respuesta = input("\n¿Quieres jugar otra partida? (s/n): ").lower()
            if respuesta in ['s', 'si', 'sí', 'y', 'yes']:  # Respuestas afirmativas
                break  # Salir del bucle interno y comenzar nueva partida
            elif respuesta in ['n', 'no']:  # Respuestas negativas
                print("¡Gracias por jugar!")  # Mensaje de despedida
                return  # Terminar el programa
            else:
                print("Respuesta no válida. Responde 's' para sí o 'n' para no.")

# Punto de entrada del programa
# Esta condición asegura que main() solo se ejecute si el archivo se ejecuta directamente
if __name__ == "__main__":
    main()
