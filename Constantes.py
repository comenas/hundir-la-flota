# Símbolos del tablero
AGUA = "~"
FALLO = "O"
ACIERTO = "X"
BARCO = "B"

# Tamaño del tablero
TAMAÑO_DEFAULT_FILAS = 10
TAMAÑO_DEFAULT_COLUMNAS = 10
TAMAÑO_MAX_FILAS = 15
TAMAÑO_MAX_COLUMNAS = 15
TAMAÑO_MIN_FILAS = 5
TAMAÑO_MIN_COLUMNAS = 5

# Valores de los barcos
VALORES_FLOTA_POR_DEFECTO = [
    {"nombre": "Portaaviones", "longitud": 5, "impactos": 0, "hundido": False, "cantidad": 1},
    {"nombre": "Acorazado",    "longitud": 4, "impactos": 0, "hundido": False, "cantidad": 2},
    {"nombre": "Destructor",   "longitud": 3, "impactos": 0, "hundido": False, "cantidad": 1},
    {"nombre": "Submarino",    "longitud": 3, "impactos": 0, "hundido": False, "cantidad": 1},
    {"nombre": "Patrullero",   "longitud": 2, "impactos": 0, "hundido": False, "cantidad": 1},
]
#nombre = nombre del barco
# longitud es el tamaño del barco
#impactos es el número de impactos recibidos(para saber cuando hundirlo)
#hundido hace falta en el modo Salvas y para saber cuando termina el
#cantidad es por personalizar la flota cuantos barcos hay de cada