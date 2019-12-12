# Agent.py
# Contains all input streams and handling for artificial intelligence
from Game import Move
from Gameboard import Gameboard
from Player import Player


class Agent(Player):

    def __init__(self, name, is_top_left):
        super().__init__(name, is_top_left)
        self.name = name

        self.agent = is_top_left
        self.opp = not is_top_left

        # list of feature weigths
        #   0 = weighting for a player's number of moves
        #   1 = weighting for a player's number of pieces
        # positive weight for agent
        # negative weight for opponent
        self.weights = [1, 1]

    # counts total number of pieces available to a player
    def pieceCount(self, board, is_player_one):
        size = board.board_size
        count = 0
        for row in range(0, size):
            # Player 1: Even rows start at index 0
            # Player 2: Non-even rows start at index 0
            start = 0

            # Player 1: Non-even rows start at index 1
            # Player 2: Even rows start at index 1
            if (is_player_one and row % 2 != 0) or (not is_player_one and row % 2 == 0):
                start = 1

            # step size = 2 because player's piece exists every other tile
            for col in range(start, size, 2):
                # board[row][col]: True if piece, False if not
                if board.board[row][col]: count += 1
        return count
    def agent_piece_count(self, board):
        return self.pieceCount(board, self.agent)
    def opp_piece_count(self, board):
        return self.pieceCount(board, self.opp)

    # determines list of possible moves for a player
    def moveList(self, board, is_player_one):
        all_moves = board.possible_moves()
        moves = []
        for m in all_moves:
            piece = m[0]
            r, c = piece[0], piece[1]
            if is_player_one:
                if (r + c) % 2 == 0: moves.append(m)
            else:
                if (r + c) % 2 != 0: moves.append(m)
        return moves
    def agent_move_list(self, board):
        return self.moveList(board, self.agent)
    def opp_move_list(self, board):
        return self.moveList(board, self.opp)

    # counts number of corner pieces belonging to a player
    def cornerPieces(self, board, is_player_one):
        all_corners = board.corners
        corner = 0
        for p in all_corners:
            r, c = p[0], p[1]
            if is_player_one:
                if (r+c) % 2 == 0 and board.is_filled(r, c): corner += 1
            else:
                if (r+c) % 2 != 0 and board.is_filled(r, c): corner += 1
        return corner
    def agent_corner_count(self, board):
        return self.cornerPieces(board, self.agent)
    def opp_corner_count(self, board):
        return self.cornerPieces(board, self.opp)

    # counts number of side pieces belonging to a player
    def sidePieces(self, board, is_player_one):
        size = board.board_size
        count = 0
        for i in range(1, size - 1):
            top = (0, i)
            bottom = (size - 1, i)
            right = (i, 0)
            left = (i, size - 1)
            candidates = [top, bottom, right, left]
            for p in candidates:
                r, c = p[0], p[1]
                if is_player_one:
                    if (r + c) % 2 == 0 and board.is_filled(r, c): count += 1
                else:
                    if (r + c) % 2 != 0 and board.is_filled(r, c): count += 1
        return count
    def agent_side_count(self, board):
        return self.sidePieces(board, self.agent)
    def opp_side_count(self, board):
        return self.sidePieces(board, self.opp)

    # determines score of a piece - NOT BEING USED
    def scorePiece(self, row, col):
        return

    # determines score of a gameboard
    # takes into consideration # of moves and # of pieces for both players
    # agent = positive score, opponent = negative score
    def gamescore(self, board, agent_moveList, opp_moveList):

        agent_MoveCount = len(agent_moveList)
        opp_MoveCount = len(opp_moveList)

        agent_PieceScore = self.agent_piece_count(board) + self.agent_side_count(board) + 2*self.agent_corner_count(board)

        opp_PieceScore = self.opp_piece_count(board) + self.opp_side_count(board) + 2 * self.opp_corner_count(board)

        agent_MoveWeight = self.weights[0]
        opp_MoveWeight = -1 * self.weights[0]
        agent_PieceWeight = self.weights[1]
        opp_PieceWeight = -1 * self.weights[1]

        score = (agent_MoveCount * agent_MoveWeight) + (opp_MoveCount * opp_MoveWeight) + (agent_PieceScore * agent_PieceWeight) + (opp_PieceScore * opp_PieceWeight)

        return score

    # lookahead 3 moves
    # alpha-beta pruning hopefully
    # if depth = 0, agent's turn, find max
    # if depth = 1, opp's turn, find min
    # if depth = 2, agent's turn, find max
    # if depth = 3, return score
    def minimax(self, board):
        moves = self.agent_move_list(board)
        return moves

    def get_move(self, board):

        move_tuple = ()
        empty = board.empty_tiles()
        if len(empty) <= 1:
            moves = board.possible_moves()
#            print("AI MOVE: ", moves[0])
            print(" ")
            move_tuple = moves[0]
        else:
            moves = self.minimax(board)
#            print("AI MOVE: ", moves[0])
            print(" ")
            move_tuple = moves[0]

        print(" ")

        move: Move = Move(move_tuple[0][0], move_tuple[0][1],
                          move_tuple[1][0], move_tuple[1][1])
        return move
