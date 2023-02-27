import time
from ev3dev2.motor import LargeMotor, MediumMotor, SpeedPercent, OUTPUT_A, OUTPUT_B, OUTPUT_D
from ev3dev2.sensor.lego import ColorSensor, TouchSensor
from game import Game

GAME_BOARD_SIZE = 3                     # the size of the game board - e.g. 3 x 3
GAME_CELL_STUD_PITCH = 3                # the pitch between cells measured in lego studs
BALL_DISP_STUD_OFFSET = (4.5, 1.5)      # the offset of the ball dispenser w.r.t. colour sensor
RETRACTED_POS_STUD_OFFSET = (-2, -2)    # the offset of the retracted position w.r.t. cell (0, 0)
REVS_PER_STUD = 0.3125                  # motor revolutions to move 1 stud
REVS_PER_BALL_DISP = 0.3333             # motor revolutions to release 1 ball
START_CELL = (0, 0)                     # the default cell (0, 0) (top left)
MOTOR_SPEED_GAME_PLAY = 100
CELL_SCAN_ORDER = [(0, 0), (0, 1), (0, 2), (1, 2), (1, 1), (1, 0), (2, 0), (2, 1), (2, 2)]

class Robot():
    def __init__(self, game=Game(), verbose=False):
        self.verbose = verbose
        self.game = game
        self.motor_y = LargeMotor(OUTPUT_A)
        self.motor_y.polarity = LargeMotor.ENCODER_POLARITY_INVERSED
        self.motor_x = LargeMotor(OUTPUT_D)
        self.motor_x.polarity = LargeMotor.ENCODER_POLARITY_INVERSED
        self.motor_ball_disp = MediumMotor(OUTPUT_B)
        self.motor_ball_disp.polarity = MediumMotor.ENCODER_POLARITY_INVERSED
        self.colour_sensor = ColorSensor()
        self.colour_sensor.mode = ColorSensor.MODE_COL_COLOR
        self.touch_sensor = TouchSensor()

        self.motor_speed_game_play = MOTOR_SPEED_GAME_PLAY
        self.cell_stud_pitch = GAME_CELL_STUD_PITCH
        self.ball_disp_stud_offset = BALL_DISP_STUD_OFFSET
        self.retracted_pos_stud_offset = RETRACTED_POS_STUD_OFFSET
        self.revs_per_stud = REVS_PER_STUD
        self.revs_per_ball_disp = REVS_PER_BALL_DISP
        self.revs_per_cell = self.cell_stud_pitch * self.revs_per_stud
        self.x_pos = 0
        self.y_pos = 0

        self.calibrate()
        self.reset()
    
    def calibrate(self):

        motors = [self.motor_x, self.motor_y]
        speeds = [-50, -50]

        print("Calibrating X-Y grid position...")
        for motor, speed in zip(motors, speeds):
            motor.run_forever(speed_sp=speed)
            while not motor.is_stalled and not motor.is_overloaded:
                time.sleep(0.02)
                #print(motor, "running")
        
            motor.stop()
        
        print("Calibration complete, moving to cell 1,1")
        self.move_motor_xy(2, 3)

    def reset(self):
        self.board = [[ColorSensor.COLOR_NOCOLOR for _ in range(GAME_BOARD_SIZE)] \
                        for _ in range(GAME_BOARD_SIZE)]

        self.x_pos = 0      # x position measured in studs
        self.y_pos = 0      # y position measured in studs

        if self.verbose:
            print("Machine Agent reset. Board = ", self.board)

    def move_motor_xy(self, studs_dx, studs_dy):

        if self.verbose: print("Existing x-y position (%s, %s)" % (self.x_pos, self.y_pos))

        # update the x, y tracking
        self.x_pos += studs_dx
        self.y_pos += studs_dy

        # run motors
        self.motor_x.on_for_rotations(SpeedPercent(self.motor_speed_game_play), self.revs_per_stud * studs_dx, block = False)
        self.motor_y.on_for_rotations(SpeedPercent(self.motor_speed_game_play), self.revs_per_stud * studs_dy, block = False)
        
        # wait for motors to stop moving
        while self.motor_x.is_running or self.motor_y.is_running:
            time.sleep(0.05)

        if self.verbose: print("Moved x-y (%s, %s) studs. New x-y position (%s, %s)" % (studs_dx, studs_dy, self.x_pos, self.y_pos))

    def move_to_cell(self, cell, dispense_ball=False):
        if self.verbose: print("Moving to cell", cell)

        studs_dx = 0
        studs_dy = 0

        if dispense_ball:
            studs_dx += self.ball_disp_stud_offset[0]
            studs_dy += self.ball_disp_stud_offset[1]
        
        cell_dx = (studs_dx + (cell[1] * self.cell_stud_pitch)) - self.x_pos
        cell_dy = (studs_dy + (cell[0] * self.cell_stud_pitch)) - self.y_pos
        self.move_motor_xy(cell_dx, cell_dy)

    def retract(self):
        studs_dx = self.retracted_pos_stud_offset[0] - self.x_pos
        studs_dy = self.retracted_pos_stud_offset[1] - self.y_pos

        if self.verbose: print ("Retracting by moving x-y (%s, %s)" % (studs_dx, studs_dy))

        self.move_motor_xy(studs_dx, studs_dy)

    def scan_gameboard(self):

        for cell in CELL_SCAN_ORDER:
            (x, y) = cell
            #if self.board[x][y] == ColorSensor.COLOR_NOCOLOR:
            if self.game.current_state[x][y] == self.game.EMPTY:
                self.move_to_cell(cell)

                if self.colour_sensor.color == ColorSensor.COLOR_RED:
                    #self.game.current_state[x][y] = ColorSensor.COLOR_RED
                    print("Found red ball at ", (x, y))
                    return (x, y)
        return None

    def place_ball(self, cell):

        self.move_to_cell(cell, dispense_ball=True)
        self.motor_ball_disp.on_for_rotations(SpeedPercent(20), self.revs_per_ball_disp)      
        time.sleep(0.5)

    def next_move(self):

        move = None
        print("Your turn human player...")
        while True:

            if self.touch_sensor.is_pressed:
                self.touch_sensor.wait_for_released()

                # scan gameboard up to three times if necessary - occasionally the sensor does not 'see' the ball
                for i in range(3):
                    move = self.scan_gameboard()

                    if move is not None:
                        self.game.move(move[0], move[1])
                        break
                
                if move is None:
                    self.game.current_player = self.game.flip_player[self.game.current_player]

                return move
            time.sleep(0.1)

