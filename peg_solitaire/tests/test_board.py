from peg_solitaire.board import Board

def test_boards_creation():
    for n in [3, 5, 7]:
        b = Board(n)
        print(f"\nn={n}, size={b.size}")
        print(b)
    return