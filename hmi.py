from enum import Enum
from ev3dev2.sound import Sound

class GameState(Enum):
    RESET = 0
    FIRST_MOVE = 1
    HUMAN_TURN = 2
    ROBOT_TURN = 3
    WIN = 4
    DRAW = 5

class HMI:
    def __init__(self, speech_enable=False, volume=50):
        self.SFX = {GameState.RESET:        "./sounds/clear_game_board.wav", \
                    GameState.FIRST_MOVE:   "./sounds/press_red_button.wav", \
                    GameState.HUMAN_TURN:   "./sounds/your_turn.wav", \
                    GameState.ROBOT_TURN:   "./sounds/please_wait.wav", \
                    GameState.WIN:          "./sounds/i_win_again.wav", \
                    GameState.DRAW:         "./sounds/its_a_draw.wav"}

        self.speech_enable = speech_enable
        self.volume = volume        
        self.ev3sound = Sound()

    def play(self, state):
        if self.speech_enable:
            #try:
            self.ev3sound.play_file(self.SFX[state], self.volume, Sound.PLAY_WAIT_FOR_COMPLETE)
            #except FileNotFoundError:
            print("Playing file:", self.SFX[state])
