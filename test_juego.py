import pytest
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
    {"nombre": "Patrullero",   "longitud": 2, "impactos": 0, "hundido": False, "cantidad": 1},
]
    assert comprobar_fin(flota) == True