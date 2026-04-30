import pytest
import copy
from unittest.mock import patch
from tablero import crear_tablero
from Constantes import FLOTA, BARCO, AGUA, ACIERTO, FALLO

import main  # importamos el módulo para poder parchear sus referencias internas


# ─── NOTA SOBRE EL BUG EN personalizar_flota ────────────────────────────────
# En el main.py actual, dentro del while de longitud y cantidad,
# el print de error se ejecuta SIEMPRE (falta un else antes del print).
# Ejemplo del bug (líneas 96-98):
#   if LONGITUD_MIN_BARCO <= longitud <= long_max:
#       correcto_longitud = True
#   print(f"  Debe estar entre...")  ← se imprime aunque sea válido
#
# CORRECCIÓN: añadir else antes de ese print en ambos bucles (longitud y cantidad).
# Los tests de abajo están escritos asumiendo el código CORREGIDO.
# ─────────────────────────────────────────────────────────────────────────────


# ═══════════════════════════════════════════════════════════════════════════════
# elegir_modo_juego
# ═══════════════════════════════════════════════════════════════════════════════

class TestElegirModoJuego:

    def test_opcion_valida_directa(self, monkeypatch):
        """Devuelve la opción si el primer input es válido."""
        monkeypatch.setattr("builtins.input", lambda _: "1")
        assert main.elegir_modo_juego() == 1

    @pytest.mark.parametrize("opcion", [1, 2, 3, 4, 5])
    def test_todas_opciones_validas(self, monkeypatch, opcion):
        """Acepta todas las opciones del 1 al 5."""
        monkeypatch.setattr("builtins.input", lambda _: str(opcion))
        assert main.elegir_modo_juego() == opcion

    def test_reintenta_con_texto(self, monkeypatch):
        """Ignora texto no numérico y acepta el siguiente input válido."""
        entradas = iter(["hola", "3"])
        monkeypatch.setattr("builtins.input", lambda _: next(entradas))
        assert main.elegir_modo_juego() == 3

    def test_reintenta_con_numero_fuera_de_rango(self, monkeypatch):
        """Ignora números fuera de rango y acepta el siguiente válido."""
        entradas = iter(["0", "6", "99", "2"])
        monkeypatch.setattr("builtins.input", lambda _: next(entradas))
        assert main.elegir_modo_juego() == 2

    def test_reintenta_combinado(self, monkeypatch):
        """Combina errores de texto y rango antes de aceptar."""
        entradas = iter(["abc", "-1", "10", "5"])
        monkeypatch.setattr("builtins.input", lambda _: next(entradas))
        assert main.elegir_modo_juego() == 5


# ═══════════════════════════════════════════════════════════════════════════════
# configurar_tablero
# ═══════════════════════════════════════════════════════════════════════════════

