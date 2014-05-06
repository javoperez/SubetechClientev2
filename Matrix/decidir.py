#!/usr/bin/env python
# coding=utf-8	

import time
import multiprocessing
import gpio
y="None"

def decidir(estado_queue, permiso_queue):
	### DESCOMENTAR EN PCDUINO
	rojo = "gpio6"
	verde = "gpio7"
	alarma= "gpio8"
	gpio.pinMode(rojo, gpio.OUTPUT)
	gpio.pinMode(verde, gpio.OUTPUT)
	gpio.pinMode(alarma, gpio.OUTPUT)
	while 1:

		edo= estado_queue.get()
		if edo== None or edo== "sale":
			edo= False
		if edo=="entra":
			edo= True
		perm= permiso_queue.get()
		print "Estado:  ", edo
		print "Permiso: ", perm
	
		if edo==False and perm== False:
			gpio.digitalWrite(alarma, gpio.LOW)
			gpio.digitalWrite(rojo, gpio.LOW)
			gpio.digitalWrite(verde, gpio.LOW)
			print "alarma, rojo y verde apagados"
		if edo==False and perm== True:
			gpio.digitalWrite(verde, gpio.HIGH)
			print "verde prendido"
		if edo==True and perm== False:

			gpio.digitalWrite(alarma, gpio.HIGH)
			gpio.digitalWrite(rojo, gpio.HIGH)
			print "Rojo y alarma prendidos.. delay"
			time.sleep(3)
			estado_queue.put(False)
			permiso_queue.put(False)

		if edo==True and perm== True:
			time.sleep(.2)
			estado_queue.put("sale")
			permiso_queue.put(False)		
		
def main():
	print "Creando procesos de comunicación..."
	estado_queue =multiprocessing.Queue()
	permiso_queue =multiprocessing.Queue()
	t = multiprocessing.Process(target=decidir, args=(estado_queue,permiso_queue))
	t.daemon = True

	estado_queue.put("entra")
	permiso_queue.put(False)


	try:
		t.start()
		time.sleep(100)
	except:
		print "ERROR: No se pudieron crear los procesos de comunicación."

if __name__ == "__main__":
	main()