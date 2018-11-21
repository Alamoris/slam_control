import random
import math

import PyQt5

from robots Robot
from my_modules import reversedRange


class SlamBrain():
    def __init__(self):
        self.not_taked = []
        self.booked = []
        self.progressed = []
        self.passed_connections = []

    def iniData(self, points, connections, first_point, robots):
        self.first_point = first_point
        self.points = points
        self.connections = connections
        self.robots = [Robot(first_point) for x in range(robots)]

    def addNewConnections(self, point):
        for i in self.connections:
            if i[0] == point:
                if i not in self.passed_connections:
                    self.not_taked.append(i)

    # Функция достижения точки
    def passedPoint(self, con, length):
        for i in self.robots:
            if i.pos_connection == con:
                if i.pos_length == length:
                    self.passed_connections.append(con)
                    i.pos_connection = con[1]

    def takeNewTask(self, point):
        # Считаю сколько свободных роботов находится в этой точке в данный момент
        robots_in_point = []
        for i in range(len(self.robots)):
            if self.robots[i].pos_connection == point:
                robots_in_point.append(i)

        # Присваивание новых заданий для роботов в входящей точке, в условиях, что свободных роботов меньше чем
        # доступных соединений, роботов столько же сколько соединений и роботов больше чем соединений
        connections = self.checkConnections(point)

        next_points = set()
        while len(next_points) < len(robots_in_point):
            next_points.add(random.randrange(len(connections)))

        if len(robots_in_point) <= len(connections):

            for i in range(len(robots_in_point)):
                next_point = next_points.pop()
                next_point = connections[next_point]
                self.robots[robots_in_point[i]].pos_connection = (point, next_point)
                self.progressed.append((point, next_point))
                self.not_taked.remove((point, next_point))

        else:
            numbers_of_free_robots = len(robots_in_point)
            for x in reversGen(len(connections)):
                nums_robots = math.ceil(numbers_of_free_robots / x)
                for i 
                numbers_of_free_robots -= nums_robots





    def updateLength(self):
        ...

    # Получение массива с соседними вершинами графа относительно входящей точки
    def checkConnections(self, point):
        connections = []
        for x in self.connections:
            if x[0] == point:
                if x[1] not in self.passed_points:
                    connections.append(x[1])

        return connections

def reversGen(x):
    x -= 1
    while x >= 0:
        yield x
        x -= 1