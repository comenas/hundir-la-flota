import copy
from Constantes import *
from tablero import crear_tablero, mostrar_tablero
from barcos import colocar_flota_aleatoria, colocar_flota_manual, crear_instancia_barco
from interfaz import pedir_coordenadas, pedir_orientacion, mostrar_resultado
from cpu import cpu_disparo
from juego import comprobar_fin, turno, barcos_a_flote
from ranking import guardar_partida, mostrar_ranking


# ─── MENÚ PRINCIPAL ───────────────────────────────────────────────────────────

def elegir_modo_juego():
    """Muestra el menú principal y devuelve la opción elegida (1-5)."""
    print("\n╔══════════════════════════════╗")
    print("║      HUNDIR LA FLOTA         ║")
    print("╠══════════════════════════════╣")
    print("║  1. Jugador vs CPU           ║")
    print("║  2. Jugador vs Jugador       ║")
    print("║  3. Modo Salvas              ║")
    print("║  4. Ver ranking              ║")
    print("║  5. Salir                    ║")
    print("╚══════════════════════════════╝")
    while True:
        try:
            opcion = int(input("Selecciona una opción (1-5): "))
            if opcion in [1, 2, 3, 4, 5]:
                return opcion
            print("Opción no válida. Elige entre 1 y 5.")
        except ValueError:
            print("Por favor, introduce un número.")


# ─── CONFIGURACIÓN DEL TABLERO ────────────────────────────────────────────────

def configurar_tablero():
    """Pide las dimensiones del tablero y lo crea.
    
    Returns:
        list: Tablero vacío de las dimensiones indicadas.
    """
    print(f"\nTablero ({TAMAÑO_MIN_FILAS}-{TAMAÑO_MAX_FILAS} filas, "
          f"{TAMAÑO_MIN_COLUMNAS}-{TAMAÑO_MAX_COLUMNAS} columnas).")
    print("Pulsa Enter para usar el tamaño por defecto (10x10).")

    def pedir_dimension(nombre, minimo, maximo, defecto):
        while True:
            entrada = input(f"  {nombre} [{defecto}]: ").strip()
            if entrada == "":
                return defecto
            try:
                valor = int(entrada)
                if minimo <= valor <= maximo:
                    return valor
                print(f"  Debe estar entre {minimo} y {maximo}.")
            except ValueError:
                print("  Introduce un número válido.")

    filas = pedir_dimension("Filas", TAMAÑO_MIN_FILAS, TAMAÑO_MAX_FILAS, TAMAÑO_DEFAULT_FILAS)
    columnas = pedir_dimension("Columnas", TAMAÑO_MIN_COLUMNAS, TAMAÑO_MAX_COLUMNAS, TAMAÑO_DEFAULT_COLUMNAS)
    return crear_tablero(filas, columnas)


# ─── PERSONALIZACIÓN DE FLOTA ─────────────────────────────────────────────────

CELDAS_FLOTA_ESTANDAR = sum(b["longitud"] * b["cantidad"] for b in FLOTA)
LONGITUD_MIN_BARCO = 2
LONGITUD_MAX_BARCO = 5


