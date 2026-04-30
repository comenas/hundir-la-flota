import pytest
from barcos import saber_posicion_valida, colocar_barco, colocar_flota_aleatoria
from tablero import crear_tablero
import Constantes as c
from Constantes import BARCO, AGUA


# fixture que crea un tablero 10x10 limpio para cada test que lo necesite
# así no tenemos que escribir crear_tablero(10,10) en cada test
@pytest.fixture
def tablero():
    return crear_tablero(10, 10)


# --- Tests para saber_posicion_valida ---

# comprobamos que devuelve True cuando la posición SÍ es válida
# probamos distintas combinaciones de fila, columna, longitud y orientación que entran bien
@pytest.mark.parametrize(
    "test_num, fila, columna, longitud, orientacion",
    [
        ("test1", 0, 0, 5, "h"),  # barco de 5 horizontal desde la esquina, cabe justo
        ("test2", 0, 0, 2, "v"),  # barco de 2 vertical desde la esquina, fácil
        ("test3", 3, 2, 4, "h"),  # barco de 4 horizontal en el centro, cabe
        ("test4", 1, 5, 3, "v"),  # barco de 3 vertical a mitad tablero, cabe
    ])
def test_saber_posicion_valida_True(test_num, tablero, fila, columna, longitud, orientacion):
    assert saber_posicion_valida(tablero, fila, columna, longitud, orientacion) == True


# comprobamos que devuelve False cuando el barco SE SALE del tablero
# todos estos casos el barco empieza dentro pero termina fuera
@pytest.mark.parametrize(
    "test_num, fila, columna, longitud, orientacion",
    [
        ("test5", 2, 6, 5, "h"),  # columna 6 + longitud 5 = llega a columna 10, que no existe
        ("test6", 9, 0, 2, "v"),  # fila 9 + longitud 2 = llega a fila 10, que no existe
        ("test7", 1, 8, 4, "h"),  # columna 8 + longitud 4 = se pasa
        ("test8", 8, 1, 3, "v"),  # fila 8 + longitud 3 = llega a fila 10, fuera
    ])
def test_saber_posicion_valida_False(test_num, tablero, fila, columna, longitud, orientacion):
    assert saber_posicion_valida(tablero, fila, columna, longitud, orientacion) == False


# comprobamos que no se puede colocar un barco donde ya hay otro
# ponemos un barco en (0,0)(0,1)(0,2) e intentamos colocar otro que pise (0,2)
def test_saber_posicion_valida_solapamiento(tablero):
    tablero[0][0] = c.BARCO
    tablero[0][1] = c.BARCO
    tablero[0][2] = c.BARCO
    assert saber_posicion_valida(tablero, 0, 2, 4, "h") == False  # empieza en una casilla ocupada


# --- Tests para colocar_barco ---

# comprobamos que un barco horizontal ocupa las casillas correctas después de colocarse
def test_colocar_barcos_horizontal(tablero):
    colocar_barco(tablero, 0, 0, 2, "h", c.FLOTA[0])
    assert tablero[0][0] == c.BARCO  # primera casilla ocupada
    assert tablero[0][1] == c.BARCO  # segunda casilla ocupada


# comprobamos que un barco vertical ocupa las casillas correctas
def test_colocar_barcos_vertical(tablero):
    colocar_barco(tablero, 0, 0, 2, "v", c.FLOTA[0])
    assert tablero[0][0] == c.BARCO  # primera casilla
    assert tablero[1][0] == c.BARCO  # avanza por filas, no por columnas


# comprobamos que lanza ValueError si el barco se sale del tablero
# un barco de longitud 5 empezando en columna 8 no cabe en horizontal
def test_colocar_barco_posicion_invalida():
    tablero = crear_tablero(10, 10)
    with pytest.raises(ValueError):
        colocar_barco(tablero, 0, 8, 5, "h", c.FLOTA[0])


