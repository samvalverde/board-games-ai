import csv
import os
from peg_solitaire.board import Board
from peg_solitaire.astar import astar
from peg_solitaire.heuristics import h_min_moves

# Parámetros de benchmark
SIZES = [3, 5, 7]       # Tableros a probar
RUNS = 3                # Número de repeticiones por tamaño
OUTPUT_FILE = "experiments/results.csv"


def run_benchmark():
    results = []
    for n in SIZES:
        for run in range(RUNS):
            print(f"\nEjecutando n={n}, corrida {run+1}/{RUNS}")
            start = Board(n)
            path, boards, metrics = astar(start, h_func=h_min_moves)

            row = {
                "n": n,
                "run": run + 1,
                "success": metrics["success"],
                "time": metrics["time"],
                "expanded": metrics["expanded"],
                "generated": metrics["generated"],
                "max_frontier": metrics["max_frontier"],
                "solution_length": metrics["solution_length"],
            }
            results.append(row)

    # Guardar resultados en CSV
    os.makedirs("experiments", exist_ok=True)
    with open(OUTPUT_FILE, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)

    print(f"\Resultados guardados en {OUTPUT_FILE}")


if __name__ == "__main__":
    run_benchmark()
