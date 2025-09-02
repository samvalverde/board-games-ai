import heapq
from dataclasses import dataclass, field
from typing import Optional
from .board import Board, Move
from .heuristics import h_min_moves

@dataclass(order=True)
class PQItem:
    f: int
    tie: int
    node: object = field(compare=False)

@dataclass
class Node:
    board: Board
    g: int
    move: Optional[Move]
    parent: Optional["Node"]

def reconstruct(node: Node):
    path, boards = [], []
    while node:
        path.append(node.move)
        boards.append(node.board)
        node = node.parent
    return list(reversed(path[:-1])), list(reversed(boards))

def astar(start: Board, h_func=h_min_moves):
    open_heap, open_map, closed = [], {}, set()
    start_node = Node(start, g=0, move=None, parent=None)
    tie = 0
    heapq.heappush(open_heap, PQItem(h_func(start), tie, start_node))
    open_map[start] = (0, None)

    while open_heap:
        current = heapq.heappop(open_heap).node
        if current.board.is_goal():
            return reconstruct(current)

        closed.add(current.board)
        for m in current.board.legal_moves():
            nb = current.board.apply(m)
            if nb in closed:
                continue
            g2 = current.g + 1
            f2 = g2 + h_func(nb)
            prev = open_map.get(nb)
            if prev is None or g2 < prev[0]:
                tie += 1
                heapq.heappush(open_heap, PQItem(f2, tie, Node(nb, g2, m, current)))
                open_map[nb] = (g2, m)
    return None
