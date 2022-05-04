from time import sleep
import serial
# these codes are for virtual car (debug without car)
# hint: please check the function "sleep". how does it work?

class virtual_car:
    def __init__(self):
        self.ser = serial.Serial()

    def SerialWrite(self,output):
        # send = 's'.encode("utf-8")
        send = output.encode("utf-8")
        self.ser.write(send)

    def SerialReadString(self):
        # TODO: Get the information from Bluetooth. Notice that the return type should be transformed into hex.
        waiting = self.ser.in_waiting
        if waiting >= 0:
            rv = self.ser.read(1).decode("utf-8") 
            return rv
        return ""
    # confront a node: 0
    # scan a RFID: 1 + UID code

    def SerialReadByte(self):
        sleep(0.05)
        waiting = self.ser.inWaiting()
        rv = self.ser.read(waiting)
        if(rv):
            UID = hex(int.from_bytes(rv, byteorder='big', signed=False))
            self.ser.flushInput()
            return UID
        else:
            return 0


