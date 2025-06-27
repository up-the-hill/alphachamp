import chess

# setup
board = chess.Board()
player_side = (
    chess.WHITE if input("Play as white or black (w/b)") == "w" else chess.BLACK
)


def render(board: chess.Board) -> str:
    """
    Print a ((opt) side-relative) chess board with special chess characters.
    """
    board_string = list(str(board))
    uni_pieces = {
        "R": "♜",
        "N": "♞",
        "B": "♝",
        "Q": "♛",
        "K": "♚",
        "P": "♟",
        "r": "♖",
        "n": "♘",
        "b": "♗",
        "q": "♕",
        "k": "♔",
        "p": "♙",
        ".": "·",
    }
    for idx, char in enumerate(board_string):
        if char in uni_pieces:
            board_string[idx] = uni_pieces[char]
    ranks = ["1", "2", "3", "4", "5", "6", "7", "8"]
    display = []
    for rank in "".join(board_string).split("\n"):
        display.append(f"  {ranks.pop()} {rank}")
    # if board.turn == chess.BLACK:
    #     display.reverse()
    display.append("    a b c d e f g h")
    return "\n" + "\n".join(display)


# game loop
while True:
    if board.is_game_over():
        break

    if board.turn == player_side:
        try:
            print(render(board))
            board.push_san(input("Move:"))
        except chess.IllegalMoveError:
            print("invalid move; try again")
    else:
        com_move = next(board.generate_legal_moves())
        print(com_move)
        board.push(com_move)
