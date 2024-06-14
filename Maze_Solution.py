'''
# Examen 2. Métodos y Modelos Computacionales

Jose Daniel Quintana Fuentes

La generación de un laberinto utiliza una metodología denominada "random spanning trees", o árboles aleatorios de cobertura,
operando sobre grafos planares. Para la primera parte de la tarea, usted generará un laberinto aleatorio utilizando una modificación de DFS llamada "recursive backtracker".

Una descripción simplificada de esta versión de DFS puede ser:
Seleccione una celda de inicio, márquela como visitada y agréguela al stack.
Mientras el stack no esté vacío:
----> Remueva la siguiente celda del stack y hágala la actual.
----> Si la celda tiene vecinos sin visitar:
--------> Agregue la celda actual al stack.
--------> Elija un vecino no visitado de forma aleatoria.
--------> Remueva la pared entre ellos.
--------> Marque el vecino seleccionado como visitado y agréguelo al stack.

SEGUNDA PARTE:

Proponga al menos tres métodos de solución basados en los algoritmos de: Prim, Kruskal y Dijkstra. Compare y concluya acerca de su desempeño y tipo de solución.
'''

# Nota: Es ncesario cambiar la ruta del archivo de grafo.json en la función si el sistema operativo es Linux o Windows.
path = 'C:/Users/Usuario/Desktop/grafo.json' # Para Windows (cambiar por la ruta que corresponda)
# path = '/dev/shm/graph.json' # Para Linux

# Librerías a utilizar:
import time
from globales import candado
import random
from grafo import Grafo
from labyrinth import Labyrinth
import threading
import json

# Macro expansions -sort of
ROWS = 5
COLUMNS = 5

# Parametros de Inicio y Fin
start = str(ROWS * COLUMNS - 1)
end = str(random.randint(0, COLUMNS - 1))

def create_labyrinth():
    """
    Esta función crea un objeto Labyrinth con el número especificado de filas y columnas, y comienza el bucle de eventos de Tkinter.

    La función utiliza las constantes globales ROWS y COLUMNS para determinar el tamaño del laberinto. El laberinto es entonces
    se muestra en la pantalla llamando al método start de la clase Labyrinth.

    :return:
    """
    maze = Labyrinth(ROWS, COLUMNS)
    maze.start()

def load_graph(filepath):
    """
    Esta función carga el grafo desde un archivo JSON.
    :param filepath: Ruta del archivo JSON.
    :return: Grafo como diccionario.
    """
    with open(filepath, 'r') as file:
        grafo = json.load(file)
        # Crea un objeto Grafo
        grafo_objeto = Grafo(V=grafo["V"], E=grafo["E"], turtle=grafo["turtle"])
    return grafo_objeto

def get_neighbors(current_cell):
    """
    Esta función obtiene los vecinos de una celda en un laberinto.
    Args:
        current_cell: Celda actual.
    Returns:

    """
    # Si la celda tiene vecinos sin visitar
    neighbors = []
    # Verificar si la celda actual tiene un vecino arriba
    if current_cell - COLUMNS > 0:
        neighbors.append(current_cell - COLUMNS)
    # Verificar si la celda actual tiene un vecino abajo
    if current_cell + COLUMNS < ROWS * COLUMNS:
        neighbors.append(current_cell + COLUMNS)
    # Verificar si la celda actual tiene un vecino a la izquierda
    if current_cell % COLUMNS != 0:
        neighbors.append(current_cell - 1)
    # Verificar si la celda actual tiene un vecino a la derecha
    if current_cell % COLUMNS != COLUMNS - 1:
        neighbors.append(current_cell + 1)
    return neighbors

