from .board import Board

def main():
    board = Board(2,2)
    board.print_board()
    # Simulate a simple 2x2 dots and boxes game
    # Each move is a tuple: (row, col, orientation)
    # orientation: 'h' for horizontal, 'v' for vertical

    moves = [
        (0, 0, 'h'),  # Top left horizontal
        (0, 0, 'v'),  # Top left vertical
        (0, 1, 'h'),  # Top right horizontal
        (0, 1, 'v'),  # Top right vertical
        (1, 0, 'h'),  # Bottom left horizontal
        (1, 0, 'v'),  # Bottom left vertical
        (1, 1, 'h'),  # Bottom right horizontal
        (1, 1, 'v'),  # Bottom right vertical
    ]

    players = ['A', 'B']
    current_player = 0

    for move in moves:
        row, col, orientation = move
        completed_box = board.make_move(orientation, row, col)
        board.print_board()
        if not completed_box:
            current_player = 1 - current_player  # Switch player

    print("Game over!")
    print("Final Scores:")
    for i, player in enumerate(players):
        print(f"Player {player}: {board.scores[i]}")

if __name__ == "__main__":
    main()