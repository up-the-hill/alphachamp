import chess


piece_values = {
    chess.PAWN: 100,
    chess.KNIGHT: 300,
    chess.BISHOP: 350,
    chess.ROOK: 500,
    chess.QUEEN: 900,
}


def get_side_score(board: chess.Board, c: chess.Color) -> int:
    pawn_val = len(board.pieces(chess.PAWN, c)) * piece_values[chess.PAWN]
    knight_val = len(board.pieces(chess.KNIGHT, c)) * piece_values[chess.KNIGHT]
    bishop_val = len(board.pieces(chess.BISHOP, c)) * piece_values[chess.BISHOP]
    rook_val = len(board.pieces(chess.ROOK, c)) * piece_values[chess.ROOK]
    queen_val = len(board.pieces(chess.QUEEN, c)) * piece_values[chess.QUEEN]

    return pawn_val + knight_val + bishop_val + rook_val + queen_val
    


def eval(board: chess.Board):
    e = 0

    # +ve eval = better position for white
    # -ve eval = worse position for black
    e += get_side_score(board, chess.WHITE)
    e -= get_side_score(board, chess.BLACK)

    # add score for having pieces closer to the center of the board
    flip = 1 if board.turn == chess.WHITE else -1

    return e * flip


def next_move(board: chess.Board, depth=4, debug=False) -> chess.Move:
    best_move: chess.Move = chess.Move.from_uci("0000")
    max_e = -9999999
    for move in board.generate_legal_moves():
        board.push(move)
        score = -negamax(board, depth - 1)
        if score > max_e:
            max_e = score
            best_move = move
        board.pop()

    if debug:
        print("eval: ", max_e)
        print("best_move: ", best_move)

    return best_move


def negamax(board: chess.Board, depth: int) -> int:
    if depth == 0:
        return eval(board)

    max_e = -9999999

    if board.is_game_over():
        if board.is_checkmate():
            return -9999999
        else:
            return 0

    for move in board.generate_legal_moves():
        board.push(move)
        score = -negamax(board, depth - 1)
        if score > max_e:
            max_e = score
        board.pop()

    return max_e
