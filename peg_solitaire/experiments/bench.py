import csv
import os
from peg_solitaire.board import Board
from peg_solitaire.astar import astar
from peg_solitaire.heuristics import h_min_moves, h_manhattan, h_combo

# Run: poetry run python -m peg_solitaire.experiments.bench

# Parámetros de benchmark
SIZES = [3, 5, 7]     # Tableros a probar
RUNS = 5              # Repeticiones por tamaño
OUTPUT_FILE = "peg_solitaire/experiments/results.csv"

HEURISTICS = {
    "min_moves": h_min_moves,
    "manhattan": h_manhattan,
    "combo": h_combo,
}


def run_benchmark():
    results = []
    for name, h_func in HEURISTICS.items():
        for n in SIZES:
            for run in range(RUNS):
                print(f"\nEjecutando h={name}, n={n}, corrida {run+1}/{RUNS}")
                start = Board(n)

                # Llamada a astar con límites más generosos
                path, boards, metrics = astar(
                    start,
                    h_func=h_func,
                    max_expansions=500_000,   # ahora medio millón
                    max_time=120              # hasta 2 minutos por corrida
                )

                row = {
                    "heuristic": name,
                    "n": n,
                    "run": run + 1,
                    "success": metrics["success"],
                    "time": metrics["time"],
                    "expanded": metrics["expanded"],
                    "generated": metrics["generated"],
                    "max_frontier": metrics["max_frontier"],
                    "solution_length": metrics["solution_length"],
                    "aborted": metrics.get("aborted", False),
                }
                results.append(row)

    # Guardar resultados en CSV
    os.makedirs("peg_solitaire/experiments", exist_ok=True)
    with open(OUTPUT_FILE, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)

    print(f"\nResultados guardados en {OUTPUT_FILE}")


if __name__ == "__main__":
    run_benchmark()
