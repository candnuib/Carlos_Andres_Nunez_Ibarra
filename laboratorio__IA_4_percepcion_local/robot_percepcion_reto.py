import argparse
import json
import os
import random
import re
import time

# ==========================================================
# 1. CONFIGURACION DEL PROBLEMA
# ==========================================================
COMANDOS = ("U", "D", "L", "R")
ORDEN_SENSORES = ("U", "D", "L", "R")
MEMORIA_ACCION = {"U": 0, "D": 1, "L": 2, "R": 3, None: 0}

TAMANO = 8
INICIO = (0, 0)
META = (7, 7)

OBSTACULOS = {
    (0, 3), (1, 3), (2, 0), (2, 2), (2, 3),
    (4, 5), (5, 2), (5, 3), (5, 4), (6, 6),
}

# Modificación 4: Segunda distribución
OBSTACULOS_2 = {
    (1, 1), (1, 4), (2, 1), (3, 4), (4, 4),
    (5, 6), (6, 2), (6, 3), (6, 4)
}

# Modificación 1 y 2: ADN expandido (4 bits sensores + 2 bits meta + 2 bits memoria)
LONGITUD_ADN = 256 
# Modificación 3: Incremento de pasos para permitir ver ciclos completos
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
# 2. PERCEPCION Y SIMULACION DEL ENTORNO
# ==========================================================
def limpiar_pantalla():
    os.system("cls" if os.name == "nt" else "clear")

def destino_de(posicion, comando):
    fila, columna = posicion
    cambios = {"U": (-1, 0), "D": (1, 0), "L": (0, -1), "R": (0, 1)}
    cf, cc = cambios[comando]
    return fila + cf, columna + cc

def esta_bloqueada(posicion, obstaculos):
    fila, columna = posicion
    return not (0 <= fila < TAMANO and 0 <= columna < TAMANO) or posicion in obstaculos

def observar(posicion, ultima_accion, obstaculos):
    # Sensores locales (4 bits)
    sensores = 0
    for comando in ORDEN_SENSORES:
        sensores <<= 1
        sensores |= int(esta_bloqueada(destino_de(posicion, comando), obstaculos))
    
    # Meta (2 bits)
    meta_abajo = 1 if META[0] >= posicion[0] else 0
    meta_derecha = 1 if META[1] >= posicion[1] else 0
    meta = (meta_abajo << 1) | meta_derecha
    
    # Memoria (2 bits)
    memoria = MEMORIA_ACCION[ultima_accion]
    
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
    observaciones = []
    acciones = []
    choques = 0
    pasos_utiles = 0
    ultima_accion = None

    for _ in range(PASOS_MAXIMOS):
        observacion = observar(posicion, ultima_accion, obstaculos)
        comando = adn[observacion]
        nueva_posicion, resultado = mover(posicion, comando, obstaculos)
        
        observaciones.append(observacion)
        acciones.append(comando)
        
        if resultado in ("borde", "obstaculo"):
            choques += 1
        if resultado == "avance":
            pasos_utiles += 1
            
        ultima_accion = comando
        posicion = nueva_posicion
        trayectoria.append(posicion)
        
        if posicion == META:
            break

    return trayectoria, choques, pasos_utiles, observaciones, acciones


# ==========================================================
# 3. REGLA DE SUPERVIVENCIA: EL FITNESS
# ==========================================================
def evaluar(adn):
    trayectoria, choques, pasos_utiles, _, _ = recorrer(adn, OBSTACULOS)
    posicion = trayectoria[-1]
    distancia = abs(META[0] - posicion[0]) + abs(META[1] - posicion[1])
    visitas_repetidas = len(trayectoria) - len(set(trayectoria))

    puntaje = 1000
    puntaje -= distancia * 40
    puntaje += pasos_utiles * 5
    puntaje -= choques * 25
    puntaje -= visitas_repetidas * 40

    if posicion == META:
        puntaje += 2000
    return puntaje

def diversidad(poblacion):
    return len({"".join(adn) for adn in poblacion})

def reglas_de_politica(adn):
    return {f"{indice:08b}": comando for indice, comando in enumerate(adn)}


# ==========================================================
# 4. OPERADORES GENETICOS
# ==========================================================
def mutar(adn, tasa_mutacion, rng):
    return [rng.choice(COMANDOS) if rng.random() < tasa_mutacion else c for c in adn]

def cruzar(primer_padre, segundo_padre, rng):
    punto = rng.randint(1, len(primer_padre) - 1)
    return primer_padre[:punto] + segundo_padre[punto:]


