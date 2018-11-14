import sys, math

import json

from PyQt5.QtCore import QBasicTimer, pyqtSignal, Qt, QPoint
from PyQt5.QtWidgets import (QMainWindow, QApplication, QWidget, QDesktopWidget, QLabel, QFrame, QLineEdit,
                             QHBoxLayout, QVBoxLayout, QPushButton, QAction)
from PyQt5.QtGui import QCursor, QPainter, QPen, QColor, QIcon


class MainWidget(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initMain()

    def initMain(self):
        my_widget = RobotWidget(self)
        self.setCentralWidget(my_widget)

        self.statusbar = self.statusBar()
        my_widget.msg2Statusbar[str].connect(self.statusbar.showMessage)

        self.setWindowIcon(QIcon('ico.png'))
        self.setWindowTitle('SLAM algorithm')
        self.resize(500, 500)
        self.center()
        self.show()

    def action_built(self):
        action = QAction(QIcon('exit.png'), "Clak", self)
        action.triggered.connect(self.test)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


class RobotWidget(QWidget):
    msg2Statusbar = pyqtSignal(str)

    def __init__(self, parent):
        super().__init__(parent)
        self.maps_window = False

        self.initWorkArea()

    def initWorkArea(self):
        #self.is_paused = False

        self.visual_widget = SetGraphWidget(self)
        left_frame, self.save_name, self.load_name, self.robot_value, self.speed_value = self.initMenuWidget()

        hbox = QHBoxLayout(self)

        hbox.addWidget(self.visual_widget)
        hbox.addWidget(left_frame)
        self.setLayout(hbox)

        # Set focus on map window
        self.visual_widget.setFocus()

    def initMenuWidget(self):
        widget = QWidget()
        widget.setFixedSize(200, 500)

        void_label = QLabel()

        speed_edit = QLineEdit()
        speed_edit.setPlaceholderText("Enter speed value")

        save_name = QLineEdit()
        save_name.setPlaceholderText("Enter file name for save")

        load_name = QLineEdit()
        load_name.setPlaceholderText("Enter file name for load")

        robot_field = QLineEdit()
        robot_field.setPlaceholderText("Enter number of robots")

        pause_button = QPushButton("Pause")
        # pause_button.clicked.connect(self.pause)

        start_button = QPushButton("Start")
        start_button.clicked.connect(self.start)

        edge_button = QPushButton("Remove edge")
        edge_button.clicked.connect(self.visual_widget.clearEdge)

        refresh_button = QPushButton("Clear map")
        refresh_button.clicked.connect(self.visual_widget.refresh)

        save_button = QPushButton("Save map to file")
        save_button.clicked.connect(self.saveToFile)

        load_button = QPushButton("Load map from file")
        load_button.clicked.connect(self.loadFromFile)

        vbox = QVBoxLayout()
        vbox.setDirection(3)

        vbox.addWidget(load_name)
        vbox.addWidget(load_button)
        vbox.addWidget(save_name)
        vbox.addWidget(save_button)
        vbox.addWidget(void_label)
        vbox.addWidget(robot_field)
        vbox.addWidget(speed_edit)
        vbox.addWidget(pause_button)
        vbox.addWidget(start_button)
        vbox.addWidget(edge_button)
        vbox.addWidget(refresh_button)
        widget.setLayout(vbox)
        return widget, save_name, load_name, robot_field, speed_edit

    def saveToFile(self):
        print(self.visual_widget.connections)
        print(self.visual_widget.point_arr)
        decoded_conncections = [((x[0].x(), x[0].y()), (x[1].x(), x[1].y())) for x in self.visual_widget.connections]
        decoded_point_array = [(x.x(), x.y()) for x in self.visual_widget.point_arr]

        connections_dumb = json.dumps(decoded_conncections)
        point_dumb = json.dumps(decoded_point_array)

        with open(self.save_name.text() + '.json', 'w') as outfile:
            json.dump((decoded_conncections, decoded_point_array), outfile)

        self.msg2Statusbar.emit("File successfully saved")

    def loadFromFile(self):
        if not self.load_name.text():
            self.msg2Statusbar.emit("Please enter the file name to load configurations")
            return
        with open(self.load_name.text() + '.json', 'r') as infile:
            connections, points = json.load(infile)

        self.visual_widget.connections = [(QPoint(x[0][0], x[0][1]), QPoint(x[1][0], x[1][1])) for x in connections]
        self.visual_widget.point_arr = [QPoint(x[0], x[1]) for x in points]

        self.visual_widget.update()
        self.msg2Statusbar.emit("Configuration loaded successfully")

    def start(self):
        if not self.maps_window:
            self.active_widget = MapCreating(self)
            self.active_widget.real_map.initMap(self.visual_widget.connections, self.visual_widget.point_arr)
            self.active_widget.searching_map.initStartOptions(self.visual_widget.connections,
                                                              self.visual_widget.point_arr,
                                                              self.robot_value.text(),
                                                              self.speed_value.text())
            self.active_widget.show()

    def pause(self):
        self.is_paused = not self.is_paused

        if self.is_paused:
            self.visual_widget.timer.stop()
        else:
            self.visual_widget.timer.start(self.visual_widget.speed, self.visual_widget)

        self.visual_widget.update()


class SetGraphWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.initUI()

    def initUI(self):
        self.curs = QCursor()

        self.connections = []
        self.point_arr = []
        self.iterator = 0
        self.cur_point = None
        self.first_point = None

        self.setFixedSize(500, 500)

    def paintEvent(self, event):
        qp = QPainter(self)
        self.drawRect(qp)

    def drawRect(self, qp):
        line_pen = QPen(Qt.black, 2)
        dot_pen = QPen(Qt.blue, 6)
        qp.setPen(line_pen)

        for x in self.connections:
            qp.drawLine(x[0], x[1])

        # if len(self.point_arr) > 1:
        for x in self.point_arr:
            qp.setPen(dot_pen)
            qp.drawPoint(x)

    def mousePressEvent(self, event):
        cur_point = QPoint(self.curs.pos())
        cur_point = self.mapFromGlobal(cur_point)

        if self.first_point is None:
            if self.iterator == 0:
                self.first_point = cur_point
                self.point_arr.append(cur_point)
            else:
                self.pointCircle(cur_point)
        else:
            self.point_arr.append(cur_point)
            self.connections.append((self.first_point, cur_point))
            self.first_point = None

        self.iterator += 1
        self.update()

    def keyPressEvent(self, event):
        key = event.key()
        print(key)

        if key == Qt.Key_R:
            print(1)
            self.refresh()
        elif key == Qt.Key_X:
            print(2)
            self.clearEdge()

    # Completely removes the entire card to fill again
    def refresh(self):
        self.connections.clear()
        self.point_arr.clear()
        self.iterator = 0
        self.setFocus()
        self.update()

    # Removes one edge of a map graph.
    def clearEdge(self):
        if len(self.point_arr) > 1:
            if self.first_point == None:
                self.connections.pop()
                self.point_arr.pop()

        self.setFocus()
        self.update()

    def pointCircle(self, cur_point):
        radius = 20
        right_point = []

        for x in self.point_arr:
            circle_value = self.circleValue(int(cur_point.x()), int(cur_point.y()), int(x.x()), int(x.y()))
            if circle_value <= radius ** 2:
                right_point.append(x)
                self.first_point = x
            # if len(right_point) <= 0:
            #    raise TypeError("Point is not found")

        min_point = 21
        for x in right_point:
            circle_value = self.circleValue(int(cur_point.x()), int(cur_point.y()), int(x.x()), int(x.y()))
            if circle_value < min_point:
                self.first_point = x
                min_point = circle_value

    #Returns the distance from the center of the circle to the point.
    def circleValue(self, x0, y0, x, y):
        return (x - x0) ** 2 + (y - y0) ** 2


class MapCreating(QWidget):
    def __init__(self, parent):
        super().__init__(parent, Qt.Window)

        self.searchBuild()

    def searchBuild(self):
        self.searching_map = SearchingMap(self)
        self.real_map = RealMap(self)

        hbox = QHBoxLayout()

        hbox.addWidget(self.searching_map)
        hbox.addWidget(self.real_map)

        self.setGeometry(200, 200, 1100, 600)
        self.setLayout(hbox)


class RealMap(QFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.build_real_map()

    def build_real_map(self):
        self.setStyleSheet("border:3px solid rgb(0, 0, 0);")

    def initMap(self, connections, points):
        self.connections, self.points = connections, points

    def paintEvent(self, event):
        qp = QPainter(self)
        self.drawRealMap(qp)

    def drawRealMap(self, qp):
        line_pen = QPen(Qt.black, 2)
        dot_pen = QPen(Qt.blue, 6)
        qp.setPen(line_pen)
        for x in self.connections:
            qp.drawLine(x[0], x[1])
        for x in self.points:
            qp.setPen(dot_pen)
            qp.drawPoint(x)


class SearchingMap(QFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.build_searching_map()

    def build_searching_map(self):
        self.timer = QBasicTimer()
        self.iterator = 0

        self.setStyleSheet("border:3px solid rgb(0, 0, 0);")

    def initStartOptions(self, connections, points, robot_value, speed):
        self.robot_value = robot_value
        self.speed = speed
        self.known_connections = connections
        self.known_point = points

    def paintEvent(self, event):
        qp = QPainter(self)
        self.drawSearchingMap(qp)

    def drawSearchingMap(self, qp):
        pen = QPen(Qt.darkMagenta, 6)
        qp.setPen(pen)
        if self.iterator == 0:
            qp.drawPoint(self.known_point[0])


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWidget()
    sys.exit(app.exec_())