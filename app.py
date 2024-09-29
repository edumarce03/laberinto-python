import random
import numpy as np
import time

# Dimensiones del laberinto
n = 10  # Número de "cuartos" en cada fila y columna
size = 2 * n + 1  # Tamaño real de la matriz (incluyendo paredes)

# Inicializamos el laberinto con paredes
maze = np.ones((size, size), dtype=int)

# Función para generar el laberinto usando un algoritmo de retroceso (backtracking)
def generate_maze(maze, x, y):
    directions = [(-2, 0), (2, 0), (0, -2), (0, 2)]  # N, S, O, E
    random.shuffle(directions)  # Mezclamos las direcciones para aleatorizar el laberinto

    for dx, dy in directions:
        new_x, new_y = x + dx, y + dy
        if (1 <= new_x < size - 1 and 1 <= new_y < size - 1 and maze[new_x, new_y] == 1):
            maze[x + dx // 2, y + dy // 2] = 0  # Elimina la pared entre las celdas
            maze[new_x, new_y] = 0  # Abre la celda
            generate_maze(maze, new_x, new_y)  # Llamada recursiva para continuar

# Generar el laberinto desde una posición inicial
def create_maze():
    generate_maze(maze, 1, 1)  # Comenzar desde la posición (1, 1)

# Función para resolver el laberinto
def solve_maze(maze, start, end):
    stack = [start]
    visited = set()
    visited.add(start)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # N, S, O, E
    solution = []

    while stack:
        current = stack[-1]
        solution.append(current)
        if current == end:
            break
        x, y = current
        found_way = False
        for direction in directions:
            new_x, new_y = x + direction[0], y + direction[1]
            if (new_x, new_y) not in visited and maze[new_x, new_y] == 0:
                stack.append((new_x, new_y))
                visited.add((new_x, new_y))
                found_way = True
                break
        if not found_way:
            stack.pop()
            solution.pop()

    return solution if stack and stack[-1] == end else []  # Devuelve la solución o lista vacía

# Pedir el nombre del agente
agent_name = input("Por favor, ingrese el nombre del agente: ")

# Generamos el laberinto
create_maze()

# Definir posiciones de inicio (esquina inferior izquierda) y fin (esquina superior derecha)
start = (1, 1)
end = (size - 2, size - 2)

# Resolver el laberinto
solution = solve_maze(maze, start, end)

# Función para mostrar el laberinto en consola
def print_maze(maze, agent_position, path_positions):
    maze_display = maze.copy()
    for (x, y) in agent_position:
        maze_display[x, y] = 2  # Marca la posición del agente (cuadrado rojo)
    for (px, py) in path_positions:
        maze_display[px, py] = 3  # Marca la trayectoria (trazo amarillo)
        
    print("\n".join("".join("█" if cell == 1 else " " if cell == 0 else "A" if cell == 2 else "•" for cell in row) for row in maze_display))

# Mostrar el laberinto y la solución en la consola
if solution:
    print(f"\nLaberinto generado:\n")
    print_maze(maze, [start], [])

    path_positions = []  # Para almacenar el camino recorrido
    for step in solution:
        time.sleep(0.5)  # Esperar 0.5 segundos entre movimientos
        path_positions.append(step)
        print("\nMoviendo agente:")
        print_maze(maze, [step], path_positions)
        
    print(f"\n¡{agent_name} ha llegado a la salida!")
else:
    print("No se encontró una solución para este laberinto.")
