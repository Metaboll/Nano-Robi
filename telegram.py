#!/usr/bin/python

import json
import requests
import time
import os
import urllib

import subprocess
#

import datetime

from threading import Timer

#https://www.raspberrypi.org/forums/viewtopic.php?t=132637
#Try putting the relevant command in ~/.config/lxsession/LXDE-pi/autostart

#Eg. To run a python script use...
#@sudo /usr/bin/python /home/pi/filename.py


from urlparse import urlparse

import commands
#import socket
import platform



from dbHelper import DBHelper
import psutil

#TOKEN = '573596384:AAHGVncTqgXdmfwRraCg15taFmuEb8e38RI'
#URL = "https://api.telegram.org/bot573596384:AAHGVncTqgXdmfwRraCg15taFmuEb8e38RI/".format(TOKEN)

TOKEN = 'user_data'
URL = "http user data".format(TOKEN)


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



class telegraph_bot(object):
	def __init__(self , my_time, my_greeting ="Hi"):
		self.db=DBHelper()
		self.last_update_id = None
		self.updates = None
		self.TOKEN = 'token user telegram'
		self.URL = "https user data".format(self.TOKEN)
		self.WPA_CONF_PATH = '/etc/wpa_supplicant/wpa_supplicant.conf'
		self.GOOGLE_SERVER_ADDRESS = ('speech.googleapis.com', 443)
		self.chat_ID = "user id chat" 

		self.boolean_thread = False
		self.my_wifi = False
		self.send_message(my_greeting, self.chat_ID)
		self.kill = False
		self.exit = False
		self.my_callback = None
		self.mosquitto = False

		self.start_time = my_time
		self.time_control = 0.0

	def get_url(self,url):
		try:
			response = requests.get(url)
			content = response.content.decode("utf8")
			return content
		except Exception as e:
			print(e)


	def get_json_from_url(self,url):
		content = self.get_url(url)
		js = json.loads(content)
		return js


	#def get_updates(self,offset=None):
	def get_updates(self):
		url = self.URL + "getUpdates"
		if self.last_update_id:
			url += "?offset={}".format(self.last_update_id)
		js = self.get_json_from_url(url)
		return js


	def get_last_update_id(self,updates):
		update_ids = []
		for update in updates["result"]:
			update_ids.append(int(update["update_id"]))
		return max(update_ids)


	def handleUpdates(self,updates):
		#for update in updates['result']:
		n = len(updates["result"]) - 1
		update = updates['result'][n] 
		try:
			#print(update)
			text=update['message']['text']
			chat=update['message']['chat']['id']

			#items=self.db.get_items()
			print("He recivido ", text)
			text = text.lower()
			time_pass = time.time() - self.start_time
			if time_pass > 4:
				if text == "shutdown" or text =="apaga" or text=="kill" or text =="kill me" or text =="shut down" or text =="Hasta la vista baby" or text =="ByeBye" or text =="Bye Bye":
					self.kill = True
					time.sleep(1)
					#self.my_callback = self.shut_down

				elif text == "state" or text =="working" or text=="are you working" or text=="living" or text=="funcionando" or text=="encendido":
					self.send_message("Yes, Im working", self.chat_ID)
					print("Yes Im working")

				elif text == "mosquitto":
					print("checking mosquitto")
					self.process_mosquitto()

				elif text == "head":
					print("checking head program")
					#self.my_process("python ./Head/head.py")
					self.my_process("python ./head.py")

				
				elif text == "exit" or text =="stop": # solo para el programa
					self.exit = True
					#self.my_callback = self.stop_telegram()

				elif text == "eye" or text =="eyes": 
					print("checking eye program")
					self.my_process("python ./eye.py")

				elif text != "":
					print("WTF?")
					self.send_message("WTF?", self.chat_ID)

			#self.send_message(text, chat)
		except KeyError as e:
			print(e)






	def get_last_chat_id_and_text(self, updates):
		num_updates = len(updates["result"])
		last_update = num_updates - 1
		text = updates["result"][last_update]["message"]["text"]
		chat_id = updates["result"][last_update]["message"]["chat"]["id"]
		return (text, chat_id)


	def send_message(self,text, chat_id,replyMarkup=None):
		#    print('////////////////////////////////////////////////')
		#    print('send')
		#    print('text {}'.format(text))
		#    print('chat_id {}'.format(chat_id))
		#    print('replyMarkup {}'.format(replyMarkup))

		#text = urllib.parse.quote_plus(text)
		url = self.URL + "sendMessage?text={}&chat_id={}&parse_mode=Markdown".format(text, chat_id)
		if replyMarkup:
			url += "&reply_markup={}".format(replyMarkup)
			#print(url)
		self.get_url(url)




	def buildKeyBord(self, items):
		keybord=[[item] for item in items]
		replyMarkup={"keyboard":keybord, "one_time_keyboard": True}
		#    print(replyMarkup)
		return json.dumps(replyMarkup)



	#def get_last_chat_id_and_text(updates):
	#    num_updates = len(updates["result"])
	#    last_update = num_updates - 1
	#    text = updates["result"][last_update]["message"]["text"]
	#    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
	#    return (text, chat_id)

	def run(self):
		updates = None
		self.last_update_id = None
		print('started')
		#********
		updates = self.get_updates()
		while True:
			if len(updates["result"]) > 0:
				#print("Numero de updates ", len(updates["result"]))
				self.last_update_id = self.get_last_update_id(updates) + 1
				self.handleUpdates(updates)
			updates = self.get_updates()
			#if self.my_callback !=None:
				#self.my_callback()
			time.sleep(1)
			if self.exit == True: 
				self.stop_telegram()
			if self.kill == True: 
				self.shut_down()
			#time_pass = time.time() - self.start_time
			time_pass = time.time() - self.time_control

			#print(time_pass)
			if time_pass > 120.0:
				my_time = (time.time() - self.start_time) / 60
				self.time_control = time.time()
				a = "Yes, Im working " + str(int(my_time))
				self.send_message(a, self.chat_ID)

			
		#while True:
			#updates = self.get_updates()
			##print(updates)
			#if len(updates["result"]) > 0:
			#	self.last_update_id = self.get_last_update_id(updates) + 1
			#	self.handleUpdates(updates)
			

	def read_(self):
		updates = self.get_updates()
		if len(updates["result"]) > 0:
			self.last_update_id = self.get_last_update_id(updates) + 1
			self.handleUpdates(updates)
		
	

	def listener(self):
		self.last_update_id = None
		self.boolean_thread = True
		self.rt = RepeatedTimer(1.0, self.read_) 

	def shut_down(self):
		self.send_message("Shut Down RaspBerry Head", self.chat_ID)
		print("Shut Down")
		#subprocess.Popen(['sudo','shutdown','-r','now'])
		subprocess.call("sudo poweroff", shell=True)
		#os._exit(0)
		#call("sudo shutdown -h now", shell=True)
		#subprocess.call("sudo shutdown -h now", shell=True)
		#subprocess.Popen(['sudo','shutdown','-r','now'])
		
	def stop_telegram(self):
		self.send_message("Stopping  RaspBerry Head", self.chat_ID)
		print("Bye Bye")
		os._exit(0)
		return
		#call("sudo shutdown -h now", shell=True)
		#subprocess.call("sudo shutdown -h now", shell=True)
		#subprocess.Popen(['sudo','shutdown','-r','now'])				

	def my_process(self, process):
                my_process = process.split(" ")
		bool_process= False
		for pid in psutil.pids():
			p = psutil.Process(pid)
			#print( "proceso .... ", p.name())
			if p.name() == my_process[0]:
				a = "process .... {} is running".format(p.name())
				self.send_message(a, self.chat_ID)
				if len(my_process)>1:
					if len(p.cmdline()) > 1 and my_process[1] == p.cmdline()[1]:
						bool_process = True
						p.kill()
						a = "killed process .... " +  process
						#print( a)
						
				else:
					p.kill()
					a = "killed process .... " + process
					#print( a)
				self.send_message(a, self.chat_ID)

		if bool_process == False:
			a = "Let's Start " + process
			#print("Let's Start " , process)

			if len(my_process)>1:
				#my_process[1] = "/home/pi/Head/" + my_process[1] 
				print(" Hola " +  my_process[0] + " " + my_process[1] )
				subprocess.call(['lxterminal', '-e',  my_process[0], my_process[1] ])
			else:
    				subprocess.call(['lxterminal', '-e',  process ])
			self.send_message(a, self.chat_ID)
				
	def process_mosquitto(self):
		process = "mosquitto"
		bool_process= False
		for pid in psutil.pids():
			p = psutil.Process(pid)
			if p.name() == process:
				a = "process .... mosquitto is running"
				print( a )
				# I dont want to kill
				#bool_process = True
				#p.kill()
				#self.mosquitto = False
				#print( "killing process .... mosquitto")
						

		if bool_process == False:
			print("Let's Start Mosquitto")
    			subprocess.call(['lxterminal', '-e',  process , '-v'])
			self.mosquitto = True

	def check_mosquitto(self):
		self.mosquitto = False
		for pid in psutil.pids():
			p = psutil.Process(pid)
			#print( "proceso .... ", p.name())
			
			if p.name() == "mosquitto":
				a = "process .... {} is running".format(p.name())
				#if len(p.cmdline()) > 1 and "mosquitto" == p.cmdline()[1]:
				#print( a)
				self.send_message(a, self.chat_ID)
				self.mosquitto = True
		if self.mosquitto == False:
			a = "Let's Start Mosquitto Broker.........."
			#print(a)
			self.send_message(a, self.chat_ID)
			subprocess.call(['lxterminal', '-e',  'mosquitto' , '-v'])
    			#subprocess.call([ 'mosquitto' , '-v'])
			self.mosquitto = True
			time.sleep(1)



	def check_wifi_is_configured(self):
		"""Check wpa_supplicant.conf has at least one network configured."""
		output = subprocess.check_output(['sudo', 'cat', self.WPA_CONF_PATH]).decode('utf-8')
		return 'network=' in output


	def check_wifi_is_connected(self):
		"""Check wlan0 has an IP address."""
		output = subprocess.check_output(['ifconfig', 'wlan0']).decode('utf-8')
		return 'inet addr' in output


	def check_can_reach_google_server(self):
		"""Check the API server is reachable on port 443."""
		print("Trying to contact Google's servers...")
		try:
			sock = socket.create_connection(GOOGLE_SERVER_ADDRESS, timeout=10)
			sock.close()
			return True
		except Exception:  # pylint: disable=W0703
			return False

	def check_connection(self):
		"""Run all checks and print status."""
		print('Checking the WiFi connection...')

		if not self.check_wifi_is_configured():
			print('Please click the WiFi icon at the top right to set up a WiFi network.')
			return False

		if not self.check_wifi_is_connected():
			print(
			"""You are not connected to WiFi. Please click the WiFi icon at the top right
			to check your settings.""")
			return False

		print('WiFi Ok...')
		self.my_wifi = True

		return self.my_wifi


	def send_my_ip(self):
		a = commands.getoutput("ifconfig").split("\n")[10].split()[1]
		my_ip = " My IP ..." + a
		print(" My IP ..." , a)
		self.send_message(my_ip, self.chat_ID)
		return a
		ip_address = ''
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		s.connect(("8.8.8.8",80))
		ip_address = s.getsockname()[0]
		s.close()

		
		#return #ip_address
		#return 'Mi ip es ... {}'.format(myip)
    
	def my_ip2(self):
		#https://stackoverflow.com/questions/31564861/python-detect-http-request-to-localhost-httplib2
		myip = gethostbyname(gethostname())
		return 'Mi ip es ... {}'.format(myip)
		#if(myip == destip):



def grettings():
	now = datetime.datetime.now()
	hour = now.hour

	if hour < 12:
		greeting = "Good morning Fernando"
	elif hour < 18:
		greeting = "Good afternoon Fernando"
	else:
		greeting = "Good night Fernando"

	print("{}!".format(greeting))
	return greeting


def change_directory():
	path = "/home/pi/Head"

	# Check current working directory.
	retval = os.getcwd()
	print "Current working directory %s" % retval

	# Now change the directory
	os.chdir( path )

	retval = os.getcwd()

	print "Directory changed successfully %s" % retval


def main():
	salute = grettings()
	change_directory()
	

	print(' Starting Telegram.py >>> ')
	print(platform.python_version())
	my_time = time.time()
	my_app = telegraph_bot( my_time , salute )
	my_app.send_my_ip()
	my_app.check_mosquitto()
        my_app.run()
	#if my_app.check_connection():
		#currentTime = time.strftime('%H:%M') 
		#print(' La hora es >>> ', currentTime)
		
		#my_app.run()
	






if __name__ == '__main__':
    main()

