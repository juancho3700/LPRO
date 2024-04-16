from email import message
import socket

client=socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)

client.connect(("B8:27:EB:FE:18:12",4))  # esta MAC sae de hcitool dev para coller a MAC en concreto
#client.connect(("FF:FF:FF:FF:FF:FF",4))  # esta MAC sae de hcitool dev para coller a MAC en concreto

print("Cliente conectado...")

try:
    while True:
        data = input("Manda algo")
        client.send(data.encode("utf-8"))
       # if not data:
       #     break
except OSError as e:
 pass
client.close()
