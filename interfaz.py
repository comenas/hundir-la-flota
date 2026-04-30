from tablero import saber_coordenada_valida,mostrar_tablero

def pedir_coordenadas(tablero): #pide coordenadas al jugador
    correcto_coord = False 
    while  not correcto_coord: #hasta que no introduzcas coordenada correcta no pasas
        try:
            coordenadas = input("introduce la corrdenada de tu disparo ej:(A7)") #pues un input
            letra = coordenadas[0] # separas la letra
            numero = int(coordenadas[1:]) #del número
            letra_comprobada = letra.upper()
            fila = ord(letra_comprobada) - ord("A") #esto es porque el tablero es del 0 - 9 no del 1 - 10 #y por si pones minúsculas
            columna = numero - 1 #lo mismo del 0 - 9
            if not saber_coordenada_valida(tablero,fila,columna): print("coordenada no válida intenta de nuevo") #si falla la coordenada
            else:
                correcto_coord = True #pasas
        except (ValueError,IndexError):
            print("Coordenada no válida usa el formato A7") #si falla el input

    return fila,columna

def pedir_orientacion(): #pide la orientación de un barco
    correcto_Ord = False
    while not correcto_Ord: #no pasas hasta que no lo pongas bien
        orientacion = input("introduce la orientación: (h/v)") #pide h o v para orientar horizontal de vertical
        if orientacion.lower() in ["h","v"]: #por si pones mayúsculas
            correcto_Ord = True
    return orientacion.lower()

def mostrar_resultado(resultado): #mostrar el resultado :d
    print(resultado)

def mostrar_turno(tablero_propio, tablero_rival): #muestra los tableros tuyo y de tu contrincante me gustaría ponerlos lado a lado pero no hay tiempo para tonterías
    mostrar_tablero(tablero_propio)
    mostrar_tablero(tablero_rival)




