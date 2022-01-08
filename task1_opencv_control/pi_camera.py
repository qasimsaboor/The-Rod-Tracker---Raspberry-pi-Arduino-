#import picamera
import cv2

class Camera(object):
    def __init__(self):

        self.cap = cv2.VideoCapture(1)
        print("Starting pi camera")

    def get_frame(self):

        #self.cap = cv2.VideoCapture(0)
        ret, frame=self.cap.read()   

        #if ret >0 :
            #print("Capturing frame from pi camera")

        #self.cap.release()

        return frame,ret


