# -*- encoding: utf-8 -*-
# ----------------------------------------------- #
#   
#  Detección de objetos OpenCV
#  Autor : Jorge Luis Mayorga
#	   Daniel Jose Penagos
#	   Sergio Tinto Sarmiento
#  Uniandes 2015 -II
# ----------------------------------------------- #



# ---- Imports ---------------------------------- #
import cv2
import numpy as np
import threading
import time
import socket
import sys
import Adafruit_BBIO.PWM as PWM
import Adafruit_BBIO.GPIO as GPIO
# ----------------------------------------------- #




# ---- Definir Constantes ----------------------- #
PWM_frequency = 600 #Hz
IndexCamara = 0
RutaObjeto1 = "img/obj1.jpg"
RutaObjeto2 = "img/obj2.jpg"
RutaObjeto3 = "img/obj3.jpg"
# ----------------------------------------------- #


# --- Declarar Variables ------------------------ #
Angle1 = 50.0
Angle2 = 50.0
Angle3 = 50.0
Angle4 = 50.0
Angle5 = 0.0
Angle6 = 0.0

Time2Sleep = 100
Time2Hungry = 30
Time2Fun =10

TimeAwake = 0.0	
TimeSleep = 0.0
TimeHungry = 0.0
TimeNoHungry = 0.0
TimeFun = 0.0
TimeBoring = 0.0

HungryLevel = 100.0
SleepLevel = 100.0
FunLevel = 100.0

camStatus = 0
# ----------------------------------------------- #



# ---- Iniciar Objetos -------------------------- #
Objeto1 = cv2.imread(RutaObjeto1,1)
Objeto2 = cv2.imread(RutaObjeto2,1)
Objeto3 = cv2.imread(RutaObjeto3,1)

GPIO.setup("P8_11", GPIO.OUT)



# ----------------------------------------------- #



# ----------------------------------------------- #
# --- Def Camera Function ----------------------- #
# ----------------------------------------------- #
def CamLoop():
	while True:
		if(camStatus==1):
			CapturaVideo = cv2.VideoCapture(IndexCamara)
			_,frame = CapturaVideo.read()
			CapturaVideo.release()
		
# ----------------------------------------------- #




# ----------------------------------------------- #
# --- Def Motor Control ------------------------- #
# ----------------------------------------------- #
def MotorLoop():
	global PWM_frequency
    	PWM.cleanup()
	PWM.start("P8_13",0,PWM_frequency,0)
	PWM.start("P8_19",0,PWM_frequency,0)
	PWM.start("P8_45",0,PWM_frequency,0)
	PWM.start("P8_46",0,PWM_frequency,0)
	PWM.start("P9_14",0,PWM_frequency,0)
	PWM.start("P9_21",0,PWM_frequency,0)
	PWM.start("P9_22",0,PWM_frequency,0)
	PWM.start("P9_42",0,PWM_frequency,0)
	while True:
		global Angle1
		global Angle2
		global Angle3
		global Angle4
		global Angle5
		global Angle6
		PWM.set_duty_cycle("P8_13",Angle1)
		PWM.set_duty_cycle("P9_14",Angle2)
		PWM.set_duty_cycle("P9_21",Angle3)
		PWM.set_duty_cycle("P9_42",Angle4)
		print str(Angle1)
		#PWM.set_duty_cycle("P8_19",Angle2)
		#PWM.set_duty_cycle("P8_46",Angle4)
		#PWM.set_duty_cycle("P9_16",Angle6)
	
# ----------------------------------------------- #



# ----------------------------------------------- #
# --- Def Internet Socket ----------------------- #
# ----------------------------------------------- #
def ServerListenLoop():
	HOST = "157.253.235.209"
	PORT = 8080
	ServerNetSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		ServerNetSocket.bind((HOST, PORT))
	except socket.error as msg:
		print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
		sys.exit()
	ServerNetSocket.listen(10)
	print 'Socket Listo.... Recibiendo datos'
	while True:
		conn, addr = ServerNetSocket.accept()
		print conn.PWM
	ServerNetSocket.close()	
# ----------------------------------------------- #




# ----------------------------------------------- #
# --- Def Internet Socket ----------------------- #
# ----------------------------------------------- #
def ServerSendLoop():
	3+3
# ----------------------------------------------- #



# ----------------------------------------------- #
# --- Iniciar Codigo ---------------------------- #
# ----------------------------------------------- #
tCamLoop = threading.Thread(target=CamLoop)
tCamLoop.daemon = True
tCamLoop.start()

tMotorLoop = threading.Thread(target=MotorLoop)
tMotorLoop.daemon = True
tMotorLoop.start()

tServerListenLoop = threading.Thread(target=ServerListenLoop)
tServerListenLoop.daemon = True
tServerListenLoop.start()

tServerSendLoop = threading.Thread(target=ServerSendLoop)
tServerSendLoop.daemon = True
tServerSendLoop.start()
# ----------------------------------------------- #

while True:
	if(userOrder = "Bailar"):
		for i in range(0,5):
			#Bailar 1
			Angle1 = 27 #Brax Der
			Angle2 = 78 #Hombrx Der
			Angle3 = 50 #Hombrx Izq
			Angle4 = 27 #Braz Der
			time.sleep(0.5)
			#Bailar 2
			Angle1 = 50 #Brax Der
			Angle2 = 78 #Hombrx Der
			Angle3 = 66 #Hombrx Izq
			Angle4 = 27 #Braz Der
			time.sleep(0.5)

		

	

	
	
	
