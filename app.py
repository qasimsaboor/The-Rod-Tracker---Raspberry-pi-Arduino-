from flask import Flask, render_template, Response, request, jsonify
#from turbo_flask import Turbo #for auto update (without button)

from task1_opencv_control.opencv_controller import OpenCVController
from task2_motor_control.motor_controller import MotorController 
from task3_sensor_control.sensor_controller import SensorController

app = Flask(__name__)
#turbo = Turbo(app)

motor_controller = MotorController()
opencv_controller = OpenCVController()
sensor_controller = SensorController()





# Server view to access the app and display the index template
@app.route('/')
def index():
    return render_template('index.html')   

# Server view to stream the video captured by the available camera
@app.route('/record_frame',methods = ['GET', 'POST'])
def frame_opencv():
    opencv_controller.process_frame()
    return { 'success': True }

@app.route('/set_cyan' ,methods = ['POST'])
def step_approx():
    motor_controller.approx_step((0,1,0))
    return { 'success': True }

@app.route('/set_random' ,methods = ['POST'])
def step_random():
    motor_controller.approx_step((1,1,1))
    return { 'success': True }

# Server view to determine the current color zone using the opencv_controller
@app.route('/get_color_from_opencv', methods = ['GET', 'POST'])
def get_color_from_opencv():
    return jsonify(opencv_controller.get_current_color())

# Server view to start the motor
@app.route('/start_motor', methods = ['POST'])
def start_motor():
    motor_controller.start_motor()  #what else?  
    return { 'success': True }

# Server view to stop the motor
@app.route('/stop_motor', methods = ['POST'])
def stop_motor():
    motor_controller.stop_motor()  #what else?  
    return { 'success': True }

# Server view to get status of the motor (working or not working)
@app.route('/get_motor_status')
def motor_status():
    return jsonify(motor_controller.is_working())

# Server view to calculate the current distance using the sensor_controller


@app.route('/get_distance')
def get_distance():
    # ...
    return { 'success': True }

# Server view to determine the current color zone using the sensor_controller
@app.route('/get_color_from_distance')
def get_color_from_distance():
    # ...
    return { 'success': True }


if __name__ == '__main__':
    app.run(host='0.0.0.0' , debug=True, threaded=True,use_reloader=False) #threaded required for RaspPi? Port required?