class TestConfigurarTablero:

    def test_enter_usa_defecto(self, monkeypatch):
        """Pulsar Enter en ambas dimensiones devuelve tablero 10x10."""
        monkeypatch.setattr("builtins.input", lambda _: "")
        tablero = main.configurar_tablero()
        assert len(tablero) == 10
        assert len(tablero[0]) == 10

    def test_dimensiones_personalizadas(self, monkeypatch):
        """Acepta dimensiones válidas introducidas por el jugador."""
        entradas = iter(["7", "8"])
        monkeypatch.setattr("builtins.input", lambda _: next(entradas))
        tablero = main.configurar_tablero()
        assert len(tablero) == 7
        assert len(tablero[0]) == 8

    def test_reintenta_valor_fuera_de_rango(self, monkeypatch):
        """Rechaza valores fuera del rango y acepta el siguiente válido."""
        entradas = iter(["1", "20", "6", ""])  # filas: 1 y 20 inválidas, 6 válida; columnas: defecto
        monkeypatch.setattr("builtins.input", lambda _: next(entradas))
        tablero = main.configurar_tablero()
        assert len(tablero) == 6
        assert len(tablero[0]) == 10

    def test_reintenta_valor_no_numerico(self, monkeypatch):
        """Rechaza texto no numérico y acepta el siguiente valor válido."""
        entradas = iter(["abc", "5", ""])
        monkeypatch.setattr("builtins.input", lambda _: next(entradas))
        tablero = main.configurar_tablero()
        assert len(tablero) == 5
        assert len(tablero[0]) == 10

    def test_dimensiones_minimas(self, monkeypatch):
        """Acepta las dimensiones mínimas permitidas (5x5)."""
        entradas = iter(["5", "5"])
        monkeypatch.setattr("builtins.input", lambda _: next(entradas))
        tablero = main.configurar_tablero()
        assert len(tablero) == 5
        assert len(tablero[0]) == 5

    def test_dimensiones_maximas(self, monkeypatch):
        """Acepta las dimensiones máximas permitidas (15x15)."""
        entradas = iter(["15", "15"])
        monkeypatch.setattr("builtins.input", lambda _: next(entradas))
        tablero = main.configurar_tablero()
        assert len(tablero) == 15
        assert len(tablero[0]) == 15


# ═══════════════════════════════════════════════════════════════════════════════
# elegir_flota
# ═══════════════════════════════════════════════════════════════════════════════

class TestElegirFlota:

    def test_opcion_1_devuelve_flota_estandar(self, monkeypatch):
        """La opción 1 devuelve una copia de la flota estándar."""
        monkeypatch.setattr("builtins.input", lambda _: "1")
        flota = main.elegir_flota()
        assert len(flota) == len(FLOTA)
        assert flota[0]["nombre"] == FLOTA[0]["nombre"]

    def test_opcion_1_devuelve_copia_independiente(self, monkeypatch):
        """La flota devuelta es un deepcopy, no la misma referencia."""
        monkeypatch.setattr("builtins.input", lambda _: "1")
        flota = main.elegir_flota()
        flota[0]["nombre"] = "MODIFICADO"
        assert FLOTA[0]["nombre"] != "MODIFICADO"

    def test_opcion_invalida_reintenta(self, monkeypatch):
        """Rechaza opciones fuera de rango y reintenta."""
        entradas = iter(["0", "3", "abc", "1"])
        monkeypatch.setattr("builtins.input", lambda _: next(entradas))
        flota = main.elegir_flota()
        assert flota is not None

    def test_opcion_2_llama_personalizar(self, monkeypatch):
        """La opción 2 llama a personalizar_flota."""
        flota_falsa = [{"nombre": "Barca", "longitud": 2, "cantidad": 1}]
        entradas = iter(["2"])
        monkeypatch.setattr("builtins.input", lambda _: next(entradas))
        with patch.object(main, "personalizar_flota", return_value=flota_falsa) as mock_fn:
            resultado = main.elegir_flota()
            mock_fn.assert_called_once()
            assert resultado == flota_falsa


# ═══════════════════════════════════════════════════════════════════════════════
# elegir_modo_salvas
# ═══════════════════════════════════════════════════════════════════════════════

class TestElegirModoSalvas:

    def test_opcion_1_devuelve_pvcpu(self, monkeypatch):
        monkeypatch.setattr("builtins.input", lambda _: "1")
        assert main.elegir_modo_salvas() == "PvCPU"

    def test_opcion_2_devuelve_pvp(self, monkeypatch):
        monkeypatch.setattr("builtins.input", lambda _: "2")
        assert main.elegir_modo_salvas() == "PvP"

    def test_reintenta_con_invalido(self, monkeypatch):
        entradas = iter(["0", "abc", "3", "1"])
        monkeypatch.setattr("builtins.input", lambda _: next(entradas))
        assert main.elegir_modo_salvas() == "PvCPU"


# ═══════════════════════════════════════════════════════════════════════════════
# elegir_colocacion
# ═══════════════════════════════════════════════════════════════════════════════

