from ranking import *

def test_guardar_y_cargar(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)  #estooo es una carpeta temporal para el test
    guardar_partida("J1", "J2", 10, "PvP")
    ranking = cargar_ranking()
    assert len(ranking) == 1
    assert ranking[0]["ganador"] == "J1"

def test_cargar_sin_archivo(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    assert cargar_ranking() == []
