from game import Game
from ai_agent import AI_Agent
from human_agent import Human_Agent

def run_game(game, player_X, player_O):
    
    # Player_X is human; Player_O is AI/Robot
    # ROBOT: carry out any initialisation tasks required prior to game commencing
    #
    #

    # The main game loop   
    while True:

        # draw game board on console output
        game.draw_board()

        # get the game status - can be None (game not over), CROSS (wins), NOUGHT (wins), or DRAW
        result = game.is_end()
        if result != None:
            if result == game.CROSS:
                print('The winner is X!')
            elif result == game.NOUGHT:
                print('The winner is O!')
            elif result == game.DRAW:
                print("It's a tie!")

            # reset the game
            game.initialize_game()

            # ROBOT: carry out any reset actions necessary at end of game
            #
            #

        if game.current_player == game.CROSS:
            # Human player
            # The below method call prompts the human to enter a board position for their next move
            # ROBOT: if the robot is instead going to scan the gameboard to work out where the human has played,
            #        then replace this with specific robot code
            #
            player_X.next_move()

        else:
            # AI player
            # get next move from AI agent
            move = player_O.next_move()
            print('AI agent selected row {}, col {}'.format(move[0], move[1]))        

            # ROBOT: insert code here to play the next move on the gameboard
            #
            # ROBOT: carry out any tasks required to allow human to play next move- e.g. retract position
            #

if __name__ == "__main__":

    # Program entry point - instantiate objects:
    # Game() is used to manage the game state, including testing for a win/draw
    # Human_Agent() represents a human player and prompts for input from the console
    # AI_Agent() is the AI player
    game = Game()
    player_X = Human_Agent(game)
    player_O = AI_Agent(game, 4)
    run_game(game, player_X, player_O)