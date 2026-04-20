from cpu import *
from tablero import crear_tablero

def test_cpu_no_repite(monkeypatch):
    tablero = crear_tablero(10, 10)
    # llenar casi todo el tablero
    for i in range(10):
        for j in range(9):
            tablero[i][j] = ACIERTO
    # solo queda (0,9) libre
    fila, columna = cpu_disparo(tablero)
    assert fila == 0
    assert columna == 9

def test_cpu_coordenada_valida():
    tablero = crear_tablero(10, 10)
    fila, columna = cpu_disparo(tablero)
    assert 0 <= fila < 10
    assert 0 <= columna < 10