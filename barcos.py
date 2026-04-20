import random
from Constantes import *
from tablero import saber_coordenada_valida
def funcion_auxiliar(orientacion,fila,columna,i):
    if orientacion == "h": #si es orizontal en cada columna
        fila_actual = fila
        columna_actual = columna + i
    else:
        fila_actual = fila + i #si es vertical en cada fila
        columna_actual = columna
    return fila_actual,columna_actual
    


def saber_posicion_valida(tablero, fila, columna, longitud, orientacion): #función que comprueba si la posición es válida
    for i in range(longitud): #mira en cada columna o fila del barco según su longitud
        fila_actual, columna_actual = funcion_auxiliar(orientacion,fila,columna,i) #para hacer el code DRY he creado la funcion auxiliar
        if not saber_coordenada_valida(tablero, fila_actual, columna_actual): #comprueba cada coordenada individualmente si está dentro del tablero
            return False
        if tablero[fila_actual][columna_actual] != AGUA: #comprueba que no esté ocupada
            return False
    return True #al pasar todas las comprobaciones devuelve true si alguna no pasa devuelve false


def colocar_barco(tablero, fila, columna, longitud, orientacion, barco): 
    #Coloca un barco en el tablero y guarda sus coordenadas en el diccionario del barco.
    #si no cuando había dos barcos se guardaban solo las coordenadas de 1, ha sido un problema del que nos hemos dado cuenta tarde y ha sido díficil arreglar
    if not saber_posicion_valida(tablero, fila, columna, longitud, orientacion): # comprueba la posición del barco
        raise ValueError("Posición del barco no válida")
    barco["coordenadas"] = []
    for i in range(longitud): #coloca el barco según orientación misma lógica que la función anterior
        fila_actual, columna_actual = funcion_auxiliar(orientacion,fila,columna,i)
        tablero[fila_actual][columna_actual] = BARCO #sustituye agua por barco en cada coordenada
        barco["coordenadas"].append((fila_actual, columna_actual)) #guarda las coordenadas del barco en su diccionario


def crear_instancia_barco(plantilla):
    #Crea un diccionario independiente para un barco individual a partir de su plantilla.
    #Nuestra solución para el problema anterior de varios barcos, permite que dos barcos iguales tengan coordenadas propias
    #simplemente cuando se envía la flota se recibe como plantillas y cada barco se nombra como plantilla y aquí se crea su propia identidad
    #así lo explicaría yo
    return {
        "nombre": plantilla["nombre"],
        "longitud": plantilla["longitud"],
        "impactos": 0,
        "hundido": False,
        "coordenadas": []
    }


def colocar_flota_aleatoria(tablero, plantillas):
    #coloca todos los barcos de la flota en posiciones aleatorias válidas.
    #crea de cada barco ahora (plantilla) su instancia para colocarla sin que se solapen en el caso de que hayan varios barcos del mismo tipo
    
    n_filas = len(tablero) - 1
    n_columnas = len(tablero[0]) - 1
    flota_activa = []

    for plantilla in plantillas: #por cada barco en la flota de hace plantilla
        for _ in range(plantilla["cantidad"]): # por cada barco individual en caso de haber varios del mismo tipo
            instancia = crear_instancia_barco(plantilla) #se crea la instancia
            colocado = False
            while not colocado: #este while es para que si lo coloca en una posición no válida lo reintente
                fila = random.randint(0, n_filas) #se coloca de forma aleatoria su posicion y su orientación
                columna = random.randint(0, n_columnas)
                orientacion = random.choice(["h", "v"])
                try:
                    colocar_barco(tablero, fila, columna, plantilla["longitud"], orientacion, instancia) # coloca
                    colocado = True
                except ValueError:
                    pass #si falla repite
            flota_activa.append(instancia) #la flota activa es la flota real con cada "identidad" saca de su plantilla

    return flota_activa


def colocar_flota_manual(tablero, plantillas, pedir_coordenadas_fn, pedir_orientacion_fn, mostrar_tablero_fn):
    #coloca los barcos de la flota manualmente pidiendo inputs al jugador,
    flota_activa = [] 
    mostrar_tablero_fn(tablero)
    #no importo las funciones y las pido como dato porque solo se usan aquí 
    for plantilla in plantillas: #misma lógica plantilla por cada barco usando flota como plantillas
        for i in range(plantilla["cantidad"]):
            numero = f" ({i+1}/{plantilla['cantidad']})" if plantilla["cantidad"] > 1 else "" #este prin es para que sepas por que barco vas y cuantos te quedan
            print(f"\nColocando {plantilla['nombre']}{numero} — longitud {plantilla['longitud']}") #para que sepas que barco estás colocando
            instancia = crear_instancia_barco(plantilla) #instancia para barco...
            colocado = False 
            while not colocado: #colocar el barco
                fila, columna = pedir_coordenadas_fn(tablero)
                orientacion = pedir_orientacion_fn()
                try:
                    colocar_barco(tablero, fila, columna, plantilla["longitud"], orientacion, instancia) #colocas el barco
                    mostrar_tablero_fn(tablero)
                    colocado = True
                except ValueError as e:
                    print(f"Error: {e}. Inténtalo de nuevo.") #si colocas en posición no válida intentas de nuevo
            flota_activa.append(instancia)

    return flota_activa #tu flota con instancias