from barcos import colocar_flota_aleatoria
from disparo import procesar_disparo
def iniciar_partida(tablero1,tablero2,flota1,flota2):
    colocar_flota_aleatoria(tablero1,flota1)
    colocar_flota_aleatoria(tablero2,flota2)

def comprobar_fin(flota):
    return all(barco["hundido"] == True for barco in flota)

def turno(tablero,flota,fila,columna):
    procesar_disparo(tablero,flota,fila,columna)

def jugar_partida(tablero1,tablero2, flota1, flota2):
    terminado = False
    jugador1 = True
    while not terminado:
        print("aquí me quedo")

print("ruben gitano")