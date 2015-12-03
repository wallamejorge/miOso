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
import requests
import json
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

camStatus = 0
userOrder = "Null"

comida = 100
jugar = 100
dormir = 100
resultadoJuego = 0


C1_min = np.array([0,100,100])   # Naranjas - Ocres
C1_max = np.array([25,255,255])

C2_min = np.array([25,100,100])  #Amarillo 
C2_max = np.array([50,255,255])

C3_min = np.array([50,100,100])  #Verdes
C3_max = np.array([75,255,255])

C4_min = np.array([75,100,100])  #Agua Marina
C4_max = np.array([100,255,255])

C5_min = np.array([100,100,100]) #Azul Oscuro
C5_max = np.array([135,255,255])

C6_min = np.array([135,100,100]) #Violeta
C6_max = np.array([155,255,255])

C7_min = np.array([155,100,100]) #Rojo
C7_max = np.array([255,255,255])

C_min = np.array([0,0,0])
C_max = np.array([100,100,100])
# ----------------------------------------------- #



# ---- Iniciar Objetos -------------------------- #
Objeto1 = cv2.imread(RutaObjeto1,1)
Objeto2 = cv2.imread(RutaObjeto2,1)
Objeto3 = cv2.imread(RutaObjeto3,1)
cap = cv2.VideoCapture(0)
k_index = 7
k_score = 0
a = range(0,15)
# ----------------------------------------------- #


# ----------------------------------------------- #
# --- Def Camera Function ----------------------- #
# ----------------------------------------------- #
def CamLoop():
	while True:
		global camStatus
		global k_index
		if(camStatus==1):	
			global k_score
			global C_min,C_max,C1_min,C1_max,C2_min,C2_max,C3_min,C3_max,C4_min,C4_max,C5_min,C5_max,C6_min,C6_max,C7_min,C7_max,cap
			for i in range(0,15):
				ret , frame = cap.read()
				hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
				if(k_index == 1):
					C_min = C1_min
					C_max = C1_max
				if(k_index == 2):
					C_min = C2_min
					C_max = C2_max
				if(k_index == 3):
					C_min = C3_min
					C_max = C3_max
				if(k_index == 4):
					C_min = C4_min
					C_max = C4_max
				if(k_index == 5):
					C_min = C5_min
					C_max = C5_max
				if(k_index == 6):
					C_min = C6_min
					C_max = C6_max
				if(k_index == 7):
					C_min = C7_min
					C_max = C7_max
				mask = cv2.inRange(hsv,C_min,C_max)
				moments = cv2.moments(mask)
				area = (moments['m00'] + 0.0)/10000.001
				a[i]=area
			k_score = np.mean(a)
			print k_score
		k = cv2.waitKey(5) & 0xFF
		if k == 27:
			break
	cv2.destroyAllWindows()
# ----------------------------------------------- # 






# ----------------------------------------------- #
# --- Def Motor Control ------------------------- #
# ---------------------------------------------- #
def MotorLoop():
	global PWM_frequency
    	PWM.cleanup()
	PWM.start("P8_13",0,PWM_frequency,0)
	PWM.start("P9_14",0,PWM_frequency,0)
	PWM.start("P9_21",0,PWM_frequency,0)
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
# ----------------------------------------------- #




# ----------------------------------------------- #
# --- Def Internet Socket ----------------------- #
# ----------------------------------------------- #
def ServerGETLoop():
	while True:
		global userOrder
		print str(1)
		try:
			global comida
			global jugar
			global dormir
			global k_index
			global k_score
			IP = "http://157.253.206.37:2000"
			NivelHambre = comida
			NivelSuenio = dormir
			NivelDiversion = jugar
			juego = k_score
			comando = "OK"
			msg = str(IP) + "/?hambre=" + str(NivelHambre) + "&" + "suenio=" + str(NivelSuenio) + "&" + "diversion=" + str(NivelDiversion) + "&" + "juego=" + str(juego) + "&tipojuego=" + str(k_index) +  "&comando=" + str(comando)
			r = requests.get(msg)
			print r.text
			data  = json.loads(r.text)
			userOrder = data['comando']
		except:
			pass
		
# ----------------------------------------------- #




# ----------------------------------------------- #
# --- Def Internet Socket ----------------------- #
# ----------------------------------------------- #
def ServerPOSTLoop():
	while True:
		global comida
		global dormir
		global jugar
		comida = comida - 1
		dormir = dormir - 1
		jugar  = jugar - 1

        	global k_index
		global k_score
		print str(2)
		try:
			IP = "http://157.253.206.37:2500"
			NivelHambre = comida
			NivelSuenio = dormir
			NivelDiversion = jugar
			JuegoRojo = 0
			JuegoAzul = 0
			JuegoVerde = 0
			comando = "OK"
			msg = str(IP) + "/?hambre=" + str(NivelHambre) + "&" + "suenio=" + str(NivelSuenio) + "&" + "diversion=" + str(NivelDiversion) + "&" + "juego=" + str(juego) + "&tipojuego=" + str(k_index) +  "&comando=" + str(comando)
			r = requests.get(msg)
			print r.text
		except:
			pass
		time.sleep(1)