class TestElegirColocacion:

    def test_opcion_2_coloca_aleatoriamente(self, monkeypatch):
        """La opción 2 coloca la flota automáticamente y devuelve instancias."""
        tablero = crear_tablero(10, 10)
        plantillas = copy.deepcopy(FLOTA)
        monkeypatch.setattr("builtins.input", lambda _: "2")
        flota = main.elegir_colocacion(tablero, plantillas)
        total_esperado = sum(b["cantidad"] for b in FLOTA)
        assert len(flota) == total_esperado

    def test_opcion_invalida_reintenta(self, monkeypatch):
        """Rechaza opciones inválidas antes de aceptar."""
        tablero = crear_tablero(10, 10)
        plantillas = copy.deepcopy(FLOTA)
        entradas = iter(["0", "abc", "3", "2"])
        monkeypatch.setattr("builtins.input", lambda _: next(entradas))
        flota = main.elegir_colocacion(tablero, plantillas)
        assert flota is not None

    def test_opcion_1_llama_colocacion_manual(self, monkeypatch):
        """La opción 1 delega en colocar_flota_manual."""
        tablero = crear_tablero(10, 10)
        plantillas = copy.deepcopy(FLOTA)
        flota_falsa = [{"nombre": "Test", "coordenadas": [(0, 0)]}]
        entradas = iter(["1"])
        monkeypatch.setattr("builtins.input", lambda _: next(entradas))
        with patch.object(main, "colocar_flota_manual", return_value=flota_falsa) as mock_fn:
            resultado = main.elegir_colocacion(tablero, plantillas)
            mock_fn.assert_called_once()
            assert resultado == flota_falsa


# ═══════════════════════════════════════════════════════════════════════════════
# mostrar_estado
# ═══════════════════════════════════════════════════════════════════════════════

class TestMostrarEstado:

    def test_muestra_tableros_sin_errores(self, capsys):
        """Muestra los dos tableros sin lanzar excepciones."""
        t1 = crear_tablero(5, 5)
        t2 = crear_tablero(5, 5)
        main.mostrar_estado(t1, t2)
        salida = capsys.readouterr().out
        assert "Tu tablero" in salida
        assert "Tablero rival" in salida

    def test_tablero_rival_oculta_barcos(self, capsys):
        """El tablero rival no muestra la celda 'B' de los barcos."""
        t1 = crear_tablero(5, 5)
        t2 = crear_tablero(5, 5)
        t2[0][0] = BARCO
        main.mostrar_estado(t1, t2)
        salida = capsys.readouterr().out
        seccion_rival = salida.split("Tablero rival")[1]
        # Buscamos "B" rodeada de espacios (la celda del barco), no la letra suelta
        assert "    B    " not in seccion_rival  # celda B visible en el tablero

    def test_tablero_propio_muestra_barcos(self, capsys):
        """El tablero propio sí muestra los barcos."""
        t1 = crear_tablero(5, 5)
        t2 = crear_tablero(5, 5)
        t1[0][0] = BARCO
        main.mostrar_estado(t1, t2)
        salida = capsys.readouterr().out
        lineas = salida.split("Tablero rival")
        assert BARCO in lineas[0]


# ═══════════════════════════════════════════════════════════════════════════════
# procesar_disparo_jugador
# ═══════════════════════════════════════════════════════════════════════════════

