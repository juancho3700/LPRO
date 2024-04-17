from saveFiles import saveFiles
from SpeechToText import STT
from bluetoothUtils import BluetoothUtil

import RPi.GPIO as GPIO
from sys import exit

import pyaudio
import struct
import wave


BUTTON_PIN = 16
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

WAV_FILE = "recorded.wav"
TEXT_FILE = "converted.txt"


def main ():
    GPIO.setmode (GPIO.BCM)
    GPIO.setup (BUTTON_PIN, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    audio = pyaudio.PyAudio ()
    bl = BluetoothUtil ()

    stream = audio.open (format = FORMAT,
                         channels = CHANNELS,
                         rate = RATE,
                         input = True,
                         frames_per_buffer = CHUNK)

    try:
        while True:
            GPIO.wait_for_edge (BUTTON_PIN, GPIO.FALLING)
            GPIO.wait_for_edge (BUTTON_PIN, GPIO.RISING)

            thread = bl.inquiry_thread ()

            end = False
            frames = []

            print ("Empiezo a grabar")
            while not end:
                data = stream.read (CHUNK, exception_on_overflow = False)
                frames.append (data)
                if GPIO.input (BUTTON_PIN) == GPIO.LOW: end = True

            print ("Guardo el archivo wav")
            saveFiles.save_wav (audio, frames, WAV_FILE, CHANNELS, FORMAT, RATE)

            print ("Audio a texto y guardo\n\n")
            text = STT.speechToText (WAV_FILE)
            saveFiles.save_txt (text, TEXT_FILE)

            thread.join ()
            
            while not bl.addr:
                bl.inquiry ()

            print ("Recibi %s. Enviando ..." % text)
            bl.connection (text)
            



    except KeyboardInterrupt:
        GPIO.cleanup ()
        exit (0)


if __name__ == "__main__":
    main ()