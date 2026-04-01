from Constantes import *
from tablero import saber_coordenada_valida

#función para saber si la posición de un barco es válidad
#esta función únicamente debe dar True o False
def saber_posicion_valida(tablero,fila,columna,longitud,orientacion):
    for i in range(longitud):
        if orientacion == "h": #según la rotación bucle para asegurar que todas la posiciones del barco son validas
            fila_actual = fila
            columna_actual = columna + i #quería que fuera algo como columna - (longitud//2) perooo no se pudo
            if saber_coordenada_valida(tablero, fila_actual, columna_actual) == False:
                return False
            elif tablero[fila_actual][columna_actual] != AGUA: #esto de aquí es para asegurarnos de que 2 barcos no se solapan
                return False
        else:
            fila_actual = fila + i
            columna_actual = columna 
            if saber_coordenada_valida(tablero, fila_actual, columna_actual) == False:
                return False
            elif tablero[fila_actual][columna_actual] != AGUA:
                return False
    return True

def colocar_barco(tablero, fila, columna, longitud, orientacion, barco):
    barco["coordenadas"] = []
    if saber_posicion_valida(tablero, fila, columna, longitud, orientacion) == False: #miramos si es válido
        raise ValueError("Posición del barco no válida")
    for i in range(longitud): #esto es el mismo bucle que la funcion de arriba, me gustaría hacerlo sin repetirme
        if orientacion == "h":  #Codigo DRY
            fila_actual = fila
            columna_actual = columna + i
        else:
            fila_actual = fila + i
            columna_actual = columna
        tablero[fila_actual][columna_actual] = BARCO
        barco["coordenadas"].append((fila_actual,columna_actual))
        
import random

def colocar_flota_aleatoria(tablero, flota):
    n_filas = len(tablero) -1
    n_columnas = len(tablero[0]) -1
    for barco in flota:
        for i in range(barco["cantidad"]): #en clase hemos dado hacer esto en una linea luego lo intento
            posicion_valida = False
            while not posicion_valida:
                fila = random.randint(0,n_filas)
                columna = random.randint(0,n_columnas)
                orientacion = random.choice(["h","v"]) #esto pilla lista no varios valores cuidado
                longitud = barco["longitud"]
                try:
                    colocar_barco(tablero,fila,columna,longitud,orientacion,barco) # pass hace que pase pero no se la diferencia con continue
                    posicion_valida = True
                except ValueError:
                    pass  #vale pass es para rellenar no hace NADA literalmente continue salta al siguiente ciclo

