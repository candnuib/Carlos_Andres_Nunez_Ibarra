import random
import time
import os


def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')


# ==========================================================
# ZONA DE TRABAJO (LA REGLA DE SUPERVIVENCIA Y ENERGÍA)
# ==========================================================
def evaluar_robot(adn):
    posicion = [0, 0]  # Coordenadas iniciales: [fila, columna]
    
    # Variables de control para las nuevas reglas
    toco_acido = False       # Bandera para detectar si el robot pasa por el pozo [4, 4]
    comandos_superfluos = 0  # Contador de movimientos ineficientes que gastan energía
    tamano = 8
    cubo = [7, 7]            # Coordenadas de la meta

    # El robot ejecuta su secuencia genetica a ciegas
    for comando in adn:
        # Registramos la distancia a la meta antes de movernos
        distancia_antes = abs(cubo[0] - posicion[0]) + abs(cubo[1] - posicion[1])

        if comando == 'U': #UP
            posicion[0] -= 1
        elif comando == 'D': #DOWN
            posicion[0] += 1
        elif comando == 'L': #LEFT
            posicion[1] -= 1
        elif comando == 'R': #RIGTH
            posicion[1] += 1

        # Limitar dentro del tablero (evita que salga de los límites físicos)
        posicion[0] = max(0, min(posicion[0], tamano - 1))
        posicion[1] = max(0, min(posicion[1], tamano - 1))

        # [NUEVO] Verificación paso a paso del pozo de ácido letal
        if posicion == [4, 4]:
            toco_acido = True

        # Registramos la distancia a la meta después del movimiento
        distancia_despues = abs(cubo[0] - posicion[0]) + abs(cubo[1] - posicion[1])

        # [NUEVO] Penalización por ineficiencia energética: 
        # Si el comando aleja al robot de la meta o no aporta, se cuenta como superfluo.
        if distancia_despues > distancia_antes:
            comandos_superfluos += 1

    distancia = abs(cubo[0] - posicion[0]) + abs(cubo[1] - posicion[1])

    # El fitness base premia la proximidad a la meta
    puntaje = 100 - distancia

    # [NUEVO] Aplicar penalización masiva si tocó el ácido
    if toco_acido:
        puntaje -= 50

    # [NUEVO] Restar puntos por cada comando superfluo (gasto de energía vital)
    puntaje -= comandos_superfluos * 2

    return puntaje


# ==========================================================
# MOTOR GRAFICO (NO MODIFICAR)
# ==========================================================
def animar_mejor_robot(adn, generacion, puntaje):
    posicion, cubo, tamano = [0, 0], [7, 7], 8

    for paso, comando in enumerate(adn):
        limpiar_pantalla()
        print(f"Gen {generacion} | Puntos: {puntaje}/100")

        if comando == 'U':
            posicion[0] -= 1
        elif comando == 'D':
            posicion[0] += 1
        elif comando == 'L':
            posicion[1] -= 1
        elif comando == 'R':
            posicion[1] += 1

        posicion[0] = max(0, min(posicion[0], tamano - 1))
        posicion[1] = max(0, min(posicion[1], tamano - 1))

        for fila in range(tamano):
            linea = ""
            for columna in range(tamano):
                if fila == cubo[0] and columna == cubo[1]:
                    linea += "🎉" if posicion == cubo else "🟩"
                elif fila == posicion[0] and columna == posicion[1]:
                    linea += "🤖"
                else:
                    linea += "⬜"
            print(linea)
        time.sleep(0.08)


# ==========================================================
# CICLO EVOLUTIVO (NO MODIFICAR)
# ==========================================================
comandos = ['U', 'D', 'L', 'R']
mejor_robot = "".join(random.choice(comandos) for _ in range(30))
generacion = 0

while evaluar_robot(mejor_robot) < 100:
    robot_mutante = ""
    for gen in mejor_robot:
        robot_mutante += random.choice(comandos) if random.random() < 0.15 else gen

    if evaluar_robot(robot_mutante) > evaluar_robot(mejor_robot):
        mejor_robot = robot_mutante

    generacion += 1
    # Se anima el progreso cada 150 iteraciones
    if generacion % 150 == 0:
        animar_mejor_robot(mejor_robot, generacion, evaluar_robot(mejor_robot))

animar_mejor_robot(mejor_robot, generacion, evaluar_robot(mejor_robot))