def recursive_backtracker():
    '''
    La función genera un laberinto utilizando el algoritmo de Recursive Backtracker. Se utiliza el objeto candado para evitar condiciones de carrera.
    La tortuga inicia en una celda luego va generando el laberinto. Hasta abarcar todas las celdas.
    # En un hilo se crea el diseño del laberinto y en otro se genera el laberinto con el algoritmo de Recursive Backtracker, el cual actualiza a la función create_labyrinth en cada iteración
    # donde la tortuga avanza en el laberinto hasta abarcar todas las celdas.

    Returns:
    '''
    # Crear un grafo vacío
    grafo = Grafo()
    # Agregar la celda de inicio al grafo
    # Definir la celda de inicio que varie entre 0 y ROWS*COLUMNS - 1
    nodo_inicio = random.randint(0, ROWS*COLUMNS - 1)
    grafo.turtle = {nodo_inicio: nodo_inicio - 1}
    # Agregar la celda de inicio al grafo.V con una lista vacía como valor
    grafo.V[nodo_inicio] = []
    # Crear un stack vacío
    stack = []
    # Marcar la celda de inicio como visitada
    visited = {nodo_inicio}
    # Agregar la celda de inicio al stack
    stack.append(nodo_inicio)
    # Mientras el stack no esté vacío y además, actualizar la posición de la tortuga
    while stack:
        # Remover la siguiente celda del stack y hacerla la celda actual
        current_cell = stack.pop()
        # Si la celda tiene vecinos sin visitar
        neighbors = get_neighbors(current_cell)
        # Vecinos sin visitar
        unvisited = [n for n in neighbors if n not in visited]
        while unvisited:
            # Elegir un vecino sin visitar al azar
            next_cell = random.choice(unvisited)
            # Agregar la celda actual al grafo.V con el vecino elegido como valor
            grafo.V[current_cell].append(next_cell)
            # Agregar el vecino elegido al grafo.V con la celda actual como valor
            grafo.V[next_cell] = [current_cell]
            # Agregar la arista entre la celda actual y el vecino elegido con un peso de 1
            grafo.add_edge(current_cell, next_cell, 1)
            # Marcar el vecino elegido como visitado
            visited.add(next_cell)
            # Agregar el vecino elegido al stack
            stack.append(next_cell)
            # Actualizar la posición de la tortuga
            grafo.turtle[current_cell] = next_cell
            # Enviar el grafo a la cola
            with candado:
                grafo.send_graph()
            # Esperar un segundo
            time.sleep(1)
            # Borrar tortuga de la actual anterior
            grafo.turtle.pop(current_cell)
            # Actualizar la celda actual
            current_cell = next_cell
            # Actualizar los vecinos de la celda actual
            neighbors = get_neighbors(current_cell)
            unvisited = [n for n in neighbors if n not in visited]

    # Actualizar la posición de la tortuga en la última celda
    with candado:
        grafo.send_graph()
    # Esperar un segundo
    time.sleep(1)

    # Save the graph as a json file
    grafo.save_graph(path)  # For operation in Windows
    print(grafo)


# Paso #3: Implementar los algoritmos de Prim, Kruskal y Dijkstra para encontrar el camino más corto entre dos nodos del laberinto.

def prim(grafo, start):
    """
    Implementación del algoritmo de Prim para encontrar el árbol de expansión mínima de un grafo.
    Args:
        grafo: Grafo a analizar.
        start: Nodo de inicio.
    Returns: Retorna el árbol de expansión mínima del grafo.
    """
    V = grafo.V
    E = grafo.E

    # Aseguramos que start sea una cadena
    #start = str(start)

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
    """
    Implementación del algoritmo de Kruskal para encontrar el árbol mínimo de cobertura de un grafo.
    Args:
        grafo: Grafo a analizar.
    Returns: Retorna el árbol mínimo de cobertura del grafo.
    """
    V = grafo.V
    E = grafo.E
    A = set()
    parent = {v: v for v in V}
    rank = {v: 0 for v in V}

    def find(v):
        if parent[v] != v:
            parent[v] = find(parent[v])
        return parent[v]

    def union(u, v):
        root_u = find(u)
        root_v = find(v)
        if root_u != root_v:
            if rank[root_u] > rank[root_v]:
                parent[root_v] = root_u
            else:
                parent[root_u] = root_v
                if rank[root_u] == rank[root_v]:
                    rank[root_v] += 1
            A.add(f'({u}, {v})')

    edges = sorted(E.items(), key=lambda item: item[1])
    for edge, weight in edges:
        u, v = map(str.strip, edge.strip("()").split(","))
        if find(u) != find(v):
            union(u, v)

    # Hallar el árbol mínimo de cobertura
    mst = {v: None for v in V}
    for edge in A: # A es el conjunto de aristas del árbol mínimo de cobertura
        u, v = map(str.strip, edge.strip("()").split(","))
        mst[v] = u

    return mst, A


