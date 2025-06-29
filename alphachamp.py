import chess


def eval(board: chess.Board):
    e = 0
    piece_values = {
        chess.PAWN: 100,
        chess.KNIGHT: 300,
        chess.BISHOP: 350,
        chess.ROOK: 500,
        chess.QUEEN: 900,
    }
    # loop over all piece codes
    # +ve eval = better position for whoseever turn it is
    # -ve eval = worse position for whoseever turn it is
    for i in range(1, 6):
        e = e + piece_values[i] * (
            len(board.pieces(i, not board.turn)) - len(board.pieces(i, board.turn))
        )

    return e


def next_move(board: chess.Board, debug=False):
    moves = board.generate_legal_moves()
    best_move: chess.Move = chess.Move.from_uci("0000")
    best_eval = float("-inf")
    for move in moves:
        board.push(move)
        # print("checking: ", move, " ", eval(board))
        if eval(board) > best_eval:
            best_move = move
            best_eval = eval(board)
        board.pop()

    if debug:
        print("eval: ", best_eval)
        print("best_move: ", best_move)

    return best_move
