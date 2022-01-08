#try:
    #from .camera import Camera # For running app
#except ImportError:#
    #from camera import Camera # For running main
#from .camera import Camera # For running app
from .pi_camera import Camera # For Raspberry Pi
import numpy as np
import cv2
from numpy.core.numeric import empty_like
import os, sys



class OpenCVController(object):

    def __init__(self):

        self.current_color = (0,0,0)

        #source for color table and value assignments: https://cvexplained.wordpress.com/2020/04/28/color-detection-hsv/
        
        self.red_l1 = np.array([0, 0, 50]) #red-range 0-10 
        self.red_h1 = np.array([10, 255, 255])
        self.red_l2 = np.array([170, 0, 50]) #red-range 170-180 
        self.red_h2 = np.array([180, 255, 255])
        #
        self.green_l = np.array([40, 100, 100])
        self.green_h = np.array([70, 255, 255])

        #
        self.yellow_l = np.array([30, 0, 0])
        self.yellow_h = np.array([40, 255, 255])
        #
        self.cyan_l = np.array([95, 150, 50])
        self.cyan_h = np.array([105, 255, 255]) 

        
        self.end_y=0
        self.limit_g=0
        self.limit_gc=0
        self.limit_c=0
        self.limit_cy=0
        self.limit_y=0
        self.marker=0

        self.turn_limit_green=0
        self.turn_limit_yellow=0
   
        self.camera = Camera()

        print('OpenCV controller initiated')

        self.directory = os.path.join(os.path.dirname(__file__), 'test_frames')
        

    def process_frame(self):

        #detect marker position##########################################
        frame_nat,ret = self.camera.get_frame()
        frame= cv2.GaussianBlur(frame_nat,(5,5),0)

        
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV )

        #label position works as sample of the region where the HSV color
        #detect marker - red is situated at the beginning and the end of the H-range -> 2 color masks
        mask_red1 = cv2.inRange (hsv, self.red_l1, self.red_h1)
        mask_red2 = cv2.inRange (hsv, self.red_l2, self.red_h2)

        mask_red_res=mask_red1+mask_red2
        mask_red_res=cv2.medianBlur(mask_red_res,15)

        xy,yy,wy,hy = 0,0,0,0
        xc,yc,wc,hc = 0,0,0,0
        xg,yg,wg,hg = 0,0,0,0
        xr,yr,wr,hr = 0,0,0,0

        marker_detected_red = cv2.findContours(mask_red_res.copy(),
                              cv2.RETR_EXTERNAL,
                              cv2.CHAIN_APPROX_SIMPLE)[-2]

        if len(marker_detected_red)>0:
            marker_area_red = max(marker_detected_red, key=cv2.contourArea)
            (xr,yr,wr,hr) = cv2.boundingRect(marker_area_red)

            cv2.rectangle(frame,(xr,yr),(xr+wr, yr+hr),(125,255,0),2)

        #detect green space###############################################
        mask_green = cv2.inRange (hsv, self.green_l, self.green_h)


        marker_detected_green = cv2.findContours(mask_green.copy(),
                              cv2.RETR_EXTERNAL,
                              cv2.CHAIN_APPROX_SIMPLE)[-2]
        

        if len(marker_detected_green)>0:
            marker_area_green = max(marker_detected_green, key=cv2.contourArea)
            (xg,yg,wg,hg) = cv2.boundingRect(marker_area_green)
            #cv2.rectangle(frame,(xg,yg),(xg+wg, yg+hg),(255,255,0),2)

        #detect cyan space###############################################
        mask_cyan = cv2.inRange (hsv, self.cyan_l, self.cyan_h)

        marker_detected_cyan = cv2.findContours(mask_cyan.copy(),
                              cv2.RETR_EXTERNAL,
                              cv2.CHAIN_APPROX_SIMPLE)[-2]
        if len(marker_detected_cyan)>0:
            marker_area_cyan = max(marker_detected_cyan, key=cv2.contourArea)
            (xc,yc,wc,hc) = cv2.boundingRect(marker_area_cyan)
            #cv2.rectangle(frame,(xc,yc),(xc+wc, yc+hc),(255,255,0),2)

        #detect yellow space###############################################
        mask_yellow = cv2.inRange (hsv, self.yellow_l, self.yellow_h)

        marker_detected_yellow = cv2.findContours(mask_yellow.copy(),
                              cv2.RETR_EXTERNAL,
                              cv2.CHAIN_APPROX_SIMPLE)[-2]

        if len(marker_detected_yellow)>0:
            marker_area_yellow = max(marker_detected_yellow, key=cv2.contourArea)
            (xy,yy,wy,hy) = cv2.boundingRect(marker_area_yellow)
            
            #corrected rectangles
            cv2.rectangle(frame,(xg,yg),(xg+wg, yg+hg),(255,255,0),2)
            cv2.rectangle(frame,(xg+wg,yg),(xy, yg+hg),(255,255,0),2)
            cv2.rectangle(frame,(xy,yy),(xy+wy, yg+hg),(255,255,0),2)

        #insert labels beneath rectangles################################################################
        height=int(yy+hy)+15
        width_green=int(xg+(xc-xg)*0.2)
        width_cyan=int(xc+(xy-xc)*0.2)
        width_yellow=int(xy+(xy-xc)*0.2)

        height_marker= yr+hr + 15

        pos_green =(width_green,height) # no np.array conversion for hardware debug!
        pos_cyan =(width_cyan,height)
        pos_yellow =(width_yellow,height) 
        pos_marker =(int(xr),height_marker) 

        cv2.putText(frame, "Green",pos_green, cv2.FONT_HERSHEY_SIMPLEX, .75, (209, 80, 0, 255),  2) 
        cv2.putText(frame, "Cyan",pos_cyan, cv2.FONT_HERSHEY_SIMPLEX, .75, (209, 80, 0, 255),  2) 
        cv2.putText(frame, "Yellow",pos_yellow, cv2.FONT_HERSHEY_SIMPLEX, .75, (209, 80, 0, 255),  2)
        cv2.putText(frame, "Marker",pos_marker, cv2.FONT_HERSHEY_SIMPLEX, .75, (209, 80, 0, 255),  2)

        #define boundaries related to left edge of marker (wr) 
        
        self.end_y = xy+wy
        self.limit_g=xg-wr
        self.limit_gc=xc-wr
        #self.limit_c=xc #improve!
        self.limit_c=xg+wg
        self.limit_cy=xy-wr
        self.limit_y=xy
        self.marker=xr
        self.turn_limit_green=xg+int(0.1*wg)
        self.turn_limit_yellow=xy+int(0.5*wy)
        
        ###################################################################
        #frame_out=frame.copy()
        #ret, jpeg = cv2.imencode('.jpg', frame_out)

        if ret == True :
        # specify the destination of the captured file
            path = 'static'  + '/buffer' +'.jpg'
            cv2.imwrite(path, frame)

        #return jpeg.tobytes() #frame_out

    def get_current_color(self):

        #cases outside the color-area
        #if self.marker > self.end_y:
            #self.current_color=(0,0,0)
 
        #if self.marker < self.limit_g:
            #self.current_color=(0,0,0)

        #cases inside
        if self.marker > self.limit_g and self.marker < self.limit_gc:
            self.current_color=(1,0,0)

        if self.marker > self.limit_gc and self.marker < self.limit_c :
            self.current_color=(1,1,0)

        if self.marker > self.limit_c and self.marker <self.limit_cy:
            self.current_color=(0,1,0)

        if self.marker > self.limit_cy and self.marker <self.limit_y:
            self.current_color=(0,1,1)

        if self.marker > self.limit_y :
            self.current_color=(0,0,1)

        #border cases - use output (1,0,1) to mark required turn-point
        #replaces 'outside color-area'-cases for Arduino Setup

        if self.marker < self.turn_limit_green:
            print('reached green limit')
            self.current_color=(1,0,1)

        if self.marker > self.turn_limit_yellow:
            print('reached yellow limit')
            self.current_color=(1,0,1)        

        return self.current_color