def dijkstra(grafo, start):
    """
    Implementación del algoritmo de Dijkstra para encontrar el camino más corto entre dos nodos de un grafo.
    Args:
        grafo: Grafo a analizar.
        start: Nodo de inicio.
    Returns: Retorna el camino más corto entre dos nodos del grafo.

    """
    V = grafo.V
    E = grafo.E
    #start = str(start)

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
            # Añadir la arista al diccionario de forma directa o inversa
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
    grafo = load_graph(path) # For operation in Windows
    # Encontrar el camino más corto entre dos nodos del laberinto con los algoritmos de Prim, Kruskal y Dijkstra:

    mst_1 = prim(grafo, start)
    print("Camino encontrado por Prim:", mst_1)

    mst_2, A = kruskal(grafo)
    print("Conjunto de aristas encontrado por Kruskal:", A)
    print("Camino encontrado por Kruskal:", mst_2)

    mst_3 = dijkstra(grafo, start)
    print("Camino encontrado por Dijkstra:", mst_3)
    print()


    def ruta(mst, start, end):
        """
        Esta función encuentra el camino desde el nodo de inicio hasta el nodo final utilizando el árbol mínimo de cobertura del grafo.
        Args:
            mst: Árbol mínimo de cobertura del grafo.
            start: Nodo de inicio.
            end: Nodo final.
        Returns: Retorna el camino desde el nodo de inicio hasta el nodo final.
        """
        # Inicializar una lista para almacenar el camino
        path = []

        # Verificar el tipo de mst para encontrar el camino desde el nodo de inicio hasta el nodo final. Debido a que Kruskal encuentra el mst diferente a Prim y Dijkstra.
        if mst == mst_3 or mst == mst_1:
            # Comenzar desde la celda objetivo y seguir las conexiones hacia atrás hasta la celda de inicio
            current = end
            while current is not None:
                path.append(current)
                current = mst[current]
                if current == start:
                    path.append(current)
                    break
            # Invertir la lista para obtener el camino desde el inicio hasta el objetivo
            path.reverse()
        else:
            # Comenzar desde la celda de inicio y seguir las conexiones hasta la celda final
            current = start
            while current is not None:
                path.append(current)
                current = mst[current]
                if current == end:
                    path.append(current)
                    break

        return path


    # Se calcula el camino más corto entre dos nodos del laberinto para cada algoritmo
    # Definir nombres de algoritmos
    nombres = ["Prim", "Kruskal", "Dijkstra"]

    # Encontrar el camino desde el nodo de inicio hasta el nodo final para cada algoritmo
    for nombre, mst in zip(nombres, [mst_1, mst_2, mst_3]):
        # Imprimir el camino encontrado por cada algoritmo
        print(f"Ruta encontrado por {nombre}:", ruta(mst, start, end))

    ruta = ruta(mst_1, start, end)

    # Crear nodos ficticios para la entrada y la salida
    grafo.add_edge(end, -1, 1)
    with candado:
        grafo.send_graph()
    # Esperar un segundo
    time.sleep(1)
    print(grafo)


    # Mover la tortuga a lo largo del camino encontrado por Prim
    # Tortuga en la celda de inicio, la tortuga comienza desde el nodo ficticio de la entrada.
    grafo.turtle[start] = str((ROWS * COLUMNS - 1) - COLUMNS)
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
    # Tortuga en la celda final, mirando hacia arriba
    grafo.turtle[end] = int(end) - COLUMNS
    # Actualizar la posición de la tortuga en la última celda
    with candado:
        grafo.send_graph()
    # Esperar un segundo
    time.sleep(1)
    # Eliminar tortuga de la celda final
    grafo.turtle.pop(ruta[-1])
    # Actualizar tortuga
    with candado:
        grafo.send_graph()
    # Esperar un segundo
    time.sleep(1)



if __name__ == '__main__':

    # Crear dos hilos para ejecutar las funciones create_labyrinth y recursive_backtracker concurrentemente
    # La función create_labyrinth se ejecuta en un hilo separado
    hilo1 = threading.Thread(target=create_labyrinth)
    hilo1.start()  # Inicia el hilo

    # La función recursive_backtracker se ejecuta en un hilo separado
    hilo2 = threading.Thread(target=recursive_backtracker)
    hilo2.start() # Inicia el hilo

    # Espera a que los hilos terminen
    hilo2.join()

    # Luego de la creación del laberinto, se resuelve el laberinto con los algoritmos de Prim, Kruskal y Dijkstra, esto por medio de la función solve_laberynth, donde contendrá
    # las funciones de Prim, Kruskal y Dijkstra. Se ejecuta en un hilo separado, a la vez que se sigue ejecutando la función create_labyrinth.

    # La función solve_laberynth se ejecuta en un hilo separado
    hilo3 = threading.Thread(target=solve_laberynth)
    hilo3.start() # Inicia el hilo

    # Finalmente se espera a que los hilos de solve_laberynth y create_labyrinth terminen.
    hilo1.join()
    hilo3.join()