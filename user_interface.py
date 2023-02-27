#!/usr/bin/env python3
import time
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_D, SpeedPercent
from ev3dev2.button import Button
#from ev3dev2.sound import Sound

from game import Game
from robot import Robot
from ai_agent import AI_Agent
#from random_agent import Random_Agent
#from human_agent import Human_Agent
from hmi import HMI, GameState
from ev3_interface import EV3Interface

def run_game():
    ev3.show_text("Please make your move and then press the red button.")
    hmi.play(GameState.FIRST_MOVE)

    # The main game loop   
    while True:

        # draw game board on console output and on EV3 screen
        game.draw_board()
        ev3.draw_grid(game.current_state)

        # get the game status - can be None (game not over), CROSS (wins), NOUGHT (wins), or DRAW
        result = game.is_end()

        if result != None:
            if result == game.CROSS:
                print('The winner is X!')
                ev3.show_text("YOU WIN!")

            elif result == game.NOUGHT:
                print('The winner is O!')
                ev3.show_text("I WIN! AGAIN!")
                time.sleep(0.1)
                hmi.play(GameState.WIN)

            elif result == game.DRAW:
                print("It's a tie!")
                ev3.show_text("IT'S A DRAW!")
                time.sleep(0.1)
                hmi.play(GameState.DRAW)

            # retract the robot arm to allow the human player to make their turn
            robot.retract()
            game.initialize_game()
            print("Clear the game board!")
            ev3.show_text("Please clear the game board.")
            time.sleep(0.1)
            hmi.play(GameState.RESET)
            ev3.show_text("Please make your move and then press the red button.")
            time.sleep(0.1)
            hmi.play(GameState.FIRST_MOVE)

        if game.current_player == game.CROSS:
            #ev3.show_text("Your turn")
            ev3.draw_menu(["Your turn"])
            ev3.lcd_update()
            time.sleep(0.1)
            hmi.play(GameState.HUMAN_TURN)
            move = robot.next_move()

        else:
            #ev3.show_text("My turn, please wait")
            ev3.draw_menu(["My turn, please wait"])
            ev3.lcd_update()
            time.sleep(0.1)
            hmi.play(GameState.ROBOT_TURN)
            move = ai_agent.next_move()
            #move = random_agent.next_move()
            robot.place_ball(move)
            robot.retract()

# Program entry point - instantiate objects:
# EV3Interface() is used to interact with buttons and screen on EV3 brick
# Game() is used to manage the game state, including testing for a win/draw
# HMI() is used to interface with external bluetooth speakers
# AI_Agent() is AI player
# Robot() is used to interface with the motors and manage the physical positioning
ev3 = EV3Interface()
ev3.show_text("Tic Tac Toe / OXO Robot")

game = Game()
hmi = HMI(speech_enable = False, volume=75)
ai_agent = AI_Agent(game, 4)
#random_agent = Random_Agent(game)
#human_agent = Human_Agent(game)

ev3.show_text("Calibrating please wait")
robot = Robot(game)

ev3.show_text("Retracting..")
robot.retract()
run_game()

"""
mX = LargeMotor(OUTPUT_D)
mY = LargeMotor(OUTPUT_A)

def btn_event_enter(state):
    if state:
        robot.retract()
        run_game()
      
def btn_event_left(state):
    if state:
        mX.on_for_rotations(SpeedPercent(50), -0.1)

def btn_event_right(state):
    if state:
        mX.on_for_rotations(SpeedPercent(50), 0.1)

def btn_event_up(state):
    if state:
        mY.on_for_rotations(SpeedPercent(50), 0.1)

def btn_event_down(state):
    if state:
        mY.on_for_rotations(SpeedPercent(50), -0.1)

btn = Button()
btn.on_enter = btn_event_enter
btn.on_left = btn_event_left
btn.on_right = btn_event_right
btn.on_up = btn_event_up
btn.on_down = btn_event_down

#ev3sp = Sound()
#ev3sp.speak("Please calibrate the sensor position, then press enter")

while True:
    btn.process()
    time.sleep(0.1)
"""