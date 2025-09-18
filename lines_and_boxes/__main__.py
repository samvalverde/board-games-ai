from .board import Board
from .metrics import TimeMetric
from .minmax import *

def leer_entero(prompt: str, default: int, minimo: int = 1) -> int:
    try:
        v = input(f"{prompt} el valor por defecto es[{default}]: ").strip()
        if v == "":
            return default
        v = int(v)
        if v < minimo:
            return default
        return v
    except Exception:
        return default
""" Realiza una partida completa y devuelve el tiempo total en ms. se usó para las gráficas
y se utilizó la ayuda de la IA"""
def time_full_game(rows: int, cols: int, depth: int, use_ab: bool) -> float:
    b = Board(rows, cols)
    total = 0.0
    while not b.is_game_over():
        t = TimeMetric().start()
        mv, _ = best_move(b, depth, use_alphabeta=use_ab)
        t.stop()
        total += t.elapsed_ms
        b.make_move(*mv)
    return total
""" Imprime una línea CSV con los datos de la corrida. se usó para las gráficas """
def print_csv_line(label: str, rows: int, cols: int, depth: int, use_ab: bool, time_ms: float):
    # use_ab: 1 = ON, 0 = OFF
    print(f"{label},{rows},{cols},{depth},{1 if use_ab else 0},{time_ms:.3f}")

def main():

    rows = leer_entero("Filas (cajas)", default=2, minimo=2)
    cols = leer_entero("Columnas (cajas)", default=2, minimo=2)
    depth = leer_entero("Profundidad de búsqueda", default=None, minimo=2)
    b = Board(rows, cols)
    print(b)
    while not b.is_game_over():
        move, val = best_move(b, depth) #profundidad 3
        print(f"Jugador {b.player} juega {move} con valor {val}") #ese es el valor de la heuristica
        b.make_move(*move)
        print(b)
    print("Cantidad de movimientos:", len(b.history))
    print("Puntajes:\n", "Jugador1:", b.scores[0], "Jugador2:", b.scores[1])
    print("Historial de movimientos(el check significa que se completo una caja):")
    for m in b.history:
        print(m)


if __name__ == "__main__":
    # Quitar estos comentarios para hacer pruebas de tiempo
     #rows, cols, depth = 2, 2, 6 
     #runs = 5
     #for i in range(1, runs+1):
     #   ms_on  = time_full_game(rows, cols, depth, use_ab=True)
     #   ms_off = time_full_game(rows, cols, depth, use_ab=False)
     #   print_csv_line("full_game", rows, cols, depth, True,  ms_on)
     #   print_csv_line("full_game", rows, cols, depth, False, ms_off)
    main()