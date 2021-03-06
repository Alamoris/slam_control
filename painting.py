import sys, math

from PyQt5.QtWidgets import QWidget, QApplication, QFrame, QVBoxLayout, QHBoxLayout, QLabel
from PyQt5.QtGui import QPen, QPainter, QColor
from PyQt5.QtCore import Qt, QPoint, QBasicTimer

from my_modules import gip_len


class SearchingMap(QFrame):
    def __init__(self, parent, progress_bars):
        self.parent = parent
        super().__init__(parent)

        self.progress_bars = progress_bars
        self.initMain()

    def initMain(self):

        self.timer = QBasicTimer()
        self.iterat = 0
        self.setStyleSheet("border:3px solid rgb(0, 0, 0);")

    def initStartOptions(self, connections, points, speed, brains):
        if not speed:
            # TODO: При релизе поставить в 20
            speed = 10
        self.timer.start(int(speed), self)
        self.connections = connections
        self.points = points
        self.points = [(point.x(), point.y()) for point in self.points.copy()]
        self.painting_connections = []
        self.cur_map = []
        self.speed = 1
        self.slam_brain = brains

        self.takeStartConnections()

    def takeStartConnections(self):
        for con in self.connections:
            if con[0] == 0:
                self.painting_connections.append([self.connections.index(con), self.speed])

    def paintEvent(self, event):
        qp = QPainter(self)

        self.painttt(qp)

    def painttt(self, qp):
        self.print_passed_connections(qp)

        col = QColor(0, 255, 255)
        robot_rect_pen = QPen(QColor(0, 0, 0))

        i = 0
        for robot in self.slam_brain.robots:
            pen = QPen(Qt.green, 5)
            qp.setPen(pen)
            x1, y1, x2, y2 = self.slam_brain.moveToNextStep(robot)

            if x1 is True and x2 is True:
                self.print_passed_connections(qp)
                self.timer.stop()

                result_info = ShowResulInfo(self, self.progress_bars)
                result_info.show()

            qp.drawLine(QPoint(x1, y1), QPoint(x2, y2))

            qp.setPen(robot_rect_pen)
            qp.setBrush(col)
            qp.drawRect(x2 - 5, y2 - 5, 12, 12)

            qp.setPen(QPen(QColor(0, 0, 0)))
            qp.drawText(x2 - 2, y2 + 6, '{0}'.format(i))

            i += 1

    def print_passed_connections(self, qp):
        pen = QPen(Qt.black, 2)
        qp.setPen(pen)

        for con in self.slam_brain.passed_connections:
            drowen_point = []
            qp.drawLine(self.points[con[0]][0], self.points[con[0]][1],
                        self.points[con[1]][0], self.points[con[1]][1])

            # TODO: Если делать нормально, то в мозгах нужно сделать массив с пройденными точками
            # тестовый модуль позволяющий рисовать номера соединений на них
            for x in con:
                    drowen_point.append(x)
                    qp.drawText(self.points[x][0] + 10, self.points[x][1] - 10, "{0}".format(x))

    def timerEvent(self, event):
        for i in range(len(self.slam_brain.robots)):
            self.progress_bars[i].incrementValue()
            self.progress_bars[len(self.progress_bars) - 2].incrementValue()

        self.progress_bars[len(self.progress_bars) - 1].incrementValue()
        self.iterat += 1
        self.update()



class ShowResulInfo(QWidget):
    def __init__(self, parent, progress_bars):
        super().__init__(parent, Qt.Window)

        self.progress_bars = progress_bars
        self.buildInfo()

    def buildInfo(self):
        self.setGeometry(500, 500, 500, 500)

        main_vbox = QVBoxLayout()
        hbox = QHBoxLayout()

        for num in range(len(self.progress_bars) - 2):
            vbox = QVBoxLayout()
            vbox.addWidget(QLabel('Path of {0} robot'.format(num)))
            vbox.addWidget(self.progress_bars[num])

            hbox.addLayout(vbox)

        main_vbox.addLayout(hbox)
        hbox = QHBoxLayout()
        vbox = QVBoxLayout()
        vbox.addWidget(QLabel('Total way length'))
        vbox.addWidget(self.progress_bars[len(self.progress_bars) - 2])
        hbox.addLayout(vbox)

        vbox = QVBoxLayout()
        vbox.addWidget(QLabel('The number of cycles'))
        vbox.addWidget(self.progress_bars[len(self.progress_bars) - 1])
        hbox.addLayout(vbox)

        main_vbox.addLayout(hbox)
        self.setLayout(main_vbox)

