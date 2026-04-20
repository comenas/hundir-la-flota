import pytest
from tablero import crear_tablero
from juego import comprobar_fin, turno, iniciar_partida, jugar_partida
from Constantes import BARCO, AGUA, ACIERTO, FALLO


# --- Tests para comprobar_fin ---

# comprobamos que la partida NO termina si al menos un barco sigue vivo
# todos hundidos menos el patrullero → debe seguir
def test_comprobar_fin_vivo():
    flota = [
        {"nombre": "Portaaviones", "longitud": 5, "impactos": 0, "hundido": True,  "cantidad": 1},
        {"nombre": "Acorazado",    "longitud": 4, "impactos": 0, "hundido": True,  "cantidad": 2},
        {"nombre": "Destructor",   "longitud": 3, "impactos": 0, "hundido": True,  "cantidad": 1},
        {"nombre": "Submarino",    "longitud": 3, "impactos": 0, "hundido": True,  "cantidad": 1},
        {"nombre": "Patrullero",   "longitud": 2, "impactos": 0, "hundido": False, "cantidad": 1},  # este sigue vivo
    ]
    assert comprobar_fin(flota) == False


# comprobamos que la partida SÍ termina cuando todos los barcos están hundidos
def test_comprobar_fin_muertos():
    flota = [
        {"nombre": "Portaaviones", "longitud": 5, "impactos": 0, "hundido": True, "cantidad": 1},
        {"nombre": "Acorazado",    "longitud": 4, "impactos": 0, "hundido": True, "cantidad": 2},
        {"nombre": "Destructor",   "longitud": 3, "impactos": 0, "hundido": True, "cantidad": 1},
        {"nombre": "Submarino",    "longitud": 3, "impactos": 0, "hundido": True, "cantidad": 1},
        {"nombre": "Patrullero",   "longitud": 2, "impactos": 0, "hundido": True, "cantidad": 1},
    ]
    assert comprobar_fin(flota) == True


# caso raro: flota vacía → all() sobre lista vacía devuelve True en Python
# así que una flota sin barcos también se considera "terminada"
def test_comprobar_fin_flota_vacia():
    assert comprobar_fin([]) == True


# con un solo barco vivo la partida tiene que seguir
def test_comprobar_fin_solo_un_barco_vivo():
    flota = [{"nombre": "Patrullero", "longitud": 2, "impactos": 0, "hundido": False, "cantidad": 1}]
    assert comprobar_fin(flota) == False


# con un solo barco y ya hundido la partida termina
def test_comprobar_fin_solo_un_barco_hundido():
    flota = [{"nombre": "Patrullero", "longitud": 2, "impactos": 2, "hundido": True, "cantidad": 1}]
    assert comprobar_fin(flota) == True


# --- Tests para turno ---

# comprobamos que turno devuelve "agua" cuando disparamos a una casilla vacía
# además comprobamos que la casilla queda marcada como FALLO en el tablero
def test_turno_agua():
    tablero = crear_tablero(10, 10)
    flota = [{"nombre": "Patrullero", "longitud": 2, "impactos": 0,
              "hundido": False, "cantidad": 1, "coordenadas": [(0, 0), (0, 1)]}]
    tablero[0][0] = BARCO
    tablero[0][1] = BARCO
    resultado = turno(tablero, flota, 5, 5)  # disparamos al (5,5), que está vacío
    assert resultado == "agua"
    assert tablero[5][5] == FALLO  # queda marcada como fallo


# comprobamos que turno devuelve "tocado" al impactar un barco sin hundirlo
# el patrullero tiene 2 casillas, con un impacto solo lo tocamos
def test_turno_tocado():
    tablero = crear_tablero(10, 10)
    flota = [{"nombre": "Patrullero", "longitud": 2, "impactos": 0,
              "hundido": False, "cantidad": 1, "coordenadas": [(0, 0), (0, 1)]}]
    tablero[0][0] = BARCO
    tablero[0][1] = BARCO
    resultado = turno(tablero, flota, 0, 0)  # primer impacto al patrullero
    assert resultado == "tocado"
    assert tablero[0][0] == ACIERTO  # casilla marcada como acierto


