import pytest
from disparo import *
from tablero import crear_tablero
@pytest.mark.parametrize(
        "test_num,fila,columna,esperado",
        [
            (1,0,5,"agua"),
            (2,0,0,"tocado"),
        ]

)
def test_procesar_disparo_valido(test_num,fila,columna,esperado):
    tablero = crear_tablero(10, 10)
    flota = [{"nombre": "Patrullero", "longitud": 2, "impactos": 0, 
          "hundido": False, "cantidad": 1, "coordenadas": [(0,0), (0,1)]}]
    tablero[0][0] = BARCO
    tablero[0][1] = BARCO
    sol = procesar_disparo(tablero,flota,fila,columna)
    assert sol == esperado
    if test_num == 1: assert tablero[fila][columna] == FALLO
    else: assert tablero[fila][columna] == ACIERTO

def test_procesar_disparo_hundido():
    tablero = crear_tablero(10, 10)
    flota = [{"nombre": "Patrullero", "longitud": 2, "impactos": 0,
              "hundido": False, "cantidad": 1, "coordenadas": [(0,0), (0,1)]}]
    tablero[0][0] = BARCO
    tablero[0][1] = BARCO
    procesar_disparo(tablero, flota, 0, 0)  # primer impacto
    sol = procesar_disparo(tablero, flota, 0, 1)  # segundo impacto
    assert sol == "hundido"

@pytest.mark.parametrize(
        "test_num,fila,columna",
        [
            (4,12,12),
            (5,0,0),
        ]

)

def test_procesar_disparo_invalido(test_num,fila,columna):
    tablero = crear_tablero(10, 10)
    flota = [{"nombre": "Patrullero", "longitud": 2, "impactos": 0,
              "hundido": False, "cantidad": 1, "coordenadas": [(0,0), (0,1)]}]
    tablero[0][0] = BARCO
    tablero[0][1] = BARCO
    procesar_disparo(tablero,flota,0,0)
    with pytest.raises(ValueError):
        procesar_disparo(tablero,flota,fila,columna)