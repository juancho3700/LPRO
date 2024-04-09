import wave

class saveFiles:

    @staticmethod
    def save_wav (audio, frames, archivo, canales, formato, rate):

        with wave.open (archivo, "wb") as file:

            file.setnchannels (canales)
            file.setsampwidth (audio.get_sample_size (formato))
            file.setframerate (rate)

            file.writeframes (b''.join (frames))

    
    @staticmethod
    def save_txt (texto, archivo):
        
        with open (archivo, "w") as file:
            file.write (texto)