# comprobamos que lanza ValueError si un barco solapa con otro ya colocado
# ponemos el primero en (0,0)(0,1)(0,2) e intentamos colocar el segundo pisando (0,2)
def test_colocar_barco_solapamiento():
    tablero = crear_tablero(10, 10)
    barco1 = {"nombre": "A", "longitud": 3, "impactos": 0, "hundido": False, "cantidad": 1}
    barco2 = {"nombre": "B", "longitud": 3, "impactos": 0, "hundido": False, "cantidad": 1}
    colocar_barco(tablero, 0, 0, 3, "h", barco1)
    with pytest.raises(ValueError):
        colocar_barco(tablero, 0, 2, 3, "v", barco2)  # empieza en (0,2) que ya está ocupado


# comprobamos que las coordenadas guardadas en el diccionario del barco son correctas (horizontal)
# esto es crítico para que procesar_disparo sepa qué barco impactamos
def test_colocar_barco_guarda_coordenadas_horizontal():
    tablero = crear_tablero(10, 10)
    barco = {"nombre": "Test", "longitud": 3, "impactos": 0, "hundido": False, "cantidad": 1}
    colocar_barco(tablero, 2, 3, 3, "h", barco)
    assert barco["coordenadas"] == [(2, 3), (2, 4), (2, 5)]  # misma fila, columnas consecutivas


# lo mismo pero para orientación vertical
def test_colocar_barco_guarda_coordenadas_vertical():
    tablero = crear_tablero(10, 10)
    barco = {"nombre": "Test", "longitud": 3, "impactos": 0, "hundido": False, "cantidad": 1}
    colocar_barco(tablero, 1, 4, 3, "v", barco)
    assert barco["coordenadas"] == [(1, 4), (2, 4), (3, 4)]  # misma columna, filas consecutivas


# comprobamos que al volver a colocar un barco las coordenadas anteriores se borran
# sin esto si mueves un barco se quedarían las coordenadas viejas y el juego se rompería
def test_colocar_barco_resetea_coordenadas_anteriores():
    tablero = crear_tablero(10, 10)
    barco = {"nombre": "Test", "longitud": 2, "impactos": 0, "hundido": False,
             "cantidad": 1, "coordenadas": [(9, 9), (9, 8)]}  # coordenadas antiguas
    colocar_barco(tablero, 0, 0, 2, "h", barco)
    assert (9, 9) not in barco["coordenadas"]       # las viejas se fueron
    assert barco["coordenadas"] == [(0, 0), (0, 1)] # las nuevas son las correctas


# --- Tests para colocar_flota_aleatoria ---

# comprobamos que el total de casillas BARCO en el tablero coincide con la suma de longitudes
# si hay más o menos casillas es que algo se solapó o no se colocó bien
def test_colocar_flota_aleatoria():
    import copy
    flota = copy.deepcopy(c.FLOTA)
    tablero = crear_tablero(10, 10)
    total_esperado = sum(b["longitud"] * b["cantidad"] for b in flota)
    colocar_flota_aleatoria(tablero, flota)
    total_real = sum(1 for fila in tablero for casilla in fila if casilla == BARCO)
    assert total_real == total_esperado


# este test comprueba lo mismo pero el enfoque es detectar solapamientos
# si dos barcos se solaparan el total de casillas BARCO sería menor que el esperado
def test_colocar_flota_aleatoria_sin_solapamientos():
    import copy
    flota = copy.deepcopy(c.FLOTA)
    tablero = crear_tablero(10, 10)
    colocar_flota_aleatoria(tablero, flota)
    total_esperado = sum(b["longitud"] * b["cantidad"] for b in c.FLOTA)
    total_real = sum(1 for fila in tablero for casilla in fila if casilla == BARCO)
    assert total_real == total_esperado


# comprobamos que todos los barcos tienen coordenadas asignadas después de colocarlos
# y que la cantidad de coordenadas coincide con su longitud
def test_colocar_flota_aleatoria_coordenadas_asignadas():
    import copy
    flota = copy.deepcopy(c.FLOTA)
    tablero = crear_tablero(10, 10)
    flota_activa = colocar_flota_aleatoria(tablero, flota)
    for barco in flota_activa:
        assert "coordenadas" in barco                    # tiene la clave coordenadas
        assert len(barco["coordenadas"]) == barco["longitud"]  # y tiene las que le tocan