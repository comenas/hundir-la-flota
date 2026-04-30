import pytest
from ranking import guardar_partida, cargar_ranking, mostrar_ranking


# comprobamos que guardar_partida guarda una entrada y cargar_ranking la recupera
# tmp_path y monkeypatch hacen que el ranking.json se cree en una carpeta temporal
# así no ensuciamos el proyecto con archivos de prueba
def test_guardar_y_cargar(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)  # cambia el directorio de trabajo a la carpeta temporal
    guardar_partida("J1", "J2", 10, "PvP")
    ranking = cargar_ranking()
    assert len(ranking) == 1           # solo hay una partida guardada
    assert ranking[0]["ganador"] == "J1"


# comprobamos que si ranking.json no existe cargar_ranking devuelve lista vacía
# sin esto el juego pegaría un petardazo al intentar leer un archivo que no existe
def test_cargar_sin_archivo(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    assert cargar_ranking() == []  # carpeta limpia → sin archivo → lista vacía


# comprobamos que se pueden guardar varias partidas seguidas y se acumulan todas
def test_guardar_multiples_partidas(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    guardar_partida("J1", "CPU", 5, "PvCPU")
    guardar_partida("J2", "J1", 20, "PvP")
    ranking = cargar_ranking()
    assert len(ranking) == 2             # dos partidas guardadas
    assert ranking[0]["ganador"] == "J1" # primera en el orden correcto
    assert ranking[1]["ganador"] == "J2" # segunda también


# comprobamos que todos los campos de una partida se guardan y recuperan correctamente
# ganador, perdedor, turnos y modo tienen que estar intactos después de guardar y cargar
def test_guardar_partida_campos_correctos(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    guardar_partida("Jugador", "CPU", 42, "Jugador vs CPU")
    ranking = cargar_ranking()
    p = ranking[0]
    assert p["ganador"] == "Jugador"
    assert p["perdedor"] == "CPU"
    assert p["turnos"] == 42
    assert p["modo"] == "Jugador vs CPU"


# comprobamos que cada llamada a guardar_partida AÑADE sin borrar las anteriores
# guardamos 5 partidas en bucle y comprobamos que siguen siendo 5
def test_guardar_acumula_sin_borrar(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    for i in range(5):
        guardar_partida(f"J{i}", "CPU", i * 10, "PvCPU")
    assert len(cargar_ranking()) == 5  # las 5 siguen ahí, ninguna se perdió


# comprobamos que mostrar_ranking avisa cuando no hay partidas guardadas
# que no pete ni se quede en silencio: tiene que decir algo
def test_mostrar_ranking_sin_partidas(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    mostrar_ranking()
    captured = capsys.readouterr()
    assert "No hay partidas" in captured.out  # mensaje de aviso al usuario


# comprobamos que mostrar_ranking imprime los datos de las partidas guardadas
# buscamos el nombre del ganador y el número de turnos en el output
def test_mostrar_ranking_con_partidas(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    guardar_partida("Jugador", "CPU", 15, "PvCPU")
    mostrar_ranking()
    captured = capsys.readouterr()
    assert "Jugador" in captured.out  # el ganador aparece en pantalla
    assert "15" in captured.out       # los turnos también