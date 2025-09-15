from typing import Optional
from peg_solitaire.board import Board, Move
import heapq
import time

class Node:
    def __init__(self, board: Board, g=0, move: Optional[Move] = None, parent: Optional["Node"] = None):
        self.board = board      # estado del tablero
        self.g = g              # costo real hasta aquí
        self.h = 0              # heurística
        self.f = 0              # f = g + h
        self.move = move        # movimiento que llevó a este estado
        self.parent = parent    # nodo padre (para reconstruir el camino)

    def __lt__(self, other: "Node"):
        return self.f < other.f


def astar(start: Board, h_func, max_expansions: int = 50_000):
    nodos_expandidos = 0
    nodos_generados = 0
    max_frontier = 0
    start_time = time.perf_counter()

    root = Node(start, g=0)
    root.h = h_func(start)
    root.f = root.g + root.h

    open_set = [root]
    closed_set = set()

    while open_set:
        current = heapq.heappop(open_set)
        nodos_expandidos += 1
        max_frontier = max(max_frontier, len(open_set))

        # 🔒 Parar si excedemos el límite
        if nodos_expandidos > max_expansions:
            elapsed = time.perf_counter() - start_time
            return None, None, {
                "time": elapsed,
                "expanded": nodos_expandidos,
                "generated": nodos_generados,
                "max_frontier": max_frontier,
                "solution_length": None,
                "success": False,
                "aborted": True,
            }

        if current.board.is_goal():
            path, boards = [], []
            while current:
                if current.move:
                    path.append(current.move)
                boards.append(current.board)
                current = current.parent
            path.reverse()
            boards.reverse()

            elapsed = time.perf_counter() - start_time
            return path, boards, {
                "time": elapsed,
                "expanded": nodos_expandidos,
                "generated": nodos_generados,
                "max_frontier": max_frontier,
                "solution_length": len(path),
                "success": True,
                "aborted": False,
            }

        closed_set.add(current.board)

        for move in current.board.legal_moves():
            new_board = current.board.apply(move)
            if new_board in closed_set:
                continue

            g = current.g + 1
            h = h_func(new_board)
            f = g + h
            nodos_generados += 1

            existing_node = next((node for node in open_set if node.board == new_board), None)
            if existing_node and existing_node.f <= f:
                continue

            new_node = Node(new_board, g=g, move=move, parent=current)
            new_node.h = h
            new_node.f = f
            heapq.heappush(open_set, new_node)

    elapsed = time.perf_counter() - start_time
    return None, None, {
        "time": elapsed,
        "expanded": nodos_expandidos,
        "generated": nodos_generados,
        "max_frontier": max_frontier,
        "solution_length": None,
        "success": False,
        "aborted": False,
    }

