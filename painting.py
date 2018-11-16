import sys, math

from PyQt5.QtWidgets import QWidget, QApplication, QFrame
from PyQt5.QtGui import QPen, QPainter, QColor
from PyQt5.QtCore import Qt, QPoint, QBasicTimer


class SearchingMap(QFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.initMain()

    def initMain(self):

        self.timer = QBasicTimer()
        self.iterat = 0
        self.setStyleSheet("border:3px solid rgb(0, 0, 0);")

    def initStartOptions(self, connections, points, robot_value, speed):
        if not speed:
            speed = 1
        self.timer.start(int(speed), self)
        self.robot_value = robot_value
        self.connections = connections
        self.points = points
        self.points = [(point.x(), point.y()) for point in self.points.copy()]
        self.painting_connections = []
        self.cur_map = []
        self.speed = 2

        self.takeStartConnections()

    def takeStartConnections(self):
        for con in self.connections:
            if con[0] == 0:
                self.painting_connections.append([self.connections.index(con), self.speed])

    def paintEvent(self, event):
        qp = QPainter(self)
        self.painttt(qp)

    def painttt(self, qp):
        pen = QPen(Qt.darkMagenta, 3)
        qp.setPen(pen)

        # Рисование пройденных ребер
        for x in self.cur_map:
            qp.drawLine(QPoint(self.points[x[0]][0], self.points[x[0]][1]),
                        QPoint(self.points[x[1]][0], self.points[x[1]][1]))

        # Основной цикл в котором дорисовывается следующий шаг и удаляются пройденные ребра
        for con in self.painting_connections.copy():
            con_index = self.painting_connections.index(con)
            new_x, new_y, length = self.calculate_next_point(self.points[self.connections[con[0]][0]][0],
                                                             self.points[self.connections[con[0]][0]][1],
                                                             self.points[self.connections[con[0]][1]][0],
                                                             self.points[self.connections[con[0]][1]][1],
                                                             con[1])

            self.painting_connections[con_index][1] = length

            # Костыль переворачивающий значение найденной точки, поскольку по формуле новая точка всегда направлена
            # в сторону увеличения y
            if self.points[self.connections[con[0]][0]][1] > self.points[self.connections[con[0]][1]][1]:
                # Проверка, достиг ли x конечной точки, что бы еще раз не переворачивать координаты
                if new_x != self.points[self.connections[con[0]][1]][0] or \
                                new_y != self.points[self.connections[con[0]][1]][1]:
                    new_x = self.points[self.connections[con[0]][0]][0] - new_x
                    new_x = self.points[self.connections[con[0]][0]][0] + new_x
                    new_y = self.points[self.connections[con[0]][0]][1] - new_y
                    new_y = self.points[self.connections[con[0]][0]][1] + new_y

            qp.drawLine(self.points[self.connections[con[0]][0]][0], self.points[self.connections[con[0]][0]][1], new_x,
                        new_y)

            # Проверяем, есть ли соединения достигнутой точки с другими ребрами, если есть, добавляем их в ребра прохода
            # Удаляем пройденное ребро из массива ребер прохода и добавляем его в массив пройденых ребер
            con_index = self.painting_connections.index(con)
            if con[1] is True:
                for i in self.connections:
                    if self.connections[con[0]][1] == i[0]:
                        self.painting_connections.append([self.connections.index(i), self.speed])
                self.painting_connections.pop(con_index)
                self.cur_map.append(self.connections[con[0]])

        if not self.painting_connections:
            print('paintiong finish')
            self.timer.stop()


        pen = QPen(Qt.green, 6)
        qp.setPen(pen)

    def timerEvent(self, event):
        self.iterat += 1
        self.update()

    # Функция выведена из уравнения длинны в прямоугольном треугольнике и уравнения прямой по двум точкам
    def calculate_next_point(self, first_x, first_y, fin_x, fin_y, length):
        # Проверяем будет ли следующий шаг увеличения длинны больше длинны ребра и если будет возвращаем последнюю точку
        if length > self.gip_len(first_x, first_y, fin_x, fin_y):
            return fin_x, fin_y, True

        # Костыль при y = const
        # ошибка возникает из-за того, что в выведенном уравнении при расчете new_x делитель = 0
        if first_y == fin_y:
            if first_x > fin_x:
                return first_x - length, first_y, length + self.speed
            else:
                return first_x + length, first_y, length + self.speed

        # Функция рассчета следующей точки на прямой при известной первой и последней точки и длинны от первой точки
        numerator = length ** 2 * (fin_y - first_y) ** 2
        denominator = (fin_x - first_x) ** 2 + (fin_y - first_y) ** 2
        new_y = math.sqrt(numerator / denominator) + first_y
        new_x = (((new_y - first_y) / (fin_y - first_y)) * (fin_x - first_x)) + first_x
        return new_x, new_y, length + self.speed

    # Рассчет длинны гипотенузы
    def gip_len(self, first_x, first_y, fin_x, fin_y):
        gip = math.sqrt((first_x - fin_x) ** 2 + (first_y - fin_y) ** 2)
        return gip

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = SearchingMap()
    sys.exit(app.exec_())