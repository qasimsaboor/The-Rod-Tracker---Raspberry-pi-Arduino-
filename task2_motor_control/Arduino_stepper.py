from pymata_express import pymata_express
import asyncio
import time
import sys


class ArduinoStep(object):
    def __init__(self):
        print('Arduino init')

    async def step_task(self,my_board, steps_per_rev, pins):
        await my_board.set_pin_mode_stepper(steps_per_rev, pins)
        await my_board.stepper_write(21, 50)

    async def stepper(self,my_board, steps_per_rev, pins):
        print('inside Arduino loop')
        task = asyncio.create_task(self.step_task(my_board, steps_per_rev, pins))
        await task
            
  
            
#ArduinoStep().step_execution(512, [8,9,10,11])