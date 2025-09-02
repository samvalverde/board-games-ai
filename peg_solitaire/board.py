from dataclasses import dataclass
from typing import Tuple, Iterable

Coord = Tuple[int, int]

@dataclass(frozen=True)
class Move:
    src: Coord
    over: Coord
    dst: Coord

class Board:

    def __init__(self, n: int, grid: Tuple[Tuple[int, ...], ...] | None = None):
        if n % 2 == 0:
            raise ValueError("n debe ser impar para que exista un centro único.")
        self.n = n
        self.size = 2 * n + 1
        if grid:
            self.grid = grid
        else:
            self.grid = self._default_cross(n)

    def _default_cross(self, n: int) -> Tuple[Tuple[int, ...], ...]:
        size = 2 * n + 1
        center = n
        grid = [[-1 for _ in range(size)] for _ in range(size)]

        for r in range(size):
            for c in range(size):
                if (abs(r - center) <= n and abs(c - center) <= 1) or \
                   (abs(c - center) <= n and abs(r - center) <= 1):
                    grid[r][c] = 1  # peón

        grid[center][center] = 0  # centro vacío
        return tuple(tuple(row) for row in grid)

    def peg_count(self) -> int:
        return sum(cell == 1 for row in self.grid for cell in row)

    def is_goal(self) -> bool:
        return self.peg_count() == 1 and self.grid[self.n][self.n] == 1

    def legal_moves(self) -> Iterable[Move]:
        moves = []
        dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        n = self.size
        for r in range(n):
            for c in range(n):
                if self.grid[r][c] != 1:
                    continue
                for dr, dc in dirs:
                    over = (r + dr, c + dc)
                    dst = (r + 2 * dr, c + 2 * dc)
                    if not (0 <= over[0] < n and 0 <= over[1] < n):
                        continue
                    if not (0 <= dst[0] < n and 0 <= dst[1] < n):
                        continue
                    if self.grid[over[0]][over[1]] == 1 and self.grid[dst[0]][dst[1]] == 0:
                        moves.append(Move((r, c), over, dst))
        return moves

    def apply(self, m: Move) -> "Board":
        grid = [list(row) for row in self.grid]
        grid[m.src[0]][m.src[1]] = 0
        grid[m.over[0]][m.over[1]] = 0
        grid[m.dst[0]][m.dst[1]] = 1
        return Board(self.n, tuple(tuple(row) for row in grid))

    def __hash__(self):
        return hash(self.grid)

    def __eq__(self, other):
        return self.grid == other.grid

    def __str__(self):
        symbols = {1: "●", 0: "○", -1: " "}
        return "\n".join(" ".join(symbols[val] for val in row) for row in self.grid)
