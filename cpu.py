import random
from Constantes import ACIERTO, FALLO
def cpu_disparo(tablero):
    disparo = False
    while not disparo:
        fila = random.randint(0,len(tablero)-1)
        columna = random.randint(0,len(tablero[0])-1)
        if tablero[fila][columna] not in [ACIERTO,FALLO]:
            return fila,columna