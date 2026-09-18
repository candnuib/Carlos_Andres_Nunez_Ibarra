import os
import random
import time

# ==========================================================
# 1. CONFIGURACIÓN DEL PROBLEMA (MODIFICADO)
# ==========================================================
COMANDOS = ("U", "D", "L", "R")
ORDEN_SENSORES = ("U", "D", "L", "R")
# Mapeo de memoria para la última acción (2 bits)
MEMORIA_ACCION = {"U": 0, "D": 1, "L": 2, "R": 3, None: 0}

TAMANO = 8
INICIO = (0, 0)
META = (7, 7)

OBSTACULOS = {
    (0, 3), (1, 3), (2, 0), (2, 2), (2, 3),
    (4, 5), (5, 2), (5, 3), (5, 4), (6, 6),
}

# MODIFICACIÓN 4: Segunda distribución de obstáculos para comparar
OBSTACULOS_2 = {
    (1, 1), (1, 4), (2, 1), (3, 4), (4, 4),
    (5, 6), (6, 2), (6, 3), (6, 4)
}

# MODIFICACIÓN 1 y 2: ADN expandido
# 4 bits (sensores) + 2 bits (cuadrante meta) + 2 bits (última acción) = 8 bits -> 256 combinaciones
LONGITUD_ADN = 256 

# MODIFICACIÓN 3: Más pasos para permitir trayectorias largas y ver ciclos
PASOS_MAXIMOS = 40 

TAMANO_POBLACION = 100
ELITE = 10
PADRES = 40

EMOJI_ROBOT = "\U0001f916"
EMOJI_META = "\U0001f7e9"
EMOJI_META_ALCANZADA = "\U0001f389"
EMOJI_OBSTACULO = "\u2b1b"
EMOJI_INICIO = "\U0001f535"
EMOJI_LIBRE = "\u2b1c"


# ==========================================================
# 2. PERCEPCIÓN Y SIMULACIÓN DEL ENTORNO (MODIFICADO)
# ==========================================================
def destino_de(posicion, comando):
    fila, columna = posicion
    cambios = {"U": (-1, 0), "D": (1, 0), "L": (0, -1), "R": (0, 1)}
    cf, cc = cambios[comando]
    return fila + cf, columna + cc

def esta_bloqueada(posicion, obstaculos):
    fila, columna = posicion
    return not (0 <= fila < TAMANO and 0 <= columna < TAMANO) or posicion in obstaculos

def observar_estado(posicion, ultima_accion, obstaculos):
    """MODIFICACIÓN 1 y 2: Combina sensores locales, dirección de meta y memoria."""
    # 1. Sensores Locales (4 bits)
    sensores = 0
    for comando in ORDEN_SENSORES:
        sensores <<= 1
        sensores |= int(esta_bloqueada(destino_de(posicion, comando), obstaculos))
    
    # 2. Dirección de la Meta (2 bits: cuadrante relativo)
    # Bit 1: 1 si la meta está más abajo (o igual), 0 si está arriba
    # Bit 0: 1 si la meta está más a la derecha (o igual), 0 si está a la izquierda
    meta_abajo = 1 if META[0] >= posicion[0] else 0
    meta_derecha = 1 if META[1] >= posicion[1] else 0
    meta = (meta_abajo << 1) | meta_derecha
    
    # 3. Memoria de la Última Acción (2 bits)
    memoria = MEMORIA_ACCION[ultima_accion]
    
    # Ensamblar estado de 8 bits: [Sensores: 4] [Meta: 2] [Memoria: 2]
    return (sensores << 4) | (meta << 2) | memoria

def mover(posicion, comando, obstaculos):
    destino = destino_de(posicion, comando)
    if not (0 <= destino[0] < TAMANO and 0 <= destino[1] < TAMANO):
        return posicion, "borde"
    if destino in obstaculos:
        return posicion, "obstaculo"
    return destino, "avance"

def recorrer(adn, obstaculos=OBSTACULOS):
    posicion = INICIO
    trayectoria = [posicion]
    ultima_accion = None
    choques = 0
    pasos_utiles = 0

    for _ in range(PASOS_MAXIMOS):
        # El estado ahora es un entero entre 0 y 255
        estado = observar_estado(posicion, ultima_accion, obstaculos)
        comando = adn[estado]
        
        nueva_posicion, resultado = mover(posicion, comando, obstaculos)
        
        if resultado in ("borde", "obstaculo"):
            choques += 1
        if resultado == "avance":
            pasos_utiles += 1
            
        ultima_accion = comando
        posicion = nueva_posicion
        trayectoria.append(posicion)
        
        if posicion == META:
            break

    return trayectoria, choques, pasos_utiles


