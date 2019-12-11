# Game.py
# Implements all game mechanics

from bitarray import bitarray


class Game:
    def __init__(self, player1, player2, board_size=18):
        # Board setup. Stored as list of board_size numbers each with a bitarray
        # format: self.board[row][col]
        self.board_size = board_size
        assert(self.board_size < 31)
        assert (self.board_size > 5)
        assert (self.board_size % 2 == 0)
        self.board = [bitarray(self.board_size) for i in range(self.board_size)]
        for bitarr in self.board:
            bitarr.setall(True)  # Start with entire board filled

        # Player1 setup (black, has top left piece)
        self.player1 = player1
        # Player2 setup (white, has top right piece)
        self.player2 = player2

        # Game variables
        self.move_count = 0

    # Main loop
    def playing_loop(self):
        done = True
        player_turn = self.player1  # player who's turn it is
        while not done:
            self.print_board() # Show board
            # Query for player's move, verify the move is valid, then do the move
            valid_move = False
            while not valid_move:
                move = player_turn.get_move()
                valid_move = self.is_valid_move(move)
                if not valid_move:
                    print("Not a valid move")
                else:
                    self.do_move(move)
            # Check if the game is over
            done = self.is_game_over()
            # Switch turns
            if player_turn is self.player1:
                player_turn = self.player2
            else:
                player_turn = self.player1


    # Checks if move is valid
    def is_valid_move(self, move):
        return False

    def is_game_over(self):
        return False

    def do_move(self, move):
        pass

    def print_board(self):
        for row in range(self.board_size):
            for col in range(self.board_size):
                if self.board[row][col]:
                    if (row+col) % 2 == 0:
                        print(" ● ", end="")
                    else:
                        print(" ◯ ", end="")
                else:
                    print("   ", end="")
            print()
        print()




