import pytest
from cpu import cpu_disparo
from tablero import crear_tablero
from Constantes import ACIERTO, FALLO, AGUA


# comprobamos que la CPU devuelve coordenadas que existen dentro del tablero
# es el test más básico: que no dispare fuera del mapa
def test_cpu_disparo_devuelve_coordenadas_validas():
    tablero = crear_tablero(10, 10)
    fila, columna = cpu_disparo(tablero)
    assert 0 <= fila < 10     # fila dentro del rango
    assert 0 <= columna < 10  # columna dentro del rango


# comprobamos que la CPU NO repite un disparo donde ya acertó antes
# llenamos todo el tablero de ACIERTOs y dejamos solo (2,2) libre
# la CPU tiene que encontrar esa única casilla libre sí o sí
def test_cpu_disparo_no_repite_acierto():
    tablero = crear_tablero(5, 5)
    for f in range(5):
        for c in range(5):
            tablero[f][c] = ACIERTO
    tablero[2][2] = AGUA  # única casilla libre
    fila, columna = cpu_disparo(tablero)
    assert fila == 2
    assert columna == 2


# igual que el anterior pero con FALLOs en lugar de ACIERTOs
# la CPU tampoco puede repetir donde ya falló
def test_cpu_disparo_no_repite_fallo():
    tablero = crear_tablero(5, 5)
    for f in range(5):
        for c in range(5):
            tablero[f][c] = FALLO
    tablero[0][0] = AGUA  # única casilla libre
    fila, columna = cpu_disparo(tablero)
    assert fila == 0
    assert columna == 0


# comprobamos que la casilla elegida por la CPU está libre (no es ACIERTO ni FALLO)
# test general con tablero vacío, simplemente que no dispara a algo ya usado
def test_cpu_disparo_casilla_libre():
    tablero = crear_tablero(10, 10)
    fila, columna = cpu_disparo(tablero)
    assert tablero[fila][columna] not in [ACIERTO, FALLO]


# caso extremo: el tablero casi lleno, solo queda una casilla libre en la esquina
# comprueba que la CPU la encuentra aunque tenga que intentarlo muchas veces
def test_cpu_disparo_tablero_casi_lleno():
    tablero = crear_tablero(5, 5)
    for f in range(5):
        for c in range(5):
            tablero[f][c] = FALLO
    tablero[4][4] = AGUA  # última casilla libre del tablero
    fila, columna = cpu_disparo(tablero)
    assert (fila, columna) == (4, 4)