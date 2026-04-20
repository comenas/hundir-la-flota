import pytest
from tablero import crear_tablero
from juego import comprobar_fin, turno, iniciar_partida, jugar_partida
from Constantes import BARCO, AGUA, ACIERTO, FALLO


# --- Tests para comprobar_fin ---

def test_comprobar_fin_vivo():
    """No termina si hay al menos un barco no hundido."""
    flota = [
        {"nombre": "Portaaviones", "longitud": 5, "impactos": 0, "hundido": True,  "cantidad": 1},
        {"nombre": "Acorazado",    "longitud": 4, "impactos": 0, "hundido": True,  "cantidad": 2},
        {"nombre": "Destructor",   "longitud": 3, "impactos": 0, "hundido": True,  "cantidad": 1},
        {"nombre": "Submarino",    "longitud": 3, "impactos": 0, "hundido": True,  "cantidad": 1},
        {"nombre": "Patrullero",   "longitud": 2, "impactos": 0, "hundido": False, "cantidad": 1},
    ]
    assert comprobar_fin(flota) == False


def test_comprobar_fin_muertos():
    """Termina cuando todos los barcos están hundidos."""
    flota = [
        {"nombre": "Portaaviones", "longitud": 5, "impactos": 0, "hundido": True, "cantidad": 1},
        {"nombre": "Acorazado",    "longitud": 4, "impactos": 0, "hundido": True, "cantidad": 2},
        {"nombre": "Destructor",   "longitud": 3, "impactos": 0, "hundido": True, "cantidad": 1},
        {"nombre": "Submarino",    "longitud": 3, "impactos": 0, "hundido": True, "cantidad": 1},
        {"nombre": "Patrullero",   "longitud": 2, "impactos": 0, "hundido": True, "cantidad": 1},
    ]
    assert comprobar_fin(flota) == True


def test_comprobar_fin_flota_vacia():
    """Una flota vacía se considera terminada (all() sobre lista vacía = True)."""
    assert comprobar_fin([]) == True


def test_comprobar_fin_solo_un_barco_vivo():
    """Con un solo barco no hundido la partida sigue."""
    flota = [{"nombre": "Patrullero", "longitud": 2, "impactos": 0, "hundido": False, "cantidad": 1}]
    assert comprobar_fin(flota) == False


def test_comprobar_fin_solo_un_barco_hundido():
    """Con un solo barco hundido la partida termina."""
    flota = [{"nombre": "Patrullero", "longitud": 2, "impactos": 2, "hundido": True, "cantidad": 1}]
    assert comprobar_fin(flota) == True


# --- Tests para turno ---

def test_turno_agua():
    """turno() devuelve 'agua' al disparar a una casilla vacía."""
    tablero = crear_tablero(10, 10)
    flota = [{"nombre": "Patrullero", "longitud": 2, "impactos": 0,
              "hundido": False, "cantidad": 1, "coordenadas": [(0, 0), (0, 1)]}]
    tablero[0][0] = BARCO
    tablero[0][1] = BARCO
    resultado = turno(tablero, flota, 5, 5)
    assert resultado == "agua"
    assert tablero[5][5] == FALLO


def test_turno_tocado():
    """turno() devuelve 'tocado' al impactar un barco sin hundirlo."""
    tablero = crear_tablero(10, 10)
    flota = [{"nombre": "Patrullero", "longitud": 2, "impactos": 0,
              "hundido": False, "cantidad": 1, "coordenadas": [(0, 0), (0, 1)]}]
    tablero[0][0] = BARCO
    tablero[0][1] = BARCO
    resultado = turno(tablero, flota, 0, 0)
    assert resultado == "tocado"
    assert tablero[0][0] == ACIERTO


def test_turno_hundido():
    """turno() devuelve 'hundido' al impactar la última casilla de un barco."""
    tablero = crear_tablero(10, 10)
    flota = [{"nombre": "Patrullero", "longitud": 2, "impactos": 0,
              "hundido": False, "cantidad": 1, "coordenadas": [(0, 0), (0, 1)]}]
    tablero[0][0] = BARCO
    tablero[0][1] = BARCO
    turno(tablero, flota, 0, 0)
    resultado = turno(tablero, flota, 0, 1)
    assert resultado == "hundido"
    assert flota[0]["hundido"] == True


