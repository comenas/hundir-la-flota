import copy
from Constantes import FLOTA_DEFAULT
from tablero import crear_tablero, mostrar_tablero
from juego import iniciar_partida, jugar_partida
from interfaz import pedir_coordenadas, mostrar_resultado, mostrar_turno
from ranking import guardar_partida, mostrar_ranking

def main():
    juego_fin = False
    while not juego_fin:
        print("1. PvP  2. PvCPU  3. Salvas  4. Ranking  5. Salir")
        opcion = input("Elige: ")
        if opcion == "1":
            tablero1 = crear_tablero(10, 10)
            tablero2 = crear_tablero(10, 10)
            flota1 = copy.deepcopy(FLOTA_DEFAULT)
            flota2 = copy.deepcopy(FLOTA_DEFAULT)
            iniciar_partida(tablero1, tablero2, flota1, flota2)
            ganador = jugar_partida(
                tablero1, tablero2, flota1, flota2,
                lambda: pedir_coordenadas(tablero2)
            )
            guardar_partida(f"J{ganador}", f"J{3-ganador}", 0, "PvP")
        elif opcion == "2":
            tablero1 = crear_tablero(10,10)
            tablero2 = crear_tablero(10,10)
            flota1 = copy.deepcopy(FLOTA_DEFAULT)
            flota2 = copy.deepcopy(FLOTA_DEFAULT)
            iniciar_partida(tablero1, tablero2, flota1, flota2)
            ganador = jugar_partida(
                tablero1, tablero2, flota1, flota2,
                lambda: pedir_coordenadas(tablero2)
            )
        elif opcion == "4":
            mostrar_ranking()
        elif opcion == "5":
            break

if __name__ == "__main__":
    main()