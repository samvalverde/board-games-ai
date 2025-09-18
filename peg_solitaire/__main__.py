import argparse
from peg_solitaire.board import Board
from peg_solitaire.astar import astar
from peg_solitaire.heuristics import h_min_moves

# Ejecutar A* desde línea de comandos
# Uso: poetry run python -m peg_solitaire -n 3

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", type=int, default=3, help="Tamaño del tablero (impar)")
    args = parser.parse_args()

    start = Board(args.n)
    print(f"Estado inicial con n={args.n}:")
    print(start)

    path, boards, metrics = astar(start, h_func=h_min_moves)

    if metrics["success"]:
        print(f"\nSolución encontrada con {metrics['solution_length']} movimientos")
        for i, board in enumerate(boards):
            print(f"\nPaso {i}:")
            print(board)
    else:
        print("\nNo se encontró solución")

    print("\nMétricas de ejecución:")
    for k, v in metrics.items():
        print(f"- {k}: {v}")
