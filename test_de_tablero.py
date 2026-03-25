import pytest
from tablero import *

 #este parametrize testea los valores válidos de la tabla
@pytest.mark.parametrize(
    "test_num, filas, columnas",
    [
        ("Test1",10,10),
        ("Test2",5,5),
        ("Test3",15,15),
        ("Test4",5,15),
        ("Test5",15,5),    
    ])
def test_crear_tablero(test_num,filas,columnas):
    tablero = crear_tablero(filas,columnas)
    assert len(tablero) == filas
    assert len(tablero[0]) == columnas
    
#esto testea los valores incorrectos
@pytest.mark.parametrize(
    "test_num, filas, columnas",
    [
        ("Test6",20,10),
        ("Test7",4,10),
        ("Test8",10,20),
        ("Test9",10,4),
        ("Test10",4,4),
        ("Test11",10,-10),
        ("Test12",-7,10)
    ])
def test_crear_tablero_dimensiones_malas(test_num,filas,columnas): 
    with pytest.raises(ValueError):
        crear_tablero(filas, columnas)
        
#los 12 tests han pasado :D
#test para coordenadas validas True
@pytest.mark.parametrize( 
    "test_num,tablero, fila, columna",
    [
        ("Test13",crear_tablero(10,10),9,9), #recordatorio van del 0 al 9
        ("Test14",crear_tablero(10,10),4,9), #cada vez que miro se me olvida
        ("Test15",crear_tablero(10,10),0,0), #y pienso que está mal
        ("Test16",crear_tablero(10,10),9,0),
        ("Test17",crear_tablero(10,10),0,9),
        ("Test18",crear_tablero(10,10),5,5),
    ])
def test_saber_coordenadas_validas_true(test_num,tablero,fila,columna):
    assert saber_coordenada_valida(tablero, fila, columna) == True
#test para coordenadas validas False
@pytest.mark.parametrize( 
    "test_num,tablero, fila, columna",
    [
        ("Test19",crear_tablero(10,10),-9,9), #recordatorio van del 0 al 9
        ("Test20",crear_tablero(10,10),4,10), #cada vez que miro se me olvida
        ("Test21",crear_tablero(10,10),0,-1), #y pienso que está mal
        ("Test22",crear_tablero(10,10),10,0),
        ("Test23",crear_tablero(10,10),0,10),
        ("Test24",crear_tablero(10,10),-5,5)
    ])
def test_saber_coordenadas_validas_false(test_num,tablero,fila,columna):
    assert saber_coordenada_valida(tablero, fila, columna) == False
#hasta aquí los tests de tablero creo
#si pongo AGUA * columnas * filas en crear tablero hay un bug
def test_filas_independientes():
    tablero = crear_tablero(5, 5)
    tablero[0][0] = ACIERTO
    assert tablero[1][0] == AGUA
#este test asegura que no vuelva a pasar
#porque al cambiar una coordenada
#antes se cambiaban otras, así aseguramos que son independientes
#pero ahora si hasta aquí los tests
    
    
    