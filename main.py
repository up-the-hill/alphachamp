import chess
from alphachamp import next_move
import ui

# setup
board = chess.Board()

# game loop
while True:
    args = input().split()

    if args[0] == "ui":
        # enter terminal interface
        player_side = (
            chess.WHITE if input("Play as white or black (w/b)") == "w" else chess.BLACK
        )
        # game loop
        while not board.is_game_over():
            if board.turn == player_side:
                try:
                    print(ui.render(board))
                    board.push_san(input("Move:"))
                except chess.IllegalMoveError:
                    print("invalid move; try again")
            else:
                board.push(next_move(board))
        break

    if args[0] == "uci":
        print("id name alphachamp")
        print("id author up-the-hill")
        print("uciok")

    elif args[0] == "isready":
        print("readyok")

    elif args[0] == "quit":
        break

    elif args[0] == "position":
        if args[1] == "startpos":
            board.reset()
        else:
            board.set_board_fen(args[-1])
        if len(args) > 2:
            if args[2] == "moves":
                for move in args[3:]:
                    board.push_uci(move)

    # elif args[:2] == ["position", "startpos"]:
    #     del hist[1:]
    #     for ply, move in enumerate(args[3:]):
    #         i, j, prom = parse(move[:2]), parse(move[2:4]), move[4:].upper()
    #         if ply % 2 == 1:
    #             i, j = 119 - i, 119 - j
    #         hist.append(hist[-1].move(Move(i, j, prom)))

    elif args[0] == "go":
        # wtime, btime, winc, binc = [int(a) / 1000 for a in args[2::2]]
        # if len(hist) % 2 == 0:
        #     wtime, winc = btime, binc
        # think = min(wtime / 40 + winc, wtime / 2 - 1)
        #
        # start = time.time()
        # move_str = None
        # for depth, gamma, score, move in Searcher().search(hist):
        #     # The only way we can be sure to have the real move in tp_move,
        #     # is if we have just failed high.
        #     if score >= gamma:
        #         i, j = move.i, move.j
        #         if len(hist) % 2 == 0:
        #             i, j = 119 - i, 119 - j
        #         move_str = render(i) + render(j) + move.prom.lower()
        #         print("info depth", depth, "score cp", score, "pv", move_str)
        #     if move_str and time.time() - start > think * 0.8:
        #         break
        #
        # print("bestmove", move_str or "(none)")
        print("bestmove ", next_move(board))
