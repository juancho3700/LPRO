from serial import Serial
from time import sleep
import json
import threading
from datetime import datetime, timedelta
import time

from pymongo import MongoClient

client = MongoClient('localhost', 27017)
mydatabase = client['LPRO']
collection = mydatabase['LPRO']

for i in collection.find(): 
    print(i) 

temporizadores = {}
tiempo_para_eliminar_rssi = 10 # En segundos

def añadeTimeStamp():
    documentos = collection.find()

    while True:
        documentos = collection.find()

        for documento in documentos:
            ultima_actualizacion = documento.get("ultima_actualizacion_rssi", 0)
            tiempo_actual = time.time()

            if tiempo_actual - ultima_actualizacion > 10:
                print("Ha pasado el timestamp, actualizo RSSI a NONE")
                collection.update_one({"_id": documento["_id"]}, {"$set": {"RSSI": "-5000"}})
                collection.update_one({"_id": documento["_id"]}, {"$set": {"ultima_actualizacion_rssi": tiempo_actual}})

        time.sleep(1)    

def actualizar_usuarios (mac, ubicacion, rssi):

    busqueda = collection.find_one({'MAC': mac})
    tiempo_actual = time.time()

    if busqueda.get('RSSI') is None: 
        print("Entro en RSSI")
        collection.update_one({"_id": busqueda["_id"]}, {"$set": {"RSSI":"-5000"}})

    if busqueda["Ubicacion"] != ubicacion and int(rssi) >= int(busqueda["RSSI"]):
        collection.update_one({"_id": busqueda["_id"]}, {"$set": {"Ubicacion":ubicacion, "RSSI": rssi, "ultima_actualizacion_rssi": tiempo_actual}})
    elif busqueda["Ubicacion"] == ubicacion and int(rssi) >= int(busqueda["RSSI"]):
        collection.update_one({"_id": busqueda["_id"]}, {"$set": {"RSSI": rssi, "ultima_actualizacion_rssi": tiempo_actual}})

def ubicacion_usuario (nombre):
    busqueda = collection.find_one({"Nombre": nombre})
    print(busqueda["Ubicacion"])
    return busqueda["Ubicacion"]


def loop_serial (puerto = '/dev/ttyACM0', baudrate = 115200):
    ser = Serial (puerto, baudrate)
    ser.flushInput ()

    

    try:
        
        while True:


            line = ser.readline ().decode ().strip ()
            string_in = line.find ("-m ") + line.find ("-p ") + 1;
            line = line [string_in:]
            line_split = line.split (" ")


            # Formato del mensaje
            # Si es una nueva conexion al sistema: 0
            # Si es un mensaje entre usuarios: 1
            # Para atualizar las raspys de las MAC con su alias: 2

            # "-p 11:11:11:11 en la 0x0026 -70"

            if line_split [0] == "-p":
                print ("Actualizando conexion")
                print(line_split [1], line_split [-2], line_split [-1])
                actualizar_usuarios (line_split [1], line_split [-2], line_split [-1])

            # "1 marcos ven a sala 3"
            elif line_split [0] == "-m":
                print ("Reenviando aviso")
                print(line)
                ubicacion = ubicacion_usuario (line_split [1])
                if ubicacion:
                    print (f"El mensaje va para {line_split [1]} en la direccion {ubicacion}")
                    envio = f"chat private {ubicacion} '{line [2:]}' \n"
                    ser.write (envio.encode ())

                else:
                    print (f"No se encontró la ubicación para {line_split [1]}")
            


    except KeyboardInterrupt:
        print ("Cerrando serial")
        ser.close ()
        exit
    



if __name__ == "__main__":
    limpieza_thread = threading.Thread(target=añadeTimeStamp)
    limpieza_thread.daemon = True
    limpieza_thread.start()
    loop_serial ()

    #ser = Serial ('/dev/ttyACM0', 115200)
    #ser.flushInput ()
    #envio = f"chat private 0x0026 'carlos ven a sala 3' \n"
    #ser.write (envio.encode ())
    #ser.close ()
    #exit
