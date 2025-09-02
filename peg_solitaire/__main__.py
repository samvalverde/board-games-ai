from .board import Board
from .astar import astar

if __name__ == "__main__":
    # Tablero clásico: n=3
    start = Board(3)
    print("Estado inicial:")
    print(start)

    result = astar(start)
    if result:
        path, boards = result
        print(f"\nSolución encontrada con {len(path)} movimientos")
    else:
        print("No se encontró solución")
