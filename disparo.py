from barcos import saber_coordenada_valida
from Constantes import *
def procesar_disparo(tablero,flota,fila,columna):
    barco = None
    for b in flota:
        if (fila, columna) in b["coordenadas"]:
            barco = b
            break
    if not saber_coordenada_valida(tablero, fila, columna):
        raise ValueError("Coordenada fuera del tablero")
    coordenada = tablero[fila][columna]
    if coordenada == ACIERTO or coordenada == FALLO:
        raise ValueError("Ya se disparó aquí")
    else:
        if coordenada == AGUA:
            tablero[fila][columna] = FALLO
            return "agua"
        else:
            tablero[fila][columna] = ACIERTO
            barco["impactos"] += 1
            if barco["impactos"] == barco["longitud"]:
                barco["hundido"] = True
                return "hundido"
            else:
                return "tocado"
