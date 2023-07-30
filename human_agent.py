from agent_base import Agent_Base
from game import Game

class Human_Agent(Agent_Base):
    def __init__(self, game=Game(), verbose=True):
        super().__init__(game)

        self.verbose = verbose

    def next_move(self):
        # prompt human player to enter next move
        while True:
            try:
                print("What's your next move? Enter in format row,col")
                move = input(">")
                move = move.split(',')
                move = int(move[0]), int(move[1])
                if not self.game.is_valid(move[0], move[1]):
                    print("Space must be empty.")
                else:
                    self.game.move(move[0], move[1])
                    return (move[0], move[1])
            except ValueError:
                print("Please enter valid move as row,col between 0,0 and 2,2")