# ----------------------------------------------- #

osoOrder = "Quieto"

# ----------------------------------------------- #
# --- Def MovimientoOso -------------------------- #
# ----------------------------------------------- #
def OsoLoop():
	while True:
		global osoOrder
		global Angle1
		global Angle2
		global Angle3
		global Angle4
		print osoOrder
		if(osoOrder == "Quieto"):
			#Saludar 1
			Angle1 = 50 #Brax Der
			Angle2 = 78 #Hombrx Der
			Angle3 = 50 #Hombrx Izq
			Angle4 = 27 #Braz Der
			time.sleep(0.5)
		if(osoOrder == "Saludar"):
			for i in range(0,4):
				#Saludar 1
				Angle1 = 50 #Brax Der
				Angle2 = 78 #Hombrx Der
				Angle3 = 50 #Hombrx Izq
				Angle4 = 78 #Braz Der
				time.sleep(0.5)
				#Saludar 2
				Angle1 = 50 #Brax Der
				Angle2 = 78 #Hombrx Der
				Angle3 = 27 #Hombrx Izq
				Angle4 = 78 #Braz Der
				time.sleep(0.5)
		if(osoOrder  == "SerFeliz"):
			for i in range(0,4):
				#Saludar 1
				Angle1 = 50 #Brax Der
				Angle2 = 27 #Hombrx Der
				Angle3 = 50 #Hombrx Izq
				Angle4 = 78 #Braz Der
				time.sleep(0.5)
				#Saludar 2
				Angle1 = 66 #Brax Der
				Angle2 = 27 #Hombrx Der
				Angle3 = 27 #Hombrx Izq
				Angle4 = 78 #Braz Der
				time.sleep(0.5)	
		if(osoOrder  == "Abrazar"):
			for i in range(0,4):
				#Saludar 1
				Angle1 = 50 #Brax Der
				Angle2 = 78 #Hombrx Der
				Angle3 = 50 #Hombrx Izq
				Angle4 = 27 #Braz Der
				time.sleep(0.5)
				#Saludar 2
				Angle1 = 27 #Brax Der
				Angle2 = 78 #Hombrx Der
				Angle3 = 66 #Hombrx Izq
				Angle4 = 27 #Braz Der
				time.sleep(0.5)
		if(osoOrder  == "Bailar"):
			for i in range(0,4):
				#Saludar 1
				Angle1 = 50 #Brax Der
				Angle2 = 78 #Hombrx Der
				Angle3 = 66 #Hombrx Izq
				Angle4 = 27 #Braz Der
				time.sleep(0.5)
				#Saludar 2
				Angle1 = 27 #Brax Der
				Angle2 = 78 #Hombrx Der
				Angle3 = 50 #Hombrx Izq
				Angle4 = 27 #Braz Der
				time.sleep(0.5)
		if(osoOrder  == "Pataleta"):
			for i in range(0,4):
				#Saludar 1
				Angle1 = 40 #Brax Der
				Angle2 = 27 #Hombrx Der
				Angle3 = 60 #Hombrx Izq
				Angle4 = 78 #Braz Der
				time.sleep(0.5)
				#Saludar 2
				Angle1 = 20 #Brax Der
				Angle2 = 27 #Hombrx Der
				Angle3 = 72 #Hombrx Izq
				Angle4 = 78 #Braz Der
				time.sleep(0.5)	

# ----------------------------------------------- #
# --- Iniciar Codigo ---------------------------- #
# ----------------------------------------------- #
tCamLoop = threading.Thread(target=CamLoop)
tCamLoop.daemon = True
tCamLoop.start()

tMotorLoop = threading.Thread(target=MotorLoop)
tMotorLoop.daemon = True
tMotorLoop.start()

tServerGETLoop = threading.Thread(target=ServerGETLoop)
tServerGETLoop.daemon = True
tServerGETLoop.start()

tServerPOSTLoop = threading.Thread(target=ServerPOSTLoop)
tServerPOSTLoop.daemon = True
tServerPOSTLoop.start()


tOsoLoop = threading.Thread(target=OsoLoop)
tOsoLoop.daemon = True
tOsoLoop.start()
# ----------------------------------------------- #

while True:
	camStatus = 1
	if(userOrder == "comer"):
		osoOrder = "Abrazar"
		time.sleep(0.5)
		comida = comida + 8
		userOrder = "Null"
		print comida
	if(userOrder == "jugar"):
		osoOrder = "Bailar"
		jugar = jugar +8
		time.sleep(0.5)
		userOrder = "Null"
	if(userOrder == "dormir"):
		osoOrder = "Pataleta"
		dormir = dormir +8
		time.sleep(0.5)
		userOrder = "Null"
	if(userOrder == "Null"):
		osoOrder = "Quieto"
	
	




	
