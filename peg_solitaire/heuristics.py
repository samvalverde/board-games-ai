def h_min_moves(board) -> int:
    """Admisible: cada movimiento quita una ficha."""
    return board.peg_count() - 1
