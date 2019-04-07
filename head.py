#! /usr/bin/python
#perl -i -pe's/\r$//;' 


import os

from ServoPi import PWM
from ServoPi import Servo

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

from eye import control_oled
#from serial_ import serial_usb
from servo  import servo
from face import vision

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


class head(object):       
	def __init__(self):

		#####***********************######
		t0 = time.time()
		self.my_face_app = vision(t0)
		#self.my_face_app.run() 

		#my_order = "SERVO "
		self.face_flag = "SERVO" # "FACE " # to note and send face is found
		self.camara_loop = True # to stop or play face tracking and looking for
		self.serial_message = ""
		
		### Setup Eyes. #####################################################################
		
		self.my_eyes = None
		self.my_eyes = self.oled_link()
		self.time_eyes_blink = 0 # if it is different to 0 you have to wait to 20 seconds
		
		if self.my_eyes:
			self.my_eyes.run_()

		### Setup Servo S. #####################################################################
		self.servo = servo(time.time())
		
		xdeg, ydeg, _ = self.servo.get_deg_values()
		print("del calculo los cojones sale ......x. ", xdeg , " y ... ", ydeg)

		self.xdeg = xdeg #160
		self.ydeg = ydeg #150


		self.x_med_deg = xdeg # horizontal fix position


		self.y_med_deg = ydeg #150
		self.y_min_deg = self.y_med_deg - 50
		self.y_max_deg = self.y_med_deg + 50


		self.buffer_xdeg = self.xdeg
		self.buffer_ydeg = self.ydeg

		self.servo.hor_ver_move( self.xdeg , self.ydeg)

		#self.t0 = time.time()
		
		


		### Serial USB raspberry comunication. #####################################################################
		#self.serial_ = None
		#self.serial_ = self.serial_link()
		#if self.serial_:
		#	self.serial_.listener() #activa para escuchar
		

	def oled_link(self ):
		try:
			my_eyes = control_oled()
			print("Oled Eyes Open----> Ok")
			return (my_eyes)

		except:
			print("Oled Eyes problems......")
			return None

	def serial_link(self ):
		try:
			serial_ = serial_usb()
			print("Serial Port Open----> Ok")
			return (serial_)


		#except KeyboardInterrupt:
		#	print(" User Keyboard Interrupt")
		#	print(" ...... ")
		#	print(" ...... ")
		#	print(" ...... ")
		#	if self.serial_:
		#		self.serial_.kill()
		#	quit()

		except:
			print(" Error Serial Communication")
			#self.serial_ = None
			return None

	def num_there(self, my_str):
		#return any(i.isdigit() for i in my_str)
		#my_arry  = [int(s) for s in my_str.split() if s.isdigit()]
		my_arry = re.findall(r'\d+', my_str) # 'hello 42 I\'m a 32 string 30'
		return	my_arry

	def shutdown(self):
		print("Head program kill........bye bye")
		#self.serial_.kill()									
		os._exit(0)			

	def control_blink_eyes(self):
		if self.my_eyes:
			if self.time_eyes_blink != 0:
				my_time = time.time() - self.time_eyes_blink
				if my_time > 10:
					self.time_eyes_blink = 0
					self.my_eyes.run_()
			
	def new_eyes_order(self, my_order):
		self.my_eyes.stop_()
		self.time_eyes_blink = time.time() # wait 20 seconds
		self.my_eyes.ejecuta(my_order)		

	def head_order(self, my_order):
		self.buffer_xdeg = self.xdeg
		self.buffer_ydeg = self.ydeg
		self.servo.ejecuta("Hi")
		self.xdeg = self.buffer_xdeg
		self.ydeg = self.buffer_ydeg
		self.servo.hor_ver_move( self.xdeg , self.ydeg)

	def update_head_position(self):
		self.servo.hor_ver_move( self.xdeg , self.ydeg)

	def my_call(self, loop_counter):#,my_mesagge):
		print("loop_counter is .. ", loop_counter)

	def run(self ): 
		
		self.control_blink_eyes()
		self.my_face_app.run(callback=self.my_call) 
			

def main():
    my_app = head()
    my_app.run() 

if __name__ == '__main__':
	main()