import sys, math

from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPen, QPainter, QColor
from PyQt5.QtCore import Qt, QPoint, QBasicTimer


class MainWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.initMain()

    def initMain(self):
        self.timer = QBasicTimer()
        self.timer.start(20, self)
        self.iterat = 0

        #self.points = [(50, 500), (50, 200), (400, 500), (50, 700)]
        #self.connections = [(2, 0), (0, 2), (0, 3)]
        #self.points = [(50, 500), (50, 200), (400, 300), (250, 500), (150, 800)]
        #self.connections = [(0, 1), (1, 2), (1, 3), (0, 4)]
        self.points = [(500, 500), (500, 200), (800, 500), (500, 800), (200, 500), (800, 200), (800, 800), (200, 800), (200, 200)]
        self.connections = [(0, 1), (0, 2), (0, 3), (0, 4), (1, 5), (2, 6), (3, 7), (4, 8)]
        self.speed = 5
        self.painting_connections = [[0, self.speed],
                                     [1, self.speed],
                                     [2, self.speed],
                                     [3, self.speed]]
        self.cur_map = []

        self.setGeometry(300, 100, 1000, 1000)
        self.setWindowTitle('Triangle paint')
        self.show()

    def paintEvent(self, event):
        qp = QPainter(self)
        self.painttt(qp)

    def painttt(self, qp):
        pen = QPen(Qt.blue, 3)
        qp.setPen(pen)
        self.init_map_con(qp)

        pen = QPen(Qt.green, 8)
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

    def init_map_con(self, qp):
        for x in self.connections:
            qp.drawLine(QPoint(self.points[x[0]][0], self.points[x[0]][1]),
                        QPoint(self.points[x[1]][0], self.points[x[1]][1]))

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
    ex = MainWidget()
    sys.exit(app.exec_())