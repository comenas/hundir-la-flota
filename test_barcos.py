import pytest
from barcos import *
from tablero import crear_tablero
from Constantes import BARCO
@pytest.fixture
def tablero():
    return crear_tablero(10, 10)
@pytest.mark.parametrize(
    "test_num, fila, columna, longitud,orientacion", #teniendo en cuenta que la longitud es 5,4,3 o 2
        [
            ("test1", 0,0,5,"h"),
            ("test2", 0,0,2,"v"),
            ("test3", 3,2,4,"h"),
            ("test4", 1,5,3,"v"),
            
         ])

def test_saber_posicion_valida_True(test_num,tablero,fila,columna,longitud,orientacion):
    sol = saber_posicion_valida(tablero,fila,columna,longitud,orientacion)
    assert sol == True
    
@pytest.mark.parametrize(
    "test_num, fila, columna, longitud,orientacion", #teniendo en cuenta que la longitud es 5,4,3 o 2
        [
            ("test5", 2,6,5,"h"),
            ("test6", 9,0,2,"v"),
            ("test7", 1,8,4,"h"),
            ("test8", 8,1,3,"v"),
            
         ])

def test_saber_posicion_valida_False(test_num,tablero,fila,columna,longitud,orientacion):
    sol = saber_posicion_valida(tablero,fila,columna,longitud,orientacion)
    assert sol == False
#es siguiente es de hecho el más importante porque se puede romper todo
def test_saber_posicion_valida_solapamiento(tablero):
    #colocamos barcos de prueba
    tablero[0][0] = BARCO
    tablero[0][1] = BARCO
    tablero[0][2] = BARCO
    # en el test se intenta colocar otro que pasa por encima
    sol = saber_posicion_valida(tablero,0,2,4,"h")
    assert sol == False
    
def test_colocar_barcos_horizontal(tablero): #test colocando un barco en horizontal
    colocar_barco(tablero,0,0,2,"h")
    assert tablero[0][0] == BARCO
    assert tablero[0][1] == BARCO
def test_colocar_barcos_vertical(tablero): #test colocando un barco en vertical
    colocar_barco(tablero,0,0,2,"v")
    assert tablero[0][0] == BARCO
    assert tablero[1][0] == BARCO
def test_colocar_barco_posicion_invalida(): #test colocar barco en una posicion no válida
    tablero = crear_tablero(10, 10)
    with pytest.raises(ValueError):
        colocar_barco(tablero, 0, 8, 5, "h")  # se sale del tablero

def test_colocar_barco_solapamiento(): #test donde se coloca un barco con la funcion
    tablero = crear_tablero(10, 10)
    colocar_barco(tablero, 0, 0, 3, "h") #y luego se intenta colocar otro por encima con la misma funcion
    with pytest.raises(ValueError):
        colocar_barco(tablero, 0, 2, 3, "v")  # solapa con el anterior
    