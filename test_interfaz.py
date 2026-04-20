import pytest
from interfaz import pedir_coordenadas, pedir_orientacion, mostrar_resultado, mostrar_turno
from tablero import crear_tablero


# --- Tests para pedir_coordenadas ---

# comprobamos que después de varias entradas incorrectas acepta la válida J10
# monkeypatch simula los inputs del usuario sin tener que teclear nada de verdad
def test_pedir_coordenadas_test1(monkeypatch):
    entradas = iter(["hola", "10", "1", "J10"])  # tres entradas malas y luego la buena
    monkeypatch.setattr("builtins.input", lambda _: next(entradas))
    tablero = crear_tablero(10, 10)
    fila, columna = pedir_coordenadas(tablero)
    assert fila == 9     # J es la décima letra → índice 9
    assert columna == 9  # 10 → índice 9


# comprobamos que también acepta "B3" después de entradas sin sentido
def test_pedir_coordenadas_test2(monkeypatch):
    entradas = iter(["horrible", "12312", "miau", "B3"])
    monkeypatch.setattr("builtins.input", lambda _: next(entradas))
    tablero = crear_tablero(10, 10)
    fila, columna = pedir_coordenadas(tablero)
    assert fila == 1     # B → índice 1
    assert columna == 2  # 3 → índice 2


# comprobamos que si la primera entrada ya es válida la acepta directamente sin reintentos
def test_pedir_coordenadas_primera_valida(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "A1")
    tablero = crear_tablero(10, 10)
    fila, columna = pedir_coordenadas(tablero)
    assert fila == 0
    assert columna == 0


# comprobamos que coordenadas fuera del tablero (Z99) se rechazan y se vuelve a pedir
# Z no existe en un tablero de 10 filas, así que tiene que rechazarla y aceptar la siguiente
def test_pedir_coordenadas_fuera_del_tablero_reintenta(monkeypatch):
    entradas = iter(["Z99", "A1"])  # Z99 fuera de rango → reintenta → A1 válida
    monkeypatch.setattr("builtins.input", lambda _: next(entradas))
    tablero = crear_tablero(10, 10)
    fila, columna = pedir_coordenadas(tablero)
    assert fila == 0
    assert columna == 0


# comprobamos el comportamiento con minúsculas: "a1" en minúscula da índice fuera de rango
# por eso la función tiene que rechazarla y aceptar "A1" con mayúscula
# este test documenta que las minúsculas no son válidas directamente
def test_pedir_coordenadas_minusculas(monkeypatch):
    entradas = iter(["a1", "A1"])  # a1 en minúscula falla → A1 en mayúscula pasa
    monkeypatch.setattr("builtins.input", lambda _: next(entradas))
    tablero = crear_tablero(10, 10)
    fila, columna = pedir_coordenadas(tablero)
    assert fila == 0
    assert columna == 0


# --- Tests para pedir_orientacion ---

# comprobamos que acepta "v" después de varias entradas incorrectas
def test_pedir_orientacion_test1(monkeypatch):
    entradas = iter(["ups", "socorro", "v"])
    monkeypatch.setattr("builtins.input", lambda _: next(entradas))
    orientacion = pedir_orientacion()
    assert orientacion == "v"


# comprobamos que acepta "H" en mayúscula y lo devuelve como "h" en minúscula
def test_pedir_orientacion_test2(monkeypatch):
    entradas = iter(["mimimi", "z", "B", "H"])
    monkeypatch.setattr("builtins.input", lambda _: next(entradas))
    orientacion = pedir_orientacion()
    assert orientacion == "h"


# caso limpio: "h" directamente en el primer intento
def test_pedir_orientacion_h_directa(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "h")
    assert pedir_orientacion() == "h"


# caso limpio: "v" directamente en el primer intento
def test_pedir_orientacion_v_directa(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "v")
    assert pedir_orientacion() == "v"


# comprobamos que "V" en mayúscula también se normaliza a "v"
def test_pedir_orientacion_mayuscula_V(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "V")
    assert pedir_orientacion() == "v"


# --- Tests para mostrar_resultado ---

# comprobamos que mostrar_resultado imprime el texto que le pasamos
# capsys captura lo que se imprime por consola para poder comprobarlo
def test_mostrar_resultado_imprime(capsys):
    mostrar_resultado("TOCADO")
    captured = capsys.readouterr()
    assert "TOCADO" in captured.out  # tiene que aparecer en el output


# lo mismo para "agua"
def test_mostrar_resultado_agua(capsys):
    mostrar_resultado("agua")
    captured = capsys.readouterr()
    assert "agua" in captured.out


# lo mismo para "hundido"
def test_mostrar_resultado_hundido(capsys):
    mostrar_resultado("hundido")
    captured = capsys.readouterr()
    assert "hundido" in captured.out


# --- Tests para mostrar_turno ---

# comprobamos que mostrar_turno imprime algo (los dos tableros) sin reventar
def test_mostrar_turno_imprime_dos_tableros(capsys):
    tablero1 = crear_tablero(5, 5)
    tablero2 = crear_tablero(5, 5)
    mostrar_turno(tablero1, tablero2)
    captured = capsys.readouterr()
    assert len(captured.out) > 0  # que haya imprimido algo


# comprobamos que el output contiene el símbolo de agua "~"
# si aparece es que se están mostrando las casillas del tablero correctamente
def test_mostrar_turno_contiene_agua(capsys):
    from Constantes import AGUA
    tablero1 = crear_tablero(5, 5)
    tablero2 = crear_tablero(5, 5)
    mostrar_turno(tablero1, tablero2)
    captured = capsys.readouterr()
    assert AGUA in captured.out  # el símbolo "~" tiene que estar ahí