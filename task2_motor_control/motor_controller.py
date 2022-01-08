#try:
    #from .fake_gpio import GPIO # For running app
#except ImportError:
    #from fake_gpio import GPIO # For running main
#import RPi.GPIO as GPIO # For testing in Raspberry Pi
# import ...
from time import sleep
import random
from task1_opencv_control.opencv_controller import OpenCVController
from pymata4 import pymata4
import asyncio

opencv_controller = OpenCVController()

board = pymata4.Pymata4()

class MotorController(object):

    def __init__(self):
        self.working = False
        self.PIN_STEP = 5 # set for Arduino
        self.PIN_DIR = 3 # set for Arduino
        
        self.strot_90 = 400
        self.strot_270= 1200 #0.225 degree per step     -> 90deg = 400 steps -> 270deg = 1200steps

        self.CW = 1     # Clockwise Rotation
        self.CCW = 0    # Counterclockwise Rotation
        self.SPR = 1600   # Steps per Revolution (360 / 0.225)

        self.delay = 0.0005 #!~ Ansteuerungsfrequenz?

        self.out_message = ''
        


    def stop_motor(self):
        self.working = False
        return 


    def approx_step(self,compare_array):
        #GPIO.setmode(GPIO.BCM)
        #GPIO.setup(self.PIN_DIR, GPIO.OUT)
        #GPIO.setup(self.PIN_STEP, GPIO.OUT)

        board.set_pin_mode_digital_output(self.PIN_DIR)
        board.set_pin_mode_digital_output(self.PIN_STEP)   

        angle =30
        total_steps=1600
        
        counter=0

        check_arr = opencv_controller.get_current_color()

        self.working = True
        self.out_message = 'rotating clockwise to <color> field'
        print('Motor started')

        if compare_array == (1,1,1): #case for 'non'-aiming

            angle_bit = random.getrandbits(1)
            dir_bit = random.getrandbits(1)

            if angle_bit == 1:
                angle_total = self.strot_90
                self.amt= '90'
            else:
                angle_total = self.strot_270
                self.amt= '270'

            if dir_bit == 1:
                dir = self.CW
                self.out_dir= 'clockwise direction'
            else:
                dir = self.CCW
                self.out_dir= 'counter-clockwise direction'

            self.out_message = 'rotating ' + str(self.amt)  + '° in '  + str(self.out_dir)

            max= int(angle_total/angle)
            board.digital_write(self.PIN_DIR, dir)
            #GPIO.output(self.PIN_DIR, dir)
        else:
            max=3000

        #go into execution loop####################################################

        for y in range(max):

            if self.working == False:
                print('out of motor loop')
                break

            opencv_controller.process_frame()
            check_arr = opencv_controller.get_current_color()

            #turn around if border reached
            if check_arr== (1,0,1) and counter > 5:
                print('turned around')
                dir +=1
                dir %=2
                board.digital_write(self.PIN_DIR, dir)
                #GPIO.output(self.PIN_DIR, dir)
                print('turned around')
                sleep(1)
                counter = 0

            if compare_array == (0,1,0) and counter >3:

                dir =1
                print('inside cyan selection')
                print('check_arr: ',check_arr)

                if check_arr[0]==1:
                    dir = self.CW
                    print('set clockwise')

                elif check_arr[2]==1:
                    dir = self.CCW
                    print('set counter-clockwise')
                
                self.out_message = 'rotating until ' + '<color> ' + 'reached'
                max = 3000 #match for Arduino Setup!
                board.digital_write(self.PIN_DIR, dir)
                #GPIO.output(self.PIN_DIR, dir)
                sleep(.5)
                counter = 0
                

            counter +=1
            print(compare_array,'//',check_arr,'//',counter)

            for x in range(angle):
                
                if self.working == True:

                    #GPIO.output(self.PIN_STEP, GPIO.HIGH)
                    board.digital_write(self.PIN_STEP, 1)
                    sleep(self.delay)
                    #GPIO.output(self.PIN_STEP, GPIO.LOW)
                    board.digital_write(self.PIN_STEP, 0)
                    sleep(self.delay)
                else:
                    break

            if self.working == False:
                self.out_message = 'stopped'
                break
            
            if compare_array != (1,1,1) and check_arr == compare_array :
                self.out_message = 'finished'
                print('reached field',check_arr)
                break
            else:
                print('checked!')

            if y == max-1 :
                self.out_message = 'finished'
                print('reached field',check_arr)
                break

            
        self.working = False      

    def is_working(self):
        print(self.out_message)
        return self.out_message   
 
