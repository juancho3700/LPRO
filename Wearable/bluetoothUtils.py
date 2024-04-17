from email import message
import threading
import bluetooth 
import socket


class BluetoothUtil:

    def __init__ (self):

        self.macList = ["B8:27:EB:FE:18:12", "58:20:71:83:84:9B"]
        self.addr = ""


    def inquiry (self):

        nearbyDevices = bluetooth.discover_devices (duration = 4, lookup_names = True, flush_cache = True, lookup_class = False)
        print ("%d devices detected" % len (nearbyDevices))

        for addr, name in nearbyDevices:
            print("  %s --- %s" % (addr, name))

            if addr in self.macList:
                self.addr = addr
                return

        self.addr = ""
        return


    def connection (self, text):

        client = socket.socket (socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
        client.connect ((self.addr, 4))
        client.send (input (text).encode ("utf-8"))
        client.close ()


    def inquiry_thread (self):

        self.addr = ""
        thread = threading.Thread (target = self.inquiry)
        thread.start ()
        return thread



if __name__ == "__main__":

    bl = BluetoothUtil ()
    addr = ""

    while not bl.addr:

        bl.inquiry ()

    client = bl.connection ("Hola que tal")
