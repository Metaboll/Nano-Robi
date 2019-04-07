#!/usr/bin/env python
# coding: utf-8
"""
Se ha desconectado los argumentos de entrada del main pero se puede coger que servo entra y que numero se pone
Esta rutina en principio cambia el numero de identificacion del servo
Tambien puede scanear que servos estan conectados 
Despues les añade un numero y los pone otro numero de identificacion mayor

"""

from collections import defaultdict



import time
import serial
#console=serial0,115200 console=tty1


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




class serial_usb(object):
	#ls -l /dev
	#sudo nano /boot/config.txt
	#sudo i2cdetect -y 1
	#lsusb
	#chmod -x  uart_control
	#sudo ./uart_control gpio
	#dmesg | grep tty


    def __init__(self ):
        #self.my_thread = my_thread
        # configure the serial connections (the parameters differs on the device you are connecting to)
	print ("Tratando conectar......")
	self.ser = serial.Serial(
		port='/dev/ttyUSB0',
		#port='/dev/serial0',#serial0ttyAMA0
		baudrate=9600,
		parity=serial.PARITY_NONE,
		stopbits=serial.STOPBITS_ONE,
		bytesize=serial.EIGHTBITS,
		timeout=0.1
		)
        self.boolean_thread = False
        #self.ser.close()
	#self.ser.open()
	#self.ser.isOpen()
	self.message = ""
	

    def write_(self, my_order):
        self.ser.write(my_order)

    def listener(self):
	self.boolean_thread = True
	self.rt = RepeatedTimer(.5, self.read_) 

    def stop_listener(self):
	if self.boolean_thread:
		self.rt.stop() 
		self.boolean_thread = False


    def kill(self):
	self.stop_listener()
	self.ser.close() 

    def keep_on_read(self):
        while 1 :
		# get keyboard input
		#print 'Enter your commands below.\r\nInsert "exit" to leave the application.'
        	response = self.ser.readline()
        	#response = self.ser.read(8)
		print("salida....",response)

    def read_(self):
        #self.message = self.ser.readline()
	data = self.ser.readline()
	if data:
		self.message = data
        #self.message = response#print ("leyendo......")
        #print(self.message)

    def ejecuta(self, texto ="", value = 0 , value2 = 0):# value2 es porque algunas ordenes necesitan dos argumentos
        getattr(self,texto)()


    def run(self):
        self.app.run_normal # it auto-starts, no need of rt.start()


def main():
    my_app = serial_usb()
    my_app.listener()
    #my_app.keep_on_read()
    #while 1:
    #    print("salida....",my_app.read_())
	#time.sleep(.1)

if __name__ == '__main__':
	main()            




	
	