class TestProcesarDisparoJugador:

    def _flota_y_tablero(self):
        tablero = crear_tablero(10, 10)
        tablero[0][0] = BARCO
        tablero[0][1] = BARCO
        flota = [{"nombre": "Patrullero", "longitud": 2, "impactos": 0,
                  "hundido": False, "coordenadas": [(0, 0), (0, 1)]}]
        return tablero, flota

    def test_disparo_agua(self, monkeypatch):
        """Devuelve 'agua' al disparar a una celda vacía."""
        tablero, flota = self._flota_y_tablero()
        monkeypatch.setattr("main.pedir_coordenadas", lambda _: (5, 5))
        resultado = main.procesar_disparo_jugador(tablero, flota, "Jugador")
        assert resultado == "agua"

    def test_disparo_tocado(self, monkeypatch):
        """Devuelve 'tocado' al impactar un barco sin hundirlo."""
        tablero, flota = self._flota_y_tablero()
        monkeypatch.setattr("main.pedir_coordenadas", lambda _: (0, 0))
        resultado = main.procesar_disparo_jugador(tablero, flota, "Jugador")
        assert resultado == "tocado"

    def test_disparo_hundido(self, monkeypatch):
        """Devuelve 'hundido' al impactar el último segmento del barco."""
        tablero, flota = self._flota_y_tablero()
        # Primer impacto para dejar el barco con 1 impacto
        flota[0]["impactos"] = 1
        tablero[0][0] = ACIERTO  # ya disparado
        monkeypatch.setattr("main.pedir_coordenadas", lambda _: (0, 1))
        resultado = main.procesar_disparo_jugador(tablero, flota, "Jugador")
        assert resultado == "hundido"

    def test_disparo_repetido_devuelve_none(self, monkeypatch):
        """Si la coordenada ya fue disparada, captura el ValueError y devuelve None."""
        tablero, flota = self._flota_y_tablero()
        tablero[0][0] = ACIERTO  # ya disparada
        monkeypatch.setattr("main.pedir_coordenadas", lambda _: (0, 0))
        resultado = main.procesar_disparo_jugador(tablero, flota, "Jugador")
        assert resultado is None

    def test_muestra_numero_disparo(self, monkeypatch, capsys):
        """Con num_disparo, imprime el encabezado del disparo."""
        tablero, flota = self._flota_y_tablero()
        monkeypatch.setattr("main.pedir_coordenadas", lambda _: (5, 5))
        main.procesar_disparo_jugador(tablero, flota, "Jugador", num_disparo="1/3")
        salida = capsys.readouterr().out
        assert "1/3" in salida

    def test_sin_numero_disparo_no_imprime_encabezado(self, monkeypatch, capsys):
        """Sin num_disparo, no imprime el encabezado de disparo."""
        tablero, flota = self._flota_y_tablero()
        monkeypatch.setattr("main.pedir_coordenadas", lambda _: (5, 5))
        main.procesar_disparo_jugador(tablero, flota, "Jugador")
        salida = capsys.readouterr().out
        assert "Disparo" not in salida


# ═══════════════════════════════════════════════════════════════════════════════
# procesar_disparo_cpu
# ═══════════════════════════════════════════════════════════════════════════════

