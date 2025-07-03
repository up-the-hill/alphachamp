import chess
from alphachamp import next_move, eval
import ui


# setup
board = chess.Board()
version = "v0.1"


def run_ui_mode():
    player_side = (
        chess.WHITE if input("Play as white or black (w/b) ") == "w" else chess.BLACK
    )

    while not board.is_game_over():
        if board.turn == player_side:
            try:
                print(ui.render(board))
                move_san = input("Move: ")
                board.push_san(move_san)
            except chess.IllegalMoveError:
                print("Illegal move; try again")
            except chess.InvalidMoveError:
                print("Invalid move; try again")
        else:
            board.push(next_move(board, debug=True))


def run_uci_mode():
    print("id name alphachamp")
    print("id author up-the-hill")
    print("uciok")

    while True:
        line = input()
        if not line:
            continue
        args = line.strip().split()
        cmd = args[0]

        if cmd == "isready":
            print("readyok")

        elif cmd == "quit":
            break

        elif cmd == "position":
            if len(args) < 2:
                continue

            if args[1] == "startpos":
                board.reset()
                move_index = 2
            elif args[1] == "fen":
                fen = " ".join(args[2:8])
                board.set_fen(fen)
                move_index = 8
            else:
                continue

            if len(args) > move_index and args[move_index] == "moves":
                for move in args[move_index + 1 :]:
                    board.push_uci(move)

        elif cmd == "go":
            print("bestmove ", next_move(board))


def main():
    print(f"Alphachamp {version}")
    print('Enter "ui" to enter ui mode (debug)')
    print('Enter "uci" to enter uci mode')
    print('Enter "eval <fen>" to evaluate a position.')
    while True:
        args = input().strip().split()
        if not args:
            continue

        cmd = args[0]

        if cmd == "ui":
            if len(args) > 1:
                board.set_fen(" ".join(args[1:]))
            run_ui_mode()
            break

        elif cmd == "uci":
            run_uci_mode()
            break

        elif cmd == "eval":
            board.set_fen(" ".join(args[1:]))
            print(ui.render(board))
            print("Eval: ", eval(board))
            break

        else:
            print("Unknown command. Please enter 'ui' or 'uci'.")


main()
