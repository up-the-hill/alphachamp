import chess


piece_values = {
    chess.PAWN: 100,
    chess.KNIGHT: 300,
    chess.BISHOP: 350,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 99999
}

centre_bonus_values = [
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 0,
    0, 1, 2, 3, 3, 2, 1, 0,
    0, 1, 3, 5, 5, 3, 1, 0,
    0, 1, 3, 5, 5, 3, 1, 0,
    0, 1, 2, 3, 3, 2, 1, 0,
    0, 1, 1, 1, 1, 1, 1, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
]

def get_side_score(board: chess.Board, c: chess.Color) -> int:
    pawn_val = len(board.pieces(chess.PAWN, c)) * piece_values[chess.PAWN]
    knight_val = len(board.pieces(chess.KNIGHT, c)) * piece_values[chess.KNIGHT]
    bishop_val = len(board.pieces(chess.BISHOP, c)) * piece_values[chess.BISHOP]
    rook_val = len(board.pieces(chess.ROOK, c)) * piece_values[chess.ROOK]
    queen_val = len(board.pieces(chess.QUEEN, c)) * piece_values[chess.QUEEN]

    centre_bonus = 0

    piece_squares = [square for square in chess.SQUARES if board.color_at(square) == c]

    for sq in piece_squares:
        centre_bonus += centre_bonus_values[sq]

    return pawn_val + knight_val + bishop_val + rook_val + queen_val + centre_bonus



def move_value(board: chess.Board, move: chess.Move):
    move_score = 0
    if board.is_capture(move):
        move_piece = board.piece_at(move.from_square)
        
        if board.is_en_passant(move):
            captured_piece_type = chess.PAWN
        else:
            target_piece = board.piece_at(move.to_square)
            if not target_piece:
                return 0 # Should not happen
            captured_piece_type = target_piece.piece_type

        if move_piece:
            move_score = piece_values[captured_piece_type] - piece_values[move_piece.piece_type]

    if move.promotion:
        move_score += piece_values[move.promotion]

    return move_score


def eval(board: chess.Board):
    e = 0

    # +ve eval = better position for white
    # -ve eval = worse position for black
    e += get_side_score(board, chess.WHITE)
    e -= get_side_score(board, chess.BLACK)

    flip = 1 if board.turn == chess.WHITE else -1

    return e * flip


def next_move(board: chess.Board, depth=4, debug=False) -> chess.Move:
    ordered_moves = sorted(board.legal_moves, key=lambda m: move_value(board, m), reverse=True)
    if not ordered_moves:
        return chess.Move.null()

    best_move: chess.Move = ordered_moves[0]
    max_e = -9999999

    for move in ordered_moves:
        board.push(move)
        score = -negamax(board, depth - 1, -99999, 99999)
        if score > max_e:
            max_e = score
            best_move = move
        board.pop()

    if debug:
        print("eval: ", max_e)
        print("best_move: ", best_move)

    return best_move


def negamax(board: chess.Board, depth: int, alpha: int, beta: int) -> int:
    if depth == 0:
        return eval(board)


    if board.is_game_over():
        if board.is_checkmate():
            return -9999999
        else:
            return -20 # contempt factor

    ordered_moves = sorted(board.legal_moves, key=lambda m: move_value(board, m), reverse=True)
    for move in ordered_moves:
        board.push(move)
        score = -negamax(board, depth - 1, -beta, -alpha)
        board.pop()
        if score >= beta:
            return beta
        alpha = max(alpha, score)

    return alpha
