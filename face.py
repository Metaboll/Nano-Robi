#! /usr/bin/python
#perl -i -pe's/\r$//;' 

from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import os


import math
import re


from config_servo import ergo_servo_config
#https://github.com/abelectronicsuk/ABElectronics_Python_Libraries/tree/master/ServoPi

from time import sleep
import random
import numpy as np

import os.path
#import subprocess
#import psutil
#from addict import Dict #https://stackoverflow.com/questions/4984647/accessing-dict-keys-like-an-attribute

import time

from threading import Timer




class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer     = None
        self.interval   = interval
        self.function   = function
        self.args       = args
        self.kwargs     = kwargs
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False




            
class vision(object):       
	def __init__(self , my_t0):
		#self.camara_loop = True

		### Setup Brain & comunication #####################################################################
		
		#self.my_mini_brain = mini_brain()
		#self.my_mini_brain.camara_loop = True # to stop or play face tracking and looking for
		#self.my_mini_brain.face_flag = "SERVO " # to note and send face is found
		
		### Setup Camera#####################################################################
		# Center Head coordinates

		self.t0 = time.time()
		self.variable_of_time_change = 3 
		self.cx = 160
		self.cy = 120

		self.t_start = my_t0
		
		self.fps = 0


	def run(self, callback=None ): 
		# Setup the camera
		self.camera = PiCamera()
		self.camera.resolution = ( 320, 240 )
		self.camera.framerate = 60
		self.rawCapture = PiRGBArray( self.camera, size=( 320, 240 ) )

		# Load a cascade file for detecting faces
		self.face_cascade = cv2.CascadeClassifier( '/home/pi/opencv-3.1.0/data/lbpcascades/lbpcascade_frontalface.xml' )

		
		# Capture frames from the camera
		for frame in self.camera.capture_continuous( self.rawCapture, format="bgr", use_video_port=True ):
			image = frame.array

			# Use the cascade file we loaded to detect faces
			gray = cv2.cvtColor( image, cv2.COLOR_BGR2GRAY )
			faces = self.face_cascade.detectMultiScale( gray )
				
			if len( faces ) == 0:
				#print ("No Face Found " )
				t = time.time() - self.t0
				if callback is not None:
					callback(loop_counter=t)#,rotation_x=last_x)
            			
				#self.my_mini_brain.face_flag = "SERVO "
            			if t > self.variable_of_time_change:
                			self.variable_of_time_change = t + int(random.uniform(0,1)*10.0) + 5.0
                			#self.app.random_pos()
				
			else:
				print ("Found " + str( len( faces ) ) + " face(s)")
				#self.my_mini_brain.face_flag = "FACE "
				n_face = 0
				# Draw a rectangle around every face and move the motor towards the face
				for ( x, y, w, h ) in faces:
					n_face += 1
					cv2.rectangle( image, ( x, y ), ( x + w, y + h ), ( 100, 255, 100 ), 2 )
					#cv2.putText( image, "Face No." + str( len( faces ) ), ( x, y ), cv2.FONT_HERSHEY_SIMPLEX, 0.5, ( 0, 0, 255 ), 2 )

					tx = x + w/2
					ty = y + h/2
					if n_face ==1:
						#HORIZONTAL

						if   ( self.cx - tx >  10 and self.my_mini_brain.xdeg <= 190 ):
							#self.my_mini_brain.xdeg += 5
							#self.my_mini_brain.update_head_position()
							pass
						elif ( self.cx - tx < -10 and self.my_mini_brain.xdeg >= 90 ):
							#self.my_mini_brain.xdeg -= 5
							#self.my_mini_brain.update_head_position()
							pass
						#VERTICAL

						if   ( self.cy - ty >  10 and self.my_mini_brain.ydeg >= self.my_mini_brain.y_min_deg):
							#self.my_mini_brain.ydeg += 5
							#self.my_mini_brain.update_head_position()
							pass
						elif ( self.cy - ty < -10 and self.my_mini_brain.ydeg <= self.my_mini_brain.y_max_deg ):
							#self.my_mini_brain.ydeg -= 5
							#self.my_mini_brain.update_head_position()
							pass
			

			# Calculate and show the FPS
			self.fps = self.fps + 1
			sfps = self.fps / ( time.time() - self.t_start )
			cv2.putText( image, "FPS : " + str( int( sfps ) ), ( 10, 10 ), cv2.FONT_HERSHEY_SIMPLEX, 0.5, ( 0, 0, 255 ), 2 )

			# Show the frame
			cv2.imshow( "Frame", image )
			cv2.waitKey( 1 )

			# Clear the stream in preparation for the next frame
			self.rawCapture.truncate( 0 )

			

def main():
    t0 = time.time()
    my_app = vision(t0)
    my_app.run() 

if __name__ == '__main__':
	main()