# ==========================================================
# 5. CICLO EVOLUTIVO
# ==========================================================
def evolucionar(tasa_mutacion, usar_cruce, semilla, maximo_generaciones=2000):
    rng = random.Random(semilla)
    poblacion = [[rng.choice(COMANDOS) for _ in range(LONGITUD_ADN)] for _ in range(TAMANO_POBLACION)]
    historial = []

    for generacion in range(maximo_generaciones + 1):
        poblacion.sort(key=evaluar, reverse=True)
        mejor = poblacion[0]
        puntaje = evaluar(mejor)
        trayectoria, choques, pasos_utiles, _, _ = recorrer(mejor, OBSTACULOS)
        historial.append((generacion, puntaje, diversidad(poblacion)))

        if trayectoria[-1] == META:
            return resultado(usar_cruce, mejor, generacion, puntaje, diversidad(poblacion), choques, pasos_utiles, historial, poblacion)

        nueva_poblacion = [robot[:] for robot in poblacion[:ELITE]]
        while len(nueva_poblacion) < TAMANO_POBLACION:
            primer_padre = rng.choice(poblacion[:PADRES])
            if usar_cruce:
                segundo_padre = rng.choice(poblacion[:PADRES])
                hijo = cruzar(primer_padre, segundo_padre, rng)
            else:
                hijo = primer_padre[:]
            nueva_poblacion.append(mutar(hijo, tasa_mutacion, rng))
        poblacion = nueva_poblacion

    poblacion.sort(key=evaluar, reverse=True)
    mejor = poblacion[0]
    trayectoria, choques, pasos_utiles, _, _ = recorrer(mejor, OBSTACULOS)
    return resultado(usar_cruce, mejor, maximo_generaciones, evaluar(mejor), diversidad(poblacion), choques, pasos_utiles, historial, poblacion)

def resultado(usar_cruce, adn, generacion, puntaje, diversidad_final, choques, pasos_utiles, historial, poblacion):
    trayectoria, _, _, _, _ = recorrer(adn, OBSTACULOS)
    return {
        "metodo": "mutacion + cruce" if usar_cruce else "solo mutacion",
        "adn": adn,
        "generacion": generacion,
        "puntaje": puntaje,
        "diversidad": diversidad_final,
        "choques": choques,
        "pasos_utiles": pasos_utiles,
        "llego": trayectoria[-1] == META,
        "historial": historial,
        "poblacion": [robot[:] for robot in poblacion],
    }


# ==========================================================
# 6. CLI Y TABLAS
# ==========================================================
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--modo", choices=("comparar", "mutacion", "cruce"), default="comparar")
    parser.add_argument("--semilla", type=int, default=7)
    args = parser.parse_args()

    experimentos = {
        "mutacion": ("solo mutacion", False),
        "cruce": ("mutacion + cruce", True),
    }
    modos = tuple(experimentos) if args.modo == "comparar" else (args.modo,)
    resultados = []

    for indice, modo in enumerate(modos):
        _, usar_cruce = experimentos[modo]
        print(f"Evolucionando: {experimentos[modo][0]}...")
        resultado_actual = evolucionar(tasa_mutacion=0.08, usar_cruce=usar_cruce, semilla=args.semilla + indice)
        resultados.append(resultado_actual)

    if len(resultados) == 2:
        print("\n=== MAPA 1 (ENTRENAMIENTO) ===")
        print("Metodo              Llego  Generaciones  Puntaje  Choques  Diversidad")
        print("---------------------------------------------------------------------")
        for res in resultados:
            llego = "si" if res["llego"] else "no"
            print(f"{res['metodo']:<20}{llego:<7}{res['generacion']:<14}{res['puntaje']:<9}{res['choques']:<9}{res['diversidad']}/{TAMANO_POBLACION}")

        print("\n=== MAPA 2 (GENERALIZACIÓN) ===")
        print("Metodo              Llego  Pasos Utiles  Choques")
        print("------------------------------------------------")
        for res in resultados:
            # Evaluamos la misma política en el Mapa 2
            tray_2, choques_2, pasos_2, _, _ = recorrer(res['adn'], OBSTACULOS_2)
            llego_2 = "si" if tray_2[-1] == META else "no"
            print(f"{res['metodo']:<20}{llego_2:<7}{pasos_2:<14}{choques_2:<9}")

if __name__ == "__main__":
    main()
