# -*- coding: utf-8 -*-
import numpy as np

class GameStatus:
    def __init__(self, board_state, turn_O):
        self.board_state = np.copy(board_state)
        self.turn_O = turn_O
        self.winner = None

    def is_terminal(self):
        """
        The game ends only when the board is full.
        """
        # If there are any empty cells (0s), the game continues
        for i in range(len(self.board_state)):
            for j in range(len(self.board_state[i])):
                if self.board_state[i][j] == 0:
                    return False
        return True  # Game is over only when no zeros remain

    def get_scores(self, terminal):
        """
        Counts all triplets for both players.
        +1 for each triplet by O (1)
        -1 for each triplet by X (-1)
        """
        rows = len(self.board_state)
        cols = len(self.board_state[0])
        score = 0

        # --- Horizontal triplets ---
        for i in range(rows):
            for j in range(cols - 2):
                triplet = self.board_state[i][j:j + 3]
                if np.all(triplet == 1):
                    score += 1
                elif np.all(triplet == -1):
                    score -= 1

        # --- Vertical triplets ---
        for j in range(cols):
            for i in range(rows - 2):
                triplet = [
                    self.board_state[i][j],
                    self.board_state[i + 1][j],
                    self.board_state[i + 2][j]
                ]
                if all(x == 1 for x in triplet):
                    score += 1
                elif all(x == -1 for x in triplet):
                    score -= 1

        # --- Diagonal (down-right) triplets ---
        for i in range(rows - 2):
            for j in range(cols - 2):
                if self.board_state[i][j] == 1 and \
                   self.board_state[i + 1][j + 1] == 1 and \
                   self.board_state[i + 2][j + 2] == 1:
                    score += 1
                elif self.board_state[i][j] == -1 and \
                     self.board_state[i + 1][j + 1] == -1 and \
                     self.board_state[i + 2][j + 2] == -1:
                    score -= 1

        # --- Diagonal (down-left) triplets ---
        for i in range(rows - 2):
            for j in range(2, cols):
                if self.board_state[i][j] == 1 and \
                   self.board_state[i + 1][j - 1] == 1 and \
                   self.board_state[i + 2][j - 2] == 1:
                    score += 1
                elif self.board_state[i][j] == -1 and \
                     self.board_state[i + 1][j - 1] == -1 and \
                     self.board_state[i + 2][j - 2] == -1:
                    score -= 1

        return score

    def get_negamax_scores(self, terminal):
        """
        Same as get_scores but formatted for Negamax.
        """
        return self.get_scores(terminal)

    def get_moves(self):
        """Returns all empty cells."""
        moves = []
        for i in range(len(self.board_state)):
            for j in range(len(self.board_state[i])):
                if self.board_state[i][j] == 0:
                    moves.append((i, j))
        return moves

    def get_new_state(self, move):
        """Returns a new GameStatus object after making a move."""
        new_board = np.copy(self.board_state)
        x, y = move
        new_board[x, y] = 1 if self.turn_O else -1
        return GameStatus(new_board, not self.turn_O)
