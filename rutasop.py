import heapq  # Librería para trabajar con colas de prioridad
import random  # Librería para generar números aleatorios

# Inicializa un mapa de tamaño dado con todos los valores a 0
def inicializar_mapa(tamano=10):
    return [[0]*tamano for _ in range(tamano)]

# Calcula la distancia Manhattan entre dos puntos (a y b)
def heuristica(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# Implementa el algoritmo A* para encontrar la ruta más corta en un mapa con obstáculos
def A_STARLOG(mapa, inicio, objetivo):
    filas, columnas = len(mapa), len(mapa[0])  # Obtiene el número de filas y columnas del mapa
    frontera, came_from, costo_hasta_ahora = [(0, inicio)], {inicio: None}, {inicio: 0}  # Inicializa las estructuras de datos
    abiertos = {inicio}  # Conjunto de nodos abiertos (por explorar)
    
    while frontera:  # Mientras haya nodos en la frontera
        _, actual = heapq.heappop(frontera)  # Extrae el nodo con menor costo
        abiertos.discard(actual)  # Remueve el nodo de los abiertos
        
        if actual == objetivo:  
            break
        
        # Recorre los vecinos del nodo actual
        for delta_f, delta_c in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            vecino = (actual[0] + delta_f, actual[1] + delta_c)
            if 0 <= vecino[0] < filas and 0 <= vecino[1] < columnas:  # Verifica que el vecino esté dentro del mapa
                nuevo_costo = costo_hasta_ahora[actual] + costo_terreno[mapa[vecino[0]][vecino[1]]]
                if vecino not in costo_hasta_ahora or nuevo_costo < costo_hasta_ahora[vecino]:  # Si el vecino es nuevo o se encontró un costo menor
                    costo_hasta_ahora[vecino] = nuevo_costo  # Actualiza el costo
                    heapq.heappush(frontera, (nuevo_costo + heuristica(objetivo, vecino), vecino))  # Añade el vecino a la frontera con su prioridad
                    abiertos.add(vecino)  # Añade el vecino a los abiertos
                    came_from[vecino] = actual  # Registra el nodo desde el cual llegamos al vecino
    
    actual, ruta = objetivo, []  # Inicializa la ruta desde el objetivo
    while actual:  # Reconstruye la ruta desde el objetivo hasta el inicio
        ruta.append(actual)
        actual = came_from.get(actual)
    return ruta[::-1]  # Devuelve la ruta en el orden correcto

# Imprime el mapa con la ruta optimizada
def imprimir_mapa(mapa, ruta):
    simbolos = {0: '.', 1: 'E', 2: 'A', 3: 'B'}  # Define símbolos para los diferentes tipos de terreno
    for r, c in ruta:
        mapa[r][c] = '*'  # Marca la ruta con '*'
    
    # Imprime referencias de columnas
    print("   " + " ".join(map(str, range(len(mapa[0])))))
    print("  " + "---" * len(mapa[0]))
    
    for idx, fila in enumerate(mapa):
        # Imprime referencia de fila y la fila del mapa
        print(f"{idx}| " + " ".join(simbolos.get(celda, str(celda)) for celda in fila))

# Agrega obstáculos en el mapa en las coordenadas especificadas
def agregar_obstaculos(mapa, obstaculos):
    for r, c, tipo in obstaculos:
        if 0 <= r < len(mapa) and 0 <= c < len(mapa[0]):
            mapa[r][c] = tipo  # Coloca el tipo de obstáculo en la coordenada especificada
    return mapa

# Solicita y verifica coordenadas del usuario
def solicitar_coordenadas(tipo, mapa, es_obstaculo=False, inicio=None, objetivo=None):
    while True:
        try:
            if es_obstaculo:
                r, c, tipo_obstaculo = map(int, input(f"Ingresa las coordenadas y tipo del {tipo} (fila columna tipo): ").split())
                if (r, c) not in {inicio, objetivo} and 0 <= r < len(mapa) and 0 <= c < len(mapa[0]) and tipo_obstaculo in {1, 2, 3}:
                    return r, c, tipo_obstaculo  # Verifica que el obstáculo no esté en el inicio o destino y que sea válido
            else:
                r, c = map(int, input(f"Ingresa las coordenadas del {tipo} (fila columna): ").split())
                if 0 <= r < len(mapa) and 0 <= c < len(mapa[0]) and mapa[r][c] == 0:
                    return r, c  # Verifica que las coordenadas sean válidas y no haya obstáculo
        except ValueError:
            pass  # Si ocurre un error de valor, ignora la entrada y solicita nuevamente
        print("Entrada no válida. Por favor, intenta de nuevo.")

# Variables y constantes
costo_terreno = {0: 1, 1: float('inf'), 2: 2, 3: 3}  # Define los costos para cada tipo de terreno
unmodified_map = inicializar_mapa()  # Inicializa el mapa

# Solicita al usuario el punto de partida y el destino final
inicio = solicitar_coordenadas("punto de partida", unmodified_map)
objetivo = solicitar_coordenadas("destino final", unmodified_map)

# Solicita obstáculos al usuario
obstaculos_usuario = []
while True:
    obstaculo = solicitar_coordenadas("obstáculo", unmodified_map, es_obstaculo=True, inicio=inicio, objetivo=objetivo)
    obstaculos_usuario.append(obstaculo)
    if input("¿Deseas agregar otro obstáculo? (si/no): ").lower() != 'si':
        break

# Añade obstáculos aleatorios
def agregar_obstaculos_aleatorios(mapa, num_obstaculos):
    obstaculos_aleatorios = []
    for _ in range(num_obstaculos):
        while True:
            r, c = random.randint(0, len(mapa)-1), random.randint(0, len(mapa[0])-1)
            tipo = random.choice([1, 2, 3])
            if (r, c) not in {inicio, objetivo} and mapa[r][c] == 0:
                obstaculos_aleatorios.append((r, c, tipo))
                break
    return agregar_obstaculos(mapa, obstaculos_aleatorios)

# Agrega un número determinado de obstáculos aleatorios al mapa
mapa_con_obstaculos = agregar_obstaculos([fila[:] for fila in unmodified_map], obstaculos_usuario)
mapa_con_obstaculos = agregar_obstaculos_aleatorios(mapa_con_obstaculos, 10)  # Aquí se define cuántos obstáculos aleatorios agregar

print("Mapa con obstáculos:")
imprimir_mapa(mapa_con_obstaculos, [])

# Calcula la ruta óptima y la imprime
ruta = A_STARLOG(mapa_con_obstaculos, inicio, objetivo)
print("Mapa con obstáculos y ruta optimizada:")
imprimir_mapa(mapa_con_obstaculos, ruta)
