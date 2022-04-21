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
    maze = mz.Maze("data/medium_maze.csv")
    point = score.Scoreboard("data/UID.csv", "得分王者")
    interf = interface.interface()
    # TODO : Initialize necessary variables

    if (sys.argv[1] == '0'):
        print("Mode 0: for treasure-hunting")
        # TODO : for treasure-hunting, which encourages you to hunt as many scores as possible
        route = maze.BFS_2(7, 12)
        cmd = maze.route_to_cmd(route)
        interf.ser.SerialWrite(cmd+'e')
        print(route)
        print(cmd)
        while True:
            interf.ser.EndlessReadUID(point)
            
        
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

        readThread = threading.Thread(target=interf.ser.EndlessReadUID(point, interf))
        readThread.daemon = True
        readThread.start()
        interf.ser.SerialWrite("rbfblbfbe")
    
    elif (sys.argv[1] == '3'):
        print("Mode 3: BFS mode.")
        # TODO: You can write your code to test specific function.
        route = maze.BFS_2(13, 26)
        print(route)
        cmd = maze.route_to_cmd(route)
        print(cmd)



if __name__ == '__main__':
    main()

# socat -d -d pty,raw,echo=0 pty,raw,echo=0 