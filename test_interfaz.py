from interfaz import *
import pytest
from tablero import crear_tablero
def test_pedir_coordenadas_test1(monkeypatch):
    entradas = iter(["hola","10","1","J10"])
    monkeypatch.setattr("builtins.input", lambda _: next(entradas))
    tablero = crear_tablero(10,10)
    fila,columna = pedir_coordenadas(tablero)
    assert fila == 9
    assert columna == 9

def test_pedir_coordenadas_test2(monkeypatch):
    entradas = iter(["horrible","12312","miau","B3"])
    monkeypatch.setattr("builtins.input",lambda _: next(entradas))
    tablero = crear_tablero(10,10)
    fila,columna = pedir_coordenadas(tablero)
    assert fila == 1
    assert columna == 2

def test_pedir_orientacion_test1(monkeypatch):
    entradas = iter(["ups","socorro","v"])
    monkeypatch.setattr("builtins.input", lambda _: next(entradas))
    orientacion = pedir_orientacion()
    assert orientacion == "v"

def test_pedir_orientacion_test2(monkeypatch):
    entradas = iter(["mimimi", "z", "B", "H"])
    monkeypatch.setattr("builtins.input", lambda _: next(entradas))
    orientacion = pedir_orientacion()
    assert orientacion == "h"



