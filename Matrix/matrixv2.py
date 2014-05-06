#!/usr/bin/env python
# coding=utf-8

import httplib
import urllib
import time
import multiprocessing
import gpio

cmd= ""
Latitud=""
Longitud=""
y= None

def leer():
	global Latitud
	global Longitud
	f = open("lat_long.txt")
	lectura=f.read()
	f.close()
	letra=""
	for letra in lectura:
		Latitud= Latitud+letra
		if letra== ",":
			break
	Longitud= lectura.replace(Latitud, "")
	Latitud=Latitud.replace(",", "")

	if Latitud== "nan":
		Latitud= "18.8091843"
	if Longitud== "nan":
		Longitud= "-99.2206003"
	print "Latitud", Latitud
	print "Longitud", Longitud
	

def conectar():
	try:

		params = urllib.urlencode({'clave': cmd,  'longitud':Longitud, 'latitud':Latitud})
		headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
		conn = httplib.HTTPConnection("162.243.55.207:49311")
		conn.request("POST", "/descontar/", params, headers)
		response = conn.getresponse()
		#print response.status, response.reason
		data = response.read()
		conn.close()
		result = ""
		
	except:
		import sys
		print sys.exc_info()[:2]
		return 401
	return response.status

sensor1 = "gpio5"
sensor2="gpio4"
y=None
def detectarpcduino(estado_queue, permiso_queue):
	while 1:
		A=gpio.digitalRead(sensor1)
		B= gpio.digitalRead(sensor2)
		if A==True:
			while B==False and y!= "salir":
				print "ciclo 1A (entra)"
				B=gpio.digitalRead(sensor2)
				if B==True:
					A=False 
					while B==True:
						B=gpio.digitalRead(sensor2)
						print "Ciclo 2A (entra)"
					y= "salir"
			estado_queue.put(True)

		y=""
			
		if B==True:
				
			while A==False  and y!= "salir":
				print "ciclo 1B"
				A=gpio.digitalRead(sensor1)
				if A==True:
					B=False 
					while A==True:
						A=gpio.digitalRead(sensor1)
						print "Ciclo 2B"
					y= "salir"
			estado_queue.put(False)
		#print "estado1" , Estado
		print estado_queue.qsize()
		time.sleep(.1)

		
##PRUEBA

def decidir(estado_queue, permiso_queue):
	pass

	### DESCOMENTAR EN PCDUINO
	rojo = "gpio6"
	verde = "gpio7"
	alarma= "gpio8"
	gpio.pinMode(rojo, gpio.OUTPUT)
	gpio.pinMode(verde, gpio.OUTPUT)
	gpio.pinMode(alarma, gpio.OUTPUT)

	while 1:
		if estado_queue.qsize>0:
			Estado= estado_queue.get()
		else:
			Estado= False

		if permiso_queue.qsize>0:
			Permiso=permiso_queue.get()
		else:
			Permiso= False
						
		if Estado==False and Permiso== False:
			gpio.digitalWrite(alarma, gpio.LOW)
			gpio.digitalWrite(rojo, gpio.LOW)
			gpio.digitalWrite(verde, gpio.LOW)
			print "alarma, rojo y verde apagados"
		if Estado==False and Permiso== True:
			gpio.digitalWrite(verde, gpio.HIGH)
			print "verde prendido"
		if Estado==True and Permiso== False:

			gpio.digitalWrite(alarma, gpio.HIGH)
			gpio.digitalWrite(rojo, gpio.HIGH)
			print "Rojo y alarma prendidos.. delay"
			time.sleep(3)
			Estado=False
			Permiso=False
			
			
		if Estado==True and Permiso== True:
			time.sleep(.2)
			Estado=False
			Permiso=False		
		time.sleep(1)

def main():
	global Latitud
	global Longitud
	global cmd
	cmd= "compartido"
	print "Creando procesos de comunicación..."
	estado_queue =multiprocessing.Queue()
	permiso_queue =multiprocessing.Queue()
	t = multiprocessing.Process(target=detectarpcduino, args=(estado_queue, permiso_queue))
	t2 = multiprocessing.Process(target=decidir, args=(estado_queue, permiso_queue))

	t.daemon = True
	t2.daemon = True
	try:
		t.start()
		time.sleep(.1)
		t2.start()
		time.sleep(.1)
		"""
		##INICIALIZO VARIABLES por primera vez
		permiso_queue.put("inicial")
		estado_queue.put("inicial")
		"""
	except:
		print "ERROR: No se pudieron crear los procesos de comunicación."


	while(cmd != "exit"):
		print "Ingresa <exit> para salir " 
		cmd = raw_input("Esperando codigo... ")
		leer()
		permiso= conectar()
	
		if permiso==200:
			Permiso=True
		else:
			Permiso=False
		time.sleep(1)
		#IMPRIMIR PERMISO Y ESTADO	
		#temporalestado= estado_queue.get()
		permiso_queue.put(Permiso)

		Latitud=""
		Longitud=""
		

	print "Terminando procesos..."
	t.terminate()
	t2.terminate()
	print t
	print t2

if __name__ == "__main__":
	main()
