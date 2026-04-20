from Constantes import *

def comprobar_medidas(filas, columnas):
    if filas > TAMAÑO_MAX_FILAS:
        raise ValueError("El máximo de filas es 15")
    if filas < TAMAÑO_MIN_FILAS:
        raise ValueError("El mínimo de filas es 5")
    if columnas > TAMAÑO_MAX_COLUMNAS:
        raise ValueError("El máximo de columnas es 15")
    if columnas < TAMAÑO_MIN_COLUMNAS:
        raise ValueError("El mínimo de columnas es 5")

def crear_tablero(filas, columnas):
    comprobar_medidas(filas, columnas)
    return [[AGUA] * columnas for _ in range(filas)]

def mostrar_tablero(tablero, ocultar_barcos=False):
    columnas = len(tablero[0])
    filas = len(tablero)
    numeros_coords = " "
    for i in range(1, columnas + 1):
        numeros_coords += str(i).rjust(2) + "   "
    print("  " + numeros_coords, "")
    for i in range(filas):
        letra = chr(65 + i)
        celdas = [AGUA if (c == BARCO and ocultar_barcos) else c for c in tablero[i]]
        print(letra + "   " + "    ".join(celdas), "")

def saber_coordenada_valida(tablero, fila, columna):
    return 0 <= fila < len(tablero) and 0 <= columna < len(tablero[0])
