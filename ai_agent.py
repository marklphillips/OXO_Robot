import math
import random
import time

from agent_base import Agent_Base
from game import Game

class AI_Agent(Agent_Base):
# this is an implementation of the classic Minimax algorithm with alpha-beta pruning
#   
    def __init__(self, game=Game(), max_depth=4):

        super().__init__(game)

        # number of moves to look ahead
        self.max_depth = max_depth

    def alpha_beta(self, maximizing_player=True, depth=0.0, alpha=-math.inf, beta=math.inf):

        result = self.game.is_end()

        if result == self.game.CROSS:
            return (-10 + depth, 0, 0)
        elif result == self.game.NOUGHT:
            return (10 - depth, 0, 0)
        elif (result == self.game.DRAW) or (depth >= self.max_depth):
            return (0, 0, 0)

        if maximizing_player:
            best_value = -math.inf
            current_player = self.game.NOUGHT
        else:
            best_value = math.inf
            current_player = self.game.CROSS

        px = None
        py = None

        for i in range(0, 3):
            for j in range(0, 3):
                if self.game.current_state[i][j] == self.game.EMPTY:
                    self.game.current_state[i][j] = current_player
                    (next_value, _, _) = self.alpha_beta(not maximizing_player, depth+0.5, alpha, beta)
                    self.game.current_state[i][j] = self.game.EMPTY

                    if maximizing_player:
                        if next_value > best_value:
                            best_value = next_value
                            px, py = i, j

                        if best_value >= beta:
                            return (best_value, px, py)

                        alpha = max(alpha, best_value)    

                    else:
                        if next_value < best_value:
                            best_value = next_value
                            px, py = i, j

                        if best_value <= alpha:
                            return (best_value, px, py)                        

                        beta = min(beta, best_value)

        return (best_value, px, py)

    def next_move(self):        
        if self.game.move_count == 0:
            # if board is empty, randomly select opening move from best options
            (px, py) = self.game.OPENING_MOVES[random.randint(0, 3)]
        else:
            # board not empty, run algorithm to find next move
            start_time = time.time()
            (_, px, py) = self.alpha_beta(maximizing_player=True)
            evalulation_time = time.time() - start_time

        # play move
        self.game.move(px, py)

        # return move in case it is required for other useage
        return (px, py)