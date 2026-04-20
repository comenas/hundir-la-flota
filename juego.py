from barcos import colocar_flota_aleatoria
from disparo import procesar_disparo


def iniciar_partida(tablero1, tablero2, plantillas1, plantillas2):
    """Coloca las flotas de ambos jugadores aleatoriamente.
    
    Returns:
        tuple: (flota_activa1, flota_activa2) listas planas de instancias de barco.
    """
    flota1 = colocar_flota_aleatoria(tablero1, plantillas1)
    flota2 = colocar_flota_aleatoria(tablero2, plantillas2)
    return flota1, flota2


def comprobar_fin(flota):
    """Devuelve True si todos los barcos de la flota están hundidos."""
    return all(barco["hundido"] for barco in flota)


def turno(tablero, flota, fila, columna):
    """Procesa un disparo y devuelve el resultado ('agua', 'tocado', 'hundido')."""
    return procesar_disparo(tablero, flota, fila, columna)


def barcos_a_flote(flota):
    """Devuelve el número de barcos que aún no están hundidos.
    
    En el modo Salvas, este número determina cuántos disparos tiene el jugador.
    """
    return sum(1 for barco in flota if not barco["hundido"])


def jugar_partida(tablero1, tablero2, flota1, flota2, obtener_coordenadas):
    """Ejecuta una partida estándar (un disparo por turno).

    Args:
        tablero1, tablero2: Tableros de cada jugador.
        flota1, flota2: Flotas activas de cada jugador.
        obtener_coordenadas: Función callable que devuelve (fila, columna).

    Returns:
        int: 1 si gana el jugador 1, 2 si gana el jugador 2.
    """
    turno_actual = 1
    while True:
        if turno_actual == 1:
            fila, columna = obtener_coordenadas()
            turno(tablero2, flota2, fila, columna)
            if comprobar_fin(flota2):
                return 1
            turno_actual = 2
        else:
            fila, columna = obtener_coordenadas()
            turno(tablero1, flota1, fila, columna)
            if comprobar_fin(flota1):
                return 2
            turno_actual = 1


def jugar_partida_salvas(tablero1, tablero2, flota1, flota2, obtener_coordenadas):
    """Ejecuta una partida en modo Salvas.
    
    Cada jugador dispara tantas veces por turno como barcos tenga a flote.

    Args:
        tablero1, tablero2: Tableros de cada jugador.
        flota1, flota2: Flotas activas de cada jugador.
        obtener_coordenadas: Función callable que devuelve (fila, columna).
            Recibe como argumento el número de disparo actual del turno.

    Returns:
        int: 1 si gana el jugador 1, 2 si gana el jugador 2.
    """
    turno_actual = 1
    while True:
        if turno_actual == 1:
            disparos = barcos_a_flote(flota1)
            for i in range(disparos):
                fila, columna = obtener_coordenadas(i + 1)
                try:
                    turno(tablero2, flota2, fila, columna)
                except ValueError:
                    pass  # coordenada repetida: se pierde ese disparo
                if comprobar_fin(flota2):
                    return 1
            turno_actual = 2
        else:
            disparos = barcos_a_flote(flota2)
            for i in range(disparos):
                fila, columna = obtener_coordenadas(i + 1)
                try:
                    turno(tablero1, flota1, fila, columna)
                except ValueError:
                    pass
                if comprobar_fin(flota1):
                    return 2
            turno_actual = 1