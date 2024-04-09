import speech_recognition as sr

class STT:

    @staticmethod
    def speechToText (archivo):

        reconocedor = sr.Recognizer ()

        with sr.AudioFile (archivo) as fuente:
            audio = reconocedor.record (fuente)

            try:
                texto = reconocedor.recognize_google (audio, language = 'es-ES')
                return texto

            except sr.UnknownValueError:
                raise ValueError ("No se pudo entender el audio")

            except sr.RequestError as e:
                raise RequestError ("Error en la solicitud a Google Speech Recognition service; {0}".format(e))
