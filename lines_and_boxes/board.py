from dataclasses import dataclass
from typing import Literal, Iterable, Tuple, List

@dataclass
class Move:
    edge_type: Literal["h", "v"]
    row: int
    col: int
    player: int
    completed_box: bool

    def __str__(self) -> str:
        dir_txt = "horizontal" if self.edge_type == "h" else "vertical"
        return f"{dir_txt}({self.row},{self.col}) por Jugador{self.player}{' ✓' if self.completed_box else ''}"
# definir la clase board
# un tablero tiene filas y columnas
# tiene bordes horizontales y verticales
@dataclass
class Board:
    rows: int
    cols: int
    horizontal_edges: List[List[bool]]
    vertical_edges: List[List[bool]]
    box_owner: List[List[int]]
    box_edges_count: List[List[int]]
    player: int
    scores: List[int]
    history: List[Move]

    """ Inicializa un tablero vacío de tamaño rows x cols. """
    def __init__(self, rows: int, cols: int):
        self.rows = rows
        self.cols = cols
        self.horizontal_edges = [[False for _ in range(cols)] for _ in range(rows + 1)]
        self.vertical_edges = [[False for _ in range(cols + 1)] for _ in range(rows)]
        self.box_owner = [[0 for _ in range(cols)] for _ in range(rows)]
        self.box_edges_count = [[0 for _ in range(cols)] for _ in range(rows)]
        self.player = 1
        self.scores = [0, 0]
        self.history = []


    """ Devuelve una copia profunda del tablero.  es la que se le pasa al minimax """
    def clone(self) -> "Board":
        nb = Board(self.rows, self.cols)
        nb.horizontal_edges = [row[:] for row in self.horizontal_edges]
        nb.vertical_edges   = [row[:] for row in self.vertical_edges]
        nb.box_owner        = [row[:] for row in self.box_owner]
        nb.box_edges_count  = [row[:] for row in self.box_edges_count]
        nb.player           = self.player
        nb.scores           = self.scores[:]
        nb.history         = self.history[:]
        return nb

    """ Devuelve las cajas adyacentes a un borde dado (si las hay)."""
    def _adjacent_boxes(self, edge_type: Literal["h", "v"], row: int, col: int) -> Iterable[Tuple[int, int]]:
        if edge_type == "h":
            if row > 0:
                yield (row - 1, col)
            if row < self.rows:
                yield (row, col)
        elif edge_type == "v":
            if col > 0:
                yield (row, col - 1)
            if col < self.cols:
                yield (row, col)

    def _edge_is_free(self, edge_type: Literal["h", "v"], row: int, col: int) -> bool:
        if edge_type == "h":
            return not self.horizontal_edges[row][col]
        elif edge_type == "v":
            return not self.vertical_edges[row][col]
        return False
    
    def is_move_valid(self, edge_type: Literal["h", "v"], row: int, col: int) -> bool:
        if edge_type == "h":
            return 0 <= row <= self.rows and 0 <= col < self.cols and self._edge_is_free(edge_type, row, col)
        elif edge_type == "v":
            return 0 <= row < self.rows and 0 <= col <= self.cols and self._edge_is_free(edge_type, row, col)
        return False

    """  Devuelve una lista de movimientos legales en el formato ('h'|'v', row, col). """
    def legal_moves(self):
        # h: r in [0..rows], c in [0..cols-1]
        for r in range(self.rows + 1):
            for c in range(self.cols):
                if not self.horizontal_edges[r][c]:
                    yield ('h', r, c)
        # v: r in [0..rows-1], c in [0..cols]
        for r in range(self.rows):
            for c in range(self.cols + 1):
                if not self.vertical_edges[r][c]:
                    yield ('v', r, c)

    """  Devuelve si el juego ha terminado. """
    def is_game_over(self) -> bool:
        return all(all(r) for r in self.horizontal_edges) and \
           all(all(r) for r in self.vertical_edges)
    """ Realiza un movimiento. Devuelve True si se completó una caja y el jugador repite turno. """
    def make_move(self, edge_type: Literal["h", "v"], row: int, col: int) -> bool:
        if not self.is_move_valid(edge_type, row, col):
            raise ValueError("Invalid move")
        
        self.draw_edge(edge_type, row, col)
        completed_box = False

        for r, c in self._adjacent_boxes(edge_type, row, col):
            self.box_edges_count[r][c] += 1
            if self.box_edges_count[r][c] == 4:
                self.box_owner[r][c] = self.player
                self.scores[self.player - 1] += 1
                completed_box = True

        self.history.append(Move(edge_type, row, col, self.player, completed_box))

        if not completed_box:
            self.player = 2 if self.player == 1 else 1
        
        return completed_box 

    """ Dibuja un borde en el tablero. """
    def draw_edge(self, edge_type: Literal["h", "v"], row: int, col: int):
        if edge_type == "h":
            self.horizontal_edges[row][col] = True
        elif edge_type == "v":
            self.vertical_edges[row][col] = True

    """ Devuelve una representación en cadena del tablero. Aqui se uso la ayuda de la IA para hacer el dibujo del tablero """
    def __str__(self):
        board_str = ""
        for r in range(self.rows + 1):
            # Dibuja bordes horizontales
            for c in range(self.cols):
                board_str += "•"
                board_str += "---" if self.horizontal_edges[r][c] else "   "
            board_str += "•\n"
            if r < self.rows:
                # Dibuja bordes verticales y dueños de cajas
                for c in range(self.cols + 1):
                    board_str += "|" if self.vertical_edges[r][c] else " "
                    if c < self.cols:
                        box_owner = self.box_owner[r][c]
                        board_str += f" {box_owner if box_owner != 0 else ' '} "
                board_str += "\n"
        return board_str

    def print_board(self):
        print(self.__str__())