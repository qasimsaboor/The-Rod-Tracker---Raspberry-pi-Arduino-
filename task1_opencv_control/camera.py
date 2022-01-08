# Please note that this is a fake camera, it will just 
# yield the images 1.jpg, 2.jpg, 3.jg and 4.jpg. It is
# just for testing purposes. You should actually use the
# picamera module and implement the get_frame properly  

from time import time
from time import sleep
import os, sys
import cv2 #extra

class Camera(object):
    def __init__(self):
        self.directory = os.path.join(os.path.dirname(__file__), 'test_frames')
        #print(self.directory)
        self.test_frames_name = ['1.jpg', '2.jpg', '3.jpg', '4.jpg']
        self.frames = [open(os.path.join(self.directory, f), 'rb').read() for f in self.test_frames_name]
        self.current_frame = int(time()) % 4
        self.count = 0

    def get_frame(self):
        if (self.count > 2000):
            self.current_frame = int(time()) % 4
            self.count = 0
        index = int(time()) % 4
        print('Frame', self.test_frames_name[self.current_frame])
        self.count =  self.count + 1
        self.count %=4
        #return self.frames[self.current_frame]
        image=cv2.imread(os.path.join(self.directory,self.test_frames_name[self.count]))
        sleep(10)
        return image