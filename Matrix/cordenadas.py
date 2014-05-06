#! /usr/bin/python
#-*- encoding: -utf-8-*-
import os
from gps import *
from time import *
import time
import threading
import httplib
import urllib

gpsd = None #variable global
import math
 
os.system('clear') #borra el contenido de la terminal

def conectar(Lat, Long):
  try:
    print "entre"
    print "estoy mandando", Lat, Long
    params = urllib.urlencode({'longitud':Long, 'latitud':Lat})
    headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
    conn = httplib.HTTPConnection("socketsubetech.proglabs.co")
    conn.request("POST", "/recibir", params, headers)
    response = conn.getresponse()
    print response.status, response.reason
    data = response.read()
    conn.close()
    result = ""
    print "exito"
  except:
    import sys
    print sys.exc_info()[:2]


class GpsPoller(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
    global gpsd #poner disponible la variable gpsd
    gpsd = gps(mode=WATCH_ENABLE) #comienza a buscar info
    self.current_value = None
    self.running = True #El "Thread" se pone en corrida
 
  def run(self):
    global gpsd
    while gpsp.running:
      gpsd.next() #toma la informacion del gpsd hasta que se vacía el buffer
Coordenadas= "Entre"
if __name__ == '__main__':
  gpsp = GpsPoller() # comienza el thread
  try:
    
    gpsp.start() # comienza la lectura
    while True:
      #Tarda unos segundos en tomar buena información

      os.system('clear')
      f=open("lat_long.txt","w")
      print
      print ' Lectura GPS'
      print '----------------------------------------'
      f.write(Coordenadas)
     # f.write("longitud: ",gpsd.fix.longitud, "\n")
      print 'latitud leida   ' , gpsd.fix.latitude
      print 'longitud leida ' , gpsd.fix.longitude
      print 'speed (m/s) ' , gpsd.fix.speed
      Coordenadas= str(gpsd.fix.latitude)+","+ str(gpsd.fix.longitude)
      f.close()
      ## PARSEAR LOS DATOS
      if math.isnan(gpsd.fix.latitude)==False and (gpsd.fix.latitude)!=0.0 :
        Latitud= float(gpsd.fix.latitude)
      else:
        Latitud=18.807065
      print "mandare:", Latitud
      #####
      if math.isnan(gpsd.fix.longitude)==False and (gpsd.fix.longitude)!=0.0:
        Longitud= float(gpsd.fix.longitude)
      else:
        Longitud=-99.22146
      print "mandare: ", Longitud

      conectar(Latitud, Longitud)
      time.sleep(.1) #delay
 
  except (KeyboardInterrupt, SystemExit): #si precionas ctrl+c
    print "\nMatando el Thread..."
    gpsp.running = False
    gpsp.join() # Espera a que el thread termine
    #Cierra el archivo
  print "Listo \nsaliendo..."
