from node import *
import maze as mz
import score
import interface
import time
from score import Scoreboard

import numpy as np
import pandas
import time
import sys
import os
import threading

def main():
    maze = mz.Maze("data/maze.csv")
    point = score.Scoreboard("data/UID.csv", "team_NTUEE")
    interf = interface.interface()
    # TODO : Initialize necessary variables

    if (sys.argv[1] == '0'):
        print("Mode 0: for treasure-hunting")
        # TODO : for treasure-hunting, which encourages you to hunt as many scores as possible
        
    elif (sys.argv[1] == '1'):
        print("Mode 1: Self-testing mode.")
        # TODO: You can write your code to test specific function.
        route = maze.BFS_2(31, 41)
        print(route)
        cmd = maze.route_to_cmd(route)
        print(cmd)
    
    elif (sys.argv[1] == '2'):
        print("Mode 2: Car Checking")
        # TODO: You can write your code to test specific function.

        readThread = threading.Thread(target=interf.ser.EndlessReadUID)
        readThread.daemon = True
        readThread.start()
        interf.ser.SerialWrite("rbfblbfbe")
        while True:
            a = ''
            a = input()
            interf.ser.SerialWrite(a)
            if a == 'e':
                break
            if interf.ser.EndlessReadUID():
                point.add_UID(interf.ser.EndlessReadUID())
                print(point.getCurrentScore())

if __name__ == '__main__':
    main()

# socat -d -d pty,raw,echo=0 pty,raw,echo=0 