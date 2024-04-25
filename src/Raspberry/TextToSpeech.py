 
from gtts import gTTS
from serial import Serial
import os


def reproducirCadena(cadena):

    # Crear un objeto gTTS
    tts = gTTS(text=cadena, lang='es')

    # Guardar el archivo de audio
    tts.save("output.mp3")

    # Reproducir el archivo de audio
    os.system("mpg123 output.mp3")


def loop_serial (puerto = '/dev/ttyACM0', baudrate = 115200):
    ser = Serial (puerto, baudrate)
    ser.flushInput ()

    try:
        while True:
            line = ser.readline ().decode ().strip ()
            string_in = line.find ("* ") +1 
            line = line [string_in:]
            reproducirCadena(line)

    except KeyboardInterrupt:
        print ("Cerrando serial")
        ser.close ()
        exit

if __name__ == "__main__":
    loop_serial ()
    #reproducirCadena("hola")
