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
    maze = mz.Maze("data/maze_8x6_3.csv")
    interf = interface.interface()
    input("Press enter to start.")
    point = score.Scoreboard("data/UID.csv", "得分王者")
    interf.ser.SerialWrite('s') # s:開始循跡
    
    # TODO : Initialize necessary variables

    if (sys.argv[1] == '0'):
        print("Mode 0: for treasure-hunting")
        # TODO : for treasure-hunting, which encourages you to hunt as many scores as possible
        route = maze.BFS_overall(1)
        cmd = maze.route_to_cmd(route)
        interf.ser.SerialWrite(cmd+'e')
        print(cmd)
        while True:
            interf.ser.EndlessReadUID(point)
            
        
    elif (sys.argv[1] == '1'):
        print("Mode 1: Self-testing mode.")
        # TODO: You can write your code to test specific function.
        route, D = maze.BFS_2(1, 48)
        print(route, D)
        route, D = maze.BFS_2(3, 45)
        print(route, D)
        route, D = maze.BFS_2(6, 43)
        print(route, D)
    
    elif (sys.argv[1] == '2'):
        print("Mode 2: BFS_overall")
        # TODO: You can write your code to test specific function.

        route = maze.BFS_overall(1)
        print(route)
        cmd = maze.route_to_cmd(route)
        print(cmd, len(cmd))

if __name__ == '__main__':
    main()

# socat -d -d pty,raw,echo=0 pty,raw,echo=0 