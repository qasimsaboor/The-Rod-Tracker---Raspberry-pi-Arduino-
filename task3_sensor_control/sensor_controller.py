#try:
    #from .fake_gpio import GPIO # For running app
#except ImportError:
    #from fake_gpio import GPIO # For running main
# import RPi.GPIO as GPIO # For testing in Raspberry Pi
import time
import numpy as np
import copy
#from pymata4 import pymata4
#import task2_motor_control.motor_controller as task2

#motor_controller= task2.MotorController()

class SensorController:

  def __init__(self):
    self.PIN_TRIGGER = 8 
    self.PIN_ECHO = 10 
    self.distance = None
    self.color_from_distance = [False, False, False]
    self.pos_diff=0
    self.cal_status = 'std_values'
    self.cm_per_step = 1/400
    self.col_low = 0
    self.col_up = 0
    self.lower= 93
    self.upper = 130
    self.buff_arr_low =np.array([])
    self.buff_arr_up =np.array([])
    self.color_distance =(False,False,False)
    self.cm_val = 0

    print('Sensor controller initiated')

  def cal_val(self,board,border):
    if border== 0:
      if len(self.buff_arr_low)>4:
        self.buff_arr_low = np.append(np.array([]),self.track_rod(board,0,False)[1])
      else:
        self.buff_arr_low = np.append(self.buff_arr_low,self.track_rod(board,0,False)[1])    
      av_low =np.average(self.buff_arr_low)
      std_dev=np.std(self.buff_arr_low)
      norm_arr_low=[n for n in self.buff_arr_low if n<av_low+std_dev and n>av_low-std_dev]
      self.lower =np.average(norm_arr_low)
      self.lower =np.average(self.buff_arr_low)
      print(self.buff_arr_low)
      print('lower limit average',self.lower) 

    else:
      print('defining upper')
      if len(self.buff_arr_up)>4:
        self.buff_arr_up = np.append(np.array([]),self.track_rod(board,0,False)[1])
      else:
        self.buff_arr_up = np.append(self.buff_arr_up,self.track_rod(board,0,False)[1])

      av_up =np.average(self.buff_arr_up)
      std_dev_up=np.std(self.buff_arr_up)
      norm_arr_up=[n for n in self.buff_arr_up if n<av_up+std_dev_up]
      self.upper =np.average(norm_arr_up)
      print(self.buff_arr_up)
      print('upper limit average',self.upper) 


  def track_rod(self,board,set_count,pred_enable):
    rep_count =set_count
    res_val=self.control_sensor(board,5)
    cm_val_buff= self.get_distance(res_val)

    if rep_count != 0 and pred_enable == True:
      if cm_val_buff < self.col_low or cm_val_buff > self.col_up :
        rep_count -=1
        print('rep count',rep_count,'  ',cm_val_buff,'cm')
        comp = abs(cm_val_buff-self.col_low) + abs(cm_val_buff-self.col_up) 
        if comp< abs(self.cm_val-self.col_low) + abs(self.cm_val-self.col_up):
          self.cm_val=cm_val_buff
          return rep_count,res_val,self.cm_val
        else:
          #return rep_count+1,res_val,self.cm_val
          return rep_count,res_val,self.cm_val
      else:
        self.cm_val=cm_val_buff
        return 0,res_val,self.cm_val
    else:
      self.cm_val=cm_val_buff
      return 0,res_val,self.cm_val

  def status_meas(self):
        
        return
        
  def control_sensor(self,board,rep):
    val_arr=np.zeros(rep)
    for k in range(rep):
      board.digital_write(8, 0)
      for i in range(20):
          board.digital_write(11, 1)
          time.sleep(0.001)
          board.digital_write(11, 0)
          time.sleep(0.001)
      value, time_stamp = board.analog_read(0)
      board.digital_write(8, 1)
      val_arr[k]= value

    av =np.average(val_arr)
    std_dev=np.std(val_arr)
    norm_arr=[n for n in val_arr if n<av+std_dev and n>av-std_dev]

    res_val=np.average(norm_arr)     
    return res_val

  def predict_pos(self,check_arr):
    if check_arr== (1,0,0):
          self.col_low= 0
          self.col_up= 1.2
    elif check_arr== (1,1,0):
          self.col_low= 1.2 
          self.col_up= 2.5
    elif check_arr== (0,1,0):
          self.col_low= 2.5
          self.col_up= 4.1
    elif check_arr== (0,1,1):
          self.col_low= 4.1
          self.col_up= 5.2
    elif check_arr== (0,0,1):
          self.col_low= 5.2
          self.col_up= 7.5

  def get_distance(self,res_val):
    self.cm_val=round((res_val-self.lower)*2.7/(self.upper-self.lower),1)    
    return self.cm_val      
    
  def get_color_from_distance(self):
    if self.cm_val < 1.2:
      self.color_from_distance = (1,0,0)
    elif self.cm_val >= 1.2 and self.cm_val  <2.5 :
      self.color_from_distance= (1,1,0)
    elif self.cm_val >= 2.5 and self.cm_val  <4.1 :
      self.color_from_distance = (0,1,0)
    elif self.cm_val >= 4.1 and self.cm_val  <5.2 :
      self.color_from_distance = (0,1,1)
    elif self.cm_val >= 5.2 and self.cm_val  <7.5 :
      self.color_from_distance = (0,0,1)
    return self.color_from_distance