class TestProcesarDisparoCpu:

    def _flota_y_tablero(self):
        tablero = crear_tablero(10, 10)
        tablero[0][0] = BARCO
        tablero[0][1] = BARCO
        flota = [{"nombre": "Patrullero", "longitud": 2, "impactos": 0,
                  "hundido": False, "coordenadas": [(0, 0), (0, 1)]}]
        return tablero, flota

    def test_disparo_cpu_agua(self, monkeypatch):
        """CPU dispara a agua y devuelve 'agua'."""
        tablero, flota = self._flota_y_tablero()
        monkeypatch.setattr("main.cpu_disparo", lambda _: (5, 5))
        resultado = main.procesar_disparo_cpu(tablero, flota)
        assert resultado == "agua"
        assert tablero[5][5] == FALLO

    def test_disparo_cpu_tocado(self, monkeypatch):
        """CPU impacta un barco y devuelve 'tocado'."""
        tablero, flota = self._flota_y_tablero()
        monkeypatch.setattr("main.cpu_disparo", lambda _: (0, 0))
        resultado = main.procesar_disparo_cpu(tablero, flota)
        assert resultado == "tocado"

    def test_disparo_cpu_hundido(self, monkeypatch):
        """CPU hunde el barco al impactar la última celda."""
        tablero, flota = self._flota_y_tablero()
        flota[0]["impactos"] = 1
        tablero[0][0] = ACIERTO
        monkeypatch.setattr("main.cpu_disparo", lambda _: (0, 1))
        resultado = main.procesar_disparo_cpu(tablero, flota)
        assert resultado == "hundido"
        assert flota[0]["hundido"] is True

    def test_muestra_numero_disparo_cpu(self, monkeypatch, capsys):
        """Con num_disparo, imprime el encabezado del disparo de la CPU."""
        tablero, flota = self._flota_y_tablero()
        monkeypatch.setattr("main.cpu_disparo", lambda _: (5, 5))
        main.procesar_disparo_cpu(tablero, flota, num_disparo="2/4")
        salida = capsys.readouterr().out
        assert "2/4" in salida

    def test_imprime_coordenada_disparada(self, monkeypatch, capsys):
        """Imprime la coordenada donde disparó la CPU."""
        tablero, flota = self._flota_y_tablero()
        monkeypatch.setattr("main.cpu_disparo", lambda _: (0, 0))  # fila A, columna 1
        main.procesar_disparo_cpu(tablero, flota)
        salida = capsys.readouterr().out
        assert "A1" in salida


# ═══════════════════════════════════════════════════════════════════════════════
# personalizar_flota
# ═══════════════════════════════════════════════════════════════════════════════

class TestPersonalizarFlota:
    # CELDAS_FLOTA_ESTANDAR = 5+4+4+3+3+2 = 21
    # Secuencia usada en todos los tests:
    #   barco 1: longitud=5, cantidad=3 → 15 celdas
    #   barco 2: longitud=3, cantidad=2 → 6 celdas  (total = 21) ✓
    # IMPORTANTE: el bug del print-de-error-siempre no consume inputs extra porque
    # el while termina en la siguiente iteración (correcto_longitud ya es True),
    # sin pedir otro input.

    def _inputs_flota_valida(self, nombres=("", "")):
        """Genera la secuencia mínima de inputs para llenar exactamente 21 celdas."""
        return iter([
            "5", "3", nombres[0],   # barco 1: long=5, cant=3 → 15 celdas
            "3", "2", nombres[1],   # barco 2: long=3, cant=2 → 6 celdas (total 21)
        ])

    def test_crea_flota_con_celdas_correctas(self, monkeypatch):
        """La flota personalizada tiene exactamente las mismas celdas que la estándar."""
        from Constantes import CELDAS_FLOTA_ESTANDAR
        monkeypatch.setattr("builtins.input", lambda _: next(self._inputs_flota_valida()))
        flota = main.personalizar_flota()
        celdas_total = sum(b["longitud"] * b["cantidad"] for b in flota)
        assert celdas_total == CELDAS_FLOTA_ESTANDAR

    def test_nombre_por_defecto(self, monkeypatch):
        """Si el nombre se deja vacío, se asigna 'Barco N'."""
        monkeypatch.setattr("builtins.input", lambda _: next(self._inputs_flota_valida()))
        flota = main.personalizar_flota()
        assert flota[0]["nombre"] == "Barco 1"
        assert flota[1]["nombre"] == "Barco 2"

    def test_nombre_personalizado(self, monkeypatch):
        """El nombre introducido por el jugador se guarda correctamente."""
        monkeypatch.setattr("builtins.input",
                            lambda _: next(self._inputs_flota_valida(("Fragata", "Corbeta"))))
        flota = main.personalizar_flota()
        assert flota[0]["nombre"] == "Fragata"
        assert flota[1]["nombre"] == "Corbeta"

    def test_devuelve_lista_de_dicts(self, monkeypatch):
        """El resultado es una lista de dicts con nombre, longitud y cantidad."""
        monkeypatch.setattr("builtins.input", lambda _: next(self._inputs_flota_valida()))
        flota = main.personalizar_flota()
        for barco in flota:
            assert "nombre" in barco
            assert "longitud" in barco
            assert "cantidad" in barco


