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
    # +ve eval = better position for white
    # -ve eval = worse position for black
    for i in range(1, 6):
        e = e + piece_values[i] * (
            len(board.pieces(i, chess.WHITE)) - len(board.pieces(i, chess.BLACK))
        )

    return e


def next_move(board: chess.Board, depth=4, debug=False) -> chess.Move:
    best_move: chess.Move = chess.Move.from_uci("0000")
    if board.turn == chess.WHITE:
        best_eval = float("-inf")
        for move in board.generate_legal_moves():
            board.push(move)
            score = minimax(board, depth - 1)
            board.pop()
            if score > best_eval:
                best_eval = score
                best_move = move
    else:
        best_eval = float("inf")
        for move in board.generate_legal_moves():
            board.push(move)
            score = minimax(board, depth - 1)
            board.pop()
            if score < best_eval:
                best_eval = score
                best_move = move

    if debug:
        print("eval: ", best_eval)
        print("best_move: ", best_move)

    return best_move


def minimax(board: chess.Board, depth: int) -> int:
    if depth == 0:
        return eval(board)

    # find highest eval score for maximising player (white)
    if board.turn == chess.WHITE:
        max_e = -99999
        for move in board.generate_legal_moves():
            board.push(move)
            score = minimax(board, depth - 1)
            max_e = max(max_e, score)
            board.pop()
        return max_e

    else:
        min_e = 99999
        for move in board.generate_legal_moves():
            board.push(move)
            score = minimax(board, depth - 1)
            min_e = min(min_e, score)
            board.pop()
        return min_e
