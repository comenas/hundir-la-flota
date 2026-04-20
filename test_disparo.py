import pytest
from disparo import *
from tablero import crear_tablero

# comprobamos los dos resultados normales de un disparo válido:
# - que da "agua" cuando no hay barco
# - que da "tocado" cuando hay barco pero no lo hunde
# además comprobamos que el tablero se actualiza correctamente (FALLO o ACIERTO)
@pytest.mark.parametrize(
        "test_num, fila, columna, esperado",
        [
            (1, 0, 5, "agua"),   # disparamos al mar, no hay barco ahí
            (2, 0, 0, "tocado"), # disparamos al barco pero no lo hundimos (tiene 2 casillas)
        ]
)
def test_procesar_disparo_valido(test_num, fila, columna, esperado):
    tablero = crear_tablero(10, 10)
    flota = [{"nombre": "Patrullero", "longitud": 2, "impactos": 0,
              "hundido": False, "cantidad": 1, "coordenadas": [(0, 0), (0, 1)]}]
    tablero[0][0] = BARCO
    tablero[0][1] = BARCO
    sol = procesar_disparo(tablero, flota, fila, columna)
    assert sol == esperado
    if test_num == 1: assert tablero[fila][columna] == FALLO   # agua → marca como FALLO
    else: assert tablero[fila][columna] == ACIERTO             # tocado → marca como ACIERTO


# comprobamos que al hundir el último trozo de un barco devuelve "hundido"
# el patrullero tiene longitud 2, así que hacen falta exactamente 2 impactos
def test_procesar_disparo_hundido():
    tablero = crear_tablero(10, 10)
    flota = [{"nombre": "Patrullero", "longitud": 2, "impactos": 0,
              "hundido": False, "cantidad": 1, "coordenadas": [(0, 0), (0, 1)]}]
    tablero[0][0] = BARCO
    tablero[0][1] = BARCO
    procesar_disparo(tablero, flota, 0, 0)  # primer impacto: tocado
    sol = procesar_disparo(tablero, flota, 0, 1)  # segundo impacto: hundido
    assert sol == "hundido"


# comprobamos que procesar_disparo lanza ValueError en los dos casos inválidos:
# - coordenada fuera del tablero (12,12 en un tablero 10x10)
# - coordenada ya disparada antes (0,0 ya tiene ACIERTO del disparo anterior)
@pytest.mark.parametrize(
        "test_num, fila, columna",
        [
            (4, 12, 12),  # fuera del tablero, no existe esa casilla
            (5, 0, 0),    # ya disparamos aquí antes, no se puede repetir
        ]
)
def test_procesar_disparo_invalido(test_num, fila, columna):
    tablero = crear_tablero(10, 10)
    flota = [{"nombre": "Patrullero", "longitud": 2, "impactos": 0,
              "hundido": False, "cantidad": 1, "coordenadas": [(0, 0), (0, 1)]}]
    tablero[0][0] = BARCO
    tablero[0][1] = BARCO
    procesar_disparo(tablero, flota, 0, 0)  # disparamos (0,0) para que quede como ACIERTO
    with pytest.raises(ValueError):
        procesar_disparo(tablero, flota, fila, columna)