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


def save_wav (frames):
    with wave.open ("output.wav", "wb") as file:
        file.setnchannels (CHANNELS)
        file.setsampwidth (audio.get_sample_size (FORMAT))
        file.setframerate (RATE)
        file.writeframes (b''.join (frames))


if __name__ == "__main__":
    GPIO.setmode (GPIO.BCM)
    GPIO.setup (BUTTON_PIN, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    audio = pyaudio.PyAudio ()

    stream = audio.open (format=FORMAT,
                         channels=CHANNELS,
                         rate=RATE,
                         input=True,
                         frames_per_buffer=CHUNK)

    try:
        while True:
            GPIO.wait_for_edge (BUTTON_PIN, GPIO.FALLING)
            GPIO.wait_for_edge (BUTTON_PIN, GPIO.RISING)

            end = False
            frames = []

            print ("Empiezo a grabar")
            while not end:
                data = stream.read (CHUNK, exception_on_overflow = False)
                frames.append (data)
                if GPIO.input (BUTTON_PIN) == GPIO.LOW: end = True

            print ("Guardo el archivo\n\n")
            save_wav (frames)

    except KeyboardInterrupt:
        GPIO.cleanup ()
        exit (0)