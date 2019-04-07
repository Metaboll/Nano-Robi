#! /usr/bin/python
#perl -i -pe's/\r$//;' 


#from gpiozero import Servo
#from gpiozero import AngularServo

from ServoPi import PWM
from ServoPi import Servo

import math


from config_servo import ergo_servo_config
#https://github.com/abelectronicsuk/ABElectronics_Python_Libraries/tree/master/ServoPi

from time import sleep
import time
import random
import numpy as np



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

class servo(object):

	def __init__(self , my_t0):
                   
            # Currently value	
            self.xdeg = 150
            self.ydeg = 150
            self.thetadeg = 150

            self.x_amp = 50
            self.y_amp = 50
            self.th_amp = 50

            self.set_robot(ergo_servo_config)
            
            self.number_servos = len(self.servos)
            print(" Number of servos = " ,self.number_servos)


            self.servo = Servo(0x40)
            self.servo.output_enable()
            self.servoMin = 180  # Min pulse length out of 4096
            self.servoMed = 400  # Min pulse length out of 4096
            self.servoMax = 500  # Max pulse length out of 4096
            self.servo.set_low_limit(0.5) #1.0
            self.servo.set_high_limit(2.0) #2.2


            self.curr_pos =  [0,0,0]
            self.padding = 2
            
            self.t0 = my_t0
            self.variable_of_time_change = 3 
            print(" Servo Head on Control = Ok" )


	def set_robot(self , servo_configuration):
            self.servo_robot = servo_configuration
            self.servos = list(self.servo_robot["motors"])


            for key in self.servos:
                item = self.servo_robot["motors"][key]
                code = item['code']
                #max_value_servo = item["max"]
                #min_value_servo = item["min"]
		#mid_value = (max_value_servo + min_value_servo)/2.0
                mid_value = item["mid"]
                amp_value_servo = item["amp"]
		item["max"] = mid_value + amp_value_servo
		item["min"] = mid_value - amp_value_servo
		#print("el valor max es ", item["max"])
		#print("el valor min es ", item["min"])
		if code == 'xdeg':
			self.xdeg = mid_value
			self.x_amp = amp_value_servo
		elif code == 'ydeg':
			self.ydeg = mid_value
			self.y_amp = amp_value_servo
		elif code == 'thetadeg':
			self.thetadeg = mid_value
			self.th_amp  = amp_value_servo

	def get_deg_values(self):
            return self.xdeg , self.ydeg, self.thetadeg
            

        #*************************************************************************************************
        #
        # MAIN FUNCTION----> thread
        #
        #   
        #*************************************************************************************************

	def run_normal(self ): #this function is always running
            print( " working servo head terminal......... everything OK" )
            t = time.time() - self.t0
            if t > self.variable_of_time_change:
                self.variable_of_time_change = t + int(random.uniform(0,1)*10.0) + 3.0
                self.random_pos()
                

	def hor_move(self, my_value):         
            last_move = self.curr_pos 
            last_move[0] = my_value
            self.motion_managent(  last_move, 1)
            time.sleep(.5)             

	def ver_move(self, my_value):         
            last_move = self.curr_pos 
            last_move[1] = my_value
            self.motion_managent(  last_move, 1)
            time.sleep(.5)    

	def hor_ver_move(self, my_h_value , my_v_value):           
            last_move = self.curr_pos 
            last_move[0] = my_h_value
            last_move[1] = my_v_value
            self.motion_managent(  last_move, 1)
            time.sleep(.5)

	def random_pos(self):
            ##pos = int(random.uniform(-1, 1)*15.0)
            ##pos = [int(1000*random.random()) for i in range(10000)]
            ##pos1 = [int(random.uniform(-1, 1)*15.0) for i in range(3)]
            #a = [ 250,100,160 ] # esde es centro[[60,200,250],[75,100,140],[140,160, 200]]
            a1 = int(random.uniform(-1, 1)*90.0) + 170
            a2 = int(random.uniform(0, 1)*20.0) + 100  
            a = [ a1,a2,160 ] 
            print("Randon move to ...." , a)
            self.motion_managent(  a, 1)
            time.sleep(.5)
            #_to_( a)

	def motion_managent(  self, movement, f = 0.1 ):
		
            #my_servos = list(self.servo_robot["motors"])

            for key in self.servos:
                item = self.servo_robot["motors"][key]
                servo = item['servo']
                max_value_servo = item["max"]
                min_value_servo = item["min"]
                my_move = movement[servo-1]
                if my_move < min_value_servo:
                    my_move = min_value_servo
                if my_move > max_value_servo:
                    my_move = max_value_servo
		    #print("maximo alcanzado ", max_value_servo, " del servo ", servo)
		#print(servo)
                self.servo.move(servo, my_move)
            self.curr_pos = movement 
            #time.sleep(f)

	def _to_( self,  to_):
            t0 = time.time()
            pulse = 0.05
            from_ = self.curr_pos
            for i in np.arange(0.0, 1.0, pulse):
                temp = (( 1.0 - i)*from_[0] + i * to_[0])
                temp2 = (( 1.0 - i)*from_[1] + i * to_[1])
                temp3 = (( 1.0 - i)*from_[2] + i * to_[2])
                self.servo_array[0].angle = temp
                self.servo_array[1].angle = temp2
                self.servo_array[2].angle = temp3
                sleep(pulse)
            self.curr_pos = to_ 

	
	def close(self ):
            pass


	def kill(self ):
            p.stop()
            #GPIO.cleanup()

	def ejecuta(self, texto ="", value = 0 , value2 = 0):# value2 es porque algunas ordenes necesitan dos argumentos
		getattr(self,texto)()

	def Hi(self):
	    print("Head order Hi")
            a = [ self.xdeg,self.ydeg - 50 ,self.thetadeg ] #self.xdeg , [ 140,75,170 ]
            b = [ self.xdeg,self.ydeg - 10 ,self.thetadeg ] # [ 140,120,170 ]
            c = [ self.xdeg,self.ydeg - 30 ,self.thetadeg ] #[ 140,90,170 ]
            self.motion_managent( b, 0.2)
            time.sleep(1)
            self.motion_managent( a, 0.2)
            time.sleep(1)
            self.motion_managent( c, 0.2)
            time.sleep(1)


	def yes(self):
            a = [ self.xdeg,self.ydeg - 30, self.thetadeg ] #[ 140,80,170 ]
            b = [ self.xdeg, self.ydeg , self.thetadeg ] # [ 140,100,170 ]
            n = random.randrange(5) + 3
            #print(n)
            while n>0:
                n -=1
                self.motion_managent( a, 0.2)
                time.sleep(.1)
                self.motion_managent( b, 0.2)
                time.sleep(.1)

	def no(self):
            a = [ self.xdeg - 40 , self.ydeg,self.thetadeg ] #[ 90,100,170 ]
            b = [ self.xdeg + 40 , self.ydeg,self.thetadeg ] # [ 170,100,170 ]
            n = random.randrange(5) + 1 
            #print(n)
            while n>0:
                n -=1
                self.motion_managent( a, 0.2)
                time.sleep(.1)
                self.motion_managent( b, 0.2)
                time.sleep(.1)
            return 
            self.motion_managent( a, 0.2)
            time.sleep(.1)
            self.motion_managent( b, 0.2)
            time.sleep(.1)
            self.motion_managent( a, 0.2)
            time.sleep(.1)
            self.motion_managent( b, 0.2)
            time.sleep(.1)
            print(".......................no....................")

class control_head(object):
    def __init__(self , my_t0_time):
        #self.my_thread = my_thread
        self.t0 = my_t0_time
        self.app = servo(my_t0_time)


    def hello(self):
        #self.app.run()
        t = time.time()-t0
        print("Segundos.....", int(t))
        #print ("Hello %s!".format(name))


    def ejecuta(self, texto ="", value = 0 , value2 = 0):# value2 es porque algunas ordenes necesitan dos argumentos
        getattr(self,texto)()



    def run(self):
        rt = RepeatedTimer(1, self.app.run_normal) # it auto-starts, no need of rt.start()
        self.app.run_normal()


def main():
    print("SERVO HEAD CONTROL TERMINAL (Python3)")
    t0 = time.time()
    my_app = control_head(t0)
    my_app.run() # your long-running job goes here...

if __name__ == '__main__':
	main()
	