# ═══════════════════════════════════════════════════════════════════════════════
# main (bucle principal)
# ═══════════════════════════════════════════════════════════════════════════════

class TestMain:

    def test_opcion_5_sale_directamente(self, monkeypatch):
        """La opción 5 termina el programa sin preguntar si jugar otra vez."""
        monkeypatch.setattr("main.elegir_modo_juego", lambda: 5)
        # Si llega a pedir input, el test falla con StopIteration
        monkeypatch.setattr("builtins.input", lambda _: (_ for _ in ()).throw(
            AssertionError("No debería pedir input tras opción 5")))
        main.main()  # no debe lanzar excepción

    def test_opcion_4_muestra_ranking(self, monkeypatch):
        """La opción 4 llama a mostrar_ranking."""
        opciones = iter([4, 5])
        monkeypatch.setattr("main.elegir_modo_juego", lambda: next(opciones))
        monkeypatch.setattr("builtins.input", lambda _: "n")
        with patch.object(main, "mostrar_ranking") as mock_ranking:
            main.main()
            mock_ranking.assert_called_once()

    def test_respuesta_no_sale(self, monkeypatch):
        """Responder 'n' a '¿jugar otra partida?' termina el programa."""
        monkeypatch.setattr("main.elegir_modo_juego", lambda: 4)
        monkeypatch.setattr("main.mostrar_ranking", lambda: None)
        monkeypatch.setattr("builtins.input", lambda _: "n")
        main.main()  # debe terminar sin bucle infinito

    def test_respuesta_si_vuelve_a_jugar(self, monkeypatch):
        """Responder 's' hace una segunda iteración del bucle principal."""
        llamadas = {"count": 0}

        def modo_juego_alternante():
            llamadas["count"] += 1
            return 5 if llamadas["count"] > 1 else 4

        monkeypatch.setattr("main.elegir_modo_juego", modo_juego_alternante)
        monkeypatch.setattr("main.mostrar_ranking", lambda: None)
        entradas = iter(["s", "n"])
        monkeypatch.setattr("builtins.input", lambda _: next(entradas))
        main.main()
        assert llamadas["count"] == 2

    def test_opcion_1_llama_juego_vs_cpu(self, monkeypatch):
        """La opción 1 llama a juego_vs_cpu."""
        opciones = iter([1, 5])
        monkeypatch.setattr("main.elegir_modo_juego", lambda: next(opciones))
        monkeypatch.setattr("builtins.input", lambda _: "n")
        with patch.object(main, "juego_vs_cpu") as mock_fn:
            main.main()
            mock_fn.assert_called_once()

    def test_opcion_2_llama_juego_vs_jugador(self, monkeypatch):
        """La opción 2 llama a juego_vs_jugador."""
        opciones = iter([2, 5])
        monkeypatch.setattr("main.elegir_modo_juego", lambda: next(opciones))
        monkeypatch.setattr("builtins.input", lambda _: "n")
        with patch.object(main, "juego_vs_jugador") as mock_fn:
            main.main()
            mock_fn.assert_called_once()

    def test_opcion_3_llama_juego_salvas(self, monkeypatch):
        """La opción 3 llama a elegir_modo_salvas y luego a juego_salvas."""
        opciones = iter([3, 5])
        monkeypatch.setattr("main.elegir_modo_juego", lambda: next(opciones))
        monkeypatch.setattr("main.elegir_modo_salvas", lambda: "PvCPU")
        monkeypatch.setattr("builtins.input", lambda _: "n")
        with patch.object(main, "juego_salvas") as mock_fn:
            main.main()
            mock_fn.assert_called_once_with("PvCPU")
