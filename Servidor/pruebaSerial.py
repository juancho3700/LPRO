from xml.etree.ElementInclude import FatalIncludeError
import serial
#import self
import time
import csv
import re


def actualizar_usuario(nombre, ubicacion):
    with open('usuarios_conectados.csv', 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        rows = list(reader)

    usuario_encontrado = False
    
    # Comprueba si es necesario actualizar la ubicacion o si no es necesario actualizar nada
    for row in rows:
        if row['Nombre'] == nombre:
            if row['Ubicacion'] == ubicacion:
                print(f"La ubicación de {nombre} ya está actualizada")
            else:
                row['Ubicacion'] = ubicacion
                usuario_encontrado = True
            break
        
    #Si no existe el usuario, lo añade al sistema
    if not usuario_encontrado:
        rows.append({'Nombre': nombre, 'Ubicacion': ubicacion})

    with open('usuarios_conectados.csv', 'w', newline='') as csvfile:
        fieldnames = ['Nombre', 'Ubicacion']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    

def obtener_ubicacion_usuario(nombre):
    with open('usuarios_conectados.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['Nombre'] == nombre:
                return row['Ubicacion']
    return None

def enviar_a_ttyACM0(cadena, puerto='/dev/ttyACM0', baudios=115200):
    try:
        ser = serial.Serial(port=puerto, baudrate=baudios, timeout=1)
        print("Conexión establecida con", puerto)
        ser.write(cadena.encode())
        print("Cadena enviada:", cadena)
        time.sleep(5)
        ser.close()
        print("Conexión cerrada")
    except Exception as e:
        print("Error:", e)

    #try:
    #   self._port = serial.serial_for_url(puerto)
    #except Exception as e:
    #    print("Error:", e)

def recibe_por_ttyACM0(puerto='/dev/ttyACM0', baudios=115200):
    ser = serial.Serial(port=puerto, baudrate=baudios, timeout=1)
    try:
        print("Conexión establecida con", puerto)

        while True:
            line = ser.readline().decode().strip()
            print("Recibido:", line)
            
            indice_inicio_1 = line.find("1 ")
            indice_inicio_0 = line.find("0 ")
            
            if indice_inicio_1 != -1:
                indice_inicio = indice_inicio_1
            elif indice_inicio_0 != -1:
                indice_inicio = indice_inicio_0
            else:
                indice_inicio = -1

            if indice_inicio != -1:
                parte_deseada = line[indice_inicio:]
                line = parte_deseada
            else:
                print("No se encontró el patrón en la frase.")
            
            
            print("mensaje cambiado " + line)
            
            # Formato del mensaje 
            # Si es una nueva conexion al sistema: 0
            # Si es un mensaje entre usuarios: 1
            # Si es una emergencia y se avisa a todos: 2
            
            # MENSAJE PARA PROBAR 0 : 0 carlos en la {direcion unicast}
            if line.startswith('0'):
                print("Conexion") 
                partes = line.split(' ')
                nombre_usuario = partes[1]
                ubicacion = partes[4]
                actualizar_usuario(nombre_usuario, ubicacion)
                print(f"Se actualizó la ubicación de {nombre_usuario} a {ubicacion}")
                    
            # MENSAJE PARA PROBAR 1 : 1 carlos a sala 3
            elif line.startswith('1'):
                print("Mensaje")
                partes = line.split(' ')
                nombre_destinatario = partes[1]
                ubicacion = obtener_ubicacion_usuario(nombre_destinatario)
                if ubicacion:
                    print(f"El mensaje está dirigido a {nombre_destinatario} en {ubicacion}")
                    cadena = f"chat private {ubicacion} '{line}' \n"
                    enviar_a_ttyACM0(cadena)
                else:
                    print(
                        f"No se encontró la ubicación para {nombre_destinatario}")
            else:
                #print("Formato no reconocido")
                None
                 

    except KeyboardInterrupt:
        print("Cerrando conexión serial...")
        ser.close()
    

recibe_por_ttyACM0()