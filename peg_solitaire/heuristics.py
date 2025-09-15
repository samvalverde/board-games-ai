def h_min_moves(board) -> int:
    """Heurística admisible:
    Cada movimiento quita exactamente una ficha.
    """
    return board.peg_count() - 1


def h_manhattan(board) -> int:
    """Heurística basada en distancia Manhattan al centro.
    Para cada peón cuenta la distancia al centro.
    Admisible, pero más informativa que h_min_moves.
    """
    center = board.n
    total = 0
    for r in range(board.size):
        for c in range(board.size):
            if board.grid[r][c] == 1:
                total += abs(r - center) + abs(c - center)
    return total


def h_combo(board) -> int:
    """Heurística combinada: peones restantes + distancia Manhattan.
    No siempre estrictamente admisible, pero mejora la eficiencia
    al discriminar más entre estados.
    """
    return h_min_moves(board) + h_manhattan(board)
