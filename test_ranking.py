import pytest
from ranking import guardar_partida, cargar_ranking, mostrar_ranking


def test_guardar_y_cargar(tmp_path, monkeypatch):
    """guardar_partida() guarda una entrada y cargar_ranking() la recupera."""
    monkeypatch.chdir(tmp_path)
    guardar_partida("J1", "J2", 10, "PvP")
    ranking = cargar_ranking()
    assert len(ranking) == 1
    assert ranking[0]["ganador"] == "J1"


def test_cargar_sin_archivo(tmp_path, monkeypatch):
    """cargar_ranking() devuelve lista vacía si no existe el archivo."""
    monkeypatch.chdir(tmp_path)
    assert cargar_ranking() == []


def test_guardar_multiples_partidas(tmp_path, monkeypatch):
    """Se pueden guardar varias partidas y todas se recuperan."""
    monkeypatch.chdir(tmp_path)
    guardar_partida("J1", "CPU", 5, "PvCPU")
    guardar_partida("J2", "J1", 20, "PvP")
    ranking = cargar_ranking()
    assert len(ranking) == 2
    assert ranking[0]["ganador"] == "J1"
    assert ranking[1]["ganador"] == "J2"


def test_guardar_partida_campos_correctos(tmp_path, monkeypatch):
    """Todos los campos se guardan correctamente."""
    monkeypatch.chdir(tmp_path)
    guardar_partida("Jugador", "CPU", 42, "Jugador vs CPU")
    ranking = cargar_ranking()
    p = ranking[0]
    assert p["ganador"] == "Jugador"
    assert p["perdedor"] == "CPU"
    assert p["turnos"] == 42
    assert p["modo"] == "Jugador vs CPU"


def test_guardar_acumula_sin_borrar(tmp_path, monkeypatch):
    """Cada llamada a guardar_partida acumula sin borrar las anteriores."""
    monkeypatch.chdir(tmp_path)
    for i in range(5):
        guardar_partida(f"J{i}", "CPU", i * 10, "PvCPU")
    assert len(cargar_ranking()) == 5


def test_mostrar_ranking_sin_partidas(tmp_path, monkeypatch, capsys):
    """mostrar_ranking() avisa si no hay partidas guardadas."""
    monkeypatch.chdir(tmp_path)
    mostrar_ranking()
    captured = capsys.readouterr()
    assert "No hay partidas" in captured.out


def test_mostrar_ranking_con_partidas(tmp_path, monkeypatch, capsys):
    """mostrar_ranking() imprime las partidas guardadas."""
    monkeypatch.chdir(tmp_path)
    guardar_partida("Jugador", "CPU", 15, "PvCPU")
    mostrar_ranking()
    captured = capsys.readouterr()
    assert "Jugador" in captured.out
    assert "15" in captured.out