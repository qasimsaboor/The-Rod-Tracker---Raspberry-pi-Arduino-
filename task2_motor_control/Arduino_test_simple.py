from pymata4 import pymata4
import time

ST_PIN = 5
DIR_PIN= 3

board = pymata4.Pymata4()

# set the pin mode
board.set_pin_mode_digital_output(ST_PIN)
board.set_pin_mode_digital_output(ST_PIN)
board.digital_write(DIR_PIN, 0)

for n in range(1500):

    print(n)
    board.digital_write(ST_PIN, 1)
    time.sleep(0.000001)
    
    board.digital_write(ST_PIN, 0)
    time.sleep(0.000001)

time.sleep(2)
board.digital_write(DIR_PIN, 1)

for m in range(512):
    
    print(m)
    board.digital_write(ST_PIN, 1)
    time.sleep(0.001)
    
    board.digital_write(ST_PIN, 0)
    time.sleep(0.001)

board.shutdown()

