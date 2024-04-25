from email import message
import threading
import bluetooth 
import socket


class BluetoothUtil:

    def __init__ (self):

        #self.macList = []
        self.macList = ["E4:5F:01:E1:D3:A5"]
        self.addr = ""


    def inquiry (self):

        while True:
            nearbyDevices = bluetooth.discover_devices (duration = 4, lookup_names = False, flush_cache = False, lookup_class = False)
            print ("%d devices detected" % len (nearbyDevices))

            for addr in nearbyDevices:
                print("  %s " % (addr))

                if addr in self.macList:
                    self.addr = addr
                    return



    def connection (self, text):

        client = socket.socket (socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
        client.connect ((self.addr, 4))
        print("Me he conectado")
        client.send (input (str(text).encode ("utf-8")))
        print("termine")
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
