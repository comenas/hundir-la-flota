from tablero import saber_coordenada_valida,mostrar_tablero

def pedir_coordenadas(tablero):
    correcto_coord = False
    while  not correcto_coord:
        try:
            coordenadas = input("introduce la corrdenada de tu disparo ej:(A7)")
            letra = coordenadas[0]
            numero = int(coordenadas[1:])
            fila = ord(letra) - ord("A")
            columna = numero - 1
            if not saber_coordenada_valida(tablero,fila,columna): print("coordenada no válida intenta de nuevo")
            else:
                correcto_coord = True
        except (ValueError,IndexError):
            print("Coordenada no válida usa el formato A7")

    return fila,columna

def pedir_orientacion():
    correcto_Ord = False
    while not correcto_Ord:
        orientacion = input("introduce la orientación: (h/v)")
        if orientacion.lower() in ["h","v"]:
            correcto_Ord = True
    return orientacion.lower()

def mostrar_resultado(resultado):
    print(resultado)

def mostrar_turno(tablero_propio, tablero_rival):
    mostrar_tablero(tablero_propio)
    mostrar_tablero(tablero_rival)




