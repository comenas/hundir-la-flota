import json
import os

def cargar_ranking():
    if not os.path.exists("ranking.json"):
        return[]
    with open("ranking.json") as f:
        return json.load(f)

def guardar_partida(ganador, perdedor, turnos, modo):
    partidas = cargar_ranking()
    partidas.append({
        "ganador": ganador,
        "perdedor": perdedor,
        "turnos": turnos,
        "modo": modo })
    with open("ranking.json", "w") as f:
        json.dump(partidas, f)

def mostrar_ranking():
    ranking = cargar_ranking()
    print(ranking)
