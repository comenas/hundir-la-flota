import pytest
from test_disparo import *
from juego import *
def test_comprobar_fin_vivo():
    flota= [
    {"nombre": "Portaaviones", "longitud": 5, "impactos": 0, "hundido": True, "cantidad": 1},
    {"nombre": "Acorazado",    "longitud": 4, "impactos": 0, "hundido": True, "cantidad": 2},
    {"nombre": "Destructor",   "longitud": 3, "impactos": 0, "hundido": True, "cantidad": 1},
    {"nombre": "Submarino",    "longitud": 3, "impactos": 0, "hundido": True, "cantidad": 1},
    {"nombre": "Patrullero",   "longitud": 2, "impactos": 0, "hundido": False, "cantidad": 1},
]
    assert comprobar_fin(flota) == False

def test_comprobar_fin_muertos():
    flota= [
    {"nombre": "Portaaviones", "longitud": 5, "impactos": 0, "hundido": True, "cantidad": 1},
    {"nombre": "Acorazado",    "longitud": 4, "impactos": 0, "hundido": True, "cantidad": 2},
    {"nombre": "Destructor",   "longitud": 3, "impactos": 0, "hundido": True, "cantidad": 1},
    {"nombre": "Submarino",    "longitud": 3, "impactos": 0, "hundido": True, "cantidad": 1},
    {"nombre": "Patrullero",   "longitud": 2, "impactos": 0, "hundido": True, "cantidad": 1},
]
    assert comprobar_fin(flota) == True

def test_turno():
    print("socorro")

def hacer_coordenadas(lista):
    iterador = iter(lista)
    return lambda: next(iterador)
#antes de leer el siguiente test debo prepararte seas quien seas
#esto ha sido un coñazo de hacer funcionar, por algo bastante simple
#tener la flota no significa tener colocados los barcos en el tablero
#hay que colocarlos a mano, la flota solo sirve en este test para saber cuando están hundidos
#es decir para nada pero no la voy a quitar por si acaso
def test_jugar_partida_jugador_1():
    # jugador 1 hunde el patrullero del jugador 2 en 2 disparos
    flota1 = [{"nombre": "Patrullero", "longitud": 2, "impactos": 0,
           "hundido": False, "cantidad": 1, "coordenadas": [(0,0),(0,1)]}]
    flota2 = [{"nombre": "Patrullero", "longitud": 2, "impactos": 0,
           "hundido": False, "cantidad": 1, "coordenadas": [(0,0),(0,1)]}]
    tablero1 = crear_tablero(10,10)
    tablero2 = crear_tablero(10,10)
    # colocar barcos manualmente en ambos tableros
    tablero1[0][0] = BARCO
    tablero1[0][1] = BARCO
    tablero2[0][0] = BARCO
    tablero2[0][1] = BARCO
    
    obtener_coords = hacer_coordenadas([(0,0), (0,0), (0,1)])
    resultado = jugar_partida(tablero1, tablero2, flota1, flota2, obtener_coords)
    assert resultado == 1

def test_jugar_partida_jugador_2():
    # jugador 1 hunde el patrullero del jugador 2 en 2 disparos
    flota1 = [{"nombre": "Patrullero", "longitud": 2, "impactos": 0,
           "hundido": False, "cantidad": 1, "coordenadas": [(0,0),(0,1)]}]
    flota2 = [{"nombre": "Patrullero", "longitud": 2, "impactos": 0,
           "hundido": False, "cantidad": 1, "coordenadas": [(0,0),(0,1)]}]
    tablero1 = crear_tablero(10,10)
    tablero2 = crear_tablero(10,10)
    # colocar barcos manualmente en ambos tableros
    tablero1[0][0] = BARCO
    tablero1[0][1] = BARCO
    tablero2[0][0] = BARCO
    tablero2[0][1] = BARCO
    
    obtener_coords = hacer_coordenadas([(0,0), (0,0), (0,3),(0,1)])
    resultado = jugar_partida(tablero1, tablero2, flota1, flota2, obtener_coords)
    assert resultado == 2