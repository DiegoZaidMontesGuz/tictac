"""
Tic Tac Toe with Minimax / Negamax AI
CSE 5120 Homework 2 — GUI and AI integration
"""

import pygame
import numpy as np
from GameStatus_5120 import GameStatus
from multiAgents import minimax, negamax
import sys, random

mode = "player_vs_ai"  # default mode for playing the game (player vs AI)


class RandomBoardTicTacToe:
    def __init__(self, size=(600, 800)):

        self.size = self.width, self.height = size
        # Define some colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GREEN = (0, 255, 0)
        self.RED = (255, 0, 0)

        # Grid Size
        self.GRID_SIZE = 5
        self.OFFSET = 5
        self.state = np.zeros((self.GRID_SIZE, self.GRID_SIZE), dtype=int)

        self.CIRCLE_COLOR = (140, 146, 172)
        self.CROSS_COLOR = (140, 146, 172)

        # This sets the WIDTH and HEIGHT of each grid location
        self.WIDTH = self.size[0] / self.GRID_SIZE
        self.HEIGHT = self.size[1] / self.GRID_SIZE

        self.cross_size = (750 - 300) / self.GRID_SIZE / 2.5

        self.O_turn = True  # Player O starts first

        # Initialize pygame
        pygame.init()
        self.font = pygame.font.Font(None, 200)
        self.game_reset()

    # -----------------------------------------------------
    # Drawing and initialization
    # -----------------------------------------------------
    def draw_game(self):
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption("Tic Tac Toe Random Grid")
        self.screen.fill(self.WHITE)

        # Outer borders
        pygame.draw.line(self.screen, self.BLACK, (50, 300), (550, 300), 6)
        pygame.draw.line(self.screen, self.BLACK, (50, 750), (550, 750), 6)
        pygame.draw.line(self.screen, self.BLACK, (50, 300), (50, 750), 6)
        pygame.draw.line(self.screen, self.BLACK, (550, 300), (550, 750), 6)

        # Horizontal grid lines
        h = 300
        while h < 750:
            pygame.draw.line(self.screen, self.BLACK, (50, h), (550, h), 6)
            h += (750 - 300) / self.GRID_SIZE

        # Vertical grid lines
        h = 50
        while h < 550:
            pygame.draw.line(self.screen, self.BLACK, (h, 300), (h, 750), 6)
            h += (550 - 50) / self.GRID_SIZE

    def change_turn(self):
        if self.game_state.turn_O:
            pygame.display.set_caption("Tic Tac Toe - O's turn")
        else:
            pygame.display.set_caption("Tic Tac Toe - X's turn")

    def draw_circle(self, x, y):
        """Draw the circle for the O player"""
        pygame.draw.circle(
            self.screen, self.CIRCLE_COLOR, (x, y),
            (750 - 300) / self.GRID_SIZE / 2.5, 5
        )

    def draw_cross(self, x, y):
        """Draw the cross for the X player"""
        line1_start = (x - self.cross_size // 2, y - self.cross_size // 2)
        line1_end = (x + self.cross_size // 2, y + self.cross_size // 2)
        line2_start = (x + self.cross_size // 2, y - self.cross_size // 2)
        line2_end = (x - self.cross_size // 2, y + self.cross_size // 2)
        pygame.draw.line(self.screen, self.RED, line1_start, line1_end, 5)
        pygame.draw.line(self.screen, self.RED, line2_start, line2_end, 5)

    # -----------------------------------------------------
    # Game logic
    # -----------------------------------------------------
    def is_game_over(self):
        """Checks whether the current game is over."""
        if self.game_state.is_terminal():
            print("Game Over!")
            return True
        return False

    def move(self, move):
        self.game_state = self.game_state.get_new_state(move)

    def play_ai(self):
        """Makes the AI move using Minimax or Negamax."""
        use_negamax = False
        depth = 3

        # Choose and execute the best move
        if use_negamax:
            score, move = negamax(self.game_state, depth)
        else:
            score, move = minimax(self.game_state, depth, maximizingPlayer=False)

        print(f"AI decided move: {move}, Score: {score}")

        if move is not None:
            # Update both AI state and GUI state
            self.game_state = self.game_state.get_new_state(move)
            self.state[move[0]][move[1]] = -1  # AI = X = -1

            # Draw AI move on the board
            px, py = self._state_to_position(move)
            self.draw_cross(px, py)
            pygame.display.update()

        if self.is_game_over():
            print("Final Score:", self.game_state.get_scores(True))

    def game_reset(self):
        """Resets the board and game state."""
        self.draw_game()
        self.state = np.zeros((self.GRID_SIZE, self.GRID_SIZE), dtype=int)
        self.game_state = GameStatus(self.state, turn_O=True)
        pygame.display.update()

    # -----------------------------------------------------
    # Main loop
    # -----------------------------------------------------
    def play_game(self, mode="player_vs_ai"):
        done = False
        clock = pygame.time.Clock()

        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    s = self._position_to_state(mouse_pos)
                    p = self._state_to_position(s)

                    # Player (O) move
                    if self.O_turn and self.state[s[0]][s[1]] == 0:
                        self.state[s[0]][s[1]] = 1  # Player O
                        self.draw_circle(p[0], p[1])
                        self.game_state = self.game_state.get_new_state(s)
                        pygame.display.update()

                        if self.is_game_over():
                            print("Game Over!")
                            done = True
                            break

                        # Let AI play right after player move
                        self.O_turn = False
                        self.play_ai()
                        self.O_turn = True

            pygame.display.update()
            clock.tick(30)

        pygame.quit()

    # -----------------------------------------------------
    # Helper functions
    # -----------------------------------------------------
    def _state_to_position(self, state=[0, 0]):
        x = 50
        y = 300
        x += ((550 - 50) / self.GRID_SIZE) * (state[0] + 1) - (
            (750 - 300) / self.GRID_SIZE / 2
        )
        y += (((750 - 300) / self.GRID_SIZE) * (state[1] + 1)) - (
            (750 - 300) / self.GRID_SIZE / 2
        )
        return [x, y]

    def _position_to_state(self, pos):
        s = [0, 0]
        h = 300
        count = 0
        while h < 750:
            if pos[1] > h and pos[1] < h + (750 - 300) / self.GRID_SIZE:
                s[1] = count
            count += 1
            h += (750 - 300) / self.GRID_SIZE

        h = 50
        count = 0
        while h < 550:
            if pos[0] > h and pos[0] < h + (550 - 50) / self.GRID_SIZE:
                s[0] = count
            h += (550 - 50) / self.GRID_SIZE
            count += 1
        return s


# -----------------------------------------------------
# Run the game
# -----------------------------------------------------
if __name__ == "__main__":
    tictactoegame = RandomBoardTicTacToe()
    tictactoegame.play_game()
