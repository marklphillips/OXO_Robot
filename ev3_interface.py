#!/usr/bin/env python3

from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_D, SpeedPercent
from ev3dev2.button import Button
from ev3dev2.display import Display
from ev3dev2.sensor.lego import ColorSensor
#from ev3dev2.sound import Sound
from textwrap import wrap
from time import sleep

class EV3Interface:
    def __init__(self):
        self.ev3_display = Display()
        self.ev3_buttons = Button()

        self.ev3_buttons.on_enter = self.btn_event_enter
        self.ev3_buttons.on_backspace = self.btn_event_backspace
        self.ev3_buttons.on_left = self.btn_event_left
        self.ev3_buttons.on_right = self.btn_event_right
        self.ev3_buttons.on_up = self.btn_event_up
        self.ev3_buttons.on_down = self.btn_event_down

    def show_text(self, string, font_name='courB24', font_width=15, font_height=24):
        self.ev3_display.clear()
        strings = wrap(string, width=int(180/font_width))
        for i in range(len(strings)):
            x_val = 89-font_width/2*len(strings[i])
            y_val = 63-(font_height+1)*(len(strings)/2-i)
            self.ev3_display.text_pixels(strings[i], False, x_val, y_val, font=font_name)
        self.ev3_display.update()


    def draw_grid(self, state):
        lcd = self.ev3_display
        symbols = {ColorSensor.COLOR_RED: "X", ColorSensor.COLOR_BLUE: "O", ColorSensor.COLOR_NOCOLOR: ""}
        cell = 30
        x0, y0 = 45, 10

        lcd.clear()
        lcd.rectangle(False, x0, y0, x0 + cell * 3, y0 + cell * 3, fill_color='white')
        for i in range(1, 3):
            lcd.line(False, x0, y0 + cell * i, x0 + cell * 3, y0 + cell * i)
            lcd.line(False, x0 + cell * i, y0, x0 + cell * i, y0 + cell * 3)


        for i in range (3):
            for j in range (3):
                x_val = int(cell * i + cell/2 - 15/2 + x0)
                y_val = int(cell * j + cell/2 - 24/2 + y0)
                lcd.text_pixels(symbols[state[j][i]], False, x_val, y_val, font='helvB24')        

    def draw_menu(self, options):
        lcd = self.ev3_display

        menu_height = 20
        screen_width, screen_height = 178, 128
        x0 = 0
        y0 = screen_height - menu_height

        lcd.line(False, x0, y0, x0 + screen_width, y0)
        num_opts = len(options)
        cell = screen_width / num_opts
        y_val = int(menu_height / 2 - 14/2 + y0)

        if num_opts == 1:
            # one centre justified option
            x_val = int(cell / 2 - 9 * len(options[0]) / 2)
            lcd.text_pixels(options[0], False, x_val, y_val, font='helvB14')
        elif num_opts == 2:
            # one left and one right justified option
            x_val = x0
            lcd.text_pixels(options[0], False, x_val, y_val, font='helvB14')
            x_val = screen_width - 9 * len(options[1])
            lcd.text_pixels(options[1], False, x_val, y_val, font='helvB14')

    def lcd_update(self):
        self.ev3_display.update()

    def btn_event_enter(self, state):
        if state:
            #robot.retract()
            #run_game()
            pass
    
    def btn_event_backspace(self, state):
        if state:
            pass
            
    def btn_event_left(self, state):
        if state:
            #mX.on_for_rotations(SpeedPercent(50), -0.1)
            pass

    def btn_event_right(self,state):
        if state:
            #mX.on_for_rotations(SpeedPercent(50), 0.1)
            pass

    def btn_event_up(self, state):
        if state:
            #mY.on_for_rotations(SpeedPercent(50), 0.1)
            pass

    def btn_event_down(self, state):
        if state:
            #mY.on_for_rotations(SpeedPercent(50), -0.1)
            pass


