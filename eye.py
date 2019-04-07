#! /usr/bin/python
#perl -i -pe's/\r$//;' 


import math
import time

from lib_oled96 import ssd1306
from time import sleep
from PIL import ImageFont, ImageDraw, Image

#from addict import Dict #https://stackoverflow.com/questions/4984647/accessing-dict-keys-like-an-attribute



import glob



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



class oled(object):
	#https://www.raspberrypi-spy.co.uk/2018/04/i2c-oled-display-module-with-raspberry-pi/
	def __init__(self ):
            from smbus import SMBus                  #  These are the only two variant lines !!
            i2cbus = SMBus(1)                        #
            # 1 = Raspberry Pi but NOT early REV1 board

            self.oled = ssd1306(i2cbus)
            self.draw = self.oled.canvas   # "draw" onto this canvas, then call display() to send the canvas contents to the hardware.
            print(" Oled Bus Conneted = Okidoky" )
            self.padding = 2
            self.shape_width = 20
            self.top = self.padding
            self.bottom = self.oled.height - self.padding - 1
            self.boolean_state = False
            #self.time_stop_threading = 0 # take control of the threading with time variable
            

        #*************************************************************************************************
        #
        # MAIN FUNCTION----> 
        #
        #   


        #*************************************************************************************************
	def run_normal(self ): #this function is always running
            #print( " run normaly")
            if self.boolean_state == True:
                self.boolean_state = False 
                self.draw.ellipse((35, self.top, 35+self.bottom, self.bottom), outline=1, fill=0)
                self.oled.display()
            else:
                self.boolean_state = True
                #self.draw.ellipse((40, self.top, 40+self.bottom-10, self.bottom-10), outline=1, fill=1)
                self.draw.ellipse((35, self.top, 35+self.bottom, self.bottom), outline=1, fill=1)
                #self.draw.ellipse((mitad_ancho - 20.0, mitad_alto - 20, mitad_ancho + 20.0, mitad_alto + 20), outline=1, fill=1)
                self.oled.display()
            

	def picture(self ):
		logo = Image.open('4.png')
		self.draw.bitmap((32, 0), logo, fill=0)
		self.draw
		self.oled.display()

	def close(self ):
            self.draw.rectangle((0, 0, self.oled.width-1, self.oled.height-1), outline=1, fill=1)
            self.oled.display()


	def rectangle(self ):
            self.draw.rectangle((0, 0, self.oled.width-1, self.oled.height-1), outline=1, fill=1)
            self.oled.display()

	def kill(self ):
            oled.onoff(0)   # kill the oled.  RAM contents still there.
            oled.cls()      # Oled still on, but screen contents now blacked out

	def display_picture(self, my_image):
		#https://www.raspberrypi-spy.co.uk/2018/04/i2c-oled-display-module-with-raspberry-pi/
		self.rectangle()
		self.oled.display()
		self.draw.bitmap((0, 0), my_image, fill=0) #antes (32, 0)
		#self.oled.image(my_image)
		self.oled.display()

class control_oled(object):
	#https://www.raspberrypi-spy.co.uk/2018/04/i2c-oled-display-module-with-raspberry-pi/
	def __init__(self ):
		#self.my_thread = my_thread
		self.app = oled()
		self.pic_files = []
		self.dic_images = {} #Dict()
		self.read_pic_files()
		self.ejecuta("hi")
		

	def read_pic_files(self):
		#https://stackoverflow.com/questions/3207219/how-do-i-list-all-files-of-a-directory
		#with open(mimovimiento) as f:
		#    self.load(f)
		my_files = glob.glob("Pics/*.ppm")
		#['Pics/eye.ppm', 'Pics/ServoPi.ppm', 'Pics/servo.ppm']
		# Alternatively load a different format image, resize it, and convert to 1 bit color.
		#image = Image.open('happycat.png').resize((disp.width, disp.height), Image.ANTIALIAS).convert('1')
		
		for im in my_files:
			image = Image.open(im).convert('1')
			temp = im.split('/', 1)[1]
			self.dic_images[temp.split('.', 1)[0]]= image
			#print("Archivos.....", temp.split('.', 1)[0])
		temp = [x.split('/', 1)[1] for x in my_files]
		print("Eye files loaded..... ", len(temp))
		self.pic_files = [y.split('.', 1)[0] for y in temp]
		
	
	def ejecuta(self, my_name_img_file):
		if my_name_img_file in self.dic_images:
			my_img_file = self.dic_images[my_name_img_file]
			#self.rt.stop()
			self.app.display_picture(my_img_file)
			#self.app.rectangle()
			#self.rt.start()

	def ejecuta_old(self, texto ="", value = 0 , value2 = 0):# value2 es porque algunas ordenes necesitan dos argumentos
		getattr(self,texto)()


	def run_(self):
		self.boolean_run_normal = True
		self.rt = RepeatedTimer(1.0, self.app.run_normal) 
		
	def stop_(self):
		self.boolean_run_normal = False
		self.rt.stop()


def main():
    print("OLED FOR EYES CONTROL TERMINAL (Python3)")
    
    my_app = control_oled()
    my_app.ejecuta("eye")
    time.sleep(4.0)
    my_app.run_() # your long-running job goes here...
    
    


if __name__ == '__main__':
	main()
	
