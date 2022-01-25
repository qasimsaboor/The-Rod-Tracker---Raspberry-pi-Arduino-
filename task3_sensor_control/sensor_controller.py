try:
    from .fake_gpio import GPIO # For running app
except ImportError:
    from fake_gpio import GPIO # For running main

import time     
# import RPi.GPIO as GPIO # For testing in Raspberry Pi
# import ...

class SensorController:

  def __init__(self):
    self.PIN_TRIGGER = 18 # do not change
    self.PIN_ECHO = 24 # do not change
    self.distance = None
    self.color_from_distance = [False, False, False]
    print('Sensor controller initiated')

  def track_rod(self):
    # ...
    print('Monitoring')

  def get_distance(self):

    GPIO.setup(self.PIN_TRIGGER, GPIO.OUT)
    GPIO.setup(self.PIN_ECHO, GPIO.IN)

    GPIO.output(self.PIN_TRIGGER, GPIO.LOW)

    print ('Waiting for sensor to settle')

    time.sleep(2)

    print ('Calculating distance')

    GPIO.output(self.PIN_TRIGGER, GPIO.HIGH)

    time.sleep(0.00001)

    GPIO.output(self.PIN_TRIGGER, GPIO.LOW)

    while GPIO.input(self.PIN_ECHO)==0:
       pulse_start_time = time.time()
    while GPIO.input(self.PIN_ECHO)==1:
       pulse_end_time = time.time()

    pulse_duration = pulse_end_time - pulse_start_time
    distance = round(pulse_duration * 17150, 2)
    print ('Distance:'),distance,'cm'

 
    GPIO.cleanup()

    return self.distance

  def get_color_from_distance(self):
    return self.color_from_distance
