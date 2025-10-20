# -*- coding: utf-8 -*-
import numpy as np

class GameStatus:
    def __init__(self, board_state, turn_O):
        self.board_state = np.copy(board_state)
        self.turn_O = turn_O
        self.winner = None

    def is_terminal(self):
        """
        Checks if the game has ended.
        Returns True if a player has won or the board is full.
        """
        rows = len(self.board_state)
        cols = len(self.board_state[0])

        

        # --- Check rows ---
        for i in range(rows):
            for j in range(cols - 2):
                if self.board_state[i][j] != 0 and \
                   self.board_state[i][j] == self.board_state[i][j + 1] == self.board_state[i][j + 2]:
                    self.winner = self.board_state[i][j]
                    return True

        # --- Check columns ---
        for j in range(cols):
            for i in range(rows - 2):
                if self.board_state[i][j] != 0 and \
                   self.board_state[i][j] == self.board_state[i + 1][j] == self.board_state[i + 2][j]:
                    self.winner = self.board_state[i][j]
                    return True

        # --- Check diagonals ---
        for i in range(rows - 2):
            for j in range(cols - 2):
                # Down-right diagonal
                if self.board_state[i][j] != 0 and \
                   self.board_state[i][j] == self.board_state[i + 1][j + 1] == self.board_state[i + 2][j + 2]:
                    self.winner = self.board_state[i][j]
                    return True

                # Down-left diagonal
                if self.board_state[i][j + 2] != 0 and \
                   self.board_state[i][j + 2] == self.board_state[i + 1][j + 1] == self.board_state[i + 2][j]:
                    self.winner = self.board_state[i][j + 2]
                    return True

        # --- Check for draw (no empty spaces) ---
        if not (0 in self.board_state):
            self.winner = 0
            return True

        return False

    def get_scores(self, terminal):
        """
        Computes a simple evaluation score for the board.
        +1 if O (human) wins
        -1 if X (AI) wins
         0 otherwise or draw
        """
        if self.winner == 1:
            return 1
        elif self.winner == -1 or self.winner == 2:
            return -1
        else:
            return 0

    def get_negamax_scores(self, terminal):
        """Same as get_scores for Negamax."""
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
