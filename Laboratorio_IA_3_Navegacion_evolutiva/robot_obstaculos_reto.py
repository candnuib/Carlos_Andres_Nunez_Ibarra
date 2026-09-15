import argparse
import os
import random
import time

# ==========================================================
# 1. CONFIGURACION DEL PROBLEMA
# ==========================================================
COMANDOS = ("U", "D", "L", "R")
TAMANO = 8
INICIO = (0, 0)
META = (7, 7)

OBSTACULOS = {
    (0, 3), (1, 3), (2, 1), (2, 2), (2, 3),
    (3, 5), (4, 5), (5, 2), (5, 3), (5, 4),
    (6, 6),
}

LONGITUD_ADN = 18
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
# 2. SIMULACION DEL ENTORNO
# ==========================================================
def limpiar_pantalla():
    os.system("cls" if os.name == "nt" else "clear")

def mover(posicion, comando):
    fila, columna = posicion
    cambios = {"U": (-1, 0), "D": (1, 0), "L": (0, -1), "R": (0, 1)}
    cambio_fila, cambio_columna = cambios[comando]
    destino = (fila + cambio_fila, columna + cambio_columna)

    if not (0 <= destino[0] < TAMANO and 0 <= destino[1] < TAMANO):
        return posicion, "borde"

    if destino in OBSTACULOS:
        return posicion, "obstaculo"

    return destino, "avance"

def recorrer(adn):
    posicion = INICIO
    trayectoria = [posicion]
    choques = 0
    pasos_utiles = 0

    for comando in adn:
        nueva_posicion, resultado = mover(posicion, comando)
        if resultado == "obstaculo":
            choques += 1
        if resultado == "avance":
            pasos_utiles += 1
        posicion = nueva_posicion
        trayectoria.append(posicion)

    return trayectoria, choques, pasos_utiles

# ==========================================================
# 3. REGLA DE SUPERVIVENCIA: EL FITNESS
# ==========================================================
def evaluar(adn):
    trayectoria, choques, pasos_utiles = recorrer(adn)
    posicion = trayectoria[-1]
    distancia = abs(META[0] - posicion[0]) + abs(META[1] - posicion[1])
    visitas_repetidas = len(trayectoria) - len(set(trayectoria))

    puntaje = 500
    puntaje -= distancia * 35
    puntaje += pasos_utiles * 4
    puntaje -= choques * 30
    puntaje -= visitas_repetidas * 15

    if posicion == META:
        puntaje += 2000
    return puntaje

def diversidad(poblacion):
    return len({"".join(adn) for adn in poblacion})

# ==========================================================
# 4. OPERADORES GENETICOS
# ==========================================================
def mutar(adn, tasa_mutacion, rng):
    return [
        rng.choice(COMANDOS) if rng.random() < tasa_mutacion else comando
        for comando in adn
    ]

def cruzar(primer_padre, segundo_padre, rng):
    punto = rng.randint(1, len(primer_padre) - 1)
    return primer_padre[:punto] + segundo_padre[punto:]

# ==========================================================
# 5. CICLO EVOLUTIVO
# ==========================================================
def evolucionar(tasa_mutacion, usar_cruce, semilla, maximo_generaciones=3000):
    rng = random.Random(semilla)
    poblacion = [
        [rng.choice(COMANDOS) for _ in range(LONGITUD_ADN)]
        for _ in range(TAMANO_POBLACION)
    ]
    historial = []

    for generacion in range(maximo_generaciones + 1):
        poblacion.sort(key=evaluar, reverse=True)
        mejor = poblacion[0]
        puntaje = evaluar(mejor)
        trayectoria, choques, pasos_utiles = recorrer(mejor)
        historial.append((generacion, puntaje, diversidad(poblacion)))

        if trayectoria[-1] == META:
            return resultado(
                usar_cruce, mejor, generacion, puntaje, diversidad(poblacion),
                choques, pasos_utiles, historial,
            )

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
    trayectoria, choques, pasos_utiles = recorrer(mejor)
    return resultado(
        usar_cruce, mejor, maximo_generaciones, evaluar(mejor),
        diversidad(poblacion), choques, pasos_utiles, historial,
    )

def resultado(usar_cruce, adn, generacion, puntaje, diversidad_final,
              choques, pasos_utiles, historial):
    trayectoria, _, _ = recorrer(adn)
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
    }

