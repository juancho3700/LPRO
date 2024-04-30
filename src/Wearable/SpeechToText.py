import speech_recognition as sr
import vosk
import sys


class STT:

    @staticmethod
    def speechToText(archivo):

        model_path = "/home/boxpeak/LPRO/Wearable/vosk-model"
        reconocedor = sr.Recognizer()

        with sr.AudioFile(archivo) as fuente:
            audio = reconocedor.record(fuente)

            try:
                recognizer = vosk.KaldiRecognizer(
                    vosk.Model(model_path), 40100)
                with open(archivo, "rb") as f:
                    audio_data = f.read()
                recognizer.AcceptWaveform(audio_data)
                result = recognizer.FinalResult()
                string_in = result.find(":") + 1
                result = result[string_in:]
                result = result.strip('"').rstrip('\n}')
                result = result[2:-1]
                return result

            except sr.UnknownValueError:
                raise ValueError("No se pudo entender el audio")
