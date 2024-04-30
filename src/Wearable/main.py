from saveFiles import saveFiles
from SpeechToText import STT
from bluetoothUtils import BluetoothUtil
import subprocess
import wave
import threading
import RPi.GPIO as GPIO
from sys import exit

import pyaudio


BUTTON_PIN = 16
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 48000

WAV_FILE = "recorded.wav"
TEXT_FILE = "converted.txt"


def main():
    subprocess.run('sudo hciconfig hci0 piscan', shell=True,
                   check=True, capture_output=False, encoding='utf-8')
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    bl = BluetoothUtil()
    stt = STT()

    try:
        while True:

            GPIO.wait_for_edge(BUTTON_PIN, GPIO.FALLING)
            GPIO.wait_for_edge(BUTTON_PIN, GPIO.RISING)

            thread = bl.inquiry_thread()

            audio = pyaudio.PyAudio()
            stream = audio.open(format=FORMAT,
                                channels=CHANNELS,
                                rate=RATE,
                                input=True,
                                frames_per_buffer=CHUNK)

            wav_file = wave.open(WAV_FILE, "wb")
            wav_file.setnchannels(CHANNELS)
            wav_file.setsampwidth(audio.get_sample_size(FORMAT))
            wav_file.setframerate(RATE)

            end = False

            print("Empiezo a grabar")
            while not end:
                audio_data = stream.read(CHUNK)
                wav_file.writeframes(audio_data)
                if GPIO.input(BUTTON_PIN) == GPIO.LOW:
                    end = True

            wav_file.close()
            stream.close()
            audio.terminate()

            print("Audio a texto y guardo\n\n")
            text = stt.speechToText(WAV_FILE)
            print(text)

            thread.join()

            print("Recibi %s. Enviando ..." % text)
            bl.connection(text)

    except KeyboardInterrupt:
        GPIO.cleanup()
        exit(0)


if __name__ == "__main__":
    main()