# comprobamos que turno devuelve "hundido" al dar en la última casilla del barco
# y que el barco queda marcado como hundido en la flota
def test_turno_hundido():
    tablero = crear_tablero(10, 10)
    flota = [{"nombre": "Patrullero", "longitud": 2, "impactos": 0,
              "hundido": False, "cantidad": 1, "coordenadas": [(0, 0), (0, 1)]}]
    tablero[0][0] = BARCO
    tablero[0][1] = BARCO
    turno(tablero, flota, 0, 0)         # primer impacto
    resultado = turno(tablero, flota, 0, 1)  # segundo impacto: lo hunde
    assert resultado == "hundido"
    assert flota[0]["hundido"] == True  # el barco queda marcado como hundido


# comprobamos que disparar dos veces al mismo sitio lanza ValueError
# si no lanzara error el jugador podría "gastar" turnos disparando donde ya disparó
def test_turno_disparo_repetido_lanza_error():
    tablero = crear_tablero(10, 10)
    flota = [{"nombre": "Patrullero", "longitud": 2, "impactos": 0,
              "hundido": False, "cantidad": 1, "coordenadas": [(0, 0), (0, 1)]}]
    tablero[0][0] = BARCO
    tablero[0][1] = BARCO
    turno(tablero, flota, 5, 5)  # primer disparo al (5,5)
    with pytest.raises(ValueError):
        turno(tablero, flota, 5, 5)  # segundo disparo al mismo sitio: tiene que explotar


# comprobamos que disparar fuera del tablero lanza ValueError
# (99,99) no existe en un tablero 10x10
def test_turno_fuera_del_tablero_lanza_error():
    tablero = crear_tablero(10, 10)
    flota = [{"nombre": "Patrullero", "longitud": 2, "impactos": 0,
              "hundido": False, "cantidad": 1, "coordenadas": [(0, 0), (0, 1)]}]
    with pytest.raises(ValueError):
        turno(tablero, flota, 99, 99)


# --- Tests para iniciar_partida ---

# comprobamos que iniciar_partida coloca barcos en los dos tableros
# el total de casillas BARCO en cada tablero tiene que coincidir con la suma de longitudes
def test_iniciar_partida_coloca_barcos_en_ambos_tableros():
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
    assert barcos_t1 == total_esperado  # tablero 1 tiene todos los barcos
    assert barcos_t2 == total_esperado  # tablero 2 también


# comprobamos que las flotas de los dos jugadores son independientes
# hundir todos los barcos de flota1 NO debe afectar al estado de flota2
def test_iniciar_partida_flotas_son_independientes():
    import copy
    from Constantes import FLOTA
    tablero1 = crear_tablero(10, 10)
    tablero2 = crear_tablero(10, 10)
    flota1 = copy.deepcopy(FLOTA)
    flota2 = copy.deepcopy(FLOTA)
    iniciar_partida(tablero1, tablero2, flota1, flota2)
    for b in flota1:
        b["hundido"] = True  # hundimos toda la flota 1 a mano
    assert any(not b["hundido"] for b in flota2)  # flota2 no se ha enterado de nada


# --- Tests para jugar_partida ---

# helper: devuelve una función que itera sobre una lista de coordenadas predefinidas
# así simulamos los turnos sin tener que pisar un input real
def hacer_coordenadas(lista):
    iterador = iter(lista)
    return lambda: next(iterador)


# comprobamos que el jugador 1 gana si hunde los dos trozos del patrullero rival
# secuencia: J1 dispara (0,0) → tocado | J2 dispara (0,0) → tocado | J1 dispara (0,1) → hundido → gana J1
def test_jugar_partida_jugador_1():
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
    # (0,0) → J1 toca a J2 | (0,0) → J2 toca a J1 | (0,1) → J1 hunde a J2 → fin
    resultado = jugar_partida(tablero1, tablero2, flota1, flota2, obtener_coords)
    assert resultado == 1


# comprobamos que el jugador 2 gana si J1 falla su primer disparo y luego J2 acierta los dos
# secuencia: J1 dispara (0,0) → toca | J2 dispara (0,0) → toca | J1 dispara (0,3) → agua | J2 dispara (0,1) → hunde → gana J2
def test_jugar_partida_jugador_2():
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