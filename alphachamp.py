import chess


def next_move(board: chess.Board, debug=False):
    com_move = next(board.generate_legal_moves())
    if debug:
        print(com_move)
    return com_move
