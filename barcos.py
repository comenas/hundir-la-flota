import random
from Constantes import *
from tablero import saber_coordenada_valida


def saber_posicion_valida(tablero, fila, columna, longitud, orientacion):
    for i in range(longitud):
        if orientacion == "h":
            fila_actual = fila
            columna_actual = columna + i
        else:
            fila_actual = fila + i
            columna_actual = columna
        if not saber_coordenada_valida(tablero, fila_actual, columna_actual):
            return False
        if tablero[fila_actual][columna_actual] != AGUA:
            return False
    return True


def colocar_barco(tablero, fila, columna, longitud, orientacion, barco):
    """Coloca un barco en el tablero y guarda sus coordenadas en el dict del barco."""
    if not saber_posicion_valida(tablero, fila, columna, longitud, orientacion):
        raise ValueError("Posición del barco no válida")
    barco["coordenadas"] = []
    for i in range(longitud):
        if orientacion == "h":
            fila_actual = fila
            columna_actual = columna + i
        else:
            fila_actual = fila + i
            columna_actual = columna
        tablero[fila_actual][columna_actual] = BARCO
        barco["coordenadas"].append((fila_actual, columna_actual))


def crear_instancia_barco(plantilla):
    """Crea un diccionario independiente para un barco individual a partir de su plantilla.
    
    Esto permite tener varios barcos del mismo tipo (ej: 2 acorazados)
    sin que compartan el mismo dict y se sobreescriban las coordenadas.
    
    Args:
        plantilla (dict): Diccionario de la FLOTA con nombre, longitud y cantidad.
    
    Returns:
        dict: Nueva instancia independiente del barco, lista para colocar.
    """
    return {
        "nombre": plantilla["nombre"],
        "longitud": plantilla["longitud"],
        "impactos": 0,
        "hundido": False,
        "coordenadas": []
    }


def colocar_flota_aleatoria(tablero, plantillas):
    """Coloca todos los barcos de la flota en posiciones aleatorias válidas.

    Para cada tipo de barco en plantillas, crea tantas instancias independientes
    como indique su campo 'cantidad', y las coloca en el tablero sin solapamientos.

    Args:
        tablero (list): Tablero donde colocar los barcos.
        plantillas (list): Lista de dicts con nombre, longitud y cantidad de cada tipo.

    Returns:
        list: Lista plana de instancias de barco ya colocadas (una por barco real).
              Ejemplo: si hay 2 acorazados, aparecen 2 dicts independientes en la lista.
    """
    n_filas = len(tablero) - 1
    n_columnas = len(tablero[0]) - 1
    flota_activa = []

    for plantilla in plantillas:
        for _ in range(plantilla["cantidad"]):
            instancia = crear_instancia_barco(plantilla)
            colocado = False
            while not colocado:
                fila = random.randint(0, n_filas)
                columna = random.randint(0, n_columnas)
                orientacion = random.choice(["h", "v"])
                try:
                    colocar_barco(tablero, fila, columna, plantilla["longitud"], orientacion, instancia)
                    colocado = True
                except ValueError:
                    pass
            flota_activa.append(instancia)

    return flota_activa


def colocar_flota_manual(tablero, plantillas, pedir_coordenadas_fn, pedir_orientacion_fn, mostrar_tablero_fn):
    """Coloca todos los barcos de la flota pidiendo coordenadas al jugador.

    Args:
        tablero (list): Tablero donde colocar los barcos.
        plantillas (list): Lista de dicts con nombre, longitud y cantidad de cada tipo.
        pedir_coordenadas_fn: Función que devuelve (fila, columna).
        pedir_orientacion_fn: Función que devuelve 'h' o 'v'.
        mostrar_tablero_fn: Función para mostrar el tablero tras cada colocación.

    Returns:
        list: Lista plana de instancias de barco ya colocadas.
    """
    flota_activa = []
    mostrar_tablero_fn(tablero)

    for plantilla in plantillas:
        for i in range(plantilla["cantidad"]):
            numero = f" ({i+1}/{plantilla['cantidad']})" if plantilla["cantidad"] > 1 else ""
            print(f"\nColocando {plantilla['nombre']}{numero} — longitud {plantilla['longitud']}")
            instancia = crear_instancia_barco(plantilla)
            colocado = False
            while not colocado:
                fila, columna = pedir_coordenadas_fn(tablero)
                orientacion = pedir_orientacion_fn()
                try:
                    colocar_barco(tablero, fila, columna, plantilla["longitud"], orientacion, instancia)
                    mostrar_tablero_fn(tablero)
                    colocado = True
                except ValueError as e:
                    print(f"Error: {e}. Inténtalo de nuevo.")
            flota_activa.append(instancia)

    return flota_activa