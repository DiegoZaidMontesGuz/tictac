# -*- coding: utf-8 -*-
import numpy as np

class GameStatus:
    def __init__(self, board_state, turn_O):
        self.board_state = board_state
        self.turn_O = turn_O
        self.oldScores = 0
        self.winner = ""

    # ------------------------------
    # Terminal state check
    # ------------------------------
    def is_terminal(self):
        # Terminal if no empty cells left (no 0s)
        for row in self.board_state:
            for cell in row:
                if cell == 0:
                    return False
        return True

    # ------------------------------
    # Minimax scoring
    # ------------------------------
    def get_scores(self, terminal):
        rows = len(self.board_state)
        cols = len(self.board_state[0])
        scores = 0

        # Horizontal
        for r in range(rows):
            for c in range(cols - 2):
                window = self.board_state[r, c:c + 3]
                s = int(np.sum(window))
                if s == 3:
                    scores += 1   # O (1)
                elif s == -3:
                    scores -= 1   # X (-1)

        # Vertical
        for c in range(cols):
            for r in range(rows - 2):
                window = self.board_state[r:r + 3, c]
                s = int(np.sum(window))
                if s == 3:
                    scores += 1
                elif s == -3:
                    scores -= 1

        # Diagonal down-right
        for r in range(rows - 2):
            for c in range(cols - 2):
                s = int(self.board_state[r, c] + self.board_state[r + 1, c + 1] + self.board_state[r + 2, c + 2])
                if s == 3:
                    scores += 1
                elif s == -3:
                    scores -= 1

        # Diagonal up-right
        for r in range(2, rows):
            for c in range(cols - 2):
                s = int(self.board_state[r, c] + self.board_state[r - 1, c + 1] + self.board_state[r - 2, c + 2])
                if s == 3:
                    scores += 1
                elif s == -3:
                    scores -= 1

        return scores

    # ------------------------------
    # Negamax scoring (identical or weighted version)
    # ------------------------------
    def get_negamax_scores(self, terminal):
        # Same as get_scores (can be scaled if desired)
        return self.get_scores(terminal)

    # ------------------------------
    # Generate all possible moves (empty cells)
    # ------------------------------
    def get_moves(self):
        moves = []
        rows = len(self.board_state)
        cols = len(self.board_state[0])
        for r in range(rows):
            for c in range(cols):
                if self.board_state[r, c] == 0:
                    moves.append((r, c))
        return moves

    # ------------------------------
    # Create a new board state after a move
    # ------------------------------
    def get_new_state(self, move):
        new_board_state = np.copy(self.board_state)
        x, y = move
        new_board_state[x, y] = 1 if self.turn_O else -1
        return GameStatus(new_board_state, not self.turn_O)
