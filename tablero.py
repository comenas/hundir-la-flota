#Script para el control del tablero con 4 funciones:
# Crear_Tablero crea el tablero según la petición del usuario con un valor 
from Constantes import *

# Necesito una funcion crear_tablero diferente a mostrar tablero
# porque el salto de linea no lo consigo hacer de forma simple ( \n )
#voy a hacer una funcion de comprobación porque no se cuanto modular hay que ser
def comprobar_medidas(filas, columnas):
    if filas > TAMAÑO_MAX_FILAS:
        raise ValueError("El máximo de filas es 15") #comprueba
    if filas < TAMAÑO_MIN_FILAS:
        raise ValueError("El mínimo de filas es 5") #que
    if columnas > TAMAÑO_MAX_COLUMNAS:
        raise ValueError("El máximo de columnas es 15")#el valor
    if columnas < TAMAÑO_MIN_COLUMNAS:
        raise ValueError("El mínimo de columnas es 5") #es válido

    
def crear_tablero(filas, columnas):
    comprobar_medidas(filas, columnas)
    tablero = []
    for i in range(filas): #pone agua segun cuantas columnas hay y el bucle se repite según cuantas filas
        fila = [AGUA] * columnas 
        tablero.append(fila)
    return tablero

#no tocar mostrar_tablero llevo 20 minutos poniendo los espacios
#para que en la consola cuadre
def mostrar_tablero(tablero, ocultar_barcos = False):
    columnas = len(tablero[0])   #sacar las columnas
    filas = len(tablero)#sacar las filas
    numeros_coords = " " #variable vacía para poner ahora en el bucle
    
    for i in range(1, columnas + 1): # este bucle controla solo la cabezera (numeros)
        numeros_coords = numeros_coords + str(i).rjust(2) + "   " 
    print("  "+numeros_coords,"\n")
    
    for i in range(filas): #este bucle controla las filas con su letrilla
        letra = chr(65 + i) #los primeros 65 caracteres son signos de puntuación
        celdas = tablero[i]
        print(letra + "   " + "    ".join(celdas),"\n")
        
def saber_coordenada_valida(tablero, fila, columna): 
    if 0 <= fila < len(tablero) and 0 <= columna < len(tablero[0]):
        return True
    else:
        return False
 #devuelve True si está dentro del tablero False si está fuera    
        
if __name__ == "__main__":
    t = crear_tablero(10, 10)
    mostrar_tablero(t)
    #print(t)  # solo para probar 
