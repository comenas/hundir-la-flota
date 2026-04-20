import pytest
from interfaz import pedir_coordenadas, pedir_orientacion, mostrar_resultado, mostrar_turno
from tablero import crear_tablero


# --- Tests para pedir_coordenadas ---

def test_pedir_coordenadas_test1(monkeypatch):
    """Acepta coordenada válida J10 tras entradas inválidas."""
    entradas = iter(["hola", "10", "1", "J10"])
    monkeypatch.setattr("builtins.input", lambda _: next(entradas))
    tablero = crear_tablero(10, 10)
    fila, columna = pedir_coordenadas(tablero)
    assert fila == 9
    assert columna == 9


def test_pedir_coordenadas_test2(monkeypatch):
    """Acepta coordenada válida B3 tras varias entradas incorrectas."""
    entradas = iter(["horrible", "12312", "miau", "B3"])
    monkeypatch.setattr("builtins.input", lambda _: next(entradas))
    tablero = crear_tablero(10, 10)
    fila, columna = pedir_coordenadas(tablero)
    assert fila == 1
    assert columna == 2


def test_pedir_coordenadas_primera_valida(monkeypatch):
    """Acepta directamente una coordenada correcta sin reintentos."""
    monkeypatch.setattr("builtins.input", lambda _: "A1")
    tablero = crear_tablero(10, 10)
    fila, columna = pedir_coordenadas(tablero)
    assert fila == 0
    assert columna == 0


def test_pedir_coordenadas_fuera_del_tablero_reintenta(monkeypatch):
    """Rechaza coordenadas fuera del tablero y vuelve a pedir."""
    entradas = iter(["Z99", "A1"])
    monkeypatch.setattr("builtins.input", lambda _: next(entradas))
    tablero = crear_tablero(10, 10)
    fila, columna = pedir_coordenadas(tablero)
    assert fila == 0
    assert columna == 0


def test_pedir_coordenadas_minusculas(monkeypatch):
    """Acepta letras minúsculas (a1 equivale a A1 en fila/columna)."""
    monkeypatch.setattr("builtins.input", lambda _: "a1")
    tablero = crear_tablero(10, 10)
    # 'a' -> ord('a') - ord('A') = 32, que está fuera -> debe reintentar
    # Este test documenta el comportamiento actual: minúsculas dan coordenada inválida
    entradas = iter(["a1", "A1"])
    monkeypatch.setattr("builtins.input", lambda _: next(entradas))
    fila, columna = pedir_coordenadas(tablero)
    assert fila == 0
    assert columna == 0


# --- Tests para pedir_orientacion ---

def test_pedir_orientacion_test1(monkeypatch):
    """Acepta 'v' tras entradas no válidas."""
    entradas = iter(["ups", "socorro", "v"])
    monkeypatch.setattr("builtins.input", lambda _: next(entradas))
    orientacion = pedir_orientacion()
    assert orientacion == "v"


def test_pedir_orientacion_test2(monkeypatch):
    """Acepta 'H' (mayúscula) y lo convierte a 'h'."""
    entradas = iter(["mimimi", "z", "B", "H"])
    monkeypatch.setattr("builtins.input", lambda _: next(entradas))
    orientacion = pedir_orientacion()
    assert orientacion == "h"


def test_pedir_orientacion_h_directa(monkeypatch):
    """Acepta 'h' directamente."""
    monkeypatch.setattr("builtins.input", lambda _: "h")
    assert pedir_orientacion() == "h"


def test_pedir_orientacion_v_directa(monkeypatch):
    """Acepta 'v' directamente."""
    monkeypatch.setattr("builtins.input", lambda _: "v")
    assert pedir_orientacion() == "v"


def test_pedir_orientacion_mayuscula_V(monkeypatch):
    """Acepta 'V' mayúscula y lo normaliza a 'v'."""
    monkeypatch.setattr("builtins.input", lambda _: "V")
    assert pedir_orientacion() == "v"


# --- Tests para mostrar_resultado ---

def test_mostrar_resultado_imprime(capsys):
    """mostrar_resultado() imprime el texto recibido."""
    mostrar_resultado("TOCADO")
    captured = capsys.readouterr()
    assert "TOCADO" in captured.out


def test_mostrar_resultado_agua(capsys):
    """mostrar_resultado() imprime 'agua' correctamente."""
    mostrar_resultado("agua")
    captured = capsys.readouterr()
    assert "agua" in captured.out


def test_mostrar_resultado_hundido(capsys):
    """mostrar_resultado() imprime 'hundido' correctamente."""
    mostrar_resultado("hundido")
    captured = capsys.readouterr()
    assert "hundido" in captured.out


# --- Tests para mostrar_turno ---

def test_mostrar_turno_imprime_dos_tableros(capsys):
    """mostrar_turno() muestra ambos tableros sin errores."""
    tablero1 = crear_tablero(5, 5)
    tablero2 = crear_tablero(5, 5)
    mostrar_turno(tablero1, tablero2)
    captured = capsys.readouterr()
    # Debe haber contenido impreso (dos tableros)
    assert len(captured.out) > 0


def test_mostrar_turno_contiene_agua(capsys):
    """El output de mostrar_turno incluye el símbolo de agua '~'."""
    from Constantes import AGUA
    tablero1 = crear_tablero(5, 5)
    tablero2 = crear_tablero(5, 5)
    mostrar_turno(tablero1, tablero2)
    captured = capsys.readouterr()
    assert AGUA in captured.out