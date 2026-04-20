import pytest
from barcos import *
from tablero import crear_tablero
import Constantes as c


@pytest.fixture
def tablero():
    return crear_tablero(10, 10)


# ─── saber_posicion_valida ────────────────────────────────────────────────────

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
    tablero[0][0] = c.BARCO
    tablero[0][1] = c.BARCO
    tablero[0][2] = c.BARCO
    assert saber_posicion_valida(tablero, 0, 2, 4, "h") == False


# ─── colocar_barco ────────────────────────────────────────────────────────────

def test_colocar_barcos_horizontal(tablero):
    barco = crear_instancia_barco(c.FLOTA[0])
    colocar_barco(tablero, 0, 0, 2, "h", barco)
    assert tablero[0][0] == c.BARCO
    assert tablero[0][1] == c.BARCO


def test_colocar_barcos_vertical(tablero):
    barco = crear_instancia_barco(c.FLOTA[0])
    colocar_barco(tablero, 0, 0, 2, "v", barco)
    assert tablero[0][0] == c.BARCO
    assert tablero[1][0] == c.BARCO


def test_colocar_barco_guarda_coordenadas(tablero):
    barco = crear_instancia_barco(c.FLOTA[0])
    colocar_barco(tablero, 0, 0, 3, "h", barco)
    assert barco["coordenadas"] == [(0, 0), (0, 1), (0, 2)]


def test_colocar_barco_posicion_invalida():
    tablero = crear_tablero(10, 10)
    barco = crear_instancia_barco(c.FLOTA[0])
    with pytest.raises(ValueError):
        colocar_barco(tablero, 0, 8, 5, "h", barco)


def test_colocar_barco_solapamiento():
    tablero = crear_tablero(10, 10)
    barco1 = crear_instancia_barco(c.FLOTA[0])
    barco2 = crear_instancia_barco(c.FLOTA[0])
    colocar_barco(tablero, 0, 0, 3, "h", barco1)
    with pytest.raises(ValueError):
        colocar_barco(tablero, 0, 2, 3, "v", barco2)


# ─── crear_instancia_barco ────────────────────────────────────────────────────

def test_crear_instancia_barco_independiente():
    """Dos instancias del mismo tipo no deben compartir coordenadas."""
    instancia1 = crear_instancia_barco(c.FLOTA[1])  # Acorazado
    instancia2 = crear_instancia_barco(c.FLOTA[1])
    instancia1["coordenadas"].append((0, 0))
    assert instancia2["coordenadas"] == []


def test_crear_instancia_barco_campos():
    plantilla = c.FLOTA[0]  # Portaaviones
    instancia = crear_instancia_barco(plantilla)
    assert instancia["nombre"] == plantilla["nombre"]
    assert instancia["longitud"] == plantilla["longitud"]
    assert instancia["impactos"] == 0
    assert instancia["hundido"] == False
    assert instancia["coordenadas"] == []


# ─── colocar_flota_aleatoria ──────────────────────────────────────────────────

def test_colocar_flota_aleatoria_celdas_correctas():
    """El número de celdas BARCO debe coincidir con el total esperado de la flota."""
    tablero = crear_tablero(10, 10)
    total_esperado = sum(b["longitud"] * b["cantidad"] for b in c.FLOTA)
    colocar_flota_aleatoria(tablero, c.FLOTA)
    total_real = sum(casilla == c.BARCO for fila in tablero for casilla in fila)
    assert total_real == total_esperado


def test_colocar_flota_aleatoria_instancias_independientes():
    """Cada barco de la flota activa debe tener sus propias coordenadas."""
    tablero = crear_tablero(10, 10)
    flota_activa = colocar_flota_aleatoria(tablero, c.FLOTA)
    coords_totales = [coord for barco in flota_activa for coord in barco["coordenadas"]]
    # No debe haber coordenadas duplicadas entre barcos distintos
    assert len(coords_totales) == len(set(coords_totales))


def test_colocar_flota_aleatoria_numero_instancias():
    """El número de instancias debe ser la suma de todas las cantidades."""
    tablero = crear_tablero(10, 10)
    flota_activa = colocar_flota_aleatoria(tablero, c.FLOTA)
    total_esperado = sum(b["cantidad"] for b in c.FLOTA)
    assert len(flota_activa) == total_esperado


def test_colocar_flota_aleatoria_acorazados_independientes():
    """Los 2 acorazados deben tener coordenadas distintas entre sí."""
    tablero = crear_tablero(10, 10)
    flota_activa = colocar_flota_aleatoria(tablero, c.FLOTA)
    acorazados = [b for b in flota_activa if b["nombre"] == "Acorazado"]
    assert len(acorazados) == 2
    assert acorazados[0]["coordenadas"] != acorazados[1]["coordenadas"]


def test_colocar_flota_personalizada():
    """Permite flotas con cantidades personalizadas."""
    tablero = crear_tablero(10, 10)
    flota_custom = [
        {"nombre": "Patrullero", "longitud": 2, "cantidad": 3},
        {"nombre": "Destructor", "longitud": 3, "cantidad": 2},
    ]
    flota_activa = colocar_flota_aleatoria(tablero, flota_custom)
    assert len(flota_activa) == 5
    patrulleros = [b for b in flota_activa if b["nombre"] == "Patrullero"]
    assert len(patrulleros) == 3