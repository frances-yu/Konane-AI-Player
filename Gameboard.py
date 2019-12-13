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
        self.center = {(int(self.board_size / 2), int(self.board_size / 2)),    (int(self.board_size / 2 - 1), int(self.board_size / 2)),
                       (int(self.board_size / 2), int(self.board_size / 2 - 1)),
                       (int(self.board_size / 2 - 1), int(self.board_size / 2 - 1))}

    def is_valid_first(self, r, c, color):
        # First move valid if piece taken from center or corner
        if not self.is_players_space(r, c, color): return False
        if not self.is_filled(r, c): return False
        return ((r, c) in self.center) or ((r, c) in self.corners)

    def is_valid_second(self, r, c, previous_r, previous_c, color):
        # Second move valid if piece taken near other one
        if not self.is_players_space(r, c, color): return False
        if not self.is_filled(r, c): return False
        return (abs(r - previous_r) == 1 and abs(c - previous_c) == 0) or (
                abs(r - previous_r) == 0 and abs(c - previous_c) == 1)

    def is_in_bounds(self, r, c):
        return (0 <= r < self.board_size) and (0 <= c < self.board_size)

    def is_players_space(self, r, c, color):
        if not self.is_in_bounds(r, c): return False
        if color == 'White' and (r + c) % 2 != 0:
            return True
        if color == 'Black' and (r + c) % 2 == 0:
            return True
        return False

    def is_valid_jump(self, r1, c1, r2, c2, color):
        # Must stay within player's spaces
        if not (self.is_players_space(r1, c1, color) and self.is_players_space(r2, c2, color)): return False
        # stay in row/col, and have proper pieces inbetween
        if not self.is_filled(r1, c1): return False  # Piece must exist
        if not ((r1 == r2) ^ (c1 == c2)): return False  # Must stay in a line and can't be same piece
        if c1 == c2:
            for r in range(min(r1, r2) + 1, max(r1, r2), 2):  # Opponent's spaces must be filled
                if not self.is_filled(r, c1): return False
            for r in range(min(r1, r2) + 2, max(r1, r2), 2):  # Players's spaces must be empty
                if self.is_filled(r, c1): return False
            if self.is_filled(r2, c2): return False  # Destination must be empty
        if r1 == r2:
            for c in range(min(c1, c2) + 1, max(c1, c2), 2):  # Opponent's spaces must be filled
                if not self.is_filled(r1, c): return False
            for c in range(min(c1, c2) + 2, max(c1, c2), 2):  # Players's spaces must be empty
                if self.is_filled(r1, c): return False
            if self.is_filled(r2, c2): return False  # Destination must be empty
        return True

    def print_board(self, move_count):
        print("Move #" + str(move_count))
        for row in range(self.board_size-1,-1,-1):
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

    # Snipers are the validly existing pieces that can potentially jump into tile: (r, c)
    # this function returns a list of tuples (r, c) of the snipers
    # i did a ton of math to figure this out :((
    def snipers(self, tile):
        pieces = []
        r = tile[0]
        c = tile[1]

        neg_r_steps = 0
        pos_r_steps = 0

        neg_c_steps = 0
        pos_c_steps = 0

        if r % 2 == 0:
            neg_r_steps = int(r/2)
            pos_r_steps = int((self.board_size - (r + 2))/2)
        else:
            neg_r_steps = int((r-1)/2)
            pos_r_steps = int((self.board_size - (r+1))/2)

        if c % 2 == 0:
            neg_c_steps = int(c/2)
            pos_c_steps = int((self.board_size - (c + 2))/2)
        else:
            neg_c_steps = int((c-1)/2)
            pos_c_steps = int((self.board_size - (c+1))/2)

        for i in range(0, neg_r_steps):
            row = r - 2*(i+1)
            col = c
            if not self.board[row + 1][c]: break
            elif self.board[row][col]:
                pieces.append((row, col))
                break

        for i in range(0, pos_r_steps):
            row = r + 2*(i+1)
            col = c
            if not self.board[row-1][col]: break
            elif self.board[row][col]:
                pieces.append((row, col))
                break

        for i in range(0, neg_c_steps):
            row = r
            col = c - 2*(i+1)
            if not self.board[row][col+1]: break
            elif self.board[row][col]:
                pieces.append((row, col))
                break

        for i in range(0, pos_c_steps):
            row = r
            col = c + 2*(i+1)
            if not self.board[row][col-1]: break
            elif self.board[row][col]:
                pieces.append((row, col))
                break

        return pieces

    # returns list of tuples (r, c) representing all empty tiles
    def empty_tiles(self):
        empty = []
        for row in range(0, self.board_size):
            for col in range(0, self.board_size):
                if not self.board[row][col]:
                    empty_tile = (row, col)
                    empty.append(empty_tile)
        return empty

    # generates list of the empty tiles
    # generates list of pieces that can jump into each empty tile
    # pieces and tiles formatted to be a valid move
    # pieces (r1, c1), empty tile (r2, c2)
    # RETURNS: ((r1, c1), (r2, c2))
    def possible_moves(self):
        moves = []

        empty_tiles = self.empty_tiles()

        if len(empty_tiles) == 0:
            for i in self.corners:
                moves.append((i, i))
            for i in self.center:
                moves.append((i, i))
            return moves
        elif len(empty_tiles) == 1:
            r, c = empty_tiles[0][0], empty_tiles[0][1]
            m = [(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)]
            for i in range(0, len(m)):
                if self.is_in_bounds(m[i][0], m[i][1]):
                    moves.append((m[i], m[i]))
            return moves
        elif len(empty_tiles) >= 2:
            for tile in empty_tiles:
                candidates = self.snipers(tile)
                for c in candidates:
                    moves.append((c, tile))
        return moves

    def even_moves(self):
        moves = []
        empty_tiles = self.empty_tiles()
        if len(empty_tiles) == 0:
            for i in self.corners:
                if (i[0] + i[1]) % 2 == 0:
                    moves.append((i, i))
            for i in self.center:
                if (i[0] + i[1] % 2 == 0):
                    moves.append((i, i))
            return moves
        elif len(empty_tiles) == 1:
            r, c = empty_tiles[0][0], empty_tiles[0][1]
            m = [(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)]
            for i in range(0, len(m)):
                if self.is_in_bounds(m[i][0], m[i][1]):
                    if (m[i][0] + m[i][1]) % 2 == 0:
                        moves.append((m[i], m[i]))
            return moves
        elif len(empty_tiles) >= 2:
            for tile in empty_tiles:
                candidates = self.snipers(tile)
                for c in candidates:
                    if (c[0] + c[1]) % 2 == 0:
                        moves.append((c, tile))
        return moves
    def odd_moves(self):
        moves = []
        empty_tiles = self.empty_tiles()
        if len(empty_tiles) == 0:
            for i in self.corners:
                if (i[0] + i[1]) % 2 != 0:
                    moves.append((i, i))
            for i in self.center:
                if (i[0] + i[1] % 2 != 0):
                    moves.append((i, i))
            return moves
        elif len(empty_tiles) == 1:
            r, c = empty_tiles[0][0], empty_tiles[0][1]
            m = [(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)]
            for i in range(0, len(m)):
                if self.is_in_bounds(m[i][0], m[i][1]):
                    if (m[i][0] + m[i][1]) % 2 != 0:
                        moves.append((m[i], m[i]))
            return moves
        elif len(empty_tiles) >= 2:
            for tile in empty_tiles:
                candidates = self.snipers(tile)
                for c in candidates:
                    if (c[0] + c[1]) % 2 != 0:
                        moves.append((c, tile))
        return moves

    # create a new Gameboard of the same size
    # set its board to be the same as the current Gameboard
    def clone(self):
        copy = Gameboard(self.board_size)
        for row in range(0, self.board_size):
            copy.board[row] = self.board[row].copy()
        return copy