def personalizar_flota():
    """Permite al jugador modificar la composición de su flota.
    
    El total de celdas debe ser igual al de la flota estándar.
    Cada barco debe tener longitud entre 2 y 5.

    Returns:
        list: Lista de plantillas de barco personalizadas.
    """
    print(f"\nFlota estándar ({CELDAS_FLOTA_ESTANDAR} celdas en total):")
    for b in FLOTA:
        print(f"  {b['nombre']}: longitud {b['longitud']} × {b['cantidad']} = "
              f"{b['longitud'] * b['cantidad']} celdas")

    print(f"\nPuedes crear tu propia flota. Reglas:")
    print(f"  - Total de celdas: exactamente {CELDAS_FLOTA_ESTANDAR}")
    print(f"  - Longitud de cada barco: entre {LONGITUD_MIN_BARCO} y {LONGITUD_MAX_BARCO}")
    print(f"  - Mínimo 1 barco")

    flota_custom = []
    celdas_usadas = 0
    numero_barco = 1

    while celdas_usadas < CELDAS_FLOTA_ESTANDAR:
        restantes = CELDAS_FLOTA_ESTANDAR - celdas_usadas
        print(f"\n  Barco {numero_barco} — celdas restantes: {restantes}")

        # Longitud
        long_max = min(LONGITUD_MAX_BARCO, restantes)
        while True:
            try:
                longitud = int(input(f"  Longitud ({LONGITUD_MIN_BARCO}-{long_max}): "))
                if LONGITUD_MIN_BARCO <= longitud <= long_max:
                    break
                print(f"  Debe estar entre {LONGITUD_MIN_BARCO} y {long_max}.")
            except ValueError:
                print("  Introduce un número.")

        # Cantidad
        max_cantidad = restantes // longitud
        while True:
            try:
                cantidad = int(input(f"  Cantidad (1-{max_cantidad}): "))
                if 1 <= cantidad <= max_cantidad:
                    break
                print(f"  Debe estar entre 1 y {max_cantidad}.")
            except ValueError:
                print("  Introduce un número.")

        nombre = input(f"  Nombre del barco [Barco {numero_barco}]: ").strip()
        if not nombre:
            nombre = f"Barco {numero_barco}"

        flota_custom.append({
            "nombre": nombre,
            "longitud": longitud,
            "cantidad": cantidad
        })
        celdas_usadas += longitud * cantidad
        numero_barco += 1

        if celdas_usadas == CELDAS_FLOTA_ESTANDAR:
            break

    print(f"\nFlota personalizada creada con {len(flota_custom)} tipo(s) de barco.")
    return flota_custom


def elegir_flota():
    """Pregunta si usar la flota estándar o personalizar.
    
    Returns:
        list: Plantillas de barco a usar.
    """
    print("\n¿Qué flota quieres usar?")
    print("  1. Flota estándar")
    print("  2. Personalizar flota")
    while True:
        try:
            opcion = int(input("Selecciona (1-2): "))
            if opcion == 1:
                return copy.deepcopy(FLOTA)
            if opcion == 2:
                return personalizar_flota()
            print("Elige 1 o 2.")
        except ValueError:
            print("Introduce un número.")


# ─── COLOCACIÓN DE FLOTA ──────────────────────────────────────────────────────

def elegir_colocacion(tablero, plantillas):
    """Pregunta al jugador si coloca la flota manual o automáticamente.
    
    Returns:
        list: Flota activa (instancias colocadas).
    """
    print("\n¿Cómo quieres colocar tu flota?")
    print("  1. Manual")
    print("  2. Automática")
    while True:
        try:
            opcion = int(input("Selecciona (1-2): "))
            if opcion == 1:
                return colocar_flota_manual(
                    tablero, plantillas,
                    pedir_coordenadas, pedir_orientacion,
                    lambda t: mostrar_tablero(t, ocultar_barcos=False)
                )
            if opcion == 2:
                return colocar_flota_aleatoria(tablero, plantillas)
            print("Elige 1 o 2.")
        except ValueError:
            print("Introduce un número.")


# ─── TURNOS JUGADOR ───────────────────────────────────────────────────────────

def mostrar_estado(tablero_propio, tablero_rival):
    print("\nTu tablero:")
    mostrar_tablero(tablero_propio, ocultar_barcos=False)
    print("\nTablero rival:")
    mostrar_tablero(tablero_rival, ocultar_barcos=True)


def procesar_disparo_jugador(tablero_rival, flota_rival, nombre_jugador, num_disparo=None):
    """Pide coordenadas y procesa un disparo del jugador.
    
    Args:
        num_disparo: Si no es None, se muestra "Disparo X/Y" (modo Salvas).
    
    Returns:
        str: Resultado del disparo ('agua', 'tocado', 'hundido').
        None: Si la coordenada ya fue disparada (se pierde el disparo).
    """
    if num_disparo:
        print(f"  Disparo {num_disparo}:")
    try:
        fila, columna = pedir_coordenadas(tablero_rival)
        resultado = turno(tablero_rival, flota_rival, fila, columna)
        mostrar_resultado(f"  → {resultado.upper()}")
        return resultado
    except ValueError as e:
        print(f"  Error: {e}. Pierdes este disparo.")
        return None


