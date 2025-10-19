# -*- coding: utf-8 -*-
"""
multiAgents.py
Implements the Minimax and Negamax algorithms (with alpha–beta pruning)
for the Tic-Tac-Toe project.
"""

import numpy as np
from GameStatus_5120 import GameStatus


# ----------------------------------------------------------------------
# Minimax with alpha–beta pruning
# ----------------------------------------------------------------------
def minimax(game_state, depth, maximizingPlayer, alpha=float("-inf"), beta=float("inf")):
    """
    Standard Minimax search.
    Returns (score, move) where move is (row, col)
    """
    terminal = game_state.is_terminal()

    # Base case: terminal state or depth limit
    if depth == 0 or terminal:
        score = game_state.get_scores(terminal)
        return score, None

    best_move = None

    if maximizingPlayer:
        maxEval = float("-inf")
        for move in game_state.get_moves():
            next_state = game_state.get_new_state(move)
            eval_score, _ = minimax(next_state, depth - 1, False, alpha, beta)
            if eval_score > maxEval:
                maxEval = eval_score
                best_move = move
            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break  # beta cut-off
        return maxEval, best_move

    else:
        minEval = float("inf")
        for move in game_state.get_moves():
            next_state = game_state.get_new_state(move)
            eval_score, _ = minimax(next_state, depth - 1, True, alpha, beta)
            if eval_score < minEval:
                minEval = eval_score
                best_move = move
            beta = min(beta, eval_score)
            if beta <= alpha:
                break  # alpha cut-off
        return minEval, best_move


# ----------------------------------------------------------------------
# Negamax version (simpler, symmetric version of Minimax)
# ----------------------------------------------------------------------
def negamax(game_state, depth, alpha=float("-inf"), beta=float("inf"), color=1):
    """
    Negamax with alpha–beta pruning.
    Returns (score, move)
    """
    terminal = game_state.is_terminal()

    # Base case
    if depth == 0 or terminal:
        score = color * game_state.get_negamax_scores(terminal)
        return score, None

    best_move = None
    best_val = float("-inf")

    for move in game_state.get_moves():
        next_state = game_state.get_new_state(move)
        val, _ = negamax(next_state, depth - 1, -beta, -alpha, -color)
        val = -val
        if val > best_val:
            best_val = val
            best_move = move
        alpha = max(alpha, val)
        if alpha >= beta:
            break  # prune

    return best_val, best_move


# ----------------------------------------------------------------------
# Simple helper to select which algorithm to run
# ----------------------------------------------------------------------
def choose_move(game_state, method="minimax", depth=3):
    """
    Wrapper for selecting between minimax or negamax
    """
    if method.lower() == "minimax":
        score, move = minimax(game_state, depth, maximizingPlayer=False)
    else:
        score, move = negamax(game_state, depth)
    return score, move
