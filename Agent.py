# Agent.py
# Contains all input streams and handling for artificial intelligence
from Game import Move
from Gameboard import Gameboard
from Player import Player

class Agent(Player):

    def __init__(self, name, is_bottom_left):
        super().__init__(name, is_bottom_left)
        self.name = name

        self.agent = not is_bottom_left
        self.opp = is_bottom_left

        # list of feature weigths
        #   0 = weighting for a player's number of moves
        #   1 = weighting for a player's ordinary pieces
        #   2 = weighting for a player's side pieces
        #   3 = weighting for a player's corner pieces
        # positive weight for agent
        # negative weight for opponent
        self.weights = [1, 1, 1, 1]

    # counts total number of pieces available to a player
    def pieceCount(self, board, is_bottom_left):
        size = board.board_size
        count = 0
        for row in range(0, size):
            # Player 1: Even rows start at index 0
            # Player 2: Non-even rows start at index 0
            start = 0

            # Player 1: Non-even rows start at index 1
            # Player 2: Even rows start at index 1
            if (is_bottom_left and row % 2 != 0) or (not is_bottom_left and row % 2 == 0):
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
    def moveList(self, board, is_bottom_left):
        all_moves = board.possible_moves()
        moves = []
        for m in all_moves:
            piece = m[0]
            r, c = piece[0], piece[1]
            if is_bottom_left:
                if (r + c) % 2 == 0: moves.append(m)
            else:
                if (r + c) % 2 != 0: moves.append(m)
        return moves
    def agent_move_list(self, board):
        return self.moveList(board, self.agent)
    def opp_move_list(self, board):
        return self.moveList(board, self.opp)

    # counts number of corner pieces belonging to a player
    def cornerPieces(self, board, is_bottom_left):
        all_corners = board.corners
        corner = 0
        for p in all_corners:
            r, c = p[0], p[1]
            if is_bottom_left:
                if (r+c) % 2 == 0 and board.is_filled(r, c): corner += 1
            else:
                if (r+c) % 2 != 0 and board.is_filled(r, c): corner += 1
        return corner
    def agent_corner_count(self, board):
        return self.cornerPieces(board, self.agent)
    def opp_corner_count(self, board):
        return self.cornerPieces(board, self.opp)

    # counts number of side pieces belonging to a player
    def sidePieces(self, board, is_bottom_left):
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
                if is_bottom_left:
                    if (r + c) % 2 == 0 and board.is_filled(r, c): count += 1
                else:
                    if (r + c) % 2 != 0 and board.is_filled(r, c): count += 1
        return count
    def agent_side_count(self, board):
        return self.sidePieces(board, self.agent)
    def opp_side_count(self, board):
        return self.sidePieces(board, self.opp)

    # determines score of a gameboard
    # takes into consideration # of moves and # of pieces for both players
    # agent = positive score, opponent = negative score
    def gamescore(self, board, agent_moveList, opp_moveList):

        agent_MoveCount = len(agent_moveList)
        opp_MoveCount = len(opp_moveList)

        # if agent has moves to make and opp doesn't, return very high score
        if agent_MoveCount > 0 and opp_MoveCount == 0:
            return 100000

        # if agent has no moves to make and opp does, return very low score
        if agent_MoveCount == 0 and opp_MoveCount > 0:
            return -100000

        agent_piece = self.agent_piece_count(board)
        opp_piece = self.opp_piece_count(board)

        agent_side = self.agent_side_count(board)
        opp_side = self.opp_side_count(board)

        agent_corner = self.agent_corner_count(board)
        opp_corner = self.opp_corner_count(board)

        agent_MoveWeight = self.weights[0]
        opp_MoveWeight = -1 * self.weights[0]

        agent_PieceWeight = self.weights[1]
        opp_PieceWeight = -1 * self.weights[1]

        agent_SideWeight = self.weights[2]
        opp_SideWeight = -1 * self.weights[2]

        agent_CornerWeight = self.weights[3]
        opp_CornerWeight = -1 * self.weights[3]

        score = (agent_MoveCount * agent_MoveWeight) + (opp_MoveCount * opp_MoveWeight) + (agent_piece * agent_PieceWeight) + (opp_piece * opp_PieceWeight) + (agent_side * agent_SideWeight) + (opp_side * opp_SideWeight) + (agent_corner * agent_CornerWeight) + (opp_corner * opp_CornerWeight)

        return score

    # lookahead 2 moves
    # alpha-beta pruning hopefully
    # if depth = 0, agent's turn, find max
    # if depth = 1, opp's turn, find min
    # if depth = 2, return score
    def minimax(self, board, depth, alpha, beta):
        agent_moves = self.agent_move_list(board)
        opp_moves = self.opp_move_list(board)

        if depth == 2:
            return self.gamescore(board, agent_moves, opp_moves), None

#        if depth == 2 or self.is_terminal_state(board, agent_moves, opp_moves):
#            return self.gamescore(board, agent_moves, opp_moves), None

        best_value = None
        best_move = ((-1, -1), (-1, -1))
        if depth == 0:
            best_value = float('-inf')
            for m in agent_moves:
                new_state = board.clone()
                new_state.do_jump(m[0][0], m[0][1], m[1][0], m[1][1])
                child_score, child_move = self.minimax(new_state, depth+1, alpha, beta)

                if best_value < child_score:
                    best_value = child_score
                    best_move = m
                    alpha = max([alpha, best_value])
                    if beta <= alpha:
                        return best_value, best_move
        elif depth == 1:
            best_value = float('inf')
            for m in opp_moves:
                new_state = board.clone()
                new_state.do_jump(m[0][0], m[0][1], m[1][0], m[1][1])
                child_score, child_move = self.minimax(new_state, depth+1, alpha, beta)

                if best_value > child_score:
                    best_value = child_score
                    best_move = m
                    beta = min([beta, best_value])
                    if beta <= alpha:
                        return best_value, best_move
        return best_value, best_move

    def get_move(self, board, prev_move):
        empty = board.empty_tiles()
        if len(empty) <= 1:
            moves = self.agent_move_list(board)
            m = moves[0]
        else:
            score, m = self.minimax(board, 0, float('-inf'), float('inf'))
        print(m)
        move: Move = Move(m[0][0], m[0][1], m[1][0], m[1][1])
        return move
