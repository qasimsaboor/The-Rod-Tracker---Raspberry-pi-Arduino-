import asyncio
import sys
from pymata_express import pymata_express
"""
This example demonstrates running a stepper motor
"""
NUM_STEPS = 512
ARDUINO_PINS = [8, 9, 10, 11]


async def stepper(my_board, steps_per_rev, pins):
    """
    Set the motor control control pins to stepper mode.
    Rotate the motor.
    :param my_board: pymata_express instance
    :param steps_per_rev: Number of steps per motor revolution
    :param pins: A list of the motor control pins
    """

    await my_board.set_pin_mode_stepper(steps_per_rev, pins)
    await asyncio.sleep(.25)
    await my_board.stepper_write(40, 3000)

   
board = pymata_express.PymataExpress()

for i in range(5):
    loop = asyncio.run() 
 
    print(i)

    try:
        loop.run_until_complete(stepper(board, NUM_STEPS, ARDUINO_PINS))
        
        

    except KeyboardInterrupt:
        loop.run_until_complete(board.shutdown())
        sys.exit(0)
        
loop.run_until_complete(board.shutdown())