def procesar_disparo_cpu(tablero_jugador, flota_jugador, num_disparo=None):
    """La CPU elige y procesa un disparo.
    
    Returns:
        str: Resultado del disparo.
    """
    if num_disparo:
        print(f"  Disparo CPU {num_disparo}:")
    fila, columna = cpu_disparo(tablero_jugador)
    resultado = turno(tablero_jugador, flota_jugador, fila, columna)
    print(f"  CPU disparó a {chr(65 + fila)}{columna + 1} → {resultado.upper()}")
    return resultado


# ─── MODOS DE JUEGO ───────────────────────────────────────────────────────────

def juego_vs_cpu():
    """Modo Jugador vs CPU — un disparo por turno."""
    print("\n═══ JUGADOR VS CPU ═══")
    tablero_jugador = configurar_tablero()
    tablero_cpu = copy.deepcopy(tablero_jugador)
    plantillas = elegir_flota()

    print("\n--- Tu flota ---")
    flota_jugador = elegir_colocacion(tablero_jugador, copy.deepcopy(plantillas))
    flota_cpu = colocar_flota_aleatoria(tablero_cpu, copy.deepcopy(plantillas))

    mostrar_estado(tablero_jugador, tablero_cpu)
    turno_actual = 1
    turnos = 0

    while True:
        turnos += 1
        if turno_actual == 1:
            print(f"\n--- TURNO {turnos}: TU TURNO ---")
            procesar_disparo_jugador(tablero_cpu, flota_cpu, "Jugador")
            if comprobar_fin(flota_cpu):
                print("\n¡GANASTE! Has hundido toda la flota enemiga.")
                guardar_partida("Jugador", "CPU", turnos, "Jugador vs CPU")
                break
        else:
            print(f"\n--- TURNO {turnos}: CPU ---")
            procesar_disparo_cpu(tablero_jugador, flota_jugador)
            if comprobar_fin(flota_jugador):
                print("\n¡HAS PERDIDO! La CPU ha hundido tu flota.")
                guardar_partida("CPU", "Jugador", turnos, "Jugador vs CPU")
                break

        mostrar_estado(tablero_jugador, tablero_cpu)
        turno_actual = 2 if turno_actual == 1 else 1


def juego_vs_jugador():
    """Modo Jugador vs Jugador — un disparo por turno."""
    print("\n═══ JUGADOR VS JUGADOR ═══")
    tablero_j1 = configurar_tablero()
    tablero_j2 = copy.deepcopy(tablero_j1)
    plantillas = elegir_flota()

    print("\n--- JUGADOR 1: coloca tu flota ---")
    flota_j1 = elegir_colocacion(tablero_j1, copy.deepcopy(plantillas))
    print("\n" * 50 + "Pasa el turno al Jugador 2...")

    print("\n--- JUGADOR 2: coloca tu flota ---")
    flota_j2 = elegir_colocacion(tablero_j2, copy.deepcopy(plantillas))

    turno_actual = 1
    turnos = 0

    while True:
        turnos += 1
        j = turno_actual
        tablero_rival = tablero_j2 if j == 1 else tablero_j1
        flota_rival = flota_j2 if j == 1 else flota_j1
        tablero_propio = tablero_j1 if j == 1 else tablero_j2

        print(f"\n--- TURNO {turnos}: JUGADOR {j} ---")
        mostrar_estado(tablero_propio, tablero_rival)
        procesar_disparo_jugador(tablero_rival, flota_rival, f"Jugador {j}")

        if comprobar_fin(flota_rival):
            print(f"\n¡JUGADOR {j} GANA! Ha hundido toda la flota rival.")
            guardar_partida(f"Jugador {j}", f"Jugador {3 - j}", turnos, "Jugador vs Jugador")
            break

        print("\n" * 50 + f"Pasa el turno al Jugador {3 - j}...")
        turno_actual = 2 if turno_actual == 1 else 1


