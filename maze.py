from node import *
import numpy as np
import csv
import pandas
from enum import IntEnum
import math
import node


class Action(IntEnum):
    ADVANCE = 1
    U_TURN = 2
    TURN_RIGHT = 3
    TURN_LEFT = 4
    HALT = 5


class Maze:
    def __init__(self, filepath):
        self.raw_data = pandas.read_csv(filepath).values
        self.nodes = []
        self.nd_dict = dict()  # key: index, value: the correspond node
        for row in self.raw_data:
            self.nd_dict[int(row[0])] = node.Node(row)

    def getStartPoint(self):
        if (len(self.nd_dict) < 2):
            print("Error: the start point is not included.")
            return 0
        return self.nd_dict[1]

    def getNodeDict(self):
        return self.nd_dict

    def BFS(self, nd):
        # Tips : return a sequence of nodes from the node to the nearest unexplored deadend
        visited = []
        queue = []
        routeR = []

        visited.append(self.nd_dict[nd].index)
        queue.append(self.nd_dict[nd].index)
        start = 0

        while queue:
            s = queue.pop(0) 
            if self.nd_dict[s].isTerminal() and start == 1:
                routeR.append(s)
                while self.nd_dict[s].Successors[0] != -1:
                    routeR.append(self.nd_dict[s].Successors[0])
                    s = self.nd_dict[s].Successors[0]
                route = [r for r in reversed(routeR)]
                return route

            start = 1

            for adjacent in self.nd_dict[s].neighbors: #find all adjacent node
                if (adjacent not in visited) and (adjacent != -1):
                    self.nd_dict[adjacent].Successors[0] = s
                    visited.append(adjacent)
                    queue.append(adjacent)

    def BFS_2(self, nd_from, nd_to):
        # Tips : return a sequence of nodes of the shortest path
        visited = []
        queue = []
        routeR = []

        visited.append(self.nd_dict[nd_from].index)
        queue.append(self.nd_dict[nd_from].index)

        for N in self.nd_dict:
            self.nd_dict[N].Successors = [-1]

        while queue:
            s = queue.pop(0) 
            if s == nd_to:
                routeR.append(s)
                while self.nd_dict[s].Successors[0] != -1:
                    routeR.append(self.nd_dict[s].Successors[0])
                    s = self.nd_dict[s].Successors[0]
                route = [r for r in reversed(routeR)]
                return route

            start = 1

            for adjacent in self.nd_dict[s].neighbors: #find all adjacent node
                if (adjacent not in visited) and (adjacent != -1):
                    self.nd_dict[adjacent].Successors[0] = s
                    visited.append(adjacent)
                    queue.append(adjacent)
        
    def BFS_overall(self, nd):
        #step0: initialize termi as terminal and start node
        termi = [nd]
        for N in self.nd_dict:
            if self.nd_dict[N].isTerminal() and N != nd:
                termi.append(N)
        
        #step1: get the distance from terminal to terminal
        distance = []
        for i in range(len(termi)):
            distance.append([])
            for j in range(len(termi)):
                if j < i:
                    distance[i].append(distance[j][i])
                if i == j:
                    distance[i].append(0)
                if i < j:
                    a = self.BFS_2(termi[i], termi[j])
                    length = len(a) - 1
                    distance[i].append(length)
        
        #step2: get the possible route
        list = self.routelist(len(termi)-1).copy()

        #step3: evaluate the route one by one
        short, shortD = [], 1000
        for l in list:
            l.insert(0, 0)
            D = 0
            for i in range(len(termi)-1):
                D += distance[l[i]][l[i+1]]
            if shortD > D:
                short = l.copy()
                shortD = D

        #step4: reconstruct the selected route(to save memory)
        route = [nd]
        for i in range(len(short)-1):
            frag = self.BFS_2(termi[short[i]], termi[short[i+1]])
            frag.pop(0)
            route.extend(frag.copy())
        return route

    def routelist(self, total, list = [], current = []):
        if len(current) == total:
            list.append(current.copy())
            return list
        for i in range(1, total+1):
            in_it = False
            for j in current:
                if i == j:
                    in_it = True
                    break
            if in_it == False:
                current.append(i)
                list = self.routelist(total, list, current).copy()
                current.remove(i)
        return list

    def getAction(self, car_dir, nd_from, nd_to):
        # TODO : get the car action
        # Tips : return an action and the next direction of the car if the nd_to is the Successor of nd_to
		# If not, print error message and return 0
        return None

    def strategy(self, nd):
        return self.BFS(nd)

    def strategy_2(self, nd_from, nd_to):
        return self.BFS_2(nd_from, nd_to)
