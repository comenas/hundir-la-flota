from barcos import saber_coordenada_valida
from Constantes import *
def procesar_disparo(tablero,flota,fila,columna): #dispara el jugador a una coordenada
    barco = None
    for b in flota:
        if (fila, columna) in b["coordenadas"]:
            barco = b
            break
    if not saber_coordenada_valida(tablero, fila, columna): #si falla pues repites
        raise ValueError("Coordenada fuera del tablero")
    coordenada = tablero[fila][columna] 
    if coordenada == ACIERTO or coordenada == FALLO: #si ya habias diparado ahí pues repites tambien
        raise ValueError("Ya se disparó aquí")
    else:
        if coordenada == AGUA: #fallas is das agua
            tablero[fila][columna] = FALLO
            return "agua"
        else:
            tablero[fila][columna] = ACIERTO #aciertas si das barco
            barco["impactos"] += 1
            if barco["impactos"] == barco["longitud"]:
                barco["hundido"] = True
                return "hundido" #hundido si hundes
            else:
                return "tocado" #tocado si tocas
#se explica solo esto