def juego_salvas(modo="PvCPU"):
    """Modo Salvas — cada jugador dispara tantas veces como barcos tenga a flote.
    
    Args:
        modo: 'PvCPU' o 'PvP'.
    """
    print(f"\n═══ MODO SALVAS — {'Jugador vs CPU' if modo == 'PvCPU' else 'Jugador vs Jugador'} ═══")
    print("Regla: disparas tantas veces por turno como barcos te queden a flote.\n")

    tablero_j1 = configurar_tablero()
    tablero_j2 = copy.deepcopy(tablero_j1)
    plantillas = elegir_flota()

    print("\n--- JUGADOR 1: coloca tu flota ---")
    flota_j1 = elegir_colocacion(tablero_j1, copy.deepcopy(plantillas))

    if modo == "PvP":
        print("\n" * 50 + "Pasa el turno al Jugador 2...")
        print("\n--- JUGADOR 2: coloca tu flota ---")
        flota_j2 = elegir_colocacion(tablero_j2, copy.deepcopy(plantillas))
    else:
        flota_j2 = colocar_flota_aleatoria(tablero_j2, copy.deepcopy(plantillas))

    turno_actual = 1
    turnos = 0

    while True:
        turnos += 1

        if turno_actual == 1:
            disparos = barcos_a_flote(flota_j1)
            print(f"\n--- TURNO {turnos}: JUGADOR 1 — {disparos} disparo(s) ---")
            mostrar_estado(tablero_j1, tablero_j2)
            for i in range(disparos):
                procesar_disparo_jugador(tablero_j2, flota_j2, "Jugador 1", num_disparo=f"{i+1}/{disparos}")
                if comprobar_fin(flota_j2):
                    print("\n¡JUGADOR 1 GANA!")
                    guardar_partida("Jugador 1", "Jugador 2" if modo == "PvP" else "CPU",
                                    turnos, f"Salvas {modo}")
                    return
        else:
            flota_atacante = flota_j2
            tablero_objetivo = tablero_j1
            flota_objetivo = flota_j1
            disparos = barcos_a_flote(flota_atacante)

            if modo == "PvP":
                print(f"\n--- TURNO {turnos}: JUGADOR 2 — {disparos} disparo(s) ---")
                print("\n" * 50 + "Pasa el turno al Jugador 2...")
                mostrar_estado(tablero_j2, tablero_j1)
                for i in range(disparos):
                    procesar_disparo_jugador(tablero_objetivo, flota_objetivo,
                                             "Jugador 2", num_disparo=f"{i+1}/{disparos}")
                    if comprobar_fin(flota_objetivo):
                        print("\n¡JUGADOR 2 GANA!")
                        guardar_partida("Jugador 2", "Jugador 1", turnos, "Salvas PvP")
                        return
            else:
                print(f"\n--- TURNO {turnos}: CPU — {disparos} disparo(s) ---")
                for i in range(disparos):
                    procesar_disparo_cpu(tablero_objetivo, flota_objetivo,
                                         num_disparo=f"{i+1}/{disparos}")
                    if comprobar_fin(flota_objetivo):
                        print("\n¡HAS PERDIDO! La CPU ha hundido tu flota.")
                        guardar_partida("CPU", "Jugador 1", turnos, "Salvas PvCPU")
                        return

            mostrar_estado(tablero_j1, tablero_j2)

        turno_actual = 2 if turno_actual == 1 else 1


def elegir_modo_salvas():
    """Pregunta si el modo Salvas es vs CPU o vs Jugador."""
    print("\nModo Salvas:")
    print("  1. Jugador vs CPU")
    print("  2. Jugador vs Jugador")
    while True:
        try:
            opcion = int(input("Selecciona (1-2): "))
            if opcion == 1:
                return "PvCPU"
            if opcion == 2:
                return "PvP"
            print("Elige 1 o 2.")
        except ValueError:
            print("Introduce un número.")


# ─── BUCLE PRINCIPAL ──────────────────────────────────────────────────────────

def main():
    """Punto de entrada del programa."""
    while True:
        opcion = elegir_modo_juego()

        if opcion == 1:
            juego_vs_cpu()
        elif opcion == 2:
            juego_vs_jugador()
        elif opcion == 3:
            modo = elegir_modo_salvas()
            juego_salvas(modo)
        elif opcion == 4:
            print("\n═══ RANKING ═══")
            mostrar_ranking()
        elif opcion == 5:
            print("\n¡Hasta la próxima!")
            break

        entrada = input("\n¿Jugar otra partida? (s/n): ").strip().lower()
        if entrada not in ["s", "si", "sí", "y", "yes"]:
            print("\n¡Hasta la próxima!")
            break


if __name__ == "__main__":
    main()