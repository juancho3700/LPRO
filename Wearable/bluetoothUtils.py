from email import message
from bluetooth import discover_devices
import socket


class BluetoothUtil:

    macList = []

    def inquiry (self, message):

        nearbyDevices = discover_devices (duration = 4, lookup_names = True, flush_cache = True, lookup_class = False)

        for addr, name in nearby_devices:
            print("  %s" % (addr))

            if addr in macList:
                self.connection (addr, message)
                return



    def connection (self, addr, message):

        client = socket.socket (socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
        client.connect ((addr, 4))

        print ("Cliente conectado...")

        try:
            while True:
                data = input (message)
                client.send (data.encode ("utf-8"))

        except OSError as e:
            pass

        client.close ()


if __name__ == "__main__":

    bl = BluetoothUtil ()
    bl.inquiry ("Hola que tal")