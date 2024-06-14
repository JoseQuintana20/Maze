import time
from globales import candado
import random
from grafo import Grafo
from labyrinth import Labyrinth
import threading
import json

# Macro expansions - sort of
ROWS = 4
COLUMNS =4
# Parametros de Inicio y Fin
start = 10
end = 10

# Paso #2: Leer el archivo de grafo.json y mostrar el laberinto en la pantalla.
# Paso #3: Implementar los algoritmos de Prim para encontrar el camino más corto entre dos nodos del laberinto.
# Paso #4: Mostrar el resultado de los algoritmos en el laberinto.

# Paso #2:
# Leer el archivo de grafo.json y mostrar el laberinto en la pantalla.

def read_graph():
    """
    Esta función lee el archivo de grafo.json y muestra el laberinto en la pantalla. Para luego solucionarlo con los algoritmos de Prim, Kruskal y Dijkstra.
    Returns:

    """
    # Mostrar el laberinto en la pantalla
    maze = Labyrinth(ROWS, COLUMNS,  path=r'C:\Users\Usuario\Desktop\grafo.json')
    maze.start()

def load_graph(filepath):
    """
    Esta función carga el grafo desde un archivo JSON.
    :param filepath: Ruta del archivo JSON.
    :return: Grafo como diccionario.
    """
    with open(filepath, 'r') as file:
        grafo = json.load(file)
        # Creo un objeto Grafo
        grafo_objeto = Grafo(V=grafo["V"], E=grafo["E"], turtle=grafo["turtle"])
    return grafo_objeto


# Paso #3: Implementar los algoritmos de Prim, Kruskal y Dijkstra para encontrar el camino más corto entre dos nodos del laberinto.

def prim(grafo, start):
    V = grafo.V
    E = grafo.E

    # Aseguramos que start sea una cadena
    start = str(start)

    key = {v: float('inf') for v in V}
    pi = {v: None for v in V}
    key[start] = 0
    in_queue = {v: True for v in V}
    Q = list(V.keys())

    while Q:
        # Extract-Min: Find the vertex with the smallest key value
        u = min(Q, key=lambda vertex: key[vertex])
        Q.remove(u)
        in_queue[u] = False

        for v in V[u]:
            v = str(v)  # Aseguramos que v sea una cadena
            edge = f'({u}, {v})' if f'({u}, {v})' in E else f'({v}, {u})'
            weight = E[edge]

            if in_queue[v] and weight < key[v]:
                key[v] = weight
                pi[v] = u

    return pi


def kruskal(grafo):
    V = grafo.V
    E = grafo.E
    edges = sorted(E.items(), key=lambda item: item[1])
    mst = {v: None for v in V}
    parent = {v: v for v in V}

    # def find(v):
    #     if parent[v] != v:
    #         parent[v] = find(parent[v])
    #     return parent[v]

    # def union(u, v):
    #     root_u = find(u)
    #     root_v = find(v)
    #     if root_u != root_v:
    #         parent[root_v] = root_u

    for (u_v, weight) in edges:
        u, v = map(str.strip, u_v.strip("()").split(","))
        if parent[u] != parent[v]:
            mst[v] = u
            #union(u, v)

    return mst


def dijkstra(grafo, start):
    V = grafo.V
    E = grafo.E
    start = str(start)

    key = {v: float('inf') for v in V}
    pi = {v: None for v in V}
    key[start] = 0
    in_queue = {v: True for v in V}
    Q = list(V.keys())

    while Q:
        u = min(Q, key=lambda vertex: key[vertex])
        Q.remove(u)
        in_queue[u] = False

        for v in V[u]:
            v = str(v)
            edge = f'({u}, {v})' if f'({u}, {v})' in E else f'({v}, {u})'
            weight = E[edge]

            if in_queue[v] and key[u] + weight < key[v]:
                key[v] = key[u] + weight
                pi[v] = u

    return pi



def solve_laberynth():
    """
    Esta función resuelve el laberinto con los algoritmos de Prim, Kruskal y Dijkstra.
    Returns:

    """
    # Leer el archivo de grafo.json
    grafo = load_graph(r'C:\Users\Usuario\Desktop\grafo.json')
    mst_1 = prim(grafo, start)
    print("Camino encontrado por Prim:", mst_1)

    mst_2 = kruskal(grafo)
    print("Camino encontrado por Kruskal:", mst_2)

    mst_3 = dijkstra(grafo, start)
    print("Camino encontrado por Dijkstra:", mst_3)
    print()


    def ruta(mst, goal):
        # Inicializar una lista para almacenar el camino
        path = []

        # Comenzar desde la celda objetivo y seguir las conexiones hacia atrás hasta la celda de inicio
        current = goal
        while current is not None:
            path.append(current)
            current = mst[current]

        # Invertir la lista para obtener el camino desde el inicio hasta el objetivo
        path.reverse()
        return path

    # for para encontrar el camino desde el punto de inicio hasta el punto final de cada una de las soluciones de los algoritmos
    # Encontrar el camino desde la celda '10' hasta la celda '15'
    # Definir nombres de algoritmos
    nombres = ["Prim", "Kruskal", "Dijkstra"]

    # Encontrar el camino desde el nodo de inicio hasta el nodo final para cada algoritmo
    goal = '15'
    for nombre, mst in zip(nombres, [mst_1, mst_2, mst_3]):
        # Imprimir el camino encontrado por cada algoritmo
        print(f"Camino encontrado por {nombre}:", ruta(mst, goal))

    ruta = ruta(mst_1, goal)
    # Mover la tortuga a lo largo del camino encontrado por Prim
    # Tortuga en la celda de inicio
    grafo.turtle[start] = start
    # Actualizar la posición de la tortuga en la celda de inicio
    with candado:
        grafo.send_graph()
    # Esperar un segundo
    time.sleep(1)
    grafo.turtle.pop(start)
    for i in range(len(ruta) - 1):
        print(f"La tortuga se mueve de la celda {ruta[i]} a la celda {ruta[i + 1]}")
        grafo.turtle[ruta[i]] = ruta[i + 1]
        # Enviar el grafo a la cola
        with candado:
            grafo.send_graph()
        # Esperar un segundo
        time.sleep(1)
        # Borrar tortuga de la actual anterior
        grafo.turtle.pop(ruta[i])
    # Tortuga en la celda final
    grafo.turtle[ruta[-1]] = ruta[-1]
    # Actualizar la posición de la tortuga en la última celda
    with candado:
        grafo.send_graph()
    # Esperar un segundo
    time.sleep(1)
    grafo.turtle.pop(ruta[-1])




if __name__ == '__main__':
    # Crear dos hilos para ejecutar las funciones create_labyrinth y recursive_backtracker concurrentemente

    # En un hilo se leé el archivo de grafo.json y se muestra el laberinto en la pantalla. Para luego solucionarlo con los algoritmos de Prim, Kruskal y Dijkstra.
    # La función read_graph se ejecuta en un hilo separado
    hilo1 = threading.Thread(target=read_graph)
    hilo1.start()  # Inicia el hilo

    # La función solve_laberynth se ejecuta en un hilo separado
    hilo2 = threading.Thread(target=solve_laberynth)
    hilo2.start()

    # Espera a que los hilos terminen
    hilo2.join()
    hilo1.join()