def test_turno_disparo_repetido_lanza_error():
    """turno() lanza ValueError si se dispara dos veces al mismo sitio."""
    tablero = crear_tablero(10, 10)
    flota = [{"nombre": "Patrullero", "longitud": 2, "impactos": 0,
              "hundido": False, "cantidad": 1, "coordenadas": [(0, 0), (0, 1)]}]
    tablero[0][0] = BARCO
    tablero[0][1] = BARCO
    turno(tablero, flota, 5, 5)
    with pytest.raises(ValueError):
        turno(tablero, flota, 5, 5)


def test_turno_fuera_del_tablero_lanza_error():
    """turno() lanza ValueError si las coordenadas están fuera del tablero."""
    tablero = crear_tablero(10, 10)
    flota = [{"nombre": "Patrullero", "longitud": 2, "impactos": 0,
              "hundido": False, "cantidad": 1, "coordenadas": [(0, 0), (0, 1)]}]
    with pytest.raises(ValueError):
        turno(tablero, flota, 99, 99)


# --- Tests para iniciar_partida ---

def test_iniciar_partida_coloca_barcos_en_ambos_tableros():
    """iniciar_partida() debe colocar barcos en ambos tableros."""
    import copy
    from Constantes import FLOTA
    tablero1 = crear_tablero(10, 10)
    tablero2 = crear_tablero(10, 10)
    flota1 = copy.deepcopy(FLOTA)
    flota2 = copy.deepcopy(FLOTA)
    iniciar_partida(tablero1, tablero2, flota1, flota2)

    barcos_t1 = sum(1 for fila in tablero1 for casilla in fila if casilla == BARCO)
    barcos_t2 = sum(1 for fila in tablero2 for casilla in fila if casilla == BARCO)

    total_esperado = sum(b["longitud"] * b["cantidad"] for b in FLOTA)
    assert barcos_t1 == total_esperado
    assert barcos_t2 == total_esperado


def test_iniciar_partida_flotas_son_independientes():
    """Las flotas de ambos jugadores deben ser independientes entre sí."""
    import copy
    from Constantes import FLOTA
    tablero1 = crear_tablero(10, 10)
    tablero2 = crear_tablero(10, 10)
    flota1 = copy.deepcopy(FLOTA)
    flota2 = copy.deepcopy(FLOTA)
    iniciar_partida(tablero1, tablero2, flota1, flota2)
    # Hundir todos los barcos de flota1 no debe afectar a flota2
    for b in flota1:
        b["hundido"] = True
    assert any(not b["hundido"] for b in flota2)


# --- Tests para jugar_partida ---

def hacer_coordenadas(lista):
    """Helper: devuelve función que itera sobre coordenadas predefinidas."""
    iterador = iter(lista)
    return lambda: next(iterador)


def test_jugar_partida_jugador_1():
    """Jugador 1 hunde el patrullero del jugador 2 en 2 disparos."""
    flota1 = [{"nombre": "Patrullero", "longitud": 2, "impactos": 0,
               "hundido": False, "cantidad": 1, "coordenadas": [(0, 0), (0, 1)]}]
    flota2 = [{"nombre": "Patrullero", "longitud": 2, "impactos": 0,
               "hundido": False, "cantidad": 1, "coordenadas": [(0, 0), (0, 1)]}]
    tablero1 = crear_tablero(10, 10)
    tablero2 = crear_tablero(10, 10)
    tablero1[0][0] = BARCO
    tablero1[0][1] = BARCO
    tablero2[0][0] = BARCO
    tablero2[0][1] = BARCO

    obtener_coords = hacer_coordenadas([(0, 0), (0, 0), (0, 1)])
    resultado = jugar_partida(tablero1, tablero2, flota1, flota2, obtener_coords)
    assert resultado == 1


def test_jugar_partida_jugador_2():
    """Jugador 2 gana cuando jugador 1 falla y J2 acierta todos."""
    flota1 = [{"nombre": "Patrullero", "longitud": 2, "impactos": 0,
               "hundido": False, "cantidad": 1, "coordenadas": [(0, 0), (0, 1)]}]
    flota2 = [{"nombre": "Patrullero", "longitud": 2, "impactos": 0,
               "hundido": False, "cantidad": 1, "coordenadas": [(0, 0), (0, 1)]}]
    tablero1 = crear_tablero(10, 10)
    tablero2 = crear_tablero(10, 10)
    tablero1[0][0] = BARCO
    tablero1[0][1] = BARCO
    tablero2[0][0] = BARCO
    tablero2[0][1] = BARCO

    obtener_coords = hacer_coordenadas([(0, 0), (0, 0), (0, 3), (0, 1)])
    resultado = jugar_partida(tablero1, tablero2, flota1, flota2, obtener_coords)
    assert resultado == 2