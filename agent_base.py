from game import Game

class Agent_Base():
    def __init__(self, game=Game()):
        self.game = game

    def next_move(self):
        pass
