import BT
import virtual_car
import maze
import score

# hint: You may design additional functions to execute the input command, which will be helpful when debugging :)

class interface:
    def __init__(self):
        print("")
        print("Arduino Bluetooth Connect Program.")
        print("")
        self.ser = BT.bluetooth()
        port = input("PC bluetooth port name: ")
        while(not self.ser.do_connect(port)):
            if(port == "quit"):
                self.ser.disconnect()
                quit()
            port = input("PC bluetooth port name: ")
        input("Press enter to start.")
        self.ser.SerialWrite('s') # s:開始循跡

    def get_UID(self):
        return self.ser.SerialReadByte()

    def send_action(self,dirc):
        # TODO : send the action to car
        return

    def end_process(self):
        self.ser.SerialWrite('e') # e: end of task
        self.ser.disconnect()