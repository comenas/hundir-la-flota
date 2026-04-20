import pytest
from barcos import saber_posicion_valida, colocar_barco, colocar_flota_aleatoria
from tablero import crear_tablero
import Constantes as c
from Constantes import BARCO, AGUA


@pytest.fixture
def tablero():
    return crear_tablero(10, 10)


# --- Tests para saber_posicion_valida ---

@pytest.mark.parametrize(
    "test_num, fila, columna, longitud, orientacion",
    [
        ("test1", 0, 0, 5, "h"),
        ("test2", 0, 0, 2, "v"),
        ("test3", 3, 2, 4, "h"),
        ("test4", 1, 5, 3, "v"),
    ])
def test_saber_posicion_valida_True(test_num, tablero, fila, columna, longitud, orientacion):
    assert saber_posicion_valida(tablero, fila, columna, longitud, orientacion) == True


@pytest.mark.parametrize(
    "test_num, fila, columna, longitud, orientacion",
    [
        ("test5", 2, 6, 5, "h"),
        ("test6", 9, 0, 2, "v"),
        ("test7", 1, 8, 4, "h"),
        ("test8", 8, 1, 3, "v"),
    ])
def test_saber_posicion_valida_False(test_num, tablero, fila, columna, longitud, orientacion):
    assert saber_posicion_valida(tablero, fila, columna, longitud, orientacion) == False


def test_saber_posicion_valida_solapamiento(tablero):
    """No se puede colocar un barco donde ya hay otro."""
    tablero[0][0] = c.BARCO
    tablero[0][1] = c.BARCO
    tablero[0][2] = c.BARCO
    assert saber_posicion_valida(tablero, 0, 2, 4, "h") == False


# --- Tests para colocar_barco ---

def test_colocar_barcos_horizontal(tablero):
    """Barco horizontal ocupa las casillas correctas."""
    colocar_barco(tablero, 0, 0, 2, "h", c.FLOTA[0])
    assert tablero[0][0] == c.BARCO
    assert tablero[0][1] == c.BARCO


def test_colocar_barcos_vertical(tablero):
    """Barco vertical ocupa las casillas correctas."""
    colocar_barco(tablero, 0, 0, 2, "v", c.FLOTA[0])
    assert tablero[0][0] == c.BARCO
    assert tablero[1][0] == c.BARCO


def test_colocar_barco_posicion_invalida():
    """Lanza ValueError si el barco se sale del tablero."""
    tablero = crear_tablero(10, 10)
    with pytest.raises(ValueError):
        colocar_barco(tablero, 0, 8, 5, "h", c.FLOTA[0])


def test_colocar_barco_solapamiento():
    """Lanza ValueError si el barco solapa con otro existente."""
    tablero = crear_tablero(10, 10)
    barco1 = {"nombre": "A", "longitud": 3, "impactos": 0, "hundido": False, "cantidad": 1}
    barco2 = {"nombre": "B", "longitud": 3, "impactos": 0, "hundido": False, "cantidad": 1}
    colocar_barco(tablero, 0, 0, 3, "h", barco1)
    with pytest.raises(ValueError):
        colocar_barco(tablero, 0, 2, 3, "v", barco2)


def test_colocar_barco_guarda_coordenadas_horizontal():
    """colocar_barco() guarda las coordenadas correctas en el dict del barco (horizontal)."""
    tablero = crear_tablero(10, 10)
    barco = {"nombre": "Test", "longitud": 3, "impactos": 0, "hundido": False, "cantidad": 1}
    colocar_barco(tablero, 2, 3, 3, "h", barco)
    assert barco["coordenadas"] == [(2, 3), (2, 4), (2, 5)]


def test_colocar_barco_guarda_coordenadas_vertical():
    """colocar_barco() guarda las coordenadas correctas en el dict del barco (vertical)."""
    tablero = crear_tablero(10, 10)
    barco = {"nombre": "Test", "longitud": 3, "impactos": 0, "hundido": False, "cantidad": 1}
    colocar_barco(tablero, 1, 4, 3, "v", barco)
    assert barco["coordenadas"] == [(1, 4), (2, 4), (3, 4)]


def test_colocar_barco_resetea_coordenadas_anteriores():
    """Al volver a colocar un barco, las coordenadas previas se borran."""
    tablero = crear_tablero(10, 10)
    barco = {"nombre": "Test", "longitud": 2, "impactos": 0, "hundido": False,
             "cantidad": 1, "coordenadas": [(9, 9), (9, 8)]}
    colocar_barco(tablero, 0, 0, 2, "h", barco)
    assert (9, 9) not in barco["coordenadas"]
    assert barco["coordenadas"] == [(0, 0), (0, 1)]


# --- Tests para colocar_flota_aleatoria ---

def test_colocar_flota_aleatoria():
    """El total de casillas BARCO coincide con la suma de longitudes de la flota."""
    import copy
    flota = copy.deepcopy(c.FLOTA)
    tablero = crear_tablero(10, 10)
    total_esperado = sum(b["longitud"] * b["cantidad"] for b in flota)
    colocar_flota_aleatoria(tablero, flota)
    total_real = sum(1 for fila in tablero for casilla in fila if casilla == BARCO)
    assert total_real == total_esperado


def test_colocar_flota_aleatoria_sin_solapamientos():
    """Ningún barco se solapa con otro tras la colocación aleatoria."""
    import copy
    flota = copy.deepcopy(c.FLOTA)
    tablero = crear_tablero(10, 10)
    colocar_flota_aleatoria(tablero, flota)
    # Verificar contando: si no hay solapamiento, el total de BARCOs debe ser exacto
    total_esperado = sum(b["longitud"] * b["cantidad"] for b in c.FLOTA)
    total_real = sum(1 for fila in tablero for casilla in fila if casilla == BARCO)
    assert total_real == total_esperado


def test_colocar_flota_aleatoria_coordenadas_asignadas():
    """Todos los barcos tienen coordenadas asignadas tras la colocación."""
    import copy
    flota = copy.deepcopy(c.FLOTA)
    tablero = crear_tablero(10, 10)
    colocar_flota_aleatoria(tablero, flota)
    for barco in flota:
        assert "coordenadas" in barco
        assert len(barco["coordenadas"]) == barco["longitud"]