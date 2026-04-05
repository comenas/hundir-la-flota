from barcos import colocar_flota_aleatoria
from disparo import procesar_disparo
def iniciar_partida(tablero1,tablero2,flota1,flota2):
    colocar_flota_aleatoria(tablero1,flota1)
    colocar_flota_aleatoria(tablero2,flota2)

def comprobar_fin(flota):
    if all(barco["hundido"] for barco in flota):
        return True
    else:
        return False

def turno(tablero,flota,fila,columna):
    return procesar_disparo(tablero,flota,fila,columna)

def jugar_partida(tablero1,tablero2, flota1, flota2, obtener_coordenadas):
    terminado = False
    turno_actual = 1
    while not terminado:
        if turno_actual == 1:
            fila,columna = obtener_coordenadas()
            turno(tablero2, flota2, fila, columna)
            if comprobar_fin(flota2):
                return 1
            turno_actual = 2
        else:
            fila,columna = obtener_coordenadas()
            turno(tablero1, flota1, fila, columna)
            if comprobar_fin(flota1):
                return 2
            turno_actual = 1
