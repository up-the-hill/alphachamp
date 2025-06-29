import chess
from alphachamp import next_move
import ui

# setup
board = chess.Board()


def run_ui_mode():
    board = chess.Board()
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
                print("invalid move; try again")
        else:
            board.push(next_move(board, True))


def run_uci_mode():
    board = chess.Board()
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
    while True:
        args = input().strip().split()
        if not args:
            continue

        cmd = args[0]

        if cmd == "ui":
            run_ui_mode()
            break

        elif cmd == "uci":
            run_uci_mode()
            break

        else:
            print("Unknown command. Please enter 'ui' or 'uci'.")


main()