# ==========================================================
# 6. VISUALIZACION Y CLI
# ==========================================================
def dibujar(resultado, pausa):
    adn = resultado["adn"]
    trayectoria, _, _ = recorrer(adn)

    for paso, posicion in enumerate(trayectoria[1:], start=1):
        limpiar_pantalla()
        print(
            f"{resultado['metodo'].upper()} | "
            f"Gen {resultado['generacion']} | Puntos: {resultado['puntaje']}"
        )
        print(
            f"{EMOJI_ROBOT} = robot | {EMOJI_META_ALCANZADA} = meta alcanzada | "
            f"{EMOJI_META} = meta | {EMOJI_OBSTACULO} = obstaculo"
        )
        print(f"{EMOJI_INICIO} = inicio | {EMOJI_LIBRE} = celda libre\n")
        for fila in range(TAMANO):
            linea = ""
            for columna in range(TAMANO):
                celda = (fila, columna)
                if celda == posicion:
                    linea += EMOJI_ROBOT
                elif celda == INICIO:
                    linea += EMOJI_INICIO
                elif celda == META:
                    linea += EMOJI_META_ALCANZADA if posicion == META else EMOJI_META
                elif celda in OBSTACULOS:
                    linea += EMOJI_OBSTACULO
                else:
                    linea += EMOJI_LIBRE
            print(linea)
        print(
            f"Paso {paso}/{len(adn)} | ADN: {''.join(adn)} | "
            f"Choques: {resultado['choques']}"
        )
        if pausa:
            time.sleep(pausa)

def mostrar_resultado(resultado, pausa):
    dibujar(resultado, pausa)
    estado = "LLEGO" if resultado["llego"] else "NO LLEGO"
    print(f"\nResultado: {estado}")
    print(f"Pasos utiles: {resultado['pasos_utiles']}")
    print(f"Diversidad final: {resultado['diversidad']}/{TAMANO_POBLACION}")
    
    # -------------------------------------------------------------
    # NUEVA SECCIÓN: REPORTE DE EVOLUCIÓN
    # -------------------------------------------------------------
    print("\n--- REGISTRO DE EVOLUCIÓN (Saltos de mejora) ---")
    print(f"{'Gen':<10} | {'Puntuación':<12} | {'Diversidad':<10}")
    print("-" * 40)
    
    mejor_puntaje = -float('inf')
    for gen, puntaje, div in resultado['historial']:
        # Solo imprimimos cuando encontramos un ADN mejor que los anteriores
        if puntaje > mejor_puntaje:
            mejor_puntaje = puntaje
            print(f"{gen:<10} | {puntaje:<12} | {div:<10}")
    print("-" * 40)
    # -------------------------------------------------------------

    if pausa:
        time.sleep(1)

def main():
    parser = argparse.ArgumentParser(
        description="Compara mutacion y cruce en una poblacion de robots."
    )
    parser.add_argument(
        "--modo",
        choices=("comparar", "mutacion", "cruce"),
        default="comparar",
    )
    parser.add_argument("--semilla", type=int, default=7)
    parser.add_argument("--sin-pausa", action="store_true")
    args = parser.parse_args()

    experimentos = {
        "mutacion": ("solo mutacion", False),
        "cruce": ("mutacion + cruce", True),
    }
    modos = tuple(experimentos) if args.modo == "comparar" else (args.modo,)
    resultados = []

    for indice, modo in enumerate(modos):
        _, usar_cruce = experimentos[modo]

        resultado_actual = evolucionar(
            tasa_mutacion=0.08,
            usar_cruce=usar_cruce,
            semilla=args.semilla + indice,
        )
        resultados.append(resultado_actual)
        mostrar_resultado(resultado_actual, 0 if args.sin_pausa else 0.08)

    if len(resultados) == 2:
        print("\nCOMPARACION")
        print("Metodo              Llego   Generaciones  Puntaje  Choques  Diversidad")
        print("-----------------------------------------------------------------------")
        for resultado_actual in resultados:
            llego = "si" if resultado_actual["llego"] else "no"
            print(
                f"{resultado_actual['metodo']:<20}{llego:<8}"
                f"{resultado_actual['generacion']:<14}"
                f"{resultado_actual['puntaje']:<9}"
                f"{resultado_actual['choques']:<9}"
                f"{resultado_actual['diversidad']}/{TAMANO_POBLACION}"
            )

if __name__ == "__main__":
    main()
