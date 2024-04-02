from serial import Serial
from time import sleep
import csv


def actualizar_usuarios (nombre, ubicacion):
    with open ('usuarios_conectados.csv', 'r', newline = '') as csvfile:
        reader = csv.DictReader (csvfile)
        rows = list (reader)

    usuario_encontrado = False

    # Comprueba si es necesario actualizar la ubicacion o si no es necesario actualizar nada
    for row in rows:
        if row ['Nombre'] == nombre:
            if row ['Ubicacion'] != ubicacion:
                row ['Ubicacion'] = ubicacion
                usuario_encontrado = True
            
            else:
                return
            
            break

    # Si no existe el usuario, lo añade al sistema
    if not usuario_encontrado:
        rows.append ({'Nombre': nombre, 'Ubicacion': ubicacion})
        
    with open ('usuarios_conectados.csv', 'w', newline = '') as csvfile:
        fieldnames = ['Nombre', 'Ubicacion']
        writer = csv.DictWriter (csvfile, fieldnames = fieldnames)
        writer.writeheader ()
        writer.writerows (rows)
    

def ubicacion_usuario (nombre):
    with open ('usuarios_conectados.csv', newline = '') as csvfile:
        reader = csv.DictReader (csvfile)
        for row in reader:
            if row ['Nombre'] == nombre:
                return row ['Ubicacion']
    return None


def loop_serial (puerto = '/dev/ttyACM0', baudrate = 115200):
    ser = Serial (puerto, baudrate)
    ser.flushInput ()

    try:
        while True:

            line = ser.readline ().decode ().strip ()
            string_in = line.find ("1 ") + line.find ("0 ") + 1;
            line = line [string_in:]
            line_split = line.split (" ")


            # Formato del mensaje
            # Si es una nueva conexion al sistema: 0
            # Si es un mensaje entre usuarios: 1
            # Si es una emergencia y se avisa a todos: 2

            if line_split [0] == "0":
                print ("Actualizando conexion")
                actualizar_usuarios (line_split [1], line_split [-1])

            elif line_split [0] == "1":
                print ("Reenviando aviso")

                ubicacion = ubicacion_usuario (line_split [1])
                if ubicacion:
                    print (f"El mensaje va para {line_split [1]} en la direccion {ubicacion}")
                    envio = f"chat private {ubicacion} '{line [2:]}' \n"
                    ser.write (envio.encode ())

                else:
                    print (f"No se encontró la ubicación para {line_split [1]}")

            print ("")

    except KeyboardInterrupt:
        print ("Cerrando serial")
        ser.close ()
        exit
    



if __name__ == "__main__":
    loop_serial ()