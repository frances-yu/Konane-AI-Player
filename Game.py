# Game.py
# Implements all game mechanics


from Gameboard import Gameboard


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

        # Start
        self.playing_loop()

    # Main loop
    def playing_loop(self):
        player_turn = 1  # player who's turn it is
        while not self.is_game_over():
            self.board.print_board(self.move_count)  # Show board

            # Query for player's move, verify the move is valid, then do the move
            valid_move = False
            move = None
            while not valid_move:
                if player_turn == 1:
                    move = self.player1.get_move(self.board)
                else:
                    move = self.player2.get_move(self.board)
                valid_move = self.is_valid_move(move, player_turn)
                if not valid_move:
                    print("Not a valid move")
            self.do_move(move)
            self.previous_move = move
            self.move_count += 1

            # Switch turns
            if player_turn == 1:
                player_turn = 2
            else:
                player_turn = 1

    def is_valid_move(self, move: Move, player):
        # Checks if move is valid based on number of moves taken so far

        # First move valid if from center or corner
        if self.move_count == 0:
            if not self.board.is_valid_first(move.r1, move.c1, player): return False

        # Second move valid if next to previous move
        elif self.move_count == 1:
            if not self.board.is_valid_second(move.r1, move.c1, self.previous_move.r1, self.previous_move.c1, player):
                return False

        # Other moves need to be a jump
        else:
            if not self.board.is_valid_jump(move.r1, move.c1, move.r2, move.c2, player): return False
        return True

    def is_game_over(self):
        # Checks if there are no moves left
        # TODO return len(self.board.possible_moves()) == 0
        return False

    def do_move(self, move):
        # First two moves remove
        if self.move_count <= 1:
            self.board.set_piece(move.r1, move.c1, False)

        # Other moves need to be a jump
        else:
            self.board.do_jump(move.r1, move.c1, move.r2, move.c2)
