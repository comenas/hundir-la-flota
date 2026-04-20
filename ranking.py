import json
import os

def cargar_ranking(): #carga el archivo donde están las partidas pasadas
    if not os.path.exists("ranking.json"):
        return[]
    with open("ranking.json") as f:
        return json.load(f)

def guardar_partida(ganador, perdedor, turnos, modo): #guarda la partida recien jugada en el archivo de rankings
    partidas = cargar_ranking()
    partidas.append({
        "ganador": ganador,
        "perdedor": perdedor,
        "turnos": turnos,
        "modo": modo })
    with open("ranking.json", "w") as f:
        json.dump(partidas, f)

def mostrar_ranking(): #muestra el ranking cuando se le pida
    ranking = cargar_ranking()
    if not ranking:
        print("No hay partidas guardadas")
        return
    for i, partida in enumerate(ranking, 1):
        print(f"{i}. Ganador: {partida["ganador"]} | Turnos: {partida["turnos"]} | Modo:{partida["modo"]}")
