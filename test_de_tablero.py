import pytest
from tablero import *

# comprobamos que crear_tablero funciona con valores válidos
# básicamente que el tablero tenga el tamaño que pedimos y no nos mienta
@pytest.mark.parametrize(
    "test_num, filas, columnas",
    [
        ("Test1", 10, 10),  # tamaño por defecto, el más normal
        ("Test2", 5, 5),    # mínimo permitido, borde inferior
        ("Test3", 15, 15),  # máximo permitido, borde superior
        ("Test4", 5, 15),   # mínimo de filas con máximo de columnas
        ("Test5", 15, 5),   # máximo de filas con mínimo de columnas
    ])
def test_crear_tablero(test_num, filas, columnas):
    tablero = crear_tablero(filas, columnas)
    assert len(tablero) == filas       # que tenga las filas que pedimos
    assert len(tablero[0]) == columnas # que tenga las columnas que pedimos


# comprobamos que crear_tablero explota (ValueError) cuando le pasamos valores incorrectos
# esto es importante para que el juego no se rompa si alguien mete un 99x99
@pytest.mark.parametrize(
    "test_num, filas, columnas",
    [
        ("Test6", 20, 10),   # demasiadas filas
        ("Test7", 4, 10),    # muy pocas filas
        ("Test8", 10, 20),   # demasiadas columnas
        ("Test9", 10, 4),    # muy pocas columnas
        ("Test10", 4, 4),    # demasiado pequeño por los dos lados
        ("Test11", 10, -10), # columnas negativas, no existe eso
        ("Test12", -7, 10)   # filas negativas, tampoco
    ])
def test_crear_tablero_dimensiones_malas(test_num, filas, columnas):
    with pytest.raises(ValueError):
        crear_tablero(filas, columnas)


# comprobamos que saber_coordenada_valida devuelve True cuando la coordenada SÍ está en el tablero
# recordatorio: el tablero va del 0 al 9, no del 1 al 10 (esto nos confundió mil veces)
@pytest.mark.parametrize(
    "test_num, tablero, fila, columna",
    [
        ("Test13", crear_tablero(10, 10), 9, 9),  # esquina inferior derecha, límite máximo
        ("Test14", crear_tablero(10, 10), 4, 9),  # borde derecho a mitad de altura
        ("Test15", crear_tablero(10, 10), 0, 0),  # esquina superior izquierda, límite mínimo
        ("Test16", crear_tablero(10, 10), 9, 0),  # esquina inferior izquierda
        ("Test17", crear_tablero(10, 10), 0, 9),  # esquina superior derecha
        ("Test18", crear_tablero(10, 10), 5, 5),  # centro del tablero, caso tranquilo
    ])
def test_saber_coordenadas_validas_true(test_num, tablero, fila, columna):
    assert saber_coordenada_valida(tablero, fila, columna) == True


# comprobamos que saber_coordenada_valida devuelve False cuando la coordenada está FUERA
# los negativos y los que se pasan del rango tienen que fallar sí o sí
@pytest.mark.parametrize(
    "test_num, tablero, fila, columna",
    [
        ("Test19", crear_tablero(10, 10), -9, 9),   # fila negativa
        ("Test20", crear_tablero(10, 10), 4, 10),   # columna 10 en tablero de 0-9: se pasa por uno
        ("Test21", crear_tablero(10, 10), 0, -1),   # columna negativa
        ("Test22", crear_tablero(10, 10), 10, 0),   # fila 10 en tablero de 0-9: se pasa por uno
        ("Test23", crear_tablero(10, 10), 0, 10),   # columna 10 otra vez, por si acaso
        ("Test24", crear_tablero(10, 10), -5, 5)    # fila negativa en el centro
    ])
def test_saber_coordenadas_validas_false(test_num, tablero, fila, columna):
    assert saber_coordenada_valida(tablero, fila, columna) == False


# este test es especial: comprueba que las filas del tablero son independientes entre sí
# hubo un bug donde al cambiar una casilla se cambiaban otras filas también
# (pasaba por usar AGUA * columnas * filas en lugar de list comprehension)
# este test existe para que ese bug no vuelva jamás
def test_filas_independientes():
    tablero = crear_tablero(5, 5)
    tablero[0][0] = ACIERTO        # cambiamos una casilla de la fila 0
    assert tablero[1][0] == AGUA   # la fila 1 no debe haberse enterado de nada