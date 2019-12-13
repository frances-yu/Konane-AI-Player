# Game.py
# Implements all game mechanics


from Gameboard import Gameboard
import time


class Move:
    def __init__(self, r1, c1, r2=-1, c2=-1):
        self.r1 = r1
        self.c1 = c1
        self.r2 = r2
        self.c2 = c2


class Game:
    def __init__(self, player1, player2, board_size=18):
        # Board setup
        self.board = Gameboard(board_size)

        # Player1 setup (white, has top left piece)
        self.player1 = player1
        # Player2 setup (black, has top right piece)
        self.player2 = player2

        # Game variables
        self.move_count = 0
        self.previous_move: Move = Move(-1, -1, -1, -1)

        self.winner = None
        self.lose = None

        # Start
        self.playing_loop()

    # Main loop
    def playing_loop(self):
        player_turn = 1  # player who's turn it is
        done = False
        total_time = time.time()
        while not self.is_game_over():

            self.board.print_board(self.move_count)  # Show board

            # Query for player's move, verify the move is valid, then do the move
            start = time.time()
            valid_move = False
            move = None
            color = ''
            while not valid_move:
                if player_turn == 1:
                    color = self.player1.name
                    move = self.player1.get_move(self.board, self.previous_move)
                else:
                    color = self.player2.name
                    move = self.player2.get_move(self.board, self.previous_move)
                valid_move = self.is_valid_move(move, color)
                if not valid_move:
                    done = move.r1 == -1 and move.c1 == -1 and move.r2 == -1 and move.c2 == -1
                    if done:
                        break
                    print("Not valid move")
            if done: break
            self.do_move(move)
            self.previous_move = move
            self.move_count += 1
            end = time.time() - start
            print(end)
            print("PLAYER " + str(player_turn) + ': ' + color)

            # Switch turns
            if player_turn == 1:
                player_turn = 2
            else:
                player_turn = 1

        if player_turn == 1:
            self.winner = 2
            self.loser = 1
            player_turn = 2
        else:
            self.winner = 1
            self.loser = 2
            player_turn = 1

        print("GAME OVER")
        print(time.time() - total_time)
        print("WINNER: PLAYER " + str(player_turn))
        self.board.print_board(self.move_count)

    def is_valid_move(self, move: Move, color):
        # Checks if move is valid based on number of moves taken so far

        # First move valid if from center or corner
        if self.move_count == 0:
            if not self.board.is_valid_first(move.r1, move.c1, color): return False

        # Second move valid if next to previous move
        elif self.move_count == 1:
            if not self.board.is_valid_second(move.r1, move.c1, self.previous_move.r1, self.previous_move.c1, color):
                return False

        # Other moves need to be a jump
        else:
            if not self.board.is_valid_jump(move.r1, move.c1, move.r2, move.c2, color): return False
        return True

    def is_game_over(self):
        # Checks if there are no moves left
        return False

    def do_move(self, move):
        # First two moves remove
        if self.move_count <= 1:
            self.board.set_piece(move.r1, move.c1, False)

        # Other moves need to be a jump
        else:
            self.board.do_jump(move.r1, move.c1, move.r2, move.c2)
