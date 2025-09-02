from .board import Board
from .minmax import *

def main():
    b = Board(2, 2)
    print(b)
    while not b.is_game_over():
        move, val = best_move(b, 5)
        print(f"Jugador {b.player} juega {move} con valor {val}") #ese es el valor de la heuristica
        b.make_move(*move)
        print(b)

if __name__ == "__main__":
    main()