import numpy as np
import math


def minimax(game_state, depth, maximizingPlayer=True):
    """
    Simple Minimax algorithm for Tic Tac Toe.
    Returns (score, move)
    """
    # Base case — stop if max depth reached or game is over
    if depth == 0 or game_state.is_terminal():
        score = game_state.get_scores(terminal=True)
        return score, None

    best_move = None

    # Maximizing player (human, O)
    if maximizingPlayer:
        max_eval = -math.inf
        for move in get_available_moves(game_state.board_state):
            child = game_state.get_new_state(move)
            eval, _ = minimax(child, depth - 1, False)
            if eval > max_eval:
                max_eval = eval
                best_move = move
        return max_eval, best_move

    # Minimizing player (AI, X)
    else:
        min_eval = math.inf
        for move in get_available_moves(game_state.board_state):
            child = game_state.get_new_state(move)
            eval, _ = minimax(child, depth - 1, True)
            if eval < min_eval:
                min_eval = eval
                best_move = move
        return min_eval, best_move


def negamax(game_state, depth, color=1):
    """
    Negamax version of Minimax (optional alternative).
    Uses a single perspective with sign flipping.
    """
    if depth == 0 or game_state.is_terminal():
        return color * game_state.get_negamax_scores(terminal=True), None

    best_score = -math.inf
    best_move = None

    for move in get_available_moves(game_state.board_state):
        child = game_state.get_new_state(move)
        score, _ = negamax(child, depth - 1, -color)
        score = -score
        if score > best_score:
            best_score = score
            best_move = move

    return best_score, best_move


def get_available_moves(board_state):
    """
    Return a list of all empty cells on the board [(i, j), ...]
    """
    moves = []
    for i in range(len(board_state)):
        for j in range(len(board_state[i])):
            if board_state[i][j] == 0:
                moves.append((i, j))
    return moves
