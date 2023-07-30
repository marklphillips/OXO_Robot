class Game:
    def __init__(self, cross_symbol = "X", nought_symbol = "O", empty_symbol = " "):
        self.CROSS = cross_symbol
        self.NOUGHT = nought_symbol
        self.EMPTY = empty_symbol
        self.DRAW = "Draw!"
        self.GAMEBOARD_SIZE = 3
        self.OPENING_MOVES = [(0, 0), (0, 2), (2, 0), (2, 2)]

        self.initialize_game()

    def initialize_game(self):
        self.current_state = [[self.EMPTY for _ in range(self.GAMEBOARD_SIZE)] for _ in range(self.GAMEBOARD_SIZE)]
        
        # track number of moves in game
        self.move_count = 0

        # Player X always plays first
        self.current_player = self.CROSS
        
        self.flip_player = {self.CROSS: self.NOUGHT, self.NOUGHT: self.CROSS}

    def draw_board(self):
        for i in range(0, 3):
            for j in range(0, 3):
                
                print('{}|'.format(self.current_state[i][j]), end=" ")
            print()
        print()

    # Determines if the made move is a legal move
    def is_valid(self, px, py):
        if px < 0 or px > 2 or py < 0 or py > 2:
            return False
        elif self.current_state[px][py] != self.EMPTY:
            return False
        else:
            return True

    # Checks if the game has ended and returns the winner in each case
    def is_end(self):
        
        for i in range(0, 3):

            # check for a vertical win
            if self.current_state[0][i] == self.current_state[1][i] == self.current_state[2][i] != self.EMPTY:
                return self.current_state[0][i]

            # check for a horizontal win
            if self.current_state[i][0] == self.current_state[i][1] == self.current_state[i][2] != self.EMPTY:
                return self.current_state[i][0]

        # check for a diagonal win
        if (self.current_state[0][0] == self.current_state[1][1] == self.current_state[2][2] != self.EMPTY) or \
            (self.current_state[0][2] == self.current_state[1][1] == self.current_state[2][0] != self.EMPTY):
            return self.current_state[1][1]
        
        for i in range(0, 3):
            for j in range(0, 3):
                # There's an empty field, we continue the game
                if (self.current_state[i][j] == self.EMPTY):
                    return None

        # otherwise, it must be a draw
        return self.DRAW

    def move(self, x, y):
        # play the move on the gameboard
        self.current_state[x][y] = self.current_player
        self.move_count += 1

        # flip to next player, ready for next turn
        self.current_player = self.flip_player[self.current_player]