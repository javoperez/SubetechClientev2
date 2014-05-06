import httplib
import urllib
import cordenadas

y= None
Latitud=""
Longitud=""

def leer():
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
		Latitud= "0"
	if Longitud== "nan":
		Longitud= "0"
	print "Latitud", Latitud
	print "Longitud", Longitud
	global Latitud
	global Longitud

def conectar():
	try:

		params = urllib.urlencode({'clave': y, 'longitud':Longitud, 'latitud':Latitud})
		headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
		conn = httplib.HTTPConnection("162.243.55.207:49311")
		conn.request("POST", "/descontar/", params, headers)
		response = conn.getresponse()
		print response.status, response.reason
		data = response.read()
		conn.close()
		result = ""
	except:
		import sys
		print sys.exc_info()[:2]


#main:

while y!= "exit":
	print "Ingresa <exit> para salir" 
	y= raw_input("Esperando codigo... ")
	leer()
	conectar()
	Latitud=""
	Longitud=""
