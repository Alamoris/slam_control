import random
import math

import PyQt5

from robots import Robot
from my_modules import reversedRange, dejkstraAlg, takeWay, normalizeDejkstraValues, wayDecoder


class SlamBrain():
    def __init__(self):
        self.not_taked = []
        self.booked = []
        self.progressed = []
        self.passed_connections = []

    def iniData(self, points, connections, first_point, robots):
        if not robots:
            robots = 1
        self.first_point = first_point
        self.points = points
        self.points = [(x.x(), x.y()) for x in self.points]
        self.connections = connections
        self.robots = [Robot((first_point.x(), first_point.y())) for x in range(int(robots))]

    def moveToNextStep(self, robot):
        first_x, first_y, fin_x, fin_y = robot.paintngStep()

        if first_x is True:
            if not self.not_taked and\
                    not self.booked and\
                    not self.progressed:
                print("Hurray your quest is complite")

            self.takeNewTask((fin_x, fin_y), robot)
            robot.pos_length = 0
            return fin_x, fin_y, fin_x, fin_y

        return first_x, first_y, fin_x, fin_y

    # Возврящает все точки соединенные с данной
    def checkForNewConnections(self, point):
        new_connections = []
        for i in self.connections:
            if self.points[i[0]] == point:
                if i not in self.passed_connections and \
                        i not in self.booked and \
                        i not in self.progressed and \
                        i not in self.not_taked:
                    self.not_taked.append(i)


        return new_connections

    def checkForAvailableConnections(self, point):
        available_connections = []
        point_index = self.points.index(point)
        for x in self.not_taked:
            if x[0] == point_index:
                available_connections.append(x)
        return available_connections

    def pointCheked(self, point):
        # Проверка, находится ли точка в пройденных точках, если не находится, добавляем ее туда
        if point not in self.passed_connections:
            for i in self.connections:
                if i[1] == self.points.index(point):
                    self.passed_connections.append(i)

        point_index = self.points.index(point)
        # Проверка, находится ли точка в массиве обрабатываемых точек, если да, убираем ее оттуда
        if point_index in self.progressed:
            self.progressed.remove(point_index)

        for x in self.booked:
            if point_index == x[1]:
                self.booked.remove(x)

    def takeNewTask(self, point, robot):
        # TODO: Новая функция управления описание в qt_slam

        # TODO: Сделать функцию, которая будет возвращать всех роботов в первую точку(или в точку, которую указали), после того, как будут исследованы все соединения
        self.pointCheked(point)

        if robot.mission:
            # TODO: Проверять на каждом прохождении точки проверять миссии остальных роботов, если есть робот который
            # TODO: идет в эту точку округлять значение положения робота и изменить его движение к самой ближней точке
            new_point = self.points[robot.mission.pop()]
            robot.pos_connection = [robot.pos_connection[1], new_point]
            self.progressed.append((robot.pos_connection[1], new_point))
        else:
            # Считаю сколько свободных роботов находится в этой точке в данный момент
            robots_in_point = []
            for i in range(len(self.robots)):
                if self.robots[i].pos_connection[1] == point:
                    robots_in_point.append(i)

            # Присваивание новых заданий для роботов в входящей точке, в условиях, что свободных роботов меньше чем
            # доступных соединений, роботов столько же сколько соединений и роботов больше чем соединений
            self.checkForNewConnections(point)

            connections = self.checkForAvailableConnections(point)

            if connections:
                # TODO: Переделать функцию на управление одним роботом и проверить на работу, если роботов больше, чем соединений в точке
                print('teke newt liner connection')
                self.haveLinerConnections(connections, robots_in_point)
            else:
                print('have not new liner connections')

                all_known_cons = self.passed_connections + self.not_taked
                point_index = self.points.index(point)

                if not self.not_taked and self.booked:
                    all_known_cons += self.booked

                dejkstra_cons, normalize_dict, decode_dict = normalizeDejkstraValues(all_known_cons)
                vektor_way = dejkstraAlg([], dejkstra_cons, normalize_dict[point_index])

                if not self.not_taked and self.booked:
                    # Для правильного построения миссии нового робота требуется в переменную all_known_cons добавить
                    # значения booked потому что они тоже являются частью изученой карты

                    rand_way = random.randrange(len(self.booked))
                    rand_way = self.booked[rand_way]

                    new_mission = takeWay(normalize_dict[point_index], normalize_dict[rand_way[1]], vektor_way)
                    new_mission = wayDecoder(new_mission, decode_dict)

                    next_connection = [new_mission.pop(), new_mission.pop()]
                else:
                    min_way_lenght = 999
                    new_mission = []
                    for i in self.not_taked:
                        way = takeWay(normalize_dict[point_index], normalize_dict[i[1]], vektor_way)
                        way = wayDecoder(way, decode_dict)
                        if len(way) < min_way_lenght:
                            min_way_lenght = len(way)
                            new_mission = way

                    self.not_taked.remove((new_mission[1], new_mission[0]))
                    self.booked.append((new_mission[1], new_mission[0]))

                    next_connection = [new_mission.pop(), new_mission.pop()]

                    self.progressed.append(next_connection[1])

                next_connection = [self.points[next_connection[0]], self.points[next_connection[1]]]
                robot.mission = new_mission
                robot.pos_connection = next_connection

    def haveLinerConnections(self, connections, robots_in_point):
        next_points = set()
        while len(next_points) < len(robots_in_point):
            next_points.add(random.randrange(len(connections)))

        next_connection = (0, 0)
        if len(robots_in_point) <= len(connections):
            for i in robots_in_point:
                next_connection = next_points.pop()
                next_connection = connections[next_connection]
                self.robots[i].pos_connection = [self.points[next_connection[0]],
                                                 self.points[next_connection[1]]]

                self.not_taked.remove(next_connection)

        else:
            numbers_of_free_robots = len(robots_in_point)
            for x in reversedRange(len(connections)):
                nums_robots = math.ceil(numbers_of_free_robots / x)
                numbers_of_free_robots -= nums_robots

                next_connection = connections.pop()
                for i in range(int(nums_robots)):
                    robot_number = robots_in_point.pop()
                    self.robots[robot_number].pos_connection = [self.points[next_connection[0]],
                                                                self.points[next_connection[1]]]

                self.not_taked.remove(next_connection)

        self.progressed.append(next_connection[1])


    def returnToBase(self):
        for robot in self.robots:
            cur_point = self.points.index(robot.pos_connection[1])
            dejkstra_cons, normalize_dict, decode_dict = normalizeDejkstraValues(self.not_taked)
            vektor_way = dejkstraAlg([], dejkstra_cons, normalize_dict[cur_point])

            if robot.pos_length > 0:
                robot.pos_connection.reverse()

            base_way = takeWay(normalize_dict[cur_point], normalize_dict[0], vektor_way)
            way = wayDecoder(base_way, decode_dict)

            way.pop()
            way.pop()

            robot.mission = way