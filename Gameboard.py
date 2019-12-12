# 18x18 Gameboard class object for Konane

from bitarray import bitarray


class Gameboard:
    def __init__(self, board_size):
        # Board setup. Stored as list of board_size numbers each with a bitarray
        # format: self.board[row][col]
        self.board_size = board_size
        assert (self.board_size < 31)
        assert (self.board_size > 3)
        assert (self.board_size % 2 == 0)
        self.board = [bitarray(self.board_size) for _ in range(self.board_size)]
        for bitarr in self.board:
            bitarr.setall(True)  # Start with entire board filled

        self.corners = {(0, 0), (self.board_size - 1, 0), (0, self.board_size - 1),
                        (self.board_size - 1, self.board_size - 1)}
        self.center = {(self.board_size / 2, self.board_size / 2), (self.board_size / 2 - 1, self.board_size / 2),
                       (self.board_size / 2, self.board_size / 2 - 1),
                       (self.board_size / 2 - 1, self.board_size / 2 - 1)}

    def is_valid_first(self, r, c, player):
        # First move valid if piece taken from center or corner
        if not self.is_players_space(r, c, player): return False
        if not self.is_filled(r, c): return False
        return ((r, c) in self.center) or ((r, c) in self.corners)

    def is_valid_second(self, r, c, previous_r, previous_c, player):
        # Second move valid if piece taken near other one
        if not self.is_players_space(r, c, player): return False
        if not self.is_filled(r, c): return False
        return (abs(r - previous_r) == 1 and abs(c - previous_c) == 0) or (
                abs(r - previous_r) == 0 and abs(c - previous_c) == 1)

    def is_in_bounds(self, r, c):
        return (0 <= r < self.board_size) and (0 <= c < self.board_size)

    def is_players_space(self, r, c, player):
        if not self.is_in_bounds(r, c): return False
        if player == 1 and (r + c) % 2 == 0:
            return True
        if player == 2 and (r + c % 2 == 1):
            return True
        return False

    def is_valid_jump(self, r1, c1, r2, c2, player):
        # Must stay within player's spaces
        if not (self.is_players_space(r1, c1, player) and self.is_players_space(r2, c2, player)): return False
        # stay in row/col, and have proper pieces inbetween
        if not self.is_filled(r1, c1): return False  # Piece must exist
        if not ((r1 == r2) ^ (c1 == c2)): return False  # Must stay in a line and can't be same piece
        if c1 == c2:
            for r in range(min(r1, r2) + 1, max(r1, r2), 2):  # Opponent's spaces must be filled
                if not self.is_filled(r, c1): return False
            for r in range(min(r1, r2) + 2, max(r1, r2) + 1, 2):  # Players's spaces must be empty
                if self.is_filled(r, c1): return False
        if r1 == r2:
            for c in range(min(c1, c2) + 1, min(c1, c2), 2):  # Opponent's spaces must be filled
                if not self.is_filled(r1, c): return False
            for c in range(min(c1, c2) + 2, min(c1, c2) + 1, 2):  # Players's spaces must be empty
                if self.is_filled(r1, c): return False
        return True

    def print_board(self, move_count):
        print("Move #" + str(move_count))
        for row in range(self.board_size):
            for col in range(self.board_size):
                if self.board[row][col]:
                    if (row + col) % 2 == 0:
                        print(" ● ", end="")
                    else:
                        print(" ◯ ", end="")
                else:
                    print("   ", end="")
            print()
        print()

    def is_filled(self, r, c):
        # Returns True if space is occupied, otherwise returns False
        if not self.is_in_bounds(r, c): return False
        return self.board[r][c]

    def set_piece(self, r, c, val):
        self.board[r][c] = val

    def do_jump(self, r1, c1, r2, c2):
        if r1 == r2:
            for c in range(c1, c2, int((c2 - c1) / abs(c2 - c1))):
                self.set_piece(r1, c, False)
        elif c1 == c2:
            for r in range(r1, r2, int((r2 - r1) / abs(r2 - r1))):
                self.set_piece(r, c1, False)
        self.set_piece(r2, c2, True)

    def possible_moves(self):
        return

#   empty = 0, black = 1, white = 2
#         self.letter_number = {'a':0,'b':1,'c':2,'d':3,'e':4,'f':5,'g':6,'h':7,
#         'i':8,'j':9,'k':10,'l':11,'m':12,'n':13,'o':14,'p':15,'q':16,'r':17}
#
#     def convert_location(self, loc):
#         col = str(loc[:1])
#         row = int(loc[1:])
#         col = self.letter_number.get(col)
#         row = 18 - row
#         return col, row
#
#     def get_value(self, loc):
#         col, row = self.convert_location(loc)
#         val = self.board[row][col]
#         print(val)
#
#     def change_value(self, loc, new_val):
#         col, row = self.convert_location(loc)
#         self.board[row][col] = new_val
#
#
# temp = Gameboard(18)
# temp.get_value('a18')
# temp.change_value('a18', 0)
# temp.get_value('a18')
