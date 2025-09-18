from math import inf
from .board import Board
from typing import Optional, Tuple

""" Heurística para evaluar el tablero desde la perspectiva del jugador `me`.
    - Diferencia de puntos (ponderada)  + penalización por cajas con 3 lados + pequeño bonus por cajas con 2 lados."""
def heuristic(b: Board, me: int) -> int:
    # diferencia de puntos con peso alto
    other = 2 if me == 1 else 1
    score = (b.scores[me-1] - b.scores[other-1]) * 100

    # penaliza cajas con 3 lados (regalar 4º lado)
    threes = sum(1 for r in range(b.rows) for c in range(b.cols)
                 if b.box_owner[r][c] == 0 and b.box_edges_count[r][c] == 3)
    score -= 6 * threes if b.player != me else 2 * threes

    # pequeño bonus por cajas con 2 lados
    twos = sum(1 for r in range(b.rows) for c in range(b.cols)
               if b.box_owner[r][c] == 0 and b.box_edges_count[r][c] == 2)
    score += 2 * twos
    return score
""" Minimax con poda alpha-beta. 
    Respeta turno extra: si el hijo mantiene el mismo jugador, no baja profundidad."""
def minimax(b: Board, 
            depth: Optional[int], 
            alpha: int, 
            beta: int, 
            me: int,
            use_alphabeta: bool) -> int:
    if  b.is_game_over():
        return heuristic(b, me)

    if depth is not None and depth == 0:
        return heuristic(b, me)
        

    maximizing = (b.player == me)

    if maximizing:
        best = -inf
        for mv in b.legal_moves():
            nb = b.clone()
            before = nb.player
            nb.make_move(*mv)
            next_depth = None if depth is None else (depth if nb.player == before else depth - 1)
            val = minimax(nb, next_depth, alpha, beta, me, use_alphabeta)
            if val > best: best = val
            if use_alphabeta:
                if val > alpha: alpha = val
                if alpha >= beta: break
        return best
    else:
        best = inf
        for mv in b.legal_moves():
            nb = b.clone()
            before = nb.player
            nb.make_move(*mv)
            next_depth = None if depth is None else (depth if nb.player == before else depth - 1)
            val = minimax(nb, next_depth, alpha, beta, me, use_alphabeta)
            if val < best: best = val
            if use_alphabeta:
                if val < beta: beta = val
                if alpha >= beta: break
        return best

def best_move(b: Board, 
              depth: Optional[int], 
              me: Optional[int] = None,
              use_alphabeta: bool = True) -> Tuple[tuple, float]:
    """
    Devuelve (mejor_movimiento, valor) para el jugador `me`.
    Si `me` es None, se asume el jugador actual del tablero.
    Respeta turno extra: si el hijo mantiene el mismo jugador, no baja profundidad.
    """
    if me is None:
        me = b.player

    maximizing = (b.player == me)
    best_val = -inf if maximizing else inf
    best_mv = None
    alpha, beta = -inf, inf

    for mv in b.legal_moves():          # mv = ('h'|'v', r, c)
        nb = b.clone()
        before = nb.player
        nb.make_move(*mv)


        next_depth = None if depth is None else (depth if nb.player == before else depth - 1)

        val = minimax(nb, next_depth, alpha, beta, me, use_alphabeta)

        if maximizing:
            if val > best_val:
                best_val, best_mv = val, mv
            if use_alphabeta and val > alpha:
                alpha = val
        else:
            if val < best_val:
                best_val, best_mv = val, mv
            if use_alphabeta and val < beta:
                beta = val

        if alpha >= beta:
            break

    return best_mv, best_val