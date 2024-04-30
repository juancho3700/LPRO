import csv
import socket
import asyncio
import bluetooth
import threading
from serial import Serial
import subprocess
import os
from inquiry_with_rssi import inquiry_rssi
import time

eventMensaxe = threading.Event()


class boxpeak_C1(object):

    #   VARIABLES

    def __init__(self):
        print("Innit a boxpeakC1")
        subprocess.run('sudo hciconfig hci0 piscan', shell=True,
                       check=True, capture_output=False, encoding='utf-8')
        self.puertoSerie = '/dev/ttyACM0'
        self.ser = Serial(self.puertoSerie, 115200)
        self.nombre_archivo = "usuarios.csv"
        self.numeroPlaca = "0x0027"
        self.inquiry = inquiry_rssi()
        self.mac = ""
        self.get_MAC()

    def get_MAC(self):
        p = (subprocess.run('hcitool dev', shell=True, check=True, capture_output=True,
             encoding='utf-8'))      # con esto sacas a MAC propia, só quedaria procesala
        lines = p.stdout.splitlines()
        self.mac = lines[1][lines[1].find("hci0") + 4:].strip()

    def peer_server(self):
        server = socket.socket(socket.AF_BLUETOOTH,
                               socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
        # esta MAC sae de hcitool dev para coller a MAC en concreto
        server.bind((self.mac, 4))
        print("Server escoitando...")

        server.listen(1)   # 1 nº de conexions
        # global eventMensaxe()
        #

        while True:
            client, addr = server.accept()  # en BL este client é a nosa interfaz
            print("Cliente conectado + "+str(addr))

            try:
                #
                while True:  # quitao' para que só faga unha interaccion
                    data = client.recv(1024).decode('utf-8')
                    print("Mensaje recibido")
                    print("Message: "+data+" from: "+str(addr))
                    nuevo = f"chat private 0x0025 '-m {data}'\n"
                    self.ser.write(nuevo.encode())
                    # self.envio(data.decode())

            except Exception as e:
                print("Me abandonaron :(")
                client.close()
                continue

        # server.close()
        # global eventMensaxe
       # eventMensaxe.set()

    def reproducirCadena(self, cadena):
        festival_process = subprocess.Popen(
            ['festival', '--tts', '--language', 'spanish'], stdin=subprocess.PIPE)
        festival_process.communicate(input=cadena.encode())

    def valor_existente(self, valor):
        with open(self.nombre_archivo, mode='r', newline='') as archivo_csv:
            lector_csv = csv.reader(archivo_csv)
            for fila in lector_csv:
                if fila[0] == valor:
                    return True
            return False

    def loop_serial(self):
        self.ser.flushInput()

        try:

            while True:
                line = self.ser.readline().decode().strip()
                print("Recibido " + line)
                string_in = line.find("-t ") + line.find("-n ") + 1
                line = line[string_in:]
                line_split = line.split(" ")
                line_t = line.split("-t ")

                if line_split[0] == "-n":
                    print("Actualizo usuarios que puedo conectarme")
                    print(line_split[1])
                    if not self.valor_existente(line_split[1]):
                        with open(self.nombre_archivo, mode='a', newline='') as archivo_csv:
                            escritor_csv = csv.writer(archivo_csv)
                            escritor_csv.writerow([line_split[1]])
                            archivo_csv.close()

                elif line_split[0] == "-t":

                    print("Recibido aviso, reproduciendo")
                    line = line_t[1]
                    # string_in = line.find ("-t ") +1
                    print(line)
                    # line = line [string_in:]

                    self.reproducirCadena(line)

        except KeyboardInterrupt:
            print("Cerrando serial")
            self.ser.close()
            exit

    def inquiry_thread(self):

        while True:
            lista = self.inquiry.device_inquiry_with_with_rssi()
            print(*lista, sep="\n")

            for addr, rssi in lista:
                if (self.valor_existente(addr)):
                    nuevo = f"chat private 0x0025 '-p {addr} en la {self.numeroPlaca} {rssi}'\n"
                    self.ser.write(nuevo.encode())
                    print(nuevo)
            # time.sleep(5)


if __name__ == "__main__":
    c1 = boxpeak_C1()
    c1_thread = threading.Thread(target=c1.inquiry_thread)
    c1_thread.start()
    c1_textSpeech = threading.Thread(target=c1.loop_serial)
    c1_textSpeech.daemon = True
    c1_textSpeech.start()
    c1.peer_server()
