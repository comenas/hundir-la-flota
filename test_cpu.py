import pytest
from cpu import cpu_disparo
from tablero import crear_tablero
from Constantes import ACIERTO, FALLO, AGUA


# --- Tests para cpu_disparo ---

def test_cpu_disparo_devuelve_coordenadas_validas():
    """El disparo de la CPU debe devolver coordenadas dentro del tablero."""
    tablero = crear_tablero(10, 10)
    fila, columna = cpu_disparo(tablero)
    assert 0 <= fila < 10
    assert 0 <= columna < 10


def test_cpu_disparo_no_repite_acierto():
    """La CPU no debe disparar a una casilla marcada como ACIERTO."""
    tablero = crear_tablero(5, 5)
    # Marcar todas las casillas como ACIERTO excepto (2,2)
    for f in range(5):
        for c in range(5):
            tablero[f][c] = ACIERTO
    tablero[2][2] = AGUA  # única casilla libre
    fila, columna = cpu_disparo(tablero)
    assert fila == 2
    assert columna == 2


def test_cpu_disparo_no_repite_fallo():
    """La CPU no debe disparar a una casilla marcada como FALLO."""
    tablero = crear_tablero(5, 5)
    # Marcar todas como FALLO excepto (0,0)
    for f in range(5):
        for c in range(5):
            tablero[f][c] = FALLO
    tablero[0][0] = AGUA  # única casilla libre
    fila, columna = cpu_disparo(tablero)
    assert fila == 0
    assert columna == 0


def test_cpu_disparo_casilla_libre():
    """La casilla elegida por la CPU debe estar libre (no ser ACIERTO ni FALLO)."""
    tablero = crear_tablero(10, 10)
    fila, columna = cpu_disparo(tablero)
    assert tablero[fila][columna] not in [ACIERTO, FALLO]


def test_cpu_disparo_tablero_casi_lleno():
    """La CPU encuentra la última casilla libre aunque casi todo esté disparado."""
    tablero = crear_tablero(5, 5)
    for f in range(5):
        for c in range(5):
            tablero[f][c] = FALLO
    tablero[4][4] = AGUA  # última libre
    fila, columna = cpu_disparo(tablero)
    assert (fila, columna) == (4, 4)