# ==========================================================
# 3. EVALUACIÓN Y CICLO EVOLUTIVO (AJUSTADO)
# ==========================================================
def evaluar(adn, obstaculos=OBSTACULOS):
    trayectoria, choques, pasos_utiles = recorrer(adn, obstaculos)
    posicion = trayectoria[-1]
    distancia = abs(META[0] - posicion[0]) + abs(META[1] - posicion[1])
    visitas_repetidas = len(trayectoria) - len(set(trayectoria))

    puntaje = 1000
    puntaje -= distancia * 50
    puntaje += pasos_utiles * 5
    puntaje -= choques * 20
    puntaje -= visitas_repetidas * 40

    if posicion == META:
        puntaje += 3000
    return puntaje

def mutar(adn, tasa_mutacion, rng):
    return [rng.choice(COMANDOS) if rng.random() < tasa_mutacion else c for c in adn]

def cruzar(p1, p2, rng):
    punto = rng.randint(1, len(p1) - 1)
    return p1[:punto] + p2[punto:]

def evolucionar(semilla):
    rng = random.Random(semilla)
    poblacion = [[rng.choice(COMANDOS) for _ in range(LONGITUD_ADN)] for _ in range(TAMANO_POBLACION)]
    
    for generacion in range(500): # Reducido a 500 para rapidez, puedes subirlo
        poblacion.sort(key=lambda adn: evaluar(adn, OBSTACULOS), reverse=True)
        mejor = poblacion[0]
        trayectoria, _, _ = recorrer(mejor, OBSTACULOS)
        
        if trayectoria[-1] == META:
            break
            
        nueva_poblacion = [robot[:] for robot in poblacion[:ELITE]]
        while len(nueva_poblacion) < TAMANO_POBLACION:
            padre1 = rng.choice(poblacion[:PADRES])
            padre2 = rng.choice(poblacion[:PADRES])
            hijo = cruzar(padre1, padre2, rng)
            nueva_poblacion.append(mutar(hijo, 0.05, rng))
        poblacion = nueva_poblacion
        
    poblacion.sort(key=lambda adn: evaluar(adn, OBSTACULOS), reverse=True)
    return poblacion[0]


# ==========================================================
# 4. PRUEBA Y COMPARACIÓN (MODIFICACIÓN 4)
# ==========================================================
def dibujar_mapa(trayectoria, obstaculos, titulo):
    os.system("cls" if os.name == "nt" else "clear")
    print(f"=== {titulo} ===")
    camino = set(trayectoria)
    for fila in range(TAMANO):
        linea = ""
        for columna in range(TAMANO):
            celda = (fila, columna)
            if celda == trayectoria[-1]:
                linea += EMOJI_ROBOT if celda != META else EMOJI_META_ALCANZADA
            elif celda == INICIO: linea += EMOJI_INICIO
            elif celda == META: linea += EMOJI_META
            elif celda in obstaculos: linea += EMOJI_OBSTACULO
            elif celda in camino: linea += "\U0001f7e8" # Cuadro amarillo para el rastro
            else: linea += EMOJI_LIBRE
        print(linea)
    print(f"Pasos tomados: {len(trayectoria)-1}")
    print(f"¿Llegó a la meta?: {'Sí' if trayectoria[-1] == META else 'No'}\n")

if __name__ == "__main__":
    print("Evolucionando política en el Mapa 1...")
    mejor_adn = evolucionar(semilla=42)
    
    # Evaluar en el Mapa 1 original
    trayectoria_1, _, _ = recorrer(mejor_adn, OBSTACULOS)
    dibujar_mapa(trayectoria_1, OBSTACULOS, "MAPA 1 (Entrenamiento)")
    time.sleep(2)
    
    # Evaluar la misma política en el Mapa 2 (Modificación 4)
    trayectoria_2, _, _ = recorrer(mejor_adn, OBSTACULOS_2)
    dibujar_mapa(trayectoria_2, OBSTACULOS_2, "MAPA 2 (Generalización)")
